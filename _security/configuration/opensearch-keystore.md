---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenSearch 金鑰儲存庫"
parent: Configuration
nav_order: 40
---

# OpenSearch 金鑰儲存庫

`opensearch-keystore` 是用來管理 OpenSearch keystore 的公用程式指令碼。OpenSearch keystore 提供一種安全的方法，用於儲存 OpenSearch 叢集中使用的敏感資訊，例如密碼與金鑰。此指令碼可讓您安全地建立、列出、新增及移除設定。它已包含在 OpenSearch 發行版本中。

此 keystore 與用來以 JKS 或 PKCS12/PFX 格式儲存 TLS 憑證、以保護傳輸層與 HTTP 層的 keystore 及 truststore 是分開的。關於那些 keystore 的資訊，請參閱 [Keystore 與 truststore 檔案]({{site.url}}{{site.baseurl}}/security/configuration/tls/#keystore-and-truststore-files)。
{: .note} 

## 使用方式

若要使用 `opensearch-keystore` 指令碼，您必須能夠存取包含 OpenSearch 安裝的檔案系統，並具備執行 OpenSearch 指令碼的能力。

若要使用 `opensearch-keystore`，請開啟終端機並使用下列命令語法：

```
opensearch-keystore [command] [options]
```
{% include copy.html %}

## 命令

`opensearch-keystore` 指令碼支援下列命令：

- `create`：初始化新的 keystore。如果 keystore 已存在，此命令會覆寫現有的 keystore。
- `list`：列出 keystore 中的所有設定。
- `add <setting-name>`：將新設定新增至目前的 keystore。新增設定時，指令碼會提示您輸入該設定的值。新增設定與值之後，兩者都會安全地儲存在 keystore 中。
- `add-file <file-name>`：將新檔案新增至 keystore。
- `remove <setting-name>`：從 keystore 移除現有的設定。
- `upgrade <setting-name>`：升級 keystore 中現有的設定。
- `passwd`：為 keystore 設定密碼。
- `has-passwd`：顯示 keystore 是否受密碼保護。
- `help`：顯示所有 `opensearch-keystore` 命令的說明資訊。

## 選項

您可以在每個命令後面附加下列選項：

- `-h, --help`：顯示指令碼及其選項的說明資訊。
- `-s, --silent`：當指令碼回應命令時提供最精簡的輸出。
- `-v, --verbose`：提供用於偵錯的詳細輸出。
- `-p, --password`（僅限 `create` 命令）：指定用於加密 keystore 的密碼。若未使用此旗標，keystore 將在沒有密碼的情況下建立。

## 範例

下列範例提供常見 `opensearch-keystore` 命令的基本語法：

### 建立新的 keystore

下列命令會建立新的 keystore：

```bash
./bin/opensearch-keystore create
```
{% include copy.html %}

如果 keystore 已存在，指令碼會詢問您是否要覆寫現有的 keystore。

指令碼會回應確認訊息，表示 keystore 已建立：
   
```bash
Created opensearch keystore in $OPENSEARCH_HOME/config/opensearch.keystore
```

### 建立新的受密碼保護 keystore

若要建立新的受密碼保護 keystore，請執行下列命令：

```bash
./bin/opensearch-keystore create -p
```
{% include copy.html %}

如果 keystore 已存在，指令碼會詢問您是否要覆寫現有的 keystore。

### 設定 keystore 密碼

下列命令會設定新的 keystore 密碼：

```bash
./bin/opensearch-keystore passwd
```
{% include copy.html %}

如果 keystore 密碼已存在，指令碼會先要求您輸入目前的 keystore 密碼，才能重設密碼。
   
**回應**

指令碼會回應確認訊息，表示 keystore 密碼已成功設定：
   
```bash
OpenSearch keystore password changed successfully.
```

啟動 OpenSearch 時，系統會提示您輸入 keystore 密碼。或者，您可以設定環境變數 KEYSTORE_PASSWORD，以避免在啟動時被提示輸入密碼。
{: .note}

### 列出 keystore 中的設定

下列命令會列出 keystore 中目前所有的設定：
   
```bash
./bin/opensearch-keystore list
```
{% include copy.html %}

指令碼會回應 keystore 中的設定清單：

```bash
keystore.seed
plugins.security.ssl.http.pemkey_password_secure
```

### 新增設定

下列命令會新增 keystore 設定：

```bash
./bin/opensearch-keystore add plugins.security.ssl.http.pemkey_password_secure
```
{% include copy.html %}

執行此命令後，系統會提示您以安全方式輸入秘密金鑰。

### 移除設定

下列命令會移除 keystore 設定：

```bash
./bin/opensearch-keystore remove plugins.security.ssl.http.pemkey_password_secure
```
{% include copy.html %}

此命令沒有任何回應。若要確認設定已刪除，請使用 `opensearch-keystore list`。

關於可使用 `opensearch-keystore` 設定的完整安全設定清單，請參閱[（進階）使用 SSL 加密密碼設定]({{site.url}}{{site.baseurl}}/security/configuration/tls/#advanced-using-encrypted-password-settings-for-ssl)。
{: .note}

### 升級 keystore

下列命令會將 keystore 格式升級至最新版本：

```bash
./bin/opensearch-keystore upgrade
```
{% include copy.html %}

## 作為 OpenSearch 設定的 keystore 項目

設定新增至 keystore 之後，會隱含地新增至 OpenSearch 組態中，就像 `opensearch.yml` 中的另一個項目一樣。
