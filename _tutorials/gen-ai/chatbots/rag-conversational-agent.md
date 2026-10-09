---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用對話式流程代理程式的 RAG 聊天機器人"
parent: Chatbots
grand_parent: Generative AI
nav_order: 160
has_children: false
has_toc: false
redirect_from:
  - /ml-commons-plugin/tutorials/rag-conversational-agent/
  - /vector-search/tutorials/chatbots/rag-conversational-agent/
---

# 使用對話式流程代理程式的 RAG 聊天機器人

本教學說明如何使用對話式流程代理程式，以您的 OpenSearch 資料作為知識庫來建立檢索增強生成 (RAG) 應用程式。

請將以 `your_` 為前綴的預留位置替換為您自己的值。
{: .note}

建立 RAG 對話式搜尋的另一種方式是使用 RAG 管線。如需更多資訊，請參閱 [使用 Cohere Command 模型的對話式搜尋]({{site.url}}{{site.baseurl}}/ml-commons-plugin/tutorials/conversational-search-cohere/)。

## 必要條件

在本教學中，您將建立一個 RAG 應用程式，提供 OpenSearch [向量索引]({{site.url}}{{site.baseurl}}/search-plugins/knn/knn-index/) 作為大型語言模型 (LLM) 的知識庫。資料擷取將使用 [語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)。如需完整的語意搜尋設定，請參閱 [本教學]({{site.url}}{{site.baseurl}}/search-plugins/neural-search-tutorial/)。

首先，您需要更新叢集設定。如果您沒有專用的機器學習 (ML) 節點，請設定 `"plugins.ml_commons.only_run_on_ml_node": false`。為避免觸發原生記憶體斷路器，請將 `"plugins.ml_commons.native_memory_threshold"` 設為 100%：

```json
PUT _cluster/settings
{
    "persistent": {
        "plugins.ml_commons.only_run_on_ml_node": false,
        "plugins.ml_commons.native_memory_threshold": 100,
        "plugins.ml_commons.agent_framework_enabled": true
    }
}
```
{% include copy-curl.html %}

## 步驟 1：準備知識庫

使用下列步驟準備用於補充 LLM 知識的知識庫。

### 步驟 1.1：註冊文字嵌入模型

註冊一個可將文字轉換為向量嵌入的文字嵌入模型：

```json
POST /_plugins/_ml/models/_register
{
  "name": "huggingface/sentence-transformers/all-MiniLM-L12-v2",
  "version": "1.0.2",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

請記下文字嵌入模型的 ID；後續步驟會用到它。

或者，您可以呼叫 [Get Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 來取得模型 ID：

```json
GET /_plugins/_ml/tasks/your_task_id
```
{% include copy-curl.html %}

部署模型：

```json
POST /_plugins/_ml/models/your_text_embedding_model_id/_deploy
```
{% include copy-curl.html %}

測試模型：

```json
POST /_plugins/_ml/models/your_text_embedding_model_id/_predict
{
  "text_docs":[ "today is sunny"],
  "return_number": true,
  "target_response": ["sentence_embedding"]
}
```
{% include copy-curl.html %}

如需在 OpenSearch 叢集內使用模型的更多資訊，請參閱 [預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/)。

### 步驟 1.2：建立資料匯入管線

建立一個包含文字嵌入處理器的資料匯入管線，該處理器可叫用上一個步驟建立的模型，從文字欄位產生嵌入：

```json
PUT /_ingest/pipeline/test_population_data_pipeline
{
    "description": "text embedding pipeline",
    "processors": [
        {
            "text_embedding": {
                "model_id": "your_text_embedding_model_id",
                "field_map": {
                    "population_description": "population_description_embedding"
                }
            }
        }
    ]
}
```
{% include copy-curl.html %}

如需資料匯入管線的更多資訊，請參閱 [資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)。

### 步驟 1.3：建立向量索引

建立向量索引，並將該資料匯入管線指定為預設管線：

```json
PUT test_population_data
{
  "mappings": {
    "properties": {
      "population_description": {
        "type": "text"
      },
      "population_description_embedding": {
        "type": "knn_vector",
        "dimension": 384
      }
    }
  },
  "settings": {
    "index": {
      "knn.space_type": "cosinesimil",
      "default_pipeline": "test_population_data_pipeline",
      "knn": "true"
    }
  }
}
```
{% include copy-curl.html %}

如需向量索引的更多資訊，請參閱 [建立向量索引]({{site.url}}{{site.baseurl}}/search-plugins/knn/knn-index/)。

### 步驟 1.4：匯入資料

將測試資料匯入向量索引：

```json
POST _bulk
{"index": {"_index": "test_population_data"}}
{"population_description": "Chart and table of population level and growth rate for the Ogden-Layton metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of Ogden-Layton in 2023 is 750,000, a 1.63% increase from 2022.\nThe metro area population of Ogden-Layton in 2022 was 738,000, a 1.79% increase from 2021.\nThe metro area population of Ogden-Layton in 2021 was 725,000, a 1.97% increase from 2020.\nThe metro area population of Ogden-Layton in 2020 was 711,000, a 2.16% increase from 2019."}
{"index": {"_index": "test_population_data"}}
{"population_description": "Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."}
{"index": {"_index": "test_population_data"}}
{"population_description": "Chart and table of population level and growth rate for the Chicago metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Chicago in 2023 is 8,937,000, a 0.4% increase from 2022.\\nThe metro area population of Chicago in 2022 was 8,901,000, a 0.27% increase from 2021.\\nThe metro area population of Chicago in 2021 was 8,877,000, a 0.14% increase from 2020.\\nThe metro area population of Chicago in 2020 was 8,865,000, a 0.03% increase from 2019."}
{"index": {"_index": "test_population_data"}}
{"population_description": "Chart and table of population level and growth rate for the Miami metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Miami in 2023 is 6,265,000, a 0.8% increase from 2022.\\nThe metro area population of Miami in 2022 was 6,215,000, a 0.78% increase from 2021.\\nThe metro area population of Miami in 2021 was 6,167,000, a 0.74% increase from 2020.\\nThe metro area population of Miami in 2020 was 6,122,000, a 0.71% increase from 2019."}
{"index": {"_index": "test_population_data"}}
{"population_description": "Chart and table of population level and growth rate for the Austin metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Austin in 2023 is 2,228,000, a 2.39% increase from 2022.\\nThe metro area population of Austin in 2022 was 2,176,000, a 2.79% increase from 2021.\\nThe metro area population of Austin in 2021 was 2,117,000, a 3.12% increase from 2020.\\nThe metro area population of Austin in 2020 was 2,053,000, a 3.43% increase from 2019."}
{"index": {"_index": "test_population_data"}}
{"population_description": "Chart and table of population level and growth rate for the Seattle metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Seattle in 2023 is 3,519,000, a 0.86% increase from 2022.\\nThe metro area population of Seattle in 2022 was 3,489,000, a 0.81% increase from 2021.\\nThe metro area population of Seattle in 2021 was 3,461,000, a 0.82% increase from 2020.\\nThe metro area population of Seattle in 2020 was 3,433,000, a 0.79% increase from 2019."}
```
{% include copy-curl.html %}

## 步驟 2：準備 LLM

本教學使用 [Amazon Bedrock Claude 模型](https://aws.amazon.com/bedrock/claude/) 進行對話式搜尋。您也可以使用其他 LLM。如需使用外部託管模型的詳細資訊，請參閱[連線至外部託管模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。

### 步驟 2.1：建立連接器

為 Claude 模型建立連接器：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Bedrock Claude Sonnet 5",
  "description": "The connector to BedRock service for claude model",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "us-east-1",
    "service_name": "bedrock",
    "model": "us.anthropic.claude-sonnet-5",
    "response_filter": "$.output.message.content[0].text"
  },
  "credential": {
    "access_key": "your_aws_access_key",
    "secret_key": "your_aws_secret_key",
    "session_token": "your_aws_session_token"
  },
  "actions": [{
    "action_type": "predict",
    "method": "POST",
    "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/converse",
    "headers": { "content-type": "application/json" },
    "request_body": "{\"messages\": [${parameters._chat_history:-}{\"role\":\"user\",\"content\":[{\"text\":\"${parameters.prompt:-}\"}]}${parameters._interactions:-}]${parameters.tool_configs:-}}"
  }]
}
```
{% include copy-curl.html %}

請記下連接器 ID；您將使用它來註冊模型。

### 步驟 2.2：註冊模型

註冊託管於 Amazon Bedrock 的 Claude 模型：

```json
POST /_plugins/_ml/models/_register
{
    "name": "Bedrock Claude Instant model",
    "function_name": "remote",
    "description": "Bedrock Claude instant-v1 model",
    "connector_id": "your_LLM_connector_id"
}
```
{% include copy-curl.html %}

請記下 LLM 模型 ID；您將在後續步驟中使用它。

### 步驟 2.3：部署模型

部署 Claude 模型：

```json
POST /_plugins/_ml/models/your_LLM_model_id/_deploy
```
{% include copy-curl.html %}

### 步驟 2.4：測試模型

若要測試模型，請傳送 Predict API 請求：

```json
POST /_plugins/_ml/models/your_LLM_model_id/_predict
{
  "parameters": {
    "prompt": "\n\nHuman: how are you? \n\nAssistant:"
  }
}
```
{% include copy-curl.html %}

## 步驟 3：註冊代理程式

OpenSearch 提供下列代理程式類型：`flow`、`conversational_flow` 及 `conversational`。如需代理程式的詳細資訊，請參閱[代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/)。

本教學將使用 `conversational_flow` 代理程式。此代理程式包含下列項目：

- 中繼資訊：`name`、`type` 及 `description`。
- `app_type`：區分應用程式類型。
- `memory`：將使用者問題與 LLM 回應儲存為對話，讓代理程式可從記憶體擷取對話歷程記錄並繼續相同的對話。
- `tools`：定義要使用的工具清單。代理程式將依序執行這些工具。

若要註冊代理程式，請傳送下列請求：

```json
POST /_plugins/_ml/agents/_register
{
    "name": "population data analysis agent",
    "type": "conversational_flow",
    "description": "This is a demo agent for population data analysis",
    "app_type": "rag",
    "memory": {
        "type": "conversation_index"
    },
    "tools": [
        {
            "type": "VectorDBTool",
            "name": "population_knowledge_base",
            "parameters": {
                "model_id": "your_text_embedding_model_id",
                "index": "test_population_data",
                "embedding_field": "population_description_embedding",
                "source_field": [
                    "population_description"
                ],
                "input": "${parameters.question}"
            }
        },
        {
            "type": "MLModelTool",
            "name": "bedrock_claude_model",
            "description": "A general tool to answer any question",
            "parameters": {
                "model_id": "your_LLM_model_id",
                "prompt": "\n\nHuman:You are a professional data analysist. You will always answer question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say don't know. \n\nContext:\n${parameters.population_knowledge_base.output:-}\n\n${parameters.chat_history:-}\n\nHuman:${parameters.question}\n\nAssistant:"
            }
        }
    ]
}
```
{% include copy-curl.html %}

OpenSearch 會回應代理程式 ID：

```json
{
  "agent_id": "fQ75lI0BHcHmo_czdqcJ"
}
```

請記下代理程式 ID；您將在下一個步驟中使用它。

## 步驟 4：執行代理程式

您將執行代理程式來分析西雅圖人口的成長。當您執行此代理程式時，代理程式會建立新的對話。之後，您可以透過詢問其他問題來繼續此對話。

### 步驟 4.1：開始新的對話

首先，透過向 LLM 詢問問題來開始新的對話：

```json
POST /_plugins/_ml/agents/your_agent_id/_execute
{
  "parameters": {
    "question": "what's the population increase of Seattle from 2021 to 2023?"
  }
}
```
{% include copy-curl.html %}

回應包含 LLM 產生的答案：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "memory_id",
          "result": "gQ75lI0BHcHmo_cz2acL" 
        },
        {
          "name": "parent_message_id",
          "result": "gg75lI0BHcHmo_cz2acZ"
        },
        {
          "name": "bedrock_claude_model",
          "result": """ Based on the context given:
- The metro area population of Seattle in 2021 was 3,461,000
- The current metro area population of Seattle in 2023 is 3,519,000
- So the population increase of Seattle from 2021 to 2023 is 3,519,000 - 3,461,000 = 58,000"""
        }
      ]
    }
  ]
}
```

回應包含下列欄位：

- `memory_id` 是記憶體 (對話) 的識別碼，會將單一對話中的所有訊息分組。請記下此 ID；您將在下一個步驟中使用它。
- `parent_message_id` 是目前訊息 (一個問題/答案) 的識別碼，代表人類與 LLM 之間的互動。一個記憶體可以包含多個訊息。

若要取得記憶體詳細資訊，請呼叫 [Get Memory API](ml-commons-plugin/api/memory-apis/get-memory/)：

```json
GET /_plugins/_ml/memory/gQ75lI0BHcHmo_cz2acL
```
{% include copy-curl.html %}

若要取得記憶體內的所有訊息，請呼叫 [Get Messages API](ml-commons-plugin/api/memory-apis/get-message/)：

```json
GET /_plugins/_ml/memory/gQ75lI0BHcHmo_cz2acL/messages
```
{% include copy-curl.html %}

若要取得訊息詳細資訊，請呼叫 [Get Message API](ml-commons-plugin/api/memory-apis/get-message/)：

```json
GET /_plugins/_ml/memory/message/gg75lI0BHcHmo_cz2acZ
```
{% include copy-curl.html %}

基於偵錯目的，您可以呼叫 [Get Message Traces API](ml-commons-plugin/api/memory-apis/get-message-traces/) 來取得訊息的追蹤資料：

```json
GET /_plugins/_ml/memory/message/gg75lI0BHcHmo_cz2acZ/traces
```
{% include copy-curl.html %}

### 4.2 透過詢問新問題來繼續對話

若要繼續相同的對話，請提供上一個步驟中的記憶體 ID。

此外，您可以提供下列參數：

- `message_history_limit`：指定您希望代理程式在新的問題/答案回合中包含多少歷史訊息。
- `prompt`：使用此參數來自訂 LLM 提示。例如，下列範例會新增指令 `always learn useful information from chat history` 
及新參數 `next_action`：

```json
POST /_plugins/_ml/agents/your_agent_id/_execute
{
  "parameters": {
    "question": "What's the population of New York City in 2023?",
    "next_action": "then compare with Seattle population of 2023",
    "memory_id": "gQ75lI0BHcHmo_cz2acL",
    "message_history_limit": 5,
    "prompt": "\n\nHuman:You are a professional data analysist. You will always answer question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say don't know. \n\nContext:\n${parameters.population_knowledge_base.output:-}\n\n${parameters.chat_history:-}\n\nHuman:always learn useful information from chat history\nHuman:${parameters.question}, ${parameters.next_action}\n\nAssistant:"
  }
}
```
{% include copy-curl.html %}

回應包含 LLM 產生的答案：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "memory_id",
          "result": "gQ75lI0BHcHmo_cz2acL"
        },
        {
          "name": "parent_message_id",
          "result": "wQ4JlY0BHcHmo_cz8Kc-"
        },
        {
          "name": "bedrock_claude_model",
          "result": """ Based on the context given:
- The current metro area population of New York City in 2023 is 18,937,000
- The current metro area population of Seattle in 2023 is 3,519,000
- So the population of New York City in 2023 (18,937,000) is much higher than the population of Seattle in 2023 (3,519,000)"""
        }
      ]
    }
  ]
}
```

如果您知道代理程式應使用哪個工具來執行特定的 Predict API 請求，您可以在執行代理程式時指定該工具。例如，如果您想將上述答案翻譯成中文，就不需要從知識庫擷取任何資料。若只要執行 Claude 模型，請在 `selected_tools` 參數中指定 `bedrock_claude_model` 工具：

```json
POST /_plugins/_ml/agents/your_agent_id/_execute
{
  "parameters": {
    "question": "Translate last answer into Chinese?",
    "selected_tools": ["bedrock_claude_model"]
  }
}
```
{% include copy-curl.html %}

代理程式將依 `selected_tools` 中定義的新順序逐一執行工具。
{: .note}

## 設定多個知識庫

您可以為代理程式設定多個知識庫。例如，如果您同時擁有產品描述與評論資料，可以使用下列兩個工具來設定代理程式：

```json
{
    "name": "My product agent",
    "type": "conversational_flow",
    "description": "This is an agent with product description and comments knowledge bases.",
    "memory": {
        "type": "conversation_index"
    },
    "app_type": "rag",
    "tools": [
        {
            "type": "VectorDBTool",
            "name": "product_description_vectordb",
            "parameters": {
                "model_id": "your_embedding_model_id",
                "index": "product_description_data",
                "embedding_field": "product_description_embedding",
                "source_field": [
                    "product_description"
                ],
                "input": "${parameters.question}"
            }
        },
        {
            "type": "VectorDBTool",
            "name": "product_comments_vectordb",
            "parameters": {
                "model_id": "your_embedding_model_id",
                "index": "product_comments_data",
                "embedding_field": "product_comment_embedding",
                "source_field": [
                    "product_comment"
                ],
                "input": "${parameters.question}"
            }
        },
        {
            "type": "MLModelTool",
            "description": "A general tool to answer any question",
            "parameters": {
                "model_id": "{{llm_model_id}}",
                "prompt": "\n\nHuman:You are a professional product recommendation engine. You will always recommend product based on the given context. If you don't have enough context, you will ask Human to provide more information. If you don't see any related product to recommend, just say we don't have such product. \n\n Context:\n${parameters.product_description_vectordb.output}\n\n${parameters.product_comments_vectordb.output}\n\nHuman:${parameters.question}\n\nAssistant:"
            }
        }
    ]
}
```
{% include copy-curl.html %}

當您執行代理程式時，代理程式會查詢產品描述與評論資料，然後將查詢結果與問題傳送給 LLM。

若要查詢特定的知識庫，請在 `selected_tools` 中指定。例如，如果問題只與產品評論相關，您可以只從 `product_comments_vectordb` 擷取資訊：

```json
POST /_plugins/_ml/agents/your_agent_id/_execute
{
  "parameters": {
    "question": "What feature people like the most for Amazon Echo Dot",
    "selected_tools": ["product_comments_vectordb", "MLModelTool"]
  }
}
```
{% include copy-curl.html %}

## 在索引上執行查詢

使用 `SearchIndexTool` 在任何索引上執行任何 OpenSearch 查詢。

### 設定：註冊代理程式

```json
POST /_plugins/_ml/agents/_register
{
    "name": "Demo agent",
    "type": "conversational_flow",
    "description": "This agent supports running any search query",
    "memory": {
        "type": "conversation_index"
    },
    "app_type": "rag",
    "tools": [
        {
            "type": "SearchIndexTool",
            "parameters": {
                "input": "{\"index\": \"${parameters.index}\", \"query\": ${parameters.query} }"
            }
        },
        {
            "type": "MLModelTool",
            "description": "A general tool to answer any question",
            "parameters": {
                "model_id": "your_llm_model_id",
                "prompt": "\n\nHuman:You are a professional data analysist. You will always answer question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say don't know. \n\n Context:\n${parameters.SearchIndexTool.output:-}\n\nHuman:${parameters.question}\n\nAssistant:"
            }
        }
    ]
}
```
{% include copy-curl.html %}

### 執行 BM25 查詢

```json
POST /_plugins/_ml/agents/your_agent_id/_execute
{
    "parameters": {
        "question": "what's the population increase of Seattle from 2021 to 2023?",
        "index": "test_population_data",
        "query": {
            "query": {
                "match": {
                    "population_description": "${parameters.question}"
                }
            },
            "size": 2,
            "_source": "population_description"
        }
    }
}
```
{% include copy-curl.html %}

### 僅公開 `question` 參數

若要僅公開 `question` 參數，請如下定義代理程式：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Demo agent",
  "type": "conversational_flow",
  "description": "This is a test agent support running any search query",
  "memory": {
    "type": "conversation_index"
  },
  "app_type": "rag",
  "tools": [
    {
      "type": "SearchIndexTool",
      "parameters": {
        "input": "{\"index\": \"${parameters.index}\", \"query\": ${parameters.query} }",
        "index": "test_population_data",
        "query": {
          "query": {
            "match": {
              "population_description": "${parameters.question}"
            }
          },
          "size": 2,
          "_source": "population_description"
        }
      }
    },
    {
      "type": "MLModelTool",
      "description": "A general tool to answer any question",
      "parameters": {
        "model_id": "your_llm_model_id",
        "prompt": "\n\nHuman:You are a professional data analyst. You will always answer question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say don't know. \n\n Context:\n${parameters.SearchIndexTool.output:-}\n\nHuman:${parameters.question}\n\nAssistant:"
      }
    }
  ]
}
```
{% include copy-curl.html %}

現在您可以執行代理程式，並只指定 `question` 參數：

```json
POST /_plugins/_ml/agents/your_agent_id/_execute
{
    "parameters": {
        "question": "what's the population increase of Seattle from 2021 to 2023?"
    }
}
```
{% include copy-curl.html %}

### 執行向量搜尋

```json
POST /_plugins/_ml/agents/your_agent_id/_execute
{
    "parameters": {
        "question": "what's the population increase of Seattle from 2021 to 2023??",
        "index": "test_population_data",
        "query": {
            "query": {
                "neural": {
                    "population_description_embedding": {
                        "query_text": "${parameters.question}",
                        "model_id": "your_embedding_model_id",
                        "k": 10
                    }
                }
            },
            "size": 2,
            "_source": ["population_description"]
        }
    }
}
```
{% include copy-curl.html %}

若要公開 `question` 參數，請參閱 [僅公開 `question` 參數](#exposing-only-the-question-parameter)。

### 執行混合搜尋查詢

混合搜尋結合關鍵字搜尋與向量搜尋，以改善搜尋相關性。如需更多資訊，請參閱 [混合搜尋]({{site.url}}{{site.baseurl}}/search-plugins/hybrid-search/)。

設定搜尋管線：

```json
PUT /_search/pipeline/nlp-search-pipeline
{
    "description": "Post processor for hybrid search",
    "phase_results_processors": [
      {
        "normalization-processor": {
          "normalization": {
            "technique": "min_max"
          },
          "combination": {
            "technique": "arithmetic_mean",
            "parameters": {
              "weights": [
                0.3,
                0.7
              ]
            }
          }
        }
      }
    ]
  }
```
{% include copy-curl.html %}

使用混合查詢執行代理程式：

```json
POST /_plugins/_ml/agents/your_agent_id/_execute
{
    "parameters": {
        "question": "what's the population increase of Seattle from 2021 to 2023??",
        "index": "test_population_data",
        "query": {
            "_source": {
                "exclude": [
                    "population_description_embedding"
                ]
            },
            "size": 2,
            "query": {
                "hybrid": {
                    "queries": [
                        {
                            "match": {
                                "population_description": {
                                    "query": "${parameters.question}"
                                }
                            }
                        },
                        {
                            "neural": {
                                "population_description_embedding": {
                                    "query_text": "${parameters.question}",
                                    "model_id": "your_embedding_model_id",
                                    "k": 10
                                }
                            }
                        }
                    ]
                }
            }
        }
    }
}
```
{% include copy-curl.html %}

若要公開 `question` 參數，請參閱 [僅公開 `question` 參數](#exposing-only-the-question-parameter)。

### 自然語言查詢

`PPLTool` 可以將自然語言查詢 (NLQ) 轉譯為 [Piped Processing Language (PPL)]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) 並執行產生的 PPL 查詢。

#### 設定

開始之前，請前往 OpenSearch Dashboards 首頁，選取 `Add sample data`，然後新增 `Sample eCommerce orders`。

<!-- vale off -->
#### 步驟 1：使用 PPLTool 註冊代理程式
<!-- vale on -->

`PPLTool` 具有下列參數：

- `model_type`（列舉）：`CLAUDE`、`OPENAI` 或 `FINETUNE`。
- `execute`（布林值）：若為 `true`，則執行產生的 PPL 查詢。
- `input`（字串）：您必須提供 `index` 和 `question` 作為輸入。

本教學將使用 Bedrock Claude，因此請將 `model_type` 設為 `CLAUDE`：

```json
POST /_plugins/_ml/agents/_register
{
    "name": "Demo agent for NLQ",
    "type": "conversational_flow",
    "description": "This is a test flow agent for NLQ",
    "memory": {
        "type": "conversation_index"
    },
    "app_type": "rag",
    "tools": [
        {
            "type": "PPLTool",
            "parameters": {
                "model_id": "your_ppl_model_id",
                "model_type": "CLAUDE",
                "execute": true,
                "input": "{\"index\": \"${parameters.index}\", \"question\": ${parameters.question} }"
            }
        },
        {
            "type": "MLModelTool",
            "description": "A general tool to answer any question",
            "parameters": {
                "model_id": "your_llm_model_id",
                "prompt": "\n\nHuman:You are a professional data analysist. You will always answer question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say don't know. \n\n Context:\n${parameters.PPLTool.output:-}\n\nHuman:${parameters.question}\n\nAssistant:"
            }
        }
    ]
}
```
{% include copy-curl.html %}

### 步驟 2：使用 NLQ 執行代理程式

執行代理程式：

```json
POST /_plugins/_ml/agents/your_agent_id/_execute
{
    "parameters": {
        "question": "How many orders do I have in last week",
        "index": "opensearch_dashboards_sample_data_ecommerce"
    }
}
```
{% include copy-curl.html %}

回應包含 LLM 產生的答案：

```json
{
    "inference_results": [
        {
            "output": [
                {
                    "name": "memory_id",
                    "result": "sqIioI0BJhBwrVXYeYOM"
                },
                {
                    "name": "parent_message_id",
                    "result": "s6IioI0BJhBwrVXYeYOW"
                },
                {
                    "name": "MLModelTool",
                    "result": " Based on the given context, the number of orders in the last week is 3992. The data shows a query that counts the number of orders where the order date is greater than 1 week ago. The query result shows the count as 3992."
                }
            ]
        }
    ]
}
```

如需更多資訊，請呼叫 [Get Message Traces API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/get-message-traces/) 取得追蹤資料：

```json
GET _plugins/_ml/memory/message/s6IioI0BJhBwrVXYeYOW/traces
```
{% include copy-curl.html %}