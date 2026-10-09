---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "局部更新動作群組"
parent: Action group APIs
grand_parent: Security APIs
nav_order: 20
---

# Patch Action Groups API
**於 1.0 版導入**
{: .label .label-purple }

更新動作群組而不加以取代。指定動作群組名稱可更新單一動作群組的個別屬性，或省略名稱以在單一呼叫中建立、更新或刪除多個動作群組。

<!-- spec_insert_start
api: security.patch_action_groups
component: endpoints
-->
## 端點
```json
PATCH /_plugins/_security/api/actiongroups
```
<!-- spec_insert_end -->
<!-- spec_insert_start
api: security.patch_action_group
component: endpoints
omit_header: true
-->
```json
PATCH /_plugins/_security/api/actiongroups/{action_group}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `action_group` | 字串 | 否 | 要更新的動作群組名稱。若省略，請求可修改多個動作群組。 |

## 請求本文欄位

請求本文為必要內容。它是一個 JSON 物件陣列。每個物件包含下列欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `op` | 字串 | 要執行的操作。有效值為 `add`、`remove`、`replace`、`move`、`copy` 與 `test`。 | 是 |
| `path` | 字串 | 要修改的路徑。指定動作群組名稱時，路徑相對於該動作群組，例如 `/allowed_actions`。省略名稱時，路徑即為動作群組的名稱，例如 `/CREATE_INDEX`。 | 是 |
| `value` | 物件 | 新值。`add`、`replace` 與 `test` 操作需要此欄位。 | 否 |

## 範例請求

下列請求會取代 `custom_action_group` 動作群組的允許動作：

```json
PATCH _plugins/_security/api/actiongroups/custom_action_group
[
  {
    "op": "replace", "path": "/allowed_actions", "value": ["indices:admin/create", "indices:admin/mapping/put"]
  }
]
```
{% include copy-curl.html security=true %}

下列請求會新增 `CREATE_INDEX` 動作群組並移除 `CRUD` 動作群組：

```json
PATCH _plugins/_security/api/actiongroups
[
  {
    "op": "add", "path": "/CREATE_INDEX", "value": { "allowed_actions": ["indices:admin/create", "indices:admin/mapping/put"] }
  },
  {
    "op": "remove", "path": "/CRUD"
  }
]
```
{% include copy-curl.html security=true %}

## 範例回應

更新單一動作群組的請求會在回應中指明該動作群組的名稱：

```json
{
  "status": "OK",
  "message": "'custom_action_group' updated."
}
```

批次請求不會指明其變更的動作群組名稱：

```json
{
  "status": "OK",
  "message": "Resource updated."
}
```
