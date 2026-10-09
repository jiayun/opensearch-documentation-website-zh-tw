---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "函式"
parent: SQL
nav_order: 7
redirect_from:
  - /search-plugins/sql/functions/
  - /search-plugins/sql/sql/functions/
---

# SQL 函式

SQL 語言支援 SQL 外掛程式的所有[常用函式]({{site.url}}{{site.baseurl}}/sql-and-ppl/functions/)，包括[相關性搜尋]({{site.url}}{{site.baseurl}}/search-plugins/sql/full-text/)，但也引入了幾個函式同義詞，這些同義詞僅在 SQL 中可用。
這些同義詞由 `V1` 引擎提供。如需更多資訊，請參閱[限制]({{site.url}}{{site.baseurl}}/search-plugins/sql/limitation/)。

## 比對查詢

`MATCHQUERY` 與 `MATCH_QUERY` 函式是 [`MATCH`]({{site.url}}{{site.baseurl}}/search-plugins/sql/full-text#match) 相關性函式的同義詞。它們不接受額外的引數，但提供另一種語法。

### 語法

若要使用 `matchquery` 或 `match_query`，請傳入您的搜尋查詢以及要搜尋的欄位名稱：

```sql
match_query(field_expression, query_expression[, option=<option_value>]*)
matchquery(field_expression, query_expression[, option=<option_value>]*)
field_expression = match_query(query_expression[, option=<option_value>]*)
field_expression = matchquery(query_expression[, option=<option_value>]*)
```
{% include copy.html %}


您可以以任意順序指定下列選項：

- `analyzer`
- `boost`

### 範例

您可以使用 `MATCHQUERY` 來取代 `MATCH`：

```sql
SELECT account_number, address
FROM accounts
WHERE MATCHQUERY(address, 'Holmes')
```
{% include copy.html %}


或者，您可以使用 `MATCH_QUERY` 來取代 `MATCH`：

```sql
SELECT account_number, address
FROM accounts
WHERE address = MATCH_QUERY('Holmes')
```
{% include copy.html %}


結果包含 address 含有 "Holmes" 的文件：

<!-- vale off -->

| account_number | address
:--- | :---
1 | 880 Holmes Lane

<!-- vale on -->

## 多重比對

[`MULTI_MATCH`]({{site.url}}{{site.baseurl}}/search-plugins/sql/full-text#multi-match) 有三個同義詞，每個的語法略有不同。它們接受查詢字串以及帶權重的欄位清單，也可以接受其他選用參數。

### 語法

```sql
multimatch('query'=query_expression[, 'fields'=field_expression][, option=<option_value>]*)
multi_match('query'=query_expression[, 'fields'=field_expression][, option=<option_value>]*)
multimatchquery('query'=query_expression[, 'fields'=field_expression][, option=<option_value>]*)
```
{% include copy.html %}


`fields` 參數為選用，可以包含單一欄位或以逗號分隔的清單（不允許空白字元）。每個欄位的權重為選用，指定在欄位名稱之後，應以 `caret` 字元 -- `^` -- 分隔，且不含空白。

### 範例

下列查詢展示多重比對查詢中，單一欄位與欄位清單的 `fields` 參數：

```sql
multi_match('fields' = "Tags^2,Title^3.4,Body,Comments^0.3", ...)
multi_match('fields' = "Title", ...)
```
{% include copy.html %}


您可以以任意順序指定下列選項：

- `analyzer`
- `boost`
- `slop`
- `type`
- `tie_breaker`
- `operator`

## 查詢字串

`QUERY` 函式是 [`QUERY_STRING`]({{site.url}}{{site.baseurl}}/search-plugins/sql/full-text#query-string) 的同義詞。

### 語法

```sql
query('query'=query_expression[, 'fields'=field_expression][, option=<option_value>]*)
```
{% include copy.html %}


`fields` 參數為選用，可以包含單一欄位或以逗號分隔的清單（不允許空白字元）。每個欄位的權重為選用，指定在欄位名稱之後，應以 `caret` 字元 -- `^` -- 分隔，且不含空白。

### 範例

下列查詢展示多重比對查詢中，單一欄位與欄位清單的 `fields` 參數：

```sql
query('fields' = "Tags^2,Title^3.4,Body,Comments^0.3", ...)
query('fields' = "Tags", ...)
```
{% include copy.html %}


您可以以任意順序指定下列選項：

- `analyzer`
- `boost`
- `slop`
- `default_field`

### 在 SQL 與 PPL 查詢中使用 `query_string` 的範例：

以下是 OpenSearch DSL 中的 REST API 搜尋請求範例。

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

上述請求等同於下列 `query` 函式：

```sql
SELECT account_number, address
FROM accounts
WHERE query('address:Lane OR address:Street')
```
{% include copy.html %}


結果包含含有 "Lane" 或 "Street" 的地址：

<!-- vale off -->

| account_number | address
:--- | :---
1 | 880 Holmes Lane
6 | 671 Bristol Street
13 | 789 Madison Street

<!-- vale on -->

## 片語比對

`MATCHPHRASEQUERY` 函式是 [`MATCH_PHRASE`]({{site.url}}{{site.baseurl}}/search-plugins/sql/full-text#query-string) 的同義詞。

### 語法

```sql
matchphrasequery(query_expression, field_expression[, option=<option_value>]*)
```
{% include copy.html %}


您可以以任意順序指定下列選項：

- `analyzer`
- `boost`
- `slop`

## 分數查詢

若要為每個符合的文件傳回相關性分數，請使用 `SCORE`、`SCOREQUERY` 或 `SCORE_QUERY` 函式。

### 語法

`SCORE` 函式需要兩個引數。第一個引數是 [`MATCH_QUERY`](#match-query) 運算式。第二個引數是選用的浮點數，用於提升分數（預設值為 1.0）：

```sql
SCORE(match_query_expression, score)
SCOREQUERY(match_query_expression, score)
SCORE_QUERY(match_query_expression, score)
```
{% include copy.html %}


### 範例

下列範例使用 `SCORE` 函式來提升文件的分數：

```sql
SELECT account_number, address, _score
FROM accounts
WHERE SCORE(MATCH_QUERY(address, 'Lane'), 0.5) OR
  SCORE(MATCH_QUERY(address, 'Street'), 100)
ORDER BY _score
```
{% include copy.html %}


結果包含符合項目及其對應的分數：

<!-- vale off -->

| account_number | address | score
:--- | :--- | :---
1 | 880 Holmes Lane | 0.5
6 | 671 Bristol Street | 100
13 | 789 Madison Street | 100

<!-- vale on -->

## 萬用字元查詢

若要依指定的萬用字元搜尋文件，請使用 `WILDCARDQUERY` 或 `WILDCARD_QUERY` 函式。

### 語法

```sql
wildcardquery(field_expression, query_expression[, boost=<value>])
wildcard_query(field_expression, query_expression[, boost=<value>])
```
{% include copy.html %}


### 範例

下列範例使用萬用字元查詢：

```sql
SELECT account_number, address
FROM accounts
WHERE wildcard_query(address, '*Holmes*');
```
{% include copy.html %}


結果包含符合萬用字元運算式的文件：

<!-- vale off -->

| account_number | address
:--- | :---
1 | 880 Holmes Lane

<!-- vale on -->