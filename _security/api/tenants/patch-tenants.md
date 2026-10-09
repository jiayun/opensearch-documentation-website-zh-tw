---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "修補租用戶"
parent: Tenant APIs
grand_parent: Security APIs
nav_order: 20
---

# Patch Tenants API
**於 1.0 版推出**
{: .label .label-purple }

更新租用戶而不取代它們。指定租用戶名稱以更新單一租用戶的個別屬性，或省略租用戶名稱以在單次呼叫中新增、刪除或修改多個租用戶。

<!-- spec_insert_start
api: security.patch_tenants
component: endpoints
-->
## 端點
```json
PATCH /_plugins/_security/api/tenants
```
<!-- spec_insert_end -->
<!-- spec_insert_start
api: security.patch_tenant
component: endpoints
omit_header: true
-->
```json
PATCH /_plugins/_security/api/tenants/{tenant}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `tenant` | 字串 | 否 | 要更新的租用戶名稱。若省略，則請求可修改多個租用戶。 |

## 請求本文欄位

請求本文為必要。它是一個 JSON 物件陣列。每個物件包含下列欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `op` | 字串 | 要執行的操作。有效值為 `add`、`remove`、`replace`、`move`、`copy` 及 `test`。 | 是 |
| `path` | 字串 | 要修改的路徑。當您指定租用戶名稱時，路徑相對於該租用戶，例如 `/description`。當您省略租用戶名稱時，路徑會以租用戶名稱開頭，例如 `/human_resources/description`。 | 是 |
| `value` | 物件 | 新值。`add`、`replace` 及 `test` 操作為必要。 | 否 |

## 請求範例

下列請求會更新 `human_resources` 租用戶的描述：

```json
PATCH _plugins/_security/api/tenants/human_resources
[
  {
    "op": "replace", "path": "/description", "value": "An updated description"
  }
]
```
{% include copy-curl.html security=true %}

下列請求會更新 `human_resources` 租用戶的描述，並新增 `another_tenant` 租用戶：

```json
PATCH _plugins/_security/api/tenants
[
  {
    "op": "replace",
    "path": "/human_resources/description",
    "value": "An updated description"
  },
  {
    "op": "add",
    "path": "/another_tenant",
    "value": {
      "description": "Another description."
    }
  }
]
```
{% include copy-curl.html security=true %}

## 回應範例

更新單一租用戶的請求會在回應中指名該租用戶：

```json
{
  "status": "OK",
  "message": "'human_resources' updated."
}
```

批次請求不會在回應中指名其變更的租用戶：

```json
{
  "status": "OK",
  "message": "Resource updated."
}
```
