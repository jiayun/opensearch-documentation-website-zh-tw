---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "租用戶資訊"
parent: Multi-tenancy configuration APIs
grand_parent: Security APIs
nav_order: 30
---

# 租用戶資訊 API
**1.0 版新增**
{: .label .label-purple }

擷取目前租用戶的後端索引名稱。

此 API 僅供超級管理員或 `kibanaserver` 使用者使用。請使用管理員憑證而非使用者名稱與密碼進行驗證。如需更多資訊，請參閱 [API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
{: .note}

<!-- spec_insert_start
api: security.tenant_info
component: endpoints
-->
## 端點
```json
GET  /_plugins/_security/tenantinfo
POST /_plugins/_security/tenantinfo
```
<!-- spec_insert_end -->

## 範例請求

```json
GET _plugins/_security/tenantinfo
```
{% include copy-curl.html security=true %}

## 範例回應

回應會將每個租用戶索引對應至其所屬的租用戶。在建立租用戶索引之前，回應為空：

```json
{}
```
