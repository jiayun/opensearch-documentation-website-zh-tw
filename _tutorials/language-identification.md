---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "語言識別"
nav_order: 65
---

# 為多語言搜尋識別文件語言

若要搜尋多種語言的文字，您可以將每種語言編製索引到各自擁有語言分析器的欄位中。本教學說明如何使用 [ML 推論匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/ml-inference/)，在匯入期間偵測文字欄位的語言，並將每個欄位複製到特定語言的欄位。本教學使用託管於 Amazon SageMaker 的 [Hugging Face `papluca/xlm-roberta-base-language-detection`](https://huggingface.co/papluca/xlm-roberta-base-language-detection) 文字分類模型，適用於自行管理的 OpenSearch 與 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/)。

請將開頭為前置詞 `your_` 的預留位置替換為您自己的值。
{: .note}

## 先決條件：將模型部署至 Amazon SageMaker

若要將模型部署至 SageMaker 端點，請在 SageMaker 筆記本中執行下列 Python 程式碼。此程式碼使用 SageMaker Python SDK 2.x，您可以執行 `pip install "sagemaker<3"` 來安裝：

```python
import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel

try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client('iam')
    # Replace with your SageMaker execution role name if different
    role = iam.get_role(RoleName='sagemaker_execution_role')['Role']['Arn']

# Hub model configuration from Hugging Face
hub = {
    'HF_MODEL_ID':'papluca/xlm-roberta-base-language-detection',
    'HF_TASK':'text-classification'
}

# Create a Hugging Face model class
huggingface_model = HuggingFaceModel(
    transformers_version='4.37.0',
    pytorch_version='2.1.0',
    py_version='py310',
    env=hub,
    role=role,
)

# Deploy the model to SageMaker Inference
predictor = huggingface_model.deploy(
    initial_instance_count=1,
    instance_type='ml.m5.large'
)

print(f"SageMaker Endpoint Name: {predictor.endpoint_name}")

# Test the model
prediction = predictor.predict({
    "inputs": "I like you. I love you",
})
print(prediction)
```
{% include copy.html %}

如果您在 SageMaker 筆記本之外執行程式碼，`sagemaker.get_execution_role()` 會傳回您目前登入所用的 IAM 角色（若有）。在此情況下，請將 `role` 設為您的 SageMaker 執行角色 ARN。

請記下輸出中的端點名稱；您將在下一個步驟中使用它來建立連接器。您也可以在 SageMaker 主控台的 **Inference** > **Endpoints** 中找到端點名稱。

## 步驟 1：建立連接器

連接器組態取決於您執行 OpenSearch 的位置。在自行管理的 OpenSearch 中，連接器會使用 AWS 存取金鑰簽署對 SageMaker 的請求。在 Amazon OpenSearch Service 中，連接器會使用 AWS Identity and Access Management (IAM) 角色。請依照您平台適用的步驟操作。

### 選項 1：自行管理的 OpenSearch

請依照下列步驟在自行管理的 OpenSearch 中建立連接器。

#### 步驟 1.1：建立 IAM 使用者

建立具有程式設計存取權的 IAM 使用者，並附加下列政策，允許該使用者叫用 SageMaker 端點：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sagemaker:InvokeEndpoint",
            "Resource": "arn:aws:sagemaker:your_aws_region:your_aws_account_id:endpoint/your_sagemaker_endpoint_name"
        }
    ]
}
```
{% include copy.html %}

為該使用者產生存取金鑰與私密金鑰。

#### 步驟 1.2：建立連接器

若要建立使用 IAM 使用者認證資訊的連接器，請傳送下列請求：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "SageMaker language identification model connector",
  "description": "Connector for a language identification model in SageMaker",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "access_key": "your_aws_access_key",
    "secret_key": "your_aws_secret_key",
    "session_token": "your_aws_session_token"
  },
  "parameters": {
    "region": "your_aws_region",
    "service_name": "sagemaker"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://runtime.sagemaker.${parameters.region}.amazonaws.com/endpoints/your_sagemaker_endpoint_name/invocations",
      "headers": {
        "content-type": "application/json"
      },
      "request_body": "{ \"inputs\": \"${parameters.inputs}\" }"
    }
  ]
}
```
{% include copy-curl.html %}

`session_token` 僅在臨時認證資訊時為必要。如果您使用 IAM 使用者的存取金鑰，請省略 `session_token`。

回應中包含連接器 ID：

```json
{
  "connector_id": "bLYgeJEBXV92Z6od5rXM"
}
```

請記下連接器 ID；您將在[步驟 2](#step-2-register-and-deploy-the-model) 中使用它。

### 選項 2：Amazon OpenSearch Service

請依照下列步驟在 Amazon OpenSearch Service 中建立連接器。

#### 步驟 1.1：建立 IAM 角色以叫用模型

前往 IAM 主控台，建立名為 `my_invoke_sagemaker_model_role` 的新 IAM 角色，並新增下列信任政策與權限。連接器會使用此角色叫用模型：

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
            "Action": "sagemaker:InvokeEndpoint",
            "Resource": "arn:aws:sagemaker:your_aws_region:your_aws_account_id:endpoint/your_sagemaker_endpoint_name"
        }
    ]
}
```
{% include copy.html %}

請記下角色 ARN；您將在後續步驟中使用它。

#### 步驟 1.2：建立 IAM 角色以簽署連接器請求

建立名為 `my_create_sagemaker_connector_role` 的 IAM 角色，用於簽署您的 Create Connector API 請求。新增下列信任政策與權限：

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

您將在步驟 1.4 中使用 `your_iam_user_arn` IAM 使用者來擔任該角色。

- 權限：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "your_iam_role_arn_created_in_step1.1"
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

#### 步驟 1.3：對應後端角色

請依照下列步驟對應後端角色：

1. 登入 OpenSearch Dashboards，並在頂端功能表選取 **Security**。
2. 選取 **Roles**，然後選取 **ml_full_access** 角色。
3. 在 **ml_full_access** 角色詳細資料頁面中，選取 **Mapped users**，然後選取 **Manage mapping**。
4. 在 **Backend roles** 欄位中輸入步驟 1.2 建立的 IAM 角色 ARN，如下圖所示。
    ![對應後端角色]({{site.url}}{{site.baseurl}}/images/vector-search-tutorials/mapping_iam_role_arn.png)
5. 選取 **Map**。

#### 步驟 1.4：建立連接器

若要建立連接器，請執行下列 Python 程式碼。此程式碼會擔任步驟 1.2 中建立的角色，並使用該角色的臨時認證資訊簽署請求：

```python
import boto3
import requests
from requests_aws4auth import AWS4Auth

host = 'your_amazon_opensearch_domain_endpoint'
region = 'your_amazon_opensearch_domain_region'
service = 'es'

assume_role_response = boto3.Session().client('sts').assume_role(
  RoleArn="your_iam_role_arn_created_in_step1.2",
  RoleSessionName="your_session_name"
)
credentials = assume_role_response["Credentials"]
awsauth = AWS4Auth(credentials["AccessKeyId"], credentials["SecretAccessKey"], region, service, session_token=credentials["SessionToken"])

path = '/_plugins/_ml/connectors/_create'
url = host + path

payload = {
  "name": "SageMaker language identification model connector",
  "description": "Connector for a language identification model in SageMaker",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "roleArn": "your_iam_role_arn_created_in_step1.1"
  },
  "parameters": {
    "region": "your_sagemaker_model_region",
    "service_name": "sagemaker"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://runtime.sagemaker.${parameters.region}.amazonaws.com/endpoints/your_sagemaker_endpoint_name/invocations",
      "headers": {
        "content-type": "application/json"
      },
      "request_body": "{ \"inputs\": \"${parameters.inputs}\" }"
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
{"connector_id":"bLYgeJEBXV92Z6od5rXM"}
```

請記下連接器 ID；您將在下一個步驟中使用它。

## 步驟 2：註冊並部署模型

若要使用步驟 1 中的連接器 ID 註冊並部署模型，請傳送下列請求：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "SageMaker language identification model",
  "function_name": "remote",
  "description": "Remote model for language identification",
  "connector_id": "bLYgeJEBXV92Z6od5rXM"
}
```
{% include copy-curl.html %}

回應包含模型 ID：

```json
{
  "task_id": "hbYheJEBXV92Z6oda7Xb",
  "status": "CREATED",
  "model_id": "hrYheJEBXV92Z6oda7X7"
}
```

請記下模型 ID；您將在後續步驟中使用它。

## 步驟 3：測試模型

若要測試模型，請傳送下列請求：

```json
POST /_plugins/_ml/models/hrYheJEBXV92Z6oda7X7/_predict
{
  "parameters": {
    "inputs": "Say this is a test"
  }
}
```
{% include copy-curl.html %}

回應中的 `label` 欄位包含偵測到的語言，`score` 欄位則包含信賴分數。標籤位於 `dataAsMap` 物件中的 `response[0].label` 路徑；您將在資料匯入管線中使用此路徑：

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
                "label": "en",
                "score": 0.9411176443099976
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

模型會傳回語言代號，例如 `en`、`de` 和 `es`。如需模型可偵測的語言清單，請參閱[模型卡](https://huggingface.co/papluca/xlm-roberta-base-language-detection)。

## 步驟 4：建立資料匯入管線

建立資料匯入管線，偵測 `name` 和 `notes` 欄位的語言，並將每個欄位複製到對應語言的欄位，例如 `name_en` 或 `notes_de`。此管線包含下列處理器：

- 一個 `ml_inference` 處理器，針對每個欄位呼叫模型。`input_map` 和 `output_map` 陣列會依序處理：第一個 `input_map` 物件對應第一個 `output_map` 物件，因此兩個陣列必須包含相同數量的物件。處理器會針對每個 `input_map` 物件呼叫模型一次，並將偵測到的語言儲存在 `predicted_name_language` 和 `predicted_notes_language` 欄位中。
- 兩個 [`copy` 處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/copy/)，將 `name` 和 `notes` 欄位複製到名稱包含偵測到的語言的目標欄位。`target_field` 使用[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)插入偵測到的語言。

若要建立管線，請傳送下列請求：

```json
PUT /_ingest/pipeline/language_identification_pipeline
{
  "description": "Ingest pipeline to identify language and create language-specific fields",
  "processors": [
    {
      "ml_inference": {
        "model_id": "hrYheJEBXV92Z6oda7X7",
        "input_map": [
          {
            "inputs": "name"
          },
          {
            "inputs": "notes"
          }
        ],
        "output_map": [
          {
            "predicted_name_language": "response[0].label"
          },
          {
            "predicted_notes_language": "response[0].label"
          }
        ]
      }
    },
    {
      "copy": {
        "source_field": "name",
        "target_field": "name_{% raw %}{{predicted_name_language}}{% endraw %}",
        "ignore_missing": true
      }
    },
    {
      "copy": {
        "source_field": "notes",
        "target_field": "notes_{% raw %}{{predicted_notes_language}}{% endraw %}",
        "ignore_missing": true
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 步驟 5：建立索引

建立預設使用此資料匯入管線的索引。索引對應會為管線針對英文、西班牙文和德文文字建立的各個語言專屬欄位指派語言分析器。如需詳細資訊，請參閱[語言分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/index/)：

```json
PUT /task_index
{
  "settings": {
    "index": {
      "default_pipeline": "language_identification_pipeline"
    }
  },
  "mappings": {
    "properties": {
      "name_en": { "type": "text", "analyzer": "english" },
      "name_es": { "type": "text", "analyzer": "spanish" },
      "name_de": { "type": "text", "analyzer": "german" },
      "notes_en": { "type": "text", "analyzer": "english" },
      "notes_es": { "type": "text", "analyzer": "spanish" },
      "notes_de": { "type": "text", "analyzer": "german" }
    }
  }
}
```
{% include copy-curl.html %}

如果模型偵測到的語言在對應中沒有欄位，OpenSearch 會使用動態對應建立該欄位，而動態對應會使用標準分析器。若要分析其他語言的文字，請將這些語言的欄位新增至對應中。
{: .note}

## 步驟 6：匯入文件

將英文、德文和西班牙文文件匯入索引：

```json
POST _bulk
{ "index": { "_index": "task_index", "_id": "1" } }
{ "name": "Buy catnip", "notes": "Mittens really likes the stuff from Humboldt." }
{ "index": { "_index": "task_index", "_id": "2" } }
{ "name": "Kaufen Sie Katzenminze", "notes": "Mittens mag die Sachen von Humboldt wirklich." }
{ "index": { "_index": "task_index", "_id": "3" } }
{ "name": "comprar hierba gatera", "notes": "A Mittens le gustan mucho las cosas de Humboldt." }
```
{% include copy-curl.html %}

若要驗證管線是否偵測到語言，請擷取德文文件：

```json
GET /task_index/_doc/2
```
{% include copy-curl.html %}

文件包含偵測到的語言，以及該語言專屬的 `name_de` 和 `notes_de` 欄位：

```json
{
  "_index": "task_index",
  "_id": "2",
  "_version": 1,
  "_seq_no": 1,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "predicted_notes_language": "de",
    "notes": "Mittens mag die Sachen von Humboldt wirklich.",
    "notes_de": "Mittens mag die Sachen von Humboldt wirklich.",
    "predicted_name_language": "de",
    "name_de": "Kaufen Sie Katzenminze",
    "name": "Kaufen Sie Katzenminze"
  }
}
```

英文文件包含 `name_en` 和 `notes_en` 欄位，西班牙文文件則包含 `name_es` 和 `notes_es` 欄位。

## 步驟 7：搜尋文件

若要搜尋所有語言特定的 `name` 欄位，請使用帶有萬用字元欄位名稱的 `multi_match` 查詢：

```json
GET /task_index/_search
{
  "query": {
    "multi_match": {
      "query": "comprar",
      "fields": ["name_*"]
    }
  }
}
```
{% include copy-curl.html %}

此查詢會比對到西班牙文文件，因為 `name_es` 欄位是使用西班牙文分析器進行分析：

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.13076457,
    "hits": [
      {
        "_index": "task_index",
        "_id": "3",
        "_score": 0.13076457,
        "_source": {
          "predicted_notes_language": "es",
          "name_es": "comprar hierba gatera",
          "notes_es": "A Mittens le gustan mucho las cosas de Humboldt.",
          "notes": "A Mittens le gustan mucho las cosas de Humboldt.",
          "predicted_name_language": "es",
          "name": "comprar hierba gatera"
        }
      }
    ]
  }
}
```

## 相關文件

- [ML 推論處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/ml-inference/)
- [語言分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/)
- [多重比對查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/multi-match/)
- [第三方 ML 平台的連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)
