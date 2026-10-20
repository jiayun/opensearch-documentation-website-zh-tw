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

對話式搜尋讓您能以自然語言提問，並透過追問來精煉答案。如此一來，對話就成為您與大型語言模型 (LLM) 之間的對話。為達成此目的，模型不能只逐一回答每個問題，而必須記住整個對話的上下文。

對話式搜尋由下列元件實作：

- [對話歷史](#conversation-history)：讓 LLM 記住目前對話的上下文，並理解追問的問題。
- [檢索增強生成 (RAG)](#rag)：讓 LLM 以專有或最新資訊補充其靜態知識庫。

## 對話歷史

對話歷史由一個類似 CRUD 的簡單 API 組成，包含兩種資源：_memories_（記憶）與 _messages_（訊息）。目前對話的所有訊息都儲存在同一個對話 _memory_ 中。一個 _message_ 代表一組問答：使用者輸入的問題與 AI 的回答。訊息不能單獨存在，必須加入某個記憶。

## RAG

RAG 會從索引與歷史中擷取資料，並將所有資訊作為上下文傳送給 LLM。LLM 接著以動態擷取的資料補充其靜態知識庫。在 OpenSearch 中，RAG 透過包含[檢索增強生成處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rag-processor/)的搜尋管線來實作。該處理器會攔截 OpenSearch 查詢結果，從對話記憶中擷取對話中先前的訊息，並將提示傳送給 LLM。處理器收到 LLM 的回應後，會將回應儲存在對話記憶中，並同時傳回原始的 OpenSearch 查詢結果與 LLM 回應。

RAG 技術支援 OpenAI、Amazon Bedrock 與 Cohere 模型。若要使用其他模型，請設定 `llm_response_field` 參數。如需更多資訊，請參閱[步驟 6：使用管線進行 RAG](#step-6-use-the-pipeline-for-rag)。
{: .note}

啟用 Security 外掛程式時，所有記憶都存在於 `private` 安全性模式中。只有建立記憶的使用者才能與該記憶互動。任何使用者都無法看到其他使用者的記憶。
{: .note}

## 必要條件

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

OpenSearch 提供一個[工作流程範本]({{site.url}}{{site.baseurl}}/vector-search/ai-search/workflows/workflow-templates#conversational-search-using-an-llm)，會自動為 LLM 建立連接器、註冊並部署 LLM，以及設定搜尋管線。建立工作流程時，您必須提供所設定 LLM 的 API 金鑰。請檢視對話式搜尋工作流程範本的[預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/conversational-search-defaults.json)，判斷是否需要更新任何參數。例如，若模型端點與預設值（`https://api.cohere.ai/v1/chat`）不同，請在 `create_connector.actions.url` 參數中指定您模型的端點。若要建立預設的對話式搜尋工作流程，請傳送下列請求：

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

您現在可以繼續執行[步驟 4、5 與 6](#step-4-ingest-rag-data-into-an-index)，將 RAG 資料匯入索引、建立對話記憶，並使用管線進行 RAG。

## 手動設定

若要手動設定對話式搜尋，請依照下列步驟操作：

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

OpenSearch 會傳回註冊任務的任務 ID，以及已註冊模型的模型 ID：

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

接著，建立包含 `retrieval_augmented_generation` 處理器的搜尋管線：

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

RAG 會以一些補充資料來擴充 LLM 的知識。

首先，建立用來儲存這些資料的索引，並將預設搜尋管線設為上一個步驟中建立的管線：

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

RAG 是一種技術，它會從索引中擷取文件，將文件傳遞給 seq2seq 模型（例如 LLM），然後以在上下文中動態擷取的資料來補充 LLM 的靜態資訊。

RAG 技術支援 OpenAI、Amazon Bedrock 和 Cohere 模型。若要使用其他模型，請設定 `llm_response_field` 參數。如需詳細資訊，請參閱[步驟 6：將管線用於 RAG](#step-6-use-the-pipeline-for-rag)。
{: .note}

若要設定 Cohere Command 模型以啟用 RAG，需要使用後處理函式來轉換模型輸出。如需詳細資訊，請參閱 [Cohere RAG 教學](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/tutorials/conversational_search/conversational_search_with_Cohere_Command.md)。

### 步驟 5：建立對話記憶

您需要建立對話記憶，用來儲存對話中的所有訊息。為了方便識別記憶，請在選用的 `name` 欄位中為記憶提供名稱，如下列範例所示。由於 `name` 參數無法更新，這是您為對話命名的唯一機會。

```json
POST /_plugins/_ml/memory/
{
  "name": "Conversation about NYC population"
}
```
{% include copy-curl.html %}

OpenSearch 會回應新建立記憶的記憶 ID：

```json
{
  "memory_id": "znCqcI0BfUsSoeNTntd7"
}
```

您將使用 `memory_id` 將訊息新增至記憶。


### 步驟 6：將管線用於 RAG

若要使用 RAG 管線，請將查詢傳送至 OpenSearch，並在 `ext.generative_qa_parameters` 物件中提供額外參數。

`generative_qa_parameters` 物件支援下列參數。

參數 | 必要 | 說明
:--- | :--- | :---
`llm_question` | 視情況而定 | LLM 必須回答的問題。若未提供 `llm_messages`，則為必要。
`llm_model` | 否 | 當您想使用不同的模型時（例如以 `gpt-4o` 取代 `gpt-4o-mini`），覆寫連線中設定的原始模型。若在建立管線時未設定預設模型，則此選項為必要。值的前綴決定處理器使用的請求與回應格式：`bedrock/` 用於 Amazon Bedrock 模型，`bedrock-converse/` 用於 Amazon Bedrock Converse API，`cohere/` 用於 Cohere 模型，OpenAI 模型則不使用前綴。
`llm_response_field` | 否 | 模型回應中包含 LLM 答案的頂層欄位名稱。若模型的請求與回應格式不在 `llm_model` 前綴涵蓋範圍內，請使用此參數。設定此參數時，處理器會忽略 `llm_model` 前綴，並將提示以單一字串的形式放在 `inputs` 連接器參數中傳送，因此連接器的請求本文必須參照 `${parameters.inputs}`。
`llm_messages` | 視情況而定 | 在搜尋結果與對話歷史之後傳送給 LLM 的訊息陣列。每則訊息都是包含 `role` 與 `content` 陣列的物件。每個 `content` 元素包含下列其中一種物件：`text`（字串）、`image`（包含 `format` 以及 `data` 或 `url` 其中之一的物件），或 `document`（包含 `format`、`name` 與 `data` 的物件）。僅支援 OpenAI 模型及使用 Amazon Bedrock Converse API（`bedrock-converse/` 前綴）的模型。若未提供 `llm_question`，則為必要。
`system_prompt` | 否 | 此請求傳送給 LLM 的系統提示。會覆寫處理器中設定的 `system_prompt`。
`user_instructions` | 否 | 此請求傳送給 LLM 的使用者指示。會覆寫處理器中設定的 `user_instructions`。
`memory_id` | 否 | 若您提供 `memory_id`，管線會擷取指定記憶中最近的 10 則訊息，並將其加入 LLM 提示中。若您未指定 `memory_id`，先前的上下文就不會加入 LLM 提示中。
`context_size` | 否 | 傳送給 LLM 的搜尋結果數量。通常需要設定此參數以符合詞元大小限制，而此限制可能因模型而異。或者，您也可以使用 Search API 中的 `size` 參數來控制傳送給 LLM 的搜尋結果數量。
`message_size` | 否 | 傳送給 LLM 的訊息數量。與搜尋結果數量類似，這會影響 LLM 接收的詞元總數。未設定時，管線會使用預設訊息數量 `10`。
`timeout` | 否 | 管線等待透過連接器使用的遠端模型回應的秒數。預設值為 `30`。

若您的 LLM 設有詞元限制，請在 OpenSearch 查詢中設定 `size` 欄位，以限制搜尋回應中使用的文件數量。否則，RAG 管線會將搜尋結果中的每份文件都傳送給 LLM。
{: .note}

如果您詢問 LLM 有關當前的問題，它無法提供答案，因為它是以數年前的資料訓練而成。不過，如果您將最新資訊加入作為上下文，LLM 就能產生回應。例如，您可以詢問 LLM 紐約市都會區在 2023 年的人口數。您將建構一個包含 OpenSearch match 查詢與 LLM 查詢的查詢。請提供 `memory_id`，讓訊息儲存在適當的記憶物件中：

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

由於上下文中包含一份含有紐約市人口資訊的文件，LLM 能夠正確回答問題（不過因為它是以前幾年的資料訓練而成，回答中包含「projected」一詞）。回應中包含補充 RAG 資料裡相符的文件以及 LLM 回應：

<details open markdown="block">
<summary>
    回應
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

現在，您將在同一個對話中向 LLM 提出後續問題。同樣地，請在請求中提供 `memory_id`：

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

LLM 會正確識別對話的主題，並回傳相關的回應：

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

若要驗證兩則訊息是否都已新增至記憶，請將 `memory_ID` 提供給 Get Messages API：

```json
GET /_plugins/_ml/memory/znCqcI0BfUsSoeNTntd7/messages
```

回應包含這兩則訊息：

<details open markdown="block">
<summary>
    回應
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

- 探索我們的[教學]({{site.url}}{{site.baseurl}}/vector-search/tutorials/)，了解如何建置 AI 搜尋應用程式。 