---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: stats
parent: Commands
grand_parent: PPL
nav_order: 45
---

<!-- vale off -->

# stats 命令

<!-- vale on -->

`stats` 命令會計算搜尋結果的彙總。

<!-- vale off -->

## 比較 stats、eventstats 與 streamstats

<!-- vale on -->

如需 `stats`、`eventstats` 與 `streamstats` 命令的完整比較，包括它們在轉換行為、輸出格式、彙總範圍及使用案例上的差異，請參閱[比較 `stats`、`eventstats` 與 `streamstats`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/streamstats/#comparing-stats-eventstats-and-streamstats)。

## 語法

`stats` 命令的語法如下：

```sql
stats [bucket_nullable=bool] <aggregation>... [by-clause]
```

## 參數

`stats` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<aggregation>` | 必要 | 彙總函式。 |
| `<by-clause>` | 選用 | 依指定的欄位或運算式將結果分組。語法：`by [span-expression,] [field,]...` 若未指定 `by-clause`，stats 命令只會傳回一列，也就是對整個搜尋結果進行的彙總。 |
| `bucket_nullable` | 選用 | 控制是否在分組彙總中包含 `null` 桶。當設為 `false` 時，會忽略 `group-by` 欄位為 null 的記錄，因而提升效能。預設值為 `plugins.ppl.syntax.legacy.preferred` 的值。 |
| `<span-expression>` | 選用 | 依間隔將欄位分成多個桶（最多可指定一個 span 運算式）。語法：`span(field_expr, interval_expr)`。依預設，間隔會使用欄位的預設單位。對於日期/時間欄位，彙總結果會忽略 null 值。範例：`span(age, 10)` 會建立以 10 年為單位的年齡桶，`span(timestamp, 1h)` 則會建立以小時為單位的桶。有效的時間單位為毫秒（`ms`）、秒（`s`）、分鐘（`m`）、小時（`h`）、日（`d`）、週（`w`）、月（`M`）、季（`q`）、年（`y`）。 |

## 彙總函式  

`stats` 命令支援下列彙總函式：

* `COUNT`/`C` -- 值的計數
* `SUM` -- 數值的總和
* `AVG` -- 數值的平均值
* `MAX` -- 最大值
* `MIN` -- 最小值
* `VAR_SAMP` -- 樣本變異數
* `VAR_POP` -- 母體變異數
* `STDDEV_SAMP` -- 樣本標準差
* `STDDEV_POP` -- 母體標準差
* `DISTINCT_COUNT_APPROX` -- 近似相異計數
* `TAKE` -- 原始值清單
* `PERCENTILE`/`PERCENTILE_APPROX` -- 百分位數計算
* `PERC<percent>`/`P<percent>` -- 百分位數捷徑函式
* `MEDIAN` -- 第 50 百分位數
* `EARLIEST` -- 依時間戳記的最早值
* `LATEST` -- 依時間戳記的最新值
* `FIRST` -- 第一個非 null 值
* `LAST` -- 最後一個非 null 值
* `LIST` -- 將所有值收集到陣列
* `VALUES` -- 將唯一值收集到已排序陣列  
  
如需每個函式的詳細文件，請參閱[彙總函式]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/functions/aggregations/)。

## 範例 1：計算事件計數  

下列查詢會計算記錄項目的總數，這是記錄匯入的基本健康狀態檢查：
  
```sql
source=otellogs
| stats count() as total_logs
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| total_logs |
| --- |
| 20 |

<!-- vale on -->
  

## 範例 2：計算欄位的平均值  

下列查詢會計算所有記錄的平均嚴重性數值。平均值隨時間上升可能表示系統不穩定性增加：
  
```sql
source=otellogs
| stats avg(severityNumber) as avg_severity
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：

<!-- vale off -->

| avg_severity |
| --- |
| 12.0 |

<!-- vale on -->
  

## 範例 3：依群組計算計數  

下列查詢會依嚴重性層級計算記錄數，讓您一眼就能看出系統健康狀態的細分情形：
  
```sql
source=otellogs
| stats count() as log_count by severityText
| sort - log_count
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| log_count | severityText |
| --- | --- |
| 7 | ERROR |
| 6 | INFO |
| 4 | WARN |
| 3 | DEBUG |

<!-- vale on -->
  

## 範例 4：依群組計算多個彙總  

下列查詢會計算每個服務的記錄總數與嚴重性範圍，協助您找出哪些服務最活躍且問題最多：
  
```sql
source=otellogs
| stats count() as total, min(severityNumber) as min_sev, max(severityNumber) as max_sev by `resource.attributes.service.name`
| sort - total
| head 5
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| total | min_sev | max_sev | resource.attributes.service.name |
| --- | --- | --- | --- |
| 4 | 9 | 9 | frontend |
| 4 | 5 | 17 | product-catalog |
| 3 | 5 | 9 | cart |
| 3 | 9 | 17 | checkout |
| 3 | 13 | 17 | frontend-proxy |

<!-- vale on -->
  

## 範例 5：依 span 計算計數  

下列查詢會將記錄分組為間隔為 10 的嚴重性桶，顯示低（0--9）、中（10--19）與高（20+）嚴重性範圍的分布：
  
```sql
source=otellogs
| stats count() as log_count by span(severityNumber, 10)
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| log_count | span(severityNumber,10) |
| --- | --- |
| 9 | 0 |
| 11 | 10 |

<!-- vale on -->
  

## 範例 6：依欄位與 span 計算計數  

下列查詢會依嚴重性數值範圍計算各嚴重性層級的記錄數，顯示嚴重性文字如何對應到數值範圍：
  
```sql
source=otellogs
| stats count() as cnt by span(severityNumber, 10) as sev_range, severityText
| sort sev_range
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| cnt | sev_range | severityText |
| --- | --- | --- |
| 3 | 0 | DEBUG |
| 6 | 0 | INFO |
| 7 | 10 | ERROR |
| 4 | 10 | WARN |

<!-- vale on -->
  

## 範例 7：計算欄位的相異計數  

下列查詢會計算回報記錄的服務名稱出現總次數，以及相異服務的數量，可用於驗證所有預期的服務都在回報：
  
```sql
source=otellogs
| stats count(`resource.attributes.service.name`) as total_entries, distinct_count(`resource.attributes.service.name`) as unique_services
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| total_entries | unique_services |
| --- | --- |
| 20 | 7 |

<!-- vale on -->
  

## 範例 8：依群組使用 VALUES 收集唯一值  

下列查詢會收集每個嚴重性層級的唯一服務名稱，方便您快速看出各層級有哪些服務受到影響：
  
```sql
source=otellogs
| stats values(`resource.attributes.service.name`) as services by severityText
| sort severityText
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| services | severityText |
| --- | --- |
| [cart,product-catalog] | DEBUG |
| [checkout,frontend-proxy,payment,product-catalog,recommendation] | ERROR |
| [cart,checkout,frontend] | INFO |
| [frontend-proxy,product-catalog] | WARN |

<!-- vale on -->
  

## 範例 9：計算欄位的百分位數  

下列查詢會計算嚴重性數值的第 90 百分位數，協助您了解嚴重性的分布情形：
  
```sql
source=otellogs
| stats percentile(severityNumber, 90) as p90_severity
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| p90_severity |
| --- |
| 17 |

<!-- vale on -->
  

## 範例 10：使用 VALUES 收集不重複的值  

下列查詢會收集記錄檔中出現的所有不重複嚴重性層級：
  
```sql
source=otellogs
| stats values(severityText) as severity_levels
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| severity_levels |
| --- |
| [DEBUG,ERROR,INFO,WARN] |

<!-- vale on -->
  

## 範例 11：忽略 null 桶

下列查詢透過設定 `bucket_nullable=false`，在分組時排除 null 值。當您只想查看具有已定義命名空間的服務時，這會很有用：

```sql
source=otellogs
| stats bucket_nullable=false count() as cnt by instrumentationScope.name
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| cnt | instrumentationScope.name |
| --- | --- |
| 2 | @opentelemetry/instrumentation-http |
| 1 | Microsoft.Extensions.Hosting |
| 1 | go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc |

<!-- vale on -->
  

## 範例 12：依日期跨度分組並處理 null 值  

下列範例使用此範例索引資料：

<!-- vale off -->

| Name | DEPTNO | birthday |
| --- | --- | --- |
| Alice | 1 | 2024-04-21 |
| Bob | 2 | 2025-08-21 |
| Jeff | null | 2025-04-22 |
| Adam | 2 | null |

<!-- vale on -->

下列查詢會依 `birthday` 欄位的年度跨度將資料分組，並自動排除 null 值：

```sql
source=example
| stats count() as cnt by span(birthday, 1y) as year
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| cnt | year |
| --- | --- |
| 1 | 2024-01-01 |
| 2 | 2025-01-01 |

<!-- vale on -->

同時依年度跨度與部門編號分組（預設情況下，結果會包含 null 的 `DEPTNO` 值）：

```sql
source=example
| stats count() as cnt by span(birthday, 1y) as year, DEPTNO
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| cnt | year | DEPTNO |
| --- | --- | --- |
| 1 | 2024-01-01 | 1 |
| 1 | 2025-01-01 | 2 |
| 1 | 2025-01-01 | null |

<!-- vale on -->

使用 `bucket_nullable=false` 從分組中排除 null 的 `DEPTNO` 值：

```sql
source=example
| stats bucket_nullable=false count() as cnt by span(birthday, 1y) as year, DEPTNO
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| cnt | year | DEPTNO |
| --- | --- | --- |
| 1 | 2024-01-01 | 1 |
| 1 | 2025-01-01 | 2 |

<!-- vale on -->
  

## 範例 13：依隱含的 @timestamp 欄位計算計數  

如果您在 `span` 函式中省略 `field` 參數，它會自動使用隱含的 `@timestamp` 欄位：
  
```sql
source=big5
| stats count() by span(1month)
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| count() | span(1month) |
| --- | --- |
| 1 | 2023-01-01 00:00:00 |

<!-- vale on -->

## 限制

下列限制適用於 `stats` 命令。

### 高基數欄位的桶彙總結果可能為近似值

在 OpenSearch 中，`terms` 桶 (bucket) 彙總的 `doc_count` 值可能是近似值。因此，對這些桶執行的任何彙總（例如 `sum` 或 `avg`）也可能是近似值。

例如，下列查詢會擷取前 10 個 URL：

```sql
source=hits
| stats bucket_nullable=false count() as c by URL
| sort - c
| head 10
```
{% include copy.html %}

此查詢在 OpenSearch 中會轉譯為使用 `"order": { "_count": "desc" }` 的 `terms` 彙總。對於高基數欄位，部分桶可能會被捨棄，因此結果可能只是近似值。

### 依 doc_count 遞增排序可能產生不準確的結果

擷取高基數欄位中出現頻率最低的詞彙時，結果可能不準確。分片層級的彙總可能會遺漏全域罕見的詞彙，或錯誤呈現其頻率，導致整體結果出現誤差。

例如，下列查詢會擷取出現頻率最低的 10 個 URL：

```sql
source=hits
| stats bucket_nullable=false count() as c by URL
| sort + c
| head 10
```
{% include copy.html %}

全域罕見的詞彙在每個分片上不一定都顯得罕見，也可能完全未出現在某些分片的結果中。反之，在某個分片上不常見的詞彙，在另一個分片上可能很常見。在這兩種情況下，分片層級的近似計算都可能導致遺漏罕見詞彙，進而造成整體結果不準確。
