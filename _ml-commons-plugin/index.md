---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "機器學習"
nav_order: 1
has_children: false
has_toc: false
nav_exclude: true
permalink: /ml-commons-plugin/
redirect_from: 
  - /ml-commons-plugin/index/
demo_cards:
- heading: 探索 AI 搜尋與 RAG 示範
  description: 試用互動式 Hugging Face 示範，展示 AI 搜尋、多模態 RAG 與代理式 RAG
  link: https://huggingface.co/spaces/opensearch-project/OpenSearch-AI
models:
- heading: 將本機模型部署到您的叢集
  link: /ml-commons-plugin/using-ml-models/
  list:
  - <b>預先訓練模型</b>：使用 OpenSearch 提供的模型立即實作
  - <b>自訂模型</b>：上傳並提供您自己的模型
- heading: 連線至外部託管的模型
  link: /ml-commons-plugin/remote-models/
  description: 連線至託管於 Amazon Bedrock、Amazon SageMaker、OpenAI、Cohere、DeepSeek 及其他平台的模型
more_cards:
- heading: 開始使用 AI 搜尋
  description: 使用本實作教學建立您的第一個語意搜尋應用程式
  link: /vector-search/tutorials/neural-search-tutorial/
- heading: AI 搜尋
  description: 探索 AI 搜尋，從<b>語意</b>、<b>混合</b>與<b>多模態</b>搜尋到<b>RAG</b>
  link: /vector-search/ai-search/
- heading: 教學
  description: 依照逐步教學，將 AI 功能整合至您的應用程式
  link: /vector-search/tutorials/
- heading: ML API 參考
  description: 探索機器學習 API 操作的完整文件
  link: /ml-commons-plugin/api/
oa-toolkit:
- heading: OpenSearch Assistant Toolkit
  link: /ml-commons-plugin/opensearch-assistant/
  list:
  - 用於任務協調的代理程式
  - 用於特定操作的工具
  - 組態自動化
algorithms:
- heading: 支援的演算法
  link: /ml-commons-plugin/algorithms/
  description: 了解原生支援的分群、模式偵測與統計分析演算法
---

# 機器學習

OpenSearch 提供兩種截然不同的機器學習 (ML) 方法：使用 ML 模型執行語意搜尋與文字生成等工作，以及執行統計演算法進行資料分析。請選擇最符合您使用情境的方法。

## 互動式示範

{% include cards.html cards=page.demo_cards %}

## 用於搜尋與 AI/ML 應用程式的 ML 模型

OpenSearch 支援 ML 模型，您可以使用這些模型，透過語意理解來提升搜尋相關性。您可以直接在 OpenSearch 叢集內部署模型，或連線至託管於外部平台的模型。這些模型可以將文字轉換為向量嵌入，實現語意搜尋功能，或提供文字生成與問答等進階功能。如需更多資訊，請參閱[整合 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/)。

{% include cards.html cards=page.models %}

## OpenSearch Assistant 與自動化

OpenSearch Assistant Toolkit 可協助您為 OpenSearch Dashboards 建立 AI 驅動的助理。

{% include cards.html cards=page.oa-toolkit %}

## 內建資料分析演算法

OpenSearch 包含內建演算法，可直接在您的叢集內分析資料，實現異常偵測、資料分群與預測分析等工作，無需外部 ML 模型。

{% include cards.html cards=page.algorithms %}

## 建置您的解決方案 

{% include cards.html cards=page.more_cards %}