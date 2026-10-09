---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 DeepSeek Chat API 的 RAG"
parent: RAG
grand_parent: Generative AI
nav_order: 120
redirect_from:
  - /vector-search/tutorials/rag/rag-deepseek-chat/
  - /tutorials/vector-search/rag/rag-deepseek-chat/
---

# 使用 DeepSeek Chat API 的 RAG

本教學說明如何使用 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) 與 [DeepSeek 聊天模型](https://api-docs.deepseek.com/api/create-chat-completion) 實作檢索增強生成 (RAG)。

如果您使用自行管理的 OpenSearch 而非 Amazon OpenSearch Service，請取得 DeepSeek API 金鑰，並使用[藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/deepseek_connector_chat_blueprint.md)建立與 DeepSeek 聊天模型的連接器。如需建立連接器的詳細資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。接著直接前往[步驟 5](#step-5-create-and-test-the-model)。

請將以 `your_` 為前綴的預留位置替換為您自己的值。
{: .note}

## 先決條件

開始之前，請先完成下列先決條件。

設定 Amazon 設定時，請只變更本教學提到的值。其他所有設定請維持預設值。
{: .important}

### 取得 DeepSeek API 金鑰

如果您還沒有 DeepSeek API 金鑰，請在開始本教學之前先取得一個。

### 建立 OpenSearch 叢集

前往 [Amazon OpenSearch Service 主控台](https://console.aws.amazon.com/aos/home) 並建立 OpenSearch 網域。

請記下網域的 Amazon Resource Name (ARN) 與 URL；您將在後續步驟中使用它們。

## 步驟 1：將 API 金鑰儲存在 AWS Secrets Manager 中

將您的 DeepSeek API 金鑰儲存在 [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)：

1. 開啟 AWS Secrets Manager。
1. 選取 **Store a new secret**。
1. 選取 **Other type of secret**。
1. 建立索引鍵-值配對，索引鍵為 **my_deepseek_key**，值為您的 DeepSeek API 金鑰。
1. 將您的秘密命名為 `my_test_deepseek_secret`。

請記下秘密 ARN；您將在後續步驟中使用它。

## 步驟 2：建立 IAM 角色

若要使用步驟 1 建立的秘密，您必須建立具有該秘密讀取權限的 AWS Identity and Access Management (IAM) 角色。此 IAM 角色將在連接器中設定，並允許連接器讀取該秘密。

前往 IAM 主控台，建立名為 `my_deepseek_secret_role` 的新 IAM 角色，並新增下列信任政策與權限：

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
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Effect": "Allow",
      "Resource": "your_secret_arn_created_in_step1"
    }
  ]
}
```
{% include copy.html %}

請記下角色 ARN；您將在後續步驟中使用它。

## 步驟 3：在 Amazon OpenSearch Service 中設定 IAM 角色

請依照下列步驟在 Amazon OpenSearch Service 中設定 IAM 角色。

### 步驟 3.1：建立用於簽署連接器請求的 IAM 角色

產生新的 IAM 角色，專門用於簽署您的 Create Connector API 請求。

建立名為 `my_create_deepseek_connector_role` 的 IAM 角色，並使用下列信任政策與權限：

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

您將在步驟 4 中使用 `your_iam_user_arn` IAM 使用者來擔任該角色。

- 權限：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "your_iam_role_arn_created_in_step2"
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

### 步驟 3.2：對應後端角色

請依照下列步驟對應後端角色：

1. 登入 OpenSearch Dashboards，並在頂端選單選取 **Security**。
2. 選取 **Roles**，然後選取 **ml_full_access** 角色。
3. 在 **ml_full_access** 角色詳細資料頁面中，選取 **Mapped users**，然後選取 **Manage mapping**。
4. 在 **Backend roles** 欄位中輸入步驟 3.1 建立的 IAM 角色 ARN，如下圖所示。
    ![對應後端角色]({{site.url}}{{site.baseurl}}/images/vector-search-tutorials/mapping_iam_role_arn.png)
4. 選取 **Map**。

IAM 角色現已成功設定於您的 OpenSearch 叢集中。

## 步驟 4：建立連接器

請依照下列步驟建立 DeepSeek 聊天模型的連接器。如需建立連接器的詳細資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

- 將 DeepSeek API 端點新增至信任的 URL 清單：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.ml_commons.trusted_connector_endpoints_regex": [
      """^https://api\.deepseek\.com/.*$"""
    ]
  }
}
```
{% include copy-curl.html %}

- 使用從 AWS 取得的臨時憑證執行下列 Python 程式碼。
 
```python
import boto3
import requests 
from requests_aws4auth import AWS4Auth

host = 'your_amazon_opensearch_domain_endpoint'
region = 'your_amazon_opensearch_domain_region'
service = 'es'

assume_role_response = boto3.Session().client('sts').assume_role(
  RoleArn="your_iam_role_arn_created_in_step3.1",
  RoleSessionName="your_session_name"
)
credentials = assume_role_response["Credentials"]
awsauth = AWS4Auth(credentials["AccessKeyId"], credentials["SecretAccessKey"], region, service, session_token=credentials["SessionToken"])

path = '/_plugins/_ml/connectors/_create'
url = host + path

payload = {
  "name": "DeepSeek Chat",
  "description": "Test connector for DeepSeek Chat",
  "version": "1",
  "protocol": "http",
  "parameters": {
    "endpoint": "api.deepseek.com",
    "model": "deepseek-chat"
  },
  "credential": {
    "secretArn": "your_secret_arn_created_in_step1",
    "roleArn": "your_iam_role_arn_created_in_step2"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://${parameters.endpoint}/v1/chat/completions",
      "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer ${credential.secretArn.my_deepseek_key}"
      },
      "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": ${parameters.messages} }"
    }
  ]
}

headers = {"Content-Type": "application/json"}

r = requests.post(url, auth=awsauth, json=payload, headers=headers)
print(r.status_code)
print(r.text)
```
{% include copy.html %}

該指令碼會輸出連接器 ID：

```json
{"connector_id":"duRJsZQBFSAM-WcznrIw"}
```

請記下連接器 ID；您將在下一個步驟中使用它。

## 步驟 5：建立並測試模型

登入 OpenSearch Dashboards，開啟 Dev Tools 主控台，並執行下列請求以建立及測試 DeepSeek 聊天模型。

1. 建立模型群組：

    ```json
    POST /_plugins/_ml/model_groups/_register
    {
      "name": "DeepSeek Chat model",
      "description": "Test model group for DeepSeek model"
    }
    ```
    {% include copy-curl.html %}

    回應包含模型群組 ID：

    ```json
    {
      "model_group_id": "UylKsZQBts7fa6byEx2M",
      "status": "CREATED"
    }
    ```

1. 註冊模型：

    ```json
    POST /_plugins/_ml/models/_register
    {
      "name": "DeepSeek Chat model",
      "function_name": "remote",
      "description": "DeepSeek Chat model",
      "model_group_id": "UylKsZQBts7fa6byEx2M",
      "connector_id": "duRJsZQBFSAM-WcznrIw"
    }
    ```
    {% include copy-curl.html %}

    回應包含模型 ID：

    ```json
    {
      "task_id": "VClKsZQBts7fa6bypR0a",
      "status": "CREATED",
      "model_id": "VSlKsZQBts7fa6bypR02"
    }
    ```

1. 部署模型：

    ```json
    POST /_plugins/_ml/models/VSlKsZQBts7fa6bypR02/_deploy
    ```
    {% include copy-curl.html %}

    回應包含部署作業的工作 ID：

    ```json
    {
      "task_id": "d-RKsZQBFSAM-Wcz3bKO",
      "task_type": "DEPLOY_MODEL",
      "status": "COMPLETED"
    }
    ```

1. 測試模型：

    ```json
    POST /_plugins/_ml/models/VSlKsZQBts7fa6bypR02/_predict
    {
      "parameters": {
        "messages": [
          {
            "role": "system",
            "content": "You are a helpful assistant."
          },
          {
            "role": "user",
            "content": "Hello!"
          }
        ]
      }
    }
    ```
    {% include copy-curl.html %}

    回應包含模型產生的文字：

    ```json
    {
      "inference_results": [
        {
          "output": [
            {
              "name": "response",
              "dataAsMap": {
                "id": "a351252c-7393-4c5d-9abe-1c47693ad336",
                "object": "chat.completion",
                "created": 1738141298,
                "model": "deepseek-chat",
                "choices": [
                  {
                    "index": 0,
                    "message": {
                      "role": "assistant",
                      "content": "Hello! How can I assist you today? 😊"
                    },
                    "logprobs": null,
                    "finish_reason": "stop"
                  }
                ],
                "usage": {
                  "prompt_tokens": 11,
                  "completion_tokens": 11,
                  "total_tokens": 22,
                  "prompt_tokens_details": {
                    "cached_tokens": 0
                  },
                  "prompt_cache_hit_tokens": 0,
                  "prompt_cache_miss_tokens": 11
                },
                "system_fingerprint": "fp_3a5770e1b4"
              }
            }
          ],
          "status_code": 200
        }
      ]
    }
    ```

## 步驟 6：設定 RAG

依照下列步驟設定 RAG。

### 步驟 6.1：建立搜尋管線

使用 [RAG 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rag-processor/) 建立搜尋管線：

```json
PUT /_search/pipeline/my-conversation-search-pipeline-deepseek-chat
{
  "response_processors": [
    {
      "retrieval_augmented_generation": {
        "tag": "Demo pipeline",
        "description": "Demo pipeline Using DeepSeek Chat",
        "model_id": "VSlKsZQBts7fa6bypR02",
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

### 步驟 6.2：建立向量資料庫

依照[本教學]({{site.url}}{{site.baseurl}}/search-plugins/neural-search-tutorial/)的步驟 1 和 2 建立嵌入模型與向量索引。然後將範例資料匯入索引：

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

### 步驟 6.3：搜尋索引

執行向量搜尋以從向量資料庫擷取文件，並使用 DeepSeek 模型進行 RAG：

```json
GET /my-nlp-index/_search?search_pipeline=my-conversation-search-pipeline-deepseek-chat
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
      "llm_model": "deepseek-chat",
      "llm_question": "What's the population increase of New York City from 2021 to 2023? How is the trending comparing with Miami?",
      "context_size": 5,
      "timeout": 15
    }
  }
}
```
{% include copy-curl.html %}

回應同時包含從向量搜尋擷取的相關文件（位於 `hits` 陣列中），以及由 DeepSeek 模型產生的答案（位於 `ext.retrieval_augmented_generation` 物件中）：

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
      "answer": "From 2021 to 2023, New York City's metro area population increased by 114,000, from 18,823,000 to 18,937,000, reflecting a growth rate of 0.61%. In comparison, Miami's metro area population grew by 98,000, from 6,167,000 to 6,265,000, with a higher growth rate of 1.59%. While New York City has a larger absolute population increase, Miami's population growth rate is significantly higher, indicating faster relative growth."
    }
  }
}
```