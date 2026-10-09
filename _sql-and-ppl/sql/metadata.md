---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "中繼資料查詢"
parent: SQL
nav_order: 9
redirect_from:
  - /search-plugins/sql/metadata/
  - /search-plugins/sql/sql/metadata/
---

# SQL 中繼資料查詢

若要檢視索引的基本中繼資料，請使用 `SHOW` 和 `DESCRIBE` 命令。

### 語法

規則 `showStatement`：

<!-- vale off -->

![showStatement]({{site.url}}{{site.baseurl}}/images/showStatement.png)

<!-- vale on -->

規則 `showFilter`：

<!-- vale off -->

![showFilter]({{site.url}}{{site.baseurl}}/images/showFilter.png)

<!-- vale on -->

### 範例 1：檢視索引的中繼資料

若要檢視符合特定模式的索引中繼資料，請使用 `SHOW` 命令。
使用萬用字元 `%` 來比對所有索引：

```sql
SHOW TABLES LIKE %
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| TABLE_CAT | TABLE_SCHEM | TABLE_NAME | TABLE_TYPE | REMARKS | TYPE_CAT | TYPE_SCHEM | TYPE_NAME | SELF_REFERENCING_COL_NAME | REF_GENERATION |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `docker-cluster` | null | accounts | BASE TABLE | null | null | null | null | null | null |
| `docker-cluster` | null | employees_nested | BASE TABLE | null | null | null | null | null | null |

<!-- vale on -->


### 範例 2：檢視特定索引的中繼資料

若要檢視索引名稱前置字元為 `acc` 的中繼資料：

```sql
SHOW TABLES LIKE acc%
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| TABLE_CAT | TABLE_SCHEM | TABLE_NAME | TABLE_TYPE | REMARKS | TYPE_CAT | TYPE_SCHEM | TYPE_NAME | SELF_REFERENCING_COL_NAME | REF_GENERATION |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `docker-cluster` | null | accounts | BASE TABLE | null | null | null | null | null | null |

<!-- vale on -->


### 範例 3：檢視索引中所有欄位的中繼資料

若要檢視符合特定模式之索引中所有欄位的中繼資料，請使用 `DESCRIBE` 命令：

```sql
DESCRIBE TABLES LIKE accounts
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| TABLE_CAT | TABLE_SCHEM | TABLE_NAME | COLUMN_NAME | DATA_TYPE | TYPE_NAME | COLUMN_SIZE | BUFFER_LENGTH | DECIMAL_DIGITS | NUM_PREC_RADIX | NULLABLE | REMARKS | COLUMN_DEF | SQL_DATA_TYPE | SQL_DATETIME_SUB | CHAR_OCTET_LENGTH | ORDINAL_POSITION | IS_NULLABLE | SCOPE_CATALOG | SCOPE_SCHEMA | SCOPE_TABLE | SOURCE_DATA_TYPE | IS_AUTOINCREMENT | IS_GENERATEDCOLUMN |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `docker-cluster` | null | accounts | account_number | null | long | null | null | null | 10 | 2 | null | null | null | null | null | 1 |  | null | null | null | null | NO |  |
| `docker-cluster` | null | accounts | firstname | null | text | null | null | null | 10 | 2 | null | null | null | null | null | 2 |  | null | null | null | null | NO |  |
| `docker-cluster` | null | accounts | address | null | text | null | null | null | 10 | 2 | null | null | null | null | null | 3 |  | null | null | null | null | NO |  |
| `docker-cluster` | null | accounts | balance | null | long | null | null | null | 10 | 2 | null | null | null | null | null | 4 |  | null | null | null | null | NO |  |
| `docker-cluster` | null | accounts | gender | null | text | null | null | null | 10 | 2 | null | null | null | null | null | 5 |  | null | null | null | null | NO |  |
| `docker-cluster` | null | accounts | city | null | text | null | null | null | 10 | 2 | null | null | null | null | null | 6 |  | null | null | null | null | NO |  |
| `docker-cluster` | null | accounts | employer | null | text | null | null | null | 10 | 2 | null | null | null | null | null | 7 |  | null | null | null | null | NO |  |
| `docker-cluster` | null | accounts | state | null | text | null | null | null | 10 | 2 | null | null | null | null | null | 8 |  | null | null | null | null | NO |  |
| `docker-cluster` | null | accounts | age | null | long | null | null | null | 10 | 2 | null | null | null | null | null | 9 |  | null | null | null | null | NO |  |
| `docker-cluster` | null | accounts | email | null | text | null | null | null | 10 | 2 | null | null | null | null | null | 10 |  | null | null | null | null | NO |  |
| `docker-cluster` | null | accounts | lastname | null | text | null | null | null | 10 | 2 | null | null | null | null | null | 11 |  | null | null | null | null | NO |  |

<!-- vale on -->

### 範例 4：檢視特定欄位的中繼資料

若只要檢視名稱符合特定模式之欄位的中繼資料，請在 `DESCRIBE` 命令中新增 `COLUMNS LIKE` 子句。下列查詢會傳回 `accounts` 索引中名稱以 `name` 結尾之欄位的中繼資料：

```sql
DESCRIBE TABLES LIKE accounts COLUMNS LIKE %name
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| TABLE_CAT | TABLE_SCHEM | TABLE_NAME | COLUMN_NAME | DATA_TYPE | TYPE_NAME | COLUMN_SIZE | BUFFER_LENGTH | DECIMAL_DIGITS | NUM_PREC_RADIX | NULLABLE | REMARKS | COLUMN_DEF | SQL_DATA_TYPE | SQL_DATETIME_SUB | CHAR_OCTET_LENGTH | ORDINAL_POSITION | IS_NULLABLE | SCOPE_CATALOG | SCOPE_SCHEMA | SCOPE_TABLE | SOURCE_DATA_TYPE | IS_AUTOINCREMENT | IS_GENERATEDCOLUMN |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `docker-cluster` | null | accounts | firstname | null | text | null | null | null | 10 | 2 | null | null | null | null | null | 1 |  | null | null | null | null | NO |  |
| `docker-cluster` | null | accounts | lastname | null | text | null | null | null | 10 | 2 | null | null | null | null | null | 2 |  | null | null | null | null | NO |  |

<!-- vale on -->
