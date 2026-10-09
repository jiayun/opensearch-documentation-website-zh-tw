---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: SAML
parent: Authentication backends
nav_order: 55
has_children: true
has_toc: false
redirect_from:
  - /security/configuration/saml/
  - /security-plugin/configuration/saml/
---

# SAML 驗證

安全性外掛程式支援透過 SAML 單一登入進行使用者驗證。安全性外掛程式實作了 SAML 2.0 協定的網頁瀏覽器 SSO 規範。

此規範適用於網頁瀏覽器。它並非對安全性外掛程式驗證使用者的通用方式，因此其主要使用情境是支援 OpenSearch Dashboards 單一登入。


## Docker 範例

我們提供一個功能完整的範例，可協助您了解如何搭配 OpenSearch Dashboards 使用 SAML。

1. 前往 demos 儲存庫的 [saml-demo 分支](https://github.com/opensearch-project/demos/tree/saml-demo) 並下載到您選擇的資料夾。如果您不熟悉如何使用 GitHub，請參閱 [OpenSearch 入門指南](https://github.com/opensearch-project/demos/blob/main/ONBOARDING.md) 以取得操作說明。

1. 瀏覽至 `demo` 資料夾：
   ```zsh
   $ cd <path-to-demos-folder>/demo
   ```

1. 視需要檢閱下列檔案：

   * `.env`：
     * 定義要使用的 OpenSearch 與 OpenSearch Dashboards 版本。預設為最新版本 ({{site.opensearch_major_minor_version}})。
     * 定義 2.12 及更新版本所需的 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 變數。
   * `./custom-config/opensearch_dashboards.yml`：包含預設 `opensearch_dashboards.yml` 檔案的 SAML 設定。
   * `./custom-config/config.yml`：設定 SAML 以進行驗證。
   * `docker-compose.yml`：定義一個 OpenSearch 伺服器節點、一個 OpenSearch Dashboards 伺服器節點，以及一個 SAML 伺服器節點。
   * `./saml/config/authsources.php`：包含可由此 SAML 網域驗證的使用者清單。

1. 從命令列執行：
   ```zsh
   $ docker compose up.
   ```

1. 在 [http://localhost:5601](http://localhost:5601){:target='\_blank'} 存取 OpenSearch Dashboards。

1. 選取 `Log in with single sign-on`。這會將您重新導向至 SAML 登入頁面。

1. 使用 `./saml/config/authsources.php` 中定義的使用者 (例如使用者名稱 `user1`、密碼 `user1pass`) 登入 OpenSearch Dashboards。

1. 登入後，請注意畫面右上角顯示的使用者 ID 與 SAML 伺服器 `./saml/config/authsources.php` 中定義之使用者的 `NameID` 屬性相同 (亦即 `user1` 的 `saml-test`)。

1. 如果您想檢查 SAML 伺服器，請執行 `docker ps` 以找出其容器 ID，然後執行 `docker exec -it <container-id> /bin/bash`。

   您可能會發現，檢閱 `/var/www/simplesamlphp/config/` 與 `/var/www/simplesamlphp/metadata/` 目錄的內容特別有幫助。


## 啟用 SAML

若要使用 SAML 進行驗證，您需要在 `config/opensearch-security/config.yml` 的 `authc` 區段中設定對應的驗證網域。由於 SAML 僅在 HTTP 層運作，您不需要任何 `authentication_backend`，並可將其設為 `noop`。請將本章節中所有 SAML 專屬的組態選項放在 SAML HTTP 驗證器的 `config` 區段中：

```yml
_meta:
  type: "config"
  config_version: 2

config:
  dynamic:
    authc:
      saml_auth_domain:
        http_enabled: true
        transport_enabled: false
        order: 1
        http_authenticator:
          type: saml
          challenge: true
          config:
            idp:
              metadata_file: okta.xml
              ...
        authentication_backend:
          type: noop
```

在 `config.yml` 中設定 SAML 之後，您還必須[在 OpenSearch Dashboards 中啟用](#opensearch-dashboards-configuration)。


## 執行多個驗證網域

我們建議至少新增一個其他驗證網域，例如 LDAP 或內部使用者資料庫，以支援不使用 SAML 的 OpenSearch API 存取。對於 OpenSearch Dashboards 及內部 OpenSearch Dashboards 伺服器使用者，您還必須新增另一個支援基本驗證的驗證網域。此驗證網域應放在鏈結中的第一個，且 `challenge` 旗標必須設為 `false`：

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
      saml_auth_domain:
        http_enabled: true
        transport_enabled: false
        order: 1
        http_authenticator:
          type: saml
          challenge: true
          config:
            ...
        authentication_backend:
          type: noop
```


## 身分提供者中繼資料

SAML 身分提供者 (IdP) 會提供 SAML 2.0 中繼資料檔案，說明 IdP 的功能與組態。安全性外掛程式可從 URL 或檔案讀取 IdP 中繼資料。您所做的選擇取決於您的 IdP 與您的偏好。SAML 2.0 中繼資料檔案為必要。

名稱 | 說明
:--- | :---
`idp.metadata_file` | 您 IdP 的 SAML 2.0 中繼資料檔案路徑。請將中繼資料檔案放在 OpenSearch 的 `config` 目錄中。此路徑必須相對於 `config` 目錄指定。若未設定 `idp.metadata_url` 則為必要。
`idp.metadata_url` | 您 IdP 的 SAML 2.0 中繼資料 URL。若未設定 `idp.metadata_file` 則為必要。


## IdP 與服務提供者實體 ID

實體 ID 是 SAML 實體 (IdP 或服務提供者 (SP)) 的全域唯一名稱。IdP 實體 ID 通常由您的 IdP 提供。SP 實體 ID 是您 IdP 中已設定之應用程式或用戶端的名稱。我們建議為 OpenSearch Dashboards 新增應用程式，並使用您 OpenSearch Dashboards 安裝的 URL 作為 SP 實體 ID。

名稱 | 說明
:--- | :---
`idp.entity_id` | 您 IdP 的實體 ID。必要。
`sp.entity_id` | 服務提供者的實體 ID。必要。

## JWT 驗證的時間差異補償

您有時可能會發現驗證伺服器與 OpenSearch 節點之間的時鐘時間並未完全同步。在這種情況下，即使只差幾秒，簽發或接收 JSON Web Token (JWT) 的系統可能會嘗試驗證 `nbf` (not before) 與 `exp` (expiration) 宣告，並因時間差異而無法驗證使用者。

根據預設，OpenSearch Security 允許 30 秒的時間範圍，以補償伺服器時鐘時間之間可能的不一致。若要為此功能設定自訂值並覆寫預設值，您可以將 `jwt_clock_skew_tolerance_seconds` 設定新增至 `config.yml`。

```yml
http_authenticator:
  type: saml
  challenge: true
  config:
    idp:
      metadata_file: okta.xml
    jwt_clock_skew_tolerance_seconds: 20
```

## OpenSearch Dashboards 設定

網頁瀏覽器 SSO 規範透過 HTTP GET 或 POST 交換資訊。例如，您登入 IdP 之後，它會將包含 SAML 回應的 HTTP POST 傳回 OpenSearch Dashboards。您必須設定 OpenSearch Dashboards 安裝的基礎 URL，也就是傳送 HTTP 請求的目標。

名稱 | 說明
:--- | :---
`kibana_url` | OpenSearch Dashboards 基礎 URL。必要。


## 使用者名稱與角色屬性

主體（例如使用者名稱）通常儲存在 SAML 回應的 `NameID` 元素中：

```
<saml2:Subject>
  <saml2:NameID>admin</saml2:NameID>
  ...
</saml2:Subject>
```

如果您的 IdP 符合 SAML 2.0 規範，則不需要設定任何特殊項目。如果您的 IdP 使用不同的元素名稱，也可以明確指定該名稱。

角色屬性是選用的。不過，大多數 IdP 都可以設定為在 SAML 斷言中加入角色。如果存在這些角色，您可以在[角色對應]({{site.url}}{{site.baseurl}}/security/access-control/index/#concepts)中使用它們：

```
<saml2:Attribute Name='Role'>
  <saml2:AttributeValue >Everyone</saml2:AttributeValue>
  <saml2:AttributeValue >Admins</saml2:AttributeValue>
</saml2:Attribute>
```

如果您想從 SAML 回應中擷取角色，則需要指定包含角色的元素名稱。

名稱 | 說明
:--- | :---
`subject_key` | SAML 回應中儲存主體的屬性。選用。若未設定，則使用 `NameID` 屬性。
`roles_key` | SAML 回應中儲存角色的屬性。選用。若未設定，則不使用任何角色。


## 請求簽署

安全性外掛程式傳送給 IdP 的請求可以選擇性地簽署。請使用下列設定來設定請求簽署。

名稱 | 說明
:--- | :---
`sp.signature_private_key` | 用於簽署請求或解碼加密的斷言的私密金鑰。選用。設定 `private_key_filepath` 時不可使用。
`sp.signature_private_key_password` | 私密金鑰的密碼（如果有的話）。
`sp.signature_private_key_filepath` | 私密金鑰的路徑。檔案必須放在 OpenSearch 的 `config` 目錄下，且路徑必須以該目錄為相對路徑指定。
`sp.signature_algorithm` | 用於簽署請求的演算法。可能的值請參閱下一個表格。

私密金鑰必須是 PKCS#8 格式。如果您想使用加密金鑰，該金鑰必須以相容於 PKCS#12 的演算法（3DES）加密。

安全性外掛程式支援下列簽章演算法。

演算法 | 值
:--- | :---
`DSA_SHA1` | http://www.w3.org/2000/09/xmldsig#dsa-sha1;
`RSA_SHA1` | http://www.w3.org/2000/09/xmldsig#rsa-sha1;
`RSA_SHA256` | http://www.w3.org/2001/04/xmldsig-more#rsa-sha256;
`RSA_SHA384` | http://www.w3.org/2001/04/xmldsig-more#rsa-sha384;
`RSA_SHA512` | http://www.w3.org/2001/04/xmldsig-more#rsa-sha512;


## 登出

通常，IdP 會在其 SAML 2.0 中繼資料中提供個別登出 URL 的資訊。若是如此，安全性外掛程式會使用這些資訊在 OpenSearch Dashboards 中呈現正確的登出連結。如果您的 IdP 不支援明確登出，您可以在使用者再次造訪 OpenSearch Dashboards 時強制重新登入。

名稱 | 說明
:--- | :---
`sp.forceAuthn` | 即使使用者與 IdP 之間有作用中的工作階段，仍強制重新登入。

安全性外掛程式僅支援 `HTTP-Redirect` 登出繫結（binding）。請確認您的 IdP 已正確設定此項。


## 交換金鑰設定

與其他通訊協定不同，SAML 並非設計用於在每次請求時交換使用者憑證。安全性外掛程式會以 SAML 回應換取一個儲存已驗證使用者屬性的輕量級 JWT。此權杖由您選擇的交換金鑰簽署。請注意，當您更換此金鑰時，所有以它簽署的權杖會立即失效。

名稱 | 說明
:--- | :---
`exchange_key` | 用於簽署權杖的金鑰。演算法為 HMACSHA512，因此建議使用 64 個字元，例如 `9a2h8ajasdfhsdiydfn7dtd6d5ashsd89a2h8ajasdHhsdiyLfn7dtd6d5ashsdI`。請務必為 `exchange_key` 輸入值，否則會傳回錯誤。



## TLS 設定

如果您是從 URL 載入 IdP 中繼資料，建議使用 SSL/TLS。如果您使用 Okta 或 Auth0 等採用受信任憑證的外部 IdP，通常不需要設定任何項目。如果您自行託管 IdP 並使用自己的根 CA，可以依照下列方式自訂 TLS 設定。這些設定僅用於透過 HTTPS 載入 SAML 中繼資料。

名稱 | 說明
:--- | :---
`idp.enable_ssl` | 是否啟用自訂 TLS 組態。預設為 `false`（使用 JDK 設定）。
`idp.verify_hostnames` | 是否驗證伺服器 TLS 憑證的主機名稱。

範例：

```yml
authc:
  saml_auth_domain:
    http_enabled: true
    transport_enabled: false
    order: 1
    http_authenticator:
      type: saml
      challenge: true
      config:
        idp:
          enable_ssl: true
          verify_hostnames: true
          ...
    authentication_backend:
      type: noop
```


### 憑證驗證

透過設定以下**其中一項**組態選項，來設定用於驗證 IdP TLS 憑證的根 CA：

```yml
config:
  idp:
    pemtrustedcas_filepath: path/to/trusted_cas.pem
```

```yml
config:
  idp:
    pemtrustedcas_content: |-
      -----BEGIN CERTIFICATE-----
      MIID/jCCAuagAwIBAgIBATANBgkqhkiG9w0BAQUFADCBjzETMBEGCgmSJomT8ixk
      ARkWA2NvbTEXMBUGCgmSJomT8ixkARkWB2V4YW1wbGUxGTAXBgNVBAoMEEV4YW1w
      bGUgQ29tIEluYy4xITAfBgNVBAsMGEV4YW1wbGUgQ29tIEluYy4gUm9vdCBDQTEh
      ...
      -----END CERTIFICATE-----
```

名稱 | 說明
:--- | :---
`idp.pemtrustedcas_filepath` | 包含 IdP 根 CA 的 PEM 檔案路徑。檔案必須放在 OpenSearch 的 `config` 目錄下，且您必須以該目錄為相對路徑指定路徑。
`idp.pemtrustedcas_content` | IdP 伺服器的根 CA 內容。設定 `pemtrustedcas_filepath` 時不可使用。


### 用戶端驗證

安全性外掛程式在擷取 IdP 中繼資料時可以使用 TLS 用戶端驗證。啟用後，安全性外掛程式會在每次中繼資料請求時向 IdP 傳送 TLS 用戶端憑證。請使用下列金鑰來設定用戶端驗證。

名稱 | 說明
:--- | :---
`idp.enable_ssl_client_auth` | 是否向 IdP 伺服器傳送用戶端憑證。預設為 `false`。
`idp.pemcert_filepath` | 包含用戶端憑證的 PEM 檔案路徑。檔案必須放在 OpenSearch 的 `config` 目錄下，且路徑必須以 `config` 目錄為相對路徑指定。
`idp.pemcert_content` | 用戶端憑證的內容。設定 `pemcert_filepath` 時不可使用。
`idp.pemkey_filepath` | 用戶端憑證之私密金鑰的路徑。檔案必須放在 OpenSearch 的 `config` 目錄下，且路徑必須以 `config` 目錄為相對路徑指定。
`idp.pemkey_content` | 您憑證之私密金鑰的內容。設定 `pemkey_filepath` 時不可使用。
`idp.pemkey_password` | 您私密金鑰的密碼（如果有的話）。


### 啟用的加密套件與通訊協定

您可以限制 IdP 連線允許的加密套件與 TLS 通訊協定。例如，您可以僅啟用強式加密套件，並將 TLS 版本限制為最新的版本。

名稱 | 說明
:--- | :---
`idp.enabled_ssl_ciphers` | 啟用的 TLS 加密套件陣列。僅支援 Java 格式。
`idp.enabled_ssl_protocols` | 啟用的 TLS 通訊協定陣列。僅支援 Java 格式。


## 最小組態範例
下列範例顯示最小組態：

```yml
_meta:
  type: "config"
  config_version: 2

config:
  dynamic:
    authc:
      saml_auth_domain:
        http_enabled: true
        transport_enabled: false
        order: 1
        http_authenticator:
          type: saml
          challenge: true
          config:
            idp:
              metadata_file: metadata.xml
              entity_id: http://idp.example.com/
            sp:
              entity_id: https://opensearch-dashboards.example.com
            kibana_url: https://opensearch-dashboards.example.com:5601/
            roles_key: Role
            exchange_key: 'peuvgOLrjzuhXf ...'
        authentication_backend:
          type: noop
```

## OpenSearch Dashboards 組態

由於大多數 SAML 特定的組態是在安全性外掛程式中完成，因此只要在您的 `opensearch_dashboards.yml` 中新增下列內容即可啟用 SAML：

```yml
opensearch_security.auth.type: "saml"
```

此外，您必須將用於驗證 SAML 斷言的 OpenSearch Dashboards 端點新增至您的允許清單：

```yml
server.xsrf.allowlist: ["/_opendistro/_security/saml/acs"]
```

如果您使用登出 POST 繫結，也需要將登出端點新增至您的允許清單：

```yml
server.xsrf.allowlist: ["/_opendistro/_security/saml/acs", "/_opendistro/_security/saml/logout"]
```

若要在 Dashboards 登入視窗中將 SAML 與其他驗證類型一併納入，請參閱[設定登入選項]({{site.url}}{{site.baseurl}}/security/configuration/multi-auth/)。
{: .note }

#### 使用其他 Cookie 的工作階段管理

為了改善工作階段管理——尤其是針對被指派多個角色的使用者——Dashboards 提供了一個選項，可將 Cookie 承載內容分割成多個 Cookie，並在收到這些 Cookie 時重新合併承載內容。這有助於避免較大的 SAML 斷言超過每個 Cookie 的大小限制。下列範例中的兩項設定可讓您為其他 Cookie 設定前置名稱，並指定其數量。這些設定會新增至 `opensearch_dashboards.yml` 檔案。其他 Cookie 的預設數量為三個：

```yml
opensearch_security.saml.extra_storage.cookie_prefix: security_authentication_saml
opensearch_security.saml.extra_storage.additional_cookies: 3
```

請注意，減少其他 Cookie 的數量可能會導致變更前正在使用的一些 Cookie 停止運作。我們建議建立固定的其他 Cookie 數量，且之後不要變更組態。

如果來自 IdP 的 ID 權杖特別大，OpenSearch 的伺服器記錄檔中可能會出現驗證錯誤，指出 HTTP 標頭過大。在這種情況下，您可以增加 `opensearch.yml` 檔案中 `http.max_header_size` 設定的值。
{: .tip }

### IdP 起始的 SSO

若要使用 IdP 起始的 SSO，請將您 IdP 的 Assertion Consumer Service 端點設為：

```
/_opendistro/_security/saml/acs/idpinitiated
```

然後將此端點新增至 `opensearch_dashboards.yml` 中的 `server.xsrf.allowlist`：

```yml
server.xsrf.allowlist: ["/_opendistro/_security/saml/acs/idpinitiated", "/_opendistro/_security/saml/acs", "/_opendistro/_security/saml/logout"]
```

## 疑難排解

- 如需常見 SAML 組態問題的解決方案，請參閱[對 SAML 進行疑難排解]({{site.url}}{{site.baseurl}}/security/authentication-backends/troubleshoot-saml/)。
