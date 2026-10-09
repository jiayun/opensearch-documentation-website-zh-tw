---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "預測串流"
parent: Model APIs
grand_parent: ML Commons APIs
nav_order: 65
---

# Predict Stream API
**於 3.3 版推出**
{: .label .label-purple }

這是實驗性功能，不建議在正式環境中使用。若要了解此功能的最新進展，或想要提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)上的討論。    
{: .warning}

Predict Stream API 提供與 [Predict API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/) 相同的功能，但會以串流格式傳回回應，在資料可用時分段傳送。這種串流方式特別適合回應內容冗長的大型語言模型互動，讓您能立即看到部分結果，而不必等待完整回應。

您也可以改透過 gRPC 串流預測結果。如需詳細資訊，請參閱 [gRPC Predict Model Stream API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/predict-model-stream/)。
{: .note}

此 API 支援下列遠端模型類型：
- [OpenAI Chat Completion](https://platform.openai.com/docs/api-reference/completions)
- [Amazon Bedrock Converse Stream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html)

## 端點

```json
POST /_plugins/_ml/models/{model_id}/_predict/stream
```

## 先決條件

使用此 API 之前，請確認您已符合下列先決條件。

### 設定叢集

請依照下列步驟設定叢集。

#### 步驟 1：安裝必要的外掛程式

Predict Stream API 相依於下列外掛程式。這些外掛程式包含在 OpenSearch 發行版本中，但必須依下列方式明確安裝：

```bash
bin/opensearch-plugin install transport-reactor-netty4
bin/opensearch-plugin install arrow-base
bin/opensearch-plugin install arrow-flight-rpc
```

如需詳細資訊，請參閱[管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。

#### 步驟 2：設定 OpenSearch 設定

將下列設定新增至您的 `opensearch.yml` 檔案或 Docker Compose 組態：

```yaml
opensearch.experimental.feature.transport.stream.enabled: true

# Choose one based on your security settings
http.type: reactor-netty4        # security disabled
http.type: reactor-netty4-secure # security enabled

# Multi-node cluster settings (if applicable)
# Use network.host IP for opensearch.yml or node name for Docker
arrow.flight.publish_host: <ip>
arrow.flight.bind_host: <ip>

# Security-enabled cluster settings (if applicable)
transport.stream.type.default: FLIGHT-SECURE
flight.ssl.enable: true
transport.ssl.enforce_hostname_verification: false
```
{% include copy.html %}

如果您使用安全性示範憑證，請在 `opensearch.yml` 檔案中將 `plugins.security.ssl.transport.enforce_hostname_verification: false` 變更為 `transport.ssl.enforce_hostname_verification: false`。
{: .note}

如需啟用實驗性功能的詳細資訊，請參閱[實驗性功能旗標]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/experimental/)。

#### 步驟 3：設定 JVM 選項

將下列設定新增至您的 `jvm.options` 檔案：

```yaml
-Dio.netty.allocator.numDirectArenas=1
-Dio.netty.noUnsafe=false
-Dio.netty.tryUnsafe=true
-Dio.netty.tryReflectionSetAccessible=true
--add-opens=java.base/java.nio=org.apache.arrow.memory.core,ALL-UNNAMED
```
{% include copy.html %}

### 設定必要的 API

請依照下列步驟設定 API。

#### 步驟 1：啟用串流功能旗標

若要啟用串流功能旗標，請依下列方式更新叢集設定：

```json
PUT _cluster/settings
{
  "persistent" : {
    "plugins.ml_commons.stream_enabled": true
  }
}
```
{% include copy-curl.html %}

#### 步驟 2：註冊相容的外部託管模型

若要註冊 OpenAI Chat Completion 模型，請傳送下列請求：

```json
POST /_plugins/_ml/models/_register
{
    "name": "OpenAI gpt-4o-mini",
    "function_name": "remote",
    "description": "OpenAI model",
    "connector": {
        "name": "OpenAI Chat Connector",
        "description": "The connector to OpenAI model service for gpt-4o-mini",
        "version": 1,
        "protocol": "http",
        "parameters": {
            "endpoint": "api.openai.com",
            "model": "gpt-4o-mini"
        },
        "credential": {
            "openAI_key": "<your_api_key>"
        },
        "actions": [
            {
                "action_type": "predict",
                "method": "POST",
                "url": "https://${parameters.endpoint}/v1/chat/completions",
                "headers": {
                    "Authorization": "Bearer ${credential.openAI_key}"
                },
                "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": ${parameters.messages} }",
                "response_filter": "$.choices[0].delta.content"
            }
        ]
    }
}
```
{% include copy-curl.html %}

若要註冊 Amazon Bedrock Converse Stream 模型，請傳送下列請求：

```json
POST /_plugins/_ml/models/_register
{
    "name": "Amazon Bedrock Converse Stream model",
    "function_name": "remote",
    "description": "Amazon Bedrock Claude model",
    "connector": {
        "name": "Amazon Bedrock Converse",
        "description": "The connector to Amazon Bedrock Converse",
        "version": 1,
        "protocol": "aws_sigv4",
        "credential": {
            "access_key": "<your_aws_access_key>",
            "secret_key": "<your_aws_secret_key>",
            "session_token": "<your_aws_session_token>"
        },
        "parameters": {
            "region": "<your_aws_region>",
            "service_name": "bedrock",
            "response_filter": "$.output.message.content[0].text",
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
        },
        "actions": [
            {
                "action_type": "predict",
                "method": "POST",
                "headers": {
                    "content-type": "application/json"
                },
                "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/converse",
                "request_body": "{\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"${parameters.inputs}\"}]}]}"
            }
        ]
    }
}
```
{% include copy-curl.html %}

## 請求範例

若要使用 Predict Stream API，您必須加入與模型類型對應的 `_llm_interface` 參數：
- OpenAI Chat Completion：`openai/v1/chat/completions`
- Amazon Bedrock Converse Stream：`bedrock/converse/claude`

若為 OpenAI Chat Completion，請傳送下列請求：

```json
POST /_plugins/_ml/models/{model_id}/_predict/stream
{
  "parameters": {
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Can you summarize Prince Hamlet of William Shakespeare in around 1000 words?"
      }
    ],
    "_llm_interface": "openai/v1/chat/completions"
  }
}
```
{% include copy-curl.html %}

若為 Amazon Bedrock Converse Stream，請傳送下列請求：

```json
POST /_plugins/_ml/models/{model_id}/_predict/stream
{
  "parameters": {
    "inputs": "Can you summarize Prince Hamlet of William Shakespeare in around 1000 words?",
    "_llm_interface": "bedrock/converse/claude"
  }
}
```
{% include copy-curl.html %}

## 回應範例

串流格式使用 Server-Sent Events (SSE)，每個區塊包含模型回應的一部分，並以 `is_last` 旗標表示是否完成。

```json
data: {"inference_results":[{"output":[{"name":"response","dataAsMap":{"content":"Sure","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"response","dataAsMap":{"content":"!","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"response","dataAsMap":{"content":"Ham","is_last":false}}]}]}

...

data: {"inference_results":[{"output":[{"name":"response","dataAsMap":{"content":" psyche","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"response","dataAsMap":{"content":".","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"response","dataAsMap":{"content":"","is_last":true}}]}]}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- |:------------------------------------------------------------------------------------------------------------|
| `inference_results` | 陣列 | 包含模型傳回的串流回應資料。 |
| `inference_results.output` | 陣列 | 包含每個推論結果的輸出物件。 |
| `inference_results.output.name` | 字串 | 輸出欄位的名稱 (通常為 `response`)。 |
| `inference_results.output.dataAsMap` | 物件 | 包含回應內容與中繼資料。 |
| `inference_results.output.dataAsMap.content` | 字串 | 模型回應中的文字內容區塊。 |
| `inference_results.output.dataAsMap.is_last` | 布林值 | 表示此區塊是否為串流中的最後一個區塊：最後一個區塊為 `true`，若還有更多區塊則為 `false`。 |