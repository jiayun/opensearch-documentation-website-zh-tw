---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "依欄位重新排序"
parent: Reranking search results
grand_parent: Optimizing search quality
has_children: false
nav_order: 20
---

# 依欄位重新排序搜尋結果
**Introduced 2.18**
{: .label .label-purple }

您可以使用 `by_field` rerank 類型，依文件欄位重新排序搜尋結果。當模型已經執行並為您的文件產生數值分數，或已套用先前的搜尋回應處理器，而您想根據彙總欄位以不同方式重新排序文件時，依欄位重新排序搜尋結果就非常實用。

若要實作重新排序，您需要設定一個在搜尋時執行的[搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/)。搜尋管線會攔截搜尋結果，並對其套用 [`rerank` 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/)。`rerank` 處理器會評估搜尋結果，並根據從文件欄位取得的新分數進行排序。

## 執行含重新排序的搜尋

若要執行含重新排序的搜尋，請依照下列步驟：

1. [設定搜尋管線](#step-1-configure-a-search-pipeline)。
1. [建立用於匯入的索引](#step-2-create-an-index-for-ingestion)。
1. [將文件匯入索引](#step-3-ingest-documents-into-the-index)。
1. [使用重新排序進行搜尋](#step-4-search-using-reranking)。

## 步驟 1：設定搜尋管線

設定一個包含 [`rerank` 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/) 的搜尋管線，並指定 `by_field` rerank 類型。管線會依 `reviews.stars` 欄位排序（以完整的點路徑指定該欄位），並傳回所有文件的原始查詢分數及其新分數：

```json
PUT /_search/pipeline/rerank_byfield_pipeline
{
  "response_processors": [
    {
      "rerank": {
        "by_field": {
          "target_field": "reviews.stars",
          "keep_previous_score" : true
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

如需請求欄位的更多資訊，請參閱 [Request fields]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/#request-body-fields)。

當 `keep_previous_score` 為 `true` 時，重新排序前的分數預設會儲存在 `previous_score` 中。如果 `previous_score` 已存在於您的文件中，請使用 `previous_score_field` 選擇不同的欄位名稱。

## 步驟 2：建立用於匯入的索引

若要使用管線中定義的 `rerank` 處理器，請建立一個 OpenSearch 索引，並將上一步建立的管線新增為預設管線：

```json
PUT /book-index
{
  "settings": {
    "index.search.default_pipeline" : "rerank_byfield_pipeline"
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "author": {
        "type": "text"
      },
      "genre": {
        "type": "keyword"
      },
      "reviews": {
        "properties": {
          "stars": {
            "type": "float"
          }
        }
      },
      "description": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 步驟 3：將文件匯入索引

若要將文件匯入上一步建立的索引，請傳送下列大量請求：

```json
POST /_bulk
{ "index": { "_index": "book-index", "_id": "1" } }
{ "title": "The Lost City", "author": "Jane Doe", "genre": "Adventure Fiction", "reviews": { "stars": 4.2 }, "description": "An exhilarating journey through a hidden civilization in the Amazon rainforest." }
{ "index": { "_index": "book-index", "_id": "2" } }
{ "title": "Whispers of the Past", "author": "John Smith", "genre": "Historical Mystery", "reviews": { "stars": 4.7 }, "description": "A gripping tale set in Victorian England, unraveling a century-old mystery." }
{ "index": { "_index": "book-index", "_id": "3" } }
{ "title": "Starlit Dreams", "author": "Emily Clark", "genre": "Science Fiction", "reviews": { "stars": 4.5 }, "description": "In a future where dreams can be shared, one girl discovers her imaginations power." }
{ "index": { "_index": "book-index", "_id": "4" } }
{ "title": "The Enchanted Garden", "author": "Alice Green", "genre": "Fantasy", "reviews": { "stars": 4.8 }, "description": "A magical garden holds the key to a young girls destiny and friendship." }

```
{% include copy-curl.html %}

## 步驟 4：使用重新排序進行搜尋

作為範例，請在您的索引上執行 `match_all` 查詢：

```json
POST /book-index/_search
{
  "query": {
     "match_all": {}
  }
}
```
{% include copy-curl.html %}

回應包含依 `reviews.stars` 欄位以遞減順序排序的文件。每份文件在 `previous_score` 欄位中包含原始查詢分數：

```json
{
  "took": 33,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": 4.8,
    "hits": [
      {
        "_index": "book-index",
        "_id": "4",
        "_score": 4.8,
        "_source": {
          "reviews": {
            "stars": 4.8
          },
          "author": "Alice Green",
          "genre": "Fantasy",
          "description": "A magical garden holds the key to a young girls destiny and friendship.",
          "previous_score": 1,
          "title": "The Enchanted Garden"
        }
      },
      {
        "_index": "book-index",
        "_id": "2",
        "_score": 4.7,
        "_source": {
          "reviews": {
            "stars": 4.7
          },
          "author": "John Smith",
          "genre": "Historical Mystery",
          "description": "A gripping tale set in Victorian England, unraveling a century-old mystery.",
          "previous_score": 1,
          "title": "Whispers of the Past"
        }
      },
      {
        "_index": "book-index",
        "_id": "3",
        "_score": 4.5,
        "_source": {
          "reviews": {
            "stars": 4.5
          },
          "author": "Emily Clark",
          "genre": "Science Fiction",
          "description": "In a future where dreams can be shared, one girl discovers her imaginations power.",
          "previous_score": 1,
          "title": "Starlit Dreams"
        }
      },
      {
        "_index": "book-index",
        "_id": "1",
        "_score": 4.2,
        "_source": {
          "reviews": {
            "stars": 4.2
          },
          "author": "Jane Doe",
          "genre": "Adventure Fiction",
          "description": "An exhilarating journey through a hidden civilization in the Amazon rainforest.",
          "previous_score": 1,
          "title": "The Lost City"
        }
      }
    ]
  },
  "profile": {
    "shards": []
  }
}
```

## 後續步驟

- 進一步了解 [`rerank` 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/)。
- 查看使用外部託管交叉編碼器模型依欄位重新排序的[完整範例]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-by-field-cross-encoder/)。