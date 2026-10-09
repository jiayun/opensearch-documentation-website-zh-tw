---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "識別字"
nav_order: 6
redirect_from:
  - /search-plugins/sql/identifiers/
  - /observability-plugin/ppl/identifiers/
  - /search-plugins/ppl/identifiers/
---


# SQL 和 PPL 識別字

識別字是用來命名資料庫物件的 ID，例如索引名稱、欄位名稱、別名等。OpenSearch 支援兩種類型的識別字：一般識別字和分隔識別字。

## 一般識別字

一般識別字是以 ASCII 字母（小寫或大寫）開頭的字元字串。
下一個字元可以是字母、數字或底線 (_)。它不能是保留關鍵字。
也不允許使用空白和其他特殊字元。

OpenSearch 支援下列一般識別字：

1. 以點 `.` 符號為前綴的識別字。用於隱藏索引。例如 `.opensearch-dashboards`。
2. 以 `@` 符號為前綴的識別字。用於 Logstash 匯入時產生的中繼資料欄位。
3. 中間含有連字號 `-` 的識別字。用於包含日期資訊的索引名稱。
4. 含有星號 `*` 的識別字。用於索引模式的萬用字元比對。

對於一般識別字，您可以直接使用名稱，無須加上反引號或跳脫字元。
在此範例中，`source`、`fields`、`account_number`、`firstname` 和 `lastname` 都是識別字。其中，`source` 欄位是保留識別字。

```sql
SELECT account_number, firstname, lastname FROM accounts;
```
{% include copy.html %}

查詢傳回下列結果：

<!-- vale off -->

| account_number | firstname | lastname |
:--- | :--- |
| 1  | Amber | Duke       
| 6  | Hattie | Bond
| 13 | Nanette | Bates
| 18 | Dale | Adams

<!-- vale on -->


## 分隔識別字

分隔識別字可以包含一般識別字不允許的特殊字元。
您必須以反引號（\`\`）括住分隔識別字。反引號可區分識別字與特殊字元。

如果索引名稱包含點（`.`），例如 `log-2021.01.11`，請使用以反引號括住的分隔識別字來跳脫它 \``log-2021.01.11`\`。

使用分隔識別字的典型範例：

1. 含有保留關鍵字的識別字。
2. 含有 `.` 的識別字。同樣地，使用 `-` 來包含日期資訊。
3. 含有其他特殊字元的識別字。例如 Unicode 字元。

若要以反引號括住索引名稱：

```sql
source=`accounts` | fields `account_number`;
```
{% include copy.html %}

查詢傳回下列結果：

<!-- vale off -->

| account_number |
:--- |
| 1  |       
| 6  |
| 13 |
| 18 |

<!-- vale on -->

## 大小寫區分

識別字會區分大小寫。它們必須與儲存在 OpenSearch 中的內容完全相同。

例如，如果您執行 `source=Accounts`，就會收到找不到索引的例外，因為實際的索引名稱是小寫。
