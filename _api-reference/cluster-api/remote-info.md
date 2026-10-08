---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遠端叢集資訊"
parent: Cluster APIs
nav_order: 67
redirect_from: 
 - /opensearch/rest-api/remote-info/
 - /api-reference/remote-info/
---

# Remote Cluster Information API
**於 1.0 版推出**
{: .label .label-purple }

Remote Cluster Information API 會擷取本機叢集上設定的所有遠端 OpenSearch 叢集的連線詳細資訊。使用此 API 可驗證連線狀態、檢查連線模式（`sniff` 或 `proxy`），以及檢視跨叢集搜尋組態的逾時設定。

相較於呼叫 `_cluster/settings`，此 API 的回應提供更多詳細資訊；前者僅傳回叢集別名和種子節點位址。此 API 還會回報作用中的連線數、連線模式，以及跨叢集搜尋期間是否略過無法使用的叢集。

<!-- spec_insert_start
api: cluster.remote_info
component: endpoints
-->
## 端點
```json
GET /_remote/info
```
<!-- spec_insert_end -->

## 請求範例

下列範例會擷取所有已設定的遠端叢集資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_remote/info
-->
{% capture step1_rest %}
GET /_remote/info
{% endcapture %}

{% capture step1_python %}

response = client.cluster.remote_info()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

未設定任何遠端叢集時，回應為空物件：

```json
{ }
```

當一個或多個遠端叢集以 `sniff` 模式設定時，回應會包含以叢集別名為鍵的連線詳細資訊：

```json
{
  "opensearch-cluster2": {
    "connected": true,
    "mode": "sniff",
    "seeds": [
      "172.28.0.2:9300"
    ],
    "num_nodes_connected": 1,
    "max_connections_per_cluster": 3,
    "initial_connect_timeout": "30s",
    "skip_unavailable": false
  }
}
```

當遠端叢集以 `proxy` 模式設定時，回應會包含代理伺服器專屬欄位，而非種子節點資訊：

```json
{
  "opensearch-cluster3": {
    "connected": true,
    "mode": "proxy",
    "proxy_address": "192.168.1.50:9443",
    "num_proxy_sockets_connected": 5,
    "max_proxy_socket_connections": 18,
    "initial_connect_timeout": "30s",
    "skip_unavailable": true
  }
}
```

## 回應本文欄位

回應是 JSON 物件，其中每個鍵都是遠端叢集別名。下表說明各叢集項目中的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `connected` | 布林值 | 表示是否存在至少一個連至遠端叢集的作用中連線。 |
| `mode` | 字串 | 遠端叢集所設定的連線模式。有效值為 `sniff`（透過種子位址探索節點）和 `proxy`（透過單一代理伺服器位址路由所有請求）。 |
| `initial_connect_timeout` | 字串 | 建立與遠端叢集的初始連線時的逾時時間。 |
| `skip_unavailable` | 布林值 | 表示在跨叢集搜尋請求期間無法連線至遠端叢集時，是否略過該叢集。當值為 `true` 時，搜尋僅傳回可用叢集的結果。當值為 `false` 時，若此叢集無法使用，整個搜尋請求就會失敗。 |

下列欄位僅在 `mode` 為 `sniff` 時出現。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `seeds` | 字串陣列 | 用於探索遠端叢集中節點的初始種子傳輸位址。 |
| `num_nodes_connected` | 整數 | 本機叢集目前已建立連線的遠端叢集節點數。 |
| `max_connections_per_cluster` | 整數 | 本機叢集與遠端叢集之間維持的連線數上限。 |

下列欄位僅在 `mode` 為 `proxy` 時出現。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `proxy_address` | 字串 | 所有連至遠端叢集的連線都會透過此位址（主機和連接埠）進行路由。 |
| `num_proxy_sockets_connected` | 整數 | 目前已建立至代理伺服器位址的通訊端連線數。 |
| `max_proxy_socket_connections` | 整數 | 允許連至代理伺服器位址的通訊端連線數上限。 |
