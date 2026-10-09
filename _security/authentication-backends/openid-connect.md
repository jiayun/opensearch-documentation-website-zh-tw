---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenID Connect
parent: Authentication backends
nav_order: 50
has_children: true
has_toc: false
redirect_from:
  - /security-plugin/configuration/openid-connect/
---

# OpenID Connect 驗證

安全性外掛程式可與使用 OpenID Connect 標準的身分提供者整合。此功能可啟用下列項目：

* 自動組態

  將安全性外掛程式指向您身分提供者 (IdP) 的中繼資料，安全性外掛程式便會使用該資料進行組態。

* 自動擷取金鑰

  安全性外掛程式會自動從您 IdP 的 JSON Web Key Set (JWKS) 端點擷取公開金鑰，以驗證 JSON Web Token (JWT)。您不需要在 `config.yml` 中設定金鑰或共用密鑰。

* 金鑰輪替

  您可以直接在 IdP 中變更用於簽署 JWT 的金鑰。如果安全性外掛程式偵測到未知的金鑰，會嘗試從 IdP 擷取該金鑰。此輪替對使用者而言是透明的。

* 將 OpenSearch Dashboards 做為單一登入，或在 Dashboards 登入視窗中做為多種驗證類型中的其中一個選項。


## 設定 OpenID Connect 整合

若要與 OpenID IdP 整合，請設定驗證網域，並選擇 `openid` 做為 HTTP 驗證類型。JWT 已包含驗證請求所需的所有資訊，因此請將 `challenge` 設為 `false`，並將 `authentication_backend` 設為 `noop`。

這是最小組態：

```yml
_meta:
  type: "config"
  config_version: 2

config:
  dynamic:
    authc:
      openid_auth_domain:
        http_enabled: true
        transport_enabled: true
        order: 0
        http_authenticator:
          type: openid
          challenge: false
          config:
            subject_key: preferred_username
            roles_key: roles
            openid_connect_url: https://keycloak.example.com:8080/auth/realms/master/.well-known/openid-configuration
            required_audience: your-openid-client-id
        authentication_backend:
          type: noop
```

下表顯示組態參數。

名稱 | 說明
:--- | :---
`openid_connect_url` | 您 IdP 的 URL，安全性外掛程式可在該處找到 OpenID Connect 中繼資料/組態設定。此 URL 因 IdP 而異。當您使用 OpenID Connect 做為後端時為必要。
`jwt_header` | 儲存權杖的 HTTP 標頭。通常是帶有 `Bearer` 配置的 `Authorization` 標頭：`Authorization: Bearer <token>`。選用。預設為 `Authorization`。
`jwt_url_parameter` | 如果權杖不是透過 HTTP 標頭傳輸，而是做為 URL 參數傳輸，請在此定義參數的名稱。選用。
`subject_key` | JSON 承載中儲存使用者名稱的索引鍵。若未定義，則使用 [subject](https://tools.ietf.org/html/rfc7519#section-4.1.2) 註冊聲明。大多數 IdP 提供者使用 `preferred_username` 聲明。若要從巢狀 JWT 聲明中擷取使用者名稱，您可以將 `subject_key` 設定為清單。選用。
`roles_key` | JSON 承載中儲存使用者角色的索引鍵。值必須是以逗號分隔的角色清單。只有在您想要使用 JWT 中的角色時，才需要此索引鍵。您可以將 `roles_key` 設定為清單，以從巢狀 JWT 聲明中擷取角色。
`required_audience` | JWT 必須指定的對象名稱。您可以指定單一值 (例如 `project1`) 或多個以逗號分隔的值 (例如 `project1,admin`)。如果您指定多個值，JWT 必須至少有一個必要的對象。此參數對應於 [JWT 的 `aud` 聲明](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3)。
`required_issuer` | 儲存於 JSON 承載中之 JWT 的目標簽發者。這對應於 [JWT 的 `iss` 聲明](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.1)。
`jwt_clock_skew_tolerance_seconds` | 指定一段以秒為單位的時間範圍，以補償 JWT 驗證伺服器與 OpenSearch 節點時鐘時間之間的任何差異，從而避免因時間不一致而導致的驗證失敗。安全性外掛程式預設為 30 秒。使用此設定可套用自訂值。
`cache_jwks_endpoint` | 是否快取從 IdP 的 JWKS 端點擷取的公開金鑰。快取這些金鑰可減少 JWT 驗證期間傳送至 IdP 的請求數。預設為 `false`。如需詳細資訊，請參閱[快取與效能](#caching-and-performance)。


## OpenID Connect URL

OpenID Connect 指定了各種用於整合的端點。最重要的端點是 `well-known`，其中列出安全性外掛程式的端點與其他組態選項。

此 URL 因 IdP 而異，但通常以 `/.well-known/openid-configuration` 結尾。

Keycloak 範例：

```
http(s)://<server>:<port>/auth/realms/<realm>/.well-known/openid-configuration
```

安全性外掛程式所需的主要資訊是 `jwks_uri`。此 URI 指定可在何處找到 JWKS 格式的 IdP 公開金鑰。例如：

```
jwks_uri: "https://keycloak.example.com:8080/auth/realms/master/protocol/openid-connect/certs"
```

```
{
   keys:[
      {
         kid:"V-diposfUJIk5jDBFi_QRouiVinG5PowskcSWy5EuCo",
         kty:"RSA",
         alg:"RS256",
         use:"sig",
         n:"rI8aUrAcI_auAdF10KUopDOmEFa4qlUUaNoTER90XXWADtKne6VsYoD3ZnHGFXvPkRAQLM5d65ScBzWungcbLwZGWtWf5T2NzQj0wDyquMRwwIAsFDFtAZWkXRfXeXrFY0irYUS9rIJDafyMRvBbSz1FwWG7RTQkILkwiC4B8W1KdS5d9EZ8JPhrXvPMvW509g0GhLlkBSbPBeRSUlAS2Kk6nY5i3m6fi1H9CP3Y_X-TzOjOTsxQA_1pdP5uubXPUh5YfJihXcgewO9XXiqGDuQn6wZ3hrF6HTlhNWGcSyQPKh1gEcmXWQlRENZMvYET-BuJEE7eKyM5vRhjNoYR3w",
         e:"AQAB"
      }
   ]
}
```

如需 IdP 端點的詳細資訊，請參閱下列內容：

- [Okta](https://developer.okta.com/docs/api/resources/oidc#well-knownopenid-configuration)
- [Keycloak](https://www.keycloak.org/guides.html#securing-apps)
- [Auth0](https://auth0.com/docs/protocols/oidc/openid-connect-discovery)
- [Connect2ID](https://connect2id.com/products/server/docs/api/discovery)
- [Salesforce](https://help.salesforce.com/articleView?id=remoteaccess_using_openid_discovery_endpoint.htm&type=5)
- [IBM OpenID Connect](https://www.ibm.com/support/knowledgecenter/en/SSEQTP_8.5.5/com.ibm.websphere.wlp.doc/ae/rwlp_oidc_endpoint_urls.html)

## 快取與效能

根據預設，安全性外掛程式不會快取 OpenID Connect 驗證的 JWKS 端點回應。若不快取，安全性外掛程式每次需要重新整理金鑰集時，都會從 IdP 擷取 JWKS，這可能會增加網路流量，並對 IdP 造成不必要的負載。

您可以在 OpenID Connect 驗證網域組態中將 `cache_jwks_endpoint` 設為 `true`，以啟用快取：

```yml
http_authenticator:
  type: openid
  challenge: false
  config:
    subject_key: preferred_username
    roles_key: roles
    openid_connect_url: https://keycloak.example.com:8080/auth/realms/master/.well-known/openid-configuration
    cache_jwks_endpoint: true
```
{% include copy.html %}

啟用快取後，安全性外掛程式會快取從 JWKS 端點擷取的公開金鑰，並在後續的 JWT 驗證中重複使用這些金鑰。快取的金鑰集會在下列情況下重新整理：

- JWT 包含目前快取中找不到的 `kid` (金鑰 ID)。
- IdP 中觸發了金鑰輪替。

對於使用 `jwks_uri` 設定的 JWT 驗證，預設會啟用 `cache_jwks_endpoint`。對於 OpenID Connect 驗證，您必須明確地將 `cache_jwks_endpoint` 設為 `true` 才能啟用快取。
{: .note }


## JWT 驗證的時間差補償

有時您可能會發現驗證伺服器與 OpenSearch 節點之間的時鐘時間並未完全同步。在這種情況下，即使只差幾秒，簽發或接收 JWT 的系統在嘗試驗證 `nbf`（不得早於）與 `exp`（到期時間）宣告時，可能會因為時間差而無法驗證使用者。

預設情況下，Security 會提供 30 秒的緩衝時間，以補償伺服器時鐘之間可能的不一致。若要為此功能設定自訂值並覆寫預設值，您可以將 `jwt_clock_skew_tolerance_seconds` 設定加入 `config.yml`：

```yml
http_authenticator:
  type: openid
  challenge: false
  config:
    subject_key: preferred_username
    roles_key: roles
    openid_connect_url: https://keycloak.example.com:8080/auth/realms/master/.well-known/openid-configuration
    jwt_clock_skew_tolerance_seconds: 20
```


## 取得公開金鑰

當 IdP 產生並簽署 JWT 時，必須將金鑰的 ID 加入 JWT 標頭。例如：

```
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "V-diposfUJIk5jDBFi_QRouiVinG5PowskcSWy5EuCo"
}
```

依照 [OpenID Connect 規格](https://openid.net/specs/openid-connect-messages-1_0-20.html)，`kid` (key ID) 為必要項目。如果 IdP 未將 `kid` 欄位加入 JWT，權杖驗證將無法運作。

如果 Security 外掛程式收到含有未知 `kid` 的 JWT，它會造訪 IdP 的 `jwks_uri` 並擷取所有可用且有效的金鑰。這些金鑰會被使用並快取，直到透過擷取另一個未知的金鑰 ID 觸發重新整理為止。


## 金鑰輪替與多個公開金鑰

Security 外掛程式可以同時維護多個有效的公開金鑰。OpenID 規格並未定義公開金鑰的有效期限，因此金鑰會一直有效，直到它從 IdP 的有效金鑰清單中移除，且有效金鑰清單已重新整理為止。

如果您想在 IdP 中輪替金鑰，請遵循以下最佳做法：

- 在 IdP 中建立新的金鑰組，並將新金鑰的優先順序設定為高於目前使用的金鑰。

  您的 IdP 會優先使用這個新金鑰，而非舊金鑰。

- 當新的 `kid` 首次出現在 JWT 中時，Security 外掛程式會重新整理金鑰清單。

  此時，舊金鑰與新金鑰皆為有效。以舊金鑰簽署的權杖也仍然有效。

- 當最後一個以舊金鑰簽署的 JWT 逾時後，即可從 IdP 中移除該舊金鑰。

如果您必須立即更換公開金鑰，也可以先刪除舊金鑰，再建立新金鑰。在這種情況下，所有以舊金鑰簽署的 JWT 會立即失效。


## TLS 設定

為防止中間人攻擊，您應使用 TLS 保護 Security 外掛程式與 IdP 之間的連線。


### 啟用 TLS

使用下列參數啟用連線至 IdP 的 TLS：

```yml
config:
  openid_connect_idp:
    enable_ssl: <true|false>
    verify_hostnames: <true|false>
```

名稱 | 說明
:--- | :---
`enable_ssl` | 是否使用 TLS。預設為 `false`。
`verify_hostnames` | 是否驗證 IdP TLS 憑證的主機名稱。預設為 `true`。


### 憑證驗證

若要驗證 IdP 的 TLS 憑證，請設定 IdP 根 CA 的路徑或根憑證的內容：

```yml
config:
  openid_connect_idp:
    enable_ssl: true
    pemtrustedcas_filepath: /full/path/to/trusted_cas.pem
```

```yml
config:
  openid_connect_idp:
    enable_ssl: true
    pemtrustedcas_content: |-
      -----BEGIN CERTIFICATE-----
      MIID/jCCAuagAwIBAgIBATANBgkqhkiG9w0BAQUFADCBjzETMBEGCgmSJomT8ixk
      ARkWA2NvbTEXMBUGCgmSJomT8ixkARkWB2V4YW1wbGUxGTAXBgNVBAoMEEV4YW1w
      bGUgQ29tIEluYy4xITAfBgNVBAsMGEV4YW1wbGUgQ29tIEluYy4gUm9vdCBDQTEh
      ...
      -----END CERTIFICATE-----
```


| 名稱 | 說明 |
| :--- | :--- |
| `pemtrustedcas_filepath` | 包含 IdP 根 CA 之 PEM 檔案的絕對路徑。 |
| `pemtrustedcas_content` | IdP 的根 CA 內容。若已設定 `pemtrustedcas_filepath` 則無法使用。 |


### TLS 用戶端驗證

若要使用 TLS 用戶端驗證，請設定 Security 外掛程式應傳送以進行 TLS 用戶端驗證的 PEM 憑證與私密金鑰（或其內容）：

```yml
config:
  openid_connect_idp:
    enable_ssl: true
    pemkey_filepath: /full/path/to/private.key.pem
    pemkey_password: private_key_password
    pemcert_filepath: /full/path/to/certificate.pem
```

```yml
config:
  openid_connect_idp:
    enable_ssl: true
    pemkey_content: |-
      -----BEGIN PRIVATE KEY-----
      MIID2jCCAsKgAwIBAgIBBTANBgkqhkiG9w0BAQUFADCBlTETMBEGCgmSJomT8ixk
      ARkWA2NvbTEXMBUGCgmSJomT8ixkARkWB2V4YW1wbGUxGTAXBgNVBAoMEEV4YW1w
      bGUgQ29tIEluYy4xJDAiBgNVBAsMG0V4YW1wbGUgQ29tIEluYy4gU2lnbmluZyBD
      ...
      -----END PRIVATE KEY-----
    pemkey_password: private_key_password
    pemcert_content: |-
      -----BEGIN CERTIFICATE-----
      MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCHRZwzwGlP2FvL
      oEzNeDu2XnOF+ram7rWPT6fxI+JJr3SDz1mSzixTeHq82P5A7RLdMULfQFMfQPfr
      WXgB4qfisuDSt+CPocZRfUqqhGlMG2l8LgJMr58tn0AHvauvNTeiGlyXy0ShxHbD
      ...
      -----END CERTIFICATE-----
```

名稱 | 說明
:--- | :---
`enable_ssl_client_auth` | 是否將用戶端憑證傳送至 IdP 伺服器。預設為 `false`。
`pemcert_filepath` | 用戶端憑證的絕對路徑。
`pemcert_content` | 用戶端憑證的內容。若已設定 `pemcert_filepath` 則無法使用。
`pemkey_filepath` | 包含用戶端憑證私密金鑰之檔案的絕對路徑。
`pemkey_content` | 用戶端憑證私密金鑰的內容。若已設定 `pemkey_filepath` 則無法使用。
`pemkey_password` | 私密金鑰的密碼（如有）。


### 啟用的加密套件與通訊協定

您可以使用下列金鑰限制允許的加密套件與 TLS 通訊協定。

名稱 | 說明
:--- | :---
`enabled_ssl_ciphers` | 陣列。啟用的 TLS 加密套件。僅支援 Java 格式。
`enabled_ssl_protocols` | 陣列。啟用的 TLS 通訊協定。僅支援 Java 格式。


## （進階）DoS 防護

為協助防範阻斷服務 (DoS) 攻擊，Security 外掛程式在特定時間範圍內僅允許最大數量的新金鑰 ID。如果新金鑰 ID 的數量超過此門檻，Security 外掛程式會傳回 HTTP 狀態碼 503 (Service Unavailable)，並拒絕查詢 IdP。預設情況下，Security 外掛程式在 10 秒內不允許超過 10 個未知金鑰 ID。下表說明如何修改這些設定。

名稱 | 說明
:--- | :---
`refresh_rate_limit_count` | 時間範圍內允許的未知金鑰 ID 最大數量。預設為 10。
`refresh_rate_limit_time_window_ms` | 檢查未知金鑰 ID 最大數量時使用的時間範圍，單位為毫秒。預設為 10000（10 秒）。


## OpenSearch Dashboards 單一登入

將以下內容加入 `opensearch_dashboards.yml` 以啟用 OpenID Connect：

```
opensearch_security.auth.type: "openid"
```


### 組態

OpenID Connect 提供者通常會以 JSON 格式在 *中繼資料 URL* 下發布其組態。因此，大多數設定可以自動擷取，使 OpenSearch Dashboards 的組態變得非常精簡。最重要的設定如下：

- [連線 URL](#openid-connect-url)
- 用戶端 ID

  每個 IdP 都可以承載多個具有不同設定與驗證通訊協定的用戶端（有時稱為應用程式）。啟用 OpenID Connect 時，您應在 IdP 中為 OpenSearch Dashboards 建立新的用戶端。用戶端 ID 可唯一識別 OpenSearch Dashboards。

- 用戶端密碼

  除了 ID 之外，每個用戶端還會被指派一個用戶端密碼 (client secret)。用戶端密碼通常在建立用戶端時產生。應用程式只有在提供用戶端密碼時，才能取得身分權杖。您可以在 IdP 上該用戶端的設定中找到此密碼。


### 組態設定

名稱 | 說明
:--- | :---
`opensearch_security.openid.connect_url` | IdP 發佈 OpenID 中繼資料的 URL。必要。
`opensearch_security.openid.client_id` | 在您的 IdP 中設定的 OpenID Connect 用戶端 ID。必要。
`opensearch_security.openid.client_secret` | 在您的 IdP 中設定的 OpenID Connect 用戶端密碼。必要。
`opensearch_security.openid.scope` | IdP 所簽發的[身分權杖範圍](https://openid.net/specs/openid-connect-messages-1_0-20.html#scopes)。選用。預設為 `openid profile email address phone`。
`opensearch_security.openid.header` | JWT 權杖的 HTTP 標頭名稱。選用。預設為 `Authorization`。
`opensearch_security.openid.logout_url` | 您 IdP 的登出 URL。選用。僅在您的 IdP 未於其中繼資料中發佈登出 URL 時才需要。
`opensearch_security.openid.base_redirect_url` | 將傳送至您 IdP 的重新導向 URL 基底。選用。僅在 OpenSearch Dashboards 位於反向代理後方時才需要，此時它應與 `opensearch_dashboards.yml` 中的 `server.host` 和 `server.port` 不同。
`opensearch_security.openid.trust_dynamic_headers` | 從反向代理 HTTP 標頭 (`X-Forwarded-Host` / `X-Forwarded-Proto`) 計算 `base_redirect_url`。選用。預設為 `false`。
`opensearch_security.openid.root_ca` | 根 CA 的路徑 (PEM 格式)，您 IdP 的憑證可與其相符或鏈結至其。選用。
`opensearch_security.openid.certificate` | 從您的 IdP 取得端點時，用於 mTLS 的憑證鏈 (PEM 格式)。選用。
`opensearch_security.openid.private_key` | 從您的 IdP 取得端點時，用於 mTLS 的私密金鑰 (PEM 格式)。選用。
`opensearch_security.openid.passphrase` | 用於單一 `private_key` 或 `pfx` 的通行短語。選用。
`opensearch_security.openid.pfx` | 從您的 IdP 取得端點時，用於 mTLS 的 PFX 或 PKCS12 編碼私密金鑰與憑證鏈。為 `certificate` 和 `private_key` 的替代方案。選用。
`opensearch_security.openid.verify_hostnames` | 是否驗證 IdP TLS 憑證的主機名稱。預設為 `true`。選用。 


### 組態範例

```yml
# Enable OpenID authentication
opensearch_security.auth.type: "openid"

# The IdP metadata endpoint
opensearch_security.openid.connect_url: "http://keycloak.example.com:8080/auth/realms/master/.well-known/openid-configuration"

# The ID of the OpenID Connect client in your IdP
opensearch_security.openid.client_id: "opensearch-dashboards-sso"

# The client secret of the OpenID Connect client
opensearch_security.openid.client_secret: "a59c51f5-f052-4740-a3b0-e14ba355b520"

# mTLS Options for obtaining endpoints from IdP
opensearch_security.openid.root_ca: /usr/share/opensearch-dashboards/config/certs/ca.pem
opensearch_security.openid.certificate: /usr/share/opensearch-dashboards/config/certs/cert.pem
opensearch_security.openid.private_key: /usr/share/opensearch-dashboards/config/certs/key.pem

# Use HTTPS instead of HTTP
opensearch.url: "https://<hostname>.com:<http port>"

# Configure the OpenSearch Dashboards internal server user
opensearch.username: "kibanaserver"
opensearch.password: "kibanaserver"

# Disable SSL verification when using self-signed demo certificates
opensearch.ssl.verificationMode: none

# allowlist basic headers and multi-tenancy header
opensearch.requestHeadersAllowlist: ["Authorization", "securitytenant"]
```

若要在 Dashboards 登入視窗中將 OpenID Connect 與其他驗證類型一併納入，請參閱[設定登入選項]({{site.url}}{{site.baseurl}}/security/configuration/multi-auth/)。
{: .note } 

### 其他參數

部分身分提供者需要自訂參數才能完成驗證程序。您可以在 `opensearch_security.openid.additional_parameters` 命名空間下的 `opensearch_dashboards.yml` 組態檔案中新增自訂參數。您可以透過傳送 GET 請求至您的身分提供者來找到這些其他參數。此功能可讓您與各種身分提供者通訊時享有更大的彈性與自訂空間。

在下列範例中，兩個自訂參數 `foo` 和 `acr_values` 及其值 `bar` 和 `1`，是透過對 OpenID 提供者傳送 GET 請求找到的：

```yml
opensearch_security.openid.additional_parameters.foo: "bar"
opensearch_security.openid.additional_parameters.acr_values: "1"
```
{% include copy.html %}



#### 使用其他 Cookie 的工作階段管理

為了改善工作階段管理——尤其是對於被指派多個角色的使用者——Dashboards 提供了一個選項，可將 Cookie 承載內容分割成多個 Cookie，並在收到時重新合併承載內容。這有助於避免較大的 OpenID Connect 斷言超出每個 Cookie 的大小限制。下列範例中的兩項設定可讓您為其他 Cookie 設定前置名稱，並指定其數量。它們會新增至 `opensearch_dashboards.yml` 檔案。其他 Cookie 的預設數量為三個：

```yml
opensearch_security.openid.extra_storage.cookie_prefix: security_authentication_oidc
opensearch_security.openid.extra_storage.additional_cookies: 3
```

請注意，減少其他 Cookie 的數量可能會導致變更前正在使用的一些 Cookie 停止運作。我們建議建立固定的其他 Cookie 數量，之後就不要變更組態。

如果來自 IdP 的 ID 權杖特別大，OpenSearch 可能會在伺服器記錄檔中記錄驗證錯誤，指出 HTTP 標頭過大。在這種情況下，您可以增加 `opensearch.yml` 檔案中 `http.max_header_size` 設定的值。
{: .tip }


### OpenSearch 安全性組態

OpenSearch Dashboards 並非嚴格要求 HTTP 基本驗證。您可以將其設定為僅使用 OpenID Connect 進行驗證。不過，如果您需要支援多種驗證方法 (例如，使用者使用 OpenID，自動化服務使用 HTTP 基本驗證)，則必須設定多個驗證網域。

如果您使用 OpenID 作為主要方法，請將 `challenge` 旗標設為 `false`。

您也可以使用其他方法 (例如用戶端憑證) 來驗證內部 Dashboards 伺服器使用者，而不需要 HTTP 基本驗證。

在 `config.yml` 中修改並套用下列範例設定：

```yml
_meta:
  type: "config"
  config_version: 2

config:
  dynamic:
    authc:
      basic_internal_auth_domain:
        http_enabled: true
        transport_enabled: true
        order: 0
        http_authenticator:
          type: basic
          challenge: false
        authentication_backend:
          type: internal
      openid_auth_domain:
        http_enabled: true
        transport_enabled: true
        order: 1
        http_authenticator:
          type: openid
          challenge: false
          config:
            subject_key: preferred_username
            roles_key: roles
            openid_connect_url: https://keycloak.example.com:8080/auth/realms/master/.well-known/openid-configuration
        authentication_backend:
          type: noop
```

## 使用 Keycloak 的 Docker 範例

下列步驟使用 Docker 和 [Keycloak IdP](https://www.keycloak.org/) 設定基本的驗證後端：


1. 下載並解壓縮[範例 OpenID Connect zip 檔案]({{site.url}}{{site.baseurl}}/assets/examples/oidc_example.zip)
2. 在 `.env` 檔案中為 `admin` 使用者更新為高強度密碼。
3. 將 `config.yml` 和 `opensearch_dashboards.yml` 中的 `{IP}` 預留位置替換為本機的 IP。
4. 檢閱下列檔案：
  - `docker-compose.yml` 定義了單一 OpenSearch 節點、OpenSearch Dashboards 及 Keycloak 伺服器。
  - `new-realm.json` 指定 [realm](https://www.keycloak.org/docs/latest/server_admin/#core-concepts-and-terms) 的詳細資訊。在此範例中，realm 名稱為 `new`。
  - `config.yml` 設定 `basic_internal_auth_domain` 和 `oidc_auth_domain`。
  - `opensearch_dashboards.yml` 應指向 Keycloak 進行驗證。請確認 `opensearch_security.openid.connect_url` 設定指向 realm 的 URL。
5. 在命令列執行 `docker compose up`。
6. 前往 `http://localhost:5601` 存取 OpenSearch Dashboards，並使用 `new-realm.json` 檔案中設定的使用者名稱 `testuser` 和密碼 `testpassword` 登入。 

登入後，`testuser` 會從 Keycloak 取得後端角色 `admin`，此角色對應至 `all_access` OpenSearch 角色。您可以在 http://localhost:8080 使用 Keycloak 管理主控台，以使用者名稱 `admin` 和密碼 `admin` 管理這些後端角色。

## 疑難排解

- 如需常見 OpenID Connect 組態問題的解決方式，請參閱[OpenID Connect 疑難排解]({{site.url}}{{site.baseurl}}/security/authentication-backends/troubleshoot-openid-connect/)。
