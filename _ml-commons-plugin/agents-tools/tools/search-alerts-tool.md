---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Search Alerts 工具"
has_children: false
has_toc: false
nav_order: 67
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# Search Alerts 工具
**於 2.13 版推出**
{: .label .label-purple }
<!-- vale on -->

`SearchAlertsTool` 會擷取所產生警示的相關資訊。如需警示的詳細資訊，請參閱 [Alerting]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/index/)。

## 步驟 1：註冊將執行 SearchAlertsTool 的流程代理程式

流程代理程式會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_Search_Alerts_Tool",
  "type": "flow",
  "description": "this is a test agent for the SearchAlertsTool",
  "memory": {
    "type": "demo"
  },
  "tools": [
      {
      "type": "SearchAlertsTool",
      "name": "DemoSearchAlertsTool",
      "parameters": {}
    }
  ]
}
```
{% include copy-curl.html %} 

如需參數說明，請參閱[註冊參數](#register-parameters)。

OpenSearch 會回應代理程式 ID：

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
    "question": "Do I have any alerts?"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會回應所產生警示的清單以及警示總數：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "Alerts=[Alert(id=rv9nYo0Bk4MTqirc_DkW, version=394, schemaVersion=5, monitorId=ZuJnYo0B9RaBCvhuEVux, workflowId=, workflowName=, monitorName=test-monitor-2, monitorVersion=1, monitorUser=User[name=admin, backend_roles=[admin], roles=[own_index, all_access], custom_attribute_names=[], user_requested_tenant=null], triggerId=ZeJnYo0B9RaBCvhuEVul, triggerName=t-1, findingIds=[], relatedDocIds=[], state=ACTIVE, startTime=2024-02-01T02:03:18.420Z, endTime=null, lastNotificationTime=2024-02-01T08:36:18.409Z, acknowledgedTime=null, errorMessage=null, errorHistory=[], severity=1, actionExecutionResults=[], aggregationResultBucket=null, executionId=ZuJnYo0B9RaBCvhuEVux_2024-02-01T02:03:18.404853331_51c18f2c-5923-47c3-b476-0f5a66c6319b, associatedAlertIds=[])]TotalAlerts=1"
        }
      ]
    }
  ]
}
```

若找不到任何警示，OpenSearch 會在結果中回應空陣列：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "Alerts=[]TotalAlerts=0"
        }
      ]
    }
  ]
}
```

## 註冊參數

下表列出註冊代理程式時可用的所有工具參數。所有參數皆為選用。

Parameter	| Type | Description	
:--- | :--- | :---
`alertIds`	| Array	| 要搜尋的警示 ID。
`alertIndex` | String | 要搜尋的警示索引名稱（預設為 `null`）。
`monitorId`	| String	| 用來篩選警示的監視器 ID。
`monitorIds` | Array | 用來篩選警示的監視器 ID 清單。
`workflowIds`	| Array | 用來篩選警示的工作流程 ID 清單。
`alertState` |	String	| 用來篩選警示的警示狀態。有效值為 `ALL`、`ACTIVE`、`ERROR`、`COMPLETED` 及 `ACKNOWLEDGED`。預設為 `ALL`。
`severityLevel` | String| 用來篩選警示的嚴重性層級。有效值為 `ALL`、`1`、`2` 及 `3`。預設為 `ALL`。
`searchString` | String	| 用來搜尋特定警示的搜尋字串。
`sortOrder`| String | 結果的排序順序。有效值為 `asc`（遞增）及 `desc`（遞減）。預設為 `asc`。 
`sortString`| String |	指定用來排序結果的監視器欄位。預設為 `monitor_name.keyword`。
`size`	| Integer |	要傳回的結果數。預設為 `20`。
`startIndex`| Integer |	要開始的警示分頁索引。預設為 `0`。

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

Parameter	| Type | Required/Optional | Description	
:--- | :--- | :--- | :---
`question` | String | Required | 要傳送給 LLM 的自然語言問題。 

## 測試工具

您可以將此工具做為代理程式工作流程的一部分執行，或使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用來測試個別工具或執行獨立作業。