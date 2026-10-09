---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行代理程式串流"
parent: Agent APIs
grand_parent: ML Commons APIs
nav_order: 25
---

# Execute Agent Stream API
**於 3.3 版推出**
{: .label .label-purple }

這是實驗性功能，不建議在正式環境中使用。若要瞭解此功能的最新進展或提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)上的討論。    
{: .warning}

Execute Agent Stream API 提供與 [Execute Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/) 相同的功能，但會以串流格式傳回回應，在資料可用時分批傳送。這種串流方式對於回應冗長的大型語言模型互動特別有幫助，讓您可以立即看到部分結果，無須等待完整回應。

您也可以透過 gRPC 以串流方式執行代理程式。如需詳細資訊，請參閱 [gRPC Execute Agent Stream API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/execute-agent-stream/)。
{: .note}

此 API 支援下列代理程式類型：

- **對話式代理程式**，搭配下列外部託管模型類型：
    - [OpenAI Chat Completion](https://platform.openai.com/docs/api-reference/completions)
    - [Amazon Bedrock Converse Stream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html)

- **AG-UI 代理程式**，使用 AG-UI 通訊協定的請求與回應格式。如需詳細資訊，請參閱 [AG-UI 代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/ag-ui/)。

## 端點

```json
POST /_plugins/_ml/agents/{agent_id}/_execute/stream
```

## 先決條件

使用此 API 前，請確保您已滿足下列先決條件。

### 設定您的叢集

請依照下列步驟設定您的叢集。

#### 步驟 1：安裝必要的外掛程式

Execute Agent Stream API 相依於下列外掛程式。這些外掛程式已包含在 OpenSearch 發行套件中，但必須依照下列方式明確安裝：

```bash
bin/opensearch-plugin install transport-reactor-netty4
bin/opensearch-plugin install arrow-flight-rpc
```

如需詳細資訊，請參閱[管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。

#### 步驟 2：設定 OpenSearch 設定

將這些設定新增至您的 `opensearch.yml` 檔案或 Docker Compose 組態：

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

如果您使用安全性示範憑證，請將您 `opensearch.yml` 檔案中的 `plugins.security.ssl.transport.enforce_hostname_verification: false` 變更為 `transport.ssl.enforce_hostname_verification: false`。
{: .note}

如需啟用實驗性功能的詳細資訊，請參閱[實驗性功能旗標]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/experimental/)。

#### 步驟 3：設定 JVM 選項

將這些設定新增至您的 `jvm.options` 檔案：

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

若要啟用串流功能旗標，請依照下列方式更新叢集設定：

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
                "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": [{\"role\":\"developer\",\"content\":\"${parameters.system_prompt}\"},${parameters._chat_history:-}{\"role\":\"user\",\"content\":\"${parameters.prompt}\"}${parameters._interactions:-}]${parameters.tool_configs:-} }"
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
                "request_body": "{ \"system\": [{\"text\": \"${parameters.system_prompt}\"}], \"messages\": [${parameters._chat_history:-}{\"role\":\"user\",\"content\":[{\"text\":\"${parameters.prompt}\"}]}${parameters._interactions:-}]${parameters.tool_configs:-} }"
            }
        ]
    }
}
```
{% include copy-curl.html %}

#### 步驟 3：註冊對話式代理程式

註冊您的代理程式時，必須包含與您的模型類型對應的 `_llm_interface` 參數：
- OpenAI Chat Completion：`openai/v1/chat/completions`
- Amazon Bedrock Converse Stream：`bedrock/converse/claude`

若要註冊您的代理程式，請傳送下列請求：

```json
POST /_plugins/_ml/agents/_register
{
    "name": "Chat Agent with RAG",
    "type": "conversational",
    "description": "This is a test agent",
    "llm": {
        "model_id": "<model_id_from_step_2>",
        "parameters": {
            "max_iteration": 5,
            "system_prompt": "You are a helpful assistant. You are able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics.\nIf the question is complex, you will split it into several smaller questions, and solve them one by one. For example, the original question is:\nhow many orders in last three month? Which month has highest?\nYou will spit into several smaller questions:\n1.Calculate total orders of last three month.\n2.Calculate monthly total order of last three month and calculate which months order is highest. You MUST use the available tools everytime to answer the question",
            "prompt": "${parameters.question}"
        }
    },
    "memory": {
        "type": "conversation_index"
    },
    "parameters": {
        "_llm_interface": "openai/v1/chat/completions"
    },
    "tools": [
        {
            "type": "IndexMappingTool",
            "name": "DemoIndexMappingTool",
            "parameters": {
                "index": "${parameters.index}",
                "input": "${parameters.question}"
            }
        },
        {
            "type": "ListIndexTool",
            "name": "RetrieveIndexMetaTool",
            "description": "Use this tool to get OpenSearch index information: (health, status, index, uuid, primary count, replica count, docs.count, docs.deleted, store.size, primary.store.size)."
        }
    ],
    "app_type": "my_app"
}
```
{% include copy-curl.html %}

## 範例請求：對話式代理程式

```json
POST /_plugins/_ml/agents/{agent_id}/_execute/stream
{
    "parameters": {
        "question": "How many indices are in my cluster?"
    }
}
```
{% include copy-curl.html %}

## 範例回應：對話式代理程式

```json
data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":"[{\"index\":0.0,\"id\":\"call_HjpbrbdQFHK0omPYa6m2DCot\",\"type\":\"function\",\"function\":{\"name\":\"RetrieveIndexMetaTool\",\"arguments\":\"\"}}]","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":"[{\"index\":0.0,\"function\":{\"arguments\":\"{}\"}}]","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":"{\"choices\":[{\"message\":{\"tool_calls\":[{\"type\":\"function\",\"function\":{\"name\":\"RetrieveIndexMetaTool\",\"arguments\":\"{}\"},\"id\":\"call_HjpbrbdQFHK0omPYa6m2DCot\"}]},\"finish_reason\":\"tool_calls\"}]}","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":"","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":"row,health,status,index,uuid,pri(number of primary shards),rep(number of replica shards),docs.count(number of available documents),docs.deleted(number of deleted documents),store.size(store size of primary and replica shards),pri.store.size(store size of primary shards)\n1,green,open,.plugins-ml-model-group,Msb1Y4W5QeiLs5yUQi-VRg,1,1,2,0,17.1kb,5.9kb\n2,green,open,.plugins-ml-memory-message,1IWd1HPeSWmM29qE6rcj_A,1,1,658,0,636.4kb,313.5kb\n3,green,open,.plugins-ml-memory-meta,OETb21fqQJa3Y2hGQbknCQ,1,1,267,7,188kb,93.9kb\n4,green,open,.plugins-ml-config,0mnOWX5gSX2s-yP27zPFNw,1,1,1,0,8.1kb,4kb\n5,green,open,.plugins-ml-model,evYOOKN4QPqtmUjxsDwJYA,1,1,5,5,421.5kb,210.7kb\n6,green,open,.plugins-ml-agent,I0SpBovjT3C6NABCBzGiiQ,1,1,6,0,205.5kb,111.3kb\n7,green,open,.plugins-ml-task,_Urzn9gdSuCRqUaYAFaD_Q,1,1,100,4,136.1kb,45.3kb\n8,green,open,top_queries-2025.09.26-00444,jb7Q1FiLSl-wTxjdSUKs_w,1,1,1736,126,1.8mb,988kb\n9,green,open,.plugins-ml-connector,YaJORo4jT0Ksp24L5cW1uA,1,1,2,0,97.8kb,48.9kb\n","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":"There","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":" are","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":" ","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":"9","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":" indices","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":" in","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":" your","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":" cluster","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":".","is_last":false}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":"","is_last":true}}]}]}
```

## 含詞元用量的範例請求
**於 3.6 版推出**
{: .label .label-purple }

若要在串流回應中接收詳細的詞元用量指標，請將 `include_token_usage` 設為 `true`：

```json
POST /_plugins/_ml/agents/{agent_id}/_execute/stream
{
    "parameters": {
        "question": "How many indices are in my cluster?",
        "include_token_usage": true
    }
}
```
{% include copy-curl.html %}

### 含詞元用量的範例回應

串流回應包含一個 `token_usage` 區塊，該區塊會在內容區塊之後、最終完成區塊之前送出：

```json
... (content chunks as shown above) ...

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"token_usage","dataAsMap":{"per_turn_usage":[{"turn":1,"model_id":"rk6okJwB_kOxOUbO6853","model_name":"gpt-4o-mini","model_url":"https://api.openai.com/v1/chat/completions","input_tokens":1042,"output_tokens":69,"total_tokens":1111,"cache_read_input_tokens":0}],"per_model_usage":[{"model_id":"rk6okJwB_kOxOUbO6853","model_name":"gpt-4o-mini","model_url":"https://api.openai.com/v1/chat/completions","call_count":1,"input_tokens":1042,"output_tokens":69,"total_tokens":1111,"cache_read_input_tokens":0}]}}]}]}

data: {"inference_results":[{"output":[{"name":"memory_id","result":"LvU1iJkBCzHrriq5hXbN"},{"name":"parent_interaction_id","result":"L_U1iJkBCzHrriq5hXbs"},{"name":"response","dataAsMap":{"content":"","is_last":true}}]}]}
```

## 範例請求：AG-UI 代理程式
**於 3.5 版推出**
{: .label .label-purple }

這是實驗性功能，不建議在正式環境中使用。如需此功能進展的最新消息，或想提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/) 的討論。
{: .warning}

AG-UI 代理程式使用 AG-UI 通訊協定格式進行前端整合：

```json
POST /_plugins/_ml/agents/{agent_id}/_execute/stream
{
    "threadId": "thread-xxxxx",
    "runId": "run-xxxxx",
    "messages": [
        {
            "id": "msg-xxxxx",
            "role": "user",
            "content": "How many indices are in my cluster?"
        }
    ],
    "tools": [],
    "context": [],
    "state": {},
    "forwardedProps": {}
}
```
{% include copy-curl.html %}

## 範例回應：AG-UI 代理程式

AG-UI 代理程式使用 AG-UI 協定格式傳回 SSE：

```json
data: {"type":"RUN_STARTED","timestamp":1734567890123,"threadId":"thread-xxxxx","runId":"run-xxxxx"}

data: {"type":"TEXT_MESSAGE_START","timestamp":1734567890124,"messageId":"msg-xxxxx","role":"assistant"}

data: {"type":"TEXT_MESSAGE_CONTENT","timestamp":1734567890125,"messageId":"msg-xxxxx","delta":"Your cluster has 9 indices."}

data: {"type":"TEXT_MESSAGE_END","timestamp":1734567890140,"messageId":"msg-xxxxx"}

data: {"type":"RUN_FINISHED","timestamp":1734567890251,"threadId":"thread-xxxxx","runId":"run-xxxxx"}
```

如需完整的 AG-UI 代理程式文件，包括設定、必要條件、欄位定義與實作細節，請參閱 [AG-UI 代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/ag-ui/)。

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明                                                                                                 |
| :--- | :--- |:------------------------------------------------------------------------------------------------------------|
| `inference_results` | 陣列 | 包含代理程式傳回的串流回應資料。                                                       |
| `inference_results.output` | 陣列 | 包含每個推論結果的輸出物件。                                                      |
| `inference_results.output.name` | 字串 | 輸出欄位的名稱。可以是 `memory_id`、`parent_interaction_id`、`response` 或 `token_usage`。                   |
| `inference_results.output.result` | 字串 | `memory_id` 與 `parent_interaction_id` 欄位的值。                                        |
| `inference_results.output.dataAsMap` | 物件 | 包含回應內容與中繼資料 (出現在 `response` 與 `token_usage` 輸出中)。                               |
| `inference_results.output.dataAsMap.content` | 字串 | 代理程式的回應內容，可能包含工具呼叫、工具結果或最終文字輸出。  |
| `inference_results.output.dataAsMap.is_last` | 布林值 | 指出這是否為串流中的最後一個區塊：最後一個區塊為 `true`，若還有更多區塊則為 `false`。 |
| `inference_results.output.dataAsMap.token_usage` | 物件 | 代理程式執行的詞元使用量指標。以獨立的串流區塊形式在最終完成區塊之前傳送。僅在 `include_token_usage` 設定為 `true` 時才會出現。**於 3.6 版推出** |

### 串流回應中的詞元使用量
**3.6 版新增**
{: .label .label-purple }

若要在串流回應中啟用詞元使用量追蹤，請在請求中將 `parameters.include_token_usage` 欄位設定為 `true`。啟用後，串流回應的順序如下：

1. 內容區塊串流傳送 (含 `is_last: false`)
2. 傳送一個包含詳細指標的 `token_usage` 區塊
3. 傳送最終完成區塊 (內容為空且 `is_last: true`)

詞元使用量區塊的結構與非串流 API 回應相同：

- **`per_turn_usage`**：代理程式執行期間每次 LLM 呼叫的詞元使用量記錄陣列。每筆記錄包含 `turn` (序號)、`model_id`、`model_name`、`model_url`、`input_tokens`、`output_tokens`、`total_tokens`，以及選用的快取相關欄位。
- **`per_model_usage`**：依模型分組的彙總詞元使用量。每筆記錄包含 `model_id`、`model_name`、`model_url`、`call_count` (LLM 呼叫次數)、`input_tokens`、`output_tokens`、`total_tokens`，以及選用的快取相關欄位。

如需詞元使用量欄位的完整說明，以及不同模型供應商如何計算詞元，請參閱 Execute Agent API 文件中的 [追蹤詞元使用量]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/#tracking-token-usage)。
