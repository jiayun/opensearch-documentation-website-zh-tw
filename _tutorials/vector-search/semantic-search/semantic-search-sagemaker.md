---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Amazon SageMaker 中進行語意搜尋"
parent: Semantic search
grand_parent: Vector search
nav_order: 60
redirect_from:
  - /vector-search/tutorials/semantic-search/semantic-search-sagemaker/
---

# 使用 Amazon SageMaker 中的模型進行語意搜尋

本教學說明如何在 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) 中使用 Amazon SageMaker 的嵌入模型來實作語意搜尋。如需更多資訊，請參閱[語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/semantic-search/)。

如果您使用 Python，可以建立 Amazon SageMaker 連接器，並使用 [`opensearch-py-ml`](https://github.com/opensearch-project/opensearch-py-ml) 用戶端 CLI 測試模型。CLI 會自動執行許多組態步驟，讓設定更快速並降低出錯的機會。如需使用 CLI 的詳細資訊，請參閱 [CLI 文件](https://opensearch-project.github.io/opensearch-py-ml/cli/index.html#)。
{: .tip}

如果您使用自我管理的 OpenSearch 而非 Amazon OpenSearch Service，請使用[藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/sagemaker_connector_blueprint.md)建立 Amazon SageMaker 中模型的連接器。如需建立連接器的詳細資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

本教學不涵蓋如何將模型部署至 Amazon SageMaker。如需部署的詳細資訊，請參閱[即時推論](https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html)。

在 Amazon OpenSearch Service 中設定嵌入模型最簡單的方式是使用 [AWS CloudFormation](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cfn-template.html)。或者，您也可以使用 [AIConnectorHelper 筆記本](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/tutorials/aws/AIConnectorHelper.ipynb) 設定嵌入模型。
{: .tip}

請將開頭為前置字元 `your_` 的預留位置取代為您自己的值。
{: .note}

## 模型輸入與輸出需求

請確保 Amazon SageMaker 中模型的輸入符合[預設前處理函式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#preprocessing-function)所需的格式。

模型輸入必須是字串陣列：

```json
["hello world", "how are you"]
```

此外，請確保模型輸出符合[預設後處理函式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#post-processing-function)所需的格式。模型輸出必須是陣列的陣列，其中每個內部陣列對應一個輸入字串的嵌入：

```json
[
  [
    -0.048237994,
    -0.07612697,
    ...
  ],
  [
    0.32621247,
    0.02328475,
    ...
  ]
]
```

如果您的模型輸入/輸出與所需的預設值不同，您可以使用 [Painless 指令碼]({{site.url}}{{site.baseurl}}/scripting/painless/)建立自己的前處理/後處理函式。

### 範例：Amazon Bedrock Titan 嵌入模型

例如，Amazon Bedrock Titan 嵌入模型（[藍圖](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/bedrock_connector_titan_embedding_blueprint.md#2-create-connector-for-amazon-bedrock)）的輸入如下：

```json
{ "inputText": "your_input_text" }
```

OpenSearch 預期的輸入格式如下：

```json
{ "text_docs": [ "your_input_text1", "your_input_text2"] }
```

若要將 `text_docs` 轉換為 `inputText`，您必須定義下列前處理函式：

```json
"pre_process_function": """
    StringBuilder builder = new StringBuilder();
    builder.append("\"");
    String first = params.text_docs[0];// Get the first doc, ml-commons will iterate all docs
    builder.append(first);
    builder.append("\"");
    def parameters = "{" +"\"inputText\":" + builder + "}"; // This is the Bedrock Titan embedding model input
    return  "{" +"\"parameters\":" + parameters + "}";"""
```
{% include copy.html %}

Amazon Bedrock Titan 嵌入模型的預設輸出格式如下：

```json
{
  "embedding": <float_array>
}
```

然而，OpenSearch 預期的格式如下：

```json
{
  "name": "sentence_embedding",
  "data_type": "FLOAT32",
  "shape": [ <embedding_size> ],
  "data": <float_array>
}
```

若要將 Amazon Bedrock Titan 嵌入模型的輸出轉換為 OpenSearch 預期的格式，您必須定義下列後處理函式：

```json
"post_process_function": """
      def name = "sentence_embedding";
      def dataType = "FLOAT32";
      if (params.embedding == null || params.embedding.length == 0) {
        return params.message;
      }
      def shape = [params.embedding.length];
      def json = "{" +
                 "\"name\":\"" + name + "\"," +
                 "\"data_type\":\"" + dataType + "\"," +
                 "\"shape\":" + shape + "," +
                 "\"data\":" + params.embedding +
                 "}";
      return json;
    """
```
{% include copy.html %}

## 先決條件：建立 OpenSearch 叢集

前往 [Amazon OpenSearch Service 主控台](https://console.aws.amazon.com/aos/home)並建立 OpenSearch 網域。

請記下網域的 Amazon Resource Name (ARN)；您將在後續步驟中使用它。

## 步驟 1：建立 IAM 角色以叫用 Amazon SageMaker 中的模型

若要叫用 Amazon SageMaker 中的模型，您必須建立具有適當權限的 AWS Identity and Access Management (IAM) 角色。連接器將使用此角色來叫用模型。

前往 IAM 主控台，建立名為 `my_invoke_sagemaker_model_role` 的新 IAM 角色，並新增下列信任政策和權限：

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

請記下角色 ARN；您將在後續步驟中使用它。

## 步驟 2：在 Amazon OpenSearch Service 中設定 IAM 角色

請依照下列步驟在 Amazon OpenSearch Service 中設定 IAM 角色。

### 步驟 2.1：建立 IAM 角色以簽署連接器請求

產生新的 IAM 角色，專門用於簽署您的 Create Connector API 請求。

建立名為 `my_create_sagemaker_connector_role` 的 IAM 角色，並使用下列信任政策和權限：

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

依照下列步驟對應後端角色：

1. 登入 OpenSearch Dashboards，並在頂端選單選取 **Security**。
2. 選取 **Roles**，然後選取 **ml_full_access** 角色。
3. 在 **ml_full_access** 角色詳細資料頁面上，選取 **Mapped users**，然後選取 **Manage mapping**。
4. 在 **Backend roles** 欄位中輸入在步驟 2.1 建立的 IAM 角色 ARN，如下圖所示。
    ![對應後端角色]({{site.url}}{{site.baseurl}}/images/vector-search-tutorials/mapping_iam_role_arn.png)
5. 選取 **Map**。

IAM 角色現已成功設定在您的 OpenSearch 叢集中。

## 步驟 3：建立連接器

依照下列步驟為模型建立連接器。如需建立連接器的更多資訊，請參閱 [連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

使用從 AWS 取得的暫時憑證執行下列 Python 程式碼。
 
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
  "name": "Sagemaker embedding model connector",
  "description": "Connector for my Sagemaker embedding model",
  "version": "1.0",
  "protocol": "aws_sigv4",
  "credential": {
    "roleArn": "your_iam_role_arn_created_in_step1"
  },
  "parameters": {
    "region": "your_sagemaker_model_region",
    "service_name": "sagemaker"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "headers": {
        "content-type": "application/json"
      },
      "url": "your_sagemaker_model_inference_endpoint",
      "request_body": "${parameters.input}",
      "pre_process_function": "connector.pre_process.default.embedding",
      "post_process_function": "connector.post_process.default.embedding"
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
{"connector_id":"tZ09Qo0BWbTmLN9FM44V"}
```

請記下連接器 ID；您會在下一個步驟中使用它。

## 步驟 4：建立並測試模型

登入 OpenSearch Dashboards，開啟 DevTools 主控台，並執行下列請求來建立及測試模型。

1. 建立模型群組：

    ```json
    POST /_plugins/_ml/model_groups/_register
    {
        "name": "Sagemaker_embedding_model",
        "description": "Test model group for Sagemaker embedding model"
    }
    ```
    {% include copy-curl.html %}

    回應包含模型群組 ID：

    ```json
    {
      "model_group_id": "MhU3Qo0BTaDH9c7tKBfR",
      "status": "CREATED"
    }
    ```

2. 註冊模型：

    ```json
    POST /_plugins/_ml/models/_register
    {
      "name": "Sagemaker embedding model",
      "function_name": "remote",
      "description": "test embedding model",
      "model_group_id": "MhU3Qo0BTaDH9c7tKBfR",
      "connector_id": "tZ09Qo0BWbTmLN9FM44V"
    }
    ```
    {% include copy-curl.html %}

    回應包含模型 ID：

    ```json
    {
      "task_id": "NhU9Qo0BTaDH9c7t0xft",
      "status": "CREATED",
      "model_id": "NxU9Qo0BTaDH9c7t1Bca"
    }
    ```

3. 部署模型：

    ```json
    POST /_plugins/_ml/models/NxU9Qo0BTaDH9c7t1Bca/_deploy
    ```
    {% include copy-curl.html %}

    回應包含部署作業的工作 ID：

    ```json
    {
      "task_id": "MxU4Qo0BTaDH9c7tJxde",
      "task_type": "DEPLOY_MODEL",
      "status": "COMPLETED"
    }
    ```

4. 測試模型：

    ```json
    POST /_plugins/_ml/models/NxU9Qo0BTaDH9c7t1Bca/_predict
    {
      "parameters": {
        "input": ["hello world", "how are you"]
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
                384
              ],
              "data": [
                -0.034477264,
                0.031023195,
                0.0067349933,
                ...]
            },
            {
              "name": "sentence_embedding",
              "data_type": "FLOAT32",
              "shape": [
                384
              ],
              "data": [
                -0.031369038,
                0.037830487,
                0.07630822,
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

首先，建立使用 Amazon SageMaker 中模型從輸入文字產生嵌入的[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)：

```json
PUT /_ingest/pipeline/my_sagemaker_embedding_pipeline
{
    "description": "text embedding pipeline",
    "processors": [
        {
            "text_embedding": {
                "model_id": "your_sagemaker_embedding_model_id_created_in_step4",
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

接著，建立用於儲存輸入文字與所產生嵌入的向量索引：

```json
PUT my_index
{
  "settings": {
    "index": {
      "knn.space_type": "cosinesimil",
      "default_pipeline": "my_sagemaker_embedding_pipeline",
      "knn": "true"
    }
  },
  "mappings": {
    "properties": {
      "text_knn": {
        "type": "knn_vector",
        "dimension": your_sagemake_model_embedding_dimension
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