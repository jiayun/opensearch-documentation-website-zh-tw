---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "為語意搜尋設定代理程式"
parent: Agentic search
grand_parent: AI search
nav_order: 90
has_children: false
---

# 為語意搜尋設定代理程式

當您擁有含嵌入的向量索引，並希望代理式搜尋能根據使用者意圖自動執行語意搜尋時，您需要在代理程式中設定嵌入模型資訊。這可讓代理程式產生用於搜尋語意相似度的 `neural` 查詢，而非搜尋完全相符的文字，為概念性問題提供更相關的結果。

當您為語意搜尋設定代理程式時，代理程式會在查詢時於傳統關鍵字搜尋與語意向量搜尋之間做選擇。

即使提供了嵌入模型 ID，代理程式仍會根據查詢意圖與情境，自主決定要使用神經 (語意) 搜尋或詞彙搜尋。例如，日期篩選條件或完全相符查詢會使用詞彙搜尋，而概念性查詢則會使用神經搜尋。
{: .note} 

**先決條件**<br>
使用語意搜尋之前，您必須設定文字嵌入模型。如需更多資訊，請參閱[選擇模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#choosing-a-model)。
{: .note}

## 步驟 1：設定向量索引

首先，設定向量索引。

### 步驟 1(a)：建立嵌入模型

註冊一個嵌入模型，將文字轉換為向量表示以供語意搜尋使用：

```json
POST /_plugins/_ml/models/_register
{
  "name": "Bedrock embedding model",
  "function_name": "remote",
  "description": "Bedrock text embedding model v2",
  "connector": {
    "name": "Amazon Bedrock Connector: embedding",
    "description": "The connector to bedrock Titan embedding model",
    "version": 1,
    "protocol": "aws_sigv4",
    "parameters": {
      "region": "your-aws-region",
      "service_name": "bedrock",
      "model": "amazon.titan-embed-text-v2:0",
      "dimensions": 1024,
      "normalize": true,
      "embeddingTypes": [
        "float"
      ]
    },
    "credential": {
      "access_key": "your-access-key",
      "secret_key": "your-secret-key",
      "session_token": "your-session-token"
    },
    "actions": [
      {
        "action_type": "predict",
        "method": "POST",
        "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/invoke",
        "headers": {
          "content-type": "application/json",
          "x-amz-content-sha256": "required"
        },
        "request_body": "{ \"inputText\": \"${parameters.inputText}\", \"dimensions\": ${parameters.dimensions}, \"normalize\": ${parameters.normalize}, \"embeddingTypes\": ${parameters.embeddingTypes} }",
        "pre_process_function": "connector.pre_process.bedrock.embedding",
        "post_process_function": "connector.post_process.bedrock.embedding"
      }
    ]
  }
}
```
{% include copy-curl.html %}

### 步驟 1(b)：建立資料匯入管線

建立資料匯入管線，在文件匯入期間自動為文字欄位產生嵌入：

```json
PUT /_ingest/pipeline/my_bedrock_embedding_pipeline
{
  "description": "text embedding pipeline",
  "processors": [
    {
      "text_embedding": {
        "model_id": "fxzel5kB-5P992SCH-qM",
        "field_map": {
          "content_text": "content_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 1(c)：建立含資料匯入管線的向量索引

建立含文字內容與向量嵌入對應的向量索引，並使用資料匯入管線自動處理文件：

```json
PUT /research_papers
{
  "settings": {
    "index": {
      "default_pipeline": "my_bedrock_embedding_pipeline",
      "knn": "true"
    }
  },
  "mappings": {
    "properties": {
      "content_embedding": {
        "type": "knn_vector",
        "dimension": 1024,
        "method": {
          "name": "hnsw",
          "engine": "lucene"
        }
      },
      "published_date": {
        "type": "date"
      },
      "rating": {
        "type": "integer"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 1(d)：將資料匯入向量索引

將研究論文文件新增至索引。資料匯入管線會自動為 `content_text` 欄位產生嵌入：

```json
POST /_bulk
{ "index": { "_index": "research_papers", "_id": "1" } }
{ "content_text": "Autonomous robotic systems for warehouse automation and industrial manufacturing", "published_date": "2024-05-15", "rating": 5 }
{ "index": { "_index": "research_papers", "_id": "2" } }
{ "content_text": "Gene expression analysis and CRISPR-Cas9 genome editing applications in cancer research", "published_date": "2024-06-02", "rating": 4 }
{ "index": { "_index": "research_papers", "_id": "3" } }
{ "content_text": "Reinforcement learning algorithms for sequential decision making and optimization problems", "published_date": "2024-03-20", "rating": 5 }
{ "index": { "_index": "research_papers", "_id": "4" } }
{ "content_text": "Climate change impact on coral reef ecosystems and marine biodiversity conservation", "published_date": "2024-04-10", "rating": 4 }
{ "index": { "_index": "research_papers", "_id": "5" } }
{ "content_text": "Tectonic plate movements and earthquake prediction using geological fault analysis", "published_date": "2024-01-22", "rating": 4 }
```
{% include copy-curl.html %}

## 步驟 2：設定代理式搜尋

接著，設定代理式搜尋。

### 步驟 2(a)：為代理式搜尋建立模型

註冊一個同時供對話代理程式與 `QueryPlanningTool` 使用的模型：

```json
POST /_plugins/_ml/models/_register
{
  "name": "My OpenAI model: gpt-5",
  "function_name": "remote",
  "description": "Model for agentic search with neural queries",
  "connector": {
    "name": "My openai connector: gpt-5",
    "description": "The connector to openai chat model",
    "version": 1,
    "protocol": "http",
    "parameters": {
      "model": "gpt-5"
    },
    "credential": {
      "openAI_key": "<OPEN AI KEY>"
    },
    "actions": [
      {
        "action_type": "predict",
        "method": "POST",
        "url": "https://api.openai.com/v1/chat/completions",
        "headers": {
          "Authorization": "Bearer ${credential.openAI_key}"
        },
        "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": [{\"role\":\"developer\",\"content\":\"${parameters.system_prompt}\"},${parameters._chat_history:-}{\"role\":\"user\",\"content\":\"${parameters.user_prompt}\"}${parameters._interactions:-}], \"reasoning_effort\":\"low\"${parameters.tool_configs:-}}"
      }
    ]
  }
}
```
{% include copy-curl.html %}

### 步驟 2(b)：建立代理程式

建立用於代理式搜尋的代理程式。若要讓代理程式使用 `neural` 查詢執行語意搜尋，您需要使用下列其中一種方法設定嵌入模型：

- [**選項 1**](#option-1-create-an-agent-without-an-embedding-model-id-recommended)：在搜尋管線中設定嵌入模型 (建議使用，較易於更新)。
- [**選項 2**](#option-2-create-an-agent-with-an-embedding-model-id)：在代理程式組態中設定嵌入模型。

#### 選項 1：建立不含嵌入模型 ID 的代理程式 (建議)

如果您打算在搜尋管線中指定 `embedding_model_id`，請使用此選項：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "GPT 5 Agent for Agentic Search",
  "type": "conversational",
  "description": "Use this for Agentic Search",
  "llm": {
    "model_id": "your-agent-model-id",
    "parameters": {
      "max_iteration": 15
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
      "type": "QueryPlanningTool",
      "parameters": {
        "model_id": "your-qpt-model-id"
      }
    }
  ],
  "app_type": "os_chat"
}
```
{% include copy-curl.html %}

#### 選項 2：使用嵌入模型 ID 建立代理程式

或者，在代理程式的 `llm.parameters` 中包含 `embedding_model_id`：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "GPT 5 Agent for Agentic Search",
  "type": "conversational",
  "description": "Use this for Agentic Search",
  "llm": {
    "model_id": "your-agent-model-id",
    "parameters": {
      "max_iteration": 15,
      "embedding_model_id": "your-embedding-model-id-from-step1"
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
      "type": "QueryPlanningTool",
      "parameters": {
        "model_id": "your-qpt-model-id"
      }
    }
  ],
  "app_type": "os_chat"
}
```
{% include copy-curl.html %}

### 步驟 2(c)：建立搜尋管線

建立具有 `agentic_query_translator` 處理器的搜尋管線。如需詳細資訊，請參閱[代理式查詢轉譯處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-query-translator-processor/)。

**如果您在步驟 2(b) 中使用選項 1（建議）**：在搜尋管線中包含 `embedding_model_id`：

```json
PUT _search/pipeline/my_pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "your-agent-id-from-step-2b",
        "embedding_model_id": "your-embedding-model-id-from-step1"
      }
    }
  ]
}
```
{% include copy-curl.html %}

**如果您在步驟 2(b) 中使用選項 2**：建立不含 `embedding_model_id` 的搜尋管線：

```json
PUT _search/pipeline/my_pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "your-agent-id-from-step-2b"
      }
    }
  ]
}
```
{% include copy-curl.html %}

如果您在代理程式和搜尋管線中都指定 `embedding_model_id`，則搜尋管線的組態優先。
{: .note}

## 步驟 3：執行代理式搜尋

使用各種組態執行代理式搜尋。

### 執行語意搜尋

使用需要語意理解的問題執行代理式搜尋：

```json
POST /research_papers/_search?search_pipeline=my_pipeline
{
  "query": {
    "agentic": {
      "query_text": "Show me 3 robots training related research papers "
    }
  }
}
```
{% include copy-curl.html %}

代理程式成功辨識出需要語意搜尋。`ext` 物件顯示，`QueryPlanningTool` 已成功使用嵌入模型 ID 產生 `neural` 查詢。回應包含依語意相似度排序的相符研究論文：

```json
{
  "took": 10509,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": 0.40031588,
    "hits": [
      {
        "_index": "research_papers",
        "_id": "1",
        "_score": 0.40031588,
        "_source": {
          "content_text": "Autonomous robotic systems for warehouse automation and industrial manufacturing",
          "rating": 5,
          "content_embedding": ["<redacted>"],
          "published_date": "2024-05-15"
        }
      },
      {
        "_index": "research_papers",
        "_id": "3",
        "_score": 0.36390686,
        "_source": {
          "content_text": "Reinforcement learning algorithms for sequential decision making and optimization problems",
          "rating": 5,
          "content_embedding": ["<redacted>"],
          "published_date": "2024-03-20"
        }
      },
      {
        "_index": "research_papers",
        "_id": "5",
        "_score": 0.34401828,
        "_source": {
          "content_text": "Tectonic plate movements and earthquake prediction using geological fault analysis",
          "rating": 4,
          "content_embedding": ["<redacted>"],
          "published_date": "2024-01-22"
        }
      }
    ]
  },
  "ext": {
    "agent_steps_summary": "I have these tools available: [ListIndexTool, IndexMappingTool, query_planner_tool]\nFirst I used: ListIndexTool — input: \"[]\"; context gained: \"Found indices; 'research_papers' appears relevant\"\nSecond I used: IndexMappingTool — input: \"[\"research_papers\"]\"; context gained: \"Index has text content and an embedding field suitable for neural search\"\nThird I used: query_planner_tool — qpt.question: \"Show me 3 research papers related to robots training.\"; index_name_provided: \"research_papers\"\nValidation: qpt output is valid and limits results to 3 using neural search with the provided model.",
    "memory_id": "jhzpl5kB-5P992SCwOqe",
    "dsl_query": "{\"size\":3.0,\"query\":{\"neural\":{\"content_embedding\":{\"model_id\":\"fxzel5kB-5P992SCH-qM\",\"k\":100.0,\"query_text\":\"robots training\"}}}}"
  }
}
```

### 執行含有篩選條件的傳統搜尋

接著，使用需要篩選而非語意理解的問題執行代理式搜尋：

```json
POST /research_papers/_search?search_pipeline=my_pipeline
{
  "query": {
    "agentic": {
      "query_text": "Show me papers published after 2024 May"
    }
  }
}
```
{% include copy-curl.html %}

代理程式將此查詢辨識為以日期為依據的篩選查詢，並產生傳統的 `range` 查詢，而非 `neural` 查詢：

```json
{
  "took": 8522,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "research_papers",
        "_id": "2",
        "_score": null,
        "_source": {
          "content_text": "Gene expression analysis and CRISPR-Cas9 genome editing applications in cancer research",
          "rating": 4,
          "content_embedding": ["<redacted>"],
          "published_date": "2024-06-02"
        },
        "sort": [
          1717286400000
        ]
      }
    ]
  },
  "ext": {
    "agent_steps_summary": "I have these tools available: [ListIndexTool, IndexMappingTool, query_planner_tool]\nFirst I used: query_planner_tool — qpt.question: \"Show me papers published after May 2024.\"; index_name_provided: \"research_papers\"\nValidation: qpt output is valid JSON and matches the user request with the specified date filter and sorting.",
    "memory_id": "vBzyl5kB-5P992SCI-o1",
    "dsl_query": "{\"size\":10.0,\"query\":{\"bool\":{\"filter\":[{\"range\":{\"published_date\":{\"gt\":\"2024-05-31T23:59:59Z\"}}}]}},\"sort\":[{\"published_date\":{\"order\":\"desc\"}}]}"
  }
}
```

### 在查詢文字中指定嵌入模型

若要覆寫嵌入模型 ID，您可以在傳送查詢時，將其直接包含在自然語言 `query_text` 中。這會優先於搜尋管線或代理程式中設定的任何 `embedding_model_id`：

```json
POST /research_papers/_search?search_pipeline=my_pipeline
{
  "query": {
    "agentic": {
      "query_text": "Show me 3 robots training related research papers use this model id for neural search:fxzel5kB-5P992SCH-qM "
    }
  }
}
```
{% include copy-curl.html %}

代理程式成功直接從查詢文字中擷取嵌入模型 ID，並產生適當的神經 DSL 查詢：

```json
{
  "took": 14989,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "max_score": 0.38957736,
    "hits": [
      {
        "_index": "research_papers",
        "_id": "1",
        "_score": 0.38957736,
        "_source": {
          "content_text": "Autonomous robotic systems for warehouse automation and industrial manufacturing",
          "rating": 5,
          "content_embedding": [],
          "published_date": "2024-05-15"
        }
      },
      {
        "_index": "research_papers",
        "_id": "3",
        "_score": 0.36386627,
        "_source": {
          "content_text": "Reinforcement learning algorithms for sequential decision making and optimization problems",
          "rating": 5,
          "content_embedding": [],
          "published_date": "2024-03-20"
        }
      },
      {
        "_index": "research_papers",
        "_id": "2",
        "_score": 0.35789147,
        "_source": {
          "content_text": "Gene expression analysis and CRISPR-Cas9 genome editing applications in cancer research",
          "rating": 4,
          "content_embedding": [],
          "published_date": "2024-06-02"
        }
      }
    ]
  },
  "ext": {
    "agent_steps_summary": "I have these tools available: [ListIndexTool, IndexMappingTool, query_planner_tool]\nFirst I used: ListIndexTool — input: \"\"; context gained: \"Found indices, including research_papers with 5 documents\"\nSecond I used: IndexMappingTool — input: \"research_papers\"; context gained: \"Index exists and contains text and embedding fields suitable for neural search\"\nThird I used: query_planner_tool — qpt.question: \"Show me 3 research papers related to robot training.\"; index_name_provided: \"research_papers\"\nValidation: qpt output is valid neural search DSL using the provided model ID and limits results to 3.",
    "memory_id": "whz1l5kB-5P992SCPOqn",
    "dsl_query": "{\"size\":3.0,\"query\":{\"neural\":{\"content_embedding\":{\"model_id\":\"fxzel5kB-5P992SCH-qM\",\"k\":100.0,\"query_text\":\"research papers related to robot training\"}}},\"sort\":[{\"_score\":{\"order\":\"desc\"}}],\"track_total_hits\":false}"
  }
}
```

## 相關文件

- [代理式查詢轉譯處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-query-translator-processor/)
- [代理式搜尋概觀]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/index/)
- [設定代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/)