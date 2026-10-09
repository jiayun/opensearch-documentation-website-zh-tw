---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得帳戶詳細資訊"
parent: Account APIs
grand_parent: Security APIs
nav_order: 20
---

# 取得帳戶詳細資訊 API
**於 1.0 版導入**
{: .label .label-purple }

傳回目前使用者的帳戶詳細資訊。例如，如果您以 `admin` 使用者身分簽署請求，回應就會包含該使用者的詳細資訊。

<!-- spec_insert_start
api: security.get_account_details
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/account
```
<!-- spec_insert_end -->

## 範例請求

```json
GET _plugins/_security/api/account
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "user_name": "admin",
  "is_reserved": true,
  "is_hidden": false,
  "is_internal_user": true,
  "user_requested_tenant": null,
  "backend_roles": [
    "admin"
  ],
  "custom_attribute_names": [],
  "tenants": {
    "global_tenant": true,
    "admin_tenant": true,
    "admin": true
  },
  "roles": [
    "all_access"
  ]
}
```
