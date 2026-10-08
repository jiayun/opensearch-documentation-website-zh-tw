---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集重新路由"
nav_order: 47
parent: Cluster APIs
has_children: false
---

# 叢集重新路由 API
**於 1.0 版推出**
{: .label .label-purple }

`/_cluster/reroute` API 可讓您手動控制叢集中個別分片的配置。這包括移動、配置或取消分片配置。此 API 通常用於進階情境，例如手動復原或自訂負載平衡。

分片移動會受到叢集配置決策器的限制。在正式環境中套用重新路由命令之前，請務必先使用 `dry_run=true` 進行測試。使用 `explain=true` 參數可取得配置決策的詳細資訊，有助於了解為何特定重新路由請求會被允許或不被允許。如果分片配置因先前的問題或叢集不穩定而失敗，您可以使用 `retry_failed=true` 參數重新嘗試配置。

如需分片分配與叢集健康狀態的詳細資訊，請參閱[叢集健康狀態]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/)和[叢集配置說明]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-allocation/)。

## 端點

```json
POST /_cluster/reroute
```

## 查詢參數

| 參數        | 資料類型 | 說明                                                                                        |
| ---------------- | --------- | -------------------------------------------------------------------------------------------------- |
| `dry_run` | 布林值 | 若為 `true`，則驗證並模擬重新路由請求，但不實際套用。預設為 `false`。    |
| `explain` | 布林值 | 若為 `true`，則傳回命令被接受或拒絕的原因說明。預設為 `false`。 |
| `retry_failed` | 布林值 | 若為 `true`，則重試先前失敗的分片配置。預設為 `false`。                |
| `metric` | 字串 | 限制傳回的中繼資料。如需可用選項的清單，請參閱[指標選項](#metric-options)。預設為 `_all`。 |
| `cluster_manager_timeout` | 時間 | 連線至叢集管理員節點的逾時時間。預設為 `30s`。                              |
| `timeout` | 時間 | 整體請求逾時時間。預設為 `30s`。                                                         |

### 指標選項

`metric` 參數會篩選 Reroute API 所傳回的叢集狀態值。這有助於縮減回應大小，或檢查叢集狀態的特定部分。此參數支援下列值：

- `_all` _(預設)_：傳回所有可用的叢集狀態區段。 
- `blocks`：包含叢集中讀取層級與寫入層級區塊的相關資訊。
- `cluster_manager_node`：顯示目前哪個節點擔任叢集管理員。
- `metadata`：傳回索引設定、對應與別名。若指定特定索引，則只會傳回其中繼資料。
- `nodes`：包含叢集中的所有節點及其中繼資料。
- `routing_table`：傳回所有分片與副本的路由資訊。
- `version`：顯示叢集狀態版本號碼。

您可以將多個值組合成以逗號分隔的清單，例如 `metric=metadata,nodes,routing_table`。

## 請求本文欄位

請求本文中的 `commands` 陣列會定義要套用至分片配置的動作。它支援下列動作。

### 移動分片

`move` 命令會將已啟動的分片 (主要或副本) 從一個節點移動到另一個節點。這可用於平衡負載，或在維護前清空節點。分片必須處於 `STARTED` 狀態。主要分片與副本分片皆可使用此命令移動。 

`move` 命令需要下列參數：

* `index`：索引的名稱。
* `shard`：分片編號。
* `from_node`：要從中移動分片的節點名稱。
* `to_node`：要將分片移動到的節點名稱。

### 取消分片配置

`cancel` 命令會取消分片的配置 (包括復原)。此命令會取消現有配置並讓系統重新初始化，藉此強制重新同步。根據預設，可以取消副本分片配置，但取消主要分片配置需要 `allow_primary=true`，以避免意外造成資料中斷。

`cancel` 命令需要下列參數：

* `index`：索引的名稱。
* `shard`：分片編號。
* `node`：要執行此動作的節點名稱或節點 ID。
* `allow_primary` _(選用)_：若為 `true`，則允許取消主要分片配置。預設為 `false`。

### 配置副本分片

`allocate_replica` 命令會將未配置的副本指派給指定的節點。此操作會遵循配置決策器。當自動配置失敗時，可使用此命令手動觸發副本配置。

`allocate_replica` 命令需要下列參數：

* `index`：索引的名稱。
* `shard`：分片編號。
* `node`：要執行此動作的節點名稱或節點 ID。

### 配置過期的主要分片

`allocate_stale_primary` 命令會強制將主要分片配置到持有過期副本的節點。 

使用此命令時應極度謹慎。它會略過安全檢查，並可能導致**資料遺失**，尤其是在另一個暫時離線的節點上存在較新的分片副本時。如果該節點之後重新加入叢集，其資料將會被刪除，或被強制提升的過期副本取代。
{: .warning}

請僅在沒有最新副本可用，且您無法還原原始資料時，才使用此命令。
{: .tip}

`allocate_stale_primary` 命令需要下列參數：

* `index`：索引的名稱。
* `shard`：分片編號。
* `node`：要執行此動作的節點名稱或節點 ID。
* `accept_data_loss`：必須設為 `true`。

### 配置空白主要分片

`allocate_empty_primary` 命令會強制將新的空白主要分片配置到節點。此操作會初始化新的主要分片，且不含任何現有資料。 

該分片先前所有的資料將會**永久遺失**。如果之後有具備該分片有效資料的節點重新加入叢集，其副本將會被清除。此命令適用於災難復原，且**不存在任何有效的分片副本**，也無法從備份或快照復原時。
{: .warning}

`allocate_empty_primary` 命令需要下列參數：

* `index`：索引的名稱。
* `shard`：分片編號。
* `node` ：要執行此動作的節點名稱或節點 ID。
* `accept_data_loss`：必須設為 `true`。

## 範例

以下是使用叢集重新路由 API 的範例。

### 移動分片

建立範例索引：

```json
PUT /test-cluster-index
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  }
}
```
{% include copy-curl.html %}

執行下列重新路由命令，將索引 `test-cluster-index` 的分片 `0` 從節點 `node1` 移動到節點 `node2`：

<!-- spec_insert_start
component: example_code
rest: POST /_cluster/reroute
body: |
{
  "commands": [
    {
      "move": {
        "index": "test-cluster-index",
        "shard": 0,
        "from_node": "node1",
        "to_node": "node2"
      }
    }
  ]
}
-->
{% capture step1_rest %}
POST /_cluster/reroute
{
  "commands": [
    {
      "move": {
        "index": "test-cluster-index",
        "shard": 0,
        "from_node": "node1",
        "to_node": "node2"
      }
    }
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.reroute(
  body =   {
    "commands": [
      {
        "move": {
          "index": "test-cluster-index",
          "shard": 0,
          "from_node": "node1",
          "to_node": "node2"
        }
      }
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 模擬重新路由

若要在不執行的情況下模擬重新路由，請設定 `dry_run=true`：

<!-- spec_insert_start
component: example_code
rest: POST /_cluster/reroute?dry_run=true
body: |
{
  "commands": [
    {
      "move": {
        "index": "test-cluster-index",
        "shard": 0,
        "from_node": "node1",
        "to_node": "node2"
      }
    }
  ]
}
-->
{% capture step1_rest %}
POST /_cluster/reroute?dry_run=true
{
  "commands": [
    {
      "move": {
        "index": "test-cluster-index",
        "shard": 0,
        "from_node": "node1",
        "to_node": "node2"
      }
    }
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.reroute(
  params = { "dry_run": "true" },
  body =   {
    "commands": [
      {
        "move": {
          "index": "test-cluster-index",
          "shard": 0,
          "from_node": "node1",
          "to_node": "node2"
        }
      }
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 重試失敗的分配

如果某些分片因先前的問題而分配失敗，您可以重新嘗試分配：

<!-- spec_insert_start
component: example_code
rest: POST /_cluster/reroute?retry_failed=true
-->
{% capture step1_rest %}
POST /_cluster/reroute?retry_failed=true
{% endcapture %}

{% capture step1_python %}


response = client.cluster.reroute(
  params = { "retry_failed": "true" },
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 說明重新路由決策

若要了解重新路由命令被接受或拒絕的原因，請加入 `explain=true`：

<!-- spec_insert_start
component: example_code
rest: POST /_cluster/reroute?explain=true
body: |
{
  "commands": [
    {
      "move": {
        "index": "test-cluster-index",
        "shard": 0,
        "from_node": "node1",
        "to_node": "node2"
      }
    }
  ]
}
-->
{% capture step1_rest %}
POST /_cluster/reroute?explain=true
{
  "commands": [
    {
      "move": {
        "index": "test-cluster-index",
        "shard": 0,
        "from_node": "node1",
        "to_node": "node2"
      }
    }
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.reroute(
  params = { "explain": "true" },
  body =   {
    "commands": [
      {
        "move": {
          "index": "test-cluster-index",
          "shard": 0,
          "from_node": "node1",
          "to_node": "node2"
        }
      }
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

這會傳回一個 `decisions` 陣列，說明結果：

```json
"decisions": [
        {
          "decider": "max_retry",
          "decision": "YES",
          "explanation": "shard has no previous failures"
        },
        {
          "decider": "replica_after_primary_active",
          "decision": "YES",
          "explanation": "shard is primary and can be allocated"
        },
        ...
        {
          "decider": "remote_store_migration",
          "decision": "YES",
          "explanation": "[none migration_direction]: primary shard copy can be relocated to a non-remote node for strict compatibility mode"
        }
      ]
```

## 回應本文欄位

回應包含叢集狀態的中繼資料；若使用 `explain=true`，也可能包含 `decisions` 陣列。

| 欄位                        | 資料類型 | 說明                                                             |
| ---------------------------- | --------- | ----------------------------------------------------------------------- |
| `acknowledged` | 布林值 | 表示重新路由請求是否已被確認。                           |
| `state.cluster_uuid` | 字串 | 叢集的唯一識別碼。                                       |
| `state.version` | 整數 | 叢集狀態的版本。                                           |
| `state.state_uuid` | 字串 | 此特定狀態版本的 UUID。                                   |
| `state.master_node` | 字串 | 與 `cluster_manager_node` 相同，此欄位是為了向後相容而保留。                                 |
| `state.cluster_manager_node` | 字串 | 當選叢集管理員節點的 ID。  |
| `state.blocks` | 物件 | 任何全域或索引層級的叢集封鎖。                               |
| `state.nodes` | 物件 | 叢集節點的中繼資料，包括其名稱與位址。                      |
| `state.routing_table` | 物件 | 每個索引的分片路由資訊。                               |
| `state.routing_nodes` | 物件 | 依節點組織的分片分配。                                     |
| `commands` | 清單 | 已處理的重新路由命令清單。                                   |
| `explanations` | 清單 | 若為 `explain=true`，則包含結果的詳細說明。          |

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/reroute`。
