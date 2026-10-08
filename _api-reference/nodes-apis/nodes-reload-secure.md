---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "節點重新載入安全設定"
parent: Nodes APIs
nav_order: 50
---

# 節點重新載入安全設定 API
**於 1.0 版推出**
{: .label .label-purple }

節點重新載入安全設定端點可讓您變更節點上的安全設定，並重新載入安全設定，而不需重新啟動節點。

## 端點

```json
POST _nodes/reload_secure_settings
POST _nodes/{node_id}/reload_secure_settings
```

## 路徑參數

您可以在請求中加入下列選用路徑參數。

參數 | 類型 | 說明
:--- | :--- | :---
`node_id` | 字串 | 以逗號分隔的節點 ID 清單，用於篩選結果。支援[節點篩選器]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/index/#node-filters)。預設為 `_all`。

## 請求本文欄位

請求可包含選用物件，內含 OpenSearch keystore 的密碼。

```json
{
  "secure_settings_password": "keystore_password"
}
```

## 請求範例

以下是 API 請求範例：

<!-- spec_insert_start
component: example_code
rest: POST /_nodes/reload_secure_settings
-->
{% capture step1_rest %}
POST /_nodes/reload_secure_settings
{% endcapture %}

{% capture step1_python %}


response = client.nodes.reload_secure_settings(
  body = { "Insert body here" }
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
      "name" : "opensearch-node1"
    }
  }
}
```

## 必要權限

如果您使用 Security 外掛程式，請務必設定下列權限：`cluster:manage/nodes`。