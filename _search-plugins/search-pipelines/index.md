---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋管線"
nav_order: 100
has_children: true
has_toc: false
redirect_from:
  - /search-plugins/search-pipelines/
---

# 搜尋管線

您可以使用_搜尋管線_來建立新的或重複使用現有的結果重新排序器、查詢重寫器，以及其他對查詢或結果進行操作的元件。搜尋管線可讓您更輕鬆地在 OpenSearch 內處理搜尋查詢和搜尋結果。將部分應用程式功能移至 OpenSearch 搜尋管線，可降低應用程式的整體複雜度。作為搜尋管線的一部分，您需指定一組執行模組化工作的搜尋處理器。接著，您即可輕鬆地新增或重新排序這些處理器，為您的應用程式自訂搜尋結果。

定義之後，搜尋管線是一份已整合至 OpenSearch 的搜尋處理器有序清單。下圖所示的管線會攔截查詢、對查詢執行處理、將其傳送至 OpenSearch、攔截結果、對結果執行處理，然後將其傳回呼叫的應用程式。

![搜尋處理器圖]({{site.url}}{{site.baseurl}}/images/search-pipelines.png)

管線的請求和回應處理都在協調節點上執行，因此沒有分片層級的處理。
{: .note}

## 搜尋處理器

搜尋處理器可依**執行階段**（其執行的時機）分類：

- [搜尋請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/search-processors#search-request-processors)：_搜尋請求處理器_會攔截搜尋請求（查詢和請求中傳入的中繼資料），對搜尋請求執行操作，並將搜尋請求提交至索引。
- [搜尋回應處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/search-processors#search-response-processors)：_搜尋回應處理器_會攔截搜尋回應和搜尋請求（查詢、結果和請求中傳入的中繼資料），對搜尋回應執行操作，並傳回搜尋回應。
- [搜尋階段結果處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/search-processors#search-phase-results-processors)：_搜尋階段結果處理器_會在協調節點層級的搜尋階段之間執行。它會攔截從某個搜尋階段擷取的結果，並在將其傳遞至下一個搜尋階段之前進行轉換。

## 範例

若要建立搜尋管線，請將請求傳送至搜尋管線端點，並指定一組將依序套用的處理器有序清單：

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
```
{% include copy-curl.html %}

如需建立和更新搜尋管線的詳細資訊，請參閱[建立搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/)。

若要將管線與查詢搭配使用，請在 `search_pipeline` 查詢參數中指定管線名稱：

```json
GET /my_index/_search?search_pipeline=my_pipeline
```
{% include copy-curl.html %}

或者，您可以使用請求的臨時管線，或為索引設定預設管線。如需深入了解，請參閱[使用搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/using-search-pipeline/)。

如需了解如何擷取現有搜尋管線的詳細資訊，請參閱[擷取搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/retrieving-search-pipeline/)。

如需搜尋管線疑難排解的相關資訊，請參閱[偵錯搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/debugging-search-pipeline/)。

若要刪除現有的搜尋管線，請參閱[刪除搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/deleting-search-pipeline/)。

## 手動與自動建立處理器

搜尋處理器可手動或自動建立：

- [使用者定義的處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/search-processors/)：在搜尋管線中手動設定的處理器，如前述[範例](#example)所示。
- [系統產生的處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/system-generated-search-processors/)：由 OpenSearch 根據搜尋請求參數自動建立的處理器。

## 搜尋管線指標

如需擷取搜尋管線統計資料的相關資訊，請參閱[搜尋管線指標]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/search-pipeline-metrics/)。