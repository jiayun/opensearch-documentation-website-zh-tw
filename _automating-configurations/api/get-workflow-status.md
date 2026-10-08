---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得工作流程狀態"
parent: Workflow APIs
nav_order: 40
---

# Get Workflow Status API

[佈建工作流程]({{site.url}}{{site.baseurl}}/automating-configurations/api/provision-workflow/)可能需要相當長的時間，尤其是當此動作涉及 OpenSearch 編製索引作業時。Get Workflow State API 可讓您監視佈建部署狀態，直到部署完成。

## 端點

```json
GET /_plugins/_flow_framework/workflow/{workflow_id}/_status
``` 

## 路徑參數

下表列出可用的路徑參數。 

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `workflow_id` | 字串 | 要取得狀態的工作流程 ID。`PUT` 方法的必要參數。 |

## 查詢參數

`all` 參數指定回應是否應傳回所有欄位。 

設為 `false`（預設值）時，回應包含下列欄位：

- `workflow_id`
- 任何 `error` 狀態
- `state`
- `resources_created` 清單

設為 `true` 時，回應包含下列額外欄位：

- `provisioning_progress`
- `provision_start_time`
- `provision_end_time`
- `user`
- `user_outputs`

若要在回應中取得所有可用欄位，請將 `all` 設為 `true`：

```json
GET /_plugins/_flow_framework/workflow/8xL8bowB8y25Tqfenm50/_status?all=true
``` 
{% include copy-curl.html %}

## 請求範例

```json
GET /_plugins/_flow_framework/workflow/8xL8bowB8y25Tqfenm50/_status
```
{% include copy-curl.html %}


## 回應範例

OpenSearch 會回應佈建狀態摘要和已建立的資源清單。 

在佈建開始之前，OpenSearch 不會傳回任何資源：

```json
{
  "workflow_id" : "8xL8bowB8y25Tqfenm50",
  "state": "NOT_STARTED"
}
```

佈建進行期間，OpenSearch 會傳回部分資源清單：

```json
{
  "workflow_id" : "8xL8bowB8y25Tqfenm50",
  "state": "PROVISIONING",
  "resources_created": [
    {
      "workflow_step_name": "create_connector",
      "workflow_step_id": "create_connector_1",
      "resource_type": "connector_id",
      "resource_id": "NdjCQYwBLmvn802B0IwE"
    }
  ]
}
```

佈建完成後，OpenSearch 會傳回完整的資源清單：

```json
{
  "workflow_id" : "8xL8bowB8y25Tqfenm50",
  "state": "COMPLETED",
  "resources_created": [
    {
      "workflow_step_name": "create_connector",
      "workflow_step_id": "create_connector_1",
      "resource_type": "connector_id",
      "resource_id": "NdjCQYwBLmvn802B0IwE"
    },
    {
      "workflow_step_name": "register_remote_model",
      "workflow_step_id": "register_model_2",
      "resource_type": "model_id",
      "resource_id": "N9jCQYwBLmvn802B0oyh"
    }
  ]
}
```