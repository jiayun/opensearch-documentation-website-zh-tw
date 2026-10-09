---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "日期"
nav_order: 25
has_children: false
parent: Date field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/date/
  - /opensearch/supported-field-types/date/
  - /field-types/date/
---

# 日期欄位類型
**於 1.0 版導入**
{: .label .label-purple }

OpenSearch 中的日期可以用下列其中一種形式表示：

- 一個對應自 epoch 起算毫秒數的 long 值。日期在內部即以此形式儲存。
- 一個已格式化的字串。
- 一個對應自 epoch 起算秒數的整數值。

若要表示日期範圍，可使用日期 [range 欄位類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/range/)。
{: .note }

## 範例

建立一個含日期欄位與兩種日期格式的對應：

```json
PUT testindex
{
  "mappings" : {
    "properties" :  {
      "release_date" : {
        "type" : "date",
        "format" : "strict_date_optional_time||epoch_millis"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 參數

下表列出日期欄位類型接受的參數。所有參數皆為選用。

參數 | 說明 
:--- | :--- 
`boost` | 一個浮點數值，指定此欄位對相關性分數的權重。高於 1.0 的值會提高該欄位的相關性，介於 0.0 與 1.0 之間的值會降低該欄位的相關性。預設為 1.0。可動態更新。
`doc_values` | 一個布林值，指定是否應將該欄位儲存在磁碟上，以便用於彙總、排序或指令碼。預設為 `true`。
`format` | 解析日期所用的格式。預設為 `strict_date_optional_time||epoch_millis`。
`ignore_malformed` | 一個布林值，指定是否忽略格式錯誤的值而不擲回例外狀況。預設為 `false`。可動態更新。
`index` | 一個布林值，指定該欄位是否可供搜尋。預設為 `true`。對於使用可插拔資料格式的索引，預設為 `false`，且不支援 `true`。如需更多資訊，請參閱 [可插拔資料格式索引]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-parameter/#pluggable-data-format-indexes)。
`locale` | 依地區與語言表示日期的方式。預設為 [`ROOT`](https://docs.oracle.com/javase/8/docs/api/java/util/Locale.html#ROOT)（不因地區與語言而異的地區設定）。
`meta` | 接受此欄位的中繼資料。
[`null_value`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/index#null-value) | 用來取代 `null` 的值。必須與該欄位屬於相同類型。若未指定此參數，當欄位值為 `null` 時，該欄位會被視為遺失。預設為 `null`。
`print_format` | OpenSearch 在搜尋回應的 `fields` 與 `docvalue_fields` 區段、彙總鍵值以及衍生來源中回傳日期所用的格式。不影響 `_source` 中的日期，這些日期會依原本提供的方式回傳。預設為 `format` 中指定的第一種格式。
`skip_list` | 一個布林值，指定是否啟用 doc values 的跳躍清單索引。啟用後，OpenSearch 會建立已編製索引的 doc values，讓查詢引擎能略過不相關的文件範圍，從而改善 `range` 查詢的效能。`@timestamp` 欄位以及用於索引排序的欄位會自動啟用跳躍清單索引。對所有其他欄位，預設為 `false`。
`store` | 一個布林值，指定是否應儲存欄位值，並使其可與 `_source` 欄位分開擷取。預設為 `false`。 

## 格式

OpenSearch 內建多種日期格式，您也可以建立自己的自訂格式。您可以指定多種日期格式，並以 `||` 分隔。

## 預設格式

您可以選擇使用實驗性的預設日期格式 `strict_date_time_no_millis||strict_date_optional_time||epoch_millis`。若要使用此實驗性預設值，請將 `opensearch.experimental.optimization.datetime_formatter_caching.enabled` 功能旗標設為 `true`。如需啟用與停用功能旗標的更多資訊，請參閱 [啟用實驗性功能]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/experimental/)。

## 內建格式

大多數日期格式都有 `strict_` 對應版本。當格式以 `strict_` 開頭時，日期必須具有格式中指定的正確位數。例如，若格式設為 `strict_year_month_day`（`"yyyy-MM-dd"`），則月份與日期都必須是兩位數。因此 `"2020-06-09"` 是有效的，而 `"2020-6-9"` 則無效。

Epoch 定義為 1970 年 1 月 1 日 00:00:00 UTC。
{: .note }

y: 年<br>
Y: [週為基準的年份](https://en.wikipedia.org/wiki/ISO_8601#Week_dates)<br>
M: 月<br>
w: 一年中的序數[週](https://en.wikipedia.org/wiki/ISO_8601#Week_dates)，從 01 到 53<br> 
d: 日<br>
D: 一年中的序數日，從 001 到 365（閏年為 366）<br>
e: 一週中的序數日，從 1（星期一）到 7（星期日）<br>
H: 小時，從 0 到 23<br>
m: 分鐘<br>
s: 秒<br>
S: 秒的小數部分<br>
Z: 時區偏移（例如 +0400；-0400；-04:00）<br>
{: .note }

### 數值日期格式

格式名稱與說明 | 範例
:--- | :---
`epoch_millis` <br> 自 epoch 起算的毫秒數。最小值為 -2<sup>63</sup>。最大值為 2<sup>63</sup> &minus; 1。 | 1553391286000
`epoch_second` <br> 自 epoch 起算的秒數。最小值為 -2<sup>63</sup> &divide; 1000。最大值為 (2<sup>63</sup> &minus; 1) &divide; 1000。 | 1553391286

### 基本日期格式

基本日期格式的各組成部分之間不以分隔符號分隔。例如 "20190323"。

格式名稱與說明 | 模式與範例
:--- | :---
**日期**| 
`basic_date_time` <br> 以 `T` 分隔的基本日期與時間。 | `"yyyyMMdd`T`HHmmss.SSSZ"`<br>`"20190323T213446.123-04:00"`
`basic_date_time_no_millis` <br> 不含毫秒、以 `T` 分隔的基本日期與時間。 | `"yyyyMMdd`T`HHmmssZ"`<br>`"20190323T213446-04:00"`
`basic_date` <br> 四位數年份、兩位數月份與兩位數日期的日期。 | `"yyyyMMdd"<br>"20190323"` 
**時間** |
`basic_time` <br> 含兩位數小時、兩位數分鐘、兩位數秒、三位數毫秒以及時區偏移的時間。 |`"HHmmss.SSSZ"` <br> `"213446.123-04:00"`
`basic_time_no_millis` <br> 不含毫秒的基本時間。 | `"HHmmssZ"` <br> `"213446-04:00"`
**T 時間** | 
`basic_t_time` <br> 前面加上 `T` 的基本時間。 | `"`T`HHmmss.SSSZ"` <br> `"T213446.123-04:00"`
`basic_t_time_no_millis` <br> 前面加上 `T`、不含毫秒的基本時間。 | `"`T`HHmmssZ"` <br> `"T213446-04:00"`
**序數日期** |
`basic_ordinal_date_time` <br> 完整的序數日期與時間。 | `"yyyyDDD`T`HHmmss.SSSZ"`<br>`"2019082T213446.123-04:00"`
`basic_ordinal_date_time_no_millis` <br> 不含毫秒的完整序數日期與時間。 | `"yyyyDDD`T`HHmmssZ"`<br>`"2019082T213446-04:00"`
`basic_ordinal_date` <br> 四位數年份與三位數一年中序數日的日期。 | `"yyyyDDD"` <br> `"2019082"`
**週為基準的日期** | 
`basic_week_date_time` <br> `strict_basic_week_date_time` <br> 以 `T` 分隔的完整週為基準日期與時間。 | `"YYYY`W`wwe`T`HHmmss.SSSZ"` <br> `"2019W126213446.123-04:00"`
`basic_week_date_time_no_millis` <br> `strict_basic_week_date_time_no_millis` <br> 不含毫秒、以 `T` 分隔的基本週為基準年份日期與時間。 | `"YYYY`W`wwe`T`HHmmssZ"` <br> "2019W126213446-04:00"
`basic_week_date` <br> `strict_basic_week_date` <br> 含四位數週為基準年份、兩位數一年中序數週與一位數一週中序數日、以 `W` 分隔的完整週為基準日期。 | `"YYYY`W`wwe"` <br> `"2019W126"`

### 完整日期格式

完整日期格式的各個組成部分會以日期分隔符號 `-` 和時間分隔符號 `:` 分隔。例如，`"2019-03-23T21:34"`。

格式名稱與說明 | 模式與範例
:--- | :---
**日期** |
`date_optional_time`<br>`strict_date_optional_time` <br> 通用的完整日期與時間。年份為必要。月份、日與時間為選用。時間與日期以 `T` 分隔。 | 多種模式。<br>`"2019--03--23T21:34:46.123456789--04:00"` <br> `"2019-03-23T21:34:46"` <br> `"2019-03-23T21:34"` <br> `"2019"`
`strict_date_optional_time_nanos` <br>通用的完整日期與時間。年份為必要。月份、日與時間為選用。若指定時間，則必須包含時、分與秒，但秒的小數部分為選用。秒的小數部分長度為一至九位數，並具有奈秒解析度。時間與日期以 `T` 分隔。 | 多種模式。<br> `"2019-03-23T21:34:46.123456789-04:00"` <br> `"2019-03-23T21:34:46"` <br> `"2019"` 
`date_time` <br> `strict_date_time` <br> 以 `T` 分隔的完整日期與時間。 | `"yyyy-MM-dd`T`HH:mm:ss.SSSZ"` <br> `"2019-03-23T21:34:46.123-04:00"`
`date_time_no_millis` <br> `strict_date_time_no_millis` <br> 不含毫秒、以 `T` 分隔的完整日期與時間。 | `"yyyy-MM-dd'T'HH:mm:ssZ"` <br> `"2019-03-23T21:34:46-04:00"` 
`date_hour_minute_second_fraction` <br> `strict_date_hour_minute_second_fraction` <br> 以 `T` 分隔的完整日期、兩位數時、兩位數分、兩位數秒，以及一至九位數的秒的小數部分。 | `"yyyy-MM-dd`T`HH:mm:ss.SSSSSSSSS"`<br>`"2019-03-23T21:34:46.123456789"` <br> `"2019-03-23T21:34:46.1"`
`date_hour_minute_second_millis` <br> `strict_date_hour_minute_second_millis` <br> 以 `T` 分隔的完整日期、兩位數時、兩位數分、兩位數秒，以及三位數毫秒。 | `"yyyy-MM-dd`T`HH:mm:ss.SSS"` <br> `"2019-03-23T21:34:46.123"` 
`date_hour_minute_second` <br> `strict_date_hour_minute_second` <br> 以 `T` 分隔的完整日期、兩位數時、兩位數分與兩位數秒。| `"yyyy-MM-dd`T`HH:mm:ss"`<br>`"2019-03-23T21:34:46"`
`date_hour_minute` <br> `strict_date_hour_minute` <br> 完整日期、兩位數時與兩位數分。 | `"yyyy-MM-dd`T`HH:mm"` <br> `"2019-03-23T21:34"`
`date_hour` <br> `strict_date_hour` <br> 以 `T` 分隔的完整日期與兩位數時。 | `"yyyy-MM-dd`T`HH"` <br> `"2019-03-23T21"` 
`date` <br> `strict_date` <br> 四位數年份、兩位數月份與兩位數日。 | `"yyyy-MM-dd"` <br> `"2019-03-23"` 
`year_month_day` <br> `strict_year_month_day` <br> 四位數年份、兩位數月份與兩位數日。 | `"yyyy-MM-dd"` <br> `"2019-03-23"` 
`year_month` <br> `strict_year_month` <br> 四位數年份與兩位數月份。 | `"yyyy-MM"` <br> `"2019-03"` 
`year` <br> `strict_year` <br> 四位數年份。 | `"yyyy"` <br> `"2019"` 
`rfc3339_lenient` <br>與 RFC3339 相容的 DateTimeFormatter，其速度遠快於其他寬鬆的完整日期格式，例如 `strict_date_optional_time` | `"YYYY"` <br> `"2019"` <br> `"YYYY-MM"` <br> `"2019-03"` <br> `"YYYY-MM-DD"` <br> `"2019-03-23"` <br> `"YYYY-MM-DDThh:mmTZD"` <br> `"2019-03-23T21:34Z"` <br> `"YYYY-MM-DDThh:mm:ssTZD"` <br> `"2019-03-23T21:34:46Z"` <br> `"YYYY-MM-DDThh:mm:ss.sTZD"` <br> `"2019-03-23T21:34:46.123456789-04:00"` <br> `"YYYY-MM-DDThh:mm:ss,sTZD"` <br> `"2019-03-23T21:34:46,123456789-04:00"`
**時間** | 
`time` <br> `strict_time` <br> 兩位數時、兩位數分、兩位數秒、一至九位數的秒的小數部分，以及時區位移。 | `"HH:mm:ss.SSSSSSSSSZ"` <br> `"21:34:46.123456789-04:00"` <br> `"21:34:46.1-04:00"`
`time_no_millis` <br> `strict_time_no_millis` <br> 兩位數時、兩位數分、兩位數秒，以及時區位移。 | `"HH:mm:ssZ"` <br> `"21:34:46-04:00"` 
`hour_minute_second_fraction` <br> `strict_hour_minute_second_fraction` <br> 兩位數時、兩位數分、兩位數秒，以及一至九位數的秒的小數部分。 | `"HH:mm:ss.SSSSSSSSS"` <br> `"21:34:46.1"` <br> `"21:34:46.123456789"` 
`hour_minute_second_millis` <br> `strict_hour_minute_second_millis` <br> 兩位數時、兩位數分、兩位數秒，以及三位數毫秒。 | `"HH:mm:ss.SSS"` <br> `"21:34:46.123"` 
`hour_minute_second` <br> `strict_hour_minute_second` <br> 兩位數時、兩位數分與兩位數秒。 | `"HH:mm:ss"` <br> `"21:34:46"` 
`hour_minute` <br> `strict_hour_minute` <br> 兩位數時與兩位數分。 | `"HH:mm"` <br> `"21:34"` 
`hour` <br> `strict_hour` <br> 兩位數時。 | `"HH"` <br> `"21"` 
**T 時間** |
`t_time` <br> `strict_t_time` <br> 以 `T` 開頭的兩位數時、兩位數分、兩位數秒、一至九位數的秒的小數部分，以及時區位移。 | `"`T`HH:mm:ss.SSSSSSSSSZ"<br>"T21:34:46.123456789-04:00"` <br> `"T21:34:46.1-04:00"`
`t_time_no_millis` <br> `strict_t_time_no_millis` <br> 以 `T` 開頭的兩位數時、兩位數分、兩位數秒，以及時區位移。 | `"`T`HH:mm:ssZ"` <br> `"T21:34:46-04:00"`
**序數日期** |
`ordinal_date_time` <br> `strict_ordinal_date_time` <br> 以 `T` 分隔的完整序數日期與時間。 | `"yyyy-DDD`T`HH:mm:ss.SSSZ"` <br> `"2019-082T21:34:46.123-04:00"` 
`ordinal_date_time_no_millis` <br> `strict_ordinal_date_time_no_millis` <br> 不含毫秒、以 `T` 分隔的完整序數日期與時間。 | `"yyyy-DDD`T`HH:mm:ssZ"` <br> `"2019-082T21:34:46-04:00"`
`ordinal_date` <br> `strict_ordinal_date`<br> 包含四位數年份與三位數年度序數日的完整序數日期。 | `"yyyy-DDD"` <br> `"2019-082"`
**以週為基礎的日期** |
`week_date_time` <br> `strict_week_date_time` <br> 以 `T` 分隔的完整以週為基礎的日期與時間。週日期為四位數的以週為基礎的年份、兩位數的年度序數週，以及一位數的星期序數日。時間為兩位數時、兩位數分、兩位數秒、一至九位數的秒的小數部分，以及時區位移。 | `"YYYY-`W`ww-e`T`HH:mm:ss.SSSSSSSSSZ"` <br> `"2019-W12-6T21:34:46.1-04:00"` <br> `"2019-W12-6T21:34:46.123456789-04:00"`
`week_date_time_no_millis` <br> `strict_week_date_time_no_millis` <br> 不含毫秒、以 `T` 分隔的完整以週為基礎的日期與時間。週日期為四位數的以週為基礎的年份、兩位數的年度序數週，以及一位數的星期序數日。時間為兩位數時、兩位數分、兩位數秒，以及時區位移。 | `"YYYY-`W`ww-e`T`HH:mm:ssZ"` <br> `"2019-W12-6T21:34:46-04:00"`
`week_date` <br> `strict_week_date` <br> 包含四位數的以週為基礎的年份、兩位數的年度序數週，以及一位數的星期序數日的完整以週為基礎的日期。 | `"YYYY-`W`ww-e"` <br> `"2019-W12-6"`
`weekyear_week_day` <br> `strict_weekyear_week_day` <br> 四位數的以週為基礎的年份、兩位數的年度序數週，以及一位數的星期序數日。 | `"YYYY-'W'ww-e"` <br> `"2019-W12-6"` 
`weekyear_week` <br> `strict_weekyear_week` <br> 四位數的以週為基礎的年份與兩位數的年度序數週。 | `"YYYY-`W`ww"` <br> `"2019-W12"` 
`weekyear` <br> `strict_weekyear` <br> 四位數的以週為基礎的年份。 | `"YYYY"` <br> `"2019"` 

## 自訂格式

您可以為日期欄位建立自訂格式。例如，下列請求以常見的 `"MM/dd/yyyy"` 格式指定日期：

```json
PUT testindex
{
  "mappings" : {
    "properties" :  {
      "release_date" : {
        "type" : "date",
        "format" : "MM/dd/yyyy"
      }
    }
  }
}
```
{% include copy-curl.html %}

為含有日期的文件編製索引：

```json
PUT testindex/_doc/21 
{
  "release_date" : "03/21/2019"
}
```
{% include copy-curl.html %}

搜尋確切日期時，請以相同格式提供該日期：

```json
GET testindex/_search
{
  "query" : {
    "match": {
      "release_date" : {
        "query": "03/21/2019"
      }
    }
  }
}
```
{% include copy-curl.html %}

範圍查詢預設會使用欄位對應的格式。您也可以提供 `format` 參數，以不同格式指定日期範圍：

```json
GET testindex/_search
{
  "query": {
    "range": {
      "release_date": {
        "gte": "2019-01-01",
        "lte": "2019-12-31",
        "format": "yyyy-MM-dd"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 日期運算

date 欄位類型支援在查詢中使用日期運算來指定時間長度。例如，[範圍查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/range/)中的 `gt`、`gte`、`lt` 和 `lte` 參數，以及[日期範圍彙總]({{site.url}}{{site.baseurl}}/query-dsl/aggregations/bucket/date-range/)中的 `from` 和 `to` 參數，都接受日期運算運算式。

日期運算運算式包含一個固定日期，其後可選擇性地接上一或多個數學運算式。固定日期可以是 `now`（自 epoch 起算的毫秒數表示的目前日期與時間），或是以 `||` 結尾並指定日期的字串（例如 `2022-05-18||`）。日期必須採用[預設格式](#default-format)（預設為 `strict_date_time_no_millis||strict_date_optional_time||epoch_millis`）。

如果您在欄位對應中指定多種日期格式，OpenSearch 會使用第一種格式將自 epoch 起算的毫秒數值轉換為字串。<br>
如果欄位的對應中沒有指定格式，OpenSearch 會使用 `strict_date_optional_time` 格式將 epoch 值轉換為字串。
{: .note}

日期運算支援下列數學運算子。

運算子 | 說明 | 範例
:--- | :--- | :---
`+` | 加法 | `+1M`：加 1 個月。
`-` | 減法 | `-1y`：減 1 年。
`/` | 向下取整 | `/h`：向下取整至該小時的起點。

日期運算支援下列時間單位：

`y`：年<br>
`M`：月<br>
`w`：週<br>
`d`：日<br>
`h` 或 `H`：小時<br>
`m`：分鐘<br>
`s`：秒
{: .note }

### 運算式範例

下列範例運算式說明日期運算的用法：

- `now+1M`：自 epoch 起算的目前日期與時間（毫秒數），加 1 個月。
- `2022-05-18||/M`：`05/18/2022`，捨入至該月的開始。解析為 `2022-05-01`。
- `2022-05-18T15:23||/h`：`05/18/2022` 的 `15:23`，捨入至該小時的開始。解析為 `2022-05-18T15`。
- `2022-05-18T15:23:17.789||+2M-1d/d`：`05/18/2022` 的 `15:23:17.789` 加 2 個月減 1 天，捨入至該日的開始。解析為 `2022-07-17`。


### 在範圍查詢中使用日期運算

下列範例說明在[範圍查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/range/)中使用日期運算。

建立一個索引，其中 `release_date` 對應為 `date`：

```json
PUT testindex 
{
  "mappings" : {
    "properties" :  {
      "release_date" : {
        "type" : "date"
      }
    }
  }
}
```
{% include copy-curl.html %}

將兩份文件編製索引至該索引：

```json
PUT testindex/_doc/1
{
  "release_date": "2022-09-14"
}
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/2
{
  "release_date": "2022-11-15"
}
```
{% include copy-curl.html %}

下列查詢搜尋 `release_date` 介於 `09/14/2022` 當日的起點與其後 2 個月又 1 天之間的文件。範圍的下界會向下取整至 `09/14/2022` 當日的起點：

```json
GET testindex/_search
{
  "query": {
    "range": {
      "release_date": {
        "gte": "2022-09-14T15:23||/d",
        "lte": "2022-09-14||+2M+1d"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含這兩份文件：

```json
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "testindex",
        "_id" : "2",
        "_score" : 1.0,
        "_source" : {
          "release_date" : "2022-11-14"
        }
      },
      {
        "_index" : "testindex",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "release_date" : "2022-09-14"
        }
      }
    ]
  }
}
```

## 衍生來源

當索引使用 [衍生來源]({{site.url}}{{site.baseurl}}/field-types/metadata-fields/source/#derived-source) 時，OpenSearch 在重建來源時可能會排序多值日期欄位中的值。衍生來源會以 `print_format` 中指定的格式傳回日期。如果未指定 `print_format`，且 `format` 包含以 `||` 分隔的多種日期格式，衍生來源會以第一種格式傳回日期。

建立一個啟用衍生來源並設定具有多種格式的 `date` 欄位的索引：

```json
PUT sample-index1
{
  "settings": {
    "index": {
      "derived_source": {
        "enabled": true
      }
    }
  },
  "mappings": {
    "properties": {
      "date": {
        "type": "date",
        "format": "strict_date_time_no_millis||strict_date_optional_time||epoch_millis"
      }
    }
  }
}
```

將一份包含混合日期格式的文件編製索引至該索引：

```json
PUT sample-index1/_doc/1
{
  "date": [1758504860, "2025-09-22T00:34", "2025-09-22T01:34:20Z"]
}
```

在 OpenSearch 重建 `_source` 之後，所有日期都會是 `strict_date_time_no_millis` 格式：

```json
{
  "date": ["1970-01-21T08:28:24Z", "2025-09-22T00:34:00Z", "2025-09-22T01:34:20Z"]
}
```
