---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Geobounds
parent: Metric aggregations
nav_order: 40
redirect_from:
  - /query-dsl/aggregations/metric/geobounds/
---

# Geobounds 彙總

`geo_bounds` 彙總是一種多值彙總，可計算涵蓋一組 [`geo_point`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-point/) 或 [`geo_shape`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-shape/) 物件的[地理邊界框](https://docs.ogc.org/is/12-063r5/12-063r5.html#30)。邊界框會以矩形的左上角與右下角頂點傳回，並以十進位編碼的緯度-經度 (lat-lon) 配對表示。

## 參數

`geo_bounds` 彙總接受下列參數。

| 參數        | 必要/選用 | 資料類型      | 說明 |
| :--              | :--               | :--            | :--         |
| `field`          | 必要          | 字串         | 包含要計算地理邊界之 geopoint 或 geoshape 的欄位名稱。 |
| `wrap_longitude` | 選用          | 布林值        | 是否允許邊界框跨越國際換日線。預設為 `true`。 |

## 範例

下列範例會傳回電子商務範例資料中每筆訂單之 `geoip.location` 的 `geo_bounds`（每個 `geoip.location` 都是一個 geopoint）：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "geo": {
      "geo_bounds": {
        "field": "geoip.location"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

如下列回應範例所示，彙總會傳回包含 `geoip.location` 欄位中所有 geopoint 的 `geobounds`：

```json
{
  "took": 16,
  "timed_out": false,
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
    "geo": {
      "bounds": {
        "top_left": {
          "lat": 52.49999997206032,
          "lon": -118.20000001229346
        },
        "bottom_right": {
          "lat": 4.599999985657632,
          "lon": 55.299999956041574
        }
      }
    }
  }
}
```

## 彙總 geoshape

您可以對 geoshape 執行 `geo_bounds` 彙總。

先插入一個包含 geoshape 欄位的索引來準備範例：

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

將文件匯入索引。GeoJSON 輸入會先指定經度：

```json
POST _bulk
{ "create": { "_index": "national_parks", "_id": "1" } }
{"name": "Yellowstone National Park", "location": {"type": "envelope","coordinates": [ [-111.15, 45.12], [-109.83, 44.12] ]}}
{ "create": { "_index": "national_parks", "_id": "2" } }
{ "name": "Yosemite National Park", "location": {"type": "envelope","coordinates": [ [-120.23, 38.16], [-119.05, 37.45] ]} }
{ "create": { "_index": "national_parks", "_id": "3" } }
{ "name": "Death Valley National Park", "location": {"type": "envelope","coordinates": [ [-117.34, 37.01], [-116.38, 36.25] ]} }
{ "create": { "_index": "national_parks", "_id": "4" } }
{ "name": "War In The Pacific National Historic Park Guam", "location": {"type": "point","coordinates": [144.72, 13.47]} }
```
{% include copy-curl.html %}

對 `location` 欄位執行 `geo_bounds` 彙總：

```json
GET national_parks/_search
{
  "size": 0,
  "aggregations": {
    "grouped": {
      "geo_bounds": {
        "field": "location",
        "wrap_longitude": true
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含能涵蓋 `location` 欄位中所有形狀的最小地理邊界框：

```json
{
  "took": 8,
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
    "hits": []
  },
  "aggregations": {
    "grouped": {
      "bounds": {
        "top_left": {
          "lat": 45.11999997776002,
          "lon": 144.71999991685152
        },
        "bottom_right": {
          "lat": 13.469999986700714,
          "lon": -109.83000006526709
        }
      }
    }
  }
}
```

## 經度環繞

若將選用的 `wrap_longitude` 參數設為 `true`，邊界框便可跨越國際換日線（180&deg; 經線），並傳回左上角經度大於右下角經度的 `bounds` 物件。`wrap_longitude` 的預設值為 `true`。

將 `wrap_longitude` 設為 `false`，對國家公園的 geoshape 重新執行 `geo_bounds` 彙總：

```json
GET national_parks/_search
{
  "size": 0,
  "aggregations": {
    "grouped": {
      "geo_bounds": {
        "field": "location",
        "wrap_longitude": false
      }
    }
  }
}
```
{% include copy-curl.html %}

請注意，新產生的地理邊界涵蓋了較大的區域，以避免跨越換日線：

```json
{
...
  "aggregations": {
    "grouped": {
      "bounds": {
        "top_left": {
          "lat": 45.11999997776002,
          "lon": -120.23000006563962
        },
        "bottom_right": {
          "lat": 13.469999986700714,
          "lon": 144.71999991685152
        }
      }
    }
  }
}
```

OpenSearch 支援透過 API 進行 geoshape 彙總，但不支援在 OpenSearch Dashboards 視覺化中使用。
{: .note}
