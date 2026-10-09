---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新載入傳輸憑證"
parent: Certificate APIs
grand_parent: Security APIs
nav_order: 40
---

# 重新載入傳輸憑證 API
**於 2.8 版推出**
{: .label .label-purple }

重新載入傳輸層通訊憑證，無須重新啟動節點。

此 API 保留給超級管理員使用。請使用管理員憑證進行驗證，而非使用者名稱與密碼。如需更多資訊，請參閱[API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
{: .note}

<!-- spec_insert_start
api: security.reload_transport_certificates
component: endpoints
-->
## 端點
```json
PUT /_plugins/_security/api/ssl/transport/reloadcerts
```
<!-- spec_insert_end -->

## 請求範例

```json
PUT _plugins/_security/api/ssl/transport/reloadcerts
```
{% include copy-curl.html security=true %}

## 回應範例

```json
{
  "message": "updated transport certs"
}
```

## 回應本文欄位

回應本文是包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `message` | 字串 | 確認傳輸憑證已更新的訊息。 |
