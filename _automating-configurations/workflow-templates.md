---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作流程範本"
nav_order: 25
---

# 工作流程範本

OpenSearch 為一些常見的機器學習 (ML) 使用案例提供多種工作流程範本。使用範本可以簡化複雜的設定流程，並為語意搜尋或對話式搜尋等使用案例提供許多預設值。

您可以在呼叫 [Create Workflow API]({{site.url}}{{site.baseurl}}/automating-configurations/api/create-workflow/) 時指定工作流程範本：

- 若要使用 OpenSearch 提供的工作流程範本，請將範本使用案例指定為 `use_case` 查詢參數（請參閱[範例](#example)）。如需 OpenSearch 提供的範本清單，請參閱[支援的工作流程範本](#supported-workflow-templates)。

- 若要使用自訂工作流程範本，請在請求本文中提供完整的範本。如需自訂範本的範例，請參閱 [JSON 範本範例]({{site.url}}{{site.baseurl}}/automating-configurations/api/create-workflow/#example-request-register-and-deploy-a-remote-model-json)或 [YAML 範本範例]({{site.url}}{{site.baseurl}}/automating-configurations/api/create-workflow/#example-request-register-and-deploy-an-externally-hosted-model-in-yaml)。

若要佈建工作流程，請將 `provision=true` 指定為查詢參數。

## 範例

在此範例中，您將設定 `semantic_search_with_cohere_embedding_query_enricher` 工作流程範本。使用此範本建立的工作流程會執行下列組態步驟：

- 部署外部託管的 Cohere 模型
- 使用該模型建立資料匯入管線
- 建立範例向量索引，並設定搜尋管線以定義該索引的預設模型 ID

### 步驟 1：建立並佈建工作流程

傳送下列請求，以使用 `semantic_search_with_cohere_embedding_query_enricher` 工作流程範本建立並佈建工作流程。此範本唯一必要的請求本文欄位是 Cohere Embed 模型的 API 金鑰：

```json
POST /_plugins/_flow_framework/workflow?use_case=semantic_search_with_cohere_embedding_query_enricher&provision=true
{
    "create_connector.credential.key" : "<YOUR API KEY>"
}
```
{% include copy-curl.html %}

OpenSearch 會回應所建立工作流程的工作流程 ID：

```json
{
  "workflow_id" : "8xL8bowB8y25Tqfenm50"
}
```

上一個步驟中的工作流程會建立預設向量索引。預設索引名稱為 `my-nlp-index`：

```json
{
  "create_index.name": "my-nlp-index"
}
```

如需此工作流程範本的所有預設參數值，請參閱 [Cohere Embed 語意搜尋預設值](https://github.com/opensearch-project/flow-framework/blob/2.13/src/main/resources/defaults/cohere-embedding-semantic-search-defaults.json)。

### 步驟 2：將文件匯入索引

若要將文件匯入上一個步驟中建立的索引，請傳送下列請求：

```json
PUT /my-nlp-index/_doc/1
{
  "passage_text": "Hello world",
  "id": "s1"
}
```
{% include copy-curl.html %}

### 步驟 3：執行向量搜尋

若要對您的索引執行向量搜尋，請使用 [`neural` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural/)子句：

```json
GET /my-nlp-index/_search
{
  "_source": {
    "excludes": [
      "passage_embedding"
    ]
  },
  "query": {
    "neural": {
      "passage_embedding": {
        "query_text": "Hi world",
        "k": 100
      }
    }
  }
}
```
{% include copy-curl.html %}

## 參數

每個工作流程範本都有已定義的結構描述，以及一組在每個步驟中具有預先定義預設值的 API。如需範本參數預設值的詳細資訊，請參閱[支援的工作流程範本](#supported-workflow-templates)。

### 覆寫預設值

若要覆寫範本的預設值，請在傳送建立工作流程請求時，於請求本文中提供新的值。例如，下列請求會變更 `semantic_search_with_cohere_embedding` 範本的 Cohere 模型、`text_embedding` 處理器輸出欄位的名稱，以及稀疏索引的名稱：

```json
POST /_plugins/_flow_framework/workflow?use_case=semantic_search_with_cohere_embedding
{
    "create_connector.model" : "embed-multilingual-v3.0",
    "text_embedding.field_map.output": "book_embedding",
    "create_index.name": "sparse-book-index"
}
```
{% include copy-curl.html %}

## 檢視工作流程資源

您建立的工作流程已佈建語意搜尋所需的所有資源。若要檢視已佈建的資源，請呼叫 [Get Workflow Status API]({{site.url}}{{site.baseurl}}/automating-configurations/api/get-workflow-status/)，並提供您工作流程的 `workflowID`：

```json
GET /_plugins/_flow_framework/workflow/8xL8bowB8y25Tqfenm50/_status
```
{% include copy-curl.html %}

## 支援的工作流程範本

若要使用工作流程範本，請在建立工作流程時於 `use_case` 查詢參數中指定該範本。支援下列範本：

<details open markdown="block">
  <summary>
    支援下列範本：
  </summary>

- 模型部署範本：
  - [Amazon Bedrock Titan 嵌入](#amazon-bedrock-titan-embedding)
  - [Amazon Bedrock Titan 多模態](#amazon-bedrock-titan-multimodal)
  - [Cohere 嵌入](#cohere-embedding)
  - [Cohere 聊天](#cohere-chat)
  - [OpenAI 嵌入](#openai-embedding)
  - [OpenAI 聊天](#openai-chat)
- 語意搜尋範本：
  - [語意搜尋](#semantic-search)
  - [使用查詢擴充器的語意搜尋](#semantic-search-with-a-query-enricher)
  - [使用本機模型的語意搜尋](#semantic-search-using-a-local-model)
  - [使用 Cohere 嵌入模型的語意搜尋](#semantic-search-using-a-cohere-embedding-model)
  - [使用 Cohere 嵌入模型搭配查詢擴充器的語意搜尋](#semantic-search-using-cohere-embedding-models-with-a-query-enricher)
  - [使用 Cohere 嵌入模型搭配重新編製索引的語意搜尋](#semantic-search-using-cohere-embedding-models-with-reindexing)
- 神經稀疏搜尋範本：
  - [神經稀疏搜尋](#neural-sparse-search)
- 多模態搜尋範本：
  - [多模態搜尋](#multimodal-search)
  - [使用 Amazon Bedrock Titan 的多模態搜尋](#multimodal-search-using-amazon-bedrock-titan)
- 混合搜尋範本：
  - [混合搜尋](#hybrid-search)
  - [使用本機模型的混合搜尋](#hybrid-search-using-a-local-model)
- 對話式搜尋範本：
  - [使用 LLM 的對話式搜尋](#conversational-search-using-an-llm)
- 代理式搜尋範本：
  - [使用流程代理程式的代理式搜尋](#agentic-search-with-a-flow-agent)
  - [使用對話式代理程式的代理式搜尋](#agentic-search-with-a-conversational-agent)

</details>

## 模型部署範本

下列工作流程範本可設定模型部署。

### Amazon Bedrock Titan 嵌入

此工作流程會建立並部署 Amazon Bedrock 嵌入模型（預設為 `titan-embed-text-v1`）。

- **使用案例**：`bedrock_titan_embedding_model_deploy`
- **建立的元件**：Amazon Bedrock Titan 嵌入模型的連接器與模型
- **必要參數**：
  - `create_connector.credential.access_key`
  - `create_connector.credential.secret_key`
  - `create_connector.credential.session_token`
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/bedrock-titan-embedding-defaults.json)

**注意**：需要 AWS 憑證以及 Amazon Bedrock 的存取權。

### Amazon Bedrock Titan 多模態

此工作流程會建立並部署 Amazon Bedrock 多模態嵌入模型（預設為 `titan-embed-image-v1`）。

- **使用案例**：`bedrock_titan_multimodal_model_deploy`
- **建立的元件**：用於 Amazon Bedrock Titan 多模態嵌入的連接器與模型
- **必要參數**： 
  - `create_connector.credential.access_key`
  - `create_connector.credential.secret_key`
  - `create_connector.credential.session_token`
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/bedrock-titan-multimodal-defaults.json)

**注意**：需要 AWS 憑證與 Amazon Bedrock 存取權限。

### Cohere 嵌入

此工作流程會建立並部署 Cohere 嵌入模型（預設為 `embed-english-v3.0`）。

- **使用案例**：`cohere_embedding_model_deploy`
- **建立的元件**：用於 Cohere 嵌入的連接器與模型
- **必要參數**： 
  - `create_connector.credential.key`
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/cohere-embedding-defaults.json)

**注意**：需要 Cohere API 金鑰。

### Cohere 聊天

此工作流程會建立並部署 Cohere 聊天模型（預設為 Cohere Command）。

- **使用案例**：`cohere_chat_model_deploy`
- **建立的元件**：用於 Cohere 聊天的連接器與模型
- **必要參數**： 
  - `create_connector.credential.key`
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/cohere-chat-defaults.json)

**注意**：需要 Cohere API 金鑰。

### OpenAI 嵌入

此工作流程會建立並部署 OpenAI 嵌入模型（預設為 `text-embedding-ada-002`）。

- **使用案例**：`open_ai_embedding_model_deploy`
- **建立的元件**：用於 OpenAI 嵌入的連接器與模型
- **必要參數**： 
  - `create_connector.credential.key`
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/openai-embedding-defaults.json)

**注意**：需要 OpenAI API 金鑰。

### OpenAI 聊天

此工作流程會建立並部署 OpenAI 聊天模型（預設為 `gpt-3.5-turbo`）。

- **使用案例**：`openai_chat_model_deploy`
- **建立的元件**：用於 OpenAI 聊天的連接器與模型
- **必要參數**： 
  - `create_connector.credential.key`
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/openai-chat-defaults.json)

**注意**：需要 OpenAI API 金鑰。

## 語意搜尋範本

下列工作流程範本可設定語意搜尋。

### 語意搜尋

此工作流程會設定[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)。

- **使用案例**：`semantic_search`
- **建立的元件**： 
  - 包含 `text_embedding` 處理器的資料匯入管線
  - 設定為使用該管線的向量索引
- **必要參數**： 
  - `create_ingest_pipeline.model_id`：要使用的文字嵌入模型的模型 ID
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/semantic-search-defaults.json)

### 搭配查詢增強器的語意搜尋

此工作流程會設定[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)，並為神經查詢設定預設模型。

- **使用案例**：`semantic_search_with_query_enricher`
- **建立的元件**： 
  - 包含 `text_embedding` 處理器的資料匯入管線
  - 設定為使用該管線的向量索引
  - 為神經查詢設定預設模型 ID 的 [`query_enricher`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/neural-query-enricher/) 搜尋處理器。
- **必要參數**： 
  - `create_ingest_pipeline.model_id`：要使用的文字嵌入模型的模型 ID
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/semantic-search-query-enricher-defaults.json)

### 使用本機模型的語意搜尋

此工作流程會設定[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)，並部署預先訓練的模型。

- **使用案例**：`semantic_search_with_local_model`
- **建立的元件**：
  - 預先訓練的模型（預設為 `huggingface/sentence-transformers/paraphrase-MiniLM-L3-v2`）
  - 包含 `text_embedding` 處理器的資料匯入管線
  - 設定為使用該管線的向量索引
  - 為神經查詢設定預設模型 ID 的 [`query_enricher`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/neural-query-enricher/) 搜尋處理器。
- **必要參數**：無
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/semantic-search-with-local-model-defaults.json)

**注意**：使用採用預設組態的本機預先訓練模型。

### 使用 Cohere 嵌入模型的語意搜尋

此工作流程會設定[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)，並部署 Cohere 嵌入模型。

- **使用案例**：`semantic_search_with_cohere_embedding`
- **建立的元件**：
  - Cohere 嵌入模型（預設為 `embed-english-v3.0`）的連接器與部署
  - 包含 `text_embedding` 處理器的資料匯入管線
  - 設定為使用該管線的向量索引
- **必要參數**：
  - `create_connector.credential.key`：Cohere 模型的 API 金鑰
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/cohere-embedding-semantic-search-defaults.json)

**注意**：需要 Cohere API 金鑰。

### 使用 Cohere 嵌入模型並搭配查詢增強器的語意搜尋

此工作流程會設定[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)、部署 Cohere 嵌入模型，並新增查詢增強器搜尋處理器。

- **使用案例**：`semantic_search_with_cohere_embedding_query_enricher`
- **建立的元件**：
  - Cohere 嵌入模型的連接器與部署
  - 包含 `text_embedding` 處理器的資料匯入管線
  - 設定為使用該管線的向量索引
  - 為神經查詢設定預設模型 ID 的 [`query_enricher`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/neural-query-enricher/) 搜尋處理器。
- **必要參數**：
  - `create_connector.credential.key`：Cohere 模型的 API 金鑰
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/cohere-embedding-semantic-search-with-query-enricher-defaults.json)

**注意**：需要 Cohere API 金鑰。 

### 使用 Cohere 嵌入模型並重新編製索引的語意搜尋

此工作流程會使用 Cohere 嵌入模型設定[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)，並對現有索引重新編製索引。

- **使用案例**：`semantic_search_with_reindex`
- **建立的元件**：
  - Cohere 嵌入模型的連接器與部署
  - 設定為使用該管線的向量索引
  - 重新編製索引的程序
- **必要參數**：
  - `create_connector.credential.key`：Cohere 模型的 API 金鑰
  - `reindex.source_index`：要重新編製索引的來源索引
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/semantic-search-with-reindex-defaults.json)

**注意**：使用 Cohere 嵌入模型，將來源索引重新編製索引至新設定的 k-NN 索引。

## 神經稀疏搜尋範本

下列工作流程範本會設定[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/)。

### 神經稀疏搜尋

此工作流程會設定[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/)。

- **使用案例**：`local_neural_sparse_search_bi_encoder`
- **建立的元件**：
  - 本機託管的預先訓練稀疏編碼模型（預設為 `amazon/neural-sparse/opensearch-neural-sparse-encoding-v1`）
  - 含有 `sparse_encoding` 處理器的資料匯入管線
  - 以該管線設定的向量索引
- **必要參數**：無
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/local-sparse-search-biencoder-defaults.json)

## 多模態搜尋範本

下列工作流程範本會設定[多模態搜尋]({{site.url}}{{site.baseurl}}/search-plugins/multimodal-search/)。

### 多模態搜尋

此工作流程會設定[多模態搜尋]({{site.url}}{{site.baseurl}}/search-plugins/multimodal-search/)。

- **使用案例**：`multimodal_search`
- **建立的元件**：
  - 含有 `text_image_embedding` 處理器的資料匯入管線
  - 以該管線設定的向量索引
- **必要參數**：
  - `create_ingest_pipeline.model_id`：要使用的多模態嵌入模型之模型 ID
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/multi-modal-search-defaults.json)

### 使用 Amazon Bedrock Titan 的多模態搜尋

此工作流程會部署 Amazon Bedrock 多模態模型並設定多模態搜尋管線。

- **使用案例**：`multimodal_search_with_bedrock_titan`
- **建立的元件**：
  - Amazon Bedrock Titan 多模態嵌入模型連接器與部署
  - 含有 `text_image_embedding` 處理器的資料匯入管線
  - 以該管線設定的多模態搜尋向量索引
- **必要參數**：
  - `create_connector.credential.access_key`
  - `create_connector.credential.secret_key`
  - `create_connector.credential.session_token`
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/multimodal-search-bedrock-titan-defaults.json)

**注意**：需要 AWS 憑證以及 Amazon Bedrock 的存取權。

## 混合搜尋範本

下列工作流程範本會設定[混合搜尋]({{site.url}}{{site.baseurl}}/search-plugins/hybrid-search/)。

### 混合搜尋

此工作流程會設定[混合搜尋]({{site.url}}{{site.baseurl}}/search-plugins/hybrid-search/)。

- **使用案例**：`hybrid_search`
- **建立的元件**：
  - 資料匯入管線
  - 以該管線設定的向量索引
  - 含有 `normalization_processor` 的搜尋管線
- **必要參數**：
  - `create_ingest_pipeline.model_id`：要使用的文字嵌入模型之模型 ID
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/hybrid-search-defaults.json)

### 使用本機模型的混合搜尋

此工作流程會設定混合搜尋並部署預先訓練模型。

- **使用案例**：`hybrid_search_with_local_model`
- **建立的元件**：
  - 預先訓練模型（預設為 `huggingface/sentence-transformers/paraphrase-MiniLM-L3-v2`）
  - 資料匯入管線
  - 以該管線設定的向量索引
  - 含有 `normalization_processor` 的搜尋管線
- **必要參數**：無
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/hybrid-search-with-local-model-defaults.json)

**注意**：使用本機預先訓練模型進行混合搜尋設定。

## 對話式搜尋範本

下列工作流程範本會設定[使用 RAG 的對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)。

### 使用 LLM 的對話式搜尋

此工作流程會部署大型語言模型並設定對話式搜尋管線。

- **使用案例**：`conversational_search_with_llm_deploy`
- **建立的元件**：
  - 聊天模型（預設為 Cohere Command）連接器與部署
  - 含有 `retrieval_augmented_generation` 處理器的搜尋管線
- **必要參數**：
  - `create_connector.credential.key`：LLM 的 API 金鑰
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/conversational-search-defaults.json)

**注意**：需要所選語言模型的 API 金鑰。

## 代理式搜尋範本

下列工作流程範本會設定[代理式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/)。

### 使用流程代理程式的代理式搜尋

此工作流程會部署 Amazon Bedrock 聊天模型，並使用[流程代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/flow-agent/)設定代理式搜尋管線。

- **使用案例**：`agentic_search_with_flow_agent`
- **建立的元件**：
  - Amazon Bedrock 連接器與遠端聊天模型（預設為 Claude 4 Sonnet）
  - `QueryPlanningTool`
  - 連接至 `QueryPlanningTool` 的流程代理程式
  - 含有 `agentic_query_translator` 請求處理器與 `agentic_context` 回應處理器的搜尋管線
- **必要參數**：
  - `create_connector.credential.access_key`
  - `create_connector.credential.secret_key`
  - `create_connector.credential.session_token`
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/agentic-search-with-flow-agent-defaults.json)

**注意**：需要 AWS 憑證以及 Amazon Bedrock 的存取權。

### 使用對話式代理程式的代理式搜尋

此工作流程會部署 Amazon Bedrock 聊天模型，並使用具有對話記憶與多項工具的[對話式代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-converse/)設定代理式搜尋管線。

- **使用案例**：`agentic_search_with_conversational_agent`
- **建立的元件**：
  - Amazon Bedrock 連接器與遠端聊天模型（預設為 Claude 4 Sonnet）
  - `QueryPlanningTool`、`ListIndexTool` 與 `IndexMappingTool`
  - 具有對話記憶與全部三項工具的對話式代理程式
  - 含有 `agentic_query_translator` 請求處理器與 `agentic_context` 回應處理器的搜尋管線
- **必要參數**：
  - `create_connector.credential.access_key`
  - `create_connector.credential.secret_key`
  - `create_connector.credential.session_token`
- [預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/agentic-search-with-conversational-agent-defaults.json)

**注意**：需要 AWS 憑證以及 Amazon Bedrock 的存取權。
