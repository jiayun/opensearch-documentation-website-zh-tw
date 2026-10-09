---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "檢索增強生成"
nav_order: 115
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# 檢索增強生成處理器
於 2.12 版推出
{: .label .label-purple }

`retrieval_augmented_generation` 處理器是一種搜尋結果處理器，您可以在[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)中用於檢索增強生成 (RAG)。此處理器會攔截查詢結果、從對話記憶中擷取對話的先前訊息，並將提示傳送給大型語言模型 (LLM)。處理器收到 LLM 的回應後，會將回應儲存至對話記憶，並同時傳回原始 OpenSearch 查詢結果與 LLM 回應。

`retrieval_augmented_generation` 處理器支援 OpenAI、Amazon Bedrock 及 Cohere 模型。若要使用 Amazon Bedrock 或 Cohere 模型，請在 `llm_model` 值前面加上 `bedrock/`、`bedrock-converse/` 或 `cohere/`。沒有前置字元的值會視為 OpenAI 模型。若要使用其他模型，請設定 `llm_response_field` 參數。如需更多資訊，請參閱[步驟 6：使用管線進行 RAG]({{site.url}}{{site.baseurl}}/vector-search/ai-search/conversational-search/#step-6-use-the-pipeline-for-rag)。
{: .note}

## 請求本文欄位

下表列出所有可用的請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`model_id` | 字串 | 管線中所使用模型的 ID。必要。
`context_field_list` | 陣列 | 文件來源中包含的欄位清單，管線會將其用作 RAG 的上下文。必要。如需更多資訊，請參閱[上下文欄位清單](#context-field-list)。 
`system_prompt` | 字串 | 傳送給 LLM 的系統提示，用以調整其行為，例如回應語氣。可以是角色描述或一組指示。選用。
`user_instructions` | 字串 | 人工產生的指示，傳送給 LLM 以引導其產生結果。 
`tag` | 字串 | 處理器的識別碼。選用。
`description` | 字串 | 處理器的說明。選用。

### 上下文欄位清單

`context_field_list` 是文件來源中包含的欄位清單，管線會將其用作 RAG 的上下文。例如，假設您的 OpenSearch 索引包含一組文件，每份文件都包含 `title` 和 `text`：

```json
{
  "_index": "qa_demo",
  "_id": "SimKcIoBOVKVCYpk1IL-",
  "_source": {
    "title": "Abraham Lincoln 2",
    "text": "Abraham Lincoln was born on February 12, 1809, the second child of Thomas Lincoln and Nancy Hanks Lincoln, in a log cabin on Sinking Spring Farm near Hodgenville, Kentucky.[2] He was a descendant of Samuel Lincoln, an Englishman who migrated from Hingham, Norfolk, to its namesake, Hingham, Massachusetts, in 1638. The family then migrated west, passing through New Jersey, Pennsylvania, and Virginia.[3] Lincoln was also a descendant of the Harrison family of Virginia; his paternal grandfather and namesake, Captain Abraham Lincoln and wife Bathsheba (née Herring) moved the family from Virginia to Jefferson County, Kentucky.[b] The captain was killed in an Indian raid in 1786.[5] His children, including eight-year-old Thomas, Abraham's father, witnessed the attack.[6][c] Thomas then worked at odd jobs in Kentucky and Tennessee before the family settled in Hardin County, Kentucky, in the early 1800s.[6]\n"
  }
}
```

您可以在處理器中設定 `"context_field_list": ["text"]`，以指定只將 `text` 的內容傳送給 LLM。 

## 範例 

下列範例示範如何使用含有 `retrieval_augmented_generation` 處理器的搜尋管線。 

### 建立搜尋管線 

下列請求會建立含有 OpenAI 模型 `retrieval_augmented_generation` 處理器的搜尋管線：

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

### 使用搜尋管線

將 OpenSearch 查詢與 `ext` 物件結合，該物件會儲存 LLM 的生成式問答參數：

```json
GET /my_rag_test_data/_search?search_pipeline=rag_pipeline
{
  "query": {
    "match": {
      "text": "Abraham Lincoln"
    }
  },
  "ext": {
    "generative_qa_parameters": {
      "llm_model": "gpt-4o-mini",
      "llm_question": "Was Abraham Lincoln a good politician",
      "memory_id": "iXC4bI0BfUsSoeNTjS30",
      "context_size": 5,
      "message_size": 5,
      "timeout": 15
    }
  }
}
```
{% include copy-curl.html %}

如需設定對話式搜尋的更多資訊，請參閱[使用 RAG 的對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)。
