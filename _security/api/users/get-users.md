---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得使用者"
parent: Internal user APIs
grand_parent: Security APIs
nav_order: 30
---

# 取得使用者 API
**於 1.0 版導入**
{: .label .label-purple }

擷取內部使用者。指定使用者名稱可擷取單一使用者，或省略使用者名稱以擷取所有內部使用者。

<!-- spec_insert_start
api: security.get_users
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/internalusers
```
<!-- spec_insert_end -->
<!-- spec_insert_start
api: security.get_user
component: endpoints
omit_header: true
-->
```json
GET /_plugins/_security/api/internalusers/{username}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `username` | 字串 | 否 | 要擷取的使用者名稱。若省略，則傳回所有內部使用者。 |

## 範例請求

下列請求會擷取所有內部使用者：

```json
GET _plugins/_security/api/internalusers
```
{% include copy-curl.html security=true %}

下列請求會擷取 `kirk` 使用者：

```json
GET _plugins/_security/api/internalusers/kirk
```
{% include copy-curl.html security=true %}

## 範例回應

回應會列出每個內部使用者。此處僅節錄部分內容：

```json
{
  "logstash": {
    "attributes": {},
    "backend_roles": [
      "logstash"
    ],
    "description": "Demo logstash user, using external role mapping",
    "hash": "",
    "hidden": false,
    "opendistro_security_roles": [],
    "reserved": false,
    "static": false
  },
  "snapshotrestore": {
    "attributes": {},
    "backend_roles": [
      "snapshotrestore"
    ],
    "description": "Demo snapshotrestore user, using external role mapping",
    "hash": "",
    "hidden": false,
    "opendistro_security_roles": [],
    "reserved": false,
    "static": false
  },
  "admin": {
    "attributes": {},
    "backend_roles": [
      "admin"
    ],
    "description": "Demo admin user",
    "hash": "",
    "hidden": false,
    "opendistro_security_roles": [],
    "reserved": true,
    "static": false
  },
  ...
}
```

針對單一使用者的請求，其回應僅包含該使用者：

```json
{
  "kirk": {
    "attributes": {
      "attribute1": "value1",
      "attribute2": "value2"
    },
    "backend_roles": [
      "captain",
      "starfleet"
    ],
    "hash": "",
    "hidden": false,
    "opendistro_security_roles": [
      "maintenance_staff",
      "database_manager"
    ],
    "reserved": false,
    "static": false
  }
}
```
