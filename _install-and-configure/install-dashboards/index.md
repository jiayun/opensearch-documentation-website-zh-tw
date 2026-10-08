---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安裝 OpenSearch Dashboards"
nav_order: 3
has_children: true
redirect_from:
  - /dashboards/install/index/
  - /dashboards/compatibility/
  - /install-and-configure/install-dashboards/
---

# 安裝 OpenSearch Dashboards

OpenSearch Dashboards 是 OpenSearch 的使用者介面。您可以使用它來探索、視覺化以及查詢您的資料。您可以使用以下任何一種方法來安裝 OpenSearch Dashboards：

- [Docker]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/docker/)
- [OpenSearch Kubernetes Operator]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/)，可將 OpenSearch 與 OpenSearch Dashboards 一併安裝
- [Helm]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/helm/)
- [Debian]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/debian/)
- [RPM]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/rpm/)
- [Tarball]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/tar/)
- [Ansible playbook]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/ansible/)，可將 OpenSearch 與 OpenSearch Dashboards 一併安裝
- [Windows]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/windows/)

OpenSearch Dashboards 會連接到現有的 OpenSearch 叢集，因此請先安裝 OpenSearch。如需更多資訊，請參閱 [安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/)。

## 為生產環境準備 OpenSearch Dashboards

[安裝快速入門]({{site.url}}{{site.baseurl}}/getting-started/quickstart/) 以及大多數指南中的預設組態，是使用示範安全性組態將 OpenSearch Dashboards 連接至 OpenSearch。在此組態中，OpenSearch Dashboards 透過 HTTP 提供頁面，不會驗證 OpenSearch 憑證，並使用 `kibanaserver` 使用者的已知預設密碼對 OpenSearch 進行驗證。在生產環境中使用 OpenSearch Dashboards 之前，請完成以下任務：

- 為生產環境準備 OpenSearch 叢集。如需更多資訊，請參閱 [為生產環境準備叢集]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production)。
- 在瀏覽器與 OpenSearch Dashboards 之間啟用 TLS，並將 `opensearch.ssl.verificationMode` 設定為 `full` 以驗證 OpenSearch 憑證。如需更多資訊，請參閱 [為 OpenSearch Dashboards 設定 TLS]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/tls/)。
- 變更 `kibanaserver` 密碼。如需更多資訊，請參閱 [Dashboards 服務帳戶密碼]({{site.url}}{{site.baseurl}}/security/configuration/passwords/#dashboards-service-account-password)。
- 設定使用者的登入方式。如需更多資訊，請參閱 [設定登入選項]({{site.url}}{{site.baseurl}}/security/configuration/multi-auth/)。

## 存取 OpenSearch Dashboards

安裝並啟動 OpenSearch Dashboards 後，請在網頁瀏覽器中開啟它：

1. 前往 `http://localhost:5601`。OpenSearch Dashboards 預設監聽連接埠 `5601`。如果 OpenSearch Dashboards 執行在不同的主機上，請將 `localhost` 替換為該主機的 IP 位址或 DNS 名稱。

   預設情況下，tarball、RPM 和 Debian 安裝會將 OpenSearch Dashboards 綁定到 `localhost`，因此您無法從其他主機存取。若要允許從其他主機存取，請在 `opensearch_dashboards.yml` 中將 `server.host` 設定為 `0.0.0.0` 或主機的 IP 位址，然後重新啟動 OpenSearch Dashboards。

1. 使用您在安裝 OpenSearch 時設定的自訂管理員密碼，以 `admin` 使用者身分登入。如果您停用了 Security 外掛程式，則不需要登入。

OpenSearch Dashboards 可能需要約 1 分鐘才能啟動。如果頁面無法載入或返回 `503` 錯誤，請稍候然後重新載入頁面。

如果您無法登入，請參閱 [常見問題](#common-issues)。

若要學習如何使用 OpenSearch Dashboards，請參閱 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/index/)。

## 瀏覽器相容性

OpenSearch Dashboards 支援以下網頁瀏覽器：

- Chrome
- Firefox
- Safari
- Edge (Chromium)

其他基於 Chromium 的瀏覽器可能也可以運作。Internet Explorer 和 Microsoft Edge Legacy **不**受支援。

<!-- vale off -->
## Node.js 相容性
<!-- vale on -->

OpenSearch Dashboards 需要 Node.js 執行階段二進位檔才能執行。在 [OpenSearch 下載頁面](https://opensearch.org/downloads.html){:target='\_blank'}提供的發行套件中已包含一個。

OpenSearch Dashboards 2.8 至 2.19 版本支援 Node.js 14、16 和 18。2.10 至 2.19 版本的發行套件包含 Node.js 18 和 Node.js 14（為了向下相容）。

OpenSearch Dashboards 3.0 至 3.4 版本包含 Node.js 20。3.5 及更高版本包含 Node.js 22。

若要使用發行套件中包含的以外的 Node.js 執行階段二進位檔，請執行以下步驟：

1. 下載並安裝 [Node.js](https://nodejs.org/en/download){:target='\_blank'}。相容版本為 `>=14.20.1 <23`。
1. 將 `OSD_NODE_HOME` 或 `NODE_HOME` 環境變數設定為 Node.js 安裝目錄：

    - 在 Linux 或 macOS 上，如果 Node.js 安裝在 `/usr/local/nodejs` 且執行階段二進位檔為 `/usr/local/nodejs/bin/node`：

      ```bash
      export NODE_HOME=/usr/local/nodejs
      ```

    - 如果使用 NVM 安裝 Node.js 且執行階段二進位檔為 `/Users/user/.nvm/versions/node/v22.22.3/bin/node`：

      ```bash
      export NODE_HOME=/Users/user/.nvm/versions/node/v22.22.3
      # or, if NODE_HOME is used for something else:
      export OSD_NODE_HOME=/Users/user/.nvm/versions/node/v22.22.3
      ```

    - 在 Windows 上，如果 Node.js 安裝在 `C:\Program Files\nodejs` 且執行階段二進位檔為 `C:\Program Files\nodejs\node.exe`，請在命令提示字元中使用以下命令：

      ```bat
      set "NODE_HOME=C:\Program Files\nodejs"
      ```

      或者，在 PowerShell 中使用以下命令：

      ```powershell
      $Env:NODE_HOME = 'C:\Program Files\nodejs'
      ```

   請參閱您的作業系統文件，以對環境變數進行永久性變更。

OpenSearch Dashboards 啟動指令碼 `bin/opensearch-dashboards` 會先使用 `OSD_NODE_HOME` 然後使用 `NODE_HOME` 搜尋 Node.js 執行階段二進位檔，最後才使用發行套件中包含的二進位檔。如果找不到可用的 Node.js 執行階段二進位檔，啟動指令碼會在失敗前嘗試在系統全域的 `PATH` 中尋找。

## 組態

若要學習如何為 OpenSearch Dashboards 設定 TLS，請參閱 [為 OpenSearch Dashboards 設定 TLS]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/tls/)。

## 常見問題

如果 OpenSearch Dashboards 無法啟動或您無法登入，請查看這些常見問題及建議的解決方案。

### 錯誤訊息：「Request Timeout after 30000ms」

如果在 OpenSearch Dashboards 啟動時遇到錯誤 `FATAL  Error: Request Timeout after 30000ms`，請在資源較多的主機上執行 OpenSearch Dashboards。我們建議使用 4 個 CPU 核心和 8 GB RAM。

### 您無法登入 OpenSearch Dashboards

OpenSearch Dashboards 沒有自己的使用者。您使用在 OpenSearch Security 外掛程式中定義的使用者登入。安裝後，請使用您在安裝 OpenSearch 時於 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 中設定的密碼，以 `admin` 使用者身分登入。`admin` 使用者沒有預設密碼，因此使用 `admin` 作為密碼將無法運作。`kibanaserver` 使用者是 OpenSearch Dashboards 用於連接到 OpenSearch 的帳戶，並非設計用於登入。

### 在 OpenSearch 中停用安全性後出現登入頁面

如果您在 OpenSearch 中停用了 Security 外掛程式，也請將 Security 外掛程式從 OpenSearch Dashboards 中移除。否則，OpenSearch Dashboards 會顯示登入頁面，但任何憑據都無法運作。如需更多資訊，請參閱 [從 OpenSearch Dashboards 移除 Security 外掛程式]({{site.url}}{{site.baseurl}}/security/configuration/disable-enable-security/#removing-the-security-plugin-from-opensearch-dashboards)。

### 錯誤訊息：「OpenSearch Dashboards server is not ready yet」

此訊息表示 OpenSearch Dashboards 無法連接到 OpenSearch。若要找出原因，請執行以下步驟：

1. 透過直接向 OpenSearch 發送請求，確認 OpenSearch 正在執行：

   ```bash
   curl https://localhost:9200 -u admin:<custom-admin-password> --insecure
   ```
   {% include copy.html %}

   如果此請求失敗，問題出在 OpenSearch 而非 OpenSearch Dashboards。請檢查 OpenSearch 記錄檔。

1. 確認 `opensearch_dashboards.yml` 中的 `opensearch.hosts` 包含 OpenSearch 的位址。

1. 確認 `opensearch_dashboards.yml` 中的 `opensearch.username` 和 `opensearch.password` 與 OpenSearch 中 `kibanaserver` 使用者的憑據相符。如果您變更了 `internal_users.yml` 中的 `kibanaserver` 密碼，請將 `opensearch.password` 設定為新的明文密碼，然後重新啟動 OpenSearch Dashboards。

### 錯誤訊息：「Client network socket disconnected before secure TLS connection was established」

OpenSearch Dashboards 使用 `opensearch.hosts` 中的協定連接到 OpenSearch。此錯誤表示 OpenSearch Dashboards 嘗試使用 HTTPS 連接，但 OpenSearch 未完成 TLS 握手。如果 OpenSearch 中停用了 Security 外掛程式，OpenSearch 會提供 HTTP，因此請在 `opensearch.hosts` 中使用 `http://`。如果啟用了 Security 外掛程式，請使用 `https://`。
