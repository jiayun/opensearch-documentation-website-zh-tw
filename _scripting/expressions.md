---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Lucene 表達式語言"
nav_order: 40
---

# Lucene 表達式語言

`expression` 語言會將單一 JavaScript 表達式編譯成 JVM 位元組碼。它會對 doc values 評估數值公式，且不支援陳述式、變數宣告或字串處理。

表達式會在編譯時解析為直接的 doc values 存取器，因此對單一文件評估表達式會簡化為算術運算，不需要類型解析、對應表查閱或方法分派。若某個公式同時可用 Lucene 表達式語言和 [Painless]({{site.url}}{{site.baseurl}}/scripting/painless/) 表達，通常以表達式執行會比以 Painless 指令碼執行更快。

此語言採用沙箱機制，且預設會為行內指令碼和已儲存的指令碼啟用，可用於 `score`、`field`、`filter`、`number_sort`、`aggs`、`bucket_aggregation`、`aggregation_selector` 和 `terms_set` 情境。將 `lang` 設為 `expression` 即可選用此語言。

## 語法

表達式指令碼由單一表達式組成，該表達式會評估為數字，而條件運算子 `?:` 是其唯一的控制流程形式。表達式可以使用 JavaScript 的算術、比較和位元運算子，以及 [Lucene expressions 模組](https://lucene.apache.org/core/10_5_0/expressions/org/apache/lucene/expressions/js/package-summary.html) 中的函式，包括 `abs`、`min`、`max`、`sqrt`、`pow`、`log`、三角函式，以及用於地理距離的 `haversin`。

表達式可以參照下列值：

- 文件欄位，透過 `doc['field_name'].value`。
- 欄位的屬性或方法，例如 `doc['field_name'].empty` 或 `doc['field_name'].sum()`。
- 指令碼參數，僅以其名稱參照。表達式會以 `discount` 參照參數，而非 `params.discount`；使用 `params` 前置字元會失敗並出現 `Unknown variable [params]`。
- 相關性分數 `_score`，僅在 `script_score` 情境中可用。

參照參數時不加 `params` 前置字元，是將指令碼從 Painless 移至 `expression` 時最容易被忽略的語法差異。
{: .tip}

## 數值欄位 API

下表列出數值欄位可用的屬性和方法。

表達式 | 說明
:--- | :---
`doc['field_name'].value` | 欄位的值，以 `double` 傳回。
`doc['field_name'].empty` | 此文件中該欄位是否沒有值。
`doc['field_name'].length` | 此文件中該欄位具有的值的數量。
`doc['field_name'].min()` | 此文件中該欄位值的最小值。
`doc['field_name'].max()` | 此文件中該欄位值的最大值。
`doc['field_name'].median()` | 此文件中該欄位值的中位數。
`doc['field_name'].avg()` | 此文件中該欄位值的平均值。
`doc['field_name'].sum()` | 此文件中該欄位值的總和。

文件中不存在的欄位會評估為 `0`。若要替換為不同的值，請先測試 `empty`，例如 `doc['ratings'].empty ? 3 : doc['ratings'].value`。

多值欄位會評估為其最小值。若要選取不同的值，請呼叫對應的方法，例如 `doc['ratings'].sum()`。

布林值欄位會以數字呈現，其中 `true` 為 `1`，`false` 為 `0`，因此布林值可以直接控制計算：`doc['on_sale'].value ? doc['price'].value - doc['price'].value * discount : doc['price'].value`。

下列搜尋會傳回每個產品的平均評分，並為唯一沒有評分的產品替換為 `-1`。它使用 `scripting-products` 索引，該索引建立於 [測試設定]({{site.url}}{{site.baseurl}}/scripting/using-scripts/#test-setup)：

```json
GET scripting-products/_search
{
  "_source": ["name"],
  "sort": [{ "sku": "asc" }],
  "script_fields": {
    "average_rating": {
      "script": {
        "lang": "expression",
        "source": "doc['ratings'].empty ? unrated : doc['ratings'].avg()",
        "params": { "unrated": -1 }
      }
    }
  }
}
```
{% include copy-curl.html %}

超寬螢幕顯示器沒有 `ratings` 值，會傳回替代值：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "took": 71,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "scripting-products",
        "_id": "3",
        "_score": null,
        "_source": {
          "name": "Mechanical keyboard"
        },
        "fields": {
          "average_rating": [
            5.0
          ]
        },
        "sort": [
          "ACC-2001"
        ]
      },
      {
        "_index": "scripting-products",
        "_id": "1",
        "_score": null,
        "_source": {
          "name": "Wireless noise cancelling headphones"
        },
        "fields": {
          "average_rating": [
            4.25
          ]
        },
        "sort": [
          "AUD-1001"
        ]
      },
      {
        "_index": "scripting-products",
        "_id": "2",
        "_score": null,
        "_source": {
          "name": "Wireless earbuds"
        },
        "fields": {
          "average_rating": [
            4.0
          ]
        },
        "sort": [
          "AUD-1002"
        ]
      },
      {
        "_index": "scripting-products",
        "_id": "4",
        "_score": null,
        "_source": {
          "name": "Ultrawide monitor"
        },
        "fields": {
          "average_rating": [
            -1.0
          ]
        },
        "sort": [
          "DSP-3001"
        ]
      }
    ]
  }
}
```
</details>

表達式傳回的每個值都是 `double`，這就是為什麼評分會顯示為 `5.0` 和 `-1.0`，而非整數。

## 日期欄位 API

日期欄位會以自 Unix 紀元以來經過的毫秒數呈現，因此整個數值欄位 API 都適用於它。此外，`date` 屬性可存取個別的日曆元件。

下表列出日期欄位可用的元件。

表達式 | 說明
:--- | :---
`doc['field_name'].date.centuryOfEra` | 世紀，從 1 到 2920000。
`doc['field_name'].date.dayOfMonth` | 月中的日，從 1 到 31。
`doc['field_name'].date.dayOfWeek` | 星期幾，從 1 代表星期一，到 7 代表星期日。
`doc['field_name'].date.dayOfYear` | 一年中的第幾天，其中 1 月 1 日為 1。
`doc['field_name'].date.era` | 紀元，其中 `0` 為西元前，`1` 為西元。
`doc['field_name'].date.hourOfDay` | 小時，從 0 到 23。
`doc['field_name'].date.millisOfDay` | 當天經過的毫秒數，從 0 到 86399999。
`doc['field_name'].date.millisOfSecond` | 秒內經過的毫秒數，從 0 到 999。
`doc['field_name'].date.minuteOfDay` | 當天經過的分鐘數，從 0 到 1439。
`doc['field_name'].date.minuteOfHour` | 分鐘，從 0 到 59。
`doc['field_name'].date.monthOfYear` | 月份，從 1 代表 1 月，到 12 代表 12 月。
`doc['field_name'].date.secondOfDay` | 當天經過的秒數，從 0 到 86399。
`doc['field_name'].date.secondOfMinute` | 秒，從 0 到 59。
`doc['field_name'].date.year` | 年份，從 -292000000 到 292000000。
`doc['field_name'].date.yearOfCentury` | 世紀內的年份，從 1 到 100。
`doc['field_name'].date.yearOfEra` | 紀元內的年份，從 1 到 292000000。

若要找出兩個日期欄位之間的整年年數，請將它們的年份相減：`doc['release_date'].date.year - doc['discontinued_date'].date.year`。

## 地理點欄位 API

下表列出 [`geo_point`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-point/) 欄位可用的屬性。

表達式 | 說明
:--- | :---
`doc['field_name'].empty` | 此文件中該欄位是否沒有值。
`doc['field_name'].lat` | 該點的緯度。
`doc['field_name'].lon` | 該點的經度。

將這些與 `haversin` 結合，即可計算以公里為單位的大圓距離。下列搜尋會依產品倉庫與華盛頓特區的距離排序產品，並以參數提供原點，讓同一個已編譯的指令碼可服務每個使用者的位置：

```json
GET scripting-products/_search
{
  "_source": ["name", "warehouse"],
  "sort": {
    "_script": {
      "type": "number",
      "script": {
        "lang": "expression",
        "source": "haversin(lat, lon, doc['warehouse'].lat, doc['warehouse'].lon)",
        "params": { "lat": 38.9072, "lon": -77.0369 }
      },
      "order": "asc"
    }
  }
}
```
{% include copy-curl.html %}

每個結果上的 `sort` 值是計算出的距離，以公里為單位：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "took": 12,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "scripting-products",
        "_id": "3",
        "_score": null,
        "_source": {
          "name": "Mechanical keyboard",
          "warehouse": { "lon": -87.6298, "lat": 41.8781 }
        },
        "sort": [
          955.1850203827704
        ]
      },
      {
        "_index": "scripting-products",
        "_id": "4",
        "_score": null,
        "_source": {
          "name": "Ultrawide monitor",
          "warehouse": { "lon": -97.7431, "lat": 30.2672 }
        },
        "sort": [
          2118.1759666556795
        ]
      },
      {
        "_index": "scripting-products",
        "_id": "1",
        "_score": null,
        "_source": {
          "name": "Wireless noise cancelling headphones",
          "warehouse": { "lon": -122.3321, "lat": 47.6062 }
        },
        "sort": [
          3736.260216407672
        ]
      },
      {
        "_index": "scripting-products",
        "_id": "2",
        "_score": null,
        "_source": {
          "name": "Wireless earbuds",
          "warehouse": { "lon": -122.4194, "lat": 37.7749 }
        },
        "sort": [
          3918.550756602828
        ]
      }
    ]
  }
}
```
</details>

## 限制

`expression` 語言有下列限制：

- 僅可讀取數值、布林值、日期和 `geo_point` 欄位，因此表達式無法比較或串連字串。讀取 `keyword` 欄位會失敗並出現由 `Field [sku] must be numeric, date, or geopoint` 造成的 `link error`。在 `text` 欄位上啟用 [`fielddata`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/field-data/) 可讓它在 Painless 中可讀取，但在表達式中則不行，且會回報相同的錯誤。
- 已儲存的欄位和 `_source` 無法使用，因此表達式無法讀取不在 doc values 中的值。兩者都是透過 `params` 存取，而表達式不會收到它，因此 `params._source` 和 `params._fields` 會失敗並出現 `Unknown variable [params]`。
- 無法測試欄位是否存在於對應中。`doc['field'].empty` 只會回報已對應的欄位在目前文件中是否有值。參照未對應的欄位會失敗並出現由 `Field [discount] does not exist in mappings` 造成的 `link error`，而將該參照包在 `empty` 中也會產生相同的失敗。
- 每個結果都是 `double`，因此表達式無法傳回字串、布林值或結構化值。

當公式需要上述任一項時，請改用 [Painless]({{site.url}}{{site.baseurl}}/scripting/painless/)。

## 相關文件

- [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)
- [在指令碼中存取文件欄位]({{site.url}}{{site.baseurl}}/scripting/accessing-fields/)
- [如何使用指令碼]({{site.url}}{{site.baseurl}}/scripting/using-scripts/)
