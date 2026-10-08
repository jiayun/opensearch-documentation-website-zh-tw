---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Nodes API"
has_children: true
has_toc: false
nav_order: 80
redirect_from:
  - /api-reference/nodes-apis/
---

# Nodes API
**1.0 版新增**
{: .label .label-purple }

Nodes API 可用來擷取叢集中個別節點的資訊。

## 節點篩選器

使用 `<node-filters>` 參數來篩選 API 回應中的目標節點集合。

<style>
table th:first-of-type {
    width: 25%;
}
table th:nth-of-type(2) {
    width: 10%;
}
table th:nth-of-type(3) {
    width: 65%;
}
</style>

參數 | 類型   | 說明
:--- |:-------| :---
`node-filters` | 字串 | 以逗號分隔的解析機制清單，OpenSearch 用來識別叢集節點。

節點篩選器支援數種節點解析機制：

- 預先定義的常數：`_local`、`_cluster_manager` 或 `_all`。
- `nodeID` 的精確比對
- 針對 `node-name`、`host-name` 或 `host-IP-address` 的簡單區分大小寫萬用字元模式比對。
- `<bool>` 值設為 `true` 或 `false` 的節點角色：
  - `cluster_manager:<bool>` 指所有具叢集管理員資格的節點。
  - `data:<bool>` 指所有資料節點。
  - `ingest:<bool>` 指所有匯入節點。
  - `voting_only:<bool>` 指所有僅投票節點。
  - `ml:<bool>` 指所有機器學習 (ML) 節點。
  - `coordinating_only:<bool>` 指所有僅協調節點。
- 針對節點屬性的簡單區分大小寫萬用字元模式比對：`<node attribute*>:<attribute value*>`。萬用字元比對模式可同時用於鍵與值。

解析機制會依用戶端指定的順序依序套用。每個機制規格可以新增或移除節點。

若只要從當選的叢集管理員節點取得統計資料，請使用下列查詢：

<!-- spec_insert_start
component: example_code
rest: GET /_nodes/_cluster_manager/stats
-->
{% capture step1_rest %}
GET /_nodes/_cluster_manager/stats
{% endcapture %}

{% capture step1_python %}


response = client.nodes.info(
  metric = "stats",
  node_id = "_cluster_manager"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要從僅作為資料節點的節點取得統計資料，請使用下列查詢：

<!-- spec_insert_start
component: example_code
rest: GET /_nodes/data:true/stats
-->
{% capture step1_rest %}
GET /_nodes/data:true/stats
{% endcapture %}

{% capture step1_python %}


response = client.nodes.info(
  metric = "stats",
  node_id = "data:true"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 解析機制的順序

解析機制的順序會依序套用，且每個機制都可以新增或移除節點。下列範例會產生不同的結果。

若要從叢集管理員節點以外的所有節點取得統計資料，請使用下列查詢：

<!-- spec_insert_start
component: example_code
rest: GET /_nodes/_all,cluster_manager:false/stats
-->
{% capture step1_rest %}
GET /_nodes/_all,cluster_manager:false/stats
{% endcapture %}

{% capture step1_python %}


response = client.nodes.info(
  metric = "stats",
  node_id = "_all,cluster_manager:false"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

不過，如果您調換解析機制的順序，結果將包含所有叢集節點，包括叢集管理員節點：

<!-- spec_insert_start
component: example_code
rest: GET /_nodes/cluster_manager:false,_all/stats
-->
{% capture step1_rest %}
GET /_nodes/cluster_manager:false,_all/stats
{% endcapture %}

{% capture step1_python %}


response = client.nodes.info(
  metric = "stats",
  node_id = "cluster_manager:false,_all"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## Nodes API 操作

下列 Nodes API 操作可供使用：

- [Nodes hot threads]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-hot-threads/)
- [Nodes info]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-info/)
- [Nodes reload secure settings]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-reload-secure/)
- [Nodes stats]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/)
- [Nodes usage]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-usage/)
