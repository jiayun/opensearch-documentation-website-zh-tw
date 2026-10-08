---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "鄰接矩陣"
parent: Bucket aggregations
nav_order: 10
redirect_from:
  - /query-dsl/aggregations/bucket/adjacency-matrix/
---

# 鄰接矩陣彙總

`adjacency_matrix` 彙總接受一組具名的篩選條件運算式，並傳回代表每一對相交篩選條件的桶 (bucket)。每個桶的文件計數表示有多少文件同時符合兩個篩選條件，讓您能夠分析不同文件群組之間的關係。

假設有三個分別名為 `A`、`B` 和 `C` 的篩選條件，回應會產生下列桶結構：

|   | `A` | `B` | `C` |
| :--- | :--- | :--- | :--- |
| `A` | `A` | `A&B` | `A&C` |
| `B` |  | `B` | `B&C` |
| `C` |  |  | `C` |

此矩陣是對稱的（桶 `A&C` 包含的文件與 `C&A` 相同），因此只會傳回上三角部分。篩選條件名稱會依字母順序排序，排在前面的名稱一律出現在 `&` 分隔符號的左側。

## 參數

`adjacency_matrix` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `filters` | 必要 | 物件 | 以鍵值組表示的一組具名篩選條件。每個鍵是篩選條件名稱，每個值是一個查詢物件。 |
| `separator` | 選用 | 字串 | 在相交桶的鍵中用來連接篩選條件名稱的字元。預設為 `&`。 |

## 範例

下列範例分析電子商務資料集，以判斷三家製造商的產品出現在同一筆訂單中的頻率：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "interactions": {
      "adjacency_matrix": {
        "filters": {
          "grpA": {
            "match": {
              "manufacturer.keyword": "Low Tide Media"
            }
          },
          "grpB": {
            "match": {
              "manufacturer.keyword": "Elitelligence"
            }
          },
          "grpC": {
            "match": {
              "manufacturer.keyword": "Oceanavigations"
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "took": 32,
  "timed_out": false,
  "terminated_early": true,
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
    "interactions": {
      "buckets": [
        {
          "key": "grpA",
          "doc_count": 1553
        },
        {
          "key": "grpA&grpB",
          "doc_count": 590
        },
        {
          "key": "grpA&grpC",
          "doc_count": 329
        },
        {
          "key": "grpB",
          "doc_count": 1370
        },
        {
          "key": "grpB&grpC",
          "doc_count": 299
        },
        {
          "key": "grpC",
          "doc_count": 1218
        }
      ]
    }
  }
}
```

`doc_count` 為 `590` 的相交桶 `grpA&grpB` 表示有 590 筆訂單同時包含 Low Tide Media 和 Elitelligence 的產品。

## 搭配子彙總使用

在 `adjacency_matrix` 內巢狀使用 `date_histogram` 等子彙總，可為關係資料加入時間維度，進而實現動態網路分析，讓您觀察群組之間的互動如何隨時間演變。

符合文件數為零的相交桶會從回應中省略。
{: .note}

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `buckets` | 陣列 | 代表個別篩選條件及其兩兩相交結果的桶清單。 |
| `buckets.key` | 字串 | 個別篩選條件桶的篩選條件名稱，或相交桶中以分隔符號連接的兩個篩選條件名稱。 |
| `buckets.doc_count` | 整數 | 符合該篩選條件或篩選條件組合的文件數。 |

## 限制

桶的數量會隨篩選條件數量呈平方成長。對於 `N` 個篩選條件，最多會產生 `N(N+1)/2` 個桶（`N` 個個別桶加上 `N*(N-1)/2` 個相交桶）。為避免使用過多記憶體，篩選條件數量上限預設為 `100`。您可以使用 `index.max_adjacency_matrix_filters` 設定，針對每個索引調整此限制。

## 相關文件

- 如需在 OpenSearch Dashboards 中將鄰接矩陣結果呈現為網路圖的完整範例，請參閱[建立 Vega 視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/vega/#creating-a-vega-visualization)。