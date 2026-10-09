---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除代理程式記憶"
parent: Agentic memory APIs
grand_parent: ML Commons APIs
nav_order: 53
---

# 刪除代理程式記憶 API
**3.3 版新增**
{: .label .label-purple }

使用此 API 依類型與 ID 刪除特定記憶，或刪除符合查詢條件的記憶。此統一 API 支援刪除任何[記憶類型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#memory-types)的記憶：`sessions`、`working`、`long-term` 或 `history`。

## 依類型與 ID 刪除記憶

使用此 API 依類型與 ID 刪除記憶。

### 端點

```json
DELETE /_plugins/_ml/memory_containers/{memory_container_id}/memories/{type}/{id}
```

### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `memory_container_id` | 字串 | 必要 | 要從中刪除記憶的記憶容器 ID。 |
| `type` | 字串 | 必要 | 要刪除的記憶類型。有效值為 `sessions`、`working`、`long-term` 與 `history`。 |
| `id` | 字串 | 必要 | 要刪除之特定記憶的 ID。 |

### 範例請求：刪除工作記憶

```json
DELETE /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/working/XyEuiJkBeh2gPPwzjYWM
```
{% include copy-curl.html %}

### 範例請求：刪除長期記憶

```json
DELETE /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/long-term/DcxjTpkBvwXRq366C1Zz
```
{% include copy-curl.html %}

### 範例請求：刪除工作階段記憶

```json
DELETE /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/sessions/CcxjTpkBvwXRq366A1aE
```
{% include copy-curl.html %}

### 範例請求：刪除歷程記憶

```json
DELETE /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/history/eMxnTpkBvwXRq366hmAU
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "result": "deleted",
  "_id": "XyEuiJkBeh2gPPwzjYWM",
  "_version": 2,
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  }
}
```

### 錯誤回應

如果您嘗試從不存在的容器刪除記憶，OpenSearch 會傳回 404 Not Found 錯誤：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "status_exception",
        "reason": "Memory container not found"
      }
    ],
    "type": "status_exception",
    "reason": "Memory container not found"
  },
  "status": 404
}
```

### 回應欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `result` | 字串 | 刪除作業的結果。 |
| `_id` | 字串 | 已刪除記憶的 ID。 |
| `_version` | 整數 | 刪除後的版本號。 |
| `_shards` | 物件 | 此作業所涉及分片的相關資訊。 |

## 依查詢刪除記憶

使用此 API 透過查詢比對特定條件，以刪除多筆記憶。

### 端點

```json
POST /_plugins/_ml/memory_containers/{memory_container_id}/memories/{type}/_delete_by_query
```

### 路徑參數

| 欄位                 | 資料類型 | 必要/選用 | 說明 |
|:----------------------| :--- | :--- | :--- |
| `memory_container_id` | 字串 | 必要 | 要從中刪除記憶的記憶容器 ID。 |
| `type` | 字串 | 必要 | 要刪除的記憶類型。有效值為 `sessions`、`working`、`long-term` 與 `history`。 |

### 請求本文欄位

請求本文必須包含用於比對您要刪除之記憶的查詢。

### 範例請求

```json
POST /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/working/_delete_by_query
{
  "query": {
    "match": {
      "owner_id": "admin"
    }
  }
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
    "took": 159,
    "timed_out": false,
    "total": 6,
    "updated": 0,
    "created": 0,
    "deleted": 6,
    "batches": 1,
    "version_conflicts": 0,
    "noops": 0,
    "retries": {
        "bulk": 0,
        "search": 0
    },
    "throttled_millis": 0,
    "requests_per_second": -1.0,
    "throttled_until_millis": 0,
    "failures": []
}
```

### 回應欄位

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `took` | 整數 | 執行請求所花費的時間（毫秒）。 |
| `timed_out` | 布林值 | 請求是否逾時。 |
| `total` | 整數 | 已處理的文件總數。 |
| `deleted` | 整數 | 已刪除的文件數。 |
| `batches` | 整數 | 已處理的批次數。 |
| `version_conflicts` | 整數 | 遭遇的版本衝突數。 |
| `noops` | 整數 | 無作業的更新數。 |
| `retries` | 物件 | 大量作業與搜尋重試的相關資訊。 |
| `throttled_millis` | 整數 | 請求被節流的時間（毫秒）。 |
| `requests_per_second` | 浮點數 | 每秒處理的請求數。 |
| `throttled_until_millis` | 整數 | 節流解除前的時間（毫秒）。 |
| `failures` | 陣列 | 作業期間發生的任何失敗。 |

