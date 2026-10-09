---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定登入選項"
parent: Configuration
nav_order: 45
---

# 為多種驗證選項設定 Dashboards 登入

您可以設定 OpenSearch Dashboards 的登入視窗，在登入時提供單一的使用者驗證選項或多個選項。Dashboards 支援基本驗證、OpenID Connect 及 SAML 作為多個選項。

## 設定多種驗證選項的一般步驟

在為多種驗證選項設定登入視窗之前，請先考量下列步驟順序。

1. 決定要在登入時提供哪些類型的驗證。
1. 設定每種驗證類型，包括身分提供者 (IdP) 的驗證網域，以及讓每種類型都能登入 OpenSearch Dashboards 的必要設定。如需 OpenID Connect 後端組態，請參閱 [OpenID Connect]({{site.url}}{{site.baseurl}}/security/authentication-backends/openid-connect/)。如需 SAML 後端組態，請參閱 [SAML]({{site.url}}{{site.baseurl}}/security/authentication-backends/saml/)。
1. 在 `opensearch_dashboards.yml` 檔案中新增、啟用並設定多選項驗證設定。

## 啟用多種驗證選項

根據預設，Dashboards 提供基本驗證以供登入。若要啟用多種驗證選項，請先在 `opensearch_dashboards.yml` 檔案中新增 `opensearch_security.auth.multiple_auth_enabled` 並將其設為 `true`。

若要在登入時將多種驗證類型指定為選項，請在 `opensearch_dashboards.yml` 檔案中新增 `opensearch_security.auth.type` 設定，並輸入多個類型作為值。當設定中新增多個驗證類型時，Dashboards 登入視窗會辨識多個類型並進行調整，以容納這些登入選項。

將 Dashboards 設定為提供多種驗證選項時，一律必須將基本驗證作為該設定的其中一個值。
{: .note }

當只需要一種驗證類型時，請為該設定新增單一值。

```yml
opensearch_security.auth.type: "openid"
```
{% include copy.html %}

如需多種驗證選項，請以逗號分隔的陣列形式為該設定新增多個值。OpenSearch Dashboards 支援基本驗證、OpenID Connect 及 SAML 的組合，作為一組有效的值。在該設定中，這些值表示為 `"basicauth"`、`"openid"` 及 `"saml"`。

```yml
opensearch_security.auth.type: ["basicauth","openid"]
opensearch_security.auth.multiple_auth_enabled: true
```
{% include copy.html %}

```yml
opensearch_security.auth.type: ["basicauth","saml"]
opensearch_security.auth.multiple_auth_enabled: true
```
{% include copy.html %}

```yml
opensearch_security.auth.type: ["basicauth","saml","openid"]
opensearch_security.auth.multiple_auth_enabled: true
```
{% include copy.html %}

當 `opensearch_security.auth.type` 設定包含 `basicauth` 及另一種驗證類型時，登入視窗會如下列範例所示。

![登入視窗中的基本驗證及另一種類型]({{site.url}}{{site.baseurl}}/images/Security/OneOptionWithoutLogo.png){: width="350" }

指定全部三種有效的驗證類型後，登入視窗會如下列範例所示。

![登入視窗中指定全部三種驗證類型]({{site.url}}{{site.baseurl}}/images/Security/TwoOptionWithoutLogo.png){: width="350" }

## 設定預設的重新導向驗證類型

啟用多種驗證類型後，您可以將其中一種以重新導向為基礎的驗證類型 (SAML 或 OpenID Connect) 設定為預設用於自動重新導向。當您希望大多數使用者透過 IdP 進行驗證，同時仍允許其他驗證方法時，這會很有用。

若要設定預設的重新導向驗證類型，請在 `opensearch_dashboards.yml` 檔案中新增 `opensearch_security.auth.default_redirect_auth_type` 設定：

```yml
opensearch_security.auth.type: ["basicauth","saml"]
opensearch_security.auth.multiple_auth_enabled: true
opensearch_security.auth.default_redirect_auth_type: "saml"
```
{% include copy.html %}

使用此組態時，未驗證的使用者會自動重新導向至 SAML IdP 進行驗證，而不是顯示 OpenSearch Dashboards 登入頁面。

`default_redirect_auth_type` 值必須是 `saml` 或 `openid`，且也必須包含在 `opensearch_security.auth.type` 陣列中。
{: .note }

### 略過自動重新導向

設定預設的重新導向驗證類型後，您可以在 OpenSearch Dashboards URL 後方附加 `?auto_login=false`，以略過自動重新導向並改為顯示登入頁面。例如：

```
https://<dashboards-host>:5601/app/dashboards?auto_login=false
```

當預設重新導向設定為使用 SAML 或 OpenID Connect 時，這對需要使用基本驗證進行驗證 (例如以叢集管理員身分) 的管理員很有用。

## 自訂登入環境

除了每種驗證類型的必要登入設定外，您還可以在 `opensearch_dashboards.yml` 檔案中設定其他設定，以自訂登入視窗，使其清楚呈現可用的選項。例如，您可以將登入按鈕上的標籤替換為 IdP 的名稱及圖示。請參閱下列設定及說明。

![經過部分自訂的多選項登入視窗]({{site.url}}{{site.baseurl}}/images/Security/TwoOptionWithLogo.png){: width="350" }

### 基本驗證設定

這些設定可讓您自訂基本的使用者名稱及密碼登入按鈕。

設定 | 說明
:--- | :--- |:--- |:--- |
`opensearch_security.ui.basicauth.login.brandimage` |  登入按鈕標誌。支援的檔案類型為 SVG、PNG 及 GIF。
`opensearch_security.ui.basicauth.login.showbrandimage` |  決定是否顯示登入按鈕的標誌。預設為 `true`。

### OpenID Connect 驗證設定

這些設定可讓您自訂與 OpenID Connect 驗證相關聯的登入按鈕。如需使用 OpenID Connect 作為單一登入選項所需的必要設定，請參閱 [OpenSearch Dashboards 單一登入]({{site.url}}{{site.baseurl}}/security/authentication-backends/openid-connect/#opensearch-dashboards-single-sign-on)。

設定 | 說明
:--- | :--- |:--- |:--- |
`opensearch_security.ui.openid.login.buttonname` |  登入按鈕的顯示名稱。預設為「Log in with single sign-on」。
`opensearch_security.ui.openid.login.brandimage` |  登入按鈕標誌。支援的檔案類型為 SVG、PNG 及 GIF。
`opensearch_security.ui.openid.login.showbrandimage` |  決定是否顯示登入按鈕的標誌。預設為 `false`。

### SAML 驗證設定

這些設定可讓您自訂與 SAML 驗證相關聯的登入按鈕。如需使用 SAML 作為登入選項所需的必要設定，請參閱 [OpenSearch Dashboards 組態]({{site.url}}{{site.baseurl}}/security/authentication-backends/saml/#opensearch-dashboards-configuration)。

設定 | 說明
:--- | :--- |:--- |:--- |
`opensearch_security.ui.saml.login.buttonname` |  登入按鈕的顯示名稱。預設為「Log in with single sign-on」。
`opensearch_security.ui.saml.login.brandimage` |  登入按鈕標誌。支援的檔案類型為 SVG、PNG 及 GIF。
`opensearch_security.ui.saml.login.showbrandimage` |  決定是否顯示登入按鈕的標誌。預設為 `false`。

## 範例設定
下列範例顯示當 `opensearch_dashboards.yml` 檔案設定為在登入時使用兩種驗證類型時的基本設定。

```yml
# The several settings directly below are typical of all `opensearch_dashboards.yml` configurations. #
server.host: 0.0.0.0
server.port: 5601
opensearch.hosts: ["https://localhost:9200"]
opensearch.ssl.verificationMode: none
opensearch.username: <preferred username>
opensearch.password: <preferred password>
opensearch.requestHeadersAllowlist: ["securitytenant","Authorization"]
opensearch_security.multitenancy.enabled: true
opensearch_security.multitenancy.tenants.preferred: ["Private", "Global"]
opensearch_security.readonly_mode.roles: ["<role_for_read_only>"]

# Settings that enable multiple option authentication in the sign-in window #
opensearch_security.auth.multiple_auth_enabled: true
opensearch_security.auth.type: ["basicauth","openid"]
opensearch_security.auth.default_redirect_auth_type: "openid"

# Basic authentication customization #
opensearch_security.ui.basicauth.login.brandimage: <path/to/OSlogo.png>
opensearch_security.ui.basicauth.login.showbrandimage: true

# OIDC auth customization and start settings #
opensearch_security.ui.openid.login.buttonname: Log in with <IdP name or other> 
opensearch_security.ui.openid.login.brandimage: <path/to/brand-logo.png>
opensearch_security.ui.openid.login.showbrandimage: true

opensearch_security.openid.base_redirect_url: <"OIDC redirect URL">
opensearch_security.openid.verify_hostnames: false
opensearch_security.openid.refresh_tokens: false
opensearch_security.openid.logout_url: <"OIDC logout URL">

opensearch_security.openid.connect_url: <"OIDC connect URL">
opensearch_security.openid.client_id: <Client ID>
opensearch_security.openid.client_secret: <Client secret>
```
{% include copy.html %}