---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋組態"
nav_order: 5
parent: Search Relevance Workbench
grand_parent: Optimizing search quality
has_children: false
---

# 搜尋組態

搜尋組態會定義用於執行實驗的查詢模式，指定查詢應如何建構與執行。

## 建立搜尋組態

您可以定義搜尋組態，描述查詢集中每個查詢的執行方式。每個搜尋組態都有一個名稱，並由查詢本文 (OpenSearch 查詢領域特定語言 [DSL] 中的查詢) 與目標索引組成。您也可以選擇為搜尋組態定義搜尋管線。

### 端點

```json
PUT _plugins/_search_relevance/search_configurations
```

### 請求本文欄位

下表列出可用的輸入參數。

欄位 | 資料類型 |  說明
:---  | :--- | :---
`name` | 字串 | 搜尋組態的名稱。
`description` | 字串 | 搜尋組態的說明。
`query` | 物件 | 以 OpenSearch query DSL 定義查詢，並以逸出內部引號的 JSON 字串提供（例如 `"query": "{\"query\":{\"multi_match\":{...}}}"`）。使用 `%SearchText%` 預留位置或 [Mustache](https://mustache.github.io/) 範本變數（例如 {% raw %}`{{queryText}}`{% endraw %}），在執行階段替代查詢集的值。如需更多資訊，請參閱[使用 Mustache 範本](#using-mustache-templates)。
`index` | 字串 | 此搜尋組態所查詢的目標索引。
`searchPipeline` | 字串 | 指定現有的搜尋管線。選用。

### 範例請求：建立搜尋組態

```json
PUT _plugins/_search_relevance/search_configurations
{
  "name": "baseline",
  "query": "{\"query\":{\"multi_match\":{\"query\":\"%SearchText%\",\"fields\":[\"id\",\"title\",\"category\",\"bullets\",\"description\",\"attrs.Brand\",\"attrs.Color\"]}}}",
  "description": "Current production algorithm",
  "index": "ecommerce"
}
```

### 使用 Mustache 範本

您可以在查詢中使用 [Mustache](https://mustache.github.io/) 範本變數，而不使用 `%SearchText%` 預留位置。如果 `query` 參數包含雙大括號 ({% raw %}`{{}}`{% endraw %})，OpenSearch 會將 `query` 轉譯為 Mustache 範本；否則，OpenSearch 會替代 `%SearchText%` 預留位置。現有的 `%SearchText%` 組態會繼續運作，不會有任何變更。

當 OpenSearch 轉譯範本時，可以使用下列變數：

- {% raw %}`{{queryText}}`{% endraw %}：目前查詢集項目中的 `queryText` 值。
- {% raw %}`{{<field_name>}}`{% endraw %}：查詢集項目中的任何自訂欄位，以其欄位名稱參照 (例如 {% raw %}`{{category}}`{% endraw %})。如需更多資訊，請參閱[查詢集]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/query-sets/)。

OpenSearch 會自動逸出替代的值，因此包含引號或其他特殊字元的查詢文字在 JSON 中仍保持有效。

不支援 Mustache 部分範本 ({% raw %}`{{>...}}`{% endraw %})，且會導致查詢遭到拒絕。
{: .note}

例如，下列請求會建立搜尋組態，將使用者查詢與 `title` 欄位進行比對，並依每個查詢集項目中的 `category` 自訂欄位篩選結果：

```json
PUT _plugins/_search_relevance/search_configurations
{
  "name": "mustache_filter",
  "query": "{\"query\":{\"bool\":{\"must\":[{\"match\":{\"title\":\"{% raw %}{{queryText}}{% endraw %}\"}}],\"filter\":[{\"term\":{\"category\":\"{% raw %}{{category}}{% endraw %}\"}}]}}}",
  "description": "Title match filtered by a category custom field",
  "index": "ecommerce"
}
```
{% include copy-curl.html %}

## 管理搜尋組態

您可以使用下列 API 擷取或刪除組態。

### 擷取搜尋組態

 此 API 會擷取搜尋組態。

#### 端點

```json
GET _plugins/_search_relevance/search_configurations
GET _plugins/_search_relevance/search_configurations/{search_configuration_id}
```

#### 範例回應

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
    "max_score": null,
    "hits": [
      {
        "_index": "search-relevance-search-config",
        "_id": "92810080-9c5a-470f-a0ff-0eb85e7b818c",
        "_score": null,
        "_source": {
          "id": "92810080-9c5a-470f-a0ff-0eb85e7b818c",
          "name": "baseline",
          "description": "Current production algorithm",
          "timestamp": "2025-06-12T08:23:03.305Z",
          "index": "ecommerce",
          "query": """{"query":{"multi_match":{"query":"%SearchText%","fields":["id","title","category","bullets","description","attrs.Brand","attrs.Color"]}}}""",
          "searchPipeline": ""
        },
        "sort": [
          1749716583305
        ]
      }
    ]
  }
}
```

### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `search_configuration_id` | 字串 | 要擷取的搜尋組態 ID。若為空，則擷取所有搜尋組態。 |

### 刪除搜尋組態

您可以使用搜尋組態 ID 刪除搜尋組態。

#### 端點

```json
DELETE _plugins/_search_relevance/search_configurations/{search_configuration_id}
```

#### 範例請求

```json
DELETE _plugins/_search_relevance/search_configurations/bb45c4c4-48ce-461b-acbc-f154c0a17ec9
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "_index": "search-relevance-search-config",
  "_id": "92810080-9c5a-470f-a0ff-0eb85e7b818c",
  "_version": 2,
  "result": "deleted",
  "forced_refresh": true,
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 9,
  "_primary_term": 1
}
```

### 搜尋搜尋組態

您可以使用 query DSL 搜尋可用的搜尋組態。

#### 端點

```json
GET _plugins/_search_relevance/search_configurations/_search
POST _plugins/_search_relevance/search_configurations/_search
```

#### 範例請求：搜尋所有搜尋組態

```json
GET _plugins/_search_relevance/search_configurations/_search
{
  "query":
  {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

#### 範例請求：依名稱搜尋搜尋組態

```json
GET _plugins/_search_relevance/search_configurations/_search
{
  "query": {
    "match": {
      "name": "baseline"
    }
  }
}
```
{% include copy-curl.html %}

請注意，儲存搜尋組態的索引包含數個 `keyword` 類型的欄位，需要完全相符。
{: .note}

#### 範例請求：使用多個條件搜尋搜尋組態

依特定目標索引與查詢模式搜尋搜尋組態：  

```json
GET _plugins/_search_relevance/search_configurations/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "index": "ecommerce"
          }
        },
        {
          "match": {
            "query": "multi_match"
          }
        }
      ]
    }
  },
  "size": 10
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.2086178,
    "hits": [
      {
        "_index": "search-relevance-search-config",
        "_id": "c86af6ed-a91e-450d-a630-aa2a3c525618",
        "_score": 1.2086178,
        "_source": {
          "id": "c86af6ed-a91e-450d-a630-aa2a3c525618",
          "name": "baseline",
          "description": "Current production algorithm",
          "timestamp": "2026-01-26T12:11:47.657Z",
          "index": "ecommerce",
          "query": """{"query":{"multi_match":{"query":"%SearchText%","fields":["asin","title","category","bullet_points","description","brand","color"]}}}""",
          "searchPipeline": ""
        }
      },
      {
        "_index": "search-relevance-search-config",
        "_id": "a4697191-744e-404a-b869-bbefb7e753ed",
        "_score": 1.2015147,
        "_source": {
          "id": "a4697191-744e-404a-b869-bbefb7e753ed",
          "name": "baseline with title weight",
          "timestamp": "2026-01-26T12:11:48.199Z",
          "index": "ecommerce",
          "query": """{"query":{"multi_match":{"query":"%SearchText%","fields":["asin","title^25","category","bullet_points","description","brand","color"]}}}""",
          "searchPipeline": ""
        }
      }
    ]
  }
}
```
