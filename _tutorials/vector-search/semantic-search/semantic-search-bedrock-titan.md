---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Amazon Bedrock Titan 的語意搜尋"
parent: Semantic search
grand_parent: Vector search
nav_order: 40
redirect_from:
  - /vector-search/tutorials/semantic-search/semantic-search-bedrock-titan/
---

# 使用 Amazon Bedrock Titan 的語意搜尋

本教學說明如何在 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) 中使用 [Amazon Bedrock Titan 嵌入模型](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html) 實作語意搜尋。如需更多資訊，請參閱[語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/semantic-search/)。

如果使用 Python，您可以透過 [`opensearch-py-ml`](https://github.com/opensearch-project/opensearch-py-ml) 用戶端 CLI 建立 Amazon Bedrock Titan 嵌入連接器並測試模型。此 CLI 會自動化許多組態步驟，讓設定更快速並降低出錯的機會。如需使用 CLI 的更多資訊，請參閱 [CLI 文件](https://opensearch-project.github.io/opensearch-py-ml/cli/index.html#)。
{: .tip}

如果使用自行管理的 OpenSearch 而非 Amazon OpenSearch Service，請使用[藍圖](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/bedrock_connector_titan_embedding_blueprint.md)建立連接至 Amazon Bedrock 上模型的連接器。如需建立連接器的更多資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

在 Amazon OpenSearch Service 中設定嵌入模型最簡單的方式是使用 [AWS CloudFormation](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cfn-template.html)。或者，您也可以使用 [AIConnectorHelper notebook](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/tutorials/aws/AIConnectorHelper.ipynb) 來設定嵌入模型。
{: .tip}

Amazon Bedrock 有[配額限制](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html)。如需提高此限制的更多資訊，請參閱 [Increase model invocation capacity with Provisioned Throughput in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html)。
{: .warning}

請將以 `your_` 前綴開頭的預留位置替換為您自己的值。
{: .note}

## 必要條件：建立 OpenSearch 叢集

前往 [Amazon OpenSearch Service 主控台](https://console.aws.amazon.com/aos/home)並建立 OpenSearch 網域。

記下網域的 Amazon Resource Name (ARN)；您會在後續步驟中使用它。

## 步驟 1：建立 IAM 角色以呼叫 Amazon Bedrock 上的模型

若要呼叫 Amazon Bedrock 上的模型，您必須建立具有適當權限的 AWS Identity and Access Management (IAM) 角色。連接器將使用此角色來呼叫模型。

前往 IAM 主控台，建立名為 `my_invoke_bedrock_role` 的新 IAM 角色，並新增下列信任政策與權限：

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
            "Resource": "arn:aws:bedrock:*::foundation-model/amazon.titan-embed-text-v1"
        }
    ]
}
```
{% include copy.html %}

記下角色 ARN；您會在後續步驟中使用它。

## 步驟 2：在 OpenSearch 中設定 IAM 角色

依照下列步驟在 Amazon OpenSearch Service 中設定 IAM 角色。

### 步驟 2.1：建立 IAM 角色以簽署連接器請求

產生一個專門用於簽署 Create Connector API 請求的新 IAM 角色。

建立名為 `my_create_bedrock_connector_role` 的 IAM 角色，並設定下列信任政策與權限：

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

您會在步驟 3 中使用 `your_iam_user_arn` IAM 使用者來擔任此角色。

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
            "Resource": "your_opensearch_domain_arn_created"
        }
    ]
}
```
{% include copy.html %}

記下此角色 ARN；您會在後續步驟中使用它。

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
  RoleArn="your_iam_role_arn_created_in_step2.1",
  RoleSessionName="your_session_name"
)
credentials = assume_role_response["Credentials"]
awsauth = AWS4Auth(credentials["AccessKeyId"], credentials["SecretAccessKey"], region, service, session_token=credentials["SessionToken"])

path = '/_plugins/_ml/connectors/_create'
url = host + path

payload = {
  "name": "Amazon Bedrock Connector: titan embedding v1",
  "description": "The connector to bedrock Titan embedding model",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "your_bedrock_model_region",
    "service_name": "bedrock"
  },
  "credential": {
    "roleArn": "your_iam_role_arn_created_in_step1"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://bedrock-runtime.your_bedrock_model_region.amazonaws.com/model/amazon.titan-embed-text-v1/invoke",
      "headers": {
        "content-type": "application/json",
        "x-amz-content-sha256": "required"
      },
      "request_body": "{ \"inputText\": \"${parameters.inputText}\" }",
      "pre_process_function": "\n    StringBuilder builder = new StringBuilder();\n    builder.append(\"\\\"\");\n    String first = params.text_docs[0];\n    builder.append(first);\n    builder.append(\"\\\"\");\n    def parameters = \"{\" +\"\\\"inputText\\\":\" + builder + \"}\";\n    return  \"{\" +\"\\\"parameters\\\":\" + parameters + \"}\";",
      "post_process_function": "\n      def name = \"sentence_embedding\";\n      def dataType = \"FLOAT32\";\n      if (params.embedding == null || params.embedding.length == 0) {\n        return params.message;\n      }\n      def shape = [params.embedding.length];\n      def json = \"{\" +\n                 \"\\\"name\\\":\\\"\" + name + \"\\\",\" +\n                 \"\\\"data_type\\\":\\\"\" + dataType + \"\\\",\" +\n                 \"\\\"shape\\\":\" + shape + \",\" +\n                 \"\\\"data\\\":\" + params.embedding +\n                 \"}\";\n      return json;\n    "
    }
  ]
}

headers = {"Content-Type": "application/json"}

r = requests.post(url, auth=awsauth, json=payload, headers=headers)
print(r.text)
```
{% include copy.html %}

指令碼會輸出連接器 ID：

```json
{"connector_id":"1p0u8o0BWbTmLN9F2Y7m"}
```

記下連接器 ID；您會在下一步中使用它。

## 步驟 4：建立並測試模型

登入 OpenSearch Dashboards，開啟 DevTools 主控台，然後執行下列請求以建立並測試模型。

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
      "model_group_id": "LxWiQY0BTaDH9c7t9xeE",
      "status": "CREATED"
    }
    ```

2. 註冊模型：

    ```json
    POST /_plugins/_ml/models/_register
    {
      "name": "bedrock titan embedding model v1",
      "function_name": "remote",
      "description": "test embedding model",
      "model_group_id": "LxWiQY0BTaDH9c7t9xeE",
      "connector_id": "N0qpQY0BOhavBOmfOCnw"
    }
    ```
    {% include copy-curl.html %}

    回應包含模型 ID：

    ```json
    {
      "task_id": "O0q3QY0BOhavBOmf1SmL",
      "status": "CREATED",
      "model_id": "PEq3QY0BOhavBOmf1Sml"
    }
    ```

3. 部署模型：

    ```json
    POST /_plugins/_ml/models/PEq3QY0BOhavBOmf1Sml/_deploy
    ```
    {% include copy-curl.html %}

    回應包含部署作業的工作 ID：

    ```json
    {
      "task_id": "PUq4QY0BOhavBOmfBCkQ",
      "task_type": "DEPLOY_MODEL",
      "status": "COMPLETED"
    }
    ```

4. 測試模型：

    ```json
    POST /_plugins/_ml/models/PEq3QY0BOhavBOmf1Sml/_predict
    {
      "parameters": {
        "inputText": "hello world"
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
                1536
              ],
              "data": [
                0.7265625,
                -0.0703125,
                0.34765625,
                ...]
            }
          ],
          "status_code": 200
        }
      ]
    }
    ```

## 步驟 5：設定語意搜尋

請依照下列步驟設定語意搜尋。

### 步驟 5.1：建立資料匯入管線

首先，建立一個[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)，使用 Amazon SageMaker 中的模型從輸入文字產生嵌入：

```json
PUT /_ingest/pipeline/my_bedrock_embedding_pipeline
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

接著，建立向量索引以儲存輸入文字和產生的嵌入：

```json
PUT my_index
{
  "settings": {
    "index": {
      "knn.space_type": "cosinesimil",
      "default_pipeline": "my_bedrock_embedding_pipeline",
      "knn": "true"
    }
  },
  "mappings": {
    "properties": {
      "text_knn": {
        "type": "knn_vector",
        "dimension": 1536
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