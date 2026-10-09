---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "授權權杖"
parent: Authentication APIs
grand_parent: Security APIs
nav_order: 60
---

# Authorization Token API
**1.0 版推出**
{: .label .label-purple }

傳回 `OK` 狀態，且 `message` 欄位為空。此端點接受 `POST` 請求，但不會核發權杖。

若要為服務帳戶產生授權權杖，請使用 [Generate User Token API]({{site.url}}{{site.baseurl}}/security/api/users/generate-user-token/)。

<!-- spec_insert_start
api: security.authtoken
component: endpoints
-->
## 端點
```json
POST /_plugins/_security/api/authtoken
```
<!-- spec_insert_end -->

## 請求範例

```json
POST _plugins/_security/api/authtoken
{}
```
{% include copy-curl.html security=true %}

## 回應範例

```json
{
  "status": "OK",
  "message": ""
}
```

## 回應本文欄位

回應本文是包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `status` | 字串 | 請求的狀態。一律為 `OK`。 |
| `message` | 字串 | 一律為空字串。 |
