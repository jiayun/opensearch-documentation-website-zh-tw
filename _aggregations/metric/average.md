---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "平均值"
parent: Metric aggregations
nav_order: 10
redirect_from:
  - /query-dsl/aggregations/metric/average/
---

# 平均值彙總

`avg` 指標是一個單值指標，會回傳某個欄位的平均值。

## 參數

`avg` 彙總使用以下參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :-- | :-- | :-- | :-- |
| `field` | 必要 | String | 要計算平均值的欄位。 |
| `missing` | 選用 | Float | 指派給遺漏該欄位之情況的值。預設情況下，`avg` 會在計算中省略遺漏值。 |

## 範例

以下範例請求計算 OpenSearch Dashboards 電子商務範例資料中 `taxful_total_price` 欄位的平均值：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "avg_taxful_total_price": {
      "avg": {
        "field": "taxful_total_price"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

回應包含 `taxful_total_price` 的平均值：

```json
{
  "took": 85,
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
    "avg_taxful_total_price": {
      "value": 75.05542864304813
    }
  }
}
```

您可以使用彙總名稱 (`avg_taxful_total_price`) 作為鍵，從回應中取得該彙總。

## 遺漏值

您可以為遺漏的彙總欄位情況指派一個值。請參閱 [Missing aggregations]({{site.url}}{{site.baseurl}}/aggregations/bucket/missing/) 以取得更多資訊。

透過匯入以下文件來準備一個範例索引。請注意，第二份文件遺漏了 `gpa` 值：

```json
POST _bulk
{ "create": { "_index": "students", "_id": "1" } }
{ "name": "John Doe", "gpa": 3.89, "grad_year": 2022}
{ "create": { "_index": "students", "_id": "2" } }
{ "name": "Jonathan Powers", "grad_year": 2025 }
{ "create": { "_index": "students", "_id": "3" } }
{ "name": "Jane Doe", "gpa": 3.52, "grad_year": 2024 }
```
{% include copy-curl.html %}

### 範例：取代遺漏值

計算平均值，並將遺漏的 GPA 欄位取代為 `0`：

```json
GET students/_search
{
  "size": 0,
  "aggs": {
    "avg_gpa": {
      "avg": {
        "field": "gpa",
        "missing": 0
      }
    }
  }
}
```
{% include copy-curl.html %}

回應如下。請將其與下一個忽略遺漏值的範例進行比較：

```json
{
  "took": 12,
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
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "avg_gpa": {
      "value": 2.4700000286102295
    }
  }
}
```

### 範例：忽略遺漏值

計算平均值，但不指定 `missing` 參數：

```json
GET students/_search
{
  "size": 0,
  "aggs": {
    "avg_gpa": {
      "avg": {
        "field": "gpa"
      }
    }
  }
}
```
{% include copy-curl.html %}

彙總器會計算平均值，並省略包含遺漏欄位值的文件（這是預設行為）：

```json
{
  "took": 255,
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
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "avg_gpa": {
      "value": 3.7050000429153442
    }
  }
}
```