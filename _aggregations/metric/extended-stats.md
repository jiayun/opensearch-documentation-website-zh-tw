---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "延伸統計資料"
parent: Metric aggregations
nav_order: 30
redirect_from:
  - /query-dsl/aggregations/metric/extended-stats/
---

# 延伸統計資料彙總

`extended_stats` 彙總是 [`stats`]({{site.url}}{{site.baseurl}}/query-dsl/aggregations/metric/stats/) 彙總更完整的版本。除了 `stats` 提供的基本統計量之外，`extended_stats` 還會計算下列項目：

- 平方和
- 變異數
- 母體變異數
- 樣本變異數
- 標準差
- 母體標準差
- 樣本標準差
- 標準差界限：
  - 上限
  - 下限
  - 母體上限
  - 母體下限
  - 樣本上限
  - 樣本下限

標準差和變異數是母體統計量；它們分別一律等於母體標準差和母體變異數。

`std_deviation_bounds` 物件定義的範圍，涵蓋平均值上下指定數量的標準差（預設為兩個標準差）。此物件一律會包含在輸出中，但僅對常態分布的資料有意義。在解讀這些值之前，請確認您的資料集符合常態分布。

## 參數

`extended_stats` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型             | 說明 |
| :--       | :--               | :--                   | :--         |
| `field`   | 必要          | 字串                | 要回傳延伸統計資料的欄位名稱。 |
| `sigma`   | 選用          | Double（非負數） | 用於計算 `std_deviation_bounds` 區間的平均值上下標準差數量。預設為 `2`。 |
| `missing` | 選用          | 數值        | 指定給欄位缺失執行個體的值。若未提供，包含缺失值的文件將不會納入延伸統計資料。 |

## 範例

下列範例請求會針對 OpenSearch Dashboards 範例電子商務資料中的 `taxful_total_price` 回傳延伸統計資料：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "extended_stats_taxful_total_price": {
      "extended_stats": {
        "field": "taxful_total_price"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

回應包含 `taxful_total_price` 的延伸統計資料：

```json
...
"aggregations" : {
  "extended_stats_taxful_total_price" : {
    "count" : 4675,
    "min" : 6.98828125,
    "max" : 2250.0,
    "avg" : 75.05542864304813,
    "sum" : 350884.12890625,
    "sum_of_squares" : 3.9367749294174194E7,
    "variance" : 2787.59157113862,
    "variance_population" : 2787.59157113862,
    "variance_sampling" : 2788.187974983536,
    "std_deviation" : 52.79764740155209,
    "std_deviation_population" : 52.79764740155209,
    "std_deviation_sampling" : 52.80329511482722,
    "std_deviation_bounds" : {
      "upper" : 180.6507234461523,
      "lower" : -30.53986616005605,
      "upper_population" : 180.6507234461523,
      "lower_population" : -30.53986616005605,
      "upper_sampling" : 180.66201887270256,
      "lower_sampling" : -30.551161586606312
    }
  }
 }
}
```

## 定義界限

您可以將 `sigma` 參數設定為任何非負值，以定義用於計算 `std_deviation_bounds` 區間的標準差數量。

### 範例：定義界限

將 `std_deviation_bounds` 標準差的數量設定為 `3`：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "extended_stats_taxful_total_price": {
      "extended_stats": {
        "field": "taxful_total_price",
        "sigma": 3
      }
    }
  }
}
```
{% include copy-curl.html %}

這會變更標準差界限：

```json
{
...
  "aggregations": {
...
      "std_deviation_bounds": {
        "upper": 233.44837084770438,
        "lower": -83.33751356160813,
        "upper_population": 233.44837084770438,
        "lower_population": -83.33751356160813,
        "upper_sampling": 233.46531398752978,
        "lower_sampling": -83.35445670143353
      }
    }
  }
}
```

## 缺失值

您可以為彙總欄位的缺失執行個體指定一個值。如需詳細資訊，請參閱[缺失彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/missing/)。

將下列文件匯入，以準備範例索引：

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

### 範例：替換缺失值

計算 `extended_stats`，並將缺失的 GPA 欄位替換為 `0`：

```json
GET students/_search
{
  "size": 0,
  "aggs": {
    "extended_stats_gpa": {
      "extended_stats": {
        "field": "gpa",
        "missing": 0
      }
    }
  }
}
```
{% include copy-curl.html %}

在回應中，`gpa` 的所有缺失值都會替換為 `0`：

```json
...
  "aggregations": {
    "extended_stats_gpa": {
      "count": 3,
      "min": 0,
      "max": 3.890000104904175,
      "avg": 2.4700000286102295,
      "sum": 7.4100000858306885,
      "sum_of_squares": 27.522500681877148,
      "variance": 3.0732667526245145,
      "variance_population": 3.0732667526245145,
      "variance_sampling": 4.609900128936772,
      "std_deviation": 1.7530735160353415,
      "std_deviation_population": 1.7530735160353415,
      "std_deviation_sampling": 2.147067797936705,
      "std_deviation_bounds": {
        "upper": 5.976147060680912,
        "lower": -1.0361470034604534,
        "upper_population": 5.976147060680912,
        "lower_population": -1.0361470034604534,
        "upper_sampling": 6.7641356244836395,
        "lower_sampling": -1.8241355672631805
      }
    }
  }
}
```

### 範例：忽略缺失值

計算 `extended_stats` 但不指定 `missing` 參數：

```json
GET students/_search
{
  "size": 0,
  "aggs": {
    "extended_stats_gpa": {
      "extended_stats": {
        "field": "gpa"
      }
    }
  }
}
```
{% include copy-curl.html %}

OpenSearch 會計算延伸統計資料，並省略包含缺失欄位值的文件（此為預設行為）：

```json
...
  "aggregations": {
    "extended_stats_gpa": {
      "count": 2,
      "min": 3.5199999809265137,
      "max": 3.890000104904175,
      "avg": 3.7050000429153442,
      "sum": 7.4100000858306885,
      "sum_of_squares": 27.522500681877148,
      "variance": 0.03422502293587115,
      "variance_population": 0.03422502293587115,
      "variance_sampling": 0.0684500458717423,
      "std_deviation": 0.18500006198883057,
      "std_deviation_population": 0.18500006198883057,
      "std_deviation_sampling": 0.2616295967044675,
      "std_deviation_bounds": {
        "upper": 4.075000166893005,
        "lower": 3.334999918937683,
        "upper_population": 4.075000166893005,
        "lower_population": 3.334999918937683,
        "upper_sampling": 4.228259236324279,
        "lower_sampling": 3.1817408495064092
      }
    }
  }
}
```

包含缺失 GPA 值的文件不會納入此計算。請注意 `count` 的差異。
