---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenID Connect 疑難排解"
parent: OpenID Connect
grand_parent: Authentication backends
nav_order: 10
redirect_from:
  - /troubleshoot/openid-connect/
---

# OpenID Connect 疑難排解

使用下列疑難排解步驟，解決透過 Security 外掛程式使用 OpenID Connect 進行 OpenSearch 驗證時遇到的問題。


---

#### 目錄
- TOC
{:toc}


---

## 將記錄層級設為 debug

為協助排解 OpenID Connect 的問題，請將 OpenSearch 的記錄層級設為 `debug`。在 `config/log4j2.properties` 中新增下列各行，然後重新啟動節點：

```
logger.securityjwt.name = com.amazon.dlic.auth.http.jwt
logger.securityjwt.level = trace
```

此設定會將大量實用資訊輸出至您的記錄檔。如果這些資訊不足，您也可以將記錄層級設為 `trace`。


## 「嘗試從您的 IdP 取得端點時失敗」

此錯誤表示 Security 外掛程式無法連線至您 IdP 的中繼資料端點。請在 `opensearch_dashboards.yml` 中檢查下列設定：

```
plugins.security.openid.connect_url: "http://keycloak.example.com:8080/auth/realms/master/.well-known/openid-configuration"
```

如果此錯誤發生在 OpenSearch 上，請在 `config.yml` 中檢查下列設定：

```yml
openid_auth_domain:
  enabled: true
  order: 1
  http_authenticator:
    type: "openid"
    ...
    config:
      openid_connect_url: http://keycloak.examplesss.com:8080/auth/realms/master/.well-known/openid-configuration
    ...
```

<!-- vale off -->
## 「ValidationError：子項目 'opensearch_security' 失敗」
<!-- vale on -->

這表示缺少一或多個 OpenSearch Dashboards 組態設定。

請檢查 `opensearch_dashboards.yml`，並確認您已設定下列最低限度的組態：

```yml
plugins.security.openid.connect_url: "..."
plugins.security.openid.client_id: "..."
plugins.security.openid.client_secret: "..."
```


<!-- vale off -->
## 「驗證失敗。請提供新的權杖。」
<!-- vale on -->

此錯誤可能有數種根本原因。


### 殘留的 Cookie 或快取的認證資料

刪除所有快取的瀏覽器資料，或在私密瀏覽視窗中重試。


### 用戶端密鑰錯誤

若要將存取權杖換成身分權杖，大多數 IdP 都會要求您提供用戶端密鑰。請檢查 `opensearch_dashboards.yml` 中的用戶端密鑰是否與您 IdP 組態中的用戶端密鑰相符：

```
plugins.security.openid.client_secret: "..."
```


### 「無法從 JWT 宣告取得主體」

此錯誤會記錄在 OpenSearch 上，表示無法從 ID 權杖擷取使用者名稱。請確認下列設定與您 IdP 簽發的 JWT 中的宣告相符：

```
openid_auth_domain:
  enabled: true
  order: 1
  http_authenticator:
    type: "openid"
    ...
    config:
      subject_key: <subject key>
    ...
```

### 「無法使用 roles_key 從 JWT 宣告取得角色」

此錯誤表示您在 `config.yml` 中設定的角色鍵不存在於您 IdP 簽發的 JWT 中。請確認下列設定與您 IdP 簽發的 JWT 中的宣告相符：

```
openid_auth_domain:
  enabled: true
  order: 1
  http_authenticator:
    type: "openid"
    ...
    config:
      roles_key: <roles key>
    ...
```
