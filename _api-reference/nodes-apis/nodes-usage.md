---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "節點使用情況"
parent: Nodes APIs
nav_order: 40
---

# Nodes Usage API
**於 1.0 版推出**
{: .label .label-purple }

節點使用情況端點會傳回節點上 REST 動作使用情況的低階資訊。

## 端點

```json
GET _nodes/usage
GET _nodes/{node_id}/usage
GET _nodes/usage/{metric}
GET _nodes/{node_id}/usage/{metric}
```

## 路徑參數

您可以在請求中包含下列選用的路徑參數。

參數 | 類型 | 說明
:--- | :--- | :---
`node_id` | 字串 | 用於篩選結果的節點 ID 清單，以逗號分隔。支援[節點篩選器]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/index/#node-filters)。預設為 `_all`。
`metric` | 字串 | 回應中將包含的指標。您可以將字串設為 `_all` 或 `rest_actions`。`rest_actions` 會傳回動作在節點上被呼叫的總次數。`_all` 會傳回節點的所有統計資料。預設為 `_all`。

## 查詢參數

您可以在請求中包含下列選用的查詢參數。

參數 | 類型 | 說明
:--- | :---| :---
`timeout` | 時間 | 設定等待節點回應的時間限制。預設為 `30s`。
`cluster_manager_timeout` | 時間 | 設定等待叢集管理員回應的時間限制。預設為 `30s`。

## 請求範例

下列請求會傳回所有節點的使用情況詳細資料：

<!-- spec_insert_start
component: example_code
rest: GET /_nodes/usage
-->
{% capture step1_rest %}
GET /_nodes/usage
{% endcapture %}

{% capture step1_python %}


response = client.nodes.info(
  node_id_or_metric = "usage"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

以下是回應範例：

```json
{
  "_nodes" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "cluster_name" : "opensearch-cluster",
  "nodes" : {
    "t7uqHu4SSuWObK3ElkCRfw" : {
      "timestamp" : 1665695174312,
      "since" : 1663994849643,
      "rest_actions" : {
        "opendistro_get_rollup_action" : 3,
        "nodes_usage_action" : 1,
        "list_dangling_indices" : 1,
        "get_index_template_action" : 258,
        "nodes_info_action" : 152665,
        "get_mapping_action" : 259,
        "get_data_streams_action" : 12,
        "cat_indices_action" : 6,
        "get_indices_action" : 3,
        "ism_explain_action" : 7,
        "nodes_reload_action" : 1,
        "get_policy_action" : 3,
        "PerformanceAnalyzerClusterConfigAction" : 2,
        "index_policy_action" : 1,
        "rank_eval_action" : 3,
        "search_action" : 592,
        "get_aliases_action" : 258,
        "document_mget_action" : 2,
        "document_get_action" : 30,
        "count_action" : 1,
        "main_action" : 1
      },
      "aggregations" : { }
    }
  }
}
```

## 必要權限

如果您使用 Security 外掛程式，請確保設定下列權限：`cluster:manage/nodes` 或 `cluster:monitor/nodes`。