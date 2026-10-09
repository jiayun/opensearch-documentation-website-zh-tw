---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "驗證資訊"
parent: Authentication APIs
grand_parent: Security APIs
nav_order: 10
redirect_from:
  - /api-reference/security/authentication/auth-info/
---

# 驗證資訊 API
**於 1.0 版推出**
{: .label .label-purple }

傳回目前通過驗證之使用者的相關資訊，包括使用者名稱、角色、後端角色、自訂屬性以及租用戶成員資格。您可以使用此 API 來偵錯驗證問題，或確認使用者所擁有的權限。

<!-- spec_insert_start
api: security.authinfo
component: endpoints
-->
## 端點
```json
GET  /_plugins/_security/authinfo
POST /_plugins/_security/authinfo
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: security.authinfo
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `auth_type` | 字串 | 目前驗證請求的類型。 |
| `verbose` | 布林值 | 是否傳回詳細回應。 |

<!-- spec_insert_end -->

## 範例請求

下列範例請求會擷取目前通過驗證之使用者的驗證資訊：

```json
GET /_plugins/_security/authinfo
```
{% include copy-curl.html security=true %}

下列範例請求會擷取詳細的驗證資訊：

```json
GET /_plugins/_security/authinfo?verbose=true
```
{% include copy-curl.html security=true %}

## 範例回應

預設回應會描述使用者、其角色及其租用戶：

```json
{
  "user": "User [name=admin, backend_roles=[admin], requestedTenant=null]",
  "user_name": "admin",
  "user_requested_tenant": null,
  "remote_address": "192.168.65.1:21728",
  "backend_roles": [
    "admin"
  ],
  "custom_attribute_names": [],
  "roles": [
    "all_access"
  ],
  "tenants": {
    "global_tenant": true,
    "admin_tenant": true,
    "admin": true
  },
  "principal": null,
  "peer_certificates": "0",
  "sso_logout_url": null
}
```

詳細回應會新增大小欄位：

```json
{
  "user": "User [name=admin, backend_roles=[admin], requestedTenant=null]",
  "user_name": "admin",
  "user_requested_tenant": null,
  "remote_address": "192.168.65.1:48870",
  "backend_roles": [
    "admin"
  ],
  "custom_attribute_names": [],
  "roles": [
    "all_access"
  ],
  "tenants": {
    "global_tenant": true,
    "admin_tenant": true,
    "admin": true
  },
  "principal": null,
  "peer_certificates": "0",
  "sso_logout_url": null,
  "size_of_user": "928 bytes",
  "size_of_custom_attributes": "112 bytes",
  "size_of_backendroles": "84 bytes"
}
```

## 回應本文欄位

回應本文是包含下列欄位的 JSON 物件。

| 屬性 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `user` | 字串 | 使用者物件的字串表示法，包含使用者名稱與後端角色。 |
| `user_name` | 字串 | 通過驗證之使用者的使用者名稱。 |
| `backend_roles` | 字串陣列 | 與使用者相關聯的後端角色，通常取自外部驗證系統。 |
| `roles` | 字串陣列 | 指派給使用者的 OpenSearch Security 角色，用於決定其權限。 |
| `tenants` | 物件 | 使用者可存取的租用戶，其中 `true` 表示讀寫存取權，`false` 表示唯讀存取權。 |
| `principal` | 字串 | 使用者的驗證主體 (若有的話)。 |
| `peer_certificates` | 字串 | 與使用者驗證相關的同儕憑證數量。 |
| `sso_logout_url` | 字串 | 單一登入 (SSO) 驗證的登出 URL (若適用)。 |
| `remote_address` | 字串 | 發出請求之用戶端的 IP 位址與連接埠。 |
| `custom_attribute_names` | 字串陣列 | 與使用者相關聯之任何自訂屬性的名稱。 |
| `user_requested_tenant` | 字串 | 使用者要求切換至的租用戶名稱 (若有)。 |

要求詳細回應時，會包含下列其他欄位。

| 屬性 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `size_of_user` | 字串 | 使用者物件在記憶體中的大小。 |
| `size_of_backendroles` | 字串 | 使用者後端角色的大小。 |
| `size_of_custom_attributes` | 字串 | 使用者自訂屬性的大小。 |
