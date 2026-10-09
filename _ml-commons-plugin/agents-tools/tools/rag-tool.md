---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "RAG 工具"
has_children: false
has_toc: false
nav_order: 65
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# RAG 工具
**於 2.13 版導入**
{: .label .label-purple }
<!-- vale on -->

`RAGTool` 會執行檢索增強生成 (RAG)。如需 RAG 的更多資訊，請參閱[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)。

RAG 會呼叫大型語言模型 (LLM)，並透過在使用者問題之外一併提供相關的 OpenSearch 文件來補充其知識。若要從 OpenSearch 索引擷取相關文件，您需要一個能協助向量搜尋的文字嵌入模型。

RAG 工具支援下列搜尋方法：

- [神經搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-search/)：密集向量擷取，使用文字嵌入模型。
- [神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/)：稀疏向量擷取，使用稀疏編碼模型。

## 開始之前

若要註冊並部署文字嵌入模型與 LLM，並將資料匯入索引，請執行[代理程式與工具教學]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents-tools-tutorial/)的步驟 1 至 5。

下列範例使用神經搜尋。若要設定神經稀疏搜尋並部署稀疏編碼模型，請參閱[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/)。

<!-- vale off -->
## 步驟 1：註冊將執行 RAGTool 的流程代理程式
<!-- vale on -->

流程代理程式會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列請求，並在 `embedding_model_id` 參數中提供文字嵌入模型 ID，在 `inference_model_id` 參數中提供 LLM 模型 ID：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_RagTool",
  "type": "flow",
  "description": "this is a test flow agent",
  "tools": [
  {
    "type": "RAGTool",
    "description": "A description of the tool",
    "parameters": {
      "embedding_model_id": "Hv_PY40Bk4MTqircAVmm",
      "inference_model_id": "SNzSY40B_1JGmyB0WbfI",
      "index": "my_test_data",
      "embedding_field": "embedding",
      "query_type": "neural",
      "source_field": [
        "text"
      ],
      "input": "${parameters.question}",
      "prompt": "\n\nHuman:You are a professional data analyst. You will always answer question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say don't know. \n\n Context:\n${parameters.output_field}\n\nHuman:${parameters.question}\n\nAssistant:"
    }
  }
]
}
```
{% include copy-curl.html %} 

參數說明請參閱[註冊參數](#register-parameters)。

OpenSearch 會回應一個代理程式 ID：

```json
{
  "agent_id": "9X7xWI0Bpc3sThaJdY9i"
}
```

若要建立包含 `RAGTool` 的對話式代理程式，請參閱[對話式代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational/)。

## 步驟 2：執行代理程式

在執行代理程式之前，請確認您已新增 OpenSearch Dashboards 的 `Sample web logs` 範例資料集。若要進一步了解，請參閱[新增範例資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

接著，傳送下列請求來執行代理程式：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "question": "what's the population increase of Seattle from 2021 to 2023"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會執行向量搜尋並傳回相關文件：

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

Parameter	| Type | Required/Optional | Description	
:--- | :--- | :--- | :---
`embedding_model_id` | String | 必要 | 用於產生向量嵌入的模型 ID。
`inference_model_id` | String | 必要 | 用於推論的 LLM 模型 ID。
`index` | String | 必要 | 從中擷取相關文件以傳遞給 LLM 的索引。
`embedding_field` | String | 必要 | 當模型對原始文字文件進行編碼時，編碼結果會儲存在一個欄位中。請將此欄位指定為 `embedding_field`。神經搜尋會透過計算查詢文字與文件 `embedding_field` 中文字之間的相似度分數，將文件與查詢進行比對。
`source_field` | String | 必要 | 要傳回的文件欄位。您可以字串陣列的形式提供多個欄位的清單，例如 `["field1", "field2"]`。
`input` | String | 流程代理程式必要 | 來自流程代理程式參數的執行階段輸入。若使用 LLM，此欄位會填入 LLM 的回應。
`output_field` | String | 選用 | 輸出欄位的名稱。預設為 `response`。
`query_type` | String | 選用 | 指定執行神經搜尋時要執行的查詢類型。有效值為 `neural` (用於密集擷取) 與 `neural_sparse` (用於稀疏擷取)。預設為 `neural`。
`doc_size` | Integer | 選用 | 要擷取的文件數量。預設為 `2`。
`prompt` | String | 選用 | 提供給 LLM 的提示。
`k` | Integer | 選用 | 執行神經搜尋時要搜尋的最近鄰居數量。預設為 10。
`enable_Content_Generation` | Boolean | 選用 | 若為 `true`，則傳回由 LLM 產生的結果。若為 `false`，則直接傳回結果，不進行 LLM 輔助的內容生成。預設為 `true`。
`nested_path` | String | 選用 | 巢狀查詢所用的巢狀物件路徑。僅用於巢狀欄位。預設為 `null`。

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

Parameter	| Type | Required/Optional | Description	
:--- | :--- | :--- | :---
`question` | String | 必要 | 要傳送給 LLM 的自然語言問題。 

## 測試工具

您可以將此工具作為代理程式工作流程的一部分執行，也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用於測試個別工具或執行獨立作業。