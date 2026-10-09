---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Amazon Bedrock 上使用 Cohere Embed 的語意搜尋"
parent: Semantic search
grand_parent: Vector search
nav_order: 35
redirect_from:
  - /vector-search/tutorials/semantic-search/semantic-search-bedrock-cohere/
---

# 在 Amazon Bedrock 上使用 Cohere Embed 的語意搜尋

本教學說明如何在 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) 中使用 [Cohere Embed 模型](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-embed.html) 實作語意搜尋。如需更多資訊，請參閱 [語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/semantic-search/)。

如果使用 Python，您可以使用 [`opensearch-py-ml`](https://github.com/opensearch-project/opensearch-py-ml) 用戶端 CLI 建立 Cohere 連接器並測試模型。此 CLI 會自動化許多組態步驟，讓設定更快速並降低出錯的機會。如需使用 CLI 的更多資訊，請參閱 [CLI 文件](https://opensearch-project.github.io/opensearch-py-ml/cli/index.html#)。
{: .tip}

如果使用自行管理的 OpenSearch 而非 Amazon OpenSearch Service，請使用 [藍圖](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/bedrock_connector_cohere_cohere.embed-english-v3_blueprint.md) 建立連接器，連至 Amazon Bedrock 上的模型。如需建立連接器的更多資訊，請參閱 [連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

在 Amazon OpenSearch Service 中設定嵌入模型最簡單的方式，是使用 [AWS CloudFormation](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cfn-template.html)。或者，您也可以使用 [AIConnectorHelper 筆記本](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/tutorials/aws/AIConnectorHelper.ipynb) 設定嵌入模型。
{: .tip}

Amazon Bedrock 有 [配額限制](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html)。如需提高此限制的更多資訊，請參閱 [透過 Amazon Bedrock 的 Provisioned Throughput 提高模型呼叫容量](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html)。
{: .warning}

請將以 `your_` 前綴開頭的預留位置取代為您自己的值。
{: .note}

## 必要條件：建立 OpenSearch 叢集

前往 [Amazon OpenSearch Service 主控台](https://console.aws.amazon.com/aos/home) 並建立 OpenSearch 網域。

記下網域的 Amazon Resource Name (ARN)；您將在後續步驟中使用它。

## 步驟 1：建立 IAM 角色以呼叫 Amazon Bedrock 上的模型

若要呼叫 Amazon Bedrock 上的模型，您必須建立具有適當權限的 AWS Identity and Access Management (IAM) 角色。連接器將使用此角色來呼叫模型。

前往 IAM 主控台，建立名為 `my_invoke_bedrock_cohere_role` 的新 IAM 角色，並新增下列信任政策與權限：

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
            "Resource": "arn:aws:bedrock:*::foundation-model/cohere.embed-english-v3"
        }
    ]
}
```
{% include copy.html %}

如果您需要支援多語言的模型，可以使用 `cohere.embed-multilingual-v3` 模型。
{: .tip}

記下角色 ARN；您將在後續步驟中使用它。

## 步驟 2：在 Amazon OpenSearch Service 中設定 IAM 角色

依照下列步驟在 Amazon OpenSearch Service 中設定 IAM 角色。

### 步驟 2.1：建立用於簽署連接器請求的 IAM 角色

專門產生一個新的 IAM 角色，用於簽署您的 Create Connector API 請求。

建立名為 `my_create_bedrock_cohere_connector_role` 的 IAM 角色，並設定下列信任政策與權限：

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

記下此角色 ARN；您將在後續步驟中使用它。

### 步驟 2.2：對應後端角色

依照下列步驟對應後端角色：

1. 登入 OpenSearch Dashboards，並在頂端選單選取 **Security**。
2. 選取 **Roles**，然後選取 **ml_full_access** 角色。 
3. 在 **ml_full_access** 角色詳細資訊頁面上，選取 **Mapped users**，然後選取 **Manage mapping**。 
4. 在 **Backend roles** 欄位中輸入步驟 2.1 建立的 IAM 角色 ARN，如下圖所示。
    ![對應後端角色]({{site.url}}{{site.baseurl}}/images/vector-search-tutorials/mapping_iam_role_arn.png)
5. 選取 **Map**。 

IAM 角色現已成功在您的 OpenSearch 叢集中完成設定。

## 步驟 3：建立連接器

依照下列步驟為模型建立連接器。如需建立連接器的更多資訊，請參閱 [連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

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
  "name": "Amazon Bedrock Cohere Connector: embedding v3",
  "description": "The connector to Bedrock Cohere embedding model",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "your_bedrock_model_region",
    "service_name": "bedrock",
    "input_type":"search_document",
    "truncate": "END"
  },
  "credential": {
    "roleArn": "your_iam_role_arn_created_in_step1"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://bedrock-runtime.your_bedrock_model_region.amazonaws.com/model/cohere.embed-english-v3/invoke",
      "headers": {
        "content-type": "application/json",
        "x-amz-content-sha256": "required"
      },
      "request_body": "{ \"texts\": ${parameters.texts}, \"truncate\": \"${parameters.truncate}\", \"input_type\": \"${parameters.input_type}\" }",
      "pre_process_function": "connector.pre_process.cohere.embedding",
      "post_process_function": "connector.post_process.cohere.embedding"
    }
  ]
}

headers = {"Content-Type": "application/json"}

r = requests.post(url, auth=awsauth, json=payload, headers=headers)
print(r.text)
```
{% include copy.html %}

如需更多資訊，請參閱 [Cohere 藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/cohere_connector_embedding_blueprint.md)。

指令碼會輸出連接器 ID：

```json
{"connector_id":"1p0u8o0BWbTmLN9F2Y7m"}
```

記下連接器 ID；您將在下一個步驟中使用它。

## 步驟 4：建立並測試模型

登入 OpenSearch Dashboards，開啟 DevTools 主控台，並執行下列請求來建立及測試模型。

1. 建立模型群組：

    ```json
    POST /_plugins/_ml/model_groups/_register
    {
        "name": "Bedrock_embedding_model",
        "description": "Test model group for bedrock embedding model"
    }
    ```
    {% include copy-curl.html %}

    回應包含模型群組 ID：

    ```json
    {
      "model_group_id": "050q8o0BWbTmLN9Foo4f",
      "status": "CREATED"
    }
    ```

2. 註冊模型：

    ```json
    POST /_plugins/_ml/models/_register
    {
      "name": "Bedrock Cohere embedding model v3",
      "function_name": "remote",
      "description": "test embedding model",
      "model_group_id": "050q8o0BWbTmLN9Foo4f",
      "connector_id": "0p0p8o0BWbTmLN9F-o4G"
    }
    ```
    {% include copy-curl.html %}

    回應包含模型 ID：

    ```json
    {
      "task_id": "TRUr8o0BTaDH9c7tSRfx",
      "status": "CREATED",
      "model_id": "VRUu8o0BTaDH9c7t9xet"
    }
    ```

3. 部署模型：

    ```json
    POST /_plugins/_ml/models/VRUu8o0BTaDH9c7t9xet/_deploy
    ```
    {% include copy-curl.html %}

    回應包含部署作業的工作 ID：

    ```json
    {
      "task_id": "1J0r8o0BWbTmLN9FjY6I",
      "task_type": "DEPLOY_MODEL",
      "status": "COMPLETED"
    }
    ```

4. 測試模型：

    ```json
    POST /_plugins/_ml/models/VRUu8o0BTaDH9c7t9xet/_predict
    {
      "parameters": {
        "texts": ["hello world"]
      }
    }
    ```
    {% include copy-curl.html %}

    回應包含模型產生的嵌入：

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
                -0.02973938,
                -0.023651123,
                -0.06021118,
                ...]
            }
          ],
          "status_code": 200
        }
      ]
    }
    ```

## 步驟 5：設定語意搜尋

依照下列步驟設定語意搜尋。

### 步驟 5.1：建立資料匯入管線

首先，建立一個 [資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)，使用 Amazon SageMaker 中的模型從輸入文字產生嵌入：

```json
PUT /_ingest/pipeline/my_bedrock_cohere_embedding_pipeline
{
    "description": "text embedding pipeline",
    "processors": [
        {
            "text_embedding": {
                "model_id": "your_bedrock_embedding_model_id_created_in_step4",
                "field_map": {
                    "text": "text_knn"
                }
            }
        }
    ]
}
```
{% include copy-curl.html %}

### 步驟 5.2：建立向量索引

接著，建立向量索引以儲存輸入文字與產生的嵌入：

```json
PUT my_index
{
  "settings": {
    "index": {
      "knn.space_type": "cosinesimil",
      "default_pipeline": "my_bedrock_cohere_embedding_pipeline",
      "knn": "true"
    }
  },
  "mappings": {
    "properties": {
      "text_knn": {
        "type": "knn_vector",
        "dimension": 1024
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 5.3：匯入資料

將範例文件匯入索引：

```json
POST /my_index/_doc/1000001
{
    "text": "hello world."
}
```
{% include copy-curl.html %}

### 步驟 5.4：搜尋索引

執行向量搜尋以從向量索引擷取文件：

```json
POST /my_index/_search
{
  "query": {
    "neural": {
      "text_knn": {
        "query_text": "hello",
        "model_id": "your_embedding_model_id_created_in_step4",
        "k": 100
      }
    }
  },
  "size": "1",
  "_source": ["text"]
}
```
{% include copy-curl.html %}