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

1. 下載 [`opensearch-dashboards-{{site.opensearch_dashboards_version}}-windows-x64.zip`](https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/{{site.opensearch_dashboards_version}}/opensearch-dashboards-{{site.opensearch_dashboards_version}}-windows-x64.zip){:target='\_blank'} 壓縮檔。

1. 若要解壓縮壓縮檔內容，請按一下滑鼠右鍵並選取 **Extract All**。壓縮檔包含約 100,000 個檔案，因此以這種方式解壓縮可能需要很長的時間。您也可以在命令提示字元或 PowerShell 中使用 Windows 隨附的 `tar` 命令解壓縮，速度較快：

   ```bat
   tar -xf opensearch-dashboards-{{site.opensearch_dashboards_version}}-windows-x64.zip
   ```
   {% include copy.html %}

   **注意**：壓縮檔中的某些檔案路徑接近部分 Windows 版本的 260 個字元路徑長度限制。將壓縮檔解壓縮至較短的路徑（例如 `C:\opensearch`）有助於避免路徑長度錯誤。如果您在解壓縮時遇到與路徑長度相關的錯誤，請執行下列步驟以啟用長路徑支援：

   1. 在工作列上 **Start** 旁的搜尋方塊中輸入 `powershell`，以開啟 PowerShell。 
   1. 在 PowerShell 中執行下列命令：
      ```powershell
      Set-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem LongPathsEnabled -Type DWORD -Value 1 -Force
      ```
      {% include copy.html %}
   1. 重新啟動您的電腦。

1. 設定 OpenSearch Dashboards。

    設定 OpenSearch Dashboards 的方式有兩種，取決於 OpenSearch 是否啟用安全性。

    若要讓 `opensearch_dashboards.yml` 檔案的任何變更生效，必須重新啟動 OpenSearch Dashboards。
    {: .note}

    1. 選項 1 -- 啟用安全性：
  
        組態檔案 `\path\to\opensearch-dashboards-{{site.opensearch_dashboards_version}}\config\opensearch_dashboards.yml` 隨附下列基本設定：
        
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

        如果您使用的 OpenSearch 已停用安全性，請使用下列命令從 OpenSearch Dashboards 移除 Security 外掛程式：
        
        ```bat
        \path\to\opensearch-dashboards-{{site.opensearch_dashboards_version}}\bin\opensearch-dashboards-plugin.bat remove securityDashboards
        ```
        {% include copy.html %}
        
        接著，將 `opensearch_dashboards.yml` 檔案的內容替換為下列設定：
        
        ```yaml
        opensearch.hosts: [http://localhost:9200]
        ```
        {% include copy.html %}

        移除 Security 外掛程式後，如果 `opensearch_dashboards.yml` 仍包含 `opensearch_security` 設定，OpenSearch Dashboards 就會因 `Unknown configuration key(s)` 錯誤而無法啟動。請務必移除所有隨附的設定。
        {: .note}
         
        請注意，此處使用的是一般的 `http` 方式，而非 `https`。
        {: .note}
    
1. 執行 OpenSearch Dashboards。

   執行 OpenSearch Dashboards 的方式有兩種：

   1. 使用 Windows 使用者介面執行批次指令碼：

      1. 前往 OpenSearch Dashboards 安裝位置的最上層目錄，並開啟 `opensearch-dashboards-{{site.opensearch_dashboards_version}}` 資料夾。
      1. 開啟 `bin` 資料夾，然後按兩下 `opensearch-dashboards.bat` 檔案以執行批次指令碼。這會開啟命令提示字元，並在其中執行 OpenSearch Dashboards 執行個體。

   1. 從命令提示字元或 PowerShell 執行批次指令碼：

      1. 在工作列上 **Start** 旁的搜尋方塊中輸入 `cmd` 以開啟命令提示字元，或輸入 `powershell` 以開啟 PowerShell。 
      1. 切換至 OpenSearch Dashboards 安裝位置的最上層目錄。
         ```bat
         cd \path\to\opensearch-dashboards-{{site.opensearch_dashboards_version}}
         ```
         {% include copy.html %}
      1. 執行批次指令碼以啟動 OpenSearch Dashboards。
         ```bat
         .\bin\opensearch-dashboards.bat
         ```
         {% include copy.html %}

1. 在網頁瀏覽器中前往 `http://localhost:5601`。OpenSearch Dashboards 可能需要約 2 分鐘才能啟動。如果您已將 OpenSearch Dashboards 設定為啟用安全性，請使用安裝 OpenSearch 時設定的[自訂管理員密碼]({{site.url}}{{site.baseurl}}/security/configuration/passwords/#setting-the-initial-admin-password)，以 `admin` 使用者身分登入。如果 OpenSearch Dashboards 在遠端主機上執行，請將 `localhost` 替換為該主機的 IP 位址或 DNS 名稱。如需詳細資訊，請參閱[存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#accessing-opensearch-dashboards)。

若要停止 OpenSearch Dashboards，請在命令提示字元或 PowerShell 中按下 `Ctrl+C`，或關閉命令提示字元或 PowerShell 視窗。
{: .tip}

## 相關文件

- [為正式環境準備 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)
