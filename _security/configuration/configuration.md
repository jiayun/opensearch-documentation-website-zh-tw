---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定安全性後端"
parent: Configuration
nav_order: 20
redirect_from:
 - /security-plugin/configuration/configuration/
---

# 設定安全性後端

設定 Security 外掛程式的第一步之一，就是決定要使用哪一個驗證後端。後端在驗證中所扮演的角色，已於[驗證流程的步驟 2 和步驟 3]({{site.url}}{{site.baseurl}}/security/authentication-backends/authc-index/#authentication-flow)中說明。此外掛程式具有內部使用者資料庫，但許多人偏好使用現有的驗證後端，例如 LDAP 伺服器，或結合兩者使用。

用於設定驗證與授權後端的主要檔案是 `/usr/share/opensearch/config/opensearch-security/config.yml`。此檔案定義了 Security 外掛程式如何擷取使用者憑證、外掛程式如何驗證憑證，以及當選用於驗證與授權的後端支援此功能時，外掛程式如何擷取其他角色。本主題提供組態檔的基本概觀，以及設定安全性時對組態檔的要求。如需設定特定後端的相關資訊，請參閱[驗證後端]({{site.url}}{{site.baseurl}}/security/authentication-backends/authc-index/)。

`config.yml` 檔案包含三個主要部分：

```yml
config:
  dynamic:
    http:
      ...
    authc:
      ...
    authz:
      ...
```

以下各節說明 `config.yml` 檔案各部分的主要元素，並提供其組態的基本範例。如需更詳細的範例，請參閱 [GitHub 上的範例檔案](https://github.com/opensearch-project/security/blob/main/config/config.yml)。


## HTTP

`http` 區段包含下列格式：

```yml
http:
  anonymous_auth_enabled: <true|false>
  xff: # optional section
    enabled: <true|false>
    internalProxies: <string> # Regex pattern
    remoteIpHeader: <string> # Name of the header in which to look. Typically: x-forwarded-for
    proxiesHeader: <string>
    trustedProxies: <string> # Regex pattern
```

此組態中使用的設定如下表所述。

| 設定 | 說明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| :--- |:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `anonymous_auth_enabled` | 啟用或停用匿名驗證。當 `true` 時，HTTP 驗證器會嘗試在 HTTP 請求中尋找使用者憑證。若找到憑證，則會驗證該使用者。若找不到任何憑證，則會將使用者驗證為 _匿名_ 使用者。此使用者接著會有使用者名稱 `anonymous` 以及一個名為 `anonymous_backendrole` 的角色。當您啟用匿名驗證時，所有已定義的 HTTP 驗證器都會是非挑戰式的。如需詳細資訊，請參閱[挑戰設定]({{site.url}}{{site.baseurl}}/security/authentication-backends/basic-authc/#the-challenge-setting)。 |
| `xff` | 用於設定以 Proxy 為基礎的驗證。如需此後端的詳細資訊，請參閱[以 Proxy 為基礎的驗證]({{site.url}}{{site.baseurl}}/security/authentication-backends/proxy/)。                                                                                                                                                                                                                                                                                                                                                                                                                           |

如需如何設定匿名驗證的指示，請參閱[匿名驗證]({{site.url}}{{site.baseurl}}/security/access-control/anonymous-authentication/)。  
{: .important }

## 驗證

`authc` 區段具有下列格式：

```yml
authc:
  <domain_name>:
    http_enabled: <true|false>
    transport_enabled: <true|false>
    order: <integer>
    http_authenticator:
      ...
    authentication_backend:
      ...
```

`authc` 區段中的項目稱為*驗證網域*。它會指定從何處取得使用者憑證，以及應對哪個後端進行驗證。

您可以使用多個驗證網域。每個驗證網域都有一個名稱 (例如 `basic_auth_internal`)、用於在 REST 與傳輸層啟用該網域的設定，以及一個 `order`。此順序可讓您將驗證網域串接在一起。Security 外掛程式會依您提供的順序使用它們。若使用者成功通過某個網域的驗證，Security 外掛程式就會略過其餘網域。

此部分組態中常見的設定如下表所示。

| 設定 | 說明 |
| :--- | :--- |
| `http_enabled` | 啟用或停用 REST 層的驗證。預設為 `true` (啟用)。 |
| `transport_enabled` | 啟用或停用傳輸層的驗證。預設為 `true` (啟用)。 |
| `order` | 當組合設定多個後端時，決定驗證請求查詢驗證網域的順序。一旦驗證成功，就不需要再查詢其餘任何網域。其值為整數。 |

`http_authenticator` 定義會指定 HTTP 層的驗證方法。下列範例顯示用於定義 HTTP 驗證器的語法：

```yml
http_authenticator:
  type: <type>
  challenge: <true|false>
  config:
    ...
```

`http_authenticator` 的 `type` 設定接受下列值。如需每個驗證選項的詳細資訊，請參閱[後續步驟](#next-steps)中的驗證後端連結。

| 值 | 說明 |
| :--- | :--- |
| `basic` | HTTP 基本驗證。如需使用基本驗證的詳細資訊，請參閱 HTTP 基本驗證文件。 |
| `kerberos` | Kerberos 驗證。如需其他組態資訊，請參閱 Kerberos 文件。 |
| `jwt` | JSON Web Token (JWT) 驗證。如需其他組態資訊，請參閱 JSON Web Token 文件。 |
| `openid` | OpenID Connect 驗證。如需其他組態資訊，請參閱 OpenID Connect 文件。 |
| `saml` | SAML 驗證。如需其他組態資訊，請參閱 SAML 文件。 |
| `proxy`、`extended-proxy` | 以 Proxy 為基礎的驗證。`extended-proxy` 類型的驗證器可讓您傳遞其他使用者屬性，以供文件層級安全性使用。如需其他組態資訊，請參閱以 Proxy 為基礎的驗證文件。 |
| `clientcert` | 透過用戶端 TLS 憑證進行驗證。此憑證必須受到您節點信任存放區中其中一個根憑證授權單位 (CA) 的信任。如需其他組態資訊，請參閱用戶端憑證驗證文件。 |

設定 HTTP 驗證器之後，您必須指定要對哪個後端系統驗證使用者：

```yml
authentication_backend:
  type: <type>
  config:
    ...
```

下表顯示 `authentication_backend` 下 `type` 設定的可能值。

| 值 | 說明 |
| :--- | :--- |
| `noop` | 不會對任何後端系統執行進一步驗證。若 HTTP 驗證器已完整驗證使用者，例如 JWT 或用戶端憑證驗證的情況，請使用 `noop`。 |
| `internal` | 使用 `internal_users.yml` 中定義的使用者與角色進行驗證。 |
| `ldap` | 對 LDAP 伺服器驗證使用者。此設定需要[其他 LDAP 專屬組態設定]({{site.url}}{{site.baseurl}}/security/authentication-backends/ldap/)。 |


## 授權

`authz` 組態用於從 LDAP 實作中擷取後端角色。使用者通過驗證之後，Security 外掛程式可選擇性地從後端系統收集其他角色。授權組態具有下列格式：

```yml
authz:
  <name>:
    http_enabled: <true|false>
    transport_enabled: <true|false>
    authorization_backend:
      type: <type>
      config:
        ...
```

您可以在此區段中定義多個項目，如同驗證項目一樣。不過，在此情況下，執行順序並不重要，且不會使用 `order` 設定。

下表顯示 `authorization_backend` 下 `type` 設定的可能值。

| 值 | 說明 |
| :--- | :--- |
| `noop` | 完全略過授權組態步驟。 |
| `ldap` | 從 LDAP 伺服器擷取其他角色。此設定需要[其他 LDAP 專屬組態設定]({{site.url}}{{site.baseurl}}/security/authentication-backends/ldap/)。 |


## 後端組態範例

您的 OpenSearch 發行版中包含的預設 `config/opensearch-security/config.yml` 檔案含有許多組態範例。請以這些範例為起點，並依您的需求加以自訂。 


## 透過 gRPC 進行驗證與授權
**於 3.5 版推出**
{: .label .label-purple }

當 Security 外掛程式已啟用且並非以僅限 SSL 模式執行時，透過 gRPC 的請求會受到驗證與授權的規範。gRPC 傳輸會與 HTTP 層共用所有驗證後端，並遵循驗證網域中的 `http_enabled` 設定。透過 gRPC 僅支援 JWT 驗證。如需詳細資訊，請參閱[搭配 gRPC 使用 JWT 驗證]({{site.url}}{{site.baseurl}}/security/authentication-backends/jwt/#using-jwt-authentication-with-grpc)。

## 後續步驟

若要瞭解如何設定驗證後端，請參閱[驗證後端]({{site.url}}{{site.baseurl}}/security/authentication-backends/)文件。或者，您也可以使用下列主題清單中的連結，檢視特定後端的文件：

* [HTTP 基本驗證]({{site.url}}{{site.baseurl}}/security/authentication-backends/basic-authc/)
* [JSON Web Token]({{site.url}}{{site.baseurl}}/security/authentication-backends/jwt/)
* [OpenID Connect]({{site.url}}{{site.baseurl}}/security/authentication-backends/openid-connect/)
* [SAML]({{site.url}}{{site.baseurl}}/security/authentication-backends/saml/)
* [Active Directory 與 LDAP]({{site.url}}{{site.baseurl}}/security/authentication-backends/ldap/)
* [以 Proxy 為基礎的驗證]({{site.url}}{{site.baseurl}}/security/authentication-backends/proxy/)
* [用戶端憑證驗證]({{site.url}}{{site.baseurl}}/security/authentication-backends/client-auth/)
* [Kerberos 驗證]({{site.url}}{{site.baseurl}}/security/authentication-backends/kerberos/)
