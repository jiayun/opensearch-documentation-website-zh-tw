---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "子搜尋"
parent: PPL
nav_order: 3
redirect_from:
  - /search-plugins/sql/ppl/subsearch/
---

# PPL 查詢中的子搜尋

這是實驗性功能，不建議在正式環境中使用。若要瞭解此功能的最新進度或提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)上的討論。    
{: .warning}

子搜尋（也稱為子查詢）可讓您在另一個查詢中使用某個查詢的結果。OpenSearch 管線處理語言（PPL）支援四種類型的子搜尋命令： 

- [`in`](#in)
- [`exists`](#exists)
- [`scalar`](#scalar)
- [`relation`](#relation) 

前三個子搜尋命令（`in`、`exists` 和 `scalar`）是運算式，可用於 `where` 命令（`where <boolean expression>`）和搜尋篩選條件（`search source=* <boolean expression>`）。`relation` 子搜尋命令是可用於 `join` 作業的陳述式。

## `in`

`in` 子搜尋可讓您檢查欄位值是否存在於另一個查詢的結果中。當您想根據其他索引或查詢的資料來篩選結果時，這項功能很有用。

### 語法

```sql
where <field> [not] in [ search source=... | ... | ... ]
```
{% include copy.html %}


### 用法

```sql
source = outer | where a in [ source = inner | fields b ]
source = outer | where (a) in [ source = inner | fields b ]
source = outer | where (a,b,c) in [ source = inner | fields d,e,f ]
source = outer | where a not in [ source = inner | fields b ]
source = outer | where (a) not in [ source = inner | fields b ]
source = outer | where (a,b,c) not in [ source = inner | fields d,e,f ]
source = outer a in [ source = inner | fields b ]
source = outer a not in [ source = inner | fields b ]
source = outer | where a in [ source = inner1 | where b not in [ source = inner2 | fields c ] | fields b ] // nested
source = table1 | inner join left = l right = r on l.a = r.a AND r.a in [ source = inner | fields d ] | fields l.a, r.a, b, c //as join filter
```
{% include copy.html %}


## `exists`

`exists` 子搜尋會檢查子搜尋查詢是否傳回任何結果。當您想在關聯子查詢中檢查相關記錄是否存在時，這項功能特別有用。

### 語法

```sql
where [not] exists [ search source=... | ... | ... ]
```
{% include copy.html %}


### 用法

以下範例示範實作 `exists` 子搜尋的不同方式，從簡單的彙總比較到複雜的巢狀計算。

這些範例根據下列假設建立： 

- `a` 和 `b` 是資料表 outer 的欄位。
- `c` 和 `d` 是資料表 inner 的欄位。
- `e` 和 `f` 是資料表 nested 的欄位。

#### 關聯

在以下範例中，內層查詢會參照外層查詢的欄位（例如當 a = c 時），在查詢之間建立相依關係。外層查詢的每一列都會執行一次子搜尋求值：


```sql
source = outer | where exists [ source = inner | where a = c ]
source = outer | where not exists [ source = inner | where a = c ]
source = outer | where exists [ source = inner | where a = c and b = d ]
source = outer | where not exists [ source = inner | where a = c and b = d ]
source = outer exists [ source = inner | where a = c ]
source = outer not exists [ source = inner | where a = c ]
source = table as t1 exists [ source = table as t2 | where t1.a = t2.a ]
```
{% include copy.html %}



#### 非關聯

在以下範例中，子搜尋獨立於外層查詢。內層查詢不會參照外層查詢的任何欄位，因此無論外層查詢有多少列，都只會執行一次求值：

```sql
source = outer | where exists [ source = inner | where c > 10 ]
source = outer | where not exists [ source = inner | where c > 10 ]
```
{% include copy.html %}


#### 巢狀

以下範例示範如何將一個子搜尋巢狀置於另一個子搜尋中，建立多層次的複雜查詢。這種方式適用於需要來自不同資料來源的多個條件的複雜篩選情境：

```sql
source = outer | where exists [ source = inner1 | where a = c and exists [ source = nested | where c = e ] ]
source = outer | where exists [ source = inner1 | where a = c | where exists [ source = nested | where c = e ] ]
```
{% include copy.html %}


## `scalar`

`scalar` 子搜尋會傳回單一值，供您在比較或計算中使用。當您需要將欄位與另一個查詢的彙總值進行比較時，這項功能很有用。

### 語法

```sql
where <field> = [ search source=... | ... | ... ]
```
{% include copy.html %}


### 用法

以下範例示範實作 `scalar` 子搜尋的不同方式，從簡單的彙總比較到複雜的巢狀計算。

#### 非關聯

在以下範例中，`scalar` 子搜尋獨立於外層查詢。這些子搜尋會擷取可用於計算或比較的單一值：

```sql
source = outer | eval m = [ source = inner | stats max(c) ] | fields m, a
source = outer | eval m = [ source = inner | stats max(c) ] + b | fields m, a
source = outer | where a > [ source = inner | stats min(c) ] | fields a
source = outer a > [ source = inner | stats min(c) ] | fields a
```
{% include copy.html %}


#### 關聯

在以下範例中，`scalar` 子搜尋會參照外層查詢的欄位，建立相依關係，使內層查詢的結果取決於外層查詢的每一列：

```sql
source = outer | eval m = [ source = inner | where outer.b = inner.d | stats max(c) ] | fields m, a
source = outer | eval m = [ source = inner | where b = d | stats max(c) ] | fields m, a
source = outer | eval m = [ source = inner | where outer.b > inner.d | stats max(c) ] | fields m, a
source = outer | where a = [ source = inner | where outer.b = inner.d | stats max(c) ]
source = outer | where a = [ source = inner | where b = d | stats max(c) ]
source = outer | where [ source = inner | where outer.b = inner.d OR inner.d = 1 | stats count() ] > 0 | fields a
source = outer a = [ source = inner | where b = d | stats max(c) ]
source = outer [ source = inner | where outer.b = inner.d OR inner.d = 1 | stats count() ] > 0 | fields a
```
{% include copy.html %}


#### 巢狀

以下範例示範如何以巢狀方式使用多個 `scalar` 子搜尋，以建立複雜的比較，或在另一個子搜尋中使用某個子搜尋的結果：

```sql
source = outer | where a = [ source = inner | stats max(c) | sort c ] OR b = [ source = inner | where c = 1 | stats min(d) | sort d ]
source = outer | where a = [ source = inner | where c =  [ source = nested | stats max(e) by f | sort f ] | stats max(d) by c | sort c | head 1 ]
```
{% include copy.html %}


## `relation`

`relation` 子搜尋可讓您在聯結作業中將查詢結果用作資料集。當您需要與經過篩選或轉換的資料集聯結，而非直接與靜態索引聯結時，這項功能很有用。

### 語法

```sql
join on <condition> [ search source=... | ... | ... ] [as alias]
```
{% include copy.html %}


### 用法

以下範例示範如何在聯結作業中使用 `relation` 子搜尋。第一個範例示範如何與經過篩選的資料集聯結，第二個範例則示範如何將 `relation` 子搜尋巢狀置於另一個查詢中：

```sql
source = table1 | join left = l right = r on condition [ source = table2 | where d > 10 | head 5 ] //subquery in join right side
source = [ source = table1 | join left = l right = r [ source = table2 | where d > 10 | head 5 ] | stats count(a) by b ] as outer | head 1
```
{% include copy.html %}

          
## 範例

以下範例示範不同子搜尋類型如何在查詢情境中搭配運作，例如多層次查詢或以巢狀方式使用多種子搜尋類型。

### 複雜查詢範例

以下範例示範如何在複雜查詢中結合不同類型的子搜尋。

**範例 1：使用 `in` 和 `scalar` 子搜尋的查詢**

以下查詢同時使用 `in` 和 `scalar` 子搜尋，尋找來自加拿大、供應名稱以「forest」開頭的零件，且可供應數量大於 1994 年訂購總數量一半的供應商：

```sql
source = supplier
| join ON s_nationkey = n_nationkey nation
| where n_name = 'CANADA'
   and s_suppkey in [ /* in subsearch */
     source = partsupp
     | where ps_partkey in [ /* nested in subsearch */
         source = part
         | where like(p_name, 'forest%')
         | fields p_partkey
       ]
       and ps_availqty > [ /* scalar subsearch */
         source = lineitem
         | where l_partkey = ps_partkey
           and l_suppkey = ps_suppkey
           and l_shipdate >= date('1994-01-01')
           and l_shipdate < date_add(date('1994-01-01'), interval 1 year)
         | stats sum(l_quantity) as sum_l_quantity
         | eval half_sum_l_quantity = 0.5 * sum_l_quantity
         | fields half_sum_l_quantity
       ]
     | fields ps_suppkey
```
{% include copy.html %}


**範例 2：使用 `relation`、`scalar` 和 `exists` 子搜尋的查詢**

以下查詢使用 `relation`、`scalar` 和 `exists` 子搜尋，尋找來自特定國家編碼、帳戶餘額高於平均值，且未曾下過任何訂單的客戶：

```sql
source = [  /* relation subsearch */
  source = customer
    | where substring(c_phone, 1, 2) in ('13', '31', '23', '29', '30', '18', '17')
      and c_acctbal > [ /* scalar subsearch */
          source = customer
          | where c_acctbal > 0.00
            and substring(c_phone, 1, 2) in ('13', '31', '23', '29', '30', '18', '17')
          | stats avg(c_acctbal)
        ]
      and not exists [ /* correlated exists subsearch */
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


## 限制

PPL 子搜尋僅在 `plugins.calcite.enabled` 設為 `true` 時才能運作。
