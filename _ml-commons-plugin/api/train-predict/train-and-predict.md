---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "訓練與預測"
parent: Model APIs
grand_parent: ML APIs
nav_order: 75
---

# 訓練與預測 API

用於訓練並立即針對相同的訓練資料集進行預測。僅能搭配非監督式學習模型使用。下表列出支援的演算法，以及要在 `algorithm` 路徑參數中指定的值。

| 演算法 | `algorithm` 值 |
| :--- | :--- |
| [Batch RCF]({{site.url}}{{site.baseurl}}/ml-commons-plugin/algorithms/#batch-rcf) | `batch_rcf` |
| [Fixed in time (FIT) RCF]({{site.url}}{{site.baseurl}}/ml-commons-plugin/algorithms/#fit-rcf) | `fit_rcf` |
| [k-means]({{site.url}}{{site.baseurl}}/ml-commons-plugin/algorithms/#k-means) | `kmeans` |
| [RCF Summarize]({{site.url}}{{site.baseurl}}/ml-commons-plugin/algorithms/#rcf-summarize) | `rcf_summarize` |

## 端點

```json
POST /_plugins/_ml/_train_predict/{algorithm}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `algorithm` | 字串 | 演算法的名稱，例如 `kmeans`。名稱不區分大小寫。必要。 |

## 請求本文欄位

下表列出可用的請求本文欄位。請使用 `input_index` 與 `input_query` 或 `input_data` 來提供資料。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `parameters` | 物件 | 演算法的超參數。可用參數取決於演算法。各演算法的參數請參閱[支援的演算法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/algorithms/)。選用。 |
| `input_index` | 陣列 | 包含資料的索引清單。 |
| `input_query` | 物件 | 從 `input_index` 選取文件的搜尋查詢。 |
| `input_data` | 物件 | 直接以資料框形式提供的資料，包含 `column_metas` 與 `rows`。 |

## 範例請求：使用已編製索引的資料進行訓練與預測

```json
POST /_plugins/_ml/_train_predict/kmeans
{
    "parameters": {
        "centroids": 2,
        "iterations": 10,
        "distance_type": "COSINE"
    },
    "input_query": {
        "query": {
            "bool": {
                "filter": [
                    {
                        "range": {
                            "k1": {
                                "gte": 0
                            }
                        }
                    }
                ]
            }
        },
        "size": 10
    },
    "input_index": [
        "test_data"
    ]
}
```
{% include copy-curl.html %}

## 範例請求：直接使用資料進行訓練與預測

```json
POST /_plugins/_ml/_train_predict/kmeans
{
    "parameters": {
        "centroids": 2,
        "iterations": 1,
        "distance_type": "EUCLIDEAN"
    },
    "input_data": {
        "column_metas": [
            {
                "name": "k1",
                "column_type": "DOUBLE"
            },
            {
                "name": "k2",
                "column_type": "DOUBLE"
            }
        ],
        "rows": [
            {
                "values": [
                    {
                        "column_type": "DOUBLE",
                        "value": 1.00
                    },
                    {
                        "column_type": "DOUBLE",
                        "value": 2.00
                    }
                ]
            },
            {
                "values": [
                    {
                        "column_type": "DOUBLE",
                        "value": 1.00
                    },
                    {
                        "column_type": "DOUBLE",
                        "value": 4.00
                    }
                ]
            },
            {
                "values": [
                    {
                        "column_type": "DOUBLE",
                        "value": 1.00
                    },
                    {
                        "column_type": "DOUBLE",
                        "value": 0.00
                    }
                ]
            },
            {
                "values": [
                    {
                        "column_type": "DOUBLE",
                        "value": 10.00
                    },
                    {
                        "column_type": "DOUBLE",
                        "value": 2.00
                    }
                ]
            },
            {
                "values": [
                    {
                        "column_type": "DOUBLE",
                        "value": 10.00
                    },
                    {
                        "column_type": "DOUBLE",
                        "value": 4.00
                    }
                ]
            },
            {
                "values": [
                    {
                        "column_type": "DOUBLE",
                        "value": 10.00
                    },
                    {
                        "column_type": "DOUBLE",
                        "value": 0.00
                    }
                ]
            }
        ]
    }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "status" : "COMPLETED",
  "prediction_result" : {
    "column_metas" : [
      {
        "name" : "ClusterID",
        "column_type" : "INTEGER"
      }
    ],
    "rows" : [
      {
        "values" : [
          {
            "column_type" : "INTEGER",
            "value" : 1
          }
        ]
      },
      {
        "values" : [
          {
            "column_type" : "INTEGER",
            "value" : 1
          }
        ]
      },
      {
        "values" : [
          {
            "column_type" : "INTEGER",
            "value" : 1
          }
        ]
      },
      {
        "values" : [
          {
            "column_type" : "INTEGER",
            "value" : 0
          }
        ]
      },
      {
        "values" : [
          {
            "column_type" : "INTEGER",
            "value" : 0
          }
        ]
      },
      {
        "values" : [
          {
            "column_type" : "INTEGER",
            "value" : 0
          }
        ]
      }
    ]
  }
}
```