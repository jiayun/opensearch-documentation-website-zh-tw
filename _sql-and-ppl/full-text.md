---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "全文搜尋"
nav_order: 11
description: "OpenSearch 透過 MATCH 函式及其他對應至 OpenSearch 全文查詢的 SQL 函式，在 SQL 中支援全文搜尋。"
redirect_from:
  - /search-plugins/sql/full-text/
---

# 全文搜尋

使用 SQL 命令進行全文搜尋。SQL 外掛程式支援 OpenSearch 中可用全文查詢的一部分。

若要了解 OpenSearch 中的全文查詢，請參閱[全文查詢]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/full-text/index/)。

## 比對

使用 `MATCH` 函式搜尋與指定欄位的 `string`、`number`、`date` 或 `boolean` 值相符的文件。

### 語法

```sql
match(field_expression, query_expression[, option=<option_value>]*)
```

您可以依任意順序指定下列選項：

- `analyzer`
- `auto_generate_synonyms_phrase`
- `fuzziness`
- `max_expansions`
- `prefix_length`
- `fuzzy_transpositions`
- `fuzzy_rewrite`
- `lenient`
- `operator`
- `minimum_should_match`
- `zero_terms_query`
- `boost`

如需參數說明及支援的值，請參閱 `match` 查詢[文件]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match/)。

### 範例 1：在 `message` 欄位中搜尋文字「this is a test」：

```json
GET my_index/_search
{
  "query": {
    "match": {
      "message": "this is a test"
    }
  }
}
```
{% include copy-curl.html %}

*SQL 查詢：*
```sql
SELECT message FROM my_index WHERE match(message, "this is a test")
```
{% include copy.html %}


*PPL 查詢：*
```sql
SOURCE=my_index | WHERE match(message, "this is a test") | FIELDS message
```
{% include copy.html %}


### 範例 2：使用 `operator` 參數搜尋 `message` 欄位：

```json
GET my_index/_search
{
  "query": {
    "match": {
      "message": {
        "query": "this is a test",
        "operator": "and"
      }
    }
  }
}
```
{% include copy-curl.html %}

*SQL 查詢：*
```sql
SELECT message FROM my_index WHERE match(message, "this is a test", operator='and')
```
{% include copy.html %}


*PPL 查詢：*
```sql
SOURCE=my_index | WHERE match(message, "this is a test", operator='and') | FIELDS message
```
{% include copy.html %}


### 範例 3：使用 `operator` 和 `zero_terms_query` 參數搜尋 `message` 欄位：

```json
GET my_index/_search
{
  "query": {
    "match": {
      "message": {
        "query": "to be or not to be",
        "operator": "and",
        "zero_terms_query": "all"
      }
    }
  }
}
```
{% include copy-curl.html %}

*SQL 查詢：*
```sql
SELECT message FROM my_index WHERE match(message, "this is a test", operator='and', zero_terms_query='all')
```
{% include copy.html %}


*PPL 查詢：*
```sql
SOURCE=my_index | WHERE match(message, "this is a test", operator='and', zero_terms_query='all') | FIELDS message
```
{% include copy.html %}


## 多欄位比對

若要在多個欄位中搜尋文字，請使用 `MULTI_MATCH` 函式。此函式對應至搜尋引擎中使用的 `multi_match` 查詢，會傳回與一或多個指定欄位中所提供的文字、數字、日期或布林值相符的文件。

### 語法

`MULTI_MATCH` 函式使用 **^** 字元來*提升 (boost)* 特定欄位的權重。提升值是乘數，可讓某個欄位中的相符項目比其他欄位中的相符項目具有更高的權重。此語法支援以雙引號、單引號、反引號或不加任何引號的方式指定欄位。使用星號 ``"*"`` 可搜尋所有欄位。星號必須加上引號。

```sql
multi_match([field_expression+], query_expression[, option=<option_value>]*)
```
{% include copy.html %}


權重為選用，並指定於欄位名稱之後。權重可以使用 `caret` 字元（`^`）或空白字元分隔。請參閱下列範例：

```sql
multi_match(["Tags" ^ 2, 'Title' 3.4, `Body`, Comments ^ 0.3], ...)
multi_match(["*"], ...)
```
{% include copy.html %}


您可以依任意順序為 `MULTI_MATCH` 指定下列選項：

- `analyzer`
- `auto_generate_synonyms_phrase`
- `cutoff_frequency`
- `fuzziness`
- `fuzzy_transpositions`
- `lenient`
- `max_expansions`
- `minimum_should_match`
- `operator`
- `prefix_length`
- `tie_breaker`
- `type`
- `slop`
- `zero_terms_query`
- `boost`

如需參數說明及支援的值，請參閱 `multi_match` 查詢[文件]({{site.url}}{{site.baseurl}}/query-dsl/full-text/multi-match/)。

### 例如，在 `firstname` 或 `lastname` 欄位中搜尋 `Dale` 的 REST API 搜尋：

```json
GET accounts/_search
{
  "query": {
    "multi_match": {
      "query": "Lane Street",
      "fields": [ "address" ],
    }
  }
}
```
{% include copy-curl.html %}

可以從 *SQL* 使用 `multi_match` 函式呼叫：

```sql
SELECT firstname, lastname
FROM accounts
WHERE multi_match(['*name'], 'Dale')
```
{% include copy.html %}


或使用 `multi_match` *PPL* 函式：

```sql
SOURCE=accounts | WHERE multi_match(['*name'], 'Dale') | fields firstname, lastname
```
{% include copy.html %}


此查詢會傳回下列結果：

<!-- vale off -->

| firstname | lastname |
| :--- | :--- |
| Dale | Adams |

<!-- vale on -->

## 查詢字串

若要根據運算子分割文字，請使用 `QUERY_STRING` 函式。`QUERY_STRING` 函式支援邏輯連接詞、萬用字元、規則運算式及鄰近搜尋。
此函式對應至搜尋引擎中使用的 `query_string` 查詢，會傳回與一或多個指定欄位中所提供的文字、數字、日期或布林值相符的文件。

### 語法

`QUERY_STRING` 函式的語法與 `MATCH_QUERY` 類似，並使用 **^** 字元來*提升 (boost)* 特定欄位的權重。提升值是乘數，可讓某個欄位中的相符項目比其他欄位中的相符項目具有更高的權重。此語法支援以雙引號、單引號、反引號或不加任何引號的方式指定欄位。使用星號 ``"*"`` 可搜尋所有欄位。星號必須加上引號。

```sql
query_string([field_expression+], query_expression[, option=<option_value>]*)
```
{% include copy.html %}


權重為選用，並指定於欄位名稱之後。權重可以使用 `caret` 字元（`^`）或空白字元分隔。請參閱下列範例：

```sql
query_string(["Tags" ^ 2, 'Title' 3.4, `Body`, Comments ^ 0.3], ...)
query_string(["*"], ...)
```
{% include copy.html %}


您可以依任意順序為 `QUERY_STRING` 指定下列選項：

- `analyzer`
- `allow_leading_wildcard`
- `analyze_wildcard`
- `auto_generate_synonyms_phrase_query`
- `boost`
- `default_operator`
- `enable_position_increments`
- `fuzziness`
- `fuzzy_rewrite`
- `escape`
- `fuzzy_max_expansions`
- `fuzzy_prefix_length`
- `fuzzy_transpositions`
- `lenient`
- `max_determinized_states`
- `minimum_should_match`
- `quote_analyzer`
- `phrase_slop`
- `quote_field_suffix`
- `rewrite`
- `type`
- `tie_breaker`
- `time_zone`

如需參數說明及支援的值，請參閱 `query_string` 查詢[文件]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)。

### 在 SQL 和 PPL 查詢中使用 `query_string` 的範例：

下列 REST API 搜尋請求

```json
GET accounts/_search
{
  "query": {
    "query_string": {
      "query": "Lane Street",
      "fields": [ "address" ],
    }
  }
}
```
{% include copy-curl.html %}

可以從 *SQL* 呼叫

```sql
SELECT account_number, address
FROM accounts
WHERE query_string(['address'], 'Lane Street', default_operator='OR')
```
{% include copy.html %}


或從 *PPL* 呼叫：

```sql
SOURCE=accounts | WHERE query_string(['address'], 'Lane Street', default_operator='OR') | fields account_number, address
```
{% include copy.html %}


此查詢會傳回下列結果：

<!-- vale off -->

| account_number | address |
| :--- | :--- |
| 1 | 880 Holmes Lane |
| 6 | 671 Bristol Street |
| 13 | 789 Madison Street |

<!-- vale on -->

## 片語比對

若要搜尋確切的片語，請使用 `MATCHPHRASE` 或 `MATCH_PHRASE` 函式。

### 語法

```sql
matchphrasequery(field_expression, query_expression)
matchphrase(field_expression, query_expression[, option=<option_value>]*)
match_phrase(field_expression, query_expression[, option=<option_value>]*)
```
{% include copy.html %}


`MATCHPHRASE`/`MATCH_PHRASE` 函式可讓您以任意順序指定下列選項：

- `analyzer`
- `slop`
- `zero_terms_query`
- `boost`

參數說明與支援的值請參閱 `match_phrase` 查詢的[文件]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/)。

### 在 SQL 與 PPL 查詢中使用 `match_phrase` 的範例：

REST API 搜尋請求
```json
GET accounts/_search
{
  "query": {
    "match_phrase": {
      "address": {
        "query": "880 Holmes Lane"
      }
    }
  }
}
```
{% include copy-curl.html %}

可以從 *SQL* 呼叫
```sql
SELECT account_number, address
FROM accounts
WHERE match_phrase(address, '880 Holmes Lane')
```
{% include copy.html %}


或從 *PPL* 呼叫
```sql
SOURCE=accounts | WHERE match_phrase(address, '880 Holmes Lane') | FIELDS account_number, address
```
{% include copy.html %}


查詢會傳回下列結果：

<!-- vale off -->

| account_number | address
:--- | :---
1 | 880 Holmes Lane

<!-- vale on -->


## 簡易查詢字串

`simple_query_string` 函式對應到 OpenSearch 中的 `simple_query_string` 查詢。它會傳回在指定的一個或多個欄位中，符合所提供文字、數字、日期或布林值的文件。
**^** 可讓您對特定欄位進行 *boost*（加權）。加權是乘數，會讓某個欄位中的相符結果比其他欄位中的相符結果獲得更高的權重。

### 語法

此語法支援以雙引號、單引號、反引號或不加引號的方式指定欄位。使用星號 ``"*"`` 可搜尋所有欄位。星號應加上引號。

```sql
simple_query_string([field_expression+], query_expression[, option=<option_value>]*)
```
{% include copy.html %}


權重為選用，指定在欄位名稱之後。可以用 `caret` 字元 -- `^` 或空白字元分隔。請參閱下列範例：

```sql
simple_query_string(["Tags" ^ 2, 'Title' 3.4, `Body`, Comments ^ 0.3], ...)
simple_query_string(["*"], ...)
```
{% include copy.html %}


您可以以任意順序為 `SIMPLE_QUERY_STRING` 指定下列選項：

- `analyze_wildcard`
- `analyzer`
- `auto_generate_synonyms_phrase_query`
- `boost`
- `default_operator`
- `flags`
- `fuzzy_max_expansions`
- `fuzzy_prefix_length`
- `fuzzy_transpositions`
- `lenient`
- `minimum_should_match`
- `quote_field_suffix`

參數說明與支援的值請參閱 `simple_query_string` 查詢的[文件]({{site.url}}{{site.baseurl}}/query-dsl/full-text/simple-query-string/)。

### 在 SQL 與 PPL 查詢中使用 `simple_query_string` 的*範例*：

REST API 搜尋請求
```json
GET accounts/_search
{
  "query": {
    "simple_query_string": {
      "query": "Lane Street",
      "fields": [ "address" ],
    }
  }
}
```
{% include copy-curl.html %}

可以從 *SQL* 呼叫
```sql
SELECT account_number, address
FROM accounts
WHERE simple_query_string(['address'], 'Lane Street', default_operator='OR')
```
{% include copy.html %}


或從 *PPL* 呼叫
```sql
SOURCE=accounts | WHERE simple_query_string(['address'], 'Lane Street', default_operator='OR') | fields account_number, address
```
{% include copy.html %}


查詢會傳回下列結果：

<!-- vale off -->

| account_number | address
:--- | :---
1 | 880 Holmes Lane
6 | 671 Bristol Street
13 | 789 Madison Street

<!-- vale on -->

## 片語前綴比對

若要依指定前綴搜尋片語，請使用 `MATCH_PHRASE_PREFIX` 函式，對查詢字串中的最後一個詞彙建立前綴查詢。

### 語法

```sql
match_phrase_prefix(field_expression, query_expression[, option=<option_value>]*)
```

`MATCH_PHRASE_PREFIX` 函式可讓您以任意順序指定下列選項：

- `analyzer`
- `slop`
- `max_expansions`
- `zero_terms_query`
- `boost`

參數說明與支援的值請參閱 `match_phrase_prefix` 查詢的[文件]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase-prefix/)。

### 在 SQL 與 PPL 查詢中使用 `match_phrase_prefix` 的*範例*：

REST API 搜尋請求
```json
GET accounts/_search
{
  "query": {
    "match_phrase_prefix": {
      "author": {
        "query": "Alexander Mil"
      }
    }
  }
}
```
{% include copy-curl.html %}

可以從 *SQL* 呼叫
```sql
SELECT author, title
FROM books
WHERE match_phrase_prefix(author, 'Alexander Mil')
```
{% include copy.html %}


或從 *PPL* 呼叫
```sql
source=books | where match_phrase_prefix(author, 'Alexander Mil') | fields author, title
```
{% include copy.html %}


查詢會傳回下列結果：

<!-- vale off -->

| author | title
:--- | :---
Alan Alexander Milne | The House at Pooh Corner
Alan Alexander Milne | Winnie-the-Pooh

<!-- vale on -->


## 布林前綴比對

使用 `match_bool_prefix` 函式，在指定欄位中搜尋符合文字前綴的文件。

### 語法

```sql
match_bool_prefix(field_expression, query_expression[, option=<option_value>]*)
```

`MATCH_BOOL_PREFIX` 函式可讓您以任意順序指定下列選項：

- `minimum_should_match`
- `fuzziness`
- `prefix_length`
- `max_expansions`
- `fuzzy_transpositions`
- `fuzzy_rewrite`
- `boost`
- `analyzer`
- `operator`

參數說明與支援的值請參閱 `match_bool_prefix` 查詢的[文件]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-bool-prefix/)。

### 在 SQL 與 PPL 查詢中使用 `match_bool_prefix` 的範例：

REST API 搜尋請求
```json
GET accounts/_search
{
  "query": {
    "match_bool_prefix": {
      "address": {
        "query": "Bristol Stre"
      }
    }
  }
}
```
{% include copy-curl.html %}

可以從 *SQL* 呼叫
```sql
SELECT firstname, address
FROM accounts
WHERE match_bool_prefix(address, 'Bristol Stre')
```
{% include copy.html %}


或從 *PPL* 呼叫
```sql
source=accounts | where match_bool_prefix(address, 'Bristol Stre') | fields firstname, address
```
{% include copy.html %}


查詢會傳回下列結果：

<!-- vale off -->

| firstname | address
:--- | :---
Hattie | 671 Bristol Street
Nanette | 789 Madison Street

<!-- vale on -->
