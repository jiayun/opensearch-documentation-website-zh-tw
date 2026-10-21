---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "List Index 工具"
has_children: false
has_toc: false
nav_order: 35
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# List Index 工具
**3.0 版新增**
{: .label .label-purple }
<!-- vale on -->

`ListIndexTool` 會擷取 OpenSearch 叢集的索引資訊，類似於 [List Indices API]({{site.url}}{{site.baseurl}}/api-reference/list/list-indices/)。

從 OpenSearch 3.0 版開始，`ListIndexTool` 取代了 `CatIndexTool`。
{: .note}

## 步驟 1：註冊將執行 ListIndexTool 的流程代理程式

流程代理程式會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_ListIndex_tool",
  "type": "flow",
  "description": "this is a test agent for the ListIndexTool",
  "tools": [
    {
      "type": "ListIndexTool",
      "name": "DemoListIndexTool",
      "parameters": {
        "input": "${parameters.question}"
      }
    }
  ]
}
```
{% include copy-curl.html %} 

參數說明請參閱[註冊參數](#register-parameters)。

OpenSearch 會回應代理程式 ID：

```json
{
  "agent_id": "9X7xWI0Bpc3sThaJdY9i"
}
```

## 步驟 2：執行代理程式

執行代理程式之前，請確認您已新增範例 OpenSearch Dashboards `Sample eCommerce orders` 資料集。如需詳細資訊，請參閱[新增範例資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

接著，傳送下列請求以執行代理程式：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "question": "How many indices do I have?"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會傳回索引資訊：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """row,health,status,index,uuid,pri(number of primary shards),rep(number of replica shards),docs.count(number of available documents),docs.deleted(number of deleted documents),store.size(store size of primary and replica shards),pri.store.size(store size of primary shards)
1,green,open,.plugins-ml-model-group,lHgGEgJhT_mpADyOZoXl2g,1,0,9,2,16.7kb,16.7kb
2,green,open,.plugins-ml-config,G7gxGQB7TZeQzBasHd5PUg,1,0,1,0,3.9kb,3.9kb
3,green,open,sample-ecommerce,UPYOQcAfRGqFAlSxcZlRjw,1,0,40320,0,2mb,2mb
4,green,open,.plugins-ml-model,WYcjBHcnRuSDHeVWPVupoA,1,0,191,45,2.1gb,2.1gb
5,green,open,opensearch_dashboards_sample_data_ecommerce,wnE6r7OvSPqc5YHj8wHSLA,1,0,4675,0,4.9mb,4.9mb
...
"""
        }
      ]
    }
  ]
}
```

## 註冊參數

下表列出註冊代理程式時可用的所有工具參數。

<!-- vale off -->
參數 | 類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`indices` | 陣列 | 選用 | 要執行列出索引操作的一或多個索引，以 JSON 陣列指定（例如 `["index1", "index2"]`）。預設為空陣列，表示所有索引。
`local` | 布林值 | 選用 | 當為 `true` 時，僅從本機節點而非叢集管理員節點擷取資訊。預設為 `false`。
`page_size` | 整數 | 選用 | 指定使用 List Indices API 時每頁傳回的索引結果數量。該 API 以分頁方式擷取索引狀態。預設為 `100`。
`include_unloaded_segments` | 布林值 | 選用 | 當為 `true` 時，索引統計資料會包含未載入記憶體之分段的資訊。預設為 `false`。
<!-- vale on -->

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

參數	| 類型 | 必要/選用 | 說明	
:--- | :--- | :--- | :---
`question` | 字串 | 必要 | 要傳送給 LLM 的自然語言問題。

## 測試工具

您可以將此工具作為代理程式工作流程的一部分執行，也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適用於測試個別工具或執行獨立操作。