---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "權限資訊"
parent: Authentication APIs
grand_parent: Security APIs
nav_order: 40
---

# Permissions Info API
**於 1.0 版導入**
{: .label .label-purple }

擷取目前使用者的 REST API 權限評估結果。

<!-- spec_insert_start
api: security.get_permissions_info
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/permissionsinfo
```
<!-- spec_insert_end -->

## 範例請求

```json
GET _plugins/_security/api/permissionsinfo
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "user": "User [name=admin, backend_roles=[admin], requestedTenant=null]",
  "user_name": "admin",
  "has_api_access": true,
  "disabled_endpoints": {}
}
```

## 回應本文欄位

回應本文是一個包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `user` | 字串 | 目前使用者的字串表示法，包含使用者名稱、後端角色與所請求的租用戶。 |
| `user_name` | 字串 | 目前使用者的名稱。 |
| `has_api_access` | 布林值 | 目前使用者是否可以呼叫 Security API。 |
| `disabled_endpoints` | 物件 | 目前使用者被停用的 Security API 端點。每個鍵是端點名稱，每個值是針對該端點停用的 HTTP 方法清單。當沒有端點被停用時，此物件為空。 |
