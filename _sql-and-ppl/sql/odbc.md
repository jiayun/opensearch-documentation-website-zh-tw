---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ODBC 驅動程式"
parent: SQL
nav_order: 72
redirect_from:
  - /search-plugins/sql/odbc/
  - /search-plugins/sql/sql/odbc/
---

# ODBC 驅動程式

開放式資料庫連線（Open Database Connectivity，ODBC）驅動程式是適用於 Windows 和 macOS 的唯讀 ODBC 驅動程式，可讓您將 [Microsoft Excel](https://github.com/opensearch-project/sql-odbc/blob/main/docs/user/microsoft_excel_support.md) 和 [Power BI](https://github.com/opensearch-project/sql-odbc/blob/main/bi-connectors/PowerBIConnector/README.md) 等商業智慧（BI）與資料視覺化應用程式連線至 SQL 外掛程式。

如需下載及使用驅動程式的資訊，請參閱 [GitHub 上的 SQL 儲存庫](https://github.com/opensearch-project/sql-odbc)。

## 規格

ODBC 驅動程式與 ODBC 3.51 版相容。

## 支援的作業系統版本

支援下列作業系統：

作業系統 | 版本
:--- | :---
Windows | Windows 10, Windows 11
macOS | Catalina 10.15.4, Mojave 10.14.6, Big Sur 11.6.7, Monterey 12.4


## 概念

術語 | 定義
:--- | :---
**DSN** | DSN（資料來源名稱）用於在系統中儲存驅動程式資訊。將資訊儲存在系統中，就不需要在驅動程式每次連線時指定資訊。
**.tdc** 檔案 | TDC 檔案包含組態資訊，Tableau 會將這些資訊套用至符合檔案中所定義之資料庫廠商名稱與驅動程式名稱的任何連線。此組態可讓您微調 ODBC 資料連線的部分設定，並開啟／關閉資料來源不支援的特定功能。


## 安裝驅動程式

若要安裝驅動程式，請從[這裡](https://opensearch.org/downloads.html)下載套裝發行版安裝程式，或從原始碼建置。


### Windows

1. 開啟下載的 `OpenSearch SQL ODBC Driver-<version>-Windows.msi` 安裝程式。

   安裝程式未經簽署，會顯示安全性對話方塊。選擇 **More info** 和 **Run anyway**。

2. 選擇 **Next** 以繼續安裝。

3. 接受協議，然後選擇 **Next**。

4. 安裝程式隨附文件和實用的資源檔案，可用於連線至各種 BI 工具（例如，供 Tableau 使用的 `.tdc` 檔案）。您可以選擇保留或移除這些資源。選擇 **Next**。

5. 選擇 **Install** 和 **Finish**。

下列連線資訊會設為預設 DSN 的一部分：

```
Host: localhost
Port: 9200
Auth: NONE
```
{% include copy.html %}


若要自訂 DSN，請使用 Windows 10 預先安裝的 **ODBC Data Source Administrator**。

### macOS

在 macOS 上安裝 ODBC 驅動程式之前，請先安裝 iODBC Driver Manager。

1. 開啟下載的 `OpenSearch SQL ODBC Driver-<version>-Darwin.pkg` 安裝程式。

   安裝程式未經簽署，會顯示安全性對話方塊。在安裝程式上按一下滑鼠右鍵，然後選擇 **Open**。

2. 選擇 **Continue** 數次以繼續安裝。

3. 選擇 **Destination** 以安裝驅動程式檔案。

4. 安裝程式隨附文件和實用的資源檔案，可用於連線至各種 BI 工具（例如，供 Tableau 使用的 `.tdc` 檔案）。您可以選擇保留或移除這些資源。選擇 **Continue**。

5. 選擇 **Install** 和 **Close**。

目前，安裝過程不會設定 DSN，因此需要手動設定。首先，開啟 `iODBC Administrator`：

```
sudo /Applications/iODBC/iODBC\ Administrator64.app/Contents/MacOS/iODBC\ Administrator64
```
{% include copy.html %}


此命令會授予應用程式儲存驅動程式與 DSN 組態的權限。

1. 選擇 **ODBC Drivers** 索引標籤。
2. 選擇 **Add a Driver**，並填入下列詳細資訊：
   - **Description of the Driver**：輸入您用於 ODBC 連線的驅動程式名稱（例如，OpenSearch SQL ODBC Driver）。
   - **Driver File Name**：輸入驅動程式檔案的路徑（預設：`<driver-install-dir>/bin/libopensearchsqlodbc.dylib`）。
   - **Setup File Name**：輸入設定檔案的路徑（預設：`<driver-install-dir>/bin/libopensearchsqlodbc.dylib`）。

3. 選擇使用者驅動程式。
4. 選擇 **OK** 以儲存選項。
5. 選擇 **User DSN** 索引標籤。
6. 選取 **Add**。
7. 選擇您先前新增的驅動程式。
8. 在 **Data Source Name (DSN)** 中，輸入用於儲存連線選項的 DSN 名稱（例如，OpenSearch SQL ODBC DSN）。
9. 在 **Comment** 中，新增選用的註解。
10. 使用 `+` 按鈕新增索引鍵值組。對於預設的本機 OpenSearch 安裝，我們建議使用下列選項：
<!-- vale off -->

   - **Host**：`localhost` - OpenSearch 伺服器端點
   - **Port**：`9200` - 伺服器連接埠
   - **Auth**：`NONE` - 驗證模式
   - **Username**：`(blank)` - 用於 BASIC 驗證的使用者名稱
   - **Password**：`(blank)`- 用於 BASIC 驗證的密碼
   - **ResponseTimeout**：`10` - 等待伺服器回應的秒數
   - **UseSSL**：`0` - 連線不使用 SSL

<!-- vale on -->

11. 選擇 **OK** 以儲存 DSN 組態。
12. 選擇 **OK** 以結束 iODBC Administrator。


## 自訂 ODBC 驅動程式

驅動程式以程式庫檔案的形式提供：Windows 使用 `opensearchsqlodbc.dll`，macOS 使用 `libopensearchsqlodbc.dylib`。

如果您搭配與 ODBC 相容的 BI 工具使用，請參閱您的 BI 工具文件，瞭解如何設定新的 ODBC 驅動程式。
通常，您只需要讓 BI 工具知道驅動程式程式庫檔案的位置，然後使用該檔案設定資料庫（即 OpenSearch）連線。


### 連線字串與其他設定

ODBC 驅動程式使用 ODBC 連線字串。
連線字串是以分號分隔的字串，用於指定連線可使用的一組選項。
通常，連線字串會採用下列其中一種方式：
  - 指定包含一組預先設定選項的資料來源名稱（DSN）（`DSN=xxx;User=xxx;Password=xxx;`）。
  - 或者，使用字串明確設定選項（`Host=xxx;Port=xxx;LogLevel=ES_DEBUG;...`）。

您可以使用 DSN 或連線字串設定下列驅動程式選項：

所有選項名稱均不區分大小寫。
{: .note }


#### 基本選項

選項 | 說明 | 類型 | 預設值
:--- | :---
`DSN` | 您用於設定連線的資料來源名稱。 | `string` | -
`Host / Server` | 目標叢集的主機名稱或 IP 位址。 | `string` | -
`Port` | OpenSearch 叢集的 REST 介面接聽的連接埠號碼。 | `string` | -

#### 驗證選項

<!-- vale off -->

選項 | 說明 | 類型 | 預設值
:--- | :---
`Auth` | 要使用的驗證機制。 | `BASIC`（基本 HTTP）、`AWS_SIGV4`（AWS 驗證）或 `NONE` | `NONE`
`User / UID` | [`Auth=BASIC`] 連線的使用者名稱。 | `string` | -
`Password / PWD` | [`Auth=BASIC`] 連線的密碼。 | `string` | -
`Region` | [`Auth=AWS_SIGV4`] 用於簽署請求的區域。 | `AWS region (for example, us-west-1)` | -

<!-- vale on -->

#### 進階選項

選項 | 說明 | 類型 | 預設值
:--- | :---
`UseSSL` | 是否透過 SSL/TLS 建立連線。 | `boolean (0 or 1)` | `false (0)`
`HostnameVerification` | 指出是否應對 SSL/TLS 連線執行憑證主機名稱驗證。 | `boolean`（0 或 1） | `true (1)`
`ResponseTimeout` | 等待主機回應的最長時間，以秒為單位。 | `integer` | `10`

#### 記錄選項

選項 | 說明 | 類型 | 預設值
:--- | :---
`LogLevel` | 驅動程式記錄檔的嚴重性層級。 | `LOG_OFF`、`LOG_FATAL`、`LOG_ERROR`、`LOG_INFO`、`LOG_DEBUG`、`LOG_TRACE` 或 `LOG_ALL` | `LOG_WARNING`
`LogOutput` | 儲存驅動程式記錄檔的位置。 | `string` | `WIN: C:\`, `MAC: /tmp`

您需要管理員權限才能變更記錄選項。
{: .note }

## 連線至 Tableau

先決條件：

- 確認已設定 DSN。
- 確認 OpenSearch 正在 DSN 中設定的 _host_ 和 _port_ 上執行。
- 確認在 macOS 和 Windows 上都已將 `.tdc` 複製至 `<user_home_directory>/Documents/My Tableau Repository/Datasources`。

1. 啟動 Tableau。在 **Connect** 區段下，前往 **To a Server** 並選擇 **Other Databases (ODBC)**。

2. 在 **DSN drop-down** 中，選取您在前述步驟中設定的 OpenSearch DSN。您新增的選項會自動填入 **Connection Attributes** 下方。

3. 選取 **Sign In**。幾秒後，Tableau 會連線至您的 OpenSearch 伺服器。連線成功後，您會進入 **Datasource** 視窗。**Database** 中會已填入 OpenSearch 叢集的名稱。
若要列出所有索引，請按一下 **Table** 下方的搜尋圖示。

4. 將資料表拖曳至連線區域，開始探索資料。選擇 **Update Now** 或 **Automatically Update** 以填入資料表資料。

請參閱 [GitHub 儲存庫](https://github.com/opensearch-project/sql/blob/1.x/sql-odbc/docs/user/tableau_support.md)中的更詳細說明。

### 疑難排解

**問題**

無法連線至伺服器。

**因應方式**

這很可能是因為 OpenSearch 伺服器未在 DSN 中設定的 **host** 和 **post** 上執行。
請確認 **host** 和 **post** 正確，且 OpenSearch 伺服器正在搭配 OpenSearch SQL 外掛程式執行。
另請確認隨安裝程式下載的 `.tdc` 已正確複製至 `<user_home_directory>/Documents/My Tableau Repository/Datasources` 目錄。

## 連線至 Microsoft Power BI

請遵循 GitHub 儲存庫中發布的[安裝說明](https://github.com/opensearch-project/sql-odbc/tree/main/bi-connectors/PowerBIConnector/README.md)與[組態說明](https://github.com/opensearch-project/sql-odbc/blob/main/bi-connectors/PowerBIConnector/power_bi_support.md)。
