---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "地理距離"
parent: Geographic and xy queries
nav_order: 20
---

# 地理距離查詢

地理距離查詢會傳回包含地理座標點的文件，且這些座標點位於所提供地理座標點的指定距離內。若文件包含多個地理座標點，只要至少一個地理座標點符合查詢，該文件就符合查詢。

搜尋的文件欄位必須對應為 `geo_point`。
{: .note}

## 範例

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

為地理座標點編製索引，並指定其緯度與經度：

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

搜尋文件，其 `point` 物件位於指定 `point` 的指定 `distance` 範圍內：

```json
GET /testindex1/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "geo_distance": {
          "distance": "50mi",
          "point": {
            "lat": 73.5,
            "lon": 40.5
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含符合條件的文件：

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "testindex1",
        "_id": "1",
        "_score": 1,
        "_source": {
          "point": {
            "lat": 74,
            "lon": 40.71
          }
        }
      }
    ]
  }
}
```

## 參數

地理距離查詢接受下列參數。

參數 | 資料類型 | 說明
:--- | :--- | :--- 
`_name` | 字串 | 篩選器的名稱。選用。
`distance` | 字串 | 座標點符合條件的距離範圍。此距離是以指定座標點為圓心的圓半徑。如需支援的距離單位，請參閱[距離單位]({{site.url}}{{site.baseurl}}/api-reference/units/#distance-units)。必要。
`distance_type` | 字串 | 指定距離的計算方式。有效值為 `arc` 或 `plane`（速度較快，但對於長距離或接近兩極的座標點不準確）。選用。預設為 `arc`。
`validation_method` | 字串 | 驗證方法。有效值為 `IGNORE_MALFORMED`（接受座標無效的地理座標點）、`COERCE`（嘗試將座標強制轉換為有效值）和 `STRICT`（座標無效時傳回錯誤）。選用。預設為 `STRICT`。
`ignore_unmapped` | 布林值 | 指定是否忽略未對應的欄位。若設為 `true`，查詢就不會傳回任何包含未對應欄位的文件。若設為 `false`，則會在欄位未對應時擲回例外。選用。預設為 `false`。

## 接受的格式

您可以在為文件編製索引及搜尋文件時，以地理座標點欄位類型接受的任何[格式]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point#formats)指定地理座標點的座標。  