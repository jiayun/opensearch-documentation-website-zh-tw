---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "佈建工作流程"
parent: Workflow APIs
nav_order: 30
---

# Provision Workflow API

佈建工作流程是一次性的設定程序，通常由叢集管理員執行，用來建立終端使用者將使用的資源。  

`workflows` 範本欄位可以包含多個工作流程。具有 `provision` 鍵的工作流程可以使用此 API 執行。當呼叫 [Create or Update Workflow API]({{site.url}}{{site.baseurl}}/automating-configurations/api/create-workflow/) 並將 `provision` 參數設為 `true` 時，也會執行此 API。

只有在工作流程尚未佈建時，您才能佈建該工作流程。如果需要重新佈建，請先解除佈建該工作流程。
{: .note}

## 端點

```json
POST /_plugins/_flow_framework/workflow/{workflow_id}/_provision
```

## 路徑參數

下表列出可用的路徑參數。 

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `workflow_id` | String | 要佈建的工作流程 ID。必要。 |

## 查詢參數

如果您在範本中包含了替代運算式，可以將它作為查詢參數或請求本文欄位的字串值傳遞。例如，如果您在範本中將憑證欄位指定為 {% raw %}`openAI_key: '${{ openai_key }}'`{% endraw %}，則可以將 `openai_key` 參數作為查詢參數或本文欄位包含進來，以便在佈建期間進行替代。例如，下列請求提供了一個查詢參數：

```json
POST /_plugins/_flow_framework/workflow/{workflow_id}/_provision?{parameter}={value}
```

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| 使用者提供的替代運算式 | String | 符合範本中替代運算式的參數。選用。 |
| `wait_for_completion_timeout`          | TimeValue | 指定同步佈建的最長等待時間。如果超過逾時時間，請求會傳回目前的工作流程狀態，而執行會以非同步方式繼續。|

## 範例請求

```json
POST /_plugins/_flow_framework/workflow/8xL8bowB8y25Tqfenm50/_provision
```
{% include copy-curl.html %}

下列請求執行同步佈建呼叫，最多等待 2 秒以完成：

```json
POST /_plugins/_flow_framework/workflow/{workflow_id}/_provision?wait_for_completion_timeout=2s
```
{% include copy-curl.html %}

下列請求使用查詢參數將運算式 {% raw %}`${{ openai_key }}`{% endraw %} 替代為值 "12345"：

```json
POST /_plugins/_flow_framework/workflow/8xL8bowB8y25Tqfenm50/_provision?openai_key=12345
```
{% include copy-curl.html %}

下列請求使用請求本文將運算式 {% raw %}`${{ openai_key }}`{% endraw %} 替代為值 "12345"：

```json
POST /_plugins/_flow_framework/workflow/8xL8bowB8y25Tqfenm50/_provision
{
  "openai_key" : "12345"
}
```
{% include copy-curl.html %}

## 範例回應

OpenSearch 會以請求中使用的相同 `workflow_id` 回應：

```json
{
  "workflow_id" : "8xL8bowB8y25Tqfenm50"
}
```

若要取得佈建狀態，請呼叫 [Get Workflow State API]({{site.url}}{{site.baseurl}}/automating-configurations/api/get-workflow-status/)。

## 啟用 wait_for_completion_timeout 的範例回應

```json
{
    "workflow_id": "K13IR5QBEpCfUu_-AQdU",
    "state": "COMPLETED",
    "resources_created": [
        {
            "workflow_step_name": "create_connector",
            "workflow_step_id": "create_connector_1",
            "resource_id": "LF3IR5QBEpCfUu_-Awd_",
            "resource_type": "connector_id"
        },
        {
            "workflow_step_id": "register_model_2",
            "workflow_step_name": "register_remote_model",
            "resource_id": "L13IR5QBEpCfUu_-BQdI",
            "resource_type": "model_id"
        },
        {
            "workflow_step_name": "deploy_model",
            "workflow_step_id": "deploy_model_3",
            "resource_id": "L13IR5QBEpCfUu_-BQdI",
            "resource_type": "model_id"
        }
    ]
}
```
