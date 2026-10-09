---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Amazon SageMaker 中使用交叉編碼器重新排序搜尋結果"
parent: Reranking search results
nav_order: 110
redirect_from:
  - /ml-commons-plugin/tutorials/reranking-cross-encoder/
  - /vector-search/tutorials/reranking/reranking-cross-encoder/
---

# 在 Amazon SageMaker 中使用交叉編碼器重新排序搜尋結果

[重新排序管線]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/reranking-search-results/)可以重新排序搜尋結果，並針對搜尋結果中的每個文件，計算其相對於搜尋查詢的相關性分數。相關性分數由交叉編碼器模型計算。

本教學說明如何在重新排序管線中使用 [Hugging Face `ms-marco-MiniLM-L-6-v2` 模型](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2)。

請將以 `your_` 前綴開頭的預留位置替換為您自己的值。
{: .note}

## 必要條件

開始之前，請先在 Amazon SageMaker 上部署模型。為獲得更好的效能，請使用 GPU。

執行下列程式碼，將模型部署到 [Amazon SageMaker](https://aws.amazon.com/pm/sagemaker)：

```python
import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel
sess = sagemaker.Session()
role = sagemaker.get_execution_role()

hub = {
    'HF_MODEL_ID':'cross-encoder/ms-marco-MiniLM-L-6-v2',
    'HF_TASK':'text-classification'
}
huggingface_model = HuggingFaceModel(
    transformers_version='4.37.0',
    pytorch_version='2.1.0',
    py_version='py310',
    env=hub,
    role=role, 
)
predictor = huggingface_model.deploy(
    initial_instance_count=1, # number of instances
    instance_type='ml.m5.xlarge' # ec2 instance type
)
```
{% include copy.html %}

請記下模型推論端點；您將在下一步中使用它來建立連接器。

## 步驟 1：建立連接器並註冊模型

若要為模型建立連接器，請傳送下列請求。

如果您使用的是自行管理的 OpenSearch，請提供您的 AWS 憑證：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Sagemaker cross-encoder model",
  "description": "Test connector for Sagemaker cross-encoder model",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "access_key": "your_access_key",
    "secret_key": "your_secret_key",
    "session_token": "your_session_token"
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
      "request_body": "{ \"inputs\": ${parameters.inputs} }",
      "pre_process_function": "\n    String escape(def input) { \n       if (input.contains(\"\\\\\")) {\n        input = input.replace(\"\\\\\", \"\\\\\\\\\");\n      }\n      if (input.contains(\"\\\"\")) {\n        input = input.replace(\"\\\"\", \"\\\\\\\"\");\n      }\n      if (input.contains('\r')) {\n        input = input = input.replace('\r', '\\\\r');\n      }\n      if (input.contains(\"\\\\t\")) {\n        input = input.replace(\"\\\\t\", \"\\\\\\\\\\\\t\");\n      }\n      if (input.contains('\n')) {\n        input = input.replace('\n', '\\\\n');\n      }\n      if (input.contains('\b')) {\n        input = input.replace('\b', '\\\\b');\n      }\n      if (input.contains('\f')) {\n        input = input.replace('\f', '\\\\f');\n      }\n      return input;\n    }\n\n   String query = params.query_text;\n   StringBuilder builder = new StringBuilder('[');\n    \n    for (int i=0; i<params.text_docs.length; i ++) {\n      builder.append('{\"text\":\"');\n      builder.append(escape(query));\n      builder.append('\", \"text_pair\":\"');\n      builder.append(escape(params.text_docs[i]));\n      builder.append('\"}');\n      if (i<params.text_docs.length - 1) {\n        builder.append(',');\n      }\n    }\n    builder.append(']');\n    \n    def parameters = '{ \"inputs\": ' + builder + ' }';\n    return  '{\"parameters\": ' + parameters + '}';\n     ",
      "post_process_function": "\n      \n      def dataType = \"FLOAT32\";\n      \n      \n      if (params.result == null)\n      {\n          return 'no result generated';\n          //return params.response;\n      }\n      def outputs = params.result;\n      \n      \n      def resultBuilder = new StringBuilder('[ ');\n      for (int i=0; i<outputs.length; i++) {\n        resultBuilder.append(' {\"name\": \"similarity\", \"data_type\": \"FLOAT32\", \"shape\": [1],');\n        //resultBuilder.append('{\"name\": \"similarity\"}');\n        \n        resultBuilder.append('\"data\": [');\n        resultBuilder.append(outputs[i].score);\n        resultBuilder.append(']}');\n        if (i<outputs.length - 1) {\n          resultBuilder.append(',');\n        }\n      }\n      resultBuilder.append(']');\n      \n      return resultBuilder.toString();\n    "
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
      "request_body": "{ \"inputs\": ${parameters.inputs} }",
      "pre_process_function": "\n    String escape(def input) { \n       if (input.contains(\"\\\\\")) {\n        input = input.replace(\"\\\\\", \"\\\\\\\\\");\n      }\n      if (input.contains(\"\\\"\")) {\n        input = input.replace(\"\\\"\", \"\\\\\\\"\");\n      }\n      if (input.contains('\r')) {\n        input = input = input.replace('\r', '\\\\r');\n      }\n      if (input.contains(\"\\\\t\")) {\n        input = input.replace(\"\\\\t\", \"\\\\\\\\\\\\t\");\n      }\n      if (input.contains('\n')) {\n        input = input.replace('\n', '\\\\n');\n      }\n      if (input.contains('\b')) {\n        input = input.replace('\b', '\\\\b');\n      }\n      if (input.contains('\f')) {\n        input = input.replace('\f', '\\\\f');\n      }\n      return input;\n    }\n\n   String query = params.query_text;\n   StringBuilder builder = new StringBuilder('[');\n    \n    for (int i=0; i<params.text_docs.length; i ++) {\n      builder.append('{\"text\":\"');\n      builder.append(escape(query));\n      builder.append('\", \"text_pair\":\"');\n      builder.append(escape(params.text_docs[i]));\n      builder.append('\"}');\n      if (i<params.text_docs.length - 1) {\n        builder.append(',');\n      }\n    }\n    builder.append(']');\n    \n    def parameters = '{ \"inputs\": ' + builder + ' }';\n    return  '{\"parameters\": ' + parameters + '}';\n     ",
      "post_process_function": "\n      \n      def dataType = \"FLOAT32\";\n      \n      \n      if (params.result == null)\n      {\n          return 'no result generated';\n          //return params.response;\n      }\n      def outputs = params.result;\n      \n      \n      def resultBuilder = new StringBuilder('[ ');\n      for (int i=0; i<outputs.length; i++) {\n        resultBuilder.append(' {\"name\": \"similarity\", \"data_type\": \"FLOAT32\", \"shape\": [1],');\n        //resultBuilder.append('{\"name\": \"similarity\"}');\n        \n        resultBuilder.append('\"data\": [');\n        resultBuilder.append(outputs[i].score);\n        resultBuilder.append(']}');\n        if (i<outputs.length - 1) {\n          resultBuilder.append(',');\n        }\n      }\n      resultBuilder.append(']');\n      \n      return resultBuilder.toString();\n    "
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

若要測試模型，請呼叫 Predict API：

```json
POST _plugins/_ml/models/your_model_id/_predict
{
  "parameters": {
    "inputs": [
      {
        "text": "I like you",
        "text_pair": "I hate you"
      },
      {
        "text": "I like you",
        "text_pair": "I love you"
      }
    ]
  }
}
```
{% include copy-curl.html %}

`inputs` 陣列中的每個項目包含一個 `query_text` 和一個 `text_docs` 字串，並以 ` . ` 分隔

或者，您可以依照下列方式測試模型：

```json
POST _plugins/_ml/_predict/text_similarity/your_model_id
{
  "query_text": "I like you",
  "text_docs": ["I hate you", "I love you"]
}
```
{% include copy-curl.html %}

連接器 `pre_process_function` 會將輸入轉換為先前 Predict API 請求中所示 `inputs` 參數所需的格式。

預設情況下，SageMaker 模型輸出採用下列格式：

```json
[
  {
    "label": "LABEL_0",
    "score": 0.054037678986787796
  },
  {
    "label": "LABEL_0",
    "score": 0.5877784490585327
  }
]
```

連接器 `pre_process_function` 會將模型輸出轉換為 [重新排序處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/) 可解讀的下列格式：

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
            0.054037678986787796
          ]
        },
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            0.5877784490585327
          ]
        }
      ],
      "status_code": 200
    }
  ]
}
```

回應包含兩個 `similarity` 輸出。對於每個 `similarity` 輸出，`data` 陣列會針對每個文件與查詢的比對提供一個相關性分數。`similarity` 輸出依照輸入文件的順序提供：第一個相似度結果對應第一個文件。

## 步驟 2：設定重新排序管線

請依照下列步驟設定重新排序管線。

### 步驟 2.1：匯入測試資料

傳送批次請求以匯入測試資料：

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

使用 MS MARCO 交叉編碼器模型建立重新排序管線：

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

如果您在 `document_fields` 中提供多個欄位名稱，則會先串接所有欄位的值，然後再執行重新排序。
{: .note}

### 步驟 2.3：測試重新排序

若要限制傳回的結果數量，您可以指定 `size` 參數。例如，將 `"size": 4` 設為傳回前四份文件：

```json
GET my-test-data/_search?search_pipeline=rerank_pipeline_sagemaker
{
  "query": {
    "match_all": {}
  },
  "size": 4,
  "ext": {
    "rerank": {
      "query_context": {
         "query_text": "What is the capital of the United States?"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含四份最相關的文件：

```json
{
  "took": 3,
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
    "max_score": 0.9997217,
    "hits": [
      {
        "_index": "my-test-data",
        "_id": "U0xye5AB9ZeWZdmDjWZn",
        "_score": 0.9997217,
        "_source": {
          "passage_text": "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district."
        }
      },
      {
        "_index": "my-test-data",
        "_id": "VExye5AB9ZeWZdmDjWZn",
        "_score": 0.55655104,
        "_source": {
          "passage_text": "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
        }
      },
      {
        "_index": "my-test-data",
        "_id": "UUxye5AB9ZeWZdmDjWZn",
        "_score": 0.115356825,
        "_source": {
          "passage_text": "Carson City is the capital city of the American state of Nevada."
        }
      },
      {
        "_index": "my-test-data",
        "_id": "Ukxye5AB9ZeWZdmDjWZn",
        "_score": 0.00021142483,
        "_source": {
          "passage_text": "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan."
        }
      }
    ]
  },
  "profile": {
    "shards": []
  }
}
```

若要將這些結果與未重新排序的結果進行比較，請在沒有重新排序管線的情況下執行搜尋：

```json
GET my-test-data/_search
{
  "query": {
    "match_all": {}
  },
  "ext": {
    "rerank": {
      "query_context": {
         "query_text": "What is the capital of the United States?"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中的第一份文件與 Carson City 有關，而 Carson City 並非美國首都：

```json
{
  "took": 1,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "my-test-data",
        "_id": "UUxye5AB9ZeWZdmDjWZn",
        "_score": 1,
        "_source": {
          "passage_text": "Carson City is the capital city of the American state of Nevada."
        }
      },
      {
        "_index": "my-test-data",
        "_id": "Ukxye5AB9ZeWZdmDjWZn",
        "_score": 1,
        "_source": {
          "passage_text": "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan."
        }
      },
      {
        "_index": "my-test-data",
        "_id": "U0xye5AB9ZeWZdmDjWZn",
        "_score": 1,
        "_source": {
          "passage_text": "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district."
        }
      },
      {
        "_index": "my-test-data",
        "_id": "VExye5AB9ZeWZdmDjWZn",
        "_score": 1,
        "_source": {
          "passage_text": "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
        }
      }
    ]
  }
}
```