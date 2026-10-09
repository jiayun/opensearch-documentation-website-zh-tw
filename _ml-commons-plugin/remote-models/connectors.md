---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "連接器"
has_children: true
has_toc: false
nav_order: 61
parent: Connecting to externally hosted models 
grand_parent: Integrating ML models
redirect_from: 
  - /ml-commons-plugin/extensibility/connectors/
---

# 第三方 ML 平台的連接器
**推出於 2.9**
{: .label .label-purple }

連接器可協助存取託管於第三方機器學習 (ML) 平台上的模型。

OpenSearch 為多個平台提供連接器，例如：

- [Amazon SageMaker](https://aws.amazon.com/sagemaker/) 可讓您託管文字嵌入模型並管理其生命週期，為 OpenSearch 中的語意搜尋查詢提供支援。連線後，Amazon SageMaker 會託管您的模型，並使用 OpenSearch 查詢推論。這對重視 Amazon SageMaker 功能 (例如模型監控、無伺服器託管，以及持續訓練與部署的工作流程自動化) 的使用者很有幫助。
- [OpenAI ChatGPT](https://platform.openai.com/docs/introduction) 可讓您從 OpenSearch 叢集內部叫用 OpenAI 聊天模型。
- [Cohere](https://cohere.com/) 可讓您使用 OpenSearch 的資料來支援 Cohere 大型語言模型。
- [Amazon Bedrock](https://aws.amazon.com/bedrock/) 支援 [Bedrock Titan Embeddings](https://aws.amazon.com/bedrock/titan/) 等模型，可在 OpenSearch 中帶動語意搜尋與檢索增強生成。
- [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai) 可讓您從 OpenSearch 叢集內部叫用 Vertex AI 模型，例如 Gemini 與文字嵌入模型。

## 連接器藍圖

建立連接器需要兩項資訊：模型的請求與回應格式，以及平台的驗證方法：

- 請求與回應格式定義於_連接器藍圖_中，其中定義了為特定平台與模型建立連接器時要提供的欄位集 (請求本文)。若要尋找適用於您平台與模型的預先建置藍圖，請參閱 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/)。如需所有連接器欄位的說明，或要為 OpenSearch 未提供的平台或模型建立藍圖，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)。

- 驗證方法定義於連接器的 `protocol` 欄位中，並由平台決定。如需詳細資訊，請參閱[連接器驗證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connector-authentication/)。

## 建立連接器

您可以用兩種方式佈建連接器：

1. [建立獨立連接器](#creating-a-standalone-connector)：獨立連接器可供 OpenSearch 中多個共用相同外部端點與組態的模型註冊重複使用。獨立連接器需要同時存取 OpenSearch 中的連接器與模型，以及第三方平台。獨立連接器會儲存在連接器索引中。

2. [為特定外部託管模型建立連接器](#creating-a-connector-for-a-specific-model)：或者，您可以建立僅能與其建立時所指定模型搭配使用的連接器。若要存取這類連接器，您只需要存取模型本身，因為連線是在模型內部建立。這些連接器會儲存在模型索引中。

如果您需要連線至不同的外部模型 (例如從 `gpt-4o-mini` 切換為 `gpt-4o`)，建議您建立個別的獨立連接器。或者，如果連接器藍圖使用預留位置，進階使用者可以在預測時覆寫連接器 `parameters`。如需詳細資訊，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)。
{: .note}

如果使用 Python，您可以使用 [`opensearch-py-ml`](https://github.com/opensearch-project/opensearch-py-ml) 用戶端 CLI 建立連接器。CLI 會自動執行許多組態步驟，讓設定更快速並降低出錯的機會。如需使用 CLI 的詳細資訊，請參閱 [CLI 文件](https://opensearch-project.github.io/opensearch-py-ml/cli/index.html#)。
{: .tip}

## 建立獨立連接器

若要建立獨立連接器，請將請求傳送至 `connectors/_create` 端點，並提供[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)中所述的所有參數：

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
        "openAI_key": "<openai_key>"
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

## 為特定模型建立連接器

若要為特定模型建立連接器，請在傳送至 `models/_register` 端點的請求之 `connector` 物件內，提供[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)中所述的所有參數：

```json
POST /_plugins/_ml/models/_register
{
    "name": "openAI-gpt-4o-mini model with a connector",
    "function_name": "remote",
    "model_group_id": "lEFGL4kB4ubqQRzegPo2",
    "description": "test model",
    "connector": {
        "name": "OpenAI Connector",
        "description": "The connector to public OpenAI model service for gpt-4o-mini",
        "version": 1,
        "protocol": "http",
        "parameters": {
            "endpoint": "api.openai.com",
            "max_tokens": 7,
            "temperature": 0,
            "model": "gpt-4o-mini"
        },
        "credential": {
            "openAI_key": "<openai_key>"
        },
        "actions": [
            {
                "action_type": "predict",
                "method": "POST",
                "url": "https://${parameters.endpoint}/v1/chat/completions",
                "headers": {
                    "Authorization": "Bearer ${credential.openAI_key}"
                },
                "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": [{\"role\": \"user\", \"content\": \"${parameters.prompt}\"}], \"max_tokens\": ${parameters.max_tokens}, \"temperature\": ${parameters.temperature} }"
            }
        ]
    }
}
```
{% include copy-curl.html %}

## 更新連接器憑證

在某些情況下，您可能需要更新用來連線至外部託管模型的憑證，例如即將到期的 API 金鑰。若要在不取消部署模型的情況下執行此操作，請在更新請求中提供新的憑證。

### 特定模型的連接器

若要更新連結至特定模型之連接器的憑證，請在下列請求中提供新的憑證：

```json
PUT /_plugins/_ml/models/{model_id}
{
  "connectors": {
    "credential": {
      "openAI_key": "<new_openai_key>"
    }
  }
}
```
{% include copy-curl.html %}

### 獨立連接器

若要更新獨立連接器的憑證，請在下列請求中提供新的憑證：

```json
PUT /_plugins/_ml/connectors/{connector_id}
{
  "credential": {
    "openAI_key": "<new_openai_key>"
  }
}
```
{% include copy-curl.html %}

## 後續步驟

- 若要尋找適用於您平台與模型的藍圖與通訊協定，請參閱 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/)。
- 若要在連接器標頭中傳遞各請求的值，請參閱[動態標頭替換]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/dynamic-header-substitution/)。
- 若要進一步瞭解如何連線至外部模型，請參閱[連線至外部託管模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。
- 若要進一步瞭解模型存取控制與模型群組，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。
