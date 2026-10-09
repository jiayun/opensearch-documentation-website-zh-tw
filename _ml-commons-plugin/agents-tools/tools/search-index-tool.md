---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Search Index 工具"
has_children: false
has_toc: false
nav_order: 90
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# Search Index 工具
**於 2.13 版推出**
{: .label .label-purple }
<!-- vale on -->

`SearchIndexTool` 會使用以查詢領域特定語言 (DSL) 撰寫的查詢來搜尋索引，並傳回查詢結果。

## 步驟 1：註冊將執行 SearchIndexTool 的流程代理程式

流程代理程式會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_Search_Index_Tool",
  "type": "flow",
  "description": "this is a test for search index tool",
  "memory": {
    "type": "demo"
  },
  "tools": [
    {
      "type": "SearchIndexTool"
    }
  ]
}
```
{% include copy-curl.html %} 

OpenSearch 會回應代理程式 ID：

```json
{
  "agent_id": "9X7xWI0Bpc3sThaJdY9i"
}
```

## 步驟 2：執行代理程式

執行代理程式之前，請確認您已新增範例 OpenSearch Dashboards `Sample eCommerce orders` 資料集。若要進一步了解，請參閱[新增範例資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

接著，傳送下列請求來執行代理程式。`SearchIndexTool` 接受一個名為 `input` 的參數。此參數包含索引名稱與查詢：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "input": "{\"index\": \"opensearch_dashboards_sample_data_ecommerce\", \"query\": {\"size\": 20,  \"_source\": \"email\"}}"
  }
}
```
{% include copy-curl.html %} 

如需參數說明，請參閱[執行參數](#execute-parameters)。

前一個請求中傳入的查詢等同於下列查詢：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 20,
  "_source": "email"
}
```

OpenSearch 會傳回查詢結果：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"eddie@underwood-family.zzz"},"_id":"_bJVWY0BAehlDanXJnAJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"mary@bailey-family.zzz"},"_id":"_rJVWY0BAehlDanXJnAJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"gwen@butler-family.zzz"},"_id":"_7JVWY0BAehlDanXJnAJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"diane@chandler-family.zzz"},"_id":"ALJVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"eddie@weber-family.zzz"},"_id":"AbJVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"diane@goodwin-family.zzz"},"_id":"ArJVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"oliver@rios-family.zzz"},"_id":"A7JVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"abd@sutton-family.zzz"},"_id":"BLJVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"wilhemina st.@tran-family.zzz"},"_id":"BbJVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"rabbia al@baker-family.zzz"},"_id":"BrJVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"rabbia al@romero-family.zzz"},"_id":"B7JVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"eddie@gregory-family.zzz"},"_id":"CLJVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"sultan al@pratt-family.zzz"},"_id":"CbJVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"eddie@wolfe-family.zzz"},"_id":"CrJVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"sultan al@thompson-family.zzz"},"_id":"C7JVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"sultan al@boone-family.zzz"},"_id":"DLJVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"george@hubbard-family.zzz"},"_id":"DbJVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"boris@maldonado-family.zzz"},"_id":"DrJVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"yahya@rivera-family.zzz"},"_id":"D7JVWY0BAehlDanXJnEJ","_score":1.0}
{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"email":"brigitte@morris-family.zzz"},"_id":"ELJVWY0BAehlDanXJnEJ","_score":1.0}
"""
        }
      ]
    }
  ]
}
```

## 執行參數

下表列出註冊代理程式時可用的所有工具參數。

參數 | 類型 | 說明
:--- | :--- | :---
`input`| 字串 | 要用於搜尋的索引名稱與查詢，格式為 JSON。`index` 參數包含索引名稱，而 `query` 參數包含以 Query DSL 格式化的查詢。例如，`"{\"index\": \"opensearch_dashboards_sample_data_ecommerce\", \"query\": {\"size\": 22,  \"_source\": \"category\"}}"`。`input` 參數及其包含的 `index` 與 `query` 參數為必要。

## 測試工具

您可以將此工具做為代理程式工作流程的一部分來執行，或使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用來測試個別工具或執行獨立作業。