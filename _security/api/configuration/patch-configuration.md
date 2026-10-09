---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "修補組態"
parent: Security configuration APIs
grand_parent: Security APIs
nav_order: 20
redirect_from:
  - /api-reference/security/configuration/patch-configuration/
---

# Patch Security Configuration API
**於 2.10 版導入**
{: .label .label-purple }

Patch Configuration API 可讓您更新 Security 外掛程式組態的特定部分，而無需取代整個組態文件。

此作業可能輕易破壞您現有的安全性組態。我們強烈建議改用 `securityadmin.sh` 指令碼，其中包含可防止組態錯誤的驗證與防護機制。
{: .warning}

<!-- spec_insert_start
api: security.patch_configuration
component: endpoints
-->
## 端點
```json
PATCH /_plugins/_security/api/securityconfig
```
<!-- spec_insert_end -->

## 請求本文欄位

請求本文是**必要**的。它是一個 **JSON 物件陣列** (NDJSON)。每個物件具有下列欄位。

| 屬性 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `op` | **必要** | 字串 | 要執行的作業。有效值為 `add`、`remove`、`replace`、`move`、`copy` 與 `test`。 |
| `path` | **必要** | 字串 | 指向組態中要修改位置的 JSON 指標路徑。 |
| `value` | 選用 | 物件 | 作業要使用的值。`add`、`replace` 與 `test` 作業需要此欄位。 |

## 範例請求

```json
PATCH /_plugins/_security/api/securityconfig
[
  {
    "op": "replace",
    "path": "/config/dynamic/authc/basic_internal_auth_domain/description",
    "value": "Authenticate via HTTP Basic against the internal users database"
  }
]
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "status": "OK",
  "message": "Resource updated."
}
```

## 回應本文欄位

回應本文是一個具有下列欄位的 JSON 物件。

| 屬性 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `status` | 字串 | 請求的狀態。成功的請求會回傳 "OK"。 |
| `message` | 字串 | 描述作業結果的訊息。 |

## 啟用此 API

基於安全性考量，此 API 預設為停用。若要啟用，請在 `opensearch.yml` 中加入以下一行：

```yml
plugins.security.unsupported.restapi.allow_securityconfig_modification: true
```
{% include copy.html %}

如需授予 Security API 存取權限的更多資訊，請參閱 [API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
