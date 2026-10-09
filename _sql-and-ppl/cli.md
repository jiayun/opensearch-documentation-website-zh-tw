---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "SQL 與 PPL CLI"
nav_order: 3
redirect_from:
 - /search-plugins/sql/cli/
---

# SQL 與 PPL CLI

SQL 與 PPL 命令列介面 (CLI) 是一個獨立的 Python 應用程式，您可以使用 `opensearchsql` 命令啟動。

 若要使用 SQL 與 PPL CLI，請在您的 OpenSearch 執行個體上安裝 SQL 外掛程式，在 macOS 或 Linux 上執行 CLI，並連線至任何有效的 OpenSearch 端點。

![SQL CLI]({{site.url}}{{site.baseurl}}/images/cli.gif)

## 功能

SQL 與 PPL CLI 具有以下功能：

- 多行輸入
- 支援 PPL
- SQL 語法與索引名稱的自動完成
- 語法突顯
- 格式化輸出：
  - 表格格式
  - 彩色欄位名稱
  - 預設啟用水平顯示，當輸出內容對您的終端機而言過寬時改用垂直顯示，以利視覺化
  - 大量輸出時提供分頁
- 無論是否啟用安全性皆可運作
- 支援載入組態檔
- 支援所有 SQL 外掛程式查詢

## 安裝

啟動您的本機 OpenSearch 執行個體，並確認已安裝 SQL 外掛程式。

1. 安裝 CLI：
```console
pip3 install opensearchsql
```
{% include copy.html %}


SQL CLI 僅適用於 Python 3。
{: .note }

2. 若要啟動 CLI，請執行：
```console
opensearchsql https://localhost:9200 --username admin --password admin
```
{% include copy.html %}

預設情況下，`opensearchsql` 命令會連線至 http://localhost:9200。

## 設定

當您首次啟動 SQL CLI 時，系統會自動在 `~/.config/opensearchsql-cli/config` (macOS 與 Linux) 建立組態檔，之後便會自動載入該組態。

您可以設定以下連線屬性：

- `endpoint`：您不需要指定選項。啟動命令 `opensearchsql` 之後的任何內容都會被視為端點。如果您未提供端點，預設情況下，SQL CLI 會連線至 http://localhost:9200。
- `-u/-w`：支援 HTTP 基本驗證的使用者名稱與密碼，例如搭配 Security 外掛程式或 Amazon OpenSearch Service 的精細存取控制。
- `--aws-auth`：啟用 AWS Signature Version 4 驗證以連線至 Amazon OpenSearch 端點。請搭配 AWS CLI (`aws configure`) 使用，以擷取本機 AWS 組態進行驗證與連線。

如需所有可用組態的清單，請參閱 [`clirc`](https://github.com/opensearch-project/sql/blob/1.x/sql-cli/src/opensearch_sql_cli/conf/clirc)。

## 使用 CLI

1. 執行 CLI 工具。如果您的叢集以預設安全性設定執行，請使用以下命令：
```console
opensearchsql --username admin --password admin https://localhost:9200
```
{% include copy.html %}

如果您的叢集在未啟用安全性的情況下執行，請執行：
```console
opensearchsql
```
{% include copy.html %}


2. 執行範例 SQL 命令：
```sql
SELECT * FROM accounts;
```
{% include copy.html %}


預設情況下，您最多會看到 200 列輸出。若要顯示更多結果，請加上 `LIMIT` 子句並指定所需的值。

若要結束 CLI 工具，請按 **Ctrl+D**。
{: .tip }

## 搭配 PPL 使用 CLI

1. 指定查詢語言來執行 CLI：
```console
opensearchsql -l ppl <params>
```
{% include copy.html %}


2. 執行 PPL 查詢：
```sql
source=accounts | fields firstname, lastname
```
{% include copy.html %}


## 查詢選項

使用以下命令列選項執行單一查詢：

- `-q`：後面接著單一查詢
- `-f`：指定 JDBC 或原始格式輸出
- `-v`：垂直顯示資料
- `-e`：將 SQL 轉換為 DSL

## CLI 選項

- `--help`：選項的說明頁面
- `-l`：查詢語言選項。可用選項為 `sql` 與 `ppl`。預設為 `sql`
- `-p`：一律使用分頁器顯示輸出
- `--clirc`：提供組態檔的路徑
