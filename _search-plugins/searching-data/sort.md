---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "排序結果"
parent: Customizing search results
nav_order: 30
redirect_from:
  - /opensearch/search/sort/
---

# 排序結果

排序可讓使用者以對自己最有意義的方式排序結果。

預設情況下，全文查詢會依相關性分數排序結果。
您可以設定 `order` 參數為 `asc` 或 `desc`，選擇依任何欄位值以遞增或遞減順序排序結果。如果您未指定 `order`，依 `_score` 排序時結果會以遞減順序排列，依其他任何欄位排序時則以遞增順序排列。

例如，若要依 `line_id` 值的遞減順序排序結果，請使用下列查詢：

```json
GET shakespeare/_search
{
  "query": {
    "term": {
      "play_name": {
        "value": "Henry IV"
      }
    }
  },
  "sort": [
    {
      "line_id": {
        "order": "desc"
      }
    }
  ]
}
```
{% include copy-curl.html %}

結果會依 `line_id` 以遞減順序排序：

```json
{
  "took" : 24,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3205,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [
      {
        "_index" : "shakespeare",
        "_id" : "3204",
        "_score" : null,
        "_source" : {
          "type" : "line",
          "line_id" : 3205,
          "play_name" : "Henry IV",
          "speech_number" : 8,
          "line_number" : "",
          "speaker" : "KING HENRY IV",
          "text_entry" : "Exeunt"
        },
        "sort" : [
          3205
        ]
      },
      {
        "_index" : "shakespeare",
        "_id" : "3203",
        "_score" : null,
        "_source" : {
          "type" : "line",
          "line_id" : 3204,
          "play_name" : "Henry IV",
          "speech_number" : 8,
          "line_number" : "5.5.45",
          "speaker" : "KING HENRY IV",
          "text_entry" : "Let us not leave till all our own be won."
        },
        "sort" : [
          3204
        ]
      },
      {
        "_index" : "shakespeare",
        "_id" : "3202",
        "_score" : null,
        "_source" : {
          "type" : "line",
          "line_id" : 3203,
          "play_name" : "Henry IV",
          "speech_number" : 8,
          "line_number" : "5.5.44",
          "speaker" : "KING HENRY IV",
          "text_entry" : "And since this business so fair is done,"
        },
        "sort" : [
          3203
        ]
      },
      {
        "_index" : "shakespeare",
        "_id" : "3201",
        "_score" : null,
        "_source" : {
          "type" : "line",
          "line_id" : 3202,
          "play_name" : "Henry IV",
          "speech_number" : 8,
          "line_number" : "5.5.43",
          "speaker" : "KING HENRY IV",
          "text_entry" : "Meeting the cheque of such another day:"
        },
        "sort" : [
          3202
        ]
      },
      {
        "_index" : "shakespeare",
        "_id" : "3200",
        "_score" : null,
        "_source" : {
          "type" : "line",
          "line_id" : 3201,
          "play_name" : "Henry IV",
          "speech_number" : 8,
          "line_number" : "5.5.42",
          "speaker" : "KING HENRY IV",
          "text_entry" : "Rebellion in this land shall lose his sway,"
        },
        "sort" : [
          3201
        ]
      },
      {
        "_index" : "shakespeare",
        "_id" : "3199",
        "_score" : null,
        "_source" : {
          "type" : "line",
          "line_id" : 3200,
          "play_name" : "Henry IV",
          "speech_number" : 8,
          "line_number" : "5.5.41",
          "speaker" : "KING HENRY IV",
          "text_entry" : "To fight with Glendower and the Earl of March."
        },
        "sort" : [
          3200
        ]
      },
      {
        "_index" : "shakespeare",
        "_id" : "3198",
        "_score" : null,
        "_source" : {
          "type" : "line",
          "line_id" : 3199,
          "play_name" : "Henry IV",
          "speech_number" : 8,
          "line_number" : "5.5.40",
          "speaker" : "KING HENRY IV",
          "text_entry" : "Myself and you, son Harry, will towards Wales,"
        },
        "sort" : [
          3199
        ]
      },
      {
        "_index" : "shakespeare",
        "_id" : "3197",
        "_score" : null,
        "_source" : {
          "type" : "line",
          "line_id" : 3198,
          "play_name" : "Henry IV",
          "speech_number" : 8,
          "line_number" : "5.5.39",
          "speaker" : "KING HENRY IV",
          "text_entry" : "Who, as we hear, are busily in arms:"
        },
        "sort" : [
          3198
        ]
      },
      {
        "_index" : "shakespeare",
        "_id" : "3196",
        "_score" : null,
        "_source" : {
          "type" : "line",
          "line_id" : 3197,
          "play_name" : "Henry IV",
          "speech_number" : 8,
          "line_number" : "5.5.38",
          "speaker" : "KING HENRY IV",
          "text_entry" : "To meet Northumberland and the prelate Scroop,"
        },
        "sort" : [
          3197
        ]
      },
      {
        "_index" : "shakespeare",
        "_id" : "3195",
        "_score" : null,
        "_source" : {
          "type" : "line",
          "line_id" : 3196,
          "play_name" : "Henry IV",
          "speech_number" : 8,
          "line_number" : "5.5.37",
          "speaker" : "KING HENRY IV",
          "text_entry" : "Towards York shall bend you with your dearest speed,"
        },
        "sort" : [
          3196
        ]
      }
    ]
  }
}
```

`sort` 參數是一個陣列，因此您可以依優先順序指定多個欄位值。

如果您有兩個欄位的 `line_id` 值相同，OpenSearch 會使用 `speech_number`，也就是排序的第二個選項：

```json
GET shakespeare/_search
{
  "query": {
    "term": {
      "play_name": {
        "value": "Henry IV"
      }
    }
  },
  "sort": [
    {
      "line_id": {
        "order": "desc"
      }
    },
    {
      "speech_number": {
        "order": "desc"
      }
    }
  ]
}
```
{% include copy-curl.html %}

您可以繼續依任意數量的欄位值排序，以取得正確順序的結果。不必是數值——您也可以依日期或時間戳記欄位排序：

```json
"sort": [
    {
      "date": {
        "order": "desc"
      }
    }
  ]
```
{% include copy-curl.html %}

經過分析的文字欄位無法用來排序文件，因為反向索引只包含個別斷詞後的詞元，而不是完整字串。例如，您無法依 `play_name` 排序。

若要繞過此限制，您可以使用對應為 keyword 類型的文字欄位原始版本。在下列範例中，`play_name.keyword` 未經分析，因此您擁有完整原始版本的副本可用於排序：

```json
GET shakespeare/_search
{
  "query": {
    "term": {
      "play_name": {
        "value": "Henry IV"
      }
    }
  },
  "sort": [
    {
      "play_name.keyword": {
        "order": "desc"
      }
    }
  ]
}
```
{% include copy-curl.html %}

結果會依 `play_name` 欄位以字母順序排序。

搭配 [`search_after` 參數]({{site.url}}{{site.baseurl}}/opensearch/search/paginate#the-search_after-parameter) 使用 `sort` 可實現更有效率的捲動。
結果會從您在 `search_after` 陣列中指定的排序值之後的文件開始。

請確保 `search_after` 陣列中的值數量與 `sort` 陣列相同，且以相同方式排序。
在此情況下，您請求的是從 `line_id = 3202` 和 `speech_number = 8` 之後的文件開始的結果：

```json
GET shakespeare/_search
{
  "query": {
    "term": {
      "play_name": {
        "value": "Henry IV"
      }
    }
  },
  "sort": [
    {
      "line_id": {
        "order": "desc"
      }
    },
    {
      "speech_number": {
        "order": "desc"
      }
    }
  ],
  "search_after": [
    "3202",
    "8"
  ]
}
```
{% include copy-curl.html %}

## 排序模式

排序模式適用於依陣列或多值欄位排序。它指定應選擇哪個陣列值來排序文件。對於包含數字陣列的數值欄位，您可以使用 `avg`、`sum` 或 `median` 模式排序。若要依最小值或最大值排序，請使用 `min` 或 `max` 模式，這些模式同時適用於數值和字串資料類型。

預設模式在遞增排序時為 `min`，在遞減排序時為 `max`。

下列範例說明如何使用排序模式依陣列欄位排序。

假設有一個儲存學生成績的索引。將兩份文件編製索引至該索引：

```json
PUT students/_doc/1
{
   "name": "John Doe",
   "grades": [70, 90]
}
```
{% include copy-curl.html %}

```json
PUT students/_doc/2
{
   "name": "Mary Major",
   "grades": [80, 100]
}
```
{% include copy-curl.html %}

使用 `avg` 模式，依最高平均成績排序所有學生：

```json
GET students/_search
{
   "query" : {
      "match_all": {}
   },
   "sort" : [
      {"grades" : {"order" : "desc", "mode" : "avg"}}
   ]
}
```
{% include copy-curl.html %}

回應包含依 `grades` 遞減排序的學生：

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
    "max_score" : null,
    "hits" : [
      {
        "_index" : "students",
        "_id" : "2",
        "_score" : null,
        "_source" : {
          "name" : "Mary Major",
          "grades" : [
            80,
            100
          ]
        },
        "sort" : [
          90
        ]
      },
      {
        "_index" : "students",
        "_id" : "1",
        "_score" : null,
        "_source" : {
          "name" : "John Doe",
          "grades" : [
            70,
            90
          ]
        },
        "sort" : [
          80
        ]
      }
    ]
  }
}
```

## 跨索引排序數值欄位

當您搜尋多個索引時，同一個欄位在每個索引中可能對應到不同的數值或日期類型。使用 `numeric_type` 選項可將所有索引的排序值轉換為單一類型。有效值為 `double`、`long`、`date` 和 `date_nanos`。

例如，`prices-eu` 索引將 `price` 對應為 `double`，而 `prices-us` 索引將其對應為 `long`：

```json
PUT /prices-eu
{
  "mappings": {
    "properties": {
      "product": { "type": "keyword" },
      "price": { "type": "double" }
    }
  }
}
```
{% include copy-curl.html %}

```json
PUT /prices-us
{
  "mappings": {
    "properties": {
      "product": { "type": "keyword" },
      "price": { "type": "long" }
    }
  }
}
```
{% include copy-curl.html %}

將文件編製索引至這兩個索引：

```json
POST /_bulk?refresh=true
{ "index": { "_index": "prices-eu", "_id": "1" } }
{ "product": "tent", "price": 129.5 }
{ "index": { "_index": "prices-eu", "_id": "2" } }
{ "product": "lantern", "price": 24.99 }
{ "index": { "_index": "prices-us", "_id": "1" } }
{ "product": "stove", "price": 60 }
{ "index": { "_index": "prices-us", "_id": "2" } }
{ "product": "backpack", "price": 95 }
```
{% include copy-curl.html %}

若未使用 `numeric_type`，每筆命中的排序值會保留其索引的類型，例如來自 `prices-eu` 的 `24.99` 以及來自 `prices-us` 的 `60`。下列請求會將所有排序值轉換為 `double`：

```json
GET /prices-eu,prices-us/_search
{
  "sort": [
    {
      "price": {
        "order": "asc",
        "numeric_type": "double"
      }
    }
  ]
}
```
{% include copy-curl.html %}

`prices-us` 文件的排序值會以 `60.0` 和 `95.0` 傳回：

```json
{
  ...
  "hits": {
    ...
    "hits": [
      {
        "_index": "prices-eu",
        "_id": "2",
        "_score": null,
        "_source": {
          "product": "lantern",
          "price": 24.99
        },
        "sort": [
          24.99
        ]
      },
      {
        "_index": "prices-us",
        "_id": "1",
        "_score": null,
        "_source": {
          "product": "stove",
          "price": 60
        },
        "sort": [
          60.0
        ]
      },
      {
        "_index": "prices-us",
        "_id": "2",
        "_score": null,
        "_source": {
          "product": "backpack",
          "price": 95
        },
        "sort": [
          95.0
        ]
      },
      {
        "_index": "prices-eu",
        "_id": "1",
        "_score": null,
        "_source": {
          "product": "tent",
          "price": 129.5
        },
        "sort": [
          129.5
        ]
      }
    ]
  }
}
```

如果您指定 `long`，小數值會被截斷。例如，`129.5` 和 `24.99` 會以 `129` 和 `24` 傳回，而僅小數部分不同的文件會排序為相等。

### 排序日期與奈秒日期欄位

`date` 欄位以毫秒儲存值，而 `date_nanos` 欄位以奈秒儲存值。如果排序欄位在某個索引中對應為 `date`，而在另一個索引中對應為 `date_nanos`，OpenSearch 會直接比較原始值，不會將其轉換為相同的解析度。因此，以遞增順序排序時，`date_nanos` 索引中的文件會排在 `date` 索引的所有文件之後，無論其時間戳記為何。

例如，建立一個 `events-ms` 索引，將 `ts` 對應為 `date`，並建立一個 `events-ns` 索引，將其對應為 `date_nanos`：

```json
PUT /events-ms
{
  "mappings": {
    "properties": {
      "ts": { "type": "date" }
    }
  }
}
```
{% include copy-curl.html %}

```json
PUT /events-ns
{
  "mappings": {
    "properties": {
      "ts": { "type": "date_nanos" }
    }
  }
}
```
{% include copy-curl.html %}

將三個事件編製索引。`events-ns` 中的 `upload` 事件發生於 11:00，介於 `events-ms` 中的 `login`（10:00）與 `logout`（12:00）事件之間：

```json
POST /_bulk?refresh=true
{ "index": { "_index": "events-ms", "_id": "1" } }
{ "event": "login", "ts": "2026-10-13T10:00:00Z" }
{ "index": { "_index": "events-ms", "_id": "2" } }
{ "event": "logout", "ts": "2026-10-13T12:00:00Z" }
{ "index": { "_index": "events-ns", "_id": "1" } }
{ "event": "upload", "ts": "2026-10-13T11:00:00.123456789Z" }
```
{% include copy-curl.html %}

對 `ts` 進行預設的遞增排序，會依序傳回 `login`、`logout`，然後是 `upload`。

若要依時間先後順序排序事件，請將 `numeric_type` 設為 `date` 或 `date_nanos`。`date` 值會將所有值轉換為毫秒，而 `date_nanos` 會將其轉換為奈秒：

```json
GET /events-ms,events-ns/_search
{
  "_source": ["event"],
  "sort": [
    {
      "ts": {
        "order": "asc",
        "numeric_type": "date_nanos"
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應會依時間先後順序傳回事件：

```json
{
  ...
  "hits": {
    ...
    "hits": [
      {
        "_index": "events-ms",
        "_id": "1",
        "_score": null,
        "_source": {
          "event": "login"
        },
        "sort": [
          1791885600000000000
        ]
      },
      {
        "_index": "events-ns",
        "_id": "1",
        "_score": null,
        "_source": {
          "event": "upload"
        },
        "sort": [
          1791889200123456789
        ]
      },
      {
        "_index": "events-ms",
        "_id": "2",
        "_score": null,
        "_source": {
          "event": "logout"
        },
        "sort": [
          1791892800000000000
        ]
      }
    ]
  }
}
```

奈秒值只能表示 1970 年至 2262 年之間的日期。如果 `date` 欄位包含超出此範圍的值，使用 `date_nanos` 進行轉換時，包含該文件的分片會發生失敗。搜尋隨後會傳回部分結果，並在回應的 `_shards.failures` 陣列中回報此失敗。若要排序包含這類日期的資料，請使用 `"numeric_type": "date"`。
{: .warning}

## 排序巢狀物件

排序[巢狀]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/)物件時，請提供 `path` 參數，指定要排序之欄位的路徑。

例如，在索引 `students` 中，將變數 `first_sem` 對應為 `nested`：

```json
PUT students
{
  "mappings" : {
    "properties": {
      "first_sem": { 
        "type" : "nested"
      }
    }
  }
}
```
{% include copy-curl.html %}

為兩份包含巢狀欄位的文件編製索引：

```json
PUT students/_doc/1
{
   "name": "John Doe",
   "first_sem" : {
     "grades": [70, 90]
   }
}
```
{% include copy-curl.html %}

```json
PUT students/_doc/2
{
  "name": "Mary Major",
  "first_sem": {
    "grades": [80, 100]
  }
}
```
{% include copy-curl.html %}

依平均成績排序時，請提供巢狀欄位的路徑：

```json
GET students/_search
{
 "query" : {
    "match_all": {}
 },
 "sort" : [
    {"first_sem.grades": {
      "order" : "desc", 
      "mode" : "avg",
      "nested": {
        "path": "first_sem"
     }
    }
    }
 ]
}
```
{% include copy-curl.html %}

`nested` 物件接受下列參數。

參數 | 說明
:--- | :---
`path` | 包含排序欄位之巢狀物件的路徑。必要。
`filter` | 一個查詢，用於選取其值將用於排序的巢狀物件。不符合篩選條件的巢狀物件會被忽略。一般而言，您會在此重複搜尋查詢的巢狀條件，讓文件僅依符合條件之巢狀物件的值排序。
`max_children` | 計算排序值時，每份文件最多考慮的巢狀物件數量。預設會考慮所有巢狀物件。
`nested` | 一個 `nested` 物件，用於排序巢狀物件內部又再巢狀一層的物件中的欄位。請指定內層的 `path`，並可選擇性地指定其自身的 `filter` 與 `max_children`。

例如，在下列索引中，每個產品都包含一個帶有區域與價格的巢狀 `offers` 物件，而每個優惠都包含一個巢狀的 `discounts` 物件：

```json
PUT sort-offers
{
  "mappings": {
    "properties": {
      "product": { "type": "keyword" },
      "offers": {
        "type": "nested",
        "properties": {
          "region": { "type": "keyword" },
          "price": { "type": "double" },
          "discounts": {
            "type": "nested",
            "properties": {
              "percent": { "type": "integer" }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

為兩個產品編製索引：

```json
POST _bulk?refresh=true
{ "index": { "_index": "sort-offers", "_id": "1" } }
{ "product": "tent", "offers": [ { "region": "eu", "price": 120, "discounts": [ { "percent": 5 }, { "percent": 15 } ] }, { "region": "us", "price": 90, "discounts": [ { "percent": 10 } ] } ] }
{ "index": { "_index": "sort-offers", "_id": "2" } }
{ "product": "stove", "offers": [ { "region": "eu", "price": 100, "discounts": [ { "percent": 20 } ] }, { "region": "us", "price": 140, "discounts": [ { "percent": 0 } ] } ] }
```
{% include copy-curl.html %}

下列請求依產品在 `eu` 區域的最低價格排序。`filter` 會排除 `us` 的優惠，因此 `tent` 會依其 `eu` 價格 120 排序，而不是依其較低的 `us` 價格 90 排序：

```json
GET sort-offers/_search
{
  "_source": ["product"],
  "sort": [
    {
      "offers.price": {
        "order": "asc",
        "mode": "min",
        "nested": {
          "path": "offers",
          "filter": {
            "term": { "offers.region": "eu" }
          }
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

`stove` 會最先傳回，排序值為 `100.0`，接著是 `tent`，排序值為 `120.0`。

若要排序多層巢狀物件中的欄位，請在外層 `nested` 物件內指定一個 `nested` 物件。下列請求依產品在任何優惠中的最高折扣排序：

```json
GET sort-offers/_search
{
  "_source": ["product"],
  "sort": [
    {
      "offers.discounts.percent": {
        "order": "desc",
        "mode": "max",
        "nested": {
          "path": "offers",
          "nested": {
            "path": "offers.discounts"
          }
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

`stove` 會最先傳回，排序值為 `20`，接著是 `tent`，排序值為 `15`。

## 處理缺失值

`missing` 參數指定缺失值的處理方式。內建的有效值為 `_last` (將缺失值的文件列在最後) 和 `_first` (將缺失值的文件列在最前面)。預設值為 `_last`。您也可以指定自訂值，作為缺失文件的排序值。

例如，您可以將一份包含 `average` 欄位的文件，以及另一份不包含 `average` 欄位的文件編製索引：

```json
PUT students/_doc/1
{
   "name": "John Doe",
   "average": 80
}
```
{% include copy-curl.html %}

```json
PUT students/_doc/2
{
   "name": "Mary Major"
}
```
{% include copy-curl.html %}

排序文件，將缺失欄位的文件排在最前面：

```json
GET students/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "average": {
        "order": "desc",
        "missing": "_first"
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應會先列出文件 2：

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
    "max_score" : null,
    "hits" : [
      {
        "_index" : "students",
        "_id" : "2",
        "_score" : null,
        "_source" : {
          "name" : "Mary Major"
        },
        "sort" : [
          9223372036854775807
        ]
      },
      {
        "_index" : "students",
        "_id" : "1",
        "_score" : null,
        "_source" : {
          "name" : "John Doe",
          "average" : 80
        },
        "sort" : [
          80
        ]
      }
    ]
  }
}
```

## 忽略未對應的欄位

如果欄位未對應，依該欄位排序的搜尋請求預設會失敗。若要避免這種情況，您可以使用 `unmapped_type` 參數，指示 OpenSearch 忽略該欄位。例如，如果您將 `unmapped_type` 設為 `long`，該欄位會被視為已對應為 `long` 類型。此外，索引中所有具有 `unmapped_type` 欄位的文件都會被視為在該欄位中沒有值，因此不會依該欄位排序。

例如，考慮兩個索引。在第一個索引中將一份包含 `average` 欄位的文件編製索引：

```json
PUT students/_doc/1
{
   "name": "John Doe",
   "average": 80
}
```
{% include copy-curl.html %}

在第二個索引中將一份不包含 `average` 欄位的文件編製索引：

```json
PUT students_no_map/_doc/2
{
   "name": "Mary Major"
}
```
{% include copy-curl.html %}

搜尋兩個索引中的所有文件，並依 `average` 欄位排序：

```json
GET students*/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "average": {
        "order": "desc"
      }
    }
  ]
}
```
{% include copy-curl.html %}

預設情況下，第二個索引會產生錯誤，因為 `average` 欄位未對應：

```json
{
  "took" : 3,
  "timed_out" : false,
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 1,
    "failures" : [
      {
        "shard" : 0,
        "index" : "students_no_map",
        "node" : "cam9NWqVSV-jUIkQ3tRubw",
        "reason" : {
          "type" : "query_shard_exception",
          "reason" : "No mapping found for [average] in order to sort on",
          "index" : "students_no_map",
          "index_uuid" : "JgfRkypKSUSpyU-ZXr9kKA"
        }
      }
    ]
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [
      {
        "_index" : "students",
        "_id" : "1",
        "_score" : null,
        "_source" : {
          "name" : "John Doe",
          "average" : 80
        },
        "sort" : [
          80
        ]
      }
    ]
  }
}
```

您可以指定 `unmapped_type` 參數，以便忽略未對應的欄位：

```json
GET students*/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "average": {
        "order": "desc",
        "unmapped_type": "long"
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應包含兩份文件：

```json
{
  "took" : 4,
  "timed_out" : false,
  "_shards" : {
    "total" : 2,
    "successful" : 2,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [
      {
        "_index" : "students",
        "_id" : "1",
        "_score" : null,
        "_source" : {
          "name" : "John Doe",
          "average" : 80
        },
        "sort" : [
          80
        ]
      },
      {
        "_index" : "students_no_map",
        "_id" : "2",
        "_score" : null,
        "_source" : {
          "name" : "Mary Major"
        },
        "sort" : [
          -9223372036854775808
        ]
      }
    ]
  }
}
```

## 使用指令碼排序

若要依未儲存在單一欄位中的值排序，請使用指令碼計算該值。在 `sort` 陣列中，指定 `_script` 物件。`_script` 物件接受下列參數。

參數 | 說明
:--- | :---
`type` | 指令碼所傳回值的類型。有效值為 `number` 和 `string`。必要。
`script` | 計算排序值的指令碼。如需更多資訊，請參閱[如何使用指令碼]({{site.url}}{{site.baseurl}}/scripting/using-scripts/)。
`order` | 排序順序。有效值為 `asc` 和 `desc`。預設為 `asc`。
`mode` | 當指令碼傳回多個值時，用於排序的值。如需更多資訊，請參閱[排序模式](#sort-mode)。
`nested` | 當指令碼讀取[巢狀]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/)物件的欄位時，要在其中執行指令碼的巢狀物件。在 `nested.path` 中指定巢狀物件的路徑。如需更多資訊，請參閱[排序巢狀物件](#sorting-nested-objects)。

下列請求會使用在 `params` 中傳入的匯率，將產品價格轉換為另一種貨幣後依價格排序：

```json
GET /prices-eu,prices-us/_search
{
  "_source": ["product", "price"],
  "sort": {
    "_script": {
      "type": "number",
      "script": {
        "source": "doc['price'].value * params.exchange_rate",
        "params": {
          "exchange_rate": 0.92
        }
      },
      "order": "desc"
    }
  }
}
```
{% include copy-curl.html %}

每個命中結果的 `sort` 陣列都包含指令碼計算出的值：

```json
{
  ...
  "hits": {
    ...
    "hits": [
      {
        "_index": "prices-eu",
        "_id": "1",
        "_score": null,
        "_source": {
          "product": "tent",
          "price": 129.5
        },
        "sort": [
          119.14
        ]
      },
      {
        "_index": "prices-us",
        "_id": "2",
        "_score": null,
        "_source": {
          "product": "backpack",
          "price": 95
        },
        "sort": [
          87.4
        ]
      },
      {
        "_index": "prices-us",
        "_id": "1",
        "_score": null,
        "_source": {
          "product": "stove",
          "price": 60
        },
        "sort": [
          55.2
        ]
      },
      {
        "_index": "prices-eu",
        "_id": "2",
        "_score": null,
        "_source": {
          "product": "lantern",
          "price": 24.99
        },
        "sort": [
          22.9908
        ]
      }
    ]
  }
}
```

以指令碼為基礎的排序會為每份符合的文件執行指令碼，因此比依欄位排序慢。如果您經常依相同的計算值排序，請考慮在編製索引時計算該值並將其儲存在欄位中。

## 追蹤分數

依預設，依欄位排序時不會計算分數。您可以將 `track_scores` 設為 `true` 來計算並追蹤分數：

```json
GET students/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "average": {
        "order": "desc"
      }
    }
  ],
  "track_scores": true
}
```
{% include copy-curl.html %}

## 依地理距離排序

您可以依 `_geo_distance` 排序文件。支援下列參數。

參數 | 說明
:--- | :---
`distance_type` | 指定計算距離的方法。有效值為 `arc` 和 `plane`。`plane` 方法速度較快，但在長距離或接近極點時較不精確。預設為 `arc`。
`mode` | 指定如何處理含有多個地理點的欄位。預設情況下，排序順序為遞增時，文件會依最短距離排序；排序順序為遞減時，則依最長距離排序。有效值為 `min`、`max`、`median` 和 `avg`。
`unit` | 指定計算排序值時使用的單位。預設為公尺 (`m`)。
`ignore_unmapped` | 指定如何處理未對應的欄位。將 `ignore_unmapped` 設為 `true` 可忽略未對應的欄位，效果與在欄位排序中設定 `unmapped_type` 相同。預設為 `false` (遇到未對應的欄位時產生錯誤)。如需更多資訊，請參閱[忽略未對應的欄位](#ignoring-unmapped-fields)。

您可以使用任何[地理點格式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-point/#formats)指定參考點，例如包含 `lat` 和 `lon` 的物件、`"lat,lon"` 字串、geohash 或 `[lon, lat]` 陣列。

`_geo_distance` 參數不支援 `missing_values`。當文件不包含用於計算距離的欄位時，距離一律視為 `infinity`。
{: .note}

例如，建立一個索引並將 `point` 欄位對應為 `geo_point`：

```json
PUT testindex1
{
  "mappings": {
    "properties": {
      "point": {
        "type": "geo_point"
      }
    }
  }
}
```
{% include copy-curl.html %}

將兩份包含地理點的文件編製索引：

```json
PUT testindex1/_doc/1
{
  "point": [74.00, 40.71] 
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/2
{
  "point": [73.77, -69.63] 
}
```
{% include copy-curl.html %}

搜尋所有文件，並依與所提供點的距離排序：

```json
GET testindex1/_search
{
  "sort": [
    {
      "_geo_distance": {
        "point": [59, -54],
        "order": "asc",
        "unit": "km",
        "distance_type": "arc",
        "mode": "min",
        "ignore_unmapped": true
      }
    }
  ],
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

回應包含排序後的文件：

```json
{
  "took" : 864,
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
    "max_score" : null,
    "hits" : [
      {
        "_index" : "testindex1",
        "_id" : "2",
        "_score" : null,
        "_source" : {
          "point" : [
            73.77,
            -69.63
          ]
        },
        "sort" : [
          1891.2667493895767
        ]
      },
      {
        "_index" : "testindex1",
        "_id" : "1",
        "_score" : null,
        "_source" : {
          "point" : [
            74.0,
            40.71
          ]
        },
        "sort" : [
          10628.402240213345
        ]
      }
    ]
  }
}
```

您可以使用地理點欄位類型支援的任何格式提供座標。所有格式的說明請參閱[地理點欄位類型文件]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point/)。
{: .note}

若要將多個地理點傳遞給 `_geo_distance`，請使用陣列：

```json
GET testindex1/_search
{
  "sort": [
    {
      "_geo_distance": {
        "point": [[59, -54], [60, -53]],
        "order": "asc",
        "unit": "km",
        "distance_type": "arc",
        "mode": "min",
        "ignore_unmapped": true
      }
    }
  ],
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

對每份文件而言，排序距離的計算方式是取搜尋中提供的所有點與文件中所有點之間距離的最小值、最大值或平均值 (由 `mode` 指定)。

## 效能考量

排序的欄位值會載入記憶體中以進行排序。因此，為了將額外負擔降到最低，我們建議將[數值類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/numeric/)對應為可接受的最小類型，例如 `short`、`integer` 和 `float`。[字串類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/string/)的排序欄位不應經過分析或斷詞。

`_id` 欄位限制不能用於排序作業。如果您需要依文件 ID 排序，請考慮將 ID 值複製到另一個已啟用 `doc_values` 的欄位。如需 `_id` 欄位限制的詳細資訊，請參閱 [ID 欄位類型]({{site.url}}{{site.baseurl}}/field-types/metadata-fields/id/)。
{: .note}