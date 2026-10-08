---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集配置說明"
nav_order: 10
parent: Cluster APIs
has_children: false
redirect_from:
 - /opensearch/rest-api/cluster-allocation/
---

# Cluster Allocation Explain API
**於 1.0 版導入**
{: .label .label-purple }

Cluster Allocation Explain API 提供叢集中分片配置的詳細說明。您可以使用此 API 來疑難排解並診斷分片配置問題。

此 API 在下列情境中特別有用：

- 瞭解為什麼某個分片仍未指派，且無法配置到任何節點。
- 判斷為什麼某個分片被配置到特定節點而非其他節點。
- 瞭解為什麼某個分片仍留在其目前的節點上，而未重新平衡到其他節點。
- 驗證配置設定與篩選器是否如預期運作。

在不帶請求本文的情況下呼叫時，此 API 會找出第一個未指派的分片，並說明為什麼無法配置該分片。在帶有特定分片資訊的情況下呼叫時，則會提供該特定分片的配置詳細資訊。


<!-- spec_insert_start
api: cluster.allocation_explain
component: endpoints
-->
## 端點
```json
GET  /_cluster/allocation/explain
POST /_cluster/allocation/explain
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: cluster.allocation_explain
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `include_disk_info` | 布林值 | 當設為 `true` 時，傳回磁碟使用量與分片大小的相關資訊。_(預設：`false`)_ |
| `include_yes_decisions` | 布林值 | 當設為 `true` 時，在配置說明中傳回任何 `YES` 決策。`YES` 決策表示針對指定節點的特定分片配置嘗試何時成功。_(預設：`false`)_ |

<!-- spec_insert_end -->

## 請求本文欄位

要產生說明的索引、分片與主要分片旗標。留空即可為第一個未指派的分片產生說明。

請求本文為選用。它是一個包含下列欄位的 JSON 物件。

| 屬性 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `current_node` | 字串 | 指定節點 ID 或節點名稱，以便僅說明目前位於指定節點上的分片。 |
| `index` | 字串 | 包含要產生說明之分片的索引名稱。 |
| `primary` | 布林值 | 當設為 `true` 時，根據節點 ID 傳回主要分片的路由說明。 |
| `shard` | 整數 | 指定您想要取得說明的分片 ID。 |

## 範例請求

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/allocation/explain?include_yes_decisions=true
body: |
{
  "index": "movies",
  "shard": 0,
  "primary": true
}
-->
{% capture step1_rest %}
GET /_cluster/allocation/explain?include_yes_decisions=true
{
  "index": "movies",
  "shard": 0,
  "primary": true
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.allocation_explain(
  params = { "include_yes_decisions": "true" },
  body =   {
    "index": "movies",
    "shard": 0,
    "primary": true
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例回應

下列回應顯示一個已指派的主要分片，以及叢集中其他節點的配置決策：

```json
{
  "index": "movies",
  "shard": 0,
  "primary": true,
  "current_state": "started",
  "current_node": {
    "id": "d8jRZcW1QmCBeVFlgOJx5A",
    "name": "opensearch-node1",
    "transport_address": "172.24.0.4:9300",
    "weight_ranking": 1
  },
  "can_remain_on_current_node": "yes",
  "can_rebalance_cluster": "yes",
  "can_rebalance_to_other_node": "no",
  "rebalance_explanation": "cannot rebalance as no target node exists that can both allocate this shard and improve the cluster balance",
  "node_allocation_decisions": [{
    "node_id": "vRxi4uPcRt2BtHlFoyCyTQ",
    "node_name": "opensearch-node2",
    "transport_address": "172.24.0.3:9300",
    "node_decision": "no",
    "weight_ranking": 1,
    "deciders": [{
        "decider": "max_retry",
        "decision": "YES",
        "explanation": "shard has no previous failures"
      },
      {
        "decider": "replica_after_primary_active",
        "decision": "YES",
        "explanation": "shard is primary and can be allocated"
      },
      {
        "decider": "enable",
        "decision": "YES",
        "explanation": "all allocations are allowed"
      },
      {
        "decider": "node_version",
        "decision": "YES",
        "explanation": "can relocate primary shard from a node with version [1.0.0] to a node with equal-or-newer version [1.0.0]"
      },
      {
        "decider": "snapshot_in_progress",
        "decision": "YES",
        "explanation": "no snapshots are currently running"
      },
      {
        "decider": "restore_in_progress",
        "decision": "YES",
        "explanation": "ignored as shard is not being recovered from a snapshot"
      },
      {
        "decider": "filter",
        "decision": "YES",
        "explanation": "node passes include/exclude/require filters"
      },
      {
        "decider": "same_shard",
        "decision": "NO",
        "explanation": "a copy of this shard is already allocated to this node [[movies][0], node[vRxi4uPcRt2BtHlFoyCyTQ], [R], s[STARTED], a[id=x8w7QxWdQQa188HKGn0iMQ]]"
      },
      {
        "decider": "disk_threshold",
        "decision": "YES",
        "explanation": "enough disk for shard on node, free: [35.9gb], shard size: [15.1kb], free after allocating shard: [35.9gb]"
      },
      {
        "decider": "throttling",
        "decision": "YES",
        "explanation": "below shard recovery limit of outgoing: [0 < 2] incoming: [0 < 2]"
      },
      {
        "decider": "shards_limit",
        "decision": "YES",
        "explanation": "total shard limits are disabled: [index: -1, cluster: -1] <= 0"
      },
      {
        "decider": "awareness",
        "decision": "YES",
        "explanation": "allocation awareness is not enabled, set cluster setting [cluster.routing.allocation.awareness.attributes] to enable it"
      }
    ]
  }]
}
```

## 範例：說明第一個未指派的分片

若要取得 OpenSearch 找到的第一個未指派分片的說明，請傳送空的請求本文：

<!-- spec_insert_start
component: example_code
rest: POST /_cluster/allocation/explain
body: {}
-->
{% capture step1_rest %}
POST /_cluster/allocation/explain
{}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.allocation_explain(
  body =   {}
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 範例回應

下列回應顯示單一節點叢集中一個未指派的副本分片：

```json
{
  "index" : "research_papers",
  "shard" : 0,
  "primary" : false,
  "current_state" : "unassigned",
  "unassigned_info" : {
    "reason" : "CLUSTER_RECOVERED",
    "at" : "2026-02-17T16:43:13.339Z",
    "last_allocation_status" : "no_attempt"
  },
  "can_allocate" : "no",
  "allocate_explanation" : "cannot allocate because allocation is not permitted to any of the nodes",
  "node_allocation_decisions" : [
    {
      "node_id" : "KfEEGG7_SsKZVFqI4ko2FA",
      "node_name" : "opensearch-node1",
      "transport_address" : "172.18.0.2:9300",
      "node_attributes" : {
        "shard_indexing_pressure_enabled" : "true"
      },
      "node_decision" : "no",
      "deciders" : [
        {
          "decider" : "same_shard",
          "decision" : "NO",
          "explanation" : "a copy of this shard is already allocated to this node [[research_papers][0], node[KfEEGG7_SsKZVFqI4ko2FA], [P], s[STARTED], a[id=SfxnuSLESQSI0Htcv0N3vA]]"
        }
      ]
    }
  ]
}
```

回應包含下列欄位：
- `current_state`：該分片為 `unassigned`。
- `unassigned_info.reason`：該分片在叢集復原期間變為未指派 (`CLUSTER_RECOVERED`)。
- `can_allocate`：設為 `no`，因為該分片無法配置到任何可用的節點。
- `node_decision`：針對叢集中唯一的節點設為 `no`。
- `decider`：`same_shard` 配置器阻止配置，因為主要分片已位於此節點上。

這是單一節點叢集中的典型情況，副本分片無法配置，因為 OpenSearch 不允許主要分片與其副本共存於同一節點上。

## 範例：說明特定已指派的分片

若要了解為何某個已指派的分片仍留在目前的節點上，請指定分片詳細資料：

<!-- spec_insert_start
component: example_code
rest: POST /_cluster/allocation/explain
body: |
{
  "index": "books",
  "shard": 0,
  "primary": true
}
-->
{% capture step1_rest %}
POST /_cluster/allocation/explain
{
  "index": "books",
  "shard": 0,
  "primary": true
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.allocation_explain(
  body =   {
    "index": "books",
    "shard": 0,
    "primary": true
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 範例回應

```json
{
  "index" : "books",
  "shard" : 0,
  "primary" : true,
  "current_state" : "started",
  "current_node" : {
    "id" : "KfEEGG7_SsKZVFqI4ko2FA",
    "name" : "opensearch-node1",
    "transport_address" : "172.18.0.2:9300",
    "attributes" : {
      "shard_indexing_pressure_enabled" : "true"
    },
    "weight_ranking" : 1
  },
  "can_remain_on_current_node" : "yes",
  "can_rebalance_cluster" : "no",
  "can_rebalance_cluster_decisions" : [
    {
      "decider" : "rebalance_only_when_active",
      "decision" : "NO",
      "explanation" : "rebalancing is not allowed until all replicas in the cluster are active"
    },
    {
      "decider" : "cluster_rebalance",
      "decision" : "NO",
      "explanation" : "the cluster has unassigned shards and cluster setting [cluster.routing.allocation.allow_rebalance] is set to [indices_all_active]"
    }
  ],
  "can_rebalance_to_other_node" : "no",
  "rebalance_explanation" : "rebalancing is not allowed"
}
```

回應包含下列欄位：
- `current_state`：此分片為 `started` 且運作正常。
- `current_node`：包含裝載此分片之節點的詳細資料。
- `can_remain_on_current_node`：設為 `yes`，因為允許此分片留在目前的節點上。
- `can_rebalance_cluster`：設為 `no`，因為叢集有未指派的分片時會停用重新平衡。
- `can_rebalance_cluster_decisions`：列出阻止重新平衡的決策器。

## 範例：包含磁碟資訊

使用 `include_disk_info` 參數取得詳細的磁碟使用量統計資料：

<!-- spec_insert_start
component: example_code
rest: POST /_cluster/allocation/explain?include_disk_info=true
body: |
{
  "index": "books",
  "shard": 0,
  "primary": true
}
-->
{% capture step1_rest %}
POST /_cluster/allocation/explain?include_disk_info=true
{
  "index": "books",
  "shard": 0,
  "primary": true
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.allocation_explain(
  params = { "include_disk_info": "true" },
  body =   {
    "index": "books",
    "shard": 0,
    "primary": true
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 範例回應

回應包含額外的 `cluster_info`，其中有磁碟使用量與分片大小詳細資料：

```json
{
  "index" : "books",
  "shard" : 0,
  "primary" : true,
  "current_state" : "started",
  "current_node" : {
    "id" : "KfEEGG7_SsKZVFqI4ko2FA",
    "name" : "opensearch-node1",
    "transport_address" : "172.18.0.2:9300",
    "attributes" : {
      "shard_indexing_pressure_enabled" : "true"
    },
    "weight_ranking" : 1
  },
  "cluster_info" : {
    "nodes" : {
      "KfEEGG7_SsKZVFqI4ko2FA" : {
        "node_name" : "opensearch-node1",
        "least_available" : {
          "path" : "/usr/share/opensearch/data/nodes/0",
          "total_bytes" : 62671097856,
          "used_bytes" : 14324834304,
          "free_bytes" : 48346263552,
          "free_disk_percent" : 77.1,
          "used_disk_percent" : 22.9
        },
        "most_available" : {
          "path" : "/usr/share/opensearch/data/nodes/0",
          "total_bytes" : 62671097856,
          "used_bytes" : 14324834304,
          "free_bytes" : 48346263552,
          "free_disk_percent" : 77.1,
          "used_disk_percent" : 22.9
        },
        "node_resource_usage_stats" : {
          "KfEEGG7_SsKZVFqI4ko2FA" : {
            "timestamp" : 1771438387501,
            "cpu_utilization_percent" : "0.5",
            "memory_utilization_percent" : "57.9",
            "io_usage_stats" : {
              "max_io_utilization_percent" : "0.0"
            }
          }
        }
      }
    },
    "shard_sizes" : {
      "[books][0][p]_bytes" : 5312,
      "[movies][0][p]_bytes" : 4862,
      "[research_papers][0][p]_bytes" : 7367
    },
    "shard_paths" : {
      "[books][0], node[KfEEGG7_SsKZVFqI4ko2FA], [P], s[STARTED], a[id=Vu7arTEfRrG9lnikaClzDg]" : "/usr/share/opensearch/data/nodes/0",
      "[movies][0], node[KfEEGG7_SsKZVFqI4ko2FA], [P], s[STARTED], a[id=f9QNud7NSACyM0YedYGfDg]" : "/usr/share/opensearch/data/nodes/0",
      "[research_papers][0], node[KfEEGG7_SsKZVFqI4ko2FA], [P], s[STARTED], a[id=SfxnuSLESQSI0Htcv0N3vA]" : "/usr/share/opensearch/data/nodes/0"
    },
    "reserved_sizes" : [ ]
  },
  "can_remain_on_current_node" : "yes",
  "can_rebalance_cluster" : "no",
  "can_rebalance_cluster_decisions" : [
    {
      "decider" : "rebalance_only_when_active",
      "decision" : "NO",
      "explanation" : "rebalancing is not allowed until all replicas in the cluster are active"
    },
    {
      "decider" : "cluster_rebalance",
      "decision" : "NO",
      "explanation" : "the cluster has unassigned shards and cluster setting [cluster.routing.allocation.allow_rebalance] is set to [indices_all_active]"
    }
  ],
  "can_rebalance_to_other_node" : "no",
  "rebalance_explanation" : "rebalancing is not allowed"
}
```

`cluster_info` 物件提供：
- `nodes`：每個節點的磁碟使用量統計資料，包括可用與已用磁碟空間百分比，以及資源使用率指標（CPU、記憶體與 I/O）。
- `shard_sizes`：叢集中每個分片的大小，以位元組為單位（回應顯示的是範例；實際回應會包含所有分片）。
- `shard_paths`：每個分片在節點上儲存的檔案系統路徑（回應顯示的是範例；實際回應會包含所有分片）。
- `reserved_sizes`：為進行中的分片作業保留的磁碟空間。

在診斷磁碟相關的配置問題，或了解磁碟空間如何影響配置決策時，這些資訊很有用。

## 範例：使用 current_node 指定節點

使用 `current_node` 參數，僅在分片位於特定節點時取得說明：

<!-- spec_insert_start
component: example_code
rest: POST /_cluster/allocation/explain
body: |
{
  "index": "books",
  "shard": 0,
  "primary": false,
  "current_node": "opensearch-node1"
}
-->
{% capture step1_rest %}
POST /_cluster/allocation/explain
{
  "index": "books",
  "shard": 0,
  "primary": false,
  "current_node": "opensearch-node1"
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.allocation_explain(
  body =   {
    "index": "books",
    "shard": 0,
    "primary": false,
    "current_node": "opensearch-node1"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

唯有當 `books` 索引的副本分片 0 目前位於 `opensearch-node1` 節點時，此查詢才會傳回說明。如果分片位於其他節點或未指派，API 會傳回錯誤。

## 回應欄位

此 API 會根據分片是否已指派而回傳不同的欄位。

### 常見回應欄位

下表列出常見的回應欄位。

欄位 | 說明
:--- | :---
`index` | 包含該分片的索引名稱。
`shard` | 索引內的分片 ID。
`primary` | 這是主要分片 (`true`) 還是副本分片 (`false`)。
`current_state` | 分片的目前狀態：`started`、`unassigned`、`initializing` 或 `relocating`。

### 已指派分片的欄位

下表列出已指派分片的回應欄位。

欄位 | 說明
:--- | :---
`current_node` | 分片目前所在節點的資訊，包括節點 ID、名稱、傳輸位址與自訂屬性。
`can_remain_on_current_node` | 分片是否允許留在其目前節點：`yes`、`no` 或 `decision_not_taken`。
`can_rebalance_cluster` | 叢集是否允許重新平衡：`yes`、`no` 或 `decision_not_taken`。
`can_rebalance_to_other_node` | 分片是否可以重新平衡到其他節點：`yes` 或 `no`。
`rebalance_explanation` | 重新平衡決策的人類可讀說明。
`can_remain_decisions` | 決定分片是否可留在目前節點的決策器陣列。僅在 `can_remain_on_current_node` 為 `no` 時才會包含。
`can_rebalance_cluster_decisions` | 決定是否允許叢集重新平衡的決策器陣列。僅在 `can_rebalance_cluster` 為 `no` 時才會包含。
`node_allocation_decisions` | 潛在目標節點的陣列，包含每個節點的指派決策。

### 未指派分片的欄位

下表列出未指派分片的回應欄位。

欄位 | 說明
:--- | :---
`unassigned_info` | 分片為何未指派的資訊，包括原因、時間戳記與最後一次指派嘗試。
`unassigned_info.reason` | 分片變成未指派的原因，例如 `INDEX_CREATED`、`CLUSTER_RECOVERED`、`NODE_LEFT` 或 `REPLICA_ADDED`。
`unassigned_info.at` | 分片變成未指派的時間戳記 (ISO 8601 格式)。
`unassigned_info.last_allocation_status` | 最後一次指派嘗試的結果：`no_attempt`、`no`、`throttled` 或 `no_valid_shard_copy`。
`unassigned_info.details` | 分片為何變成未指派的其他詳細資訊。僅在有其他詳細資訊可用時才會包含。
`can_allocate` | 分片是否可以指派：`yes`、`no`、`throttled`、`no_valid_shard_copy` 或 `allocation_delayed`。
`allocate_explanation` | 分片無法指派原因的人類可讀說明。
`configured_delay` | 指派分片前所設定的延遲。僅在 `can_allocate` 為 `allocation_delayed` 時才會包含。
`configured_delay_in_millis` | 以毫秒為單位的設定延遲。僅在 `can_allocate` 為 `allocation_delayed` 時才會包含。
`remaining_delay` | 分片可以指派前的剩餘時間。僅在 `can_allocate` 為 `allocation_delayed` 時才會包含。
`remaining_delay_in_millis` | 以毫秒為單位的剩餘延遲。僅在 `can_allocate` 為 `allocation_delayed` 時才會包含。
`node_allocation_decisions` | 節點的陣列，包含每個節點的指派決策。

### 節點指派決策欄位

下表列出節點指派決策陣列中的欄位。

欄位 | 說明
:--- | :---
`node_id` | 節點的唯一識別碼。
`node_name` | 節點的名稱。
`transport_address` | 節點的傳輸位址。
`node_attributes` | 指派給節點的自訂屬性，例如可用區域或執行個體類型。
`node_decision` | 此節點的指派決策：`yes`、`no`、`throttled`、`worse_balance` 或 `awaiting_info`。
`weight_ranking` | 此節點在指派決策中的相對權重排名。數值越低表示偏好越高。僅在為指派決策對節點進行排名時才會包含。
`deciders` | 決定是否將分片指派給此節點的配置器陣列。
`store` | 節點上找到的分片資料資訊 (適用於副本分片)。包含 `matching_size` 與 `matching_size_in_bytes`。僅在分片儲存資訊可用時才會包含。

### 決策器欄位

`deciders` 陣列中的每個決策器都包含下列欄位。

欄位 | 說明
:--- | :---
`decider` | 做出決策的配置器名稱。
`decision` | 配置器做出的決策：`YES`、`NO` 或 `THROTTLE`。
`explanation` | 配置器為何做出此決策的詳細說明，包括任何相關的設定或限制。

## 常見配置器

下表列出影響分片指派決策的常見配置器。

配置器 | 說明
:--- | :---
`same_shard` | 防止主要分片與其副本被指派到同一個節點。
`disk_threshold` | 根據低水位與高水位閾值，檢查節點是否有足夠的磁碟空間容納該分片。
`filter` | 根據索引設定 (例如 `index.routing.allocation.include`、`exclude` 或 `require`) 套用指派篩選器。
`awareness` | 根據節點屬性強制執行分片指派感知，將分片分散到可用區域或機架。
`enable` | 使用 `cluster.routing.allocation.enable` 設定，檢查叢集、索引或分片層級是否啟用分片指派。
`throttling` | 根據 `cluster.routing.allocation.node_concurrent_recoveries` 限制並行分片復原的數量。
`shards_limit` | 強制執行每個節點 (`cluster.routing.allocation.total_shards_per_node`) 或每個索引的最大分片數量。
`max_retry` | 防止對已多次指派失敗的分片重複進行指派嘗試。
`node_version` | 確保分片只指派給具有相容 OpenSearch 版本的節點，防止版本降級。
`snapshot_in_progress` | 當該分片的快照作業正在進行時，防止分片指派。
`restore_in_progress` | 控制從快照還原分片期間的指派。
`rebalance_only_when_active` | 當並非所有分片複本 (主要與副本) 都在叢集中處於作用中狀態時，防止重新平衡。
`cluster_rebalance` | 根據 `cluster.routing.allocation.allow_rebalance` 設定控制何時允許叢集重新平衡：`always`、`indices_primaries_active` 或 `indices_all_active`。
`replica_after_primary_active` | 確保副本分片只在其主要分片處於作用中狀態後才被指派。

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`cluster:monitor/allocation/explain`。
