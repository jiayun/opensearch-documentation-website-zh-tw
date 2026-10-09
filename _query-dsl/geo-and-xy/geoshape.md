---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Geoshape
parent: Geographic and xy queries
nav_order: 40
---

# Geoshape 查詢

使用 geoshape 查詢來搜尋包含 [geopoint]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point/) 或 [geoshape]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-shape/) 欄位的文件。您可以使用[在查詢中定義的 geoshape](#using-a-new-shape-definition)來篩選文件，或使用[預先編製索引的 geoshape](#using-a-pre-indexed-shape-definition)。

被搜尋的文件欄位必須對應為 `geo_point` 或 `geo_shape`。
{: .note}

## 空間關係

當您提供 geoshape 給 geoshape 查詢時，文件中的 geopoint 和 geoshape 欄位會使用下列空間關係與提供的形狀進行比對。

關係 | 說明 | 支援的地理欄位類型
:--- | :--- | :--- 
`INTERSECTS` | (預設) 比對其 geopoint 或 geoshape 與查詢中提供的形狀相交的文件。 | `geo_point`, `geo_shape`
`DISJOINT` | 比對其 geoshape 與查詢中提供的形狀不相交的文件。 | `geo_shape`
`WITHIN` | 比對其 geoshape 完全位於查詢中提供的形狀內的文件。 | `geo_shape`
`CONTAINS` | 比對其 geoshape 完全包含查詢中提供的形狀的文件。 | `geo_shape`

## 在 geoshape 查詢中定義形狀

您可以在 geoshape 查詢中定義用來篩選文件的形狀，方法是[在查詢時提供新的形狀定義](#using-a-new-shape-definition)，或[參照在另一個索引中預先編製索引的形狀名稱](#using-a-pre-indexed-shape-definition)。  

## 使用新的形狀定義

若要提供新的形狀給 geoshape 查詢，請在 `geo_shape` 欄位中定義它。您可以使用 [GeoJSON 格式](https://geojson.org/)或 [Well-Known Text (WKT) 格式](https://docs.opengeospatial.org/is/12-063r5/12-063r5.html)來定義 geoshape。 

下列範例說明如何搜尋包含 geoshape 且符合查詢時所定義之 geoshape 的文件。

### 步驟 1：建立索引

首先，建立索引並將 `location` 欄位對應為 `geo_shape`：

```json
PUT /testindex
{
  "mappings": {
    "properties": {
      "location": {
        "type": "geo_shape"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 2：將文件編製索引

將一個包含點的文件和另一個包含多邊形的文件編製索引：

```json
PUT testindex/_doc/1
{
  "location": {
    "type": "point",
    "coordinates": [ 73.0515, 41.5582 ]
  }
}
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/2
{
  "location": {
    "type": "polygon",
    "coordinates": [
      [
        [
          73.0515,
          41.5582
        ],
        [
          72.6506,
          41.5623
        ],
        [
          72.6734,
          41.7658
        ],
        [
          73.0515,
          41.5582
        ]
      ]
    ]
  }
}
```
{% include copy-curl.html %}

### 步驟 3：執行 geoshape 查詢

最後，定義 geoshape 來篩選文件。下列各節說明如何在查詢中提供各種 geoshape。如需各種 geoshape 格式的詳細資訊，請參閱 [Geoshape 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-shape/)。 

#### 包絡矩形

[`envelope`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-shape#envelope) 是 `[[minLon, maxLat], [maxLon, minLat]]` 格式的邊界矩形。搜尋包含 geoshape 欄位且與提供的包絡矩形相交的文件：

```json
GET /testindex/_search
{
  "query": {
    "geo_shape": {
      "location": {
        "shape": {
          "type": "envelope",
          "coordinates": [
            [
              71.0589,
              42.3601
            ],
            [
              74.006,
              40.7128
            ]
          ]
        },
        "relation": "WITHIN"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含這兩份文件：

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
    "max_score": 0,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0,
        "_source": {
          "location": {
            "type": "point",
            "coordinates": [
              73.0515,
              41.5582
            ]
          }
        }
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 0,
        "_source": {
          "location": {
            "type": "polygon",
            "coordinates": [
              [
                [
                  73.0515,
                  41.5582
                ],
                [
                  72.6506,
                  41.5623
                ],
                [
                  72.6734,
                  41.7658
                ],
                [
                  73.0515,
                  41.5582
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

#### 點

搜尋其 geoshape 欄位包含所提供點的文件：

```json
GET /testindex/_search
{
  "query": {
    "geo_shape": {
      "location": {
        "shape": {
          "type": "point",
          "coordinates": [
            72.8000, 
            41.6300
          ]
        },
        "relation": "CONTAINS"
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 線串

搜尋其 geoshape 欄位與提供的線串不相交的文件：

```json
GET /testindex/_search
{
  "query": {
    "geo_shape": {
      "location": {
        "shape": {
          "type": "linestring",
          "coordinates": [[74.0060, 40.7128], [71.0589, 42.3601]]
        },
        "relation": "DISJOINT"
      }
    }
  }
}
```
{% include copy-curl.html %}

線串 geoshape 查詢不支援 `WITHIN` 關係。
{: .note}

#### 多邊形

在 GeoJSON 格式中，您必須以逆時針順序列出多邊形的頂點，並封閉多邊形，使第一個頂點和最後一個頂點相同。

搜尋其 geoshape 欄位位於所提供多邊形內的文件：

```json
GET /testindex/_search
{
  "query": {
    "geo_shape": {
      "location": {
        "shape": {
          "type": "polygon",
          "coordinates": [
            [
              [74.0060, 40.7128], 
              [73.7562, 42.6526], 
              [71.0589, 42.3601], 
              [74.0060, 40.7128]
            ]
          ]
        },
        "relation": "WITHIN"
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 多點

搜尋其 geoshape 欄位與提供的點不相交的文件：

```json
GET /testindex/_search
{
  "query": {
    "geo_shape": {
      "location": {
        "shape": {
          "type": "multipoint",
          "coordinates" : [
            [74.0060, 40.7128], 
            [71.0589, 42.3601]
          ]
        },
        "relation": "DISJOINT"
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 多線串

搜尋其 geoshape 欄位與提供的線不相交的文件：

```json
GET /testindex/_search
{
  "query": {
    "geo_shape": {
      "location": {
        "shape": {
          "type": "multilinestring",
          "coordinates" : [
            [[74.0060, 40.7128], [71.0589, 42.3601]],
            [[73.7562, 42.6526], [72.6734, 41.7658]]
          ]
        },
        "relation": "disjoint"
      }
    }
  }
}
```
{% include copy-curl.html %}

多線串 geoshape 查詢不支援 `WITHIN` 關係。
{: .note}

#### 多重多邊形

搜尋 geoshape 欄位位於所提供多重多邊形內的文件：

```json
GET /testindex/_search
{
  "query": {
    "geo_shape": {
      "location": {
        "shape": {
          "type" : "multipolygon",
          "coordinates" : [
          [
            [
              [74.0060, 40.7128], 
              [73.7562, 42.6526], 
              [71.0589, 42.3601], 
              [74.0060, 40.7128]
            ],
            [
              [73.0515, 41.5582], 
              [72.6506, 41.5623], 
              [72.6734, 41.7658], 
              [73.0515, 41.5582]
            ]
          ],
          [
            [
              [73.9146, 40.8252], 
              [73.8871, 41.0389], 
              [73.6853, 40.9747], 
              [73.9146, 40.8252]
            ]
          ]
        ]
        },
        "relation": "WITHIN"
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 幾何集合

搜尋 geoshape 欄位位於所提供多邊形內的文件：

```json
GET /testindex/_search
{
  "query": {
    "geo_shape": {
      "location": {
        "shape": {
          "type": "geometrycollection",
          "geometries": [
            {
              "type": "polygon",
              "coordinates": [[
                [74.0060, 40.7128], 
                [73.7562, 42.6526], 
                [71.0589, 42.3601], 
                [74.0060, 40.7128]
              ]]
            },
            {
              "type": "polygon",
              "coordinates": [[
                [73.0515, 41.5582], 
                [72.6506, 41.5623], 
                [72.6734, 41.7658], 
                [73.0515, 41.5582]
              ]]
            }
          ]
        },
        "relation": "WITHIN"
      }
    }
  }
}
```
{% include copy-curl.html %}

幾何集合包含 linestring 或 multilinestring 的 geoshape 查詢不支援 `WITHIN` 關係。
{: .note}

## 使用預先編製索引的形狀定義

建構 geoshape 查詢時，您也可以參照預先編製索引在其他索引中的形狀名稱。使用此方法，您可以在編製索引時定義 geoshape，並在搜尋時依名稱參照它。

您可以使用 [GeoJSON](https://geojson.org/) 或 [Well-Known Text (WKT)](https://docs.opengeospatial.org/is/12-063r5/12-063r5.html) 格式定義預先編製索引的 geoshape。如需各種 geoshape 格式的更多資訊，請參閱 [Geoshape 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-shape/)。

`indexed_shape` 物件支援下列參數。

參數 | 必要／選用 | 說明
:--- | :--- | :---
`id` | 必要 | 包含預先編製索引形狀之文件的文件 ID。
`index` | 選用 | 包含預先編製索引形狀之索引的名稱。預設為 `shapes`。
`path` | 選用 | 包含預先編製索引形狀之欄位的欄位名稱（以路徑表示）。預設為 `shape`。
`routing` | 選用 | 包含預先編製索引形狀之文件的路由值。如果形狀文件是以自訂路由值編製索引，則為必要。

下列範例說明如何參照預先編製索引在其他索引中的形狀名稱。在此範例中，索引 `pre-indexed-shapes` 包含定義邊界的形狀，而索引 `testindex` 包含要對照這些邊界檢查的形狀。

首先，建立 `pre-indexed-shapes` 索引，並將此索引的 `boundaries` 欄位對應為 `geo_shape`：

```json
PUT /pre-indexed-shapes
{
  "mappings": {
    "properties": {
      "boundaries": {
        "type": "geo_shape",
        "orientation" : "left"
      }
    }
  }
}
```
{% include copy-curl.html %}

如需為多邊形指定不同頂點方向的更多資訊，請參閱 [多邊形]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-shape/#polygon)。

將指定搜尋邊界的多邊形編製索引至 `pre-indexed-shapes` 索引。該多邊形的 ID 為 `search_triangle`。在此範例中，您將以 WKT 格式編製索引該多邊形：

```json
PUT /pre-indexed-shapes/_doc/search_triangle
{
  "boundaries": 
    "POLYGON ((74.0060 40.7128, 71.0589 42.3601, 73.7562 42.6526, 74.0060 40.7128))"
}
```
{% include copy-curl.html %}

如果您尚未這樣做，請將一個包含點的文件和另一個包含多邊形的文件編製索引至 `testindex` 索引：

```json
PUT /testindex/_doc/1
{
  "location": {
    "type": "point",
    "coordinates": [ 73.0515, 41.5582 ]
  }
}
```
{% include copy-curl.html %}

```json
PUT /testindex/_doc/2
{
  "location": {
    "type": "polygon",
    "coordinates": [
      [
        [
          73.0515,
          41.5582
        ],
        [
          72.6506,
          41.5623
        ],
        [
          72.6734,
          41.7658
        ],
        [
          73.0515,
          41.5582
        ]
      ]
    ]
  }
}
```
{% include copy-curl.html %}

搜尋 geoshape 位於 `search_triangle` 內的文件：

```json
GET /testindex/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "geo_shape": {
          "location": {
            "indexed_shape": {
              "index": "pre-indexed-shapes",
              "id": "search_triangle",
              "path": "boundaries"
            },
            "relation": "WITHIN"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含這兩個文件：

```json
{
  "took": 11,
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
        "_index": "testindex",
        "_id": "1",
        "_score": 1,
        "_source": {
          "location": {
            "type": "point",
            "coordinates": [
              73.0515,
              41.5582
            ]
          }
        }
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 1,
        "_source": {
          "location": {
            "type": "polygon",
            "coordinates": [
              [
                [
                  73.0515,
                  41.5582
                ],
                [
                  72.6506,
                  41.5623
                ],
                [
                  72.6734,
                  41.7658
                ],
                [
                  73.0515,
                  41.5582
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

## 查詢 geopoint

您也可以使用 geoshape 查詢來搜尋包含 geopoint 的文件。

針對 geopoint 欄位的 geoshape 查詢僅支援預設的 `INTERSECTS` 空間關係，因此您不需要提供 `relation` 參數。
{: .note}

{: .important }
> 針對 geopoint 欄位的 geoshape 查詢不支援下列 geoshape：
> 
> - 點
> - 線串
> - 多點
> - 多線串
> - 包含上述任一 geoshape 類型的幾何集合

建立一個對應，其中 `location` 為 `geo_point`：

```json
PUT /testindex1
{
  "mappings": {
    "properties": {
      "location": {
        "type": "geo_point"
      }
    }
  }
}
```
{% include copy-curl.html %}

將兩個點編製索引至該索引。在此範例中，您將以字串提供 geopoint 座標：

```json
PUT /testindex1/_doc/1
{
  "location": "41.5623, 72.6506"
}
```
{% include copy-curl.html %}

```json
PUT /testindex1/_doc/2
{
  "location": "76.0254, 39.2467" 
}
```
{% include copy-curl.html %}

 如需以各種格式提供 geopoint 座標的資訊，請參閱 [格式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-point/#formats)。

搜尋與所提供多邊形相交的 geopoint：

```json
GET /testindex1/_search
{
  "query": {
    "geo_shape": {
      "location": {
        "shape": {
          "type": "polygon",
          "coordinates": [
            [
              [74.0060, 40.7128], 
              [73.7562, 42.6526], 
              [71.0589, 42.3601], 
              [74.0060, 40.7128]
            ]
          ]
        }
      }
    }
  }
}

```
{% include copy-curl.html %}

回應傳回文件 1：

```json
{
  "took": 21,
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
    "max_score": 0,
    "hits": [
      {
        "_index": "testindex1",
        "_id": "1",
        "_score": 0,
        "_source": {
          "location": "41.5623, 72.6506"
        }
      }
    ]
  }
}
```

請注意，當您編製索引 geopoint 時，您以 `"latitude, longitude"` 格式指定其座標。當您搜尋符合的文件時，座標陣列為 `[longitude, latitude]` 格式。因此，文件 1 會出現在結果中，但文件 2 不會。

## 參數

Geoshape 查詢接受下列參數。

參數 | 資料類型 | 說明
:--- | :--- | :--- 
`ignore_unmapped` | 布林值 | 指定是否忽略未對應的欄位。若設為 `true`，則查詢不會傳回任何包含未對應欄位的文件。若設為 `false`，則當欄位未對應時會擲回例外。選用。預設為 `false`。

## 高成本查詢

Geoshape 欄位預設會將圖形儲存在 BKD 樹狀結構中，且對這些欄位的查詢不論 [`search.allow_expensive_queries`]({{site.url}}{{site.baseurl}}/query-dsl/index/#expensive-queries) 設定為何都會執行。

以 `tree` 或 `strategy` 參數對應的 geoshape 欄位則會將圖形儲存在前綴樹狀結構中。對前綴樹狀結構欄位的查詢只有在 `search.allow_expensive_queries` 為 `true` 時才會執行。