---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 RAG 的對話式搜尋"
parent: AI search
has_children: false
nav_order: 70
redirect_from:
  - /ml-commons-plugin/conversational-search/
  - /search-plugins/conversational-search/
---

# 使用 RAG 的對話式搜尋

對話式搜尋讓您能以自然語言提問，並透過追問來精煉答案。如此一來，對話就成為您與大型語言模型 (LLM) 之間的對話。為了達成這一點，模型不能逐一回答每個問題，而需要記住整個對話的上下文。

對話式搜尋由下列元件實作：

- [對話歷史](#conversation-history)：讓 LLM 記住目前對話的上下文，並理解追問的問題。
- [檢索增強生成 (RAG)](#rag)：讓 LLM 以專有或最新資訊補充其靜態知識庫。

## 對話歷史

對話歷史由一個類似 CRUD 的簡單 API 組成，包含兩種資源：_memories_（記憶）與 _messages_（訊息）。目前對話的所有訊息都儲存在同一個對話 _memory_ 中。一則 _message_ 代表一組問答：使用者輸入的問題與 AI 的回答。訊息不會單獨存在；必須加入某個 memory。

## RAG

RAG 會從索引與歷史中擷取資料，並將所有資訊作為上下文傳送給 LLM。LLM 接著以動態擷取的資料補充其靜態知識庫。在 OpenSearch 中，RAG 透過包含[檢索增強生成處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rag-processor/)的搜尋管線實作。該處理器會攔截 OpenSearch 查詢結果，從對話記憶中擷取對話先前的訊息，並將提示傳送給 LLM。處理器收到 LLM 的回應後，會將回應儲存在對話記憶中，並同時傳回原始的 OpenSearch 查詢結果與 LLM 回應。

截至 OpenSearch 2.11，RAG 技術僅在 OpenAI 模型與 Amazon Bedrock 上的 Anthropic Claude 模型上測試過。
{: .warning}

當 Security 外掛程式啟用時，所有 memory 都存在於 `private` 安全模式中。只有建立某個 memory 的使用者才能與該 memory 互動。任何使用者都無法看到其他使用者的 memory。
{: .note}

## 先決條件

若要開始使用對話式搜尋，請啟用對話記憶與 RAG 管線功能：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.ml_commons.memory_feature_enabled": true,
    "plugins.ml_commons.rag_pipeline_feature_enabled": true
  }
}
```
{% include copy-curl.html %}

## 設定對話式搜尋

設定對話式搜尋有兩種方式：

- [**自動化工作流程**](#automated-workflow)（建議用於快速設定）：以最少的組態自動建立資料匯入管線與索引。
- [**手動設定**](#manual-setup)（建議用於自訂組態）：手動設定每個元件，以獲得更大的彈性與控制。

## 自動化工作流程

OpenSearch 提供[工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates#conversational-search-using-an-llm)，可自動為 LLM 建立連接器、註冊並部署 LLM，以及設定搜尋管線。建立工作流程時，您必須提供所設定 LLM 的 API 金鑰。請檢視對話式搜尋工作流程範本的[預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/conversational-search-defaults.json)，判斷是否需要更新任何參數。例如，如果模型端點與預設值 (`https://api.cohere.ai/v1/chat`) 不同，請在 `create_connector.actions.url` 參數中指定您模型的端點。若要建立預設的對話式搜尋工作流程，請傳送下列請求：

```json
POST /_plugins/_flow_framework/workflow?use_case=conversational_search_with_llm_deploy&provision=true
{
"create_connector.credential.key": "<YOUR_API_KEY>"
}
```
{% include copy-curl.html %}

OpenSearch 會以所建立工作流程的工作流程 ID 回應：

```json
{
  "workflow_id" : "U_nMXJUBq_4FYQzMOS4B"
}
```

若要檢查工作流程狀態，請傳送下列請求：

```json
GET /_plugins/_flow_framework/workflow/U_nMXJUBq_4FYQzMOS4B/_status
```
{% include copy-curl.html %}

工作流程完成後，`state` 會變更為 `COMPLETED`。該工作流程會建立下列元件：

- 模型連接器：連接至指定的模型。
- 已註冊並部署的模型：模型已可進行推論。
- 搜尋管線：已設定為處理對話式查詢。

您現在可以繼續[步驟 4、5 與 6](#step-4-ingest-rag-data-into-an-index)，將 RAG 資料匯入索引、建立對話記憶，並使用該管線進行 RAG。

## 手動設定

若要手動設定對話式搜尋，請依照下列步驟進行：

1. [為模型建立連接器](#step-1-create-a-connector-for-a-model)。
1. [註冊並部署模型](#step-2-register-and-deploy-the-model)。
1. [建立搜尋管線](#step-3-create-a-search-pipeline)。
1. [將 RAG 資料匯入索引](#step-4-ingest-rag-data-into-an-index)。
1. [建立對話記憶](#step-5-create-a-conversation-memory)。
1. [使用管線進行 RAG](#step-6-use-the-pipeline-for-rag)。

### 步驟 1：為模型建立連接器

RAG 需要 LLM 才能運作。若要連接至 LLM，請建立[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。下列請求會為 OpenAI gpt-4o-mini 模型建立連接器：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "OpenAI Chat Connector",
  "description": "The connector to public OpenAI model service for gpt-4o-mini",
  "version": 2,
  "protocol": "http",
  "parameters": {
    "endpoint": "api.openai.com",
    "model": "gpt-4o-mini",
    "temperature": 0
  },
  "credential": {
    "openAI_key": "<YOUR_OPENAI_KEY>"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://${parameters.endpoint}/v1/chat/completions",
      "headers": {
        "Authorization": "Bearer ${credential.openAI_key}"
      },
      "request_body": """{ "model": "${parameters.model}", "messages": ${parameters.messages}, "temperature": ${parameters.temperature} }"""
    }
  ]
}
```
{% include copy-curl.html %}

OpenSearch 會以該連接器的連接器 ID 回應：

```json
{
  "connector_id": "u3DEbI0BfUsSoeNTti-1"
}
```

如需連接至其他服務與模型的範例請求，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)。
{: .tip}

### 步驟 2：註冊並部署模型

請註冊您在上一個步驟中為其建立連接器的 LLM。若要向 OpenSearch 註冊模型，請提供上一個步驟傳回的 `connector_id`：

```json
POST /_plugins/_ml/models/_register
{
  "name": "openAI-gpt-4o-mini",
  "function_name": "remote",
  "description": "test model",
  "connector_id": "u3DEbI0BfUsSoeNTti-1"
}
``` 
{% include copy-curl.html %}

OpenSearch 會為註冊任務傳回任務 ID，並為已註冊的模型傳回模型 ID：

```json
{
  "task_id": "gXDIbI0BfUsSoeNT_jAb",
  "status": "CREATED",
  "model_id": "gnDIbI0BfUsSoeNT_jAw"
}
```

若要確認註冊已完成，請呼叫 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)：

```json
GET /_plugins/_ml/tasks/gXDIbI0BfUsSoeNT_jAb
```
{% include copy-curl.html %}

回應中的 `state` 會變更為 `COMPLETED`：

```json
{
  "model_id": "gnDIbI0BfUsSoeNT_jAw",
  "task_type": "REGISTER_MODEL",
  "function_name": "REMOTE",
  "state": "COMPLETED",
  "worker_node": [
    "kYv-Z5-mQ4uCUy_cRC6LXA"
  ],
  "create_time": 1706927128091,
  "last_update_time": 1706927128125,
  "is_async": false
}
```

若要部署模型，請將 `model_id` 提供給 Deploy API：

```json
POST /_plugins/_ml/models/gnDIbI0BfUsSoeNT_jAw/_deploy
```
{% include copy-curl.html %}

OpenSearch 會確認模型已部署：

```json
{
  "task_id": "cnDObI0BfUsSoeNTDzGd",
  "task_type": "DEPLOY_MODEL",
  "status": "COMPLETED"
}
```

### 步驟 3：建立搜尋管線

接著，建立含有 `retrieval_augmented_generation` 處理器的搜尋管線：

```json
PUT /_search/pipeline/rag_pipeline
{
  "response_processors": [
    {
      "retrieval_augmented_generation": {
        "tag": "openai_pipeline_demo",
        "description": "Demo pipeline Using OpenAI Connector",
        "model_id": "gnDIbI0BfUsSoeNT_jAw",
        "context_field_list": ["text"],
        "system_prompt": "You are a helpful assistant",
        "user_instructions": "Generate a concise and informative answer in less than 100 words for the given question"
      }
    }
  ]
}
```
{% include copy-curl.html %}

如需處理器欄位的相關資訊，請參閱[檢索增強生成處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rag-processor/)。

### 步驟 4：將 RAG 資料匯入索引

RAG 會以一些補充資料來擴增 LLM 知識。

首先，建立用來儲存此資料的索引，並將預設搜尋管線設為前一個步驟所建立的管線：

```json
PUT /my_rag_test_data
{
  "settings": {
    "index.search.default_pipeline" : "rag_pipeline"
  },
  "mappings": {
    "properties": {
      "text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

接著，將補充資料匯入索引：

```json
POST _bulk
{"index": {"_index": "my_rag_test_data", "_id": "1"}}
{"text": "Abraham Lincoln was born on February 12, 1809, the second child of Thomas Lincoln and Nancy Hanks Lincoln, in a log cabin on Sinking Spring Farm near Hodgenville, Kentucky.[2] He was a descendant of Samuel Lincoln, an Englishman who migrated from Hingham, Norfolk, to its namesake, Hingham, Massachusetts, in 1638. The family then migrated west, passing through New Jersey, Pennsylvania, and Virginia.[3] Lincoln was also a descendant of the Harrison family of Virginia; his paternal grandfather and namesake, Captain Abraham Lincoln and wife Bathsheba (née Herring) moved the family from Virginia to Jefferson County, Kentucky.[b] The captain was killed in an Indian raid in 1786.[5] His children, including eight-year-old Thomas, Abraham's father, witnessed the attack.[6][c] Thomas then worked at odd jobs in Kentucky and Tennessee before the family settled in Hardin County, Kentucky, in the early 1800s."}
{"index": {"_index": "my_rag_test_data", "_id": "2"}}
{"text": "Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."}
```
{% include copy-curl.html %}

## RAG 管線

RAG 是一種技術，會從索引擷取文件、將其傳送至 seq2seq 模型 (例如 LLM)，然後在上下文中以動態擷取的資料補充靜態的 LLM 資訊。

自 OpenSearch 2.12 起，RAG 技術僅曾以 OpenAI 模型、Amazon Bedrock 上的 Anthropic Claude 模型，以及 Cohere Command 模型進行測試。
{: .warning}

設定 Cohere Command 模型以啟用 RAG 時，需要使用後處理函式來轉換模型輸出。如需詳細資訊，請參閱 [Cohere RAG 教學](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/tutorials/conversational_search/conversational_search_with_Cohere_Command.md)。

### 步驟 5：建立對話記憶

您需要建立對話記憶，用來儲存對話中的所有訊息。為了讓記憶容易識別，請在選用的 `name` 欄位中提供記憶的名稱，如下列範例所示。由於 `name` 參數無法更新，這是您唯一能為對話命名的機會。

```json
POST /_plugins/_ml/memory/
{
  "name": "Conversation about NYC population"
}
```
{% include copy-curl.html %}

OpenSearch 會以新建立記憶的記憶 ID 回應：

```json
{
  "memory_id": "znCqcI0BfUsSoeNTntd7"
}
```

您將使用 `memory_id` 將訊息新增至記憶。


### 步驟 6：使用管線進行 RAG

若要使用 RAG 管線，請將查詢傳送至 OpenSearch，並在 `ext.generative_qa_parameters` 物件中提供其他參數。

`generative_qa_parameters` 物件支援下列參數。

參數 | 必要 | 說明
:--- | :--- | :---
`llm_question` | 是 | LLM 必須回答的問題。
`llm_model` | 否 | 當您想使用不同的模型時 (例如使用 `gpt-4o` 而非 `gpt-4o-mini`)，覆寫連線中設定的原始模型。若建立管線時未設定預設模型，則必須使用此選項。
`memory_id` | 否 | 若您提供 `memory_id`，管線會擷取指定記憶中最近的 10 則訊息，並將其新增至 LLM 提示。若您未指定 `memory_id`，則不會將先前的上下文新增至 LLM 提示。
`context_size` | 否 | 傳送至 LLM 的搜尋結果數目。這通常是為了符合詞元大小限制所需，而該限制會因模型而異。或者，您可以使用 Search API 中的 `size` 參數，控制傳送至 LLM 的搜尋結果數目。
`message_size` | 否 | 傳送至 LLM 的訊息數目。與搜尋結果數目類似，這會影響 LLM 接收的詞元總數。未設定時，管線會使用預設訊息大小 `10`。
`timeout` | 否 | 管線等待使用連接器的遠端模型回應的秒數。預設為 `30`。

若您的 LLM 包含設定的詞元限制，請在 OpenSearch 查詢中設定 `size` 欄位，以限制搜尋回應中使用的文件數目。否則，RAG 管線會將搜尋結果中的每份文件都傳送至 LLM。
{: .note}

若您向 LLM 詢問關於現況的問題，它無法提供答案，因為它是以前幾年的資料訓練而成。不過，若您將最新資訊新增為上下文，LLM 就能產生回應。例如，您可以詢問 LLM 2023 年紐約市都會區的人口數。您將建構一個包含 OpenSearch match 查詢與 LLM 查詢的查詢。請提供 `memory_id`，讓訊息儲存在適當的記憶物件中：

```json
GET /my_rag_test_data/_search
{
  "query": {
    "match": {
      "text": "What's the population of NYC metro area in 2023"
    }
  },
  "ext": {
    "generative_qa_parameters": {
      "llm_model": "gpt-4o-mini",
      "llm_question": "What's the population of NYC metro area in 2023",
      "memory_id": "znCqcI0BfUsSoeNTntd7",
      "context_size": 5,
      "message_size": 5,
      "timeout": 15
    }
  }
}
```
{% include copy-curl.html %}

由於上下文包含一份內含紐約市人口資訊的文件，LLM 得以正確回答該問題 (不過它包含了「projected」一詞，因為它是以前幾年的資料訓練而成)。回應包含來自補充 RAG 資料的相符文件以及 LLM 回應：

<details open markdown="block">
  <summary>
    Response
  </summary>
  {: .text-delta}

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 5.781642,
    "hits": [
      {
        "_index": "my_rag_test_data",
        "_id": "2",
        "_score": 5.781642,
        "_source": {
          "text": """Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."""
        }
      },
      {
        "_index": "my_rag_test_data",
        "_id": "1",
        "_score": 0.9782871,
        "_source": {
          "text": "Abraham Lincoln was born on February 12, 1809, the second child of Thomas Lincoln and Nancy Hanks Lincoln, in a log cabin on Sinking Spring Farm near Hodgenville, Kentucky.[2] He was a descendant of Samuel Lincoln, an Englishman who migrated from Hingham, Norfolk, to its namesake, Hingham, Massachusetts, in 1638. The family then migrated west, passing through New Jersey, Pennsylvania, and Virginia.[3] Lincoln was also a descendant of the Harrison family of Virginia; his paternal grandfather and namesake, Captain Abraham Lincoln and wife Bathsheba (née Herring) moved the family from Virginia to Jefferson County, Kentucky.[b] The captain was killed in an Indian raid in 1786.[5] His children, including eight-year-old Thomas, Abraham's father, witnessed the attack.[6][c] Thomas then worked at odd jobs in Kentucky and Tennessee before the family settled in Hardin County, Kentucky, in the early 1800s."
        }
      }
    ]
  },
  "ext": {
    "retrieval_augmented_generation": {
      "answer": "The population of the New York City metro area in 2023 is projected to be 18,937,000.",
      "message_id": "x3CecI0BfUsSoeNT9tV9"
    }
  }
}
```
</details>

現在您將在同一段對話中向 LLM 提出後續問題。同樣地，請在請求中提供 `memory_id`：

```json
GET /my_rag_test_data/_search
{
  "query": {
    "match": {
      "text": "What was it in 2022"
    }
  },
  "ext": {
    "generative_qa_parameters": {
      "llm_model": "gpt-4o-mini",
      "llm_question": "What was it in 2022",
      "memory_id": "znCqcI0BfUsSoeNTntd7",
      "context_size": 5,
      "message_size": 5,
      "timeout": 15
    }
  }
}
```
{% include copy-curl.html %}

LLM 正確辨識出對話的主題，並傳回相關的回應：

```json
{
  ...
  "ext": {
    "retrieval_augmented_generation": {
      "answer": "The population of the New York City metro area in 2022 was 18,867,000.",
      "message_id": "p3CvcI0BfUsSoeNTj9iH"
    }
  }
}
```

若要確認這兩則訊息都已新增至記憶，請將 `memory_ID` 提供給 Get Messages API：

```json
GET /_plugins/_ml/memory/znCqcI0BfUsSoeNTntd7/messages
```

回應包含這兩則訊息：

<details open markdown="block">
  <summary>
    Response
  </summary>
  {: .text-delta}

```json
{
  "messages": [
    {
      "memory_id": "znCqcI0BfUsSoeNTntd7",
      "message_id": "x3CecI0BfUsSoeNT9tV9",
      "create_time": "2024-02-03T20:33:50.754708446Z",
      "input": "What's the population of NYC metro area in 2023",
      "prompt_template": """[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content":"Generate a concise and informative answer in less than 100 words for the given question"}]""",
      "response": "The population of the New York City metro area in 2023 is projected to be 18,937,000.",
      "origin": "retrieval_augmented_generation",
      "additional_info": {
        "metadata": """["Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019.","Abraham Lincoln was born on February 12, 1809, the second child of Thomas Lincoln and Nancy Hanks Lincoln, in a log cabin on Sinking Spring Farm near Hodgenville, Kentucky.[2] He was a descendant of Samuel Lincoln, an Englishman who migrated from Hingham, Norfolk, to its namesake, Hingham, Massachusetts, in 1638. The family then migrated west, passing through New Jersey, Pennsylvania, and Virginia.[3] Lincoln was also a descendant of the Harrison family of Virginia; his paternal grandfather and namesake, Captain Abraham Lincoln and wife Bathsheba (née Herring) moved the family from Virginia to Jefferson County, Kentucky.[b] The captain was killed in an Indian raid in 1786.[5] His children, including eight-year-old Thomas, Abraham's father, witnessed the attack.[6][c] Thomas then worked at odd jobs in Kentucky and Tennessee before the family settled in Hardin County, Kentucky, in the early 1800s."]"""
      }
    },
    {
      "memory_id": "znCqcI0BfUsSoeNTntd7",
      "message_id": "p3CvcI0BfUsSoeNTj9iH",
      "create_time": "2024-02-03T20:36:10.24453505Z",
      "input": "What was it in 2022",
      "prompt_template": """[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content":"Generate a concise and informative answer in less than 100 words for the given question"}]""",
      "response": "The population of the New York City metro area in 2022 was 18,867,000.",
      "origin": "retrieval_augmented_generation",
      "additional_info": {
        "metadata": """["Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019.","Abraham Lincoln was born on February 12, 1809, the second child of Thomas Lincoln and Nancy Hanks Lincoln, in a log cabin on Sinking Spring Farm near Hodgenville, Kentucky.[2] He was a descendant of Samuel Lincoln, an Englishman who migrated from Hingham, Norfolk, to its namesake, Hingham, Massachusetts, in 1638. The family then migrated west, passing through New Jersey, Pennsylvania, and Virginia.[3] Lincoln was also a descendant of the Harrison family of Virginia; his paternal grandfather and namesake, Captain Abraham Lincoln and wife Bathsheba (née Herring) moved the family from Virginia to Jefferson County, Kentucky.[b] The captain was killed in an Indian raid in 1786.[5] His children, including eight-year-old Thomas, Abraham's father, witnessed the attack.[6][c] Thomas then worked at odd jobs in Kentucky and Tennessee before the family settled in Hardin County, Kentucky, in the early 1800s."]"""
      }
    }
  ]
}
```
</details>

## 後續步驟

- 探索我們的[教學]({{site.url}}{{site.baseurl}}/vector-search/tutorials/)，了解如何建立 AI 搜尋應用程式。 