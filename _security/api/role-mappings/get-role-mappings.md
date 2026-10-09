---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得角色對應"
parent: Role mapping APIs
grand_parent: Security APIs
nav_order: 30
---

# 取得角色對應 API
**於 1.0 版導入**
{: .label .label-purple }

擷取角色對應。指定角色名稱以擷取單一角色的對應，或省略角色名稱以擷取所有角色對應。

<!-- spec_insert_start
api: security.get_role_mappings
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/rolesmapping
```
<!-- spec_insert_end -->
<!-- spec_insert_start
api: security.get_role_mapping
component: endpoints
omit_header: true
-->
```json
GET /_plugins/_security/api/rolesmapping/{role}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `role` | 字串 | 否 | 您要擷取其對應的角色名稱。若省略，則傳回所有角色對應。 |

## 範例請求

下列請求會擷取所有角色對應：

```json
GET _plugins/_security/api/rolesmapping
```
{% include copy-curl.html security=true %}

下列請求會擷取 `role_starfleet` 角色的對應：

```json
GET _plugins/_security/api/rolesmapping/role_starfleet
```
{% include copy-curl.html security=true %}

## 範例回應

回應在此經過刪節：

```json
{
  "manage_snapshots": {
    "and_backend_roles": [],
    "backend_roles": [
      "snapshotrestore"
    ],
    "hidden": false,
    "hosts": [],
    "reserved": false,
    "users": []
  },
  "logstash": {
    "and_backend_roles": [],
    "backend_roles": [
      "logstash"
    ],
    "hidden": false,
    "hosts": [],
    "reserved": false,
    "users": []
  },
  "kibana_user": {
    "and_backend_roles": [],
    "backend_roles": [
      "kibanauser"
    ],
    "description": "Maps kibanauser to kibana_user",
    "hidden": false,
    "hosts": [],
    "reserved": false,
    "users": []
  },
  ...
}
```

針對單一角色對應之請求的回應僅包含該對應：

```json
{
  "role_starfleet": {
    "and_backend_roles": [],
    "backend_roles": [
      "starfleet",
      "captains",
      "defectors",
      "cn=ldaprole,ou=groups,dc=example,dc=com"
    ],
    "hidden": false,
    "hosts": [
      "*.starfleetintranet.com"
    ],
    "reserved": false,
    "users": [
      "worf"
    ]
  }
}
```
