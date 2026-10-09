---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得憑證"
parent: Certificate APIs
grand_parent: Security APIs
nav_order: 10
---

# 取得憑證 API
**於 2.0 版導入**
{: .label .label-purple }

擷取接收請求的節點上正在使用的 HTTP 與傳輸層憑證。若要擷取叢集中每個節點上正在使用的憑證，請使用 [Get All Certificates API]({{site.url}}{{site.baseurl}}/security/api/certificates/get-all-certificates/)。

此 API 僅供超級管理員（superadmin）使用。請使用管理員憑證進行驗證，而非使用者名稱與密碼。如需更多資訊，請參閱 [API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
{: .note}

<!-- spec_insert_start
api: security.get_certificates
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/ssl/certs
```
<!-- spec_insert_end -->

## 範例請求

```json
GET _plugins/_security/api/ssl/certs
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "http_certificates_list": [
    {
      "issuer_dn": "CN=Example Com Inc. Root CA,OU=Example Com Inc. Root CA,O=Example Com Inc.,DC=example,DC=com",
      "subject_dn": "CN=node-0.example.com,OU=node,O=node,L=test,C=de",
      "san": "[[2, localhost], [2, node-0.example.com], [7, 0:0:0:0:0:0:0:1], [7, 127.0.0.1], [8, 1.2.3.4.5.5]]",
      "not_before": "2024-02-20T17:03:25Z",
      "not_after": "2034-02-17T17:03:25Z"
    }
  ],
  "transport_certificates_list": [
    {
      "issuer_dn": "CN=Example Com Inc. Root CA,OU=Example Com Inc. Root CA,O=Example Com Inc.,DC=example,DC=com",
      "subject_dn": "CN=node-0.example.com,OU=node,O=node,L=test,C=de",
      "san": "[[2, localhost], [2, node-0.example.com], [7, 0:0:0:0:0:0:0:1], [7, 127.0.0.1], [8, 1.2.3.4.5.5]]",
      "not_before": "2024-02-20T17:03:25Z",
      "not_after": "2034-02-17T17:03:25Z"
    }
  ]
}
```

## 回應本文欄位

回應本文是一個包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `http_certificates_list` | 物件陣列 | 保護 REST 層的憑證。 |
| `transport_certificates_list` | 物件陣列 | 保護傳輸層的憑證。 |

每個憑證包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `issuer_dn` | 字串 | 簽發該憑證的憑證授權單位的辨別名稱。 |
| `subject_dn` | 字串 | 憑證主體的辨別名稱。 |
| `san` | 字串 | 憑證中的主體別名。 |
| `not_before` | 字串 | 憑證生效的日期與時間。 |
| `not_after` | 字串 | 憑證到期的日期與時間。 |
