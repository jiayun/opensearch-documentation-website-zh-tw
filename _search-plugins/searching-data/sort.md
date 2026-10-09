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

排序功能可讓您的使用者以對他們最有意義的方式排序結果。

依預設，全文查詢會依相關性分數排序結果。
您可以將 `order` 參數設為 `asc` 或 `desc`，選擇依任何欄位值以遞增或遞減順序排序結果。

例如，若要依 `line_id` 值以遞減順序排序結果，請使用下列查詢：

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

`sort` 參數是陣列，因此您可以依優先順序指定多個欄位值。

如果您有兩個欄位的 `line_id` 值相同，OpenSearch 會使用第二個排序選項 `speech_number`：

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

您可以繼續依任意數量的欄位值排序，讓結果以正確的順序排列。欄位值不一定要是數值&mdash;您也可以依日期或時間戳記欄位排序：

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

經過分析的文字欄位無法用於排序文件，因為倒排索引只包含個別斷詞後的詞彙，而非完整字串。因此，例如您無法依 `play_name` 排序。

若要避開此限制，您可以使用對應為 keyword 類型的文字欄位原始版本。在下列範例中，`play_name.keyword` 未經分析，因此您有一份完整原始版本的副本可供排序使用：

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

將 `sort` 與 [`search_after` 參數]({{site.url}}{{site.baseurl}}/opensearch/search/paginate#the-search_after-parameter) 搭配使用，可提高捲動效率。
結果會從您在 `search_after` 陣列中指定的排序值之後的文件開始。

請確保 `search_after` 陣列中的值與 `sort` 陣列中的值數量相同，且排列順序也相同。
在此情況下，您請求的結果會從 `line_id = 3202` 和 `speech_number = 8` 之後的文件開始：

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

## 排序巢狀物件

排序 [巢狀]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/nested/) 物件時，請提供 `path` 參數，指定要排序欄位的路徑。

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

將兩份包含巢狀欄位的文件編製索引：

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
`distance_type` | 指定計算距離的方法。有效值為 `arc` 和 `plane`。`plane` 方法較快，但對於長距離或靠近極點的位置較不準確。預設為 `arc`。
`mode` | 指定如何處理含有多個地理點的欄位。依預設，當排序順序為遞增時，文件會依最短距離排序；當排序順序為遞減時，則依最長距離排序。有效值為 `min`、`max`、`median` 和 `avg`。
`unit` | 指定用於計算排序值的單位。預設為公尺 (`m`)。
`ignore_unmapped` | 指定如何處理未對應的欄位。將 `ignore_unmapped` 設為 `true` 可忽略未對應的欄位。預設為 `false` (遇到未對應的欄位時產生錯誤)。

`_geo_distance` 參數不支援 `missing_values`。當文件不包含用於計算距離的欄位時，距離一律視為 `infinity`。
{: .note}

例如，建立索引並將 `point` 欄位對應為 `geo_point`：

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

將兩個包含地理點的文件編製索引：

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

搜尋所有文件並依與所提供點的距離排序：

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

回應包含已排序的文件：

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

您可以使用 geopoint 欄位類型支援的任何格式提供座標。如需所有格式的說明，請參閱 [geopoint 欄位類型文件]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point/)。
{: .note}

若要將多個地理點傳遞至 `_geo_distance`，請使用陣列：

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

對於每份文件，排序距離會計算為搜尋中提供的所有點與文件中所有點之間距離的最小值、最大值或平均值 (依 `mode` 指定)。

## 效能考量

排序的欄位值會載入記憶體中以進行排序。因此，為了將額外負擔降到最低，我們建議將[數值類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/numeric/)對應為可接受的最小類型，例如 `short`、`integer` 和 `float`。[字串類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/string/)的排序欄位不應經過分析或斷詞。

`_id` 欄位限制不能用於排序作業。如果您需要依文件 ID 排序，請考慮將 ID 值複製到另一個已啟用 `doc_values` 的欄位。如需 `_id` 欄位限制的詳細資訊，請參閱 [ID 欄位類型]({{site.url}}{{site.baseurl}}/field-types/metadata-fields/id/)。
{: .note}