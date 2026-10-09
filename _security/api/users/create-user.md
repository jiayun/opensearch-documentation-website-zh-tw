---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新使用者"
parent: Internal user APIs
grand_parent: Security APIs
nav_order: 10
---

# 建立或更新使用者 API
**1.0 版推出**
{: .label .label-purple }

建立或取代指定的使用者。您必須指定 `password`（純文字）或 `hash`（經雜湊處理的使用者密碼）其中之一。如果您指定 `password`，Security 外掛程式會在儲存密碼前自動對其進行雜湊處理。

請注意，您在 `opendistro_security_roles` 陣列中提供的任何角色都必須已經存在，Security 外掛程式才能將使用者對應至該角色。若要查看預先定義的角色，請參閱[預先定義的角色清單]({{site.url}}{{site.baseurl}}/security/access-control/users-roles#predefined-roles)。如需建立角色的說明，請參閱[建立或更新角色 API]({{site.url}}{{site.baseurl}}/security/api/roles/create-role/)。

<!-- spec_insert_start
api: security.create_user
component: endpoints
-->
## 端點
```json
PUT /_plugins/_security/api/internalusers/{username}
```
<!-- spec_insert_end -->

## 請求本文欄位

請求本文為必要項目。它是包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `password` | 字串 | 使用者的純文字密碼。Security 外掛程式會在儲存密碼前對其進行雜湊處理。除非您指定 `hash`，否則為必要項目。 | 否 |
| `hash` | 字串 | 使用者密碼的雜湊值。使用此欄位提供您自行雜湊處理的密碼。除非您指定 `password`，否則為必要項目。 | 否 |
| `backend_roles` | 字串陣列 | 指派給使用者的後端角色。角色對應會使用後端角色來決定使用者的安全性角色。 | 否 |
| `opendistro_security_roles` | 字串陣列 | 直接對應至使用者的安全性角色。每個角色都必須已經存在。 | 否 |
| `attributes` | 物件 | 與使用者相關聯的自訂名稱/值配對。可在文件層級安全性查詢及角色對應中使用。 | 否 |
| `description` | 字串 | 使用者的說明。 | 否 |
| `hidden` | 布林值 | 是否對 API 及 OpenSearch Dashboards 隱藏該使用者。預設為 `false`。 | 否 |
| `reserved` | 布林值 | 使用者是否為唯讀且無法修改。預設為 `false`。 | 否 |

## 請求範例

```json
PUT _plugins/_security/api/internalusers/kirk
{
  "password": "Str0ngPassw0rd_9182!",
  "opendistro_security_roles": [
    "maintenance_staff",
    "database_manager"
  ],
  "backend_roles": [
    "captain",
    "starfleet"
  ],
  "attributes": {
    "attribute1": "value1",
    "attribute2": "value2"
  }
}
```
{% include copy-curl.html security=true %}

## 回應範例

```json
{
  "status": "CREATED",
  "message": "'kirk' created."
}
```
