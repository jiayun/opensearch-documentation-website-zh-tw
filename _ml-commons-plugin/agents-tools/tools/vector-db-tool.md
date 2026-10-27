---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "向量資料庫工具"
has_children: false
has_toc: false
nav_order: 110
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# 向量資料庫工具
**於 2.13 版導入**
{: .label .label-purple }
<!-- vale on -->

`VectorDBTool` 會執行稠密向量擷取。如需 OpenSearch 向量資料庫功能的更多資訊，請參閱[向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/)。

## 步驟 1：註冊並部署文字嵌入模型

OpenSearch 支援多種預先訓練的模型。您可以使用其中一種模型、使用自己的自訂模型，或為外部託管的模型建立連接器。如需支援的預先訓練模型清單，請參閱 [OpenSearch 提供的預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/)。如需自訂模型的更多資訊，請參閱 [自訂本機模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/custom-local-models/)。如需整合外部託管模型的資訊，請參閱 [連線至外部託管的模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。

在本範例中，您將使用 `huggingface/sentence-transformers/all-MiniLM-L12-v2` 預先訓練模型進行匯入與搜尋。若要註冊並部署該模型至 OpenSearch，請傳送以下請求：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "huggingface/sentence-transformers/all-MiniLM-L12-v2",
  "version": "1.0.2",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %} 

OpenSearch 會回應模型註冊與部署任務的任務 ID：

```json
{
  "task_id": "M_9KY40Bk4MTqirc5lP8",
  "status": "CREATED"
}
```

您可以呼叫 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 來監視任務狀態：

```json
GET _plugins/_ml/tasks/M_9KY40Bk4MTqirc5lP8
```
{% include copy-curl.html %} 

模型註冊並部署完成後，任務 `state` 會變為 `COMPLETED`，且 OpenSearch 會傳回該模型的模型 ID：

```json
{
  "model_id": "Hv_PY40Bk4MTqircAVmm",
  "task_type": "REGISTER_MODEL",
  "function_name": "TEXT_EMBEDDING",
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

首先，您將設定資料匯入管線，使用上一個步驟設定的文字嵌入模型來編碼文件：

```json
PUT /_ingest/pipeline/test-pipeline-local-model
{
  "description": "text embedding pipeline",
  "processors": [
    {
      "text_embedding": {
        "model_id": "Hv_PY40Bk4MTqircAVmm",
        "field_map": {
          "text": "embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %} 

接著，建立 k-NN 索引，並將該管線指定為預設管線：

```json
PUT my_test_data
{
  "mappings": {
    "properties": {
      "text": {
        "type": "text"
      },
      "embedding": {
        "type": "knn_vector",
        "dimension": 384,
        "space_type": "cosinesimil"
      }
    }
  },
  "settings": {
    "index": {
      "default_pipeline": "test-pipeline-local-model",
      "knn": "true"
    }
  }
}
```
{% include copy-curl.html %} 

最後，傳送大量請求，將資料匯入索引：

```json
POST _bulk
{"index": {"_index": "my_test_data", "_id": "1"}}
{"text": "Chart and table of population level and growth rate for the Ogden-Layton metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of Ogden-Layton in 2023 is 750,000, a 1.63% increase from 2022.\nThe metro area population of Ogden-Layton in 2022 was 738,000, a 1.79% increase from 2021.\nThe metro area population of Ogden-Layton in 2021 was 725,000, a 1.97% increase from 2020.\nThe metro area population of Ogden-Layton in 2020 was 711,000, a 2.16% increase from 2019."}
{"index": {"_index": "my_test_data", "_id": "2"}}
{"text": "Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."}
{"index": {"_index": "my_test_data", "_id": "3"}}
{"text": "Chart and table of population level and growth rate for the Chicago metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Chicago in 2023 is 8,937,000, a 0.4% increase from 2022.\\nThe metro area population of Chicago in 2022 was 8,901,000, a 0.27% increase from 2021.\\nThe metro area population of Chicago in 2021 was 8,877,000, a 0.14% increase from 2020.\\nThe metro area population of Chicago in 2020 was 8,865,000, a 0.03% increase from 2019."}
{"index": {"_index": "my_test_data", "_id": "4"}}
{"text": "Chart and table of population level and growth rate for the Miami metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Miami in 2023 is 6,265,000, a 0.8% increase from 2022.\\nThe metro area population of Miami in 2022 was 6,215,000, a 0.78% increase from 2021.\\nThe metro area population of Miami in 2021 was 6,167,000, a 0.74% increase from 2020.\\nThe metro area population of Miami in 2020 was 6,122,000, a 0.71% increase from 2019."}
{"index": {"_index": "my_test_data", "_id": "5"}}
{"text": "Chart and table of population level and growth rate for the Austin metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Austin in 2023 is 2,228,000, a 2.39% increase from 2022.\\nThe metro area population of Austin in 2022 was 2,176,000, a 2.79% increase from 2021.\\nThe metro area population of Austin in 2021 was 2,117,000, a 3.12% increase from 2020.\\nThe metro area population of Austin in 2020 was 2,053,000, a 3.43% increase from 2019."}
{"index": {"_index": "my_test_data", "_id": "6"}}
{"text": "Chart and table of population level and growth rate for the Seattle metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Seattle in 2023 is 3,519,000, a 0.86% increase from 2022.\\nThe metro area population of Seattle in 2022 was 3,489,000, a 0.81% increase from 2021.\\nThe metro area population of Seattle in 2021 was 3,461,000, a 0.82% increase from 2020.\\nThe metro area population of Seattle in 2020 was 3,433,000, a 0.79% increase from 2019."}
```
{% include copy-curl.html %} 

## 步驟 3：註冊將執行 VectorDBTool 的流程代理程式

流程代理程式 (flow agent) 會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列請求，並提供步驟 1 所設定模型的模型 ID。此模型會將您的查詢編碼為向量嵌入：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_VectorDB",
  "type": "flow",
  "description": "this is a test agent",
  "tools": [
    {
      "type": "VectorDBTool",
      "parameters": {
        "model_id": "Hv_PY40Bk4MTqircAVmm",
        "index": "my_test_data",
        "embedding_field": "embedding",
        "source_field": ["text"],
        "input": "${parameters.question}"
      }
    }
  ]
}
```
{% include copy-curl.html %}

如需參數說明，請參閱[註冊參數](#register-parameters)。

OpenSearch 會回應一個代理程式 ID：

```json
{
  "agent_id": "9X7xWI0Bpc3sThaJdY9i"
}
```

## 步驟 4：執行代理程式

傳送下列請求以執行代理程式：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "question": "what's the population increase of Seattle from 2021 to 2023"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會執行向量搜尋並傳回相關的文件：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """{"_index":"my_test_data","_source":{"text":"Chart and table of population level and growth rate for the Seattle metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\n
          The current metro area population of Seattle in 2023 is 3,519,000, a 0.86% increase from 2022.\\n
          The metro area population of Seattle in 2022 was 3,489,000, a 0.81% increase from 2021.\\n
          The metro area population of Seattle in 2021 was 3,461,000, a 0.82% increase from 2020.\\n
          The metro area population of Seattle in 2020 was 3,433,000, a 0.79% increase from 2019."},"_id":"6","_score":0.8173238}
        {"_index":"my_test_data","_source":{"text":"Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\n
        The current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\n
        The metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\n
        The metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\n
        The metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."},"_id":"2","_score":0.6641471}
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
`model_id` | 字串 | 必要 | 搜尋時要使用之模型的模型 ID。
`index` | 字串 | 必要 | 要搜尋的索引。此值也可由 LLM 在執行階段提供；執行階段的值優先於註冊的預設值。
`embedding_field` | 字串 | 必要 | 當模型將原始文字文件編碼時，編碼結果會儲存在某個欄位中。請將此欄位指定為 `embedding_field`。OpenSearch 會計算查詢文字與文件 `embedding_field` 中文字之間的相似性分數，藉此將文件與查詢進行比對。此值也可由 LLM 在執行階段提供；執行階段的值優先於註冊的預設值。
`source_field` | 字串 | 必要 | 要傳回的文件欄位。您可以提供多個欄位，以字串陣列的形式表示，例如 `["field1", "field2"]`。
`input` | 字串 | 流程代理程式必要 | 來自流程代理程式參數的執行階段輸入。若使用大型語言模型 (LLM)，此欄位會填入 LLM 的回應。
`doc_size` | 整數 | 選用 | 要擷取的文件數量。預設為 `2`。
`k` | 整數 | 選用 | 要搜尋的最近鄰數量。預設為 `10`。
`nested_path` | 字串 | 選用 | 巢狀查詢所用巢狀物件的路徑。僅用於巢狀欄位。預設為 `null`。

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

參數	| 類型 | 必要／選用 | 說明	
:--- | :--- | :--- | :---
`question` | 字串 | 必要 | 要傳送給 LLM 的自然語言問題。

## 測試工具

您可以將此工具做為代理程式工作流程的一部分來執行，或使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用來測試個別工具或執行獨立作業。