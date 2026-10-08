---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集路由與感知"
nav_order: 48
parent: Cluster APIs
has_children: false
redirect_from:
  - /api-reference/cluster-awareness/
  - /opensearch/rest-api/cluster-awareness/
---

# Cluster Routing And Awareness API
**於 1.0 版引入**
{: .label .label-purple }

若要控制搜尋流量在各區域之間的路由方式，您可以為感知屬性值指派權重。這適用於分區部署、異質叢集，或將流量導離狀況不良的區域。

## 先決條件

使用此 API 前，您必須設定叢集感知屬性與節點屬性。您可以在 `opensearch.yml` 檔案中設定，或透過 Cluster Settings API 設定。 

例如，若要使用 `opensearch.yml` 設定 `zone` 與 `rack` 感知屬性，請以逗號分隔的清單指定這些屬性：

```yaml
cluster.routing.allocation.awareness.attributes: zone,rack
```
{% include copy.html %}

或者，您可以使用 Cluster Settings API 設定感知屬性：

<!-- spec_insert_start
component: example_code
rest: PUT /_cluster/routing/awareness/zone/weights
body: |
{
  "weights":
  {
    "zone_1": "1",
    "zone_2": "1",
    "zone_3": "0"
  },
  "_version" : -1
}
-->
{% capture step1_rest %}
PUT /_cluster/routing/awareness/zone/weights
{
  "weights": {
    "zone_1": "1",
    "zone_2": "1",
    "zone_3": "0"
  },
  "_version": -1
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.put_weighted_routing(
  attribute = "zone",
  body =   {
    "weights": {
      "zone_1": "1",
      "zone_2": "1",
      "zone_3": "0"
    },
    "_version": -1
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

如需 OpenSearch 設定的詳細資訊，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)。

## 端點

```json
PUT /_cluster/routing/awareness/{attribute}/weights
GET /_cluster/routing/awareness/{attribute}/weights?local
GET /_cluster/routing/awareness/{attribute}/weights
DELETE /_cluster/routing/awareness/{attribute}/weights
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`attribute` | 字串 | 已設定的感知屬性名稱（例如 `zone`）。路徑中指定的屬性決定權重套用至哪個感知屬性。

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 |  資料類型 | 說明 |
| :--- | :--- | :--- |
| `local` | 布林值 | 僅可在 `GET` 請求中提供。若為 `true`，請求會從接收請求的節點擷取資訊，而非從叢集管理員節點擷取。預設為 `false`。|

## 請求本文欄位

下表列出 `PUT` 與 `DELETE` 方法可用的請求本文欄位。

| 參數  | 資料類型 | 適用方法 | 說明  |
| :--- | :--- | :--- | :--- |
| `weights` | 物件 | `PUT` | 指定感知屬性值的自訂權重。權重會影響搜尋請求在各區域或其他感知屬性值之間的分配方式。權重為相對值，可使用任何比例。例如，若三個區域的權重比例為 `2:3:5`，則分別有 20%、30% 與 50% 的請求路由至對應區域。權重為 `0` 時，該區域將不會接收搜尋流量。此欄位為 `PUT` 方法的必要欄位。 |
| `_version` | 整數 | `PUT`, `DELETE` | 用於樂觀並行控制（OCC）。確保僅在目前版本相符時才套用變更，以防止更新衝突。每次成功執行 `PUT` 或 `DELETE` 操作後，版本都會遞增。若要啟動並行控制，您必須在初始請求中將 `_version` 設為 `-1`。此欄位為 `PUT` 與 `DELETE` 方法的必要欄位。 |


## 請求範例：加權輪詢搜尋

下列請求範例建立輪詢分片配置，將搜尋流量分配至兩個區域，同時排除第三個區域，使其不接收任何流量：

<!-- spec_insert_start
component: example_code
rest: PUT /_cluster/routing/awareness/zone/weights
body: |
{
  "weights":
  {
    "zone_1": "1",
    "zone_2": "1",
    "zone_3": "0"
  },
  "_version" : -1
}
-->
{% capture step1_rest %}
PUT /_cluster/routing/awareness/zone/weights
{
  "weights": {
    "zone_1": "1",
    "zone_2": "1",
    "zone_3": "0"
  },
  "_version": -1
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.put_weighted_routing(
  attribute = "zone",
  body =   {
    "weights": {
      "zone_1": "1",
      "zone_2": "1",
      "zone_3": "0"
    },
    "_version": -1
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

此請求執行後，`_version` 會遞增至 `0`。

若要為多個感知屬性建立分片配置，請針對每個屬性分別傳送請求。

## 請求範例：更新組態

`PUT` 請求會完全取代指定感知屬性的現有權重組態。請求中省略的所有值都會從組態中移除。例如，下列請求會更新區域 1 與 3 的權重，並移除區域 2：

<!-- spec_insert_start
component: example_code
rest: PUT /_cluster/routing/awareness/zone/weights
body: |
{
  "weights":
  {
    "zone_1": "2",
    "zone_3": "1"
  },
  "_version" : 0
}
-->
{% capture step1_rest %}
PUT /_cluster/routing/awareness/zone/weights
{
  "weights": {
    "zone_1": "2",
    "zone_3": "1"
  },
  "_version": 0
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.put_weighted_routing(
  attribute = "zone",
  body =   {
    "weights": {
      "zone_1": "2",
      "zone_3": "1"
    },
    "_version": 0
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

此請求執行後，`_version` 會遞增至 `1`。

## 請求範例：檢視組態

若要檢視目前的權重組態及其版本，請傳送下列請求。在後續的更新或刪除請求中，請使用傳回的版本號碼：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/routing/awareness/zone/weights
-->
{% capture step1_rest %}
GET /_cluster/routing/awareness/zone/weights
{% endcapture %}

{% capture step1_python %}


response = client.cluster.get_weighted_routing(
  attribute = "zone"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

```json
{
  "weights": {
    "zone_1": "2.0",
    "zone_3": "1.0"
  },
  "_version": 1,
  "discovered_cluster_manager": true
}
```

## 請求範例：刪除組態

若要移除權重組態，請在 `DELETE` 請求中提供目前版本：

```json
DELETE /_cluster/routing/awareness/zone/weights
{
  "_version": 1
}
```
{% include copy-curl.html %}

此請求執行後，`_version` 會遞增至 `2`。

## 後續步驟

- 如需區域啟用的詳細資訊，請參閱[叢集停用]({{site.url}}{{site.baseurl}}/api-reference/cluster-decommission/)。
- 如需配置感知的詳細資訊，請參閱[叢集形成]({{site.url}}{{site.baseurl}}/opensearch/cluster/#advanced-step-6-configure-shard-allocation-awareness-or-forced-awareness)。
