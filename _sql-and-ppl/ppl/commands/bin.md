---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: bin
parent: Commands
grand_parent: PPL
nav_order: 8
---

<!-- vale off -->

# bin 命令

<!-- vale on -->

`bin` 命令會將數值分組至等間隔的桶中，適合用於建立直方圖及分析資料分布。此命令接受數值或時間欄位，並產生新欄位，其中的值代表各桶的下限。

## 語法

`bin` 命令的語法如下：

```sql
bin <field> [span=<interval>] [minspan=<interval>] [bins=<count>] [aligntime=(earliest | latest | <time-specifier>)] [start=<value>] [end=<value>]
```

## 參數

`bin` 命令支援下列參數。

| 參數 | 必要／選用 | 說明 |
| --- | --- | --- |
| `<field>` | 必要 | 要分組至桶中的欄位。接受數值或時間欄位。 |
| `span` | 選用 | 每個桶的間隔大小。不可與 `bins` 或 `minspan` 參數一起使用。支援數值、對數（`log10`、`2log10`）及時間間隔。請參閱[時間單位](#time-units)。|
| `minspan` | 選用 | 自動計算間隔時的最小間隔大小。不可與 `span` 或 `bins` 參數一起使用。 |
| `bins` | 選用 | 要建立的等寬桶數量上限。必須介於 `2` 與 `50000` 之間（含上下限）。不可與 `span` 或 `minspan` 參數一起使用。請參閱[時間戳記欄位的 bins 參數](#the-bins-parameter-for-timestamp-fields)。|
| `aligntime` | 選用 | 對齊時間欄位的桶時間。僅適用於時間離散化。有效值為 `earliest`、`latest` 或特定時間。請參閱[對齊選項](#align-time-options)。|
| `start` | 選用 | 間隔範圍的起始值。預設為欄位的最小值。 |
| `end` | 選用 | 間隔範圍的結束值。預設為欄位的最大值。 |

### 時間戳記欄位的 bins 參數

時間戳記欄位的 `bins` 參數有下列要求：

- **必須啟用下推**：將 `plugins.calcite.pushdown.enabled` 設為 `true` 以啟用下推（預設啟用）。若停用下推，請改用 `span` 參數（例如 `bin @timestamp span=5m`）。
- **時間戳記欄位必須用作彙總桶**：分桶後的時間戳記欄位必須包含在 `stats` 彙總中（例如 `source=events | bin @timestamp bins=3 | stats count() by @timestamp`）。不支援在彙總桶以外的時間戳記欄位上使用 `bins`。


### 時間單位

`span` 參數可使用下列時間單位：

* 微秒（`us`）
* 毫秒（`ms`）
* 百分之一秒（`cs`）
* 十分之一秒（`ds`）
* 秒（`s`、`sec`、`secs`、`second` 或 `seconds`）
* 分鐘（`m`、`min`、`mins`、`minute` 或 `minutes`）
* 小時（`h`、`hr`、`hrs`、`hour` 或 `hours`）
* 天（`d`、`day` 或 `days`）
* 月（`M`、`mon`、`month` 或 `months`）

### 時間對齊選項

`aligntime` 參數可使用下列選項：

* `earliest` -- 將桶對齊至資料中最早的時間戳記。
* `latest` -- 將桶對齊至資料中最晚的時間戳記。
* `<time-specifier>` -- 將桶對齊至特定的紀元時間值或時間修飾詞運算式。
  
### 參數行為

指定多個參數時，優先順序為：`span` > `minspan` > `bins` > `start`/`end` > 預設。

### 特殊參數類型

`bin` 命令會對某些參數類型進行下列特殊處理：

* 對數間隔（例如 `log10` 或 `2log10`）會建立對數桶邊界，而非線性桶邊界。
* 以天或月為單位的間隔會自動對齊至日曆邊界，並傳回日期字串（`YYYY-MM-DD`），而非時間戳記。
* `aligntime` 參數僅適用於小於一天的時間間隔（不包括以天或月為單位的間隔）。
* `start` 和 `end` 參數會擴大範圍（絕不縮小範圍），並影響桶寬度的計算。

## 範例 1：記錄資料的回應時間分布

```sql
source=otellogs
| rex field=body "(?<duration>\d+)ms"
| bin duration span=100
| stats count() as request_count by duration
| sort duration
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| request_count | duration |
| --- | --- |
| 17 | null |
| 1 | 0-100 |
| 1 | 30000-30100 |
| 1 | 3200-3300 |

<!-- vale on -->
  

## 範例 2：嚴重性等級分布

```sql
source=otellogs
| bin severityNumber span=5
| stats count() as log_count by severityNumber
| sort severityNumber
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| log_count | severityNumber |
| --- | --- |
| 4 | 10-15 |
| 7 | 15-20 |
| 9 | 5-10 |

<!-- vale on -->
  

## 範例 3：對數間隔（log10）  

```sql
source=accounts
| bin balance span=log10
| fields balance
| head 2
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| balance |
| --- |
| 10000.0-100000.0 |
| 1000.0-10000.0 |

<!-- vale on -->
  

## 範例 4：含係數的對數間隔  

```sql
source=accounts
| bin balance span=2log10
| fields balance
| head 3
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| balance |
| --- |
| 20000.0-200000.0 |
| 2000.0-20000.0 |
| 20000.0-200000.0 |

<!-- vale on -->
  

## 範例 5：bins 參數的基本用法  

```sql
source=time_test
| bin value bins=5
| fields value
| head 3
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| value |
| --- |
| 8000-9000 |
| 7000-8000 |
| 9000-10000 |

<!-- vale on -->
  

## 範例 6：使用 bins 參數的記錄資料量分布

```sql
source=otellogs
| stats count() as volume by `resource.attributes.service.name`
| bin volume bins=4
| stats count() as service_count by volume
| sort volume
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| service_count | volume |
| --- | --- |
| 1 | 1-2 |
| 1 | 2-3 |
| 3 | 3-4 |
| 2 | 4-5 |

<!-- vale on -->
  

## 範例 7：較多的桶數量  

```sql
source=accounts
| bin age bins=21
| fields age, account_number
| head 3
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| age | account_number |
| --- | --- |
| 32-33 | 1 |
| 36-37 | 6 |
| 28-29 | 13 |

<!-- vale on -->
  

<!-- vale off -->

## 範例 8：minspan 的基本用法  

<!-- vale on -->

```sql
source=accounts
| bin age minspan=5
| fields age, account_number
| head 3
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| age | account_number |
| --- | --- |
| 30-40 | 1 |
| 30-40 | 6 |
| 20-30 | 13 |

<!-- vale on -->
  

## 範例 9：較大的 minspan  

```sql
source=accounts
| bin age minspan=101
| fields age
| head 1
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| age |
| --- |
| 0-1000 |

<!-- vale on -->
  

## 範例 10：起始與結束範圍  

```sql
source=accounts
| bin age start=0 end=101
| fields age
| head 1
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| age |
| --- |
| 0-100 |

<!-- vale on -->
  

## 範例 11：較大的結束範圍  

```sql
source=accounts
| bin balance start=0 end=100001
| fields balance
| head 1
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| balance |
| --- |
| 0-100000 |

<!-- vale on -->
  

## 範例 12：搭配 start/end 的間隔  

```sql
source=accounts
| bin age span=1 start=25 end=35
| fields age
| head 6
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| age |
| --- |
| 32-33 |
| 36-37 |
| 28-29 |
| 33-34 |

<!-- vale on -->
  

## 範例 13：小時間隔  

```sql
source=time_test
| bin @timestamp span=1h
| fields @timestamp, value
| head 3
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | value |
| --- | --- |
| 2025-07-28 00:00:00 | 8945 |
| 2025-07-28 01:00:00 | 7623 |
| 2025-07-28 02:00:00 | 9187 |

<!-- vale on -->
  

## 範例 14：分鐘間隔  

```sql
source=time_test
| bin @timestamp span=45minute
| fields @timestamp, value
| head 3
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | value |
| --- | --- |
| 2025-07-28 00:00:00 | 8945 |
| 2025-07-28 01:30:00 | 7623 |
| 2025-07-28 02:15:00 | 9187 |

<!-- vale on -->
  

## 範例 15：秒間隔  

```sql
source=time_test
| bin @timestamp span=30seconds
| fields @timestamp, value
| head 3
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | value |
| --- | --- |
| 2025-07-28 00:15:30 | 8945 |
| 2025-07-28 01:42:00 | 7623 |
| 2025-07-28 02:28:30 | 9187 |

<!-- vale on -->
  

## 範例 16：以天為單位的間隔  

```sql
source=time_test
| bin @timestamp span=7day
| fields @timestamp, value
| head 3
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | value |
| --- | --- |
| 2025-07-24 00:00:00 | 8945 |
| 2025-07-24 00:00:00 | 7623 |
| 2025-07-24 00:00:00 | 9187 |

<!-- vale on -->
  

## 範例 17：使用時間修飾詞對齊時間  

```sql
source=time_test
| bin @timestamp span=2h aligntime='@d+3h'
| fields @timestamp, value
| head 3
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | value |
| --- | --- |
| 2025-07-27 23:00:00 | 8945 |
| 2025-07-28 01:00:00 | 7623 |
| 2025-07-28 01:00:00 | 9187 |

<!-- vale on -->
  

## 範例 18：使用紀元時間戳記對齊時間  

```sql
source=time_test
| bin @timestamp span=2h aligntime=1500000000
| fields @timestamp, value
| head 3
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | value |
| --- | --- |
| 2025-07-27 22:40:00 | 8945 |
| 2025-07-28 00:40:00 | 7623 |
| 2025-07-28 00:40:00 | 9187 |

<!-- vale on -->
  

## 範例 19：預設行為（無參數）  

```sql
source=accounts
| bin age
| fields age, account_number
| head 3
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| age | account_number |
| --- | --- |
| 32.0-33.0 | 1 |
| 36.0-37.0 | 6 |
| 28.0-29.0 | 13 |

<!-- vale on -->
  

## 範例 20：對字串欄位分桶  

```sql
source=accounts
| eval age_str = CAST(age AS STRING)
| bin age_str bins=3
| stats count() by age_str
| sort age_str
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| count() | age_str |
| --- | --- |
| 1 | 20-30 |
| 3 | 30-40 |

<!-- vale on -->
