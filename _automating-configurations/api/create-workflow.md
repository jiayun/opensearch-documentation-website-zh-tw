---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新工作流程"
parent: Workflow APIs
nav_order: 10
---

# 建立或更新工作流程 API

建立工作流程會將工作流程範本的內容新增至 flow framework 系統索引。您可以使用 JSON 格式（指定 `Content-Type: application/json`）或 YAML 格式（指定 `Content-Type: application/yaml`）提供工作流程。根據預設，系統會驗證工作流程，以協助找出無效的組態，包括：

* 工作流程步驟需要尚未安裝的 OpenSearch 外掛程式。
* 工作流程步驟依賴由這些步驟本身提供的先前節點輸入。
* 工作流程步驟欄位含有無效的值。
* 工作流程圖（節點/邊）組態包含循環或具有重複的 ID。

若要取得工作流程步驟的驗證範本，請呼叫 [Get Workflow Steps API]({{site.url}}{{site.baseurl}}/automating-configurations/api/get-workflow-steps/)。

您可以在工作流程步驟欄位的值中加入預留位置運算式。例如，您可以在範本中將認證資訊欄位指定為 {% raw %}`openAI_key: '${{ openai_key }}'`{% endraw %}。在佈建期間，此運算式會以使用者提供的值取代，格式為 {% raw %}`${{ <value> }}`{% endraw %}。您可以使用 [Provision Workflow API]({{site.url}}{{site.baseurl}}/automating-configurations/api/provision-workflow/)，或使用此 API 並將 `provision` 參數設為 `true`，以參數形式傳遞實際的金鑰。

建立工作流程後，請將其 `workflow_id` 提供給其他 API。

`POST` 方法會建立新的工作流程。`PUT` 方法會更新現有的工作流程。您可以指定 `update_fields` 參數來更新特定欄位。

只有在工作流程尚未佈建時，您才能更新完整的工作流程。
{: .note}

## 端點

```json
POST /_plugins/_flow_framework/workflow
PUT /_plugins/_flow_framework/workflow/{workflow_id}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `workflow_id` | 字串 | 要更新的工作流程 ID。`PUT` 方法的必要參數。 |

## 查詢參數

工作流程通常會在不同的步驟中建立及佈建。不過，在您徹底測試工作流程後，可以加入 `provision` 查詢參數，將建立與佈建步驟合併：

```json
POST /_plugins/_flow_framework/workflow?provision=true
```
{% include copy-curl.html %}

設為 `true` 時，會在建立後立即執行 [Provision Workflow API]({{site.url}}{{site.baseurl}}/automating-configurations/api/provision-workflow/)。

根據預設，工作流程在建立時會經過驗證，以確保語法有效且圖形不包含循環。您可以使用 `validation` 查詢參數控制此行為。若將 `validation` 設為 `all`，OpenSearch 會執行完整的範本驗證。`validation` 參數的任何其他值都會略過驗證，讓您能儲存不完整或仍在進行中的範本。若要停用範本驗證，請將 `validation` 設為 `none`：

```json
POST /_plugins/_flow_framework/workflow?validation=none
```
{% include copy-curl.html %}

在尚未佈建的工作流程中，您可以更新 `workflows` 欄位以外的欄位。例如，您可以依下列方式更新 `name` 和 `description` 欄位：

```json
PUT /_plugins/_flow_framework/workflow/{workflow_id}?update_fields=true
{
  "name": "new-template-name",
  "description": "A new description for the existing template"
}
```
{% include copy-curl.html %}

您無法同時指定 `provision` 和 `update_fields` 參數。
{: .note}

若工作流程已佈建，您可以更新並重新佈建完整範本：

```json
PUT /_plugins/_flow_framework/workflow/{workflow_id}?reprovision=true
{
  <updated complete template>
}
```

您可以在工作流程中新增步驟，但無法刪除步驟。目前只能更新索引設定、搜尋管線及資料匯入管線步驟。
{: .note}

若要控制請求等待佈建與重新佈建程序完成的時間長度，請使用 `wait_for_completion_timeout` 參數：

```json
POST /_plugins/_flow_framework/workflow/?provision=true&wait_for_completion_timeout=2s
```
{% include copy-curl.html %}

```json
PUT /_plugins/_flow_framework/workflow/{workflow_id}/?reprovision=true&wait_for_completion_timeout=2s
```
{% include copy-curl.html %}

若作業未在指定時間內完成，回應會傳回目前的工作流程狀態，而執行作業會以非同步方式繼續進行。

只有在 `provision` 或 `reprovision` 設為 `true` 時，才能使用 `wait_for_completion_timeout` 參數
{: .note}

例如，下列請求會佈建工作流程，並最多等待 2 秒讓其完成：
您可以依下列方式，使用[工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates/)建立及佈建工作流程：

```json
POST /_plugins/_flow_framework/workflow?use_case={use_case}&provision=true
{
    "create_connector.credential.key" : "<YOUR API KEY>"
}
```
{% include copy-curl.html %}

下表列出可用的查詢參數。所有查詢參數皆為選用。只有在 `provision` 參數設為 `true` 時，才允許使用者提供的參數。

| 參數 | 資料類型 | 說明 |
|:---------------------------------------|:----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `provision` | 布林值 | 是否在請求中一併佈建工作流程。預設為 `false`。 |
| `update_fields` | 布林值 | 是否只更新請求本文中包含的欄位。預設為 `false`。 |
| `reprovision` | 布林值 | 若範本已佈建，是否重新佈建整個範本。必須在請求本文中提供完整範本。預設為 `false`。 |
| `validation` | 字串 | 是否驗證工作流程。有效值為 `all`（驗證範本）和 `none`（不驗證範本）。預設為 `all`。 |
| `use_case` | 字串 | 建立工作流程時要使用的[工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates/#supported-workflow-templates)名稱。 |
| `wait_for_completion_timeout` | 時間值 | 指定同步佈建或重新佈建的最長等待時間。若超過逾時時間，請求會傳回目前的工作流程狀態，而執行作業會以非同步方式繼續進行。|
| 使用者提供的替代運算式 | 字串 | 與範本中替代運算式相符的參數。只有在 `provision` 設為 `true` 時才允許使用。選用。若 `provision` 設為 `false`，您可以在 [Provision Workflow API 查詢參數]({{site.url}}{{site.baseurl}}/automating-configurations/api/provision-workflow/#query-parameters)中傳遞這些參數。 |

## 請求本文欄位

下表列出可用的請求欄位。

|欄位	|資料類型	|必要/選用	|說明	|
|:---	|:---	|:---	|:---	|
|`name`	|字串	|必要	|工作流程的名稱。	|
|`description`	|字串	|選用	|工作流程的說明。	|
|`use_case`	|字串	|選用	| 使用者提供的使用案例，可搭配 [Search Workflow API]({{site.url}}{{site.baseurl}}/automating-configurations/api/search-workflow/) 尋找相關工作流程。您可以使用此欄位指定自訂值。這與 `use_case` 查詢參數不同。 |
|`version`	|物件	|選用	| 包含兩個欄位的鍵值對應表：`template` 用於識別範本版本，而 `compatibility` 用於識別最低必要 OpenSearch 版本的清單。	|
|`workflows`	|物件	|選用	|工作流程的對應表。僅支援 `provision` 鍵。工作流程鍵的值是鍵值對應表，其中包含 `user_params` 的欄位，以及 `nodes` 和 `edges` 的清單。	|

## 請求範例：以 YAML 註冊並部署外部託管的模型

若要提供 YAML 格式的範本，請在請求標頭中指定 `Content-Type: application/yaml`：

```bash
curl -XPOST "http://localhost:9200/_plugins/_flow_framework/workflow" -H 'Content-Type: application/yaml'
```

YAML 範本允許註解。 
{: .tip}

以下是用於註冊並部署外部託管模型的 YAML 範本範例：

```yaml
# This Name Is Required API
name: createconnector-registerremotemodel-deploymodel
# Other Fields Are Optional But Useful API
description: This template creates a connector to a remote model, registers it, and
  deploys that model
# Other Templates With A Similar Use Case Can Be Searched API
use_case: REMOTE_MODEL_DEPLOYMENT
version:
  # Templates may be versioned by their authors
  template: 1.0.0
  # Compatibility with OpenSearch 2.12.0 and higher and 3.0.0 and higher
  compatibility:
  - 2.12.0
  - 3.0.0
# One Or More Workflows Can Be Included, Presently Only Provision Is Supported API
workflows:
  provision:
    # These nodes are the workflow steps corresponding to ML Commons APIs
    nodes:
    # This ID must be unique to this workflow
    - id: create_connector_1
      # There may be multiple steps with the same type
      type: create_connector
      # These inputs match the Create Connector API body
      user_inputs:
        name: OpenAI Chat Connector
        description: The connector to public OpenAI model service for gpt-4o-mini
        version: '1'
        protocol: http
        parameters:
          endpoint: api.openai.com
          model: gpt-4o-mini
        credential:
          openAI_key: '12345'
        actions:
        - action_type: predict
          method: POST
          url: https://${parameters.endpoint}/v1/chat/completions
    # This ID must be unique to this workflow
    - id: register_model_2
      type: register_remote_model
      # This step needs the connector_id produced as an output of the previous step
      previous_node_inputs:
        create_connector_1: connector_id
      # These inputs match the Register Model API body
      user_inputs:
        name: openAI-gpt-4o-mini
        function_name: remote
        description: test model
    # This ID must be unique to this workflow
    - id: deploy_model_3
      type: deploy_model
      # This step needs the model_id produced as an output of the previous step
      previous_node_inputs:
        register_model_2: model_id
    # Since the nodes include previous_node_inputs these are optional to define
    # They will be added automatically and included in the stored template
    # Additional edges may also be added here if required for sequencing
    edges:
    - source: create_connector_1
      dest: register_model_2
    - source: register_model_2
      dest: deploy_model_3
```
{% include copy-curl.html %}

## 請求範例：註冊並部署遠端模型（JSON）

若要提供 JSON 格式的範本，請在請求標頭中指定 `Content-Type: application/json`：

```bash
curl -XPOST "http://localhost:9200/_plugins/_flow_framework/workflow" -H 'Content-Type: application/json'
```
以下 JSON 範本與上一節提供的 YAML 範本等效： 

```json
{
  "name": "createconnector-registerremotemodel-deploymodel",
  "description": "This template creates a connector to a remote model, registers it, and deploys that model",
  "use_case": "REMOTE_MODEL_DEPLOYMENT",
  "version": {
    "template": "1.0.0",
    "compatibility": [
      "2.12.0",
      "3.0.0"
    ]
  },
  "workflows": {
    "provision": {
      "nodes": [
        {
          "id": "create_connector_1",
          "type": "create_connector",
          "user_inputs": {
            "name": "OpenAI Chat Connector",
            "description": "The connector to public OpenAI model service for gpt-4o-mini",
            "version": "1",
            "protocol": "http",
            "parameters": {
              "endpoint": "api.openai.com",
              "model": "gpt-4o-mini"
            },
            "credential": {
              "openAI_key": "12345"
            },
            "actions": [
              {
                "action_type": "predict",
                "method": "POST",
                "url": "https://${parameters.endpoint}/v1/chat/completions"
              }
            ]
          }
        },
        {
          "id": "register_model_2",
          "type": "register_remote_model",
          "previous_node_inputs": {
            "create_connector_1": "connector_id"
          },
          "user_inputs": {
            "name": "openAI-gpt-4o-mini",
            "function_name": "remote",
            "description": "test model"
          }
        },
        {
          "id": "deploy_model_3",
          "type": "deploy_model",
          "previous_node_inputs": {
            "register_model_2": "model_id"
          }
        }
      ],
      "edges": [
        {
          "source": "create_connector_1",
          "dest": "register_model_2"
        },
        {
          "source": "register_model_2",
          "dest": "deploy_model_3"
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

OpenSearch 回應中會包含 `workflow_id`：

```json
{
  "workflow_id" : "8xL8bowB8y25Tqfenm50"
}
```

建立工作流程後，您可以搭配 `workflow_id` 使用其他工作流程 API。

## 啟用 wait_for_completion_timeout 時的回應範例

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