---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Neural Sparse Search 工具"
has_children: false
has_toc: false
nav_order: 50
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# Neural Sparse Search 工具
**於 2.13 版推出**
{: .label .label-purple }
<!-- vale on -->

`NeuralSparseSearchTool` 會執行稀疏向量擷取。如需 neural sparse search 的詳細資訊，請參閱 [Neural sparse search]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/)。

## 步驟 1：註冊並部署稀疏編碼模型

OpenSearch 支援多個預先訓練的稀疏編碼模型。您可以使用其中一個模型，也可以使用自己的自訂模型。如需支援的預先訓練模型清單，請參閱 [Sparse encoding models]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/#sparse-encoding-models)。如需詳細資訊，請參閱 [OpenSearch-provided pretrained models]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/) 和 [Custom local models]({{site.url}}{{site.baseurl}}/ml-commons-plugin/custom-local-models/)。

在此範例中，您將使用 `amazon/neural-sparse/opensearch-neural-sparse-encoding-v2-distill` 預先訓練模型來進行匯入和搜尋。若要註冊模型並將其部署至 OpenSearch，請傳送下列請求：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "amazon/neural-sparse/opensearch-neural-sparse-encoding-v2-distill",
  "version": "1.0.0",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

OpenSearch 會回應模型註冊與部署工作的任務 ID：

```json
{
  "task_id": "M_9KY40Bk4MTqirc5lP8",
  "status": "CREATED"
}
```

您可以呼叫 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 來監視任務的狀態：

```json
GET _plugins/_ml/tasks/M_9KY40Bk4MTqirc5lP8
```
{% include copy-curl.html %}

模型註冊並部署後，任務 `state` 會變成 `COMPLETED`，且 OpenSearch 會傳回該模型的模型 ID：

```json
{
  "model_id": "Nf9KY40Bk4MTqirc6FO7",
  "task_type": "REGISTER_MODEL",
  "function_name": "SPARSE_ENCODING",
  "state": "COMPLETED",
  "worker_node": [
    "UyQSTQ3nTFa3IP6IdFKoug"
  ],
  "create_time": 1706767869692,
  "last_update_time": 1706767935556,
  "is_async": true
}
```

## 步驟 2：將資料匯入索引

首先，您將設定資料匯入管線，以使用上一個步驟中設定的稀疏編碼模型來編碼文件：

```json
PUT /_ingest/pipeline/pipeline-sparse
{
  "description": "An sparse encoding ingest pipeline",
  "processors": [
    {
      "sparse_encoding": {
        "model_id": "Nf9KY40Bk4MTqirc6FO7",
        "field_map": {
          "passage_text": "passage_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

接著，建立索引並將該管線指定為預設管線：

```json
PUT index_for_neural_sparse
{
  "settings": {
    "default_pipeline": "pipeline-sparse"
  },
  "mappings": {
    "properties": {
      "passage_embedding": {
        "type": "rank_features"
      },
      "passage_text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

最後，傳送大量請求將資料匯入索引：

```json
POST _bulk
{ "index" : { "_index" : "index_for_neural_sparse", "_id" : "1" } }
{ "passage_text" : "company AAA has a history of 123 years" }
{ "index" : { "_index" : "index_for_neural_sparse", "_id" : "2" } }
{ "passage_text" : "company AAA has over 7000 employees" }
{ "index" : { "_index" : "index_for_neural_sparse", "_id" : "3" } }
{ "passage_text" : "Jack and Mark established company AAA" }
{ "index" : { "_index" : "index_for_neural_sparse", "_id" : "4" } }
{ "passage_text" : "company AAA has a net profit of 13 millions in 2022" }
{ "index" : { "_index" : "index_for_neural_sparse", "_id" : "5" } }
{ "passage_text" : "company AAA focus on the large language models domain" }
```
{% include copy-curl.html %}

## 步驟 3：註冊將執行 NeuralSparseSearchTool 的流程代理程式

流程代理程式會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列請求，並提供步驟 1 中設定之模型的模型 ID。此模型會將您的查詢編碼為稀疏向量嵌入：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Neural_Sparse_Agent_For_RAG",
  "type": "flow",
  "tools": [
    {
      "type": "NeuralSparseSearchTool",
      "parameters": {
        "description":"use this tool to search data from the knowledge base of company AAA",
        "model_id": "Nf9KY40Bk4MTqirc6FO7",
        "index": "index_for_neural_sparse",
        "embedding_field": "passage_embedding",
        "source_field": ["passage_text"],
        "input": "${parameters.question}",
        "doc_size":2
      }
    }
  ]
}
```
{% include copy-curl.html %}

如需參數說明，請參閱 [Register parameters](#register-parameters)。

OpenSearch 會回應代理程式 ID：

```json
{
  "agent_id": "9X7xWI0Bpc3sThaJdY9i"
}
```

## 步驟 4：執行代理程式

執行代理程式之前，請確認您已新增範例 OpenSearch Dashboards `Sample web logs` 資料集。如需詳細資訊，請參閱 [Adding sample data]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

接著，傳送下列請求來執行代理程式：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "question":"how many employees does AAA have?"
  }
}
```
{% include copy-curl.html %}

OpenSearch 會傳回推論結果：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """{"_index":"index_for_neural_sparse","_source":{"passage_text":"company AAA has over 7000 employees"},"_id":"2","_score":30.586042}
{"_index":"index_for_neural_sparse","_source":{"passage_text":"company AAA has a history of 123 years"},"_id":"1","_score":16.088133}
"""
        }
      ]
    }
  ]
}
```

## 註冊參數

下表列出註冊代理程式時可用的所有工具參數。

參數	| 類型 | 必要/選用 | 說明	
:--- | :--- | :--- | :---
`model_id` | 字串 | 必要 | 搜尋時要使用的稀疏編碼模型 ID。
`index` | 字串 | 必要 | 要搜尋的索引。
`embedding_field` | 字串 | 必要 | 當 neural sparse 模型編碼原始文字文件時，編碼結果會儲存在某個欄位中。請將此欄位指定為 `embedding_field`。Neural sparse search 會計算查詢文字與文件 `embedding_field` 中文字的相似度分數，藉此將文件與查詢進行比對。
`source_field` | 字串 | 必要 | 要傳回的文件欄位。您可以提供多個欄位清單作為字串陣列，例如 `["field1", "field2"]`。
`input` | 字串 | 流程代理程式必要 | 來自流程代理程式參數的執行階段輸入。若使用大型語言模型 (LLM)，此欄位會填入 LLM 回應。
`name` | 字串  | 選用 | 工具名稱。當 LLM 需要為任務選取合適的工具時很有用。
`description` | 字串 | 選用 | 工具的說明。當 LLM 需要為任務選取合適的工具時很有用。
`doc_size` | 整數 | 選用 | 要擷取的文件數。預設為 `2`。
`nested_path` | 字串 | 選用 | 巢狀查詢之巢狀物件的路徑。僅用於巢狀欄位。預設為 `null`。

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

參數	| 類型 | 必要/選用 | 說明	
:--- | :--- | :--- | :---
`question` | 字串 | 必要 | 要傳送給 LLM 的自然語言問題。


## 測試工具

您可以將此工具做為代理程式工作流程的一部分來執行，也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用來測試個別工具或執行獨立作業。