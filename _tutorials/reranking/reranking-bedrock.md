---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Amazon Bedrock 模型重新排序搜尋結果"
parent: Reranking search results
nav_order: 100
redirect_from:
  - /ml-commons-plugin/tutorials/reranking-bedrock/
  - /vector-search/tutorials/reranking/reranking-bedrock/
---

# 使用 Amazon Bedrock 模型重新排序搜尋結果

[重新排序管線]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/reranking-search-results/)可以重新排序搜尋結果，為搜尋結果中的每份文件提供相對於搜尋查詢的相關性分數。相關性分數由交叉編碼器模型計算。

本教學說明如何使用 [Amazon Bedrock Rerank API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Rerank.html)，以託管於 Amazon Bedrock 的模型重新排序搜尋結果。

請將開頭為前置字元 `your_` 的預留位置取代為您自己的值。
{: .note}

## 先決條件：在 Amazon Bedrock 上測試模型

使用模型之前，請先在 Amazon Bedrock 上進行測試。如需支援的重新排序器模型，請參閱 [Amazon Bedrock 中重新排序的支援區域與模型](https://docs.aws.amazon.com/bedrock/latest/userguide/rerank-supported.html)。如需模型 ID，請參閱 [Amazon Bedrock 中支援的基礎模型](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)。若要執行重新排序測試，請使用下列程式碼：

```python
import json
import boto3
bedrock_region = "your_bedrock_model_region_like_us-west-2"
bedrock_agent_runtime_client = boto3.client("bedrock-agent-runtime", region_name=bedrock_region)

model_id = "amazon.rerank-v1:0"

response = bedrock_agent_runtime_client.rerank(
    queries=[
        {
            "textQuery": {
                "text": "What is the capital city of America?",
            },
            "type": "TEXT"
        }
    ],
    rerankingConfiguration={
        "bedrockRerankingConfiguration": {
            "modelConfiguration": {
                "modelArn": f"arn:aws:bedrock:{bedrock_region}::foundation-model/{model_id}"
            },
        },
        "type": "BEDROCK_RERANKING_MODEL"
    },
    sources=[
        {
            "inlineDocumentSource": {
                "textDocument": {
                    "text": "Carson City is the capital city of the American state of Nevada.",
                },
                "type": "TEXT"
            },
            "type": "INLINE"
        },
        {
            "inlineDocumentSource": {
                "textDocument": {
                    "text": "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.",
                },
                "type": "TEXT"
            },
            "type": "INLINE"
        },
        {
            "inlineDocumentSource": {
                "textDocument": {
                    "text": "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.",
                },
                "type": "TEXT"
            },
            "type": "INLINE"
        },
        {
            "inlineDocumentSource": {
                "textDocument": {
                    "text": "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
                },
                "type": "TEXT"
            },
            "type": "INLINE"
        },        
    ]
)

results = response["results"]
print(json.dumps(results, indent=2))
```
{% include copy.html %}

重新排序後的結果會依最高分數排序：

```json
[
  {
    "index": 2,
    "relevanceScore": 0.7711548805236816
  },
  {
    "index": 0,
    "relevanceScore": 0.0025114635936915874
  },
  {
    "index": 1,
    "relevanceScore": 2.4876489987946115e-05
  },
  {
    "index": 3,
    "relevanceScore": 6.339210358419223e-06
  }
]
```

若要依索引排序結果，請使用下列程式碼：

```python
print(json.dumps(sorted(results, key=lambda x: x['index']),indent=2))
```

以下是依索引排序的結果：

```json
[
  {
    "index": 0,
    "relevanceScore": 0.0025114635936915874
  },
  {
    "index": 1,
    "relevanceScore": 2.4876489987946115e-05
  },
  {
    "index": 2,
    "relevanceScore": 0.7711548805236816
  },
  {
    "index": 3,
    "relevanceScore": 6.339210358419223e-06
  }
]
```

## 步驟 1：建立連接器並註冊模型

若要建立連接器並註冊模型，請使用下列步驟。

### 步驟 1.1：為模型建立連接器

首先，為模型建立連接器。

如果您使用自我管理的 OpenSearch，請提供您的 AWS 憑證：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Amazon Bedrock Rerank API",
  "description": "Test connector for Amazon Bedrock Rerank API",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "access_key": "your_access_key",
    "secret_key": "your_secret_key",
    "session_token": "your_session_token"
  },
  "parameters": {
    "service_name": "bedrock",
    "endpoint": "bedrock-agent-runtime",
    "region": "your_bedrock_model_region_like_us-west-2",
    "api_name": "rerank",
    "model_id": "amazon.rerank-v1:0"
  },
  "actions": [
    {
      "action_type": "PREDICT",
      "method": "POST",
      "url": "https://${parameters.endpoint}.${parameters.region}.amazonaws.com/${parameters.api_name}",
      "headers": {
        "x-amz-content-sha256": "required",
        "content-type": "application/json"
      },
      "pre_process_function": "connector.pre_process.bedrock.rerank",
      "request_body": """
        {
          "queries": ${parameters.queries},
          "rerankingConfiguration": {
            "bedrockRerankingConfiguration": {
              "modelConfiguration": {
                "modelArn": "arn:aws:bedrock:${parameters.region}::foundation-model/${parameters.model_id}"
              }
            },
            "type": "BEDROCK_RERANKING_MODEL"
          },
          "sources": ${parameters.sources}
        }
      """,
      "post_process_function": "connector.post_process.bedrock.rerank"
    }
  ]
}
```
{% include copy-curl.html %}

如果您使用 Amazon OpenSearch Service，則可以提供允許存取 Amazon Bedrock 的 AWS Identity and Access Management (IAM) 角色 Amazon Resource Name (ARN)。如需詳細資訊，請參閱 [AWS 文件](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ml-amazon-connector.html)。使用下列請求建立連接器：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Amazon Bedrock Rerank API",
  "description": "Test connector for Amazon Bedrock Rerank API",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "roleArn": "your_role_arn_which_allows_access_to_bedrock_agent_runtime_rerank_api"
  },
  "parameters": {
    "service_name": "bedrock",
    "endpoint": "bedrock-agent-runtime",
    "region": "your_bedrock_model_region_like_us-west-2",
    "api_name": "rerank",
    "model_id": "amazon.rerank-v1:0"
  },
  "actions": [
    {
      "action_type": "PREDICT",
      "method": "POST",
      "url": "https://${parameters.endpoint}.${parameters.region}.amazonaws.com/${parameters.api_name}",
      "headers": {
        "x-amz-content-sha256": "required",
        "content-type": "application/json"
      },
      "pre_process_function": "connector.pre_process.bedrock.rerank",
      "request_body": """
        {
          "queries": ${parameters.queries},
          "rerankingConfiguration": {
            "bedrockRerankingConfiguration": {
              "modelConfiguration": {
                "modelArn": "arn:aws:bedrock:${parameters.region}::foundation-model/${parameters.model_id}"
              }
            },
            "type": "BEDROCK_RERANKING_MODEL"
          },
          "sources": ${parameters.sources}
        }
      """,
      "post_process_function": "connector.post_process.bedrock.rerank"
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 1.2：註冊並部署模型

使用回應中的連接器 ID 來註冊並部署模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "Amazon Bedrock Rerank API",
  "function_name": "remote",
  "description": "test Amazon Bedrock Rerank API",
  "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

記下回應中的模型 ID；後續步驟將會用到。

### 步驟 1.3：測試模型

使用 Predict API 測試模型：

```json
POST _plugins/_ml/_predict/text_similarity/your_model_id
{
  "query_text": "What is the capital city of America?",
  "text_docs": [
    "Carson City is the capital city of the American state of Nevada.",
    "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.",
    "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.",
    "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
  ]
}
```
{% include copy-curl.html %}

或者，您也可以使用下列查詢來測試模型。此查詢會略過 `pre_process_function`，直接呼叫 Rerank API：

```json
POST _plugins/_ml/models/your_model_id/_predict
{
  "parameters": {
    "queries": [
      {
        "textQuery": {
            "text": "What is the capital city of America?"
        },
        "type": "TEXT"
      }
    ],
    "sources": [
        {
            "inlineDocumentSource": {
                "textDocument": {
                    "text": "Carson City is the capital city of the American state of Nevada."
                },
                "type": "TEXT"
            },
            "type": "INLINE"
        },
        {
            "inlineDocumentSource": {
                "textDocument": {
                    "text": "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan."
                },
                "type": "TEXT"
            },
            "type": "INLINE"
        },
        {
            "inlineDocumentSource": {
                "textDocument": {
                    "text": "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district."
                },
                "type": "TEXT"
            },
            "type": "INLINE"
        },
        {
            "inlineDocumentSource": {
                "textDocument": {
                    "text": "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
                },
                "type": "TEXT"
            },
            "type": "INLINE"
        }
    ]
  }
}
```
{% include copy-curl.html %}

連接器 `pre_process_function` 會將輸入轉換為 Predict API `parameters` 所需的格式。

預設情況下，Amazon Bedrock Rerank API 的輸出格式如下：

```json
[
  {
    "index": 2,
    "relevanceScore": 0.7711548724998493
  },
  {
    "index": 0,
    "relevanceScore": 0.0025114635138098534
  },
  {
    "index": 1,
    "relevanceScore": 2.4876490010363496e-05
  },
  {
    "index": 3,
    "relevanceScore": 6.339210403977635e-06
  }
]
```

連接器 `post_process_function` 會將模型的輸出轉換為 [Reranker 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/) 可以解讀的格式，並依索引排序結果。

回應包含四個 `similarity` 輸出。對於每個 `similarity` 輸出，`data` 陣列包含每份文件相對於查詢的相關性分數。`similarity` 輸出會依照輸入文件的順序提供；第一個相似度結果對應第一份文件：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            0.0025114636
          ]
        },
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            2.487649e-05
          ]
        },
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            0.7711549
          ]
        },
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            6.3392104e-06
          ]
        }
      ],
      "status_code": 200
    }
  ]
}
```

## 步驟 2：建立重新排序管線

若要建立重新排序管線，請依照下列步驟操作。

### 步驟 2.1：匯入測試資料

使用下列請求將資料匯入您的索引：

```json
POST _bulk
{ "index": { "_index": "my-test-data" } }
{ "passage_text" : "Carson City is the capital city of the American state of Nevada." }
{ "index": { "_index": "my-test-data" } }
{ "passage_text" : "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan." }
{ "index": { "_index": "my-test-data" } }
{ "passage_text" : "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district." }
{ "index": { "_index": "my-test-data" } }
{ "passage_text" : "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states." }
```
{% include copy-curl.html %}

### 步驟 2.2：建立重新排序管線

使用 Amazon Bedrock 重新排序模型建立重新排序管線：

```json
PUT /_search/pipeline/rerank_pipeline_bedrock
{
    "description": "Pipeline for reranking with Bedrock rerank model",
    "response_processors": [
        {
            "rerank": {
                "ml_opensearch": {
                    "model_id": "your_model_id_created_in_step1"
                },
                "context": {
                    "document_fields": ["passage_text"]
                }
            }
        }
    ]
}
```
{% include copy-curl.html %}

如果您在 `document_fields` 中提供多個欄位名稱，所有欄位的值會先串連，然後再執行重新排序。
{: .note}

### 步驟 2.3：測試重新排序

首先，測試不使用重新排序管線的查詢：

```json
POST my-test-data/_search
{
  "query": {
    "match": {
      "passage_text": "What is the capital city of America?"
    }
  },
  "highlight": {
    "pre_tags": ["<strong>"],
    "post_tags": ["</strong>"],
    "fields": {"passage_text": {}}
  },
  "_source": false,
  "fields": ["passage_text"]
}
```
{% include copy-curl.html %}

回應中的第一份文件是 `Carson City is the capital city of the American state of Nevada`，這是不正確的：

```json
{
  "took": 2,
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
    "max_score": 2.5045562,
    "hits": [
      {
        "_index": "my-test-data",
        "_id": "1",
        "_score": 2.5045562,
        "fields": {
          "passage_text": [
            "Carson City is the capital city of the American state of Nevada."
          ]
        },
        "highlight": {
          "passage_text": [
            "Carson <strong>City</strong> <strong>is</strong> <strong>the</strong> <strong>capital</strong> <strong>city</strong> <strong>of</strong> <strong>the</strong> American state <strong>of</strong> Nevada."
          ]
        }
      },
      {
        "_index": "my-test-data",
        "_id": "2",
        "_score": 0.5807494,
        "fields": {
          "passage_text": [
            "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan."
          ]
        },
        "highlight": {
          "passage_text": [
            "<strong>The</strong> Commonwealth <strong>of</strong> <strong>the</strong> Northern Mariana Islands <strong>is</strong> a group <strong>of</strong> islands in <strong>the</strong> Pacific Ocean.",
            "Its <strong>capital</strong> <strong>is</strong> Saipan."
          ]
        }
      },
      {
        "_index": "my-test-data",
        "_id": "3",
        "_score": 0.5261191,
        "fields": {
          "passage_text": [
            "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district."
          ]
        },
        "highlight": {
          "passage_text": [
            "(also known as simply Washington or D.C., and officially as <strong>the</strong> District <strong>of</strong> Columbia) <strong>is</strong> <strong>the</strong> <strong>capital</strong>",
            "<strong>of</strong> <strong>the</strong> United States.",
            "It <strong>is</strong> a federal district."
          ]
        }
      },
      {
        "_index": "my-test-data",
        "_id": "4",
        "_score": 0.5083029,
        "fields": {
          "passage_text": [
            "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
          ]
        },
        "highlight": {
          "passage_text": [
            "<strong>Capital</strong> punishment (<strong>the</strong> death penalty) has existed in <strong>the</strong> United States since beforethe United States",
            "As <strong>of</strong> 2017, <strong>capital</strong> punishment <strong>is</strong> legal in 30 <strong>of</strong> <strong>the</strong> 50 states."
          ]
        }
      }
    ]
  }
}
```

接著，測試使用重新排序管線的查詢：

```json
POST my-test-data/_search?search_pipeline=rerank_pipeline_bedrock
{
  "query": {
    "match": {
      "passage_text": "What is the capital city of America?"
    }
  },
  "ext": {
    "rerank": {
      "query_context": {
         "query_text": "What is the capital city of America?"
      }
    }
  },
  "highlight": {
    "pre_tags": ["<strong>"],
    "post_tags": ["</strong>"],
    "fields": {"passage_text": {}}
  },
  "_source": false,
  "fields": ["passage_text"]
}
```
{% include copy-curl.html %}

回應中的第一份文件是 `"Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district."`，這是正確的：

```json
{
  "took": 2,
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
    "max_score": 0.7711549,
    "hits": [
      {
        "_index": "my-test-data",
        "_id": "3",
        "_score": 0.7711549,
        "fields": {
          "passage_text": [
            "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district."
          ]
        },
        "highlight": {
          "passage_text": [
            "(also known as simply Washington or D.C., and officially as <strong>the</strong> District <strong>of</strong> Columbia) <strong>is</strong> <strong>the</strong> <strong>capital</strong>",
            "<strong>of</strong> <strong>the</strong> United States.",
            "It <strong>is</strong> a federal district."
          ]
        }
      },
      {
        "_index": "my-test-data",
        "_id": "1",
        "_score": 0.0025114636,
        "fields": {
          "passage_text": [
            "Carson City is the capital city of the American state of Nevada."
          ]
        },
        "highlight": {
          "passage_text": [
            "Carson <strong>City</strong> <strong>is</strong> <strong>the</strong> <strong>capital</strong> <strong>city</strong> <strong>of</strong> <strong>the</strong> American state <strong>of</strong> Nevada."
          ]
        }
      },
      {
        "_index": "my-test-data",
        "_id": "2",
        "_score": 02.487649e-05,
        "fields": {
          "passage_text": [
            "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan."
          ]
        },
        "highlight": {
          "passage_text": [
            "<strong>The</strong> Commonwealth <strong>of</strong> <strong>the</strong> Northern Mariana Islands <strong>is</strong> a group <strong>of</strong> islands in <strong>the</strong> Pacific Ocean.",
            "Its <strong>capital</strong> <strong>is</strong> Saipan."
          ]
        }
      },
      {
        "_index": "my-test-data",
        "_id": "4",
        "_score": 6.3392104e-06,
        "fields": {
          "passage_text": [
            "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
          ]
        },
        "highlight": {
          "passage_text": [
            "<strong>Capital</strong> punishment (<strong>the</strong> death penalty) has existed in <strong>the</strong> United States since beforethe United States",
            "As <strong>of</strong> 2017, <strong>capital</strong> punishment <strong>is</strong> legal in 30 <strong>of</strong> <strong>the</strong> 50 states."
          ]
        }
      }
    ]
  },
  "profile": {
    "shards": []
  }
}
```

您可以指定 `query_text_path` 而非 `query_text`，藉此重複使用相同的查詢：

```json
POST my-test-data/_search?search_pipeline=rerank_pipeline_bedrock
{
  "query": {
    "match": {
      "passage_text": "What is the capital city of America?"
    }
  },
  "ext": {
    "rerank": {
      "query_context": {
         "query_text_path": "query.match.passage_text.query"
      }
    }
  },
  "highlight": {
    "pre_tags": ["<strong>"],
    "post_tags": ["</strong>"],
    "fields": {"passage_text": {}}
  },
  "_source": false,
  "fields": ["passage_text"]
}
```
{% include copy-curl.html %}

