---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Windows
parent: Installing OpenSearch
nav_order: 40
---

# 在 Windows 上安裝 OpenSearch

以下各節說明如何從 zip 壓縮檔在 Windows 上安裝 OpenSearch。

一般而言，從 zip 壓縮檔安裝 OpenSearch 可以拆解成幾個步驟：

1. **下載並解壓縮 OpenSearch。**
1. **（選用）測試 OpenSearch。**
   - 在套用任何自訂組態之前，先確認 OpenSearch 能夠執行。
   - 這可以在沒有任何安全性的情況下完成（沒有密碼、沒有憑證），或是使用可透過隨附指令碼套用的示範安全性組態來完成。
1. **為您的環境設定 OpenSearch。**
   -  對 OpenSearch 套用基本設定，並開始在您的環境中使用它。

Windows 版 OpenSearch 壓縮檔是一個自成一體的目錄，內含執行 OpenSearch 所需的一切，包括整合的 Java Development Kit (JDK)。如果您有自己的 Java 安裝並設定環境變數 `JAVA_HOME`，且未設定 `OPENSEARCH_JAVA_HOME` 環境變數，OpenSearch 就會使用該安裝。若要了解如何設定 `OPENSEARCH_JAVA_HOME` 環境變數，請參閱[步驟 3：在您的環境中設定 OpenSearch](#step-3-set-up-opensearch-in-your-environment)。

## 先決條件

請確認您已安裝 zip 工具。

## 步驟 1：下載並解壓縮 OpenSearch

請執行下列步驟，在 Windows 上安裝 OpenSearch。

1. 下載 [`opensearch-{{site.opensearch_version}}-windows-x64.zip`](https://artifacts.opensearch.org/releases/bundle/opensearch/{{site.opensearch_version}}/opensearch-{{site.opensearch_version}}-windows-x64.zip){:target='\_blank'} 壓縮檔。
1. 若要解壓縮壓縮檔內容，請按一下滑鼠右鍵並選取 **Extract All**。或者，您也可以使用 Windows 內附的 `tar` 命令，從 Command Prompt 或 PowerShell 解壓縮，處理大型壓縮檔時速度更快：

   ```bat
   tar -xf opensearch-{{site.opensearch_version}}-windows-x64.zip
   ```
   {% include copy.html %}

請確認解壓縮路徑中沒有空格，因為這會導致 OpenSearch 無法啟動。
{: .warning}

## 步驟 2：（選用）測試 OpenSearch

在進行任何組態設定之前，您應該先測試 OpenSearch 安裝。否則，日後若發生問題，將難以判斷是安裝問題，還是您在安裝後套用的自訂設定所造成。在這個階段，有兩種快速測試 OpenSearch 的方法：

1. **（已啟用安全性）** 使用 Windows 壓縮檔內附的批次指令碼套用一般組態。 
1. **（已停用安全性）** 在套用您自己的自訂安全性設定之前，先手動停用 Security 外掛程式並測試執行個體。

批次指令碼會對您的 OpenSearch 執行個體套用一般組態。此組態會定義一些環境變數，也會套用自簽 TLS 憑證。或者，您也可以選擇自行設定這些項目。

如果您只想確認服務已正確設定，且打算自行設定安全性設定，那麼您可能會想停用 Security 外掛程式，並在沒有加密或驗證的情況下啟動服務。

處於預設組態的 OpenSearch 節點（使用示範憑證及預設密碼的使用者）不適合用於正式環境。如果您打算在正式環境中使用該節點，至少應將示範 TLS 憑證替換為您自己的 TLS 憑證，並[更新內部使用者與密碼清單]({{site.url}}{{site.baseurl}}/security/configuration/yaml/)。如需更多指引以確保您的節點依照安全性需求完成設定，請參閱[安全性組態]({{site.url}}{{site.baseurl}}/security/configuration/index/)。
{: .warning}

### 選項 1：在啟用安全性的情況下測試您的 OpenSearch 設定

1. 從 Command prompt 或 Powershell 執行示範批次指令碼。

      1. 在工作列上 **Start** 旁的搜尋方塊中輸入 `cmd` 以開啟 Command Prompt，或輸入 `powershell` 以開啟 Powershell。 
      1. 切換至 OpenSearch 安裝的頂層目錄。
         ```bat
         cd \path\to\opensearch-{{site.opensearch_version}}
         ```
         {% include copy.html %}

      1. 執行批次指令碼。
         若使用 OpenSearch 2.12 或更新版本，請依照[管理員密碼需求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)指定自訂管理員密碼。如果您未設定密碼，批次指令碼會結束，而不會啟動 OpenSearch。

         在 Command Prompt 中，請使用下列命令：
         ```bat
         set OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>
         ```
         {% include copy.html %}

         在 PowerShell 中，請使用下列命令：
         ```powershell
         $env:OPENSEARCH_INITIAL_ADMIN_PASSWORD="<custom-admin-password>"
         ```
         {% include copy.html %}

         Command Prompt 的 `set` 命令不會在 PowerShell 中設定環境變數，因此請務必使用適用於您 Shell 的命令。
         {: .note}

         接著執行批次指令碼：
         ```bat
         .\opensearch-windows-install.bat
         ```
         {% include copy.html %}

1. 開啟新的命令提示字元，並將請求傳送至伺服器，以確認 OpenSearch 正在執行。請注意使用了 `--insecure` 旗標，這是必要的，因為 TLS 憑證是自簽的。
   - 將請求傳送至連接埠 9200：
      ```bat
      curl.exe -X GET https://localhost:9200 -u "admin:<custom-admin-password>" --insecure
      ```
      {% include copy.html %}

      您應該會取得如下所示的回應：
      ```json
      {
         "name" : "hostname-here",
         "cluster_name" : "opensearch",
         "cluster_uuid" : "7Nqtr0LrQTOveFcBb7Kufw",
         "version" : {
            "distribution" : "opensearch",
            "number" : <version>,
            "build_type" : <build-type>,
            "build_hash" : <build-hash>,
            "build_date" : <build-date>,
            "build_snapshot" : false,
            "lucene_version" : <lucene-version>,
            "minimum_wire_compatibility_version" : "7.10.0",
            "minimum_index_compatibility_version" : "7.0.0"
         },
         "tagline" : "The OpenSearch Project: https://opensearch.org/"
      }
      ```
   - 查詢外掛程式端點：
      ```bat
      curl.exe -X GET https://localhost:9200/_cat/plugins?v -u "admin:<custom-admin-password>" --insecure
      ```
      {% include copy.html %}

      回應應該如下所示：
      ```text
      name     component                            version
      hostname opensearch-alerting                  {{site.opensearch_version}}
      hostname opensearch-anomaly-detection         {{site.opensearch_version}}
      hostname opensearch-asynchronous-search       {{site.opensearch_version}}
      hostname opensearch-cross-cluster-replication {{site.opensearch_version}}
      hostname opensearch-custom-codecs             {{site.opensearch_version}}
      hostname opensearch-flow-framework            {{site.opensearch_version}}
      hostname opensearch-geospatial                {{site.opensearch_version}}
      hostname opensearch-index-management          {{site.opensearch_version}}
      hostname opensearch-job-scheduler             {{site.opensearch_version}}
      hostname opensearch-knn                       {{site.opensearch_version}}
      hostname opensearch-ltr                       {{site.opensearch_version}}
      hostname opensearch-ml                        {{site.opensearch_version}}
      hostname opensearch-neural-search             {{site.opensearch_version}}
      hostname opensearch-notifications             {{site.opensearch_version}}
      hostname opensearch-notifications-core        {{site.opensearch_version}}
      hostname opensearch-observability             {{site.opensearch_version}}
      hostname opensearch-reports-scheduler         {{site.opensearch_version}}
      hostname opensearch-search-relevance          {{site.opensearch_version}}
      hostname opensearch-security                  {{site.opensearch_version}}
      hostname opensearch-security-analytics        {{site.opensearch_version}}
      hostname opensearch-skills                    {{site.opensearch_version}}
      hostname opensearch-sql                       {{site.opensearch_version}}
      hostname opensearch-system-templates          {{site.opensearch_version}}
      hostname opensearch-ubi                       {{site.opensearch_version}}
      hostname query-insights                       {{site.opensearch_version}}
      ```

### 選項 2：在停用安全性的情況下測試您的 OpenSearch 設定

1. 開啟 `opensearch-{{site.opensearch_version}}\config` 資料夾。
1. 使用文字編輯器開啟 `opensearch.yml` 檔案。
1. 新增下列這一行以停用 Security 外掛程式：
   ```yaml
   plugins.security.disabled: true
   ```
   {% include copy.html %}

1. 儲存變更並關閉檔案。
1. 前往 OpenSearch 安裝的最上層目錄，並開啟 `opensearch-{{site.opensearch_version}}` 資料夾。
1. 按兩下 `opensearch-windows-install.bat` 檔案以執行預設組態。這會開啟一個正在執行 OpenSearch 執行個體的命令提示字元視窗。
1. 開啟新的命令提示字元視窗，並向伺服器傳送請求，以確認 OpenSearch 正在執行。由於 Security 外掛程式已停用，因此您將使用 `HTTP` 而非 `HTTPS` 傳送命令。
   - 向連接埠 9200 傳送請求：
      ```bat
      curl.exe -X GET http://localhost:9200
      ```
      {% include copy.html %}

      您應會收到類似下列內容的回應：
      ```json
      {
         "name" : "hostname-here",
         "cluster_name" : "opensearch",
         "cluster_uuid" : "7Nqtr0LrQTOveFcBb7Kufw",
         "version" : {
            "distribution" : "opensearch",
            "number" : "{{site.opensearch_version}}",
            "build_type" : "zip",
            "build_hash" : <build-hash>,
            "build_date" : <build-date>,
            "build_snapshot" : false,
            "lucene_version" : <lucene-version>,
            "minimum_wire_compatibility_version" : "2.19.0",
            "minimum_index_compatibility_version" : "2.0.0"
         },
         "tagline" : "The OpenSearch Project: https://opensearch.org/"
      }
      ```
   - 查詢外掛程式端點：
      ```bat
      curl.exe -X GET http://localhost:9200/_cat/plugins?v
      ```
      {% include copy.html %}

      回應應類似下列內容：
      ```text
      name     component                            version
      hostname opensearch-alerting                  {{site.opensearch_version}}
      hostname opensearch-anomaly-detection         {{site.opensearch_version}}
      hostname opensearch-asynchronous-search       {{site.opensearch_version}}
      hostname opensearch-cross-cluster-replication {{site.opensearch_version}}
      hostname opensearch-custom-codecs             {{site.opensearch_version}}
      hostname opensearch-flow-framework            {{site.opensearch_version}}
      hostname opensearch-geospatial                {{site.opensearch_version}}
      hostname opensearch-index-management          {{site.opensearch_version}}
      hostname opensearch-job-scheduler             {{site.opensearch_version}}
      hostname opensearch-knn                       {{site.opensearch_version}}
      hostname opensearch-ltr                       {{site.opensearch_version}}
      hostname opensearch-ml                        {{site.opensearch_version}}
      hostname opensearch-neural-search             {{site.opensearch_version}}
      hostname opensearch-notifications             {{site.opensearch_version}}
      hostname opensearch-notifications-core        {{site.opensearch_version}}
      hostname opensearch-observability             {{site.opensearch_version}}
      hostname opensearch-reports-scheduler         {{site.opensearch_version}}
      hostname opensearch-search-relevance          {{site.opensearch_version}}
      hostname opensearch-security                  {{site.opensearch_version}}
      hostname opensearch-security-analytics        {{site.opensearch_version}}
      hostname opensearch-skills                    {{site.opensearch_version}}
      hostname opensearch-sql                       {{site.opensearch_version}}
      hostname opensearch-system-templates          {{site.opensearch_version}}
      hostname opensearch-ubi                       {{site.opensearch_version}}
      hostname query-insights                       {{site.opensearch_version}}
      ```

若要停止 OpenSearch，請在命令提示字元或 Powershell 中按下 `Ctrl+C`，或直接關閉命令提示字元或 Powershell 視窗。
{: .tip} 

## 步驟 3：在您的環境中設定 OpenSearch

先前沒有 OpenSearch 使用經驗的使用者，可能需要一份建議設定清單，以便開始使用此服務。根據預設，OpenSearch 不會繫結至網路介面，外部主機無法連線至 OpenSearch。此外，安全性設定若不是尚未定義（全新安裝），就是已填入預設的使用者名稱與密碼（若您已執行安全性示範指令碼）。執行該指令碼的方式為呼叫 <span style="white-space: nowrap">`opensearch-windows-install.bat`。</span>下列建議可讓使用者將 OpenSearch 繫結至網路介面。

下列建議設定可讓您：

- 將 OpenSearch 繫結至主機上的 IP 或網路介面。
- 設定初始與最大 JVM 堆積大小。
- 定義指向隨附 JDK 的環境變數。

下列步驟假設您已在[選項 1](#option-1-test-your-opensearch-settings-with-security-enabled) 中執行安全性示範指令碼，該指令碼會設定 Security 外掛程式所需的 TLS 憑證。若您在啟用 Security 外掛程式但沒有 TLS 組態的情況下啟動 OpenSearch，OpenSearch 將無法啟動。若您是使用[選項 2](#option-2-test-your-opensearch-settings-with-security-disabled) 測試 OpenSearch，請從 `opensearch.yml` 中移除 `plugins.security.disabled: true` 這一行，而不是新增 `plugins.security.disabled: false`。若 `opensearch.yml` 中包含重複的相同設定，OpenSearch 將無法啟動，並出現 `Duplicate Object property` 錯誤。在繼續之前，請參閱[安全性組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)以取得相關指引。
{:.note}

在修改任何組態檔案之前，最好先儲存一份備份。備份檔案可用來還原因組態錯誤而造成的任何問題。
{:.tip}

1. 開啟 `opensearch-{{site.opensearch_version}}\config` 資料夾。
1. 使用文字編輯器開啟 `opensearch.yml` 檔案。
1. 新增下列幾行：
   ```yaml
   # Bind OpenSearch to the correct network interface. Use 0.0.0.0
   # to include all available interfaces or specify an IP address
   # assigned to a specific interface.
   network.host: 0.0.0.0

   # Unless you have already configured a cluster, you should set
   # discovery.type to single-node, or the bootstrap checks will
   # fail when you try to start the service.
   discovery.type: single-node

   # If you previously disabled the Security plugin in opensearch.yml,
   # be sure to re-enable it. Otherwise you can skip this setting.
   plugins.security.disabled: false
   ```
   {% include copy.html %}

1. 儲存變更並關閉檔案。
1. 指定初始與最大 JVM 堆積大小。
   1.  開啟 `opensearch-{{site.opensearch_version}}\config` 資料夾。
   1.  使用文字編輯器開啟 `jvm.options` 檔案。
   1. 修改初始與最大堆積大小的值。一開始，您應將這些值設定為可用系統記憶體的一半。對於專用主機，可根據您的工作流程需求提高此值。<br>
    例如，若主機有 8 GB 記憶體，您可能會想將初始與最大堆積大小設定為 4 GB：
    ```bash
    -Xms4g
    -Xmx4g
    ```
    {% include copy.html %}

   1. 儲存變更並關閉檔案。
1. 指定隨附 JDK 的位置。 
    1. 在工作列上 **Start** 旁的搜尋方塊中，輸入 `edit environment variables for your account` 或 `edit the system environment variables`。若要編輯系統環境變數，您需要系統管理員權限。使用者環境變數的優先順序高於系統環境變數。
    1. 選取 **Edit environment variables for your account** 或 **Edit the system environment variables**。 
    1. 若開啟了 **System Properties** 對話方塊，請在 **Advanced** 索引標籤中選取 **Environment Variables**。
    1. 在 **User variables** 或 **System variables** 下，選取 **New**。
    1. 在 **Variable name** 中輸入 `OPENSEARCH_JAVA_HOME`。
    1. 在 **Variable value** 中輸入 `\path\to\opensearch-{{site.opensearch_version}}\jdk`。
    1. 選取 **OK** 以關閉所有對話方塊。

1. 使用 `\path\to\opensearch-{{site.opensearch_version}}\bin\opensearch.bat` 啟動或重新啟動 OpenSearch。

## 外掛程式相容性

Performance Analyzer 外掛程式在 Windows 上無法使用。其他所有 OpenSearch 外掛程式（包括 k-NN 外掛程式）皆可使用。完整的外掛程式清單請參閱[可用的外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/#available-plugins)。

## 相關文件

- [為正式環境準備叢集]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production)
- [常見安裝問題]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#common-issues)
- [OpenSearch 組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)
- [安裝 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)
- [關於 Security 外掛程式]({{site.url}}{{site.baseurl}}/security/index/)
