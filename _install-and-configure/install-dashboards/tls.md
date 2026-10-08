---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定 TLS"
parent: Installing OpenSearch Dashboards
nav_order: 50
redirect_from:
  - /dashboards/install/tls/
---

# 為 OpenSearch Dashboards 設定 TLS

為了方便測試與入門，OpenSearch Dashboards 預設透過 HTTP 執行。若要為 HTTPS 啟用 TLS，請更新 `opensearch_dashboards.yml` 中的下列設定。

設定 | 說明
:--- | :---
`server.ssl.enabled` | 啟用 OpenSearch Dashboards 伺服器與使用者網頁瀏覽器之間的 SSL 通訊。設定為 `true` 以使用 HTTPS，或 `false` 以使用 HTTP。
`server.ssl.supportedProtocols` | 指定支援的 TLS 協定陣列。可能的值為 `TLSv1`、`TLSv1.1` 以及 `TLSv1.2`、`TLSv1.3`。預設值為 `['TLSv1.1', 'TLSv1.2', and 'TLSv1.3']`。
`server.ssl.cipherSuites` | 指定 TLS 加密套件陣列。選用。
`server.ssl.certificate` | 如果 `server.ssl.enabled` 設定為 `true`，則指定 OpenSearch Dashboards 有效的 Privacy Enhanced Mail (PEM) 伺服器憑證之完整路徑。您可以 [產生自己的憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/) 或從憑證授權單位 (CA) 獲取。
`server.ssl.key` | 如果 `server.ssl.enabled` 設定為 `true`，則指定伺服器憑證金鑰的完整路徑，例如 `/usr/share/opensearch-dashboards-1.0.0/config/my-client-cert-key.pem`。您可以 [產生自己的憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/) 或從 CA 獲取。
`server.ssl.keyPassphrase` | 設定金鑰的密碼。如果金鑰沒有密碼，請省略此設定。選用。
`server.ssl.keystore.path` | 使用 JKS (Java KeyStore) 或 PKCS12/PFX (Public-Key Cryptography Standards) 檔案，而非 PEM 憑證與金鑰。
`server.ssl.keystore.password` | 設定 keystore 的密碼。必要。
`server.ssl.clientAuthentication` | 指定要使用的 TLS 用戶端驗證模式。可以是下列其中之一：`none`、`optional` 或 `required`。如果設定為 `required`，您的網頁瀏覽器需要傳送由 `server.ssl.certificateAuthorities` 中設定的 CA 所簽署的有效用戶端憑證。預設值為 `none`。
`server.ssl.certificateAuthorities` | 在陣列中指定一個或多個核發用戶端驗證憑證之 CA 憑證的完整路徑。如果 `server.ssl.clientAuthentication` 設定為 `optional` 或 `required` 則為必要。
`server.ssl.truststore.path` | 使用 JKS 或 PKCS12/PFX truststore 檔案，而非 PEM CA 憑證。
`server.ssl.truststore.password` | 設定 truststore 的密碼。必要。
`opensearch.ssl.verificationMode` | 建立 OpenSearch 與 OpenSearch Dashboards 之間的通訊。有效值為 `full`、`certificate` 或 `none`。如果啟用了 TLS，建議使用 `full`，這將啟用主機名稱驗證。`certificate` 會檢查憑證但不會檢查主機名稱。`none` 不執行任何檢查（適用於 HTTP）。預設值為 `full`。
`opensearch.ssl.certificateAuthorities` | 如果 `opensearch.ssl.verificationMode` 設定為 `full` 或 `certificate`，則在陣列中指定一個或多個組成 OpenSearch 叢集信任鏈之 CA 憑證的完整路徑。例如，如果您使用中間 CA 來核發管理員、用戶端和節點憑證，則可能需要包含根 CA _以及_ 中間 CA。
`opensearch.ssl.truststore.path` | 使用 JKS 或 PKCS12/PFX truststore 檔案，而非 PEM CA 憑證。
`opensearch.ssl.truststore.password` | 設定 truststore 的密碼。必要。
`opensearch.ssl.alwaysPresentCertificate` | 如果設定為 `true`，則將用戶端憑證傳送至 OpenSearch 叢集，這在 OpenSearch 啟用 mTLS 時是必要的。預設值為 `false`。
`opensearch.ssl.certificate` | 如果 `opensearch.ssl.alwaysPresentCertificate` 設定為 `true`，則指定 OpenSearch 叢集有效用戶端憑證的完整路徑。您可以 [產生自己的憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/) 或從 CA 獲取。
`opensearch.ssl.key` | 如果 `opensearch.ssl.alwaysPresentCertificate` 設定為 `true`，則指定用戶端憑證金鑰的完整路徑。您可以 [產生自己的憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/) 或從 CA 獲取。
`opensearch.ssl.keyPassphrase` | 設定金鑰的密碼。如果金鑰沒有密碼，請省略此設定。選用。
`opensearch.ssl.keystore.path` | 使用 JKS 或 PKCS12/PFX keystore 檔案，而非 PEM 憑證與金鑰。
`opensearch.ssl.keystore.password` | 設定 keystore 的密碼。必要。
`opensearch_security.cookie.secure` | 如果 OpenSearch Dashboards 啟用了 TLS，請將此設定更改為 `true`。對於 HTTP，請將其設定為 `false`。
`opensearch_security.session.keepalive`| 決定每次使用者活動時是否重設（「保持活動」）工作階段 TTL。選用。預設值為 `true`。
`opensearch_security.session.ttl`| 定義使用者工作階段的存活時間 (TTL)，單位為毫秒。選用。預設值為 `3600000` (1 小時)。

下列 `opensearch_dashboards.yml` 組態顯示 OpenSearch 與 OpenSearch Dashboards 使用示範組態在同一台機器上執行：

```yml
server.host: '0.0.0.0'
server.ssl.enabled: true
server.ssl.certificate: /usr/share/opensearch-dashboards/config/client-cert.pem
server.ssl.key: /usr/share/opensearch-dashboards/config/client-cert-key.pem
opensearch.hosts: ["https://localhost:9200"]
opensearch.ssl.verificationMode: full
opensearch.ssl.certificateAuthorities: [ "/usr/share/opensearch-dashboards/config/root-ca.pem", "/usr/share/opensearch-dashboards/config/intermediate-ca.pem" ]
opensearch.username: "kibanaserver"
opensearch.password: "kibanaserver"
opensearch.requestHeadersAllowlist: [ authorization,securitytenant ]
opensearch_security.multitenancy.enabled: true
opensearch_security.multitenancy.tenants.preferred: ["Private", "Global"]
opensearch_security.readonly_mode.roles: ["kibana_read_only"]
opensearch_security.cookie.secure: true
```

如果您使用 Docker 安裝選項，可以將自訂的 `opensearch_dashboards.yml` 檔案傳遞給容器。若要了解更多資訊，請參閱 [Docker 安裝頁面]({{site.url}}{{site.baseurl}}/opensearch/install/docker/)。

在啟用這些設定並啟動應用程式後，您可以連線至 `https://localhost:5601` 的 OpenSearch Dashboards。如果您的憑證是自我簽署的，您可能需要確認瀏覽器警告。為了避免這類警告（或完全的瀏覽器不相容），最佳做法是使用來自受信任 CA 的憑證。
