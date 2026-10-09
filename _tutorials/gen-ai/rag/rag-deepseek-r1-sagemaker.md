---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Amazon SageMaker 中使用 DeepSeek-R1 實作 RAG"
parent: RAG
grand_parent: Generative AI
nav_order: 140
redirect_from:
  - /vector-search/tutorials/rag/rag-deepseek-r1-sagemaker/
  - /tutorials/vector-search/rag/rag-deepseek-r1-sagemaker/
---

# 在 Amazon SageMaker 中使用 DeepSeek-R1 實作 RAG

本教學說明如何使用 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) 與 [DeepSeek-R1 模型](https://huggingface.co/deepseek-ai/DeepSeek-R1) 實作檢索增強生成 (RAG)。

如果您使用的是自行管理的 OpenSearch 而非 Amazon OpenSearch Service，請使用[該藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/deepseek_connector_chat_blueprint.md)建立連往 DeepSeek-R1 模型的連接器。如需建立連接器的更多資訊，請參閱 [連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。然後直接前往[步驟 4](#step-4-create-and-test-the-model)。

請將以 `your_` 為前綴的預留位置替換為您自己的值。
{: .note}

## 必要條件

開始之前，請先滿足下列必要條件。

設定 Amazon 設定時，僅變更本教學中提到的值。其餘所有設定請維持預設值。
{: .important}

### 將 DeepSeek-R1 部署至 Amazon SageMaker

依照[這篇部落格文章](https://community.aws/content/2sG84dNUCFzA9z4HdfqTI0tcvKP/deploying-deepseek-r1-on-amazon-sagemaker)中的指示，將 DeepSeek-R1 模型部署至 Amazon SageMaker。

記下 Amazon SageMaker DeepSeek-R1 模型的 Amazon Resource Name (ARN) 與 URL；後續步驟會用到。

### 建立 OpenSearch 叢集

前往 [Amazon OpenSearch Service 主控台](https://console.aws.amazon.com/aos/home)並建立 OpenSearch 網域。

記下網域的 ARN 與 URL；後續步驟會用到。

## 步驟 1：建立供 Amazon SageMaker 存取的 IAM 角色

若要在 Amazon SageMaker 中叫用 DeepSeek-R1 模型，您必須建立具有適當權限的 AWS Identity and Access Management (IAM) 角色。連接器將使用此角色來叫用模型。

前往 IAM 主控台，建立名為 `my_invoke_sagemaker_deepseek_model_role` 的新 IAM 角色，並新增下列信任政策與權限：

- 自訂信任政策：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "es.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```
{% include copy.html %}

- 權限：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sagemaker:InvokeEndpoint"
            ],
            "Resource": [
                "your_sagemaker_model_inference_endpoint_arn"
            ]
        }
    ]
}
```
{% include copy.html %}

記下角色 ARN；後續步驟會用到。

## 步驟 2：在 Amazon OpenSearch Service 中設定 IAM 角色

依照下列步驟在 Amazon OpenSearch Service 中設定 IAM 角色。

### 步驟 2.1：建立用於簽署連接器請求的 IAM 角色

產生一個專門用於簽署 Create Connector API 請求的新 IAM 角色。

建立名為 `my_create_sagemaker_deepseek_connector_role` 的 IAM 角色，並附上下列信任政策與權限：

- 自訂信任政策：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "your_iam_user_arn"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
{% include copy.html %}

您將在步驟 3 中使用 `your_iam_user_arn` IAM 使用者來擔任此角色。

- 權限：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "your_iam_role_arn_created_in_step1"
    },
    {
      "Effect": "Allow",
      "Action": "es:ESHttpPost",
      "Resource": "your_opensearch_domain_arn"
    }
  ]
}
```
{% include copy.html %}

記下此角色 ARN；後續步驟會用到。

### 步驟 2.2：對應後端角色

依照下列步驟對應後端角色：

1. 登入 OpenSearch Dashboards，並在頂端選單選取 **Security**。
2. 選取 **Roles**，然後選取 **ml_full_access** 角色。
3. 在 **ml_full_access** 角色詳細資料頁面上，選取 **Mapped users**，然後選取 **Manage mapping**。
4. 在 **Backend roles** 欄位中輸入步驟 2.1 建立的 IAM 角色 ARN，如下圖所示。
    ![對應後端角色]({{site.url}}{{site.baseurl}}/images/vector-search-tutorials/mapping_iam_role_arn.png)
5. 選取 **Map**。

IAM 角色現已成功在您的 OpenSearch 叢集中完成設定。

## 步驟 3：建立連接器

依照下列步驟為 DeepSeek-R1 模型建立連接器。如需建立連接器的更多資訊，請參閱 [連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

使用一次性臨時憑證執行下列 Python 程式碼。

```python
import boto3
import requests 
from requests_aws4auth import AWS4Auth

host = 'your_amazon_opensearch_domain_endpoint'
region = 'your_amazon_opensearch_domain_region'
service = 'es'

assume_role_response = boto3.Session().client('sts').assume_role(
  RoleArn="your_iam_role_arn_created_in_step2.1",
  RoleSessionName="your_session_name"
)
credentials = assume_role_response["Credentials"]
awsauth = AWS4Auth(credentials["AccessKeyId"], credentials["SecretAccessKey"], region, service, session_token=credentials["SessionToken"])


path = '/_plugins/_ml/connectors/_create'
url = host + path

payload = {
  "name": "DeepSeek R1 model connector",
  "description": "Connector for my Sagemaker DeepSeek model",
  "version": "1.0",
  "protocol": "aws_sigv4",
  "credential": {
    "roleArn": "your_iam_role_arn_created_in_step1"
  },
  "parameters": {
    "service_name": "sagemaker",
    "region": "your_sagemaker_model_region",
    "do_sample": true,
    "top_p": 0.9,
    "temperature": 0.7,
    "max_new_tokens": 512
  },
  "actions": [
    {
      "action_type": "PREDICT",
      "method": "POST",
      "url": "your_sagemaker_model_inference_endpoint",
      "headers": {
        "content-type": "application/json"
      },
      "request_body": "{ \"inputs\": \"${parameters.inputs}\", \"parameters\": {\"do_sample\": ${parameters.do_sample}, \"top_p\": ${parameters.top_p}, \"temperature\": ${parameters.temperature}, \"max_new_tokens\": ${parameters.max_new_tokens}} }",
      "post_process_function": "\n      if (params.result == null || params.result.length == 0) {\n        throw new Exception('No response available');\n      }\n      \n      def completion = params.result[0].generated_text;\n      return '{' +\n               '\"name\": \"response\",'+\n               '\"dataAsMap\": {' +\n                  '\"completion\":\"' + escape(completion) + '\"}' +\n             '}';\n    "
    }
  ]
}

headers = {"Content-Type": "application/json"}

r = requests.post(url, auth=awsauth, json=payload, headers=headers)
print(r.status_code)
print(r.text)
```
{% include copy.html %}

指令碼會輸出連接器 ID：

```json
{"connector_id":"HnS5sJQBVQUimUskjpFl"}
```

記下連接器 ID；下一個步驟會用到。

## 步驟 4：建立並測試模型

登入 OpenSearch Dashboards，開啟 DevTools 主控台，並執行下列請求來建立及測試 DeepSeek-R1 模型。

1. 建立模型群組：

    ```json
    POST /_plugins/_ml/model_groups/_register
    {
        "name": "Sagemaker DeepSeek model",
        "description": "Test model group for Sagemaker DeepSeek model"
    }
    ```
    {% include copy-curl.html %}

    回應中包含模型群組 ID：

    ```json
    {
      "model_group_id": "H3S8sJQBVQUimUskW5Fm",
      "status": "CREATED"
    }
    ```

2. 註冊模型：

    ```json
    POST /_plugins/_ml/models/_register
    {
      "name": "Sagemaker DeepSeek R1 model",
      "function_name": "remote",
      "description": "DeepSeek R1 model on Sagemaker",
      "model_group_id": "H3S8sJQBVQUimUskW5Fm",
      "connector_id": "HnS5sJQBVQUimUskjpFl"
    }
    ```
    {% include copy-curl.html %}

    回應中包含模型 ID：

    ```json
    {
      "task_id": "Sim9sJQBts7fa6byEh1S",
      "status": "CREATED",
      "model_id": "Sym9sJQBts7fa6byEh1-"
    }
    ```

3. 部署模型：

    ```json
    POST /_plugins/_ml/models/Sym9sJQBts7fa6byEh1-/_deploy
    ```
    {% include copy-curl.html %}

    回應中包含部署作業的任務 ID：

    ```json
    {
      "task_id": "TCm9sJQBts7fa6byex2j",
      "task_type": "DEPLOY_MODEL",
      "status": "COMPLETED"
    }
    ```

4. 測試模型：

    ```json
    POST /_plugins/_ml/models/Sym9sJQBts7fa6byEh1-/_predict
    {
      "parameters": {
        "inputs": "hello"
      }
    }
    ```
    {% include copy-curl.html %}

    回應中包含模型產生的文字：

    ```json
    {
      "inference_results": [
        {
          "output": [
            {
              "name": "response",
              "dataAsMap": {
                "response": [
                  {
                    "generated_text": """hello<think>

    </think>

    Hello! How can I assist you today? 😊"""
                  }
                ]
              }
            }
          ],
          "status_code": 200
        }
      ]
    }
    ```

## 步驟 5：設定 RAG

請依照下列步驟設定 RAG。

### 步驟 5.1：建立搜尋管線

使用 [RAG 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rag-processor/)建立搜尋管線：

```json
PUT /_search/pipeline/my-conversation-search-pipeline-deepseek
{
  "response_processors": [
    {
      "retrieval_augmented_generation": {
        "tag": "Demo pipeline",
        "description": "Demo pipeline Using DeepSeek R1",
        "model_id": "Sym9sJQBts7fa6byEh1-",
        "context_field_list": [
          "text"
        ],
        "system_prompt": "You are a helpful assistant.",
        "user_instructions": "Generate a concise and informative answer in less than 100 words for the given question"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 5.2：建立向量資料庫

請依照[本教學]({{site.url}}{{site.baseurl}}/search-plugins/neural-search-tutorial/)的步驟 1 和 2 建立嵌入模型與向量索引。接著將範例資料匯入索引：

```json
POST _bulk
{"index": {"_index": "my-nlp-index", "_id": "1"}}
{"text": "Chart and table of population level and growth rate for the Ogden-Layton metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of Ogden-Layton in 2023 is 750,000, a 1.63% increase from 2022.\nThe metro area population of Ogden-Layton in 2022 was 738,000, a 1.79% increase from 2021.\nThe metro area population of Ogden-Layton in 2021 was 725,000, a 1.97% increase from 2020.\nThe metro area population of Ogden-Layton in 2020 was 711,000, a 2.16% increase from 2019."}
{"index": {"_index": "my-nlp-index", "_id": "2"}}
{"text": "Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."}
{"index": {"_index": "my-nlp-index", "_id": "3"}}
{"text": "Chart and table of population level and growth rate for the Chicago metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Chicago in 2023 is 8,937,000, a 0.4% increase from 2022.\\nThe metro area population of Chicago in 2022 was 8,901,000, a 0.27% increase from 2021.\\nThe metro area population of Chicago in 2021 was 8,877,000, a 0.14% increase from 2020.\\nThe metro area population of Chicago in 2020 was 8,865,000, a 0.03% increase from 2019."}
{"index": {"_index": "my-nlp-index", "_id": "4"}}
{"text": "Chart and table of population level and growth rate for the Miami metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Miami in 2023 is 6,265,000, a 0.8% increase from 2022.\\nThe metro area population of Miami in 2022 was 6,215,000, a 0.78% increase from 2021.\\nThe metro area population of Miami in 2021 was 6,167,000, a 0.74% increase from 2020.\\nThe metro area population of Miami in 2020 was 6,122,000, a 0.71% increase from 2019."}
{"index": {"_index": "my-nlp-index", "_id": "5"}}
{"text": "Chart and table of population level and growth rate for the Austin metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Austin in 2023 is 2,228,000, a 2.39% increase from 2022.\\nThe metro area population of Austin in 2022 was 2,176,000, a 2.79% increase from 2021.\\nThe metro area population of Austin in 2021 was 2,117,000, a 3.12% increase from 2020.\\nThe metro area population of Austin in 2020 was 2,053,000, a 3.43% increase from 2019."}
{"index": {"_index": "my-nlp-index", "_id": "6"}}
{"text": "Chart and table of population level and growth rate for the Seattle metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Seattle in 2023 is 3,519,000, a 0.86% increase from 2022.\\nThe metro area population of Seattle in 2022 was 3,489,000, a 0.81% increase from 2021.\\nThe metro area population of Seattle in 2021 was 3,461,000, a 0.82% increase from 2020.\\nThe metro area population of Seattle in 2020 was 3,433,000, a 0.79% increase from 2019."}
```
{% include copy-curl.html %}

### 步驟 5.3：搜尋索引

執行向量搜尋以從向量資料庫擷取文件，並使用 DeepSeek 模型進行 RAG：

```json
GET /my-nlp-index/_search?search_pipeline=my-conversation-search-pipeline-deepseek
{
  "query": {
    "neural": {
      "passage_embedding": {
        "query_text": "What's the population increase of New York City from 2021 to 2023? How is the trending comparing with Miami?",
        "model_id": "USkHsZQBts7fa6bybx3G",
        "k": 5
      }
    }
  },
  "size": 4,
  "_source": [
    "text"
  ],
  "ext": {
    "generative_qa_parameters": {
      "llm_model": "bedrock/claude",
      "llm_question": "What's the population increase of New York City from 2021 to 2023? How is the trending comparing with Miami?",
      "context_size": 5,
      "timeout": 15
    }
  }
}
```
{% include copy-curl.html %}

回應同時包含從向量搜尋擷取的相關文件（位於 `hits` 陣列中）以及 DeepSeek 模型產生的答案（位於 `ext.retrieval_augmented_generation` 物件中）：

```json
{
  "took": 5,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 6,
      "relation": "eq"
    },
    "max_score": 0.05248103,
    "hits": [
      {
        "_index": "my-nlp-index",
        "_id": "2",
        "_score": 0.05248103,
        "_source": {
          "text": """Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."""
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "4",
        "_score": 0.029023321,
        "_source": {
          "text": """Chart and table of population level and growth rate for the Miami metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of Miami in 2023 is 6,265,000, a 0.8% increase from 2022.\nThe metro area population of Miami in 2022 was 6,215,000, a 0.78% increase from 2021.\nThe metro area population of Miami in 2021 was 6,167,000, a 0.74% increase from 2020.\nThe metro area population of Miami in 2020 was 6,122,000, a 0.71% increase from 2019."""
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "3",
        "_score": 0.028097045,
        "_source": {
          "text": """Chart and table of population level and growth rate for the Chicago metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of Chicago in 2023 is 8,937,000, a 0.4% increase from 2022.\nThe metro area population of Chicago in 2022 was 8,901,000, a 0.27% increase from 2021.\nThe metro area population of Chicago in 2021 was 8,877,000, a 0.14% increase from 2020.\nThe metro area population of Chicago in 2020 was 8,865,000, a 0.03% increase from 2019."""
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "6",
        "_score": 0.026973149,
        "_source": {
          "text": """Chart and table of population level and growth rate for the Seattle metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of Seattle in 2023 is 3,519,000, a 0.86% increase from 2022.\nThe metro area population of Seattle in 2022 was 3,489,000, a 0.81% increase from 2021.\nThe metro area population of Seattle in 2021 was 3,461,000, a 0.82% increase from 2020.\nThe metro area population of Seattle in 2020 was 3,433,000, a 0.79% increase from 2019."""
        }
      }
    ]
  },
  "ext": {
    "retrieval_augmented_generation": {
      "answer": """You are a helpful assistant.\nGenerate a concise and informative answer in less than 100 words for the given question\nSEARCH RESULT 1: Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019.\nSEARCH RESULT 2: Chart and table of population level and growth rate for the Miami metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of Miami in 2023 is 6,265,000, a 0.8% increase from 2022.\nThe metro area population of Miami in 2022 was 6,215,000, a 0.78% increase from 2021.\nThe metro area population of Miami in 2021 was 6,167,000, a 0.74% increase from 2020.\nThe metro area population of Miami in 2020 was 6,122,000, a 0.71% increase from 2019.\nSEARCH RESULT 3: Chart and table of population level and growth rate for the Chicago metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of Chicago in 2023 is 8,937,000, a 0.4% increase from 2022.\nThe metro area population of Chicago in 2022 was 8,901,000, a 0.27% increase from 2021.\nThe metro area population of Chicago in 2021 was 8,877,000, a 0.14% increase from 2020.\nThe metro area population of Chicago in 2020 was 8,865,000, a 0.03% increase from 2019.\nSEARCH RESULT 4: Chart and table of population level and growth rate for the Seattle metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of Seattle in 2023 is 3,519,000, a 0.86% increase from 2022.\nThe metro area population of Seattle in 2022 was 3,489,000, a 0.81% increase from 2021.\nThe metro area population of Seattle in 2021 was 3,461,000, a 0.82% increase from 2020.\nThe metro area population of Seattle in 2020 was 3,433,000, a 0.79% increase from 2019.\nQUESTION: What's the population increase of New York City from 2021 to 2023? How is the trending comparing with Miami\nAlright, let's tackle this question step by step. The user is asking for the population increase of New York City from 2021 to 2023 and how this trend compares to Miami's. 

First, I'll look through the search results to find the relevant data. From SEARCH RESULT 1, I see the populations for NYC in 2021, 2022, and 2023. In 2021, it was 18,823,000, and by 2023, it's 18,937,000. That's an increase of 114,000 over two years.

Next, I'll calculate the annual growth rates. From 2021 to 2022, the growth rate was 0.23%, and from 2022 to 2023, it's 0.37%. So, the trend shows an increase in the growth rate each year.

Now, looking at Miami in SEARCH RESULT 2, the population in 2021 was 6,167,000, and in 2023, it's 6,265,000. That's an increase of 98,000 over the same period. The growth rates were 0.74% in 2021-2022 and 0.8% in 2022-2023, also showing an increasing trend but at a higher rate than NYC.

Putting it all together, NYC's population increased by 114,000 with growth rates rising from 0.23% to 0.37%. Miami saw a slightly smaller increase of 98,000 but with higher growth rates, from 0.74% to 0.8%. So, Miami's growth is both higher in absolute terms and has a faster increasing rate compared to NYC.
</think>

The population of New York City increased by 114,000 from 2021 to 2023. The growth rate rose from 0.1% in 2021 to 0.37% in 2023. Comparatively, Miami's population increased by 98,000 during the same period"""
    }
  }
}
```