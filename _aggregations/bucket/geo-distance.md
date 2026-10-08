---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "地理距離"
parent: Bucket aggregations
nav_order: 70
redirect_from:
  - /query-dsl/aggregations/bucket/geo-distance/
---

# 地理距離彙總

`geo_distance` 彙總會以中心點為圓心，將文件分組到以距離劃分的環形區域中。每個範圍定義一個環，系統會依據文件的 `geo_point` 欄位值與指定原點之間的距離，將文件放入對應的桶 (bucket)。此彙總在概念上與 [`range` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/range/)類似，但作用對象是地理座標，而非數值。

目標欄位必須對應為 `geo_point`。若文件的 geo_point 欄位包含多個值，系統會計算所有距離，並據此將文件分配到對應的桶。

## 參數

`geo_distance` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 必要 | 字串 | 用來計算距離的 `geo_point` 欄位。 |
| `origin` | 必要 | 物件、字串或陣列 | 測量距離的中心點。接受物件格式（`{"lat": 40.71, "lon": -74.00}`）、字串格式（`"40.71, -74.00"`）或 GeoJSON 陣列格式（`[-74.00, 40.71]`）。 |
| `ranges` | 必要 | 陣列 | 定義各個桶的距離範圍清單。每個範圍可包含 `from`、`to`，以及選用的 `key`。 |
| `unit` | 選用 | 字串 | `ranges` 中距離值的單位。預設為 `m`（公尺）。有效值：`m`、`km`、`mi`、`yd`、`in`、`cm`、`mm`。 |
| `distance_type` | 選用 | 字串 | 用來計算距離的演算法。<br>有效值如下：<br> - `arc`：使用地球完整的球面幾何計算距離。最精確，但速度最慢。<br> - `plane`：將座標投影到平面上並計算歐幾里得距離。速度最快，但精確度最低。僅適用於小範圍的地理區域（約 5 km 以內）。<br><br>預設為 `arc`。  |
| `keyed` | 選用 | 布林值 | 設為 `true` 時，會以範圍名稱為鍵的物件形式傳回桶，而非陣列。預設為 `false`。 |

## 範例：基本距離環

下列範例以紐約市為中心，將電子商務訂單分組到三個以英里為單位的距離環中：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "distance_from_nyc": {
      "geo_distance": {
        "field": "geoip.location",
        "origin": "40.7128, -74.0060",
        "unit": "mi",
        "ranges": [
          { "to": 50 },
          { "from": 50, "to": 500 },
          { "from": 500 }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：使用自訂範圍名稱的鍵值回應

將 `keyed` 設為 `true` 時，會以物件而非陣列的形式傳回桶。您可以使用 `key` 屬性為每個範圍指定自訂名稱：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "distance_from_nyc": {
      "geo_distance": {
        "field": "geoip.location",
        "origin": "40.7128, -74.0060",
        "unit": "mi",
        "keyed": true,
        "ranges": [
          { "to": 50, "key": "local" },
          { "from": 50, "to": 500, "key": "domestic" },
          { "from": 500, "key": "international" }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

下列回應對應於上述鍵值範例：

```json
{
  "took": 18,
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
    "distance_from_nyc": {
      "buckets": {
        "local": {
          "from": 0.0,
          "to": 50.0,
          "doc_count": 896
        },
        "domestic": {
          "from": 50.0,
          "to": 500.0,
          "doc_count": 0
        },
        "international": {
          "from": 500.0,
          "doc_count": 3779
        }
      }
    }
  }
}
```

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `buckets` | 陣列或物件 | 距離桶。預設以陣列形式傳回；當 `keyed` 為 `true` 時，則以物件形式傳回。 |
| `buckets.key` | 字串 | 自動產生的範圍標籤（例如 `*-500.0` 或 `500.0-3000.0`），若有指定則為自訂鍵。 |
| `buckets.from` | Double | 距離範圍的下限，以指定的 `unit` 為單位。 |
| `buckets.to` | Double | 距離範圍的上限，以指定的 `unit` 為單位。 |
| `buckets.doc_count` | 整數 | 落在此距離範圍內的文件數量。 |
