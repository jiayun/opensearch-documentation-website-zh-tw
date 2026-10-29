---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "統計資料"
parent: ML APIs
nav_order: 120
---

# ML Stats API

Stats API 會傳回基本的機器學習 (ML) 統計資料，例如正在執行的任務數量。若要使用更詳細的時間序列指標來監控機器學習工作流程，請參閱[監控機器學習工作流程]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/telemetry/metrics/#monitoring-machine-learning-workflows)。
{: .note }

回應包含叢集層級的統計資料（例如 ML 索引狀態和模型數量），以及節點層級的統計資料（例如請求數量），並依演算法和模型細分。

## 端點

```json
GET /_plugins/_ml/stats
GET /_plugins/_ml/stats/{stat}
GET /_plugins/_ml/{nodeId}/stats/
GET /_plugins/_ml/{nodeId}/stats/{stat}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `nodeId` | 字串 | 以逗號分隔的節點 ID 清單，用於指定要傳回統計資料的節點。若省略，則傳回所有節點的統計資料。 |
| `stat` | 字串 | 以逗號分隔的統計資料清單，用於指定要傳回的統計資料。有效的叢集層級值為 `ml_model_index_status`、`ml_connector_index_status`、`ml_config_index_status`、`ml_task_index_status`、`ml_controller_index_status`、`ml_model_count` 和 `ml_connector_count`。有效的節點層級值為 `ml_jvm_heap_usage`、`ml_executing_task_count`、`ml_request_count`、`ml_failure_count`、`ml_deployed_model_count` 和 `ml_circuit_breaker_trigger_count`。 |

## 請求本文欄位

您也可以在請求本文中提供下列選用欄位，藉此篩選統計資料。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `target_stat_levels` | 陣列 | 要傳回的統計層級。有效值為 `cluster`、`node`、`algorithm`、`model` 和 `action`。 |
| `cluster_level_stats` | 陣列 | 要傳回的叢集層級統計資料。有效值請參閱 `stat` 路徑參數。 |
| `node_level_stats` | 陣列 | 要傳回的節點層級統計資料。有效值請參閱 `stat` 路徑參數。 |
| `action_level_stats` | 陣列 | 要傳回的動作層級統計資料。有效值為 `ml_action_request_count` 和 `ml_action_failure_count`。 |
| `node_ids` | 陣列 | 要傳回其統計資料的節點 ID。 |
| `algorithms` | 陣列 | 要傳回其統計資料的演算法，例如 `kmeans` 或 `text_embedding`。 |
| `models` | 陣列 | 要傳回其統計資料的模型 ID。 |
| `actions` | 陣列 | 要傳回其統計資料的動作。有效值為 `train`、`predict`、`train_predict`、`execute`、`register`、`deploy`、`undeploy` 和 `batch_predict`。 |

## 請求範例：取得所有節點的所有統計資料

```json
GET /_plugins/_ml/stats
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "ml_controller_index_status" : "non-existent",
  "ml_task_index_status" : "green",
  "ml_config_index_status" : "green",
  "ml_connector_index_status" : "green",
  "ml_model_count" : 13,
  "ml_connector_count" : 1,
  "ml_model_index_status" : "green",
  "nodes" : {
    "zbduvgCCSOeu6cfbQhTpnQ" : {
      "ml_jvm_heap_usage" : 77,
      "ml_failure_count" : 0,
      "ml_executing_task_count" : 0,
      "ml_request_count" : 69,
      "ml_circuit_breaker_trigger_count" : 0,
      "ml_deployed_model_count" : 3,
      "algorithms" : {
        "text_embedding" : {
          "predict" : {
            "ml_action_request_count" : 2
          },
          "deploy" : {
            "ml_action_request_count" : 3
          },
          "register" : {
            "ml_action_request_count" : 6
          }
        },
        "kmeans" : {
          "train" : {
            "ml_action_request_count" : 3
          }
        },
        ...
      },
      "models" : {
        "GtrMP6EBzLnYocCrLsvl" : {
          "predict" : {
            "ml_action_request_count" : 2
          },
          "deploy" : {
            "ml_action_request_count" : 2
          }
        },
        ...
      }
    }
  }
}
```

## 請求範例：取得特定節點的所有統計資料

```json
GET /_plugins/_ml/{nodeId}/stats/
```
{% include copy-curl.html %}

## 請求範例：取得特定節點的指定統計資料 

```json
GET /_plugins/_ml/{nodeId}/stats/{stat}
```
{% include copy-curl.html %}

## 請求範例：取得所有節點的指定統計資料

```json
GET /_plugins/_ml/stats/{stat}
```
{% include copy-curl.html %}

## 範例請求：使用請求本文篩選統計資料

```json
GET /_plugins/_ml/stats
{
  "target_stat_levels": ["node", "algorithm"],
  "node_level_stats": ["ml_request_count"],
  "algorithms": ["kmeans"],
  "actions": ["train"]
}
```
{% include copy-curl.html %}
