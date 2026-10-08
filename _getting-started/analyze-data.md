---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分析您的資料"
nav_order: 60
---

# 分析您的資料

您在先前教學中建立的 `students` 索引包含三份文件，因此您可以逐一檢查回應中的每個結果。實際的索引可能包含數千份文件，使這種做法不切實際。在本教學中，您將探索、篩選並排序 **Sample flight data** 資料集，此資料集包含約 13,000 份文件。您也會使用彙總來摘要資料。

## 新增範例資料

本教學使用 OpenSearch Dashboards 提供的範例資料集，因此需要一個執行中的 OpenSearch Dashboards 執行個體。如果您依照[安裝快速入門]({{site.url}}{{site.baseurl}}/getting-started/quickstart/)操作，您的安裝中已包含 OpenSearch Dashboards。

若要新增 **Sample flight data** 資料集，請依照下列步驟操作：

1. 在網頁瀏覽器中開啟 `http://localhost:5601`。這是[未設定安全性]({{site.url}}{{site.baseurl}}/getting-started/quickstart/#set-up-a-cluster-without-security)之叢集的位址。如果您[已設定叢集的安全性]({{site.url}}{{site.baseurl}}/getting-started/quickstart/#set-up-a-cluster-with-security)，請開啟 `https://localhost:5601`，並使用您設定的密碼以 `admin` 身分登入。
1. 在 OpenSearch Dashboards 首頁上，選取 **Add sample data**。
1. 在 **Sample flight data** 面板中，選取 **Add data**。

新增此資料集會建立名為 `opensearch_dashboards_sample_data_flights` 的索引。每份文件代表一個航班，並記錄其航空公司、出發地與目的地、票價、距離及延誤時間。

OpenSearch Dashboards 會在您新增資料集時產生文件 ID 與 `timestamp` 值，因此這些值會與本教學中的值不同。所有其他欄位值都來自固定的資料集，因此會相符。

## 探索資料

在查詢索引之前，請先了解其內容。若要計算索引中的文件數量，請傳送下列請求：

```json
GET /opensearch_dashboards_sample_data_flights/_count
```
{% include copy-curl.html %}

OpenSearch 會傳回文件數量：

```json
{
  "count": 13059,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  }
}
```

若要檢視欄位類型，請請求對應：

```json
GET /opensearch_dashboards_sample_data_flights/_mapping
```
{% include copy-curl.html %}

回應列出 27 個欄位。本教學中的範例使用下列欄位。

| 欄位 | 類型 | 說明 |
| :--- | :--- | :--- |
| `Carrier` | `keyword` | 營運該航班的航空公司。 |
| `OriginCityName` | `keyword` | 航班出發的城市。 |
| `DestCityName` | `keyword` | 航班抵達的城市。 |
| `DestCountry` | `keyword` | 目的地的兩字母國碼。 |
| `AvgTicketPrice` | `float` | 平均票價，以美元為單位。 |
| `FlightDelayMin` | `integer` | 出發延誤時間，以分鐘為單位。 |
| `Cancelled` | `boolean` | 航班是否已取消。 |
| `timestamp` | `date` | 出發日期與時間。 |

此索引中的每個字串欄位都對應為 `keyword`，因此所有字串搜尋都是完全比對。若要對經過分析的 `text` 欄位進行全文搜尋，請參閱[搜尋您的資料]({{site.url}}{{site.baseurl}}/getting-started/search-data/)。

若要查看文件的樣貌，請執行只傳回一個結果的搜尋：

```json
GET /opensearch_dashboards_sample_data_flights/_search
{
  "size": 1
}
```
{% include copy-curl.html %}

回應包含一個航班。此航班從法蘭克福飛往雪梨且沒有延誤，因此 `FlightDelayMin` 為 `0`，而 `FlightDelay` 為 `false`：

```json
"hits": [
  {
    "_index": "opensearch_dashboards_sample_data_flights",
    "_id": "3_6eY6ABLgrkzSeVlh5V",
    "_score": 1,
    "_source": {
      "FlightNum": "9HY9SWR",
      "DestCountry": "AU",
      "OriginWeather": "Sunny",
      "OriginCityName": "Frankfurt am Main",
      "AvgTicketPrice": 841.2656419677076,
      "DistanceMiles": 10247.856675613455,
      "FlightDelay": false,
      "DestWeather": "Rain",
      "Dest": "Sydney Kingsford Smith International Airport",
      "FlightDelayType": "No Delay",
      "OriginCountry": "DE",
      "dayOfWeek": 0,
      "DistanceKilometers": 16492.32665375846,
      "timestamp": "2026-08-24T00:00:00",
      "DestLocation": {
        "lat": "-33.94609833",
        "lon": "151.177002"
      },
      "DestAirportID": "SYD",
      "Carrier": "OpenSearch Dashboards Airlines",
      "Cancelled": false,
      "FlightTimeMin": 1030.7704158599038,
      "Origin": "Frankfurt am Main Airport",
      "OriginLocation": {
        "lat": "50.033333",
        "lon": "8.570556"
      },
      "DestRegion": "SE-BD",
      "OriginAirportID": "FRA",
      "OriginRegion": "DE-HE",
      "DestCityName": "Sydney",
      "FlightTimeHour": 17.179506930998397,
      "FlightDelayMin": 0
    }
  }
]
```

## 篩選結果

下列範例將 `size` 設為 `0`，這會讓 OpenSearch 傳回相符文件的數量，而不傳回文件本身。當您想知道有多少文件相符，而非哪些文件相符時，請使用此做法。

### 比對確切值

若要計算單一航空公司營運的航班數量，請使用 `term` 查詢：

```json
GET /opensearch_dashboards_sample_data_flights/_search
{
  "size": 0,
  "query": {
    "term": {
      "Carrier": "OpenSearch-Air"
    }
  }
}
```
{% include copy-curl.html %}

OpenSearch 會在 `hits.total.value` 中回報相符的航班數量：

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
      "value": 3220,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

### 比對值的範圍

若要計算延誤一小時以上的航班數量，請對 `FlightDelayMin` 使用 `range` 查詢：

```json
GET /opensearch_dashboards_sample_data_flights/_search
{
  "size": 0,
  "query": {
    "range": {
      "FlightDelayMin": {
        "gte": 60
      }
    }
  }
}
```
{% include copy-curl.html %}

回應回報 2,867 個相符的航班：

```json
{
  "took": 7,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2867,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

### 組合條件

實際的問題通常會組合多個條件。若要計算單一航空公司延誤一小時以上且未取消的航班數量，請使用 `bool` 查詢：

```json
GET /opensearch_dashboards_sample_data_flights/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        { "term": { "Carrier": "OpenSearch-Air" } },
        { "range": { "FlightDelayMin": { "gte": 60 } } }
      ],
      "must_not": [
        { "term": { "Cancelled": true } }
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應回報 625 個相符的航班：

```json
{
  "took": 4,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 625,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

`filter` 子句必須全部相符，而 `must_not` 子句會排除與其相符的文件。如需詳細資訊，請參閱[布林值查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/)。

## 排序結果並選取欄位

根據預設，OpenSearch 會傳回分數最高的 10 份文件，以及每份文件的完整來源。由於前述查詢僅使用篩選條件，每份文件的分數都相同，因此順序是任意的。若要選擇順序並縮減回應大小，請加入 `sort`、`size` 和 `_source`。

下列請求會尋找飛往澳洲的航班，傳回票價最高的兩筆，並且只包含每份文件中的四個欄位：

```json
GET /opensearch_dashboards_sample_data_flights/_search
{
  "size": 2,
  "_source": ["Carrier", "OriginCityName", "DestCityName", "AvgTicketPrice"],
  "query": {
    "term": {
      "DestCountry": "AU"
    }
  },
  "sort": [
    { "AvgTicketPrice": "desc" }
  ]
}
```
{% include copy-curl.html %}

OpenSearch 會傳回票價最高的兩個航班：

```json
{
  "took": 58,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 416,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "opensearch_dashboards_sample_data_flights",
        "_id": "wf6eY6ABLgrkzSeVlyX-",
        "_score": null,
        "_source": {
          "OriginCityName": "Paris",
          "AvgTicketPrice": 1197.6326773063201,
          "Carrier": "OpenSearch-Air",
          "DestCityName": "Sydney"
        },
        "sort": [
          1197.6327
        ]
      },
      {
        "_index": "opensearch_dashboards_sample_data_flights",
        "_id": "A_6eY6ABLgrkzSeVolFS",
        "_score": null,
        "_source": {
          "OriginCityName": "Billings",
          "AvgTicketPrice": 1191.012703382442,
          "Carrier": "Logstash Airways",
          "DestCityName": "Brisbane"
        },
        "sort": [
          1191.0127
        ]
      }
    ]
  }
}
```

`hits.total.value` 欄位顯示有 416 個相符的航班，而 `size` 將回應限制為其中 2 個。每個命中結果都包含一個 `sort` 陣列，其中含有 OpenSearch 用來排序的值；`_score` 為 `null`，因為依欄位排序會取代相關性排名。

## 使用彙總摘要資料

到目前為止的查詢都是傳回文件或計算文件數量。_彙總_ 會將許多文件摘要成單一結果，讓您能夠回答任何單一文件都未包含的問題，例如哪家航空公司最常誤點。

### 計算每個群組的文件數量

`terms` 彙總會依欄位的值將文件分組，並計算每個群組的數量。下列請求會計算每家航空公司營運的航班數量。將 `size` 設為 `0` 可讓 13,059 份相符文件不出現在回應中，只留下摘要：

```json
GET /opensearch_dashboards_sample_data_flights/_search
{
  "size": 0,
  "aggs": {
    "flights_per_carrier": {
      "terms": {
        "field": "Carrier"
      }
    }
  }
}
```
{% include copy-curl.html %}

OpenSearch 會為每家航空公司傳回一個桶 (bucket)，並依文件數量排序：

```json
{
  "took": 6,
  "timed_out": false,
  "terminated_early": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "flights_per_carrier": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "Logstash Airways",
          "doc_count": 3331
        },
        {
          "key": "BeatsWest",
          "doc_count": 3274
        },
        {
          "key": "OpenSearch Dashboards Airlines",
          "doc_count": 3234
        },
        {
          "key": "OpenSearch-Air",
          "doc_count": 3220
        }
      ]
    }
  }
}
```

`hits.total.value` 欄位顯示 `10000`，且 `relation` 為 `gte`，這是因為當相符數量達到 10,000 時，OpenSearch 就會停止追蹤確切總數。只有命中總數是近似值。彙總仍會包含每一份相符文件，因此各桶的數量加總起來就是全部 13,059 個航班。

### 計算每個群組的指標

將一個彙總巢狀置於另一個彙總中，即可計算每個桶的指標。下列請求加入了 `avg` 彙總，用以計算每家航空公司的 `FlightDelayMin` 平均值：

```json
GET /opensearch_dashboards_sample_data_flights/_search
{
  "size": 0,
  "aggs": {
    "flights_per_carrier": {
      "terms": {
        "field": "Carrier"
      },
      "aggs": {
        "average_delay": {
          "avg": {
            "field": "FlightDelayMin"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

現在每個桶都包含該航空公司的平均誤點時間。Logstash Airways 的平均誤點時間最長，約為 50 分鐘：

```json
{
  "took": 2,
  "timed_out": false,
  "terminated_early": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "flights_per_carrier": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "Logstash Airways",
          "doc_count": 3331,
          "average_delay": {
            "value": 49.55268688081657
          }
        },
        {
          "key": "BeatsWest",
          "doc_count": 3274,
          "average_delay": {
            "value": 45.957544288332315
          }
        },
        {
          "key": "OpenSearch Dashboards Airlines",
          "doc_count": 3234,
          "average_delay": {
            "value": 46.368274582560296
          }
        },
        {
          "key": "OpenSearch-Air",
          "doc_count": 3220,
          "average_delay": {
            "value": 47.41304347826087
          }
        }
      ]
    }
  }
}
```

### 依時間將文件分組

`date_histogram` 彙總會將文件分組到各個時間間隔中，讓您能夠繪製資料隨時間變化的圖表。下列請求會計算每週的航班數量：

```json
GET /opensearch_dashboards_sample_data_flights/_search
{
  "size": 0,
  "aggs": {
    "flights_over_time": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "week"
      }
    }
  }
}
```
{% include copy-curl.html %}

OpenSearch 會為每週傳回一個桶，每個桶都有一個 `key_as_string` 欄位，其中包含該間隔的起始時間。由於 OpenSearch Dashboards 會在您新增範例資料時產生 `timestamp` 值，因此您的間隔會從您新增資料的日期開始：

```json
{
  "took": 17,
  "timed_out": false,
  "terminated_early": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "flights_over_time": {
      "buckets": [
        {
          "key_as_string": "2026-08-24T00:00:00.000Z",
          "key": 1787529600000,
          "doc_count": 2202
        },
        {
          "key_as_string": "2026-08-31T00:00:00.000Z",
          "key": 1788134400000,
          "doc_count": 2177
        },
        {
          "key_as_string": "2026-09-07T00:00:00.000Z",
          "key": 1788739200000,
          "doc_count": 2142
        },
        {
          "key_as_string": "2026-09-14T00:00:00.000Z",
          "key": 1789344000000,
          "doc_count": 2187
        },
        {
          "key_as_string": "2026-09-21T00:00:00.000Z",
          "key": 1789948800000,
          "doc_count": 2188
        },
        {
          "key_as_string": "2026-09-28T00:00:00.000Z",
          "key": 1790553600000,
          "doc_count": 2163
        }
      ]
    }
  }
}
```

如需可用彙總的詳細資訊，請參閱[彙總]({{site.url}}{{site.baseurl}}/aggregations/)。

## 將資料視覺化

若要在 OpenSearch Dashboards 中以視覺化方式探索資料，請參閱 OpenSearch Dashboards 入門文件，並從[建立索引模式]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#step-2-create-an-index-pattern)開始。

每個航班都會在 `OriginLocation` 和 `DestLocation` 欄位中記錄其出發與目的地機場的座標，因此您可以在地圖上繪製航班。如需詳細資訊，請參閱[地圖應用程式]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/maps/)。

## 後續步驟

- 若要深入了解如何彙整資料，請參閱[彙總]({{site.url}}{{site.baseurl}}/aggregations/)。
- 若要探索 OpenSearch Dashboards 應用程式，請參閱[OpenSearch Dashboards 入門]({{site.url}}{{site.baseurl}}/dashboards/getting-started/index/)。
- 若要在完成後關閉叢集，請參閱[停止叢集]({{site.url}}{{site.baseurl}}/getting-started/quickstart/#stop-the-cluster)。
