---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Jobs API
parent: Job Scheduler
nav_order: 10
redirect_from:
    - /monitoring-plugins/job-scheduler/api/
---

# Job Scheduler Jobs API 
於 3.2 版推出
{: .label .label-purple }

Jobs API 可讓您檢視所有 Job Scheduler 工作。

## 端點

```json
GET /_plugins/_job_scheduler/api/jobs
```

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `by_node` | 布林值 | 傳回依執行所在節點分組的工作。預設為 `false`。 |

## 請求範例

```json
GET /_plugins/_job_scheduler/api/jobs
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "jobs": [
    {
      "job_type": "reports-scheduler",
      "job_id": "Cuu8Z5gBTcOdmakPQ51t",
      "index_name": ".opendistro-reports-definitions",
      "name": "index_report",
      "descheduled": false,
      "enabled": true,
      "enabled_time": "2025-08-01T22:24:08.044Z",
      "last_update_time": "2025-08-01T22:24:08.044Z",
      "last_execution_time": "none",
      "last_expected_execution_time": "none",
      "next_expected_execution_time": "2025-08-04T02:15:00.000Z",
      "schedule": {
        "type": "cron",
        "expression": "15 2 1,15 * 1",
        "timezone": "Africa/Abidjan",
        "delay": "none"
      },
      "lock_duration": "no_lock",
      "jitter": "none"
    },
    {
      "job_type": "scheduler_sample_extension",
      "job_id": "jobid1",
      "index_name": ".scheduler_sample_extension",
      "name": "sample-job-it",
      "descheduled": false,
      "enabled": true,
      "enabled_time": "1970-07-23T00:27:45.353Z",
      "last_update_time": "1970-07-23T00:27:45.353Z",
      "last_execution_time": "2025-08-01T22:28:45.357484385Z",
      "last_expected_execution_time": "2025-08-01T22:28:45.353111804Z",
      "next_expected_execution_time": "2025-08-01T22:29:45.353111804Z",
      "schedule": {
        "type": "interval",
        "start_time": "1970-07-23T00:27:45.353Z",
        "interval": 1,
        "unit": "Minutes",
        "delay": "none"
      },
      "lock_duration": 10,
      "jitter": "none"
    }
  ],
  "failures": [],
  "total_jobs": 2
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `jobs` | 陣列 | 包含 Job Scheduler 回報的所有工作。 |
| `job_type` | 字串 | 排定該工作的外掛程式。 |
| `job_id` | 字串 | 工作的唯一識別碼。 |
| `index_name` | 字串 | 儲存工作資訊的索引。 |
| `name` | 字串 | 工作名稱。名稱不一定是唯一的。 |
| `descheduled` | 布林值 | 表示工作是否已由 Job Scheduler 排定執行 (`false`) 或未排定 (`true`)。 |
| `enabled` | 布林值 | 表示工作是否為作用中 (`true`) 或非作用中 (`false`)，由使用 Job Scheduler 的外掛程式定義。 |
| `enabled_time` | 字串 | 工作最初排定的時間。 |
| `last_update_time` | 字串 | 工作上次更新的時間。 |
| `last_expected_exection_time` | 字串 | 工作最近一次執行的時間。 |
| `next_expected_execution_time` | 字串 | 工作預期下次執行的時間。 |
| `schedule` | 對應表 | 工作的執行排程。可定義 [Cron](#cron-schedule) 或[間隔](#interval-schedule)排程。 |
| `schedule.type` | 字串 | 排程類型。有效值為 `cron` 和 `interval`。 |
| `lock_duration` | 整數 | 工作在執行期間可保持鎖定的最長時間 (秒)。 |
| `jitter` | 雙精度浮點數 | 套用至工作執行時間的隨機延遲，以防止整個系統同時執行。 |
| `failures` | 陣列 | 未成功回報工作的節點清單。 |
| `total_jobs` | 整數 | 所有節點回報的工作總數。 |

### 間隔排程

`interval` 排程支援下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `start_time` | 字串 | 排程開始時間。 |
| `interval` | 整數 | 工作執行之間的數值間隔時間 (例如 `10`)。 |
| `unit` | 字串 | 間隔單位 (例如 `Minutes`、`Hours` 或 `Days`)。 |
| `delay` | 字串 | 在工作執行前套用的固定時間。 |

### Cron 排程

`cron` 排程支援下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `expression` | 字串 | 定義排程的 Cron 運算式。 |
| `timezone` | 字串 | 與 Cron 排程關聯的時區。 |
