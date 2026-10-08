---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: RPM
parent: Installing OpenSearch
redirect_from:
- /opensearch/install/rpm/
nav_order: 25
---

{% comment %}
The following liquid syntax declares a variable, major_version_mask, which is transformed into "N.x" where "N" is the major version number. This is required for proper versioning references to the Yum repo.
{% endcomment %}
{% assign version_parts = site.opensearch_major_minor_version | split: "." %}
{% assign major_version_mask = version_parts[0] | append: ".x" %}

# 使用 RPM 安裝 OpenSearch

與 [Tarball]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/tar/) 方法相比，使用 RPM Package Manager (RPM) 安裝 OpenSearch 可大幅簡化流程。許多技術考量，例如安裝路徑、組態檔案的位置，以及建立由 `systemd` 管理的服務等，都會由套件管理員自動處理。

一般而言，從 RPM 發行版安裝 OpenSearch 可分為幾個步驟：

1. **下載並安裝 OpenSearch。**
   - 從 RPM 套件手動安裝，或從 YUM 儲存庫安裝。
1. **（選用）測試 OpenSearch。**
   - 在套用任何自訂組態之前，確認 OpenSearch 能夠執行。
   - 您可以在完全不使用安全性（無密碼、無憑證）的情況下進行測試，也可以使用由套件內附指令碼套用的示範安全性組態進行測試。
1. **針對您的環境設定 OpenSearch。**
   -  將基本設定套用至 OpenSearch，並開始在您的環境中使用。

RPM 發行版提供在 Red Hat 或以 Red Hat 為基礎的 Linux 發行版中執行 OpenSearch 所需的一切。如需支援的作業系統清單，請參閱[作業系統相容性]({{site.url}}{{site.baseurl}}/install-and-configure/os-comp/)。

本指南假設您熟悉 Linux 命令列介面 (CLI) 的操作。您應了解如何輸入命令、在目錄之間切換，以及編輯文字檔案。部分範例命令使用 `vi` 文字編輯器，但您可以使用任何可用的文字編輯器。
{:.note}

## 步驟 1：下載並安裝 OpenSearch

您可以從套件或 YUM 儲存庫安裝 OpenSearch。

### 從套件安裝 OpenSearch

1. 直接從 [OpenSearch 下載頁面](https://opensearch.org/downloads.html){:target='\_blank'}下載所需版本的 RPM 套件。RPM 套件提供 **x64** 與 **arm64** 兩種架構的版本。
1. 匯入公開的 GNU Privacy Guard (GPG) 金鑰。此金鑰用於驗證您的 OpenSearch 執行個體已經過簽署。
   
    ```bash
    sudo rpm --import https://artifacts.opensearch.org/publickeys/opensearch-release.pgp
    ```
    {% include copy.html %}
   
1. 在 CLI 中，您可以使用 `rpm` 或 `yum` 安裝套件。

   全新安裝 OpenSearch 3.7 及更新版本時，您可以使用下列安裝時期環境變數來控制 Security 外掛程式的行為：
   * `DISABLE_INSTALL_DEMO_CONFIG=true` -- 防止安裝程式設定示範安全性組態（憑證、使用者與角色）。若您將手動設定安全性，請使用此變數。
   * `DISABLE_SECURITY_PLUGIN=true` -- 完全停用 Security 外掛程式。僅在不需要安全性的測試或開發環境中使用此變數。

   若要使用這些環境變數，請透過 `env` 關鍵字將其加在安裝命令之前：
   ```bash
   sudo env DISABLE_INSTALL_DEMO_CONFIG=true yum install opensearch-{{site.opensearch_version}}-linux-x64.rpm
   ```
   {% include copy.html %}

   全新安裝 OpenSearch 2.12 及更新版本時，您必須定義自訂的管理員密碼，才能設定示範安全性組態。請依照[管理員密碼要求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)，使用下列其中一個命令來定義自訂管理員密碼。

   使用 yum 安裝 x64 套件：
   ```bash
   sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password> yum install opensearch-{{site.opensearch_version}}-linux-x64.rpm
   ```
   {% include copy.html %}

   使用 rpm 安裝 x64 套件：
   ```bash
   sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password> rpm -ivh opensearch-{{site.opensearch_version}}-linux-x64.rpm
   ```
   {% include copy.html %}

   使用 yum 安裝 arm64 套件：
   ```bash
   sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password> yum install opensearch-{{site.opensearch_version}}-linux-arm64.rpm
   ```
   {% include copy.html %}

   使用 rpm 安裝 arm64 套件：
   ```bash
   sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password> rpm -ivh opensearch-{{site.opensearch_version}}-linux-arm64.rpm
   ```
   {% include copy.html %}

   OpenSearch 2.11 及更早版本請使用下列命令。

   使用 yum 安裝 x64 套件：
   ```bash
   sudo yum install opensearch-<version>-linux-x64.rpm
   ```
   {% include copy.html %}

   使用 rpm 安裝 x64 套件：
   ```bash
   sudo rpm -ivh opensearch-<version>-linux-x64.rpm
   ```
   {% include copy.html %}

   使用 yum 安裝 arm64 套件：
   ```bash
   sudo yum install opensearch-<version>-linux-arm64.rpm
   ```
   {% include copy.html %}

   使用 rpm 安裝 arm64 套件：
   ```bash
   sudo rpm -ivh opensearch-<version>-linux-arm64.rpm
   ```
   {% include copy.html %}

1. 安裝成功後，將 OpenSearch 啟用為服務。

   ```bash
   sudo systemctl enable opensearch
   ```
   {% include copy.html %}

1. 啟動 OpenSearch。

   ```bash
   sudo systemctl start opensearch
   ```
   {% include copy.html %}

1. 確認 OpenSearch 已正確啟動：

   ```bash
   sudo systemctl status opensearch
   ```
   {% include copy.html %}

### 從 YUM 儲存庫安裝 OpenSearch

YUM 是以 Red Hat 為基礎之作業系統的主要套件管理工具，可讓您從 YUM 儲存庫下載並安裝 RPM 套件。

1. 為 OpenSearch 建立本機儲存庫檔案：
   ```bash
   sudo curl -SL https://artifacts.opensearch.org/releases/bundle/opensearch/{{major_version_mask}}/opensearch-{{major_version_mask}}.repo -o /etc/yum.repos.d/opensearch-{{major_version_mask}}.repo
   ```
   {% include copy.html %}

1. 清除您的 YUM 快取，以確保安裝順利進行：
   ```bash
   sudo yum clean all
   ```
   {% include copy.html %}

1. 確認儲存庫已成功建立。
    ```bash
    sudo yum repolist
    ```
    {% include copy.html %}

1. 下載儲存庫檔案後，列出所有可用的 OpenSearch 版本：
   ```bash
   sudo yum list opensearch --showduplicates
   ```
   {% include copy.html %}

1. 選擇您要安裝的 OpenSearch 版本：
   - 除非另有指定，否則將安裝最新可用的 OpenSearch 版本。

   OpenSearch 2.12 及更新版本在全新安裝時，必須提供自訂的管理員密碼，才能設定示範安全性組態。若要設定自訂管理員密碼，請使用下列命令：

   ```bash
   sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password> yum install opensearch
   ```
   {% include copy.html %}

   OpenSearch 2.11 及更早版本請使用下列命令：

   ```bash
   sudo yum install opensearch
   ```
   {% include copy.html %}

   - 若要安裝特定版本的 OpenSearch，請在套件名稱後方加上版本號碼。

   OpenSearch 2.12 及更新版本在全新安裝時，必須提供自訂的管理員密碼，才能設定示範安全性組態。若要設定自訂管理員密碼，請使用下列命令：
   ```bash
   sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password> yum install 'opensearch-{{site.opensearch_version}}'
   ```
   {% include copy.html %}

   OpenSearch 2.11 及更早版本請使用下列命令：
   ```bash
   sudo yum install 'opensearch-2.11.0'
   ```
   {% include copy.html %}

1. 安裝期間，安裝程式會向您顯示 GPG 金鑰指紋。請確認資訊與下列內容相符：
   ```bash
   Fingerprint: A8B2 D9E0 4CD5 1FEF 6AA2 DB53 BA81 D999 8119 1457
   ```
   {% include copy.html %}

    - 若正確，請輸入 `yes` 或 `y`。OpenSearch 安裝將繼續進行。
1. 完成後，您即可執行 OpenSearch。
    ```bash
    sudo systemctl start opensearch
    ```
    {% include copy.html %}

1. 確認 OpenSearch 已正確啟動。
    ```bash
    sudo systemctl status opensearch
    ```
    {% include copy.html %}

## 步驟 2：（選用）測試 OpenSearch

在進行任何組態設定之前，您應該先測試 OpenSearch 的安裝。否則，日後可能難以判斷問題是出自安裝問題，還是您在安裝後套用的自訂設定。

使用 RPM 套件安裝 OpenSearch 時，系統會自動套用一些示範安全性設定。其中包括自我簽署的 TLS 憑證，以及數個使用者和角色。若您想自行設定這些項目，請參閱[在您的環境中設定 OpenSearch](#step-3-set-up-opensearch-in-your-environment)。

採用預設組態（使用示範憑證及預設密碼使用者）的 OpenSearch 節點不適用於生產環境。若您打算在生產環境中使用該節點，至少應將示範 TLS 憑證替換為您自己的 TLS 憑證，並[更新內部使用者和密碼清單]({{site.url}}{{site.baseurl}}/security/configuration/yaml/)。如需其他指引，以確保您的節點依照您的安全性需求進行設定，請參閱[安全性組態]({{site.url}}{{site.baseurl}}/security/configuration/index/)。
{: .warning}

1. 向伺服器傳送請求，以確認 OpenSearch 正在執行。請注意此處使用了 `--insecure` 旗標，由於 TLS 憑證為自我簽署，因此此旗標為必要。
   - 向連接埠 9200 傳送請求：
      ```bash
      curl -X GET https://localhost:9200 -u 'admin:<custom-admin-password>' --insecure
      ```
      {% include copy.html %}

      您應該會收到類似以下的回應：
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
   - 查詢 plugins 端點：
      ```bash
      curl -X GET https://localhost:9200/_cat/plugins?v -u 'admin:<custom-admin-password>' --insecure
      ```
      {% include copy.html %}

      回應應如下所示：
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

## 步驟 3：在您的環境中設定 OpenSearch

先前沒有 OpenSearch 使用經驗的使用者，可能會需要一份建議設定清單，以便開始使用此服務。根據預設，OpenSearch 不會繫結至網路介面，外部主機也無法連線至它。此外，安全性設定會填入預設的使用者名稱和密碼。以下建議可讓使用者將 OpenSearch 繫結至網路介面、建立並簽署 TLS 憑證，以及設定基本驗證。

以下建議設定可讓您：

- 將 OpenSearch 繫結至主機上的 IP 或網路介面。
- 設定 JVM 堆積的初始大小和最大大小。
- 定義指向隨附 JDK 的環境變數。
- 設定您自己的 TLS 憑證——不需要第三方憑證授權單位 (CA)。
- 建立具有自訂密碼的 admin 使用者。

若您已執行安全性示範指令碼，則需要手動重新設定已被修改的設定。在繼續之前，請參閱[安全性組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)以取得指引。
{:.note}

在修改任何組態檔案之前，最好先儲存一份備份副本再進行變更。備份檔案可用來減輕錯誤組態所造成的任何問題。
{:.tip}

1. 開啟 `opensearch.yml`。
   ```bash
   sudo vi /etc/opensearch/opensearch.yml
   ```
   {% include copy.html %}

1. 新增以下幾行。

   將 OpenSearch 繫結至正確的網路介面。使用 0.0.0.0 以包含所有可用介面，或指定指派給特定介面的 IP 位址：
   ```bash
   network.host: 0.0.0.0
   ```
   {% include copy.html %}

   除非您已設定叢集，否則應將 discovery.type 設為 single-node，不然當您嘗試啟動服務時，啟動檢查 (bootstrap check) 將會失敗：
   ```yaml
   discovery.type: single-node
   ```
   {% include copy.html %}

   若您改為設定多節點叢集，請在主機上將 `vm.max_map_count` 設為至少 `262144`。否則，服務啟動時啟動檢查將會失敗。如需更多資訊，請參閱[重要設定]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#important-settings)。

   若您先前已在 opensearch.yml 中停用 Security 外掛程式，請務必重新啟用。否則，您可以略過此設定：
   ```yaml
   plugins.security.disabled: false
   ```
   {% include copy.html %}

1. 儲存變更並關閉檔案。
1. 指定 JVM 堆積的初始大小和最大大小。
   1.  開啟 `jvm.options`。
         ```bash
         vi /etc/opensearch/jvm.options
         ```
         {% include copy.html %}

   1. 修改初始和最大堆積大小的值。一開始，您應將這些值設為可用系統記憶體的一半。對於專用主機，可根據您的工作流程需求提高此值。
      -  舉例來說，若主機有 8 GB 記憶體，您可能會想將初始和最大堆積大小設為 4 GB：
         ```bash
         -Xms4g
         -Xmx4g
         ```
         {% include copy.html %}

   1. 儲存變更並關閉檔案。

### 設定 TLS

TLS 憑證可讓用戶端確認主機身分，並加密用戶端與主機之間的流量，為您的叢集提供額外的安全性。如需更多資訊，請參閱 [Security 外掛程式]({{site.url}}{{site.baseurl}}/security/index/)文件中的[設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/)和[產生憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/)。在開發環境中進行的工作，通常使用自我簽署憑證就已足夠。本節將引導您完成產生自己的 TLS 憑證並將其套用至 OpenSearch 主機所需的基本步驟。

1. 前往將存放憑證的目錄。
   ```bash
   cd /etc/opensearch
   ```
   {% include copy.html %}

1. 刪除示範憑證。
   ```bash
   sudo rm -f *pem
   ```
   {% include copy.html %}

1. 產生根憑證。您將使用此憑證來簽署其他憑證。

   為根憑證建立私密金鑰：
   ```bash
   sudo openssl genrsa -out root-ca-key.pem 2048
   ```
   {% include copy.html %}

   使用私密金鑰建立自我簽署的根憑證。請務必替換傳遞給 -subj 的引數，使其符合您的特定主機：
   ```bash
   sudo openssl req -new -x509 -sha256 -key root-ca-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=ROOT" -out root-ca.pem -days 730
   ```
   {% include copy.html %}
1. 接著，建立 admin 憑證。此憑證用於取得較高的權限，以執行與 Security 外掛程式相關的管理工作。

   為 admin 憑證建立私密金鑰：
   ```bash
   sudo openssl genrsa -out admin-key-temp.pem 2048
   ```
   {% include copy.html %}

   將私密金鑰轉換為 PKCS#8：
   ```bash
   sudo openssl pkcs8 -inform PEM -outform PEM -in admin-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out admin-key.pem
   ```
   {% include copy.html %}

   建立憑證簽署請求 (CSR)。通用名稱 (CN) 為「A」是可接受的，因為此憑證用於驗證較高權限的存取，且未與主機綁定：
   ```bash
   sudo openssl req -new -key admin-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=A" -out admin.csr
   ```
   {% include copy.html %}

   使用您先前建立的根憑證和私密金鑰簽署 admin 憑證：
   ```bash
   sudo openssl x509 -req -in admin.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out admin.pem -days 730
   ```
   {% include copy.html %}
1. 為正在設定的節點建立憑證。

   為節點憑證建立私密金鑰：
   ```bash
   sudo openssl genrsa -out node1-key-temp.pem 2048
   ```
   {% include copy.html %}

   將私密金鑰轉換為 PKCS#8：
   ```bash
   sudo openssl pkcs8 -inform PEM -outform PEM -in node1-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out node1-key.pem
   ```
   {% include copy.html %}

   建立 CSR，並替換傳遞給 -subj 的引數，使其符合您的特定主機。CN 應符合主機的 DNS A 記錄——請勿使用主機名稱：
   ```bash
   sudo openssl req -new -key node1-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=node1.dns.a-record" -out node1.csr
   ```
   {% include copy.html %}

   建立擴充檔案，為主機定義 SAN DNS 名稱。此名稱應符合主機的 DNS A 記錄：
   ```bash
   sudo sh -c 'echo subjectAltName=DNS:node1.dns.a-record > node1.ext'
   ```
   {% include copy.html %}

   使用您先前建立的根憑證和私密金鑰簽署節點憑證：
   ```bash
   sudo openssl x509 -req -in node1.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out node1.pem -days 730 -extfile node1.ext
   ```
   {% include copy.html %}
1. 移除不再需要的暫存檔案。
   ```bash
   sudo rm -f *temp.pem *csr *ext
   ```
   {% include copy.html %}

1. 確認其餘憑證的擁有者為 `opensearch` 使用者。
   ```bash
   sudo chown opensearch:opensearch admin-key.pem admin.pem node1-key.pem node1.pem root-ca-key.pem root-ca.pem root-ca.srl
   ```
   {% include copy.html %}

1. 依照[產生憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/#add-distinguished-names-to-opensearchyml)中的說明，將這些憑證新增至 `opensearch.yml`。進階使用者也可以選擇使用指令碼附加這些設定。執行此指令碼之前，請務必將節點辨別名稱中的 CN 替換為實際的 DNS A 記錄：
   ```bash
   #! /bin/bash

   echo "plugins.security.ssl.transport.pemcert_filepath: /etc/opensearch/node1.pem" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "plugins.security.ssl.transport.pemkey_filepath: /etc/opensearch/node1-key.pem" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "plugins.security.ssl.transport.pemtrustedcas_filepath: /etc/opensearch/root-ca.pem" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "plugins.security.ssl.http.enabled: true" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "plugins.security.ssl.http.pemcert_filepath: /etc/opensearch/node1.pem" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "plugins.security.ssl.http.pemkey_filepath: /etc/opensearch/node1-key.pem" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "plugins.security.ssl.http.pemtrustedcas_filepath: /etc/opensearch/root-ca.pem" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "plugins.security.allow_default_init_securityindex: true" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "plugins.security.authcz.admin_dn:" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "  - 'CN=A,OU=UNIT,O=ORG,L=TORONTO,ST=ONTARIO,C=CA'" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "plugins.security.nodes_dn:" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "  - 'CN=node1.dns.a-record,OU=UNIT,O=ORG,L=TORONTO,ST=ONTARIO,C=CA'" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "plugins.security.audit.type: internal_opensearch" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "plugins.security.enable_snapshot_restore_privilege: true" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "plugins.security.check_snapshot_restore_write_privileges: true" | sudo tee -a /etc/opensearch/opensearch.yml
   echo "plugins.security.restapi.roles_enabled: [\"all_access\", \"security_rest_api_access\"]" | sudo tee -a /etc/opensearch/opensearch.yml
   ```
   {% include copy.html %}

1. （選用）為自我簽署的根憑證新增信任。

   將根憑證複製到正確的目錄：
   ```bash
   sudo cp /etc/opensearch/root-ca.pem /etc/pki/ca-trust/source/anchors/
   ```
   {% include copy.html %}

   新增信任：
   ```bash
   sudo update-ca-trust
   ```
   {% include copy.html %}

### 設定使用者

OpenSearch 可透過多種方式定義及驗證使用者。其中一種不需要額外後端基礎架構的方法，是在 `internal_users.yml` 中手動設定使用者。如需設定使用者的詳細資訊，請參閱 [YAML 檔案]({{site.url}}{{site.baseurl}}/security/configuration/yaml/)。以下步驟說明如何移除 `admin` 使用者以外的所有示範使用者，以及如何使用指令碼替換 `admin` 的預設密碼。

1. 前往 Security 外掛程式的工具目錄。
   ```bash
   cd /usr/share/opensearch/plugins/opensearch-security/tools
   ```
   {% include copy.html %}

1. 執行 `hash.sh` 以產生新密碼。
   - 如果尚未定義 JDK 的路徑，此指令碼將會失敗。

      找不到 JDK 時的輸出範例：
      ```bash
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

   - 叫用指令碼時宣告環境變數，以避免發生問題：
      ```bash
      OPENSEARCH_JAVA_HOME=/usr/share/opensearch/jdk ./hash.sh
      ```
      {% include copy.html %}

   - 在提示字元中輸入所需的密碼，並記下輸出的雜湊值。
1. 開啟 `internal_users.yml`。
   ```bash
   sudo vi /etc/opensearch/opensearch-security/internal_users.yml
   ```
   {% include copy.html %}

1. 移除 `admin` 以外的所有示範使用者，並將雜湊值替換為先前步驟中 `hash.sh` 提供的輸出。檔案內容應類似以下範例：
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

現在 TLS 憑證已安裝完成，且示範使用者已移除或已指派新密碼，最後一個步驟是套用組態變更。這個最後的組態步驟需要在主機上執行 OpenSearch 時叫用 `securityadmin.sh`。

1. OpenSearch 必須處於執行狀態，`securityadmin.sh` 才能套用變更。如果您對 `opensearch.yml` 進行了變更，請重新啟動 OpenSearch：
   ```bash
   sudo systemctl restart opensearch
   ```
   {% include copy.html %}

1. 開啟另一個連線至主機的終端機工作階段，並前往包含 `securityadmin.sh` 的目錄：
   ```bash
   cd /usr/share/opensearch/plugins/opensearch-security/tools
   ```
   {% include copy.html %}

1. 叫用指令碼。如需您必須傳遞之引數的定義，請參閱[使用 securityadmin.sh 套用變更]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)。如果您已在 $PATH 中宣告環境變數，則可以省略該變數：
   ```bash
   OPENSEARCH_JAVA_HOME=/usr/share/opensearch/jdk ./securityadmin.sh -cd /etc/opensearch/opensearch-security/ -cacert /etc/opensearch/root-ca.pem -cert /etc/opensearch/admin.pem -key /etc/opensearch/admin-key.pem -icl -nhnv
   ```
   {% include copy.html %}

### 確認服務正在執行

OpenSearch 現在已在您的主機上執行，並使用自訂 TLS 憑證以及用於基本驗證的安全使用者。您可以從另一台主機向您的 OpenSearch 節點傳送 API 請求，以確認外部連線能力。

在先前的測試中，您將請求導向 `localhost`。現在 TLS 憑證已套用，且新憑證參照的是您主機的實際 DNS 記錄，因此傳送至 `localhost` 的請求將無法通過 CN 檢查，憑證也會被視為無效。請改為將請求傳送至您產生憑證時指定的位址。

傳送請求之前，您應該先在用戶端中為根憑證新增信任。如果您未新增信任，則必須使用 `-k` 選項，讓 cURL 略過 CN 與根憑證驗證。
{:.tip}

```bash
$ curl https://your.host.address:9200 -u admin:yournewpassword -k
{
  "name" : "hostname-here",
  "cluster_name" : "opensearch",
  "cluster_uuid" : "efC0ANNMQlGQ5TbhNflVPg",
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

## 升級至較新版本

使用 RPM 或 YUM 安裝的 OpenSearch 執行個體可以輕鬆升級至較新版本。我們建議使用 YUM 進行更新，但您也可以使用 RPM 升級。


### 使用 RPM 手動升級

請直接從 [OpenSearch Project 下載頁面](https://opensearch.org/downloads.html){:target='\_blank'}下載所需升級版本的 RPM 套件。

前往包含該發行版本的目錄，然後執行下列命令：
```bash
rpm -Uvh opensearch-{{site.opensearch_version}}-linux-x64.rpm
```
{% include copy.html %}

### 使用 YUM 升級

若要使用 YUM 將 OpenSearch 升級至最新版本：
```bash
sudo yum update opensearch
```
{% include copy.html %}

 您也可以升級至特定的 OpenSearch 版本：
 ```bash
 sudo yum update opensearch-<version-number>
 ```
{% include copy.html %}

### 套件升級後自動重新啟動服務

OpenSearch RPM 套件不支援在套件升級後自動重新啟動服務。

## 相關文件

- [為生產環境準備叢集]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production)
- [常見安裝問題]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#common-issues)
- [OpenSearch 組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)
- [安裝並設定 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/)
- [OpenSearch 外掛程式安裝]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)
- [關於 Security 外掛程式]({{site.url}}{{site.baseurl}}/security/index/)
