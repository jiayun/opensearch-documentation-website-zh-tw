---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "基本查詢"
parent: SQL
nav_order: 5
redirect_from:
  - /search-plugins/sql/basic/
  - /search-plugins/sql/sql/basic/
---


# 基本 SQL 查詢

使用 `SELECT` 子句，搭配 `FROM`、`WHERE`、`GROUP BY`、`HAVING`、`ORDER BY` 與 `LIMIT` 來搜尋及彙總資料。

在這些子句中，`SELECT` 與 `FROM` 是必要的，因為它們指定要擷取哪些欄位，以及從哪些索引擷取。所有其他子句皆為選用，請依需求使用。

## 語法

搜尋及彙總資料的完整語法如下：

```sql
SELECT [DISTINCT] (* | expression) [[AS] alias] [, ...]
FROM index_name
[WHERE predicates]
[GROUP BY expression [, ...]
 [HAVING predicates]]
[ORDER BY expression [IS [NOT] NULL] [ASC | DESC] [, ...]]
[LIMIT [offset, ] size]
```
{% include copy.html %}


## 基本概念

除了 SQL 的預先定義關鍵字之外，最基本的元素是字面值與識別字。
字面值是數值、字串、日期或布林值常數。識別字是 OpenSearch 索引或欄位名稱。
搭配算術運算子與 SQL 函式，即可使用字面值與識別字建立複雜的運算式。

規則 `expressionAtom`：

<!-- vale off -->

![expressionAtom 規則]({{site.url}}{{site.baseurl}}/images/expressionAtom.png)

<!-- vale on -->

運算式接著可與邏輯運算子結合成述詞。在 `WHERE` 與 `HAVING` 子句中使用述詞，即可依特定條件篩選資料。

規則 `expression`：

![expression]({{site.url}}{{site.baseurl}}/images/expression.png)

規則 `predicate`：

![expression]({{site.url}}{{site.baseurl}}/images/predicate.png)

## 執行順序

這些 SQL 子句的執行順序與其出現順序不同：

```sql
FROM index
 WHERE predicates
  GROUP BY expressions
   HAVING predicates
    SELECT expressions
     ORDER BY expressions
      LIMIT size
```
{% include copy.html %}


## SELECT

指定要擷取的欄位。

### 語法

規則 `selectElements`：

<!-- vale off -->

![selectElements 規則]({{site.url}}{{site.baseurl}}/images/selectElements.png)

<!-- vale on -->

規則 `selectElement`：

<!-- vale off -->

![selectElements 規則]({{site.url}}{{site.baseurl}}/images/selectElement.png)

<!-- vale on -->

*範例 1*：使用 `*` 擷取索引中的所有欄位：

```sql
SELECT *
FROM accounts
```
{% include copy.html %}


<!-- vale off -->

| account_number | firstname | gender | city | balance | employer | state | email | address | lastname | age
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---
| 1 | Amber | M | Brogan | 39225 | Pyrami | IL | amberduke@pyrami.com | 880 Holmes Lane | Duke | 32
| 16 | Hattie | M | Dante | 5686 | Netagy | TN | hattiebond@netagy.com | 671 Bristol Street | 	Bond | 36
| 13 | Nanette | F | Nogal | 32838 | Quility | VA | nanettebates@quility.com | 789 Madison Street | Bates | 28
| 18 | Dale | M | Orick | 4180 |  | MD | daleadams@boink.com | 467 Hutchinson Court | Adams | 33

<!-- vale on -->

*範例 2*：使用欄位名稱僅擷取特定欄位：

```sql
SELECT firstname, lastname
FROM accounts
```
{% include copy.html %}


<!-- vale off -->

| firstname | lastname
| :--- | :---
| Amber | Duke
| Hattie | Bond
| Nanette | Bates
| Dale | Adams

<!-- vale on -->

*範例 3*：使用欄位別名代替欄位名稱。欄位別名可讓欄位名稱更易於閱讀：

```sql
SELECT account_number AS num
FROM accounts
```

<!-- vale off -->

| num
:---
| 1
| 6
| 13
| 18

<!-- vale on -->

*範例 4*：使用 `DISTINCT` 子句僅取回唯一的欄位值。您可以指定一或多個欄位名稱：

```sql
SELECT DISTINCT age
FROM accounts
```

<!-- vale off -->

| age
:---
| 28
| 32
| 33
| 36

<!-- vale on -->

## FROM

指定要搜尋的索引。
您可以在 `FROM` 子句中指定子查詢。

### 語法

規則 `tableName`：

<!-- vale off -->

![tableName 規則]({{site.url}}{{site.baseurl}}/images/tableName.png)

<!-- vale on -->

*範例 1*：使用索引別名跨索引查詢。若要瞭解索引別名，請參閱 [索引別名]({{site.url}}{{site.baseurl}}/opensearch/index-alias/)。
在此範例查詢中，`acc` 是 `accounts` 索引的別名：

```sql
SELECT account_number, accounts.age
FROM accounts
```

或

```sql
SELECT account_number, acc.age
FROM accounts acc
```

<!-- vale off -->

| account_number | age
| :--- | :---
| 1 | 32
| 6 | 36
| 13 | 28
| 18 | 33

<!-- vale on -->

*範例 2*：使用索引模式查詢符合特定模式的索引：

```sql
SELECT account_number
FROM account*
```

<!-- vale off -->

| account_number
:---
| 1
| 6
| 13
| 18

<!-- vale on -->

## WHERE

指定條件以篩選結果。

<!-- vale off -->

| 運算子 | 行為
:--- | :---
`=` | 等於。
`<>` | 不等於。
`>` | 大於。
`<` | 小於。
`>=` | 大於或等於。
`<=` | 小於或等於。
`IN` | 指定多個 `OR` 運算子。
`BETWEEN` | 類似範圍查詢。如需範圍查詢的詳細資訊，請參閱 [範圍查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/range/)。
`LIKE` | 用於全文搜尋。如需全文查詢的詳細資訊，請參閱 [全文查詢]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/full-text/index/)。
`IS NULL` | 檢查欄位值是否為 `NULL`。
`IS NOT NULL` | 檢查欄位值是否為 `NOT NULL`。

<!-- vale on -->

將比較運算子 (`=`、`<>`、`>`、`>=`、`<`、`<=`) 與布林運算子 `NOT`、`AND` 或 `OR` 結合，即可建立更複雜的運算式。

*範例 1*：對數字、字串或日期使用比較運算子：

```sql
SELECT account_number
FROM accounts
WHERE account_number = 1
```

<!-- vale off -->

| account_number
| :---
| 1

<!-- vale on -->

*範例 2*：OpenSearch 支援彈性結構描述，因此索引中的文件可能具有不同的欄位。使用 `IS NULL` 或 `IS NOT NULL` 僅擷取缺少的欄位或現有的欄位。OpenSearch 不會區分缺少的欄位與明確設定為 `NULL` 的欄位：

```sql
SELECT account_number, employer
FROM accounts
WHERE employer IS NULL
```

<!-- vale off -->

| account_number | employer
| :--- | :---
| 18 |

<!-- vale on -->

*範例 3*：刪除符合 `WHERE` 子句中述詞的文件：

```sql
DELETE FROM accounts
WHERE age > 30
```

## GROUP BY

將具有相同欄位值的文件分組到桶 (bucket) 中。

*範例 1*：依欄位分組：

```sql
SELECT age
FROM accounts
GROUP BY age
```

<!-- vale off -->

| id | age
:--- | :---
0 | 28
1 | 32
2 | 33
3 | 36

<!-- vale on -->

*範例 2*：依欄位別名分組：

```sql
SELECT account_number AS num
FROM accounts
GROUP BY num
```

<!-- vale off -->

| id | num
:--- | :---
0 | 1
1 | 6
2 | 13
3 | 18

<!-- vale on -->

*範例 4*：在 `GROUP BY` 子句中使用純量函式：

```sql
SELECT ABS(age) AS a
FROM accounts
GROUP BY ABS(age)
```

<!-- vale off -->

| id | a
:--- | :---
0 | 28.0
1 | 32.0
2 | 33.0
3 | 36.0

<!-- vale on -->

## HAVING

使用 `HAVING` 子句，依據彙總函式 (`COUNT`、`AVG`、`SUM`、`MIN` 與 `MAX`) 在每個桶內進行彙總。
`HAVING` 子句會篩選 `GROUP BY` 子句的結果：

*範例 1*：

```sql
SELECT age, MAX(balance)
FROM accounts
GROUP BY age HAVING MIN(balance) > 10000
```

<!-- vale off -->

| id | age | MAX (balance)
:--- | :---
0 | 28 | 32838
1 | 32 | 39225

<!-- vale on -->

## ORDER BY

使用 `ORDER BY` 子句將結果排序成您想要的順序。

*範例 1*：使用 `ORDER BY` 依遞增或遞減順序排序。除了一般欄位名稱之外，也支援使用 `ordinal`、`alias` 或 `scalar` 函式：

```sql
SELECT account_number
FROM accounts
ORDER BY account_number DESC
```

<!-- vale off -->

| account_number
| :---
| 18
| 13
| 6
| 1

<!-- vale on -->

*範例 2*：指定缺少欄位的文件要放在結果的開頭或結尾。OpenSearch 的預設行為是在結尾傳回 null 或缺少的欄位。若要將它們移到非 null 值之前，請使用 `IS NOT NULL` 運算子：

```sql
SELECT employer
FROM accounts
ORDER BY employer IS NOT NULL
```

<!-- vale off -->

| employer
| :---
||
| Netagy
| Pyrami
| Quility

<!-- vale on -->

## LIMIT

指定要擷取的文件數上限。用於防止將大量資料擷取至記憶體。

*範例 1*：若傳入單一引數，該引數會對應至 OpenSearch 中的 `size` 參數，且 `from` 參數會設為 0。

```sql
SELECT account_number
FROM accounts
ORDER BY account_number LIMIT 1
```

<!-- vale off -->

| account_number
| :---
| 1

<!-- vale on -->

*範例 2*：若傳入兩個引數，第一個會對應至 OpenSearch 中的 `from` 參數，第二個對應至 `size` 參數。您可以用它為小型索引進行簡單的分頁，但對大型索引而言效率不彰。
使用 `ORDER BY` 以確保各頁之間的順序一致：

```sql
SELECT account_number
FROM accounts
ORDER BY account_number LIMIT 1, 1
```

<!-- vale off -->

| account_number
| :---
| 6

<!-- vale on -->
