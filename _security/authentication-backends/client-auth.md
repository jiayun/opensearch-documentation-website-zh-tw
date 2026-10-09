---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "用戶端憑證驗證"
parent: Authentication backends
nav_order: 70
redirect_from:
  - /security/configuration/client-auth/
  - /security-plugin/configuration/client-auth/
---

# 用戶端憑證驗證

在從憑證授權單位 (CA) 取得您自己的憑證，或[使用 OpenSSL 產生您自己的憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/)之後，您就可以開始設定 OpenSearch，以使用用戶端憑證來驗證使用者。

用戶端憑證驗證比單純使用基本驗證 (使用者名稱與密碼) 提供更多安全性優勢。由於用戶端憑證驗證同時需要用戶端憑證及其私密金鑰，而這些通常由使用者持有，因此較不易受到暴力破解攻擊的影響，這類攻擊是惡意人士試圖猜測使用者的密碼。

用戶端憑證驗證的另一個優點是您可以將它與基本驗證搭配使用，提供兩層安全性。

## 啟用用戶端憑證驗證

若要啟用用戶端憑證驗證，您必須先將 `opensearch.yml` 中的 `clientauth_mode` 設為 `OPTIONAL` 或 `REQUIRE`：

```yml
plugins.security.ssl.http.clientauth_mode: OPTIONAL
```

接著，在 `config.yml` 的 `client_auth_domain` 區段中啟用用戶端憑證驗證。

```yml
clientcert_auth_domain:
  description: "Authenticate via SSL client certificates"
  http_enabled: true
  transport_enabled: true
  order: 1
  http_authenticator:
    type: clientcert
    config:
      username_attribute: cn #optional, if omitted DN becomes username
      skip_users:
    	    - "DC=de,L=test,O=users,OU=bridge,CN=dashboard"
    challenge: false
  authentication_backend:
    type: noop
```

## 將角色指派給憑證的一般名稱

您現在可以將憑證的一般名稱 (CN) 指派給角色。此步驟需要您識別憑證的 CN 以及您要指派給它的角色。若要檢視所有預先定義的 OpenSearch 角色清單，請參閱[預先定義的角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#predefined-roles)。若要開始，請先[定義角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#defining-roles)，然後將憑證的 CN 對應到該角色。

在決定要對應到憑證 CN 的角色之後，您可以使用 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#mapping-users-to-roles)、[`roles_mapping.yml`]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#roles_mappingyml) 或 [REST API]({{site.url}}{{site.baseurl}}/security/api/role-mappings/create-role-mapping/) 來對應角色。下列範例使用 `REST API` 將 CN `CLIENT1` 對應到角色 `readall`。

**範例請求**

```json
PUT _plugins/_security/api/rolesmapping/readall
{
  "backend_roles" : ["sample_role" ],
  "hosts" : [ "example.host.com" ],
  "users" : [ "CLIENT1" ]
}
```

**範例回應**

```json
{
  "status": "OK",
  "message": "'readall' updated."
}
```

將角色對應到用戶端憑證的 CN 之後，您就可以使用這些認證資訊連線到您的叢集。

下列程式碼範例使用 Python `requests` 程式庫連線到本機 OpenSearch 叢集，並將 GET 請求傳送到 `movies` 索引。

```python
import requests
import json
base_url = 'https://localhost:9200/'
headers = {
  'Content-Type': 'application/json'
}
cert_file_path = "/full/path/to/client-cert.pem"
key_file_path = "/full/path/to/client-cert-key.pem"
root_ca_path = "/full/path/to/root-ca.pem"

# Send the request.
path = 'movies/_doc/3'
url = base_url + path
response = requests.get(url, cert = (cert_file_path, key_file_path), verify=root_ca_path)
print(response.text)
```

{% comment %}

### (Advanced) Exclude certain users from client cert authentication

If you are using multiple authentication methods, it can make sense to exclude certain users from the client cert authentication.

Consider the following scenario for a typical OpenSearch Dashboards setup: OpenSearch Dashboard has basic auth setup and user login from a browser. However, you also have an OpenSearch Dashboards server user. OpenSearch Dashboards uses this user to manage stored objects and perform monitoring and maintenance tasks. You do not want to use this user certificate to log in a user who submitted basic auth logic from a browser.

In this case, it makes sense to exclude the OpenSearch Dashboards server user from the client cert authentication so that the user who enters login information in the browser is validated. You can use the `skip_users` configuration setting to define which users should be skipped. Wildcards and regular expressions are supported:

```yml

skip_users:
  - "DC=de,L=test,O=users,OU=bridge,CN=dashboard"

```

## Configuring Beats

You can also configure your Beats so that it uses a client certificate for authentication with OpenSearch. Afterwards, it can start sending output to OpenSearch.

This output configuration specifies which settings you need for client certificate authentication:

```yml
output.opensearch:
  enabled: true
  # Array of hosts to connect to.
  hosts: ["localhost:9200"]
  # Protocol - either `http` (default) or `https`.
  protocol: "https"
  ssl.certificate_authorities: ["/full/path/to/CA.pem"]
  ssl.verification_mode: certificate
  ssl.certificate: "/full/path/to/client-cert.pem"
  ssl.key: "/full/path/to/to/client-cert-key.pem"
```
{% endcomment %}

## 搭配 Docker 使用憑證

雖然我們建議使用 ODFE 的[封存檔]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/tar/)安裝來測試用戶端憑證驗證組態，您也可以使用任何其他安裝類型。如需使用 Docker 安全性的指示，請參閱[設定基本安全性設定]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#configuring-basic-security-settings)。
