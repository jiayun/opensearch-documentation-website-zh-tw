---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "語意搜尋"
parent: AI search
nav_order: 35
has_children: false
redirect_from:
  - /search-plugins/neural-text-search/
  - /search-plugins/semantic-search/
---

# 語意搜尋

語意搜尋會考量查詢的上下文與意圖。在 OpenSearch 中，語意搜尋是透過文字嵌入模型來實現。語意搜尋會建立稠密向量（一連串的浮點數），並將資料匯入向量索引。

**先決條件**<br>
在使用語意搜尋之前，您必須設定文字嵌入模型。如需詳細資訊，請參閱[選擇模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#choosing-a-model)。
{: .note}

## 設定語意搜尋

您可以透過兩種方式之一來設定語意搜尋。在[手動設定](#manual-setup)中，您自行設定資料匯入管線與索引，可完全掌控每個元件。或者，您也可以[使用語意欄位](#using-a-semantic-field)，這種方式可簡化設定程序，同時仍允許您自訂部分組態。

## 手動設定

若要手動設定語意搜尋，請依照下列步驟：

1. [建立資料匯入管線](#step-1-create-an-ingest-pipeline)。
1. [建立用於匯入的索引](#step-2-create-an-index-for-ingestion)。
1. [將文件匯入索引](#step-3-ingest-documents-into-the-index)。
1. [搜尋索引](#step-4-search-the-index)。

### 步驟 1：建立資料匯入管線

若要產生向量嵌入，您需要建立包含 [`text_embedding` 處理器]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/processors/text-embedding/)的[資料匯入管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/)，該處理器會將文件欄位中的文字轉換為向量嵌入。處理器的 `field_map` 會決定要從哪些輸入欄位產生向量嵌入，以及要將嵌入儲存在哪些輸出欄位中。

下列範例請求會建立資料匯入管線，其中 `passage_text` 的文字會轉換為文字嵌入，而嵌入會儲存在 `passage_embedding` 中：

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

若要將長文字分割為段落，請在 `text_embedding` 處理器之前使用 `text_chunking` 匯入處理器。如需詳細資訊，請參閱[文字區塊化]({{site.url}}{{site.baseurl}}/search-plugins/text-chunking/)。

### 步驟 2：建立用於匯入的索引

為了使用您在管線中定義的文字嵌入處理器，請建立向量索引，並將上一個步驟建立的管線新增為預設管線。請確保 `field_map` 中定義的欄位對應為正確的類型。延續先前的範例，`passage_embedding` 欄位必須對應為維度符合模型維度的 k-NN 向量。同樣地，`passage_text` 欄位應對應為 `text`。

下列範例請求會建立已設定預設資料匯入管線的向量索引：

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

如需建立向量索引及其支援方法的詳細資訊，請參閱[建立向量索引]({{site.url}}{{site.baseurl}}/search-plugins/knn/knn-index/)。

### 步驟 3：將文件匯入索引

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

在文件匯入索引之前，資料匯入管線會對文件執行 `text_embedding` 處理器，為 `passage_text` 欄位產生文字嵌入。編製索引的文件包含 `passage_text` 欄位（其中含有原始文字）以及 `passage_embedding` 欄位（其中含有向量嵌入）。

### 步驟 4：搜尋索引

若要在索引上執行向量搜尋，請在 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/) 查詢中使用 `neural` 查詢子句。若要將搜尋限制在符合條件的文件，請使用[向量搜尋篩選器]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/index/)。

下列範例請求使用布林查詢來合併兩個查詢子句：一個神經查詢和一個 `match` 查詢。`script_score` 查詢會為查詢子句指派自訂權重：

```json
GET /my-nlp-index/_search
{
  "_source": {
    "excludes": [
      "passage_embedding"
    ]
  },
  "query": {
    "bool": {
      "should": [
        {
          "script_score": {
            "query": {
              "neural": {
                "passage_embedding": {
                  "query_text": "Hi world",
                  "model_id": "bQ1J8ooBpBj3wT4HVUsb",
                  "k": 100
                }
              }
            },
            "script": {
              "source": "_score * 1.5"
            }
          }
        },
        {
          "script_score": {
            "query": {
              "match": {
                "passage_text": "Hi world"
              }
            },
            "script": {
              "source": "_score * 1.7"
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應會包含這兩份文件，並依兩個子句的合併分數排序：

```json
{
  "took": 211,
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
    "max_score": 0.5848836,
    "hits": [
      {
        "_index": "my-nlp-index",
        "_id": "2",
        "_score": 0.5848836,
        "_source": {
          "passage_text": "Hi planet",
          "id": "s2"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "1",
        "_score": 0.5824303,
        "_source": {
          "passage_text": "Hello world",
          "id": "s1"
        }
      }
    ]
  }
}
```

若要在一個步驟中建立資料匯入管線和索引，您可以使用[語意搜尋工作流程範本]({{site.url}}{{site.baseurl}}/vector-search/ai-search/workflows/workflow-templates/#semantic-search)。
{: .tip}

### 在索引或欄位上設定預設模型

[`neural`]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural/) 查詢需要模型 ID 才能產生向量嵌入。若要避免在每次神經查詢請求中傳入模型 ID，您可以在向量索引或欄位上設定預設模型。 

首先，建立包含 [`neural_query_enricher`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/neural-query-enricher/) 請求處理器的[搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/)。若要為索引設定預設模型，請在 `default_model_id` 參數中提供模型 ID。若要為特定欄位設定預設模型，請在 `neural_field_default_id` 對應表中提供欄位名稱及對應的模型 ID。如果您同時提供 `default_model_id` 和 `neural_field_default_id`，則 `neural_field_default_id` 優先：

```json
PUT /_search/pipeline/default_model_pipeline 
{
  "request_processors": [
    {
      "neural_query_enricher" : {
        "default_model_id": "bQ1J8ooBpBj3wT4HVUsb",
        "neural_field_default_id": {
           "my_field_1": "uZj0qYoBMtvQlfhaYeud",
           "my_field_2": "upj0qYoBMtvQlfhaZOuM"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

接著，為您的索引設定預設模型：

```json
PUT /my-nlp-index/_settings
{
  "index.search.default_pipeline" : "default_model_pipeline"
}
```
{% include copy-curl.html %}

現在，您可以在搜尋時省略模型 ID：

```json
GET /my-nlp-index/_search
{
  "_source": {
    "excludes": [
      "passage_embedding"
    ]
  },
  "query": {
    "neural": {
      "passage_embedding": {
        "query_text": "Hi world",
        "k": 100
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含這兩份文件：

```json
{
  "took" : 41,
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
    "max_score" : 1.22762,
    "hits" : [
      {
        "_index" : "my-nlp-index",
        "_id" : "2",
        "_score" : 1.22762,
        "_source" : {
          "passage_text" : "Hi planet",
          "id" : "s2"
        }
      },
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

## 使用語意欄位

若要使用 `semantic` 欄位手動設定語意搜尋，請依照下列步驟操作。如需更多資訊，包括使用 `semantic` 欄位時的限制，請參閱[語意欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/semantic/)。 

### 步驟 1：建立包含語意欄位的索引

建立一個索引，並在 `semantic` 欄位中指定 `model_id`。在此範例中，`semantic` 欄位為 `passage_text`。OpenSearch 會根據模型組態自動建立對應的嵌入欄位。不需要資料匯入管線——OpenSearch 會在編製索引時使用指定的模型自動產生嵌入：

```json
PUT /my-nlp-index
{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "text"
      },
      "passage_text": {
        "type": "semantic",
        "model_id": "9kPWYJcBmp4cG9LrbAvW"
      }
    }
  }
}
```
{% include copy-curl.html %}

建立索引後，您可以擷取其對應，以驗證嵌入欄位是否已自動建立：

```json
GET /my-nlp-index/_mapping
```
{% include copy-curl.html %}

回應會顯示自動建立的 `passage_text_semantic_info` 欄位：

```json
{
  "my-nlp-index": {
    "mappings": {
      "properties": {
        "id": {
          "type": "text"
        },
        "passage_text": {
          "type": "semantic",
          "model_id": "9kPWYJcBmp4cG9LrbAvW",
          "raw_field_type": "text"
        },
        "passage_text_semantic_info": {
          "properties": {
            "embedding": {
              "type": "knn_vector",
              "dimension": 384,
              "method": {
                "engine": "faiss",
                "space_type": "l2",
                "name": "hnsw",
                "parameters": {}
              }
            },
            "model": {
              "properties": {
                "id": {
                  "type": "text",
                  "index": false
                },
                "name": {
                  "type": "text",
                  "index": false
                },
                "type": {
                  "type": "text",
                  "index": false
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### 步驟 2：將文件匯入索引

若要將文件匯入上一個步驟建立的索引，請傳送下列請求：

```json
PUT /my-nlp-index/_doc/1
{
  "passage_text": "Hello world",
  "id": "s1"
}
```
{% include copy-curl.html %}

在文件匯入索引之前，OpenSearch 會執行內建的資料匯入管線，產生嵌入並將其儲存在 `passage_text_semantic_info.embedding` 欄位中。若要確認嵌入已正確產生，請擷取該文件：

```json
GET /my-nlp-index/_doc/1
```
{% include copy-curl.html %}

回應會在 `passage_text_semantic_info` 欄位中包含產生的嵌入：

```json
{
  "_index": "my-nlp-index",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "passage_text": "Hello world",
    "passage_text_semantic_info": {
      "model": {
        "name": "huggingface/sentence-transformers/all-MiniLM-L6-v2",
        "id": "9kPWYJcBmp4cG9LrbAvW",
        "type": "TEXT_EMBEDDING"
      },
      "embedding": [
        -0.034477286,
        ...
      ]
    },
    "id": "s1"
  }
}
```

### 步驟 3：搜尋索引

若要查詢 `semantic` 欄位的嵌入，請提供 `semantic` 欄位的名稱（在此範例中為 `passage_text`）及查詢文字。您無需指定 `model_id`，OpenSearch 會自動從索引對應中的欄位組態擷取它，並改寫查詢，將底層嵌入欄位設為查詢目標：

```json
GET /my-nlp-index/_search
{
  "_source": {
    "excludes": [
      "passage_text_semantic_info"
    ]
  },
  "query": {
    "neural": {
      "passage_text": {
        "query_text": "Hi world"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含符合條件的文件：

```json
{
  "took": 48,
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
    "max_score": 0.7564365,
    "hits": [
      {
        "_index": "my-nlp-index",
        "_id": "1",
        "_score": 0.7564365,
        "_source": {
          "passage_text": "Hello world",
          "id": "s1"
        }
      }
    ]
  }
}
```

## 後續步驟

- 若要將搜尋結果限制為符合條件的文件，請參閱[篩選向量搜尋結果]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/index/)。
- 若要了解如何建置 AI 搜尋應用程式，請探索我們的[語意搜尋教學]({{site.url}}{{site.baseurl}}/vector-search/tutorials/semantic-search/)。
