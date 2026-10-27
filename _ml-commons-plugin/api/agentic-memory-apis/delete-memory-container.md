---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除記憶容器"
parent: Agentic memory APIs
grand_parent: ML APIs
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

| 參數 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `delete_all_memories` | 布林值 | 選用 | 控制刪除容器時是否刪除所有記憶索引。預設為 `false`。當值為 `false` 時，會保留記憶索引（工作階段、工作記憶、長期記憶、歷程記錄）。 |
| `delete_memories` | 陣列 | 選用 | 刪除容器時要刪除的記憶類型陣列。預設為空陣列。接受的值：`sessions`、`working`、`long-term`、`history`。範例：`delete_memories=sessions,working`。 |

您也可以在請求本文中提供 `delete_all_memories` 和 `delete_memories`。如果在這兩個位置都指定了同一個參數，則以查詢參數為優先。

## 範例請求：基本刪除（保留記憶索引）

```json
DELETE /_plugins/_ml/memory_containers/SdjmmpgBOh0h20Y9kWuN
```
{% include copy-curl.html %}

## 範例請求：刪除容器及所有記憶索引

```json
DELETE /_plugins/_ml/memory_containers/SdjmmpgBOh0h20Y9kWuN?delete_all_memories=true
```
{% include copy-curl.html %}

## 請求範例：刪除容器及特定記憶類型

```json
DELETE /_plugins/_ml/memory_containers/SdjmmpgBOh0h20Y9kWuN?delete_memories=sessions,working
```
{% include copy-curl.html %}

## 範例回應

```json
{
    "_index": ".plugins-ml-am-memory-container",
    "_id": "SdjmmpgBOh0h20Y9kWuN",
    "_version": 2,
    "result": "deleted",
    "forced_refresh": true,
    "_shards": {
        "total": 1,
        "successful": 1,
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

只有在沒有其他記憶容器使用相同 `index_prefix` 時，才能刪除記憶索引。如果其他容器共用該前綴，則指定 `delete_all_memories` 或 `delete_memories` 的請求會失敗並傳回 409 Conflict 錯誤，且不會刪除該容器。若要刪除該容器，請在不含這些參數的情況下傳送請求。
{: .note}

## 回應欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `_index` | 字串 | 儲存記憶容器的索引名稱。 |
| `result` | 字串 | 刪除作業的結果。 |
| `_id` | 字串 | 已刪除之記憶容器的 ID。 |
| `_version` | 整數 | 刪除後的版本號碼。 |
| `forced_refresh` | 布林值 | 作業完成後是否強制執行重新整理。 |
| `_shards` | 物件 | 此作業所涉及分片的相關資訊。 |
| `_seq_no` | Long | 指派給刪除作業的序號。 |
| `_primary_term` | Long | 索引的主要分片任期。 |