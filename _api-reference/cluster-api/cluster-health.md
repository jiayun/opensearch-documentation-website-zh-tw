---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集健康狀態"
nav_order: 40
parent: Cluster APIs
has_children: false
redirect_from: 
 - /api-reference/cluster-health/
 - /opensearch/rest-api/cluster-health/
---

# Cluster Health API
**於 1.0 版推出**
{: .label .label-purple }

叢集健康狀態 API 可讓您快速掌握叢集的運作狀態。OpenSearch 使用三種顏色表示叢集健康狀態，這些顏色代表分片的配置狀態：

- **綠色**（最佳）：所有主要分片及其副本都已配置到節點。叢集可完整運作。
- **黃色**：所有主要分片都已配置，但部分副本分片尚未指派。叢集可以運作，但尚未具備完整的備援能力。
- **紅色**（最差）：至少有一個主要分片尚未指派。部分資料無法使用，搜尋請求可能傳回不完整的結果。

判定整體健康狀態時，以最差的狀態為準：如果您請求多個索引的健康狀態，整體狀態會由最差的索引狀態決定。同樣地，索引的狀態會由其最差的分片狀態決定。

<!-- spec_insert_start
api: cluster.health
component: endpoints
-->
## 端點
```json
GET /_cluster/health
GET /_cluster/health/{index}
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: cluster.health
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | 清單或字串 | 以逗號分隔的資料串流、索引和別名清單，用於限制請求範圍。支援萬用字元（`*`）。若要指定所有資料串流和索引，請省略此參數，或使用 `*` 或 `_all`。 |

<!-- spec_insert_end -->

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `awareness_attribute` | 字串 | 要傳回其叢集健康狀態的感知屬性名稱（例如 `zone`）。僅在 `level` 設為 `awareness_attributes` 時適用。 | N/A |
| `cluster_manager_timeout` | 字串 | 等待叢集管理員節點回應的時間長度。如需支援的時間單位詳細資訊，請參閱[通用參數]({{site.url}}{{site.baseurl}}/api-reference/units/#time-units)。 | N/A |
| `expand_wildcards` | 清單或字串 | 指定萬用字元運算式可以比對的索引類型。支援以逗號分隔的值。<br> 有效值如下：<br> - `all`：比對任何索引，包括隱藏索引。<br> - `closed`：比對已關閉且非隱藏的索引。<br> - `hidden`：比對隱藏索引。必須與 `open`、`closed` 或兩者搭配使用。<br> - `none`：不接受萬用字元運算式。<br> - `open`：比對已開啟且非隱藏的索引。 | `open` |
| `level` | 字串 | 控制叢集健康狀態回應中包含的詳細資訊量。<br> 有效值如下：`awareness_attributes`、`cluster`、`indices` 和 `shards`。 | `cluster` |
| `local` | 布林值 | 是否僅從本機節點傳回資訊，而非從叢集管理員節點傳回。 | `false` |
| `timeout` | 字串 | 等待叢集管理員節點回應的時間長度。如需支援的時間單位詳細資訊，請參閱[通用參數]({{site.url}}{{site.baseurl}}/api-reference/units/#time-units)。 | N/A |
| `wait_for_active_shards` | 整數或字串或 NULL 或字串 | 等待指定數量的分片處於作用中狀態後，才傳回回應。使用 `all` 可指定所有分片。<br> 有效值如下：<br> - `all`：等待所有分片處於作用中狀態。 | `0` |
| `wait_for_events` | 字串 | 等待目前佇列中具有指定優先順序的所有事件處理完畢。<br> 有效值如下：<br> - `immediate`：最高優先順序，盡快處理。<br> - `urgent`：非常高的優先順序，在 immediate 事件之後處理。<br> - `high`：高優先順序，在 urgent 事件之後處理。<br> - `normal`：預設優先順序，在高優先順序事件之後處理。<br> - `low`：低優先順序，在 normal 事件之後處理。<br> - `languid`：最低優先順序，在所有其他事件之後處理。 | N/A |
| `wait_for_no_initializing_shards` | 布林值 | 是否等待叢集中沒有正在初始化的分片。 | `false` |
| `wait_for_no_relocating_shards` | 布林值 | 是否等待叢集中沒有正在重新配置的分片。 | `false` |
| `wait_for_nodes` | 整數或字串 | 等待指定數量的節點（`N`）可用。接受 `>=N`、`<=N`、`>N` 和 `<N`。您也可以使用 `ge(N)`、`le(N)`、`gt(N)` 和 `lt(N)` 表示法。 | N/A |
| `wait_for_status` | 字串 | 等待叢集健康狀態達到指定狀態或更佳狀態。<br> 有效值如下：`green`、`GREEN`、`yellow`、`YELLOW`、`red` 和 `RED`。 | N/A |
| `weights` | JSON 物件 | 在 PUT 請求的請求本文中，為屬性指派權重。權重可以設為任意比例，例如 2:3:5。若三個區域的比例為 2:3:5，則每傳送 100 個請求到叢集，各區域會以隨機順序分別收到 20、30 或 50 個搜尋請求。當指派的權重為 `0` 時，該區域不會收到任何搜尋流量。 | N/A |

<!-- spec_insert_end -->

## 請求範例：擷取所有索引的叢集健康狀態

下列請求會擷取叢集中所有索引的叢集健康狀態：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/health
-->
{% capture step1_rest %}
GET /_cluster/health
{% endcapture %}

{% capture step1_python %}

response = client.cluster.health()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

回應包含叢集健康狀態資訊：

```json
{
  "cluster_name" : "opensearch-cluster",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "discovered_master" : true,
  "discovered_cluster_manager" : true,
  "active_primary_shards" : 138,
  "active_shards" : 138,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 110,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 55.64516129032258
}
```

回應顯示 `yellow` 狀態，因為這是單一節點叢集，其副本分片無法配置。`timed_out` 欄位為 `false`，表示回應已在預設逾時期間內傳回。

## 請求範例：等待特定健康狀態

下列請求會等待 50 秒，讓叢集達到黃色或更佳狀態：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/health?wait_for_status=yellow&timeout=50s
-->
{% capture step1_rest %}
GET /_cluster/health?wait_for_status=yellow&timeout=50s
{% endcapture %}

{% capture step1_python %}


response = client.cluster.health(
  params = { "wait_for_status": "yellow", "timeout": "50s" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

如果叢集健康狀態在 50 秒內變成黃色或綠色，請求會立即傳回回應。否則，一旦超過逾時時間，就會傳回回應。

## 範例請求：依感知屬性擷取叢集健康狀態

若要依感知屬性（例如區域或機架）檢查叢集健康狀態，請在 `level` 查詢參數中指定 `awareness_attributes`：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/health?level=awareness_attributes
-->
{% capture step1_rest %}
GET /_cluster/health?level=awareness_attributes
{% endcapture %}

{% capture step1_python %}


response = client.cluster.health(
  params = { "level": "awareness_attributes" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含依感知屬性劃分的叢集健康狀態指標：

```json
{
  "cluster_name": "runTask",
  "status": "green",
  "timed_out": false,
  "number_of_nodes": 3,
  "number_of_data_nodes": 3,
  "discovered_master": true,
  "discovered_cluster_manager": true,
  "active_primary_shards": 0,
  "active_shards": 0,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 0,
  "delayed_unassigned_shards": 0,
  "number_of_pending_tasks": 0,
  "number_of_in_flight_fetch": 0,
  "task_max_waiting_in_queue_millis": 0,
  "active_shards_percent_as_number": 100,
  "awareness_attributes": {
    "zone": {
      "zone-3": {
        "active_shards": 0,
        "initializing_shards": 0,
        "relocating_shards": 0,
        "unassigned_shards": 0,
        "data_nodes": 1,
        "weight": 1
      },
      "zone-1": {
        "active_shards": 0,
        "initializing_shards": 0,
        "relocating_shards": 0,
        "unassigned_shards": 0,
        "data_nodes": 1,
        "weight": 1
      },
      "zone-2": {
        "active_shards": 0,
        "initializing_shards": 0,
        "relocating_shards": 0,
        "unassigned_shards": 0,
        "data_nodes": 1,
        "weight": 1
      }
    },
    "rack": {
      "rack-3": {
        "active_shards": 0,
        "initializing_shards": 0,
        "relocating_shards": 0,
        "unassigned_shards": 0,
        "data_nodes": 1,
        "weight": 1
      },
      "rack-1": {
        "active_shards": 0,
        "initializing_shards": 0,
        "relocating_shards": 0,
        "unassigned_shards": 0,
        "data_nodes": 1,
        "weight": 1
      },
      "rack-2": {
        "active_shards": 0,
        "initializing_shards": 0,
        "relocating_shards": 0,
        "unassigned_shards": 0,
        "data_nodes": 1,
        "weight": 1
      }
    }
  }
}
```

若您想瞭解特定感知屬性的資訊，可以將該感知屬性的名稱納入查詢參數：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/health?level=awareness_attributes&awareness_attribute=zone
-->
{% capture step1_rest %}
GET /_cluster/health?level=awareness_attributes&awareness_attribute=zone
{% endcapture %}

{% capture step1_python %}


response = client.cluster.health(
  params = { "level": "awareness_attributes", "awareness_attribute": "zone" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

針對上述請求，OpenSearch 僅傳回 `zone` 感知屬性的叢集健康狀態資訊。

只有在叢集啟動前，或叢集啟動後但尚未收到任何編製索引請求之前，針對感知屬性[啟用副本數量強制規則]({{site.url}}{{site.baseurl}}/opensearch/cluster#replica-count-enforcement)並[設定強制感知]({{site.url}}{{site.baseurl}}/opensearch/cluster#forced-awareness)，未指派分片的資訊才會準確。如果您在叢集收到編製索引請求之後才啟用副本強制規則，未指派分片的資訊可能不準確。如果您未設定副本數量強制規則與強制感知，`unassigned_shards` 欄位將包含 -1。
{: .warning}

## 回應本文欄位

下表列出所有回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `cluster_name` | 字串 | 叢集的名稱。 |
| `status` | 字串 | 根據分片分配狀態得出的整體叢集健康狀態。<br> - `green`：所有主要分片與副本分片皆已分配。<br> - `yellow`：所有主要分片皆已分配，但部分副本尚未分配。<br> - `red`：至少有一個主要分片未指派。<br><br> 整體狀態由所有索引中最差的分片狀態決定。 |
| `timed_out` | 布林值 | 表示請求是否在達到所需的健康狀態之前超過逾時時間。`false` 表示回應在逾時時間內傳回。`true` 表示在達到所需狀態之前，逾時時間已到期。 |
| `number_of_nodes` | 整數 | 叢集中節點的總數，包括所有節點類型（資料節點、叢集管理員節點、匯入節點等）。 |
| `number_of_data_nodes` | 整數 | 叢集中被指定為資料節點的節點數量。資料節點儲存分片並處理與資料相關的操作。 |
| `discovered_cluster_manager` | 布林值 | 表示是否已探索到叢集管理員節點且可連線。若為 `false`，叢集可能處於不穩定狀態。 |
| `discovered_master` | 布林值 | 舊版欄位。請改用 `discovered_cluster_manager`。為了向下相容而保留。 |
| `active_primary_shards` | 整數 | 叢集中目前已分配且作用中的主要分片數量。每份文件都恰好儲存在一個主要分片中。 |
| `active_shards` | 整數 | 作用中分片的總數，包括主要分片與副本分片。數值越高表示資料備援能力越好。 |
| `relocating_shards` | 整數 | 目前正從一個節點移動到另一個節點的分片數量。分片重新配置發生在重新平衡期間，或當節點加入或離開叢集時。 |
| `initializing_shards` | 整數 | 目前正在初始化的分片數量。這會發生在首次建立索引時，或當節點重新加入叢集並需要復原分片資料時。 |
| `unassigned_shards` | 整數 | 存在於叢集狀態中，但尚未分配給任何節點的分片數量。未指派分片通常出現在無法分配副本時（在單一節點叢集中），或當節點故障而需要重新分配分片時。 |
| `delayed_unassigned_shards` | 整數 | 刻意延後分配的未指派分片數量。當節點短暫中斷連線且預期會恢復連線時，OpenSearch 可以延後分配，以避免不必要的分片移動。 |
| `number_of_pending_tasks` | 整數 | 已排入佇列並等待叢集管理員執行的叢集層級變更數量（例如建立索引、更新對應或決定分片分配）。 |
| `number_of_in_flight_fetch` | 整數 | 目前在整個叢集中持續執行的分片層級擷取操作數量。 |
| `task_max_waiting_in_queue_millis` | 整數 | 等待最久的工作在佇列中停留的時間，以毫秒為單位。數值偏高可能表示叢集管理員負載過重。 |
| `active_shards_percent_as_number` | 雙精度浮點數 | 作用中分片占應存在的分片總數（主要分片與副本分片）的百分比。值為 100.0 表示所有分片皆已分配。 |
| `indices` | 物件 | 當 `level=indices` 或 `level=shards` 時傳回。包含各索引的健康狀態資訊，其結構與叢集層級欄位相同。 |
| `shards` | 物件 | 當 `level=shards` 時傳回。包含各分片的健康狀態資訊，巢狀置於 `indices` 物件中。 |
| `awareness_attributes` | 物件 | 當 `level=awareness_attributes` 時傳回。包含依感知屬性（例如區域或機架）劃分的叢集健康狀態資訊。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：
`cluster:monitor/health`。
