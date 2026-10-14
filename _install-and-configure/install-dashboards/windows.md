---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Windows
parent: Installing OpenSearch Dashboards
nav_order: 40
redirect_from: 
  - /dashboards/install/windows/
---

<!-- vale off -->
# 在 Windows 上安裝 OpenSearch Dashboards
<!-- vale on -->

## 必要條件

在安裝 OpenSearch Dashboards 之前，請先完成下列工作：

- 安裝 OpenSearch。如需更多資訊，請參閱[在 Windows 上安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/windows/)。
- 安裝 zip 公用程式。

## 在 Windows 上安裝 OpenSearch Dashboards

若要在 Windows 上安裝 OpenSearch Dashboards，請依照下列步驟操作：

1. 下載 [`opensearch-dashboards-{{site.opensearch_dashboards_version}}-windows-x64.zip`](https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/{{site.opensearch_dashboards_version}}/opensearch-dashboards-{{site.opensearch_dashboards_version}}-windows-x64.zip){:target='\_blank'} 封存檔。

1. 若要解壓縮封存檔內容，請按右鍵選取 **Extract All**。此封存檔包含約 100,000 個檔案，因此以這種方式解壓縮可能需要很長時間。或者，您也可以從命令提示字元或 PowerShell 使用 Windows 內建的 `tar` 命令來解壓縮封存檔，速度會更快：

   ```bat
   tar -xf opensearch-dashboards-{{site.opensearch_dashboards_version}}-windows-x64.zip
   ```
   {% include copy.html %}

   **注意**：封存檔中有些檔案路徑接近某些 Windows 版本 260 個字元的路徑長度上限。將封存檔解壓縮到較短的路徑，例如 `C:\opensearch`，有助於避免路徑長度錯誤。如果您在解壓縮封存檔時遇到與路徑長度相關的錯誤，請執行下列步驟以啟用長路徑支援：

   1. 在工作列上 **Start** 旁的搜尋方塊中輸入 `powershell` 以開啟 Powershell。
   1. 在 Powershell 中執行下列命令：
      ```powershell
      Set-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem LongPathsEnabled -Type DWORD -Value 1 -Force
      ```
      {% include copy.html %}
   1. 重新啟動您的電腦。

1. 設定 OpenSearch Dashboards。

    依據 OpenSearch 是啟用或停用安全性來設定，有兩種設定 OpenSearch Dashboards 的方式。

    對 `opensearch_dashboards.yml` 檔案所做的任何變更，都必須重新啟動 OpenSearch Dashboards 才會生效。
    {: .note}

    1. 選項 1 -- 啟用安全性：
  
        組態檔 `\path\to\opensearch-dashboards-{{site.opensearch_dashboards_version}}\config\opensearch_dashboards.yml` 出廠時已包含下列基本設定：
        
        ```yaml
        opensearch.hosts: [https://localhost:9200]
        opensearch.ssl.verificationMode: none
        opensearch.username: kibanaserver
        opensearch.password: kibanaserver
        opensearch.requestHeadersWhitelist: [authorization, securitytenant]
        
        opensearch_security.multitenancy.enabled: true
        opensearch_security.multitenancy.tenants.preferred: [Private, Global]
        opensearch_security.readonly_mode.roles: [kibana_read_only]
        # Use this setting if you are running opensearch-dashboards without https
        opensearch_security.cookie.secure: false
        ```
    
    1. 選項 2 -- 停用 OpenSearch 安全性：

        如果您使用的是停用安全性的 OpenSearch，請使用下列命令從 OpenSearch Dashboards 移除 Security 外掛程式：
        
        ```bat
        \path\to\opensearch-dashboards-{{site.opensearch_dashboards_version}}\bin\opensearch-dashboards-plugin.bat remove securityDashboards
        ```
        {% include copy.html %}
        
        然後將 `opensearch_dashboards.yml` 檔案的內容替換為下列設定：
        
        ```yaml
        opensearch.hosts: [http://localhost:9200]
        ```
        {% include copy.html %}

        移除 Security 外掛程式後，如果 `opensearch_dashboards.yml` 仍包含 `opensearch_security` 設定，OpenSearch Dashboards 將無法啟動並出現 `Unknown configuration key(s)` 錯誤。請務必移除所有出廠預設的設定。
        {: .note}
         
        請注意使用的是純 `http` 方法，而非 `https`。
        {: .note}
    
1. 執行 OpenSearch Dashboards。

   執行 OpenSearch Dashboards 有兩種方式：

   1. 使用 Windows UI 執行批次指令碼：

      1. 前往 OpenSearch Dashboards 安裝目錄的最上層目錄，並開啟 `opensearch-dashboards-{{site.opensearch_dashboards_version}}` 資料夾。
      1. 開啟 `bin` 資料夾，並按兩下 `opensearch-dashboards.bat` 檔案來執行批次指令碼。這會開啟一個命令提示字元視窗，其中執行著 OpenSearch Dashboards 執行個體。

   1. 從命令提示字元或 Powershell 執行批次指令碼：

      1. 在工作列上 **Start** 旁的搜尋方塊中輸入 `cmd` 以開啟命令提示字元，或輸入 `powershell` 以開啟 Powershell。
      1. 切換到 OpenSearch Dashboards 安裝的最上層目錄。
         ```bat
         cd \path\to\opensearch-dashboards-{{site.opensearch_dashboards_version}}
         ```
         {% include copy.html %}
      1. 執行批次指令碼以啟動 OpenSearch Dashboards。
         ```bat
         .\bin\opensearch-dashboards.bat
         ```
         {% include copy.html %}

1. 在網頁瀏覽器中前往 `http://localhost:5601`。OpenSearch Dashboards 可能需要約 2 分鐘才能啟動。如果您在設定 OpenSearch Dashboards 時啟用了安全性，請使用安裝 OpenSearch 時設定的自訂管理員密碼，以 `admin` 使用者身分登入。如果 OpenSearch Dashboards 執行於遠端主機，請將 `localhost` 替換為該主機的 IP 位址或 DNS 名稱。如需更多資訊，請參閱[存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#accessing-opensearch-dashboards)。

若要停止 OpenSearch Dashboards，請在命令提示字元或 Powershell 中按 `Ctrl+C`，或關閉命令提示字元或 Powershell 視窗。
{: .tip}

## 相關文件

- [為正式環境準備 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)
