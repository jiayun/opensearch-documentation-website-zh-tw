---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "混合搜尋"
parent: AI search
has_children: true
nav_order: 40
redirect_from:
   - /search-plugins/hybrid-search/
   - /vector-search/ai-search/hybrid-search/
---

# 混合搜尋
於 2.11 版推出
{: .label .label-purple }

混合搜尋結合關鍵字搜尋與語意搜尋，以提升搜尋相關性。若要實作混合搜尋，您需要設定一個在搜尋時執行的[搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/)。搜尋管線會在中間階段攔截搜尋結果，並套用處理程序來正規化及合併文件分數。

混合搜尋提供兩種搜尋階段結果處理器，兩者的差異在於合併的內容不同：

- [正規化處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/)以分數為基礎。它會將每個查詢子句的分數轉換為共同的尺度，然後加以合併，並保留文件之間的差距。當兩份文件分數之間的差異含有最終排名必須反映的資訊，或者當您需要透過正規化技術、合併技術及分數界限進行精細控制時，請選擇此處理器。
- [分數排名處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/score-ranker-processor/)以排名為基礎。它使用倒數排名融合 (RRF)，依據文件在每個查詢子句結果中的位置來合併文件，而忽略分數本身。當您想要一種不需先衡量查詢子句如何為文件評分即可運作的組態時，請選擇此處理器。如需更多資訊，請參閱[倒數排名融合]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/rrf/)。

下列範例使用正規化處理器。若要在您自己的資料與判斷清單上比較這兩種處理器，請參閱[最佳化混合搜尋]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/optimize-hybrid-search/)。

**先決條件**<br>
若要依照此範例操作，您必須設定文字嵌入模型。如需更多資訊，請參閱[選擇模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#choosing-a-model)。如果您已經產生文字嵌入，請跳至[步驟 3](#step-3-configure-a-search-pipeline)。
{: .note}

## 設定混合搜尋

設定混合搜尋有兩種方式：

- [**自動化工作流程**](#automated-workflow)（建議用於快速設定）：以最少的組態自動建立資料匯入管線、索引及搜尋管線。
- [**手動設定**](#manual-setup)（建議用於自訂組態）：手動設定每個元件，以獲得更大的彈性與控制權。

## 自動化工作流程

OpenSearch 提供[工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates/#hybrid-search)，可自動建立資料匯入管線、索引及搜尋管線。建立工作流程時，您必須提供所設定模型的模型 ID。請檢閱混合搜尋工作流程範本的[預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/hybrid-search-defaults.json)，以判斷是否需要更新任何參數。例如，如果模型維度與預設值 (`1024`) 不同，請在 `output_dimension` 參數中指定模型的維度。若要建立預設的混合搜尋工作流程，請傳送下列請求：

```json
POST /_plugins/_flow_framework/workflow?use_case=hybrid_search&provision=true
{
"create_ingest_pipeline.model_id": "mBGzipQB2gmRjlv_dOoB"
}
```
{% include copy-curl.html %}

OpenSearch 會回應所建立工作流程的工作流程 ID：

```json
{
  "workflow_id" : "U_nMXJUBq_4FYQzMOS4B"
}
```

若要檢查工作流程狀態，請傳送下列請求：

```json
GET /_plugins/_flow_framework/workflow/U_nMXJUBq_4FYQzMOS4B/_status
```
{% include copy-curl.html %}

工作流程完成後，`state` 會變更為 `COMPLETED`。工作流程會建立下列元件：

- 名為 `nlp-ingest-pipeline` 的資料匯入管線
- 名為 `my-nlp-index` 的索引
- 名為 `nlp-search-pipeline` 的搜尋管線

您現在可以繼續進行[步驟 4 和 5](#step-4-ingest-documents-into-the-index)，將文件匯入索引並搜尋該索引。

## 手動設定

若要手動設定混合搜尋，請依照下列步驟操作：

1. [建立資料匯入管線](#step-1-create-an-ingest-pipeline)。
1. [建立用於匯入的索引](#step-2-create-an-index-for-ingestion)。
1. [設定搜尋管線](#step-3-configure-a-search-pipeline)。
1. [將文件匯入索引](#step-4-ingest-documents-into-the-index)。
1. [使用混合搜尋來搜尋索引](#step-5-search-the-index-using-hybrid-search)。

## 步驟 1：建立資料匯入管線

若要產生向量嵌入，您需要建立一個[資料匯入管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/)，其中包含 [`text_embedding` 處理器]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/processors/text-embedding/)，它會將文件欄位中的文字轉換為向量嵌入。處理器的 `field_map` 會決定要從哪些輸入欄位產生向量嵌入，以及要在哪些輸出欄位中儲存嵌入。

下列範例請求會建立一個資料匯入管線，將 `passage_text` 中的文字轉換為文字嵌入，並將嵌入儲存在 `passage_embedding` 中：

```json
PUT /_ingest/pipeline/nlp-ingest-pipeline
{
  "description": "A text embedding pipeline",
  "processors": [
    {
      "text_embedding": {
        "model_id": "bQ1J8ooBpBj3wT4HVUsb",
        "field_map": {
          "passage_text": "passage_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 步驟 2：建立用於匯入的索引

為了使用管線中定義的文字嵌入處理器，請建立向量索引，並將上一個步驟建立的管線新增為預設管線。請確保 `field_map` 中定義的欄位對應為正確的類型。延續此範例，`passage_embedding` 欄位必須對應為維度符合模型維度的 k-NN 向量。同樣地，`passage_text` 欄位應對應為 `text`。

下列範例請求會建立一個已設定預設資料匯入管線的向量索引：

```json
PUT /my-nlp-index
{
  "settings": {
    "index.knn": true,
    "default_pipeline": "nlp-ingest-pipeline"
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "text"
      },
      "passage_embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "engine": "lucene",
          "space_type": "l2",
          "name": "hnsw",
          "parameters": {}
        }
      },
      "passage_text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

如需建立向量索引及使用支援方法的詳細資訊，請參閱[建立向量索引]({{site.url}}{{site.baseurl}}/search-plugins/knn/knn-index/)。


## 步驟 3：設定搜尋管線

若要使用 [`normalization-processor`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/) 設定搜尋管線，請使用下列請求。處理器中的正規化技術設為 `min_max`，合併技術設為 `arithmetic_mean`。`weights` 陣列會以十進位百分比指定指派給每個查詢子句的權重：

```json
PUT /_search/pipeline/nlp-search-pipeline
{
  "description": "Post processor for hybrid search",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": {
          "technique": "min_max"
        },
        "combination": {
          "technique": "arithmetic_mean",
          "parameters": {
            "weights": [
              0.3,
              0.7
            ]
          }
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 步驟 4：將文件匯入索引

若要將文件匯入上一個步驟建立的索引，請傳送下列請求：

```json
PUT /my-nlp-index/_doc/1
{
  "passage_text": "Hello world",
  "id": "s1"
}
```
{% include copy-curl.html %}

```json
PUT /my-nlp-index/_doc/2
{
  "passage_text": "Hi planet",
  "id": "s2"
}
```
{% include copy-curl.html %}

在文件匯入索引之前，資料匯入管線會對文件執行 `text_embedding` 處理器，為 `passage_text` 欄位產生文字嵌入。已編製索引的文件包含 `passage_text` 欄位，其中存放原始文字，以及 `passage_embedding` 欄位，其中存放向量嵌入。 

## 步驟 5：使用混合搜尋來搜尋索引

若要對您的索引執行混合搜尋，請使用 [`hybrid` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/hybrid/)，此查詢會結合關鍵字搜尋與語意搜尋的結果。

#### 範例：結合 neural 查詢與 match 查詢

下列範例請求結合了兩個查詢子句：`neural` 查詢與 `match` 查詢。它透過查詢參數指定上一個步驟建立的搜尋管線：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "_source": {
    "exclude": [
      "passage_embedding"
    ]
  },
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "passage_text": {
              "query": "Hi world"
            }
          }
        },
        {
          "neural": {
            "passage_embedding": {
              "query_text": "Hi world",
              "model_id": "aVeif4oB5Vm0Tdw8zYO2",
              "k": 5
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

您也可以為 `my-nlp-index` 索引設定預設搜尋管線。如需詳細資訊，請參閱[預設搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/using-search-pipeline/#default-search-pipeline)。

回應包含符合條件的文件：

```json
{
  "took" : 36,
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
    "max_score" : 1.2251667,
    "hits" : [
      {
        "_index" : "my-nlp-index",
        "_id" : "1",
        "_score" : 1.2251667,
        "_source" : {
          "passage_text" : "Hello world",
          "id" : "s1"
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

#### 範例：結合 match 查詢與 term 查詢

下列範例請求結合了兩個查詢子句：`match` 查詢與 `term` 查詢。它透過查詢參數指定上一個步驟建立的搜尋管線：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "_source": {
    "exclude": [
      "passage_embedding"
    ]
  },
  "query": {
    "hybrid": {
      "queries": [
           {
             "match":{
                 "passage_text": "hello"
              }
           },
           {
             "term":{
              "passage_text":{
                 "value":"planet"
              }
             }
           }
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應包含符合條件的文件：

```json
{
    "took": 11,
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
        "max_score": 0.7,
        "hits": [
            {
                "_index": "my-nlp-index",
                "_id": "2",
                "_score": 0.7,
                "_source": {
                    "id": "s2",
                    "passage_text": "Hi planet"
                }
            },
            {
                "_index": "my-nlp-index",
                "_id": "1",
                "_score": 0.3,
                "_source": {
                    "id": "s1",
                    "passage_text": "Hello world"
                }
            }
        ]
    }
}
```
{% include copy-curl.html %}

## 篩選資料

混合搜尋支援兩種篩選方式：

- **預先篩選** 會在評分之前移除文件。若要使用預先篩選，請在 `hybrid` 查詢中新增最上層的 `filter`。這是篩選混合搜尋結果最常見的方式。如需詳細資訊，請參閱[使用預先篩選的混合搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/pre-filtering/)
- **事後篩選** 會在所有評分完成後移除文件。若要使用事後篩選，請在搜尋請求中新增 `post_filter`。在搭配彙總的面向搜尋中，若您希望面向反映未篩選的查詢，同時只篩選顯示的命中結果，請使用此方式。如需詳細資訊，請參閱[使用事後篩選的混合搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/post-filtering/)。

## 後續步驟

- 探索我們的[教學]({{site.url}}{{site.baseurl}}/vector-search/tutorials/)，了解如何建置 AI 搜尋應用程式。 