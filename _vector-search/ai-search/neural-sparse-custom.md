---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用自訂組態進行神經稀疏搜尋"
parent: Neural sparse search
grand_parent: AI search
nav_order: 20
has_children: false
---

# 使用自訂組態進行神經稀疏搜尋

使用自動產生的向量嵌入的神經稀疏搜尋有兩種模式：僅文件 (doc-only) 與雙編碼器 (bi-encoder)。如需更多資訊，請參閱[自動產生稀疏向量嵌入]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-with-pipelines/)。

查詢時，您可以透過下列方式使用自訂模型：

- **雙編碼器模式**：使用您部署的稀疏編碼模型，從查詢文字產生嵌入。這必須與您在匯入時使用的模型相同。

- **搭配自訂斷詞器的僅文件模式**：使用您部署的斷詞器模型，對查詢文字進行斷詞。詞元權重取自預先計算的查閱表。

以下是在神經稀疏搜尋中使用自訂模型的完整範例。

## 步驟 1：設定稀疏編碼模型/斷詞器

使用雙編碼器模式以及搭配自訂斷詞器的僅文件模式時，您都必須設定用於匯入的稀疏編碼模型。雙編碼器模式在搜尋時使用相同的模型；僅文件模式在搜尋時使用個別的斷詞器。

### 步驟 1(a)：選擇搜尋模式

選擇搜尋模式以及適當的模型/斷詞器組合：

- **雙編碼器**：在匯入與搜尋期間都使用 `amazon/neural-sparse/opensearch-neural-sparse-encoding-v2-distill` 模型。

- **搭配自訂斷詞器的僅文件模式**：在匯入期間使用 `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-distill` 模型，並在搜尋期間使用 `amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1` 斷詞器。

下表提供兩種搜尋模式所有可用組合的搜尋相關性比較，讓您可以為您的使用案例選擇最佳組合。

#### 英文語言模型

| 模式      | 匯入模型                                               | 搜尋模型                                                  | BEIR 上的平均搜尋相關性 | 模型參數 |
|-----------|---------------------------------------------------------------|---------------------------------------------------------------|------------------------------|------------------|
| 僅文件  | `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v1` | `amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1`    | 0.49                         | 133M             |
| 僅文件  | `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v2-distill` | `amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1`    | 0.504                         | 67M             |
| 僅文件  | `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v2-mini` | `amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1`    | 0.497                         | 23M             |
| 僅文件  | `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-distill` | `amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1`    | 0.517                         | 67M             |
| 僅文件  | `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-gte` | `amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1`    | 0.546                         | 133M             |
| 雙編碼器| `amazon/neural-sparse/opensearch-neural-sparse-encoding-v1`     | `amazon/neural-sparse/opensearch-neural-sparse-encoding-v1`     | 0.524                        | 133M             |
| 雙編碼器| `amazon/neural-sparse/opensearch-neural-sparse-encoding-v2-distill`     | `amazon/neural-sparse/opensearch-neural-sparse-encoding-v2-distill`     | 0.528                        | 67M             |

#### 多語言模型

| 模式      | 匯入模型                                               | 搜尋模型                                                  | MIRACL 上的平均搜尋相關性 | 模型參數 |
|-----------|---------------------------------------------------------------|---------------------------------------------------------------|------------------------------|------------------|
| 僅文件  | `amazon/neural-sparse/opensearch-neural-sparse-encoding-multilingual-v1` | `amazon/neural-sparse/opensearch-neural-sparse-tokenizer-multilingual-v1`    | 0.629                         | 168M             |

### 步驟 1(b)：註冊模型/斷詞器

兩種模式都請註冊稀疏編碼模型。若使用搭配自訂斷詞器的僅文件模式，請在稀疏編碼模型之外另外註冊自訂斷詞器。

#### 雙編碼器模式

使用雙編碼器模式時，您只需要註冊 `amazon/neural-sparse/opensearch-neural-sparse-encoding-v2-distill` 模型。

註冊稀疏編碼模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "amazon/neural-sparse/opensearch-neural-sparse-encoding-v2-distill",
  "version": "1.0.0",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

註冊模型是非同步工作。OpenSearch 會為您註冊的每個模型傳回一個工作 ID：

```json
{
  "task_id": "aFeif4oB5Vm0Tdw8yoN7",
  "status": "CREATED"
}
```

您可以呼叫 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 來檢查工作狀態：

```json
GET /_plugins/_ml/tasks/aFeif4oB5Vm0Tdw8yoN7
```
{% include copy-curl.html %}

工作完成後，工作狀態會變成 `COMPLETED`，而 ML Tasks API 回應會包含已註冊模型的模型 ID：

```json
{
  "model_id": "<bi-encoder model ID>",
  "task_type": "REGISTER_MODEL",
  "function_name": "SPARSE_ENCODING",
  "state": "COMPLETED",
  "worker_node": [
    "4p6FVOmJRtu3wehDD74hzQ"
  ],
  "create_time": 1694358489722,
  "last_update_time": 1694358499139,
  "is_async": true
}
```

請記下您所建立模型的 `model_id`；後續步驟會用到。

#### 搭配自訂斷詞器的僅文件模式

使用搭配自訂斷詞器的僅文件模式時，您需要註冊匯入時要使用的 `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-distill` 模型，以及搜尋時要使用的 `amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1` 斷詞器。

註冊稀疏編碼模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-distill",
  "version": "1.0.0",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

註冊斷詞器：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1",
  "version": "1.0.1",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

與雙編碼器模式相同，請使用 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 檢查註冊工作的狀態。ML Tasks API 傳回後，工作狀態會變成 `COMPLETED`。請記下您所建立模型與斷詞器的 `model_id`；後續步驟會用到。

## 步驟 2：匯入資料

在雙編碼器與僅文件兩種模式中，您都會在匯入時使用稀疏編碼模型來產生稀疏向量嵌入。

### 步驟 2(a)：建立資料匯入管線

若要產生稀疏向量嵌入，您需要建立一個包含 [`sparse_encoding` 處理器]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/processors/sparse-encoding/) 的[資料匯入管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/)，該處理器會將文件欄位中的文字轉換為向量嵌入。處理器的 `field_map` 決定要從哪些輸入欄位產生向量嵌入，以及要將嵌入儲存在哪些輸出欄位。

下列範例請求會建立一個資料匯入管線，其中 `passage_text` 的文字將被轉換為稀疏向量嵌入，並儲存在 `passage_embedding` 中。請在請求中提供已註冊模型的模型 ID：

```json
PUT /_ingest/pipeline/nlp-ingest-pipeline-sparse
{
  "description": "An sparse encoding ingest pipeline",
  "processors": [
    {
      "sparse_encoding": {
        "model_id": "<bi-encoder or doc-only model ID>",
        "prune_type": "max_ratio",
        "prune_ratio": 0.1,
        "field_map": {
          "passage_text": "passage_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

若要將長文字分割成段落，請在 `sparse_encoding` 處理器之前使用 `text_chunking` 資料匯入處理器。如需更多資訊，請參閱 [文字分塊]({{site.url}}{{site.baseurl}}/search-plugins/text-chunking/)。

### 步驟 2(b)：建立用於匯入的索引

若要使用管線中定義的稀疏編碼處理器，請建立一個 rank features 索引，並將上一步建立的管線新增為預設管線。請確保 `field_map` 中定義的欄位已對應為正確的類型。延續前述範例，`passage_embedding` 欄位必須對應為 [`rank_features`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/rank/#rank-features)。同樣地，`passage_text` 欄位必須對應為 `text`。

下列範例請求會建立一個設定了預設資料匯入管線的 rank features 索引：

```json
PUT /my-nlp-index
{
  "settings": {
    "default_pipeline": "nlp-ingest-pipeline-sparse"
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "text"
      },
      "passage_embedding": {
        "type": "rank_features"
      },
      "passage_text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

若要節省磁碟空間，您可以依照下列方式將嵌入向量從來源中排除：

```json
PUT /my-nlp-index
{
  "settings": {
    "default_pipeline": "nlp-ingest-pipeline-sparse"
  },
  "mappings": {
    "_source": {
      "excludes": [
        "passage_embedding"
      ]
    },
    "properties": {
      "id": {
        "type": "text"
      },
      "passage_embedding": {
        "type": "rank_features"
      },
      "passage_text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

一旦 `<token, weight>` 配對從來源中排除，就無法復原。在套用此最佳化之前，請確認您的應用程式不需要 `<token, weight>` 配對。
{: .important}

### 步驟 2(c)：將文件匯入索引

若要將文件匯入上一步建立的索引，請傳送下列請求：

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

在文件匯入索引之前，資料匯入管線會對文件執行 `sparse_encoding` 處理器，為 `passage_text` 欄位產生向量嵌入。編製索引後的文件包含 `passage_text` 欄位（其中包含原始文字）以及 `passage_embedding` 欄位（其中包含向量嵌入）。

## 步驟 3：搜尋資料

若要對索引執行神經稀疏搜尋，請在 [Query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/index/) 查詢中使用 `neural_sparse` 查詢子句。

下列範例請求使用 `neural_sparse` 查詢，以原始文字查詢搜尋相關文件。請提供 bi-encoder 模式的模型 ID，或自訂斷詞器的 doc-only 模式的斷詞器 ID：

```json
GET my-nlp-index/_search
{
  "query": {
    "neural_sparse": {
      "passage_embedding": {
        "query_text": "Hi world",
        "model_id": "<bi-encoder or tokenizer ID>"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的文件：

```json
{
  "took" : 688,
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
    "max_score" : 30.0029,
    "hits" : [
      {
        "_index" : "my-nlp-index",
        "_id" : "1",
        "_score" : 30.0029,
        "_source" : {
          "passage_text" : "Hello world",
          "passage_embedding" : {
            "!" : 0.8708904,
            "door" : 0.8587369,
            "hi" : 2.3929274,
            "worlds" : 2.7839446,
            "yes" : 0.75845814,
            "##world" : 2.5432441,
            "born" : 0.2682308,
            "nothing" : 0.8625516,
            "goodbye" : 0.17146169,
            "greeting" : 0.96817183,
            "birth" : 1.2788506,
            "come" : 0.1623208,
            "global" : 0.4371151,
            "it" : 0.42951578,
            "life" : 1.5750692,
            "thanks" : 0.26481047,
            "world" : 4.7300377,
            "tiny" : 0.5462298,
            "earth" : 2.6555297,
            "universe" : 2.0308156,
            "worldwide" : 1.3903781,
            "hello" : 6.696973,
            "so" : 0.20279501,
            "?" : 0.67785245
          },
          "id" : "s1"
        }
      },
      {
        "_index" : "my-nlp-index",
        "_id" : "2",
        "_score" : 16.480486,
        "_source" : {
          "passage_text" : "Hi planet",
          "passage_embedding" : {
            "hi" : 4.338913,
            "planets" : 2.7755864,
            "planet" : 5.0969057,
            "mars" : 1.7405145,
            "earth" : 2.6087382,
            "hello" : 3.3210192
          },
          "id" : "s2"
        }
      }
    ]
  }
}
```

## 設定搜尋的預設模型

使用自訂模型時，您可以在索引層級設定預設模型 ID，以簡化查詢。這樣就不需要在每個查詢中指定 `model_id`。

首先，建立一個包含 [`neural_query_enricher`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/neural-query-enricher/) 處理器的搜尋管線：

```json
PUT /_search/pipeline/neural_search_pipeline
{
  "request_processors": [
    {
      "neural_query_enricher" : {
        "default_model_id": "<bi-encoder model/tokenizer ID>"
      }
    }
  ]
}
```
{% include copy-curl.html %}

然後將此管線設定為索引的預設管線：

```json
PUT /my-nlp-index/_settings 
{
  "index.search.default_pipeline" : "neural_search_pipeline"
}
```
{% include copy-curl.html %}

設定預設模型後，您在執行查詢時即可省略 `model_id`。

如需更多關於在索引上設定預設模型的資訊，或想了解如何在特定欄位上設定預設模型，請參閱 [在索引或欄位上設定預設模型]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/#setting-a-default-model-on-an-index-or-field)。

## 後續步驟

- 瀏覽我們的[教學]({{site.url}}{{site.baseurl}}/vector-search/tutorials/)，了解如何建置 AI 搜尋應用程式。 
