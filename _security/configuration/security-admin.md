---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "套用組態檔案的變更"
parent: Configuration
nav_order: 25
has_children: true
has_toc: false
redirect_from:
  - /security-plugin/configuration/security-admin/
---

# 套用組態檔案的變更

在 **Windows** 上，請使用 **securityadmin.bat** 取代 **securityadmin.sh**。如需詳細資訊，請參閱 [Windows 用法](#windows-usage)。
{: .note}

Security 外掛程式會將其組態（包括使用者、角色、權限和後端設定）儲存在 OpenSearch 叢集上的[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)中。將這些設定儲存在索引中，可讓您在不重新啟動叢集的情況下變更設定，而且不需要在每個節點上個別編輯組態檔案。這是透過執行 `securityadmin.sh` 指令碼來完成的。

此指令碼的第一項工作是初始化 `.opendistro_security` 索引。這會使用 `/config/opensearch-security` 中的組態檔案，將您的初始組態載入索引。`.opendistro_security` 索引初始化之後，您就可以使用 OpenSearch Dashboards 或 REST API 來管理使用者、角色和權限。

此指令碼位於 `/plugins/opensearch-security/tools/securityadmin.sh`。這是顯示 `securityadmin.sh` 指令碼所在位置的相對路徑。絕對路徑取決於您安裝 OpenSearch 的目錄。例如，如果您使用 Docker 安裝 OpenSearch，路徑會類似以下內容：`/usr/share/opensearch/plugins/opensearch-security/tools/securityadmin.sh`。

`securityadmin.sh` 指令碼要求您的 OpenSearch 叢集啟用 SSL/TLS HTTP。繼續操作之前，請在 `opensearch.yml` 檔案中設定 `plugins.security.ssl.http.enabled: true`。如果您的叢集未在 HTTP 層使用 SSL/TLS，但需要 `securityadmin.sh`，請在單一節點（例如`ingest` 節點）上啟用 SSL/TLS，然後在該節點上執行 `securityadmin.sh`。請僅在一個節點上設定 [REST 層 TLS]({{site.url}}{{site.baseurl}}/security/configuration/tls/#rest-layer-tls) 設定，以啟用此設定。每次變更 `opensearch.yml` 檔案後，都必須在該節點上重新啟動 OpenSearch。
{: .note}

## 注意事項

如果您變更 `config/opensearch-security` 中的組態檔案，OpenSearch _不會_自動套用這些變更。您必須執行 `securityadmin.sh`，將更新後的檔案載入索引。`securityadmin.sh` 檔案位於 `<OPENSEARCH_HOME>/plugins/opensearch-security/tools/securityadmin.[sh|bat]`。

執行 `securityadmin.sh` 會**覆寫** `.opendistro_security` 索引的一個或多個部分。請極為謹慎地執行，以免遺失現有的資源。請參考以下範例：

1. 您初始化 `.opendistro_security` 索引。
1. 您使用 REST API 建立十個使用者。
1. 您決定使用 `<OPENSEARCH_HOME>/config/opensearch-security/` 目錄中的 `internal_users.yml` 建立新的[保留使用者]({{site.url}}{{site.baseurl}}/security/access-control/api/#reserved-and-hidden-resources)。
1. 您再次執行 `securityadmin.sh`，將新的保留使用者載入索引。
1. 您遺失了使用 REST API 建立的全部十個使用者。

為避免這種情況，請在進行變更並重新執行指令碼之前，先備份目前的組態：

```bash
./securityadmin.sh -backup my-backup-directory \
  -icl \
  -nhnv \
  -cacert ../../../config/root-ca.pem \
  -cert ../../../config/kirk.pem \
  -key ../../../config/kirk-key.pem
```

您也可以讓 OpenSearch 保留安全性組態的歷史紀錄，以便在發生非預期的變更後還原較早的版本。如需詳細資訊，請參閱[安全性組態版本 API]({{site.url}}{{site.baseurl}}/security/api/configuration-versions/)。

如果您使用 `-f` 引數而非 `-cd`，就可以將單一 YAML 檔案載入索引，而不是載入整個 YAML 檔案目錄。例如，如果您建立了十個新角色，可以安全地將 `internal_users.yml` 載入索引而不會遺失這些角色；只有內部使用者會被覆寫。

```bash
./securityadmin.sh -f ../../../config/opensearch-security/internal_users.yml \
  -t internalusers \
  -icl \
  -nhnv \
  -cacert ../../../config/root-ca.pem \
  -cert ../../../config/kirk.pem \
  -key ../../../config/kirk-key.pem
```

若要在套用安全性組態之前解析所有環境變數，請使用 `-rev` 參數。

```bash
./securityadmin.sh -cd ../../../config/opensearch-security/ \
 -rev \
 -cacert ../../../root-ca.pem \
 -cert ../../../kirk.pem \
 -key ../../../kirk.key.pem
```

以下範例顯示 `config.yml` 檔案中的環境變數：

```yml
password: ${env.LDAP_PASSWORD}
```

## 設定管理員憑證

若要使用 `securityadmin.sh`，您必須將所有管理員憑證的辨別名稱 (DN) 新增至 `opensearch.yml`。例如，如果您使用示範憑證，`opensearch.yml` 中可能會包含以下適用於 `kirk` 憑證的程式碼行：

```yml
plugins.security.authcz.admin_dn:
  - CN=kirk,OU=client,O=client,L=test,C=DE
```

您無法將節點憑證當作管理員憑證使用，兩者必須分開。此外，請勿在 DN 的各部分之間加入空白字元。
{: .warning }


## 基本用法

`securityadmin.sh` 工具可以從任何能存取 OpenSearch 叢集 HTTP 連接埠（預設連接埠為 9200）的機器上執行。您不需要透過 SSH 存取節點，即可變更 Security 外掛程式組態。


每個節點也在 `plugins/opensearch-security/tools/securityadmin.sh` 提供此工具。您可能需要先將指令碼設為可執行，才能執行它：

```bash
chmod +x plugins/opensearch-security/tools/securityadmin.sh
```

若要列出所有可用的命令列選項，請不帶任何引數執行指令碼：

```bash
./plugins/opensearch-security/tools/securityadmin.sh
```

## 搭配 PEM 檔案使用 `securityadmin`

若要載入初始組態（所有 YAML 檔案），您可以使用以下命令：

```bash
./securityadmin.sh -cd ../../../config/opensearch-security/ -icl -nhnv \
  -cacert ../../../config/root-ca.pem \
  -cert ../../../config/kirk.pem \
  -key ../../../config/kirk-key.pem
```

- `-cd` 選項指定 Security 外掛程式組態檔案的位置。
- `-icl` (`--ignore-clustername`) 選項會讓 Security 外掛程式不論叢集名稱為何都上傳組態。或者，您也可以使用 `-cn` (`--clustername`) 選項指定叢集名稱。
- 由於示範憑證是自我簽署的，此命令會使用 `-nhnv` (`--disable-host-name-verification`) 選項停用主機名稱驗證。
- `-cacert`、`-cert` 和 `-key` 選項定義根 CA 憑證、管理員憑證，以及管理員憑證私密金鑰的位置。如果私密金鑰有密碼，請使用 `-keypass` 選項指定。

下表列出 PEM 選項。

名稱 | 說明
:--- | :---
`-cert` | 包含管理員憑證及所有中繼憑證（如有）的 PEM 檔案位置。您可以使用絕對路徑或相對路徑。相對路徑會以 `securityadmin.sh` 的執行目錄為基準進行解析。
`-key` | 包含管理員憑證私密金鑰的 PEM 檔案位置。您可以使用絕對路徑或相對路徑。相對路徑會以 `securityadmin.sh` 的執行目錄為基準進行解析。金鑰必須為 PKCS#8 格式。
`-keypass` | 管理員憑證私密金鑰的密碼（如有）。
`-cacert` | 包含根憑證的 PEM 檔案位置。您可以使用絕對路徑或相對路徑。相對路徑會以 `securityadmin.sh` 的執行目錄為基準進行解析。

## 搭配 keystore 與 truststore 檔案使用 `securityadmin`

JKS 格式的 keystore 檔案與 `securityadmin.sh` 相容，如下列範例設定所示：

```bash
./securityadmin.sh -cd ../../../config/opensearch-security -icl -nhnv
  -ts <path/to/truststore> -tspass <truststore password>
  -ks <path/to/keystore> -kspass <keystore password>
```

使用下列選項來控制 keystore 與 truststore 設定。

名稱 | 說明
:--- | :---
`-ks` | 包含管理員憑證及所有中繼憑證 (若有) 的 keystore 位置。您可以使用絕對或相對路徑。相對路徑會相對於 `securityadmin.sh` 執行目錄解析。
`-kspass` | keystore 密碼。
`-kst` | keystore 類型，可為 JKS 或 PKCS#12/PFX。若未指定，Security 外掛程式會嘗試根據副檔名判斷類型。
`-ksalias` | 管理員憑證的別名 (若有)。
`-ts` | 包含根憑證的 truststore 位置。您可以使用絕對或相對路徑。相對路徑會相對於 `securityadmin.sh` 執行目錄解析。
`-tspass` | truststore 密碼。
`-tst` | truststore 類型，可為 JKS 或 PKCS#12/PFX。若未指定，Security 外掛程式會嘗試根據副檔名判斷類型。
`-tsalias` | 根憑證的別名 (若有)。

簽署 `admin` 憑證的憑證授權單位 (CA) 可能與用於簽署傳輸或 HTTP 憑證的 CA 不同。不過，該 CA 必須新增至 truststore 才能驗證憑證。如需詳細資訊，請參閱[產生節點與用戶端憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/#optional-generate-node-and-client-certificates)。
{: .note}

## 範例命令

使用 PEM 憑證套用 `config/opensearch-security/` 中的所有 YAML 檔案：

```bash
/usr/share/opensearch/plugins/opensearch-security/tools/securityadmin.sh \
  -cacert /etc/opensearch/root-ca.pem \
  -cert /etc/opensearch/kirk.pem \
  -key /etc/opensearch/kirk-key.pem \
  -cd /usr/share/opensearch/config/opensearch-security/
```

使用 PEM 憑證套用單一 YAML 檔案 (`config.yml`)：

```bash
./securityadmin.sh \
  -f ../../../config/opensearch-security/config.yml \
  -icl -nhnv -cert /etc/opensearch/kirk.pem \
  -cacert /etc/opensearch/root-ca.pem \
  -key /etc/opensearch/kirk-key.pem \
  -t config
```

使用 keystore 與 truststore 檔案套用 `config/opensearch-security/` 中的所有 YAML 檔案：

```bash
./securityadmin.sh \
  -cd /usr/share/opensearch/config/opensearch-security/ \
  -ks /path/to/keystore.jks \
  -kspass changeit \
  -ts /path/to/truststore.jks \
  -tspass changeit
  -nhnv
  -icl
```


### OpenSearch 設定

如果您執行的是預設的 OpenSearch 安裝，其會接聽連接埠 9200 並使用 `opensearch` 作為叢集名稱，則可以完全省略下列設定。否則，請使用下列參數指定您的 OpenSearch 設定。

名稱 | 說明
:--- | :---
`-h` | OpenSearch 主機名稱。預設為 `localhost`。
`-p` | OpenSearch 連接埠。預設為 9200
`-cn` | 叢集名稱。預設為 `opensearch`。
`-icl` | 忽略叢集名稱。
`-sniff` | 探查叢集節點。探查會使用 OpenSearch `_cluster/state` API 偵測可用的節點。
`-arc,--accept-red-cluster` | 即使叢集狀態為 red 也執行 `securityadmin.sh`。預設為 `false`，表示指令碼不會在 red 叢集上執行。


### 憑證驗證設定

使用下列選項來控制憑證驗證。

名稱 | 說明
:--- | :---
`-nhnv` | 不驗證主機名稱。預設為 `false`。
`-nrhn` | 不解析主機名稱。僅在未設定 `-nhnv` 時相關。


### 組態檔案設定

下列參數定義您要推送至 Security 外掛程式的組態檔案。您可以推送單一檔案，或指定包含一或多個組態檔案的目錄。

名稱 | 說明
:--- | :---
`-cd` | 包含多個 Security 外掛程式組態檔案的目錄。
`-f` | 單一組態檔案。無法與 `-cd` 搭配使用。
`-t` | 檔案類型。
`-rl` | 重新載入目前的組態並排清內部快取。

若要上傳目錄中的所有組態檔案，請使用：

```bash
./securityadmin.sh -cd ../../../config/opensearch-security -ts ... -tspass ... -ks ... -kspass ...
```

如果您想推送單一組態檔案，請使用：

```bash
./securityadmin.sh -f ../../../config/opensearch-security/internal_users.yml -t internalusers  \
    -ts ... -tspass ... -ks ... -kspass ...
```

檔案類型必須為下列其中之一：

* `config`
* `roles`
* `rolesmapping`
* `internalusers`
* `actiongroups`


### 密碼套件設定

您可能不需要變更密碼套件設定。如果需要，請使用下列選項。

名稱 | 說明
:--- | :---
`-ec` | 以逗號分隔的已啟用 TLS 密碼套件清單。
`-ep` | 以逗號分隔的已啟用 TLS 通訊協定清單。


### 備份、還原與遷移

您可以使用下列命令，從叢集下載所有目前的組態檔案：

```bash
./securityadmin.sh -backup my-backup-directory -ts ... -tspass ... -ks ... -kspass ...
```

此命令會將叢集目前的 Security 外掛程式組態傾印至您指定目錄中的個別檔案。您接著可以使用這些檔案作為備份，或將組態載入至不同的叢集。當您將概念驗證移至生產環境，或需要新增其他[保留或隱藏資源]({{site.url}}{{site.baseurl}}/security/access-control/api/#reserved-and-hidden-resources)時，此命令很有用：

```bash
./securityadmin.sh \
  -backup my-backup-directory \
  -icl \
  -nhnv \
  -cacert ../../../config/root-ca.pem \
  -cert ../../../config/kirk.pem \
  -key ../../../config/kirk-key.pem
```

若要將傾印的檔案上傳至另一個叢集：

```bash
./securityadmin.sh -h production.example.com -p 9301 -cd /etc/backup/ -ts ... -tspass ... -ks ... -kspass ...
```

若要將組態 YAML 檔案從 Open Distro for Elasticsearch 0.x.x 格式遷移至 OpenSearch 1.x.x 格式：

```bash
./securityadmin.sh -migrate ../../../config/opensearch-security -ts ... -tspass ... -ks ... -kspass ...
```

名稱 | 說明
:--- | :---
`-backup` | 從執行中的叢集擷取目前的 Security 外掛程式組態，並將其傾印至工作目錄。
`-migrate` | 將組態 YAML 檔案從 Open Distro for Elasticsearch 0.x.x 遷移至 OpenSearch 1.x.x。


### 其他選項

名稱 | 說明
:--- | :---
`-dci` | 刪除 Security 外掛程式組態索引並結束。如果叢集狀態因 Security 外掛程式索引損毀而為 red，此選項很有用。
`-dg,--diagnose` | 將診斷追蹤記錄至檔案。指令碼會列印所產生檔案的位置。
`-esa` | 啟用分片配置並結束。如果您在執行完整叢集重新啟動時停用了分片配置，且需要重新建立 Security 外掛程式索引，此選項很有用。
`-w` | 顯示所使用管理員憑證的相關資訊。
`-rl` | 根據預設，Security 外掛程式會將已驗證的使用者及其角色與權限快取一小時。此選項會重新載入儲存於叢集中的目前 Security 外掛程式組態，使任何快取的使用者、角色與權限失效。
`-i` | Security 外掛程式索引名稱。預設為 `.opendistro_security`。
`-er` | 為 `opensearch_security` 索引設定明確的副本數或自動擴充運算式。
`-era` | 啟用副本自動擴充。
`-dra` | 停用副本自動擴充。
`-us` | 更新副本設定。

## Windows 使用方式

在 Windows 上，`securityadmin.sh` 的對應工具是位於 `\path\to\opensearch-{{site.opensearch_version}}\plugins\opensearch-security\tools\` 目錄中的 `securityadmin.bat` 指令碼。

執行前面章節的範例命令時，請使用**命令提示字元**或 **Powershell**。在工作列 **Start** 旁的搜尋方塊中輸入 `cmd` 即可開啟命令提示字元，或輸入 `powershell` 開啟 Powershell。

例如，若要印出所有可用的命令列選項，請不帶任何引數執行該指令碼：

```bat
.\plugins\opensearch-security\tools\securityadmin.bat
```

輸入多行命令時，請使用插入號 (`^`) 字元來跳脫命令列中的下一個字元。

例如，若要載入初始組態 (所有 YAML 檔案)，請使用以下命令：

```bat
.\securityadmin.bat -cd ..\..\..\config\opensearch-security\ -icl -nhnv ^
  -cacert ..\..\..\config\root-ca.pem ^
  -cert ..\..\..\config\kirk.pem ^
  -key ..\..\..\config\kirk-key.pem
```

## 疑難排解

- 如需常見 `securityadmin.sh` 組態問題的解決方案，請參閱[疑難排解 securityadmin.sh]({{site.url}}{{site.baseurl}}/security/configuration/troubleshoot-security-admin/)。
