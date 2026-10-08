---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Geotile 網格"
parent: Bucket aggregations
nav_order: 87
redirect_from:
  - /query-dsl/aggregations/bucket/geotile-grid/
---

# Geotile 網格彙總

Geotile 網格彙總會將文件分組到網格單元中，以進行地理分析。每個網格單元都對應一個[地圖圖磚](https://en.wikipedia.org/wiki/Tiled_web_map)，並使用 `{zoom}/{x}/{y}` 格式來識別。您可以使用 geotile 網格彙總，對 [geopoint]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-point/) 或 [geoshape]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-shape/) 欄位中的文件進行彙總。一個值得注意的差異是，geopoint 只會出現在一個桶 (bucket) 中，而 geoshape 則會計入與其相交的所有 geotile 網格單元。

## 精確度

`precision` 參數控制決定網格單元大小的細微程度。精確度越低，網格單元就越大。

下列範例說明低精確度和高精確度的彙總請求。

首先，建立索引，並將 `location` 欄位對應為 `geo_point`：

```json
PUT national_parks
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

將下列文件編製索引到範例索引中：

```json
PUT national_parks/_doc/1
{
  "name": "Yellowstone National Park",
  "location": "44.42, -110.59" 
}
```
{% include copy-curl.html %}

```json
PUT national_parks/_doc/2
{
  "name": "Yosemite National Park",
  "location": "37.87, -119.53" 
}
```
{% include copy-curl.html %}

```json
PUT national_parks/_doc/3
{
  "name": "Death Valley National Park",
  "location": "36.53, -116.93" 
}
```
{% include copy-curl.html %}

您可以使用多種格式為 geopoint 編製索引。如需所有支援格式的清單，請參閱 [geopoint 文件]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point#formats)。
{: .note}

## 低精確度請求

執行一個將三份文件全部分到同一個桶的低精確度請求：

```json
GET national_parks/_search
{
  "aggregations": {
    "grouped": {
      "geotile_grid": {
        "field": "location",
        "precision": 1
      }
    }
  }
}
```
{% include copy-curl.html %}

您可以使用 `GET` 或 `POST` HTTP 方法來執行 geotile 網格彙總查詢。
{: .note}

回應會將所有文件分在同一組，因為這些文件彼此距離夠近，可以分到同一個網格單元中：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 51,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "national_parks",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Yellowstone National Park",
          "location": "44.42, -110.59"
        }
      },
      {
        "_index": "national_parks",
        "_id": "2",
        "_score": 1,
        "_source": {
          "name": "Yosemite National Park",
          "location": "37.87, -119.53"
        }
      },
      {
        "_index": "national_parks",
        "_id": "3",
        "_score": 1,
        "_source": {
          "name": "Death Valley National Park",
          "location": "36.53, -116.93"
        }
      }
    ]
  },
  "aggregations": {
    "grouped": {
      "buckets": [
        {
          "key": "1/0/0",
          "doc_count": 3
        }
      ]
    }
  }
}
```
</details>

## 高精確度請求

現在執行一個高精確度請求：

```json
GET national_parks/_search
{
  "aggregations": {
    "grouped": {
      "geotile_grid": {
        "field": "location",
        "precision": 6
      }
    }
  }
}
```
{% include copy-curl.html %}

由於細微程度較高，三份文件都會分別分到不同的桶中：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}
  
```json
{
  "took": 15,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "national_parks",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Yellowstone National Park",
          "location": "44.42, -110.59"
        }
      },
      {
        "_index": "national_parks",
        "_id": "2",
        "_score": 1,
        "_source": {
          "name": "Yosemite National Park",
          "location": "37.87, -119.53"
        }
      },
      {
        "_index": "national_parks",
        "_id": "3",
        "_score": 1,
        "_source": {
          "name": "Death Valley National Park",
          "location": "36.53, -116.93"
        }
      }
    ]
  },
  "aggregations": {
    "grouped": {
      "buckets": [
        {
          "key": "6/12/23",
          "doc_count": 1
        },
        {
          "key": "6/11/25",
          "doc_count": 1
        },
        {
          "key": "6/10/24",
          "doc_count": 1
        }
      ]
    }
  }
}
```
</details>

您也可以在 `bounds` 參數中提供邊界範圍的座標，以限制地理區域。`bounds` 和 `geo_bounding_box` 座標都可以使用任何一種 [geopoint 格式]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point#formats) 來指定。下列查詢對 `bounds` 參數使用 well-known text (WKT) 「POINT(`longitude` `latitude`)」格式：

```json
GET national_parks/_search
{
  "size": 0,
  "aggregations": {
    "grouped": {
      "geotile_grid": {
        "field": "location",
        "precision": 6,
        "bounds": {
            "top_left": "POINT (-120 38)",
            "bottom_right": "POINT (-116 36)"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應只包含位於指定邊界內的兩筆結果：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}
  
```json
{
  "took": 48,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "national_parks",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Yellowstone National Park",
          "location": "44.42, -110.59"
        }
      },
      {
        "_index": "national_parks",
        "_id": "2",
        "_score": 1,
        "_source": {
          "name": "Yosemite National Park",
          "location": "37.87, -119.53"
        }
      },
      {
        "_index": "national_parks",
        "_id": "3",
        "_score": 1,
        "_source": {
          "name": "Death Valley National Park",
          "location": "36.53, -116.93"
        }
      }
    ]
  },
  "aggregations": {
    "grouped": {
      "buckets": [
        {
          "key": "6/11/25",
          "doc_count": 1
        },
        {
          "key": "6/10/24",
          "doc_count": 1
        }
      ]
    }
  }
}
```
</details>

`bounds` 參數可以搭配或不搭配 `geo_bounding_box` 篩選器使用；這兩個參數彼此獨立，兩者之間可以有任何空間關係。

## 彙總 geoshape

若要對 geoshape 欄位執行彙總，請先建立索引，並將 `location` 欄位對應為 `geo_shape`：

```json
PUT national_parks
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

接著，將一些文件編製索引至 `national_parks` 索引：

```json
PUT national_parks/_doc/1
{
  "name": "Yellowstone National Park",
  "location":
  {"type": "envelope","coordinates": [ [-111.15, 45.12], [-109.83, 44.12] ]}
}
```
{% include copy-curl.html %}

```json
PUT national_parks/_doc/2
{
  "name": "Yosemite National Park",
  "location": 
  {"type": "envelope","coordinates": [ [-120.23, 38.16], [-119.05, 37.45] ]}
}
```
{% include copy-curl.html %}

```json
PUT national_parks/_doc/3
{
  "name": "Death Valley National Park",
  "location": 
  {"type": "envelope","coordinates": [ [-117.34, 37.01], [-116.38, 36.25] ]}
}
```
{% include copy-curl.html %}

您可以依下列方式對 `location` 欄位執行彙總：

```json
GET national_parks/_search
{
  "aggregations": {
    "grouped": {
      "geotile_grid": {
        "field": "location",
        "precision": 6
      }
    }
  }
}
```
{% include copy-curl.html %}

彙總 geoshape 時，一個 geoshape 可能會計入多個桶，因為它與多個網格單元重疊：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took" : 3,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "national_parks",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "name" : "Yellowstone National Park",
          "location" : {
            "type" : "envelope",
            "coordinates" : [
              [
                -111.15,
                45.12
              ],
              [
                -109.83,
                44.12
              ]
            ]
          }
        }
      },
      {
        "_index" : "national_parks",
        "_id" : "2",
        "_score" : 1.0,
        "_source" : {
          "name" : "Yosemite National Park",
          "location" : {
            "type" : "envelope",
            "coordinates" : [
              [
                -120.23,
                38.16
              ],
              [
                -119.05,
                37.45
              ]
            ]
          }
        }
      },
      {
        "_index" : "national_parks",
        "_id" : "3",
        "_score" : 1.0,
        "_source" : {
          "name" : "Death Valley National Park",
          "location" : {
            "type" : "envelope",
            "coordinates" : [
              [
                -117.34,
                37.01
              ],
              [
                -116.38,
                36.25
              ]
            ]
          }
        }
      }
    ]
  },
  "aggregations" : {
    "grouped" : {
      "buckets" : [
        {
          "key" : "6/12/23",
          "doc_count" : 1
        },
        {
          "key" : "6/12/22",
          "doc_count" : 1
        },
        {
          "key" : "6/11/25",
          "doc_count" : 1
        },
        {
          "key" : "6/11/24",
          "doc_count" : 1
        },
        {
          "key" : "6/10/24",
          "doc_count" : 1
        }
      ]
    }
  }
}
```
</details>

OpenSearch 支援透過 API 進行 geoshape 彙總，但 OpenSearch Dashboards 視覺化尚不支援。如果您希望視覺化也能實作 geoshape 彙總，請為相關的 [GitHub 議題](https://github.com/opensearch-project/dashboards-maps/issues/250)投票。
{: .note}

## 支援的參數

Geotile 網格彙總請求支援下列參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
field | 字串 | 包含 geopoint 的欄位。此欄位必須對應為 `geo_point` 欄位。如果欄位包含陣列，則會彙總所有陣列值。必要。
`precision` | 整數 | 用於決定網格單元以將結果分桶的精細度層級。單元不得超過所需精確度的指定大小（對角線）。有效值範圍為 [0, 29]。選用。預設值為 7。 
`bounds` | 物件 | 用於篩選 geopoint 的邊界框。邊界框由左上角與右下角頂點定義。頂點以 geopoint 形式指定，可使用下列任一格式：<br>- 包含緯度與經度的物件<br>- [`longitude`, `latitude`] 格式的陣列<br>- 「`latitude`,`longitude`」格式的字串<br>- geohash <br>- WKT<br> 如需格式範例，請參閱 [geopoint 格式]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point#formats)。選用。
`size` | 整數 | 要傳回的桶數上限。當桶數多於 `size` 時，OpenSearch 會傳回包含較多文件的桶。選用。預設值為 10,000。
`shard_size` | 整數 | 從每個分片傳回的桶數上限。選用。預設值為 max (10, `size` &middot; 分片數量)，可為優先順序較高的桶提供較準確的計數。