---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: xy
parent: Geographic and xy queries
nav_order: 50
redirect_from: 
  - /opensearch/query-dsl/geo-and-xy/xy/
  - /query-dsl/query-dsl/geo-and-xy/xy/
---

# xy 查詢

若要搜尋包含 [xy point]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/xy-point/) 或 [xy shape]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/xy-shape/) 欄位的文件，請使用 xy 查詢。

## 空間關係

當您將 xy shape 提供給 xy 查詢時，文件中的 xy 欄位會使用下列空間關係與提供的形狀進行比對。

關係 | 說明 | 支援的 xy 欄位類型
:--- | :--- | :--- 
`INTERSECTS` | （預設）比對其 xy point 或 xy shape 與查詢中提供的形狀相交的文件。 | `xy_point`, `xy_shape`
`DISJOINT` | 比對其 xy shape 與查詢中提供的形狀不相交的文件。 | `xy_shape`
`WITHIN` | 比對其 xy shape 完全位於查詢中提供的形狀內的文件。 | `xy_shape`
`CONTAINS` | 比對其 xy shape 完全包含查詢中提供的形狀的文件。 | `xy_shape`

下列範例說明如何搜尋包含 xy shape 的文件。若要了解如何搜尋包含 xy point 的文件，請參閱[查詢 xy point](#querying-xy-points)一節。

## 在 xy 查詢中定義形狀

您可以在 xy 查詢中定義形狀，方法是在查詢時提供新的形狀定義，或參照在另一個索引中預先編製索引的形狀名稱。

### 使用新的形狀定義

若要為 xy 查詢提供新的形狀，請在 `xy_shape` 欄位中定義它。

下列範例說明如何搜尋包含 xy shape 且符合查詢時所定義 xy shape 的文件。

首先，建立索引並將 `geometry` 欄位對應為 `xy_shape`：

```json
PUT testindex
{
  "mappings": {
    "properties": {
      "geometry": {
        "type": "xy_shape"
      }
    }
  }
}
```
{% include copy-curl.html %}

將包含點的文件和包含多邊形的文件編製索引：

```json
PUT testindex/_doc/1
{
  "geometry": { 
    "type": "point",
    "coordinates": [0.5, 3.0]
  }
}
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/2
{
  "geometry" : {
    "type" : "polygon",
    "coordinates" : [
      [[2.5, 6.0],
      [0.5, 4.5], 
      [1.5, 2.0], 
      [3.5, 3.5],
      [2.5, 6.0]]
    ]
  }
}
```
{% include copy-curl.html %}

定義一個 [`envelope`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/xy-shape#envelope)&mdash;即 `[[minX, maxY], [maxX, minY]]` 格式的邊界矩形。搜尋 xy point 或形狀與該邊界矩形相交的文件：

```json
GET testindex/_search
{
  "query": {
    "xy_shape": {
      "geometry": {
        "shape": {
          "type": "envelope",
          "coordinates": [ [ 0.0, 6.0], [ 4.0, 2.0] ]
        },
        "relation": "WITHIN"
      }
    }
  }
}
```
{% include copy-curl.html %}

下圖說明此範例。點和多邊形都位於邊界矩形內。

![xy shape 查詢]({{site.url}}{{site.baseurl}}/images/xy_query.png){: width="250" }


回應包含這兩份文件：

```json
{
  "took" : 363,
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
    "max_score" : 0.0,
    "hits" : [
      {
        "_index" : "testindex",
        "_id" : "1",
        "_score" : 0.0,
        "_source" : {
          "geometry" : {
            "type" : "point",
            "coordinates" : [
              0.5,
              3.0
            ]
          }
        }
      },
      {
        "_index" : "testindex",
        "_id" : "2",
        "_score" : 0.0,
        "_source" : {
          "geometry" : {
            "type" : "polygon",
            "coordinates" : [
              [
                [
                  2.5,
                  6.0
                ],
                [
                  0.5,
                  4.5
                ],
                [
                  1.5,
                  2.0
                ],
                [
                  3.5,
                  3.5
                ],
                [
                  2.5,
                  6.0
                ]
              ]
            ]
          }
        }
      }
    ]
  }
}
```

### 使用預先編製索引的形狀定義

建構 xy 查詢時，您也可以參照在另一個索引中預先編製索引的形狀名稱。使用此方法，您可以在編製索引時定義 xy shape 並依名稱參照它，並在 `indexed_shape` 物件中提供下列參數。

參數 | 說明
:--- | :---
`index` | 包含預先編製索引形狀的索引名稱。
`id` | 包含預先編製索引形狀之文件的文件 ID。
`path` | 以路徑形式包含預先編製索引形狀的欄位名稱。
`routing` | 包含預先編製索引形狀之文件的路由值。若形狀文件是以自訂路由值編製索引，則為必要。

下列範例說明如何參照在另一個索引中預先編製索引的形狀名稱。在此範例中，索引 `pre-indexed-shapes` 包含定義邊界的形狀，而索引 `testindex` 包含會依據這些邊界檢查其位置的形狀。

首先，建立索引 `pre-indexed-shapes` 並將此索引的 `geometry` 欄位對應為 `xy_shape`：

```json
PUT pre-indexed-shapes
{
  "mappings": {
    "properties": {
      "geometry": {
        "type": "xy_shape"
      }
    }
  }
}
```
{% include copy-curl.html %}

將指定邊界的邊界矩形編製索引並命名為 `rectangle`：

```json
PUT pre-indexed-shapes/_doc/rectangle
{
  "geometry": {
    "type": "envelope",
    "coordinates" : [ [ 0.0, 6.0], [ 4.0, 2.0] ]
  }
}
```
{% include copy-curl.html %}

將包含點的文件和包含多邊形的文件編製索引至索引 `testindex`：

```json
PUT testindex/_doc/1
{
  "geometry": { 
    "type": "point",
    "coordinates": [0.5, 3.0]
  }
}
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/2
{
  "geometry" : {
    "type" : "polygon",
    "coordinates" : [
      [[2.5, 6.0],
      [0.5, 4.5], 
      [1.5, 2.0], 
      [3.5, 3.5],
      [2.5, 6.0]]
    ]
  }
}
```
{% include copy-curl.html %}

使用篩選器搜尋在索引 `testindex` 中其形狀與 `rectangle` 相交的文件：

```json
GET testindex/_search
{
  "query": {
    "bool": {
      "filter": {
        "xy_shape": {
          "geometry": {
            "indexed_shape": {
              "index": "pre-indexed-shapes",
              "id": "rectangle",
              "path": "geometry"
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

上述查詢使用預設空間關係 `INTERSECTS`，並同時傳回點和多邊形：

```json
{
  "took" : 26,
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
    "max_score" : 0.0,
    "hits" : [
      {
        "_index" : "testindex",
        "_id" : "1",
        "_score" : 0.0,
        "_source" : {
          "geometry" : {
            "type" : "point",
            "coordinates" : [
              0.5,
              3.0
            ]
          }
        }
      },
      {
        "_index" : "testindex",
        "_id" : "2",
        "_score" : 0.0,
        "_source" : {
          "geometry" : {
            "type" : "polygon",
            "coordinates" : [
              [
                [
                  2.5,
                  6.0
                ],
                [
                  0.5,
                  4.5
                ],
                [
                  1.5,
                  2.0
                ],
                [
                  3.5,
                  3.5
                ],
                [
                  2.5,
                  6.0
                ]
              ]
            ]
          }
        }
      }
    ]
  }
}
```

## 查詢 xy point

您也可以使用 xy 查詢來搜尋包含 xy point 的文件。 

建立對應，將 `point` 設為 `xy_point`：

```json
PUT testindex1
{
  "mappings": {
    "properties": {
      "point": {
        "type": "xy_point"
      }
    }
  }
}
```
{% include copy-curl.html %}

將三個點編製索引：

```json
PUT testindex1/_doc/1
{
  "point": "1.0, 1.0" 
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/2
{
  "point": "2.0, 0.0" 
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/3
{
  "point": "-2.0, 2.0" 
}
```
{% include copy-curl.html %}

搜尋位於圓心為 (0, 0) 且半徑為 2 的圓內的點：

```json
GET testindex1/_search
{
  "query": {
    "xy_shape": {
      "point": {
        "shape": {
          "type": "circle",
          "coordinates": [0.0, 0.0],
          "radius": 2
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

xy point 僅支援預設的 `INTERSECTS` 空間關係，因此您不需要提供 `relation` 參數。
{: .note}

下圖說明此範例。點 1 和點 2 位於圓內，而點 3 位於圓外。

![xy point 查詢]({{site.url}}{{site.baseurl}}/images/xy_query_point.png){: width="300" }

回應會傳回文件 1 和 2：

```json
{
  "took" : 575,
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
    "max_score" : 0.0,
    "hits" : [
      {
        "_index" : "testindex1",
        "_id" : "1",
        "_score" : 0.0,
        "_source" : {
          "point" : "1.0, 1.0"
        }
      },
      {
        "_index" : "testindex1",
        "_id" : "2",
        "_score" : 0.0,
        "_source" : {
          "point" : "2.0, 0.0"
        }
      }
    ]
  }
}
```