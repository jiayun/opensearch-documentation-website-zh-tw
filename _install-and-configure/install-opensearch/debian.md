---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Debian
parent: Installing OpenSearch
redirect_from:
- /opensearch/install/deb/
nav_order: 20
---

{% comment %}
The following liquid syntax declares a variable, major_version_mask, which is transformed into "N.x" where "N" is the major version number. This is required for proper versioning references to the Yum repo.
{% endcomment %}
{% assign version_parts = site.opensearch_major_minor_version | split: "." %}
{% assign major_version_mask = version_parts[0] | append: ".x" %}

# 在 Debian 上安裝 OpenSearch

與 [Tar 封存檔]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/tar/) 方法相比，使用 Advanced Packaging Tool (APT) 套件管理員安裝 OpenSearch 可大幅簡化流程。許多技術層面的考量，例如安裝路徑、組態檔案的位置，以及建立由 `systemd` 管理的服務等，都會由套件管理員自動處理。

一般而言，從 Debian 發行版本安裝 OpenSearch 可分為以下幾個步驟：

1. **下載並安裝 OpenSearch。**
   - 從 Debian 套件或 APT 儲存庫手動安裝。
1. **（選用）測試 OpenSearch。**
   - 在套用任何自訂組態之前，確認 OpenSearch 能夠執行。
   - 您可以在完全不使用安全性（無密碼、無憑證）的情況下進行測試，也可以使用由套件內附指令碼套用的示範安全性組態。
1. **針對您的環境設定 OpenSearch。**
   -  套用 OpenSearch 的基本設定，並開始在您的環境中使用。

Debian 發行版本提供在 Debian 系 Linux 發行版本（例如 Ubuntu）中執行 OpenSearch 所需的一切。

本指南假設您熟悉 Linux 命令列介面 (CLI) 的操作。您應了解如何輸入命令、在目錄之間切換，以及編輯文字檔案。部分範例命令使用 `vi` 文字編輯器，但您可以使用任何可用的文字編輯器。
{:.note}

## 步驟 1：下載並安裝 OpenSearch

您可以從套件或 APT 儲存庫安裝 OpenSearch。

### 從套件安裝 OpenSearch

1. 直接從 [OpenSearch 下載頁面](https://opensearch.org/downloads.html){:target='\_blank'}下載所需版本的 Debian 套件。Debian 套件提供 **x64** 與 **arm64** 兩種架構的版本供下載。
1. 在 CLI 中，使用 `dpkg` 安裝套件。

   對於 OpenSearch 3.7 及更新版本的全新安裝，您可以使用下列安裝時環境變數來控制 Security 外掛程式的行為：
   * `DISABLE_INSTALL_DEMO_CONFIG=true` -- 防止安裝程式設定示範安全性組態（憑證、使用者與角色）。若您將手動設定安全性，請在安裝時使用此變數。
   * `DISABLE_SECURITY_PLUGIN=true` -- 完全停用 Security 外掛程式。僅在不需要安全性的測試或開發環境中使用此變數。

   若要使用這些環境變數，請在安裝命令前搭配 `env` 關鍵字加入這些變數：
   ```bash
   sudo env DISABLE_INSTALL_DEMO_CONFIG=true dpkg -i opensearch-{{site.opensearch_version}}-linux-x64.deb
   ```
   {% include copy.html %}

   對於 OpenSearch 2.12 及更新版本的全新安裝，您必須定義自訂的管理員密碼，才能設定示範安全性組態。請使用下列其中一個命令來定義自訂管理員密碼：

   x64：
   ```bash
   sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password> dpkg -i opensearch-{{site.opensearch_version}}-linux-x64.deb
   ```
   {% include copy.html %}

   arm64：
   ```bash
   sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password> dpkg -i opensearch-{{site.opensearch_version}}-linux-arm64.deb
   ```
   {% include copy.html %}

   對於 OpenSearch 2.11 及更早版本，請使用下列命令。

   x64：
   ```bash
   sudo dpkg -i opensearch-<version>-linux-x64.deb
   ```
   {% include copy.html %}

   arm64：
   ```bash
   sudo dpkg -i opensearch-<version>-linux-arm64.deb
   ```
   {% include copy.html %}

1. 安裝成功後，將 OpenSearch 啟用為服務：
    ```bash
    sudo systemctl enable opensearch
    ```
    {% include copy.html %}

1. 啟動 OpenSearch 服務：
    ```bash
    sudo systemctl start opensearch
    ```
    {% include copy.html %}

1. 確認 OpenSearch 已正確啟動：
    ```bash
    sudo systemctl status opensearch
    ```
    {% include copy.html %}

### 指紋驗證

Debian 套件未經簽署。若您想驗證指紋，OpenSearch 專案提供了 `.sig` 檔案以及 `.deb` 套件，可搭配 GNU Privacy Guard (GPG) 使用。

1. 下載所需的 Debian 套件：
   ```bash
   curl -SLO https://artifacts.opensearch.org/releases/bundle/opensearch/{{site.opensearch_version}}/opensearch-{{site.opensearch_version}}-linux-x64.deb
   ```
   {% include copy.html %}

1. 下載對應的簽章檔案：
   ```bash
   curl -SLO https://artifacts.opensearch.org/releases/bundle/opensearch/{{site.opensearch_version}}/opensearch-{{site.opensearch_version}}-linux-x64.deb.sig
   ```
   {% include copy.html %}

1. 下載並匯入 GPG 金鑰：
   ```bash
   curl -o- https://artifacts.opensearch.org/publickeys/opensearch-release.pgp | gpg --import -
   ```
   {% include copy.html %}

1. 驗證簽章：
   ```bash
   gpg --verify opensearch-{{site.opensearch_version}}-linux-x64.deb.sig opensearch-{{site.opensearch_version}}-linux-x64.deb
   ```
   {% include copy.html %}

### 從 APT 儲存庫安裝 OpenSearch

APT 是 Debian 系作業系統的主要套件管理工具，可讓您從 APT 儲存庫下載並安裝 Debian 套件。 

1. 安裝必要的套件：
   ```bash
   sudo apt-get update && sudo apt-get -y install lsb-release ca-certificates curl gnupg2
   ```
    {% include copy.html %}

1. 若 keyrings 目錄尚不存在，請建立該目錄：
   ```bash
   sudo mkdir -p /etc/apt/keyrings
   ```
    {% include copy.html %}

1. 匯入公開 GPG 金鑰。此金鑰用於驗證 APT 儲存庫已經過簽署。
    ```bash
    curl -fsSL https://artifacts.opensearch.org/publickeys/opensearch-release.pgp \
    | sudo gpg --dearmor -o /etc/apt/keyrings/opensearch.gpg
    ```
    {% include copy.html %}

1. 為 OpenSearch 建立 APT 儲存庫：
   ```bash
   echo "deb [signed-by=/etc/apt/keyrings/opensearch.gpg] https://artifacts.opensearch.org/releases/bundle/opensearch/3.x/apt stable main" \
   | sudo tee /etc/apt/sources.list.d/opensearch-3.x.list
   ```
   {% include copy.html %}

1. 確認儲存庫已成功建立：
    ```bash
    sudo apt-get update
    ```
    {% include copy.html %}

1. （選用）自 2024 年 5 月 22 日起，APT 儲存庫的 `Origin` 與 `Label` 值已隨著[此變更](https://github.com/opensearch-project/opensearch-build/issues/4485)更新。若您在此日期之前建立了 APT 儲存庫，請執行下列命令以接受更新後的發行資訊：
    ```bash
    sudo apt-get update --allow-releaseinfo-change
    ```
    {% include copy.html %}

1. 加入儲存庫資訊後，列出所有可用的 OpenSearch 版本：
   ```bash
   sudo apt list -a opensearch
   ```
   {% include copy.html %}

1. 選擇您要安裝的 OpenSearch 版本：
   - 除非另有指定，否則會安裝最新可用版本的 OpenSearch。

     對於 OpenSearch 2.12 及更新版本的全新安裝，您必須定義自訂的管理員密碼，才能設定示範安全性組態：
     ```bash
     sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password> apt-get install opensearch
     ```
     {% include copy.html %}

     如需更多資訊，請參閱[管理員密碼需求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)。
     {: .note}

   - 安裝特定版本的 OpenSearch。

     對於 OpenSearch 2.12 及更新版本的全新安裝，您必須定義自訂的管理員密碼，才能設定示範安全性組態：
     ```bash
     sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password> apt-get install opensearch={{site.opensearch_version}}
     ```
     {% include copy.html %}

     對於 OpenSearch 2.11 及更早版本，請使用下列命令：
     ```bash
     sudo apt-get install opensearch=<version>
     ```
     {% include copy.html %}

1. 若安裝成功，即表示 APT 已驗證儲存庫中繼資料是以受信任的 GPG 金鑰簽署。若要手動確認您匯入的金鑰與官方 OpenSearch 發行金鑰相符，請執行下列命令：

   ```bash
   gpg --no-default-keyring --keyring /etc/apt/trusted.gpg.d/opensearch.gpg --fingerprint
   ```
   {% include copy.html %}

   您應會在輸出中看到下列片段：
   ```bash
   pub   rsa4096 2021-05-11 [SC]
      C5B7 4989 65EF D1C2 924B  A9D5 39D3 1987 9310 D3FC
   ```
   {% include copy.html %}

1. 完成後，啟用 OpenSearch：
    ```bash
    sudo systemctl enable opensearch
    ```
    {% include copy.html %}

1. 啟動 OpenSearch：
    ```bash
    sudo systemctl start opensearch
    ```
    {% include copy.html %}

1. 確認 OpenSearch 已正確啟動：
    ```bash
    sudo systemctl status opensearch
    ```
    {% include copy.html %}

## 步驟 2：（選用）測試 OpenSearch

在進行任何組態設定之前，您應該先測試 OpenSearch 的安裝。否則，日後發生問題時，可能難以判斷問題是源自安裝問題，還是您在安裝後套用的自訂設定。

使用 Debian 套件安裝 OpenSearch 時，系統會自動套用部分示範安全性設定，包括自我簽署的 TLS 憑證以及數個使用者和角色。若您想自行設定這些項目，請參閱[在您的環境中設定 OpenSearch](#step-3-set-up-opensearch-in-your-environment)。

採用預設組態（使用示範憑證及預設密碼的使用者）的 OpenSearch 節點不適用於生產環境。若您打算在生產環境中使用該節點，至少應將示範 TLS 憑證替換為您自己的 TLS 憑證，並[更新內部使用者及密碼清單]({{site.url}}{{site.baseurl}}/security-plugin/configuration/yaml/)。如需確保節點依照您的安全性需求進行設定的其他指引，請參閱[安全性組態]({{site.url}}{{site.baseurl}}/security-plugin/configuration/index/)。
{: .warning}

1. 向伺服器傳送請求，以確認 OpenSearch 正在執行。請注意 `--insecure` 旗標的使用，由於 TLS 憑證為自我簽署，因此必須使用此旗標。
   - 向連接埠 9200 傳送請求：
      ```bash
      curl -X GET https://localhost:9200 -u 'admin:<custom-admin-password>' --insecure
      ```
      {% include copy.html %}

      您應該會收到類似以下內容的回應：
      ```json
      {
         "name":"hostname",
         "cluster_name":"opensearch",
         "cluster_uuid":"QqgpHCbnSRKcPAizqjvoOw",
         "version":{
            "distribution":"opensearch",
            "number":<version>,
            "build_type":<build-type>,
            "build_hash":<build-hash>,
            "build_date":<build-date>,
            "build_snapshot":false,
            "lucene_version":<lucene-version>,
            "minimum_wire_compatibility_version":"7.10.0",
            "minimum_index_compatibility_version":"7.0.0"
         },
         "tagline":"The OpenSearch Project: https://opensearch.org/"
      }
      ```
   - 查詢外掛程式端點：
    ```bash
    curl -X GET https://localhost:9200/_cat/plugins?v -u 'admin:<custom-admin-password>' --insecure
    ```
    {% include copy.html %}

    回應應類似以下內容：
    ```text
    name          component                            version
    hostname      opensearch-alerting                  {{site.opensearch_version}}
    hostname      opensearch-anomaly-detection         {{site.opensearch_version}}
    hostname      opensearch-asynchronous-search       {{site.opensearch_version}}
    hostname      opensearch-cross-cluster-replication {{site.opensearch_version}}
    hostname      opensearch-geospatial                {{site.opensearch_version}}
    hostname      opensearch-index-management          {{site.opensearch_version}}
    hostname      opensearch-job-scheduler             {{site.opensearch_version}}
    hostname      opensearch-knn                       {{site.opensearch_version}}
    hostname      opensearch-ml                        {{site.opensearch_version}}
    hostname      opensearch-neural-search             {{site.opensearch_version}}
    hostname      opensearch-notifications             {{site.opensearch_version}}
    hostname      opensearch-notifications-core        {{site.opensearch_version}}
    hostname      opensearch-observability             {{site.opensearch_version}}
    hostname      opensearch-performance-analyzer      {{site.opensearch_version}}
    hostname      opensearch-reports-scheduler         {{site.opensearch_version}}
    hostname      opensearch-security                  {{site.opensearch_version}}
    hostname      opensearch-security-analytics        {{site.opensearch_version}}
    hostname      opensearch-sql                       {{site.opensearch_version}}
    ```

## 步驟 3：在您的環境中設定 OpenSearch

沒有 OpenSearch 使用經驗的使用者，可能需要一份建議設定清單，以便開始使用此服務。根據預設，OpenSearch 不會繫結至網路介面，外部主機也無法連線。此外，安全性設定會填入預設的使用者名稱和密碼。以下建議可讓使用者將 OpenSearch 繫結至網路介面、建立並簽署 TLS 憑證，以及設定基本驗證。

以下建議設定可讓您：

- 將 OpenSearch 繫結至主機上的 IP 或網路介面。
- 設定 JVM 堆積的初始大小和最大大小。
- 定義指向隨附 JDK 的環境變數。
- 設定您自己的 TLS 憑證，不需要第三方憑證授權單位 (CA)。
- 建立具有自訂密碼的管理員使用者。

若您已執行安全性示範指令碼，則需要手動重新設定已被修改的設定。在繼續之前，請參閱[安全性組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)以取得指引。
{:.note}

在修改任何組態檔案之前，最好先儲存一份備份副本。備份檔案可用來減輕錯誤組態所造成的問題。
{:.tip}

1. 開啟 `opensearch.yml`：
   ```bash
   sudo vi /etc/opensearch/opensearch.yml
   ```
   {% include copy.html %}

1. 將內容替換為以下各行。

   用來儲存資料的目錄路徑（多個位置請以逗號分隔）：
   ```yaml
   path.data: /var/lib/opensearch
   ```
   {% include copy.html %}

   記錄檔路徑：
   ```yaml
   path.logs: /var/log/opensearch
   ```
   {% include copy.html %}

   將 OpenSearch 繫結至正確的網路介面。使用 0.0.0.0 以納入所有可用介面，或指定已指派給特定介面的 IP 位址：
   ```yaml
   network.host: 0.0.0.0
   ```
   {% include copy.html %}

   除非您已設定叢集，否則應將 discovery.type 設為 single-node，不然在您嘗試啟動服務時，啟動檢查將會失敗：
   ```yaml
   discovery.type: single-node
   ```
   {% include copy.html %}

   若您改為設定多節點叢集，請在主機上將 `vm.max_map_count` 設為至少 `262144`。否則，服務啟動時啟動檢查會失敗。如需更多資訊，請參閱[重要設定]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#important-settings)。

   若您先前已在 opensearch.yml 中停用 Security 外掛程式，請務必重新啟用。否則，您可以略過此設定：
   ```yaml
   plugins.security.disabled: false
   ```
   {% include copy.html %}

   [設定 TLS](#configure-tls) 一節提供新增自訂 TLS 組態的指引。

1. 儲存變更並關閉檔案。
1. 指定 JVM 堆積的初始大小和最大大小。
   1.  開啟 `jvm.options`：

         ```bash
         sudo vi /etc/opensearch/jvm.options
         ```
         {% include copy.html %}

   1. 修改初始堆積大小和最大堆積大小的值。一開始，您應將這些值設為可用系統記憶體的一半。若為專用主機，可依據您的工作流程需求增加此值。
      -  例如，若主機有 8 GB 記憶體，您可以將初始堆積大小和最大堆積大小設為 4 GB：

         ```text
         -Xms4g
         -Xmx4g
         ```
         {% include copy.html %}

   1. 儲存變更並關閉檔案。

### 設定 TLS

TLS 憑證可讓用戶端確認主機的身分，並加密用戶端與主機之間的流量，為您的叢集提供額外的安全性。如需詳細資訊，請參閱 [Security 外掛程式]({{site.url}}{{site.baseurl}}/security-plugin/index/)文件中的[設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security-plugin/configuration/tls/)與[產生憑證]({{site.url}}{{site.baseurl}}/security-plugin/configuration/generate-certificates/)。在開發環境中進行的工作，通常使用自我簽署憑證即可。本節將引導您完成產生自己的 TLS 憑證並將其套用至 OpenSearch 主機所需的基本步驟。

1. 刪除示範憑證：

   ```bash
   sudo sh -c 'rm /etc/opensearch/*.pem'
   ```
   {% include copy.html %}

1. 產生根憑證。您將使用此憑證來簽署其他憑證。

   為根憑證建立私密金鑰：
   ```bash
   sudo openssl genrsa -out /etc/opensearch/root-ca-key.pem 2048
   ```
   {% include copy.html %}

   使用私密金鑰建立自我簽署的根憑證。請務必取代傳遞給 -subj 的引數，使其反映您的特定主機：
   ```bash
   sudo openssl req -new -x509 -sha256 -key /etc/opensearch/root-ca-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=ROOT" -out /etc/opensearch/root-ca.pem -days 730
   ```
   {% include copy.html %}

1. 接著，建立管理員憑證。此憑證用於取得較高的權限，以執行與 Security 外掛程式相關的管理工作。

   為管理員憑證建立私密金鑰：
   ```bash
   sudo openssl genrsa -out /etc/opensearch/admin-key-temp.pem 2048
   ```
   {% include copy.html %}

   將私密金鑰轉換為 PKCS#8：
   ```bash
   sudo openssl pkcs8 -inform PEM -outform PEM -in /etc/opensearch/admin-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out /etc/opensearch/admin-key.pem
   ```
   {% include copy.html %}

   建立憑證簽署請求 (CSR)。一般名稱 (CN) 使用「A」即可，因為此憑證用於驗證較高權限的存取，且不與主機綁定：
   ```bash
   sudo openssl req -new -key /etc/opensearch/admin-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=A" -out /etc/opensearch/admin.csr
   ```
   {% include copy.html %}

   使用您先前建立的根憑證與私密金鑰簽署管理員憑證：
   ```bash
   sudo openssl x509 -req -in /etc/opensearch/admin.csr -CA /etc/opensearch/root-ca.pem -CAkey /etc/opensearch/root-ca-key.pem -CAcreateserial -sha256 -out /etc/opensearch/admin.pem -days 730
   ```
   {% include copy.html %}

1. 為正在設定的節點建立憑證。

   為節點憑證建立私密金鑰：
   ```bash
   sudo openssl genrsa -out /etc/opensearch/node1-key-temp.pem 2048
   ```
   {% include copy.html %}

   將私密金鑰轉換為 PKCS#8：
   ```bash
   sudo openssl pkcs8 -inform PEM -outform PEM -in /etc/opensearch/node1-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out /etc/opensearch/node1-key.pem
   ```
   {% include copy.html %}

   建立 CSR，並取代傳遞給 -subj 的引數，使其反映您的特定主機。CN 應與該主機的 DNS A 記錄相符，請勿使用主機名稱：
   ```bash
   sudo openssl req -new -key /etc/opensearch/node1-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=node1.dns.a-record" -out /etc/opensearch/node1.csr
   ```
   {% include copy.html %}

   建立擴充檔案，為主機定義 SAN DNS 名稱。此名稱應與主機的 DNS A 記錄相符：
   ```bash
   sudo sh -c 'echo subjectAltName=DNS:node1.dns.a-record > /etc/opensearch/node1.ext'
   ```
   {% include copy.html %}

   使用您先前建立的根憑證與私密金鑰簽署節點憑證：
   ```bash
   sudo openssl x509 -req -in /etc/opensearch/node1.csr -CA /etc/opensearch/root-ca.pem -CAkey /etc/opensearch/root-ca-key.pem -CAcreateserial -sha256 -out /etc/opensearch/node1.pem -days 730 -extfile /etc/opensearch/node1.ext
   ```
   {% include copy.html %}

1. 移除不再需要的暫存檔案：

   ```bash
   sudo sh -c 'rm -f /etc/opensearch/*temp.pem /etc/opensearch/*.csr /etc/opensearch/*.ext'
   ```
   {% include copy.html %}

1. 確認其餘憑證的擁有者為 `opensearch` 使用者：

   ```bash
   sudo chown opensearch:opensearch /etc/opensearch/admin-key.pem /etc/opensearch/admin.pem /etc/opensearch/node1-key.pem /etc/opensearch/node1.pem /etc/opensearch/root-ca-key.pem /etc/opensearch/root-ca.pem /etc/opensearch/root-ca.srl
   ```
   {% include copy.html %}

1. 依照[產生憑證]({{site.url}}{{site.baseurl}}/security-plugin/configuration/generate-certificates/#add-distinguished-names-to-opensearchyml)中的說明，將這些憑證新增至 `/etc/opensearch/opensearch.yml`。進階使用者也可以選擇使用下列指令碼附加這些設定。執行此指令碼之前，請務必將節點辨別名稱中的 CN 取代為實際的 DNS A 記錄：
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
   sudo install -m 0644 /etc/opensearch/root-ca.pem /usr/local/share/ca-certificates/root-ca.crt
   ```
   {% include copy.html %}

   新增信任：
   ```bash
   sudo update-ca-certificates
   ```
   {% include copy.html %}

### 設定使用者

OpenSearch 可透過多種方式定義及驗證使用者。其中一種不需要額外後端基礎架構的方法，是在 `internal_users.yml` 中手動設定使用者。如需設定使用者的詳細資訊，請參閱 [YAML 檔案]({{site.url}}{{site.baseurl}}/security-plugin/configuration/yaml/)。以下步驟說明如何使用指令碼取代 `admin` 的預設密碼：

1. 前往 Security 外掛程式的工具目錄：

   ```bash
   cd /usr/share/opensearch/plugins/opensearch-security/tools
   ```
   {% include copy.html %}

1. 執行 `hash.sh` 以產生新密碼。
   - 如果尚未定義 JDK 的路徑，此指令碼將會失敗。

      找不到 JDK 時的範例輸出：
      ```text
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
      OPENSEARCH_JAVA_HOME=/usr/share/opensearch/jdk ./hash.sh
      ```
      {% include copy.html %}

   - 在提示時輸入所需的密碼，並記下輸出的雜湊值。
1. 開啟 `internal_users.yml`：

   ```bash
   sudo vi /etc/opensearch/opensearch-security/internal_users.yml
   ```
   {% include copy.html %}

1. 將 `internal_users.yml` 中的 admin 密碼雜湊值取代為步驟 2 中 `hash.sh` 提供的輸出。該檔案應類似以下範例：

   ```yaml
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

   user1:
      hash: "$2y$12$zoHpvTCRjjQr6h0PEaabueCaGam3/LDvT6rZZGDGMusD7oehQjw/O"
      reserved: false
      backend_roles: []
      description: "New internal user"

   # Other users
   ...
   ```
   {% include copy.html %}

### 套用變更

現在 TLS 憑證已安裝完成，且示範使用者已移除或已指派新密碼，最後一個步驟是套用組態變更。此最後的組態步驟需要在主機上執行 OpenSearch 時呼叫 `securityadmin.sh`。

1. OpenSearch 必須處於執行狀態，`securityadmin.sh` 才能套用變更。如果您變更了 `opensearch.yml`，請重新啟動 OpenSearch：
   ```bash
   sudo systemctl restart opensearch
   ```
   {% include copy.html %}

1. 前往包含 `securityadmin.sh` 的目錄：
   ```bash
   cd /usr/share/opensearch/plugins/opensearch-security/tools
   ```
   {% include copy.html %}

1. 呼叫指令碼。如需您必須傳遞之引數的定義，請參閱[使用 securityadmin.sh 套用變更]({{site.url}}{{site.baseurl}}/security-plugin/configuration/security-admin/)。如果您已在 $PATH 中宣告環境變數，則可以省略該環境變數：
   ```bash
   sudo OPENSEARCH_JAVA_HOME=/usr/share/opensearch/jdk ./securityadmin.sh -cd /etc/opensearch/opensearch-security/ -cacert /etc/opensearch/root-ca.pem -cert /etc/opensearch/admin.pem -key /etc/opensearch/admin-key.pem -icl -nhnv
   ```
   {% include copy.html %}

### 確認服務正在執行

OpenSearch 現在已在您的主機上執行，並使用自訂 TLS 憑證及用於基本驗證的安全使用者。您可以從另一台主機向您的 OpenSearch 節點傳送 API 請求，以確認外部連線能力。

在先前的測試中，您將請求導向 `localhost`。現在 TLS 憑證已套用，且新憑證參照您主機實際的 DNS 記錄，因此傳送至 `localhost` 的請求將無法通過 CN 檢查，憑證也會被視為無效。請改為將請求傳送至您在產生憑證時指定的位址。

在傳送請求之前，您應在用戶端中新增對根憑證的信任。如果您未新增信任，則必須使用 `-k` 選項，讓 cURL 略過 CN 及根憑證驗證。
{:.tip}

```bash
curl https://localhost:9200 -u admin:<yournewpassword> -k
```
{% include copy.html %}

您應會收到以下回應：

```json
{
   "name":"hostname",
   "cluster_name":"opensearch",
   "cluster_uuid":"QqgpHCbnSRKcPAizqjvoOw",
   "version":{
      "distribution":"opensearch",
      "number":<version>,
      "build_type":<build-type>,
      "build_hash":<build-hash>,
      "build_date":<build-date>,
      "build_snapshot":false,
      "lucene_version":<lucene-version>,
      "minimum_wire_compatibility_version":"7.10.0",
      "minimum_index_compatibility_version":"7.0.0"
   },
   "tagline":"The OpenSearch Project: https://opensearch.org/"
}
```

## 升級至較新版本

使用 `dpkg` 或 `apt-get` 安裝的 OpenSearch 執行個體可以輕鬆升級至較新版本。

### 使用 `dpkg` 手動升級

直接從 [OpenSearch Project 下載頁面](https://opensearch.org/downloads.html){:target='\_blank'}下載所需升級版本的 Debian 套件。

前往包含該發行版本的目錄，並執行以下命令：

```bash
sudo dpkg -i opensearch-{{site.opensearch_version}}-linux-x64.deb
```
{% include copy.html %}

### 使用 `apt-get` 升級

若要使用 `apt-get` 升級至最新版本的 OpenSearch：

```bash
sudo apt-get upgrade opensearch
```
{% include copy.html %}

您也可以升級至特定的 OpenSearch 版本：

```bash
sudo apt-get upgrade opensearch=<version>
```
{% include copy.html %}

### 在套件升級後自動重新啟動服務

若要在套件升級後自動重新啟動 OpenSearch，請透過 `systemd` 啟用 `opensearch.service`：

```bash
sudo systemctl enable opensearch.service
```
{% include copy.html %}

## 相關文件

- [為正式環境準備叢集]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production)
- [常見的安裝問題]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#common-issues)
- [OpenSearch 組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)
- [安裝及設定 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/)
- [OpenSearch 外掛程式安裝]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)
- [關於 Security 外掛程式]({{site.url}}{{site.baseurl}}/security-plugin/index/)
