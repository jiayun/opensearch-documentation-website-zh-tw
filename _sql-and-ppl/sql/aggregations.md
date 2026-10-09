---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "彙總函式"
parent: SQL
nav_order: 11
redirect_from:
  - /search-plugins/sql/aggregations/
  - /search-plugins/sql/sql/aggregations/
---

# SQL 彙總函式

彙總函式會對 `GROUP BY` 子句定義的子集進行運算。若沒有 `GROUP BY` 子句，彙總函式會對結果集中的所有元素進行運算。您可以在 `GROUP BY`、`SELECT` 和 `HAVING` 子句中使用彙總函式。

OpenSearch 支援下列彙總函式。

<!-- vale off -->

函式 | 說明
:--- | :---
`AVG` | 傳回結果的平均值。
`COUNT` | 傳回結果的數量。
`SUM` | 傳回結果的總和。
`MIN` | 傳回結果的最小值。
`MAX` | 傳回結果的最大值。
`VAR_POP` 或 `VARIANCE` | 捨棄 null 值後，傳回結果的母體變異數。當結果只有一列時，傳回 0。
`VAR_SAMP` | 捨棄 null 值後，傳回結果的樣本變異數。當結果只有一列時，傳回 null。
`STD` 或 `STDDEV` | 傳回結果的樣本標準差。當結果只有一列時，傳回 0。
`STDDEV_POP` | 傳回結果的母體標準差。當結果只有一列時，傳回 0。
`STDDEV_SAMP` | 傳回結果的樣本標準差。當結果只有一列時，傳回 null。

<!-- vale on -->

下列範例參照 `employees` 資料表。您可以使用批次編製索引作業，將下列文件編製索引至 OpenSearch，以試用這些範例：

```json
PUT employees/_bulk?refresh
{"index":{"_id":"1"}}
{"employee_id": 1, "department":1, "firstname":"Amber", "lastname":"Duke", "sales":1356, "sale_date":"2020-01-23"}
{"index":{"_id":"2"}}
{"employee_id": 1, "department":1, "firstname":"Amber", "lastname":"Duke", "sales":39224, "sale_date":"2021-01-06"}
{"index":{"_id":"6"}}
{"employee_id":6, "department":1, "firstname":"Hattie", "lastname":"Bond", "sales":5686, "sale_date":"2021-06-07"}
{"index":{"_id":"7"}}
{"employee_id":6, "department":1, "firstname":"Hattie", "lastname":"Bond", "sales":12432, "sale_date":"2022-05-18"}
{"index":{"_id":"13"}}
{"employee_id":13,"department":2, "firstname":"Nanette", "lastname":"Bates", "sales":32838, "sale_date":"2022-04-11"}
{"index":{"_id":"18"}}
{"employee_id":18,"department":2, "firstname":"Dale", "lastname":"Adams", "sales":4180, "sale_date":"2022-11-05"}
```
{% include copy-curl.html %}

## GROUP BY

`GROUP BY` 子句定義結果集的子集。彙總函式會對這些子集進行運算，並為每個子集傳回一列結果。 

您可以在 `GROUP BY` 子句中使用識別字、序數或運算式。

### 在 GROUP BY 中使用識別字

您可以在 `GROUP BY` 子句中指定要進行彙總的欄位名稱（資料行名稱）。例如，下列查詢會傳回各部門的部門編號與銷售總額： 
```sql
SELECT department, sum(sales)
FROM employees
GROUP BY department;
```
{% include copy.html %}


<!-- vale off -->

| department | sum(sales)
:--- | :---
1 | 58700  |
2 | 37018 |

<!-- vale on -->

### 在 GROUP BY 中使用序數

您可以在 `GROUP BY` 子句中指定要進行彙總的資料行編號。資料行編號取決於資料行在 `SELECT` 子句中的位置。例如，下列查詢等同於前一個查詢。它會傳回各部門的部門編號與銷售總額。它會依結果集的第一個資料行（即 `department`）將結果分組：

```sql
SELECT department, sum(sales)
FROM employees
GROUP BY 1;
```
{% include copy.html %}


<!-- vale off -->

| department | sum(sales)
:--- | :---
1 | 58700  |
2 | 37018 |

<!-- vale on -->

### 在 GROUP BY 中使用運算式

您可以在 `GROUP BY` 子句中使用運算式。例如，下列查詢會傳回各年的平均銷售額：

```sql
SELECT year(sale_date), avg(sales)
FROM employees
GROUP BY year(sale_date);
```
{% include copy.html %}


<!-- vale off -->

| year(start_date) | avg(sales)
:--- | :---
| 2020  | 1356.0 |
| 2021 | 22455.0 |
| 2022 | 16484.0  |

<!-- vale on -->

## SELECT

您可以在 `SELECT` 子句中直接使用彙總運算式，或將其作為較大運算式的一部分。此外，您可以使用運算式作為彙總函式的引數。

### 在 SELECT 中直接使用彙總運算式

下列查詢會傳回各部門的平均銷售額：

```sql
SELECT department, avg(sales)
FROM employees
GROUP BY department;
```
{% include copy.html %}


<!-- vale off -->

| department | avg(sales)
:--- | :---
1 | 14675.0 |
2 | 18509.0 |

<!-- vale on -->

### 在 SELECT 中將彙總運算式作為較大運算式的一部分

下列查詢會以平均銷售額的 5% 計算各部門員工的平均佣金：

```sql
SELECT department, avg(sales) * 0.05 as avg_commission
FROM employees
GROUP BY department;
```
{% include copy.html %}


<!-- vale off -->

| department | avg_commission
:--- | :---
1 | 733.75 |
2 | 925.45 |

<!-- vale on -->

### 使用運算式作為彙總函式的引數

下列查詢會計算各部門的平均佣金金額。它先針對每個 `sales` 值，以 `sales` 的 5% 計算佣金金額。接著計算所有佣金值的平均值：

```sql
SELECT department, avg(sales * 0.05) as avg_commission
FROM employees
GROUP BY department;
```
{% include copy.html %}


<!-- vale off -->

| department | avg_commission
:--- | :---
1 | 733.75 |
2 | 925.45 |

<!-- vale on -->

### COUNT

`COUNT` 函式接受引數（例如 `*`）或常值（例如 `1`）。
下表說明各種形式的 `COUNT` 函式如何運作。

<!-- vale off -->

| 函式類型 | 說明
`COUNT(field)` | 計算指定欄位（或運算式）的值不是 null 的列數。
`COUNT(*)` | 計算資料表中的總列數。
`COUNT(1)`（與 `COUNT(*)` 相同） | 計算任何非 null 常值的數量。

<!-- vale on -->

例如，下列查詢會傳回各年的銷售筆數：

```sql
SELECT year(sale_date), count(sales)
FROM employees
GROUP BY year(sale_date);
```
{% include copy.html %}


<!-- vale off -->

| year(sale_date) | count(sales)
:--- | :---
2020 | 1
2021 | 2
2022 | 3

<!-- vale on -->

## HAVING

`WHERE` 和 `HAVING` 都用於篩選結果。`WHERE` 篩選會在 `GROUP BY` 階段之前套用，因此您無法在 `WHERE` 子句中使用彙總函式。不過，您可以使用 `WHERE` 子句限制後續套用彙總的列。

`HAVING` 篩選會在 `GROUP BY` 階段之後套用，因此您可以使用 `HAVING` 子句限制結果中包含的群組。 

### 搭配 GROUP BY 使用 HAVING

您可以在 `HAVING` 條件中使用彙總運算式，或使用其在 `SELECT` 子句中定義的別名。

下列查詢在 `HAVING` 子句中使用彙總運算式。它會傳回銷售超過一筆的各位員工的銷售筆數：

```sql
SELECT employee_id, count(sales)
FROM employees
GROUP BY employee_id
HAVING count(sales) > 1;
```
{% include copy.html %}


<!-- vale off -->

| employee_id | count(sales)
:--- | :---
1 | 2 |
6 | 2

<!-- vale on -->

`HAVING` 子句中的彙總不必與 `SELECT` 清單中的彙總相同。下列查詢在 `HAVING` 子句中使用 `count` 函式，而在 `SELECT` 子句中使用 `sum` 函式。它會傳回銷售超過一筆的各位員工的銷售總額：

```sql
SELECT employee_id, sum(sales)
FROM employees
GROUP BY employee_id
HAVING count(sales) > 1;
```
{% include copy.html %}


<!-- vale off -->

| employee_id | sum (sales)
:--- | :---
1 | 40580 |
6 | 18120

<!-- vale on -->

作為 SQL 標準的擴充功能，您在 `GROUP BY` 子句中不受限於只能使用識別字。下列查詢在 `GROUP BY` 子句中使用別名，且等同於前一個查詢：

```sql
SELECT employee_id as id, sum(sales)
FROM employees
GROUP BY id
HAVING count(sales) > 1;
```
{% include copy.html %}


<!-- vale off -->

| id | sum (sales)
:--- | :---
1 | 40580 |
6 | 18120

<!-- vale on -->

您也可以在 `HAVING` 子句中使用彙總運算式的別名。下列查詢會傳回銷售額超過 $40,000 的各部門的銷售總額：

```sql
SELECT department, sum(sales) as total
FROM employees
GROUP BY department
HAVING total > 40000;
```
{% include copy.html %}


<!-- vale off -->

| department | total
:--- | :---
1 | 58700 |

<!-- vale on -->

如果識別字有歧義（例如，同時存在於 `SELECT` 別名和索引欄位中），則會優先採用別名。在下列查詢中，識別字會被替換為在 `SELECT` 子句中指定別名的運算式：

```sql
SELECT department, sum(sales) as sales
FROM employees
GROUP BY department
HAVING sales > 40000;
```
{% include copy.html %}


<!-- vale off -->

| department | sales
:--- | :---
1 | 58700 |

<!-- vale on -->

### 不搭配 GROUP BY 使用 HAVING

您可以在沒有 `GROUP BY` 子句的情況下使用 `HAVING` 子句。在此情況下，整個資料集會視為一個群組。如果 `department` 資料行中有超過一個值，下列查詢會傳回 `True`：

```sql
SELECT 'True' as more_than_one_department FROM employees HAVING min(department) < max(department);
```
{% include copy.html %}


<!-- vale off -->

| more_than_one_department |
:--- |
True |

<!-- vale on -->

如果員工資料表中的所有員工都屬於同一個部門，結果將包含零列：

<!-- vale off -->

| more_than_one_department
:--- |
 |

<!-- vale on -->
