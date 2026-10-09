---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Kerberos
parent: Authentication backends
nav_order: 75
---

# Kerberos 驗證

Kerberos 是一種穩健且安全的使用者驗證方法，它透過核發「票證」來進行安全的身分驗證，避免密碼經由網際網路傳送。

若要使用 Kerberos 驗證，您必須在 `opensearch.yml` 和 `config.yml` 中設定下列設定。

## OpenSearch 節點組態

在 `opensearch.yml` 中定義下列設定：

```yml
plugins.security.kerberos.krb5_filepath: 'krb5.conf'
plugins.security.kerberos.acceptor_keytab_filepath: 'opensearch_keytab.tab'
plugins.security.kerberos.acceptor_principal: 'HTTP/localhost'
```

名稱 | 說明
:--- | :---
`krb5_filepath` | Kerberos 組態檔案的路徑。此檔案包含與您的 Kerberos 安裝相關的各種設定，例如 Kerberos 金鑰配送中心 (KDC) 的 `realm` 名稱、`hostnames` 和連接埠。
`acceptor_keytab_filepath` | `keytab` 檔案的路徑，此檔案包含 Security 外掛程式透過 Kerberos 發出請求時所使用的主體 (principal)。
`acceptor_principal` | Security 外掛程式透過 Kerberos 發出請求時所使用的主體。此值必須存在於 `keytab` 檔案中。

基於安全性限制，`keytab` 和 `krb5.conf` 檔案必須放在 `config` 目錄或其子目錄中，而且它們在 `opensearch.yml` 中的路徑必須是相對路徑，而非絕對路徑。
{: .note }

## 叢集安全性組態

下列範例顯示 `config.yml` 中典型的 Kerberos 驗證網域：

```yml
kerberos_auth_domain:
  enabled: true
  order: 1
  http_authenticator:
    type: kerberos
    challenge: true
    config:
      krb_debug: false
      strip_realm_from_principal: true
  authentication_backend:
    type: noop
```

在 HTTP 層級使用瀏覽器時，透過 Kerberos 進行的驗證是以 SPNEGO 達成。Kerberos/SPNEGO 的實作會因您的瀏覽器和作業系統而有所不同。在決定是否需要將 `challenge` 旗標設為 `true` 或 `false` 時，這一點很重要。

與 [HTTP 基本驗證]({{site.url}}{{site.baseurl}}/security/authentication-backends/basic-authc/) 相同，此旗標決定當 HTTP 請求中找不到 `Authorization` 標頭，或此標頭不等於 `negotiate` 時，Security 外掛程式應如何回應。

若設為 `true`，Security 外掛程式會傳送狀態碼為 401 的回應，並將 `WWW-Authenticate` 標頭設為 `negotiate`。這會告知用戶端 (瀏覽器) 重新傳送已設定 `Authorization` 標頭的請求。若設為 `false`，Security 外掛程式將無法從請求中擷取認證資訊，驗證便會失敗。因此，只有在初始請求中就已傳送 Kerberos 認證資訊時，將 `challenge` 設為 `false` 才有意義。

名稱 | 說明
:--- | :---
`krb_debug` | 顧名思義，將此設定設為 `true` 會將 Kerberos 專屬的偵錯訊息輸出至 `stdout`。若您的 Kerberos 整合發生問題，請使用此設定。預設值為 `false`。
`strip_realm_from_principal` | 設為 `true` 時，Security 外掛程式會從使用者名稱中移除領域 (realm)。預設值：`true`。

由於 Kerberos/SPNEGO 是在 HTTP 層級驗證使用者，因此不需要額外的 `authentication_backend`。請將此值設為 `noop`。
