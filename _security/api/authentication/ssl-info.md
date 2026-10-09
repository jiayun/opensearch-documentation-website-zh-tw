---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "SSL 資訊"
parent: Authentication APIs
grand_parent: Security APIs
nav_order: 50
---

# SSL Info API
**於 1.0 版推出**
{: .label .label-purple }

擷取 SSL 組態的相關資訊。

<!-- spec_insert_start
api: security.get_sslinfo
component: endpoints
-->
## 端點
```json
GET /_opendistro/_security/sslinfo
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: security.get_sslinfo
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `show_dn` | 布林值或字串 | 是否在回應中包含所有網域名稱。 |

<!-- spec_insert_end -->

## 範例請求

```json
GET _opendistro/_security/sslinfo
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "principal": null,
  "peer_certificates": "0",
  "ssl_protocol": "TLSv1.3",
  "ssl_cipher": "TLS_AES_128_GCM_SHA256",
  "ssl_provider_http": "JDK",
  "ssl_provider_transport_server": "JDK",
  "ssl_provider_transport_client": "JDK"
}
```

## 回應本文欄位

回應本文是包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `principal` | 字串 | 驗證該請求的用戶端憑證辨別名稱，或當請求以其他方式驗證時為 `null`。 |
| `peer_certificates` | 字串 | 用戶端提供的憑證數量，以字串形式傳回。未提供任何用戶端憑證的請求會傳回 `0`。 |
| `ssl_protocol` | 字串 | 為該請求協商出的 TLS 通訊協定版本。 |
| `ssl_cipher` | 字串 | 為該請求協商出的加密套件。 |
| `ssl_provider_http` | 字串 | HTTP 層所使用的 TLS 提供者。 |
| `ssl_provider_transport_server` | 字串 | 傳入傳輸層連線所使用的 TLS 提供者。 |
| `ssl_provider_transport_client` | 字串 | 傳出傳輸層連線所使用的 TLS 提供者。 |
| `peer_certificates_list` | 字串陣列 | 用戶端所提供憑證的辨別名稱，或當用戶端未提供任何憑證時為 `null`。僅當 `show_dn` 為 `true` 時傳回。 |
| `local_certificates_list` | 字串陣列 | 節點所提供憑證的辨別名稱。僅當 `show_dn` 為 `true` 時傳回。 |
