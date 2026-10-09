---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新辨別名稱"
parent: Distinguished name APIs
grand_parent: Security APIs
nav_order: 10
---

# 建立或更新辨別名稱 API
**於 1.0 版推出**
{: .label .label-purple }

在叢集或節點的允許清單中新增或更新指定的辨別名稱。

此 API 保留給超級管理員使用。請使用管理員憑證進行驗證，而非使用者名稱與密碼。如需更多資訊，請參閱[API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
{: .note}

<!-- spec_insert_start
api: security.update_distinguished_name
component: endpoints
-->
## 端點
```json
PUT /_plugins/_security/api/nodesdn/{cluster_name}
```
<!-- spec_insert_end -->

## 範例請求

```json
PUT _plugins/_security/api/nodesdn/cluster1
{
  "nodes_dn": [
    "CN=cluster1.example.com"
  ]
}
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "status": "CREATED",
  "message": "'cluster1' created."
}
```
