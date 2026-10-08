---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "多樣化取樣器"
parent: Bucket aggregations
nav_order: 40
redirect_from:
  - /query-dsl/aggregations/bucket/diversified-sampler/
---

# 多樣化取樣器彙總

`diversified_sampler` 彙總是一種篩選彙總，會將子彙總的處理範圍限制在分數最高的文件樣本中，同時確保樣本包含多樣化的內容。它擴充了 [`sampler` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/sampler/)，會對共用相同欄位值的文件進行重複資料刪除，以避免任何單一類別主導整個樣本。

當您需要確保不同群組都能獲得公平呈現時，此彙總非常實用，例如避免單一多產作者使分析結果產生偏差，或在以位置為基礎的分析中確保地理多樣性。它也能透過較小但更具代表性的樣本產生有用的結果，進而降低 `significant_terms` 等成本高昂的子彙總所需的運算成本。

## 參數

`diversified_sampler` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 選用 | 字串 | 用於重複資料刪除的欄位。每份文件必須只產生單一值。與 `script` 互斥。 |
| `script` | 選用 | 物件 | 產生重複資料刪除值的指令碼。與 `field` 互斥。 |
| `shard_size` | 選用 | 整數 | 每個分片上收集的分數最高文件數量上限。預設為 `100`。 |
| `max_docs_per_value` | 選用 | 整數 | 共用相同重複資料刪除值的文件可進入樣本的數量上限。預設為 `1`。 |
| `execution_hint` | 選用 | 字串 | 控制重複資料刪除值在記憶體中的管理方式。請參閱[執行提示](#execution-hint)。 |

### 執行提示

下表列出有效的 `execution_hint` 值。

| 值 | 說明 |
| :--- | :--- |
| `map` | 直接將欄位值保存在記憶體中。 |
| `global_ordinals` | 使用 Lucene 針對該欄位的序數對應，在高基數欄位上可提供更佳的記憶體效率。 |
| `bytes_hash` | 儲存每個值的雜湊而非值本身。在某些情境下可能提升速度，但有因雜湊衝突而導致重複資料刪除不正確的風險。 |

如果所選策略不適用於該欄位類型，OpenSearch 可能會忽略 `execution_hint`。
{: .note}


## 範例：依欄位進行重複資料刪除

下列範例從電子商務資料集中對訂單進行取樣，每個 `customer_gender` 值最多限制 50 份文件，接著對樣本執行 `terms` 子彙總以查看類別分布：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "my_sample": {
      "diversified_sampler": {
        "shard_size": 200,
        "field": "customer_gender",
        "max_docs_per_value": 50
      },
      "aggs": {
        "categories": {
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

## 範例：依指令碼進行重複資料刪除

當您需要依據計算或組合而成的欄位進行多樣化時，可以使用指令碼產生重複資料刪除值。下列範例使用指令碼依 `customer_gender` 進行多樣化，並將每個值限制為 3 份文件：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "my_sample": {
      "diversified_sampler": {
        "shard_size": 200,
        "max_docs_per_value": 3,
        "script": {
          "lang": "painless",
          "source": "doc['customer_gender'].value"
        }
      },
      "aggs": {
        "categories": {
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

## 範例回應

```json
{
  "took": 65,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "my_sample": {
      "doc_count": 6,
      "categories": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
          {
            "key": "Men's Clothing",
            "doc_count": 3
          },
          {
            "key": "Women's Clothing",
            "doc_count": 3
          },
          {
            "key": "Women's Shoes",
            "doc_count": 2
          },
          {
            "key": "Men's Accessories",
            "doc_count": 1
          }
        ]
      }
    }
  }
}
```

在 `max_docs_per_value` 設為 `3` 且有兩個不同性別值的情況下，樣本最多包含 6 份文件（每個值 3 份），確保子彙總結果中的呈現保持均衡。

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `doc_count` | 整數 | 多樣化樣本中的文件總數。 |

## 限制

- `field` 或 `script` 必須為每份文件產生單一值。不支援多值欄位，使用多值欄位會導致錯誤。
- 重複資料刪除會在每個分片上獨立套用，因此不同分片上具有相同值的文件不會彼此進行重複資料刪除。
- 此彙總無法巢狀置於使用 `breadth_first` 收集模式的 `terms` 彙總之下，因為廣度優先收集會捨棄多樣化取樣器所需的相關性分數。
- 地理或日期類型的多樣性值（例如 `"7d"` 或 `"10km"`）沒有專用語法。若要依地理區域或時間間隔進行多樣化，請撰寫將原始值分組為桶 (bucket) 的指令碼，例如使用 `(int)(doc['geoip.location'].lat / 10)` 劃分緯度帶，或使用 `doc['order_date'].value.dayOfWeek` 依星期幾分組。
