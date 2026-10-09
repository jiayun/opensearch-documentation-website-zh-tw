---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: describe
parent: Commands
grand_parent: PPL
nav_order: 12
---

<!-- vale off -->

# describe 命令

<!-- vale on -->

`describe` 命令會查詢索引中繼資料。`describe` 命令只能作為 PPL 查詢中的第一個命令使用。

## 語法

`describe` 命令具有下列語法。此命令的引數是以點分隔的資料表路徑，由選用的資料來源、選用的結構描述，以及必要的資料表名稱組成：

```sql
describe [<data-source>.][<schema>.]<table-name>
```

## 參數

`describe` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<table-name>` | 必要 | 要查詢的資料表。 |  
| `<data-source>` | 選用 | 要使用的資料來源。預設為 OpenSearch `datasource`。 |
| `<schema>` | 選用 | 要使用的結構描述。預設為預設結構描述。 |

## 範例 1：擷取所有中繼資料  

此範例說明 `accounts` 索引：
  
```sql
describe accounts
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| TABLE_CAT | TABLE_SCHEM | TABLE_NAME | COLUMN_NAME | DATA_TYPE | TYPE_NAME | COLUMN_SIZE | BUFFER_LENGTH | DECIMAL_DIGITS | NUM_PREC_RADIX | NULLABLE | REMARKS | COLUMN_DEF | SQL_DATA_TYPE | SQL_DATETIME_SUB | CHAR_OCTET_LENGTH | ORDINAL_POSITION | IS_NULLABLE | SCOPE_CATALOG | SCOPE_SCHEMA | SCOPE_TABLE | SOURCE_DATA_TYPE | IS_AUTOINCREMENT | IS_GENERATEDCOLUMN |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| docTestCluster | null | accounts | account_number | null | bigint | null | null | null | 10 | 2 | null | null | null | null | null | 0 |  | null | null | null | null | NO |  |
| docTestCluster | null | accounts | firstname | null | string | null | null | null | 10 | 2 | null | null | null | null | null | 1 |  | null | null | null | null | NO |  |
| docTestCluster | null | accounts | address | null | string | null | null | null | 10 | 2 | null | null | null | null | null | 2 |  | null | null | null | null | NO |  |
| docTestCluster | null | accounts | balance | null | bigint | null | null | null | 10 | 2 | null | null | null | null | null | 3 |  | null | null | null | null | NO |  |
| docTestCluster | null | accounts | gender | null | string | null | null | null | 10 | 2 | null | null | null | null | null | 4 |  | null | null | null | null | NO |  |
| docTestCluster | null | accounts | city | null | string | null | null | null | 10 | 2 | null | null | null | null | null | 5 |  | null | null | null | null | NO |  |
| docTestCluster | null | accounts | employer | null | string | null | null | null | 10 | 2 | null | null | null | null | null | 6 |  | null | null | null | null | NO |  |
| docTestCluster | null | accounts | state | null | string | null | null | null | 10 | 2 | null | null | null | null | null | 7 |  | null | null | null | null | NO |  |
| docTestCluster | null | accounts | age | null | bigint | null | null | null | 10 | 2 | null | null | null | null | null | 8 |  | null | null | null | null | NO |  |
| docTestCluster | null | accounts | email | null | string | null | null | null | 10 | 2 | null | null | null | null | null | 9 |  | null | null | null | null | NO |  |
| docTestCluster | null | accounts | lastname | null | string | null | null | null | 10 | 2 | null | null | null | null | null | 10 |  | null | null | null | null | NO |  |

<!-- vale on -->
  

## 範例 2：擷取具有條件與篩選的中繼資料  

此範例會從 `accounts` 索引擷取 `bigint` 類型的資料行：
  
```sql
describe accounts
| where TYPE_NAME="bigint"
| fields COLUMN_NAME
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| COLUMN_NAME |
| --- |
| account_number |
| balance |
| age |

<!-- vale on -->
  
<!-- temporarily commented out because the admin section is not ported
## Example 3: Fetching table metadata for a Prometheus data source

See [Fetch metadata for table in Prometheus datasource]({{site.url}}{{site.baseurl}}/sql-and-ppl/sql-and-ppl-api/data-source-apis/) for more context.
-->