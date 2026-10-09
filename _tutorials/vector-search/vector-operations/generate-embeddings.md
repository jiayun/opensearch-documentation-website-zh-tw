---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "產生嵌入"
parent: Vector operations
grand_parent: Vector search
nav_order: 5
redirect_from:
  - /ml-commons-plugin/tutorials/generate-embeddings/
  - /vector-search/tutorials/vector-operations/generate-embeddings/
---

# 從物件陣列產生嵌入

本教學說明如何為物件陣列產生嵌入。如需更多資訊，請參閱[自動產生嵌入]({{site.url}}{{site.baseurl}}/vector-search/getting-started/auto-generated-embeddings/)。

請將開頭為前綴 `your_` 的預留位置取代為您自己的值。
{: .note}

## 步驟 1：註冊嵌入模型

在本教學中，您將使用託管於 Amazon Bedrock 的 [Amazon Titan Text Embeddings 模型](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)。

首先，請依照 [Amazon Bedrock Titan 藍圖範例](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/bedrock_connector_titan_embedding_blueprint.md) 註冊並部署模型。

測試模型，並提供模型 ID：

```json
POST /_plugins/_ml/models/your_embedding_model_id/_predict
{
    "parameters": {
        "inputText": "hello world"
    }
}
```
{% include copy-curl.html %}

回應包含推論結果：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "sentence_embedding",
          "data_type": "FLOAT32",
          "shape": [ 1536 ],
          "data": [0.7265625, -0.0703125, 0.34765625, ...]
        }
      ],
      "status_code": 200
    }
  ]
}
```

## 步驟 2：建立資料匯入管線

請依照下列步驟建立用於產生嵌入的資料匯入管線。

### 步驟 2.1：建立向量索引

首先，建立向量索引：

```json
PUT my_books
{
  "settings" : {
      "index.knn" : "true",
      "default_pipeline": "bedrock_embedding_pipeline"
  },
  "mappings": {
    "properties": {
      "books": {
        "type": "nested",
        "properties": {
          "title_embedding": {
            "type": "knn_vector",
            "dimension": 1536
          },
          "title": {
            "type": "text"
          },
          "description": {
            "type": "text"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 2.2：建立資料匯入管線

接著建立內部資料匯入管線，為單一陣列元素產生嵌入。

此管線包含三個處理器：

- `text_embedding` 處理器：將暫存欄位的值轉換為嵌入。

若要建立這類管線，請傳送下列請求：

```json
PUT _ingest/pipeline/bedrock_embedding_pipeline
{
  "processors": [
    {
      "text_embedding": {
        "model_id": "your_embedding_model_id",
        "field_map": {
          "books.title": "title_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2.3：模擬管線

首先，您將在包含兩個書籍物件的陣列上測試管線，這兩個物件都有 `title` 欄位：

```json
POST _ingest/pipeline/bedrock_embedding_pipeline/_simulate
{
  "docs": [
    {
      "_index": "my_books",
      "_id": "1",
      "_source": {
        "books": [
          {
            "title": "first book",
            "description": "This is first book"
          },
          {
            "title": "second book",
            "description": "This is second book"
          }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應包含兩個物件在其 `title_embedding` 欄位中產生的嵌入：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "my_books",
        "_id": "1",
        "_source": {
          "books": [
            {
              "title": "first book",
              "title_embedding": [-1.1015625, 0.65234375, 0.7578125, ...],
              "description": "This is first book"
            },
            {
              "title": "second book",
              "title_embedding": [-0.65234375, 0.21679688, 0.7265625, ...],
              "description": "This is second book"
            }
          ]
        },
        "_ingest": {
          "_value": null,
          "timestamp": "2024-05-28T16:16:50.538929413Z"
        }
      }
    }
  ]
}
```

接著，您將在包含兩個書籍物件的陣列上測試管線，其中一個有 `title` 欄位，另一個則沒有：

```json
POST _ingest/pipeline/bedrock_embedding_foreach_pipeline/_simulate
{
  "docs": [
    {
      "_index": "my_books",
      "_id": "1",
      "_source": {
        "books": [
          {
            "title": "first book",
            "description": "This is first book"
          },
          {
            "description": "This is second book"
          }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應包含含有 `title` 欄位之物件所產生的嵌入：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "my_books",
        "_id": "1",
        "_source": {
          "books": [
            {
              "title": "first book",
              "title_embedding": [-1.1015625, 0.65234375, 0.7578125, ...],
              "description": "This is first book"
            },
            {
              "description": "This is second book"
            }
          ]
        },
        "_ingest": {
          "_value": null,
          "timestamp": "2024-05-28T16:19:03.942644042Z"
        }
      }
    }
  ]
}
```
### 步驟 2.4：測試資料匯入

匯入一份文件：

```json
PUT my_books/_doc/1
{
  "books": [
    {
      "title": "first book",
      "description": "This is first book"
    },
    {
      "title": "second book",
      "description": "This is second book"
    }
  ]
}
```
{% include copy-curl.html %}

取得該文件：

```json
GET my_books/_doc/1
```
{% include copy-curl.html %}

回應包含產生的嵌入：

```json
{
  "_index": "my_books",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "books": [
      {
        "description": "This is first book",
        "title": "first book",
        "title_embedding": [-1.1015625, 0.65234375, 0.7578125, ...]
      },
      {
        "description": "This is second book",
        "title": "second book",
        "title_embedding": [-0.65234375, 0.21679688, 0.7265625, ...]
      }
    ]
  }
}      
```

您也可以大量匯入多份文件，並透過呼叫 Get Document API 來測試產生的嵌入：

```json
POST _bulk
{ "index" : { "_index" : "my_books" } }
{ "books" : [{"title": "first book", "description": "This is first book"}, {"title": "second book", "description": "This is second book"}] }
{ "index" : { "_index" : "my_books" } }
{ "books" : [{"title": "third book", "description": "This is third book"}, {"description": "This is fourth book"}] }
```
{% include copy-curl.html %}
