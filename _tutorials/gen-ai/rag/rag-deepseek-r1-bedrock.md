---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Amazon Bedrock 上使用 DeepSeek-R1 的 RAG"
parent: RAG
grand_parent: Generative AI
nav_order: 130
redirect_from:
  - /vector-search/tutorials/rag/rag-deepseek-r1-bedrock/
  - /tutorials/vector-search/rag/rag-deepseek-r1-bedrock/
---

# 在 Amazon Bedrock 上使用 DeepSeek-R1 的 RAG

本教學說明如何使用 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) 與 [DeepSeek-R1 模型](https://huggingface.co/deepseek-ai/DeepSeek-R1) 實作檢索增強生成 (RAG)。

如果您使用自行管理的 OpenSearch 而非 Amazon OpenSearch Service，請使用[藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/deepseek_connector_chat_blueprint.md)建立與 DeepSeek-R1 模型的連接器。如需建立連接器的詳細資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。接著直接前往[步驟 4](#step-4-create-and-test-the-model)。

請將開頭為前綴 `your_` 的預留位置替換為您自己的值。
{: .note}

## 先決條件

開始之前，請先完成下列先決條件。

設定 Amazon 設定時，請只變更本教學提及的值。其他所有設定請維持預設值。
{: .important}

### 將 DeepSeek-R1 部署至 Amazon Bedrock

在 Amazon Bedrock 上部署 DeepSeek-R1。如需詳細資訊，請參閱 [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)。請記下 Amazon Bedrock DeepSeek-R1 模型的 Amazon Resource Name (ARN)；您將在後續步驟中使用它。

### 建立 OpenSearch 叢集

前往 [Amazon OpenSearch Service 主控台](https://console.aws.amazon.com/aos/home)並建立 OpenSearch 網域。

請記下網域 ARN 與 URL；您將在後續步驟中使用它們。

## 步驟 1：建立用於存取 Amazon Bedrock 的 IAM 角色

若要在 Amazon Bedrock 上叫用 DeepSeek-R1 模型，您必須建立具有適當權限的 AWS Identity and Access Management (IAM) 角色。連接器將使用此角色來叫用模型。

前往 IAM 主控台，建立名為 `my_invoke_bedrock_deepseek_model_role` 的新 IAM 角色，並新增下列信任政策與權限：

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
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Effect": "Allow",
            "Resource": "your_DeepSeek_R1_model_ARN"
        }
    ]
}
```
{% include copy.html %}

請記下角色 ARN；您將在後續步驟中使用它。

## 步驟 2：在 Amazon OpenSearch Service 中設定 IAM 角色

請依照下列步驟在 Amazon OpenSearch Service 中設定 IAM 角色。

### 步驟 2.1：建立用於簽署連接器請求的 IAM 角色

產生新的 IAM 角色，專門用於簽署您的 Create Connector API 請求。

建立名為 `my_create_bedrock_deepseek_connector_role` 的 IAM 角色，並設定下列信任政策與權限：

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

您將在步驟 3 中使用 `your_iam_user_arn` IAM 使用者來擔任該角色。

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

請記下此角色 ARN；您將在後續步驟中使用它。

### 步驟 2.2：對應後端角色

請依照下列步驟對應後端角色：

1. 登入 OpenSearch Dashboards，並在頂端選單選取 **Security**。
2. 選取 **Roles**，然後選取 **ml_full_access** 角色。 
3. 在 **ml_full_access** 角色詳細資料頁面中，選取 **Mapped users**，然後選取 **Manage mapping**。 
4. 在 **Backend roles** 欄位中輸入步驟 2.1 建立的 IAM 角色 ARN，如下圖所示。
    ![對應後端角色]({{site.url}}{{site.baseurl}}/images/vector-search-tutorials/mapping_iam_role_arn.png)
5. 選取 **Map**。 

IAM 角色現已成功設定於您的 OpenSearch 叢集中。

## 步驟 3：建立連接器

請依照下列步驟建立 DeepSeek-R1 模型的連接器。如需建立連接器的詳細資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

使用從 AWS 取得的臨時憑證執行下列 Python 程式碼。

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
  "description": "Connector for my Bedrock DeepSeek model",
  "version": "1.0",
  "protocol": "aws_sigv4",
  "credential": {
    "roleArn": "your_iam_role_arn_created_in_step1"
  },
  "parameters": {
    "service_name": "bedrock",
    "region": "your_bedrock_model_region",
    "model_id": "your_deepseek_bedrock_model_arn",
    "temperature": 0,
    "max_gen_len": 4000
  },
  "actions": [
    {
      "action_type": "PREDICT",
      "method": "POST",
      "url": "https://bedrock-runtime.us-east-1.amazonaws.com/model/${parameters.model_id}/invoke",
      "headers": {
        "content-type": "application/json"
      },
      "request_body": "{ \"prompt\": \"<｜begin▁of▁sentence｜><｜User｜>${parameters.inputs}<｜Assistant｜>\", \"temperature\": ${parameters.temperature}, \"max_gen_len\": ${parameters.max_gen_len} }",
      "post_process_function": "\n      return '{' +\n               '\"name\": \"response\",'+\n               '\"dataAsMap\": {' +\n                  '\"completion\":\"' + escape(params.generation) + '\"}' +\n             '}';\n    "
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

請記下連接器 ID；您將在下一個步驟中使用它。

## 步驟 4：建立並測試模型

登入 OpenSearch Dashboards，開啟 DevTools 主控台，然後執行下列請求以建立並測試 DeepSeek-R1 模型。

1. 建立模型群組：

    ```json
    POST /_plugins/_ml/model_groups/_register
    {
        "name": "Bedrock DeepSeek model",
        "description": "Test model group for Bedrock DeepSeek model"
    }
    ```
    {% include copy-curl.html %}

    回應包含模型群組 ID：

    ```json
    {
      "model_group_id": "Vylgs5QBts7fa6bylR0v",
      "status": "CREATED"
    }
    ```

2. 註冊模型：

    ```json
    POST /_plugins/_ml/models/_register
    {
      "name": "Bedrock DeepSeek R1 model",
      "function_name": "remote",
      "description": "DeepSeek R1 model on Bedrock",
      "model_group_id": "Vylgs5QBts7fa6bylR0v",
      "connector_id": "KHS7s5QBVQUimUskoZGp"
    }
    ```
    {% include copy-curl.html %}

    回應包含模型 ID：

    ```json
    {
      "task_id": "hOS7s5QBFSAM-Wczv7KD",
      "status": "CREATED",
      "model_id": "heS7s5QBFSAM-Wczv7Kb"
    }
    ```

3. 部署模型：

    ```json
    POST /_plugins/_ml/models/heS7s5QBFSAM-Wczv7Kb/_deploy
    ```
    {% include copy-curl.html %}

    回應包含部署作業的工作 ID：

    ```json
    {
      "task_id": "euRhs5QBFSAM-WczTrI6",
      "task_type": "DEPLOY_MODEL",
      "status": "COMPLETED"
    }
    ```

4. 測試模型：

    ```json
    POST /_plugins/_ml/models/heS7s5QBFSAM-Wczv7Kb/_predict
    {
      "parameters": {
        "inputs": "hello"
      }
    }
    ```
    {% include copy-curl.html %}

    回應包含模型生成的文字：

    ```json
    {
      "inference_results": [
        {
          "output": [
            {
              "name": "response",
              "dataAsMap": {
                "completion": """<think>\n\n</think>\n\nHello! How can I assist you today? 😊"""
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

建立包含 [RAG 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rag-processor/)的搜尋管線：

```json
PUT /_search/pipeline/my-conversation-search-pipeline-deepseek
{
  "response_processors": [
    {
      "retrieval_augmented_generation": {
        "tag": "Demo pipeline",
        "description": "Demo pipeline Using DeepSeek R1",
        "model_id": "heS7s5QBFSAM-Wczv7Kb",
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

依照[此教學]({{site.url}}{{site.baseurl}}/search-plugins/neural-search-tutorial/)的步驟 1 和 2，建立嵌入模型和向量索引。接著將範例資料匯入索引：

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

執行向量搜尋，從向量資料庫擷取文件，並使用 DeepSeek 模型進行 RAG：

```json
GET /my-nlp-index/_search?search_pipeline=my-conversation-search-pipeline-deepseek
{
  "query": {
    "neural": {
      "passage_embedding": {
        "query_text": "What's the population increase of New York City from 2021 to 2023? How is the trending comparing with Miami?",
        "model_id": "heS7s5QBFSAM-Wczv7Kb",
        "k": 5
      }
    }
  },
  "size": 2,
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

回應包含從向量搜尋擷取的相關文件（位於 `hits` 陣列中），以及 DeepSeek 模型產生的答案（位於 `ext.retrieval_augmented_generation` 物件中）：

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
    "max_score": 0.04107812,
    "hits": [
      {
        "_index": "my-nlp-index",
        "_id": "4",
        "_score": 0.04107812,
        "_source": {
          "text": """Chart and table of population level and growth rate for the Miami metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of Miami in 2023 is 6,265,000, a 0.8% increase from 2022.\nThe metro area population of Miami in 2022 was 6,215,000, a 0.78% increase from 2021.\nThe metro area population of Miami in 2021 was 6,167,000, a 0.74% increase from 2020.\nThe metro area population of Miami in 2020 was 6,122,000, a 0.71% increase from 2019."""
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "2",
        "_score": 0.03810156,
        "_source": {
          "text": """Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."""
        }
      }
    ]
  },
  "ext": {
    "retrieval_augmented_generation": {
      "answer": """You are a helpful assistant.\nGenerate a concise and informative answer in less than 100 words for the given question\nSEARCH RESULT 1: Chart and table of population level and growth rate for the Miami metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of Miami in 2023 is 6,265,000, a 0.8% increase from 2022.\nThe metro area population of Miami in 2022 was 6,215,000, a 0.78% increase from 2021.\nThe metro area population of Miami in 2021 was 6,167,000, a 0.74% increase from 2020.\nThe metro area population of Miami in 2020 was 6,122,000, a 0.71% increase from 2019.\nSEARCH RESULT 2: Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019.\nQUESTION: What's the population increase of New York City from 2021 to 2023? How is the trending comparing with Miami?\nOkay, I need to figure out the population increase of New York City from 2021 to 2023 and compare it with Miami's growth. Let me start by looking at the data provided.

From SEARCH RESULT 2, in 2021, NYC's population was 18,823,000, and in 2022, it was 18,867,000. Then in 2023, it's 18,937,000. So, from 2021 to 2022, it increased by 44,000, and from 2022 to 2023, it went up by 70,000. Adding those together, the total increase from 2021 to 2023 is 114,000.

Now, looking at Miami's data in SEARCH RESULT 1, in 2021, the population was 6,167,000, and in 2023, it's 6,265,000. That's an increase of 98,000 over the same period. 

Comparing the two, NYC's increase is higher than Miami's. NYC went up by 114,000, while Miami was 98,000. Also, NYC's growth rate is a bit lower than Miami's. NYC's average annual growth rate is around 0.37%, whereas Miami's is about 0.75%. So, while NYC's population increased more in total, Miami's growth rate is higher. I should present this clearly, highlighting both the total increase and the growth rates to show the comparison accurately.
</think>

From 2021 to 2023, New York City's population increased by 114,000, compared to Miami's increase of 98,000. While NYC's total growth is higher, Miami's annual growth rate (0.75%) is notably faster than NYC's (0.37%)."""
    }
  }
}
```