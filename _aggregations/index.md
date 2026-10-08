---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "彙總"
has_children: false
nav_order: 5
nav_exclude: true
permalink: /aggregations/
redirect_from:
  - /query-dsl/aggregations/aggregations/
  - /opensearch/aggregations/
  - /query-dsl/aggregations/
  - /aggregations/index/
---

# 彙總

OpenSearch 的用途不只是搜尋。彙總可讓您運用 OpenSearch 強大的分析引擎來分析您的資料，並從中擷取統計資料。

彙總的使用案例相當多樣，從即時分析資料以採取行動，到使用 OpenSearch Dashboards 建立視覺化儀表板都有。

OpenSearch 可以在數毫秒內對大量資料集執行彙總。與查詢相比，彙總會耗用更多 CPU 週期和記憶體。

## 彙總的一般結構

彙總查詢的結構如下：

```json
GET _search
{
  "size": 0,
  "aggs": {
    "<aggregation_name>": {
      "<aggregation_type>": {}
    }
  }
}
```
{% include copy-curl.html %}

如果您只想取得彙總結果，而不需要查詢結果，請將 `size` 設定為 `0`。

在 `aggs` 屬性中（您也可以視需要改用 `aggregations`），您可以定義任意數量的彙總。每個彙總都由其名稱以及 OpenSearch 支援的其中一種彙總類型來定義。

彙總的名稱可協助您在回應中區分不同的彙總。`<aggregation_type>` 預留位置指定彙總類型，例如 `sum` 或 `min`。

## 彙總範例

下列範例使用 OpenSearch Dashboards 的電子商務範例資料。若要新增範例資料，請登入 OpenSearch Dashboards，選擇 **Home**，然後選擇 **Try our sample data**。在 **Sample eCommerce orders** 中，選擇 **Add data**。

此範例使用 `avg` 彙總來找出 `taxful_total_price` 欄位的平均值：

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

回應中包含一個 `aggregations` 區塊，其中含有計算出的平均值：

```json
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 4675,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "avg_taxful_total_price" : {
      "value" : 75.05542864304813
    }
  }
}
```

## 彙總類型

彙總主要有三種類型：

- [指標彙總](#metric-aggregations)：對數值欄位計算 `sum`、`min`、`max` 和 `avg` 等指標。
- [桶 (bucket) 彙總](#bucket-aggregations)：根據特定條件將查詢結果分組。
- [管線彙總](#pipeline-aggregations)：將某個彙總的輸出作為另一個彙總的輸入。

### 指標彙總

指標彙總會對數值欄位的值計算統計資料：

- [`avg`]({{site.url}}{{site.baseurl}}/aggregations/metric/average/)：計算平均值。
- [`cardinality`]({{site.url}}{{site.baseurl}}/aggregations/metric/cardinality/)：計算不重複值的數量。
- [`extended_stats`]({{site.url}}{{site.baseurl}}/aggregations/metric/extended-stats/)：取得包含標準差在內的完整統計資料。
- [`max`]({{site.url}}{{site.baseurl}}/aggregations/metric/maximum/)：找出最大值。
- [`min`]({{site.url}}{{site.baseurl}}/aggregations/metric/minimum/)：找出最小值。
- [`percentile`]({{site.url}}{{site.baseurl}}/aggregations/metric/percentile/)：計算百分位數（例如中位數、第 95 百分位數）。
- [`stats`]({{site.url}}{{site.baseurl}}/aggregations/metric/stats/)：取得基本統計資料（`count`、`sum`、`min`、`max` 和 `avg`）。
- [`sum`]({{site.url}}{{site.baseurl}}/aggregations/metric/sum/)：計算值的總和。
- [`value_count`]({{site.url}}{{site.baseurl}}/aggregations/metric/value-count/)：計算非 null 值的數量。

完整的指標彙總清單，請參閱[指標彙總]({{site.url}}{{site.baseurl}}/aggregations/metric/)。

### 桶彙總

桶彙總會根據欄位值、範圍或其他條件，將文件分組到不同的桶中：

- [`terms`]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms/)：依不重複的欄位值分組。
- [`date_histogram`]({{site.url}}{{site.baseurl}}/aggregations/bucket/date-histogram/)：依時間間隔分組。
- [`histogram`]({{site.url}}{{site.baseurl}}/aggregations/bucket/histogram/)：依數值間隔分組。
- [`range`]({{site.url}}{{site.baseurl}}/aggregations/bucket/range/)：依數值範圍分組。
- [`filter`]({{site.url}}{{site.baseurl}}/aggregations/bucket/filter/)：建立單一個符合篩選條件的桶。
- [`filters`]({{site.url}}{{site.baseurl}}/aggregations/bucket/filters/)：建立多個桶，每個篩選條件各一個。
- [`missing`]({{site.url}}{{site.baseurl}}/aggregations/bucket/missing/)：將缺少某欄位值的文件分組。
- [`significant_terms`]({{site.url}}{{site.baseurl}}/aggregations/bucket/significant-terms/)：在資料集中尋找不尋常或值得關注的詞彙。

完整的桶彙總清單，請參閱[桶彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/)。

### 管線彙總

管線彙總會處理其他彙總的輸出：

- [`avg_bucket`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/avg-bucket/)：計算各桶之間的平均值。
- [`cumulative_sum`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/cumulative-sum/)：計算各桶之間的累計總和。
- [`bucket_sort`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/bucket-sort/)：排序並限制傳回的桶數量。

完整的管線彙總清單，請參閱[管線彙總]({{site.url}}{{site.baseurl}}/aggregations/pipeline/)。

## 巢狀彙總

位於彙總之中的彙總稱為_巢狀彙總_或_子彙總_。

指標彙總會產生簡單的結果，且不能包含巢狀彙總。

桶彙總會產生由文件組成的桶，您可以將其巢狀置於其他彙總中。透過在桶彙總中巢狀放置指標彙總和桶彙總，您可以對資料執行複雜的分析。

### 巢狀彙總的一般語法

```json
{
  "aggs": {
    "name": {
      "type": {
        "data"
      },
      "aggs": {
        "nested": {
          "type": {
            "data"
          }
        }
      }
    }
  }
}
```

內層的 `aggs` 關鍵字會開始一個新的巢狀彙總。父彙總與巢狀彙總的語法相同。巢狀彙總會在前面父彙總的情境中執行。

### 巢狀彙總範例

下列範例使用 OpenSearch Dashboards 的電子商務範例資料，依類別將訂單分組，並計算每個類別內的平均價格。此查詢會傳回依字母降冪排序的前 5 個類別：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": {
        "field": "category.keyword",
        "size": 5,
        "order": {
          "_key": "desc"
        }
      },
      "aggs": {
        "avg_price": {
          "avg": {
            "field": "taxful_total_price"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中包含每個類別的桶，這些桶依字母降冪排序，且每個桶內都計算了平均價格：

```json
{
  "took" : 22,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 4675,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "categories" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 572,
      "buckets" : [
        {
          "key" : "Women's Shoes",
          "doc_count" : 1136,
          "avg_price" : {
            "value" : 92.8513836927817
          }
        },
        {
          "key" : "Women's Clothing",
          "doc_count" : 1903,
          "avg_price" : {
            "value" : 70.99312352207042
          }
        },
        {
          "key" : "Women's Accessories",
          "doc_count" : 830,
          "avg_price" : {
            "value" : 73.28953313253012
          }
        },
        {
          "key" : "Men's Shoes",
          "doc_count" : 944,
          "avg_price" : {
            "value" : 97.24356130826271
          }
        },
        {
          "key" : "Men's Clothing",
          "doc_count" : 2024,
          "avg_price" : {
            "value" : 73.81122043292984
          }
        }
      ]
    }
  }
}
```

更多巢狀彙總範例，請參閱[管線彙總]({{site.url}}{{site.baseurl}}/aggregations/pipeline/#buckets-path)。

您也可以將彙總與搜尋查詢搭配使用，在彙總之前先縮小要分析的資料範圍。如果您未新增查詢，OpenSearch 會隱含地使用 `match_all` 查詢。

## 使用彙總

您可以透過 OpenSearch API 或 OpenSearch Dashboards 使用彙總。

### 使用彙總 API

您可以使用 cURL 等工具從命令列執行彙總請求，也可以從 OpenSearch Dashboards 的 Dev Tools 主控台執行。如需更多關於使用 Dev Tools 主控台的資訊，請參閱[在 Dev Tools 主控台中執行查詢]({{site.url}}{{site.baseurl}}/dashboards/visualize/run-queries/)。

如需 API 請求和回應的範例，請參閱[彙總範例](#example-aggregation)和[巢狀彙總範例](#nested-aggregation-example)區段。如需各種彙總類型的詳細語法和參數，請參閱[彙總類型](#aggregation-types)區段中列出的各類型專屬文件頁面。如需針對範例資料集執行彙總的實作教學，請參閱[使用彙總摘要資料]({{site.url}}{{site.baseurl}}/getting-started/analyze-data/#summarize-data-using-aggregations)。

### 在 OpenSearch Dashboards 中使用彙總

OpenSearch Dashboards 中的許多視覺化類型都由彙總驅動。當您建立視覺化時，OpenSearch Dashboards 會根據您的選取項目自動產生彙總查詢。如果您是 OpenSearch Dashboards 的新手，請參閱[OpenSearch Dashboards 入門]({{site.url}}{{site.baseurl}}/dashboards/getting-started/)。

您在 **Visualize** 應用程式中看到的指標和桶 (bucket) 選項，對應於本頁所述的彙總類型。`Count` 是預設的 Y 軸指標，它會顯示每個桶中的文件數量 (`doc_count`)，而且不需要選取欄位。

**Visualize** 應用程式中提供下列指標：`Count`、`Average`、`Max`、`Median`、`Min`、`Percentile Ranks`、`Percentiles`、`Standard Deviation`、`Sum`、`Top Hit`、`Unique Count`、`Cumulative Sum`、`Derivative`、`Moving Avg`、`Serial Diff`、`Average Bucket`、`Max Bucket`、`Min Bucket` 以及 `Sum Bucket`。

**Visualize** 應用程式中提供下列桶彙總：`Date Histogram`、`Date Range`、`Filters`、`Histogram`、`IPv4 Range`、`Range`、`Significant Terms` 以及 `Terms`。

如需各選項的說明，以及它們如何對應至 Aggregations API，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/#data-tab)。如需實作教學，請參閱[建立以彙總為基礎的視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/aggregation-based-viz/)。

## 文字欄位上的彙總

根據預設，OpenSearch 不支援對 [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 欄位進行彙總。由於 `text` 欄位會經過斷詞，對 `text` 欄位進行彙總時，必須將斷詞過程反轉回原始字串，然後再根據該字串建立彙總。這類操作會耗用大量記憶體，並降低叢集效能。

雖然您可以在對應中將 [`fielddata`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/#parameters) 參數設為 `true`，以啟用對 `text` 欄位的彙總，但彙總仍會以斷詞後的字詞為基礎，而非原始文字。

我們建議將 `text` 欄位的原始版本保留為 [`keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/keyword/) 欄位，以便對其進行彙總。

下列範例會建立一個 `product_name` 欄位，其中包含名為 `raw` 的 `keyword` 子欄位。您可以對 `product_name.raw` 進行彙總，而不是對 `product_name`：

```json
PUT products
{
  "mappings": {
    "properties": {
      "product_name": {
        "type": "text",
        "fielddata": true,
        "fields": {
          "raw": {
            "type": "keyword"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

如需更多關於對應的資訊，請參閱[對應]({{site.url}}{{site.baseurl}}/mappings/)。

## 限制

由於彙總器會使用 `double` 資料類型處理所有值，因此大於或等於 2<sup>53</sup> 的 `long` 值為近似值。

## 後續步驟

- 探索[指標彙總]({{site.url}}{{site.baseurl}}/aggregations/metric/)，以計算資料的統計值。
- 了解[桶彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/)，以依類別、範圍或時間間隔將資料分組並分析。
- 探索[管線彙總]({{site.url}}{{site.baseurl}}/aggregations/pipeline/)，以使用其他彙總的輸出進行進階分析。
- 使用彙總[在 OpenSearch Dashboards 中建立視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/viz-index/)。
