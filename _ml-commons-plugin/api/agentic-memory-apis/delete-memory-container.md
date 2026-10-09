---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除記憶容器"
parent: Agentic memory APIs
grand_parent: ML Commons APIs
nav_order: 30
---

# 刪除記憶容器 API
**於 3.3 版推出**
{: .label .label-purple }

使用此 API，依 ID 刪除記憶容器。

## 端點

```json
DELETE /_plugins/_ml/memory_containers/{memory_container_id}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要／選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `memory_container_id` | 字串 | 必要 | 要刪除的記憶容器 ID。 |

## 查詢參數

下表列出可用的查詢參數。

| 參數 | 資料類型 | 必要／選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `delete_all_memories` | 布林值 | 選用 | 控制刪除容器時是否刪除所有記憶索引。預設為 `false`。當值為 `false` 時，會保留記憶索引（sessions、working、long-term、history）。 |
| `delete_memories` | 陣列 | 選用 | 刪除容器時要刪除的記憶類型陣列。預設為空陣列。接受的值：`sessions`、`working`、`long-term`、`history`。範例：`delete_memories=sessions,working`。 |

## 請求範例：基本刪除（保留記憶索引）

```json
DELETE /_plugins/_ml/memory_containers/SdjmmpgBOh0h20Y9kWuN
```

## 請求範例：刪除容器及所有記憶索引

```json
DELETE /_plugins/_ml/memory_containers/SdjmmpgBOh0h20Y9kWuN?delete_all_memories=true
```

## 請求範例：刪除容器及特定記憶類型

```json
DELETE /_plugins/_ml/memory_containers/SdjmmpgBOh0h20Y9kWuN?delete_memories=sessions,working
```
{% include copy-curl.html %}

## 回應範例

```json
{
    "_index": ".plugins-ml-memory-container",
    "_id": "SdjmmpgBOh0h20Y9kWuN",
    "_version": 3,
    "result": "deleted",
    "forced_refresh": true,
    "_shards": {
        "total": 2,
        "successful": 2,
        "failed": 0
    },
    "_seq_no": 6,
    "_primary_term": 1
}
```

## 錯誤回應

如果您嘗試刪除不存在的記憶容器，OpenSearch 會傳回 404 Not Found 錯誤：

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

## 回應欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `result` | 字串 | 刪除操作的結果。 |
| `_id` | 字串 | 已刪除的記憶容器 ID。 |
| `_version` | 整數 | 刪除後的版本號碼。 |
| `_shards` | 物件 | 參與操作的分片資訊。 |
| `_seq_no` | 長整數 | 指派給刪除操作的序號。 |
| `_primary_term` | 長整數 | 索引的主要分片任期。 |