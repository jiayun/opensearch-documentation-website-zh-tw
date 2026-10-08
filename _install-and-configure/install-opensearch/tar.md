---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Tarball
parent: Installing OpenSearch
nav_order: 30
redirect_from:
  - /opensearch/install/tar/
---

# 從 tarball 安裝 OpenSearch

從 tarball（又稱 tar 封存檔）安裝 OpenSearch，適合想要精細控制安裝細節（例如檔案權限與安裝路徑）的使用者。

一般而言，從 tarball 安裝 OpenSearch 可分為以下幾個步驟：

1. **下載並解壓縮 OpenSearch。**
1. **設定重要的系統設定。**
   - 這些設定會在修改任何 OpenSearch 檔案之前套用至主機。
1. **（選用）測試 OpenSearch。**
   - 在套用任何自訂組態之前，確認 OpenSearch 能夠執行。
   - 您可以在不使用任何安全性（無密碼、無憑證）的情況下進行，也可以使用由隨附指令碼套用的示範安全性組態進行。
1. **針對您的環境設定 OpenSearch。**
   -  將基本設定套用至 OpenSearch，並開始在您的環境中使用。

tarball 是一個獨立完整的目錄，內含執行 OpenSearch 所需的一切，包括整合的 Java Development Kit (JDK)。此安裝方式與大多數 Linux 發行版相容，包括 CentOS 7、Amazon Linux 2 及 Ubuntu 18.04。如果您有自己安裝的 Java，並在終端機中設定了環境變數 `JAVA_HOME`，則 macOS 也可以使用。

本指南假設您熟悉 Linux 命令列介面 (CLI) 的操作。您應了解如何輸入命令、在目錄之間切換，以及編輯文字檔案。部分範例命令使用 `vi` 文字編輯器，但您可以使用任何可用的文字編輯器。
{:.note}

## 步驟 1：下載並解壓縮 OpenSearch

1. 從 [OpenSearch 下載頁面](https://opensearch.org/downloads.html){:target='\_blank'}下載適當的 tar.gz 封存檔，或使用命令列（例如使用 `wget`）下載。
   ```bash
   # x64
   wget https://artifacts.opensearch.org/releases/bundle/opensearch/{{site.opensearch_version}}/opensearch-{{site.opensearch_version}}-linux-x64.tar.gz

   # ARM64
   wget https://artifacts.opensearch.org/releases/bundle/opensearch/{{site.opensearch_version}}/opensearch-{{site.opensearch_version}}-linux-arm64.tar.gz
   ```
1. 解壓縮 tarball 的內容。
   ```bash
   # x64
   tar -xvf opensearch-{{site.opensearch_version}}-linux-x64.tar.gz
   
   # ARM64
   tar -xvf opensearch-{{site.opensearch_version}}-linux-arm64.tar.gz
   ```

## 步驟 2：設定重要的系統設定

啟動 OpenSearch 之前，您應先檢查一些[重要的系統設定]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#important-settings){:target='\_blank'}。
1. 停用主機上的記憶體分頁與置換，以提升效能。
   ```bash
   sudo swapoff -a
   ```
   {% include copy.html %}

1. 增加 OpenSearch 可用的記憶體對應數量。
   ```bash
   # Edit the sysctl config file
   sudo vi /etc/sysctl.conf

   # Add a line to define the desired value
   # or change the value if the key exists,
   # and then save your changes.
   vm.max_map_count=262144

   # Reload the kernel parameters using sysctl
   sudo sysctl -p

   # Verify that the change was applied by checking the value
   cat /proc/sys/vm/max_map_count
   ```

## 步驟 3：（選用）測試 OpenSearch

繼續之前，您應先測試 OpenSearch 的安裝。否則，日後發生問題時，將難以判斷是安裝問題所致，還是安裝後套用的自訂設定所致。在此階段，有兩種快速測試 OpenSearch 的方法：

1. **（啟用安全性）** 使用 tar 封存檔中隨附的示範安全性指令碼套用通用組態。
1. **（停用安全性）** 手動停用 Security 外掛程式，並在套用您自己的自訂安全性設定之前測試執行個體。

示範安全性指令碼會將通用組態套用至您的 OpenSearch 執行個體。此組態會定義一些環境變數，並套用自我簽署的 TLS 憑證。如果您想自行設定這些項目，請參閱[步驟 4：在您的環境中設定 OpenSearch](#step-4-set-up-opensearch-in-your-environment)。

如果您只想確認服務已正確設定，並打算自行設定安全性設定，則可以停用 Security 外掛程式，並在不加密也不驗證的情況下啟動服務。

由示範安全性指令碼設定的 OpenSearch 節點不適用於正式環境。如果您打算在執行 `opensearch-tar-install.sh` 之後將該節點用於正式環境，至少應將示範 TLS 憑證替換為您自己的 TLS 憑證，並[更新內部使用者與密碼清單]({{site.url}}{{site.baseurl}}/security/configuration/yaml/)。如需確保節點依照您的安全性需求進行設定的更多指引，請參閱[安全性組態]({{site.url}}{{site.baseurl}}/security/configuration/index/)。
{: .warning}

### 選項 1：在啟用安全性的情況下測試 OpenSearch 設定

1. 切換至 OpenSearch 安裝的最上層目錄。
   ```bash
   cd /path/to/opensearch-{{site.opensearch_version}}
   ```
   {% include copy.html %}

1. 使用安全性示範組態執行 OpenSearch 啟動指令碼。
   ```bash
   ./opensearch-tar-install.sh
   ```
   {% include copy.html %}

   若為 OpenSearch 2.12 或更新版本，請在安裝前使用下列命令設定新的自訂管理員密碼，並遵循[管理員密碼要求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)：
   ```bash
   $ export OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>
   ```
   {% include copy.html %}

1. 開啟另一個終端機工作階段，並向伺服器傳送請求，以確認 OpenSearch 正在執行。請注意 `--insecure` 旗標的使用，由於 TLS 憑證為自我簽署，因此必須使用此旗標。
   - 向連接埠 9200 傳送請求：
      ```bash
      curl -X GET https://localhost:9200 -u 'admin:<custom-admin-password>' --insecure
      ```
      {% include copy.html %}

      您應會收到類似以下的回應：
      ```bash
      {
         "name" : "hostname",
         "cluster_name" : "opensearch",
         "cluster_uuid" : "6XNc9m2gTUSIoKDqJit0PA",
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
      ```bash
      curl -X GET https://localhost:9200/_cat/plugins?v -u 'admin:<custom-admin-password>' --insecure
      ```
      {% include copy.html %}

      回應應類似以下內容：
      ```bash
      name     component                            version
      hostname opensearch-alerting                  {{site.opensearch_version}}
      hostname opensearch-anomaly-detection         {{site.opensearch_version}}
      hostname opensearch-asynchronous-search       {{site.opensearch_version}}
      hostname opensearch-cross-cluster-replication {{site.opensearch_version}}
      hostname opensearch-index-management          {{site.opensearch_version}}
      hostname opensearch-job-scheduler             {{site.opensearch_version}}
      hostname opensearch-knn                       {{site.opensearch_version}}
      hostname opensearch-ml                        {{site.opensearch_version}}
      hostname opensearch-notifications             {{site.opensearch_version}}
      hostname opensearch-notifications-core        {{site.opensearch_version}}
      hostname opensearch-observability             {{site.opensearch_version}}
      hostname opensearch-performance-analyzer      {{site.opensearch_version}}
      hostname opensearch-reports-scheduler         {{site.opensearch_version}}
      hostname opensearch-security                  {{site.opensearch_version}}
      hostname opensearch-sql                       {{site.opensearch_version}}
      ```
1. 返回原本的終端機工作階段，並按下 `CTRL + C` 停止處理程序。

### 選項 2：在停用安全性的情況下測試您的 OpenSearch 設定

1. 開啟組態檔案。
   ```bash
   vi /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   ```
   {% include copy.html %}

1. 新增下列這一行以停用 Security 外掛程式：
   ```bash
   plugins.security.disabled: true
   ```
   {% include copy.html %}

1. 儲存變更並關閉檔案。
1. 開啟另一個終端機工作階段，並向伺服器傳送請求，以確認 OpenSearch 正在執行。由於 Security 外掛程式已停用，您將使用 `HTTP` 而非 `HTTPS` 傳送命令。
   - 向連接埠 9200 傳送請求。
      ```bash
      curl -X GET http://localhost:9200
      ```
      {% include copy.html %}

      您應該會收到類似下列內容的回應：
      ```bash
      {
         "name" : "hostname",
         "cluster_name" : "opensearch",
         "cluster_uuid" : "6XNc9m2gTUSIoKDqJit0PA",
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
   - 查詢外掛程式端點。
      ```bash
      curl -X GET http://localhost:9200/_cat/plugins?v
      ```
      {% include copy.html %}

      回應應類似下列內容：
      ```bash
      name     component                            version
      hostname opensearch-alerting                  {{site.opensearch_version}}
      hostname opensearch-anomaly-detection         {{site.opensearch_version}}
      hostname opensearch-asynchronous-search       {{site.opensearch_version}}
      hostname opensearch-cross-cluster-replication {{site.opensearch_version}}
      hostname opensearch-index-management          {{site.opensearch_version}}
      hostname opensearch-job-scheduler             {{site.opensearch_version}}
      hostname opensearch-knn                       {{site.opensearch_version}}
      hostname opensearch-ml                        {{site.opensearch_version}}
      hostname opensearch-notifications             {{site.opensearch_version}}
      hostname opensearch-notifications-core        {{site.opensearch_version}}
      hostname opensearch-observability             {{site.opensearch_version}}
      hostname opensearch-performance-analyzer      {{site.opensearch_version}}
      hostname opensearch-reports-scheduler         {{site.opensearch_version}}
      hostname opensearch-security                  {{site.opensearch_version}}
      hostname opensearch-sql                       {{site.opensearch_version}}
      ```

## 步驟 4：在您的環境中設定 OpenSearch

沒有 OpenSearch 使用經驗的使用者，可能會需要一份建議設定清單，以便開始使用此服務。根據預設，OpenSearch 不會繫結至網路介面，外部主機也無法連線。此外，安全性設定若不是尚未定義 (全新安裝)，就是在您透過叫用 `opensearch-tar-install.sh` 執行安全性示範指令碼後，填入了預設的使用者名稱和密碼。下列建議可讓使用者將 OpenSearch 繫結至網路介面、建立並簽署 TLS 憑證，以及設定基本驗證。

下列建議設定可讓您：

- 將 OpenSearch 繫結至主機上的 IP 或網路介面。
- 設定初始和最大 JVM 堆積大小。
- 定義指向隨附 JDK 的環境變數。
- 設定您自己的 TLS 憑證，不需要第三方憑證授權單位 (CA)。
- 建立具有自訂密碼的管理員使用者。

如果您已執行安全性示範指令碼，則需要手動重新設定已被修改的設定。在繼續之前，請參閱[安全性組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)以取得指引。
{:.note}

在修改任何組態檔案之前，最好先儲存一份備份副本再進行變更。備份檔案可用於還原因錯誤組態所造成的任何問題。
{:.tip}

1. 開啟 `opensearch.yml`。
   ```bash
   vi /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   ```
   {% include copy.html %}

1. 新增下列幾行。
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
1. 指定初始和最大 JVM 堆積大小。
   1.  開啟 `jvm.options`。
         ```bash
         vi /path/to/opensearch-{{site.opensearch_version}}/config/jvm.options
         ```
         {% include copy.html %}

   1. 修改初始和最大堆積大小的值。作為起點，您應將這些值設定為可用系統記憶體的一半。對於專用主機，可根據您的工作流程需求提高此值。
      -  舉例來說，如果主機有 8 GB 記憶體，您可能會想將初始和最大堆積大小設定為 4 GB：
         ```bash
         -Xms4g
         -Xmx4g
         ```
         {% include copy.html %}

   1. 儲存變更並關閉檔案。
1. 指定隨附 JDK 的位置。
   ```bash
   export OPENSEARCH_JAVA_HOME=/path/to/opensearch-{{site.opensearch_version}}/jdk
   ```
   {% include copy.html %}

### 設定 TLS

TLS 憑證可讓用戶端確認主機的身分，並加密用戶端與主機之間的流量，為您的叢集提供額外的安全性。如需詳細資訊，請參閱 [Security 外掛程式]({{site.url}}{{site.baseurl}}/security/index/)文件中的[設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/)和[產生憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/)。在開發環境中進行的工作，通常使用自我簽署憑證就已足夠。本節將引導您完成產生自己的 TLS 憑證並將其套用至 OpenSearch 主機所需的基本步驟。

1. 前往 OpenSearch 的 `config` 目錄。憑證將儲存在此處。
   ```bash
   cd /path/to/opensearch-{{site.opensearch_version}}/config/
   ```
   {% include copy.html %}

1. 產生根憑證。您將使用此憑證來簽署其他憑證。
   ```bash
   # Create a private key for the root certificate
   openssl genrsa -out root-ca-key.pem 2048
   
   # Use the private key to create a self-signed root certificate. Be sure to
   # replace the arguments passed to -subj so they reflect your specific host.
   openssl req -new -x509 -sha256 -key root-ca-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=ROOT" -out root-ca.pem -days 730
   ```
1. 接著，建立管理員憑證。此憑證用於取得較高權限，以執行與 Security 外掛程式相關的管理工作。
   ```bash
   # Create a private key for the admin certificate.
   openssl genrsa -out admin-key-temp.pem 2048

   # Convert the private key to PKCS#8.
   openssl pkcs8 -inform PEM -outform PEM -in admin-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out admin-key.pem
   
   # Create the CSR. A common name (CN) of "A" is acceptable because this certificate is
   # used for authenticating elevated access and is not tied to a host.
   openssl req -new -key admin-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=A" -out admin.csr
   
   # Sign the admin certificate with the root certificate and private key you created earlier.
   openssl x509 -req -in admin.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out admin.pem -days 730
   ```
1. 為正在設定的節點建立憑證。
   ```bash
   # Create a private key for the node certificate.
   openssl genrsa -out node1-key-temp.pem 2048
   
   # Convert the private key to PKCS#8.
   openssl pkcs8 -inform PEM -outform PEM -in node1-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out node1-key.pem
   
   # Create the CSR and replace the arguments passed to -subj so they reflect your specific host.
   # The CN should match a DNS A record for the host--do not use the hostname.
   openssl req -new -key node1-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=node1.dns.a-record" -out node1.csr
   
   # Create an extension file that defines a SAN DNS name for the host. This
   # should match the DNS A record of the host.
   echo 'subjectAltName=DNS:node1.dns.a-record' > node1.ext
   
   # Sign the node certificate with the root certificate and private key that you created earlier.
   openssl x509 -req -in node1.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out node1.pem -days 730 -extfile node1.ext
   ```
1. 移除不再需要的暫存檔案。
   ```bash
   rm *temp.pem *csr *ext
   ```
   {% include copy.html %}

1. 依照[產生憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/#add-distinguished-names-to-opensearchyml)中的說明，將這些憑證新增至 `opensearch.yml`。進階使用者也可以選擇使用指令碼附加這些設定：
   ```bash
   #! /bin/bash

   # Before running this script, make sure to replace the /path/to your OpenSearch directory,
   # and remember to replace the CN in the node's distinguished name with a real
   # DNS A record.

   echo "plugins.security.ssl.transport.pemcert_filepath: /path/to/opensearch-{{site.opensearch_version}}/config/node1.pem" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "plugins.security.ssl.transport.pemkey_filepath: /path/to/opensearch-{{site.opensearch_version}}/config/node1-key.pem" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "plugins.security.ssl.transport.pemtrustedcas_filepath: /path/to/opensearch-{{site.opensearch_version}}/config/root-ca.pem" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "plugins.security.ssl.http.enabled: true" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "plugins.security.ssl.http.pemcert_filepath: /path/to/opensearch-{{site.opensearch_version}}/config/node1.pem" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "plugins.security.ssl.http.pemkey_filepath: /path/to/opensearch-{{site.opensearch_version}}/config/node1-key.pem" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "plugins.security.ssl.http.pemtrustedcas_filepath: /path/to/opensearch-{{site.opensearch_version}}/config/root-ca.pem" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "plugins.security.allow_default_init_securityindex: true" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "plugins.security.authcz.admin_dn:" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "  - 'CN=A,OU=UNIT,O=ORG,L=TORONTO,ST=ONTARIO,C=CA'" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "plugins.security.nodes_dn:" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "  - 'CN=node1.dns.a-record,OU=UNIT,O=ORG,L=TORONTO,ST=ONTARIO,C=CA'" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "plugins.security.audit.type: internal_opensearch" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "plugins.security.enable_snapshot_restore_privilege: true" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "plugins.security.check_snapshot_restore_write_privileges: true" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   echo "plugins.security.restapi.roles_enabled: [\"all_access\", \"security_rest_api_access\"]" | sudo tee -a /path/to/opensearch-{{site.opensearch_version}}/config/opensearch.yml
   ```
   {% include copy.html %}

1. （選用）為自我簽署的根憑證新增信任。
   ```bash
   # Copy the root certificate to the correct directory
   sudo cp /path/to/opensearch-{{site.opensearch_version}}/config/root-ca.pem /etc/pki/ca-trust/source/anchors/

   # Add trust
   sudo update-ca-trust
   ```

### 設定使用者

OpenSearch 可透過多種方式定義和驗證使用者。其中一種不需要額外後端基礎架構的方法，是在 `internal_users.yml` 中手動設定使用者。如需設定使用者的詳細資訊，請參閱 [YAML 檔案]({{site.url}}{{site.baseurl}}/security/configuration/yaml/)。下列步驟說明如何使用指令碼移除 `admin` 使用者以外的所有示範使用者，以及如何替換 `admin` 的預設密碼。

1. 將 Security 外掛程式的指令碼設為可執行。
   ```bash
   chmod 755 /path/to/opensearch-{{site.opensearch_version}}/plugins/opensearch-security/tools/*.sh
   ```
   {% include copy.html %}

1. 執行 `hash.sh` 以產生新密碼。
   - 如果尚未定義 JDK 的路徑，此指令碼將會失敗。
      ```bash
      # Example output if a JDK isn't found...
      $ ./hash.sh
      **************************************************************************
      ** This tool will be deprecated in the next major release of OpenSearch **
      ** https://github.com/opensearch-project/security/issues/1755           **
      **************************************************************************
      which: no java in (/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/user/.local/bin:/home/user/bin)
      WARNING: nor OPENSEARCH_JAVA_HOME nor JAVA_HOME is set, will use 
      ./hash.sh: line 35: java: command not found
      ```
      {% include copy.html %}

   - 為避免發生問題，請在呼叫指令碼時宣告環境變數：
      ```bash
      OPENSEARCH_JAVA_HOME=/path/to/opensearch-{{site.opensearch_version}}/jdk ./hash.sh
      ```
      {% include copy.html %}

   - 在提示中輸入所需的密碼，並記下輸出的雜湊值。
1. 開啟 `internal_users.yml`。
   ```bash
   vi /path/to/opensearch-{{site.opensearch_version}}/config/opensearch-security/internal_users.yml
   ```
   {% include copy.html %}

1. 移除 `admin` 以外的所有示範使用者，並將雜湊值替換為先前步驟中 `hash.sh` 提供的輸出。此檔案應類似下列範例：
   ```bash
   ---
   # This is the internal user database
   # The hash value is a bcrypt hash and can be generated with plugin/tools/hash.sh

   _meta:
      type: "internalusers"
      config_version: 2

   # Define your internal users here

   admin:
      hash: "$2y$1EXAMPLEQqwS8TUcoEXAMPLEeZ3lEHvkEXAMPLERqjyh1icEXAMPLE."
      reserved: true
      backend_roles:
      - "admin"
      description: "Admin user"
   ```
   {% include copy.html %}

### 套用變更

現在 TLS 憑證已安裝完成，且示範使用者已移除或已指派新密碼，最後一個步驟是套用組態變更。此最後的組態步驟需要在主機上執行 OpenSearch 時呼叫 `securityadmin.sh`。

1. 啟動 OpenSearch。OpenSearch 必須處於執行狀態，`securityadmin.sh` 才能套用變更。
   ```bash
   # Change directories
   cd /path/to/opensearch-{{site.opensearch_version}}/bin

   # Run the service in the foreground
   ./opensearch
   ```
1. 開啟與主機連線的另一個終端機工作階段，並前往包含 `securityadmin.sh` 的目錄。
   ```bash
   # Change to the correct directory
   cd /path/to/opensearch-{{site.opensearch_version}}/plugins/opensearch-security/tools
   ```
1. 呼叫指令碼。如需您必須傳遞之引數的定義，請參閱[使用 securityadmin.sh 套用變更]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)。
   ```bash
   # You can omit the environment variable if you declared this in your $PATH.
   OPENSEARCH_JAVA_HOME=/path/to/opensearch-{{site.opensearch_version}}/jdk ./securityadmin.sh -cd /path/to/opensearch-{{site.opensearch_version}}/config/opensearch-security/ -cacert /path/to/opensearch-{{site.opensearch_version}}/config/root-ca.pem -cert /path/to/opensearch-{{site.opensearch_version}}/config/admin.pem -key /path/to/opensearch-{{site.opensearch_version}}/config/admin-key.pem -icl -nhnv
   ```
1. 停止並重新啟動執行中的 OpenSearch 程序以套用變更。

### 確認服務正在執行

OpenSearch 現在已在您的主機上執行，並使用自訂的 TLS 憑證，以及一個用於基本驗證的安全使用者。您可以從另一台主機向您的 OpenSearch 節點傳送 API 請求，以確認外部連線能力。

在先前的測試中，您將請求傳送至 `localhost`。現在已套用 TLS 憑證，且新憑證參照的是您主機實際的 DNS 記錄，因此傳送至 `localhost` 的請求將無法通過通用名稱 (CN) 檢查，憑證也會被視為無效。您應改為將請求傳送至您在產生憑證時指定的位址。

在傳送請求之前，您應在用戶端中加入對根憑證的信任。若您未加入信任，則必須使用 `-k` 選項，讓 cURL 略過 CN 與根憑證驗證。
{:.tip}

```bash
$ curl https://your.host.address:9200 -u admin:yournewpassword -k
{
  "name" : "hostname-here",
  "cluster_name" : "opensearch",
  "cluster_uuid" : "efC0ANNMQlGQ5TbhNflVPg",
  "version" : {
    "distribution" : "opensearch",
    "number" : "2.1.0",
    "build_type" : "tar",
    "build_hash" : "388c80ad94529b1d9aad0a735c4740dce2932a32",
    "build_date" : "2022-06-30T21:31:04.823801692Z",
    "build_snapshot" : false,
    "lucene_version" : "9.2.0",
    "minimum_wire_compatibility_version" : "7.10.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
```

### 使用 `systemd` 將 OpenSearch 作為服務執行

本節將引導您為 OpenSearch 建立服務，並將其註冊至 `systemd`。定義服務之後，您可以使用 `systemctl` 命令來啟用、啟動及停止 OpenSearch 服務。本節中的命令假設 OpenSearch 已安裝至 `/opt/opensearch`，請依據您的安裝路徑進行變更。

以下組態僅適用於非正式環境中的測試。我們不建議在正式環境中使用以下組態。若您想在主機上將 OpenSearch 作為由 systemd 管理的服務執行，應使用 [RPM]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/rpm/) 發行版本安裝 OpenSearch。tarball 安裝並未定義特定的安裝路徑、使用者、角色或權限。若未妥善保護您的主機環境，可能會導致非預期的行為。
{: .warning}

1. 為 OpenSearch 服務建立使用者。
   ```bash
   sudo adduser --system --shell /bin/bash -U --no-create-home opensearch
   ```
   {% include copy.html %}

1. 將您的使用者加入 `opensearch` 使用者群組。
   ```bash
   sudo usermod -aG opensearch $USER
   ```
   {% include copy.html %}

1. 將檔案擁有者變更為 `opensearch`。若您的 OpenSearch 檔案位於其他目錄，請務必變更路徑。
   ```bash
   sudo chown -R opensearch /opt/opensearch/
   ```
   {% include copy.html %}

1. 建立服務檔案並開啟以進行編輯。
   ```bash
   sudo vi /etc/systemd/system/opensearch.service
   ```
   {% include copy.html %}

1. 輸入以下範例服務組態。若您的 OpenSearch 檔案位於其他目錄，請務必變更參照的路徑。
   ```bash
   [Unit]
   Description=OpenSearch
   Wants=network-online.target
   After=network-online.target

   [Service]
   Type=forking
   RuntimeDirectory=data

   WorkingDirectory=/opt/opensearch
   ExecStart=/opt/opensearch/bin/opensearch -d

   User=opensearch
   Group=opensearch
   StandardOutput=journal
   StandardError=inherit
   LimitNOFILE=65535
   LimitNPROC=4096
   LimitAS=infinity
   LimitFSIZE=infinity
   TimeoutStopSec=0
   KillSignal=SIGTERM
   KillMode=process
   SendSIGKILL=no
   SuccessExitStatus=143
   TimeoutStartSec=75

   [Install]
   WantedBy=multi-user.target
   ```
   {% include copy.html %}

1. 重新載入 `systemd` 管理員組態。
   ```bash
   sudo systemctl daemon-reload
   ```
   {% include copy.html %}

1. 啟用 OpenSearch 服務。
   ```bash
   sudo systemctl enable opensearch.service
   ```
   {% include copy.html %}

1. 啟動 OpenSearch 服務。
   ```bash
   sudo systemctl start opensearch
   ```
   {% include copy.html %}

1. 確認服務正在執行。
   ```bash
   sudo systemctl status opensearch
   ```
   {% include copy.html %}

## 相關文件

- [為正式環境準備叢集]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production)
- [常見的安裝問題]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#common-issues)
- [OpenSearch 組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)
- [為 Tarball 安裝設定 Performance Analyzer]({{site.url}}{{site.baseurl}}/monitoring-plugins/pa/index/#install-performance-analyzer)
- [安裝及設定 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/)
- [OpenSearch 外掛程式安裝]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)
- [關於 Security 外掛程式]({{site.url}}{{site.baseurl}}/security/index/)