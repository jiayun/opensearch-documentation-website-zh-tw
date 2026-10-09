---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "大量複寫 API"
nav_order: 55
parent: Cross-cluster replication
---

# 大量複寫 API

使用大量複寫操作，透過單一 API 呼叫以程式設計方式管理多個索引的跨叢集複寫。您可以指定索引模式來選取相符的索引，並大量執行啟動、停止、暫停或繼續操作。

所有大量複寫操作皆為非同步。每個請求都會傳回一個 `task_id`，您可用來[檢查工作進度](#get-bulk-task-status)或[取消操作](#cancel-bulk-task)。每個叢集一次只能執行一個大量複寫工作；當有大量複寫操作正在進行時，若再提交新的大量複寫操作，會導致 `409 Conflict` 錯誤。如果大量複寫操作對某些索引失敗，工作會繼續處理其餘索引，並回報操作成功與失敗的索引清單。您可以隨時取消執行中的大量工作，但已處理的索引不會還原。索引會以可設定的批次處理（請參閱[設定](#settings)）。大量複寫操作不具等冪性：若您在前一個工作執行完畢後提交相同的請求，會建立新的工作。

## 模式比對

`pattern` 欄位支援與 OpenSearch 索引模式相同的語法：

- `*` 可比對任意數量的字元。
- `?` 可比對單一字元。
- 模式不得以 `_` 開頭。
- 模式不得包含空格、引號（`"`）、角括號（`<`、`>`）、直立線（`|`）、反斜線（`\`）、井號（`#`）或逗號（`,`）。

範例：
- `my-index-*` 可比對 `my-index-1`、`my-index-2`、`my-index-logs` 等。
- `*` 可比對所有索引（不含以 `.` 開頭的系統索引）。
- `logs-2024-0?` 可比對 `logs-2024-01`--`logs-2024-09`。

---

<details markdown="block">
  <summary>
    目錄
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 大量啟動複寫
**於 3.7 版推出**
{: .label .label-purple }

為領導叢集中所有符合指定模式的索引啟動複寫。請將此請求傳送至跟隨者叢集。

### 端點

```json
POST /_plugins/_replication/_bulk_start
```

### 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明 | 必要
:--- | :--- |:--- |:--- 
`leader_alias` | 字串 | 跨叢集連線的名稱。您可在[設定跨叢集連線]({{site.url}}{{site.baseurl}}/replication-plugin/get-started/#set-up-a-cross-cluster-connection)時定義此別名。 | 是
`pattern` | 字串 | 用來比對領導叢集上索引的索引模式。支援萬用字元。例如，`my-index-*` 或 `*` 代表所有索引。 | 是
`use_roles` | 物件 | 後續索引之間所有後端複寫工作要使用的角色。請指定 `leader_cluster_role` 和 `follower_cluster_role`。請參閱[對應領導與跟隨者叢集角色]({{site.url}}{{site.baseurl}}/replication-plugin/permissions/#map-the-leader-and-follower-cluster-roles)。 | 若已啟用安全性外掛程式
`filters` | 物件 | 包含篩選條件的物件，用來精簡索引選取。 | 否
`filters.exclude_index` | 陣列 | 要從操作中排除的索引名稱清單。 | 否

### 範例請求

```json
POST /_plugins/_replication/_bulk_start
{
   "leader_alias": "<connection-alias-name>",
   "pattern": "<index-pattern>",
   "use_roles": {
      "leader_cluster_role": "<role-name>",
      "follower_cluster_role": "<role-name>"
   },
   "filters": {
      "exclude_index": ["<index-name-1>", "<index-name-2>"]
   }
}
```
{% include copy-curl.html %}

## 大量停止複寫
**於 3.7 版推出**
{: .label .label-purple }

停止複寫，並將所有相符的跟隨者索引轉換為可接受寫入操作的標準索引。請將此請求傳送至跟隨者叢集。

### 端點

```json
POST /_plugins/_replication/_bulk_stop
```

### 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明 | 必要
:--- | :--- |:--- |:---
`pattern` | 字串 | 用來比對跟隨者索引的索引模式。支援萬用字元。例如，`follower-*` 或 `*` 代表所有複寫中的索引。 | 是
`filters` | 物件 | 包含篩選條件的物件，用來精簡索引選取。 | 否
`filters.exclude_index` | 陣列 | 要從操作中排除的索引名稱清單。 | 否

### 範例請求

```json
POST /_plugins/_replication/_bulk_stop
{
   "pattern": "<index-pattern>",
   "filters": {
      "exclude_index": ["<index-name-1>", "<index-name-2>"]
   }
}
```
{% include copy-curl.html %}

## 大量暫停複寫
**於 3.7 版推出**
{: .label .label-purple }

暫停所有相符跟隨者索引的複寫。請將此請求傳送至跟隨者叢集。

複寫暫停超過 12 小時後即無法繼續。您必須[停止複寫]({{site.url}}{{site.baseurl}}/replication-plugin/api/#stop-replication)、刪除跟隨者索引，並重新啟動領導者的複寫。
{: .warning }

### 端點

```json
POST /_plugins/_replication/_bulk_pause
```

### 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明 | 必要
:--- | :--- |:--- |:---
`pattern` | 字串 | 用來比對跟隨者索引的索引模式。支援萬用字元。 | 是
`filters` | 物件 | 包含篩選條件的物件，用來精簡索引選取。 | 否
`filters.exclude_index` | 陣列 | 要從操作中排除的索引名稱清單。 | 否

### 範例請求

```json
POST /_plugins/_replication/_bulk_pause
{
   "pattern": "<index-pattern>",
   "filters": {
      "exclude_index": ["<index-name-1>", "<index-name-2>"]
   }
}
```
{% include copy-curl.html %}

## 大量繼續複寫
**於 3.7 版推出**
{: .label .label-purple }

為所有符合指定模式且已暫停的跟隨者索引繼續複寫。領導叢集必須可連線，且每個索引的保留租約必須仍然有效。請將此請求傳送至跟隨者叢集。

### 端點

```json
POST /_plugins/_replication/_bulk_resume
```

### 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明 | 必要
:--- | :--- |:--- |:---
`pattern` | 字串 | 用來比對已暫停跟隨者索引的索引模式。支援萬用字元。 | 是
`filters` | 物件 | 包含篩選條件的物件，用來精簡索引選取。 | 否
`filters.exclude_index` | 陣列 | 要從操作中排除的索引名稱清單。 | 否

### 範例請求

```json
POST /_plugins/_replication/_bulk_resume
{
   "pattern": "<index-pattern>",
   "filters": {
      "exclude_index": ["<index-name-1>", "<index-name-2>"]
   }
}
```
{% include copy-curl.html %}

## 取得大量複寫狀態
**於 3.7 版推出**
{: .label .label-purple }

傳回所有符合模式之索引的目前複寫狀態。與[取得大量工作狀態](#get-bulk-task-status)端點不同，此端點傳回的是即時複寫狀態，而非大量複寫操作的進度。請將此請求傳送至跟隨者叢集。

### 端點

```json
GET /_plugins/_replication/_bulk_status?pattern={index-pattern}
```

### 查詢參數

下表列出可用的查詢參數。

參數 | 資料類型 | 說明 | 必要
:--- | :--- |:--- |:---
`pattern` | 字串 | 用於比對追隨者索引的索引模式。支援萬用字元。 | 是

### 回應範例

```json
{
   "indices": {
      "bulk-test-3": {
         "status": "SYNCING",
         "reason": "User initiated",
         "leader_alias": "leader-cluster",
         "leader_index": "bulk-test-3",
         "follower_index": "bulk-test-3",
         "syncing_details": {
            "leader_checkpoint": -1,
            "follower_checkpoint": -1,
            "seq_no": 0
         }
      },
      "bulk-test-6": {
         "status": "PAUSED",
         "reason": "bulk_pause",
         "leader_alias": "leader-cluster",
         "leader_index": "bulk-test-6",
         "follower_index": "bulk-test-6"
      },
      "bulk-test-9": {
         "status": "BOOTSTRAPPING",
         "reason": "User initiated",
         "leader_alias": "leader-cluster",
         "leader_index": "bulk-test-9",
         "follower_index": "bulk-test-9",
         "bootstrap_details": {
            "status": "IN_PROGRESS",
            "shard_restore_details": {
               "total_shards": 5,
               "successful_shards": 2,
               "failed_shards": 0,
               "in_progress_shards": 3
            }
         }
      }
   }
}
```

### 回應本文欄位

下表列出回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`indices` | 物件 | 將索引名稱對應至其複寫狀態物件的對應表。
`indices.<index>.status` | 字串 | 目前的複寫狀態。可能的值為 `SYNCING`、`BOOTSTRAPPING`、`PAUSED`、`RESTORING`。
`indices.<index>.reason` | 字串 | 目前狀態的原因。
`indices.<index>.leader_alias` | 字串 | 領導者叢集的跨叢集連線別名。
`indices.<index>.leader_index` | 字串 | 領導者叢集上的索引名稱。
`indices.<index>.follower_index` | 字串 | 追隨者叢集上的索引名稱。
`indices.<index>.syncing_details` | 物件 | 複寫進度詳細資訊。當狀態為 `SYNCING` 時存在。
`indices.<index>.syncing_details.leader_checkpoint` | 整數 | 領導者索引上的最新檢查點。
`indices.<index>.syncing_details.follower_checkpoint` | 整數 | 追隨者索引上的最新檢查點。
`indices.<index>.syncing_details.seq_no` | 整數 | 目前的序號。
`indices.<index>.bootstrap_details` | 物件 | 初始載入進度詳細資訊。僅在狀態為 `BOOTSTRAPPING` 時存在。初始載入完成且複寫進入同步階段後，此欄位會由 `syncing_details` 取代。
`indices.<index>.bootstrap_details.status` | 字串 | 初始載入狀態。可能的值為 `IN_PROGRESS`、`COMPLETED`、`FAILED`。
`indices.<index>.bootstrap_details.shard_restore_details` | 物件 | 初始載入期間的分片層級還原進度。
`indices.<index>.bootstrap_details.shard_restore_details.total_shards` | 整數 | 要還原的分片總數。
`indices.<index>.bootstrap_details.shard_restore_details.successful_shards` | 整數 | 成功還原的分片數量。
`indices.<index>.bootstrap_details.shard_restore_details.failed_shards` | 整數 | 還原失敗的分片數量。
`indices.<index>.bootstrap_details.shard_restore_details.in_progress_shards` | 整數 | 目前正在還原的分片數量。

## 取得批次任務狀態
**於 3.7 版引入**
{: .label .label-purple }

傳回批次複寫任務的進度。使用任何批次複寫操作傳回的 `task_id` 來檢查任務狀態。將此請求傳送至追隨者叢集。

### 端點

```json
GET /_plugins/_replication/_task_status/{task_id}
```

### 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明 | 必要
:--- | :--- |:--- |:---
`task_id` | 字串 | 批次複寫操作傳回的任務 ID。 | 是

### 回應範例

```json
{
   "operation_type": "bulk_stop_replication",
   "pattern": "my-index-*",
   "start_time": 1717600000000,
   "num_success": 7,
   "num_failed": 1,
   "num_pending": 2,
   "num_cancelled": 0,
   "failed_indices": [
      {
         "index": "my-index-3",
         "failure_reason": "No replication in progress for index:my-index-3"
      }
   ]
}
```

### 回應本文欄位

下表列出回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`operation_type` | 字串 | 批次複寫操作的類型。可能的值為 `bulk_start_replication`、`bulk_stop_replication`、`bulk_pause_replication`、`bulk_resume_replication`。
`pattern` | 字串 | 此操作使用的索引模式。
`start_time` | 長整數 | 任務開始時的 Epoch 時間戳記（以毫秒為單位）。
`num_success` | 整數 | 操作成功完成的索引數量。
`num_failed` | 整數 | 操作失敗的索引數量。
`num_pending` | 整數 | 等待處理的索引數量。當此數量達到 `0` 時，任務即完成。
`num_cancelled` | 整數 | 因任務取消而未處理的索引數量。
`failed_indices` | 陣列 | 物件陣列，其中包含每個失敗索引的 `index` 名稱和 `failure_reason`。

## 取消批次任務
**於 3.7 版引入**
{: .label .label-purple }

取消正在執行的批次複寫任務。已處理的索引會維持此操作套用的狀態；其餘索引則會標記為已取消。將此請求傳送至追隨者叢集。

### 端點

```json
POST /_plugins/_replication/_task_cancel/{task_id}
```

### 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明 | 必要
:--- | :--- |:--- |:---
`task_id` | 字串 | 要取消的批次複寫操作的任務 ID。 | 是

## 設定

如需批次複寫設定，請參閱[批次複寫設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/settings/#bulk-replication-settings)。若要瞭解如何更新動態設定，請參閱[動態設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/#dynamic-settings)。

## 錯誤回應

下列範例顯示您在使用批次複寫 API 操作時可能遇到的常見錯誤回應。

### 批次任務已在執行中

如果您在另一個批次複寫操作已在進行時提交批次複寫操作，OpenSearch 會傳回 409 錯誤：

```json
{
   "error": {
      "root_cause": [
         {
            "type": "resource_already_exists_exception",
            "reason": "A bulk replication task is already running. Only one bulk task is allowed at a time."
         }
      ],
      "type": "resource_already_exists_exception",
      "reason": "A bulk replication task is already running. Only one bulk task is allowed at a time."
   },
   "status": 409
}
```

提交新任務之前，請等待目前的任務完成或將其[取消](#cancel-bulk-task)。

### 沒有索引符合模式

如果找不到符合指定模式的索引，OpenSearch 會傳回 404 錯誤：

```json
{
   "error": {
      "root_cause": [
         {
            "type": "resource_not_found_exception",
            "reason": "No indices found matching pattern: [non-existent-*] on leader cluster"
         }
      ],
      "type": "resource_not_found_exception",
      "reason": "No indices found matching pattern: [non-existent-*] on leader cluster"
   },
   "status": 404
}
```

### 缺少領導叢集別名

如果您在提交大量啟動複寫請求時未提供 `leader_alias`，OpenSearch 會傳回 400 錯誤：

```json
{
   "error": {
      "root_cause": [
         {
            "type": "action_request_validation_exception",
            "reason": "Validation Failed: 1: leader_alias is required for bulk start;"
         }
      ],
      "type": "action_request_validation_exception",
      "reason": "Validation Failed: 1: leader_alias is required for bulk start;"
   },
   "status": 400
}
```

### 所有索引驗證失敗

如果所有符合的索引都已處於操作所要求的狀態（例如，您對複寫已暫停的索引傳送暫停複寫操作），OpenSearch 會傳回 400 錯誤：

```json
{
   "error": {
      "root_cause": [
         {
            "type": "illegal_argument_exception",
            "reason": "Index bulk-test-1 is already paused; Index bulk-test-2 is already paused"
         }
      ],
      "type": "illegal_argument_exception",
      "reason": "Index bulk-test-1 is already paused; Index bulk-test-2 is already paused"
   },
   "status": 400
}
```

### 找不到工作

如果您嘗試取消或檢查不存在或已完成的工作，OpenSearch 會傳回 404 錯誤：

```json
{
   "error": {
      "root_cause": [
         {
            "type": "resource_not_found_exception",
            "reason": "Task a3PiBHTWTTulezYixxCwkw:7709 not found or already completed"
         }
      ],
      "type": "resource_not_found_exception",
      "reason": "Task a3PiBHTWTTulezYixxCwkw:7709 not found or already completed"
   },
   "status": 404
}
```


## 限制

請注意以下限制：

- Bulk Replication API 不會自動為失敗的索引重新執行操作。請手動重新執行大量複寫操作，或針對個別索引使用 [Replication API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/api/)。
- 大量複寫工作是暫時性的，不會在節點重新啟動後保存。由大量啟動複寫操作啟動的個別複寫工作則是持久的。