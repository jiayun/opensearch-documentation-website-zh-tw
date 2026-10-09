---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "範圍"
parent: Term-level queries
nav_order: 50
---

# 範圍查詢

您可以使用 `range` 查詢來搜尋某個欄位中的值範圍。

若要搜尋 `line_id` 值 >= 10 且 <= 20 的文件，請使用以下請求：

```json
GET shakespeare/_search
{
  "query": {
    "range": {
      "line_id": {
        "gte": 10,
        "lte": 20
      }
    }
  }
}
```
{% include copy-curl.html %}

## 運算子

範圍查詢中的欄位參數接受以下選用的運算子參數：

- `gte`：大於或等於
- `gt`：大於
- `lte`：小於或等於
- `lt`：小於

## 日期欄位

您可以對包含日期的欄位使用範圍查詢。例如，假設您有一個 `products` 索引，並想找出 2019 年新增的所有產品：

```json
GET products/_search
{
  "query": {
    "range": {
      "created": {
        "gte": "2019/01/01",
        "lte": "2019/12/31"
      }
    }
  }
}
```
{% include copy-curl.html %}

如需支援的日期格式的更多資訊，請參閱 [格式]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/date/#formats)。

### 格式

若要在查詢中使用與欄位對應格式不同的日期格式，請在 `format` 欄位中指定。

例如，如果 `products` 索引將 `created` 欄位對應為 `strict_date_optional_time`，您可以為查詢日期指定不同的格式，如下所示：

```json
GET /products/_search
{
  "query": {
    "range": {
      "created": {
        "gte": "01/01/2022",
        "lte": "31/12/2022",
        "format":"dd/MM/yyyy"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 缺少的日期組成部分

OpenSearch 會使用以下值填補缺少的日期組成部分：

- `MONTH_OF_YEAR`：`01`
- `DAY_OF_MONTH`：`01`
- `HOUR_OF_DAY`：`23`
- `MINUTE_OF_HOUR`：`59`
- `SECOND_OF_MINUTE`：`59`
- `NANO_OF_SECOND`：`999_999_999`

如果缺少年份，則不會填補。

例如，請考慮以下只在開始日期中指定年份的請求：

```json
GET /products/_search
{
  "query": {
    "range": {
      "created": {
        "gte": "2022",
        "lte": "2022-12-31"
      }
    }
  }
}
```
{% include copy-curl.html %}

開始日期會以預設值填補，因此使用的 `gte` 參數為 `2022-01-01T23:59:59.999999999Z`。

### 相對日期

您可以使用 [日期運算]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/date/#date-math) 來指定相對日期。

若要從指定日期減去 1 年又 1 天，請使用以下查詢：

```json
GET products/_search
{
  "query": {
    "range": {
      "created": {
        "gte": "2019/01/01||-1y-1d"
      }
    }
  }
}
```
{% include copy-curl.html %}

在前面的範例中，`2019/01/01` 是日期運算的錨定日期（起點）。在兩個直立線符號（`||`）之後，您指定的是相對於錨定日期的數學運算式。在此範例中，您減去了 1 年（`-1y`）和 1 天（`-1d`）。

您也可以在日期或時間單位後加上斜線來將日期捨入。

若要找出過去一年內（以月為單位捨入）新增的產品，請使用以下查詢：

```json
GET products/_search
{
  "query": {
    "range": {
      "created": {
        "gte": "now-1y/M"
      }
    }
  }
}
```
{% include copy-curl.html %}

關鍵字 `now` 代表目前的日期與時間。
{: .tip}

### 相對日期的捨入

下表指定相對日期的捨入方式。

參數 | 捨入規則 | 範例：值 `2022-05-18||/M` 捨入為
:--- | :--- | :---
`gt` | 向上捨入至不在捨入區間內的第一個毫秒。 | `2022-06-01T00:00:00.000`
`gte` | 向下捨入至第一個毫秒。 | `2022-05-01T00:00:00.000`
`lt` | 向下捨入至捨入日期之前的最後一個毫秒。 | `2022-04-30T23:59:59.999`
`lte` | 向上捨入至捨入區間內的最後一個毫秒。 | `2022-05-31T23:59:59.999`

### 時區

預設情況下，系統會假設日期採用 [世界協調時間（UTC）](https://en.wikipedia.org/wiki/Coordinated_Universal_Time)。如果您在查詢中指定 `time_zone` 參數，提供的日期值會轉換為 UTC。您可以將 `time_zone` 參數指定為 [UTC 偏移](https://en.wikipedia.org/wiki/UTC_offset)，例如 `-04:00`，或 [IANA 時區 ID](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)，例如 `America/New_York`。例如，以下查詢指定查詢中提供的 `gte` 日期位於 `-04:00` 時區：

```json
GET /products/_search
{
  "query": {
    "range": {
      "created": {
        "time_zone": "-04:00",
        "gte": "2022-04-17T06:00:00"
      }
    }
  }
}
```
{% include copy-curl.html %}

前面查詢中的 `gte` 參數會轉換為 `2022-04-17T10:00:00 UTC`，這是 `2022-04-17T06:00:00-04:00` 的 UTC 對應值。

`time_zone` 參數不會影響 `now` 值，因為 `now` 一律對應於 UTC 的目前系統時間。
{: .note}

## 參數

此查詢接受欄位名稱（`<field>`）作為頂層參數：

```json
GET _search
{
  "query": {
    "range": {
      "<field>": {
        "gt": 10,
        ...
      }
    }
  }
}
```
{% include copy-curl.html %}


除了[運算子](#operators)之外，您還可以為 `<field>` 指定以下選用參數。

參數 | 資料類型 | 描述
:--- | :--- | :---
`format` | 字串 | 此查詢中日期的[格式]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/date/#formats)。預設為欄位的對應格式。
`relation` | 字串 | 指示範圍查詢如何比對 [`range`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/range/) 欄位的值。有效值為：<br> - `INTERSECTS`（預設）：比對 `range` 欄位值與查詢中提供的範圍相交的文件。  <br> - `CONTAINS`：比對 `range` 欄位值包含查詢中提供的整個範圍的文件。 <br> - `WITHIN`：比對 `range` 欄位值完全位於查詢中提供的範圍內的文件。
`boost` | 浮點數 | 指定此欄位對相關性分數權重的浮點數值。高於 1.0 的值會提高該欄位的相關性；介於 0.0 與 1.0 之間的值會降低該欄位的相關性。預設為 1.0。
`time_zone` | 字串 | 在查詢中用於將 [`date`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/date/) 值轉換為 UTC 的時區。有效值為 ISO 8601 [UTC 偏移](https://en.wikipedia.org/wiki/List_of_UTC_offsets)和 [IANA 時區 ID](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)。如需更多資訊，請參閱[時區](#time-zone)。

如果 [`search.allow_expensive_queries`]({{site.url}}{{site.baseurl}}/query-dsl/index/#expensive-queries) 設定為 `false`，則不會對 [`text`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/text/) 和 [`keyword`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/keyword/) 欄位執行範圍查詢。
{: .important}
