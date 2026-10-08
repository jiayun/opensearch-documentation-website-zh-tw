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

## 前置條件

在安裝 OpenSearch Dashboards 之前，請完成以下任務：

- 安裝 OpenSearch。如需更多資訊，請參閱 [在 Windows 上安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/windows/)。
- 安裝 zip 壓縮工具。

## 在 Windows 上安裝 OpenSearch Dashboards

若要在 Windows 上安裝 OpenSearch Dashboards，請按照以下步驟操作：

1. 下載 [`opensearch-dashboards-{{site.opensearch_dashboards_version}}-windows-x64.zip`](https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/{{site.opensearch_dashboards_version}}/opensearch-dashboards-{{site.opensearch_dashboards_version}}-windows-x64.zip){:target='\_blank'} 封存檔。

1. 若要解壓縮封存檔內容，請按右鍵選取 **全部解壓縮 (Extract All)**。
   
   **注意**：某些版本的 Windows 作業系統會限制檔案路徑長度。如果您在解壓縮封存檔時遇到與路徑長度相關的錯誤，請執行以下步驟以啟用長路徑支援：

   1. 在工作列上 **開始** 按鈕旁的搜尋框中輸入 `powershell` 以開啟 Powershell。
   1. 在 Powershell 中執行以下命令：
      ```bat
      Set-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem LongPathsEnabled -Type DWORD -Value 1 -Force
      ```
   1. 重新啟動您的電腦。

1. 設定 OpenSearch Dashboards。

    根據 OpenSearch 的安全性設定是否啟用，有兩種設定 OpenSearch Dashboards 的方式。

    為了讓對 `opensearch_dashboards.yml` 檔案的任何變更生效，必須重新啟動 OpenSearch Dashboards。
    {: .note}

    1. 選項 1 -- 啟用安全性：
  
        組態檔案 `\path\to\opensearch-dashboards-{{site.opensearch_dashboards_version}}\config\opensearch_dashboards.yml` 隨附以下基本設定：
        
        ```
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

        如果您在停用安全性的情況下使用 OpenSearch，請使用以下命令從 OpenSearch Dashboards 中移除 Security 外掛程式：
        
        ```
        \path\to\opensearch-dashboards-{{site.opensearch_dashboards_version}}\bin\opensearch-dashboards-plugin.bat remove securityDashboards
        ```
        
        基本的 `opensearch_dashboards.yml` 檔案應包含：
        
        ```
        opensearch.hosts: [http://localhost:9200]
        ```
         
        請注意使用純 `http` 方法，而非 `https`。
        {: .note}
    
1. 執行 OpenSearch Dashboards。

   執行 OpenSearch Dashboards 有兩種方式：

   1. 使用 Windows UI 執行批次指令碼：

      1. 導覽至 OpenSearch Dashboards 安裝的頂層目錄，並開啟 `opensearch-dashboards-{{site.opensearch_dashboards_version}}` 資料夾。
      1. 開啟 `bin` 資料夾，並透過按兩下 `opensearch-dashboards.bat` 檔案來執行批次指令碼。這將開啟一個命令提示字元視窗並執行 OpenSearch Dashboards 執行個體。

   1. 從命令提示字元或 Powershell 執行批次指令碼：

      1. 在工作列上 **開始** 按鈕旁的搜尋框中輸入 `cmd` 以開啟命令提示字元，或輸入 `powershell` 以開啟 Powershell。
      1. 切換至 OpenSearch Dashboards 安裝的頂層目錄。
         ```bat
         cd \path\to\opensearch-dashboards-{{site.opensearch_dashboards_version}}
         ```
      1. 執行批次指令碼以啟動 OpenSearch Dashboards。
         ```bat
         .\bin\opensearch-dashboards.bat
         ```

1. 在網頁瀏覽器中，前往 `http://localhost:5601` 並使用您在安裝 OpenSearch 時設定的自訂管理員密碼，以 `admin` 使用者身分登入。如果 OpenSearch Dashboards 執行在遠端主機上，請將 `localhost` 替換為該主機的 IP 位址或 DNS 名稱。如需更多資訊，請參閱 [存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#accessing-opensearch-dashboards)。

若要停止 OpenSearch Dashboards，請在命令提示字元或 Powershell 中按 `Ctrl+C`，或關閉命令提示字元或 Powershell 視窗。
{: .tip}

## 相關文件

- [為生產環境準備 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)
