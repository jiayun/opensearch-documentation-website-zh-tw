---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Geohash 網格"
parent: Bucket aggregations
nav_order: 80
redirect_from:
  - /query-dsl/aggregations/bucket/geohash-grid/
---

# Geohash 網格彙總

`geohash_grid` 彙總會根據文件的 [geohash](https://en.wikipedia.org/wiki/Geohash) 值，將文件分組至網格儲存格中。每個儲存格都以其 geohash 字串標示，而 precision 參數則控制儲存格的大小——精確度值越低，產生的儲存格越少、越大；精確度值越高，產生的儲存格越多、越小。您可以對 [geo_point]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point/) 或 [geo_shape]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-shape/) 欄位彙總文件。geo_point 只會放入一個儲存格，而 geo_shape 則會計入與其相交的每個儲存格。

精確度值的範圍為 1 到 12。高精確度的請求會產生大量的桶 (bucket)，因此可能耗用大量記憶體並產生龐大的回應。使用高精確度值之前，請先篩選至較小的地理區域。
{: .note}

## 參數

`geohash_grid` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 必要 | 字串 | 要進行彙總的欄位。必須對應為 `geo_point` 或 `geo_shape`。 |
| `precision` | 選用 | 整數或字串 | 控制儲存格大小的 geohash 長度。有效的整數值為 1 到 12。您也可以指定近似距離（例如 `1km` 或 `10m`），OpenSearch 會選取儲存格不超過該大小的精確度等級。預設為 `5`。 |
| `bounds` | 選用 | 物件 | 限制要納入考量之點的邊界框。只有位於邊界框內的點才會進行彙總。接受所有 [geo_point 格式]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point#formats)。 |
| `size` | 選用 | 整數 | 要傳回的桶數上限。當桶數多於 `size` 時，會傳回文件計數最高的桶。預設為 `10000`。 |
| `shard_size` | 選用 | 整數 | 每個分片傳回的桶數上限。預設為 max(10, `size` × 分片數)。 |

## 範例：低精確度網格

下列範例將電子商務客戶位置分組至精確度 4（約 39 km × 19.5 km）的 geohash 儲存格中：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "geo_hash": {
      "geohash_grid": {
        "field": "geoip.location",
        "precision": 4
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：搭配邊界框篩選的高精確度網格

放大檢視特定區域時，請先將文件篩選至該區域，再請求高精確度。下列範例使用 `geo_bounding_box` 查詢將範圍縮小至紐約市地區，然後以精確度 7（約 153 m × 152 m）進行彙總：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "zoomed_in": {
      "filter": {
        "geo_bounding_box": {
          "geoip.location": {
            "top_left": "41.0, -74.5",
            "bottom_right": "40.5, -73.5"
          }
        }
      },
      "aggs": {
        "detailed_grid": {
          "geohash_grid": {
            "field": "geoip.location",
            "precision": 7
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

下列回應對應高精確度範例：

```json
{
  "took": 23,
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
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "zoomed_in": {
      "doc_count": 896,
      "detailed_grid": {
        "buckets": [
          {
            "key": "dr72h56",
            "doc_count": 747
          },
          {
            "key": "dr5rs14",
            "doc_count": 149
          }
        ]
      }
    }
  }
}
```

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `buckets` | 陣列 | 網格儲存格的桶，依 `doc_count` 遞減排序。 |
| `buckets.key` | 字串 | 識別該儲存格的 geohash 字串。 |
| `buckets.doc_count` | 整數 | 此儲存格中的文件數（或 geoshape 相交數）。 |

您可以將傳回的 geohash 鍵同時作為 `geo_bounding_box` 查詢的 `top_left` 和 `bottom_right`，以更高的精確度放大檢視該儲存格。用戶端的 geohash 程式庫（例如 JavaScript 的 [ngeohash](https://github.com/sunng87/node-geohash)）可以將桶鍵解碼為經緯度邊界框，以便繪製地圖。
{: .tip}

## 彙總 geoshape

若要對 geoshape 欄位執行彙總，請先建立索引，並將 `location` 欄位對應為 `geo_shape`：

```json
PUT /national_parks
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
PUT /national_parks/_doc/1
{
  "name": "Yellowstone National Park",
  "location":
  {"type": "envelope","coordinates": [ [-111.15, 45.12], [-109.83, 44.12] ]}
}
```
{% include copy-curl.html %}

```json
PUT /national_parks/_doc/2
{
  "name": "Yosemite National Park",
  "location": 
  {"type": "envelope","coordinates": [ [-120.23, 38.16], [-119.05, 37.45] ]}
}
```
{% include copy-curl.html %}

```json
PUT /national_parks/_doc/3
{
  "name": "Death Valley National Park",
  "location": 
  {"type": "envelope","coordinates": [ [-117.34, 37.01], [-116.38, 36.25] ]}
}
```
{% include copy-curl.html %}

您可以依下列方式對 `location` 欄位執行彙總：

```json
GET /national_parks/_search
{
  "aggregations": {
    "grouped": {
      "geohash_grid": {
        "field": "location",
        "precision": 1
      }
    }
  }
}
```
{% include copy-curl.html %}

當 geoshape 橫跨多個網格儲存格時，可能會出現在多個桶中：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}
  
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
          "key" : "9",
          "doc_count" : 3
        },
        {
          "key" : "c",
          "doc_count" : 1
        }
      ]
    }
  }
}
```
</details>

OpenSearch 透過 API 支援 geoshape 彙總，但 OpenSearch Dashboards 視覺化不支援。
{: .note}

## Geohash 精確度

下表列出各精確度等級的近似儲存格尺寸。儲存格尺寸會隨緯度而變化；表中數值代表赤道處的最寬情況。

精確度 /<br>geohash 長度 | 緯度位元數 | 經度位元數 | 緯度誤差 | 經度誤差 | 儲存格高度 | 儲存格寬度
:---:|:-------------:|:--------------:|:--------------:|:---------------:|:-----------:|:----------:
  1  |       2       |       3        |      ±23       |       ±23       |  4992.6 km  | 5009.4 km  
  2  |       5       |       5        |      ±2.8      |      ±5.6       |  624.1 km   | 1252.3 km  
  3  |       7       |       8        |     ±0.70      |      ±0.70      |   156 km    |  156.5 km  
  4  |      10       |       10       |     ±0.087     |      ±0.18      |   19.5 km   |  39.1 km   
  5  |      12       |       13       |     ±0.022     |     ±0.022      |   4.9 km    |   4.9 km   
  6  |      15       |       15       |    ±0.0027     |     ±0.0055     |   609.4 m   |   1.2 km   
  7  |      17       |       18       |    ±0.00068    |    ±0.00068     |   152.5 m   |  152.9 m   
  8  |      20       |       20       |    ±0.00086    |    ±0.000172    |    19 m     |   38.2 m   
  9  |      22       |       23       |   ±0.000021    |    ±0.000021    |    4.8 m    |   4.8 m    
 10  |      25       |       25       |  ±0.00000268   |   ±0.00000536   |   59.5 cm   |   1.2 m    
 11  |      27       |       28       |  ±0.00000067   |   ±0.00000067   |   14.9 cm   |  14.9 cm   
 12  |      30       |       30       |  ±0.00000008   |   ±0.00000017   |   1.9 cm    |   3.7 cm   
