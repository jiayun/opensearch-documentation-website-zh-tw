---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Geocentroid
parent: Metric aggregations
nav_order: 45
---

# Geocentroid 彙總

`geo_centroid` 彙總會計算一組 `geo_point` 值的地理中心或焦點。它會將中心點位置以經緯度對的形式傳回。

## 參數

`geo_centroid` 彙總使用以下參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :-- | :-- | :-- | :-- |
| `field` | 必要 | 字串 | 包含要計算 geocentroid 之 geopoints 的欄位名稱。 |

## 範例

以下範例會傳回電子商務範例資料中每筆訂單 `geoip.location` 的 `geo_centroid`。每個 `geoip.location` 都是一個 geopoint：


```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "centroid": {
      "geo_centroid": {
        "field": "geoip.location"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

回應包含一個 `centroid` 物件，其中具有代表所有已編製索引資料點中心點位置的 `lat` 和 `lon` 屬性：

```json
{
  "took": 35,
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
    "centroid": {
      "location": {
        "lat": 35.54990372113027,
        "lon": -9.079764742533712
      },
      "count": 4675
    }
  }
}
```

中心點位置位於摩洛哥北部的大西洋。考慮到資料庫中訂單的地理分佈非常廣泛，這個結果並沒有太大的意義。

## 巢狀於其他彙總之下

您可以將 `geo_centroid` 彙總巢狀於桶彙總中，以計算資料子集的中心點。

### 範例：巢狀於 terms 彙總之下

您可以將 `geo_centroid` 彙總巢狀於字串欄位的 `terms` 桶中。

若要找出每個大洲訂單 `geoip` 的中心點位置，請在 `geoip.continent_name` 欄位內進行中心點的子彙總：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "continents": {
      "terms": {
        "field": "geoip.continent_name"
      },
      "aggs": {
        "centroid": {
          "geo_centroid": {
            "field": "geoip.location"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

這會為每個大洲的桶傳回一個中心點位置：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 34,
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
    "continents": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "Asia",
          "doc_count": 1220,
          "centroid": {
            "location": {
              "lat": 28.023606536509163,
              "lon": 47.83377046025068
            },
            "count": 1220
          }
        },
        {
          "key": "North America",
          "doc_count": 1206,
          "centroid": {
            "location": {
              "lat": 39.06542286878007,
              "lon": -85.36152573149485
            },
            "count": 1206
          }
        },
        {
          "key": "Europe",
          "doc_count": 1172,
          "centroid": {
            "location": {
              "lat": 48.125767892293325,
              "lon": 2.7529009746915243
            },
            "count": 1172
          }
        },
        {
          "key": "Africa",
          "doc_count": 899,
          "centroid": {
            "location": {
              "lat": 30.780756367941297,
              "lon": 13.464182392125318
            },
            "count": 899
          }
        },
        {
          "key": "South America",
          "doc_count": 178,
          "centroid": {
            "location": {
              "lat": 4.599999985657632,
              "lon": -74.10000007599592
            },
            "count": 178
          }
        }
      ]
    }
  }
}
```
</details>
