---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: timechart
parent: Commands
grand_parent: PPL
nav_order: 49
---

<!-- vale off -->

# timechart 命令

<!-- vale on -->

`timechart` 命令會建立以時間為基礎的資料彙總。它會依時間間隔將資料分組，並可選擇性地依欄位分組，然後對每個群組套用彙總函式。結果以非樞紐格式傳回，每個時間與欄位的組合各佔一列。

## 語法

`timechart` 命令的語法如下：

```sql
timechart [timefield=<field_name>] [span=<time_interval>] [limit=<number>] [useother=<boolean>] [usenull=<boolean>] [nullstr=<string>] <aggregation_function> [by <field>]
```

## 參數

`timechart` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `timefield` | 選用 | 用於依時間分組的欄位。必須是時間戳記欄位。預設為 `@timestamp`。 |
| `span` | 選用 | 指定資料分組的時間間隔。預設為 `1m` (1 分鐘)。如需支援的時間單位完整清單，請參閱[時間單位](#time-units)。 |
| `limit` | 選用 | 指定使用 `by` 子句時要顯示的不同值數量上限。預設為 `10`。當不同值超過上限時，若 `useother` 未設為 `false`，其餘值會被歸入一個 `OTHER` 類別。「最顯著」的不同值是透過計算所有時間間隔的彙總值總和來決定。設為 `0` 可不加限制地顯示所有不同值 (當 `limit=0` 時，`useother` 會自動設為 `false`)。僅在使用 `by` 子句時適用。 |
| `useother` | 選用 | 控制是否為超出 `limit` 的值建立 `OTHER` 類別。設為 `false` 時，只會顯示前 N 個值 (數量由 `limit` 指定)，且不會有 `OTHER` 類別。設為 `true` 時，超出 `limit` 的值會被歸入一個 `OTHER` 類別。此參數僅在使用 `by` 子句且值數量超過 `limit` 時適用。預設為 `true`。 |
| `usenull` | 選用 | 控制是否將 `by` 欄位為 null 值的文件歸入一個獨立的 `NULL` 類別。當 `usenull=false` 時，`by` 欄位為 null 值的文件會從結果中排除。當 `usenull=true` 時，`by` 欄位為 null 值的文件會被歸入一個獨立的 `NULL` 類別。預設為 `true`。 |
| `nullstr` | 選用 | 指定 `by` 欄位為 null 值之文件的類別名稱。此參數僅在 `usenull` 為 `true` 時適用。預設為 `"NULL"`。 |
| `<aggregation_function>` | 必要 | 要套用至每個時間桶的彙總函式。僅支援單一彙總函式。可用函式：[stats]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/stats/) 命令支援的所有彙總函式，以及 timechart 專屬的彙總。 |
| `by` | 選用 | 除了時間間隔之外，再依指定欄位將結果分組。若未指定，則對每個時間間隔內的所有文件執行彙總。 |

## 注意事項

使用 `timechart` 命令時，請注意下列事項：

* `timechart` 命令需要資料中有時間戳記欄位。預設使用 `@timestamp` 欄位，但您可以使用 `timefield` 參數指定其他欄位。  
* 結果以非樞紐格式傳回，每個有資料的時間與欄位組合各佔一列。  
* 只有包含資料的組合才會納入結果---空白組合會被省略，而不會顯示 null 或零值。  
* `limit` 參數的前 N 個值，是依每個不同欄位值在所有時間間隔的值總和來選取。  
* 使用 `limit` 參數時，超出上限的值會被歸入一個 `OTHER` 類別 (除非 `useother=false`)。   
* `by` 欄位為 null 值的文件會被視為一個獨立類別，並在結果中顯示為 null。  

### 時間單位

`span` 參數可使用下列時間單位：

* 毫秒 (`ms`)
* 秒 (`s`)
* 分鐘 (`m`，區分大小寫)
* 小時 (`h`)
* 天 (`d`)
* 週 (`w`)
* 月 (`M`，區分大小寫)
* 季 (`q`)
* 年 (`y`)

## timechart 專屬彙總函式

`timechart` 命令提供專門計算每單位時間數值的速率型彙總函式。

<!-- vale off -->
### per_second
<!-- vale on -->

**用法**：`per_second(field)` 計算每個時間桶內數值欄位的每秒速率。

**計算公式**：`per_second(field) = sum(field) / span_in_seconds`，其中 `span_in_seconds` 為以秒為單位的間隔。

**回傳類型**：DOUBLE

<!-- vale off -->
### per_minute
<!-- vale on -->

**用法**：`per_minute(field)` 計算每個時間桶內數值欄位的每分鐘速率。

**計算公式**：`per_minute(field) = sum(field) * 60 / span_in_seconds`，其中 `span_in_seconds` 為以秒為單位的間隔。

**回傳類型**：DOUBLE

<!-- vale off -->
### per_hour
<!-- vale on -->

**用法**：`per_hour(field)` 計算每個時間桶內數值欄位的每小時速率。

**計算公式**：`per_hour(field) = sum(field) * 3600 / span_in_seconds`，其中 `span_in_seconds` 為以秒為單位的間隔。

**回傳類型**：DOUBLE

<!-- vale off -->
### per_day
<!-- vale on -->

**用法**：`per_day(field)` 計算每個時間桶內數值欄位的每天速率。

**計算公式**：`per_day(field) = sum(field) * 86400 / span_in_seconds`，其中 `span_in_seconds` 為以秒為單位的間隔。

**回傳類型**：DOUBLE
  
## 範例 1：每 5 分鐘的記錄事件數量

下列查詢以 5 分鐘視窗統計所有記錄事件，以監控整體系統活動：

```sql
source=otellogs
| timechart timefield=@timestamp span=5m count()
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| @timestamp | count() |
| --- | --- |
| 2024-02-01 09:10:00 | 5 |
| 2024-02-01 09:15:00 | 5 |
| 2024-02-01 09:20:00 | 5 |
| 2024-02-01 09:25:00 | 5 |

<!-- vale on -->
  

## 範例 2：各服務隨時間變化的錯誤率

下列查詢以 10 分鐘視窗統計各服務的錯誤記錄，以追蹤服務健康狀態：

```sql
source=otellogs
| where severityText = 'ERROR'
| timechart timefield=@timestamp span=10m count() by `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| @timestamp | resource.attributes.service.name | count() |
| --- | --- | --- |
| 2024-02-01 09:10:00 | checkout | 1 |
| 2024-02-01 09:10:00 | payment | 2 |
| 2024-02-01 09:20:00 | checkout | 1 |
| 2024-02-01 09:20:00 | frontend-proxy | 1 |
| 2024-02-01 09:20:00 | product-catalog | 1 |
| 2024-02-01 09:20:00 | recommendation | 1 |

<!-- vale on -->
  

## 範例 3：前 3 大服務，其餘歸入 OTHER

下列查詢將明細限制為依記錄數量排名的前 3 大服務，並將其餘服務歸入 OTHER 類別：

```sql
source=otellogs
| timechart timefield=@timestamp span=15m limit=3 count() by `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| @timestamp | resource.attributes.service.name | count() |
| --- | --- | --- |
| 2024-02-01 09:00:00 | OTHER | 1 |
| 2024-02-01 09:00:00 | cart | 2 |
| 2024-02-01 09:00:00 | frontend | 1 |
| 2024-02-01 09:00:00 | product-catalog | 1 |
| 2024-02-01 09:15:00 | OTHER | 8 |
| 2024-02-01 09:15:00 | cart | 1 |
| 2024-02-01 09:15:00 | frontend | 3 |
| 2024-02-01 09:15:00 | product-catalog | 3 |

<!-- vale on -->
  

## 範例 4：排除 OTHER 類別

下列查詢透過設定 useother=false，只顯示前 2 個服務，且不包含 OTHER 桶：

```sql
source=otellogs
| timechart timefield=@timestamp span=30m limit=2 useother=false count() by `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| @timestamp | resource.attributes.service.name | count() |
| --- | --- | --- |
| 2024-02-01 09:00:00 | frontend | 4 |
| 2024-02-01 09:00:00 | product-catalog | 4 |

<!-- vale on -->
  

## 範例 5：依嚴重性計算每秒錯誤率

下列查詢使用 per_second 速率函式，將不同時間範圍內的錯誤計數標準化，並依嚴重性層級分組：

```sql
source=otellogs
| where severityNumber >= 13
| timechart timefield=@timestamp span=2m per_second(severityNumber) by severityText
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| @timestamp | severityText | per_second(severityNumber) |
| --- | --- | --- |
| 2024-02-01 09:12:00 | ERROR | 0.14166666666666666 |
| 2024-02-01 09:12:00 | WARN | 0.10833333333333334 |
| 2024-02-01 09:14:00 | ERROR | 0.14166666666666666 |
| 2024-02-01 09:16:00 | ERROR | 0.14166666666666666 |
| 2024-02-01 09:18:00 | WARN | 0.10833333333333334 |
| 2024-02-01 09:20:00 | ERROR | 0.14166666666666666 |
| 2024-02-01 09:22:00 | WARN | 0.10833333333333334 |
| 2024-02-01 09:24:00 | ERROR | 0.2833333333333333 |
| 2024-02-01 09:26:00 | WARN | 0.10833333333333334 |
| 2024-02-01 09:28:00 | ERROR | 0.14166666666666666 |

<!-- vale on -->
  
## 範例 6：隨時間變化的不重複服務計數

下列查詢會追蹤每小時有多少個不重複的服務正在主動記錄，可用於偵測服務中斷：

```sql
source=otellogs
| timechart timefield=@timestamp span=1h distinct_count(`resource.attributes.service.name`)
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| @timestamp | distinct_count(`resource.attributes.service.name`) |
| --- | --- |
| 2024-02-01 09:00:00 | 7 |

<!-- vale on -->
  

## 範例 7：搭配 count() 使用 limit=0 以顯示所有值  

此範例使用 `events_many_hosts` 資料集，其中包含 11 個不重複的主機。

若要顯示所有不重複的值而不套用任何限制，請設定 `limit=0`：
  
```sql
source=events_many_hosts
| timechart span=1h limit=0 count() by host
```
{% include copy.html %}
  
所有 11 個主機會以個別資料列的形式傳回，且不含 `OTHER` 類別：
  
<!-- vale off -->

| @timestamp | host | count() |
| --- | --- | --- |
| 2024-07-01 00:00:00 | web-01 | 1 |
| 2024-07-01 00:00:00 | web-02 | 1 |
| 2024-07-01 00:00:00 | web-03 | 1 |
| 2024-07-01 00:00:00 | web-04 | 1 |
| 2024-07-01 00:00:00 | web-05 | 1 |
| 2024-07-01 00:00:00 | web-06 | 1 |
| 2024-07-01 00:00:00 | web-07 | 1 |
| 2024-07-01 00:00:00 | web-08 | 1 |
| 2024-07-01 00:00:00 | web-09 | 1 |
| 2024-07-01 00:00:00 | web-10 | 1 |
| 2024-07-01 00:00:00 | web-11 | 1 |

<!-- vale on -->

## 範例 8：搭配 count() 函式使用 useother=false  

下列查詢透過設定 `useother=false`，將結果限制為前 10 個主機，且不建立 `OTHER` 類別：
  
```sql
source=events_many_hosts
| timechart span=1h useother=false count() by host
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | host | count() |
| --- | --- | --- |
| 2024-07-01 00:00:00 | web-01 | 1 |
| 2024-07-01 00:00:00 | web-02 | 1 |
| 2024-07-01 00:00:00 | web-03 | 1 |
| 2024-07-01 00:00:00 | web-04 | 1 |
| 2024-07-01 00:00:00 | web-05 | 1 |
| 2024-07-01 00:00:00 | web-06 | 1 |
| 2024-07-01 00:00:00 | web-07 | 1 |
| 2024-07-01 00:00:00 | web-08 | 1 |
| 2024-07-01 00:00:00 | web-09 | 1 |
| 2024-07-01 00:00:00 | web-10 | 1 |

<!-- vale on -->
  

<!-- vale off -->

## 範例 9：搭配 useother 參數與 avg() 函式使用 limit 參數  

<!-- vale on -->

下列查詢會依每小時的平均 `cpu_usage` 顯示前 3 個主機。其餘所有主機會分組為 `OTHER` 類別（預設為 `useother=true`）：
  
```sql
source=events_many_hosts
| timechart span=1h limit=3 avg(cpu_usage) by host
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | host | avg(cpu_usage) |
| --- | --- | --- |
| 2024-07-01 00:00:00 | OTHER | 41.3 |
| 2024-07-01 00:00:00 | web-03 | 55.3 |
| 2024-07-01 00:00:00 | web-07 | 48.6 |
| 2024-07-01 00:00:00 | web-09 | 67.8 |

<!-- vale on -->
  
下列查詢會依每小時的平均 `cpu_usage` 顯示前 3 個主機，且透過設定 `useother=false` 不建立 `OTHER` 類別：

```sql
source=events_many_hosts
| timechart span=1h limit=3 useother=false avg(cpu_usage) by host
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | host | avg(cpu_usage) |
| --- | --- | --- |
| 2024-07-01 00:00:00 | web-03 | 55.3 |
| 2024-07-01 00:00:00 | web-07 | 48.6 |
| 2024-07-01 00:00:00 | web-09 | 67.8 |

<!-- vale on -->
  

## 範例 10：處理 by 欄位中的 null 值

下列查詢示範 `by` 欄位中的 null 值如何被視為個別類別：

```sql
source=events_null
| timechart span=1h count() by host
```
{% include copy.html %}
  
`events_null` 資料集包含一筆沒有 `host` 值的項目。由於預設設定為 `usenull=true` 與 `nullstr="NULL"`，此項目會分組為個別的 `NULL` 類別：
  
<!-- vale off -->

| @timestamp | host | count() |
| --- | --- | --- |
| 2024-07-01 00:00:00 | NULL | 1 |
| 2024-07-01 00:00:00 | db-01 | 1 |
| 2024-07-01 00:00:00 | web-01 | 2 |
| 2024-07-01 00:00:00 | web-02 | 2 |

<!-- vale on -->
  

## 範例 11：計算每秒封包速率  

下列查詢使用 `per_second()` 函式，計算網路流量資料的每秒封包速率：
  
```sql
source=events
| timechart span=30m per_second(packets) by host
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | host | per_second(packets) |
| --- | --- | --- |
| 2023-01-01 10:00:00 | server1 | 0.1 |
| 2023-01-01 10:00:00 | server2 | 0.05 |
| 2023-01-01 10:30:00 | server1 | 0.1 |
| 2023-01-01 10:30:00 | server2 | 0.05 |

<!-- vale on -->
  

## 限制

`timechart` 命令有下列限制：

* 每個 `timechart` 命令僅支援單一彙總函式。
* 不支援 `bins` 參數與其他 `bin` 選項。若要控制時間間隔，請使用 `span` 參數。  