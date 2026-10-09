---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "語意搜尋"
parent: Vector search
has_children: true
has_toc: false
nav_order: 50
redirect_from:
  - /vector-search/tutorials/semantic-search/
  - /tutorials/vector-search/semantic-search/
semantic_search:
- heading: 使用 OpenAI 嵌入模型進行語意搜尋
  link: /tutorials/vector-search/semantic-search/semantic-search-openai/
  list:
  - <b>平台：</b> OpenSearch, Amazon OpenSearch Service
  - <b>模型：</b> OpenAI 嵌入
  - <b>部署：</b> 供應商 API
- heading: 使用 Cohere Embed 進行語意搜尋
  link: /tutorials/vector-search/semantic-search/semantic-search-cohere/
  list:
  - <b>平台：</b> OpenSearch, Amazon OpenSearch Service
  - <b>模型：</b> Cohere Embed
  - <b>部署：</b> 供應商 API
- heading: 使用 Amazon Bedrock 上的 Cohere Embed 進行語意搜尋
  link: /tutorials/vector-search/semantic-search/semantic-search-bedrock-cohere/
  list:
  - <b>平台：</b> OpenSearch, Amazon OpenSearch Service
  - <b>模型：</b> Cohere Embed
  - <b>部署：</b> Amazon Bedrock
- heading: 使用 Amazon Bedrock Titan 進行語意搜尋
  link: /tutorials/vector-search/semantic-search/semantic-search-bedrock-titan/
  list:
  - <b>平台：</b> OpenSearch, Amazon OpenSearch Service
  - <b>模型：</b> Amazon Titan
  - <b>部署：</b> Amazon Bedrock
- heading: 使用另一個帳戶中的 Amazon Bedrock Titan 進行語意搜尋
  link: /tutorials/vector-search/semantic-search/semantic-search-bedrock-titan-other/
  list:
  - <b>平台：</b> OpenSearch, Amazon OpenSearch Service
  - <b>模型：</b> Amazon Titan
  - <b>部署：</b> Amazon Bedrock（位於與您的 Amazon OpenSearch Service 帳戶不同的帳戶中）
- heading: 使用 Amazon SageMaker 中的模型進行語意搜尋
  link: /tutorials/vector-search/semantic-search/semantic-search-sagemaker/
  list:
  - <b>平台：</b> OpenSearch, Amazon OpenSearch Service
  - <b>模型：</b> 自訂
  - <b>部署：</b> Amazon SageMaker
- heading: 使用 AWS CloudFormation 和 Amazon SageMaker 進行語意搜尋
  link: /tutorials/vector-search/semantic-search/semantic-search-cfn-sagemaker/
  list:
  - <b>平台：</b> OpenSearch, Amazon OpenSearch Service
  - <b>模型：</b> 自訂
  - <b>部署：</b> Amazon SageMaker + CloudFormation
- heading: 使用 AWS CloudFormation 和 Amazon Bedrock 進行語意搜尋
  link: /tutorials/vector-search/semantic-search/semantic-search-cfn-bedrock/
  list:
  - <b>平台：</b> OpenSearch, Amazon OpenSearch Service
  - <b>模型：</b> Amazon Titan + Cohere
  - <b>部署：</b> Amazon Bedrock + CloudFormation
- heading: 使用非對稱模型進行語意搜尋
  link: /tutorials/vector-search/semantic-search/semantic-search-asymmetric/
  list:
  - <b>平台：</b> OpenSearch
  - <b>模型：</b> Hugging Face Multilingual-E5-small
  - <b>部署：</b> 本機叢集
- heading: 使用文字分塊進行語意搜尋
  link: /tutorials/vector-search/semantic-search/long-document/
  list:
  - <b>平台：</b> OpenSearch, Amazon OpenSearch Service
  - <b>模型：</b> Amazon Titan Text Embeddings
  - <b>部署：</b> Amazon Bedrock
---

# 語意搜尋教學

了解如何在 OpenSearch 中實作語意搜尋，使用嵌入模型依據語意而非完全相符的關鍵字來比對查詢。

{% include cards.html cards=page.semantic_search %}