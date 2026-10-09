---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "記錄檔模式分析工具"
has_children: false
has_toc: false
nav_order: 38
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# 記錄檔模式分析工具
**於 3.3.0 版推出**
{: .label .label-purple }
<!-- vale on -->

`LogPatternAnalysisTool` 會透過比較基準與選取時間範圍之間的差異，偵測異常的記錄檔模式與序列，藉此執行進階記錄檔分析。它支援下列分析模式：

- 記錄檔序列分析 (含追蹤關聯)
- 記錄檔模式差異分析
- 用於錯誤偵測的記錄檔洞察分析

此工具使用機器學習分群演算法與統計方法，找出在選取期間出現頻率明顯高於基準期間的異常模式，協助偵測系統問題與效能異常。

## 分析模式

此工具會根據提供的參數自動選取適當的分析模式：

- **記錄檔序列分析**：同時提供追蹤欄位與基準時間範圍時，此工具會分析與追蹤相關的記錄檔序列，以找出異常的執行路徑。
- **記錄檔模式差異分析**：提供基準時間範圍但未提供追蹤欄位時，此工具會比較基準期間與選取期間的記錄檔模式，以偵測異常模式。
- **記錄檔洞察分析**：僅提供選取時間範圍時，此工具會根據錯誤關鍵字執行模式分析，以找出重大問題。

## 步驟 1：註冊將執行 LogPatternAnalysisTool 的流程代理程式

流程代理程式會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_Log_Pattern_Analysis_Tool",
  "type": "flow",
  "description": "this is a test agent for the LogPatternAnalysisTool",
  "memory": {
    "type": "demo"
  },
  "tools": [
    {
      "type": "LogPatternAnalysisTool",
      "parameters": {}
    }
  ]
}
```
{% include copy-curl.html %}

註冊此工具不需要任何參數。此工具會在執行時使用動態參數驗證。 

OpenSearch 會回應代理程式 ID：

```json
{
  "agent_id": "OQutgJYBAc35E4_KvI1q"
}
```

## 步驟 2：執行代理程式

執行代理程式以進行各種分析類型。

### 記錄檔序列分析 

若要執行以追蹤為基礎的序列分析，請提供 `traceFieldName`、`baseTimeRangeStart` 及 `baseTimeRangeEnd`：

```json
POST /_plugins/_ml/agents/OQutgJYBAc35E4_KvI1q/_execute
{
  "parameters": {
    "index": "ss4o_logs-otel-2025.06.24",
    "timeField": "@timestamp",
    "logFieldName": "body",
    "traceFieldName": "traceId",
    "baseTimeRangeStart": "2025-06-24 07:33:05",
    "baseTimeRangeEnd": "2025-06-24 07:51:27",
    "selectionTimeRangeStart": "2025-06-24 07:50:26",
    "selectionTimeRangeEnd": "2025-06-24 07:55:56"
  }
}
```
{% include copy-curl.html %}

OpenSearch 會傳回與基準模式有顯著差異的異常追蹤序列：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "{\"EXCEPTIONAL\": {\"trace456\": \"User login -> Database timeout -> Error handling -> Retry -> Response sent\"}, \"BASE\": {\"trace123\": \"User login -> Database query -> Response sent\"}}"
        }
      ]
    }
  ]
}
```

### 記錄檔模式差異分析

若要執行模式比較分析，請提供 `baseTimeRangeStart` 與 `baseTimeRangeEnd`：

```json
POST /_plugins/_ml/agents/OQutgJYBAc35E4_KvI1q/_execute
{
  "parameters": {
    "index": "opensearch_dashboards_sample_data_logs",
    "timeField": "@timestamp",
    "logFieldName": "message",
    "baseTimeRangeStart": "2018-07-22 00:00:00",
    "baseTimeRangeEnd": "2018-07-22 12:00:00",
    "selectionTimeRangeStart": "2018-07-22 12:00:00",
    "selectionTimeRangeEnd": "2018-07-22 23:59:59"
  }
}
```
{% include copy-curl.html %}

OpenSearch 會傳回在各時間區段之間頻率有顯著變化的模式：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "{\"patternMapDifference\": [{\"pattern\": \"<*> ERROR <*> Connection timeout\", \"base\": 0.02, \"selection\": 0.15, \"lift\": 7.5}]}"
        }
      ]
    }
  ]
}
```

### 記錄檔洞察分析

若要執行錯誤模式偵測，請僅提供選取時間範圍：

```json
POST /_plugins/_ml/agents/OQutgJYBAc35E4_KvI1q/_execute
{
  "parameters": {
    "index": "application_logs",
    "timeField": "@timestamp",
    "logFieldName": "message",
    "selectionTimeRangeStart": "2025-01-15 10:00:00",
    "selectionTimeRangeEnd": "2025-01-15 11:00:00"
  }
}
```
{% include copy-curl.html %}

OpenSearch 會傳回附有範例記錄檔的錯誤模式：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "{\"logInsights\": [{\"pattern\": \"<*> ERROR User <*> authentication failed\", \"count\": 23, \"sampleLogs\": [\"2025-01-15 10:30:15 ERROR User user123 authentication failed\", \"2025-01-15 10:32:08 ERROR User admin456 authentication failed\"]}]}"
        }
      ]
    }
  ]
}
```

## 執行參數

下表列出可用於執行代理程式的工具參數。

| Parameter | Type | Required/Optional | Description |
|:----------|:-----|:------------------|:------------|
| `index` | String | Required | 包含記錄資料的 OpenSearch 索引名稱 (例如 `ss4o_logs-otel-2025.06.24`)。 |
| `timeField` | String | Required | 索引對應中用於時間篩選的日期/時間欄位。 |
| `logFieldName` | String | Required | 包含要分析之原始記錄訊息的欄位 (例如 `body`、`message` 或 `log`)。 |
| `traceFieldName` | String | Optional | 包含追蹤 ID 或關聯 ID 以啟用序列分析的欄位 (例如 `traceId` 或 `correlationId`)。記錄檔序列分析模式必要。 |
| `baseTimeRangeStart` | String | Optional | 基準比較期間的開始時間，格式為 UTC 日期字串 (例如 `2025-06-24 07:33:05`)。序列與模式差異分析模式必要。 |
| `baseTimeRangeEnd` | String | Optional | 基準比較期間的結束時間，格式為 UTC 日期字串 (例如 `2025-06-24 07:51:27`)。序列與模式差異分析模式必要。 |
| `selectionTimeRangeStart` | String | Required | 分析目標期間的開始時間，格式為 UTC 日期字串 (例如 `2025-06-24 07:50:26`)。 |
| `selectionTimeRangeEnd` | String | Required | 分析目標期間的結束時間，格式為 UTC 日期字串 (例如 `2025-06-24 07:55:56`)。 |

## 測試工具

您可以將此工具做為代理程式工作流程的一部分執行，或使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用來測試個別工具或執行獨立作業。

## 限制

記錄檔模式分析工具具有下列限制：

- **記錄檔量**：此工具會透過 PPL 查詢處理記錄檔，每個查詢最多 10,000 份文件。為達到最佳效能，請將分析限制在特定時間範圍。
- **結果限制**：
  - 模式差異分析：傳回前 10 個顯著模式。
  - 記錄檔洞察分析：傳回前 5 個錯誤模式，每個模式最多附 2 筆範例記錄檔。