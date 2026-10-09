---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "跨叢集複寫 API"
nav_order: 50
parent: Cross-cluster replication
redirect_from:
  - /replication-plugin/api/
---

# 跨叢集複寫 API

使用這些複寫操作以程式化方式管理跨叢集複寫。

<details markdown="block">
  <summary>
    目錄
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

## 開始複寫
**於 1.1 版推出**
{: .label .label-purple }

從領導叢集起始將索引複寫至跟隨叢集。將此請求傳送至跟隨叢集。


### 端點

```json
PUT /_plugins/_replication/{follower-index}/_start
```

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `leader_alias` | 字串 | 跨叢集連線的名稱。您在[設定跨叢集連線]({{site.url}}{{site.baseurl}}/replication-plugin/get-started/#set-up-a-cross-cluster-connection)時定義此別名。 | 是 |
| `leader_index` | 字串 | 您要複寫的領導叢集上的索引。 | 是 |
| `use_roles` | 物件 | 用於索引之間所有後續後端複寫工作的角色。指定 `leader_cluster_role` 與 `follower_cluster_role`。請參閱[對應領導與跟隨叢集角色]({{site.url}}{{site.baseurl}}/replication-plugin/permissions/#map-the-leader-and-follower-cluster-roles)。 | 若已啟用 Security 外掛程式 |

### 範例請求

```json
PUT /_plugins/_replication/follower-01/_start
{
   "leader_alias": "my-connection-alias",
   "leader_index": "leader-01",
   "use_roles": {
      "leader_cluster_role": "cross_cluster_replication_leader_full_access",
      "follower_cluster_role": "cross_cluster_replication_follower_full_access"
   }
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
   "acknowledged": true
}
```

## 停止複寫
**於 1.1 版推出**
{: .label .label-purple }

終止複寫並將跟隨索引轉換為標準索引。將此請求傳送至跟隨叢集。

### 端點

```json
POST /_plugins/_replication/{follower-index}/_stop
```

### 範例請求

```json
POST /_plugins/_replication/follower-01/_stop
{}
```
{% include copy-curl.html %}

### 範例回應

```json
{
   "acknowledged": true
}
```

## 暫停複寫
**於 1.1 版推出**
{: .label .label-purple }

暫停領導索引的複寫。將此請求傳送至跟隨叢集。

### 端點

```json
POST /_plugins/_replication/{follower-index}/_pause
```

### 範例請求

```json
POST /_plugins/_replication/follower-01/_pause
{}
```
{% include copy-curl.html %}

若暫停時間超過保留租約期間，您將無法繼續複寫。若要復原，請使用 [force-resume]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/force-resume/)，其會從領導叢集的快照還原跟隨索引。

### 範例回應

```json
{
   "acknowledged": true
}
```

## 繼續複寫
**於 1.1 版推出**
{: .label .label-purple }

繼續領導索引的複寫。將此請求傳送至跟隨叢集。

### 端點

```json
POST /_plugins/_replication/{follower-index}/_resume
```

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `force_resume` | 布林值 | 設為 `true` 時，會執行停止-刪除-開始循環，以在保留租約過期時從領導叢集還原跟隨索引。當複寫已暫停超過 12 小時且一般繼續複寫失敗時，請使用此項。如需更多資訊，請參閱[強制繼續複寫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/force-resume/)。預設為 `false`。 | 否 |

### 範例請求

```json
POST /_plugins/_replication/follower-01/_resume
{}
```
{% include copy-curl.html %}

### 範例回應

```json
{
   "acknowledged": true
}
```

### 錯誤回應

下表說明繼續複寫操作常見的錯誤回應。

| 狀態碼 | 錯誤 | 說明 |
| :--- | :--- | :--- |
| 404 | `Retention lease doesn't exist. Use force_resume=true to restore from snapshot.` | 保留租約已過期，且 `force_resume` 未設為 `true`。請以 `"force_resume": true` 重試請求。 |
| 400 | Replication is not in PAUSED state | 強制繼續複寫僅能在複寫暫停時使用。請先檢查複寫狀態。 |
| 500 | Failed to stop replication | 內部停止操作失敗。請確認叢集健康狀態並重試。 |
| 500 | Failed to delete follower index | 停止複寫後無法刪除跟隨索引。可能需要手動清理。 |
| 500 | Failed to start replication | 刪除跟隨索引後，內部開始操作失敗。您可能需要再次手動開始複寫。 |

## 取得複寫狀態
**於 1.1 版推出**
{: .label .label-purple }

取得索引複寫的狀態。可能的狀態為 `SYNCING`、`BOOTSTRAPING`、`PAUSED` 及 `REPLICATION NOT IN PROGRESS`。使用同步詳細資料來衡量複寫延遲。將此請求傳送至跟隨叢集。

### 端點

```json
GET /_plugins/_replication/{follower-index}/_status
```

### 範例請求

```json
GET /_plugins/_replication/follower-01/_status
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "status" : "SYNCING",
  "reason" : "User initiated",
  "leader_alias" : "my-connection-name",
  "leader_index" : "leader-01",
  "follower_index" : "follower-01",
  "syncing_details" : {
    "leader_checkpoint" : 19,
    "follower_checkpoint" : 19,
    "seq_no" : 0
  }
}
```
若要在回應中包含分片複寫詳細資料，請新增 `&verbose=true` 參數。

領導與跟隨檢查點值一開始為負整數，並反映分片數量（一個分片為 -1，五個分片為 -5，依此類推）。每次進行變更時，這些值會遞增至正整數。例如，當您在領導索引上進行變更時，`leader_checkpoint` 會變成 `0`。`follower_checkpoint` 一開始仍為 `-1`，直到跟隨索引從領導叢集提取該變更，此時它會遞增至 `0`。若這些值相同，表示索引已完全同步。

## 取得領導叢集統計資料
**於 1.1 版推出**
{: .label .label-purple }

取得指定叢集上已複寫領導索引的相關資訊。

### 端點

```json
GET /_plugins/_replication/leader_stats
```

### 範例請求

```json
GET /_plugins/_replication/leader_stats
```
{% include copy-curl.html %}

### 範例回應

```json
{
   "num_replicated_indices": 2,
   "operations_read": 15,
   "translog_size_bytes": 1355,
   "operations_read_lucene": 0,
   "operations_read_translog": 15,
   "total_read_time_lucene_millis": 0,
   "total_read_time_translog_millis": 659,
   "bytes_read": 1000,
   "index_stats":{
      "leader-index-1":{
         "operations_read": 7,
         "translog_size_bytes": 639,
         "operations_read_lucene": 0,
         "operations_read_translog": 7,
         "total_read_time_lucene_millis": 0,
         "total_read_time_translog_millis": 353,
         "bytes_read":466
      },
      "leader-index-2":{
         "operations_read": 8,
         "translog_size_bytes": 716,
         "operations_read_lucene": 0,
         "operations_read_translog": 8,
         "total_read_time_lucene_millis": 0,
         "total_read_time_translog_millis": 306,
         "bytes_read": 534
      }
   }
}
```

## 取得跟隨叢集統計資料
**於 1.1 版推出**
{: .label .label-purple }

取得指定叢集上跟隨 (同步中) 索引的相關資訊。

### 端點

```json
GET /_plugins/_replication/follower_stats
```

### 範例請求

```json
GET /_plugins/_replication/follower_stats
```
{% include copy-curl.html %}

### 範例回應

```json
{
   "num_syncing_indices": 2,
   "num_bootstrapping_indices": 0,
   "num_paused_indices": 0,
   "num_failed_indices": 0,
   "num_shard_tasks": 2,
   "num_index_tasks": 2,
   "operations_written": 3,
   "operations_read": 3,
   "failed_read_requests": 0,
   "throttled_read_requests": 0,
   "failed_write_requests": 0,
   "throttled_write_requests": 0,
   "follower_checkpoint": 1,
   "leader_checkpoint": 1,
   "total_write_time_millis": 2290,
   "index_stats":{
      "follower-index-1":{
         "operations_written": 2,
         "operations_read": 2,
         "failed_read_requests": 0,
         "throttled_read_requests": 0,
         "failed_write_requests": 0,
         "throttled_write_requests": 0,
         "follower_checkpoint": 1,
         "leader_checkpoint": 1,
         "total_write_time_millis": 1355
      },
      "follower-index-2":{
         "operations_written": 1,
         "operations_read": 1,
         "failed_read_requests": 0,
         "throttled_read_requests": 0,
         "failed_write_requests": 0,
         "throttled_write_requests": 0,
         "follower_checkpoint": 0,
         "leader_checkpoint": 0,
         "total_write_time_millis": 935
      }
   }
}
```

## 取得 auto-follow 統計資料
**於 1.1 版推出**
{: .label .label-purple }

取得 auto-follow 活動以及指定叢集上所設定之任何複寫規則的相關資訊。

### 端點

```json
GET /_plugins/_replication/autofollow_stats
```

### 範例請求

```json
GET /_plugins/_replication/autofollow_stats
```
{% include copy-curl.html %}

### 範例回應

```json
{
   "num_success_start_replication": 2,
   "num_failed_start_replication": 0,
   "num_failed_leader_calls": 0,
   "failed_indices":[
      
   ],
   "autofollow_stats":[
      {
         "name":"my-replication-rule",
         "pattern":"movies*",
         "num_success_start_replication": 2,
         "num_failed_start_replication": 0,
         "num_failed_leader_calls": 0,
         "failed_indices":[
            
         ]
      }
   ]
}
```

## 更新設定
**於 1.1 版推出**
{: .label .label-purple }

更新跟隨索引上的設定。

### 端點

```json
PUT /_plugins/_replication/{follower-index}/_update
```

### 範例請求

```json
PUT /_plugins/_replication/follower-01/_update
{
   "settings": {
      "index.number_of_shards": 4,
      "index.number_of_replicas": 2
   }
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
   "acknowledged": true
}
```

## 建立複寫規則
**於 1.1 版推出**
{: .label .label-purple }

自動對符合指定模式的索引開始複寫。如果領導叢集上的新索引符合該模式，OpenSearch 會自動建立跟隨索引並開始複寫。您也可以使用此 API 更新現有的複寫規則。

將此請求傳送至跟隨叢集。

建立所有 auto-follow 模式後，請務必記下其名稱。複寫外掛程式目前並未包含可擷取現有模式清單的 API 操作。
{: .tip }

### 端點

```json
POST /_plugins/_replication/_autofollow
```

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `leader_alias` | 字串 | 跨叢集連線的名稱。您可以在[設定跨叢集連線]({{site.url}}{{site.baseurl}}/replication-plugin/get-started/#set-up-a-cross-cluster-connection)時定義此別名。 | 是 |
| `name` | 字串 | auto-follow 模式的名稱。 | 是 |
| `pattern` | 字串 | 要與指定領導叢集中索引比對的索引模式陣列。支援萬用字元。例如 `leader-*`。 | 是 |
| `follower_index_pattern` | 字串 | 跟隨索引名稱的模式。使用 `{% raw %}{{leader_index}}{% endraw %}` 預留位置來包含領導索引名稱。例如，`{% raw %}{{leader_index}}{% endraw %}-replica` 會建立名為 `<leader_index_name>-replica` 的跟隨索引。當跟隨叢集上已存在同名索引，或從多個領導叢集複寫索引時，請使用此欄位以避免名稱衝突。若省略，跟隨索引會使用與領導索引相同的名稱。 | 否 |
| `use_roles` | 物件 | 索引之間所有後續後端複寫工作要使用的角色。請指定 `leader_cluster_role` 和 `follower_cluster_role`。請參閱[對應領導與跟隨叢集角色]({{site.url}}{{site.baseurl}}/replication-plugin/permissions/#map-the-leader-and-follower-cluster-roles)。 | 若已啟用 Security 外掛程式 |

### 範例請求

```json
POST /_plugins/_replication/_autofollow
{
   "leader_alias": "my-connection-alias",
   "name": "my-replication-rule",
   "pattern": "leader-*",
   "follower_index_pattern": "{% raw %}{{leader_index}}{% endraw %}-replica",
   "use_roles": {
      "leader_cluster_role": "cross_cluster_replication_leader_full_access",
      "follower_cluster_role": "cross_cluster_replication_follower_full_access"
   }
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
   "acknowledged": true
}
```

## 刪除複寫規則
**於 1.1 版推出**
{: .label .label-purple }

刪除指定的複寫規則。此操作會防止任何新索引被複寫，但不會停止該規則已啟動的現有複寫。在您停止複寫之前，已複寫的索引會保持唯讀。

將此請求傳送至跟隨叢集。

### 端點

```json
DELETE /_plugins/_replication/_autofollow
```

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `leader_alias` | 字串 | 跨叢集連線的名稱。您可以在[設定跨叢集連線]({{site.url}}{{site.baseurl}}/replication-plugin/get-started/#set-up-a-cross-cluster-connection)時定義此別名。 | 是 |
| `name` | 字串 | 模式的名稱。 | 是 |

### 範例請求

```json
DELETE /_plugins/_replication/_autofollow
{
   "leader_alias": "my-connection-alias",
   "name": "my-replication-rule"
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
   "acknowledged": true
}
```
