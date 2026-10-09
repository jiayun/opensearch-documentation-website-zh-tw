---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "修補角色"
parent: Role APIs
grand_parent: Security APIs
nav_order: 20
---

# Patch Roles API
**於 1.0 版推出**
{: .label .label-purple }

更新角色而不取代角色。指定角色名稱可更新單一角色的個別屬性；省略角色名稱則可在單次呼叫中建立、更新或刪除多個角色。

<!-- spec_insert_start
api: security.patch_roles
component: endpoints
-->
## 端點
```json
PATCH /_plugins/_security/api/roles
```
<!-- spec_insert_end -->
<!-- spec_insert_start
api: security.patch_role
component: endpoints
omit_header: true
-->
```json
PATCH /_plugins/_security/api/roles/{role}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `role` | 字串 | 否 | 要更新的角色名稱。若省略，請求可修改多個角色。 |

## 請求本文欄位

請求本文為必要項目。請求本文是 JSON 物件的陣列。每個物件包含下列欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `op` | 字串 | 要執行的操作。有效值為 `add`、`remove`、`replace`、`move`、`copy` 和 `test`。 | 是 |
| `path` | 字串 | 要修改的路徑。指定角色名稱時，路徑是相對於該角色，例如 `/index_permissions/0/fls`。省略角色名稱時，路徑以角色名稱開頭，例如 `/reporting-role/cluster_permissions`。 | 是 |
| `value` | 物件 | 新的值。`add`、`replace` 和 `test` 操作為必要。 | 否 |

使用 `-` 作為陣列索引，可將新權限附加至權限陣列的結尾。
{: .note}

## 請求範例

下列請求會取代 `test-role` 角色的欄位層級安全性設定，並移除其文件層級安全性設定：

```json
PATCH _plugins/_security/api/roles/test-role
[
  {
    "op": "replace", "path": "/index_permissions/0/fls", "value": ["myfield1", "myfield2"]
  },
  {
    "op": "remove", "path": "/index_permissions/0/dls"
  }
]
```
{% include copy-curl.html security=true %}

下列請求會新增 `reporting-role` 角色並移除 `test-role-2` 角色：

```json
PATCH _plugins/_security/api/roles
[
  {
    "op": "add",
    "path": "/reporting-role",
    "value": {
      "cluster_permissions": [
        "cluster_composite_ops"
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

更新單一角色的請求會在回應中列出該角色的名稱：

```json
{
  "status": "OK",
  "message": "'test-role' updated."
}
```

大量請求不會列出其所變更角色的名稱：

```json
{
  "status": "OK",
  "message": "Resource updated."
}
```
