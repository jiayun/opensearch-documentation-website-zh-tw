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

若要從 Jupyter notebook 執行本教學的步驟，請使用 [DeepSeek RAG 示範 notebook](https://github.com/opensearch-project/ml-commons/blob/main/docs/tutorials/aws/DeepSeek_demo_notebook_for_RAG.ipynb)。

如果您使用的是自行管理的 OpenSearch 而非 Amazon OpenSearch Service，請使用[該藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/deepseek_connector_chat_blueprint.md)建立連接至 DeepSeek-R1 模型的連接器。如需建立連接器的更多資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。然後直接前往[步驟 4](#step-4-create-and-test-the-model)。

請將以 `your_` 為前綴的預留位置替換為您自己的值。
{: .note}

## 先決條件

開始之前，請先完成下列先決條件。

設定 Amazon 設定時，請只變更本教學提及的值。其他所有設定請維持預設值。
{: .important}

### 取得 Amazon Bedrock 上 DeepSeek-R1 的存取權

DeepSeek-R1 是 Amazon Bedrock 上的無伺服器模型。您可以透過跨區域推論設定檔 `us.deepseek.r1-v1:0` 呼叫它，該設定檔會將請求路由至 `us-east-1`、`us-east-2` 和 `us-west-2` 區域中的 `deepseek.r1-v1:0` 模型。如需詳細資訊，請參閱 [Amazon Bedrock 支援的基礎模型](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) 和 [使用跨區域推論提高輸送量](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)。

請記下推論設定檔的 Amazon Resource Name (ARN)，其格式為 `arn:aws:bedrock:your_bedrock_model_region:your_aws_account_id:inference-profile/us.deepseek.r1-v1:0`；您將在後續步驟中使用它。

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
            "Resource": [
                "your_DeepSeek_R1_inference_profile_ARN",
                "arn:aws:bedrock:*::foundation-model/deepseek.r1-v1:0"
            ]
        }
    ]
}
```
{% include copy.html %}

此角色需要具備推論設定檔，以及設定檔所路由請求之各個區域中基礎模型的權限。

請記下角色 ARN；您將在後續步驟中使用它。

## 步驟 2：在 Amazon OpenSearch Service 中設定 IAM 角色

請依照下列步驟在 Amazon OpenSearch Service 中設定 IAM 角色。

### 步驟 2.1：建立用於簽署連接器請求的 IAM 角色

專門為簽署您的 Create Connector API 請求產生一個新的 IAM 角色。

建立一個名為 `my_create_bedrock_deepseek_connector_role` 的 IAM 角色，並使用下列信任政策與權限：

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
      "Resource": "your_opensearch_domain_arn/*"
    }
  ]
}
```
{% include copy.html %}

請記下此角色的 ARN；您將在後續步驟中使用它。

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

請依照下列步驟為 DeepSeek-R1 模型建立連接器。如需建立連接器的詳細資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

使用從 AWS 取得的臨時認證資訊執行下列 Python 程式碼。

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
    "model_id": "us.deepseek.r1-v1:0",
    "temperature": 0,
    "max_tokens": 4000
  },
  "actions": [
    {
      "action_type": "PREDICT",
      "method": "POST",
      "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model_id}/invoke",
      "headers": {
        "content-type": "application/json"
      },
      "request_body": "{ \"prompt\": \"<｜begin▁of▁sentence｜><｜User｜>${parameters.inputs}<｜Assistant｜>\", \"temperature\": ${parameters.temperature}, \"max_tokens\": ${parameters.max_tokens} }",
      "post_process_function": "\n      return '{' +\n               '\"name\": \"response\",'+\n               '\"dataAsMap\": {' +\n                  '\"completion\":\"' + escape(params.choices[0].text) + '\"}' +\n             '}';\n    "
    }
  ]
}

headers = {"Content-Type": "application/json"}

r = requests.post(url, auth=awsauth, json=payload, headers=headers)
print(r.status_code)
print(r.text)
```
{% include copy.html %}

將 `region` 設定為可使用 `us.deepseek.r1-v1:0` 推論設定檔的區域。連接器會將請求傳送至該區域的 Amazon Bedrock 端點。

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

首先，建立嵌入模型。Amazon OpenSearch Service 不支援本機模型，因此請使用外部託管的嵌入模型：依照[使用 Amazon Bedrock Titan 進行語意搜尋]({{site.url}}{{site.baseurl}}/tutorials/vector-search/semantic-search/semantic-search-bedrock-titan/)中的步驟 1--4 操作。在自行管理的 OpenSearch 中，您也可以改用本機模型，如[語意與混合搜尋入門]({{site.url}}{{site.baseurl}}/tutorials/vector-search/neural-search-tutorial/)所述。

建立資料匯入管線，使用嵌入模型從 `text` 欄位產生嵌入：

```json
PUT /_ingest/pipeline/my-nlp-ingest-pipeline
{
  "description": "text embedding pipeline",
  "processors": [
    {
      "text_embedding": {
        "model_id": "your_embedding_model_id",
        "field_map": {
          "text": "passage_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

建立使用此管線的向量索引。`dimension` 必須與嵌入模型的輸出維度相符，Amazon Bedrock Titan Text Embeddings 模型的輸出維度為 1,536：

```json
PUT /my-nlp-index
{
  "settings": {
    "index": {
      "default_pipeline": "my-nlp-ingest-pipeline",
      "knn": "true"
    }
  },
  "mappings": {
    "properties": {
      "passage_embedding": {
        "type": "knn_vector",
        "dimension": 1536,
        "space_type": "cosinesimil"
      },
      "text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

將範例資料匯入索引：

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
        "model_id": "your_embedding_model_id",
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

回應包含從向量搜尋擷取到的相關文件（位於 `hits` 陣列中），以及 DeepSeek 模型產生的答案（位於 `ext.retrieval_augmented_generation` 物件中）：

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
    "max_score": 0.85223955,
    "hits": [
      {
        "_index": "my-nlp-index",
        "_id": "2",
        "_score": 0.85223955,
        "_source": {
          "text": "Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "4",
        "_score": 0.7766204,
        "_source": {
          "text": "Chart and table of population level and growth rate for the Miami metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Miami in 2023 is 6,265,000, a 0.8% increase from 2022.\\nThe metro area population of Miami in 2022 was 6,215,000, a 0.78% increase from 2021.\\nThe metro area population of Miami in 2021 was 6,167,000, a 0.74% increase from 2020.\\nThe metro area population of Miami in 2020 was 6,122,000, a 0.71% increase from 2019."
        }
      }
    ]
  },
  "ext": {
    "retrieval_augmented_generation": {
      "answer": """<think>
Okay, let's tackle this question. The user wants to know the population increase of New York City from 2021 to 2023 and compare the trend with Miami.

...
</think>

New York City's metro population increased by 114,000 from 2021 (18,823,000) to 2023 (18,937,000), with growth rates rising from 0.1% to 0.37%. Miami's metro population grew by 98,000 in the same period (6,167,000 to 6,265,000), but its growth rates were consistently higher (0.74% to 0.8%). While NYC saw a larger absolute increase due to its bigger size, Miami experienced faster percentage growth, reflecting a stronger upward trend. NYC's growth rebounded after a near-stable 2020, whereas Miami maintained steady, robust annual increases."""
    }
  }
}
```

## 相關文件

- [使用 RAG 的對話式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/conversational-search/)
- [第三方 ML 平台的連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)
- [檢索增強生成處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rag-processor/)
- [文字嵌入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-embedding/)
- [Neural 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural/)
