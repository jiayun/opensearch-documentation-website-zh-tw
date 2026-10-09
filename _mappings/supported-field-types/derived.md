---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "衍生欄位"
nav_order: 55
has_children: false
parent: Specialized search field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/derived/
---

# 衍生欄位類型
**於 2.15 版推出**
{: .label .label-purple }

衍生欄位可讓您透過在現有欄位上執行指令碼，動態建立新欄位。現有欄位可從包含原始文件的 `_source` 欄位擷取，或從欄位的 doc values 取得。當您在索引對應或搜尋請求中定義衍生欄位後，即可像使用一般欄位一樣，在查詢中使用該欄位。

## 何時使用衍生欄位

衍生欄位在欄位操作上提供彈性，並優先考量儲存效率。然而，由於它們是在查詢時計算，因此可能降低查詢效能。衍生欄位在需要即時資料轉換的情境中特別實用，例如：

- **記錄檔分析**：從記錄訊息中擷取時間戳記和記錄層級。
- **效能指標**：從開始和結束時間戳記計算回應時間。
- **安全性分析**：即時 IP 地理位置定位和使用者代理程式剖析，以進行威脅偵測。
- **實驗性使用案例**：測試新的資料轉換、建立用於 A/B 測試的臨時欄位，或產生一次性報告，而不需變更對應或重新編製資料索引。

儘管查詢時計算可能影響效能，衍生欄位的彈性和儲存效率仍使其成為這些應用情境的寶貴工具。

## 目前限制

目前衍生欄位有下列限制：

- **評分和排序**：尚未支援。
- **彙總**：衍生欄位支援大多數彙總類型。不支援下列彙總：地理 (geodistance、geohash grid、geohex grid、geotile grid、geobounds、geocentroid)、significant terms、significant text 和 scripted metric。
- **儀表板支援**：這些欄位不會顯示在 OpenSearch Dashboards 的可用欄位清單中。不過，如果您知道衍生欄位名稱，仍可使用它們進行篩選。
- **鏈結衍生欄位**：一個衍生欄位不能用來定義另一個衍生欄位。
- **join 欄位類型**：衍生欄位不支援 [join 欄位類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/join/)。

我們計劃在未來版本中解決這些限制。

## 先決條件

使用衍生欄位之前，請務必符合下列先決條件：

- **啟用 `_source` 或 `doc_values`**：確保為指令碼中使用的欄位啟用 `_source` 欄位或 doc values。
- **啟用高成本查詢**：確保將 [`search.allow_expensive_queries`]({{site.url}}{{site.baseurl}}/query-dsl/index/#expensive-queries) 設為 `true`。
- **功能控制**：衍生欄位預設為啟用。您可以使用下列設定啟用或停用衍生欄位：
    - **索引層級**：更新 `index.query.derived_field.enabled` 設定。
    - **叢集層級**：更新 `search.derived_field.enabled` 設定。
    這兩個設定都是動態的，因此不需重新編製索引或重新啟動節點即可變更。
- **效能考量**：使用衍生欄位之前，請評估[效能影響](#performance)，以確保衍生欄位符合您的規模需求。

## 定義衍生欄位

您可以在[索引對應中](#defining-derived-fields-in-index-mappings)或[直接在搜尋請求中](#defining-and-searching-derived-fields-in-a-search-request)定義衍生欄位。

## 範例設定

若要試用本頁的範例，請先建立下列 `logs` 索引：

```json
PUT logs
{
  "mappings": {
    "properties": {
      "request": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "clientip": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

將範例文件新增至索引：

```json
POST _bulk
{ "index" : { "_index" : "logs", "_id" : "1" } }
{ "request": "894030400 GET /english/images/france98_venues.gif HTTP/1.0 200 778", "clientip": "61.177.2.0" }
{ "index" : { "_index" : "logs", "_id" : "2" } }
{ "request": "894140400 GET /french/playing/mascot/mascot.html HTTP/1.1 200 5474", "clientip": "185.92.2.0" }
{ "index" : { "_index" : "logs", "_id" : "3" } }
{ "request": "894250400 POST /english/venues/images/venue_header.gif HTTP/1.0 200 711", "clientip": "61.177.2.0" }
{ "index" : { "_index" : "logs", "_id" : "4" } }
{ "request": "894360400 POST /images/home_fr_button.gif HTTP/1.1 200 2140", "clientip": "129.178.2.0" }
{ "index" : { "_index" : "logs", "_id" : "5" } }
{ "request": "894470400 DELETE /images/102384s.gif HTTP/1.0 200 785", "clientip": "227.177.2.0" }
```
{% include copy-curl.html %}

## 在索引對應中定義衍生欄位

若要從 `logs` 索引中編製索引的 `request` 欄位衍生出 `timestamp`、`method` 和 `size` 欄位，請設定下列對應：

```json
PUT /logs/_mapping
{
  "derived": {
    "timestamp": {
      "type": "date",
      "format": "MM/dd/yyyy",
      "script": {
        "source": """
        emit(Long.parseLong(doc["request.keyword"].value.splitOnToken(" ")[0]))
        """
      }
    },
    "method": {
      "type": "keyword",
      "script": {
        "source": """
        emit(doc["request.keyword"].value.splitOnToken(" ")[1])
        """
      }
    },
    "size": {
      "type": "long",
      "script": {
        "source": """
        emit(Long.parseLong(doc["request.keyword"].value.splitOnToken(" ")[5]))
        """
      }
    }
  }
}
```
{% include copy-curl.html %}

請注意，`timestamp` 欄位有一個額外的 `format` 參數，用於指定顯示 `date` 欄位的格式。如果您未包含 `format` 參數，則格式預設為 `strict_date_time_no_millis`。如需支援的日期格式詳細資訊，請參閱[參數](#parameters)。

## 參數

下表列出 `derived` 欄位類型接受的參數。所有參數都是動態的，不需重新編製文件索引即可修改。

| 參數 | 必要/選用 | 說明 |
| :--- | :--- | :--- |
| `type` | 必要 | 衍生欄位的類型。支援的類型包括 `boolean`、`date`、`geo_point`、`ip`、`keyword`、`text`、`long`、`double`、`float` 和 `object`。 |
| `script` | 必要 | 與衍生欄位相關聯的指令碼。指令碼發出的任何值都必須使用 `emit()` 發出。發出值的類型必須符合衍生欄位的 `type`。如果已啟用 `doc_values` 和 `_source` 欄位，指令碼可以存取這兩個欄位。欄位的 doc value 可使用 `doc['field_name'].value` 存取，而來源可使用 `params._source["field_name"]` 存取。 |
| `format` | 選用 | 用於剖析日期的格式。僅適用於 `date` 欄位。有效值為 `strict_date_time_no_millis`、`strict_date_optional_time` 和 `epoch_millis`。如需詳細資訊，請參閱[格式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#formats)。|
| `ignore_malformed`| 選用 | 一個布林值，指定在衍生欄位上執行查詢時是否忽略格式錯誤的值。預設值為 `false` (遇到格式錯誤的值時擲回例外狀況)。 |
| `prefilter_field` | 選用 | 一個已編製索引的文字欄位，用於提升衍生欄位的效能。指定現有的已編製索引欄位，以便在篩選衍生欄位之前先對其進行篩選。如需詳細資訊，請參閱[預先篩選欄位](#prefilter-field)。 |

## 在指令碼中發出值

`emit()` 函式僅能在衍生欄位指令碼內容中使用。它用來為執行指令碼的文件發出一或多個（適用於多值欄位）指令碼值。

下表列出支援欄位類型的 `emit()` 函式格式。

| 類型      | 發出格式                      | 支援多值欄位|
|-----------|----------------------------------|--------------|
| `boolean` | `emit(boolean)`                  | 否           |
| `double`  | `emit(double)`                   | 是          |
| `date`    | `emit(long timeInMilis)`         | 是          |
| `float`   | `emit(float)`                    | 是          |
| `geo_point`| `emit(double lat, double lon)`   | 是          |
| `ip`      | `emit(String ip)`                | 是          |
| `keyword` | `emit(String)`                   | 是          |
| `long`    | `emit(long)`                     | 是          |
| `object`  | `emit(String json)` (有效的 JSON) | 是          |
| `text`    | `emit(String)`                   | 是          |

預設情況下，衍生欄位與其發出值之間的類型不符會導致搜尋請求失敗並產生錯誤。若將 `ignore_malformed` 設定為 `true`，則會略過失敗的文件，且搜尋請求會成功。
{: .note}

每個文件發出值的大小上限為 1 MB。
{: .important}

## 搜尋索引對應中定義的衍生欄位

若要搜尋衍生欄位，請使用與搜尋一般欄位相同的語法。例如，下列請求會搜尋衍生 `timestamp` 欄位在指定範圍內的文件：

```json
POST /logs/_search
{
  "query": {
    "range": {
      "timestamp": {
        "gte": "1970-01-11T08:20:30.400Z",   
        "lte": "1970-01-11T08:26:00.400Z"
      }
    }
  },
  "fields": ["timestamp"]
}
```
{% include copy-curl.html %}

回應包含符合的文件：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 315,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "logs",
        "_id": "1",
        "_score": 1,
        "_source": {
          "request": "894030400 GET /english/images/france98_venues.gif HTTP/1.0 200 778",
          "clientip": "61.177.2.0"
        },
        "fields": {
          "timestamp": [
            "1970-01-11T08:20:30.400Z"
          ]
        }
      },
      {
        "_index": "logs",
        "_id": "2",
        "_score": 1,
        "_source": {
          "request": "894140400 GET /french/playing/mascot/mascot.html HTTP/1.1 200 5474",
          "clientip": "185.92.2.0"
        },
        "fields": {
          "timestamp": [
            "1970-01-11T08:22:20.400Z"
          ]
        }
      },
      {
        "_index": "logs",
        "_id": "3",
        "_score": 1,
        "_source": {
          "request": "894250400 POST /english/venues/images/venue_header.gif HTTP/1.0 200 711",
          "clientip": "61.177.2.0"
        },
        "fields": {
          "timestamp": [
            "1970-01-11T08:24:10.400Z"
          ]
        }
      },
      {
        "_index": "logs",
        "_id": "4",
        "_score": 1,
        "_source": {
          "request": "894360400 POST /images/home_fr_button.gif HTTP/1.1 200 2140",
          "clientip": "129.178.2.0"
        },
        "fields": {
          "timestamp": [
            "1970-01-11T08:26:00.400Z"
          ]
        }
      }
    ]
  }
}
```
</details>

## 在搜尋請求中定義與搜尋衍生欄位

您也可以直接在搜尋請求中定義衍生欄位，並與一般已編製索引的欄位一起查詢。例如，下列請求會建立 `url` 與 `status` 衍生欄位，並將這些欄位與一般 `request` 和 `clientip` 欄位一起搜尋：

```json
POST /logs/_search
{
  "derived": {
    "url": {
      "type": "text",
      "script": {
        "source": """
        emit(doc["request"].value.splitOnToken(" ")[2])
        """
      }
    },
    "status": {
      "type": "keyword",
      "script": {
        "source": """
        emit(doc["request"].value.splitOnToken(" ")[4])
        """
      }
    }
  },
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "clientip": "61.177.2.0"
          }
        },
        {
          "match": {
            "url": "images"
          }
        },
        {
          "term": {
            "status": "200"
          }
        }
      ]
    }
  },
  "fields": ["request", "clientip", "url", "status"]
}
```
{% include copy-curl.html %}

回應包含符合的文件：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 6,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 2.8754687,
    "hits": [
      {
        "_index": "logs",
        "_id": "1",
        "_score": 2.8754687,
        "_source": {
          "request": "894030400 GET /english/images/france98_venues.gif HTTP/1.0 200 778",
          "clientip": "61.177.2.0"
        },
        "fields": {
          "request": [
            "894030400 GET /english/images/france98_venues.gif HTTP/1.0 200 778"
          ],
          "clientip": [
            "61.177.2.0"
          ],
          "url": [
            "/english/images/france98_venues.gif"
          ],
          "status": [
            "200"
          ]
        }
      },
      {
        "_index": "logs",
        "_id": "3",
        "_score": 2.8754687,
        "_source": {
          "request": "894250400 POST /english/venues/images/venue_header.gif HTTP/1.0 200 711",
          "clientip": "61.177.2.0"
        },
        "fields": {
          "request": [
            "894250400 POST /english/venues/images/venue_header.gif HTTP/1.0 200 711"
          ],
          "clientip": [
            "61.177.2.0"
          ],
          "url": [
            "/english/venues/images/venue_header.gif"
          ],
          "status": [
            "200"
          ]
        }
      }
    ]
  }
}
```
</details>

衍生欄位在搜尋時會使用索引分析設定中指定的預設分析器。您可以覆寫預設分析器，或在搜尋請求中指定搜尋分析器，方式與一般欄位相同。如需更多資訊，請參閱[分析器]({{site.url}}{{site.baseurl}}/analyzers/)。
{: .note}

當欄位同時存在索引對應與搜尋定義時，以搜尋定義為優先。
{: .note}

### 擷取欄位

您可以在搜尋請求中使用 `fields` 參數擷取衍生欄位，方式與一般欄位相同，如前面的範例所示。您也可以使用萬用字元擷取符合指定模式的所有衍生欄位。

### 醒目提示

類型為 `text` 的衍生欄位支援使用[統一醒目提示器]({{site.url}}{{site.baseurl}}/opensearch/search/highlight#the-unified-highlighter)進行醒目提示。例如，下列請求指定對衍生 `url` 欄位進行醒目提示：

```json
POST /logs/_search
{
  "derived": {
    "url": {
      "type": "text",
      "script": {
        "source": """
        emit(doc["request"].value.splitOnToken(" " )[2])
        """
      }
    }
  },
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "clientip": "61.177.2.0"
          }
        },
        {
          "match": {
            "url": "images"
          }
        }
      ]
    }
  },
  "fields": ["request", "clientip", "url"],
  "highlight": {
    "fields": {
      "url": {}
    }
  }
}
```
{% include copy-curl.html %}

回應會在 `url` 欄位中指定醒目提示：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 45,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.8754687,
    "hits": [
      {
        "_index": "logs",
        "_id": "1",
        "_score": 1.8754687,
        "_source": {
          "request": "894030400 GET /english/images/france98_venues.gif HTTP/1.0 200 778",
          "clientip": "61.177.2.0"
        },
        "fields": {
          "request": [
            "894030400 GET /english/images/france98_venues.gif HTTP/1.0 200 778"
          ],
          "clientip": [
            "61.177.2.0"
          ],
          "url": [
            "/english/images/france98_venues.gif"
          ]
        },
        "highlight": {
          "url": [
            "/english/<em>images</em>/france98_venues.gif"
          ]
        }
      },
      {
        "_index": "logs",
        "_id": "3",
        "_score": 1.8754687,
        "_source": {
          "request": "894250400 POST /english/venues/images/venue_header.gif HTTP/1.0 200 711",
          "clientip": "61.177.2.0"
        },
        "fields": {
          "request": [
            "894250400 POST /english/venues/images/venue_header.gif HTTP/1.0 200 711"
          ],
          "clientip": [
            "61.177.2.0"
          ],
          "url": [
            "/english/venues/images/venue_header.gif"
          ]
        },
        "highlight": {
          "url": [
            "/english/venues/<em>images</em>/venue_header.gif"
          ]
        }
      }
    ]
  }
}
```
</details>

## 彙總

衍生欄位支援大多數的彙總類型。

不支援地理、顯著詞彙、顯著文字及指令碼指標彙總。
{: .note}

例如，下列請求會在 `method` 衍生欄位上建立簡單的 `terms` 彙總：

```json
POST /logs/_search
{
  "size": 0,
  "aggs": {
    "methods": {
      "terms": {
        "field": "method"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含下列桶：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took" : 12,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 5,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "methods" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "GET",
          "doc_count" : 2
        },
        {
          "key" : "POST",
          "doc_count" : 2
        },
        {
          "key" : "DELETE",
          "doc_count" : 1
        }
      ]
    }
  }
}
```
</details>

## 效能

衍生欄位不會編製索引，而是透過從 `_source` 欄位或 doc values 擷取值來動態計算。因此，它們的執行速度較慢。若要改善效能，請嘗試下列做法：

- 在已編製索引的欄位上新增查詢篩選條件，並搭配衍生欄位，以修剪搜尋空間。
- 在指令碼中使用 doc values 而非 `_source`，以加快存取速度 (若適用)。
- 考慮使用 [`prefilter_field`](#prefilter-field)，以在搜尋請求中不需明確篩選條件的情況下自動修剪搜尋空間。

### 預先篩選欄位

指定預先篩選欄位有助於在搜尋請求中不需新增明確篩選條件的情況下修剪搜尋空間。預先篩選欄位會指定現有的已編製索引欄位 (`prefilter_field`)，在建構查詢時自動據以篩選。`prefilter_field` 必須是文字欄位 ([`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 或 [`match_only_text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/match-only-text/))。

例如，您可以將 `prefilter_field` 新增至 `method` 衍生欄位。更新索引對應，指定在 `request` 欄位上進行預先篩選：

```json
PUT /logs/_mapping
{
  "derived": {
    "method": {
      "type": "keyword",
      "script": {
        "source": """
        emit(doc["request.keyword"].value.splitOnToken(" ")[1])
        """
      },
      "prefilter_field": "request"
    }
  }
}
```
{% include copy-curl.html %}

現在使用 `method` 衍生欄位上的查詢進行搜尋：

```json
POST /logs/_search
{
  "profile": true,
  "query": {
    "term": {
      "method": {
        "value": "GET"
      }
    }
  },
  "fields": ["method"]
}
```
{% include copy-curl.html %}

OpenSearch 會自動在您的查詢中新增 `request` 欄位的篩選條件：

```json
"#request:GET #DerivedFieldQuery (Query: [ method:GET])"
```

您可以使用 `profile` 選項來分析衍生欄位效能，如上述範例所示。
{: .tip} 

## 衍生物件欄位

指令碼可以發出有效的 JSON 物件，讓您查詢子欄位而不需將它們編製索引，方式與一般欄位相同。這對於需要偶爾搜尋某些子欄位的大型 JSON 物件很有用。在此情況下，將子欄位編製索引的成本很高，而為每個子欄位定義衍生欄位也會增加許多資源負擔。如果您未[明確提供子欄位類型](#explicit-subfield-type)，則會[推斷](#inferred-subfield-type)子欄位類型。

例如，下列請求將 `derived_request_object` 衍生欄位定義為 `object` 類型：

```json
PUT logs_object
{
  "mappings": {
    "properties": {
      "request_object": { "type": "text" }
    },
    "derived": {
      "derived_request_object": {
        "type": "object",
        "script": {
          "source": "emit(params._source[\"request_object\"])"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

請考慮下列文件，其中 `request_object` 是 JSON 物件的字串表示：

```json
POST _bulk
{ "index" : { "_index" : "logs_object", "_id" : "1" } }
{ "request_object": "{\"@timestamp\": 894030400, \"clientip\":\"61.177.2.0\", \"request\": \"GET /english/venues/images/venue_header.gif HTTP/1.0\", \"status\": 200, \"size\": 711}" }
{ "index" : { "_index" : "logs_object", "_id" : "2" } }
{ "request_object": "{\"@timestamp\": 894140400, \"clientip\":\"129.178.2.0\", \"request\": \"GET /images/home_fr_button.gif HTTP/1.1\", \"status\": 200, \"size\": 2140}" }
{ "index" : { "_index" : "logs_object", "_id" : "3" } }
{ "request_object": "{\"@timestamp\": 894240400, \"clientip\":\"227.177.2.0\", \"request\": \"GET /images/102384s.gif HTTP/1.0\", \"status\": 400, \"size\": 785}" }
{ "index" : { "_index" : "logs_object", "_id" : "4" } }
{ "request_object": "{\"@timestamp\": 894340400, \"clientip\":\"61.177.2.0\", \"request\": \"GET /english/images/venue_bu_city_on.gif HTTP/1.0\", \"status\": 400, \"size\": 1397}\n" }
{ "index" : { "_index" : "logs_object", "_id" : "5" } }
{ "request_object": "{\"@timestamp\": 894440400, \"clientip\":\"132.176.2.0\", \"request\": \"GET /french/news/11354.htm HTTP/1.0\", \"status\": 200, \"size\": 3460, \"is_active\": true}" }
```
{% include copy-curl.html %}

下列查詢會搜尋 `derived_request_object` 的 `@timestamp` 子欄位：

```json
POST /logs_object/_search
{
  "query": {
    "range": {
      "derived_request_object.@timestamp": {
        "gte": "894030400",   
        "lte": "894140400"
      }
    }
  },
  "fields": ["derived_request_object.@timestamp"]
}
```
{% include copy-curl.html %}

回應包含相符的文件：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 26,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "logs_object",
        "_id": "1",
        "_score": 1,
        "_source": {
          "request_object": """{"@timestamp": 894030400, "clientip":"61.177.2.0", "request": "GET /english/venues/images/venue_header.gif HTTP/1.0", "status": 200, "size": 711}"""
        },
        "fields": {
          "derived_request_object.@timestamp": [
            894030400
          ]
        }
      },
      {
        "_index": "logs_object",
        "_id": "2",
        "_score": 1,
        "_source": {
          "request_object": """{"@timestamp": 894140400, "clientip":"129.178.2.0", "request": "GET /images/home_fr_button.gif HTTP/1.1", "status": 200, "size": 2140}"""
        },
        "fields": {
          "derived_request_object.@timestamp": [
            894140400
          ]
        }
      }
    ]
  }
}
```

</details>

您也可以指定要醒目提示衍生物件欄位：

```json
POST /logs_object/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "derived_request_object.clientip": "61.177.2.0"
          }
        },
        {
          "match": {
            "derived_request_object.request": "images"
          }
        }
      ]
    }
  },
  "fields": ["derived_request_object.*"],
  "highlight": {
    "fields": {
      "derived_request_object.request": {}
    }
  }
}
```
{% include copy-curl.html %}

回應會將醒目提示新增至 `derived_request_object.request` 欄位：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 5,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 2,
    "hits": [
      {
        "_index": "logs_object",
        "_id": "1",
        "_score": 2,
        "_source": {
          "request_object": """{"@timestamp": 894030400, "clientip":"61.177.2.0", "request": "GET /english/venues/images/venue_header.gif HTTP/1.0", "status": 200, "size": 711}"""
        },
        "fields": {
          "derived_request_object.request": [
            "GET /english/venues/images/venue_header.gif HTTP/1.0"
          ],
          "derived_request_object.clientip": [
            "61.177.2.0"
          ]
        },
        "highlight": {
          "derived_request_object.request": [
            "GET /english/venues/<em>images</em>/venue_header.gif HTTP/1.0"
          ]
        }
      },
      {
        "_index": "logs_object",
        "_id": "4",
        "_score": 2,
        "_source": {
          "request_object": """{"@timestamp": 894340400, "clientip":"61.177.2.0", "request": "GET /english/images/venue_bu_city_on.gif HTTP/1.0", "status": 400, "size": 1397}
"""
        },
        "fields": {
          "derived_request_object.request": [
            "GET /english/images/venue_bu_city_on.gif HTTP/1.0"
          ],
          "derived_request_object.clientip": [
            "61.177.2.0"
          ]
        },
        "highlight": {
          "derived_request_object.request": [
            "GET /english/<em>images</em>/venue_bu_city_on.gif HTTP/1.0"
          ]
        }
      }
    ]
  }
}
```

</details>

### 推斷的子欄位類型 

類型推斷採用與[動態對應]({{site.url}}{{site.baseurl}}/opensearch/mappings#dynamic-mapping)相同的邏輯。不同於從第一份文件推斷子欄位類型，這裡使用文件的隨機樣本來推斷類型。如果隨機樣本中的任何文件都找不到該子欄位，類型推斷就會失敗並記錄一則警告。對於在文件中很少出現的子欄位，建議定義明確的欄位類型。對這類子欄位使用動態類型推斷，可能導致查詢沒有任何結果，就像欄位遺失一樣。 

### 明確的子欄位類型

若要定義明確的子欄位類型，請在 `properties` 物件中提供 `type` 參數。在下列範例中，`derived_logs_object.is_active` 欄位被定義為 `boolean`。由於此欄位只存在於其中一份文件中，其類型推斷可能會失敗，因此定義明確的類型非常重要：

```json
POST /logs_object/_search
{
  "derived": {
    "derived_request_object": {
      "type": "object",
      "script": {
        "source": "emit(params._source[\"request_object\"])"
      },
      "properties": {
        "is_active": "boolean"
      }
    }
  },
  "query": {
    "term": {
      "derived_request_object.is_active": true
    }
  },
  "fields": ["derived_request_object.is_active"]
}
```
{% include copy-curl.html %}

回應包含符合的文件：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 13,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "logs_object",
        "_id": "5",
        "_score": 1,
        "_source": {
          "request_object": """{"@timestamp": 894440400, "clientip":"132.176.2.0", "request": "GET /french/news/11354.htm HTTP/1.0", "status": 200, "size": 3460, "is_active": true}"""
        },
        "fields": {
          "derived_request_object.is_active": [
            true
          ]
        }
      }
    ]
  }
}
```

</details>
