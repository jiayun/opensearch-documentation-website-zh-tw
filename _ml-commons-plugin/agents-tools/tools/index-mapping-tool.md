---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引對應工具"
has_children: false
has_toc: false
nav_order: 30
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# 索引對應工具
**於 2.13 版導入**
{: .label .label-purple }
<!-- vale on -->

`IndexMappingTool` 會擷取叢集中索引的對應與設定資訊。

## 步驟 1：註冊將執行 IndexMappingTool 的流程代理程式

流程代理程式會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_IndexMapping_tool",
  "type": "flow",
  "description": "this is a test agent for the IndexMappingTool",
  "tools": [
      {
      "type": "IndexMappingTool",
      "name": "DemoIndexMappingTool",
      "parameters": {
        "index": "${parameters.index}",
        "input": "${parameters.question}"
      }
    }
  ]
}
```
{% include copy-curl.html %} 

如需參數說明，請參閱[註冊參數](#register-parameters)。

OpenSearch 會回應代理程式 ID：

```json
{
  "agent_id": "9X7xWI0Bpc3sThaJdY9i"
}
```

## 步驟 2：執行代理程式

在執行代理程式之前，請確定您已新增 OpenSearch Dashboards 的 `Sample eCommerce orders` 範例資料集。若要了解更多，請參閱[新增範例資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

接著，傳送下列請求並提供索引名稱與問題來執行代理程式：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "index": [ "sample-ecommerce" ],
    "question": "What fields are in the sample-ecommerce index?"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會傳回指定索引的對應與設定：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """index: sample-ecommerce

mappings:
properties={items_purchased_failure={type=integer}, items_purchased_success={type=integer}, order_id={type=integer}, timestamp={type=date}, total_revenue_usd={type=integer}}


settings:
index.creation_date=1706752839713
index.number_of_replicas=1
index.number_of_shards=1
index.provided_name=sample-ecommerce
index.replication.type=DOCUMENT
index.uuid=UPYOQcAfRGqFAlSxcZlRjw
index.version.created=137217827


"""
        }
      ]
    }
  ]
}
```

## 註冊參數

下表列出註冊代理程式時可用的所有工具參數。

參數 | 類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`input` | 字串 | 必要 | 用於傳回索引資訊的使用者輸入。
`index` | 陣列 | 必要 | 一或多個索引的逗號分隔清單，用於取得對應與設定資訊。預設為空清單，表示所有索引。
`local` | 布林值 | 選用 | 是否只傳回本機節點的資訊，而不是叢集管理員節點的資訊（預設為 `false`）。

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

參數	| 類型 | 必要/選用 | 說明	
:--- | :--- | :--- | :---
`question` | 字串 | 必要 | 要傳送至 LLM 的自然語言問題。 
`index` | 陣列 | 選用 | 一或多個索引的逗號分隔清單，用於取得對應與設定資訊。預設為空清單，表示所有索引。

## 測試工具

您可以將此工具作為代理程式工作流程的一部分執行，也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適用於測試個別工具或執行獨立作業。