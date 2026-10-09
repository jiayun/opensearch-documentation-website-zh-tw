---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得角色"
parent: Role APIs
grand_parent: Security APIs
nav_order: 30
---

# Get Roles API
**於 1.0 版導入**
{: .label .label-purple }

擷取角色。指定角色名稱以擷取單一角色，或省略角色名稱以擷取所有角色。

<!-- spec_insert_start
api: security.get_roles
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/roles
```
<!-- spec_insert_end -->
<!-- spec_insert_start
api: security.get_role
component: endpoints
omit_header: true
-->
```json
GET /_plugins/_security/api/roles/{role}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `role` | 字串 | 否 | 要擷取的角色名稱。若省略，則傳回所有角色。 |

## 範例請求

下列請求會擷取所有角色：

```json
GET _plugins/_security/api/roles
```
{% include copy-curl.html security=true %}

下列請求會擷取 `test-role` 角色：

```json
GET _plugins/_security/api/roles/test-role
```
{% include copy-curl.html security=true %}

## 範例回應

回應在此經過精簡：

```json
{
  "observability_read_access": {
    "cluster_permissions": [
      "cluster:admin/opensearch/observability/get"
    ],
    "hidden": false,
    "index_permissions": [],
    "reserved": true,
    "static": false,
    "tenant_permissions": []
  },
  ...
}
```

針對單一角色請求的回應只包含該角色：

```json
{
  "test-role": {
    "cluster_permissions": [
      "cluster_composite_ops",
      "indices_monitor"
    ],
    "hidden": false,
    "index_permissions": [
      {
        "allowed_actions": [
          "read"
        ],
        "dls": "",
        "fls": [],
        "index_patterns": [
          "movies*"
        ],
        "masked_fields": []
      }
    ],
    "reserved": false,
    "static": false,
    "tenant_permissions": [
      {
        "allowed_actions": [
          "kibana_all_read"
        ],
        "tenant_patterns": [
          "human_resources"
        ]
      }
    ]
  }
}
```
