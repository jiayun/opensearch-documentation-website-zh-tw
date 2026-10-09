---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料分布工具"
has_children: false
has_toc: false
nav_order: 25
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# 資料分布工具
**於 3.3.0 版引入**
{: .label .label-purple }
<!-- vale on -->

`DataDistributionTool` 會分析資料集內的資料分布模式，並比較不同時段之間的分布。它支援單一資料集分析與比較分析，可識別欄位值分布的顯著變化，協助偵測異常、趨勢與資料品質問題。

此工具同時支援[查詢領域專用語言（DSL）]({{site.url}}{{site.baseurl}}/query-dsl/)與[管線處理語言（PPL）]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/)查詢，以靈活擷取與篩選資料。

## 分析模式

此工具會根據提供的參數，自動選取適當的分析模式：

- **比較分析**：同時提供基準與選取時間範圍時，此工具會比較兩個時段之間的欄位分布，以識別顯著變化與差異。
- **單一資料集分析**：僅提供選取時間範圍時，此工具會分析資料集內的分布模式，提供欄位值頻率與特性的深入資訊。

## 步驟 1：註冊執行 DataDistributionTool 的流程代理程式

流程代理程式會依序執行一系列工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_Data_Distribution_Tool",
  "type": "flow",
  "description": "this is a test agent for the DataDistributionTool",
  "memory": {
    "type": "demo"
  },
  "tools": [
    {
      "type": "DataDistributionTool",
      "parameters": {}
    }
  ]
}
```
{% include copy-curl.html %}

註冊此工具不需要任何參數。此工具會在執行時動態驗證參數。 

OpenSearch 會回應代理程式 ID：

```json
{
  "agent_id": "OQutgJYBAc35E4_KvI1q"
}
```

## 步驟 2：執行代理程式

執行代理程式以進行比較分布分析或單一資料集分布分析。

### 比較分析

若要對兩個時段進行比較分布分析，請同時提供基準與選取時間範圍：

```json
POST /_plugins/_ml/agents/OQutgJYBAc35E4_KvI1q/_execute
{
  "parameters": {
    "index": "logs-2025.01.15",
    "timeField": "@timestamp",
    "selectionTimeRangeStart": "2025-01-15 10:00:00",
    "selectionTimeRangeEnd": "2025-01-15 11:00:00",
    "baselineTimeRangeStart": "2025-01-15 08:00:00",
    "baselineTimeRangeEnd": "2025-01-15 09:00:00",
    "size": 1000,
    "queryType": "dsl",
    "filter": ["{\"term\": {\"status\": \"error\"}}", "{\"range\": {\"response_time\": {\"gte\": 100}}}"]
  }
}
```
{% include copy-curl.html %}

OpenSearch 會傳回逐一欄位的比較結果，顯示時段之間的分布變化：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "{\"comparisonAnalysis\": [{\"field\": \"status\", \"divergence\": 0.2, \"topChanges\": [{\"value\": \"error\", \"selectionPercentage\": 0.3, \"baselinePercentage\": 0.1}, {\"value\": \"success\", \"selectionPercentage\": 0.7, \"baselinePercentage\": 0.9}]}]}"
        }
      ]
    }
  ]
}
```

### 單一資料集分析

若要進行單一資料集分布分析，請僅提供選取時間範圍：

```json
POST /_plugins/_ml/agents/OQutgJYBAc35E4_KvI1q/_execute
{
  "parameters": {
    "index": "application_logs",
    "timeField": "@timestamp",
    "selectionTimeRangeStart": "2025-01-15 10:00:00",
    "selectionTimeRangeEnd": "2025-01-15 11:00:00",
    "size": 1000,
    "queryType": "dsl"
  }
}
```
{% include copy-curl.html %}

OpenSearch 會傳回所分析資料集的分布模式：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "{\"singleAnalysis\": [{\"field\": \"status\", \"divergence\": 0.7, \"topChanges\": [{\"value\": \"error\", \"selectionPercentage\": 0.3}, {\"value\": \"success\", \"selectionPercentage\": 0.7}]}]}"
        }
      ]
    }
  ]
}
```

## 使用 PPL 查詢

執行代理程式，使用 PPL 擷取資料：

```json
POST /_plugins/_ml/agents/OQutgJYBAc35E4_KvI1q/_execute
{
  "parameters": {
    "index": "logs-2025.01.15",
    "timeField": "@timestamp",
    "selectionTimeRangeStart": "2025-01-15 10:00:00",
    "selectionTimeRangeEnd": "2025-01-15 11:00:00",
    "size": 1000,
    "queryType": "ppl",
    "ppl": "source=logs-2025.01.15 | where status='error'"
  }
}
```
{% include copy-curl.html %}

## 使用自訂 DSL 查詢

使用完整的自訂 DSL 查詢執行代理程式：

```json
POST /_plugins/_ml/agents/OQutgJYBAc35E4_KvI1q/_execute
{
  "parameters": {
    "index": "logs-2025.01.15",
    "timeField": "@timestamp",
    "selectionTimeRangeStart": "2025-01-15 10:00:00",
    "selectionTimeRangeEnd": "2025-01-15 11:00:00",
    "size": 1000,
    "queryType": "dsl",
    "dsl": "{\"bool\": {\"must\": [{\"term\": {\"status\": \"error\"}}], \"filter\": [{\"range\": {\"response_time\": {\"gte\": 100}}}]}}"
  }
}
```
{% include copy-curl.html %}

## 執行參數

下表列出執行代理程式時可用的工具參數。

| 參數 | 類型 | 必要／選用 | 說明 |
|:----------|:-----|:------------------|:------------|
| `index` | 字串 | 必要 | 包含待分析資料的 OpenSearch 索引名稱。 |
| `timeField` | 字串 | 必要 | 用於依時間篩選的日期／時間欄位。 |
| `selectionTimeRangeStart` | 字串 | 必要 | 分析時段的開始時間，採用 UTC 日期字串格式（例如，`2025-01-15 10:00:00`）。 |
| `selectionTimeRangeEnd` | 字串 | 必要 | 分析時段的結束時間，採用 UTC 日期字串格式（例如，`2025-01-15 11:00:00`）。 |
| `baselineTimeRangeStart` | 字串 | 選用 | 基準比較時段的開始時間，採用 UTC 日期字串格式（例如，`2025-01-15 10:00:00`）。比較分析模式需要此參數。 |
| `baselineTimeRangeEnd` | 字串 | 選用 | 基準比較時段的結束時間，採用 UTC 日期字串格式（例如，`2025-01-15 11:00:00`）。比較分析模式需要此參數。 |
| `size` | 整數 | 選用 | 要分析的文件數量上限。預設為 `1000`。上限為 `10000`。 |
| `queryType` | 字串 | 選用 | 查詢類型。有效值為 `ppl` 與 `dsl`。預設為 `dsl`。 |
| `filter` | 陣列 | 選用 | 用於篩選的額外 DSL 查詢條件，以 JSON 字串指定（例如，`["{\"term\": {\"status\": \"error\"}}", "{\"range\": {\"level\": {\"gte\": 3}}}"]`）。 |
| `dsl` | 字串 | 選用 | 以 JSON 字串表示的完整原始 DSL 查詢。若提供此參數，則優先於 `filter` 參數。 |
| `ppl` | 字串 | 選用 | 不含時間資訊的完整 PPL 陳述式。當 `queryType` 為 `ppl` 時使用。 |

## 測試工具

您可以將此工具作為代理程式工作流程的一部分執行，或使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用於測試個別工具或執行獨立作業。

## 限制

資料分布工具有下列限制：

- **文件數量上限**：此工具每次執行預設最多處理 1,000 份文件，可設定的上限為 10,000 份文件（`MAX_SIZE_LIMIT = 10000`）。
- **欄位基數限制**：系統會自動篩除高基數欄位，以確保分析結果具有意義：
  - ID 欄位：最多 30 個相異值。
  - 資料欄位：最多 10 個相異值（或資料集大小 ÷ 2，取較大者）。
- **結果限制**： 
  - 比較分析：傳回前 10 個欄位差異。
  - 單一資料集分析：傳回前 30 個欄位分布。
  - 每個欄位的主要變化：限 10 個項目。