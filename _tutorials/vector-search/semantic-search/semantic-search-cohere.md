---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Cohere Embed 的語意搜尋"
parent: Semantic search
grand_parent: Vector search
nav_order: 30
redirect_from:
  - /vector-search/tutorials/semantic-search/semantic-search-cohere/
---

# 使用 Cohere Embed 的語意搜尋

本教學說明如何在 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) 中使用 [Cohere Embed 模型](https://docs.cohere.com/reference/embed) 實作語意搜尋。如需更多資訊，請參閱[語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/semantic-search/)。

如果使用 Python，您可以使用 [`opensearch-py-ml`](https://github.com/opensearch-project/opensearch-py-ml) 用戶端 CLI 來建立 Cohere 連接器並測試模型。此 CLI 會自動化許多組態步驟，讓設定更快速並減少出錯的機會。如需使用 CLI 的更多資訊，請參閱 [CLI 文件](https://opensearch-project.github.io/opensearch-py-ml/cli/index.html#)。
{: .tip}

如果使用自我管理的 OpenSearch 而非 Amazon OpenSearch Service，請使用[藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/cohere_connector_embedding_blueprint.md)建立連至 Cohere Embed 模型的連接器。如需建立連接器的更多資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

在 Amazon OpenSearch Service 中設定嵌入模型最簡單的方式是使用 [AWS CloudFormation](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cfn-template.html)。或者，您也可以使用 [AIConnectorHelper 筆記本](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/tutorials/aws/AIConnectorHelper.ipynb) 來設定嵌入模型。
{: .tip}

Cohere Embed 模型也在 Amazon Bedrock 上提供。若要使用託管於 Amazon Bedrock 的模型，請參閱[在 Amazon Bedrock 上使用 Cohere Embed 模型的語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/tutorials/semantic-search/semantic-search-bedrock-cohere/)。

請將以 `your_` 前綴開頭的預留位置替換為您自己的值。
{: .note}

## 先決條件：建立 OpenSearch 叢集

前往 [Amazon OpenSearch Service 主控台](https://console.aws.amazon.com/aos/home)並建立 OpenSearch 網域。

請記下網域的 Amazon Resource Name (ARN)；您將在後續步驟中使用它。

## 步驟 1：將 API 金鑰存放在 AWS Secrets Manager

將您的 Cohere API 金鑰存放在 [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)：

1. 開啟 AWS Secrets Manager。
1. 選取 **Store a new secret**。
1. 選取 **Other type of secret**。
1. 建立鍵值對，以 **my_cohere_key** 作為鍵，並以您的 Cohere API 金鑰作為值。
1. 將您的秘密命名為 `my_test_cohere_secret`。

請記下秘密的 ARN；您將在後續步驟中使用它。

## 步驟 2：建立 IAM 角色

若要使用步驟 1 中建立的秘密，您必須建立一個具有該秘密讀取權限的 AWS Identity and Access Management (IAM) 角色。此 IAM 角色將在連接器中設定，並允許連接器讀取該秘密。

前往 IAM 主控台，建立名為 `my_cohere_secret_role` 的新 IAM 角色，並新增下列信任政策與權限：

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

請記下角色的 ARN；您將在後續步驟中使用它。

## 步驟 3：在 Amazon OpenSearch Service 中設定 IAM 角色

依照下列步驟在 Amazon OpenSearch Service 中設定 IAM 角色。

### 步驟 3.1：建立用於簽署連接器請求的 IAM 角色

產生一個專門用於簽署 Create Connector API 請求的新 IAM 角色。

建立名為 `my_create_connector_role` 的 IAM 角色，並使用下列信任政策與權限：

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

您將在步驟 4 中使用 `your_iam_user_arn` IAM 使用者來擔任此角色。

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
            "Resource": "your_opensearch_domain_arn_created"
        }
    ]
}
```
{% include copy.html %}

請記下此角色的 ARN；您將在後續步驟中使用它。

### 步驟 3.2：對應後端角色

依照下列步驟對應後端角色：

1. 登入 OpenSearch Dashboards，並在頂端選單選取 **Security**。
2. 選取 **Roles**，然後選取 **ml_full_access** 角色。 
3. 在 **ml_full_access** 角色詳細資訊頁面上，選取 **Mapped users**，然後選取 **Manage mapping**。 
4. 在 **Backend roles** 欄位中輸入步驟 3.1 中建立的 IAM 角色 ARN，如下圖所示。
    ![對應後端角色]({{site.url}}{{site.baseurl}}/images/vector-search-tutorials/mapping_iam_role_arn.png)
4. 選取 **Map**。 

IAM 角色現已成功在您的 OpenSearch 叢集中設定。

## 步驟 4：建立連接器

依照下列步驟為模型建立連接器。如需建立連接器的更多資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

使用從 AWS 取得的暫時憑證執行下列 Python 程式碼。
 
```python
import boto3
import requests 
from requests_aws4auth import AWS4Auth

host = 'your_amazon_opensearch_domain_endpoint_created'
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
  "name": "cohere-embed-v3",
  "description": "The connector to public Cohere model service for embed",
  "version": "1",
  "protocol": "http",
  "credential": {
    "secretArn": "your_secret_arn_created_in_step1",
    "roleArn": "your_iam_role_arn_created_in_step2"
  },
  "parameters": {
    "model": "embed-english-v3.0",
    "input_type":"search_document",
    "truncate": "END"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://api.cohere.ai/v1/embed",
      "headers": {
        "Authorization": "Bearer ${credential.secretArn.my_cohere_key}",
        "Request-Source": "unspecified:opensearch"
      },
      "request_body": "{ \"texts\": ${parameters.texts}, \"truncate\": \"${parameters.truncate}\", \"model\": \"${parameters.model}\", \"input_type\": \"${parameters.input_type}\" }",
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

此指令碼會輸出連接器 ID：

```json
{"connector_id":"qp2QP40BWbTmLN9Fpo40"}
```

請記下連接器 ID；您將在下一個步驟中使用它。

## 步驟 5：建立並測試模型

登入 OpenSearch Dashboards，開啟 DevTools 主控台，然後執行下列請求以建立並測試模型。

1. 建立模型群組：

    ```json
    POST /_plugins/_ml/model_groups/_register
    {
        "name": "Cohere_embedding_model",
        "description": "Test model group for cohere embedding model"
    }
    ```
    {% include copy-curl.html %}

    回應中包含模型群組 ID：

    ```json
    {
      "model_group_id": "KEqTP40BOhavBOmfXikp",
      "status": "CREATED"
    }
    ```

2. 註冊模型：

    ```json
    POST /_plugins/_ml/models/_register
    {
      "name": "cohere embedding model v3",
      "function_name": "remote",
      "description": "test embedding model",
      "model_group_id": "KEqTP40BOhavBOmfXikp",
      "connector_id": "qp2QP40BWbTmLN9Fpo40"
    }
    ```
    {% include copy-curl.html %}

    回應中包含模型 ID：

    ```json
    {
      "task_id": "q52VP40BWbTmLN9F9I5S",
      "status": "CREATED",
      "model_id": "MErAP40BOhavBOmfQCkf"
    }
    ```

3. 部署模型：

    ```json
    POST /_plugins/_ml/models/MErAP40BOhavBOmfQCkf/_deploy
    ```
    {% include copy-curl.html %}

    回應中包含部署作業的工作 ID：

    ```json
    {
      "task_id": "KUqWP40BOhavBOmf4Clx",
      "task_type": "DEPLOY_MODEL",
      "status": "COMPLETED"
    }
    ```

4. 測試模型：

    ```json
    POST /_plugins/_ml/models/MErAP40BOhavBOmfQCkf/_predict
    {
      "parameters": {
        "texts": ["hello world", "how are you"]
      }
    }
    ```
    {% include copy-curl.html %}

    回應中包含模型產生的嵌入：

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
                -0.029510498,
                -0.023223877,
                -0.059631348,
                ...]
            },
            {
              "name": "sentence_embedding",
              "data_type": "FLOAT32",
              "shape": [
                1024
              ],
              "data": [
                0.02279663,
                0.014976501,
                -0.04058838,]
            }
          ],
          "status_code": 200
        }
      ]
    }
    ```

## 步驟 6：設定語意搜尋

請依照下列步驟設定語意搜尋。

### 步驟 6.1：建立資料匯入管線

首先，建立一個[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)，使用模型從輸入文字產生嵌入：

```json
PUT /_ingest/pipeline/my_cohere_embedding_pipeline
{
    "description": "text embedding pipeline",
    "processors": [
        {
            "text_embedding": {
                "model_id": "your_cohere_embedding_model_id_created_in_step5",
                "field_map": {
                    "text": "text_knn"
                }
            }
        }
    ]
}
```
{% include copy-curl.html %}

### 步驟 6.2：建立向量索引

接著，建立向量索引以儲存輸入文字和產生的嵌入：

```json
PUT my_index
{
  "settings": {
    "index": {
      "knn.space_type": "cosinesimil",
      "default_pipeline": "my_cohere_embedding_pipeline",
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

### 步驟 6.3：匯入資料

將範例文件匯入索引：

```json
POST /my_index/_doc/1000001
{
    "text": "hello world."
}
```
{% include copy-curl.html %}

### 步驟 6.4：搜尋索引

執行向量搜尋以從向量索引擷取文件：

```json
POST /my_index/_search
{
  "query": {
    "neural": {
      "text_knn": {
        "query_text": "hello",
        "model_id": "your_embedding_model_id_created_in_step5",
        "k": 100
      }
    }
  },
  "size": "1",
  "_source": ["text"]
}
```
{% include copy-curl.html %}