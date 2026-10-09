---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定 TLS 憑證"
parent: Configuration
nav_order: 35
has_children: true
has_toc: false
redirect_from:
  - /security-plugin/configuration/tls/
---

# 設定 TLS 憑證

TLS 是在 `opensearch.yml` 中設定。憑證用於保護傳輸層流量 (叢集內的節點對節點通訊) 與 REST 層流量 (用戶端與叢集內節點之間的通訊)。TLS 在 REST 層為選用，在傳輸層則為必要。

您可以在 [GitHub](https://github.com/opensearch-project/security/blob/main/config/opensearch.yml.example) 上找到包含所有選項的範例組態範本。
{: .note }


## X.509 PEM 憑證與 PKCS \#8 金鑰

以下表格包含可用來設定 PEM 憑證與私密金鑰位置的設定。


### 傳輸層 TLS

名稱 | 說明
:--- | :---
`plugins.security.ssl.transport.pemkey_filepath` | 憑證金鑰檔案 (PKCS \#8) 的路徑，必須位於 `config` 目錄下，並使用相對路徑指定。必要。
`plugins.security.ssl.transport.pemkey_password` | 金鑰密碼。若金鑰沒有密碼，請省略此設定。選用。
`plugins.security.ssl.transport.pemcert_filepath` | X.509 節點憑證鏈 (PEM 格式) 的路徑，必須位於 `config` 目錄下，並使用相對路徑指定。必要。
`plugins.security.ssl.transport.pemtrustedcas_filepath` | 根憑證授權單位 (CA) (PEM 格式) 的路徑，必須位於 `config` 目錄下，並使用相對路徑指定。必要。


### REST 層 TLS

名稱 | 說明
:--- | :---
`plugins.security.ssl.http.enabled` | 是否在 REST 層啟用 TLS。若啟用，則僅允許 HTTPS。選用。預設為 `false`。
`plugins.security.ssl.http.pemkey_filepath` | 憑證金鑰檔案 (PKCS \#8) 的路徑，必須位於 `config` 目錄下，並使用相對路徑指定。必要。
`plugins.security.ssl.http.pemkey_password` | 金鑰密碼。若金鑰沒有密碼，請省略此設定。選用。
`plugins.security.ssl.http.pemcert_filepath` | X.509 節點憑證鏈 (PEM 格式) 的路徑，必須位於 `config` 目錄下，並使用相對路徑指定。必要。
`plugins.security.ssl.http.pemtrustedcas_filepath` | 根 CA (PEM 格式) 的路徑，必須位於 `config` 目錄下，並使用相對路徑指定。必要。


## Keystore 與 truststore 檔案

除了 PEM 格式的憑證與私密金鑰之外，您也可以改用 JKS 或 PKCS12/PFX 格式的 keystore 與 truststore 檔案。若要讓安全性外掛程式運作，您需要憑證與私密金鑰。

以下設定可設定 keystore 與 truststore 檔案的位置與密碼。如有需要，您可以為 REST 層與傳輸層使用不同的 keystore 與 truststore 檔案。


### 傳輸層 TLS

名稱 | 說明
:--- | :---
`plugins.security.ssl.transport.keystore_type` | keystore 檔案的類型，`JKS` 或 `PKCS12/PFX`。選用。預設為 `JKS`。
`plugins.security.ssl.transport.keystore_filepath` | keystore 檔案的路徑，必須位於 `config` 目錄下，並使用相對路徑指定。必要。
`plugins.security.ssl.transport.keystore_alias` | keystore 的別名。選用。預設為第一個別名。
`plugins.security.ssl.transport.keystore_password` | keystore 檔案的密碼。選用。預設為 `changeit`。
`plugins.security.ssl.transport.keystore_keypassword` | keystore 中私密金鑰的密碼。若未設定，則使用 `keystore_password`。選用。
`plugins.security.ssl.transport.truststore_type` | truststore 檔案的類型，`JKS` 或 `PKCS12/PFX`。預設為 `JKS`。
`plugins.security.ssl.transport.truststore_filepath` | truststore 檔案的路徑，必須位於 `config` 目錄下，並使用相對路徑指定。必要。
`plugins.security.ssl.transport.truststore_alias` | truststore 的別名。選用。預設為所有憑證。
`plugins.security.ssl.transport.truststore_password` | truststore 密碼。預設為 `changeit`。

### REST 層 TLS

名稱 | 說明
:--- | :---
`plugins.security.ssl.http.enabled` | 是否在 REST 層啟用 TLS。若啟用，則僅允許 HTTPS。選用。預設為 `false`。
`plugins.security.ssl.http.keystore_type` | keystore 檔案的類型，JKS 或 PKCS12/PFX。選用。預設為 JKS。
`plugins.security.ssl.http.keystore_filepath` | keystore 檔案的路徑，必須位於 `config` 目錄下，並使用相對路徑指定。必要。
`plugins.security.ssl.http.keystore_alias` | keystore 的別名。選用。預設為第一個別名。
`plugins.security.ssl.http.keystore_password` | keystore 檔案的密碼。選用。預設為 `changeit`。
`plugins.security.ssl.http.keystore_keypassword` | keystore 中私密金鑰的密碼。若未設定，則使用 `keystore_password`。選用。
`plugins.security.ssl.http.truststore_type` | truststore 檔案的類型，JKS 或 PKCS12/PFX。預設為 JKS。
`plugins.security.ssl.http.truststore_filepath` | truststore 檔案的路徑，必須位於 `config` 目錄下，並使用相對路徑指定。必要。
`plugins.security.ssl.http.truststore_alias` | truststore 的別名。選用。預設為所有憑證。
`plugins.security.ssl.http.truststore_password` | truststore 的密碼。預設為 `changeit`。


## 為傳輸層 TLS 分別使用用戶端與伺服器憑證

根據預設，傳輸層 TLS 憑證需要在憑證的 `Extended Key Usage` 區段中同時設定為用戶端 (`TLS Web Client Authentication`) 與伺服器 (`TLS Web Server Authentication`)，因為使用 TLS 憑證的節點會負責在內部提供與接收通訊請求。
如果您想為用戶端與伺服器使用不同的憑證，請將 `plugins.security.ssl.transport.extended_key_usage_enabled: true` 設定新增至 `opensearch.yml`。接著，設定[分別的用戶端與伺服器 X.509 PEM 憑證與 PKCS #8 金鑰]({{site.url}}{{site.baseurl}}/security/configuration/tls/#separate-client-and-server-x509-pem-certificates-and-pkcs-8-keys)或[分別的用戶端與伺服器 keystore 與 truststore 檔案]({{site.url}}{{site.baseurl}}/security/configuration/tls/#separate-client-and-server-keystore-and-truststore-files)區段中所述的設定。

### 分別的用戶端與伺服器 X.509 PEM 憑證與 PKCS #8 金鑰

名稱 | 說明
:--- | :---
`plugins.security.ssl.transport.server.pemkey_filepath` | 伺服器憑證金鑰檔案 (PKCS \#8) 的路徑。必須使用 `config` 目錄下的相對路徑指定。必要。
`plugins.security.ssl.transport.server.pemkey_password` | 伺服器金鑰密碼。若金鑰沒有密碼，請省略此設定。選用。
`plugins.security.ssl.transport.server.pemcert_filepath` | X.509 節點伺服器憑證鏈 (PEM 格式) 的路徑。必須使用 `config` 目錄下的相對路徑指定。必要。
`plugins.security.ssl.transport.server.pemtrustedcas_filepath` | 根 CA (PEM 格式) 的路徑。必須使用 `config` 目錄下的相對路徑指定。必要。
`plugins.security.ssl.transport.client.pemkey_filepath` | 用戶端憑證金鑰檔案 (PKCS \#8) 的路徑。必須使用 `config` 目錄下的相對路徑指定。必要。
`plugins.security.ssl.transport.client.pemkey_password` | 用戶端金鑰密碼。若金鑰沒有密碼，請省略此設定。選用。
`plugins.security.ssl.transport.client.pemcert_filepath` | X.509 節點用戶端憑證鏈 (PEM 格式) 的路徑。必須使用 `config` 目錄下的相對路徑指定。必要。
`plugins.security.ssl.transport.client.pemtrustedcas_filepath` | 根 CA (PEM 格式) 的路徑。必須使用 `config` 目錄下的相對路徑指定。必要。

### 分開的用戶端與伺服器金鑰儲存區和信任儲存區檔案

名稱 | 說明
:--- | :---
`plugins.security.ssl.transport.keystore_type` | 金鑰儲存區檔案的類型，可以是 `JKS` 或 `PKCS12/PFX`。選用。預設為 `JKS`。
`plugins.security.ssl.transport.keystore_filepath` | 金鑰儲存區檔案的路徑。必須使用 `config` 目錄下的相對路徑指定。必要。
`plugins.security.ssl.transport.keystore_password` | 金鑰儲存區檔案的密碼。選用。預設為 `changeit`。
`plugins.security.ssl.transport.server.keystore_alias` | 伺服器金鑰的別名。選用。預設為第一個別名。
`plugins.security.ssl.transport.client.keystore_alias` | 用戶端金鑰的別名。選用。預設為第一個別名。
`plugins.security.ssl.transport.server.keystore_keypassword` | 金鑰儲存區中伺服器私密金鑰的密碼。若未設定，則使用 `keystore_password`。選用。預設為 `changeit`。
`plugins.security.ssl.transport.client.keystore_keypassword` | 金鑰儲存區中用戶端私密金鑰的密碼。若未設定，則使用 `keystore_password`。選用。預設為 `changeit`。
`plugins.security.ssl.transport.server.truststore_alias` | 伺服器的別名。選用。預設為所有憑證。
`plugins.security.ssl.transport.client.truststore_alias` | 用戶端的別名。選用。預設為所有憑證。
`plugins.security.ssl.transport.truststore_filepath` | `truststore` 檔案的路徑。必須使用 `config` 目錄下的相對路徑指定。必要。
`plugins.security.ssl.transport.truststore_type` | `truststore` 檔案的類型，可以是 `JKS` 或 `PKCS12/PFX`。預設為 `JKS`。
`plugins.security.ssl.transport.truststore_password` | `truststore` 密碼。預設為 `changeit`。


## 設定節點憑證

OpenSearch Security 需要識別叢集中節點之間的請求。它使用節點憑證來保護這些請求。設定節點憑證最簡單的方法是在 `opensearch.yml` 中列出這些憑證的辨別名稱（DN）。所有節點上的 `opensearch.yml` 都必須包含所有 DN。請記住，Security 外掛程式支援萬用字元和正規表示式：

```yml
plugins.security.nodes_dn:
  - 'CN=node.other.com,OU=SSL,O=Test,L=Test,C=DE'
  - 'CN=*.example.com,OU=SSL,O=Test,L=Test,C=DE'
  - 'CN=elk-devcluster*'
  - '/CN=.*regex/'
```

如果您的節點憑證在 SAN 區段中具有物件識別碼（OID），便可以省略此組態。


## 設定管理員憑證

超級管理員憑證是具有較高權限的一般用戶端憑證，可用於執行管理性的安全性工作。您需要管理員憑證，才能使用 [`plugins/opensearch-security/tools/securityadmin.sh`]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/) 或 REST API 變更 Security 外掛程式組態。您可以在 `opensearch.yml` 中指定超級管理員憑證的 DN，以設定這些憑證：

```yml
plugins.security.authcz.admin_dn:
  - CN=admin,OU=SSL,O=Test,L=Test,C=DE
```

基於安全性考量，您不能使用萬用字元或正規表示式作為 `admin_dn` 設定的值。

如需管理員與超級管理員使用者角色的詳細資訊，請參閱[管理員與超級管理員角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#admin-and-super-admin-roles)。


## （進階）主機名稱驗證與 DNS 查詢

除了根據根 CA 和／或中繼 CA 驗證 TLS 憑證之外，Security 外掛程式還可以在傳輸層套用額外的檢查。

啟用 `enforce_hostname_verification` 後，Security 外掛程式會驗證通訊對象的主機名稱是否與憑證中的主機名稱相符。主機名稱取自您憑證中的 `subject` 或 `SAN` 項目。例如，如果您節點的主機名稱是 `node-0.example.com`，則 TLS 憑證中的主機名稱也必須設為 `node-0.example.com`。否則，會擲出錯誤：

```
[ERROR][c.a.o.s.s.t.opensearchSecuritySSLNettyTransport] [WX6omJY] SSL Problem No name matching <hostname> found
[ERROR][c.a.o.s.s.t.opensearchSecuritySSLNettyTransport] [WX6omJY] SSL Problem Received fatal alert: certificate_unknown
```

此外，啟用 `resolve_hostname` 時，Security 外掛程式會透過您的 DNS 解析已驗證的主機名稱。如果無法解析主機名稱，會擲出錯誤：


名稱 | 說明
:--- | :---
`transport.ssl.enforce_hostname_verification` | 是否在傳輸層驗證主機名稱。選用。預設為 `true`。
`plugins.security.ssl.transport.enforce_hostname_verification`（已棄用） | 此設定已棄用。請改用 `transport.ssl.enforce_hostname_verification`。
`transport.ssl.resolve_hostname` | 是否在傳輸層使用 DNS 解析主機名稱。選用。預設為 `true`。只有啟用主機名稱驗證時才會生效。
`plugins.security.ssl.transport.resolve_hostname`（已棄用） | 此設定已棄用。請改用 `transport.ssl.resolve_hostname`。


## （進階）用戶端驗證

啟用 TLS 用戶端驗證後，REST 用戶端可以隨 HTTP 請求傳送 TLS 憑證，以向 Security 外掛程式提供身分資訊。TLS 用戶端驗證有三種主要使用情境：

- 使用 REST 管理 API 時提供管理員憑證。
- 根據用戶端憑證設定角色與權限。
- 為 OpenSearch Dashboards、Logstash 或 Beats 等工具提供身分資訊。

TLS 用戶端驗證有三種模式：

* `NONE`：Security 外掛程式不接受 TLS 用戶端憑證。如果傳送了憑證，該憑證會被捨棄。
* `OPTIONAL`：Security 外掛程式會接受傳送的 TLS 用戶端憑證，但不要求提供憑證。
* `REQUIRE`：Security 外掛程式只有在傳送有效的用戶端 TLS 憑證時，才會接受 REST 請求。

對於 REST 管理 API，用戶端驗證模式至少必須為 OPTIONAL。

您可以使用下列設定來設定用戶端驗證模式：

名稱 | 說明
:--- | :---
`plugins.security.ssl.http.clientauth_mode` | 要使用的 TLS 用戶端驗證模式。可以是 `NONE`、`OPTIONAL`（預設）或 `REQUIRE`。選用。


## （進階）啟用的加密演算法與通訊協定

您可以限制 REST 層允許的加密演算法與 TLS 通訊協定。例如，您可以只允許強式加密演算法，並將 TLS 版本限制為最新版本。

如果未啟用此設定，瀏覽器與 Security 外掛程式會自動協商加密演算法與 TLS 版本，這在某些情況下可能導致使用較弱的加密套件。您可以使用下列設定來設定加密演算法與通訊協定。

名稱 | 資料類型 | 說明
:--- | :--- | :---
`plugins.security.ssl.http.enabled_ciphers` | 陣列 | REST 層啟用的 TLS 加密套件。僅支援 Java 格式。
`plugins.security.ssl.http.enabled_protocols` | 陣列 | REST 層啟用的 TLS 通訊協定。僅支援 Java 格式。
`plugins.security.ssl.transport.enabled_ciphers` | 陣列 | 傳輸層啟用的 TLS 加密套件。僅支援 Java 格式。
`plugins.security.ssl.transport.enabled_protocols` | 陣列 | 傳輸層啟用的 TLS 通訊協定。僅支援 Java 格式。

### 範例設定

```yml
plugins.security.ssl.http.enabled_ciphers:
  - "TLS_DHE_RSA_WITH_AES_256_CBC_SHA"
  - "TLS_DHE_DSS_WITH_AES_128_CBC_SHA256"
plugins.security.ssl.http.enabled_protocols:
  - "TLSv1.1"
  - "TLSv1.2"
```

由於不安全，Security 外掛程式預設停用 `TLSv1`。如果您需要使用 `TLSv1` 並接受相關風險，仍然可以啟用它：

```yml
plugins.security.ssl.http.enabled_protocols:
  - "TLSv1"
  - "TLSv1.1"
  - "TLSv1.2"
```

## (進階) 停用 Java 8 的用戶端起始重新協商

設定 `-Djdk.tls.rejectClientInitiatedRenegotiation=true` 以停用安全的用戶端起始重新協商，該功能預設為啟用。此設定可透過 `config/jvm.options` 中的 `OPENSEARCH_JAVA_OPTS` 進行設定。

## (進階) 為 SSL 使用加密的密碼設定

預設的不安全 SSL 密碼設定已被棄用。若要使用這些設定的安全替代方案，使用者可以使用其替代形式。具體而言，使用者可以在 SSL 設定後面加上 `_secure` 後綴。產生的安全替代設定如下：

* plugins.security.ssl.http.pemkey_password_secure
* plugins.security.ssl.http.keystore_password_secure
* plugins.security.ssl.http.keystore_keypassword_secure
* plugins.security.ssl.http.truststore_password_secure
* plugins.security.ssl.transport.pemkey_password_secure
* plugins.security.ssl.transport.server.pemkey_password_secure
* plugins.security.ssl.transport.client.pemkey_password_secure
* plugins.security.ssl.transport.keystore_password_secure
* plugins.security.ssl.transport.keystore_keypassword_secure
* plugins.security.ssl.transport.server.keystore_keypassword_secure
* plugins.security.ssl.transport.client.keystore_keypassword_secure
* plugins.security.ssl.transport.truststore_password_secure

這些設定允許在設定中使用加密的密碼。

## 熱重新載入 TLS 憑證

更新 HTTP 層與傳輸層上已過期或即將過期的 TLS 憑證時，不需要重新啟動叢集。您可以改為啟用 TLS 憑證的熱重新載入。啟用後，就地熱重新載入會每 5 秒監視您的 keystore 資源是否有更新。如果您在 OpenSearch 的 `config` 目錄中新增或修改憑證、金鑰檔案或 keystore 設定，叢集中的節點會偵測到變更並自動重新載入金鑰與憑證。

若要啟用就地熱重新載入，請在 `opensearch.yml` 中新增以下一行：

```yml
plugins.security.ssl.certificates_hot_reload.enabled: true
```
{% include copy.html %}

### 使用 Reload Certificates API

在不使用熱重新載入的情況下，您可以使用 Reload Certificates API 重新讀取已更換的憑證。

若要啟用 Reload Certificates API，請在 `opensearch.yml` 中新增以下一行：

```yml
plugins.security.ssl_cert_reload_enabled: true
```
{% include copy.html %}

此設定預設為 `false`。
{: .note }

啟用重新載入後，請使用 Reload Certificates API 來更換過期的憑證。新憑證必須儲存在與先前憑證相同的位置，以避免 `opensearch.yml` 檔案發生任何變更。

預設情況下，Reload Certificates API 預期舊憑證會被以相同 `Issuer/Subject DN` 與 `SAN` 簽發的有效憑證取代。此行為可以透過在 `opensearch.yml` 中新增以下設定來停用：

```yml
plugins.security.ssl.http.enforce_cert_reload_dn_verification: false
plugins.security.ssl.transport.enforce_cert_reload_dn_verification: false
```
{% include copy.html %}


只有[超級管理員]({{site.url}}{{site.baseurl}}/security/configuration/tls/#configuring-admin-certificates)才能使用 Reload Certificates API。
{: .note }

#### 在傳輸層重新載入 TLS 憑證

 以下命令使用 Reload Certificates API 在傳輸層重新載入 TLS 憑證：

```bash
curl --cacert <ca.pem> --cert <admin.pem> --key <admin.key> -XPUT https://localhost:9200/_plugins/_security/api/ssl/transport/reloadcerts
```
{% include copy.html %}

您應該會收到以下回應：

```
{ "message": "successfully updated transport certs"}
```

#### 在 HTTP 層重新載入 TLS 憑證

以下命令使用 Reload Certificates API 在 HTTP 層重新載入 TLS 憑證：

```bash
curl --cacert <ca.pem> --cert <admin.pem> --key <admin.key> -XPUT https://localhost:9200/_plugins/_security/api/ssl/http/reloadcerts
```
{% include copy.html %}

您應該會收到以下回應：

```
{ "message": "successfully updated http certs"}
```

## 為 gRPC 設定 TLS 憑證

您可以在 `opensearch.yml` 中為選用的 gRPC 傳輸設定 TLS。如需使用 gRPC 外掛程式的更多資訊，請參閱[啟用 gRPC API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/index/#grpc-settings)。

### PEM 金鑰設定 (X.509 PEM 憑證與 PKCS #8 金鑰)

下表列出可用的 gRPC PEM 金鑰設定。

名稱 | 說明
:--- | :---
`plugins.security.ssl.aux.secure-transport-grpc.enabled` | 是否為 gRPC 啟用 TLS。啟用後僅允許 HTTPS。選用。預設為 `false`。
`plugins.security.ssl.aux.secure-transport-grpc.pemkey_filepath` | 憑證金鑰檔案 (PKCS #8) 的路徑，以相對於 `config` 目錄的相對路徑指定。檔案必須位於 `config` 目錄內。必要。
`plugins.security.ssl.aux.secure-transport-grpc.pemkey_password` | 金鑰密碼。若金鑰沒有密碼，請省略此設定。選用。
`plugins.security.ssl.aux.secure-transport-grpc.pemcert_filepath` | X.509 節點憑證鏈 (PEM 格式) 的路徑，以相對於 `config` 目錄的相對路徑指定。檔案必須位於 `config` 目錄內。必要。
`plugins.security.ssl.aux.secure-transport-grpc.pemtrustedcas_filepath` | 根 CA (PEM 格式) 的路徑，以相對於 `config` 目錄的相對路徑指定。檔案必須位於 `config` 目錄內。必要。

### Keystore 與 truststore

下表列出可用的 gRPC keystore 與 truststore 設定。

名稱 | 說明
:--- | :---
`plugins.security.ssl.aux.secure-transport-grpc.enabled` | 是否為 gRPC 啟用 TLS。啟用後僅允許 HTTPS。選用。預設為 `false`。
`plugins.security.ssl.aux.secure-transport-grpc.keystore_type` | keystore 檔案的類型，JKS 或 PKCS12/PFX。選用。預設為 JKS。
`plugins.security.ssl.aux.secure-transport-grpc.keystore_filepath` | keystore 檔案的路徑，以相對於 `config` 目錄的相對路徑指定。檔案必須位於 `config` 目錄內。必要。
`plugins.security.ssl.aux.secure-transport-grpc.keystore_alias` | 要從提供的 keystore 中使用的金鑰組別名。選用。預設為新增至 keystore 的第一個金鑰組。
`plugins.security.ssl.aux.secure-transport-grpc.keystore_password` | keystore 的密碼。預設為 `changeit`。
`plugins.security.ssl.aux.secure-transport-grpc.truststore_type` | truststore 檔案的類型，JKS 或 PKCS12/PFX。預設為 JKS。
`plugins.security.ssl.aux.secure-transport-grpc.truststore_filepath` | truststore 檔案的路徑，以相對於 `config` 目錄的相對路徑指定。檔案必須位於 `config` 目錄內。必要。
`plugins.security.ssl.aux.secure-transport-grpc.truststore_alias` | 要從提供的 truststore 中使用的憑證別名。選用。預設為所有憑證。
`plugins.security.ssl.aux.secure-transport-grpc.truststore_password` | truststore 的密碼。預設為 `changeit`。

## 疑難排解

- 如需常見 TLS 組態問題的解決方案，請參閱 [TLS 疑難排解]({{site.url}}{{site.baseurl}}/security/configuration/troubleshoot-tls/)。
