---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除辨別名稱"
parent: Distinguished name APIs
grand_parent: Security APIs
nav_order: 40
---

# 刪除辨別名稱 API
**於 1.0 版導入**
{: .label .label-purple }

刪除指定叢集或節點允許清單中的所有辨別名稱。

此 API 僅供超級管理員使用。請使用管理員憑證而非使用者名稱與密碼進行驗證。如需更多資訊，請參閱 [API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
{: .note}

<!-- spec_insert_start
api: security.delete_distinguished_name
component: endpoints
-->
## 端點
```json
DELETE /_plugins/_security/api/nodesdn/{cluster_name}
```
<!-- spec_insert_end -->

## 範例請求

```json
DELETE _plugins/_security/api/nodesdn/cluster1
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "status": "OK",
  "message": "'cluster1' deleted."
}
```
