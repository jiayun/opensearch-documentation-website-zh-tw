---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Search Anomaly Results 工具"
has_children: false
has_toc: false
nav_order: 80
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# Search Anomaly Results 工具
**於 2.13 版導入**
{: .label .label-purple }
<!-- vale on -->

`SearchAnomalyResultsTool` 會擷取異常偵測器結果的相關資訊。如需異常偵測器的更多資訊，請參閱[異常偵測]({{site.url}}{{site.baseurl}}/observing-your-data/ad/index/)。

## 步驟 1：註冊將執行 SearchAnomalyResultsTool 的流程代理程式

流程代理程式會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_Search_Anomaly_Results_Tool",
  "type": "flow",
  "description": "this is a test agent for the SearchAnomalyResultsTool",
  "memory": {
    "type": "demo"
  },
  "tools": [
    {
      "type": "SearchAnomalyResultsTool",
      "name": "DemoSearchAnomalyResultsTool",
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
  "agent_id": "HuJZYo0B9RaBCvhuUlpy"
}
```

## 步驟 2：執行代理程式

傳送下列請求以執行代理程式：

```json
POST /_plugins/_ml/agents/HuJZYo0B9RaBCvhuUlpy/_execute
{
  "parameters": {
    "question": "Do I have any anomalies?"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會回應叢集上設定的個別異常偵測器清單（每個結果包含偵測器 ID、異常等級與信賴度），以及找到的異常結果總數：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "AnomalyResults=[{detectorId=ef9lYo0Bk4MTqircmjnm,grade=1.0,confidence=0.9403051246569198}{detectorId=E-JlYo0B9RaBCvhunFtw,grade=1.0,confidence=0.9163498216870274}]TotalAnomalyResults=2"
        }
      ]
    }
  ]
}
```

如果找不到任何異常，OpenSearch 會在結果中回應空陣列：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "AnomalyResults=[]TotalAnomalyResults=0"
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
`detectorId`	| 字串	| 要從中傳回結果的偵測器 ID。
`realTime`	| 布林值 | 是否傳回即時異常偵測器結果。將此參數設為 `false` 可僅傳回歷史分析結果。
`anomalyGradeThreshold` | 浮點數	| 傳回的異常偵測器結果的最低異常等級。異常等級是介於 0 到 1 之間的數字，表示資料點的異常程度。
`dataStartTime` | 長整數	| 要傳回異常偵測器結果的最早時間，以 epoch 毫秒為單位。
`dataEndTime` | 長整數 |	要傳回異常偵測器結果的最晚時間，以 epoch 毫秒為單位。
`sortOrder`	|字串 | 結果的排序順序。有效值為 `asc`（遞增）與 `desc`（遞減）。預設為 `desc`。 
`sortString`| 字串 |	指定用於排序結果的偵測器欄位。預設為 `data_start_time`。
`size`	| 整數 |	要傳回的結果數量。預設為 `20`。
`startIndex`| 整數 |	結果開始分頁的索引。預設為 `0`。

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

參數	| 類型 | 必要/選用 | 說明	
:--- | :--- | :--- | :---
`question` | 字串 | 必要 | 要傳送給 LLM 的自然語言問題。 

## 測試工具

您可以在代理程式工作流程中執行此工具，也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適用於測試個別工具或執行獨立作業。