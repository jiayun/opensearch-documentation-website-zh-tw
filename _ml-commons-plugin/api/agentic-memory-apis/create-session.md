---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立工作階段"
parent: Agentic memory APIs
grand_parent: ML Commons APIs
nav_order: 40
---

# 建立工作階段
**於 3.3 版推出**
{: .label .label-purple }

使用此 API 在記憶體容器中建立新的工作階段。工作階段代表使用者與代理程式之間不同的互動情境。

## 路徑與 HTTP 方法

```json
POST /_plugins/_ml/memory_containers/{memory_container_id}/memories/sessions
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `memory_container_id` | 字串 | 必要 | 將建立工作階段的記憶體容器 ID。 |

## 請求欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `session_id` | 字串 | 選用 | 自訂工作階段 ID。若提供此 ID，工作階段將使用此 ID。若未提供，則會產生隨機 ID。 |
| `summary` | 字串 | 選用 | 工作階段摘要或說明。 |
| `metadata` | 物件 | 選用 | 以鍵值對形式提供的工作階段其他中繼資料。 |
| `namespace` | 物件 | 選用 | 用於組織工作階段的命名空間資訊。 |

## 範例請求：使用自訂 ID 建立工作階段

```json
POST /_plugins/_ml/memory_containers/SdjmmpgBOh0h20Y9kWuN/memories/sessions
{
  "session_id": "abc123",
  "metadata": {
    "key1": "value1"
  }
}
```

## 範例回應：自訂工作階段 ID

```json
{
  "session_id": "abc123",
  "status": "created"
}
```

## 範例請求：建立具有自動產生 ID 的工作階段

```json
POST /_plugins/_ml/memory_containers/SdjmmpgBOh0h20Y9kWuN/memories/sessions
{
  "summary": "This is a test session",
  "metadata": {
    "key1": "value1"
  },
  "namespace": {
    "user_id": "bob"
  }
}
```
{% include copy-curl.html %}

## 範例回應：自動產生的工作階段 ID

```json
{
  "session_id": "jTYm35kBt8CyICnjxJl9",
  "status": "created"
}
```

## 回應欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `session_id` | 字串 | 所建立工作階段的 ID (無論是提供或自動產生)。 |
| `status` | 字串 | 建立作業的狀態。 |
