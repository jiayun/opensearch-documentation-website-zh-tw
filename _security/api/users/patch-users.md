---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "修補使用者"
parent: Internal user APIs
grand_parent: Security APIs
nav_order: 20
---

# 修補使用者 API
**於 1.0 版推出**
{: .label .label-purple }

更新內部使用者而不取代使用者。指定使用者名稱可更新單一使用者的個別屬性，或省略使用者名稱，在單次呼叫中建立、更新或刪除多個使用者。

<!-- spec_insert_start
api: security.patch_users
component: endpoints
-->
## 端點
```json
PATCH /_plugins/_security/api/internalusers
```
<!-- spec_insert_end -->
<!-- spec_insert_start
api: security.patch_user
component: endpoints
omit_header: true
-->
```json
PATCH /_plugins/_security/api/internalusers/{username}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `username` | 字串 | 否 | 要更新的使用者名稱。若省略，請求可以修改多個使用者。 |

## 請求本文欄位

請求本文為必要項目。它是 JSON 物件的陣列。每個物件包含下列欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `op` | 字串 | 要執行的操作。有效值為 `add`、`remove`、`replace`、`move`、`copy` 和 `test`。 | 是 |
| `path` | 字串 | 要修改的路徑。當您指定使用者名稱時，路徑是相對於該使用者的路徑，例如 `/backend_roles`。當您省略使用者名稱時，路徑會指定使用者，例如 `/spock`。 | 是 |
| `value` | 物件 | 新值。對於 `add`、`replace` 和 `test` 操作，此欄位為必要項目。 | 否 |

## 請求範例

下列請求更新 `kirk` 使用者的後端角色：

```json
PATCH _plugins/_security/api/internalusers/kirk
[
  {
    "op": "replace",
    "path": "/backend_roles",
    "value": [
      "commander"
    ]
  }
]
```
{% include copy-curl.html security=true %}

下列請求新增 `spock` 和 `worf` 使用者，並移除 `riker` 使用者：

```json
PATCH _plugins/_security/api/internalusers
[
  {
    "op": "add",
    "path": "/spock",
    "value": {
      "password": "Str0ngPassw0rd_7741!",
      "backend_roles": [
        "science"
      ]
    }
  },
  {
    "op": "add",
    "path": "/worf",
    "value": {
      "password": "Str0ngPassw0rd_3390!",
      "backend_roles": [
        "security"
      ]
    }
  },
  {
    "op": "remove",
    "path": "/riker"
  }
]
```
{% include copy-curl.html security=true %}

## 回應範例

當您更新單一使用者時，回應會包含使用者名稱：

```json
{
  "status": "OK",
  "message": "'kirk' updated."
}
```

當您更新多個使用者時，回應如下：

```json
{
  "status": "OK",
  "message": "Resource updated."
}
```
