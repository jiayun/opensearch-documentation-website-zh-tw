---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋異常偵測器工具"
has_children: false
has_toc: false
nav_order: 70
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# 搜尋異常偵測器工具
**於 2.13 版推出**
{: .label .label-purple }
<!-- vale on -->

`SearchAnomalyDetectorsTool` 會擷取您叢集上所設定之異常偵測器的相關資訊。如需異常偵測器的詳細資訊，請參閱[異常偵測]({{site.url}}{{site.baseurl}}/observing-your-data/ad/index/)。

## 步驟 1：註冊將執行 SearchAnomalyDetectorsTool 的流程代理程式（flow agent）

流程代理程式會依序執行一系列工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_Search_Anomaly_Detectors_Tool",
  "type": "flow",
  "description": "this is a test agent for the SearchAnomalyDetectorsTool",
  "tools": [
      {
      "type": "SearchAnomalyDetectorsTool",
      "name": "DemoSearchAnomalyDetectorsTool",
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
    "question": "Do I have any anomaly detectors?"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會回應您叢集上所設定之異常偵測器的清單，以及異常偵測器的總數：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "AnomalyDetectors=[{id=y2M-Yo0B-yCFzT-N_XXU,name=sample-http-responses-detector,type=SINGLE_ENTITY,description=A sample detector to detect anomalies with HTTP response code logs.,index=[sample-http-responses],lastUpdateTime=1706750311891}]TotalAnomalyDetectors=1"
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
`detectorName`	| 字串	| 要搜尋的偵測器名稱。
`detectorNamePattern`	| 字串 | 用來比對要搜尋的偵測器名稱的萬用字元查詢。
`indices` | 字串	| 傳回的偵測器用作資料來源的索引名稱或索引模式。
`highCardinality` | 布林值	| 是否傳回高基數偵測器的資訊。將此參數保留為未設定（或設為 `null`），即可傳回高基數（多實體）與非高基數（單一實體）偵測器的資訊。將此參數設為 `true`，即可僅傳回高基數偵測器的資訊。將此參數設為 `false`，即可僅傳回非高基數偵測器的資訊。
`lastUpdateTime` | Long |	指定要傳回的偵測器其最後更新時間的最早界限，以 epoch 毫秒為單位。預設為 `null`。
`sortOrder`	|字串 | 結果的排序順序。有效值為 `asc`（遞增）與 `desc`（遞減）。預設為 `asc`。 
`sortString`| 字串 |	指定用來排序結果的偵測器欄位。預設為 `name.keyword`。
`size`	| 整數 |	要傳回的結果數量。預設為 `20`。
`startIndex`| 整數 |	起始偵測器的分頁索引位置。預設為 `0`。
`running`| 布林值 | 是否傳回目前正在執行的偵測器資訊。將此參數保留為未設定（或設為 `null`），即可傳回正在執行與未在執行的偵測器資訊。將此參數設為 `true`，即可僅傳回正在執行的偵測器資訊。將此參數設為 `false`，即可僅傳回目前未在執行的偵測器資訊。預設為 `null`。
`failed` |	布林值	| 是否傳回目前發生失敗的偵測器資訊。將此參數保留為未設定（或設為 `null`），即可傳回失敗與未失敗的偵測器資訊。將此參數設為 `true`，即可僅傳回失敗的偵測器資訊。將此參數設為 `false`，即可僅傳回未失敗的偵測器資訊。預設為 `null`。

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

參數	| 類型 | 必要/選用 | 說明	
:--- | :--- | :--- | :---
`question` | 字串 | 必要 | 要傳送給 LLM 的自然語言問題。 

## 測試工具

您可以將此工具做為代理程式工作流程的一部分來執行，或使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用來測試個別工具或執行獨立作業。