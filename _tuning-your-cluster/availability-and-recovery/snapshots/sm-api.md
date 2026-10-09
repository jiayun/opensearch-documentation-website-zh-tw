---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "快照管理 API"
parent: Snapshots
nav_order: 30
has_children: false
grand_parent: Availability and recovery
redirect_from: 
  - /opensearch/snapshots/sm-api/
---

# 快照管理 API

使用快照管理 (SM) API 自動化[建立快照]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore#take-snapshots)。

---

<details markdown="block">
  <summary>
    目錄
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

---

## 建立或更新政策
於 2.1 版引入
{: .label .label-purple }

建立或更新 SM 政策。

#### 端點

建立：

```json
POST _plugins/_sm/policies/{policy_name} 
```

更新：

```json
PUT _plugins/_sm/policies/{policy_name}?if_seq_no=0&if_primary_term=1
```

更新請求必須提供 `seq_no` 與 `primary_term` 參數。

### 範例請求

```json
POST _plugins/_sm/policies/daily-policy
{
  "description": "Daily snapshot policy",
  "creation": {
    "schedule": {
      "cron": {
        "expression": "0 8 * * *",
        "timezone": "UTC"
      }
    },
    "time_limit": "1h"
  },
  "deletion": {
    "schedule": {
      "cron": {
        "expression": "0 1 * * *",
        "timezone": "America/Los_Angeles"
      }
    },
    "condition": {
      "max_age": "7d",
      "max_count": 21,
      "min_count": 7
    },
    "time_limit": "1h",
    "snapshot_pattern": "external-backup-*"
  },
  "snapshot_config": {
    "date_format": "yyyy-MM-dd-HH:mm",
    "timezone": "America/Los_Angeles",
    "indices": "*",
    "repository": "s3-repo",
    "ignore_unavailable": "true",
    "include_global_state": "false",
    "partial": "true",
    "metadata": {
      "any_key": "any_value"
    }
  },
  "notification": {
    "channel": {
      "id": "NC3OpoEBzEoHMX183R3f"
    },
    "conditions": {
      "creation": true,
      "deletion": false,
      "failure": false,
      "time_limit_exceeded": false
    }
  }
}
```

### 範例回應

```json
{
  "_id" : "daily-policy-sm-policy",
  "_version" : 5,
  "_seq_no" : 54983,
  "_primary_term" : 21,
  "sm_policy" : {
    "name" : "daily-policy",
    "description" : "Daily snapshot policy",
    "schema_version" : 15,
    "creation" : {
      "schedule" : {
        "cron" : {
          "expression" : "0 8 * * *",
          "timezone" : "UTC"
        }
      },
      "time_limit" : "1h"
    },
    "deletion" : {
      "schedule" : {
        "cron" : {
          "expression" : "0 1 * * *",
          "timezone" : "America/Los_Angeles"
        }
      },
      "condition" : {
        "max_age" : "7d",
        "min_count" : 7,
        "max_count" : 21
      },
      "time_limit" : "1h",
      "snapshot_pattern" : "external-backup-*"
    },
    "snapshot_config" : {
      "indices" : "*",
      "metadata" : {
        "any_key" : "any_value"
      },
      "ignore_unavailable" : "true",
      "timezone" : "America/Los_Angeles",
      "include_global_state" : "false",
      "date_format" : "yyyy-MM-dd-HH:mm",
      "repository" : "s3-repo",
      "partial" : "true"
    },
    "schedule" : {
      "interval" : {
        "start_time" : 1656425122909,
        "period" : 1,
        "unit" : "Minutes"
      }
    },
    "enabled" : true,
    "last_updated_time" : 1656425122909,
    "enabled_time" : 1656425122909,
    "notification" : {
      "channel" : {
        "id" : "NC3OpoEBzEoHMX183R3f"
      },
      "conditions" : {
        "creation" : true,
        "deletion" : false,
        "failure" : false,
        "time_limit_exceeded" : false
      }
    }
  }
}
```

### 參數

您可指定下列參數來建立/更新 SM 政策。

參數 | 類型 | 說明
:--- | :--- |:--- |:--- |
`description` | 字串 | SM 政策的說明。選用。
`enabled` | 布林值 | 是否要在建立時啟用此 SM 政策？選用。
`snapshot_config` | 物件 | 快照建立的組態選項。必要。
`snapshot_config.date_format` | 字串 | 快照名稱的格式為 `<policy_name>-<date>-<random number>`。`date_format` 指定快照名稱中日期的格式。支援 OpenSearch 支援的所有日期格式。選用。預設為 "yyyy-MM-dd'T'HH:mm:ss"。
`snapshot_config.date_format_timezone` | 字串 | 快照名稱的格式為 `<policy_name>-<date>-<random number>`。`date_format_timezone` 指定快照名稱中日期的時區。選用。預設為 `UTC`。
`snapshot_config.indices` | 字串 | 快照中的索引名稱。多個索引名稱以 `,` 分隔。支援萬用字元 (`*`)。選用。預設為 `*` (所有索引)。
`snapshot_config.repository` | 字串 | 用來儲存快照的儲存庫。必要。
`snapshot_config.ignore_unavailable` | 布林值 | 是否要忽略無法使用的索引？選用。預設為 `false`。
`snapshot_config.include_global_state` | 布林值 | 是否要包含叢集狀態？選用。由於[安全性外掛程式考量]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore#security-considerations)，預設為 `true`。
`snapshot_config.partial` | 布林值 | 是否要允許部分快照？選用。預設為 `false`。
`snapshot_config.metadata` | 物件 | 以鍵值對形式呈現的中繼資料。選用。
`creation` | 物件 | 快照建立的組態。在 OpenSearch 3.3 及更新版本中為選用。**重要**：在所有節點升級至 OpenSearch 3.3 或更新版本之前，請勿將此項保持未設定。
`creation.schedule` | 字串 | 用來建立快照的 cron 排程。必要。
`creation.time_limit` | 字串 | 設定等待快照建立完成的最長時間。若 time_limit 長於排定的快照建立時間間隔，則在 time_limit 經過之前不會建立任何排定的快照。例如，若 time_limit 設為 35 分鐘，且快照從午夜開始每 30 分鐘建立一次，則會建立 00:00 與 01:00 的快照，但會略過 00:30 的快照。選用。
`deletion` | 物件 | 快照刪除的組態。選用。預設為保留所有快照。
`deletion.schedule` | 字串 | 用來刪除快照的 cron 排程。選用。預設為使用 `creation.schedule`，此為必要。
`deletion.time_limit` | 字串 | 設定等待快照刪除完成的最長時間。選用。
`deletion.condition` | 物件 | 快照刪除的條件。必要。
`deletion.condition.max_count` | 整數 | 要保留的快照數量上限。選用。您必須指定 `max_age`、`max_count` 或兩者。
`deletion.condition.max_age` | 字串 | 快照保留的最長時間。選用。您必須指定 `max_age`、`max_count` 或兩者。
`deletion.condition.min_count` | 整數 | 要保留的快照數量下限。選用。預設為 `1`。
`deletion.snapshot_pattern` | 字串 | 要納入刪除的其他快照模式。這可讓您除了政策本身的快照之外，一併刪除符合指定模式的快照。支援萬用字元 (`*`)。選用。
`notification` | 物件 | 定義 SM 事件的通知。選用。
`notification.channel` | 物件 | 定義通知的管道。您必須先[建立並設定通知管道]({{site.url}}{{site.baseurl}}/notifications-plugin/api/)，才能設定 SM 通知。必要。
`notification.channel.id` | 字串 | 用於通知的管道 ID。若要取得所有已建立管道的管道 ID，請使用 `GET _plugins/_notifications/configs`。必要。
`notification.conditions` | 物件 | 您要收到通知的 SM 事件。將您感興趣的事件設為 `true`。
`notification.conditions.creation` | 布林值 | 是否要收到快照建立的通知？選用。預設為 `true`。
`notification.conditions.deletion` | 布林值 | 是否要收到快照刪除的通知？選用。預設為 `false`。
`notification.conditions.failure` | 布林值 | 是否要收到建立或刪除失敗的通知？選用。預設為 `false`。
`notification.conditions.time_limit_exceeded` | 布林值 | 是否要在快照作業耗時超過 time_limit 時收到通知？選用。預設為 `false`。

## 取得政策
於 2.1 版引入
{: .label .label-purple }

取得 SM 政策。

#### 端點

取得所有 SM 政策：

```json
GET _plugins/_sm/policies
```
您可以使用[查詢字串]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)，並指定分頁、排序依據欄位及排序順序：

```json
GET _plugins/_sm/policies?from=0&size=20&sortField=sm_policy.name&sortOrder=desc&queryString=*
```

取得特定 SM 政策：

```
GET _plugins/_sm/policies/{policy_name}
```

### 請求範例

```json
GET _plugins/_sm/policies/daily-policy
```

### 回應範例

```json
{
  "_id" : "daily-policy-sm-policy",
  "_version" : 6,
  "_seq_no" : 44696,
  "_primary_term" : 19,
  "sm_policy" : {
    "name" : "daily-policy",
    "description" : "Daily snapshot policy",
    "schema_version" : 15,
    "creation" : {
      "schedule" : {
        "cron" : {
          "expression" : "0 8 * * *",
          "timezone" : "UTC"
        }
      },
      "time_limit" : "1h"
    },
    "deletion" : {
      "schedule" : {
        "cron" : {
          "expression" : "0 1 * * *",
          "timezone" : "America/Los_Angeles"
        }
      },
      "condition" : {
        "max_age" : "7d",
        "min_count" : 7,
        "max_count" : 21
      },
      "time_limit" : "1h",
      "snapshot_pattern" : "external-backup-*"
    },
    "snapshot_config" : {
      "metadata" : {
        "any_key" : "any_value"
      },
      "ignore_unavailable" : "true",
      "include_global_state" : "false",
      "date_format" : "yyyy-MM-dd-HH:mm",
      "repository" : "s3-repo",
      "partial" : "true"
    },
    "schedule" : {
      "interval" : {
        "start_time" : 1656341042874,
        "period" : 1,
        "unit" : "Minutes"
      }
    },
    "enabled" : true,
    "last_updated_time" : 1656341042874,
    "enabled_time" : 1656341042874
  }
}
```

## 說明
於 2.1 版引入
{: .label .label-purple }

提供所有指定政策的啟用／停用狀態及中繼資料。多個政策名稱以 `,` 分隔。您也可以使用萬用字元模式指定所需的政策。 

![SM 狀態機]({{site.url}}{{site.baseurl}}/images/sm-state-machine.png){: width="150" style="float: left; margin-right: 15px;" }

SM 使用狀態機來建立及刪除快照。左圖顯示建立工作流程的一個執行週期，從 CREATION_START 狀態到 CREATION_FINISHED 狀態。刪除工作流程遵循與建立工作流程相同的模式。 

建立工作流程從 CREATION_START 狀態開始，並持續檢查是否符合建立 cron 排程中的條件。符合條件後，建立工作流程會切換至 CREATION_CONDITION_MET 狀態，接著進入 CREATING 狀態。CREATING 狀態會以非同步方式呼叫 Create Snapshot API，然後等待快照建立作業在 CREATION_FINISHED 狀態結束。快照建立作業結束後，建立工作流程會返回 CREATION_START 狀態，並繼續循環。`metadata.creation` 和 `metadata.deletion` 的 `current_state` 欄位會傳回狀態機的目前狀態。

#### 端點

```json
GET _plugins/_sm/policies/{policy_names}/_explain
```

### 請求範例

```json
GET _plugins/_sm/policies/daily*/_explain
```

### 回應範例

```json
{
  "policies" : [
    {
      "name" : "daily-policy",
      "creation" : {
        "current_state" : "CREATION_START",
        "trigger" : {
          "time" : 1656403200000
        }
      },
      "deletion" : {
        "current_state" : "DELETION_START",
        "trigger" : {
          "time" : 1656403200000
        }
      },
      "policy_seq_no" : 44696,
      "policy_primary_term" : 19,
      "enabled" : true
    }
  ]
}
```

下表列出回應中每個政策的所有欄位。

欄位 | 說明 
:--- |:--- 
`name` | SM 政策的名稱。
`creation` | 最新建立作業的資訊。請參閱下列子欄位。
`deletion` | 最新刪除作業的資訊。請參閱下列子欄位。
`policy_seq_no` <br> `policy_primary_term` | SM 政策的版本。
`enabled` | 政策是否正在執行？

下表列出每個政策的 `creation` 和 `deletion` 物件中的所有欄位。

欄位 | 說明 
:--- |:--- 
`current_state` | 如前一節所述，執行快照建立／刪除作業的狀態機目前所處的狀態。
`trigger.time` | 下次建立／刪除作業的執行時間，以自紀元起算的毫秒數表示。
`latest_execution` | 描述最新一次建立／刪除作業的執行情形。
`latest_execution.status` | 最新一次建立／刪除作業的執行狀態。可能的值包括：<br> `IN_PROGRESS`：快照建立／刪除作業已開始。<br> `SUCCESS`：快照建立／刪除作業已成功完成。<br> `RETRYING`：建立／刪除嘗試已失敗。將重試三次。<br> `FAILED`：建立／刪除嘗試在重試三次後仍失敗。結束目前的執行週期並進入下一個執行週期。<br> `TIME_LIMIT_EXCEEDED`：建立／刪除作業的時間超過政策中設定的 time_limit。結束目前的執行週期並進入下一個執行週期。
`latest_execution.start_time` | 最新一次執行的開始時間，以自紀元起算的毫秒數表示。
`latest_execution.end_time` | 最新一次執行的結束時間，以自紀元起算的毫秒數表示。
`latest_execution.info.message` | 以易於理解的訊息描述最新一次執行的狀態。
`latest_execution.info.cause` | 若最新一次執行失敗，則包含失敗原因。
`retry.count` | 剩餘的執行重試次數。


## 啟動政策
於 2.1 版引入
{: .label .label-purple }

將政策的 `enabled` 旗標設為 `true`，以啟動政策。 

#### 端點

```json
POST  _plugins/_sm/policies/{policy_name}/_start
```

### 請求範例

```json
POST  _plugins/_sm/policies/daily-policy/_start
```

### 回應範例

```json
{
  "acknowledged" : true
}
```

## 停止政策
於 2.1 版引入
{: .label .label-purple }

將 SM 政策的 `enabled` 旗標設為 `false`。在您[啟動](#start-a-policy)政策之前，政策不會執行。

#### 端點

```json
POST  _plugins/_sm/policies/{policy_name}/_stop
```

### 請求範例

```json
POST  _plugins/_sm/policies/daily-policy/_stop
```

### 回應範例

```json
{
  "acknowledged" : true
}
```

## 刪除政策
於 2.1 版引入
{: .label .label-purple }

刪除指定的 SM 政策。

#### 端點

```json
DELETE  _plugins/_sm/policies/{policy_name}
```

### 請求範例

```json
DELETE _plugins/_sm/policies/daily-policy
```

### 回應範例

```json
{
  "_index" : ".opendistro-ism-config",
  "_id" : "daily-policy-sm-policy",
  "_version" : 8,
  "result" : "deleted",
  "forced_refresh" : true,
  "_shards" : {
    "total" : 2,
    "successful" : 2,
    "failed" : 0
  },
  "_seq_no" : 45366,
  "_primary_term" : 20
}
```
