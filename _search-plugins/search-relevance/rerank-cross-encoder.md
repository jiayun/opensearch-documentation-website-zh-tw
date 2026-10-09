---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用交叉編碼器模型重新排序"
parent: Reranking search results
grand_parent: Optimizing search quality
has_children: false
nav_order: 10
---

# 使用交叉編碼器模型重新排序搜尋結果
**於 2.12 版推出**
{: .label .label-purple }

您可以使用交叉編碼器模型重新排序搜尋結果，以提升搜尋相關性。若要實作重新排序，您需要設定一個在搜尋時執行的[搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/)。搜尋管線會攔截搜尋結果，並對其套用 [`rerank` 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/)。`rerank` 處理器會評估搜尋結果，並依據交叉編碼器模型提供的新分數加以排序。

**先決條件**<br>
設定重新排序管線之前，您必須先設定交叉編碼器模型。如需使用 OpenSearch 所提供模型的相關資訊，請參閱[交叉編碼器模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/#cross-encoder-models)。如需使用自訂模型的相關資訊，請參閱[自訂本機模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/custom-local-models/)。
{: .note}

## 執行含重新排序的搜尋

若要執行含重新排序的搜尋，請依照下列步驟進行：

1. [設定搜尋管線](#step-1-configure-a-search-pipeline)。
1. [建立用於匯入的索引](#step-2-create-an-index-for-ingestion)。
1. [將文件匯入索引](#step-3-ingest-documents-into-the-index)。
1. [使用重新排序進行搜尋](#step-4-search-using-reranking)。

## 步驟 1：設定搜尋管線

接著，使用 [`rerank` 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/)設定搜尋管線，並指定 `ml_opensearch` 重新排序類型。在請求中，提供交叉編碼器模型的模型 ID，以及要做為內容使用的文件欄位：

```json
PUT /_search/pipeline/my_pipeline
{
  "description": "Pipeline for reranking with a cross-encoder",
  "response_processors": [
    {
      "rerank": {
        "ml_opensearch": {
          "model_id": "gnDIbI0BfUsSoeNT_jAw"
        },
        "context": {
          "document_fields": [
            "passage_text"
          ]
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

如需請求欄位的詳細資訊，請參閱[請求欄位]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/#request-body-fields)。

## 步驟 2：建立用於匯入的索引

為了使用您在管線中定義的 `rerank` 處理器，請建立 OpenSearch 索引，並將前一個步驟建立的管線新增為預設管線：

```json
PUT /my-index
{
  "settings": {
    "index.search.default_pipeline" : "my_pipeline"
  },
  "mappings": {
    "properties": {
      "passage_text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 步驟 3：將文件匯入索引

若要將文件匯入前一個步驟建立的索引，請傳送下列大量請求：

```json
POST /_bulk
{ "index": { "_index": "my-index" } }
{ "passage_text" : "I said welcome to them and we entered the house" }
{ "index": { "_index": "my-index" } }
{ "passage_text" : "I feel welcomed in their family" }
{ "index": { "_index": "my-index" } }
{ "passage_text" : "Welcoming gifts are great" }

```
{% include copy-curl.html %}

## 步驟 4：使用重新排序進行搜尋

若要在您的索引上執行重新排序搜尋，請使用任何 OpenSearch 查詢，並提供額外的 `ext.rerank` 欄位：

```json
POST /my-index/_search
{
  "query": {
    "match": {
      "passage_text": "how to welcome in family"
    }
  },
  "ext": {
    "rerank": {
      "query_context": {
         "query_text": "how to welcome in family"
      }
    }
  }
}
```
{% include copy-curl.html %}

或者，您也可以提供包含內容之欄位的完整路徑。如需詳細資訊，請參閱[重新排序處理器範例]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/#example)。

## 後續步驟

- 進一步了解 [`rerank` 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/)。
- 參閱[使用外部託管的交叉編碼器模型依欄位重新排序]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-by-field-cross-encoder/)的完整範例。