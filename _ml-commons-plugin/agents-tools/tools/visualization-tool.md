---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "視覺化工具"
has_children: false
has_toc: false
nav_order: 120
parent: Tools
grand_parent: Agents and tools
---

# 視覺化工具
**於 2.13 版推出**
{: .label .label-purple }

使用 `VisualizationTool` 來尋找與問題相關的視覺化。

## 步驟 1：註冊將執行 VisualizationTool 的流程代理程式

流程代理程式會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_Visualization_tool",
  "type": "flow",
  "description": "this is a test agent for the VisuailizationTool",
  "tools": [
      {
      "type": "VisualizationTool",
      "name": "DemoVisualizationTool",
      "parameters": {
        "index": ".kibana",
        "input": "${parameters.question}",
        "size": 3
      }
    }
  ]
}
```
{% include copy-curl.html %} 

參數說明請參閱 [Register parameters](#register-parameters)。

OpenSearch 會回應代理程式 ID：

```json
{
  "agent_id": "9X7xWI0Bpc3sThaJdY9i"
}
```

## 步驟 2：執行代理程式

執行代理程式之前，請確認您已新增 OpenSearch Dashboards 的 `Sample eCommerce orders` 範例資料集。若要了解更多，請參閱 [Adding sample data]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

接著，傳送下列請求來執行代理程式：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "question": "what's the revenue for today?"
  }
}
```
{% include copy-curl.html %} 

預設情況下，OpenSearch 會傳回前三個相符的視覺化。您可以使用 `size` 參數來指定傳回的結果數量。輸出以 CSV 格式傳回，包含兩個欄位：`Title`（在 OpenSearch Dashboards 中顯示的視覺化標題）和 `Id`（此視覺化的唯一 ID）：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """Title,Id
[eCommerce] Total Revenue,10f1a240-b891-11e8-a6d9-e546fe2bba5f
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
`input` | String | 必要 | 用於比對視覺化的使用者輸入。
`index` | String | 選用 | 要搜尋的索引。預設為 `.kibana`（OpenSearch Dashboards 資料的系統索引）。
`size` | Integer | 選用 | 要傳回的視覺化數量。預設為 `3`。

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

Parameter	| Type | Required/Optional | Description	
:--- | :--- | :--- | :---
`question` | String | 必要 | 要傳送給 LLM 的自然語言問題。

## 測試工具

您可以將此工具作為代理程式工作流程的一部分執行，也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用於測試個別工具或執行獨立操作。