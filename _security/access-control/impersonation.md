---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用者身分模擬"
parent: Access control
nav_order: 105
redirect_from:
 - /security-plugin/access-control/impersonation/
---

# 使用者身分模擬

使用者身分模擬可讓具備特殊權限的使用者以其他使用者的身分操作，而無需知道或存取被模擬使用者的憑證。

身分模擬可用於測試與疑難排解，或讓系統服務安全地以某位使用者的身分操作。

身分模擬可發生在 REST 介面或傳輸層。


## REST 介面

若要允許某位使用者模擬另一位使用者，請將下列內容新增至 `opensearch.yml`：

```yml
plugins.security.authcz.rest_impersonation_user:
  <AUTHENTICATED_USER>:
    - <IMPERSONATED_USER_1>
    - <IMPERSONATED_USER_2>
```

被模擬使用者欄位支援萬用字元。將其設為 `*` 可讓 `AUTHENTICATED_USER` 模擬任何使用者。


## 傳輸介面

同樣地，新增下列內容以啟用傳輸層身分模擬：

```yml
plugins.security.authcz.impersonation_dn:
  "CN=spock,OU=client,O=client,L=Test,C=DE":
    - worf
```


## 模擬使用者

若要模擬另一位使用者，請向系統提交請求，並將 HTTP 標頭 `opendistro_security_impersonate_as` 設為要模擬的使用者名稱。一個不錯的測試方式是對 `_plugins/_security/authinfo` URI 發出 GET 請求：

```bash
curl -XGET -u 'admin:<custom-admin-password>' -k -H "opendistro_security_impersonate_as: user_1" https://localhost:9200/_plugins/_security/authinfo?pretty
```
