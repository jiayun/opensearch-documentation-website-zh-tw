---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Geohex 網格"
parent: Bucket aggregations
nav_order: 85
redirect_from:
  - /opensearch/geohexgrid-agg/
  - /query-dsl/aggregations/geohexgrid-agg/
  - /aggregations/geohexgrid/
  - /query-dsl/aggregations/geohexgrid/
  - /query-dsl/aggregations/bucket/geohex-grid/
---

# Geohex 網格彙總

六角形階層式地理空間索引系統 (Hexagonal Hierarchical Geospatial Indexing System，H3) 會將地球的區域分割成可識別的六角形網格單元。

H3 網格系統克服了 Geohash 分區不均勻的限制，因此非常適合用於鄰近性應用。Geohash 會對緯度與經度組合進行編碼，導致極點附近的分區明顯較小，而赤道附近的分區則約為一個經度。然而，H3 網格系統的失真程度很低，且僅限於 122 個分區中的 5 個。這五個分區位於使用率較低的區域（例如海洋中央），使重要區域不受誤差影響。因此，根據 H3 網格系統將文件分組，可提供比 Geohash 網格更好的彙總結果。

Geohex 網格彙總會將[地理點]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point/)分組到網格單元中，以進行地理分析。每個網格單元都對應一個 [H3 網格單元](https://h3geo.org/docs/core-library/h3Indexing/#h3-cell-indexp)，並使用 [H3Index 表示法](https://h3geo.org/docs/core-library/h3Indexing/#h3index-representation)加以識別。

## 精確度

`precision` 參數控制決定網格單元大小的精細程度。精確度越低，網格單元就越大。

下列範例說明低精確度與高精確度的彙總請求。

首先，建立索引並將 `location` 欄位對應為 `geo_point`：

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

您可以使用多種格式將地理點編製索引。如需所有支援格式的清單，請參閱[地理點文件]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point#formats)。
{: .note}

## 低精確度請求

執行低精確度請求，將這三份文件一起分桶 (bucket)：

```json
GET national_parks/_search
{
  "aggregations": {
    "grouped": {
      "geohex_grid": {
        "field": "location",
        "precision": 1
      }
    }
  }
}
```
{% include copy-curl.html %}

您可以使用 `GET` 或 `POST` HTTP 方法執行 Geohex 網格彙總查詢。
{: .note}

回應將文件 2 與文件 3 分在同一組，因為它們的距離夠近，可以歸入同一個網格單元的桶中：

```json
{
  "took" : 4,
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
          "location" : "44.42, -110.59"
        }
      },
      {
        "_index" : "national_parks",
        "_id" : "2",
        "_score" : 1.0,
        "_source" : {
          "name" : "Yosemite National Park",
          "location" : "37.87, -119.53"
        }
      },
      {
        "_index" : "national_parks",
        "_id" : "3",
        "_score" : 1.0,
        "_source" : {
          "name" : "Death Valley National Park",
          "location" : "36.53, -116.93"
        }
      }
    ]
  },
  "aggregations" : {
    "grouped" : {
      "buckets" : [
        {
          "key" : "8129bffffffffff",
          "doc_count" : 2
        },
        {
          "key" : "8128bffffffffff",
          "doc_count" : 1
        }
      ]
    }
  }
}
```

## 高精確度請求

現在執行高精確度請求：

```json
GET national_parks/_search
{
  "aggregations": {
    "grouped": {
      "geohex_grid": {
        "field": "location",
        "precision": 6
      }
    }
  }
}
```
{% include copy-curl.html %}

由於精細程度較高，這三份文件會分別歸入不同的桶：

```json
{
  "took" : 5,
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
          "location" : "44.42, -110.59"
        }
      },
      {
        "_index" : "national_parks",
        "_id" : "2",
        "_score" : 1.0,
        "_source" : {
          "name" : "Yosemite National Park",
          "location" : "37.87, -119.53"
        }
      },
      {
        "_index" : "national_parks",
        "_id" : "3",
        "_score" : 1.0,
        "_source" : {
          "name" : "Death Valley National Park",
          "location" : "36.53, -116.93"
        }
      }
    ]
  },
  "aggregations" : {
    "grouped" : {
      "buckets" : [
        {
          "key" : "8629ab6dfffffff",
          "doc_count" : 1
        },
        {
          "key" : "8629857a7ffffff",
          "doc_count" : 1
        },
        {
          "key" : "862896017ffffff",
          "doc_count" : 1
        }
      ]
    }
  }
}
```

## 篩選請求

高精確度請求會耗用大量資源，因此建議您使用 `geo_bounding_box` 之類的篩選條件來限制地理區域。例如，下列查詢套用篩選條件來限制搜尋區域：

```json
GET national_parks/_search
{
  "size" : 0,  
  "aggregations": {
    "filtered": {
      "filter": {
        "geo_bounding_box": {
          "location": {
            "top_left": "38, -120",
            "bottom_right": "36, -116"
          }
        }
      },
      "aggregations": {
        "grouped": {
          "geohex_grid": {
            "field": "location",
            "precision": 6
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含位於 `geo_bounding_box` 邊界內的兩份文件：

```json
{
  "took" : 4,
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
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "filtered" : {
      "doc_count" : 2,
      "grouped" : {
        "buckets" : [
          {
            "key" : "8629ab6dfffffff",
            "doc_count" : 1
          },
          {
            "key" : "8629857a7ffffff",
            "doc_count" : 1
          }
        ]
      }
    }
  }
}
```

您也可以在 `bounds` 參數中提供邊界範圍的座標，以限制地理區域。`bounds` 與 `geo_bounding_box` 座標皆可使用任一種[地理點格式]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point#formats)指定。下列查詢對 `bounds` 參數使用 well-known text (WKT) "POINT(`longitude` `latitude`)" 格式：

```json
GET national_parks/_search
{
  "size": 0,
  "aggregations": {
    "grouped": {
      "geohex_grid": {
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

回應僅包含位於指定邊界內的兩筆結果：

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
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "grouped" : {
      "buckets" : [
        {
          "key" : "8629ab6dfffffff",
          "doc_count" : 1
        },
        {
          "key" : "8629857a7ffffff",
          "doc_count" : 1
        }
      ]
    }
  }
}
```

`bounds` 參數可以搭配或不搭配 `geo_bounding_box` 篩選條件使用；這兩個參數彼此獨立，兩者之間可以有任何空間關係。

## 支援的參數

Geohex 網格彙總請求支援下列參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
field | 字串 | 包含地理點的欄位。此欄位必須對應為 `geo_point` 欄位。若欄位包含陣列，則會彙總所有陣列值。必要。
`precision` | 整數 | 用於決定網格單元以將結果分桶的精細程度。網格單元不得超過所需精確度的指定大小（對角線）。有效值範圍為 [0, 15]。選用。預設值為 5。
`bounds` | 物件 | 用於篩選地理點的邊界方塊。邊界方塊由左上角與右下角頂點定義。頂點以地理點指定，格式可為下列其中一種：<br>- 包含緯度與經度的物件<br>- [`longitude`, `latitude`] 格式的陣列<br>- "`latitude`,`longitude`" 格式的字串<br>- Geohash <br>- WKT<br> 如需格式範例，請參閱[地理點格式]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point#formats)。選用。
`size` | 整數 | 要傳回的桶數上限。當桶數多於 `size` 時，OpenSearch 會傳回包含較多文件的桶。選用。預設值為 10,000。
`shard_size` | 整數 | 每個分片要傳回的桶數上限。選用。預設值為 max (10, `size` &middot; 分片數)，可為優先順序較高的桶提供較準確的計數。