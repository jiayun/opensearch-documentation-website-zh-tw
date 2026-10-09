---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "地理邊界框"
parent: Geographic and xy queries
nav_order: 10
redirect_from:
  - /opensearch/query-dsl/geo-and-xy/geo-bounding-box/
  - /query-dsl/query-dsl/geo-and-xy/geo-bounding-box/
---

# 地理邊界框查詢

若要搜尋包含 [geopoint]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point/) 欄位的文件，請使用地理邊界框查詢。地理邊界框查詢會傳回其 geopoint 位於查詢中所指定邊界框內的文件。若文件包含多個 geopoint，只要至少有一個 geopoint 位於邊界框內，該文件即符合查詢。

## 範例

您可以使用地理邊界框查詢來搜尋包含 geopoint 的文件。

建立對應，將 `point` 欄位對應為 `geo_point`：

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

將三個 geopoint 編製索引為具有緯度和經度的物件：

```json
PUT testindex1/_doc/1
{
  "point": { 
    "lat": 74.00,
    "lon": 40.71
  }
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/2
{
  "point": { 
    "lat": 72.64,
    "lon": 22.62
  } 
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/3
{
  "point": { 
    "lat": 75.00,
    "lon": 28.00
  }
}
```
{% include copy-curl.html %}

搜尋所有文件，並篩選出點位於查詢中所定義矩形內的文件：

```json
GET testindex1/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "geo_bounding_box": {
          "point": {
            "top_left": {
              "lat": 75,
              "lon": 28
            },
            "bottom_right": {
              "lat": 73,
              "lon": 41
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含符合的文件：

```json
{
  "took" : 20,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "testindex1",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "point" : {
            "lat" : 74.0,
            "lon" : 40.71
          }
        }
      }
    ]
  }
}
```

上述回應不包含 geopoint 為 `"lat": 75.00, "lon": 28.00` 的文件，這是因為 geopoint 的[精確度](#precision)有限。
{: .note}

## 精確度

geopoint 座標在編製索引時一律會向下捨入。查詢時，邊界框的上界會向下捨入，下界則會向上捨入。因此，位於邊界框下緣和左緣的 geopoint 文件，可能因捨入誤差而不包含在結果中。另一方面，位於邊界框上緣和右緣的 geopoint，即使超出邊界，仍可能包含在結果中。緯度的捨入誤差小於 4.20 &times; 10<sup>&minus;8</sup> 度，經度的捨入誤差小於 8.39 &times; 10<sup>&minus;8</sup> 度（約 1 公分）。

## 指定邊界框

您可以提供頂點座標、geohash 或 [Well-Known Text (WKT)](https://docs.opengeospatial.org/is/12-063r5/12-063r5.html) 字串來指定邊界框。

### 使用頂點座標指定邊界框

提供下列任一頂點座標組合：

- `top_left` 和 `bottom_right`
- `top_right` 和 `bottom_left`
- `top`、`left`、`bottom` 和 `right`

以 geopoint 欄位類型可接受的任何[格式]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point#formats)指定座標值。

下列範例顯示如何使用 `top`、`left`、`bottom` 和 `right` 座標指定邊界框：

```json
GET testindex1/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "geo_bounding_box": {
          "point": {
            "top": 75,
            "left": 28,
            "bottom": 73,
            "right": 41            
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 使用 geohash 指定邊界框

如果您使用 geohash 指定邊界框，該 geohash 會視為一個矩形。邊界框的左上頂點對應至 `top_left` geohash 的左上頂點，而邊界框的右下頂點對應至 `bottom_right` geohash 的右下頂點。

下列範例顯示如何使用 geohash 指定與前述範例相同的邊界框：

```json
GET testindex1/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "geo_bounding_box": {
          "point": {
            "top_left": "ut7ftjkfxm34",
            "bottom_right": "uuvpkcprc4rc"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

若要指定涵蓋某個 geohash 整個區域的邊界框，請將該 geohash 同時提供為邊界框的 `top_left` 和 `bottom_right` 參數：

```json
GET testindex1/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "geo_bounding_box": {
          "point": {
            "top_left": "ut",
            "bottom_right": "ut"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 使用 WKT 指定邊界框

若要以 WKT 格式定義邊界框，請提供 `wkt` 參數，並以 `BBOX (minLon, maxLon, maxLat, minLat)` 形式提供邊界矩形。`BBOX` 是地理邊界框查詢唯一接受的 WKT 幾何圖形。

下列範例顯示如何使用 WKT 指定與前述範例相同的邊界框：

```json
GET testindex1/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "geo_bounding_box": {
          "point": {
            "wkt": "BBOX (28, 41, 75, 73)"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 參數

地理邊界框查詢接受下列參數。

參數 | 資料類型 | 說明
:--- | :--- | :--- 
`_name` | 字串 | 篩選條件的名稱。選用。
`validation_method` | 字串 | 驗證方法。有效值為 `IGNORE_MALFORMED`（接受含無效座標的 geopoint）、`COERCE`（嘗試將座標強制轉換為有效值），以及 `STRICT`（座標無效時傳回錯誤）。預設為 `STRICT`。
`type` | 字串 | 指定篩選條件的執行方式。有效值為 `indexed`（將篩選條件編製索引）和 `memory`（在記憶體中執行篩選條件）。預設為 `memory`。
`ignore_unmapped` | 布林值 | 指定是否忽略未對應的欄位。若設為 `true`，查詢不會傳回任何具有未對應欄位的文件。若設為 `false`，則欄位未對應時會擲回例外狀況。預設為 `false`。

