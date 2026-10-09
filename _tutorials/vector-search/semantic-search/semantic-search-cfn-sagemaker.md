---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 AWS CloudFormation 與 Amazon SageMaker 進行語意搜尋"
parent: Semantic search
grand_parent: Vector search
nav_order: 70
redirect_from:
  - /vector-search/tutorials/semantic-search/semantic-search-cfn-sagemaker/
---

# 使用 AWS CloudFormation 與 Amazon SageMaker 進行語意搜尋 

本教學說明如何使用 [AWS CloudFormation](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cfn-template.html) 與 Amazon SageMaker，在 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) 中實作語意搜尋。如需更多資訊，請參閱[語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/semantic-search/)。

如果您使用自行管理的 OpenSearch 而非 Amazon OpenSearch Service，請使用[藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/sagemaker_connector_blueprint.md)建立與 Amazon SageMaker 模型的連接器。如需建立連接器的詳細資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。 

CloudFormation 整合會自動執行[使用 SageMaker 嵌入模型的語意搜尋教學]({{site.url}}{{site.baseurl}}/vector-search/tutorials/semantic-search/semantic-search-sagemaker/)中的步驟。CloudFormation 範本會建立 IAM 角色，並叫用 AWS Lambda 函式來設定 AI 連接器與模型。

請將以 `your_` 為前綴的預留位置取代為您自己的值。
{: .note}

## 模型輸入與輸出需求

請確認您的 Amazon SageMaker 模型輸入符合[預設前處理函式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#preprocessing-function)所需的格式。 

模型輸入必須是字串陣列：

```json
["hello world", "how are you"]
```

此外，請確認模型輸出符合[預設後處理函式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#post-processing-function)所需的格式。模型輸出必須是陣列的陣列，其中每個內部陣列對應一個輸入字串的嵌入：

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

如果您的模型輸入/輸出與所需的預設格式不同，您可以使用 [Painless 指令碼]({{site.url}}{{site.baseurl}}/scripting/painless/)建立自己的前處理/後處理函式。

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

預設的 Amazon Bedrock Titan 嵌入模型輸出格式如下：

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

## 步驟 1：對應後端角色

OpenSearch CloudFormation 範本會使用 Lambda 函式，建立具有 AWS Identity and Access Management (IAM) 角色的 AI 連接器。您必須將 IAM 角色對應至 `ml_full_access`，以授予所需的權限。請依照[使用 SageMaker 嵌入模型的語意搜尋教學的步驟 2.2]({{site.url}}{{site.baseurl}}/vector-search/tutorials/semantic-search/semantic-search-sagemaker/#step-22-map-a-backend-role)對應後端角色。

IAM 角色指定於 CloudFormation 範本中的 **Lambda Invoke OpenSearch ML Commons Role Name** 欄位。預設 IAM 角色為 `LambdaInvokeOpenSearchMLCommonsRole`，因此您必須將 `arn:aws:iam::your_aws_account_id:role/LambdaInvokeOpenSearchMLCommonsRole` 後端角色對應至 `ml_full_access`。

若需要更廣泛的對應，您可以使用萬用字元授予所有角色 `ml_full_access`：  

```
arn:aws:iam::your_aws_account_id:role/*
```  

由於 `all_access` 包含的權限比 `ml_full_access` 更多，將後端角色對應至 `all_access` 也是可接受的。

## 步驟 2：執行 CloudFormation 範本  

CloudFormation 範本整合可於 [Amazon OpenSearch Service 主控台](https://console.aws.amazon.com/aos/home)中使用。請從左側導覽窗格選取 **Integrations**，如下圖所示。

![語意搜尋 CloudFormation 整合]({{site.url}}{{site.baseurl}}/images/vector-search-tutorials/semantic_search_remote_model_Integration_1.png)  

請選擇下列其中一個選項，將模型部署至 Amazon SageMaker。

### 選項 1：將預先訓練的模型部署至 Amazon SageMaker  

您可以從 [Deep Java Library 模型儲存庫](https://djl.ai/)部署預先訓練的 Hugging Face 句子轉換器嵌入模型，如下圖所示。

![將預先訓練的模型部署至 Amazon SageMaker]({{site.url}}{{site.baseurl}}/images/vector-search-tutorials/semantic_search_remote_model_Integration_2.png)

請填寫下列欄位，其餘欄位全部保留預設值：  

1. 輸入您的 **Amazon OpenSearch Endpoint**。  
2. 使用預設的 **SageMaker Configuration** 快速開始，或視需要修改。如需支援的 Amazon SageMaker 執行個體類型，請參閱 [Amazon SageMaker 文件](https://aws.amazon.com/sagemaker/)。  
3. 將 **SageMaker Endpoint Url** 欄位留空。如果您提供 URL，模型將不會部署至 Amazon SageMaker，也不會建立新的推論端點。  
4. 將 **Custom Image** 欄位留空。預設映像為 `djl-inference:0.22.1-cpu-full`。如需可用的映像，請參閱 [AWS Deep Learning Containers](https://docs.aws.amazon.com/deep-learning-containers/latest/devguide/deep-learning-containers-images.html)。  
5. 將 **Custom Model Data Url** 欄位留空。  
6. **Custom Model Environment** 欄位預設為 `djl://ai.djl.huggingface.pytorch/sentence-transformers/all-MiniLM-L6-v2`。如需支援的模型清單，請參閱[支援的模型](#supported-models)。  

### 選項 2：使用現有的 SageMaker 推論端點  

如果您已有 SageMaker 推論端點，可以使用該端點設定模型，如下圖所示。  

![使用現有的 SageMaker 推論端點]({{site.url}}{{site.baseurl}}/images/vector-search-tutorials/semantic_search_remote_model_Integration_3.png)

填寫下列欄位，其他欄位則保留預設值：  

1. 輸入您的 **Amazon OpenSearch Endpoint**。  
2. 輸入您的 **SageMaker Endpoint Url**。  
3. 將 **Custom Image**、**Custom Model Data Url** 和 **Custom Model Environment** 欄位留空。  

### 輸出

部署後，您可以在 CloudFormation 堆疊的 **Outputs** 中找到 OpenSearch AI 連接器和模型 ID。  

如果發生錯誤，請依照下列步驟檢視記錄檔：

1. 開啟 Amazon SageMaker 主控台。
1. 前往 **CloudWatch Logs** 區段。
1. 搜尋包含您的 CloudFormation 堆疊名稱（或與其相關聯）的 **Log Groups**。

## 支援的模型

[Deep Java Library 模型儲存庫](https://djl.ai/)提供下列 Hugging Face 句子轉換器嵌入模型：

```
djl://ai.djl.huggingface.pytorch/sentence-transformers/LaBSE/
djl://ai.djl.huggingface.pytorch/sentence-transformers/all-MiniLM-L12-v1/
djl://ai.djl.huggingface.pytorch/sentence-transformers/all-MiniLM-L12-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/all-MiniLM-L6-v1/
djl://ai.djl.huggingface.pytorch/sentence-transformers/all-MiniLM-L6-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/all-distilroberta-v1/
djl://ai.djl.huggingface.pytorch/sentence-transformers/all-mpnet-base-v1/
djl://ai.djl.huggingface.pytorch/sentence-transformers/all-mpnet-base-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/all-roberta-large-v1/
djl://ai.djl.huggingface.pytorch/sentence-transformers/allenai-specter/
djl://ai.djl.huggingface.pytorch/sentence-transformers/bert-base-nli-cls-token/
djl://ai.djl.huggingface.pytorch/sentence-transformers/bert-base-nli-max-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/bert-base-nli-mean-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/bert-base-nli-stsb-mean-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/bert-base-wikipedia-sections-mean-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/bert-large-nli-cls-token/
djl://ai.djl.huggingface.pytorch/sentence-transformers/bert-large-nli-max-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/bert-large-nli-mean-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/bert-large-nli-stsb-mean-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/clip-ViT-B-32-multilingual-v1/
djl://ai.djl.huggingface.pytorch/sentence-transformers/distilbert-base-nli-mean-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/distilbert-base-nli-stsb-mean-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/distilbert-base-nli-stsb-quora-ranking/
djl://ai.djl.huggingface.pytorch/sentence-transformers/distilbert-multilingual-nli-stsb-quora-ranking/
djl://ai.djl.huggingface.pytorch/sentence-transformers/distiluse-base-multilingual-cased-v1/
djl://ai.djl.huggingface.pytorch/sentence-transformers/facebook-dpr-ctx_encoder-multiset-base/
djl://ai.djl.huggingface.pytorch/sentence-transformers/facebook-dpr-ctx_encoder-single-nq-base/
djl://ai.djl.huggingface.pytorch/sentence-transformers/facebook-dpr-question_encoder-multiset-base/
djl://ai.djl.huggingface.pytorch/sentence-transformers/facebook-dpr-question_encoder-single-nq-base/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-MiniLM-L-12-v3/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-MiniLM-L-6-v3/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-MiniLM-L12-cos-v5/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-MiniLM-L6-cos-v5/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-bert-base-dot-v5/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-bert-co-condensor/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-distilbert-base-dot-prod-v3/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-distilbert-base-tas-b/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-distilbert-base-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-distilbert-base-v3/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-distilbert-base-v4/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-distilbert-cos-v5/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-distilbert-dot-v5/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-distilbert-multilingual-en-de-v2-tmp-lng-aligned/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-distilbert-multilingual-en-de-v2-tmp-trained-scratch/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-distilroberta-base-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-roberta-base-ance-firstp/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-roberta-base-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/msmarco-roberta-base-v3/
djl://ai.djl.huggingface.pytorch/sentence-transformers/multi-qa-MiniLM-L6-cos-v1/
djl://ai.djl.huggingface.pytorch/sentence-transformers/multi-qa-MiniLM-L6-dot-v1/
djl://ai.djl.huggingface.pytorch/sentence-transformers/multi-qa-distilbert-cos-v1/
djl://ai.djl.huggingface.pytorch/sentence-transformers/multi-qa-distilbert-dot-v1/
djl://ai.djl.huggingface.pytorch/sentence-transformers/nli-bert-base/
djl://ai.djl.huggingface.pytorch/sentence-transformers/nli-bert-large-max-pooling/
djl://ai.djl.huggingface.pytorch/sentence-transformers/nli-distilbert-base/
djl://ai.djl.huggingface.pytorch/sentence-transformers/nli-distilroberta-base-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/nli-roberta-base-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/nli-roberta-large/
djl://ai.djl.huggingface.pytorch/sentence-transformers/nq-distilbert-base-v1/
djl://ai.djl.huggingface.pytorch/sentence-transformers/paraphrase-MiniLM-L12-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/paraphrase-MiniLM-L3-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/paraphrase-MiniLM-L6-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/paraphrase-TinyBERT-L6-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/paraphrase-albert-base-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/paraphrase-albert-small-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/paraphrase-distilroberta-base-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/paraphrase-multilingual-mpnet-base-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/paraphrase-xlm-r-multilingual-v1/
djl://ai.djl.huggingface.pytorch/sentence-transformers/quora-distilbert-base/
djl://ai.djl.huggingface.pytorch/sentence-transformers/quora-distilbert-multilingual/
djl://ai.djl.huggingface.pytorch/sentence-transformers/roberta-base-nli-mean-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/roberta-base-nli-stsb-mean-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/roberta-large-nli-mean-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/roberta-large-nli-stsb-mean-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/stsb-bert-base/
djl://ai.djl.huggingface.pytorch/sentence-transformers/stsb-bert-large/
djl://ai.djl.huggingface.pytorch/sentence-transformers/stsb-distilbert-base/
djl://ai.djl.huggingface.pytorch/sentence-transformers/stsb-distilroberta-base-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/stsb-roberta-base-v2/
djl://ai.djl.huggingface.pytorch/sentence-transformers/stsb-roberta-base/
djl://ai.djl.huggingface.pytorch/sentence-transformers/stsb-roberta-large/
djl://ai.djl.huggingface.pytorch/sentence-transformers/stsb-xlm-r-multilingual/
djl://ai.djl.huggingface.pytorch/sentence-transformers/use-cmlm-multilingual/
djl://ai.djl.huggingface.pytorch/sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/xlm-r-bert-base-nli-stsb-mean-tokens/
djl://ai.djl.huggingface.pytorch/sentence-transformers/xlm-r-distilroberta-base-paraphrase-v1/
```