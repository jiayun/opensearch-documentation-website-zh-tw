---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Amazon Bedrock 上的 Cohere Rerank 對搜尋結果重新排序"
parent: Reranking search results
nav_order: 95
redirect_from:
  - /vector-search/tutorials/reranking/reranking-cohere-bedrock/
---

# 使用 Amazon Bedrock 上的 Cohere Rerank 對搜尋結果重新排序

本教學說明如何在 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) 與自行管理的 OpenSearch 中，使用託管於 Amazon Bedrock 的 [Cohere Rerank 模型](https://docs.aws.amazon.com/bedrock/latest/userguide/rerank-supported.html) 實作搜尋結果重新排序。

[重新排序管線]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/reranking-search-results/) 可以對搜尋結果重新排序，並針對搜尋結果中的每份文件，計算其相對於搜尋查詢的相關性分數。相關性分數由交叉編碼器模型計算。

請將以 `your_` 前綴開頭的預留位置替換為您自己的值。
{: .note}

## 先決條件：在 Amazon Bedrock 上測試模型

在使用模型之前，請使用下列程式碼在 Amazon Bedrock 上測試：

```python
import json
import boto3
bedrock_region = "your_bedrock_model_region_like_us-west-2"
bedrock_runtime_client = boto3.client("bedrock-runtime", region_name=bedrock_region)

modelId = "cohere.rerank-v3-5:0"
contentType = "application/json"
accept = "*/*"

body = json.dumps({
    "query": "What is the capital city of America?",
    "documents": [
        "Carson City is the capital city of the American state of Nevada.",
        "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.",
        "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.",
        "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
    ],
    "api_version": 2
})

response = bedrock_runtime_client.invoke_model(
    modelId=modelId,
    contentType=contentType,
    accept=accept, 
    body=body
)
results = json.loads(response.get('body').read())["results"]
print(json.dumps(results, indent=2))
```
{% include copy.html %}

回應包含依相關性分數排序的重新排序結果：

```json
[
  {
    "index": 2,
    "relevance_score": 0.7190094
  },
  {
    "index": 0,
    "relevance_score": 0.32418242
  },
  {
    "index": 1,
    "relevance_score": 0.07456104
  },
  {
    "index": 3,
    "relevance_score": 0.06124987
  }
]
```

若要依索引排序結果，請使用下列程式碼：

```python
print(json.dumps(sorted(results, key=lambda x: x['index']), indent=2))
```
{% include copy.html %}

排序後的結果如下：

```json
[
  {
    "index": 0,
    "relevance_score": 0.32418242
  },
  {
    "index": 1,
    "relevance_score": 0.07456104
  },
  {
    "index": 2,
    "relevance_score": 0.7190094
  },
  {
    "index": 3,
    "relevance_score": 0.06124987
  }
]
```

## 步驟 1：建立連接器並註冊模型

若要為模型建立連接器，請傳送下列請求。

如果您使用的是自行管理的 OpenSearch，請提供您的 AWS 憑證：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Amazon Bedrock Cohere rerank model",
  "description": "Test connector for Amazon Bedrock Cohere rerank model",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "access_key": "your_access_key",
    "secret_key": "your_secret_key",
    "session_token": "your_session_token"
  },
  "parameters": {
    "service_name": "bedrock",
    "endpoint": "bedrock-runtime",
    "region": "your_bedrock_model_region_like_us-west-2",
    "model_name": "cohere.rerank-v3-5:0",
    "api_version": 2
  },
  "actions": [
    {
      "action_type": "PREDICT",
      "method": "POST",
      "url": "https://${parameters. endpoint}.${parameters.region}.amazonaws.com/model/${parameters.model_name}/invoke",
      "headers": {
        "x-amz-content-sha256": "required",
        "content-type": "application/json"
      },
      "pre_process_function": """
        def query_text = params.query_text;
        def text_docs = params.text_docs;
        def textDocsBuilder = new StringBuilder('[');
        for (int i=0; i<text_docs.length; i++) {
          textDocsBuilder.append('"');
          textDocsBuilder.append(text_docs[i]);
          textDocsBuilder.append('"');
          if (i<text_docs.length - 1) {
            textDocsBuilder.append(',');
          }
        }
        textDocsBuilder.append(']');
        def parameters = '{ "query": "' + query_text + '",  "documents": ' + textDocsBuilder.toString() + ' }';
        return  '{"parameters": ' + parameters + '}';
        """,
      "request_body": """
        { 
          "documents": ${parameters.documents},
          "query": "${parameters.query}",
          "api_version": ${parameters.api_version}
        }
        """,
      "post_process_function": """
        if (params.results == null || params.results.length == 0) {
          throw new IllegalArgumentException("Post process function input is empty.");
        }
        def outputs = params.results;
        def relevance_scores = new Double[outputs.length];
        for (int i=0; i<outputs.length; i++) {
          def index = new BigDecimal(outputs[i].index.toString()).intValue();
          relevance_scores[index] = outputs[i].relevance_score;
        }
        def resultBuilder = new StringBuilder('[');
        for (int i=0; i<relevance_scores.length; i++) {
          resultBuilder.append(' {"name": "similarity", "data_type": "FLOAT32", "shape": [1],');
          resultBuilder.append('"data": [');
          resultBuilder.append(relevance_scores[i]);
          resultBuilder.append(']}');
          if (i<outputs.length - 1) {
            resultBuilder.append(',');
          }
        }
        resultBuilder.append(']');
        return resultBuilder.toString();
      """
    }
  ]
}
```
{% include copy-curl.html %}

如果您使用的是 Amazon OpenSearch Service，您可以提供允許存取 Amazon Bedrock 的 AWS Identity and Access Management (IAM) 角色 Amazon Resource Name (ARN)：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Amazon Bedrock Cohere rerank model",
  "description": "Test connector for Amazon Bedrock Cohere rerank model",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "roleArn": "your_role_arn_which_allows_access_to_bedrock_model"
  },
  "parameters": {
    "service_name": "bedrock",
    "endpoint": "bedrock-runtime",
    "region": "your_bedrock_model_region_like_us-west-2",
    "model_name": "cohere.rerank-v3-5:0",
    "api_version": 2
},
  "actions": [
    {
      "action_type": "PREDICT",
      "method": "POST",
      "url": "https://${parameters. endpoint}.${parameters.region}.amazonaws.com/model/${parameters.model_name}/invoke",
      "headers": {
        "x-amz-content-sha256": "required",
        "content-type": "application/json"
      },
      "pre_process_function": """
        def query_text = params.query_text;
        def text_docs = params.text_docs;
        def textDocsBuilder = new StringBuilder('[');
        for (int i=0; i<text_docs.length; i++) {
          textDocsBuilder.append('"');
          textDocsBuilder.append(text_docs[i]);
          textDocsBuilder.append('"');
          if (i<text_docs.length - 1) {
            textDocsBuilder.append(',');
          }
        }
        textDocsBuilder.append(']');
        def parameters = '{ "query": "' + query_text + '",  "documents": ' + textDocsBuilder.toString() + ' }';
        return  '{"parameters": ' + parameters + '}';
        """,
      "request_body": """
        { 
          "documents": ${parameters.documents},
          "query": "${parameters.query}",
          "api_version": ${parameters.api_version}
        }
        """,
      "post_process_function": """
        if (params.results == null || params.results.length == 0) {
          throw new IllegalArgumentException("Post process function input is empty.");
        }
        def outputs = params.results;
        def relevance_scores = new Double[outputs.length];
        for (int i=0; i<outputs.length; i++) {
          def index = new BigDecimal(outputs[i].index.toString()).intValue();
          relevance_scores[index] = outputs[i].relevance_score;
        }
        def resultBuilder = new StringBuilder('[');
        for (int i=0; i<relevance_scores.length; i++) {
          resultBuilder.append(' {"name": "similarity", "data_type": "FLOAT32", "shape": [1],');
          resultBuilder.append('"data": [');
          resultBuilder.append(relevance_scores[i]);
          resultBuilder.append(']}');
          if (i<outputs.length - 1) {
            resultBuilder.append(',');
          }
        }
        resultBuilder.append(']');
        return resultBuilder.toString();
      """
    }
  ]
}
```

如需更多資訊，請參閱 [AWS 文件](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ml-amazon-connector.html)。

使用回應中的連接器 ID 來註冊並部署模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "Amazon Bedrock Cohere rerank model",
    "function_name": "remote",
    "description": "test rerank model",
    "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

請記下回應中的模型 ID；後續步驟將會用到。

使用 Predict API 測試模型：

```json
POST _plugins/_ml/models/your_model_id/_predict
{
  "parameters": {
    "query": "What is the capital city of America?",
    "documents": [
      "Carson City is the capital city of the American state of Nevada.",
      "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.",
      "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.",
      "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
    ]
  }
}
```
{% include copy-curl.html %}

或者，您也可以依照下列方式測試模型：

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

連接器 `pre_process_function` 會將輸入轉換為先前所示參數所需的格式。

預設情況下，Amazon Bedrock Rerank API 的輸出具有下列格式：

```json
[
  {
    "index": 2,
    "relevance_score": 0.7190094
  },
  {
    "index": 0,
    "relevance_score": 0.32418242
  },
  {
    "index": 1,
    "relevance_score": 0.07456104
  },
  {
    "index": 3,
    "relevance_score": 0.06124987
  }
]
```

連接器 `post_process_function` 會將模型的輸出轉換為 [重新排序處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/) 可以解讀的格式，並依索引排序結果。此調整後的格式如下：

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
            0.32418242
          ]
        },
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            0.07456104
          ]
        },
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            0.7190094
          ]
        },
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            0.06124987
          ]
        }
      ],
      "status_code": 200
    }
  ]
}
```

回應包含四個 `similarity` 物件。對於每個 `similarity` 物件，`data` 陣列包含每個文件相對於查詢的相關性分數。`similarity` 物件會依照輸入文件的順序提供——第一個物件對應第一個文件。這與 Cohere Rerank 模型的預設輸出不同，後者會依相關性分數排序文件。文件順序會在 `connector.post_process.cohere.rerank` 後處理函式中變更，讓輸出與重新排序管線相容。

## 步驟 2：設定重新排序管線

請依照下列步驟設定重新排序管線。

### 步驟 2.1：匯入測試資料

傳送大量請求以匯入測試資料：

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

使用 Cohere Rerank 模型建立重新排序管線：

```json
PUT /_search/pipeline/rerank_pipeline_bedrock
{
    "description": "Pipeline for reranking with Bedrock Cohere rerank model",
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

如果您在 `document_fields` 中提供多個欄位名稱，會先串接所有欄位的值，然後再執行重新排序。
{: .note}

### 步驟 2.3：測試重新排序

若要限制傳回的結果數量，您可以指定 `size` 參數。例如，將 `"size": 2` 設為傳回前兩份文件。

首先，在不使用重新排序管線的情況下測試查詢：

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

接著，使用重新排序管線測試查詢：

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
    "max_score": 0.7190094,
    "hits": [
      {
        "_index": "my-test-data",
        "_id": "3",
        "_score": 0.7190094,
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
        "_score": 0.32418242,
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
        "_score": 0.07456104,
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
        "_score": 0.06124987,
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

若要避免將查詢寫兩次，請使用 `query_text_path` 而非 `query_text`，如下所示：

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