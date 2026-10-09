---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "距離功能"
parent: Specialized queries
nav_order: 5
has_math: true
---

# 距離功能查詢

使用 `distance_feature` 查詢來提升與特定日期或地理位置較接近之文件的相關性。這可協助您在搜尋結果中優先顯示較新或鄰近的內容。舉例來說，您可以為較近期製造的產品指派較高的權重，或提升最接近使用者指定位置的項目。

您可以將此查詢套用至包含日期或位置資料的欄位。它通常用於 `bool` 查詢的 `should` 子句中，以改善相關性分數，而不會篩除結果。

## 設定索引

使用 `distance_feature` 查詢之前，請確認您的索引至少包含下列其中一種欄位類型：

- [`date`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/)
- [`date_nanos`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date-nanos/)
- [`geo_point`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-point/)

在此範例中，您將設定可用來執行距離功能查詢的 `opening_date` 和 `coordinates` 欄位：

```json
PUT /stores
{
  "mappings": {
    "properties": {
      "opening_date": {
        "type": "date"
      },
      "coordinates": {
        "type": "geo_point"
      }
    }
  }
}
```
{% include copy-curl.html %}

將範例文件新增至索引：

```json
PUT /stores/_doc/1
{
  "store_name": "Green Market",
  "opening_date": "2025-03-10",
  "coordinates": [74.00, 40.70]
}
```
{% include copy-curl.html %}

```json
PUT /stores/_doc/2
{
  "store_name": "Fresh Foods",
  "opening_date": "2025-04-01",
  "coordinates": [73.98, 40.75]
}
```
{% include copy-curl.html %}

```json
PUT /stores/_doc/3
{
  "store_name": "City Organics",
  "opening_date": "2021-04-20",
  "coordinates": [74.02, 40.68]
}
```
{% include copy-curl.html %}

## 範例：根據新近程度提升分數

下列查詢會搜尋 `store_name` 符合 `market` 的文件，並提升最近開幕的商店：

```json
GET /stores/_search
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "store_name": "market"
        }
      },
      "should": {
        "distance_feature": {
          "field": "opening_date",
          "origin": "2025-04-07",
          "pivot": "10d"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的文件：

```json
{
  "took": 4,
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
    "max_score": 1.2372394,
    "hits": [
      {
        "_index": "stores",
        "_id": "1",
        "_score": 1.2372394,
        "_source": {
          "store_name": "Green Market",
          "opening_date": "2025-03-10",
          "coordinates": [
            74,
            40.7
          ]
        }
      }
    ]
  }
}
```

### 範例：根據地理鄰近程度提升分數

下列查詢會搜尋 `store_name` 符合 `market` 的文件，並提升較接近指定原點位置的結果：

```json
GET /stores/_search
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "store_name": "market"
        }
      },
      "should": {
        "distance_feature": {
          "field": "coordinates",
          "origin": [74.00, 40.71],
          "pivot": "500m"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的文件：

```json
{
  "took": 3,
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
    "max_score": 1.2910118,
    "hits": [
      {
        "_index": "stores",
        "_id": "1",
        "_score": 1.2910118,
        "_source": {
          "store_name": "Green Market",
          "opening_date": "2025-03-10",
          "coordinates": [
            74,
            40.7
          ]
        }
      }
    ]
  }
}
```

## 參數

下表列出 `distance_feature` 查詢支援的所有最上層參數。

| 參數 | 必要／選用 | 說明 |
|-----------|-------------------|-------------|
| `field`   | 必要          | 用來計算距離的欄位名稱。必須是 `date`、`date_nanos` 或 `geo_point` 欄位，且具有 `index: true`（預設）和 `doc_values: true`（預設）。 |
| `origin`  | 必要          | 用來計算距離的原點。`date` 欄位請使用 [日期]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/) 或 [日期數學運算式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#date-math)（例如 `now-1h`），`geo_point` 欄位請使用 [地理座標點]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-point/)。 |
| `pivot`   | 必要          | 與 `origin` 的距離，在該距離時分數會獲得 `boost` 值的一半。日期欄位請使用時間單位（例如 `10d`），地理欄位請使用距離單位（例如 `1km`）。如需詳細資訊，請參閱 [單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。|
| `boost`   | 選用          | 相符文件相關性分數的乘數。必須是非負浮點數。預設值為 `1.0`。 |

## 分數的計算方式

`distance_feature` 查詢會使用下列公式計算文件的相關性分數：

$$ \text{score} = \text{boost} \cdot \frac {\text{pivot}} {\text{pivot} + \text{distance}} $$,

其中 $$\text{distance}$$ 是 `origin` 與欄位值之間的絕對差。

## 略過不具競爭力的命中

與其他修改分數的查詢 (例如 `function_score` 查詢) 不同，`distance_feature` 查詢經過最佳化，可在停用總命中數追蹤 (`track_total_hits`) 時有效率地略過不具競爭力的命中。
