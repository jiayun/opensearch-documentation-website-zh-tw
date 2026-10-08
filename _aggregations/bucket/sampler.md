---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Sampler
parent: Bucket aggregations
nav_order: 170
redirect_from:
  - /query-dsl/aggregations/bucket/sampler/
---

# Sampler 彙總

`sampler` 彙總將子彙總的處理範圍限制在每個分片中得分最高的文件。這將焦點縮小到最相關的匹配項，而不是處理整個結果集，從而減少計算時間，並透過排除長尾中的低相關性文件來提高彙總結果的品質。

抽樣對於像 `significant_terms` 這樣的子彙總特別有用。如果沒有 sampler，完整的結果集將包含大量邊緣相關的文件，這些文件的通用詞元在數量上佔主導地位，掩蓋了在最高分匹配項中發現的真正具特徵的詞元。

關於防止單一欄位值主導樣本的多元化抽樣，請參閱 [`diversified_sampler` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/diversified-sampler/)。

## 參數

`sampler` 彙總使用以下參數。

| 參數 | 必要/選用 | 資料類型 | 描述 |
| :--- | :--- | :--- | :--- |
| `shard_size` | 選用 | 整數 | 從每個分片中收集的最高分文件的最大數量。預設值為 `100`。 |

## 範例

以下範例將樣本限制在每個分片 200 個最高分文件，然後執行 `terms` 子彙總，以找出該樣本中產品類別的分布情況：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "sample": {
      "sampler": {
        "shard_size": 200
      },
      "aggs": {
        "top_categories": {
          "terms": {
            "field": "category.keyword"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應顯示樣本包含 200 個文件，且 `terms` 子彙總僅對這 200 個文件進行操作，而非全部 4,675 個文件：

```json
{
  ...
  "aggregations": {
    "sample": {
      "doc_count": 200,
      "top_categories": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
          {
            "key": "Men's Clothing",
            "doc_count": 82
          },
          {
            "key": "Women's Clothing",
            "doc_count": 82
          },
          {
            "key": "Women's Shoes",
            "doc_count": 49
          },
          {
            "key": "Women's Accessories",
            "doc_count": 40
          },
          {
            "key": "Men's Shoes",
            "doc_count": 37
          },
          {
            "key": "Men's Accessories",
            "doc_count": 25
          }
        ]
      }
    }
  }
}
```

## 回應本文欄位

下表列出了回應本文的欄位。

| 欄位 | 資料類型 | 描述 |
| :--- | :--- | :--- |
| `doc_count` | 整數 | 所有分片中樣本文件的總數。 |

## 限制

`sampler` 彙總不能巢狀於使用 `breadth_first` 收集模式的 `terms` 彙總之下，因為廣度優先收集會捨棄 sampler 所需的相關性分數。
