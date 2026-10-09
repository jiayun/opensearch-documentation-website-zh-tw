---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新排序搜尋結果"
has_children: true
has_toc: false
nav_order: 20
redirect_from:
  - /vector-search/tutorials/reranking/
  - /tutorials/reranking/
reranking:
- heading: 使用 Cohere Rerank 重新排序搜尋結果
  link: /tutorials/reranking/reranking-cohere/
  list:
  - <b>平台：</b> OpenSearch
  - <b>模型：</b> Cohere Rerank
  - <b>部署：</b> Provider API
- heading: 在 Amazon Bedrock 上使用 Cohere Rerank 重新排序搜尋結果
  link: /tutorials/reranking/reranking-cohere-bedrock/
  list:
  - <b>平台：</b> OpenSearch、Amazon OpenSearch Service
  - <b>模型：</b> Cohere Rerank
  - <b>部署：</b> Amazon Bedrock
- heading: 使用 Amazon Bedrock 模型重新排序搜尋結果
  link: /tutorials/reranking/reranking-bedrock/
  list:
  - <b>平台：</b> OpenSearch
  - <b>模型：</b> Amazon Bedrock 重新排序模型
  - <b>部署：</b> Amazon Bedrock
- heading: 在 Amazon SageMaker 中使用交叉編碼器重新排序搜尋結果
  link: /tutorials/reranking/reranking-cross-encoder/
  list:
  - <b>平台：</b> OpenSearch
  - <b>模型：</b> Hugging Face MS MARCO
  - <b>部署：</b> Amazon SageMaker
- heading: 在 Amazon SageMaker 中使用重新排序模型重新排序搜尋結果
  link: /tutorials/reranking/reranking-sagemaker/
  list:
  - <b>平台：</b> OpenSearch、Amazon OpenSearch Service
  - <b>模型：</b> Hugging Face BAAI/bge-reranker
  - <b>部署：</b> Amazon SageMaker
- heading: 依欄位重新排序搜尋結果
  link: /tutorials/reranking/reranking-by-field/
  list:
  - <b>平台：</b> OpenSearch、Amazon OpenSearch Service
  - <b>模型：</b> Cohere Rerank
  - <b>部署：</b> Provider API
---

# 重新排序搜尋結果教學

了解如何使用 Cohere Rerank 和 Amazon Bedrock 等機器學習模型重新排序結果，以改善搜尋相關性。重新排序會依據與查詢的語意相似度，對初始搜尋結果重新排序。如需重新排序的更多資訊，請參閱[重新排序搜尋結果]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/reranking-search-results/)。

{% include cards.html cards=page.reranking %}

## 相關文件

- 探索更廣泛的[搜尋品質]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/)工具組，其中包含 User Behavior Insights、Learning to Rank、Search Relevance Workbench 以及查詢改寫功能。