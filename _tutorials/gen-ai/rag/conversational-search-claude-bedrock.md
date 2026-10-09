---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Amazon Bedrock 上使用 Anthropic Claude 進行對話式搜尋"
parent: RAG
grand_parent: Generative AI
nav_order: 160
redirect_from:
  - /vector-search/tutorials/conversational-search/conversational-search-claude-bedrock/
  - /tutorials/vector-search/rag/conversational-search/conversational-search-claude-bedrock/
---

# 在 Amazon Bedrock 上使用 Anthropic Claude 進行對話式搜尋

本教學說明如何使用託管於 Amazon Bedrock 的 Anthropic Claude 模型，設定搭配檢索增強生成 (RAG) 的對話式搜尋。如需更多資訊，請參閱[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)。

請將開頭為前置字元 `your_` 的預留位置取代為您自己的值。
{: .note}

或者，您可以使用代理程式與工具來建置 RAG/對話式搜尋。如需更多資訊，請參閱[檢索增強生成聊天機器人]({{site.url}}{{site.baseurl}}/ml-commons-plugin/tutorials/rag-conversational-agent/)。

## 先決條件

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

您可以使用下列 Amazon Bedrock API 來設定對話式搜尋：

1. [Converse API](#option-1-amazon-bedrock-converse-api)
2. [Invoke API](#option-2-amazon-bedrock-invoke-api)

<!-- vale off -->
## 選項 1：Amazon Bedrock Converse API
<!-- vale on -->

請依照下列步驟，使用 Amazon Bedrock Converse API 進行對話式搜尋。

### 步驟 1.1：建立連接器並註冊模型

首先，為 Claude 模型建立連接器。在此範例中，您將使用 Anthropic Claude 3.5 Sonnet：

```json
POST _plugins/_ml/connectors/_create
{
    "name": "Amazon Bedrock claude v3",
    "description": "Test connector for Amazon Bedrock claude v3",
    "version": 1,
    "protocol": "aws_sigv4",
    "credential": {
        "access_key": "your_access_key",
        "secret_key": "your_secret_key",
        "session_token": "your_session_token"
    },
    "parameters": {
        "region": "your_aws_region",
        "service_name": "bedrock",
        "model": "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "system_prompt": "you are a helpful assistant.",
        "temperature": 0.0,
        "top_p": 0.9,
        "max_tokens": 1000
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "headers": {
                "content-type": "application/json"
            },
            "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/converse",
            "request_body": "{ \"system\": [{\"text\": \"${parameters.system_prompt}\"}], \"messages\": ${parameters.messages} , \"inferenceConfig\": {\"temperature\": ${parameters.temperature}, \"topP\": ${parameters.top_p}, \"maxTokens\": ${parameters.max_tokens}} }"
        }
    ]
}
```
{% include copy-curl.html %}

若要使用 Claude 2，請將 `model` 指定為 `anthropic.claude-v2`，而非 `anthropic.claude-3-5-sonnet-20240620-v1:0`。

請記下連接器 ID；您將使用它來註冊模型。

接著，註冊模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "Bedrock Claude3.5 model",
    "description": "Bedrock Claude3.5 model",
    "function_name": "remote",
    "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

請記下模型 ID；您將在下列步驟中使用它。

測試模型：

```json
POST /_plugins/_ml/models/your_model_id/_predict
{
  "parameters": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "text": "hello"
          }
        ]
      }
    ]
  }
}
```
{% include copy-curl.html %}


回應中包含模型生成的文字：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "metrics": {
              "latencyMs": 955.0
            },
            "output": {
              "message": {
                "content": [
                  {
                    "text": "Hello! How can I assist you today? Feel free to ask me any questions or let me know if you need help with anything."
                  }
                ],
                "role": "assistant"
              }
            },
            "stopReason": "end_turn",
            "usage": {
              "inputTokens": 14.0,
              "outputTokens": 30.0,
              "totalTokens": 44.0
            }
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

### 步驟 1.2：設定 RAG

若要設定 RAG，請建立包含 RAG 處理器的搜尋管線：

```json
PUT /_search/pipeline/my-conversation-search-pipeline-claude
{
  "response_processors": [
    {
      "retrieval_augmented_generation": {
        "tag": "Demo pipeline",
        "description": "Demo pipeline Using Bedrock Claude",
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

執行基本的 RAG 搜尋，不儲存對話歷程：

```json
GET /qa_demo/_search?search_pipeline=my-conversation-search-pipeline-claude
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
      "llm_model": "bedrock-converse/anthropic.claude-3-sonnet-20240229-v1:0",
      "llm_question": "What's the population increase of New York City from 2021 to 2023?",
      "context_size": 5
    }
  }
}
```
{% include copy-curl.html %}

回應包含模型的回答及相關文件：

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
    "max_score": 9.042081,
    "hits": [
      {
        "_index": "qa_demo",
        "_id": "2",
        "_score": 9.042081,
        "_source": {
          "text": "Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."
        }
      }
    ]
  },
  "ext": {
    "retrieval_augmented_generation": {
      "answer": "The population of the New York City metro area increased by 114,000 people from 2021 to 2023. In 2021, the population was 18,823,000. By 2023, it had grown to 18,937,000. This represents a total increase of about 0.61% over the two-year period, with growth rates of 0.23% from 2021 to 2022 and 0.37% from 2022 to 2023."
    }
  }
}
```

### 步驟 1.3：設定對話式搜尋

請依照下列步驟，將對話歷程儲存在記憶中，以設定對話式搜尋。 

1. 建立記憶：

    ```json
    POST /_plugins/_ml/memory/
    {
    "name": "Conversation about NYC population"
    }
    ```
    {% include copy-curl.html %}

    回應包含記憶 ID：

    ```json
    {
    "memory_id": "sBAqY5UBSzdNxlHvrSJK"
    }
    ```

2. 若要儲存對話歷程，請在搜尋請求中加入記憶 ID：

    ```json 
    GET /qa_demo/_search?search_pipeline=my-conversation-search-pipeline-claude
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
        "llm_model": "bedrock-converse/anthropic.claude-3-sonnet-20240229-v1:0",
        "llm_question": "What's the population increase of New York City from 2021 to 2023?",
        "context_size": 5,
        "memory_id": "sBAqY5UBSzdNxlHvrSJK"
        }
    }
    }
    ```
    {% include copy-curl.html %}

    回應包含模型的回答及相關文件：

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
        "max_score": 9.042081,
        "hits": [
        {
            "_index": "qa_demo",
            "_id": "2",
            "_score": 9.042081,
            "_source": {
            "text": "Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."
            }
        }
        ]
    },
    "ext": {
        "retrieval_augmented_generation": {
        "answer": "The population of the New York City metro area increased by 114,000 people from 2021 to 2023. In 2021, the population was 18,823,000. By 2023, it had grown to 18,937,000. This represents a total increase of about 0.61% over the two-year period, with growth rates of 0.23% from 2021 to 2022 and 0.37% from 2022 to 2023.",
        "message_id": "sRAqY5UBSzdNxlHvzCIL"
        }
    }
    }
    ```

3. 若要繼續對話，請在下一次搜尋中提供相同的記憶 ID：

    ```json
    GET /qa_demo/_search?search_pipeline=my-conversation-search-pipeline-claude
    {
    "query": {
        "match": {
        "text": "What's the population increase of Chicago from 2021 to 2023?"
        }
    },
    "size": 1,
    "_source": [
        "text"
    ],
    "ext": {
        "generative_qa_parameters": {
        "llm_model": "bedrock-converse/anthropic.claude-3-sonnet-20240229-v1:0",
        "llm_question": "can you compare the population increase of Chicago with New York City",
        "context_size": 5,
        "memory_id": "sBAqY5UBSzdNxlHvrSJK"
        }
    }
    }
    ```
    {% include copy-curl.html %}

    模型使用記憶中的對話歷程，將芝加哥的人口資料與先前討論過的紐約市統計資料進行比較：

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
        "max_score": 3.6660428,
        "hits": [
        {
            "_index": "qa_demo",
            "_id": "3",
            "_score": 3.6660428,
            "_source": {
            "text": "Chart and table of population level and growth rate for the Chicago metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Chicago in 2023 is 8,937,000, a 0.4% increase from 2022.\\nThe metro area population of Chicago in 2022 was 8,901,000, a 0.27% increase from 2021.\\nThe metro area population of Chicago in 2021 was 8,877,000, a 0.14% increase from 2020.\\nThe metro area population of Chicago in 2020 was 8,865,000, a 0.03% increase from 2019."
            }
        }
        ]
    },
    "ext": {
        "retrieval_augmented_generation": {
        "answer": "Based on the provided data for Chicago, we can compare its population increase to New York City from 2021 to 2023:\n\nChicago's population increased from 8,877,000 in 2021 to 8,937,000 in 2023, a total increase of 60,000 people or about 0.68%.\n\nNew York City's population increased by 114,000 people or 0.61% in the same period.\n\nWhile New York City had a larger absolute increase, Chicago experienced a slightly higher percentage growth rate during this two-year period.",
        "message_id": "shArY5UBSzdNxlHvQyL-"
        }
    }
    }
    ```

<!-- vale off -->
## 選項 2：Amazon Bedrock Invoke API
<!-- vale on -->

請依照下列步驟，使用 Amazon Bedrock Invoke API 進行對話式搜尋。

Amazon Bedrock Invoke API 不支援 Anthropic Claude 3.x 模型，因為這些模型需要不同的介面。
{: .important}

### 步驟 2.1：建立連接器並註冊模型

首先，為 Claude 模型建立連接器。在此範例中，您將使用 Anthropic Claude v2：

```json
POST _plugins/_ml/connectors/_create
{
    "name": "Bedrock Claude2",
    "description": "Connector for Bedrock Claude2",
    "version": 1,
    "protocol": "aws_sigv4",
    "credential": {
        "access_key": "your_access_key",
        "secret_key": "your_secret_key",
        "session_token": "your_session_token"
    },
    "parameters": {
        "region": "your_aws_region",
        "service_name": "bedrock",
        "model": "anthropic.claude-v2"
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "headers": {
                "content-type": "application/json"
            },
            "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/invoke",
            "request_body": "{\"prompt\":\"\\n\\nHuman: ${parameters.inputs}\\n\\nAssistant:\",\"max_tokens_to_sample\":300,\"temperature\":0.5,\"top_k\":250,\"top_p\":1,\"stop_sequences\":[\"\\\\n\\\\nHuman:\"]}"
        }
    ]
}
```
{% include copy-curl.html %}

記下連接器 ID，稍後會用它來註冊模型。

接著，註冊模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "Bedrock Claude2 model",
    "function_name": "remote",
    "description": "Bedrock Claude2 model",
    "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

記下模型 ID，後續步驟會用到它。

測試模型：

```json
POST /_plugins/_ml/models/your_model_id/_predict
{
    "parameters": {
      "inputs": "Who won the world series in 2020?"
    }
}
```
{% include copy-curl.html %}

回應會包含模型產生的文字：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "type": "completion",
            "completion": " The Los Angeles Dodgers won the 2020 World Series, defeating the Tampa Bay Rays 4 games to 2. The World Series was played at a neutral site in Arlington, Texas due to the COVID-19 pandemic. It was the Dodgers' first World Series championship since 1988.",
            "stop_reason": "stop_sequence",
            "stop": "\n\nHuman:"
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

### 步驟 2.2：設定 RAG

若要設定 RAG，請建立一個包含 RAG 處理器的搜尋管線：

```json
PUT /_search/pipeline/my-conversation-search-pipeline-claude2
{
  "response_processors": [
    {
      "retrieval_augmented_generation": {
        "tag": "Demo pipeline",
        "description": "Demo pipeline Using Bedrock Claude2",
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

執行基本的 RAG 搜尋，不儲存對話歷史記錄：

```json
GET /qa_demo/_search?search_pipeline=my-conversation-search-pipeline-claude2
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
      "llm_model": "bedrock/claude",
      "llm_question": "What's the population increase of New York City from 2021 to 2023?",
      "context_size": 5,
      "timeout": 15
    }
  }
}
```
{% include copy-curl.html %}

回應與 [步驟 1.2](#step-12-configure-rag) 中的回應類似。

### 步驟 2.3：設定對話式搜尋

請繼續前往 [步驟 1.3](#step-13-configure-conversational-search) 以設定對話式搜尋。