---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "SAML 疑難排解"
parent: SAML
grand_parent: Authentication backends
nav_order: 10
redirect_from:
  - /troubleshoot/saml/
---

# SAML 疑難排解

使用下列疑難排解步驟，解決使用 SAML 進行 OpenSearch Dashboards 驗證時遇到的問題。


---

#### 目錄
- TOC
{:toc}


---

## 檢查 sp.entity_id

大多數身分識別提供者 (IdP) 允許您為不同的應用程式設定多種驗證方法。例如，在 Okta 中，這些用戶端稱為「Applications」；在 Keycloak 中，則稱為「Clients」。每個用戶端都有自己的實體 ID。請務必設定 `sp.entity_id` 以符合這些設定：

```yml
saml:
  ...
  http_authenticator:
    type: 'saml'
    challenge: true
    config:
      ...
      sp:
        entity_id: opensearch-dashboards-saml
```


## 檢查 SAML 宣告取用者服務 URL

成功登入後，您的 IdP 會使用 HTTP POST 將 SAML 回應傳送至 OpenSearch Dashboards 的「宣告取用者服務 URL」(ACS)。

OpenSearch Dashboards Security 外掛程式提供的端點為：

```
/_opendistro/_security/saml/acs
```

請確認您已在 IdP 中正確設定此端點。有些 IdP 也會要求您將其傳送請求的所有端點加入允許清單。請確認 ACS 端點已列入清單中。

OpenSearch Dashboards 也要求您將此端點加入允許清單。請確認 `opensearch_dashboards.yml` 中有下列項目：

```
server.xsrf.allowlist: [/_opendistro/_security/saml/acs]
```


## 簽署所有文件

有些 IdP 預設不會簽署 SAML 文件。請務必讓 IdP 簽署所有文件。


#### Keycloak

![Keycloak UI]({{site.url}}{{site.baseurl}}/images/saml-keycloak-sign-documents.png)


## 角色設定

在 SAML 回應中包含使用者角色取決於您的 IdP。例如，在 Keycloak 中，此設定位於用戶端的 **Mappers** 區段；在 Okta 中，您必須設定群組屬性陳述式。請確認此設定正確，且 SAML 組態中的 `roles_key` 與 SAML 回應中的角色名稱相符：

```yml
saml:
  ...
  http_authenticator:
    type: 'saml'
    challenge: true
    config:
      ...
      roles_key: Role
```


## 檢查 SAML 回應

如果您不確定 IdP 的 SAML 回應包含哪些內容，以及它將使用者名稱與角色放在何處，可以在 `log4j2.properties` 中啟用偵錯模式：

```
logger.token.name = com.amazon.dlic.auth.http.saml.Token
logger.token.level = debug
```

此設定會將 SAML 回應輸出至 OpenSearch 記錄檔，讓您可以檢查並偵錯。將此記錄器設為 `debug` 會產生大量輸出，因此不建議在正式環境中使用。

另一種檢查 SAML 回應的方法，是在登入 OpenSearch Dashboards 時監控網路流量。IdP 會使用 HTTP POST 請求，將 Base64 編碼的 SAML 回應傳送至：

```
/_opendistro/_security/saml/acs
```

請檢查此 POST 請求的酬載，並使用 [base64decode.org](https://www.base64decode.org/) 之類的工具進行解碼。


## 檢查角色對應

Security 外掛程式使用標準角色對應，將使用者或後端角色對應至一或多個 Security 角色。

對於使用者名稱，Security 外掛程式預設使用 SAML 回應的 `NameID` 屬性。對某些 IdP 而言，此屬性包含的不是預期的使用者名稱，而是某個內部使用者 ID。請檢查 SAML 回應的內容，找出您想用作使用者名稱的元素，並透過設定 `subject_key` 來設定它：

```yml
saml:
  ...
  http_authenticator:
    type: 'saml'
    challenge: true
    config:
      ...
      subject_key: preferred_username
```

若要確認 SAML 回應中包含正確的後端角色，請檢查其內容並設定正確的屬性名稱：

```yml
saml:
  ...
  http_authenticator:
    type: 'saml'
    challenge: true
    config:
      ...
      roles_key: Role
```


## 檢查 JWT 權杖

Security 外掛程式會將 SAML 回應換成較輕量的 JSON Web Token (JWT)。JWT 中的使用者名稱與後端角色最終會對應至 Security 外掛程式中的角色。如果對應有問題，您可以使用與[檢查 SAML 回應](#inspect-the-saml-response)相同的設定來啟用權杖偵錯模式。

此設定會將 JWT 輸出至 OpenSearch 記錄檔，讓您可以使用 [JWT.io](https://jwt.io/) 之類的工具進行檢查與偵錯。
