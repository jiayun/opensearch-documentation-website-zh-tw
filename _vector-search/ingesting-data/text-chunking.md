---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "文字分段"
parent: Ingesting data
nav_order: 80
redirect_from:
  - /search-plugins/text-chunking/
---

# 文字分段
Introduced 2.13
{: .label .label-purple }

在 [AI 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/) 中處理大型文字文件時，通常需要將其分割成較小的段落，因為大多數嵌入模型都有詞元長度限制。這個稱為_文字分段_的流程，可確保每個嵌入都代表一段符合模型限制的聚焦內容，藉此維持向量搜尋結果的品質與相關性。

若要將長文字分割成段落，您可以使用 `text_chunking` 處理器，作為 `text_embedding` 或 `sparse_encoding` 處理器的前置處理步驟，以取得每個分段段落的嵌入。如需處理器參數的詳細資訊，請參閱[文字分段處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-chunking/)。開始之前，請依照[預先訓練模型文件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/)中概述的步驟註冊嵌入模型。下列範例會先將文字分割成段落進行前置處理，然後使用 `text_embedding` 或 `sparse_encoding` 處理器產生嵌入。

## 使用文字嵌入處理器進行文字分段

下列範例使用文字嵌入處理器來執行文字分段。


### 步驟 1：建立管線

下列範例請求會建立資料匯入管線，將 `passage_text` 欄位中的文字轉換為分段段落，並儲存在 `passage_chunk` 欄位中。接著將 `passage_chunk` 欄位中的文字轉換為文字嵌入，並將嵌入儲存在 `passage_chunk_embedding` 欄位中：

```json
PUT _ingest/pipeline/text-chunking-embedding-ingest-pipeline
{
  "description": "A text chunking and embedding ingest pipeline",
  "processors": [
    {
      "text_chunking": {
        "algorithm": {
          "fixed_token_length": {
            "token_limit": 10,
            "overlap_rate": 0.2,
            "tokenizer": "standard"
          }
        },
        "field_map": {
          "passage_text": "passage_chunk"
        }
      }
    },
    {
      "text_embedding": {
        "model_id": "LMLPWY4BROvhdbtgETaI",
        "field_map": {
          "passage_chunk": "passage_chunk_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2：建立用於匯入的索引

若要使用資料匯入管線，您需要建立向量索引。`passage_chunk_embedding` 欄位必須是 `nested` 類型。`knn.dimension` 欄位必須包含模型的維度數量：

```json
PUT testindex
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "passage_text": {
        "type": "text"
      },
      "passage_chunk_embedding": {
        "type": "nested",
        "properties": {
          "knn": {
            "type": "knn_vector",
            "dimension": 768
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 3：將文件匯入索引

若要將文件匯入上一個步驟中建立的索引，請傳送下列請求：

```json
POST testindex/_doc?pipeline=text-chunking-embedding-ingest-pipeline
{
  "passage_text": "This is an example document to be chunked. The document contains a single paragraph, two sentences and 24 tokens by standard tokenizer in OpenSearch."
}
```
{% include copy-curl.html %}

### 步驟 4：搜尋索引

您可以使用 `nested` 查詢對索引執行向量搜尋。我們建議將 `score_mode` 設為 `max`，如此文件分數會設為所有段落嵌入中的最高分數：

```json
GET testindex/_search
{
  "query": {
    "nested": {
      "score_mode": "max",
      "path": "passage_chunk_embedding",
      "query": {
        "neural": {
          "passage_chunk_embedding.knn": {
            "query_text": "document",
            "model_id": "LMLPWY4BROvhdbtgETaI"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 使用稀疏編碼處理器進行文字分段

下列範例使用稀疏編碼處理器來執行文字分段。


### 步驟 1：建立管線

下列範例請求會建立資料匯入管線，將 `passage_text` 欄位中的文字轉換為分段段落，並儲存在 `passage_chunk` 欄位中。接著將 `passage_chunk` 欄位中的文字轉換為文字嵌入，並將嵌入儲存在 `passage_chunk_embedding` 欄位中：

```json
PUT _ingest/pipeline/text-chunking-embedding-ingest-pipeline
{
  "description": "A text chunking and embedding ingest pipeline",
  "processors": [
    {
      "text_chunking": {
        "algorithm": {
          "fixed_token_length": {
            "token_limit": 10,
            "overlap_rate": 0.2,
            "tokenizer": "standard"
          }
        },
        "field_map": {
          "passage_text": "passage_chunk"
        }
      }
    },
    {
      "sparse_encoding": {
        "model_id": "cCzQbZsBdDf9VgDzpyiR",
        "field_map": {
          "passage_chunk": "passage_chunk_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2：建立用於匯入的索引

若要使用資料匯入管線，您需要建立支援稀疏嵌入的索引。`passage_chunk_embedding` 欄位必須是 `nested` 類型。對於傳統的[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-search/)，`sparse_encoding` 欄位必須是 `rank_features` 類型：

```json
PUT /testindex
{
  "mappings": {
    "properties": {
      "passage_text": {
        "type": "text"
      },
      "passage_chunk_embedding": {
        "type": "nested",
        "properties": {
          "sparse_encoding": {
            "type": "rank_features"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

對於[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)，`index.sparse` 設定必須設為 `true`，且 `sparse_encoding` 欄位必須是 `sparse_vector` 類型：

```json
PUT /testindex
{
  "settings": {
    "index": {
      "sparse": true
    }
  },
  "mappings": {
    "properties": {
      "text": {
        "type": "text"
      },
      "passage_chunk_embedding": {
        "type": "nested",
        "properties": {
          "sparse_encoding": {
            "type": "sparse_vector",
            "method": {
              "name": "seismic",
              "parameters": {
                "approximate_threshold": 1
              }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 3：將文件匯入索引

若要將文件匯入上一個步驟中建立的索引，請傳送下列請求：

```json
POST testindex/_doc?pipeline=text-chunking-embedding-ingest-pipeline
{
  "passage_text": "This is an example document to be chunked. The document contains a single paragraph, two sentences and 24 tokens by standard tokenizer in OpenSearch."
}
```
{% include copy-curl.html %}

### 步驟 4：搜尋索引

您可以使用 `nested` 查詢對索引執行向量搜尋。我們建議將 `score_mode` 設為 `max`，如此文件分數會設為所有段落嵌入中的最高分數：

```json
GET /testindex/_search
{
  "query": {
    "nested": {
      "score_mode": "max",
      "path": "passage_chunk_embedding",
      "query": {
        "neural_sparse": {
          "passage_chunk_embedding.sparse_encoding": {
            "query_text": "document",
            "model_id": "LGv7bZsBtp4cObNZc6R6"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 後續步驟

- 探索我們的[教學]({{site.url}}{{site.baseurl}}/vector-search/tutorials/)，了解如何建置 AI 搜尋應用程式。 
