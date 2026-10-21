---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 AWS CloudFormation 與 Amazon Bedrock 的語意搜尋"
parent: Semantic search
grand_parent: Vector search
nav_order: 75
redirect_from:
  - /vector-search/tutorials/semantic-search/semantic-search-cfn-bedrock/
---

# 使用 AWS CloudFormation 與 Amazon Bedrock 進行語意搜尋

本教學說明如何使用 [AWS CloudFormation](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cfn-template.html) 與 Amazon Bedrock，在 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) 中實作語意搜尋。如需詳細資訊，請參閱[語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/semantic-search/)。

如果您使用的是自行管理的 OpenSearch，而非 Amazon OpenSearch Service，請使用[藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/)建立連接 Amazon Bedrock 模型的連接器。如需建立連接器的詳細資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

CloudFormation 整合可自動執行[使用 Amazon Bedrock Titan 進行語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/tutorials/semantic-search/semantic-search-bedrock-titan/)與[在 Amazon Bedrock 上使用 Cohere Embed 進行語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/tutorials/semantic-search/semantic-search-bedrock-cohere/)教學中的步驟。CloudFormation 範本會建立 AWS Identity and Access Management (IAM) 角色，並叫用 AWS Lambda 函式來設定 AI 連接器與模型。

請將以 `your_` 前綴開頭的預留位置替換為您自己的值。
{: .note}

## 必要條件：建立 OpenSearch 叢集

前往 [Amazon OpenSearch Service 主控台](https://console.aws.amazon.com/aos/home)並建立 OpenSearch 網域。

請記下網域的 Amazon Resource Name (ARN)；後續步驟會用到它。

## 步驟 1：對應後端角色

OpenSearch CloudFormation 範本使用 Lambda 函式來建立具有 IAM 角色的 AI 連接器。您必須將該 IAM 角色對應到 `ml_full_access`，才能授予必要的權限。請依照 [使用 Amazon Bedrock Titan 的語意搜尋教學的步驟 2.2]({{site.url}}{{site.baseurl}}/vector-search/tutorials/semantic-search/semantic-search-bedrock-titan/#step-22-map-a-backend-role) 來對應後端角色。

IAM 角色在 CloudFormation 範本中由 **Lambda Invoke OpenSearch ML Commons Role Name** 欄位指定。預設的 IAM 角色是 `LambdaInvokeOpenSearchMLCommonsRole`，因此您必須將 `arn:aws:iam::your_aws_account_id:role/LambdaInvokeOpenSearchMLCommonsRole` 後端角色對應到 `ml_full_access`。

若要進行更廣泛的對應，您可以使用萬用字元將 `ml_full_access` 授予所有角色：  

```
arn:aws:iam::your_aws_account_id:role/*
```  

由於 `all_access` 包含的權限比 `ml_full_access` 更多，因此將後端角色對應到 `all_access` 也是可以接受的。

如果您的網域存取政策尚未允許此 IAM 角色，請將該角色加入網域存取政策。

## 步驟 2：執行 CloudFormation 範本

CloudFormation 範本整合功能可在 [Amazon OpenSearch Service 主控台](https://console.aws.amazon.com/aos/home)中使用。從左側導覽窗格中選取 **Integrations**，如下圖所示。

![語意搜尋 CloudFormation 整合]({{site.url}}{{site.baseurl}}/images/vector-search-tutorials/semantic_search_bedrock_integration_1.png)

若要建立連接器，請填寫下列表單。

![將預先訓練的模型部署至 Amazon Bedrock]({{site.url}}{{site.baseurl}}/images/vector-search-tutorials/semantic_search_bedrock_integration_2.png)

主控台為公有網域與虛擬私有雲端 (VPC) 網域提供不同的範本。VPC 網域範本會在您的 VPC 中執行 Lambda 函式，因此也需要執行 Lambda 函式所用的安全群組與子網路。

請填寫下列欄位，其餘欄位皆保留預設值：

1. 輸入您的 **Amazon OpenSearch Endpoint**。
2. 在 **Model Configuration** 中，選取要部署的 **Model**。請從下列支援的模型中選擇一個：
    - `amazon.titan-embed-text-v1`
    - `amazon.titan-embed-image-v1`
    - `amazon.titan-embed-text-v2:0`
    - `cohere.embed-english-v3`
    - `cohere.embed-multilingual-v3`
3. 選取 **Model Region**（此為 Amazon Bedrock 區域）。
4. 在 **AddProcessFunction** 中，選取 `true` 以啟用連接器中的預設前處理與後處理函式，或選取 `false` 將其停用。

## 輸出

部署完成後，您可以在 **CloudFormation stack Outputs** 中找到 **ConnectorId**、**ModelId** 與 **BedrockEndpoint**。  

如果發生錯誤，請依照下列步驟檢視記錄檔：

1. 前往 **CloudWatch Logs** 區段。
2. 搜尋包含 (或關聯至) 您 CloudFormation 堆疊名稱的 **Log Groups**。

## 步驟 3：設定語意搜尋

請依照下列步驟設定語意搜尋。

### 步驟 3.1：建立資料匯入管線

首先，建立一個使用 Amazon Bedrock 模型從輸入文字產生嵌入的[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)：

```json
PUT /_ingest/pipeline/my_bedrock_embedding_pipeline
{
    "description": "text embedding pipeline",
    "processors": [
        {
            "text_embedding": {
                "model_id": "your_model_id_from_stack_outputs",
                "field_map": {
                    "text": "text_knn"
                }
            }
        }
    ]
}
```
{% include copy-curl.html %}

### 步驟 3.2：建立向量索引

接著，建立向量索引以儲存輸入文字與產生的嵌入。將 `dimension` 設為您在範本中所選模型的嵌入大小（在此範例中，`amazon.titan-embed-text-v1` 為 1536）：

```json
PUT my_index
{
  "settings": {
    "index": {
      "default_pipeline": "my_bedrock_embedding_pipeline",
      "knn": "true"
    }
  },
  "mappings": {
    "properties": {
      "text_knn": {
        "type": "knn_vector",
        "dimension": 1536,
        "space_type": "cosinesimil"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 3.3：匯入資料

將範例文件匯入索引：

```json
POST /my_index/_doc/1000001
{
    "text": "hello world."
}
```
{% include copy-curl.html %}

### 步驟 3.4：搜尋索引

執行向量搜尋，從向量索引擷取文件：

```json
POST /my_index/_search
{
  "query": {
    "neural": {
      "text_knn": {
        "query_text": "hello",
        "model_id": "your_model_id_from_stack_outputs",
        "k": 100
      }
    }
  },
  "size": "1",
  "_source": ["text"]
}
```
{% include copy-curl.html %}

## 相關文件

- [語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/semantic-search/)
- [連線至外部託管的模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/)
- [文字嵌入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-embedding/)
- [神經查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural/)
