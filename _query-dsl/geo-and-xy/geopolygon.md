---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Geopolygon
parent: Geographic and xy queries
nav_order: 30
---

# Geopolygon 查詢

geopolygon 查詢會回傳包含位於指定多邊形內之地理點的文件。包含多個地理點的文件，只要至少有一個地理點符合查詢條件，即視為符合該查詢。

多邊形以座標形式的頂點清單來指定。與為 geoshape 欄位指定多邊形不同，此多邊形不必封閉（無須將第一點與最後一點指定為同一點）。雖然頂點不必依順時針或逆時針順序排列，但建議您以其中一種順序列出，以確保能正確擷取多邊形。

被搜尋的文件欄位必須對應為 `geo_point`。
{: .note}

## 範例

建立一個對應，將 `point` 欄位對應為 `geo_point`：

```json
PUT /testindex1
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

編製索引一個地理點，並指定其緯度與經度：

```json
PUT testindex1/_doc/1
{
  "point": { 
    "lat": 73.71,
    "lon": 41.32
  }
}
```
{% include copy-curl.html %}

搜尋 `point` 物件位於指定 `geo_polygon` 內的文件：

```json
GET /testindex1/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "geo_polygon": {
          "point": {
            "points": [
              { "lat": 74.5627, "lon": 41.8645 },
              { "lat": 73.7562, "lon": 42.6526 },
              { "lat": 73.3245, "lon": 41.6189 },
              { "lat": 74.0060, "lon": 40.7128 }
           ]
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

前一個請求中指定的多邊形是下圖所描繪的四邊形。符合條件的文件位於此四邊形內。四邊形頂點的座標以 `(latitude, longitude)` 格式指定。

![搜尋位於指定四邊形內的點]({{site.url}}{{site.baseurl}}/images/geopolygon-query.png)

回應包含符合條件的文件：

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
            "lat": 73.71,
            "lon": 41.32
          }
        }
      }
    ]
  }
}
```

在前述搜尋請求中，您以順時針順序指定多邊形頂點：

```json
"geo_polygon": {
    "point": {
    "points": [
        { "lat": 74.5627, "lon": 41.8645 },
        { "lat": 73.7562, "lon": 42.6526 },
        { "lat": 73.3245, "lon": 41.6189 },
        { "lat": 74.0060, "lon": 40.7128 }
    ]
    }
}
```

或者，您也可以以逆時針順序指定頂點：

```json
"geo_polygon": {
    "point": {
    "points": [
        { "lat": 74.5627, "lon": 41.8645 },
        { "lat": 74.0060, "lon": 40.7128 },
        { "lat": 73.3245, "lon": 41.6189 },
        { "lat": 73.7562, "lon": 42.6526 }
    ]
    }
}
```

產生的查詢回應會包含同一個符合條件的文件。

不過，如果您以下列順序指定頂點：

```json
"geo_polygon": {
    "point": {
    "points": [
        { "lat": 74.5627, "lon": 41.8645 },
        { "lat": 74.0060, "lon": 40.7128 },
        { "lat": 73.7562, "lon": 42.6526 },
        { "lat": 73.3245, "lon": 41.6189 }
    ]
    }
}
```

回應將不會傳回任何結果。

## 參數

Geopolygon 查詢接受下列參數。

參數 | 資料類型 | 說明
:--- | :--- | :--- 
`_name` | 字串 | 篩選器的名稱。選用。
`validation_method` | 字串 | 驗證方法。有效值為 `IGNORE_MALFORMED`（接受座標無效的地理點）、`COERCE`（嘗試將座標強制轉換為有效值），以及 `STRICT`（當座標無效時回傳錯誤）。選用。預設為 `STRICT`。
`ignore_unmapped` | 布林值 | 指定是否忽略未對應的欄位。若設為 `true`，則查詢不會回傳任何包含未對應欄位的文件。若設為 `false`，則當欄位未對應時會擲回例外狀況。選用。預設為 `false`。

## 接受的格式

您可以在為文件編製索引及搜尋文件時，以 geopoint 欄位類型接受的任何[格式]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point#formats)指定地理點座標。  