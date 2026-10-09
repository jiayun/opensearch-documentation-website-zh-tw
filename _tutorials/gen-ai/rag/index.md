---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: RAG
parent: Generative AI
has_children: true
has_toc: false
nav_order: 10
redirect_from:
  - /vector-search/tutorials/rag/
  - /vector-search/tutorials/conversational-search/
  - /tutorials/vector-search/rag/
  - /tutorials/gen-ai/rag/
rag:
- heading: 使用 DeepSeek Chat API 的檢索增強生成 (RAG)
  link: /tutorials/gen-ai/rag/rag-deepseek-chat/
  list:
  - <b>平台：</b> OpenSearch、Amazon OpenSearch Service
  - <b>模型：</b> DeepSeek Chat
  - <b>部署：</b> 供應商 API
- heading: 在 Amazon Bedrock 上使用 DeepSeek-R1 的 RAG
  link: /tutorials/gen-ai/rag/rag-deepseek-r1-bedrock/
  list:
  - <b>平台：</b> OpenSearch、Amazon OpenSearch Service
  - <b>模型：</b> DeepSeek-R1
  - <b>部署：</b> Amazon Bedrock
- heading: 在 Amazon SageMaker 中使用 DeepSeek-R1 的 RAG
  link: /tutorials/gen-ai/rag/rag-deepseek-r1-sagemaker/
  list:
  - <b>平台：</b> OpenSearch、Amazon OpenSearch Service
  - <b>模型：</b> DeepSeek-R1
  - <b>部署：</b> Amazon SageMaker
conversational_search:
- heading: 使用 Cohere Command 的對話式搜尋
  link: /tutorials/gen-ai/rag/conversational-search-cohere/
  list:
  - <b>平台：</b> OpenSearch
  - <b>模型：</b> Cohere Command
  - <b>部署：</b> 供應商 API
- heading: 使用 OpenAI 的對話式搜尋
  link: /tutorials/gen-ai/rag/conversational-search-openai/
  list:
  - <b>平台：</b> OpenSearch
  - <b>模型：</b> OpenAI GPT-4o
  - <b>部署：</b> 供應商 API
- heading: 在 Amazon Bedrock 上使用 Anthropic Claude 的對話式搜尋
  link: /tutorials/gen-ai/rag/conversational-search-claude-bedrock/
  list:
  - <b>平台：</b> OpenSearch
  - <b>模型：</b> Anthropic Claude
  - <b>部署：</b> Amazon Bedrock API
---

# RAG 教學

了解如何使用 OpenSearch 實作檢索增強生成 (RAG)，結合向量搜尋檢索與大型語言模型，以產生有依據且具備情境感知能力的回應。

{% include cards.html cards=page.rag %}

## 使用 RAG 的對話式搜尋教學

下列教學說明如何使用 RAG 實作對話式搜尋。

{% include cards.html cards=page.conversational_search %}