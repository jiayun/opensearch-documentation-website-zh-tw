---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得動作群組"
parent: Action group APIs
grand_parent: Security APIs
nav_order: 30
---

# Get Action Groups API
**於 1.0 版導入**
{: .label .label-purple }

擷取動作群組。指定動作群組名稱可擷取單一動作群組，或省略名稱以擷取所有動作群組。

<!-- spec_insert_start
api: security.get_action_groups
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/actiongroups
```
<!-- spec_insert_end -->
<!-- spec_insert_start
api: security.get_action_group
component: endpoints
omit_header: true
-->
```json
GET /_plugins/_security/api/actiongroups/{action_group}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `action_group` | 字串 | 否 | 要擷取的動作群組名稱。若省略，則傳回所有動作群組。 |

## 範例請求

下列請求會擷取所有動作群組：

```json
GET _plugins/_security/api/actiongroups
```
{% include copy-curl.html security=true %}

下列請求會擷取 `custom_action_group` 動作群組：

```json
GET _plugins/_security/api/actiongroups/custom_action_group
```
{% include copy-curl.html security=true %}

## 範例回應

回應在此經過簡略：

```json
{
  "custom_action_group": {
    "allowed_actions": [
      "indices:data/write/index*",
      "indices:data/write/update*",
      "indices:admin/mapping/put",
      "indices:data/write/bulk*",
      "read",
      "write"
    ],
    "hidden": false,
    "reserved": false,
    "static": false
  },
  "data_access": {
    "allowed_actions": [
      "indices:data/*",
      "crud"
    ],
    "description": "Allow all read/write operations on data",
    "hidden": false,
    "reserved": true,
    "static": true,
    "type": "index"
  },
  "delete": {
    "allowed_actions": [
      "indices:data/write/delete*"
    ],
    "description": "Allow deleting documents",
    "hidden": false,
    "reserved": true,
    "static": true,
    "type": "index"
  },
  "cluster_manage_pipelines": {
    "allowed_actions": [
      "cluster:admin/ingest/pipeline/*"
    ],
    "description": "Manage pipelines",
    "hidden": false,
    "reserved": true,
    "static": true,
    "type": "cluster"
  },
  ...
}
```

當您擷取單一動作群組時，回應只包含該動作群組：

```json
{
  "custom_action_group": {
    "allowed_actions": [
      "indices:data/write/index*",
      "indices:data/write/update*",
      "indices:admin/mapping/put",
      "indices:data/write/bulk*",
      "read",
      "write"
    ],
    "hidden": false,
    "reserved": false,
    "static": false
  }
}
```
