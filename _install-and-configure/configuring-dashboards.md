---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定 OpenSearch Dashboards"
nav_order: 15
---

# 設定 OpenSearch Dashboards

OpenSearch Dashboards 啟動時會從 `opensearch_dashboards.yml` 組態檔讀取設定。檔案位置取決於您安裝 OpenSearch Dashboards 的方式。

安裝方式 | 檔案位置
:--- | :---
Docker | `/usr/share/opensearch-dashboards/config/opensearch_dashboards.yml`
Debian 或 RPM 套件 | `/etc/opensearch-dashboards/opensearch_dashboards.yml`
Tarball 或 Windows ZIP 封存檔 | OpenSearch Dashboards 安裝目錄中的 `config/opensearch_dashboards.yml`

變更 `opensearch_dashboards.yml` 後，請重新啟動 OpenSearch Dashboards 以套用變更。

部分 OpenSearch Dashboards 設定也可以在不編輯 `opensearch_dashboards.yml` 的情況下於 UI 中變更。如需詳細資訊，請參閱[進階設定]({{site.url}}{{site.baseurl}}/dashboards/management/advanced-settings/)。

## 範例組態檔

下列 `opensearch_dashboards.yml` 檔案將 OpenSearch Dashboards 設定為接受所有網路介面的連線，並連線至使用 Security 外掛程式的 OpenSearch 叢集：

```yaml
server.host: "0.0.0.0"
server.port: 5601
opensearch.hosts: ["https://localhost:9200"]
opensearch.username: "kibanaserver"
opensearch.password: "<kibanaserver-password>"
opensearch.ssl.verificationMode: full
opensearch.ssl.certificateAuthorities: ["/etc/opensearch-dashboards/root-ca.pem"]
opensearch.requestHeadersAllowlist: ["authorization", "securitytenant"]
```
{% include copy.html %}

請將 `<kibanaserver-password>` 替換為 `kibanaserver` 使用者的密碼，並更新憑證授權單位路徑以符合您的環境。有關 `kibanaserver` 使用者的資訊，請參閱[多租用戶組態]({{site.url}}{{site.baseurl}}/security/multi-tenancy/multi-tenancy-config/#kibana_server-role-details)。

如需所有設定的清單，請參閱 OpenSearch Dashboards 儲存庫中的範例 [`opensearch_dashboards.yml`](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/config/opensearch_dashboards.yml) 檔案。

## 伺服器設定

下表列出 OpenSearch Dashboards 伺服器的設定。

設定 | 資料類型 | 說明
:--- | :--- | :---
`server.host` | 字串 | OpenSearch Dashboards 伺服器繫結的主機名稱或 IP 位址。若要允許其他機器連線，請將此項設為非回送位址或 `0.0.0.0`。預設為 `localhost`。
`server.port` | 整數 | OpenSearch Dashboards 接聽的連接埠。預設為 `5601`。
`server.name` | 字串 | 此 OpenSearch Dashboards 執行個體的顯示名稱。預設為機器的主機名稱。
`server.basePath` | 字串 | 當 OpenSearch Dashboards 在反向代理後方執行時，提供服務的路徑，例如 `/dashboards`。必須以斜線（`/`）開頭，且結尾不可有斜線。預設為空。
`server.rewriteBasePath` | 布林值 | OpenSearch Dashboards 是否從傳入的請求路徑中移除 `server.basePath`。若您的反向代理在轉送請求前會移除基底路徑，請設為 `false`。預設為 `false`。

## OpenSearch 連線設定

下表列出控制 OpenSearch Dashboards 如何連線至 OpenSearch 的設定。

設定 | 資料類型 | 說明
:--- | :--- | :---
`opensearch.hosts` | 字串或字串陣列 | OpenSearch Dashboards 傳送請求的目標 OpenSearch 節點 URL。所有節點都必須屬於同一個叢集。預設為 `http://localhost:9200`。
`opensearch.username` | 字串 | OpenSearch Dashboards 伺服器用來連線至 OpenSearch 的使用者名稱，例如用於管理自身的系統索引。
`opensearch.password` | 字串 | `opensearch.username` 的密碼。
`opensearch.requestTimeout` | 整數 | 等待 OpenSearch 回應的時間，以毫秒為單位。預設為 `30000`（30 秒）。
`opensearch.pingTimeout` | 整數 | 等待 OpenSearch 回應 ping 的時間，以毫秒為單位。預設為 `opensearch.requestTimeout` 的值。
`opensearchDashboards.index` | 字串 | OpenSearch Dashboards 用來儲存已儲存物件（例如索引模式、視覺化和儀表板）的索引名稱。預設為 `.kibana`。

## TLS 設定

若要加密瀏覽器與 OpenSearch Dashboards 之間（`server.ssl.*` 設定）或 OpenSearch Dashboards 與 OpenSearch 之間（`opensearch.ssl.*` 設定）的流量，請參閱[為 OpenSearch Dashboards 設定 TLS]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/tls/)。

## Security 外掛程式設定

OpenSearch Dashboards 的 Security 外掛程式使用以 `opensearch_security` 開頭的設定。這些設定會在所屬功能的文件中一併說明：

- OpenID Connect (`opensearch_security.openid.*`)：請參閱 [OpenSearch Dashboards 單一登入]({{site.url}}{{site.baseurl}}/security/authentication-backends/openid-connect/#opensearch-dashboards-single-sign-on)。
- SAML (`opensearch_security.saml.*`)：請參閱 [OpenSearch Dashboards 設定]({{site.url}}{{site.baseurl}}/security/authentication-backends/saml/#opensearch-dashboards-settings)。
- 登入頁面上的多種驗證類型 (`opensearch_security.auth.*`)：請參閱 [為多種驗證選項設定 Dashboards 登入]({{site.url}}{{site.baseurl}}/security/configuration/multi-auth/)。
- 多租用戶 (`opensearch_security.multitenancy.*`)：請參閱 [多租用戶組態]({{site.url}}{{site.baseurl}}/security/multi-tenancy/multi-tenancy-config/)。

## 記錄設定

根據預設，OpenSearch Dashboards 會將記錄寫入標準輸出。下表列出記錄設定。

設定 | 資料類型 | 說明
:--- | :--- | :---
`logging.dest` | 字串 | 記錄的寫入位置。設為 `stdout` 或記錄檔的路徑。預設為 `stdout`。
`logging.silent` | 布林值 | 若為 `true`，OpenSearch Dashboards 不會寫入任何記錄。預設為 `false`。
`logging.quiet` | 布林值 | 若為 `true`，OpenSearch Dashboards 只會寫入錯誤訊息。預設為 `false`。
`logging.verbose` | 布林值 | 若為 `true`，OpenSearch Dashboards 會記錄所有事件，包括系統使用資訊及所有請求。預設為 `false`。

## 語言設定

若要以英文以外的語言顯示 OpenSearch Dashboards 介面，請將 `i18n.locale` 設定為地區設定識別碼，例如：

```yaml
i18n.locale: "fr-FR"
```
{% include copy.html %}

預設值為 `en`。每個可用的地區設定在 OpenSearch Dashboards 儲存庫的 [`src/translations`](https://github.com/opensearch-project/OpenSearch-Dashboards/tree/main/src/translations) 目錄中都有對應的翻譯檔案，並以其地區設定識別碼命名。翻譯可能不完整，因此部分文字仍可能以英文顯示。

## 相關文件

- [設定與管理]({{site.url}}{{site.baseurl}}/dashboards/settings-and-administration/)
- [進階設定]({{site.url}}{{site.baseurl}}/dashboards/management/advanced-settings/)
