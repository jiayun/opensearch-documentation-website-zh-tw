---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除 ML 任務"
parent: ML Tasks APIs
grand_parent: ML APIs
nav_order: 20
---

# 刪除 ML 任務 API

根據 `task_id` 刪除機器學習 (ML) 任務。

OpenSearch 在執行刪除請求時不會檢查任務狀態。目前仍在執行中的任務有可能在完成前就被刪除。若要檢查任務狀態，請在刪除任務前先執行 `GET /_plugins/_ml/tasks/<task_id>`。
{: .note}

## 端點

```json
DELETE /_plugins/_ml/tasks/{task_id}
```

## 範例請求

```json
DELETE /_plugins/_ml/tasks/xQRYLX8BydmmU1x6nuD3
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "_index" : ".plugins-ml-task",
  "_id" : "xQRYLX8BydmmU1x6nuD3",
  "_version" : 4,
  "result" : "deleted",
  "forced_refresh" : true,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 42,
  "_primary_term" : 7
}
```

## 錯誤回應

如果您嘗試刪除不存在的任務，OpenSearch 會傳回 404 Not Found 錯誤：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "status_exception",
        "reason": "Failed to find task"
      }
    ],
    "type": "status_exception",
    "reason": "Failed to find task"
  },
  "status": 404
}
```