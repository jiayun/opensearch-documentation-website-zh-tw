---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用搜尋管線"
nav_order: 20
has_children: false
parent: Search pipelines
---

# 使用搜尋管線

您可以透過下列方式使用搜尋管線：

- 為請求[指定現有的管線](#specifying-an-existing-search-pipeline-for-a-request)。
- 為請求[使用暫時性管線](#using-a-temporary-search-pipeline-for-a-request)。
- 為索引中的所有請求設定[預設管線](#default-search-pipeline)。

## 為請求指定現有的搜尋管線

在[建立搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/)之後，您可以透過下列方式在查詢中使用該管線。如需搭配 `filter_query` 處理器使用搜尋管線的完整範例，請參閱 [`filter_query` 處理器範例]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/filter-query-processor#example)。

### 在查詢參數中指定管線

您可以在 `search_pipeline` 查詢參數中指定管線名稱，如下所示：

```json
GET /my_index/_search?search_pipeline=my_pipeline
```
{% include copy-curl.html %}

### 在請求本文中指定管線

您可以在搜尋請求本文中提供搜尋管線 ID，如下所示：

```json
GET /my-index/_search
{
    "query": {
        "match_all": {}
    },
    "from": 0,
    "size": 10,
    "search_pipeline": "my_pipeline"
}
```
{% include copy-curl.html %}

對於多重搜尋，您可以在搜尋請求本文中提供搜尋管線 ID，如下所示：

```json
GET /_msearch
{ "index": "test"}
{ "query": { "match_all": {} }, "from": 0, "size": 10, "search_pipeline": "my_pipeline"}
{ "index": "test-1", "search_type": "dfs_query_then_fetch"}
{ "query": { "match_all": {} }, "search_pipeline": "my_pipeline1" }

```
{% include copy-curl.html %}

## 為請求使用暫時性搜尋管線

除了建立搜尋管線之外，您也可以定義僅用於目前查詢的暫時性搜尋管線：

```json
POST /my-index/_search
{
  "query" : {
    "match" : {
      "text_field" : "some search text"
    }
  },
  "search_pipeline" : {
    "request_processors": [
      {
        "filter_query" : {
          "tag" : "tag1",
          "description" : "This processor is going to restrict to publicly visible documents",
          "query" : {
            "term": {
              "visibility": "public"
            }
          }
        }
      }
    ],
    "response_processors": [
      {
        "rename_field": {
          "field": "message",
          "target_field": "notification"
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

使用此語法時，管線不會保存，僅用於指定它的該次查詢。

## 預設搜尋管線

為了方便起見，您可以為索引設定預設搜尋管線。一旦索引有了預設管線，您就不需要在每個搜尋請求中指定 `search_pipeline` 查詢參數。

### 為索引設定預設搜尋管線

若要為索引設定預設搜尋管線，請在索引的設定中指定 `index.search.default_pipeline`：

```json
PUT /my_index/_settings 
{
  "index.search.default_pipeline" : "my_pipeline"
}
```
{% include copy-curl.html %}

為 `my_index` 設定預設管線後，您可以對所有文件執行相同的搜尋：

```json
GET /my_index/_search
```
{% include copy-curl.html %}

回應只包含公開文件，表示管線已預設套用：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took" : 19,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 0.0,
    "hits" : [
      {
        "_index" : "my_index",
        "_id" : "1",
        "_score" : 0.0,
        "_source" : {
          "message" : "This is a public message",
          "visibility" : "public"
        }
      }
    ]
  }
}
```
</details>

您可以跨多個共用相同預設管線的索引進行搜尋。例如，`alias1` 有兩個索引 `my_index1` 和 `my_index2`，兩者都附加了預設管線 `my_pipeline`：

```json
GET /alias1/_search
```
{% include copy-curl.html %}

回應只包含文件的公開版本，確認預設管線已成功套用：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
    "took": 59,
    "timed_out": false,
    "_shards": {
        "total": 2,
        "successful": 2,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 0.0,
        "hits": [
            {
                "_index": "my_index1",
                "_id": "1",
                "_score": 0.0,
                "_source": {
                    "message": "This is a public message",
                    "visibility": "public"
                }
            }
        ]
    }
}
```
</details>

### 為請求停用預設管線

如果您想在不套用預設管線的情況下執行搜尋請求，可以將 `search_pipeline` 查詢參數設定為 `_none`：

```json
GET /my_index/_search?search_pipeline=_none
```
{% include copy-curl.html %}

### 移除預設管線

若要從索引移除預設管線，請將其設定為 `null` 或 `_none`：

```json
PUT /my_index/_settings 
{
  "index.search.default_pipeline" : null
}
```
{% include copy-curl.html %}

```json
PUT /my_index/_settings 
{
  "index.search.default_pipeline" : "_none"
}
```
{% include copy-curl.html %}
