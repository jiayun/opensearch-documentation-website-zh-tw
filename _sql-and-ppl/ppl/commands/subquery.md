---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: subquery
parent: Commands
grand_parent: PPL
nav_order: 47
---

<!-- vale off -->

# subquery 命令

<!-- vale on -->

`subquery` 命令可讓您將一個 PPL 查詢嵌入另一個查詢中，以進行進階篩選與資料擷取。子查詢會先執行，其結果會由外層查詢用於篩選、比較或聯結。

子查詢的常見使用案例包括：

* 根據另一個查詢的結果篩選資料。
* 檢查相關資料是否存在。
* 執行依賴其他資料表彙總值的計算。
* 建立具有動態條件的複雜聯結。

## 語法

`subquery` 命令的語法如下：

`subquery: [ source=... | ... | ... ]`  

子查詢使用與一般 PPL 查詢相同的語法，但必須以方括號括住。子查詢有四種主要類型：

- [`IN`](#in-subquery)
- [`EXISTS`](#exists-subquery)
- [純量](#scalar-subquery)
- [關聯](#relation-subquery)

### IN 子查詢

測試某個欄位值是否存在於子查詢的結果中：
  
```sql
where <field> [not] in [ source=... | ... | ... ]
```
{% include copy.html %}

以下為 `IN` 子查詢語法的範例：

```sql
source = outer | where a in [ source = inner | fields b ]
source = outer | where (a) in [ source = inner | fields b ]
source = outer | where (a,b,c) in [ source = inner | fields d,e,f ]
source = outer | where a not in [ source = inner | fields b ]
source = outer | where (a) not in [ source = inner | fields b ]
source = outer | where (a,b,c) not in [ source = inner | fields d,e,f ]
source = outer a in [ source = inner | fields b ] // search filtering with subquery
source = outer a not in [ source = inner | fields b ] // search filtering with subquery
source = outer | where a in [ source = inner1 | where b not in [ source = inner2 | fields c ] | fields b ] // nested
source = table1 | inner join left = l right = r on l.a = r.a AND r.a in [ source = inner | fields d ] | fields l.a, r.a, b, c //as join filter
```
{% include copy.html %}
  
### EXISTS 子查詢

測試子查詢是否傳回任何結果：
  
```sql
where [not] exists [ source=... | ... | ... ]
```
{% include copy.html %}

以下為 `EXISTS` 子查詢語法的範例：

```sql
// Assumptions: `a`, `b` are fields of table outer, `c`, `d` are fields of table inner,  `e`, `f` are fields of table nested
source = outer | where exists [ source = inner | where a = c ]
source = outer | where not exists [ source = inner | where a = c ]
source = outer | where exists [ source = inner | where a = c and b = d ]
source = outer | where not exists [ source = inner | where a = c and b = d ]
source = outer exists [ source = inner | where a = c ] // search filtering with subquery
source = outer not exists [ source = inner | where a = c ] // search filtering with subquery
source = table as t1 exists [ source = table as t2 | where t1.a = t2.a ] //table alias is useful in exists subquery
source = outer | where exists [ source = inner1 | where a = c and exists [ source = nested | where c = e ] ] //nested
source = outer | where exists [ source = inner1 | where a = c | where exists [ source = nested | where c = e ] ] //nested
source = outer | where exists [ source = inner | where c > 10 ] //uncorrelated exists
source = outer | where not exists [ source = inner | where c > 10 ] //uncorrelated exists
source = outer | where exists [ source = inner ] | eval l = "nonEmpty" | fields l //special uncorrelated exists
```
{% include copy.html %}
  
### 純量子查詢

傳回單一值，可用於比較或計算：   
  
```sql
where <field> = [ source=... | ... | ... ]
```
{% include copy.html %}

以下為純量子查詢語法的範例：

```sql
//Uncorrelated scalar subquery in Select
source = outer | eval m = [ source = inner | stats max(c) ] | fields m, a
source = outer | eval m = [ source = inner | stats max(c) ] + b | fields m, a
//Uncorrelated scalar subquery in Where**
source = outer | where a > [ source = inner | stats min(c) ] | fields a
//Uncorrelated scalar subquery in Search filter
source = outer a > [ source = inner | stats min(c) ] | fields a
//Correlated scalar subquery in Select
source = outer | eval m = [ source = inner | where outer.b = inner.d | stats max(c) ] | fields m, a
source = outer | eval m = [ source = inner | where b = d | stats max(c) ] | fields m, a
source = outer | eval m = [ source = inner | where outer.b > inner.d | stats max(c) ] | fields m, a
//Correlated scalar subquery in Where
source = outer | where a = [ source = inner | where outer.b = inner.d | stats max(c) ]
source = outer | where a = [ source = inner | where b = d | stats max(c) ]
source = outer | where [ source = inner | where outer.b = inner.d OR inner.d = 1 | stats count() ] > 0 | fields a
//Correlated scalar subquery in Search filter
source = outer a = [ source = inner | where b = d | stats max(c) ]
source = outer [ source = inner | where outer.b = inner.d OR inner.d = 1 | stats count() ] > 0 | fields a
//Nested scalar subquery
source = outer | where a = [ source = inner | stats max(c) | sort c ] OR b = [ source = inner | where c = 1 | stats min(d) | sort d ]
source = outer | where a = [ source = inner | where c =  [ source = nested | stats max(e) by f | sort f ] | stats max(d) by c | sort c | head 1 ]
```
{% include copy.html %}
  
### 關聯子查詢

用於 `join` 作業，以提供動態的右側資料：  
  
```sql
| join ON condition [ source=... | ... | ... ]
```
{% include copy.html %}

以下為關聯子查詢語法的範例：

```sql
source = table1 | join left = l right = r on condition [ source = table2 | where d > 10 | head 5 ] //subquery in join right side
source = [ source = table1 | join left = l right = r [ source = table2 | where d > 10 | head 5 ] | stats count(a) by b ] as outer | head 1
```
{% include copy.html %}

## 組態

`subquery` 命令的行為由 `plugins.ppl.subsearch.maxout` 設定控制，該設定指定子搜尋可傳回的最大資料列數。預設值為 `10000`。若值為 `0`，表示此限制沒有上限。

若要更新此設定，請傳送以下請求：

```json
PUT /_plugins/_query/settings
{
  "persistent": {
    "plugins.ppl.subsearch.maxout": "0"
  }
}
```
{% include copy-curl.html %}
  

## 範例 1：TPC-H q20

以下查詢示範使用巢狀子查詢實作的複雜 TPC-H 查詢 20：

```sql
source = supplier
| join ON s_nationkey = n_nationkey nation
| where n_name = 'CANADA'
  and s_suppkey in [
    source = partsupp
    | where ps_partkey in [
        source = part
        | where like(p_name, 'forest%')
        | fields p_partkey
      ]
      and ps_availqty > [
        source = lineitem
        | where l_partkey = ps_partkey
          and l_suppkey = ps_suppkey
          and l_shipdate >= date('1994-01-01')
          and l_shipdate < date_add(date('1994-01-01'), interval 1 year)
        | stats sum(l_quantity) as sum_l_quantity
        | eval half_sum_l_quantity = 0.5 * sum_l_quantity // Stats and Eval commands can combine when issues/819 resolved
        | fields half_sum_l_quantity
      ]
    | fields ps_suppkey
  ]
```
{% include copy.html %}
  

## 範例 2：TPC-H q22

以下查詢示範使用 `EXISTS` 與純量子查詢實作的 TPC-H 查詢 22：

```sql
source = [
  source = customer
    | where substring(c_phone, 1, 2) in ('13', '31', '23', '29', '30', '18', '17')
      and c_acctbal > [
          source = customer
          | where c_acctbal > 0.00
            and substring(c_phone, 1, 2) in ('13', '31', '23', '29', '30', '18', '17')
          | stats avg(c_acctbal)
        ]
      and not exists [
          source = orders
          | where o_custkey = c_custkey
        ]
    | eval cntrycode = substring(c_phone, 1, 2)
    | fields cntrycode, c_acctbal
  ] as custsale
| stats count() as numcust, sum(c_acctbal) as totacctbal by cntrycode
| sort cntrycode
```
{% include copy.html %}
