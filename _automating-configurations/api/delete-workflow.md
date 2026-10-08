---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除工作流程"
parent: Workflow APIs
nav_order: 80
---

# Delete Workflow API

當您不再需要某個工作流程範本時，可以呼叫 Delete Workflow API 將其刪除。

請注意，刪除工作流程只會刪除已儲存的範本，不會取消佈建其資源。

刪除工作流程時，其對應的狀態（由 [Workflow State API]({{site.url}}{{site.baseurl}}/automating-configurations/api/get-workflow-status/) 傳回）也會一併刪除，除非佈建狀態為 `IN_PROGRESS` 或已佈建資源。

## 端點

```json
DELETE /_plugins/_flow_framework/workflow/{workflow_id}
``` 

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `workflow_id` | String | 要擷取的工作流程 ID。必要。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `clear_status` | Boolean | 決定在刪除範本後，是否刪除工作流程狀態（不取消佈建資源）。只有在佈建狀態不是 `IN_PROGRESS` 時，OpenSearch 才會刪除工作流程狀態。預設為 `false`。 |

## 請求範例

```json
DELETE /_plugins/_flow_framework/workflow/8xL8bowB8y25Tqfenm50
```
{% include copy-curl.html %}

```json
DELETE /_plugins/_flow_framework/workflow/8xL8bowB8y25Tqfenm50?clear_status=true
```
{% include copy-curl.html %}

## 回應範例

如果工作流程存在，刪除回應會包含刪除的狀態。成功時，`result` 欄位會設為 `deleted`；如果工作流程不存在（可能已經被刪除），則會設為 `not_found`：

```json
{
  "_index": ".plugins-flow_framework-templates",
  "_id": "8xL8bowB8y25Tqfenm50",
  "_version": 2,
  "result": "deleted",
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 2,
  "_primary_term": 1
}
```
