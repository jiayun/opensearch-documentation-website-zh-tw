---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "更新代理式記憶"
parent: Agentic memory APIs
grand_parent: ML Commons APIs
nav_order: 52
---

# Update Memory API
**於 3.3 版推出**
{: .label .label-purple }

使用此 API，依據類型和 ID 更新特定記憶。此統一 API 支援更新 `sessions`、`working` 和 `long-term` [記憶類型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#memory-types)。`history` 記憶不支援更新。

## 端點

```json
PUT /_plugins/_ml/memory_containers/{memory_container_id}/memories/{type}/{id}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `memory_container_id` | 字串 | 必要 | 記憶容器的 ID。 |
| `type` | 字串 | 必要 | 記憶類型。有效值為 `sessions`、`working` 和 `long-term`。請注意，`history` 記憶無法更新。 |
| `id` | 字串 | 必要 | 要更新的記憶 ID。 |

## 請求欄位

請求欄位會依要更新的記憶類型而有所不同。所有請求欄位皆為選用。

### 工作階段記憶請求欄位

下表列出所有工作階段記憶的請求本文欄位。 

| 欄位      | 資料類型             | 說明 |
|:-----------|:----------------------| :--- |
| `summary`  | 字串                | 工作階段的摘要。
| `metadata` | 物件   | 記憶的其他中繼資料（例如 `status`、`branch` 或自訂欄位）。 |
| `agents`   | 物件   | 代理程式的其他資訊。 |
| `additional_info` | 物件 | 要與工作階段關聯的其他中繼資料。 |

### 工作記憶請求欄位

下表列出所有工作記憶的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `messages` | 陣列 | 更新後的對話訊息（適用於對話類型）。選用。 |
| `structured_data` | 物件 | 更新後的結構化資料內容（適用於 `data` 記憶酬載）。 |
| `binary_data` | 物件 | 更新後的二進位資料內容（適用於 `data` 記憶酬載）。選用。           |
| `tags` | 物件 | 更新後用於分類的標籤。                       |
| `metadata` | 物件  | 記憶的其他中繼資料（例如 `status`、`branch` 或自訂欄位）。

### 長期記憶請求欄位

下表列出所有長期記憶的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `memory` | 字串 | 更新後的記憶內容。選用。 |
| `tags` | 物件 | 更新後用於分類的標籤。選用。 |

## 請求範例：更新工作階段

```json
PUT /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/sessions/N2CDipkB2Mtr6INFFcX8
{
  "additional_info": {
    "key1": "value1",
    "last_activity": "2025-09-15T17:30:00Z"
  }
}
```
{% include copy-curl.html %}

## 請求範例：更新工作記憶

```json
PUT /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/working/XyEuiJkBeh2gPPwzjYWM
{
  "tags": {
    "topic": "updated_topic",
    "priority": "high"
  }
}
```
{% include copy-curl.html %}

## 請求範例：更新長期記憶

```json
PUT /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/long-term/DcxjTpkBvwXRq366C1Zz
{
  "memory": "User's name is Bob Smith",
  "tags": {
    "topic": "personal info",
    "updated": "true"
  }
}
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "result": "updated",
  "_id": "N2CDipkB2Mtr6INFFcX8",
  "_version": 2,
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  }
}
```

## 回應欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `result` | 字串 | 更新操作的結果。 |
| `_id` | 字串 | 更新後的記憶 ID。 |
| `_version` | 整數 | 更新後的記憶版本號碼。 |
| `_shards` | 物件 | 參與此操作的分片資訊。 |
