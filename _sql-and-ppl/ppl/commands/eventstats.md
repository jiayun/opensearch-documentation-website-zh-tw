---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: eventstats
parent: Commands
grand_parent: PPL
nav_order: 14
---

<!-- vale off -->

# eventstats 命令

<!-- vale on -->

`eventstats` 命令會以計算得出的摘要統計資料來豐富您的事件資料。它會分析事件中指定的欄位，計算各種統計量值，然後將這些結果作為新欄位附加到每個原始事件。

`eventstats` 命令的運作方式如下：

1. 它會對整個搜尋結果或定義的群組執行計算。
2. 原始事件保持不變，並新增欄位來存放統計結果。
3. 此命令對於比較分析、識別離群值，以及為個別事件提供額外脈絡特別有用。

## 比較 stats 命令

如需 `stats`、`eventstats` 與 `streamstats` 命令的完整比較，包括它們在轉換行為、輸出格式、彙總範圍與使用案例上的差異，請參閱[比較 `stats`、`eventstats` 與 `streamstats`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/streamstats/#comparing-stats-eventstats-and-streamstats)。

## 語法

`eventstats` 命令的語法如下：

```sql
eventstats [bucket_nullable=bool] <function>... [by-clause]
```

以下是 `eventstats` 命令語法的範例：

```sql
source = table | eventstats avg(a)
source = table | where a < 50 | eventstats count(c)
source = table | eventstats min(c), max(c) by b
source = table | eventstats count(c) as count_by by b | where count_by > 1000
source = table | eventstats dc(field) as distinct_count
source = table | eventstats distinct_count(category) by region
```

## 參數

`eventstats` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<function>` | 必要 | 彙總函式或視窗函式。 |
| `bucket_nullable` | 選用 | 控制 `eventstats` 命令在 group-by 彙總中是否將 `null` 桶視為有效群組。設為 `false` 時，彙總期間不會將 `null` 的 group-by 值視為不同群組。預設值由 `plugins.ppl.syntax.legacy.preferred` 決定。 |
| `<by-clause>` | 選用 | 依指定的欄位或運算式分組結果。語法：`by [span-expression,] [field,]...` 預設為對整個搜尋結果進行彙總。 |
| `<span-expression>` | 選用 | 依區間將欄位切分為多個桶；最多只能指定一個 span 運算式。語法：`span(field_expr, interval_expr)`。例如，`span(age, 10)` 會建立 10 年為一單位的年齡桶，而 `span(timestamp, 1h)` 會建立每小時的桶。 |

### 時間單位

span 運算式可使用下列時間單位：

* 毫秒 (`ms`)
* 秒 (`s`)
* 分鐘 (`m`，區分大小寫)
* 小時 (`h`)
* 天 (`d`)
* 週 (`w`)
* 月 (`M`，區分大小寫)
* 季 (`q`)
* 年 (`y`)  

## 彙總函式

`eventstats` 命令支援下列彙總函式：

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
* `EARLIEST` -- 依時間戳記取得最早的值
* `LATEST` -- 依時間戳記取得最新的值  

每個函式的詳細說明文件，請參閱[函式]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/functions/aggregations/)。  

## 範例 1：以每個服務的計數豐富記錄檔  

下列查詢會將每個服務的記錄總數新增到每筆記錄項目，讓您在檢視個別記錄詳細資料的同時，也能了解每個服務的活躍程度：
  
```sql
source=otellogs
| eventstats count() as service_total by `resource.attributes.service.name`
| where severityText = 'ERROR'
| sort `resource.attributes.service.name`
| fields severityText, `resource.attributes.service.name`, service_total, body
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name | service_total | body |
| --- | --- | --- | --- |
| ERROR | checkout | 3 | NullPointerException in CheckoutService.placeOrder at line 142 |
| ERROR | checkout | 3 | Kafka producer delivery failed: message too large for topic order-events (max 1048576 bytes) |
| ERROR | frontend-proxy | 3 | [2024-02-01T09:20:00.456Z] "POST /api/checkout HTTP/1.1" 503 - 0 30000 checkout-8d4f7b-mk2p9 |

<!-- vale on -->
  

## 範例 2：依群組計算嚴重性統計  

下列查詢會將每個服務的平均嚴重性與錯誤計數新增到每筆記錄項目：
  
```sql
source=otellogs
| where severityText = 'ERROR'
| eventstats avg(severityNumber) as avg_sev, count() as error_count by `resource.attributes.service.name`
| sort `resource.attributes.service.name`
| fields `resource.attributes.service.name`, severityNumber, avg_sev, error_count
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| resource.attributes.service.name | severityNumber | avg_sev | error_count |
| --- | --- | --- | --- |
| checkout | 17 | 17.0 | 2 |
| checkout | 17 | 17.0 | 2 |
| frontend-proxy | 17 | 17.0 | 1 |
| payment | 17 | 17.0 | 2 |
| payment | 17 | 17.0 | 2 |
| product-catalog | 17 | 17.0 | 1 |
| recommendation | 17 | 17.0 | 1 |

<!-- vale on -->
  

## 範例 3：Null 桶處理

下列查詢使用 `bucket_nullable=false` 從 group-by 彙總中排除 null 值：

```sql
source=otellogs
| eventstats bucket_nullable=false count() as scope_count by instrumentationScope.name
| where severityText = 'ERROR'
| sort `resource.attributes.service.name`
| fields `resource.attributes.service.name`, `instrumentationScope.name`, scope_count
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| resource.attributes.service.name | instrumentationScope.name | scope_count |
| --- | --- | --- |
| checkout | null | null |
| checkout | null | null |
| frontend-proxy | null | null |
| payment | null | null |
| payment | @opentelemetry/instrumentation-http | 2 |
| product-catalog | null | null |
| recommendation | null | null |

<!-- vale on -->
