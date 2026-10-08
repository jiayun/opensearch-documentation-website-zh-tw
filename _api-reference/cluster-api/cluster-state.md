---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集狀態"
nav_order: 55
parent: Cluster APIs
---

# 叢集狀態 API
**於 1.0 版引入**
{: .label .label-purple }

`/_cluster/state` API 會擷取叢集的目前狀態，包括中繼資料、路由表、節點與其他元件。此 API 主要用於監控、偵錯與內部用途。它提供叢集管理員節點所維護的叢集狀態各部分的快照。

## 端點

```json
GET /_cluster/state
GET /_cluster/state/{metric}
GET /_cluster/state/{metric}/{target}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數   | 資料類型         | 說明 |
| ----------- | ----------------- | ----------- |
| `metric` | 字串或清單 | 以逗號分隔的指標清單，用於指定要包含在回應中的指標。可用選項清單請參閱 [指標選項](#metric-options)。預設為 `_all`。 |
| `target` | 字串或清單 | 以逗號分隔的索引名稱、資料串流與索引別名清單，用於限制回應的範圍。 |

## 指標選項

您可以使用 `metric` 路徑參數限制 API 傳回的資訊。可用的選項如下：

- `_all` _（預設）_：傳回所有指標。 
- `blocks`：包含索引層級與全域封鎖的資訊。
- `metadata`：傳回叢集中繼資料，包括設定、索引對應與範本。
- `nodes`：傳回叢集中節點的資訊。
- `routing_table`：提供所有分片的路由資訊。
- `cluster_manager_node`：顯示目前獲選的叢集管理員節點 ID。
- `version`：顯示目前的叢集狀態版本。

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數        | 資料類型 | 說明 |
| ---------------- | --------- | ----------- |
| `local` | 布林值 | 若為 `true`，則從本機節點而非叢集管理員節點擷取狀態。預設為 `false`。 |
| `cluster_manager_timeout` | 時間 | 連線至叢集管理員節點的逾時時間。預設為 `30s`。 |
| `flat_settings` | 布林值 | 若為 `true`，則以扁平格式傳回設定。預設為 `false`。 |
| `wait_for_metadata_version` | 整數 | 在回應之前，等待中繼資料版本等於或大於此值。 |
| `wait_for_timeout` | 時間 | 指定使用 `wait_for_metadata_version` 時的等待時間。預設為 `30s`。 |
| `ignore_unavailable` | 布林值 | 是否忽略遺失或已關閉的索引。預設為 `false`。 |
| `expand_wildcards` | 字串 | 指定萬用字元運算式可比對的索引類型。支援以逗號分隔的值。<br> 有效值為：<br> - `all`：比對任何索引，包括隱藏的索引。<br> - `closed`：比對已關閉且非隱藏的索引。<br> - `hidden`：比對隱藏的索引。必須與 `open`、`closed` 或兩者合併使用。<br> - `none`：不接受萬用字元運算式。<br> - `open`：比對開啟且非隱藏的索引。<br> 預設為 `open`。 |
| `allow_no_indices` | 布林值 | 當萬用字元運算式或索引別名未解析到任何索引時，是否失敗。預設為 `true`。 |



## 請求範例

擷取完整的叢集狀態：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/state
-->
{% capture step1_rest %}
GET /_cluster/state
{% endcapture %}

{% capture step1_python %}

response = client.cluster.state()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

擷取特定索引的中繼資料與路由表：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/state/metadata,routing_table/my-index
-->
{% capture step1_rest %}
GET /_cluster/state/metadata,routing_table/my-index
{% endcapture %}

{% capture step1_python %}


response = client.cluster.state(
  metric = "metadata,routing_table",
  index = "my-index"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

僅擷取目前獲選的叢集管理員節點：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/state/cluster_manager_node
-->
{% capture step1_rest %}
GET /_cluster/state/cluster_manager_node
{% endcapture %}

{% capture step1_python %}


response = client.cluster.state(
  metric = "cluster_manager_node"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應欄位

下表列出所有回應欄位。

| 欄位                  | 資料類型 | 說明                                                                       |
| ---------------------- | --------- | --------------------------------------------------------------------------------- |
| `cluster_name` | 字串 | 叢集的名稱。                                                          |
| `cluster_uuid` | 字串 | 叢集的唯一識別碼。                                                |
| `version` | 整數 | 叢集狀態的目前版本。                                             |
| `state_uuid` | 字串 | 此狀態版本的唯一識別碼。                                  |
| `master_node` | 字串 | 與 `cluster_manager_node` 相同，此欄位是為了向後相容而保留。                                    |
| `cluster_manager_node` | 字串 | 獲選的叢集管理員節點的節點 ID。 |
| `blocks` | 物件 | 索引層級的封鎖設定。                                                       |
| `metadata` | 物件 | 索引對應、設定與別名。                                            |
| `nodes` | 物件 | 叢集中所有節點的詳細資訊。                                              |
| `routing_table` | 物件 | 每個索引的分片至節點配置。                                               |
| `routing_nodes` | 物件 | 指派給各節點的分片清單。                                            |
| `indices` | 物件 | 特定索引的狀態中繼資料。                                                    |

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:monitor/state`。
