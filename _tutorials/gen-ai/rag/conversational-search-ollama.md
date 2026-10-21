---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Ollama 進行對話式搜尋"
parent: RAG
grand_parent: Generative AI
nav_order: 180
---

# 使用 Ollama 進行對話式搜尋

本教學說明如何使用在 [Ollama](https://ollama.com/) 中於本機託管的大型語言模型（LLM），設定結合檢索增強生成（RAG）的對話式搜尋。本教學使用 `qwen3:4b` 模型。如需詳細資訊，請參閱[對話式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/conversational-search/)。

本教學中的連接器會呼叫 Ollama 提供、與 OpenAI 相容的 Chat Completions API。同一個連接器也適用於其他提供 OpenAI 相容 API 的本機或自行託管伺服器，例如 llama.cpp 或 vLLM。若要使用這些伺服器之一，請變更 `endpoint` 和 `model` 連接器參數，以及信任的端點模式，使其符合您的伺服器。

請將以 `your_` 為前綴的預留位置替換為您自己的值。
{: .note}

或者，您也可以使用代理程式與工具建構 RAG／對話式搜尋。如需詳細資訊，請參閱[使用對話流程代理程式的 RAG 聊天機器人]({{site.url}}{{site.baseurl}}/tutorials/gen-ai/chatbots/rag-conversational-agent/)。

## 先決條件

開始之前，請設定模型伺服器、設定叢集設定，並匯入測試資料。

### 設定 Ollama

在執行 OpenSearch 的主機上安裝 Ollama，然後下載 `qwen3:4b` 模型：

```bash
ollama pull qwen3:4b
```
{% include copy.html %}

根據預設，Ollama 會在 `127.0.0.1:11434` 上接聽，本教學使用此位址作為連接器端點。

如果 OpenSearch 在 Docker 容器中執行，`127.0.0.1` 指的是 OpenSearch 容器，而非執行 Ollama 的主機或容器。在此情況下，請在連接器端點和信任的端點模式中，使用 OpenSearch 容器可連線的 Ollama 位址。如果 Ollama 在與 OpenSearch 相同的 Docker 網路中的容器內執行，請使用 Ollama 容器名稱，例如 `ollama:11434`。如果 Ollama 在主機上執行，請設定 `OLLAMA_HOST` 環境變數，將 Ollama 設定為在容器可連線的位址上接聽。
{: .note}

### 設定叢集設定

根據預設，ML Commons 會拒絕傳送至解析為私有或回送 IP 位址（例如 `127.0.0.1`）之主機的連接器請求。此外，連接器 URL 必須符合 `plugins.ml_commons.trusted_connector_endpoints_regex` 設定中的模式，而預設模式不包含本機 `http://` 端點。

若要允許連接器傳送請求至本機 Ollama 伺服器，請啟用連接器使用私有 IP 位址的功能，並將 Ollama 端點新增至信任的端點：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.ml_commons.connector.private_ip_enabled": true,
    "plugins.ml_commons.trusted_connector_endpoints_regex": [
      "^http://127\\.0\\.0\\.1:11434/.*$"
    ]
  }
}
```
{% include copy-curl.html %}

`plugins.ml_commons.trusted_connector_endpoints_regex` 設定會取代整份信任的端點清單，包括預設模式。如果您的叢集使用連接器連線至其他端點，也請將這些端點的模式納入清單中。如需詳細資訊，請參閱[新增信任的端點]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/#adding-trusted-endpoints)。
{: .important}

若要檢視目前的信任端點清單（包括預設模式），請傳送下列請求：

```json
GET /_cluster/settings?include_defaults=true&filter_path=*.plugins.ml_commons.trusted_connector_endpoints_regex
```
{% include copy-curl.html %}

### 匯入測試資料

匯入測試資料：

```json
POST _bulk
{"index": {"_index": "qa_demo", "_id": "1"}}
{"text": "Chart and table of population level and growth rate for the Ogden-Layton metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of Ogden-Layton in 2023 is 750,000, a 1.63% increase from 2022.\nThe metro area population of Ogden-Layton in 2022 was 738,000, a 1.79% increase from 2021.\nThe metro area population of Ogden-Layton in 2021 was 725,000, a 1.97% increase from 2020.\nThe metro area population of Ogden-Layton in 2020 was 711,000, a 2.16% increase from 2019."}
{"index": {"_index": "qa_demo", "_id": "2"}}
{"text": "Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."}
{"index": {"_index": "qa_demo", "_id": "3"}}
{"text": "Chart and table of population level and growth rate for the Chicago metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Chicago in 2023 is 8,937,000, a 0.4% increase from 2022.\\nThe metro area population of Chicago in 2022 was 8,901,000, a 0.27% increase from 2021.\\nThe metro area population of Chicago in 2021 was 8,877,000, a 0.14% increase from 2020.\\nThe metro area population of Chicago in 2020 was 8,865,000, a 0.03% increase from 2019."}
{"index": {"_index": "qa_demo", "_id": "4"}}
{"text": "Chart and table of population level and growth rate for the Miami metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Miami in 2023 is 6,265,000, a 0.8% increase from 2022.\\nThe metro area population of Miami in 2022 was 6,215,000, a 0.78% increase from 2021.\\nThe metro area population of Miami in 2021 was 6,167,000, a 0.74% increase from 2020.\\nThe metro area population of Miami in 2020 was 6,122,000, a 0.71% increase from 2019."}
{"index": {"_index": "qa_demo", "_id": "5"}}
{"text": "Chart and table of population level and growth rate for the Austin metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Austin in 2023 is 2,228,000, a 2.39% increase from 2022.\\nThe metro area population of Austin in 2022 was 2,176,000, a 2.79% increase from 2021.\\nThe metro area population of Austin in 2021 was 2,117,000, a 3.12% increase from 2020.\\nThe metro area population of Austin in 2020 was 2,053,000, a 3.43% increase from 2019."}
{"index": {"_index": "qa_demo", "_id": "6"}}
{"text": "Chart and table of population level and growth rate for the Seattle metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Seattle in 2023 is 3,519,000, a 0.86% increase from 2022.\\nThe metro area population of Seattle in 2022 was 3,489,000, a 0.81% increase from 2021.\\nThe metro area population of Seattle in 2021 was 3,461,000, a 0.82% increase from 2020.\\nThe metro area population of Seattle in 2020 was 3,433,000, a 0.79% increase from 2019."}
```
{% include copy-curl.html %}

## 步驟 1：建立連接器並註冊模型

首先，為託管在 Ollama 中的 `qwen3:4b` 模型建立連接器：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Ollama Qwen3",
  "description": "Connector for the Qwen3 model hosted in Ollama",
  "version": "1.0",
  "protocol": "http",
  "parameters": {
    "endpoint": "127.0.0.1:11434",
    "model": "qwen3:4b"
  },
  "credential": {
    "openAI_key": "your_api_key"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "http://${parameters.endpoint}/v1/chat/completions",
      "headers": {
        "Authorization": "Bearer ${credential.openAI_key}"
      },
      "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": ${parameters.messages} }"
    }
  ]
}
```
{% include copy-curl.html %}

Ollama 不會檢查 API 金鑰，因此您可以在 `openAI_key` 中提供任何值。如果您的模型伺服器需要 API 金鑰，請在 `openAI_key` 中提供該金鑰；連接器會以 `Authorization` 標頭將其作為 bearer 權杖傳送。如需更多資訊，請參閱[此藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/ollama_connector_chat_blueprint.md)。

`qwen3:4b` 模型會在答案之前產生其推理過程，因此在沒有 GPU 的主機上，回應可能需要數分鐘。如果對模型的請求因逾時而失敗，請新增一個 `client_config` 物件並設定較大的 `read_timeout` 值（單位為秒），以提高連接器的讀取逾時時間（預設為 30 秒），例如 `"client_config": {"read_timeout": 300}`。如需更多資訊，請參閱[請求本文欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#request-body-fields)。
{: .note}

記下連接器 ID；您將使用它來註冊模型。

接下來，註冊並部署模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "Ollama Qwen3 model",
  "function_name": "remote",
  "description": "Qwen3 model hosted in Ollama",
  "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

記下模型 ID；您將在後續步驟中使用它。

測試模型：

```json
POST /_plugins/_ml/models/your_model_id/_predict
{
  "parameters": {
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Who won the world series in 2020?"
      }
    ]
  }
}
```
{% include copy-curl.html %}

回應包含模型產生的文字。Ollama 會在 `content` 欄位中傳回答案，並將模型的推理過程放在另一個 `reasoning` 欄位中。以下回應已經過刪減：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "id": "chatcmpl-417",
            "object": "chat.completion",
            "created": 1792110903,
            "model": "qwen3:4b",
            "system_fingerprint": "fp_ollama",
            "choices": [
              {
                "index": 0,
                "message": {
                  "role": "assistant",
                  "content": "The **Los Angeles Dodgers** won the 2020 World Series, defeating the **Tampa Bay Rays** in a best-of-seven series (4–2).",
                  "reasoning": "Okay, the user is asking who won the World Series in 2020. Let me think about this carefully."
                },
                "finish_reason": "stop"
              }
            ],
            "usage": {
              "prompt_tokens": 33,
              "completion_tokens": 801,
              "total_tokens": 834
            }
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

RAG 處理器在後續步驟中傳回的答案只包含 `content` 文字，不包含推理過程。

## 步驟 2：設定 RAG

若要設定 RAG，請建立一個包含 RAG 處理器的搜尋管線：

```json
PUT /_search/pipeline/my-conversation-search-pipeline-ollama
{
  "response_processors": [
    {
      "retrieval_augmented_generation": {
        "tag": "Demo pipeline",
        "description": "Demo pipeline using Ollama",
        "model_id": "your_model_id",
        "context_field_list": [
          "text"
        ],
        "system_prompt": "You are a helpful assistant",
        "user_instructions": "Generate a concise and informative answer in less than 100 words for the given question"
      }
    }
  ]
}
```
{% include copy-curl.html %}

執行基本的 RAG 搜尋，不儲存對話歷史。RAG 處理器會將 `llm_model` 值作為 `model` 參數傳遞給連接器，因此請將 `llm_model` 設定為 Ollama 中的模型名稱：

```json
GET /qa_demo/_search?search_pipeline=my-conversation-search-pipeline-ollama
{
  "query": {
    "match": {
      "text": "What's the population increase of New York City from 2021 to 2023?"
    }
  },
  "size": 1,
  "_source": [
    "text"
  ],
  "ext": {
    "generative_qa_parameters": {
      "llm_model": "qwen3:4b",
      "llm_question": "What's the population increase of New York City from 2021 to 2023?",
      "context_size": 5,
      "timeout": 15
    }
  }
}
```
{% include copy-curl.html %}

回應包含模型答案與相關文件：

```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 6,
      "relation": "eq"
    },
    "max_score": 4.110037,
    "hits": [
      {
        "_index": "qa_demo",
        "_id": "2",
        "_score": 4.110037,
        "_source": {
          "text": "Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."
        }
      }
    ]
  },
  "ext": {
    "retrieval_augmented_generation": {
      "answer": "The population increased by 114,000 people (from 18,823,000 in 2021 to 18,937,000 in 2023). This represents a 0.60% growth over the two-year period."
    }
  }
}
```

## 步驟 3：設定對話式搜尋

請依照下列步驟，透過將對話歷史儲存在記憶體中來設定對話式搜尋。

1. 建立記憶體：

    ```json
    POST /_plugins/_ml/memory/
    {
      "name": "Conversation about NYC population"
    }
    ```
    {% include copy-curl.html %}

    回應包含記憶體 ID：

    ```json
    {
      "memory_id": "rBAbY5UBSzdNxlHvIyI3"
    }
    ```

2. 若要儲存對話歷史，請在搜尋請求中包含記憶體 ID：

    ```json
    GET /qa_demo/_search?search_pipeline=my-conversation-search-pipeline-ollama
    {
      "query": {
        "match": {
          "text": "What's the population increase of New York City from 2021 to 2023?"
        }
      },
      "size": 1,
      "_source": [
        "text"
      ],
      "ext": {
        "generative_qa_parameters": {
          "llm_model": "qwen3:4b",
          "llm_question": "What's the population increase of New York City from 2021 to 2023?",
          "context_size": 5,
          "timeout": 15,
          "memory_id": "rBAbY5UBSzdNxlHvIyI3"
        }
      }
    }
    ```
    {% include copy-curl.html %}

    回應包含模型答案、相關文件，以及儲存在記憶體中的訊息 ID：

    ```json
    {
      "took": 1,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 6,
          "relation": "eq"
        },
        "max_score": 4.110037,
        "hits": [
          {
            "_index": "qa_demo",
            "_id": "2",
            "_score": 4.110037,
            "_source": {
              "text": "Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."
            }
          }
        ]
      },
      "ext": {
        "retrieval_augmented_generation": {
          "answer": "New York City's metro area population increased by 114,000 from 2021 (18,823,000) to 2023 (18,937,000), representing a 0.61% rise over that two-year period.",
          "message_id": "rRAcY5UBSzdNxlHvyiI1"
        }
      }
    }
    ```

3. 若要繼續對話，請在下一次搜尋中提供相同的記憶體 ID：

    ```json
    GET /qa_demo/_search?search_pipeline=my-conversation-search-pipeline-ollama
    {
      "query": {
        "match": {
          "text": "What's the population increase of Miami from 2021 to 2023?"
        }
      },
      "size": 1,
      "_source": [
        "text"
      ],
      "ext": {
        "generative_qa_parameters": {
          "llm_model": "qwen3:4b",
          "llm_question": "compare population increase of New York City and Miami",
          "context_size": 5,
          "timeout": 15,
          "memory_id": "rBAbY5UBSzdNxlHvIyI3"
        }
      }
    }
    ```
    {% include copy-curl.html %}

    模型會利用記憶體中的對話歷史，將邁阿密的人口資料與先前討論過的紐約市統計數據進行比較：

    ```json
    {
      "took": 1,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 6,
          "relation": "eq"
        },
        "max_score": 1.666383,
        "hits": [
          {
            "_index": "qa_demo",
            "_id": "4",
            "_score": 1.666383,
            "_source": {
              "text": "Chart and table of population level and growth rate for the Miami metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Miami in 2023 is 6,265,000, a 0.8% increase from 2022.\\nThe metro area population of Miami in 2022 was 6,215,000, a 0.78% increase from 2021.\\nThe metro area population of Miami in 2021 was 6,167,000, a 0.74% increase from 2020.\\nThe metro area population of Miami in 2020 was 6,122,000, a 0.71% increase from 2019."
            }
          }
        ]
      },
      "ext": {
        "retrieval_augmented_generation": {
          "answer": "New York City grew by 114,000 (0.61%) from 18.82M in 2021 to 18.94M in 2023. Miami increased by 98,000 (0.8% annually) from 6.17M in 2021 to 6.27M in 2023.",
          "message_id": "rhAdY5UBSzdNxlHv5SKa"
        }
      }
    }
    ```

## 相關文件

- [搭配 RAG 的對話式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/conversational-search/)
- [擷取增強生成處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rag-processor/)
- [第三方 ML 平台的連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)
