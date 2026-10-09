---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenSearch FIPS 組態"
parent: Configuration
nav_order: 55
---

# OpenSearch FIPS 組態

[聯邦資訊處理標準 (FIPS) 140-3](https://csrc.nist.gov/pubs/fips/140-3/final) 是一項美國政府標準，定義了密碼編譯模組的安全性需求。在符合 FIPS 的環境中執行 OpenSearch 時，您必須設定系統使用通過 FIPS 驗證的密碼編譯提供者。

若要達成 FIPS 合規，OpenSearch 需要：

- 所有密碼編譯作業都使用通過 FIPS 驗證的密碼編譯提供者（OpenSearch 內含 Bouncy Castle FIPS）。
- 設定為使用這些通過 FIPS 驗證提供者的 JVM。
- 使用 [BC-FJA](https://www.bouncycastle.org/download/bouncy-castle-java-fips/) 已認證之 Java 版本的 JVM（例如，OpenSearch v3.2.0+ 搭配 BC-FJA v2.1.0 時使用 Java 11、17 或 21）。
- BCFKS 或 PKCS11 格式且符合 FIPS 的 keystore 與 truststore。
- 符合 FIPS 最低需求的強式密碼（112 位元，約 14 個字元）。

## FIPS 示範安裝程式

預設情況下，JVM 使用 `cacerts` truststore（通常為 PKCS12 格式）進行 SSL/TLS 連線。此 truststore 包含受信任的憑證授權單位 (CA) 憑證。然而，標準 PKCS12 格式不符合 FIPS 規範。

OpenSearch 提供一個 FIPS 示範安裝程式 CLI 工具，可簡化 truststore 的組態程序。此工具提供自動化的方式，將 JVM 預設 truststore 轉換為 BCFKS 格式，以設定符合 FIPS 規範的 truststore。專案原始碼可在 `distribution/tools/fips-demo-installer-cli` 取得。

此工具僅設計用於示範與開發用途。部署至正式環境之前，請仔細檢閱所有產生的組態，並將示範設定替換為適合正式環境的值。
{: .warning}

### 必要條件

執行 FIPS 示範安裝程式之前，請確認符合下列必要條件：

- 已安裝 OpenSearch，且可存取安裝目錄。
- 您對 OpenSearch 組態目錄具有寫入權限。
- 組態目錄中存在 `jvm.options` 檔案。

### 可用命令

FIPS 示範安裝程式提供下列命令。

| 命令 | 說明 |
|---------|-------------|
| `generated` | 從 JVM 預設 truststore 產生新的 BCFKS truststore。 |
| `system` | 使用現有的系統 PKCS11 truststore。 |
| `show-providers` | 顯示可用的安全性提供者並結束（不會變更組態）。 |

### 組態選項

FIPS 示範安裝程式支援下列命令列選項。

| 選項 | 說明 |
|--------|-------------|
| `-f`, `--force` | 即使 `jvm.options` 中已存在 FIPS 設定，仍強制執行組態。 |
| `-n`, `--non-interactive` | 以非互動模式執行（使用預設值，不出現提示）。 |
| `-p`, `--password` | 為 BCFKS truststore 指定密碼（在非互動模式下覆寫自動產生的密碼）。 |
| `--pkcs11-provider` | 直接指定 PKCS11 提供者名稱（與 `system` 命令搭配使用）。 |
| `--help` | 顯示所支援命令的說明資訊。 |

### 非互動模式

若要在自動化部署時以非互動模式執行安裝程式，請使用 `-n` 或 `--non-interactive` 旗標：

```bash
./bin/opensearch-fips-demo-installer -n
```
{% include copy.html %}

非互動模式會在沒有提示的情況下執行，並自動執行下列動作：

- 預設產生新的 BCFKS truststore。
- 自動確認所有提示。
- 產生安全的 24 字元密碼（或使用透過 `-p` 指定的密碼）。
- 使用 `system` 命令時，選取第一個可用的 PKCS11 提供者。

非互動模式非常適合自動化佈建指令碼與組態管理工具。
{: .note}

### 範例

以下是 FIPS 示範安裝程式的一些常見命令範例。

在 Windows 上，請使用 `opensearch-fips-demo-installer.bat` 而非 bash 指令碼。
{: .note}

互動模式（對所有選擇出現提示）：
```bash
./bin/opensearch-fips-demo-installer
```
{% include copy.html %}

使用自動產生密碼的非互動模式---覆寫現有的 FIPS 組態：
```bash
./bin/opensearch-fips-demo-installer -n -f
```
{% include copy.html %}

以自訂密碼產生 BCFKS truststore：
```bash
./bin/opensearch-fips-demo-installer generated -p "MySecurePassword123!"
```
{% include copy.html %}

搭配特定提供者使用系統 PKCS11 truststore：
```bash
./bin/opensearch-fips-demo-installer system --pkcs11-provider YourPKCS11-Provider
```
{% include copy.html %}

### 組態輸出

執行 FIPS 示範安裝程式後，下列屬性會新增至您的 `jvm.options` 檔案：

```bash
################################################################
## Start OpenSearch FIPS Demo Configuration
## WARNING: revise all the lines below before you go into production
################################################################

-Djavax.net.ssl.trustStore=/path/to/opensearch/config/opensearch-fips-truststore.bcfks
-Djavax.net.ssl.trustStorePassword=<your-password>
-Djavax.net.ssl.trustStoreType=BCFKS
-Djavax.net.ssl.trustStoreProvider=BCFIPS
################################################################
```

若未定義其他 truststore，這些屬性會設定 JVM 對所有 SSL/TLS 連線使用符合 FIPS 規範的 truststore。

## FIPS 疑難排解

本節涵蓋在 FIPS 模式下執行 OpenSearch 時遇到的常見問題。

### 未指定 truststore 類型

下列錯誤表示 `jvm.options` 中的 FIPS truststore 組態不完整或遺失：

```
Trust store type must be specified using the '-Djavax.net.ssl.trustStoreType' JVM option. Accepted values are PKCS11 and BCFKS.
```

若要解決此問題：

- 確認您已成功執行 FIPS 示範安裝程式。
- 檢查 `jvm.options` 是否包含 FIPS truststore 組態區塊。

### 找不到 truststore 檔案

如果您看到指出找不到 truststore 檔案的錯誤，請確認：

- `jvm.options` 中的路徑正確且為絕對路徑。
- truststore 檔案存在於指定的位置。
- OpenSearch 對 truststore 檔案具有讀取權限。

### 憑證轉換失敗

JVM 預設 truststore 中的某些憑證可能與 BCFKS 格式不相容。安裝程式會報告成功轉換的憑證數量。請檢閱輸出，確保關鍵憑證已成功轉換。

### Keystore 密碼對 FIPS 模式而言太弱

當 [OpenSearch keystore]({{site.url}}{{site.baseurl}}/security/configuration/opensearch-keystore) `$OPENSEARCH_HOME/config/opensearch.keystore` 包含不符合 FIPS 需求的密碼時，OpenSearch 會無法啟動並出現下列錯誤：

```
org.bouncycastle.crypto.fips.FipsUnapprovedOperationError: password must be at least 112 bits
```

在 FIPS 模式下，Bouncy Castle 會強制要求密碼強度至少為 112 位元，約 14 個字元。

由於 FIPS 模式已啟用，`opensearch-keystore passwd` 命令不接受現有的弱式密碼。或者，您可以依照下列方式重建 keystore：

1. 列出現有的機密以供備份（如有需要）：
```bash
./bin/opensearch-keystore list
```
{% include copy.html %}

2. 使用符合 FIPS 規範的密碼（至少 14 個字元）建立新的 keystore：
```bash
./bin/opensearch-keystore create --password
```
{% include copy.html %}

3. 重新新增原本儲存在舊 keystore 中的機密（如有需要）：
```bash
./bin/opensearch-keystore add <setting-name>
```
{% include copy.html %}

請確保新密碼長度至少 14 個字元，並混合大寫字母、小寫字母、數字與特殊字元。基於安全性最佳實務，建議使用密碼管理工具來產生並儲存複雜的密碼。
{: .note}

## 後續步驟

為 OpenSearch 設定 FIPS 模式之後：

- 檢閱[安全性組態]({{site.url}}{{site.baseurl}}/security/configuration/index/)指南，了解其他安全性設定。
- 為節點對節點與用戶端對節點加密設定 [TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/)。
- 為您的叢集設定[驗證與授權]({{site.url}}{{site.baseurl}}/security/configuration/configuration/)。
- 為內部使用者密碼設定 [PBKDF2 密碼雜湊]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/security-settings/#expert-level-settings)，以確保符合 FIPS 規範。
- 設定[使用 FIPS 核准之雜湊演算法的欄位遮罩]({{site.url}}{{site.baseurl}}/security/access-control/field-masking/)，取代預設的 BLAKE2b。
- 檢閱 [OpenSearch 安全性最佳實務]({{site.url}}{{site.baseurl}}/security/configuration/best-practices/)，取得全面的安全性指引。
