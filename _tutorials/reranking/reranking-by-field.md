---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "依欄位重新排序搜尋結果"
parent: Reranking search results
nav_order: 120
redirect_from:
  - /vector-search/tutorials/reranking/reranking-by-field/
---

# 使用 Cohere Rerank 依欄位重新排序搜尋結果

您可以[依欄位重新排序搜尋結果]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/#the-by_field-rerank-type)。當您的文件包含特別重要的欄位，或您想使用外部託管的模型重新排序結果時，此功能相當實用。如需更多資訊，請參閱[依欄位重新排序搜尋結果]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-by-field/)。

本教學說明如何在自行管理的 OpenSearch 和 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) 中，使用 [Cohere Rerank](https://docs.cohere.com/reference/rerank-1) 模型依欄位重新排序搜尋結果。

請將以 `your_` 前綴開頭的預留位置替換為您自己的值。
{: .note}

## 步驟 1（自行管理的 OpenSearch）：建立連接器

若要建立連接器，請傳送下列請求：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "cohere-rerank",
    "description": "The connector to Cohere reanker model",
    "version": "1",
    "protocol": "http",
    "credential": {
        "cohere_key": "your_cohere_api_key"
    },
    "parameters": {
        "model": "rerank-english-v3.0",
        "return_documents": true
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "url": "https://api.cohere.ai/v1/rerank",
            "headers": {
                "Authorization": "Bearer ${credential.cohere_key}"
            },
            "request_body": "{ \"documents\": ${parameters.documents}, \"query\": \"${parameters.query}\", \"model\": \"${parameters.model}\", \"top_n\": ${parameters.top_n},  \"return_documents\": ${parameters.return_documents} }"
        }
    ]
}
```
{% include copy-curl.html %}

回應包含連接器 ID：

```json
{"connector_id":"qp2QP40BWbTmLN9Fpo40"}
```

請記下連接器 ID；您將在後續步驟中使用它。接著前往[步驟 2](#step-2-register-the-cohere-rerank-model)。

## 步驟 1（Amazon OpenSearch Service）：建立連接器

請依照下列步驟，使用 Amazon OpenSearch Service 建立連接器。

### 先決條件：建立 OpenSearch 叢集

前往 [Amazon OpenSearch Service 主控台](https://console.aws.amazon.com/aos/home)，並建立 OpenSearch 網域。

請記下網域的 Amazon Resource Name（ARN）和 URL；您將在後續步驟中使用它們。

### 步驟 1.1：將 API 金鑰儲存在 AWS Secrets Manager 中

將您的 Cohere API 金鑰儲存在 [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html) 中：

1. 開啟 AWS Secrets Manager。
1. 選取 **Store a new secret**。
1. 選取 **Other type of secret**。
1. 建立鍵值配對，以 **my_cohere_key** 作為鍵，並以您的 Cohere API 金鑰作為值。
1. 將您的秘密命名為 `my_test_cohere_secret`。

請記下秘密的 ARN；您將在後續步驟中使用它。

### 步驟 1.2：建立 IAM 角色

若要使用步驟 1 中建立的秘密，您必須建立具有該秘密讀取權限的 AWS Identity and Access Management（IAM）角色。此 IAM 角色將設定於連接器中，讓連接器能夠讀取該秘密。

前往 IAM 主控台，建立名為 `my_cohere_secret_role` 的新 IAM 角色，並新增下列信任政策和權限：

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

### 步驟 1.3：在 Amazon OpenSearch Service 中設定 IAM 角色

請依照下列步驟，在 Amazon OpenSearch Service 中設定 IAM 角色。

#### 步驟 1.3.1：建立用於簽署連接器請求的 IAM 角色

建立專門用於簽署您的 Create Connector API 請求的新 IAM 角色。

建立名為 `my_create_cohere_connector_role` 的 IAM 角色，並設定下列信任政策和權限：

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

您將在步驟 4.1 中使用 `your_iam_user_arn` IAM 使用者擔任此角色。

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
            "Resource": "your_opensearch_domain_arn_created_in_step0"
        }
    ]
}
```
{% include copy.html %}

請記下此角色的 ARN；您將在後續步驟中使用它。

#### 步驟 1.3.2：對應後端角色

請依照下列步驟對應後端角色：

1. 登入 OpenSearch Dashboards，並在頂端選單中選取 **Security**。
2. 選取 **Roles**，然後選取 **ml_full_access** 角色。 
3. 在 **ml_full_access** 角色詳細資料頁面上，選取 **Mapped users**，然後選取 **Manage mapping**。 
4. 在 **Backend roles** 欄位中輸入步驟 3.1 中建立的 IAM 角色 ARN，如下圖所示。
    ![對應後端角色]({{site.url}}{{site.baseurl}}/images/vector-search-tutorials/mapping_iam_role_arn.png)
4. 選取 **Map**。 

IAM 角色現已成功設定於您的 OpenSearch 叢集中。

## 步驟 1.4：建立連接器

請依照下列步驟，為模型建立連接器。如需建立連接器的詳細資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

使用從 AWS 取得的臨時憑證執行下列 Python 程式碼。
 
```python
import boto3
import requests 
from requests_aws4auth import AWS4Auth

host = 'your_amazon_opensearch_domain_endpoint_created_in_step0'
region = 'your_amazon_opensearch_domain_region'
service = 'es'

assume_role_response = boto3.Session().client('sts').assume_role(
  RoleArn="your_iam_role_arn_created_in_step1.3.1",
  RoleSessionName="your_session_name"
)
credentials = assume_role_response["Credentials"]

awsauth = AWS4Auth(credentials["AccessKeyId"], credentials["SecretAccessKey"], region, service, session_token=credentials["SessionToken"])

path = '/_plugins/_ml/connectors/_create'
url = host + path

payload = {
    "name": "cohere-rerank",
    "description": "The connector to Cohere reanker model",
    "version": "1",
    "protocol": "http",
    "credential": {
        "secretArn": "your_secret_arn_created_in_step1",
        "roleArn": "your_iam_role_arn_created_in_step2"
    },
    "parameters": {
        "model": "rerank-english-v3.0",
        "return_documents": true

    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "url": "https://api.cohere.ai/v1/rerank",
            "headers": {
                "Authorization": "Bearer ${credential.secretArn.my_cohere_key}"
            },
            "request_body": "{ \"documents\": ${parameters.documents}, \"query\": \"${parameters.query}\", \"model\": \"${parameters.model}\", \"top_n\": ${parameters.top_n}, \"return_documents\": ${parameters.return_documents} }"
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

## 步驟 2：註冊 Cohere Rerank 模型

使用自行管理的 OpenSearch 或 Amazon OpenSearch Service 方法成功建立連接器後，即可註冊 Cohere Rerank 模型。

請使用步驟 1.4 中的連接器 ID 來建立模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "cohere rerank model",
    "function_name": "remote",
    "description": "test rerank model",
    "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

請記下連接器 ID，後續步驟會用到。

# 步驟 3：測試模型

若要測試模型，請傳送下列請求：

```json
POST /_plugins/_ml/models/your_model_id/_predict
{
  "parameters": {
	"top_n" : 100,
    "query": "What day is it?",
	"documents" : ["Monday", "Tuesday", "apples"]
  }
}
```
{% include copy-curl.html %}

回應會包含相符的文件：

```json
{
	"inference_results": [
		{
			"output": [
				{
					"name": "response",
					"dataAsMap": {
						"id": "e15a3922-3d89-4adc-96cf-9b85a619fb66",
						"results": [
							{
								"document": {
									"text": "Monday"
								},
								"index": 0.0,
								"relevance_score": 0.21076629
							},
							{
								"document": {
									"text": "Tuesday"
								},
								"index": 1.0,
								"relevance_score": 0.13206616
							},
							{
								"document": {
									"text": "apples"
								},
								"index": 2.0,
								"relevance_score": 1.0804956E-4
							}
						],
						"meta": {
							"api_version": {
								"version": "1"
							},
							"billed_units": {
								"search_units": 1.0
							}
						}
					}
				}
			],
			"status_code": 200
		}
	]
}
```

每份文件都會由重新排序模型指派一個分數。接下來您將建立一個搜尋管線，該管線會呼叫 Cohere 模型，並根據相關性分數重新排列搜尋結果。

## 步驟 3：重新排列搜尋結果

請依照下列步驟重新排列搜尋結果。

### 步驟 3.1：建立索引

若要建立索引，請傳送下列請求：

```json
POST _bulk
{ "index": { "_index": "nyc_facts", "_id": 1 } }
{ "fact_title": "Population of New York", "fact_description": "New York City has an estimated population of over 8.3 million people as of 2023, making it the most populous city in the United States." }
{ "index": { "_index": "nyc_facts", "_id": 2 } }
{ "fact_title": "Statue of Liberty", "fact_description": "The Statue of Liberty, a symbol of freedom, was gifted to the United States by France in 1886 and stands on Liberty Island in New York Harbor." }
{ "index": { "_index": "nyc_facts", "_id": 3 } }
{ "fact_title": "New York City is a Global Financial Hub", "fact_description": "New York City is home to the New York Stock Exchange (NYSE) and Wall Street, which are central to the global finance industry." }
{ "index": { "_index": "nyc_facts", "_id": 4 } }
{ "fact_title": "Broadway", "fact_description": "Broadway is a major thoroughfare in New York City known for its theaters. It's also considered the birthplace of modern American theater and musicals." }
{ "index": { "_index": "nyc_facts", "_id": 5 } }
{ "fact_title": "Central Park", "fact_description": "Central Park, located in Manhattan, spans 843 acres and is one of the most visited urban parks in the world, offering green spaces, lakes, and recreational areas." }
{ "index": { "_index": "nyc_facts", "_id": 6 } }
{ "fact_title": "Empire State Building", "fact_description": "The Empire State Building, completed in 1931, is an iconic Art Deco skyscraper that was the tallest building in the world until 1970." }
{ "index": { "_index": "nyc_facts", "_id": 7 } }
{ "fact_title": "Times Square", "fact_description": "Times Square, often called 'The Cross-roads of the World,' is known for its bright lights, Broadway theaters, and New Year's Eve ball drop." }
{ "index": { "_index": "nyc_facts", "_id": 8 } }
{ "fact_title": "Brooklyn Bridge", "fact_description": "The Brooklyn Bridge, completed in 1883, connects Manhattan and Brooklyn and was the first suspension bridge to use steel in its construction." }
{ "index": { "_index": "nyc_facts", "_id": 9 } }
{ "fact_title": "New York City Public Library", "fact_description": "The New York Public Library, founded in 1895, has over 50 million items in its collections and serves as a major cultural and educational resource." }
{ "index": { "_index": "nyc_facts", "_id": 10 } }
{ "fact_title": "New York's Chinatown", "fact_description": "New York's Chinatown, one of the largest in the world, is known for its vibrant culture, food, and history. It plays a key role in the city's Chinese community." }
```
{% include copy-curl.html %}

### 步驟 3.2：建立重新排序管線

若要建立重新排序管線，請傳送下列請求：

```json
PUT /_search/pipeline/cohere_pipeline
{
  "response_processors": [
    {
      "ml_inference": {
        "model_id": "your_model_id",
        "input_map": {
          "documents": "fact_description",
          "query": "_request.ext.query_context.query_text",
          "top_n": "_request.ext.query_context.top_n"
        },
        "output_map": {
          "relevance_score": "results[*].relevance_score",
          "description": "results[*].document.text"
        },
        "full_response_path": false,
        "ignore_missing": false,
        "ignore_failure": false,
        "one_to_one": false,
        "override": false,
        "model_config": {}
      }
    },
    {
      "rerank": {
        "by_field": {
          "target_field": "relevance_score",
          "remove_target_field": false,
          "keep_previous_score": false,
          "ignore_failure": false
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 3.3：測試管線

若要測試管線，請傳送一個與已編製索引文件相關的查詢，並將 `top_n` 設為大於或等於 `size` 的值：

```json
GET nyc_facts/_search?search_pipeline=cohere_pipeline
{
  "query": {
    "match_all": {}
  },
  "size": 5,
  "ext": {
    "rerank": {
      "query_context": {
        "query_text": "Where do people go to see a show?",
        "top_n" : "10"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會包含重新排序後的文件：

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
      "value": 10,
      "relation": "eq"
    },
    "max_score": 0.34986588,
    "hits": [
      {
        "_index": "nyc_facts",
        "_id": "_7a76b04b5016c71c",
        "_score": 0.34986588,
        "_source": {
          "result_document": "Broadway is a major thoroughfare in New York City known for its theaters. It's also considered the birthplace of modern American theater and musicals.",
          "fact_title": "Times Square",
          "fact_description": "Times Square, often called 'The Cross-roads of the World,' is known for its bright lights, Broadway theaters, and New Year's Eve ball drop.",
          "relevance_score": 0.34986588
        }
      },
      {
        "_index": "nyc_facts",
        "_id": "_00c26e453971ed68",
        "_score": 0.1066906,
        "_source": {
          "result_document": "Times Square, often called 'The Cross-roads of the World,' is known for its bright lights, Broadway theaters, and New Year's Eve ball drop.",
          "fact_title": "New York City Public Library",
          "fact_description": "The New York Public Library, founded in 1895, has over 50 million items in its collections and serves as a major cultural and educational resource.",
          "relevance_score": 0.1066906
        }
      },
      {
        "_index": "nyc_facts",
        "_id": "_d03d3610a5a5bd82",
        "_score": 0.00019563535,
        "_source": {
          "result_document": "The New York Public Library, founded in 1895, has over 50 million items in its collections and serves as a major cultural and educational resource.",
          "fact_title": "Broadway",
          "fact_description": "Broadway is a major thoroughfare in New York City known for its theaters. It's also considered the birthplace of modern American theater and musicals.",
          "relevance_score": 0.00019563535
        }
      },
      {
        "_index": "nyc_facts",
        "_id": "_9284bae64eab7f63",
        "_score": 0.000019988918,
        "_source": {
          "result_document": "The Statue of Liberty, a symbol of freedom, was gifted to the United States by France in 1886 and stands on Liberty Island in New York Harbor.",
          "fact_title": "Brooklyn Bridge",
          "fact_description": "The Brooklyn Bridge, completed in 1883, connects Manhattan and Brooklyn and was the first suspension bridge to use steel in its construction.",
          "relevance_score": 0.000019988918
        }
      },
      {
        "_index": "nyc_facts",
        "_id": "_7aa6f2934f47911b",
        "_score": 0.0000104515475,
        "_source": {
          "result_document": "The Brooklyn Bridge, completed in 1883, connects Manhattan and Brooklyn and was the first suspension bridge to use steel in its construction.",
          "fact_title": "Statue of Liberty",
          "fact_description": "The Statue of Liberty, a symbol of freedom, was gifted to the United States by France in 1886 and stands on Liberty Island in New York Harbor.",
          "relevance_score": 0.0000104515475
        }
      }
    ]
  },
  "profile": {
    "shards": []
  }
}
```

評估重新排序後的結果時，請著重於 `result_document` 欄位及其對應的 `relevance_score`。`fact_description` 欄位顯示的是原始文件文字，並不反映重新排序的順序。
{: .note}
