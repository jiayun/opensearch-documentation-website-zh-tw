---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得多租用戶組態"
parent: Multi-tenancy configuration APIs
grand_parent: Security APIs
nav_order: 20
---

# 取得多租用戶組態 API
**2.7 版導入**
{: .label .label-purple }

擷取多租用戶組態。

<!-- spec_insert_start
api: security.get_tenancy_config
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/tenancy/config
```
<!-- spec_insert_end -->

## 請求範例

```json
GET _plugins/_security/api/tenancy/config
```
{% include copy-curl.html security=true %}

## 回應範例

```json
{
  "default_tenant": "",
  "private_tenant_enabled": true,
  "multitenancy_enabled": true,
  "sign_in_options": [],
  "preferred_tenants": []
}
```
