---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "篩選查詢"
nav_order: 20
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# 篩選查詢處理器
於 2.8 版推出
{: .label .label-purple }

`filter_query` 搜尋請求處理器會攔截搜尋請求，並對該請求套用額外的查詢，以篩選結果。當您不想重寫應用程式中現有的查詢，但需要對結果進行額外篩選時，這個處理器非常實用。

## 請求本文欄位

下表列出所有可用的請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`query` | 物件 | 以查詢領域特定語言 (DSL) 表示的查詢。OpenSearch 查詢類型的清單請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/)。必要。
`tag` | 字串 | 處理器的識別碼。選用。
`description` | 字串 | 處理器的描述。選用。
`ignore_failure` | 布林值 | 若為 `true`，OpenSearch 會[忽略此處理器的任何失敗]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/#ignoring-processor-failures)，並繼續執行搜尋管線中其餘的處理器。選用。預設為 `false`。

## 範例

以下範例示範如何使用包含 `filter_query` 處理器的搜尋管線。

### 設定

建立名為 `my_index` 的索引，並將兩份文件編製索引，一份公開、一份私密：

```json
POST /my_index/_doc/1
{
  "message": "This is a public message", 
  "visibility":"public"
}
```
{% include copy-curl.html %}

```json
POST /my_index/_doc/2
{
  "message": "This is a private message", 
  "visibility": "private"
}
```
{% include copy-curl.html %}

### 建立搜尋管線

以下請求會建立名為 `my_pipeline` 的搜尋管線，其中包含一個 `filter_query` 請求處理器，該處理器使用 term 查詢僅傳回公開的訊息：

```json
PUT /_search/pipeline/my_pipeline 
{
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
  ]
}
```
{% include copy-curl.html %}

### 使用搜尋管線

在不使用搜尋管線的情況下搜尋 `my_index` 中的文件：

```json
GET /my_index/_search
```
{% include copy-curl.html %}

回應包含兩份文件：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}
```json
{
  "took" : 47,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my_index",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "message" : "This is a public message",
          "visibility" : "public"
        }
      },
      {
        "_index" : "my_index",
        "_id" : "2",
        "_score" : 1.0,
        "_source" : {
          "message" : "This is a private message",
          "visibility" : "private"
        }
      }
    ]
  }
}
```
</details>

若要使用管線進行搜尋，請在 `search_pipeline` 查詢參數中指定管線名稱：

```json
GET /my_index/_search?search_pipeline=my_pipeline
```
{% include copy-curl.html %}

回應僅包含 `public` 可見性的文件：

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