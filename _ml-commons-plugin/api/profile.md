---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行概況"
parent: ML APIs
nav_order: 110
---

# ML Profile API

Profile API 會傳回機器學習 (ML) 任務與模型的執行階段資訊。您可以使用它來在執行階段偵錯模型問題。

## 傳回的請求數量

預設情況下，Profile API 會監控最近 100 個請求。若要變更監控的請求數量，請更新下列叢集設定：

```json
PUT _cluster/settings
{
  "persistent" : {
    "plugins.ml_commons.monitoring_request_count" : 1000000 
  }
}
```
{% include copy-curl.html %}

若要清除所有監控的請求，請將 `plugins.ml_commons.monitoring_request_count` 設定為 `0`。 

## 端點

```json
GET /_plugins/_ml/profile
GET /_plugins/_ml/profile/models
GET /_plugins/_ml/profile/models/{model_id}
GET /_plugins/_ml/profile/tasks
GET /_plugins/_ml/profile/tasks/{task_id}
```

## 路徑參數

參數 | 資料類型 | 說明
:--- | :--- | :---
`model_id` | 字串 | 傳回特定模型的執行階段資料。您可以提供多個以逗號分隔的模型 ID，以擷取多個模型執行概況。
`task_id`| 字串 | 傳回特定任務的執行階段資料。您可以提供多個以逗號分隔的任務 ID，以擷取多個任務執行概況。

### 請求本文欄位

所有執行概況請求本文欄位皆為選用。

欄位 | 資料類型 | 說明
:--- | :--- | :--- 
`node_ids` | 陣列 | 傳回指定節點的所有任務與執行概況。 
`model_ids` | 陣列 | 傳回指定模型的執行階段資料。
`task_ids` | 陣列 | 傳回指定任務的執行階段資料。
`return_all_tasks` | 布林值 | 決定請求是否傳回所有任務。設為 `false` 時，回應中會省略任務執行概況。
`return_all_models` | 布林值 | 決定執行概況請求是否傳回所有模型。設為 `false` 時，回應中會省略模型執行概況。

## 範例請求：傳回特定節點上的所有任務與模型

```json
GET /_plugins/_ml/profile
{
  "node_ids": ["KzONM8c8T4Od-NoUANQNGg"],
  "return_all_tasks": true,
  "return_all_models": true
}
```
{% include copy-curl.html %}

## 回應範例 

```json
{
  "nodes" : {
    "qTduw0FJTrmGrqMrxH0dcA" : { # node id
      "models" : {
        "WWQI44MBbzI2oUKAvNUt" : { # model id
          "worker_nodes" : [ # routing table
            "KzONM8c8T4Od-NoUANQNGg"
          ]
        }
      }
    },
    ...
    "KzONM8c8T4Od-NoUANQNGg" : { # node id
      "models" : {
        "WWQI44MBbzI2oUKAvNUt" : { # model id
          "model_state" : "DEPLOYED", # model status
          "predictor" : "org.opensearch.ml.engine.algorithms.text_embedding.TextEmbeddingDenseModel@592814c9",
          "target_worker_nodes" : [ # nodes planned for deployment
            "KzONM8c8T4Od-NoUANQNGg"
          ],
          "worker_nodes" : [ # routing table
            "KzONM8c8T4Od-NoUANQNGg"
          ],
          "model_inference_stats" : { # model inference latency on this node
            "count" : 2,
            "max" : 88.827301,
            "min" : 4.251,
            "average" : 46.5391505,
            "p50" : 46.5391505,
            "p90" : 80.3683304,
            "p99" : 87.98140399
          },
          "predict_request_stats" : { # predict request stats on this node
            "count" : 2, # total predict requests on this node
            "max" : 89.978681, # max latency in milliseconds
            "min" : 5.402,
            "average" : 47.6903405,
            "p50" : 47.6903405,
            "p90" : 81.5210129,
            "p99" : 89.13291418999998
          }
        }
      }
    },
    ...
  }
}
```
