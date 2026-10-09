---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "變更密碼"
parent: Account APIs
grand_parent: Security APIs
nav_order: 10
redirect_from:
  - /api-reference/security/authentication/change-password/
---

# 變更密碼 API
**於 1.0 版推出**
{: .label .label-purple }

變更目前使用者的密碼。

<!-- spec_insert_start
api: security.change_password
component: endpoints
-->
## 端點
```json
PUT /_plugins/_security/api/account
```
<!-- spec_insert_end -->

## 請求本文欄位

請求本文為必要。其為包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `current_password` | 字串 | 使用者目前的密碼。 | 是 |
| `password` | 字串 | 新密碼。其必須符合由 `plugins.security.restapi.password_validation_regex` 設定的密碼原則，且不得與使用者名稱過於相似。 | 是 |

## 請求範例

```json
PUT /_plugins/_security/api/account
{
  "current_password": "OldPassword_4471!",
  "password": "NewPassword_8823!"
}
```
{% include copy-curl.html security=true %}

## 回應範例

```json
{
  "status": "OK",
  "message": "'pw-demo' updated."
}
```

## 回應本文欄位

回應本文為包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `status` | 字串 | 請求的狀態。成功的請求會傳回 `OK`。 |
| `message` | 字串 | 指出密碼已變更之使用者名稱的訊息。 |
