---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "局部更新角色對應"
parent: Role mapping APIs
grand_parent: Security APIs
nav_order: 20
---

# Patch Role Mappings API
**於 1.0 版推出**
{: .label .label-purple }

更新角色對應，無須取代整個對應。指定角色名稱可更新單一角色對應的個別屬性，或省略角色名稱以在單次呼叫中建立、更新或刪除多個角色對應。

<!-- spec_insert_start
api: security.patch_role_mappings
component: endpoints
-->
## 端點
```json
PATCH /_plugins/_security/api/rolesmapping
```
<!-- spec_insert_end -->
<!-- spec_insert_start
api: security.patch_role_mapping
component: endpoints
omit_header: true
-->
```json
PATCH /_plugins/_security/api/rolesmapping/{role}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `role` | 字串 | 否 | 您要更新其對應的角色名稱。若省略，請求可修改多個角色對應。 |

## 請求本文欄位

請求本文為必要項目。它是由 JSON 物件組成的陣列。每個物件包含下列欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `op` | 字串 | 要執行的操作。有效值為 `add`、`remove`、`replace`、`move`、`copy` 和 `test`。 | 是 |
| `path` | 字串 | 要修改的路徑。當您指定角色名稱時，路徑相對於該角色的對應，例如 `/users`。當您省略角色名稱時，路徑會指定角色名稱，例如 `/readall`。 | 是 |
| `value` | 物件 | 新值。對於 `add`、`replace` 和 `test` 操作，此欄位為必要項目。 | 否 |

## 請求範例

下列請求會取代對應至 `my-role` 角色的使用者和後端角色：

```json
PATCH _plugins/_security/api/rolesmapping/my-role
[
  {
    "op": "replace", "path": "/users", "value": ["myuser"]
  },
  {
    "op": "replace", "path": "/backend_roles", "value": ["mybackendrole"]
  }
]
```
{% include copy-curl.html security=true %}

下列請求會新增 `readall` 角色的對應，並移除 `test-role-2` 角色的對應：

```json
PATCH _plugins/_security/api/rolesmapping
[
  {
    "op": "add",
    "path": "/readall",
    "value": {
      "backend_roles": [
        "reporting"
      ]
    }
  },
  {
    "op": "remove",
    "path": "/test-role-2"
  }
]
```
{% include copy-curl.html security=true %}

## 回應範例

更新單一角色對應的請求會在回應中列出角色名稱：

```json
{
  "status": "OK",
  "message": "'my-role' updated."
}
```

批次請求不會列出其變更的角色對應名稱：

```json
{
  "status": "OK",
  "message": "Resource updated."
}
```
