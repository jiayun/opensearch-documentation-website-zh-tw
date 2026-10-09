---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "篩選結果"
parent: Customizing search results
nav_order: 36
---

# 篩選搜尋結果

您可以使用不同的方法來篩選搜尋，每種方法適用於特定情境。您可以在查詢層級套用篩選條件，使用 `boolean` 查詢子句以及 `post_filter` 和 `aggregation` 層級的篩選條件，如下所示：

- **查詢層級篩選：** 套用 `boolean` 查詢篩選子句來篩選搜尋命中結果和彙總，例如將結果縮小至特定類別或品牌。
- **後置篩選：** 使用 `post_filter` 根據使用者的選擇來精簡搜尋命中結果，同時保留所有彙總選項。
- **彙總層級篩選：** 根據選取的篩選條件調整特定彙總，而不影響其他彙總。

## 使用布林查詢進行查詢層級篩選

使用具有篩選子句的 `boolean` 查詢，將篩選條件同時套用至搜尋命中結果和彙總。例如，如果購物者從 `BrandA` 搜尋 `smartphones`，布林查詢可以將結果限制為僅來自 `BrandA` 的那些智慧型手機。下列步驟將引導您完成查詢層級篩選。

1. 建立索引 `electronics` 並使用下列請求提供對應：

```json
PUT /electronics
{
  "mappings": {
    "properties": {
      "brand": { "type": "keyword" },
      "category": { "type": "keyword" },
      "price": { "type": "float" },
      "features": { "type": "keyword" }
    }
  }
}
```
{% include copy-curl.html %}

2. 使用下列請求將文件新增至 `electronics` 索引：

```json
POST /_bulk?refresh
{ "index": { "_index": "electronics", "_id": "1" } }
{ "brand": "BrandA", "category": "Smartphone", "price": 699.99, "features": ["5G", "Dual Camera"] }
{ "index": { "_index": "electronics", "_id": "2" } }
{ "brand": "BrandA", "category": "Laptop", "price": 1199.99, "features": ["Touchscreen", "16GB RAM"] }
{ "index": { "_index": "electronics", "_id": "3" } }
{ "brand": "BrandB", "category": "Smartphone", "price": 799.99, "features": ["5G", "Triple Camera"] }
```
{% include copy-curl.html %}

3. 使用下列請求套用 `boolean` 篩選查詢，以僅顯示來自 `BrandA` 的 `smartphones`：

```json
GET /electronics/_search
{
  "query": {
    "bool": {
      "filter": [
        { "term": { "brand": "BrandA" }},
        { "term": { "category": "Smartphone" }}
      ]
    }
  }
}
```
{% include copy-curl.html %}

## 使用 `post-filter` 縮小結果範圍同時保留彙總可見性

使用 `post_filter` 限制搜尋命中結果，同時保留所有彙總選項。例如，如果購物者選取 `BrandA`，結果會經過篩選，僅顯示 `BrandA` 產品，同時維持彙總中所有品牌選項的可見性，如下列範例請求所示：

```json
GET /electronics/_search
{
  "query": {
    "bool": {
      "filter": { "term": { "category": "Smartphone" }}
    }
  },
  "aggs": {
    "brands": {
      "terms": { "field": "brand" }
    }
  },
  "post_filter": {
    "term": { "brand": "BrandA" }
  }
}
```
{% include copy-curl.html %}

結果應在搜尋命中結果中顯示 `BrandA` 智慧型手機，並在彙總中顯示所有品牌。

## 使用彙總層級篩選來精簡彙總

您可以使用彙總層級篩選，將篩選條件套用至特定彙總，而不影響其所屬的主要彙總。

例如，您可以使用彙總層級篩選，根據選取的品牌 `BrandA` 和 `BrandB` 來篩選 `price_ranges` 彙總，而不影響主要的 `price_ranges` 彙總，如下列範例請求所示。這會顯示與所選品牌相關的價格範圍，同時也會顯示所有產品的整體價格範圍。

```json
GET /electronics/_search
{
  "query": {
    "bool": {
      "filter": { "term": { "category": "Smartphone" }}
    }
  },
  "aggs": {
    "price_ranges": {
      "range": {
        "field": "price",
        "ranges": [
          { "to": 500 },
          { "from": 500, "to": 1000 },
          { "from": 1000 }
        ]
      }
    },
    "filtered_brands": {
      "filter": {
        "terms": { "brand": ["BrandA", "BrandB"] }
      },
      "aggs": {
        "price_ranges": {
          "range": {
            "field": "price",
            "ranges": [
              { "to": 500 },
              { "from": 500, "to": 1000 },
              { "from": 1000 }
            ]
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}
