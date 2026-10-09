---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Search Monitors 工具"
has_children: false
has_toc: false
nav_order: 100
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# Search Monitors 工具
**於 2.13 版推出**
{: .label .label-purple }
<!-- vale on -->

`SearchMonitorsTool` 會擷取您叢集上已設定的警示監視器資訊。如需警示監視器的詳細資訊，請參閱[監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/)。

## 步驟 1：註冊將執行 SearchMonitorsTool 的流程代理程式

流程代理程式會依序執行一系列工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_Search_Monitors_Tool",
  "type": "flow",
  "description": "this is a test agent for the SearchMonitorsTool",
  "memory": {
    "type": "demo"
  },
  "tools": [
    {
      "type": "SearchMonitorsTool",
      "name": "DemoSearchMonitorsTool",
      "parameters": {}
    }
  ]
}
```
{% include copy-curl.html %} 

如需參數說明，請參閱[註冊參數](#register-parameters)。

OpenSearch 會傳回代理程式 ID：

```json
{
  "agent_id": "EuJYYo0B9RaBCvhuy1q8"
}
```

## 步驟 2：執行代理程式

傳送下列請求以執行代理程式：

```json
POST /_plugins/_ml/agents/EuJYYo0B9RaBCvhuy1q8/_execute
{
  "parameters": {
    "question": "Do I have any alerting monitors?"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會傳回您叢集上已設定的警示監視器清單，以及警示監視器的總數：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "Monitors=[{id=j_9mYo0Bk4MTqircEzk_,name=test-monitor,type=query_level_monitor,enabled=true,enabledTime=1706752873144,lastUpdateTime=1706752873145}{id=ZuJnYo0B9RaBCvhuEVux,name=test-monitor-2,type=query_level_monitor,enabled=true,enabledTime=1706752938405,lastUpdateTime=1706752938405}]TotalMonitors=2"
        }
      ]
    }
  ]
}
```

若找不到任何監視器，OpenSearch 會在結果中傳回空陣列：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "Monitors=[]TotalMonitors=0"
        }
      ]
    }
  ]
}
```

## 註冊參數

下表列出註冊代理程式時可用的所有工具參數。所有參數皆為選用。

參數	| 類型 | 說明	
:--- | :--- | :---
`monitorId`	| 字串	| 要搜尋的監視器 ID。
`monitorName`	| 字串	| 要搜尋的監視器名稱。
`monitorNamePattern`	| 字串 | 用於比對要搜尋的監視器名稱的萬用字元查詢。
`enabled` |	布林值	| 是否傳回目前已啟用的監視器資訊。不設定此參數（或將其設為 `null`）即可傳回已啟用和已停用的監視器資訊。將此參數設為 `true`，即可僅傳回已啟用的監視器資訊。將此參數設為 `false`，即可僅傳回已停用的監視器資訊。預設為 `null`。
`hasTriggers` |	布林值	| 是否傳回已啟用觸發條件的監視器資訊。不設定此參數（或將其設為 `null`）即可傳回已啟用和已停用觸發條件的監視器資訊。將此參數設為 `true`，即可僅傳回已啟用觸發條件的監視器資訊。將此參數設為 `false`，即可僅傳回已停用觸發條件的監視器資訊。預設為 `null`。
`indices` | 字串	| 傳回的監視器所追蹤之索引的索引名稱或索引模式。
`sortOrder`| 字串 | 結果的排序順序。有效值為 `asc`（遞增）和 `desc`（遞減）。預設為 `asc`。 
`sortString`| 字串 |	指定用來排序結果的監視器欄位。預設為 `name.keyword`。
`size`	| 整數 |	要傳回的結果數量。預設為 `20`。
`startIndex`| 整數 |	作為起點的監視器分頁索引。預設為 `0`。

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

參數	| 類型 | 必要／選用 | 說明	
:--- | :--- | :--- | :---
`question` | 字串 | 必要 | 要傳送給 LLM 的自然語言問題。 

## 測試工具

您可以將此工具作為代理程式工作流程的一部分執行，或使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用於測試個別工具或執行獨立操作。