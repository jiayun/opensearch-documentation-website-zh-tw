---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Amazon SageMaker 中的重新排序器對搜尋結果重新排序"
parent: Reranking search results
nav_order: 115
redirect_from:
  - /vector-search/tutorials/reranking/reranking-sagemaker/
---

# 使用 Amazon SageMaker 中的重新排序器對搜尋結果重新排序

[重新排序管線]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/reranking-search-results/)可以對搜尋結果重新排序，並針對搜尋結果中的每個文件，計算其相對於搜尋查詢的相關性分數。相關性分數由重新排序器模型計算。

本教學說明如何在自管 OpenSearch 與 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) 中對搜尋結果重新排序。本教學使用託管於 Amazon SageMaker 的 [Hugging Face `BAAI/bge-reranker-v2-m3`](https://huggingface.co/BAAI/bge-reranker-v2-m3) 模型。

請將以 `your_` 前綴開頭的預留位置替換為您自己的值。
{: .note}

## 必要條件：將模型部署至 Amazon SageMaker

請使用下列程式碼將模型部署至 Amazon SageMaker。建議使用 GPU 以獲得更好的效能：  

```python
import json
import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri
from sagemaker.serverless import ServerlessInferenceConfig

try:
	role = sagemaker.get_execution_role()
except ValueError:
	iam = boto3.client('iam')
	role = iam.get_role(RoleName='sagemaker_execution_role')['Role']['Arn']

# Hub Model configuration. https://huggingface.co/models
hub = {
	'HF_MODEL_ID':'BAAI/bge-reranker-v2-m3'
}

# create Hugging Face Model Class
huggingface_model = HuggingFaceModel(
	image_uri=get_huggingface_llm_image_uri("huggingface-tei",version="1.2.3"),
	env=hub,
	role=role, 
)

# deploy model to SageMaker Inference
predictor = huggingface_model.deploy(
	initial_instance_count=1,
	instance_type="ml.g5.2xlarge",
  )
```
{% include copy.html %}

如需更多資訊，請參閱[如何使用 Amazon SageMaker 部署此模型](https://huggingface.co/BAAI/bge-reranker-v2-m3?sagemaker_deploy=true)。

若要執行重新排序測試，請使用下列程式碼：

```python
result = predictor.predict(data={
    "query":"What is the capital city of America?",
    "texts":[
        "Carson City is the capital city of the American state of Nevada.",
        "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.",
        "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.",
        "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
    ]
})

print(json.dumps(result, indent=2))
```
{% include copy.html %}

回應包含依相關性分數排序的重新排序結果：

```json
[
  {
    "index": 2,
    "score": 0.92879725
  },
  {
    "index": 0,
    "score": 0.013636836
  },
  {
    "index": 1,
    "score": 0.000593021
  },
  {
    "index": 3,
    "score": 0.00012148176
  }
]
```

若要依索引排序結果，請使用下列程式碼：

```python
print(json.dumps(sorted(result, key=lambda x: x['index']),indent=2))
```
{% include copy.html %}

排序後的結果如下：

```json
[
  {
    "index": 0,
    "score": 0.013636836
  },
  {
    "index": 1,
    "score": 0.000593021
  },
  {
    "index": 2,
    "score": 0.92879725
  },
  {
    "index": 3,
    "score": 0.00012148176
  }
]
```

請記下模型推論端點；您將在下一步中使用它來建立連接器。您可以使用下列程式碼確認推論端點 URL：

```python
region_name = boto3.Session().region_name
endpoint_name = predictor.endpoint_name
endpoint_url = f"https://runtime.sagemaker.{region_name}.amazonaws.com/endpoints/{endpoint_name}/invocations"
print(endpoint_url)
```
{% include copy.html %}

## 步驟 1：建立連接器並註冊模型

若要為模型建立連接器，請傳送下列請求。

如果您使用的是自管 OpenSearch，請提供您的 AWS 憑證：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Sagemakre cross-encoder model",
  "description": "Test connector for Sagemaker cross-encoder model",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "access_key": "your_access_key",
    "secret_key": "your_secret_key",
    "session_token": "your_session_token"
  },
  "parameters": {
    "region": "your_sagemaker_model_region_like_us-west-2",
    "service_name": "sagemaker"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "your_sagemaker_model_inference_endpoint_created_in_last_step",
      "headers": {
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
        def parameters = '{ "query": "' + query_text + '",  "texts": ' + textDocsBuilder.toString() + ' }';
        return  '{"parameters": ' + parameters + '}';
      """,
      "request_body": """
        { 
          "query": "${parameters.query}",
          "texts": ${parameters.texts}
        }
      """,
      "post_process_function": """
        if (params.result == null || params.result.length == 0) {
          throw new IllegalArgumentException("Post process function input is empty.");
        }
        def outputs = params.result;
        def scores = new Double[outputs.length];
        for (int i=0; i<outputs.length; i++) {
          def index = new BigDecimal(outputs[i].index.toString()).intValue();
          scores[index] = outputs[i].score;
        }
        def resultBuilder = new StringBuilder('[');
        for (int i=0; i<scores.length; i++) {
          resultBuilder.append(' {"name": "similarity", "data_type": "FLOAT32", "shape": [1],');
          resultBuilder.append('"data": [');
          resultBuilder.append(scores[i]);
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

如果您使用的是 Amazon OpenSearch Service，您可以提供允許存取 SageMaker 模型推論端點的 AWS Identity and Access Management (IAM) 角色 Amazon Resource Name (ARN)：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Sagemakre cross-encoder model",
  "description": "Test connector for Sagemaker cross-encoder model",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "roleArn": "your_role_arn_which_allows_access_to_sagemaker_model_inference_endpoint"
  },
  "parameters": {
    "region": "your_sagemkaer_model_region_like_us-west-2",
    "service_name": "sagemaker"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "your_sagemaker_model_inference_endpoint_created_in_last_step",
      "headers": {
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
        def parameters = '{ "query": "' + query_text + '",  "texts": ' + textDocsBuilder.toString() + ' }';
        return  '{"parameters": ' + parameters + '}';
      """,
      "request_body": """
        { 
          "query": "${parameters.query}",
          "texts": ${parameters.texts}
        }
      """,
      "post_process_function": """
        if (params.result == null || params.result.length == 0) {
          throw new IllegalArgumentException("Post process function input is empty.");
        }
        def outputs = params.result;
        def scores = new Double[outputs.length];
        for (int i=0; i<outputs.length; i++) {
          def index = new BigDecimal(outputs[i].index.toString()).intValue();
          scores[index] = outputs[i].score;
        }
        def resultBuilder = new StringBuilder('[');
        for (int i=0; i<scores.length; i++) {
          resultBuilder.append(' {"name": "similarity", "data_type": "FLOAT32", "shape": [1],');
          resultBuilder.append('"data": [');
          resultBuilder.append(scores[i]);
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

如需更多資訊，請參閱 [AWS 文件](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ml-amazon-connector.html)、[本教學]({{site.url}}{{site.baseurl}}/vector-search/tutorials/semantic-search/semantic-search-sagemaker/)以及 [AIConnectorHelper 筆記本](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/tutorials/aws/AIConnectorHelper.ipynb)。

使用回應中的連接器 ID 來註冊並部署模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "Sagemaker Cross-Encoder model",
    "function_name": "remote",
    "description": "test rerank model",
    "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

請記下回應中的模型 ID；您將在後續步驟中使用它。

使用 Predict API 測試模型：

```json
POST _plugins/_ml/models/your_model_id/_predict
{
  "parameters": {
    "query": "What is the capital city of America?",
    "texts": [
      "Carson City is the capital city of the American state of Nevada.",
      "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.",
      "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.",
      "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
    ]
  }
}
```
{% include copy-curl.html %}

或者，您可以依照下列方式測試模型：

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

預設情況下，模型輸出具有下列格式：

```json
[
  {
    "index": 2,
    "score": 0.92879725
  },
  {
    "index": 0,
    "score": 0.013636836
  },
  {
    "index": 1,
    "score": 0.000593021
  },
  {
    "index": 3,
    "score": 0.00012148176
  }
]
```

連接器 `post_process_function` 會將模型的輸出轉換為 [重新排序處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/) 可解讀的格式，並依索引排序結果。轉換後的格式如下：

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
            0.013636836
          ]
        },
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            0.013636836
          ]
        },
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            0.92879725
          ]
        },
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            0.00012148176
          ]
        }
      ],
      "status_code": 200
    }
  ]
}
```

回應包含兩個 `similarity` 物件。對於每個 `similarity` 物件，`data` 陣列包含每份文件相對於查詢的相關性分數。`similarity` 物件會依輸入文件的順序提供——第一個物件對應第一份文件。

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

使用 cross-encoder 模型建立重新排序管線：

```json
PUT /_search/pipeline/rerank_pipeline_sagemaker
{
    "description": "Pipeline for reranking with Sagemaker cross-encoder model",
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

回應中的第一份文件是 `Carson City is the capital city of the American state of Nevada`，這是錯誤的：

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
POST my-test-data/_search?search_pipeline=rerank_pipeline_sagemaker
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
    "max_score": 0.92879725,
    "hits": [
      {
        "_index": "my-test-data",
        "_id": "3",
        "_score": 0.92879725,
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
        "_score": 0.013636836,
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
        "_score": 0.013636836,
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
        "_score": 0.00012148176,
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
POST my-test-data/_search?search_pipeline=rerank_pipeline_sagemaker
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