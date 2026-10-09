---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "日期與時間函式"
parent: Functions
grand_parent: PPL
nav_order: 6
---

# 日期與時間函式  

所有 PPL 日期與時間函式都使用 UTC 時區。輸入與輸出值都會解讀為 UTC。例如，輸入的時間戳記常值如 `'2020-08-26 01:01:01'` 會假設為 UTC，而 `now()` 函式也會以 UTC 傳回目前的日期與時間。

PPL 支援下列日期與時間函式。

## ADDDATE

**用法**：`ADDDATE(date, INTERVAL expr unit)`、`ADDDATE(date, days)`

將間隔或天數加到日期。第一種形式會將間隔加到日期，第二種形式會將指定的整數天數加到日期。如果第一個引數是 `TIME`，則使用今天的日期。如果第一個引數是 `DATE`，則使用午夜的時間。

**參數**：

- `date` (必要)：要修改的日期、時間戳記或時間值。
- `INTERVAL expr unit` (第一種形式為必要)：要加到日期的間隔。
- `days` (第二種形式為必要)：要加入的整數天數。

**傳回類型**：間隔形式為 `TIMESTAMP`；當輸入為 `DATE` 時，整數天數形式為 `DATE`；當輸入為 `TIMESTAMP` 或 `TIME` 時為 `TIMESTAMP`。

同義詞：[`DATE_ADD`](#date_add) (以間隔形式使用時)

### 範例
  
```sql
source=people
| eval `'2020-08-26' + 1h` = ADDDATE(DATE('2020-08-26'), INTERVAL 1 HOUR), `'2020-08-26' + 1` = ADDDATE(DATE('2020-08-26'), 1), `ts '2020-08-26 01:01:01' + 1` = ADDDATE(TIMESTAMP('2020-08-26 01:01:01'), 1)
| fields `'2020-08-26' + 1h`, `'2020-08-26' + 1`, `ts '2020-08-26 01:01:01' + 1`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| '2020-08-26' + 1h | '2020-08-26' + 1 | ts '2020-08-26 01:01:01' + 1 |
| --- | --- | --- |
| 2020-08-26 01:00:00 | 2020-08-27 | 2020-08-27 01:01:01 |

<!-- vale on -->
  
## ADDTIME

**用法**：`ADDTIME(expr1, expr2)`

將第二個運算式加到第一個運算式並傳回結果。如果引數是 `TIME`，則使用今天的日期。如果引數是 `DATE`，則使用午夜的時間。

**參數**：

- `expr1` (必要)：基準日期、時間戳記或時間值。
- `expr2` (必要)：要加到第一個運算式的日期、時間戳記或時間值。

**傳回類型**：當第一個引數是 `DATE` 或 `TIMESTAMP` 時為 `TIMESTAMP`；當第一個引數是 `TIME` 時為 `TIME`。

#### 範例

下列範例顯示將兩個 DATE 值相加：

```sql
source=people
| eval `'2008-12-12' + 0` = ADDTIME(DATE('2008-12-12'), DATE('2008-11-15'))
| fields `'2008-12-12' + 0`
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| '2008-12-12' + 0 |
| --- |
| 2008-12-12 00:00:00 |

<!-- vale on -->

下列範例顯示將 TIME 與 DATE 值相加：

```sql
source=people
| eval `'23:59:59' + 0` = ADDTIME(TIME('23:59:59'), DATE('2004-01-01'))
| fields `'23:59:59' + 0`
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| '23:59:59' + 0 |
| --- |
| 23:59:59 |

<!-- vale on -->

下列範例顯示將 DATE 與 TIME 合併為時間戳記：

```sql
source=people
| eval `'2004-01-01' + '23:59:59'` = ADDTIME(DATE('2004-01-01'), TIME('23:59:59'))
| fields `'2004-01-01' + '23:59:59'`
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| '2004-01-01' + '23:59:59' |
| --- |
| 2004-01-01 23:59:59 |

<!-- vale on -->

下列範例顯示將兩個 TIME 值相加：

```sql
source=people
| eval `'10:20:30' + '00:05:42'` = ADDTIME(TIME('10:20:30'), TIME('00:05:42'))
| fields `'10:20:30' + '00:05:42'`
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| '10:20:30' + '00:05:42' |
| --- |
| 10:26:12 |

<!-- vale on -->

下列範例顯示將兩個 TIMESTAMP 值相加：

```sql
source=people
| eval `'2007-02-28 10:20:30' + '20:40:50'` = ADDTIME(TIMESTAMP('2007-02-28 10:20:30'), TIMESTAMP('2002-03-04 20:40:50'))
| fields `'2007-02-28 10:20:30' + '20:40:50'`
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| '2007-02-28 10:20:30' + '20:40:50' |
| --- |
| 2007-03-01 07:01:20 |

<!-- vale on -->
  
## CONVERT_TZ

**用法**：`CONVERT_TZ(timestamp, from_timezone, to_timezone)`

建構從來源時區轉換為目標時區的本機時間戳記。當三個函式引數中有任何一個無效時會傳回 `NULL`：時間戳記不是 `yyyy-MM-dd HH:mm:ss` 格式、時區不是 `(+/-)HH:mm` 格式、日期無效 (例如 2 月 30 日)，或時區超出 -13:59 到 +14:00 的有效範圍。

**參數**：

- `timestamp` (必要)：要以 `yyyy-MM-dd HH:mm:ss` 格式轉換的時間戳記或字串。
- `from_timezone` (必要)：`(+/-)HH:mm` 格式的來源時區。
- `to_timezone` (必要)：`(+/-)HH:mm` 格式的目標時區。

**傳回類型**：`TIMESTAMP`

#### 範例

```sql
source=people
| eval `convert_tz('2008-05-15 12:00:00','+00:00','+10:00')` = convert_tz('2008-05-15 12:00:00','+00:00','+10:00')
| fields `convert_tz('2008-05-15 12:00:00','+00:00','+10:00')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| convert_tz('2008-05-15 12:00:00','+00:00','+10:00') |
| --- |
| 2008-05-15 22:00:00 |

<!-- vale on -->
  
`convert_tz` 的有效時區範圍是 (-13:59, +14:00) (含端點)。超出此範圍的時區 (例如本範例中的 +15:00) 會傳回 `NULL`：

```sql
source=people
| eval `convert_tz('2008-05-15 12:00:00','+00:00','+15:00')` = convert_tz('2008-05-15 12:00:00','+00:00','+15:00')
| fields `convert_tz('2008-05-15 12:00:00','+00:00','+15:00')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| convert_tz('2008-05-15 12:00:00','+00:00','+15:00') |
| --- |
| null |

<!-- vale on -->

下列範例顯示從正時區轉換為跨越換日線的負時區：

```sql
source=people
| eval `convert_tz('2008-05-15 12:00:00','+03:30','-10:00')` = convert_tz('2008-05-15 12:00:00','+03:30','-10:00')
| fields `convert_tz('2008-05-15 12:00:00','+03:30','-10:00')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| convert_tz('2008-05-15 12:00:00','+03:30','-10:00') |
| --- |
| 2008-05-14 22:30:00 |

<!-- vale on -->
  
`convert_tz` 中需要有效的日期。對於無效的日期 (例如 4 月 31 日，這不是公曆中的日期)，會傳回 `NULL`：

```sql
source=people
| eval `convert_tz('2008-04-31 12:00:00','+03:30','-10:00')` = convert_tz('2008-04-31 12:00:00','+03:30','-10:00')
| fields `convert_tz('2008-04-31 12:00:00','+03:30','-10:00')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| convert_tz('2008-04-31 12:00:00','+03:30','-10:00') |
| --- |
| null |

<!-- vale on -->
  
下列範例顯示 2 月 30 日也會傳回 `NULL`：

```sql
source=people
| eval `convert_tz('2008-02-30 12:00:00','+03:30','-10:00')` = convert_tz('2008-02-30 12:00:00','+03:30','-10:00')
| fields `convert_tz('2008-02-30 12:00:00','+03:30','-10:00')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| convert_tz('2008-02-30 12:00:00','+03:30','-10:00') |
| --- |
| null |

<!-- vale on -->
  
2008 年 2 月 29 日是有效日期，因為該年是閏年：
  
```sql
source=people
| eval `convert_tz('2008-02-29 12:00:00','+03:30','-10:00')` = convert_tz('2008-02-29 12:00:00','+03:30','-10:00')
| fields `convert_tz('2008-02-29 12:00:00','+03:30','-10:00')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| convert_tz('2008-02-29 12:00:00','+03:30','-10:00') |
| --- |
| 2008-02-28 22:30:00 |

<!-- vale on -->
  
下列範例顯示 2007 年 2 月 29 日會傳回 `NULL`，因為 2007 年不是閏年：

```sql
source=people
| eval `convert_tz('2007-02-29 12:00:00','+03:30','-10:00')` = convert_tz('2007-02-29 12:00:00','+03:30','-10:00')
| fields `convert_tz('2007-02-29 12:00:00','+03:30','-10:00')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| convert_tz('2007-02-29 12:00:00','+03:30','-10:00') |
| --- |
| null |

<!-- vale on -->
  
`convert_tz` 的有效時區範圍是 [-13:59, +14:00] (含端點)。超出此範圍的時區 (例如本範例中的 +14:01) 會傳回 `NULL`：
  
```sql
source=people
| eval `convert_tz('2008-02-01 12:00:00','+14:01','+00:00')` = convert_tz('2008-02-01 12:00:00','+14:01','+00:00')
| fields `convert_tz('2008-02-01 12:00:00','+14:01','+00:00')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| convert_tz('2008-02-01 12:00:00','+14:01','+00:00') |
| --- |
| null |

<!-- vale on -->
  
`convert_tz` 的有效時區範圍是 (-13:59, +14:00) (含端點)。在此範圍內的時區 (例如本範例中的 +14:00) 會傳回正確轉換的日期時間物件：
  
```sql
source=people
| eval `convert_tz('2008-02-01 12:00:00','+14:00','+00:00')` = convert_tz('2008-02-01 12:00:00','+14:00','+00:00')
| fields `convert_tz('2008-02-01 12:00:00','+14:00','+00:00')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| convert_tz('2008-02-01 12:00:00','+14:00','+00:00') |
| --- |
| 2008-01-31 22:00:00 |

<!-- vale on -->
  
下列範例顯示 -14:00 (超出有效範圍) 會傳回 `NULL`：

```sql
source=people
| eval `convert_tz('2008-02-01 12:00:00','-14:00','+00:00')` = convert_tz('2008-02-01 12:00:00','-14:00','+00:00')
| fields `convert_tz('2008-02-01 12:00:00','-14:00','+00:00')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| convert_tz('2008-02-01 12:00:00','-14:00','+00:00') |
| --- |
| null |

<!-- vale on -->
  
`convert_tz` 的有效時區範圍是 [-13:59, +14:00] (含端點)。位於範圍下限的時區 (例如 -13:59) 是有效的，並會傳回轉換後的結果：
  
```sql
source=people
| eval `convert_tz('2008-02-01 12:00:00','-13:59','+00:00')` = convert_tz('2008-02-01 12:00:00','-13:59','+00:00')
| fields `convert_tz('2008-02-01 12:00:00','-13:59','+00:00')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| convert_tz('2008-02-01 12:00:00','-13:59','+00:00') |
| --- |
| 2008-02-02 01:59:00 |

<!-- vale on -->
  
## CURDATE

**用法**：`CURDATE()`

以 `YYYY-MM-DD` 格式的值傳回目前日期。此函式會傳回陳述式執行當下的 UTC 目前日期。

**參數**：無

**傳回類型**：`DATE`

### 範例
  
```sql
source=people
| eval `CURDATE()` = CURDATE()
| fields `CURDATE()`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| CURDATE() |
| --- |
| 2025-08-02 |

<!-- vale on -->
  
## CURRENT_DATE

**用法**：`CURRENT_DATE()`

`CURDATE()` 的同義詞。

**參數**：無

**傳回類型**：`DATE`

### 範例
  
```sql
source=people
| eval `CURRENT_DATE()` = CURRENT_DATE()
| fields `CURRENT_DATE()`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| CURRENT_DATE() |
| --- |
| 2025-08-02 |

<!-- vale on -->
  
## CURRENT_TIME

**用法**：`CURRENT_TIME()`

`CURTIME()` 的同義詞。

**參數**：無

**傳回類型**：`TIME`

### 範例
  
```sql
source=people
| eval `CURRENT_TIME()` = CURRENT_TIME()
| fields `CURRENT_TIME()`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| CURRENT_TIME() |
| --- |
| 15:39:05 |

<!-- vale on -->
  
## CURRENT_TIMESTAMP

**用法**：`CURRENT_TIMESTAMP()`

`NOW()` 的同義詞。

**參數**：無

**傳回類型**：`TIMESTAMP`

### 範例
  
```sql
source=people
| eval `CURRENT_TIMESTAMP()` = CURRENT_TIMESTAMP()
| fields `CURRENT_TIMESTAMP()`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| CURRENT_TIMESTAMP() |
| --- |
| 2025-08-02 15:54:19 |

<!-- vale on -->
  
## CURTIME

**用法**：`CURTIME()`

以 UTC 時區、`hh:mm:ss` 格式的值傳回目前時間。`CURTIME()` 會傳回陳述式開始執行的時間，與 [`NOW()`](#now) 相同。

**參數**：無

**傳回類型**：`TIME`

#### 範例

```sql
source=people
| eval `value_1` = CURTIME(), `value_2` = CURTIME()
| fields `value_1`, `value_2`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| value_1 | value_2 |
| --- | --- |
| 15:39:05 | 15:39:05 |

<!-- vale on -->
  
## DATE

**用法**：`DATE(expr)`

從輸入字串 `expr` 建構日期類型。如果引數是日期或時間戳記，則會從運算式中擷取日期值的部分。

**參數**：
- `expr`（必要）：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**傳回類型**：`DATE`

#### 範例

下列範例會從字串中擷取日期：

```sql
source=people
| eval `DATE('2020-08-26')` = DATE('2020-08-26')
| fields `DATE('2020-08-26')`
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| DATE('2020-08-26') |
| --- |
| 2020-08-26 |

<!-- vale on -->

下列範例會從時間戳記中擷取日期：

```sql
source=people
| eval `DATE(TIMESTAMP('2020-08-26 13:49:00'))` = DATE(TIMESTAMP('2020-08-26 13:49:00'))
| fields `DATE(TIMESTAMP('2020-08-26 13:49:00'))`
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| DATE(TIMESTAMP('2020-08-26 13:49:00')) |
| --- |
| 2020-08-26 |

<!-- vale on -->

下列範例會從同時包含日期與時間的字串中擷取日期：

```sql
source=people
| eval `DATE('2020-08-26 13:49')` = DATE('2020-08-26 13:49')
| fields `DATE('2020-08-26 13:49')`
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| DATE('2020-08-26 13:49') |
| --- |
| 2020-08-26 |

<!-- vale on -->
  
## DATE_ADD

**用法**：`DATE_ADD(date, INTERVAL expr unit)`

將間隔 `expr` 加到 `date`。如果第一個引數是 `TIME`，則會使用今天的日期。如果第一個引數是 `DATE`，則會使用午夜時間。

**參數**：
- `date`（必要）：`DATE`、`TIMESTAMP` 或 `TIME` 值。
- `INTERVAL expr unit`（必要）：`INTERVAL` 運算式。

**傳回類型**：`TIMESTAMP`

同義詞：[`ADDDATE`](#adddate)
反義詞：[`DATE_SUB`](#date_sub)

#### 範例
  
```sql
source=people
| eval `'2020-08-26' + 1h` = DATE_ADD(DATE('2020-08-26'), INTERVAL 1 HOUR), `ts '2020-08-26 01:01:01' + 1d` = DATE_ADD(TIMESTAMP('2020-08-26 01:01:01'), INTERVAL 1 DAY)
| fields `'2020-08-26' + 1h`, `ts '2020-08-26 01:01:01' + 1d`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| '2020-08-26' + 1h | ts '2020-08-26 01:01:01' + 1d |
| --- | --- |
| 2020-08-26 01:00:00 | 2020-08-27 01:01:01 |

<!-- vale on -->
  
## DATE_FORMAT

**用法**：`DATE_FORMAT(date, format)`

使用 `format` 引數中的指定符來格式化 `date` 引數。如果提供的是 `TIME` 類型的引數，則使用本機日期。

**參數**：
- `date`（必要）：`STRING`、`DATE`、`TIME` 或 `TIMESTAMP` 值。
- `format`（必要）：包含格式指定符的 `STRING`。

**傳回類型**：`STRING`

下表說明可用的格式指定符。

| 指定符 | 說明 |
| --- | --- |
| `%a` | 星期名稱縮寫（Sun..Sat） |
| `%b` | 月份名稱縮寫（Jan..Dec） |
| `%c` | 月份，數值（0..12） |
| `%D` | 當月日期，附英文序數後綴（0th、1st、2nd、3rd、...） |
| `%d` | 當月日期，數值（00..31） |
| `%e` | 當月日期，數值（0..31） |
| `%f` | 微秒（000000..999999） |
| `%H` | 小時（00..23） |
| `%h` | 小時（01..12） |
| `%I` | 小時（01..12） |
| `%i` | 分鐘，數值（00..59） |
| `%j` | 一年中的第幾天（001..366） |
| `%k` | 小時（0..23） |
| `%l` | 小時（1..12） |
| `%M` | 月份名稱（January..December） |
| `%m` | 月份，數值（00..12） |
| `%p` | AM 或 PM |
| `%r` | 時間，12 小時制（hh:mm:ss 後接 AM 或 PM） |
| `%S` | 秒（00..59） |
| `%s` | 秒（00..59） |
| `%T` | 時間，24 小時制（hh:mm:ss） |
| `%U` | 週（00..53），以星期日為一週的第一天；WEEK() 模式 0 |
| `%u` | 週（00..53），以星期一為一週的第一天；WEEK() 模式 1 |
| `%V` | 週（01..53），以星期日為一週的第一天；WEEK() 模式 2；與 `%X` 搭配使用 |
| `%v` | 週（01..53），以星期一為一週的第一天；WEEK() 模式 3；與 `%x` 搭配使用 |
| `%W` | 星期名稱（Sunday..Saturday） |
| `%w` | 一週中的第幾天（0=星期日..6=星期六） |
| `%X` | 以星期日為一週第一天時該週所屬的年份，數值，四位數；與 `%V` 搭配使用 |
| `%x` | 以星期一為一週第一天時該週所屬的年份，數值，四位數；與 `%v` 搭配使用 |
| `%Y` | 年份，數值，四位數 |
| `%y` | 年份，數值（兩位數） |
| `%%` | 字面 % 字元 |
| `x` | x，適用於 [aydmshiHIMYDSEL] 以外的任何小寫或大寫字母 |

#### 範例
  
```sql
source=people
| eval `DATE_FORMAT('1998-01-31 13:14:15.012345', '%T.%f')` = DATE_FORMAT('1998-01-31 13:14:15.012345', '%T.%f'), `DATE_FORMAT(TIMESTAMP('1998-01-31 13:14:15.012345'), '%Y-%b-%D %r')` = DATE_FORMAT(TIMESTAMP('1998-01-31 13:14:15.012345'), '%Y-%b-%D %r')
| fields `DATE_FORMAT('1998-01-31 13:14:15.012345', '%T.%f')`, `DATE_FORMAT(TIMESTAMP('1998-01-31 13:14:15.012345'), '%Y-%b-%D %r')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| DATE_FORMAT('1998-01-31 13:14:15.012345', '%T.%f') | DATE_FORMAT(TIMESTAMP('1998-01-31 13:14:15.012345'), '%Y-%b-%D %r') |
| --- | --- |
| 13:14:15.012345 | 1998-Jan-31st 01:14:15 PM |

<!-- vale on -->
  
## DATETIME

**用法**：`DATETIME(timestamp)` 或 `DATETIME(date, to_timezone)`

將 `datetime` 轉換為新的時區。

**參數**：
- `timestamp` (必要)：`TIMESTAMP` 或 `STRING` 值。
- `to_timezone` (選用)：`STRING` 時區值。

**傳回類型**：`TIMESTAMP`

#### 範例

下列範例將 `datetime` 轉換為不同的時區：

```sql
source=people
| eval `DATETIME('2004-02-28 23:00:00-10:00', '+10:00')` = DATETIME('2004-02-28 23:00:00-10:00', '+10:00')
| fields `DATETIME('2004-02-28 23:00:00-10:00', '+10:00')`
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| DATETIME('2004-02-28 23:00:00-10:00', '+10:00') |
| --- |
| 2004-02-29 19:00:00 |

<!-- vale on -->

有效的時區範圍為 (-13:59, +14:00)（含端點）。下列範例顯示超出此範圍的時區會傳回 `NULL`：

```sql
source=people
| eval  `DATETIME('2008-01-01 02:00:00', '-14:00')` = DATETIME('2008-01-01 02:00:00', '-14:00')
| fields `DATETIME('2008-01-01 02:00:00', '-14:00')`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| DATETIME('2008-01-01 02:00:00', '-14:00') |
| --- |
| null |

<!-- vale on -->
  
## DATE_SUB

**用法**：`DATE_SUB(date, INTERVAL expr unit)`

從 `date` 減去間隔 `expr`。如果第一個引數為 `TIME`，則使用今天的日期。如果第一個引數為 `DATE`，則使用午夜的時間。

**參數**：
- `date` (必要)：`DATE`、`TIMESTAMP` 或 `TIME` 值。
- `INTERVAL expr unit` (必要)：`INTERVAL` 運算式。

**傳回類型**：`TIMESTAMP`

同義字：[`SUBDATE`](#subdate)
反義字：[`DATE_ADD`](#date_add)

#### 範例
  
```sql
source=people
| eval `'2008-01-02' - 31d` = DATE_SUB(DATE('2008-01-02'), INTERVAL 31 DAY), `ts '2020-08-26 01:01:01' + 1h` = DATE_SUB(TIMESTAMP('2020-08-26 01:01:01'), INTERVAL 1 HOUR)
| fields `'2008-01-02' - 31d`, `ts '2020-08-26 01:01:01' + 1h`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| '2008-01-02' - 31d | ts '2020-08-26 01:01:01' + 1h |
| --- | --- |
| 2007-12-02 00:00:00 | 2020-08-26 00:01:01 |

<!-- vale on -->
  
## DATEDIFF

**用法**：`DATEDIFF(date1, date2)`

計算指定值的日期部分差異。如果第一個引數為 `TIME`，則使用今天的日期。

**參數**：
- `date1` (必要)：`DATE`、`TIMESTAMP` 或 `TIME` 值。
- `date2` (必要)：`DATE`、`TIMESTAMP` 或 `TIME` 值。

**傳回類型**：`LONG`

#### 範例
  
```sql
source=people
| eval `'2000-01-02' - '2000-01-01'` = DATEDIFF(TIMESTAMP('2000-01-02 00:00:00'), TIMESTAMP('2000-01-01 23:59:59')), `'2001-02-01' - '2004-01-01'` = DATEDIFF(DATE('2001-02-01'), TIMESTAMP('2004-01-01 00:00:00')), `today - today` = DATEDIFF(TIME('23:59:59'), TIME('00:00:00'))
| fields `'2000-01-02' - '2000-01-01'`, `'2001-02-01' - '2004-01-01'`, `today - today`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| '2000-01-02' - '2000-01-01' | '2001-02-01' - '2004-01-01' | today - today |
| --- | --- | --- |
| 1 | -1064 | 0 |

<!-- vale on -->
  
## DAY

**用法**：`DAY(date)`

擷取 `date` 的月份中的日，範圍為 1 到 31。

**參數**：
- `date` (必要)：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**傳回類型**：`INTEGER`

同義字：[`DAYOFMONTH`](#dayofmonth)、[`DAY_OF_MONTH`](#day_of_month)

#### 範例
  
```sql
source=people
| eval `DAY(DATE('2020-08-26'))` = DAY(DATE('2020-08-26'))
| fields `DAY(DATE('2020-08-26'))`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| DAY(DATE('2020-08-26')) |
| --- |
| 26 |

<!-- vale on -->
  
## DAYNAME

**用法**：`DAYNAME(date)`

傳回 `date` 的星期名稱。

**參數**：
- `date` (必要)：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**傳回類型**：`STRING`

#### 範例
  
```sql
source=people
| eval `DAYNAME(DATE('2020-08-26'))` = DAYNAME(DATE('2020-08-26'))
| fields `DAYNAME(DATE('2020-08-26'))`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| DAYNAME(DATE('2020-08-26')) |
| --- |
| Wednesday |

<!-- vale on -->
  
## DAYOFMONTH

**用法**：`DAYOFMONTH(date)`

擷取 `date` 的月份中的日，範圍為 1 到 31。

**參數**：
- `date` (必要)：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**傳回類型**：`INTEGER`

同義字：[`DAY`](#day)、[`DAY_OF_MONTH`](#day_of_month)

#### 範例
  
```sql
source=people
| eval `DAYOFMONTH(DATE('2020-08-26'))` = DAYOFMONTH(DATE('2020-08-26'))
| fields `DAYOFMONTH(DATE('2020-08-26'))`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| DAYOFMONTH(DATE('2020-08-26')) |
| --- |
| 26 |

<!-- vale on -->
  
## DAY_OF_MONTH

**用法**：`DAY_OF_MONTH(date)`

擷取 `date` 的月份中的日，範圍為 1 到 31。

**參數**：
- `date` (必要)：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**傳回類型**：`INTEGER`

同義字：[`DAY`](#day)、[`DAYOFMONTH`](#dayofmonth)

#### 範例
  
```sql
source=people
| eval `DAY_OF_MONTH(DATE('2020-08-26'))` = DAY_OF_MONTH(DATE('2020-08-26'))
| fields `DAY_OF_MONTH(DATE('2020-08-26'))`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| DAY_OF_MONTH(DATE('2020-08-26')) |
| --- |
| 26 |

<!-- vale on -->
  
## DAYOFWEEK

**用法**：`DAYOFWEEK(date)`

傳回 `date` 的星期索引 (1 = 星期日、2 = 星期一、...、7 = 星期六)。

**參數**：
- `date` (必要)：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**傳回類型**：`INTEGER`

同義字：[`DAY_OF_WEEK`](#day_of_week)

#### 範例
  
```sql
source=people
| eval `DAYOFWEEK(DATE('2020-08-26'))` = DAYOFWEEK(DATE('2020-08-26'))
| fields `DAYOFWEEK(DATE('2020-08-26'))`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| DAYOFWEEK(DATE('2020-08-26')) |
| --- |
| 4 |

<!-- vale on -->
  
## DAY_OF_WEEK

**用法**：`DAY_OF_WEEK(date)`

傳回 `date` 的星期索引 (1 = 星期日、2 = 星期一、...、7 = 星期六)。

**參數**：
- `date` (必要)：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**傳回類型**：`INTEGER`

同義字：[`DAYOFWEEK`](#dayofweek)

#### 範例
  
```sql
source=people
| eval `DAY_OF_WEEK(DATE('2020-08-26'))` = DAY_OF_WEEK(DATE('2020-08-26'))
| fields `DAY_OF_WEEK(DATE('2020-08-26'))`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| DAY_OF_WEEK(DATE('2020-08-26')) |
| --- |
| 4 |

<!-- vale on -->
  
## DAYOFYEAR

**用法**：`DAYOFYEAR(date)`

傳回 `date` 的一年中的日，範圍為 1 到 366。

**參數**：
- `date` (必要)：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**傳回類型**：`INTEGER`

同義字：[`DAY_OF_YEAR`](#day_of_year)

#### 範例
  
```sql
source=people
| eval `DAYOFYEAR(DATE('2020-08-26'))` = DAYOFYEAR(DATE('2020-08-26'))
| fields `DAYOFYEAR(DATE('2020-08-26'))`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| DAYOFYEAR(DATE('2020-08-26')) |
| --- |
| 239 |

<!-- vale on -->
  
## DAY_OF_YEAR

**用法**：`DAY_OF_YEAR(date)`

傳回 `date` 的一年中的日，範圍為 1 到 366。

**參數**：
- `date` (必要)：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**傳回類型**：`INTEGER`

同義字：[`DAYOFYEAR`](#dayofyear)

#### 範例
  
```sql
source=people
| eval `DAY_OF_YEAR(DATE('2020-08-26'))` = DAY_OF_YEAR(DATE('2020-08-26'))
| fields `DAY_OF_YEAR(DATE('2020-08-26'))`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| DAY_OF_YEAR(DATE('2020-08-26')) |
| --- |
| 239 |

<!-- vale on -->
  
## EXTRACT

**用法**：`EXTRACT(part FROM date)`

根據指定的 `part` 參數，傳回包含依序排列數字的 `LONG`。傳回的 `LONG` 之特定格式由下表決定。

**參數**：
- `part` (必要)：部分詞元 (請見下表)。
- `date` (必要)：`STRING`、`DATE`、`TIME` 或 `TIMESTAMP` 值。

**傳回類型**：`LONG`

此表中的格式規範與 [`DATE_FORMAT`](#date_format) 函式中的格式規範相同。下表說明 `part` 與特定格式的對應。


| `part` | 格式 |
| --- | --- |
| `MICROSECOND` | `%f` |
| `SECOND` | `%s` |
| `MINUTE` | `%i` |
| `HOUR` | `%H` |
| `DAY` | `%d` |
| `WEEK` | `%X` |
| `MONTH` | `%m` |
| `YEAR` | `%V` |
| `SECOND_MICROSECOND` | `%s%f` |
| `MINUTE_MICROSECOND` | `%i%s%f` |
| `MINUTE_SECOND` | `%i%s` |
| `HOUR_MICROSECOND` | `%H%i%s%f` |
| `HOUR_SECOND` | `%H%i%s` |
| `HOUR_MINUTE` | `%H%i` |
| `DAY_MICROSECOND` | `%d%H%i%s%f` |
| `DAY_SECOND` | `%d%H%i%s` |
| `DAY_MINUTE` | `%d%H%i` |
| `DAY_HOUR` | `%d%H%` |
| `YEAR_MONTH` | `%V%m` |

#### 範例
  
```sql
source=people
| eval `extract(YEAR_MONTH FROM "2023-02-07 10:11:12")` = extract(YEAR_MONTH FROM "2023-02-07 10:11:12")
| fields `extract(YEAR_MONTH FROM "2023-02-07 10:11:12")`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| extract(YEAR_MONTH FROM "2023-02-07 10:11:12") |
| --- |
| 202302 |

<!-- vale on -->
  
## FROM_DAYS

**用法**：`FROM_DAYS(N)`

給定天數 `N`，傳回日期值。

**參數**：
- `N` (必要)：`INTEGER` 或 `LONG` 值。

**傳回類型**：`DATE`

#### 範例
  
```sql
source=people
| eval `FROM_DAYS(733687)` = FROM_DAYS(733687)
| fields `FROM_DAYS(733687)`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| FROM_DAYS(733687) |
| --- |
| 2008-10-07 |

<!-- vale on -->
  
## FROM_UNIXTIME

**用法**：`FROM_UNIXTIME(timestamp)` 或 `FROM_UNIXTIME(timestamp, format)`

將引數表示為時間戳記或字串值。執行 [`UNIX_TIMESTAMP`](#unix_timestamp) 函式的反向轉換。若提供第二個引數，則會用於格式化結果，方式與 [`DATE_FORMAT`](#date_format) 函式所使用的格式字串相同。若時間戳記超出 `1970-01-01 00:00:00`--`3001-01-18 23:59:59.999999` 範圍（0 至 32536771199.999999 的紀元時間），函式會傳回 `NULL`。

**參數**：
- `timestamp` (必要)：代表 Unix 時間戳記的 `DOUBLE` 值。
- `format` (選用)：`STRING` 格式規範。

**傳回類型**：`TIMESTAMP` (不含格式)、`STRING` (含格式)

**範例**
  
```sql
source=people
| eval `FROM_UNIXTIME(1220249547)` = FROM_UNIXTIME(1220249547)
| fields `FROM_UNIXTIME(1220249547)`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| FROM_UNIXTIME(1220249547) |
| --- |
| 2008-09-01 06:12:27 |

<!-- vale on -->
  
```sql
source=people
| eval `FROM_UNIXTIME(1220249547, '%T')` = FROM_UNIXTIME(1220249547, '%T')
| fields `FROM_UNIXTIME(1220249547, '%T')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| FROM_UNIXTIME(1220249547, '%T') |
| --- |
| 06:12:27 |

<!-- vale on -->
  
## GET_FORMAT

**用法**：`GET_FORMAT(type, format)`

根據輸入引數，傳回包含字串格式規範的字串值。

**參數**：
- `type` (必要)：下列其中一個詞元：`DATE`、`TIME`、`TIMESTAMP`。
- `format` (必要)：`STRING`，必須為下列其中之一：`USA`、`JIS`、`ISO`、`EUR`、`INTERNAL`。

**傳回類型**：`STRING`

**範例**
  
```sql
source=people
| eval `GET_FORMAT(DATE, 'USA')` = GET_FORMAT(DATE, 'USA')
| fields `GET_FORMAT(DATE, 'USA')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| GET_FORMAT(DATE, 'USA') |
| --- |
| `%m.%d.%Y` |

<!-- vale on -->
  
## HOUR

**用法**：`HOUR(time)`

擷取 `time` 的小時值。與一日中的時間值不同，時間值的範圍很大且可大於 23，因此 `HOUR(time)` 的傳回值也可能大於 23。

**參數**：
- `time` (必要)：`STRING`、`TIME` 或 `TIMESTAMP` 值。

**傳回類型**：`INTEGER`

同義詞：[`HOUR_OF_DAY`](#hour_of_day)

#### 範例
  
```sql
source=people
| eval `HOUR(TIME('01:02:03'))` = HOUR(TIME('01:02:03'))
| fields `HOUR(TIME('01:02:03'))`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| HOUR(TIME('01:02:03')) |
| --- |
| 1 |

<!-- vale on -->
  
## HOUR_OF_DAY

**用法**：`HOUR_OF_DAY(time)`

擷取 `time` 的小時值。與一日中的時間值不同，時間值的範圍很大且可大於 23，因此 `HOUR_OF_DAY(time)` 的傳回值也可能大於 23。

**參數**：
- `time` (必要)：`STRING`、`TIME` 或 `TIMESTAMP` 值。

**傳回類型**：`INTEGER`

同義詞：[`HOUR`](#hour)

#### 範例
  
```sql
source=people
| eval `HOUR_OF_DAY(TIME('01:02:03'))` = HOUR_OF_DAY(TIME('01:02:03'))
| fields `HOUR_OF_DAY(TIME('01:02:03'))`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| HOUR_OF_DAY(TIME('01:02:03')) |
| --- |
| 1 |

<!-- vale on -->
  
## LAST_DAY

**用法**：`LAST_DAY(date)`

對有效的引數，以 `DATE` 傳回該月的最後一天。

**參數**：
- `date` (必要)：`DATE`、`STRING`、`TIMESTAMP` 或 `TIME` 值。

**傳回類型**：`DATE`

#### 範例
  
```sql
source=people
| eval `last_day('2023-02-06')` = last_day('2023-02-06')
| fields `last_day('2023-02-06')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| last_day('2023-02-06') |
| --- |
| 2023-02-28 |

<!-- vale on -->
  
## LOCALTIMESTAMP

**用法**：`LOCALTIMESTAMP()`

`LOCALTIMESTAMP()` 是 [`NOW()`](#now) 的同義詞。

**參數**：無

**傳回類型**：`TIMESTAMP`

#### 範例
  
```sql
source=people
| eval `LOCALTIMESTAMP()` = LOCALTIMESTAMP()
| fields `LOCALTIMESTAMP()`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| LOCALTIMESTAMP() |
| --- |
| 2025-08-02 15:54:19 |

<!-- vale on -->
  
## LOCALTIME

**用法**：`LOCALTIME()`

`LOCALTIME()` 是 [`NOW()`](#now) 的同義詞。

**參數**：無

**傳回類型**：`TIMESTAMP`

#### 範例
  
```sql
source=people
| eval `LOCALTIME()` = LOCALTIME()
| fields `LOCALTIME()`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| LOCALTIME() |
| --- |
| 2025-08-02 15:54:19 |

<!-- vale on -->
  
## MAKEDATE

**用法**：`MAKEDATE(year, dayofyear)`

給定 `year` 與 `day-of-year` 值，傳回日期。`dayofyear` 必須大於 0，否則結果為 `NULL`。若任一引數為 `NULL`，結果也會是 `NULL`。引數會四捨五入為整數。

**參數**：
- `year` (必要)：年份的 `DOUBLE` 值。
- `dayofyear` (必要)：一年中第幾天的 `DOUBLE` 值。

**傳回類型**：`DATE`

限制：
- `year` 為零時會解讀為 2000
- 不接受負的 `year`
- `day-of-year` 應大於零
- `day-of-year` 可大於 365/366，計算會切換至下一年 (請見範例)

#### 範例
  
```sql
source=people
| eval `MAKEDATE(1945, 5.9)` = MAKEDATE(1945, 5.9), `MAKEDATE(1984, 1984)` = MAKEDATE(1984, 1984)
| fields `MAKEDATE(1945, 5.9)`, `MAKEDATE(1984, 1984)`
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| MAKEDATE(1945, 5.9) | MAKEDATE(1984, 1984) |
| --- | --- |
| 1945-01-06 | 1989-06-06 |

<!-- vale on -->
  
## MAKETIME

**用法**：`MAKETIME(hour, minute, second)`

傳回根據小時、分鐘和秒引數計算的時間值。如果任一引數為 `NULL`，則傳回 `NULL`。第二個引數可以包含小數部分，其餘引數則四捨五入為整數。

**參數**：
- `hour`（必要）：表示小時的 `DOUBLE` 值。
- `minute`（必要）：表示分鐘的 `DOUBLE` 值。
- `second`（必要）：表示秒的 `DOUBLE` 值。

**回傳類型**：`TIME`

限制：
- 使用 24 小時制，可用的時間範圍為 [`00:00:00.0`--`23:59:59.(9)`]
- 秒的小數部分最多取 9 位數（奈秒精度）

#### 範例
  
```sql
source=people
| eval `MAKETIME(20, 30, 40)` = MAKETIME(20, 30, 40), `MAKETIME(20.2, 49.5, 42.100502)` = MAKETIME(20.2, 49.5, 42.100502)
| fields `MAKETIME(20, 30, 40)`, `MAKETIME(20.2, 49.5, 42.100502)`
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| MAKETIME(20, 30, 40) | MAKETIME(20.2, 49.5, 42.100502) |
| --- | --- |
| 20:30:40 | 20:50:42.100502 |

<!-- vale on -->
  
## MICROSECOND

**用法**：`MICROSECOND(expr)`

傳回時間或時間戳記運算式 `expr` 中的微秒數，數值範圍為 0 到 999999。

**參數**：
- `expr`（必要）：`STRING`、`TIME` 或 `TIMESTAMP` 值。

**回傳類型**：`INTEGER`

#### 範例
  
```sql
source=people
| eval `MICROSECOND(TIME('01:02:03.123456'))` = MICROSECOND(TIME('01:02:03.123456'))
| fields `MICROSECOND(TIME('01:02:03.123456'))`
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| MICROSECOND(TIME('01:02:03.123456')) |
| --- |
| 123456 |

<!-- vale on -->
  
## MINUTE

**用法**：`MINUTE(time)`

傳回 `time` 的分鐘數，範圍為 0 到 59。

**參數**：
- `time`（必要）：`STRING`、`TIME` 或 `TIMESTAMP` 值。

**回傳類型**：`INTEGER`

同義函式：[`MINUTE_OF_HOUR`](#minute_of_hour)

#### 範例
  
```sql
source=people
| eval `MINUTE(TIME('01:02:03'))` =  MINUTE(TIME('01:02:03'))
| fields `MINUTE(TIME('01:02:03'))`
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| MINUTE(TIME('01:02:03')) |
| --- |
| 2 |

<!-- vale on -->
  
## MINUTE_OF_DAY

**用法**：`MINUTE_OF_DAY(time)`

傳回一天中已經過的分鐘數，範圍為 0 到 1439。

**參數**：
- `time`（必要）：`STRING`、`TIME` 或 `TIMESTAMP` 值。

**回傳類型**：`INTEGER`

#### 範例
  
```sql
source=people
| eval `MINUTE_OF_DAY(TIME('01:02:03'))` = MINUTE_OF_DAY(TIME('01:02:03'))
| fields `MINUTE_OF_DAY(TIME('01:02:03'))`
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| MINUTE_OF_DAY(TIME('01:02:03')) |
| --- |
| 62 |

<!-- vale on -->
  
## MINUTE_OF_HOUR

**用法**：`MINUTE_OF_HOUR(time)`

傳回 `time` 的分鐘數，範圍為 0 到 59。

**參數**：
- `time`（必要）：`STRING`、`TIME` 或 `TIMESTAMP` 值。

**回傳類型**：`INTEGER`

同義函式：[`MINUTE`](#minute)

#### 範例
  
```sql
source=people
| eval `MINUTE_OF_HOUR(TIME('01:02:03'))` =  MINUTE_OF_HOUR(TIME('01:02:03'))
| fields `MINUTE_OF_HOUR(TIME('01:02:03'))`
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| MINUTE_OF_HOUR(TIME('01:02:03')) |
| --- |
| 2 |

<!-- vale on -->
  
## MONTH

**用法**：`MONTH(date)`

傳回 `date` 的月份，範圍為 1 到 12，分別代表一月到十二月。

**參數**：
- `date`（必要）：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**回傳類型**：`INTEGER`

同義函式：[`MONTH_OF_YEAR`](#month_of_year)

#### 範例
  
```sql
source=people
| eval `MONTH(DATE('2020-08-26'))` =  MONTH(DATE('2020-08-26'))
| fields `MONTH(DATE('2020-08-26'))`
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| MONTH(DATE('2020-08-26')) |
| --- |
| 8 |

<!-- vale on -->
  
## MONTH_OF_YEAR

**用法**：`MONTH_OF_YEAR(date)`

傳回 `date` 的月份，範圍為 1 到 12，分別代表一月到十二月。

**參數**：
- `date`（必要）：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**回傳類型**：`INTEGER`

同義函式：[`MONTH`](#month)

#### 範例
  
```sql
source=people
| eval `MONTH_OF_YEAR(DATE('2020-08-26'))` =  MONTH_OF_YEAR(DATE('2020-08-26'))
| fields `MONTH_OF_YEAR(DATE('2020-08-26'))`
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| MONTH_OF_YEAR(DATE('2020-08-26')) |
| --- |
| 8 |

<!-- vale on -->
  
## MONTHNAME

**用法**：`MONTHNAME(date)`

傳回 `date` 的完整月份名稱。

**參數**：
- `date`（必要）：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**回傳類型**：`STRING`

#### 範例
  
```sql
source=people
| eval `MONTHNAME(DATE('2020-08-26'))` = MONTHNAME(DATE('2020-08-26'))
| fields `MONTHNAME(DATE('2020-08-26'))`
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| MONTHNAME(DATE('2020-08-26')) |
| --- |
| August |

<!-- vale on -->
  
## NOW

**用法**：`NOW()`

以 'YYYY-MM-DD hh:mm:ss' 格式的值傳回目前的日期和時間。此值以 UTC 時區表示。`NOW()` 傳回固定的時間，表示陳述式開始執行的時間。這與 [`SYSDATE()`](#sysdate) 的行為不同，後者傳回其執行當下的確切時間。

**參數**：無

**回傳類型**：`TIMESTAMP`

#### 範例
  
```sql
source=people
| eval `value_1` = NOW(), `value_2` = NOW()
| fields `value_1`, `value_2`
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| value_1 | value_2 |
| --- | --- |
| 2025-08-02 15:39:05 | 2025-08-02 15:39:05 |

<!-- vale on -->
  
## PERIOD_ADD

**用法**：`PERIOD_ADD(P, N)`

將 `N` 個月加到期間 `P`（格式為 YYMM 或 YYYYMM）。傳回格式為 YYYYMM 的值。

**參數**：
- `P`（必要）：表示 YYMM 或 YYYYMM 格式期間的 `INTEGER` 值。
- `N`（必要）：要增加的月數，為 `INTEGER` 數值。

**回傳類型**：`INTEGER`

#### 範例
  
```sql
source=people
| eval `PERIOD_ADD(200801, 2)` = PERIOD_ADD(200801, 2), `PERIOD_ADD(200801, -12)` = PERIOD_ADD(200801, -12)
| fields `PERIOD_ADD(200801, 2)`, `PERIOD_ADD(200801, -12)`
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| PERIOD_ADD(200801, 2) | PERIOD_ADD(200801, -12) |
| --- | --- |
| 200803 | 200701 |

<!-- vale on -->
  
## PERIOD_DIFF

**用法**：`PERIOD_DIFF(P1, P2)`

傳回以 YYMM 或 YYYYMM 格式指定的期間 `P1` 與 `P2` 之間的月數。

**參數**：
- `P1`（必要）：表示 YYMM 或 YYYYMM 格式期間的 `INTEGER` 值。
- `P2`（必要）：表示 YYMM 或 YYYYMM 格式期間的 `INTEGER` 值。

**回傳類型**：`INTEGER`

#### 範例
  
```sql
source=people
| eval `PERIOD_DIFF(200802, 200703)` = PERIOD_DIFF(200802, 200703), `PERIOD_DIFF(200802, 201003)` = PERIOD_DIFF(200802, 201003)
| fields `PERIOD_DIFF(200802, 200703)`, `PERIOD_DIFF(200802, 201003)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| PERIOD_DIFF(200802, 200703) | PERIOD_DIFF(200802, 201003) |
| --- | --- |
| 11 | -25 |

<!-- vale on -->
  
## QUARTER

**用法**：`QUARTER(date)`

傳回 `date` 的季度，範圍為 1 到 4。

**參數**：
- `date` (必要)：一個 `STRING`、`DATE` 或 `TIMESTAMP` 值。

**傳回類型**：`INTEGER`

#### 範例
  
```sql
source=people
| eval `QUARTER(DATE('2020-08-26'))` = QUARTER(DATE('2020-08-26'))
| fields `QUARTER(DATE('2020-08-26'))`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| QUARTER(DATE('2020-08-26')) |
| --- |
| 3 |

<!-- vale on -->
  
## SEC_TO_TIME

**用法**：`SEC_TO_TIME(number)`

以 HH:mm:ss[.nnnnnn] 格式傳回時間。請注意，此函式傳回的時間介於 00:00:00 與 23:59:59 之間。如果輸入值太大 (大於 86399)，此函式會循環並從 00:00:00 開始傳回輸出。如果輸入值太小 (小於 0)，此函式會循環並從 23:59:59 開始倒數傳回輸出。

**參數**：
- `number` (必要)：一個 `INTEGER`、`LONG`、`DOUBLE` 或 `FLOAT` 值。

**傳回類型**：`TIME`

#### 範例
  
```sql
source=people
| eval `SEC_TO_TIME(3601)` = SEC_TO_TIME(3601)
| eval `SEC_TO_TIME(1234.123)` = SEC_TO_TIME(1234.123)
| fields `SEC_TO_TIME(3601)`, `SEC_TO_TIME(1234.123)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| SEC_TO_TIME(3601) | SEC_TO_TIME(1234.123) |
| --- | --- |
| 01:00:01 | 00:20:34.123 |

<!-- vale on -->
  
## SECOND

**用法**：`SECOND(time)`

傳回 `time` 的秒數，範圍為 0 到 59。

**參數**：
- `time` (必要)：一個 `STRING`、`TIME` 或 `TIMESTAMP` 值。

**傳回類型**：`INTEGER`

同義詞：[`SECOND_OF_MINUTE`](#second_of_minute)

#### 範例
  
```sql
source=people
| eval `SECOND(TIME('01:02:03'))` = SECOND(TIME('01:02:03'))
| fields `SECOND(TIME('01:02:03'))`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| SECOND(TIME('01:02:03')) |
| --- |
| 3 |

<!-- vale on -->
  
## SECOND_OF_MINUTE

**用法**：`SECOND_OF_MINUTE(time)`

傳回 `time` 的秒數，範圍為 0 到 59。

**參數**：
- `time` (必要)：一個 `STRING`、`TIME` 或 `TIMESTAMP` 值。

**傳回類型**：`INTEGER`

同義詞：[`SECOND`](#second)

#### 範例
  
```sql
source=people
| eval `SECOND_OF_MINUTE(TIME('01:02:03'))` = SECOND_OF_MINUTE(TIME('01:02:03'))
| fields `SECOND_OF_MINUTE(TIME('01:02:03'))`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| SECOND_OF_MINUTE(TIME('01:02:03')) |
| --- |
| 3 |

<!-- vale on -->
  
## STRFTIME

**版本：3.3.0**

**用法**：`STRFTIME(time, format)`

接受 UNIX 時間戳記 (以秒為單位)，並使用指定的格式將其呈現為字串。對於數值輸入，UNIX 時間必須以秒為單位。大於 100000000000 的值會自動視為毫秒並轉換為秒。您可以搭配 `strftime` 函式使用時間格式變數。此函式執行 [`UNIX_TIMESTAMP`](#unix_timestamp) 的反向操作，且類似於 [`FROM_UNIXTIME`](#from_unixtime)，但使用 POSIX 風格的格式規範。

**參數**：
- `time` (必要)：一個 `INTEGER`、`LONG`、`DOUBLE` 或 `TIMESTAMP` 值。
- `format` (必要)：一個 `STRING` 格式規範。

**傳回類型**：`STRING`

**注意事項**：
- 僅在啟用 Calcite 引擎時可用
- 所有時間戳記都會解譯為 UTC 時區
- 文字格式使用語言中立的 Locale.ROOT (星期與月份名稱會以縮寫形式顯示)
- 不支援字串輸入 - 請先使用 `unix_timestamp()` 轉換字串
- 支援傳回日期/時間值的函式 (例如 `date()`、`now()`、`timestamp()`)

下表說明可用的規範引數：


<!-- vale off -->

| 規範 | 說明 |
| --- | --- |
| `%a` | 縮寫的星期名稱 (Mon..Sun) |
| `%A` | 星期名稱 (Mon..Sun) - 注意：Locale.ROOT 使用縮寫形式 |
| `%b` | 縮寫的月份名稱 (Jan..Dec) |
| `%B` | 月份名稱 (Jan..Dec) - 注意：Locale.ROOT 使用縮寫形式 |
| `%c` | 日期與時間 (例如 Mon Jul 18 09:30:00 2019) |
| `%C` | 世紀，以 2 位數十進位數字表示 |
| `%d` | 月份中的日，以零補齊 (01..31) |
| `%e` | 月份中的日，以空格補齊 ( 1..31) |
| `%Ez` | 與 UTC 的時區位移分鐘數 (例如 UTC 為 +0、IST 為 +330、EST 為 -300) |
| `%f` | 微秒，以十進位數字表示 (000000..999999) |
| `%F` | ISO 8601 日期格式 (`%Y-%m-%d`) |
| `%g` | ISO 8601 年份，不含世紀 (00..99) |
| `%G` | ISO 8601 年份，含世紀 |
| `%H` | 小時 (24 小時制) (00..23) |
| `%I` | 小時 (12 小時制) (01..12) |
| `%j` | 一年中的第幾天 (001..366) |
| `%k` | 小時 (24 小時制)，以空格補齊 ( 0..23) |
| `%m` | 月份，以十進位數字表示 (01..12) |
| `%M` | 分鐘 (00..59) |
| `%N` | 秒以下位數 (預設 `%9N` = 奈秒)。接受 1-9 的任何精確度值 (例如 `%3N` = 3 位數、`%5N` = 5 位數、`%9N` = 9 位數)。精確度直接控制顯示的位數 |
| `%p` | AM 或 PM |
| `%Q` | 秒以下元件 (預設為毫秒)。可指定精確度：`%3Q` = 毫秒、`%6Q` = 微秒、`%9Q` = 奈秒。其他精確度值 (例如 `%5Q`) 預設為 `%3Q` |
| `%s` | UNIX Epoch 時間戳記，以秒為單位 |
| `%S` | 秒 (00..59) |
| `%T` | 24 小時制時間 (`%H:%M:%S`) |
| `%U` | 一年中的第幾週，從 0 開始 (00..53) |
| `%V` | ISO 週數 (01..53) |
| `%w` | 星期，以十進位表示 (0=星期日..6=星期六) |
| `%x` | MM/dd/yyyy 格式的日期 (例如 07/13/2019) |
| `%X` | HH:mm:ss 格式的時間 (例如 09:30:00) |
| `%y` | 年份，不含世紀 (00..99) |
| `%Y` | 年份，含世紀 |
| `%z` | 時區位移 (+hhmm 或 -hhmm) |
| `%:z` | 含冒號的時區位移 (+hh:mm 或 -hh:mm) |
| `%::z` | 含冒號的時區位移 (+hh:mm:ss) |
| `%:::z` | 僅時區位移小時 (+hh 或 -hh) |
| `%Z` | 時區縮寫 (例如 EST、PDT) |
| `%%` | 字面 % 字元 |

<!-- vale on -->

**範例**
  
```sql
source=people | eval `strftime(1521467703, "%Y-%m-%dT%H:%M:%S")` = strftime(1521467703, "%Y-%m-%dT%H:%M:%S") | fields `strftime(1521467703, "%Y-%m-%dT%H:%M:%S")`
```
{% include copy.html %}

<!-- vale off -->  
| strftime(1521467703, "%Y-%m-%dT%H:%M:%S") |
| --- |
| 2018-03-19T13:55:03 |

<!-- vale on --> 

```sql
source=people | eval `strftime(1521467703, "%F %T")` = strftime(1521467703, "%F %T") | fields `strftime(1521467703, "%F %T")`
```
{% include copy.html %}
  
<!-- vale off -->

| strftime(1521467703, "%Y-%m-%dT%H:%M:%S") |
| --- |
| 2018-03-19T13:55:03 |

<!-- vale on -->

```sql
source=people | eval `strftime(1521467703, "%a %b %d, %Y")` = strftime(1521467703, "%a %b %d, %Y") | fields `strftime(1521467703, "%a %b %d, %Y")`
```
{% include copy.html %}

<!-- vale off -->  
| strftime(1521467703, "%a %b %d, %Y") |
| --- |
| Mon Mar 19, 2018 |

<!-- vale on -->

```sql
source=people | eval `strftime(1521467703, "%%Y")` = strftime(1521467703, "%%Y") | fields `strftime(1521467703, "%%Y")`
```
{% include copy.html %}

<!-- vale off -->  
| strftime(1521467703, "%%Y") |
| --- |
| `%Y` |

<!-- vale on -->

```sql
source=people | eval `strftime(date('2020-09-16'), "%Y-%m-%d")` = strftime(date('2020-09-16'), "%Y-%m-%d") | fields `strftime(date('2020-09-16'), "%Y-%m-%d")`
```
{% include copy.html %}

```text
  
fetched rows / total rows = 1/1
+----------------------------------------+
| strftime(date('2020-09-16'), "%Y-%m-%d") |
|-----------------------------------------|
| 2020-09-16                             |
  
+----------------------------------------+
  
```

```sql
  
source=people | eval `strftime(timestamp('2020-09-16 14:30:00'), "%F %T")` = strftime(timestamp('2020-09-16 14:30:00'), "%F %T") | fields `strftime(timestamp('2020-09-16 14:30:00'), "%F %T")`
  
```
{% include copy.html %}

```text
  
fetched rows / total rows = 1/1
+--------------------------------------------------+
| strftime(timestamp('2020-09-16 14:30:00'), "%F %T") |
|---------------------------------------------------|
| 2020-09-16 14:30:00                              |
  
+--------------------------------------------------+
  
```

```sql
  
source=people | eval `strftime(now(), "%Y-%m-%d %H:%M:%S")` = strftime(now(), "%Y-%m-%d %H:%M:%S") | fields `strftime(now(), "%Y-%m-%d %H:%M:%S")`
  
```
{% include copy.html %}

```text
  
fetched rows / total rows = 1/1
+------------------------------------+
| strftime(now(), "%Y-%m-%d %H:%M:%S") |
|-------------------------------------|
| 2025-09-03 12:30:45                |
  
+------------------------------------+
  
```
## STR_TO_DATE

**用法**：`STR_TO_DATE(string, format)`

使用第二個引數字串中指定的格式，從第一個引數字串擷取 `TIMESTAMP`。輸入引數必須包含足夠的資訊，才能剖析為 `DATE`、`TIMESTAMP` 或 `TIME`。可接受的字串格式指定符與 [`DATE_FORMAT`](#date_format) 函式使用的相同。當引數配對無效而導致陳述式無法剖析，或任何 `DATE` 欄位的值為 0 時，傳回 `NULL`。否則，傳回包含剖析值的 `TIMESTAMP`（以及任何未剖析欄位的預設值）。

**參數**：
- `string`（必要）：要剖析的 `STRING` 值。
- `format`（必要）：`STRING` 格式指定符。

**回傳類型**：`TIMESTAMP`

#### 範例

```sql
  
source=people
| eval `str_to_date("01,5,2013", "%d,%m,%Y")` = str_to_date("01,5,2013", "%d,%m,%Y")
| fields `str_to_date("01,5,2013", "%d,%m,%Y")`
  
```
{% include copy.html %}
  
查詢傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+--------------------------------------+
| str_to_date("01,5,2013", "%d,%m,%Y") |
|--------------------------------------|
| 2013-05-01 00:00:00                  |
  
+--------------------------------------+
  
```
  
## SUBDATE

**用法**：`SUBDATE(date, INTERVAL expr unit)` 或 `SUBDATE(date, days)`

從 `date` 減去時間間隔 `expr`，或將第二個引數視為整數天數，從 `date` 減去該天數。如果第一個引數是 `TIME`，則使用今天的日期。如果第一個引數是 `DATE`，則使用午夜時間。

**參數**：
- `date`（必要）：`DATE`、`TIMESTAMP` 或 `TIME` 值。
- `expr`（必要）：`INTERVAL` 運算式或 `LONG` 天數。

**回傳類型**：`TIMESTAMP`（搭配 INTERVAL）、`DATE`（DATE 搭配 LONG）、`TIMESTAMP`（TIMESTAMP/TIME 搭配 LONG）

同義函式：以 INTERVAL 形式的第二個引數呼叫時，為 [`DATE_SUB`](#date_sub)
反義函式：[`ADDDATE`](#adddate)

#### 範例

```sql
  
source=people
| eval `'2008-01-02' - 31d` = SUBDATE(DATE('2008-01-02'), INTERVAL 31 DAY), `'2020-08-26' - 1` = SUBDATE(DATE('2020-08-26'), 1), `ts '2020-08-26 01:01:01' - 1` = SUBDATE(TIMESTAMP('2020-08-26 01:01:01'), 1)
| fields `'2008-01-02' - 31d`, `'2020-08-26' - 1`, `ts '2020-08-26 01:01:01' - 1`
  
```
{% include copy.html %}
  
查詢傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+---------------------+------------------+------------------------------+
| '2008-01-02' - 31d  | '2020-08-26' - 1 | ts '2020-08-26 01:01:01' - 1 |
|---------------------+------------------+------------------------------|
| 2007-12-02 00:00:00 | 2020-08-25       | 2020-08-25 01:01:01          |
  
+---------------------+------------------+------------------------------+
  
```
  
## SUBTIME

**用法**：`SUBTIME(expr1, expr2)`

從 `expr1` 減去 `expr2`，並傳回結果。如果引數是 `TIME`，則使用今天的日期。如果引數是 `DATE`，則使用午夜時間。

**參數**：
- `expr1`（必要）：`DATE`、`TIMESTAMP` 或 `TIME` 值。
- `expr2`（必要）：`DATE`、`TIMESTAMP` 或 `TIME` 值。

**回傳類型**：`TIMESTAMP`（DATE/TIMESTAMP 搭配 DATE/TIMESTAMP/TIME）、`TIME`（TIME 搭配 DATE/TIMESTAMP/TIME）

反義函式：[`ADDTIME`](#addtime)

#### 範例

```sql
  
source=people
| eval `'2008-12-12' - 0` = SUBTIME(DATE('2008-12-12'), DATE('2008-11-15'))
| fields `'2008-12-12' - 0`
  
```
{% include copy.html %}
  
查詢傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+---------------------+
| '2008-12-12' - 0    |
|---------------------|
| 2008-12-12 00:00:00 |
  
+---------------------+
  
```
  
```sql
  
source=people
| eval `'23:59:59' - 0` = SUBTIME(TIME('23:59:59'), DATE('2004-01-01'))
| fields `'23:59:59' - 0`
  
```
{% include copy.html %}
  
查詢傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+----------------+
| '23:59:59' - 0 |
|----------------|
| 23:59:59       |
  
+----------------+
  
```
  
```sql
  
source=people
| eval `'2004-01-01' - '23:59:59'` = SUBTIME(DATE('2004-01-01'), TIME('23:59:59'))
| fields `'2004-01-01' - '23:59:59'`
  
```
{% include copy.html %}
  
查詢傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+---------------------------+
| '2004-01-01' - '23:59:59' |
|---------------------------|
| 2003-12-31 00:00:01       |
  
+---------------------------+
  
```
  
```sql
  
source=people
| eval `'10:20:30' - '00:05:42'` = SUBTIME(TIME('10:20:30'), TIME('00:05:42'))
| fields `'10:20:30' - '00:05:42'`
  
```
{% include copy.html %}
  
查詢傳回下列結果：

```text  
fetched rows / total rows = 1/1
+-------------------------+
| '10:20:30' - '00:05:42' |
|-------------------------|
| 10:14:48                |
  
+-------------------------+
```
  
```sql 
source=people
| eval `'2007-03-01 10:20:30' - '20:40:50'` = SUBTIME(TIMESTAMP('2007-03-01 10:20:30'), TIMESTAMP('2002-03-04 20:40:50'))
| fields `'2007-03-01 10:20:30' - '20:40:50'`
```
{% include copy.html %}
  
查詢傳回下列結果：

```text  
fetched rows / total rows = 1/1
+------------------------------------+
| '2007-03-01 10:20:30' - '20:40:50' |
|------------------------------------|
| 2007-02-28 13:39:40                |
  
+------------------------------------+  
```
  
## SYSDATE

**用法**：`SYSDATE()` 或 `SYSDATE(precision)`

以 'YYYY-MM-DD hh:mm:ss[.nnnnnn]' 格式的值傳回目前的日期與時間。`SYSDATE()` 傳回其執行當下的 UTC 日期與時間。這與 [`NOW()`](#now) 的行為不同，後者傳回固定的時間，表示陳述式開始執行的時間。如果提供引數，該引數會指定 0 到 6 的小數秒精確度，回傳值會包含具有該位數的小數秒部分。

**參數**：
- `precision`（選用）：介於 0 到 6 的 `INTEGER` 值，用於指定小數秒精確度。

**回傳類型**：`TIMESTAMP`

#### 範例

```sql
  
source=people
| eval `value_1` = SYSDATE(), `value_2` = SYSDATE(6)
| fields `value_1`, `value_2`
  
```
{% include copy.html %}
  
查詢傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+---------------------+----------------------------+
| value_1             | value_2                    |
|---------------------+----------------------------|
| 2025-08-02 15:39:05 | 2025-08-02 15:39:05.123456 |
  
+---------------------+----------------------------+
  
```
  
## TIME

**用法**：`TIME(expr)`

將輸入字串 `expr` 視為時間，建構時間類型。如果引數為日期、時間或時間戳記類型，則從運算式擷取時間值部分。

**參數**：
- `expr`（必要）：`STRING`、`DATE`、`TIME` 或 `TIMESTAMP` 值。

**回傳類型**：`TIME`

#### 範例

```sql
  
source=people
| eval `TIME('13:49:00')` = TIME('13:49:00')
| fields `TIME('13:49:00')`
  
```
{% include copy.html %}
  
查詢傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+------------------+
| TIME('13:49:00') |
|------------------|
| 13:49:00         |
  
+------------------+
  
```
  
```sql
  
source=people
| eval `TIME('13:49')` = TIME('13:49')
| fields `TIME('13:49')`
  
```
{% include copy.html %}
  
查詢傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+---------------+
| TIME('13:49') |
|---------------|
| 13:49:00      |
  
+---------------+
  
```
  
```sql
  
source=people
| eval `TIME('2020-08-26 13:49:00')` = TIME('2020-08-26 13:49:00')
| fields `TIME('2020-08-26 13:49:00')`
  
```
{% include copy.html %}
  
查詢傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+-----------------------------+
| TIME('2020-08-26 13:49:00') |
|-----------------------------|
| 13:49:00                    |
  
+-----------------------------+
  
```
  
```sql
  
source=people
| eval `TIME('2020-08-26 13:49')` = TIME('2020-08-26 13:49')
| fields `TIME('2020-08-26 13:49')`
  
```
{% include copy.html %}
  
查詢傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+--------------------------+
| TIME('2020-08-26 13:49') |
|--------------------------|
| 13:49:00                 |
  
+--------------------------+
  
```
  
## TIME_FORMAT

**用法**：`TIME_FORMAT(time, format)`

使用 `format` 引數中的規範符來格式化 `time` 引數。此函式支援 [`DATE_FORMAT`](#date_format) 函式可用之時間格式規範符的子集。使用 [`DATE_FORMAT`](#date_format) 支援的日期格式規範符將回傳 0 或 `NULL`。可接受的格式規範符列於下表。若傳入 `DATE` 類型的引數，則會將其視為午夜的 `TIMESTAMP`（即 00:00:00）。

**參數**：
- `time`（必要）：`STRING`、`DATE`、`TIME` 或 `TIMESTAMP` 值。
- `format`（必要）：`STRING` 格式規範符。

**回傳類型**：`STRING`

下表說明可用的規範符引數：

<!-- vale off -->

| 規範符 | 說明 |
| --- | --- |
| `%f` | 微秒 (000000..999999) |
| `%H` | 小時 (00..23) |
| `%h` | 小時 (01..12) |
| `%I` | 小時 (01..12) |
| `%i` | 分鐘，數值 (00..59) |
| `%p` | `AM` 或 `PM` |
| `%r` | 時間，12 小時制 (hh:mm:ss 後接 `AM` 或 `PM`) |
| `%S` | 秒 (00..59) |
| `%s` | 秒 (00..59) |
| `%T` | 時間，24 小時制 (hh:mm:ss) |

<!-- vale on -->

#### 範例

```sql
  
source=people
| eval `TIME_FORMAT('1998-01-31 13:14:15.012345', '%f %H %h %I %i %p %r %S %s %T')` = TIME_FORMAT('1998-01-31 13:14:15.012345', '%f %H %h %I %i %p %r %S %s %T')
| fields `TIME_FORMAT('1998-01-31 13:14:15.012345', '%f %H %h %I %i %p %r %S %s %T')`
  
```
{% include copy.html %}
  
查詢回傳以下結果：

```text
  
fetched rows / total rows = 1/1
+----------------------------------------------------------------------------+
| TIME_FORMAT('1998-01-31 13:14:15.012345', '%f %H %h %I %i %p %r %S %s %T') |
|----------------------------------------------------------------------------|
| 012345 13 01 01 14 PM 01:14:15 PM 15 15 13:14:15                           |
  
+----------------------------------------------------------------------------+
  
```
  
## TIME_TO_SEC

**用法**：`TIME_TO_SEC(time)`

回傳轉換為秒數的 `time` 引數。

**參數**：
- `time`（必要）：`STRING`、`TIME` 或 `TIMESTAMP` 值。

**回傳類型**：`LONG`

#### 範例

```sql
  
source=people
| eval `TIME_TO_SEC(TIME('22:23:00'))` = TIME_TO_SEC(TIME('22:23:00'))
| fields `TIME_TO_SEC(TIME('22:23:00'))`
  
```
{% include copy.html %}
  
查詢回傳以下結果：

```text
  
fetched rows / total rows = 1/1
+-------------------------------+
| TIME_TO_SEC(TIME('22:23:00')) |
|-------------------------------|
| 80580                         |
  
+-------------------------------+
  
```
  
## TIMEDIFF

**用法**：`TIMEDIFF(time1, time2)`

以時間形式回傳兩個時間運算式之間的差值。

**參數**：
- `time1`（必要）：`TIME` 值。
- `time2`（必要）：`TIME` 值。

**回傳類型**：`TIME`

#### 範例

```sql
  
source=people
| eval `TIMEDIFF('23:59:59', '13:00:00')` = TIMEDIFF('23:59:59', '13:00:00')
| fields `TIMEDIFF('23:59:59', '13:00:00')`
  
```
{% include copy.html %}
  
查詢回傳以下結果：

```text
  
fetched rows / total rows = 1/1
+----------------------------------+
| TIMEDIFF('23:59:59', '13:00:00') |
|----------------------------------|
| 10:59:59                         |
  
+----------------------------------+
  
```
  
## TIMESTAMP

**用法**：`TIMESTAMP(expr)` 或 `TIMESTAMP(expr1, expr2)`

以輸入字串 `expr` 建構時間戳記類型。若引數不是字串，則會以預設時區 UTC 將 `expr` 轉換為時間戳記類型。若引數是時間，則會在轉換前套用今天的日期。若有兩個引數，則將時間運算式 `expr2` 加到日期或時間戳記運算式 `expr1`，並以時間戳記值回傳結果。

**參數**：
- `expr`（必要）：`STRING`、`DATE`、`TIME` 或 `TIMESTAMP` 值。
- `expr2`（選用）：`STRING`、`DATE`、`TIME` 或 `TIMESTAMP` 值。

**回傳類型**：`TIMESTAMP`

#### 範例

```sql
  
source=people
| eval `TIMESTAMP('2020-08-26 13:49:00')` = TIMESTAMP('2020-08-26 13:49:00'), `TIMESTAMP('2020-08-26 13:49:00', TIME('12:15:42'))` = TIMESTAMP('2020-08-26 13:49:00', TIME('12:15:42'))
| fields `TIMESTAMP('2020-08-26 13:49:00')`, `TIMESTAMP('2020-08-26 13:49:00', TIME('12:15:42'))`
  
```
{% include copy.html %}
  
查詢回傳以下結果：

```text
  
fetched rows / total rows = 1/1
+----------------------------------+----------------------------------------------------+
| TIMESTAMP('2020-08-26 13:49:00') | TIMESTAMP('2020-08-26 13:49:00', TIME('12:15:42')) |
|----------------------------------+----------------------------------------------------|
| 2020-08-26 13:49:00              | 2020-08-27 02:04:42                                |
  
+----------------------------------+----------------------------------------------------+
  
```
  
## TIMESTAMPADD

**用法**：`TIMESTAMPADD(interval, count, datetime)`

根據傳入的 `DATE`/`TIME`/`TIMESTAMP`/`STRING` 引數，以及決定要加入之時間量的 `INTERVAL` 與 `INTEGER` 引數，回傳 `TIMESTAMP` 值。若第三個引數是 `STRING`，則必須格式化為有效的 `TIMESTAMP`。若僅提供 `TIME`，仍會回傳 `TIMESTAMP`，並以目前日期填入 `DATE` 部分。若第三個引數是 `DATE`，則會自動轉換為 `TIMESTAMP`。

**參數**：
- `interval`（必要）：以下其中之一：`MICROSECOND`、`SECOND`、`MINUTE`、`HOUR`、`DAY`、`WEEK`、`MONTH`、`QUARTER`、`YEAR`。
- `count`（必要）：要加入的區間數量，為 `INTEGER`。
- `datetime`（必要）：`DATE`、`TIME`、`TIMESTAMP` 或 `STRING` 值。

**回傳類型**：`TIMESTAMP`

**範例**

```sql
  
source=people
| eval `TIMESTAMPADD(DAY, 17, '2000-01-01 00:00:00')` = TIMESTAMPADD(DAY, 17, '2000-01-01 00:00:00')
| eval `TIMESTAMPADD(QUARTER, -1, '2000-01-01 00:00:00')` = TIMESTAMPADD(QUARTER, -1, '2000-01-01 00:00:00')
| fields `TIMESTAMPADD(DAY, 17, '2000-01-01 00:00:00')`, `TIMESTAMPADD(QUARTER, -1, '2000-01-01 00:00:00')`
  
```
{% include copy.html %}
  
查詢回傳以下結果：

```text
  
fetched rows / total rows = 1/1
+----------------------------------------------+--------------------------------------------------+
| TIMESTAMPADD(DAY, 17, '2000-01-01 00:00:00') | TIMESTAMPADD(QUARTER, -1, '2000-01-01 00:00:00') |
|----------------------------------------------+--------------------------------------------------|
| 2000-01-18 00:00:00                          | 1999-10-01 00:00:00                              |
  
+----------------------------------------------+--------------------------------------------------+
  
```
  
## TIMESTAMPDIFF

**用法**：`TIMESTAMPDIFF(interval, start, end)`

以區間單位回傳開始與結束日期/時間之間的差值。若提供 `TIME` 作為引數，則會轉換為 `TIMESTAMP`，並以目前日期填入 `DATE` 部分。引數會在適當時自動轉換為 `TIME`/`TIMESTAMP`。任何為 `STRING` 的引數都必須格式化為有效的 `TIMESTAMP`。

**參數**：
- `interval`（必要）：以下其中之一：`MICROSECOND`、`SECOND`、`MINUTE`、`HOUR`、`DAY`、`WEEK`、`MONTH`、`QUARTER`、`YEAR`。
- `start`（必要）：`DATE`、`TIME`、`TIMESTAMP` 或 `STRING` 值。
- `end`（必要）：`DATE`、`TIME`、`TIMESTAMP` 或 `STRING` 值。

**回傳類型**：`LONG`

**範例**

```sql
  
source=people
| eval `TIMESTAMPDIFF(YEAR, '1997-01-01 00:00:00', '2001-03-06 00:00:00')` = TIMESTAMPDIFF(YEAR, '1997-01-01 00:00:00', '2001-03-06 00:00:00')
| eval `TIMESTAMPDIFF(SECOND, time('00:00:23'), time('00:00:00'))` = TIMESTAMPDIFF(SECOND, time('00:00:23'), time('00:00:00'))
| fields `TIMESTAMPDIFF(YEAR, '1997-01-01 00:00:00', '2001-03-06 00:00:00')`, `TIMESTAMPDIFF(SECOND, time('00:00:23'), time('00:00:00'))`
  
```
{% include copy.html %}
  
查詢回傳以下結果：

```text
  
fetched rows / total rows = 1/1
+-------------------------------------------------------------------+-----------------------------------------------------------+
| TIMESTAMPDIFF(YEAR, '1997-01-01 00:00:00', '2001-03-06 00:00:00') | TIMESTAMPDIFF(SECOND, time('00:00:23'), time('00:00:00')) |
|-------------------------------------------------------------------+-----------------------------------------------------------|
| 4                                                                 | -23                                                       |
  
+-------------------------------------------------------------------+-----------------------------------------------------------+
  
```
  
## TO_DAYS

**用法**：`TO_DAYS(date)`

傳回指定日期的天數（自第 0 年起算的天數）。若日期無效，則傳回 `NULL`。

**參數**：
- `date`（必要）：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**傳回類型**：`LONG`

#### 範例

```sql
  
source=people
| eval `TO_DAYS(DATE('2008-10-07'))` = TO_DAYS(DATE('2008-10-07'))
| fields `TO_DAYS(DATE('2008-10-07'))`
  
```
{% include copy.html %}
  
查詢會傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+-----------------------------+
| TO_DAYS(DATE('2008-10-07')) |
|-----------------------------|
| 733687                      |
  
+-----------------------------+
  
```
  
## TO_SECONDS

**用法**：`TO_SECONDS(date)`

傳回指定值自第 0 年起算的秒數。若值無效，則傳回 `NULL`。可使用 `LONG` 類型的引數。其格式必須為 YMMDD、YYMMDD、YYYMMDD 或 YYYYMMDD。請注意，`LONG` 類型的引數不能有前置零，因為它會使用八進位數字系統進行剖析。

**參數**：
- `date`（必要）：`STRING`、`LONG`、`DATE`、`TIME` 或 `TIMESTAMP` 值。

**傳回類型**：`LONG`

#### 範例

```sql
  
source=people
| eval `TO_SECONDS(DATE('2008-10-07'))` = TO_SECONDS(DATE('2008-10-07'))
| eval `TO_SECONDS(950228)` = TO_SECONDS(950228)
| fields `TO_SECONDS(DATE('2008-10-07'))`, `TO_SECONDS(950228)`
  
```
{% include copy.html %}
  
查詢會傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+--------------------------------+--------------------+
| TO_SECONDS(DATE('2008-10-07')) | TO_SECONDS(950228) |
|--------------------------------+--------------------|
| 63390556800                    | 62961148800        |
  
+--------------------------------+--------------------+
  
```
  
## UNIX_TIMESTAMP

**用法**：`UNIX_TIMESTAMP()` 或 `UNIX_TIMESTAMP(date)`

將指定的引數轉換為 Unix 時間（自 Epoch 起算的秒數，即 1970 年的一開始）。若未提供引數，則傳回目前的 Unix 時間。日期引數可以是 `DATE`、`TIMESTAMP` 字串，或 `YYMMDD`、`YYMMDDhhmmss`、`YYYYMMDD` 或 `YYYYMMDDhhmmss` 格式的數字。若引數包含時間部分，則可選擇性地包含小數秒部分。若引數格式無效或超出範圍 `1970-01-01 00:00:00`--`3001-01-18 23:59:59.999999`（0 至 32536771199.999999 epoch 時間），則函式會傳回 `NULL`。您可以使用 [`FROM_UNIXTIME`](#from_unixtime) 執行反向轉換。

**參數**：
- `date`（選用）：`DOUBLE`、`DATE` 或 `TIMESTAMP` 值。

**傳回類型**：`DOUBLE`

#### 範例

```sql
  
source=people
| eval `UNIX_TIMESTAMP(double)` = UNIX_TIMESTAMP(20771122143845), `UNIX_TIMESTAMP(timestamp)` = UNIX_TIMESTAMP(TIMESTAMP('1996-11-15 17:05:42'))
| fields `UNIX_TIMESTAMP(double)`, `UNIX_TIMESTAMP(timestamp)`
  
```
{% include copy.html %}
  
查詢會傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+------------------------+---------------------------+
| UNIX_TIMESTAMP(double) | UNIX_TIMESTAMP(timestamp) |
|------------------------+---------------------------|
| 3404817525.0           | 848077542.0               |
  
+------------------------+---------------------------+
  
```
  
## UTC_DATE

**用法**：`UTC_DATE()`

以 `YYYY-MM-DD` 格式的值傳回目前的 UTC 日期。

**參數**：無

**傳回類型**：`DATE`

#### 範例

```sql
  
source=people
| eval `UTC_DATE()` = UTC_DATE()
| fields `UTC_DATE()`
  
```
{% include copy.html %}
  
查詢會傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+------------+
| UTC_DATE() |
|------------|
| 2025-10-03 |
  
+------------+
  
```
  
## UTC_TIME

**用法**：`UTC_TIME()`

以 'hh:mm:ss' 格式的值傳回目前的 UTC 時間。

**參數**：無

**傳回類型**：`TIME`

#### 範例

```sql
  
source=people
| eval `UTC_TIME()` = UTC_TIME()
| fields `UTC_TIME()`
  
```
{% include copy.html %}
  
查詢會傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+------------+
| UTC_TIME() |
|------------|
| 17:54:27   |
  
+------------+
  
```
  
## UTC_TIMESTAMP

**用法**：`UTC_TIMESTAMP()`

以 'YYYY-MM-DD hh:mm:ss' 格式的值傳回目前的 UTC 時間戳記。

**參數**：無

**傳回類型**：`TIMESTAMP`

#### 範例

```sql
  
source=people
| eval `UTC_TIMESTAMP()` = UTC_TIMESTAMP()
| fields `UTC_TIMESTAMP()`
  
```
{% include copy.html %}
  
查詢會傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+---------------------+
| UTC_TIMESTAMP()     |
|---------------------|
| 2025-10-03 17:54:28 |
  
+---------------------+
  
```
  
## WEEK

**用法**：`WEEK(date)` 或 `WEEK(date, mode)`

傳回 `date` 的週數。若省略模式引數，則使用預設模式 0。

**參數**：
- `date`（必要）：`DATE`、`TIMESTAMP` 或 `STRING` 值。
- `mode`（選用）：`INTEGER` 模式值（0--7）。

**傳回類型**：`INTEGER`

同義詞：[`WEEK_OF_YEAR`](#week_of_year)

下表說明 `mode` 參數的運作方式。

| 模式 | 每週第一天 | 範圍 | 第 1 週是第一個... |
| --- | --- | --- | --- |
| 0 | 星期日 | 0--53 | 包含本年度星期日的該週 |
| 1 | 星期一 | 0--53 | 本年度有 4 天以上的該週 |
| 2 | 星期日 | 1--53 | 包含本年度星期日的該週 |
| 3 | 星期一 | 1--53 | 本年度有 4 天以上的該週 |
| 4 | 星期日 | 0--53 | 本年度有 4 天以上的該週 |
| 5 | 星期一 | 0--53 | 包含本年度星期一的該週 |
| 6 | 星期日 | 1--53 | 本年度有 4 天以上的該週 |
| 7 | 星期一 | 1--53 | 包含本年度星期一的該週 |

#### 範例

```sql
  
source=people
| eval `WEEK(DATE('2008-02-20'))` = WEEK(DATE('2008-02-20')), `WEEK(DATE('2008-02-20'), 1)` = WEEK(DATE('2008-02-20'), 1)
| fields `WEEK(DATE('2008-02-20'))`, `WEEK(DATE('2008-02-20'), 1)`
  
```
{% include copy.html %}
  
查詢會傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+--------------------------+-----------------------------+
| WEEK(DATE('2008-02-20')) | WEEK(DATE('2008-02-20'), 1) |
|--------------------------+-----------------------------|
| 7                        | 8                           |
  
+--------------------------+-----------------------------+
  
```
  
## WEEKDAY

**用法**：`WEEKDAY(date)`

傳回 `date` 的星期索引（0 = 星期一、1 = 星期二、...、6 = 星期日）。它與 [`DAYOFWEEK`](#dayofweek) 函式類似，但對各星期幾傳回的索引值與該函式不同。

**參數**：
- `date`（必要）：`STRING`、`DATE`、`TIME` 或 `TIMESTAMP` 值。

**傳回類型**：`INTEGER`

#### 範例

```sql
  
source=people
| eval `weekday(DATE('2020-08-26'))` = weekday(DATE('2020-08-26'))
| eval `weekday(DATE('2020-08-27'))` = weekday(DATE('2020-08-27'))
| fields `weekday(DATE('2020-08-26'))`, `weekday(DATE('2020-08-27'))`
  
```
{% include copy.html %}
  
查詢會傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+-----------------------------+-----------------------------+
| weekday(DATE('2020-08-26')) | weekday(DATE('2020-08-27')) |
|-----------------------------+-----------------------------|
| 2                           | 3                           |
  
+-----------------------------+-----------------------------+
  
```
  
## WEEK_OF_YEAR

**用法**：`WEEK_OF_YEAR(date)` 或 `WEEK_OF_YEAR(date, mode)`

傳回 `date` 的週數。若省略 mode 引數，則使用預設模式 0。

**參數**：
- `date`（必要）：`DATE`、`TIMESTAMP` 或 `STRING` 值。
- `mode`（選用）：`INTEGER` 模式值（0--7）。

**回傳類型**：`INTEGER`

同義詞：[`WEEK`](#week)

下表說明 mode 引數的運作方式：

<!-- vale off -->

| 模式 | 每週第一天 | 範圍 | 第 1 週是第一個 ... 的週 |
| --- | --- | --- | --- |
| 0 | 星期日 | 0--53 | 本年度包含星期日的週 |
| 1 | 星期一 | 0--53 | 本年度有 4 天以上的週 |
| 2 | 星期日 | 1--53 | 本年度包含星期日的週 |
| 3 | 星期一 | 1--53 | 本年度有 4 天以上的週 |
| 4 | 星期日 | 0--53 | 本年度有 4 天以上的週 |
| 5 | 星期一 | 0--53 | 本年度包含星期一的週 |
| 6 | 星期日 | 1--53 | 本年度有 4 天以上的週 |
| 7 | 星期一 | 1--53 | 本年度包含星期一的週 |

<!-- vale on -->

#### 範例

```sql
  
source=people
| eval `WEEK_OF_YEAR(DATE('2008-02-20'))` = WEEK(DATE('2008-02-20')), `WEEK_OF_YEAR(DATE('2008-02-20'), 1)` = WEEK_OF_YEAR(DATE('2008-02-20'), 1)
| fields `WEEK_OF_YEAR(DATE('2008-02-20'))`, `WEEK_OF_YEAR(DATE('2008-02-20'), 1)`
  
```
{% include copy.html %}
  
查詢會傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+----------------------------------+-------------------------------------+
| WEEK_OF_YEAR(DATE('2008-02-20')) | WEEK_OF_YEAR(DATE('2008-02-20'), 1) |
|----------------------------------+-------------------------------------|
| 7                                | 8                                   |
  
+----------------------------------+-------------------------------------+
  
```
  
## YEAR

**用法**：`YEAR(date)`

傳回 `date` 的年份，範圍為 1000 至 9999；「零」日期則傳回 0。

**參數**：
- `date`（必要）：`STRING`、`DATE` 或 `TIMESTAMP` 值。

**回傳類型**：`INTEGER`

#### 範例

```sql
  
source=people
| eval `YEAR(DATE('2020-08-26'))` = YEAR(DATE('2020-08-26'))
| fields `YEAR(DATE('2020-08-26'))`
  
```
{% include copy.html %}
  
查詢會傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+--------------------------+
| YEAR(DATE('2020-08-26')) |
|--------------------------|
| 2020                     |
  
+--------------------------+
  
```
  
## YEARWEEK

**用法**：`YEARWEEK(date)` 或 `YEARWEEK(date, mode)`

以整數傳回 `date` 的年份與週。可接受選用的 mode 引數，與 [`WEEK`](#week) 函式可用的模式一致。

**參數**：
- `date`（必要）：`STRING`、`DATE`、`TIME` 或 `TIMESTAMP` 值。
- `mode`（選用）：`INTEGER` 模式值（0--7）。

**回傳類型**：`INTEGER`

#### 範例

```sql
  
source=people
| eval `YEARWEEK('2020-08-26')` = YEARWEEK('2020-08-26')
| eval `YEARWEEK('2019-01-05', 1)` = YEARWEEK('2019-01-05', 1)
| fields `YEARWEEK('2020-08-26')`, `YEARWEEK('2019-01-05', 1)`
  
```
{% include copy.html %}
  
查詢會傳回下列結果：

```text
  
fetched rows / total rows = 1/1
+------------------------+---------------------------+
| YEARWEEK('2020-08-26') | YEARWEEK('2019-01-05', 1) |
|------------------------+---------------------------|
| 202034                 | 201901                    |
  
+------------------------+---------------------------+
  
```
  