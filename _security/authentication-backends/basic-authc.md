---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "HTTP 基本驗證"
parent: Authentication backends
nav_order: 46
redirect_from:
---


# HTTP 基本驗證

HTTP 基本驗證提供一個簡單的質詢與回應流程，用於存取 OpenSearch 及其資源，並提示您輸入使用者名稱與密碼登入。您可以在組態的 `http_authenticator` 區段中，將 `type` 指定為 `basic` 來啟用 HTTP 基本驗證，如下列範例所示：

```yml
_meta:
  type: "config"
  config_version: 2

config:
  dynamic:
    authc:
      basic_internal_auth_domain:
        description: "Authenticate using HTTP basic against the internal users database"
        http_enabled: true
        transport_enabled: true
        order: 1
        http_authenticator:
          type: basic
          challenge: true
        authentication_backend:
          type: internal
```

此外，您可以將內部使用者資料庫指定為驗證後端，方法是將 `internal` 指定為 `authentication_backend` 的類型。關於此後端的資訊，請參閱[內部使用者資料庫](#the-internal-user-database)。

一旦將 `basic` 指定為 HTTP 驗證器的類型，並將 `internal` 指定為驗證後端的類型，除非您打算將其他驗證後端與 HTTP 基本驗證搭配使用，否則不需要在 `config.yml` 中進行進一步組態。請繼續閱讀，以了解與此類設定相關的注意事項，以及關於 `challenge` 設定的更多資訊。


## challenge 設定

在大多數情況下，將 `challenge` 設定為 `true` 對基本驗證而言是適當的。此設定定義了當 HTTP 標頭中的 `Authorization` 欄位未指定時，Security 外掛程式的行為。預設情況下，此設定為 `true`。

當 `challenge` 設定為 `true` 時，Security 外掛程式會將狀態為 `UNAUTHORIZED` (401) 的回應傳回給用戶端。如果用戶端是透過瀏覽器存取叢集，這會觸發驗證對話方塊，並提示使用者輸入使用者名稱與密碼。當 HTTP 基本驗證是唯一使用的後端時，這是常見的組態。

當 `challenge` 設定為 `false`，且請求中未指定 `Authorization` 標頭時，Security 外掛程式不會將 `WWW-Authenticate` 回應傳回給用戶端，驗證便會失敗。此組態常用於您設定的驗證網域中包含多個會發出質詢的 `http_authenticator` 設定的情況。例如，當您打算將基本驗證與 SAML 一起使用時，可能就是這種情況。關於此組態的範例與更完整的說明，請參閱 SAML 文件中的[執行多個驗證網域]({{site.url}}{{site.baseurl}}/security/authentication-backends/saml/#running-multiple-authentication-domains)。

當您定義多個 HTTP 驗證器時，請務必將不發出質詢的驗證器排在前面---例如 `proxy` 與 `clientcert`---並將會發出質詢的 HTTP 驗證器排在最後。例如，在將不發出質詢的 HTTP 基本驗證後端與會發出質詢的 SAML 後端配對的組態中，您可以在 HTTP 基本 `authc` 網域中指定 `order: 0`，並在 SAML 網域中指定 `order: 1`。
{: .note }


## 內部使用者資料庫

使用 HTTP 基本驗證時，內部使用者資料庫會儲存內部使用者，並包含其雜湊後的密碼與其他使用者屬性，例如角色。使用者及其設定保存在 `internal_users.yml` 組態檔中。關於此檔案的更多資訊，請參閱安全性組態文件中的 [internal_users.yml]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#internal_usersyml)。

