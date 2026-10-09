---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用位元組向量的語意搜尋"
parent: Vector operations
grand_parent: Vector search
nav_order: 10
redirect_from:
  - /ml-commons-plugin/tutorials/semantic-search-byte-vectors/
  - /vector-search/tutorials/vector-operations/semantic-search-byte-vectors/
---

# 使用位元組量化向量的語意搜尋

本教學說明如何使用 [Cohere Embed 模型](https://docs.cohere.com/reference/embed)與位元組量化向量建立語意搜尋。如需使用位元組量化向量的更多資訊，請參閱 [位元組向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#byte-vectors) 與 [語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/semantic-search/)。

Cohere Embed v3 模型支援數種 `embedding_types`。在本教學中，您將使用 `INT8` 類型來編碼位元組量化向量。

Cohere Embed v3 模型支援數種輸入類型。本教學使用下列輸入類型：

- `search_document`：當您有想要儲存在向量資料庫中的文字（以文件形式）時，請使用此輸入類型。
- `search_query`：當您在結構化搜尋查詢以找出向量資料庫中最相關的文件時，請使用此輸入類型。

如需輸入類型的更多資訊，請參閱 [Cohere 文件](https://docs.cohere.com/docs/embed-api#the-input_type-parameter)。

在本教學中，您將建立兩個模型：

- 一個用於匯入的模型，其 `input_type` 為 `search_document`
- 一個用於搜尋的模型，其 `input_type` 為 `search_query`

請將以 `your_` 為前綴的預留位置替換為您自己的值。
{: .note}

## 步驟 1：建立用於匯入的嵌入模型

為 Cohere 模型建立連接器，並指定 `search_document` 輸入類型：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "Cohere embedding connector with int8 embedding type for ingestion",
    "description": "Test connector for Cohere embedding model",
    "version": 1,
    "protocol": "http",
    "credential": {
        "cohere_key": "your_cohere_api_key"
    },
    "parameters": {
        "model": "embed-english-v3.0",
        "embedding_types": ["int8"],
        "input_type": "search_document"
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${credential.cohere_key}",
                "Request-Source": "unspecified:opensearch"
            },
            "url": "https://api.cohere.ai/v1/embed",
            "request_body": "{ \"model\": \"${parameters.model}\", \"texts\": ${parameters.texts}, \"input_type\":\"${parameters.input_type}\", \"embedding_types\": ${parameters.embedding_types} }",
            "pre_process_function": "connector.pre_process.cohere.embedding",
            "post_process_function": "\n    def name = \"sentence_embedding\";\n    def data_type = \"FLOAT32\";\n    def result;\n    if (params.embeddings.int8 != null) {\n      data_type = \"INT8\";\n      result = params.embeddings.int8;\n    } else if (params.embeddings.uint8 != null) {\n      data_type = \"UINT8\";\n      result = params.embeddings.uint8;\n    } else if (params.embeddings.float != null) {\n      data_type = \"FLOAT32\";\n      result = params.embeddings.float;\n    }\n    \n    if (result == null) {\n      return \"Invalid embedding result\";\n    }\n    \n    def embedding_list = new StringBuilder(\"[\");\n    \n    for (int m=0; m<result.length; m++) {\n      def embedding_size = result[m].length;\n      def embedding = new StringBuilder(\"[\");\n      def shape = [embedding_size];\n      for (int i=0; i<embedding_size; i++) {\n        def val;\n        if (\"FLOAT32\".equals(data_type)) {\n          val = result[m][i].floatValue();\n        } else if (\"INT8\".equals(data_type) || \"UINT8\".equals(data_type)) {\n          val = result[m][i].intValue();\n        }\n        embedding.append(val);\n        if (i < embedding_size - 1) {\n          embedding.append(\",\");  \n        }\n      }\n      embedding.append(\"]\");  \n      \n      // workaround for compatible with neural-search\n      def dummy_data_type = 'FLOAT32';\n      \n      def json = '{' +\n                   '\"name\":\"' + name + '\",' +\n                   '\"data_type\":\"' + dummy_data_type + '\",' +\n                   '\"shape\":' + shape + ',' +\n                   '\"data\":' + embedding +\n                   '}';\n      embedding_list.append(json);\n      if (m < result.length - 1) {\n        embedding_list.append(\",\");  \n      }\n    }\n    embedding_list.append(\"]\");  \n    return embedding_list.toString();\n    "
        }
    ]
}
```
{% include copy-curl.html %}

為確保與 OpenSearch 相容，`data_type`（在回應的 `inference_results.output.data_type` 欄位中輸出）必須在後處理函式中設為 `FLOAT32`，即使實際的嵌入類型將是 `INT8`。
{: .important}

請記下回應中的連接器 ID；您將用它來註冊模型。

註冊模型，並提供其連接器 ID：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "Cohere embedding model for INT8 with search_document input type",
    "function_name": "remote",
    "description": "test model",
    "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

請記下回應中的模型 ID；您將在後續步驟中使用它。

測試模型，並提供模型 ID：

```json
POST /_plugins/_ml/models/your_embedding_model_id/_predict
{
    "parameters": {
        "texts": ["hello", "goodbye"]
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
                    "shape": [
                        1024
                    ],
                    "data": [
                        20,
                        -11,
                        -60,
                        -91,
                        ...
                    ]
                },
                {
                    "name": "sentence_embedding",
                    "data_type": "FLOAT32",
                    "shape": [
                        1024
                    ],
                    "data": [
                        58,
                        -30,
                        9,
                        -51,
                        ...
                    ]
                }
            ],
            "status_code": 200
        }
    ]
}
```

## 步驟 2：匯入資料

首先，建立資料匯入管線：

```json
PUT /_ingest/pipeline/pipeline-cohere
{
  "description": "Cohere embedding ingest pipeline",
  "processors": [
    {
      "text_embedding": {
        "model_id": "your_embedding_model_id_created_in_step1",
        "field_map": {
          "passage_text": "passage_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

接著，建立向量索引，並將 `passage_embedding` 欄位的 `data_type` 設為 `byte`，以便儲存位元組量化向量：

```json
PUT my_test_data
{
  "settings": {
    "index": {
      "knn": true,
      "knn.algo_param.ef_search": 100,
      "default_pipeline": "pipeline-cohere"
    }
  },
  "mappings": {
    "properties": {
      "passage_text": {
        "type": "text"
      },
      "passage_embedding": {
        "type": "knn_vector",
        "dimension": 1024,
        "data_type": "byte",
        "method": {
          "name": "hnsw",
          "space_type": "l2",
          "engine": "lucene",
          "parameters": {
            "ef_construction": 128,
            "m": 24
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

最後，匯入測試資料：

```json
POST _bulk
{ "index" : { "_index" : "my_test_data" } }
{ "passage_text" : "OpenSearch is the flexible, scalable, open-source way to build solutions for data-intensive applications. Explore, enrich, and visualize your data with built-in performance, developer-friendly tools, and powerful integrations for machine learning, data processing, and more." }
{ "index" : { "_index" : "my_test_data"} }
{ "passage_text" : "BM25 is a keyword-based algorithm that performs well on queries containing keywords but fails to capture the semantic meaning of the query terms. Semantic search, unlike keyword-based search, takes into account the meaning of the query in the search context. Thus, semantic search performs well when a query requires natural language understanding." }
```
{% include copy-curl.html %}

## 步驟 3：設定語意搜尋

建立一個連接至嵌入模型的連接器，並使用 `search_query` 輸入類型：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "Cohere embedding connector with int8 embedding type for search",
    "description": "Test connector for Cohere embedding model. Use this connector for search.",
    "version": 1,
    "protocol": "http",
    "credential": {
        "cohere_key": "your_cohere_api_key"
    },
    "parameters": {
        "model": "embed-english-v3.0",
        "embedding_types": ["int8"],
        "input_type": "search_query"
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${credential.cohere_key}",
                "Request-Source": "unspecified:opensearch"
            },
            "url": "https://api.cohere.ai/v1/embed",
            "request_body": "{ \"model\": \"${parameters.model}\", \"texts\": ${parameters.texts}, \"input_type\":\"${parameters.input_type}\", \"embedding_types\": ${parameters.embedding_types} }",
            "pre_process_function": "connector.pre_process.cohere.embedding",
            "post_process_function": "\n    def name = \"sentence_embedding\";\n    def data_type = \"FLOAT32\";\n    def result;\n    if (params.embeddings.int8 != null) {\n      data_type = \"INT8\";\n      result = params.embeddings.int8;\n    } else if (params.embeddings.uint8 != null) {\n      data_type = \"UINT8\";\n      result = params.embeddings.uint8;\n    } else if (params.embeddings.float != null) {\n      data_type = \"FLOAT32\";\n      result = params.embeddings.float;\n    }\n    \n    if (result == null) {\n      return \"Invalid embedding result\";\n    }\n    \n    def embedding_list = new StringBuilder(\"[\");\n    \n    for (int m=0; m<result.length; m++) {\n      def embedding_size = result[m].length;\n      def embedding = new StringBuilder(\"[\");\n      def shape = [embedding_size];\n      for (int i=0; i<embedding_size; i++) {\n        def val;\n        if (\"FLOAT32\".equals(data_type)) {\n          val = result[m][i].floatValue();\n        } else if (\"INT8\".equals(data_type) || \"UINT8\".equals(data_type)) {\n          val = result[m][i].intValue();\n        }\n        embedding.append(val);\n        if (i < embedding_size - 1) {\n          embedding.append(\",\");  \n        }\n      }\n      embedding.append(\"]\");  \n      \n      // workaround for compatible with neural-search\n      def dummy_data_type = 'FLOAT32';\n      \n      def json = '{' +\n                   '\"name\":\"' + name + '\",' +\n                   '\"data_type\":\"' + dummy_data_type + '\",' +\n                   '\"shape\":' + shape + ',' +\n                   '\"data\":' + embedding +\n                   '}';\n      embedding_list.append(json);\n      if (m < result.length - 1) {\n        embedding_list.append(\",\");  \n      }\n    }\n    embedding_list.append(\"]\");  \n    return embedding_list.toString();\n    "
        }
    ]
}
```
{% include copy-curl.html %}

請記下回應中的連接器 ID；您將使用它來註冊模型。

註冊模型，並提供其連接器 ID：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "Cohere embedding model for INT8 with search_document input type",
    "function_name": "remote",
    "description": "test model",
    "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

請記下回應中的模型 ID；您將使用它來執行查詢。

執行向量搜尋，並提供模型 ID：

```json
POST /my_test_data/_search
{
  "query": {
    "neural": {
      "passage_embedding": {
        "query_text": "semantic search",
        "model_id": "your_embedding_model_id",
        "k": 100
      }
    }
  },
  "size": "1",
  "_source": ["passage_text"]
}
```
{% include copy-curl.html %}

回應中包含查詢結果：

```json
{
  "took": 143,
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
    "max_score": 9.345969e-7,
    "hits": [
      {
        "_index": "my_test_data",
        "_id": "_IXCuY0BJr_OiKWden7i",
        "_score": 9.345969e-7,
        "_source": {
          "passage_text": "BM25 is a keyword-based algorithm that performs well on queries containing keywords but fails to capture the semantic meaning of the query terms. Semantic search, unlike keyword-based search, takes into account the meaning of the query in the search context. Thus, semantic search performs well when a query requires natural language understanding."
        }
      }
    ]
  }
}
```