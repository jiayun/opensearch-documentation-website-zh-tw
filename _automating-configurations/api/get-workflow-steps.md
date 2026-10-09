---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得工作流程步驟"
parent: Workflow APIs
nav_order: 50
---

# Get Workflow Steps API

此 API 會傳回工作流程步驟的清單，包括其必要的輸入、輸出、預設逾時值以及必要的外掛程式。例如，對於 `register_remote_model` 步驟，Get Workflow Steps API 會傳回以下資訊：

```json
{
  "register_remote_model": {
    "inputs": [
      "name",
      "connector_id"
    ],
    "outputs": [
      "model_id",
      "register_model_status"
    ],
    "required_plugins": [
      "opensearch-ml"
    ]
  }
}
``` 

## 端點

```json
GET /_plugins/_flow_framework/workflow/_steps
GET /_plugins/_flow_framework/workflow/_steps?workflow_step={step_name}
``` 

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `workflow_step` | 字串 | 要擷取的步驟名稱。可指定多個步驟名稱，以逗號分隔的清單形式提供。例如 `create_connector,delete_model,deploy_model`。 |

## 請求範例

若要擷取所有工作流程步驟，請使用以下請求：

```json
GET /_plugins/_flow_framework/workflow/_steps
``` 
{% include copy-curl.html %}

若要擷取特定的工作流程步驟，請將步驟名稱作為查詢參數傳遞至請求：

```json
GET /_plugins/_flow_framework/workflow/_step?workflow_steps=create_connector,delete_model,deploy_model
```
{% include copy-curl.html %}


## 回應範例

OpenSearch 會以工作流程步驟回應。傳回步驟中的欄位順序可能與原始 JSON 不完全一致，但功能完全相同。

若要以 YAML 格式擷取範本，請在請求標頭中指定 `Content-Type: application/yaml`：

```bash
curl -XGET "http://localhost:9200/_plugins/_flow_framework/workflow/_steps" -H 'Content-Type: application/yaml'
```

若要以 JSON 格式擷取範本，請在請求標頭中指定 `Content-Type: application/json`：

```bash
curl -XGET "http://localhost:9200/_plugins/_flow_framework/workflow/_steps" -H 'Content-Type: application/json'
```
