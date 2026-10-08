---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Windows
parent: Installing OpenSearch
nav_order: 40
---

# 在 Windows 上安裝 OpenSearch

以下各節說明如何從 zip 封存檔在 Windows 上安裝 OpenSearch。

一般而言，從 zip 封存檔安裝 OpenSearch 可分為幾個步驟：

1. **下載並解壓縮 OpenSearch。**
1. **（選用）測試 OpenSearch。**
   - 在套用任何自訂組態之前，確認 OpenSearch 能夠執行。
   - 您可以在不使用任何安全性（沒有密碼、沒有憑證）的情況下進行，也可以使用示範安全性組態，此組態可透過隨附的指令碼套用。
1. **針對您的環境設定 OpenSearch。**
   -  將基本設定套用至 OpenSearch，並開始在您的環境中使用。

Windows 版 OpenSearch 封存檔是一個獨立的目錄，包含執行 OpenSearch 所需的一切，其中包括整合的 Java Development Kit (JDK)。如果您有自己安裝的 Java 並設定了環境變數 `JAVA_HOME`，則在未設定 `OPENSEARCH_JAVA_HOME` 環境變數的情況下，OpenSearch 會使用該安裝。若要了解如何設定 `OPENSEARCH_JAVA_HOME` 環境變數，請參閱[步驟 3：在您的環境中設定 OpenSearch](#step-3-set-up-opensearch-in-your-environment)。

## 先決條件

請確認您已安裝 zip 公用程式。

## 步驟 1：下載並解壓縮 OpenSearch

請執行下列步驟，在 Windows 上安裝 OpenSearch。

1. 下載 [`opensearch-{{site.opensearch_version}}-windows-x64.zip`](https://artifacts.opensearch.org/releases/bundle/opensearch/{{site.opensearch_version}}/opensearch-{{site.opensearch_version}}-windows-x64.zip){:target='\_blank'} 封存檔。
1. 若要解壓縮封存檔內容，請按一下滑鼠右鍵並選取 **Extract All**。

請確認解壓縮路徑中沒有空格，否則 OpenSearch 將無法啟動。
{: .warning}

## 步驟 2：（選用）測試 OpenSearch

在進行任何設定之前，您應先測試 OpenSearch 的安裝。否則，日後發生問題時，可能難以判斷問題是源自安裝問題，還是您在安裝後套用的自訂設定。在此階段，有兩種快速測試 OpenSearch 的方法：

1. **（已啟用安全性）**使用 Windows 封存檔中隨附的批次指令碼套用通用組態。 
1. **（已停用安全性）**手動停用 Security 外掛程式，並在套用您自己的自訂安全性設定之前測試執行個體。

批次指令碼會將通用組態套用至您的 OpenSearch 執行個體。此組態會定義一些環境變數，並套用自我簽署的 TLS 憑證。或者，您也可以選擇自行設定這些項目。

如果您只想確認服務已正確設定，並打算自行設定安全性設定，則可以停用 Security 外掛程式，並在不加密或不驗證的情況下啟動服務。

採用預設組態（使用示範憑證，以及具有預設密碼的使用者）的 OpenSearch 節點不適用於正式作業環境。如果您打算在正式作業環境中使用該節點，至少應將示範 TLS 憑證替換為您自己的 TLS 憑證，並[更新內部使用者與密碼清單]({{site.url}}{{site.baseurl}}/security/configuration/yaml/)。如需其他指引以確保您的節點依照安全性需求進行設定，請參閱[安全性組態]({{site.url}}{{site.baseurl}}/security/configuration/index/)。
{: .warning}

### 選項 1：在啟用安全性的情況下測試您的 OpenSearch 設定

1. 從命令提示字元或 Powershell 執行示範批次指令碼。

      1. 在工作列上 **Start** 旁的搜尋方塊中輸入 `cmd` 以開啟命令提示字元，或輸入 `powershell` 以開啟 Powershell。 
      1. 切換至 OpenSearch 安裝的最上層目錄。
         ```bat
         cd \path\to\opensearch-{{site.opensearch_version}}
         ```
         {% include copy.html %}

      1. 執行批次指令碼。
         對於 OpenSearch 2.12 或更新版本，請使用下列命令指定自訂的管理員密碼，並遵循[管理員密碼需求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)：
         ```bat
         > set OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>
         ```
         {% include copy.html %}
         ```bat
         .\opensearch-windows-install.bat
         ```
         {% include copy.html %}

1. 開啟新的命令提示字元，並向伺服器傳送請求，以確認 OpenSearch 正在執行。請注意 `--insecure` 旗標的使用，由於 TLS 憑證為自我簽署，因此必須使用此旗標。
   - 向連接埠 9200 傳送請求：
      ```bat
      curl.exe -X GET https://localhost:9200 -u "admin:<custom-admin-password>" --insecure
      ```
      {% include copy.html %}

      您應會收到如下所示的回應：
      ```bat
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

      回應應如下所示：
      ```bat
      hostname opensearch-alerting                  {{site.opensearch_version}}
      hostname opensearch-anomaly-detection         {{site.opensearch_version}}
      hostname opensearch-asynchronous-search       {{site.opensearch_version}}
      hostname opensearch-cross-cluster-replication {{site.opensearch_version}}
      hostname opensearch-geospatial                {{site.opensearch_version}}
      hostname opensearch-index-management          {{site.opensearch_version}}
      hostname opensearch-job-scheduler             {{site.opensearch_version}}
      hostname opensearch-knn                       {{site.opensearch_version}}
      hostname opensearch-ml                        {{site.opensearch_version}}
      hostname opensearch-neural-search             {{site.opensearch_version}}
      hostname opensearch-notifications             {{site.opensearch_version}}
      hostname opensearch-notifications-core        {{site.opensearch_version}}
      hostname opensearch-observability             {{site.opensearch_version}}
      hostname opensearch-reports-scheduler         {{site.opensearch_version}}
      hostname opensearch-security                  {{site.opensearch_version}}
      hostname opensearch-security-analytics        {{site.opensearch_version}}
      hostname opensearch-sql                       {{site.opensearch_version}}
      ```

### 選項 2：在停用安全性的情況下測試您的 OpenSearch 設定

1. 開啟 `opensearch-{{site.opensearch_version}}\config` 資料夾。
1. 使用文字編輯器開啟 `opensearch.yml` 檔案。
1. 新增以下這一行以停用 Security 外掛程式：
   ```yaml
   plugins.security.disabled: true
   ```
   {% include copy.html %}

1. 儲存變更並關閉檔案。
1. 前往 OpenSearch 安裝的最上層目錄，並開啟 `opensearch-{{site.opensearch_version}}` 資料夾。
1. 按兩下 `opensearch-windows-install.bat` 檔案以執行預設設定。這會開啟一個正在執行 OpenSearch 執行個體的命令提示字元。
1. 開啟新的命令提示字元，並向伺服器傳送請求，以確認 OpenSearch 正在執行。由於 Security 外掛程式已停用，您將使用 `HTTP` 而非 `HTTPS` 傳送命令。
   - 向連接埠 9200 傳送請求：
      ```bat
      curl.exe -X GET http://localhost:9200
      ```
      {% include copy.html %}

      您應該會收到類似以下的回應：
      ```bat
      {
         "name" : "hostname-here",
         "cluster_name" : "opensearch",
         "cluster_uuid" : "7Nqtr0LrQTOveFcBb7Kufw",
         "version" : {
            "distribution" : "opensearch",
            "number" : "2.4.0",
            "build_type" : "zip",
            "build_hash" : "77ef9e304dd6ee95a600720a387a9735bbcf7bc9",
            "build_date" : "2022-11-05T05:50:15.404072800Z",
            "build_snapshot" : false,
            "lucene_version" : "9.4.1",
            "minimum_wire_compatibility_version" : "7.10.0",
            "minimum_index_compatibility_version" : "7.0.0"
         },
         "tagline" : "The OpenSearch Project: https://opensearch.org/"
      }
      ```
   - 查詢外掛程式端點：
      ```bat
      curl.exe -X GET http://localhost:9200/_cat/plugins?v
      ```
      {% include copy.html %}

      回應應如下所示：
      ```bat
      hostname opensearch-alerting                  {{site.opensearch_version}}
      hostname opensearch-anomaly-detection         {{site.opensearch_version}}
      hostname opensearch-asynchronous-search       {{site.opensearch_version}}
      hostname opensearch-cross-cluster-replication {{site.opensearch_version}}
      hostname opensearch-geospatial                {{site.opensearch_version}}
      hostname opensearch-index-management          {{site.opensearch_version}}
      hostname opensearch-job-scheduler             {{site.opensearch_version}}
      hostname opensearch-knn                       {{site.opensearch_version}}
      hostname opensearch-ml                        {{site.opensearch_version}}
      hostname opensearch-neural-search             {{site.opensearch_version}}
      hostname opensearch-notifications             {{site.opensearch_version}}
      hostname opensearch-notifications-core        {{site.opensearch_version}}
      hostname opensearch-observability             {{site.opensearch_version}}
      hostname opensearch-reports-scheduler         {{site.opensearch_version}}
      hostname opensearch-security                  {{site.opensearch_version}}
      hostname opensearch-security-analytics        {{site.opensearch_version}}
      hostname opensearch-sql                       {{site.opensearch_version}}
      ```

若要停止 OpenSearch，請在 Command Prompt 或 Powershell 中按下 `Ctrl+C`，或直接關閉 Command Prompt 或 Powershell 視窗。
{: .tip} 

## 步驟 3：在您的環境中設定 OpenSearch

沒有 OpenSearch 使用經驗的使用者，可能需要一份建議設定清單，以便開始使用此服務。預設情況下，OpenSearch 不會繫結至網路介面，外部主機也無法連線。此外，安全性設定若非尚未定義（全新安裝），就是在您透過叫用 <span style="white-space: nowrap">`opensearch-windows-install.bat`</span> 執行安全性示範指令碼後，填入了預設的使用者名稱和密碼。以下建議可讓使用者將 OpenSearch 繫結至網路介面。

以下建議設定可讓您：

- 將 OpenSearch 繫結至主機上的 IP 或網路介面。
- 設定 JVM 堆積的初始大小與最大大小。
- 定義指向隨附 JDK 的環境變數。

如果您已執行安全性示範指令碼，則需要手動重新設定已遭修改的設定。在繼續之前，請參閱[安全性組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)以取得指引。
{:.note}

在修改任何組態檔案之前，最好先儲存一份備份副本。備份檔案可用來還原因錯誤組態所造成的任何問題。
{:.tip}

1. 開啟 `opensearch-{{site.opensearch_version}}\config` 資料夾。
1. 使用文字編輯器開啟 `opensearch.yml` 檔案。
1. 新增以下幾行：
   ```bash
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
1. 指定 JVM 堆積的初始大小與最大大小。
   1.  開啟 `opensearch-{{site.opensearch_version}}\config` 資料夾。
   1.  使用文字編輯器開啟 `jvm.options` 檔案。
   1. 修改堆積初始大小與最大大小的值。一開始，您應將這些值設定為可用系統記憶體的一半。對於專用主機，可根據您的工作流程需求調高此值。<br>
    例如，如果主機有 8 GB 記憶體，您可能會想將堆積的初始大小與最大大小設定為 4 GB：
    ```bash
    -Xms4g
    -Xmx4g
    ```
    {% include copy.html %}

   1. 儲存變更並關閉檔案。
1. 指定隨附 JDK 的位置。 
    1. 在工作列上 **Start** 旁的搜尋方塊中，輸入 `edit environment variables for your account` 或 `edit the system environment variables`。若要編輯系統環境變數，您需要系統管理員權限。使用者環境變數的優先順序高於系統環境變數。
    1. 選取 **Edit environment variables for your account** 或 **Edit the system environment variables**。 
    1. 如果開啟了 **System Properties** 對話方塊，請在 **Advanced** 索引標籤中選取 **Environment Variables**。
    1. 在 **User variables** 或 **System variables** 下，選取 **New**。
    1. 在 **Variable name** 中，輸入 `OPENSEARCH_JAVA_HOME`。
    1. 在 **Variable value** 中，輸入 `\path\to\opensearch-{{site.opensearch_version}}\jdk`。
    1. 選取 **OK** 以關閉所有對話方塊。

1. 使用 `\path\to\opensearch-{{site.opensearch_version}}\bin\opensearch.bat` 啟動或重新啟動 OpenSearch。

## 外掛程式相容性

Performance Analyzer 外掛程式無法在 Windows 上使用。所有其他 OpenSearch 外掛程式（包括 k-NN 外掛程式）皆可使用。如需完整的外掛程式清單，請參閱[可用的外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/#available-plugins)。

## 相關文件

- [準備用於生產環境的叢集]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production)
- [常見安裝問題]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#common-issues)
- [OpenSearch 組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)
- [OpenSearch 外掛程式安裝]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)
- [關於 Security 外掛程式]({{site.url}}{{site.baseurl}}/security/index/)
