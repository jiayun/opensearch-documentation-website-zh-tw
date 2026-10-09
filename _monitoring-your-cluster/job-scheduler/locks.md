---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Locks API
parent: Job Scheduler
nav_order: 20
---

# Job Scheduler Locks API 
於 3.2 版推出
{: .label .label-purple }

Job Scheduler 使用分散式鎖定機制，確保整個叢集中同一時間只有一個作業執行個體在執行。Locks API 會傳回 Job Scheduler 所管理之所有作用中作業鎖定的相關資訊。

## 端點

```json
GET /_plugins/_job_scheduler/api/locks
GET /_plugins/_job_scheduler/api/locks/{lock_id}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `<lock_id>` | 字串 | 鎖定的唯一識別碼，格式為 `"index"-"job_id"`（例如 `.scheduler_sample_extension-jobid1`）。索引名稱與作業 ID 必須以連字號（`-`）分隔。|

## 範例請求

```json
GET /_plugins/_job_scheduler/api/locks
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "total_locks": 1,
  "locks": {
    ".scheduler_sample_extension-jobid1": {
      "job_index_name": ".scheduler_sample_extension",
      "job_id": "jobid1",
      "lock_time": 1754410412,
      "lock_duration_seconds": 10,
      "released": false
    }
  }
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `total_locks` | 整數 | 作用中與已釋放鎖定的總數。 |
| `locks` | 對應表 | 鎖定 ID 及其相關聯鎖定資訊的對應表。 |
| `job_index_name` | 字串 | 儲存作業之索引的名稱。 |
| `job_id` | 字串 | 作業 ID。 |
| `lock_time` | 自紀元起算的秒數 | 取得鎖定的時間。 |
| `lock_duration_seconds` | 整數 | 鎖定有效的時間長度上限。 |
| `released` | 布林值 | 	指出鎖定已釋放（`true`）或目前為作用中（`false`）。 |