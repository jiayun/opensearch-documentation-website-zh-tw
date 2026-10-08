---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安裝 OpenSearch"
nav_order: 2
has_children: true
redirect_from:
  - /opensearch/install/
  - /opensearch/install/compatibility/
  - /opensearch/install/important-settings/
  - /opensearch/install/index/
  - /install-and-configure/install-opensearch/
---

# 安裝 OpenSearch

您可以使用 Docker、Helm、OpenSearch Kubernetes Operator、tarball、RPM、Debian 套件、Ansible 或在 Windows 上安裝 OpenSearch。每種方法都要求在您的主機上[開啟特定連接埠](#network-requirements)並設定[重要設定](#important-settings)。

若要在您的電腦上嘗試 OpenSearch，請參閱 [安裝快速入門]({{site.url}}{{site.baseurl}}/getting-started/quickstart/)。

關於作業系統相容性，請參閱 [相容的作業系統]({{site.url}}{{site.baseurl}}/install-and-configure/os-comp/)。

## 安裝步驟

安裝步驟根據部署方法而有所不同。如需針對您的部署方式的步驟，請參閱以下安裝指南：

- [Docker]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/)
- [OpenSearch Kubernetes Operator]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/)
- [Helm]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/helm/)
- [Debian]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/debian/)
- [RPM]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/rpm/)
- [Tarball]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/tar/)
- [Ansible playbook]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/ansible/)
- [Windows]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/windows/)

## 為生產環境準備叢集

[安裝快速入門]({{site.url}}{{site.baseurl}}/getting-started/quickstart/) 以及大多數指南中的預設安裝會建立一個使用示範安全性組態的叢集。示範組態使用自我簽署的示範憑證以及內部使用者的已知密碼，因此僅適用於測試。在生產環境中使用叢集之前，請完成以下任務：

- 將示範憑證替換為由您自己的憑證授權單位核發的憑證。如需更多資訊，請參閱 [設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/)。
- 設定使用者驗證方式。您可以使用 Security 外掛程式的內部使用者資料庫，或連接外部身分提供者以實現單一登入，例如 [SAML]({{site.url}}{{site.baseurl}}/security/authentication-backends/saml/)、[OpenID Connect]({{site.url}}{{site.baseurl}}/security/authentication-backends/openid-connect/) 或 [LDAP]({{site.url}}{{site.baseurl}}/security/authentication-backends/ldap/)。如需更多資訊，請參閱 [設定安全性後端]({{site.url}}{{site.baseurl}}/security/configuration/configuration/)。
- 將使用者或由身分提供者提供的後端角色對應到授予叢集存取權限的角色。如需更多資訊，請參閱 [定義使用者與角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/)。
- 替換示範內部使用者的預設密碼，或刪除不需要的使用者。如需更多資訊，請參閱 [示範組態密碼]({{site.url}}{{site.baseurl}}/security/configuration/passwords/#demo-configuration-passwords)。
- 在每台主機上設定 [重要設定](#important-settings)。
- 執行多個節點（包括專用的叢集管理員節點），以便在節點發生故障時叢集仍可用。如需更多資訊，請參閱 [建立叢集]({{site.url}}{{site.baseurl}}/tuning-your-cluster/)。
- 使用快照備份您的資料。如需更多資訊，請參閱 [快照]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/index/)。

如需更多安全性建議，請參閱 [OpenSearch 安全性最佳實踐]({{site.url}}{{site.baseurl}}/security/configuration/best-practices/)。

## 檔案系統建議

在生產環境的工作流程中，請避免使用網路檔案系統作為節點儲存空間。使用網路檔案系統作為節點儲存空間可能會因為網路狀況（如延遲或吞吐量受限）或讀寫速度等因素，導致叢集出現效能問題。只要可能，您應該使用安裝在主機上的固態硬碟 (SSD) 作為節點儲存空間。

## Java 相容性

Linux 版的 OpenSearch 分發版在 `jdk` 目錄中附帶了相容的 [Adoptium JDK](https://adoptium.net/) Java 版本。若要查看 JDK 版本，請執行 `./jdk/bin/java -version`。例如，OpenSearch 1.0.0 tarball 附帶 Java 15.0.1+9 (non-LTS)，OpenSearch 1.3.0 附帶 Java 11.0.14.1+1 (LTS)，而 OpenSearch 2.0.0 附帶 Java 17.0.2+8 (LTS)。OpenSearch 已通過所有相容 Java 版本的測試。

OpenSearch 版本 | 相容的 Java 版本 | 內建 Java 版本
:---------- | :-------- | :-----------
1.0--1.2.x    | 11, 15     | 15.0.1+9
1.3.x          | 8, 11, 14  | 11.0.25+9
2.0.0--2.11.x    | 11, 17     | 17.0.2+8
2.12.0+        | 11, 17, 21 | 21.0.11+10
3.2.0+        | 21, 24 | 24.0.2+12
3.5.0+        | 21, 25 | 25.0.2+10
3.6.1+        | 21, 25, 26 | 25.0.4.1+1

若要使用不同的 Java 安裝版本，請將 `OPENSEARCH_JAVA_HOME` 或 `JAVA_HOME` 環境變數設定為 Java 安裝位置。例如：

```bash
export OPENSEARCH_JAVA_HOME=/path/to/opensearch-{{site.opensearch_version}}/jdk
```
{% include copy.html %}

## 網路要求

OpenSearch 元件需要開啟以下 TCP 連接埠。

連接埠號碼 | OpenSearch 元件
:--- | :--- 
443 | AWS OpenSearch Service 中啟用傳輸中加密 (TLS) 的 OpenSearch Dashboards
5601 | OpenSearch Dashboards
9200 | OpenSearch REST API
9300 | 節點通訊與傳輸 (內部)、跨叢集搜尋
9600 | Performance Analyzer

不使用 UDP 連接埠。
{: .note}

## 重要設定

對於在 Linux 上執行的生產環境工作負載，請確保 [Linux 設定](https://www.kernel.org/doc/Documentation/sysctl/vm.txt) `vm.max_map_count` 至少設定為 `262144`。

即使您使用 Docker 映像檔，也請在主機機器上設定此值。若要檢查目前的值，請執行此命令：

```bash
cat /proc/sys/vm/max_map_count
```
{% include copy.html %}

若要增加此值，請將以下行新增至 `/etc/sysctl.conf`：

```
vm.max_map_count=262144
```
{% include copy.html %}

然後重新載入設定：

```bash
sudo sysctl -p
```
{% include copy.html %}

對於 Windows 工作負載，請在 Docker Desktop WSL 分發版中設定 `vm.max_map_count`。首先，在分發版中開啟 shell：

```bash
wsl -d docker-desktop
```
{% include copy.html %}

然後設定該值：

```bash
sysctl -w vm.max_map_count=262144
```
{% include copy.html %}

[範例 `docker-compose.yml`]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#sample-docker-composeyml) 檔案還包含幾個關鍵設定：

- `bootstrap.memory_lock=true`

  停用分頁 (swapping)（與 `memlock` 一同設定）。分頁可能會大幅降低效能與穩定性，因此您應確保在生產環境叢集中將其停用。

  啟用 `bootstrap.memory_lock` 設定將導致 JVM 預留其所需的所有記憶體。[Java SE Hotspot VM Garbage Collection Tuning Guide](https://docs.oracle.com/javase/9/gctuning/other-considerations.htm#JSGCT-GUID-B29C9153-3530-4C15-9154-E74F44E3DAD9) 記錄了預設 1 gigabyte (GB) 的 Class Metadata 原生記憶體預留。結合 Java heap，在記憶體低於這些要求的 VM 上，這可能會因為缺乏原生記憶體而導致錯誤。為了防止錯誤，請使用 `-XX:CompressedClassSpaceSize` 或 `-XX:MaxMetaspaceSize` 限制預留記憶體大小，並設定 Java heap 的大小以確保您有足夠的系統記憶體。

- `OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m`

  設定 Java heap 的大小（我們建議設定為系統 RAM 的一半）。
  
 OpenSearch 的 heap 記憶體配置預設為 `-Xms1g -Xmx1g`，其優先級高於使用百分比表示法 (`-XX:MinRAMPercentage`, `-XX:MaxRAMPercentage`) 指定的組態。例如，如果您設定 `OPENSEARCH_JAVA_OPTS=-XX:MinRAMPercentage=30 -XX:MaxRAMPercentage=70`，預定義的 `-Xms1g -Xmx1g` 值將覆蓋這些設定。使用 `OPENSEARCH_JAVA_OPTS` 定義記憶體配置時，請確保使用 `-Xms` 和 `-Xmx` 表示法。
{: .note}

- `nofile 65536`

  為 OpenSearch 使用者設定 65536 個開啟檔案的限制。

- `port 9600`

  允許您透過連接埠 9600 存取 Performance Analyzer。

請勿在多個位置宣告相同的 JVM 選項，因為這可能會導致非預期的行為或 OpenSearch 服務無法啟動。如果您使用環境變數（例如 `OPENSEARCH_JAVA_OPTS=-Xms3g -Xmx3g`）宣告 JVM 選項，則應將 `config/jvm.options` 中對該 JVM 選項的所有引用註解掉。反之，如果您在 `config/jvm.options` 中定義 JVM 選項，則不應使用環境變數定義這些 JVM 選項。
{: .note}

## 重要系統屬性

OpenSearch 有許多系統屬性（列於下表），您可以使用 `-D` 命令列參數表示法在 `config/jvm.options` 或 `OPENSEARCH_JAVA_OPTS` 中指定這些屬性。

屬性 | 說明
:---------- | :-------- 
`opensearch.xcontent.string.length.max=<value>` | 預設情況下，OpenSearch 不對 JSON/YAML/CBOR/Smile 字串欄位的最大長度設定任何限制。為了保護您的叢集免於潛在的分散式阻斷服務 (DDoS) 或記憶體問題，您可以將 `opensearch.xcontent.string.length.max` 系統屬性設定為合理的限制（最大值為 2,147,483,647），例如 `-Dopensearch.xcontent.string.length.max=5000000`。 | 
`opensearch.xcontent.fast_double_writer=[true|false]` | 預設情況下，OpenSearch 使用 Java Runtime Environment 提供的預設實作來序列化浮點數。將此值設定為 `true` 以使用 Schubfach 演算法，該演算法速度較快，但可能會導致微小的精度差異。預設值為 `false`。 |
`opensearch.xcontent.name.length.max=<value>` | 預設情況下，OpenSearch 不對 JSON/YAML/CBOR/Smile 欄位名稱的最大長度設定任何限制。為了保護您的叢集免於潛在的 DDoS 或記憶體問題，您可以將 `opensearch.xcontent.name.length.max` 系統屬性設定為合理的限制（最大值為 2,147,483,647），例如 `-Dopensearch.xcontent.name.length.max=50000`。 |
`opensearch.xcontent.depth.max=<value>` | 預設情況下，OpenSearch 不對 JSON/YAML/CBOR/Smile 文件的最大巢狀深度設定任何限制。為了保護您的叢集免於潛在的 DDoS 或記憶體問題，您可以將 `opensearch.xcontent.depth.max` 系統屬性設定為合理的限制（最大值為 2,147,483,647），例如 `-Dopensearch.xcontent.depth.max=1000`。 |
`opensearch.xcontent.codepoint.max=<value>` | 預設情況下，OpenSearch 對 YAML 文件的最大大小（以碼點為單位）設定 `52428800` 的限制。為了保護您的叢集免於潛在的 DDoS 或記憶體問題，您可以將 `opensearch.xcontent.codepoint.max` 系統屬性更改為合理的限制（最大值為 2,147,483,647）。例如 `-Dopensearch.xcontent.codepoint.max=5000000`。 |

## 常見問題

下列問題可能會發生在任何安裝方法中。

### 錯誤訊息：「max virtual memory areas vm.max_map_count [65530] is too low」

如果主機的 `vm.max_map_count` 設定過低，OpenSearch 在 Linux 上將無法啟動。OpenSearch 記錄檔會包含以下錯誤：

```
ERROR: [1] bootstrap checks failed
[1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
```

要修正此錯誤，請按照 [重要設定](#important-settings) 中的說明，將 `vm.max_map_count` 設定為至少 `262144`。如果您使用 Docker，請在主機機器上設定此值，而非在容器中設定。

### 錯誤訊息：「NotSslRecordException: not an SSL/TLS record」

示範安全性組態透過 HTTPS 提供 REST API 服務。如果用戶端透過 HTTP 發送請求，用戶端將收到空回應，且 OpenSearch 會為每個請求記錄以下錯誤：

```
io.netty.handler.ssl.NotSslRecordException: not an SSL/TLS record: 474554202f20485454502f312e310d0a...
```

要修正此錯誤，請將請求發送到 `https://localhost:9200` 而非 `http://localhost:9200`。請檢查每個連接到 OpenSearch 的用戶端，包括監視工具以及主機上定期發送請求的其他服務。

### 錯誤訊息：「Password failed validation」

如果 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 的值不是強密碼，OpenSearch 將無法啟動。OpenSearch 記錄檔會包含類似於以下的錯誤：

```
Password admin failed validation: "Password is too short". Please re-try with a minimum 8 character password and must contain at least one uppercase letter, one lowercase letter, one digit, and one special character that is strong.
```

要修正此錯誤，請選擇符合 [管理員密碼要求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements) 的密碼。

### 錯誤訊息：「the default discovery settings are unsuitable for production use」

當 OpenSearch 綁定到 `localhost` 以外的位址時（例如，在您將 `network.host` 設定為 `0.0.0.0` 以便其他主機可以存取之後），OpenSearch 會執行啟動檢查 (bootstrap checks)。如果節點沒有設定探索 (discovery) 設定，OpenSearch 將無法啟動並記錄以下錯誤：

```
bound or publishing to a non-loopback address, enforcing bootstrap checks
ERROR: [1] bootstrap checks failed
[1]: the default discovery settings are unsuitable for production use; at least one of [discovery.seed_hosts, discovery.seed_providers, cluster.initial_cluster_manager_nodes / cluster.initial_master_nodes] must be configured
```

要修正此錯誤，請在 `opensearch.yml` 中設定探索：

- 對於單節點叢集，請設定 `discovery.type: single-node`。
- 對於多節點叢集，請設定 `discovery.seed_hosts` 和 `cluster.initial_cluster_manager_nodes`。如需更多資訊，請參閱 [建立叢集]({{site.url}}{{site.baseurl}}/tuning-your-cluster/)。
