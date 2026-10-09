---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新載入 HTTP 憑證"
parent: Certificate APIs
grand_parent: Security APIs
nav_order: 50
---

# 重新載入 HTTP 憑證 API
**2.8 版新增**
{: .label .label-purple }

在不重新啟動節點的情況下，重新載入 HTTP 層的通訊憑證。

此 API 僅供超級管理員 (superadmin) 使用。請使用管理員憑證進行驗證，而非使用者名稱與密碼。如需更多資訊，請參閱 [API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
{: .note}

<!-- spec_insert_start
api: security.reload_http_certificates
component: endpoints
-->
## 端點
```json
PUT /_plugins/_security/api/ssl/http/reloadcerts
```
<!-- spec_insert_end -->

## 請求範例

```json
PUT _plugins/_security/api/ssl/http/reloadcerts
```
{% include copy-curl.html security=true %}

## 回應範例

```json
{
  "message": "updated http certs"
}
```

## 回應本文欄位

回應本文是一個包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `message` | 字串 | 確認 HTTP 憑證已更新的訊息。 |
