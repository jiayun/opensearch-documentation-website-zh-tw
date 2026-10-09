---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "連線至外部託管的模型"
parent: Integrating ML models
has_children: true
has_toc: false
nav_order: 60
redirect_from: 
  - /ml-commons-plugin/extensibility/index/
  - /ml-commons-plugin/remote-models/
---

# 連線至外部託管的模型
**於 2.9 版推出**
{: .label .label-purple }

與託管於第三方平台的機器學習 (ML) 模型整合，可讓系統管理員與資料科學家在 OpenSearch 叢集之外執行 ML 工作負載。連線至外部託管的模型，可讓 ML 開發人員建立與其他 ML 服務的整合，例如 Amazon SageMaker 或 OpenAI。

若要整合託管於第三方平台的模型，請從下列選項中選擇：

- 如果您是想與特定 ML 服務建立整合的 ML 開發人員，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)。
- 如果您是想建立與 ML 服務連線的系統管理員或資料科學家，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

## 必要條件

如果您是部署 ML 連接器的管理員，請確認連接器的目標模型已部署在您選擇的平台上。此外，請確認您有權限向連接器的第三方 API 傳送與接收資料。

當您的第三方平台啟用存取控制時，您可以在連接器 API 內使用 `authorization` 或 `credential` 設定來輸入安全性設定。

### 新增信任的端點

若要在 OpenSearch 中設定連接器，請使用 `plugins.ml_commons.trusted_connector_endpoints_regex` 設定將信任的端點新增至叢集設定，該設定支援 Java regex 運算式：

```json
PUT /_cluster/settings
{
    "persistent": {
        "plugins.ml_commons.trusted_connector_endpoints_regex": [
          "^https://runtime\\.sagemaker\\..*[a-z0-9-]\\.amazonaws\\.com/.*$",
          "^https://api\\.openai\\.com/.*$",
          "^https://api\\.cohere\\.ai/.*$",
          "^https://bedrock-runtime\\..*[a-z0-9-]\\.amazonaws\\.com/.*$",
          "^https://.*-aiplatform\\.googleapis\\.com/.*$"
        ]
    }
}
```
{% include copy-curl.html %}

此設定會取代整份信任端點清單，因此請包含叢集所需的每個模式。
{: .note}



### 設定連接器存取控制

如果您打算使用遠端連接器，請務必使用已啟用 Security 外掛程式的 OpenSearch 叢集。使用 Security 外掛程式可讓您使用連接器存取控制，這是使用遠端連接器時的必要條件。
{: .warning}

如果您需要連接器的細微存取控制，請使用下列叢集設定：

```json
PUT /_cluster/settings
{
    "persistent": {
        "plugins.ml_commons.connector_access_control_enabled": true
    }
}
```
{% include copy-curl.html %}

啟用存取控制後，您即可安裝 [Security 外掛程式]({{site.url}}{{site.baseurl}}/security/index/)。這會使 `backend_roles`、`add_all_backend_roles` 或 `access_model` 選項變為必要，才能使用連接器 API。若成功，OpenSearch 會傳回下列回應：

```json
{
  "acknowledged": true,
  "persistent": {
    "plugins": {
      "ml_commons": {
        "connector_access_control_enabled": "true"
      }
    }
  },
  "transient": {}
}
```

## 步驟 1：註冊模型群組

若要註冊模型，您有下列選項：

- 您可以使用 `model_group_id` 將模型版本註冊到現有的模型群組。
- 如果您不使用 `model_group_id`，ML Commons 會以新的模型群組建立模型。

若要註冊模型群組，請傳送下列請求：

```json
POST /_plugins/_ml/model_groups/_register
{
  "name": "remote_model_group",
  "description": "A model group for external models"
}
```
{% include copy-curl.html %}

回應包含模型群組 ID，您將使用它把模型註冊到此模型群組：

```json
{
 "model_group_id": "wlcnb4kBJ1eYAeTMHlV6",
 "status": "CREATED"
}
```

若要進一步了解模型群組，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。

## 步驟 2：建立連接器

您可以建立獨立連接器，供 OpenSearch 中共用相同外部端點與組態的多個模型註冊重複使用。或者，您也可以在建立模型時指定連接器，使其僅能用於該模型。如需更多資訊與範例連接器，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

如果您使用的是 Amazon OpenSearch Service，建立連接器的程序有所不同。如需更多資訊，請參閱[在 Amazon OpenSearch Service 中建立連接器](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ml-amazon-connector.html)。
{: .note}

Connectors Create API（`/_plugins/_ml/connectors/_create`）會建立連接器，協助在 OpenSearch 中註冊與部署外部模型。使用 `endpoint` 參數，您可以透過其特定的 API 端點將 ML Commons 連線至任何支援的 ML 工具。例如，您可以使用 `api.openai.com` 端點連線至 ChatGPT 模型：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "OpenAI Chat Connector",
    "description": "The connector to public OpenAI model service for gpt-4o-mini",
    "version": 1,
    "protocol": "http",
    "parameters": {
        "endpoint": "api.openai.com",
        "model": "gpt-4o-mini"
    },
    "credential": {
        "openAI_key": "..."
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "url": "https://${parameters.endpoint}/v1/chat/completions",
            "headers": {
                "Authorization": "Bearer ${credential.openAI_key}"
            },
            "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": ${parameters.messages} }"
        }
    ]
}
```
{% include copy-curl.html %}

回應包含新建立連接器的連接器 ID：

```json
{
  "connector_id": "a1eMb4kBJ1eYAeTMAljY"
}
```

## 步驟 3：註冊外部託管的模型

若要將外部託管的模型註冊到步驟 1 建立的模型群組，請在下列請求中提供步驟 1 的模型群組 ID 與步驟 2 的連接器 ID。您必須將 `function_name` 指定為 `remote`：

```json
POST /_plugins/_ml/models/_register
{
    "name": "openAI-gpt-4o-mini",
    "function_name": "remote",
    "model_group_id": "1jriBYsBq7EKuKzZX131",
    "description": "test model",
    "connector_id": "a1eMb4kBJ1eYAeTMAljY"
}
```
{% include copy-curl.html %}

OpenSearch 會傳回註冊作業的工作 ID：

```json
{
  "task_id": "cVeMb4kBJ1eYAeTMFFgj",
  "status": "CREATED"
}
```

若要檢查作業狀態，請將工作 ID 提供給 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)：

```bash
GET /_plugins/_ml/tasks/cVeMb4kBJ1eYAeTMFFgj
```
{% include copy-curl.html %}

當作業完成時，狀態會變為 `COMPLETED`：

```json
{
  "model_id": "cleMb4kBJ1eYAeTMFFg4",
  "task_type": "REGISTER_MODEL",
  "function_name": "REMOTE",
  "state": "COMPLETED",
  "worker_node": [
    "XPcXLV7RQoi5m8NI_jEOVQ"
  ],
  "create_time": 1689793598499,
  "last_update_time": 1689793598530,
  "is_async": false
}
```

請記下傳回的 `model_id`，因為部署模型時需要用到它。

## 步驟 4：部署模型

依預設，當您第一次傳送 Predict API 請求時，外部託管的模型會自動部署。若要停用外部託管模型的自動部署，請將 `plugins.ml_commons.model_auto_deploy.enable` 設為 `false`：
```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.model_auto_deploy.enable" : "false"
  }
}
```
{% include copy-curl.html %}

若要部署模型，請使用 [Deploy API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/deploy-model/)。

```bash
POST /_plugins/_ml/models/cleMb4kBJ1eYAeTMFFg4/_deploy
```
{% include copy-curl.html %}

回應包含工作 ID，您可以用它來檢查部署作業的狀態：

```json
{
  "task_id": "vVePb4kBJ1eYAeTM7ljG",
  "status": "CREATED"
}
```

如同上一個步驟，呼叫 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 來檢查作業狀態：

```bash
GET /_plugins/_ml/tasks/vVePb4kBJ1eYAeTM7ljG
```
{% include copy-curl.html %}

當作業完成時，狀態會變為 `COMPLETED`：

```json
{
  "model_id": "cleMb4kBJ1eYAeTMFFg4",
  "task_type": "DEPLOY_MODEL",
  "function_name": "REMOTE",
  "state": "COMPLETED",
  "worker_node": [
    "n-72khvBTBi3bnIIR8FTTw"
  ],
  "create_time": 1689793851077,
  "last_update_time": 1689793851101,
  "is_async": true
}
```

## 步驟 5（選用）：測試模型

使用 [Predict API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/) 來測試模型：

```json
POST /_plugins/_ml/models/cleMb4kBJ1eYAeTMFFg4/_predict
{
  "parameters": {
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }
}
```
{% include copy-curl.html %}

若要進一步了解 OpenAI 內的聊天功能，請參閱 [OpenAI Chat API](https://platform.openai.com/docs/api-reference/chat)。

回應包含 OpenAI 模型提供的推論結果：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "id": "chatcmpl-7e6s5DYEutmM677UZokF9eH40dIY7",
            "object": "chat.completion",
            "created": 1689793889,
            "model": "gpt-4o-mini",
            "choices": [
              {
                "index": 0,
                "message": {
                  "role": "assistant",
                  "content": "Hello! How can I assist you today?"
                },
                "finish_reason": "stop"
              }
            ],
            "usage": {
              "prompt_tokens": 19,
              "completion_tokens": 9,
              "total_tokens": 28
            }
          }
        }
      ]
    }
  ]
}
```
## 步驟 6：使用模型進行批次匯入

若要了解如何使用模型進行批次匯入以提升匯入效能，請參閱[使用外部託管的 ML 模型進行批次匯入]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/batch-ingestion/)。

## 步驟 7：使用模型進行搜尋

若要了解如何使用模型進行向量搜尋，請參閱[AI 搜尋方法]({{site.url}}{{site.baseurl}}/vector-search/ai-search/#ai-search-methods)。

## 步驟 8（選用）：取消部署模型

您可以透過在模型設定中定義 TTL 來自動取消部署模型，或使用 Undeploy API 手動取消部署模型。如需更多資訊，請參閱 [Undeploy API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/undeploy-model/)。

## 後續步驟

- 如需連接器的更多資訊（包括範例連接器），請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。
- 如需連接器欄位的更多資訊，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)。
- 如需在 OpenSearch 中管理 ML 模型的更多資訊，請參閱[在 OpenSearch 中使用 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-serving-framework/)。
- 如需在 OpenSearch 中與 ML 模型互動的更多資訊，請參閱[在 OpenSearch Dashboards 中管理 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/ml-dashboard/)
如需如何設定模型防護機制的說明，請參閱[防護機制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/guardrails/)。
