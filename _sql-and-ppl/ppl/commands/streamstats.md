---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: streamstats
parent: Commands
grand_parent: PPL
nav_order: 46
---

<!-- vale off -->

# streamstats 命令

<!-- vale on -->

`streamstats` 命令會在事件依序處理時計算累計或滾動統計值。與一次處理整個資料集的 `stats` 或 `eventstats` 不同，`streamstats` 會以漸進方式處理事件，因此適合時間序列與以序列為基礎的分析。

主要功能包括支援 `window` (滑動視窗計算) 與 `current` (是否將目前事件納入計算) 參數，以及識別趨勢或偵測事件序列變化等專門使用情境。  
  
<!-- vale off -->

## 比較 stats、eventstats 與 streamstats

<!-- vale on -->

`stats`、`eventstats` 與 `streamstats` 命令都能產生彙總結果，例如平均值、總和與最大值。但它們的運作方式與產生的結果有所不同。下表摘要說明這些差異。

| 面向 | `stats` | `eventstats` | `streamstats` |
| --- | --- | --- | --- |
| 轉換行為 | 將所有事件轉換為彙總結果表格，失去原始事件結構 | 將彙總結果作為新欄位加入原始事件，不移除事件結構 | 在每個事件流經管線時，將累計 (逐筆計算) 彙總結果加入該事件 |
| 輸出格式 | 輸出僅包含彙總值，不保留原始事件 | 保留原始事件，並加入包含摘要統計值的額外欄位 | 保留原始事件，並加入包含累計總數或累計統計值的額外欄位 |
| 彙總範圍 | 以搜尋中的所有事件為基礎 (或由 `by` 子句定義的群組) | 以所有相關事件為基礎，然後將結果加回群組中的每個事件 | 在處理每個事件時逐步進行計算；可以視窗限定範圍 |
| 使用情境 | 只需要彙總結果時 (例如計數、平均值、總和) | 需要彙總統計值與原始事件資料並用時 | 需要跨事件串流的累計總數或累計統計值時 |  
  
## 語法

`streamstats` 命令的語法如下：

```sql
streamstats [bucket_nullable=bool] [current=<bool>] [window=<int>] [global=<bool>] [reset_before="("<eval-expression>")"] [reset_after="("<eval-expression>")"] <function>... [by-clause]
```

以下是 `streamstats` 命令語法的範例：

```sql
source = table | streamstats avg(a)
source = table | streamstats current = false avg(a)
source = table | streamstats window = 5 sum(b)
source = table | streamstats current = false window = 2 max(a)
source = table | where a < 50 | streamstats count(c)
source = table | streamstats min(c), max(c) by b
source = table | streamstats count(c) as count_by by b | where count_by > 1000
source = table | streamstats dc(field) as distinct_count
source = table | streamstats distinct_count(category) by region
source = table | streamstats current=false window=2 global=false avg(a) by b
source = table | streamstats window=2 reset_before=a>31 avg(b)
source = table | streamstats current=false reset_after=a>31 avg(b) by c
```
{% include copy.html %}

## 參數

`streamstats` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<function>` | 必要 | 彙總函式或視窗函式。 |
| `bucket_nullable` | 選用 | 控制在 group-by 彙總中是否將 null 桶視為有效群組。當為 `false` 時，彙總期間不會將 null 的 group-by 值視為獨立群組。預設為 `plugins.ppl.syntax.legacy.preferred` 的值。 |
| `current` | 選用 | 是否將目前事件納入摘要計算。當為 `true` 時，會納入目前事件；當為 `false` 時，則使用前一個事件的欄位值。預設為 `true`。 |
| `window` | 選用 | 計算統計值時使用的事件數。預設為 `0` (使用所有先前與目前的事件)。 |
| `global` | 選用 | 僅在指定 `window` 時使用。決定使用單一視窗 (`true`)，還是為 `by` 子句定義的每個群組使用個別視窗 (`false`)。當為 `false` 且 `window` 非零時，會為 `by` 子句中指定欄位的每組值使用個別視窗。預設為 `true`。 |
| `reset_before` | 選用 | 當 `eval-expression` 評估為 `true` 時，在 `streamstats` 計算事件的累計指標之前重設所有累積統計值。若與 `window` 搭配使用，視窗也會一併重設。語法：`reset_before="(<eval-expression>)"`。預設為 `false`。 |
| `reset_after` | 選用 | 當 `eval-expression` 評估為 `true` 時，在 `streamstats` 計算事件的累計指標之後重設所有累積統計值。運算式可以參考 `streamstats` 傳回的欄位。若與 `window` 搭配使用，視窗也會一併重設。語法：`reset_after="(<eval-expression>)"`。預設為 `false`。 |
| `<by-clause>` | 選用 | 用於分組的欄位與運算式，包括純量函式與彙總函式。`span` 子句可用來依區間將特定欄位分割成桶。語法：`by [span-expression,] [field,]...` 若未指定，所有事件會作為單一群組處理，並在整個事件串流上計算累計統計值。 |
| `<span-expression>` | 選用 | 依區間將欄位分割成桶 (最多一個)。語法：`span(field_expr, interval_expr)`。預設情況下，區間使用欄位的預設單位。對於日期/時間欄位，彙總結果會忽略 null 值。範例：`span(age, 10)` 會建立以 10 歲為間隔的年齡桶，`span(timestamp, 1h)` 會建立每小時的桶。有效的時間單位為毫秒 (`ms`)、秒 (`s`)、分鐘 (`m`)、小時 (`h`)、天 (`d`)、週 (`w`)、月 (`M`)、季 (`q`)、年 (`y`)。 |


## 彙總函式  

`streamstats` 命令支援下列彙總函式：

* `COUNT` -- 值的計數  
* `SUM` -- 數值的總和  
* `AVG` -- 數值的平均值  
* `MAX` -- 最大值  
* `MIN` -- 最小值  
* `VAR_SAMP` -- 樣本變異數  
* `VAR_POP` -- 母體變異數  
* `STDDEV_SAMP` -- 樣本標準差  
* `STDDEV_POP` -- 母體標準差  
* `DISTINCT_COUNT`/`DC` -- 值的不重複計數  
* `EARLIEST` -- 依時間戳記取得最早值  
* `LATEST` -- 依時間戳記取得最晚值 
  
每個函式的詳細說明文件，請參閱[彙總函式]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/functions/aggregations/)。

## 範例 1：依服務計算錯誤的累計次數  

下列查詢會依服務分組，計算錯誤記錄檔的累計次數。這對於追蹤事故期間錯誤在各服務之間的累積情況很有用：
  
```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| sort `resource.attributes.service.name`
| streamstats count() as running_count by `resource.attributes.service.name`
| fields `resource.attributes.service.name`, severityText, running_count
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| resource.attributes.service.name | severityText | running_count |
| --- | --- | --- |
| checkout | ERROR | 1 |
| checkout | ERROR | 2 |
| frontend-proxy | ERROR | 1 |
| frontend-proxy | WARN | 2 |
| frontend-proxy | WARN | 3 |
| payment | ERROR | 1 |
| payment | ERROR | 2 |
| product-catalog | WARN | 1 |
| product-catalog | WARN | 2 |
| product-catalog | ERROR | 3 |
| recommendation | ERROR | 1 |

<!-- vale on -->
  

## 範例 2：計算滑動視窗內截至前一筆事件的最高嚴重性層級

下列查詢會逐筆計算前 2 筆記錄檔項目（不含目前事件）中的最高嚴重性層級。當嚴重性升高並超出近期模式時，這有助於發出警示：

```sql
source=otellogs
| sort @timestamp
| streamstats current=false window=2 max(severityNumber) as prev_max_severity
| fields @timestamp, severityText, severityNumber, prev_max_severity
| head 6
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| @timestamp | severityText | severityNumber | prev_max_severity |
| --- | --- | --- | --- |
| 2024-02-01 09:10:00 | INFO | 9 | null |
| 2024-02-01 09:11:00 | INFO | 9 | 9 |
| 2024-02-01 09:12:00 | WARN | 13 | 9 |
| 2024-02-01 09:13:00 | ERROR | 17 | 13 |
| 2024-02-01 09:14:00 | DEBUG | 5 | 17 |
| 2024-02-01 09:15:00 | ERROR | 17 | 17 |

<!-- vale on -->
  

## 範例 3：比較全域與群組專屬視窗  

`global` 參數接受下列值：

* `true`：會對所有資料列套用全域視窗，但視窗內的計算仍會遵循 `by` 群組。
* `false`：視窗本身會依群組建立，表示每個群組會取得獨立的視窗。 
  
下列範例使用包含下列資料的範例索引：

<!-- vale off -->

| name | country | state | month | year | age |
| --- | --- | --- | --- | --- | --- |
| Jake | USA | California | 4 | 2023 | 70 |
| Hello | USA | New York | 4 | 2023 | 30 |
| John | Canada | Ontario | 4 | 2023 | 25 |
| Jane | Canada | Quebec | 4 | 2023 | 20 |
| Jim | Canada | B.C | 4 | 2023 | 27 |
| Peter | Canada | B.C | 4 | 2023 | 57 |
| Rick | Canada | B.C | 4 | 2023 | 70 |
| David | USA | Washington | 4 | 2023 | 40 |

<!-- vale on -->

下列範例會依國家計算各帳戶 `age` 的逐筆累計平均值，並使用不同的 `global` 參數。  

當 `global=true` 時，視窗會依輸入順序滑過所有資料列，但彙總仍會依 `country` 計算。滑動視窗大小為 `2`：
  
```sql
source=state_country
| streamstats window=2 global=true avg(age) as running_avg by country
```
{% include copy.html %}
  
因此，在全域計算所有資料列的 `running_avg` 時，`David` 和 `Rick` 會包含在同一個滑動視窗中：
  
<!-- vale off -->

| name | country | state | month | year | age | running_avg |
| --- | --- | --- | --- | --- | --- | --- |
| Jake | USA | California | 4 | 2023 | 70 | 70.0 |
| Hello | USA | New York | 4 | 2023 | 30 | 50.0 |
| John | Canada | Ontario | 4 | 2023 | 25 | 25.0 |
| Jane | Canada | Quebec | 4 | 2023 | 20 | 22.5 |
| Jim | Canada | B.C | 4 | 2023 | 27 | 23.5 |
| Peter | Canada | B.C | 4 | 2023 | 57 | 42.0 |
| Rick | Canada | B.C | 4 | 2023 | 70 | 63.5 |
| David | USA | Washington | 4 | 2023 | 40 | 40.0 |

<!-- vale on -->
  
相對地，當 `global=false` 時，每個 `by` 群組會形成獨立的串流與視窗：

```sql
source=state_country
| streamstats window=2 global=false avg(age) as running_avg by country
```
{% include copy.html %}
  
`David` 和 `Hello` 會為 `USA` 群組形成一個視窗。因此，對於 `David`，`running_avg` 會是 `35.0`，而不是前一個案例中的 `40.0`：
  
<!-- vale off -->

| name | country | state | month | year | age | running_avg |
| --- | --- | --- | --- | --- | --- | --- |
| Jake | USA | California | 4 | 2023 | 70 | 70.0 |
| Hello | USA | New York | 4 | 2023 | 30 | 50.0 |
| John | Canada | Ontario | 4 | 2023 | 25 | 25.0 |
| Jane | Canada | Quebec | 4 | 2023 | 20 | 22.5 |
| Jim | Canada | B.C | 4 | 2023 | 27 | 23.5 |
| Peter | Canada | B.C | 4 | 2023 | 57 | 42.0 |
| Rick | Canada | B.C | 4 | 2023 | 70 | 63.5 |
| David | USA | Washington | 4 | 2023 | 40 | 35.0 |

<!-- vale on -->
  

## 範例 4：有條件地重設統計資料  

下列查詢會依 `country` 計算各帳戶 `age` 的逐筆累計平均值，並套用重設：
  
```sql
source=state_country
| streamstats current=false reset_before=age>34 reset_after=age<25 avg(age) as avg_age by country
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| name | country | state | month | year | age | avg_age |
| --- | --- | --- | --- | --- | --- | --- |
| Jake | USA | California | 4 | 2023 | 70 | null |
| Hello | USA | New York | 4 | 2023 | 30 | 70.0 |
| John | Canada | Ontario | 4 | 2023 | 25 | null |
| Jane | Canada | Quebec | 4 | 2023 | 20 | 25.0 |
| Jim | Canada | B.C | 4 | 2023 | 27 | null |
| Peter | Canada | B.C | 4 | 2023 | 57 | null |
| Rick | Canada | B.C | 4 | 2023 | 70 | null |
| David | USA | Washington | 4 | 2023 | 40 | null |

<!-- vale on -->
  


## 範例 5：Null 桶行為

當 `bucket_nullable=false` 時，null 值會從分組彙總中排除：

```sql
source=accounts
| streamstats bucket_nullable=false count() as cnt by employer
| fields account_number, firstname, employer, cnt
```
{% include copy.html %}
  
`by` 欄位為 `null` 的資料列會從彙總中排除，因此 `Dale` 的 `cnt` 為 `null`：
  
<!-- vale off -->

| account_number | firstname | employer | cnt |
| --- | --- | --- | --- |
| 1 | Amber | Pyrami | 1 |
| 6 | Hattie | Netagy | 1 |
| 13 | Nanette | Quility | 1 |
| 18 | Dale | null | null |

<!-- vale on -->
  
當 `bucket_nullable=true` 時，null 值會視為有效的群組：

```sql
source=accounts
| streamstats bucket_nullable=true count() as cnt by employer
| fields account_number, firstname, employer, cnt
```
{% include copy.html %}
  
因此，`Dale` 的 `cnt` 會包含在內並正常計算：
  
<!-- vale off -->

| account_number | firstname | employer | cnt |
| --- | --- | --- | --- |
| 1 | Amber | Pyrami | 1 |
| 6 | Hattie | Netagy | 1 |
| 13 | Nanette | Quility | 1 |
| 18 | Dale | null | 1 |

<!-- vale on -->
