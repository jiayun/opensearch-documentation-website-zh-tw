---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除租用戶"
parent: Tenant APIs
grand_parent: Security APIs
nav_order: 40
---

# 刪除租用戶 API
**1.0 版新增**
{: .label .label-purple }

刪除指定的租用戶。

<!-- spec_insert_start
api: security.delete_tenant
component: endpoints
-->
## 端點
```json
DELETE /_plugins/_security/api/tenants/{tenant}
```
<!-- spec_insert_end -->

## 範例請求

```json
DELETE _plugins/_security/api/tenants/test-tenant
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "status": "OK",
  "message": "'test-tenant' deleted."
}
```
