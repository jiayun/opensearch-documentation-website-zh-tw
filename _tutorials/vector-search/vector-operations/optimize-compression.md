---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Cohere 壓縮嵌入最佳化向量搜尋"
parent: Vector operations
grand_parent: Vector search
nav_order: 20
redirect_from:
  - /vector-search/tutorials/vector-operations/optimize-compression/
---

# 使用 Cohere 壓縮嵌入最佳化向量搜尋

本教學說明如何使用 Cohere 壓縮嵌入來最佳化向量搜尋。這些嵌入可讓向量表示更有效率地儲存並更快速地擷取，使其非常適合大規模搜尋應用程式。

本教學與 2.17 版及更新版本相容，但 [步驟 4：搜尋索引](#step-4-search-the-index) 中的 [使用範本查詢與搜尋管線](#using-a-template-query-and-a-search-pipeline) 除外，該功能需要 2.19 版或更新版本。

本教學使用 Amazon Bedrock 上的 Cohere Embed Multilingual v3 模型。如需在 Amazon Bedrock 上使用 Cohere 壓縮嵌入的詳細資訊，請參閱[這篇部落格文章](https://aws.amazon.com/about-aws/whats-new/2024/06/amazon-bedrock-compressed-embeddings-cohere-embed/)。

在本教學中，您將使用下列 OpenSearch 元件：
- [ML 推論資料匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/ml-inference/) 
- [ML 推論搜尋請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/ml-inference-search-request/)
- [搜尋範本查詢]({{site.url}}{{site.baseurl}}/api-reference/search-template/) 
- [向量索引]({{site.url}}{{site.baseurl}}/search-plugins/knn/index/) 與 [位元組向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#byte-vectors)

請將開頭為前置詞 `your_` 的預留位置取代為您自己的值。
{: .note}

## 步驟 1：設定嵌入模型

請依照下列步驟建立連接至 Amazon Bedrock 的連接器，以存取 Cohere Embed 模型。

### 步驟 1.1：建立連接器

使用[此藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/bedrock_connector_cohere_cohere.embed-multilingual-v3_blueprint.md)為嵌入模型建立連接器。如需建立連接器的詳細資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

由於您將在本教學中使用 [ML 推論處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/ml-inference/)，因此不需要在連接器中指定前處理或後處理函式。
{: .note}

若要建立連接器，請傳送下列請求。`"embedding_types": ["int8"]` 參數會指定來自 Cohere 模型的 8 位元整數量化嵌入。此設定會將嵌入從 32 位元浮點數壓縮為 8 位元整數，減少儲存空間並提升運算速度。雖然精確度會略微降低，但對搜尋工作而言通常可忽略不計。這些量化嵌入與 OpenSearch 支援位元組向量的 `knn_index` 相容：

```json
POST _plugins/_ml/connectors/_create
{
  "name": "Amazon Bedrock Connector: Cohere embed-multilingual-v3",
  "description": "Test connector for Amazon Bedrock Cohere embed-multilingual-v3",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "access_key": "your_aws_access_key",
    "secret_key": "your_aws_secret_key",
    "session_token": "your_aws_session_token"
  },
  "parameters": {
    "region": "your_aws_region",
    "service_name": "bedrock",
    "truncate": "END",
    "input_type": "search_document",
    "model": "cohere.embed-multilingual-v3",
    "embedding_types": ["int8"]
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "headers": {
        "x-amz-content-sha256": "required",
        "content-type": "application/json"
      },
      "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/invoke",
      "request_body": "{ \"texts\": ${parameters.texts}, \"truncate\": \"${parameters.truncate}\", \"input_type\": \"${parameters.input_type}\", \"embedding_types\":  ${parameters.embedding_types} }"

    }
  ]
}
```
{% include copy-curl.html %}

如需模型參數的詳細資訊，請參閱 [Cohere 文件](https://docs.cohere.com/v2/docs/embeddings)與 [Amazon Bedrock 文件](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-embed.html)

回應中包含連接器 ID：

```json
{
  "connector_id": "AOP0OZUB3JwAtE25PST0"
}
```

請記下連接器 ID；您將在下一步中使用它。

### 步驟 1.2：註冊模型

接著，使用您在上一步建立的連接器註冊模型。`interface` 參數為選用。如果模型不需要特定的介面組態，請將此參數設為空物件：`"interface": {}`：

```json
POST _plugins/_ml/models/_register?deploy=true
{
  "name": "Bedrock Cohere embed-multilingual-v3",
  "version": "1.0",
  "function_name": "remote",
  "description": "Bedrock Cohere embed-multilingual-v3",
  "connector_id": "AOP0OZUB3JwAtE25PST0",
  "interface": {
    "input": "{\n    \"type\": \"object\",\n    \"properties\": {\n        \"parameters\": {\n            \"type\": \"object\",\n            \"properties\": {\n                \"texts\": {\n                    \"type\": \"array\",\n                    \"items\": {\n                        \"type\": \"string\"\n                    }\n                },\n                \"embedding_types\": {\n                    \"type\": \"array\",\n                    \"items\": {\n                        \"type\": \"string\",\n                        \"enum\": [\"float\", \"int8\", \"uint8\", \"binary\", \"ubinary\"]\n                    }\n                },\n                \"truncate\": {\n                    \"type\": \"array\",\n                    \"items\": {\n                        \"type\": \"string\",\n                        \"enum\": [\"NONE\", \"START\", \"END\"]\n                    }\n                },\n                \"input_type\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"search_document\", \"search_query\", \"classification\", \"clustering\"]\n                }\n            },\n            \"required\": [\"texts\"]\n        }\n    },\n    \"required\": [\"parameters\"]\n}",
    "output": "{\n    \"type\": \"object\",\n    \"properties\": {\n        \"inference_results\": {\n            \"type\": \"array\",\n            \"items\": {\n                \"type\": \"object\",\n                \"properties\": {\n                    \"output\": {\n                        \"type\": \"array\",\n                        \"items\": {\n                            \"type\": \"object\",\n                            \"properties\": {\n                                \"name\": {\n                                    \"type\": \"string\"\n                                },\n                                \"dataAsMap\": {\n                                    \"type\": \"object\",\n                                    \"properties\": {\n                                        \"id\": {\n                                            \"type\": \"string\",\n                                            \"format\": \"uuid\"\n                                        },\n                                        \"texts\": {\n                                            \"type\": \"array\",\n                                            \"items\": {\n                                                \"type\": \"string\"\n                                            }\n                                        },\n                                        \"embeddings\": {\n                                            \"type\": \"object\",\n                                            \"properties\": {\n                                                \"binary\": {\n                                                    \"type\": \"array\",\n                                                    \"items\": {\n                                                        \"type\": \"array\",\n                                                        \"items\": {\n                                                            \"type\": \"number\"\n                                                        }\n                                                    }\n                                                },\n                                                \"float\": {\n                                                    \"type\": \"array\",\n                                                    \"items\": {\n                                                        \"type\": \"array\",\n                                                        \"items\": {\n                                                            \"type\": \"number\"\n                                                        }\n                                                    }\n                                                },\n                                                \"int8\": {\n                                                    \"type\": \"array\",\n                                                    \"items\": {\n                                                        \"type\": \"array\",\n                                                        \"items\": {\n                                                            \"type\": \"number\"\n                                                        }\n                                                    }\n                                                },\n                                                \"ubinary\": {\n                                                    \"type\": \"array\",\n                                                    \"items\": {\n                                                        \"type\": \"array\",\n                                                        \"items\": {\n                                                            \"type\": \"number\"\n                                                        }\n                                                    }\n                                                },\n                                                \"uint8\": {\n                                                    \"type\": \"array\",\n                                                    \"items\": {\n                                                        \"type\": \"array\",\n                                                        \"items\": {\n                                                            \"type\": \"number\"\n                                                        }\n                                                    }\n                                                }\n                                            }\n                                        },\n                                        \"response_type\": {\n                                            \"type\": \"string\"\n                                        }\n                                    },\n                                    \"required\": [\"embeddings\"]\n                                }\n                            },\n                            \"required\": [\"name\", \"dataAsMap\"]\n                        }\n                    },\n                    \"status_code\": {\n                        \"type\": \"integer\"\n                    }\n                },\n                \"required\": [\"output\", \"status_code\"]\n            }\n        }\n    },\n    \"required\": [\"inference_results\"]\n}"
  }
}
```
{% include copy-curl.html %}

如需詳細資訊，請參閱[模型介面文件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/#the-interface-parameter)

回應中包含模型 ID：

```json
{
  "task_id": "COP0OZUB3JwAtE25yiQr",
  "status": "CREATED",
  "model_id": "t64OPpUBX2k07okSZc2n"
}
```

若要測試模型，請傳送下列請求：

```json
POST _plugins/_ml/models/t64OPpUBX2k07okSZc2n/_predict
{
  "parameters": {
    "texts": ["Say this is a test"],
    "embedding_types": [ "int8" ]
  }
}
```
{% include copy-curl.html %}

回應包含產生的嵌入：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "id": "db07a08c-283d-4da5-b0c5-a9a54ef35d01",
            "texts": [
              "Say this is a test"
            ],
            "embeddings": {
              "int8": [
                [
                  -26.0,
                  31.0,
                  ...
                ]
              ]
            },
            "response_type": "embeddings_by_type"
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

## 步驟 2：建立資料匯入管線

資料匯入管線可讓您在將文件編製索引之前處理文件。在此案例中，您將使用資料匯入管線，為資料中的 `title` 和 `description` 欄位產生嵌入。

設定管線有兩種方式：

1. [分別為 `title` 和 `description` 呼叫模型](#option-1-invoke-the-model-separately-for-title-and-description)：此選項會針對每個欄位傳送個別請求，產生獨立的嵌入。
1. [合併 `title` 和 `description`，只呼叫模型一次](#option-2-invoke-the-model-once-by-combining-title-and-description)：此選項會將欄位串接成單一輸入並傳送一個請求，產生代表這兩個欄位的單一嵌入。

### 選項 1：分別為 `title` 和 `description` 呼叫模型

```json
PUT _ingest/pipeline/ml_inference_pipeline_cohere
{
"processors": [
    {
    "ml_inference": {
        "tag": "ml_inference",
        "description": "This processor is going to run ml inference during ingest request",
        "model_id": "t64OPpUBX2k07okSZc2n",
        "input_map": [
        {
            "texts": "$..title"
        },
        {
            "texts": "$..description"
        }
        ],
        "output_map": [
        {
            "title_embedding": "embeddings.int8[0]"
        },
        {
            "description_embedding": "embeddings.int8[0]"
        }
        ],
        "model_config": {
        "embedding_types": ["int8"]
        },
        "ignore_failure": false
    }
    }
]
}
```
{% include copy-curl.html %}
    
### 選項 2：合併 `title` 和 `description`，只呼叫模型一次

```json
PUT _ingest/pipeline/ml_inference_pipeline_cohere
{
    "description": "Concatenate title and description fields",
    "processors": [
        {
        "set": {
            "field": "title_desc_tmp",
            "value": [
            "{{title}}",
            "{{description}}"
            ]
        }
        },
        {
        "ml_inference": {
            "tag": "ml_inference",
            "description": "This processor is going to run ml inference during ingest request",
            "model_id": "t64OPpUBX2k07okSZc2n",
            "input_map": [
            {
                "texts": "title_desc_tmp"
            }
            ],
            "output_map": [
            {
                "title_embedding": "embeddings.int8[0]",
                "description_embedding": "embeddings.int8[1]"
            }
            ],
            "model_config": {
            "embedding_types": ["int8"]
            },
            "ignore_failure": true
        }
        },
        {
        "remove": {
            "field": "title_desc_tmp"
        }
        }
    ]
}
```
{% include copy-curl.html %}

傳送下列 [simulate]({{site.url}}{{site.baseurl}}/ingest-pipelines/simulate-ingest/) 請求來測試管線：

```json
POST _ingest/pipeline/ml_inference_pipeline_cohere/_simulate
{
  "docs": [
    {
      "_index": "books",
      "_id": "1",
      "_source": {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "description": "A novel of decadence and excess in the Jazz Age, exploring themes of wealth, love, and the American Dream.",
        "publication_year": 1925,
        "genre": "Classic Fiction"
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應包含產生的嵌入：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "books",
        "_id": "1",
        "_source": {
          "publication_year": 1925,
          "author": "F. Scott Fitzgerald",
          "genre": "Classic Fiction",
          "description": "A novel of decadence and excess in the Jazz Age, exploring themes of wealth, love, and the American Dream.",
          "title": "The Great Gatsby",
          "title_embedding": [
            18,
            33,
            ...
          ],
          "description_embedding": [
            -21,
            -14,
            ...
          ]
        },
        "_ingest": {
          "timestamp": "2025-02-25T09:11:32.192125042Z"
        }
      }
    }
  ]
}
```

## 步驟 3：建立向量索引並匯入資料

接著，建立向量索引：

```json
PUT books
{
  "settings": {
    "index": {
      "default_pipeline": "ml_inference_pipeline_cohere",
      "knn": true,
      "knn.algo_param.ef_search": 100
    }
  },
  "mappings": {
    "properties": {
      "title_embedding": {
        "type": "knn_vector",
        "dimension": 1024,
        "data_type": "byte",
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "lucene",
          "parameters": {
            "ef_construction": 100,
            "m": 16
          }
        }
      },
      "description_embedding": {
        "type": "knn_vector",
        "dimension": 1024,
        "data_type": "byte",
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "lucene",
          "parameters": {
            "ef_construction": 100,
            "m": 16
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

將測試資料匯入索引：

```json
POST _bulk
{"index":{"_index":"books"}}
{"title":"The Great Gatsby","author":"F. Scott Fitzgerald","description":"A novel of decadence and excess in the Jazz Age, exploring themes of wealth, love, and the American Dream.","publication_year":1925,"genre":"Classic Fiction"}
{"index":{"_index":"books"}}
{"title":"To Kill a Mockingbird","author":"Harper Lee","description":"A powerful story of racial injustice and loss of innocence in the American South during the Great Depression.","publication_year":1960,"genre":"Literary Fiction"}
{"index":{"_index":"books"}}
{"title":"Pride and Prejudice","author":"Jane Austen","description":"A romantic novel of manners that follows the character development of Elizabeth Bennet as she learns about the repercussions of hasty judgments and comes to appreciate the difference between superficial goodness and actual goodness.","publication_year":1813,"genre":"Romance"}
```
{% include copy-curl.html %}

## 步驟 4：搜尋索引

您可以透過下列方式對索引執行向量搜尋： 
- [使用範本查詢和搜尋管線](#using-a-template-query-and-a-search-pipeline)
- [在搜尋管線中改寫查詢](#rewriting-the-query-in-the-search-pipeline)

### 使用範本查詢與搜尋管線

首先，建立搜尋管線：

```json
PUT _search/pipeline/ml_inference_pipeline_cohere_search
{
  "request_processors": [
    {
      "ml_inference": {
        "model_id": "t64OPpUBX2k07okSZc2n",
        "input_map": [
          {
            "texts": "$..ext.ml_inference.text"
          }
        ],
        "output_map": [
          {
            "ext.ml_inference.vector": "embeddings.int8[0]"
          }
        ],
        "model_config": {
          "input_type": "search_query",
          "embedding_types": ["int8"]
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

接著，使用範本查詢來執行搜尋：

```json
GET books/_search?search_pipeline=ml_inference_pipeline_cohere_search&verbose_pipeline=false
{
  "query": {
    "template": {
      "knn": {
        "description_embedding": {
          "vector": "${ext.ml_inference.vector}",
          "k": 10
        }
      }
    }
  },
  "ext": {
    "ml_inference": {
      "text": "American Dream"
    }
  },
  "_source": {
    "excludes": [
      "title_embedding", "description_embedding"
    ]
  },
  "size": 2
}
```
{% include copy-curl.html %}

若要查看每個搜尋處理器的輸入與輸出，請在請求中加入 `&verbose_pipeline=true`。這對於偵錯及了解搜尋管線如何修改查詢很有用。如需更多資訊，請參閱[偵錯搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/debugging-search-pipeline/)。

### 在搜尋管線中重寫查詢

建立另一個會重寫查詢的搜尋管線：

```json
PUT _search/pipeline/ml_inference_pipeline_cohere_search2
{
  "request_processors": [
    {
      "ml_inference": {
        "model_id": "t64OPpUBX2k07okSZc2n",
        "input_map": [
          {
            "texts": "$..match.description.query"
          }
        ],
        "output_map": [
          {
            "query_vector": "embeddings.int8[0]"
          }
        ],
        "model_config": {
          "input_type": "search_query",
          "embedding_types": ["int8"]
        },
        "query_template": """
          {
            "query": {
              "knn": {
                "description_embedding": {
                  "vector": ${query_vector},
                  "k": 10
                }
              }
            },
            "_source": {
              "excludes": [
                "title_embedding",
                "description_embedding"
              ]
            },
            "size": 2
          }
        """
      }
    }
  ]
}
```
{% include copy-curl.html %}

現在使用此管線執行向量搜尋：

```json
GET books/_search?search_pipeline=ml_inference_pipeline_cohere_search2
{
  "query": {
    "match": {
      "description": "American Dream"
    }
  }
}
```
{% include copy-curl.html %}

回應中包含相符的文件：

```json
{
  "took": 96,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 7.271585e-7,
    "hits": [
      {
        "_index": "books",
        "_id": "U640PJUBX2k07okSEMwy",
        "_score": 7.271585e-7,
        "_source": {
          "publication_year": 1925,
          "author": "F. Scott Fitzgerald",
          "genre": "Classic Fiction",
          "description": "A novel of decadence and excess in the Jazz Age, exploring themes of wealth, love, and the American Dream.",
          "title": "The Great Gatsby"
        }
      },
      {
        "_index": "books",
        "_id": "VK40PJUBX2k07okSEMwy",
        "_score": 6.773544e-7,
        "_source": {
          "publication_year": 1960,
          "author": "Harper Lee",
          "genre": "Literary Fiction",
          "description": "A powerful story of racial injustice and loss of innocence in the American South during the Great Depression.",
          "title": "To Kill a Mockingbird"
        }
      }
    ]
  }
}
```

## 步驟 5 (選用)：使用二進位嵌入

在本節中，您將擴充此設定以支援二進位嵌入，其可提供更有效率的儲存空間與更快速的擷取。二進位嵌入可大幅降低儲存空間需求並提升搜尋速度，非常適合大規模應用程式。

您不需要修改連接器或模型——只需要更新向量索引、資料匯入管線與搜尋管線。

### 步驟 5.1：建立資料匯入管線

使用與[步驟 2](#step-2-create-an-ingest-pipeline)相同的組態建立名為 `ml_inference_pipeline_cohere_binary` 的新資料匯入管線，但將所有出現的 `int8` 取代為 `binary`。

### 選項 1：分別為 `title` 與 `description` 叫用模型

```json
PUT _ingest/pipeline/ml_inference_pipeline_cohere
{
"processors": [
    {
    "ml_inference": {
        "tag": "ml_inference",
        "description": "This processor is going to run ml inference during ingest request",
        "model_id": "t64OPpUBX2k07okSZc2n",
        "input_map": [
        {
            "texts": "$..title"
        },
        {
            "texts": "$..description"
        }
        ],
        "output_map": [
        {
            "title_embedding": "embeddings.binary[0]"
        },
        {
            "description_embedding": "embeddings.binary[0]"
        }
        ],
        "model_config": {
        "embedding_types": ["binary"]
        },
        "ignore_failure": false
    }
    }
]
}
```
{% include copy-curl.html %}
    
### 選項 2：合併 `title` 與 `description` 以叫用模型一次

```json
PUT _ingest/pipeline/ml_inference_pipeline_cohere
{
    "description": "Concatenate title and description fields",
    "processors": [
        {
        "set": {
            "field": "title_desc_tmp",
            "value": [
            "{{title}}",
            "{{description}}"
            ]
        }
        },
        {
        "ml_inference": {
            "tag": "ml_inference",
            "description": "This processor is going to run ml inference during ingest request",
            "model_id": "t64OPpUBX2k07okSZc2n",
            "input_map": [
            {
                "texts": "title_desc_tmp"
            }
            ],
            "output_map": [
            {
                "title_embedding": "embeddings.binary[0]",
                "description_embedding": "embeddings.binary[1]"
            }
            ],
            "model_config": {
            "embedding_types": ["binary"]
            },
            "ignore_failure": true
        }
        },
        {
        "remove": {
            "field": "title_desc_tmp"
        }
        }
    ]
}
```
{% include copy-curl.html %}


### 步驟 5.2：建立向量索引並匯入資料

建立包含[二進位向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#binary-vectors)欄位的新向量索引：

```json
PUT books_binary_embedding
{
  "settings": {
    "index": {
      "default_pipeline": "ml_inference_pipeline_cohere_binary",
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "title_embedding": {
        "type": "knn_vector",
        "dimension": 1024,
        "data_type": "binary",
        "space_type": "hamming",
        "method": {
          "name": "hnsw",
          "engine": "faiss"
        }
      },
      "description_embedding": {
        "type": "knn_vector",
        "dimension": 1024,
        "data_type": "binary",
        "space_type": "hamming",
        "method": {
          "name": "hnsw",
          "engine": "faiss"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

將測試資料匯入索引：

```json
POST _bulk
{"index":{"_index":"books_binary_embedding"}}
{"title":"The Great Gatsby","author":"F. Scott Fitzgerald","description":"A novel of decadence and excess in the Jazz Age, exploring themes of wealth, love, and the American Dream.","publication_year":1925,"genre":"Classic Fiction"}
{"index":{"_index":"books_binary_embedding"}}
{"title":"To Kill a Mockingbird","author":"Harper Lee","description":"A powerful story of racial injustice and loss of innocence in the American South during the Great Depression.","publication_year":1960,"genre":"Literary Fiction"}
{"index":{"_index":"books_binary_embedding"}}
{"title":"Pride and Prejudice","author":"Jane Austen","description":"A romantic novel of manners that follows the character development of Elizabeth Bennet as she learns about the repercussions of hasty judgments and comes to appreciate the difference between superficial goodness and actual goodness.","publication_year":1813,"genre":"Romance"}
```
{% include copy-curl.html %}

### 步驟 5.3：建立搜尋管線

使用與[步驟 2](#step-4-search-the-index)相同的組態，建立名為 `ml_inference_pipeline_cohere_search_binary` 的新搜尋管線，但將所有出現的 `int8` 取代為 `binary`。

1. 將 `embeddings.int8[0]` 變更為 `embeddings.binary[0]`。
1. 將 `"embedding_types": ["int8"]` 變更為 `"embedding_types": ["binary"]`。

### 使用範本查詢與搜尋管線

首先，建立搜尋管線：

```json
PUT _search/pipeline/ml_inference_pipeline_cohere_search_binary
{
  "request_processors": [
    {
      "ml_inference": {
        "model_id": "t64OPpUBX2k07okSZc2n",
        "input_map": [
          {
            "texts": "$..ext.ml_inference.text"
          }
        ],
        "output_map": [
          {
            "ext.ml_inference.vector": "embeddings.binary[0]"
          }
        ],
        "model_config": {
          "input_type": "search_query",
          "embedding_types": ["binary"]
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 在搜尋管線中改寫查詢

建立另一個會改寫查詢的搜尋管線：

```json
PUT _search/pipeline/ml_inference_pipeline_cohere_search_binary2
{
  "request_processors": [
    {
      "ml_inference": {
        "model_id": "t64OPpUBX2k07okSZc2n",
        "input_map": [
          {
            "texts": "$..match.description.query"
          }
        ],
        "output_map": [
          {
            "query_vector": "embeddings.binary[0]"
          }
        ],
        "model_config": {
          "input_type": "search_query",
          "embedding_types": ["binary"]
        },
        "query_template": """
          {
            "query": {
              "knn": {
                "description_embedding": {
                  "vector": ${query_vector},
                  "k": 10
                }
              }
            },
            "_source": {
              "excludes": [
                "title_embedding",
                "description_embedding"
              ]
            },
            "size": 2
          }
        """
      }
    }
  ]
}
```
{% include copy-curl.html %}

接著，您可以使用該搜尋管線執行向量搜尋，如[步驟 4](#step-4-search-the-index)所述。