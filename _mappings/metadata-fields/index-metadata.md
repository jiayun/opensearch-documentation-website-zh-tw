---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引"
parent: Metadata fields
nav_order: 40
redirect_from:
  - /field-types/metadata-fields/index-metadata/
---

# 索引中繼資料欄位

`_index` 中繼資料欄位包含儲存文件的索引名稱。當搜尋以多個索引為目標時，例如透過逗號分隔的清單、萬用字元模式或別名，可使用 `_index` 將查詢條件僅套用於其中部分索引、統計每個索引的結果數、依索引排序結果，或從指令碼傳回索引名稱。

OpenSearch 不會將 `_index` 儲存為索引中的欄位。每個分片都知道自己所屬索引的名稱，因此它會透過將條件與該名稱比對來評估 `_index` 上的條件。因此，對 `_index` 的查詢若不是符合分片中的所有文件，就是完全不符合任何文件。

## 支援的查詢

您可以使用下列查詢來搜尋 `_index` 欄位：

- `term` 和 `terms`
- `match`、`query_string` 和 `simple_query_string`，OpenSearch 會將這些查詢轉換為此欄位的 `term` 查詢
- `prefix` 和 `wildcard`
- `exists`，會符合每一份文件

不支援 `regexp`、`fuzzy` 和 `range` 查詢。OpenSearch 會拒絕在 `_index` 上使用這些查詢的搜尋。

比對會區分大小寫，因此對 `ORDERS-ONLINE` 的 `term` 查詢不會符合 `orders-online` 索引。若要忽略大小寫，請在查詢中將 `case_insensitive` 設為 `true`。

對 `_index` 的查詢除了接受索引名稱，也接受別名。例如，若 `web-orders` 別名指向 `orders-online` 索引，則對 `web-orders` 的 `term` 查詢會符合 `orders-online` 中的每一份文件。`prefix` 和 `wildcard` 查詢也會將其模式與別名進行比對。

## 遠端索引

在[跨叢集搜尋]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/)中，來自遠端叢集的文件，其 `_index` 值會包含遠端叢集別名，後面接著一個冒號，例如 `east:orders-online`。搜尋結果會傳回這個加上前綴的名稱，彙總桶 (bucket) 也會以它作為鍵。

若要在 `prefix` 或 `wildcard` 查詢中比對遠端索引，模式必須包含 `:` 分隔符號。例如，`*:orders-*` 會比對每個遠端叢集中 `orders-*` 索引內的文件，但不會比對本機索引。不含分隔符號的模式（例如 `east*orders-online`）只會與本機索引名稱比對，因此不會比對 `east:orders-online` 中的文件。

## 範例：將查詢條件套用至特定索引

在此範例中，一家商店將線上訂單與店內訂單分別儲存在不同的索引中。目標是找出越野跑步產品的訂單，但僅在線上訂單的總額至少為 100 時才將其納入。

首先，將兩筆線上訂單新增至 `orders-online` 索引：

```json
PUT /orders-online/_doc/1
{
  "product": "Trail running shoes",
  "total": 129.99
}
```
{% include copy-curl.html %}

```json
PUT /orders-online/_doc/2
{
  "product": "Trail running socks",
  "total": 14.5
}
```
{% include copy-curl.html %}

接著，將一筆店內訂單新增至 `orders-in-store` 索引：

```json
PUT /orders-in-store/_doc/1
{
  "product": "Trail running shoes",
  "total": 119.99
}
```
{% include copy-curl.html %}

使用 `orders-*` 模式搜尋這兩個索引：

```json
GET /orders-*/_search
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "product": "trail running"
        }
      },
      "should": [
        {
          "bool": {
            "filter": [
              { "term": { "_index": "orders-online" } },
              { "range": { "total": { "gte": 100 } } }
            ]
          }
        },
        {
          "term": {
            "_index": "orders-in-store"
          }
        }
      ],
      "minimum_should_match": 1
    }
  },
  "aggs": {
    "orders_per_channel": {
      "terms": {
        "field": "_index"
      }
    }
  },
  "sort": [
    { "_index": "asc" }
  ],
  "_source": ["product", "total"],
  "script_fields": {
    "source_index": {
      "script": {
        "source": "doc[\"_index\"].value"
      }
    }
  }
}
```
{% include copy-curl.html %}

此請求以下列幾種方式使用 `_index` 欄位：

- `should` 子句對每個索引套用不同的條件。`orders-online` 中的文件還必須具有至少 100 的 `total`，而 `orders-in-store` 中任何符合條件的文件都會被傳回。
- `orders_per_channel` 彙總會計算每個索引中符合條件的訂單數量。
- `sort` 參數會依索引名稱的字母順序排列結果。
- `source_index` 指令碼欄位會從 `doc["_index"]` 讀取索引名稱，並在每個命中的 `fields` 物件中傳回該名稱。

回應包含兩筆鞋類訂單。襪子訂單被排除，因為它位於 `orders-online` 且其總額小於 100：

```json
{
  "took": 18,
  "timed_out": false,
  "_shards": {
    "total": 2,
    "successful": 2,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "orders-in-store",
        "_id": "1",
        "_score": null,
        "_source": {
          "product": "Trail running shoes",
          "total": 119.99
        },
        "fields": {
          "source_index": [
            "orders-in-store"
          ]
        },
        "sort": [
          "orders-in-store"
        ]
      },
      {
        "_index": "orders-online",
        "_id": "1",
        "_score": null,
        "_source": {
          "product": "Trail running shoes",
          "total": 129.99
        },
        "fields": {
          "source_index": [
            "orders-online"
          ]
        },
        "sort": [
          "orders-online"
        ]
      }
    ]
  },
  "aggregations": {
    "orders_per_channel": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "orders-in-store",
          "doc_count": 1
        },
        {
          "key": "orders-online",
          "doc_count": 1
        }
      ]
    }
  }
}
```
