---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "彙總函式"
parent: Functions
grand_parent: PPL
nav_order: 1
---

# 彙總函式

彙總函式會跨多個資料列進行計算，並傳回單一結果值。這些函式會搭配 `stats`、`eventstats` 及 `streamstats` 命令使用，以分析及彙總資料。

下表顯示彙總函式如何處理 `NULL` 及遺漏值。

| 函式 | `null` | 遺漏值 |
| --- | --- | --- |
| `COUNT` | 不計入 | 不計入 |
| `SUM` | 忽略 | 忽略 |
| `AVG` | 忽略 | 忽略 |
| `MAX` | 忽略 | 忽略 |
| `MIN` | 忽略 | 忽略 |
| `FIRST` | 忽略 | 忽略 |
| `LAST` | 忽略 | 忽略 |
| `LIST` | 忽略 | 忽略 |
| `VALUES` | 忽略 | 忽略 |
  
## 函式

PPL 提供下列彙總函式，可用於資料分析與彙總。

### COUNT

**用法**：`COUNT(expr)`、`C(expr)`、`c(expr)`、`count(expr)`

計算所擷取資料列中 `expr` 值的數量。`C()`、`c()` 及 `count()` 可作為 `COUNT()` 的縮寫。若要進行篩選計數，請使用 `eval` 運算式指定篩選條件。

**參數**：

- `expr` (選用)：要計算其值的運算式。

**傳回類型**：`LONG`

#### 範例

```sql
source=accounts
| stats count(), c(), count, c
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| count() | c() | count | c |
| --- | --- | --- | --- |
| 4 | 4 | 4 | 4 |

<!-- vale on -->
  
下列範例只會計算符合特定條件的記錄：

```sql
source=accounts
| stats count(eval(age > 30)) as mature_users
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| mature_users |
| --- |
| 3 |

<!-- vale on -->
  
### SUM

**用法**：`SUM(expr)`

傳回 `expr` 值的總和。

**參數**：

- `expr` (必要)：要加總其值的運算式。

**傳回類型**：與輸入類型相同 (`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE`)

#### 範例

```sql
source=accounts
| stats sum(age) by gender
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| sum(age) | gender |
| --- | --- |
| 28 | F |
| 101 | M |

<!-- vale on -->
  
### AVG

**用法**：`AVG(expr)`

傳回 `expr` 的平均值。

**參數**：

- `expr` (必要)：要計算其平均值的運算式。

**傳回類型**：數值輸入為 `DOUBLE`；`DATE`、`TIME` 或 `TIMESTAMP` 輸入則與輸入類型相同

#### 範例

```sql
source=accounts
| stats avg(age) by gender
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| avg(age) | gender |
| --- | --- |
| 28.0 | F |
| 33.666666666666664 | M |

<!-- vale on -->
  
### MAX

**用法**：`MAX(expr)`

傳回 `expr` 的最大值。對於非數值欄位，此函式會傳回依字母順序排列時最後的值。

**參數**：

- `expr` (必要)：要找出最大值的運算式。

**傳回類型**：與輸入類型相同

#### 範例

```sql
source=accounts
| stats max(age)
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| max(age) |
| --- |
| 36 |

<!-- vale on -->

下列範例會傳回 `firstname` 文字欄位中依字母順序排列時最後的值：

```sql
source=accounts
| stats max(firstname)
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| max(firstname) |
| --- |
| Nanette |

<!-- vale on -->
  
### MIN

**用法**：`MIN(expr)`

傳回 `expr` 的最小值。對於非數值欄位，此函式會傳回依字母順序排列時最前的值。

**參數**：

- `expr` (必要)：要找出最小值的運算式。

**傳回類型**：與輸入類型相同

#### 範例

```sql
source=accounts
| stats min(age)
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| min(age) |
| --- |
| 28 |

<!-- vale on -->

下列範例會傳回 `firstname` 文字欄位中依字母順序排列時最前的值：

```sql
source=accounts
| stats min(firstname)
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| min(firstname) |
| --- |
| Amber |

<!-- vale on -->
  
### VAR_SAMP

**用法**：`VAR_SAMP(expr)`

傳回 `expr` 的樣本變異數。

**參數**：

- `expr` (必要)：要計算樣本變異數的運算式。

**傳回類型**：`DOUBLE`

#### 範例

```sql
source=accounts
| stats var_samp(age)
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| var_samp(age) |
| --- |
| 10.916666666666666 |

<!-- vale on -->
  
### VAR_POP

**用法**：`VAR_POP(expr)`

傳回 `expr` 的母體變異數。

**參數**：

- `expr` (必要)：要計算母體變異數的運算式。

**傳回類型**：`DOUBLE`

#### 範例

```sql
source=accounts
| stats var_pop(age)
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| var_pop(age) |
| --- |
| 8.1875 |

<!-- vale on -->
  
### STDDEV_SAMP

**用法**：`STDDEV_SAMP(expr)`

傳回 `expr` 的樣本標準差。

**參數**：

- `expr` (必要)：要計算樣本標準差的運算式。

**傳回類型**：`DOUBLE`

#### 範例

```sql
source=accounts
| stats stddev_samp(age)
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| stddev_samp(age) |
| --- |
| 3.304037933599835 |

<!-- vale on -->
  
### STDDEV_POP

**用法**：`STDDEV_POP(expr)`

傳回 `expr` 的母體標準差。

**參數**：

- `expr` (必要)：要計算母體標準差的運算式。

**傳回類型**：`DOUBLE`

#### 範例

```sql
source=accounts
| stats stddev_pop(age)
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| stddev_pop(age) |
| --- |
| 2.8613807855648994 |

<!-- vale on -->
  
### DISTINCT_COUNT, DC

**用法**：`DISTINCT_COUNT(expr)`、`DC(expr)`

使用 `HyperLogLog++` 演算法傳回相異值的近似數量。這兩個函式功能相同。如需演算法準確度與精確度控制的詳細資訊，請參閱[控制精確度]({{site.url}}{{site.baseurl}}/aggregations/metric/cardinality/#controlling-precision)。

**參數**：

- `expr` (必要)：要計算相異值數量的運算式。

**傳回類型**：`LONG`

#### 範例

```sql
source=accounts
| stats dc(state) as distinct_states, distinct_count(state) as dc_states_alt by gender
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| distinct_states | dc_states_alt | gender |
| --- | --- | --- |
| 1 | 1 | F |
| 3 | 3 | M |

<!-- vale on -->
  
### DISTINCT_COUNT_APPROX

**用法**：`DISTINCT_COUNT_APPROX(expr)`

使用 `HyperLogLog++` 演算法傳回 `expr` 中相異值的近似數量。

**參數**：

- `expr` (必要)：要計算近似相異值數量的運算式。

**傳回類型**：`LONG`

#### 範例

```sql
source=accounts
| stats distinct_count_approx(gender)
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| distinct_count_approx(gender) |
| --- |
| 2 |

<!-- vale on -->
  
### EARLIEST

**用法**：`EARLIEST(field [, time_field])`

根據時間戳記排序，傳回 `field` 的最早值。

**參數**：

- `field`（必要）：要傳回最早值的欄位。
- `time_field`（選用）：用於時間排序的欄位。若未指定，預設為 `@timestamp`。

**回傳類型**：與輸入欄位類型相同

#### 範例

```sql
source=events
| stats earliest(message) by host
| sort host
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| earliest(message) | host |
| --- | --- |
| Starting up | server1 |
| Initializing | server2 |

<!-- vale on -->

下列範例使用自訂時間欄位取代預設的 `@timestamp` 欄位進行排序：

```sql
source=events
| stats earliest(status, event_time) by category
| sort category
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| earliest(status, event_time) | category |
| --- | --- |
| pending | orders |
| active | users |

<!-- vale on -->
  
### LATEST

**用法**：`LATEST(field [, time_field])`

根據時間戳記排序，傳回 `field` 的最晚值。

**參數**：

- `field`（必要）：要傳回最晚值的欄位。
- `time_field`（選用）：用於時間排序的欄位。若未指定，預設為 `@timestamp`。

**回傳類型**：與輸入欄位類型相同

#### 範例

```sql
source=events
| stats latest(message) by host
| sort host
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| latest(message) | host |
| --- | --- |
| Shutting down | server1 |
| Maintenance mode | server2 |

<!-- vale on -->

下列範例使用自訂時間欄位取代預設的 `@timestamp` 欄位進行排序：

```sql
source=events
| stats latest(status, event_time) by category
| sort category
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| latest(status, event_time) | category |
| --- | --- |
| cancelled | orders |
| inactive | users |

<!-- vale on -->
  
### TAKE

**用法**：`TAKE(field [, size])`

傳回欄位的原始值。此函式不保證傳回值的順序。

**參數**：

- `field`（必要）：要擷取值的文字欄位。
- `size`（選用）：要傳回的值數量。預設為 `10`。

**回傳類型**：`ARRAY`

#### 範例

```sql
source=accounts
| stats take(firstname)
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| take(firstname) |
| --- |
| [Amber,Hattie,Nanette,Dale] |

<!-- vale on -->
  
### PERCENTILE, PERCENTILE_APPROX

**用法**：`PERCENTILE(expr, percent)`、`PERCENTILE_APPROX(expr, percent)`

傳回 `expr` 在指定百分比的近似百分位數值。

**參數**：

- `expr`（必要）：要計算百分位數的運算式。
- `percent`（必要）：介於 `0` 與 `100` 之間的常數數值。

**回傳類型**：與輸入類型相同

從 3.1.0 版開始，百分位數的實作從 `AVLTreeDigest` 切換為 `MergingDigest`。如需更多資訊，請參閱[對應的議題](https://github.com/opensearch-project/OpenSearch/issues/18122)。
{: .note}

#### 範例

```sql
source=accounts
| stats percentile(age, 90) by gender
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| percentile(age, 90) | gender |
| --- | --- |
| 28 | F |
| 36 | M |

<!-- vale on -->
  
#### 百分位數捷徑函式

為方便起見，OpenSearch PPL 為常用的百分位數提供捷徑函式：
- `PERC<percent>(expr)` - 等同於 `PERCENTILE(expr, <percent>)`。
- `P<percent>(expr)` - 等同於 `PERCENTILE(expr, <percent>)`。

支援從 `0` 到 `100` 的整數與小數百分位數（例如 `PERC95`、`P99.5`）：
  
```sql
source=accounts 
| stats perc99.5(age);
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| perc99.5(age) |
| --- |
| 36 |

<!-- vale on -->
  
```sql
source=accounts 
| stats p50(age);
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| p50(age) |
| --- |
| 33 |

<!-- vale on -->
  
### MEDIAN

**用法**：`MEDIAN(expr)`

傳回 `expr` 的中位數（第 50 百分位數）值。這等同於 `PERCENTILE(expr, 50)`。

**參數**：

- `expr`（必要）：要計算中位數的運算式。

**回傳類型**：與輸入類型相同

#### 範例

```sql
source=accounts
| stats median(age)
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| median(age) |
| --- |
| 33 |

<!-- vale on -->
  
### FIRST

**用法**：`FIRST(field)`

根據文件的自然順序，傳回 `field` 的第一個非空值 (null)。若沒有任何記錄存在，或所有記錄在 `field` 上都是 `NULL` 值，則傳回 `NULL`。

**參數**：

- `field`（必要）：要傳回第一個值的欄位。

**回傳類型**：與輸入欄位類型相同

#### 範例

```sql
source=accounts
| stats first(firstname) by gender
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| first(firstname) | gender |
| --- | --- |
| Nanette | F |
| Amber | M |

<!-- vale on -->
  
### LAST

**用法**：`LAST(field)`

根據文件的自然順序，傳回 `field` 的最後一個非空值 (null)。若沒有任何記錄存在，或所有記錄在 `field` 上都是 `NULL` 值，則傳回 `NULL`。

**參數**：

- `field`（必要）：要傳回最後一個值的欄位。

**回傳類型**：與輸入欄位類型相同

#### 範例

```sql
source=accounts
| stats last(firstname) by gender
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| last(firstname) | gender |
| --- | --- |
| Nanette | F |
| Dale | M |

<!-- vale on -->
  
### LIST

**用法**：`LIST(expr)`

將指定運算式的所有值收集到一個陣列中。值會轉換為字串，`NULL` 值會被過濾掉，且重複值會保留。此函式最多傳回 `100` 個值，且不保證順序。

**參數**：

- `expr`（必要）：要收集值的欄位運算式。

**回傳類型**：`ARRAY`

此彙總函式不支援 array、struct 或 object 欄位類型。
{: .note}

#### 範例

下列範例將字串欄位的所有值收集到一個陣列中：

```sql
source=accounts
| stats list(firstname)
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| list(firstname) |
| --- |
| [Amber,Hattie,Nanette,Dale] |

<!-- vale on -->
  
### VALUES

**用法**：`VALUES(expr)`

將指定運算式的所有唯一值收集到一個排序後的陣列中。值會轉換為字串，`NULL` 值會被過濾掉，且重複值會被移除。

**參數**：

- `expr`（必要）：要收集唯一值的運算式。

**回傳類型**：`ARRAY`

> `plugins.ppl.values.max.limit` 設定可控制傳回的唯一值數量上限：
> - 預設值為 0，表示傳回不限數量的值。
> - 將此設定為任何正整數，即可限制唯一值的數量。
{: .note}

<!-- temporarily commented out because the admin section is not ported

* See the [PPL Settings]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/admin/settings#plugins-ppl-values-max-limit) documentation for more details
-->

#### 範例

下列範例將字串欄位中的唯一值收集到排序後的陣列中：

```sql
source=accounts
| stats values(firstname)
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| values(firstname) |
| --- |
| [Amber,Dale,Hattie,Nanette] |

<!-- vale on -->
