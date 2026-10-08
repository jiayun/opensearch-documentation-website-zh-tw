---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集停用"
nav_order: 30
parent: Cluster APIs
has_children: false
redirect_from: 
  - /api-reference/cluster-decommission/
  - /opensearch/rest-api/cluster-decommission/
---

# Cluster Decommission API
**Introduced 1.0**
{: .label .label-purple }

叢集停用作業新增了以感知為基礎的停用支援。這對多區域部署非常有幫助，因為感知屬性（例如 `zones`）可協助以受控的方式將新的升級套用至叢集。這在發生中斷時特別有用，在這種情況下，您可以停用不健康的區域，以防止複寫請求停滯，並避免請求待處理量變得過大。

如需配置感知的詳細資訊，請參閱[分片配置感知]({{site.url}}{{site.baseurl}}/opensearch/cluster/#shard-allocation-awareness)。


## 端點

```json
PUT  /_cluster/decommission/awareness/{awareness_attribute_name}/{awareness_attribute_value}
GET  /_cluster/decommission/awareness/{awareness_attribute_name}/_status
DELETE /_cluster/decommission/awareness
```

## 路徑參數

參數 | 類型 | 說明
:--- | :--- | :---
`awareness_attribute_name` | 字串 | 感知屬性的名稱，通常為 `zone`。
`awareness_attribute_value` | 字串 | 感知屬性的值。例如，如果您有分片配置在兩個不同的區域，可以為每個區域指定 `zone-a` 或 `zoneb` 的值。叢集停用作業會停用方法中所列的區域。

## 範例請求

下列範例示範如何使用 Cluster Decommission API。

### 停用和重新啟用區域

您可以使用下列範例請求來停用和重新啟用區域：


下列範例請求會停用 `zone-a`：

<!-- spec_insert_start
component: example_code
rest: PUT /_cluster/decommission/awareness/<zone>/<zone-a>
-->
{% capture step1_rest %}
PUT /_cluster/decommission/awareness/<zone>/<zone-a>
{% endcapture %}

{% capture step1_python %}


response = client.cluster.put_decommission_awareness(
  awareness_attribute_name = "<zone>",
  awareness_attribute_value = "<zone-a>"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

如果您想重新啟用已停用的區域，可以使用 `DELETE` 方法：

<!-- spec_insert_start
component: example_code
rest: DELETE /_cluster/decommission/awareness
-->
{% capture step1_rest %}
DELETE /_cluster/decommission/awareness
{% endcapture %}

{% capture step1_python %}

response = client.cluster.delete_decommission_awareness()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 取得區域停用狀態

下列範例請求會傳回所有區域的停用狀態。

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/decommission/awareness/zone/_status
-->
{% capture step1_rest %}
GET /_cluster/decommission/awareness/zone/_status
{% endcapture %}

{% capture step1_python %}


response = client.cluster.get_decommission_awareness(
  awareness_attribute_name = "zone"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 範例回應

下列範例回應顯示成功停用區域：

```json
{
      "acknowledged": true
}
```

### 取得區域停用狀態

下列範例回應會傳回所有區域的停用狀態：


```json
{
     "zone-1": "INIT | DRAINING | IN_PROGRESS | SUCCESSFUL | FAILED"
}
```


## 後續步驟

- 如需區域感知與權重的詳細資訊，請參閱[叢集感知]({{site.url}}{{site.baseurl}}/api-reference/cluster-awareness/)。
- 如需配置感知的詳細資訊，請參閱[叢集形成]({{site.url}}{{site.baseurl}}/opensearch/cluster/#advanced-step-6-configure-shard-allocation-awareness-or-forced-awareness)。
