---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取消佈建工作流程"
parent: Workflow APIs
nav_order: 70
---

# Deprovision Workflow API

當您不再需要某個工作流程時，可以取消佈建其資源。大多數建立資源的工作流程步驟都有對應的工作流程步驟，可復原該動作。若要擷取目前為某個工作流程建立的所有資源，請呼叫 [Get Workflow Status API]({{site.url}}{{site.baseurl}}/automating-configurations/api/get-workflow-status/)。當您呼叫 Deprovision Workflow API 時，系統會使用與佈建步驟對應的工作流程步驟，移除 Get Workflow Status API 回應中 `resources_created` 欄位所包含的資源。

工作流程會以相反順序執行佈建步驟。如果因資源相依性而發生失敗，例如嘗試刪除仍處於部署狀態的已註冊模型，只要至少有一個資源已被刪除，工作流程就會重試失敗的步驟。

為防止資料遺失，使用 `create_index`、`create_search_pipeline` 和 `create_ingest_pipeline` 步驟建立的資源，必須將其資源 ID 納入 `allow_delete` 參數。

## 端點

```json
POST /_plugins/_flow_framework/workflow/{workflow_id}/_deprovision
``` 

## 路徑參數

下表列出可用的路徑參數。 

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `workflow_id` | 字串 | 要取消佈建的工作流程 ID。必要。 |
| `allow-delete` | 字串 | 以逗號分隔的資源 ID 清單，列出要取消佈建的資源。刪除類型為 `index_name` 或 `pipeline_id` 的資源時為必要。 |

### 請求範例

```json
POST /_plugins/_flow_framework/workflow/8xL8bowB8y25Tqfenm50/_deprovision
``` 
{% include copy-curl.html %}

### 回應範例

如果取消佈建成功，OpenSearch 會回傳與請求中使用的相同 `workflow_id`： 

```json
{
  "workflow_id" : "8xL8bowB8y25Tqfenm50"
}
```

如果取消佈建未完全移除所有資源，OpenSearch 會回傳 `202 (ACCEPTED)` 狀態，並指出未取消佈建的資源：

```json
{
    "error": "Failed to deprovision some resources: [connector_id Lw7PX4wBfVtHp98y06wV]."
}
```

在某些情況下，失敗是因為移除另一個相依資源需要一些時間。在這種情況下，您可以嘗試再次傳送相同的請求。
{: .tip}

如果取消佈建需要 `allow_delete` 參數，OpenSearch 會回傳 `403 (FORBIDDEN)` 狀態，並指出未取消佈建的資源：

```json
{
    "error": "These resources require the allow_delete parameter to deprovision: [index_name my-index]."
}
```

若要取得比錯誤回應摘要更詳細的取消佈建狀態，請查詢 [Get Workflow Status API]({{site.url}}{{site.baseurl}}/automating-configurations/api/get-workflow-status/)。 

成功時，工作流程會回到 `NOT_STARTED` 狀態。如果某些資源尚未移除，回應中會列出這些資源。