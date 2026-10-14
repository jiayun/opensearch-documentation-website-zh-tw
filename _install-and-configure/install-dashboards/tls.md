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

根據預設，為了方便測試與入門，OpenSearch Dashboards 透過 HTTP 執行。

下表列出 OpenSearch Dashboards 依您的組態所使用的憑證。

憑證 | 設定 | 說明
:--- | :--- | :---
伺服器憑證與金鑰 | `server.ssl.certificate`, `server.ssl.key` | OpenSearch Dashboards 透過 HTTPS 向網頁瀏覽器呈現的憑證。請使用為 OpenSearch Dashboards 主機簽發的憑證。此憑證與 OpenSearch 節點憑證不同。
CA 憑證 | `opensearch.ssl.certificateAuthorities` | 簽署 OpenSearch 節點憑證之 CA 的憑證。OpenSearch Dashboards 使用這些憑證來驗證 OpenSearch，因此它們與您的 OpenSearch 叢集所使用的 CA 憑證相同。
用戶端憑證與金鑰 | `opensearch.ssl.certificate`, `opensearch.ssl.key` | 僅在 OpenSearch 要求 OpenSearch Dashboards 使用憑證進行驗證（mTLS）時才需要。此憑證必須由 OpenSearch 信任的 CA 簽署。

若要為 HTTPS 啟用 TLS，請在 `opensearch_dashboards.yml` 中更新下列設定。

設定 | 說明
:--- | :---
`server.ssl.enabled` | 啟用 OpenSearch Dashboards 伺服器與使用者網頁瀏覽器之間的 SSL 通訊。設為 `true` 表示 HTTPS，設為 `false` 表示 HTTP。
`server.ssl.supportedProtocols` | 指定支援的 TLS 通訊協定陣列。有效值為 `TLSv1`、`TLSv1.1`、`TLSv1.2` 及 `TLSv1.3`。預設為 `['TLSv1.1', 'TLSv1.2', and 'TLSv1.3']`。
`server.ssl.cipherSuites` | 指定 TLS 加密套件陣列。選用。
`server.ssl.certificate` | 若 `server.ssl.enabled` 設為 `true`，則指定 OpenSearch Dashboards 有效 Privacy Enhanced Mail（PEM）伺服器憑證的完整路徑。您可以[產生自己的憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/)，或向憑證授權單位（CA）取得。
`server.ssl.key` | 若 `server.ssl.enabled` 設為 `true`，則指定伺服器憑證金鑰的完整路徑，例如 `/usr/share/opensearch-dashboards-1.0.0/config/my-client-cert-key.pem`。您可以[產生自己的憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/)，或向 CA 取得。
`server.ssl.keyPassphrase` | 設定金鑰的密碼。若金鑰沒有密碼，請省略此設定。選用。
`server.ssl.keystore.path` | 使用 JKS（Java KeyStore）或 PKCS12/PFX（Public-Key Cryptography Standards）檔案，而非 PEM 憑證與金鑰。
`server.ssl.keystore.password` | 設定金鑰庫的密碼。必要。
`server.ssl.clientAuthentication` | 指定要使用的 TLS 用戶端驗證模式。可為下列其中一項：`none`、`optional` 或 `required`。若設為 `required`，您的網頁瀏覽器需要傳送由 `server.ssl.certificateAuthorities` 中所設定 CA 簽署的有效用戶端憑證。預設為 `none`。
`server.ssl.certificateAuthorities` | 以陣列指定一或多個 CA 憑證的完整路徑，這些憑證簽發用於用戶端驗證的憑證。若 `server.ssl.clientAuthentication` 設為 `optional` 或 `required`，則為必要。
`server.ssl.truststore.path` | 使用 JKS 或 PKCS12/PFX 信任庫檔案，而非 PEM CA 憑證。
`server.ssl.truststore.password` | 設定信任庫的密碼。必要。
`opensearch.ssl.verificationMode` | 建立 OpenSearch 與 OpenSearch Dashboards 之間的通訊。有效值為 `full`、`certificate` 或 `none`。若啟用 TLS，建議使用 `full`，其會啟用主機名稱驗證。`certificate` 會檢查憑證但不檢查主機名稱。`none` 不執行任何檢查（適用於 HTTP）。預設為 `full`。
`opensearch.ssl.certificateAuthorities` | 若 `opensearch.ssl.verificationMode` 設為 `full` 或 `certificate`，則以陣列指定一或多個 CA 憑證的完整路徑，這些憑證構成 OpenSearch 叢集的信任鏈。例如，若您使用中繼 CA 來簽發您的管理、用戶端及節點憑證，您可能需要同時包含根 CA _及_ 中繼 CA。
`opensearch.ssl.truststore.path` | 使用 JKS 或 PKCS12/PFX 信任庫檔案，而非 PEM CA 憑證。
`opensearch.ssl.truststore.password` | 設定信任庫的密碼。必要。
`opensearch.ssl.alwaysPresentCertificate` | 若設為 `true`，則將用戶端憑證傳送至 OpenSearch 叢集，當 OpenSearch 中啟用 mTLS 時此為必要。預設為 `false`。
`opensearch.ssl.certificate` | 若 `opensearch.ssl.alwaysPresentCertificate` 設為 `true`，則指定 OpenSearch 叢集有效用戶端憑證的完整路徑。您可以[產生自己的憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/)，或向 CA 取得。
`opensearch.ssl.key` | 若 `opensearch.ssl.alwaysPresentCertificate` 設為 `true`，則指定用戶端憑證金鑰的完整路徑。您可以[產生自己的憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/)，或向 CA 取得。
`opensearch.ssl.keyPassphrase` | 設定金鑰的密碼。若金鑰沒有密碼，請省略此設定。選用。
`opensearch.ssl.keystore.path` | 使用 JKS 或 PKCS12/PFX 金鑰庫檔案，而非 PEM 憑證與金鑰。
`opensearch.ssl.keystore.password` | 設定金鑰庫的密碼。必要。
`opensearch_security.cookie.secure` | 若為 OpenSearch Dashboards 啟用 TLS，請將此設定變更為 `true`。若為 HTTP，請設為 `false`。
`opensearch_security.session.keepalive`| 決定是否在每次使用者活動時重設工作階段 TTL（「保持運作」）。選用。預設為 `true`。
`opensearch_security.session.ttl`| 定義使用者工作階段的存留時間（TTL），以毫秒為單位。選用。預設為 `3600000`（1 小時）。

## 範例：OpenSearch Dashboards 與 OpenSearch 位於同一部機器

下列範例為執行於與使用示範安全性組態之 OpenSearch 節點相同機器上的 OpenSearch Dashboards 設定 TLS。此範例需要在 OpenSearch Dashboards 的 `config` 目錄中有下列檔案：

- `root-ca.pem`：簽署 OpenSearch 節點憑證的根 CA 憑證。示範安全性組態會在 OpenSearch 的 `config` 目錄中建立此檔案，例如 Docker 為 `/usr/share/opensearch/config/`、RPM 與 Debian 為 `/etc/opensearch/`，或 tar 壓縮檔安裝的 `config` 目錄。請將其複製到 OpenSearch Dashboards 的 `config` 目錄。
- `client-cert.pem` 與 `client-cert-key.pem`：OpenSearch Dashboards 向網頁瀏覽器呈現的憑證與金鑰。示範安全性組態不會建立這些檔案。您可以[產生自己的憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/)，或向 CA 取得。若要測試，您可以使用下列命令建立自簽憑證與金鑰：

  ```bash
  openssl req -x509 -newkey rsa:2048 -nodes -keyout client-cert-key.pem -out client-cert.pem -days 30 -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost"
  ```
  {% include copy.html %}

若 `opensearch_dashboards.yml` 中指定的憑證或金鑰檔案不存在，OpenSearch Dashboards 會因 `ENOENT: no such file or directory` 錯誤而無法啟動。
{: .note}

示範節點憑證包含 `localhost` 作為主體別名，因此當 `opensearch.hosts` 使用 `localhost` 時，`full` 驗證模式會成功。

將下列設定新增至 `opensearch_dashboards.yml`：

```yml
server.host: '0.0.0.0'
server.ssl.enabled: true
server.ssl.certificate: /usr/share/opensearch-dashboards/config/client-cert.pem
server.ssl.key: /usr/share/opensearch-dashboards/config/client-cert-key.pem
opensearch.hosts: ["https://localhost:9200"]
opensearch.ssl.verificationMode: full
opensearch.ssl.certificateAuthorities: [ "/usr/share/opensearch-dashboards/config/root-ca.pem" ]
opensearch.username: "kibanaserver"
opensearch.password: "kibanaserver"
opensearch.requestHeadersAllowlist: [ authorization,securitytenant ]
opensearch_security.multitenancy.enabled: true
opensearch_security.multitenancy.tenants.preferred: ["Private", "Global"]
opensearch_security.readonly_mode.roles: ["kibana_read_only"]
opensearch_security.cookie.secure: true
```
{% include copy.html %}

若您的 OpenSearch 憑證由中繼 CA 簽署，請將中繼 CA 憑證新增至 `opensearch_dashboards.yml` 中的 `opensearch.ssl.certificateAuthorities`：

```yml
opensearch.ssl.certificateAuthorities: [ "/usr/share/opensearch-dashboards/config/root-ca.pem", "/usr/share/opensearch-dashboards/config/intermediate-ca.pem" ]
```
{% include copy.html %}

若您使用 Docker 安裝選項，您可以將自訂的 `opensearch_dashboards.yml` 檔案傳遞至容器。若要深入了解，請參閱 [Docker 安裝頁面]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/docker/)。

啟用這些設定並啟動應用程式後，您可以在 `https://localhost:5601` 連線至 OpenSearch Dashboards。若您的憑證為自簽，您可能需要確認瀏覽器警告。為避免這類警告（或瀏覽器完全不相容），最佳做法是使用來自受信任 CA 的憑證。
