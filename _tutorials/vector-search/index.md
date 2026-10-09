---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "向量搜尋"
has_children: true
has_toc: false
nav_order: 10
redirect_from:
  - /vector-search/tutorials/
  - /tutorials/vector-search/
vector_search_101:
- heading: 向量搜尋入門
  description: 了解如何執行原始向量搜尋
  link: /vector-search/getting-started/
- heading: 語意搜尋與混合搜尋入門
  description: 建立您的第一個 AI 搜尋應用程式
  link: /tutorials/vector-search/neural-search-tutorial/
ai_search_types:
- heading: 語意搜尋
  description: 理解查詢背後的含義與意圖，以提供更相關的結果
  link: /vector-search/ai-search/semantic-search/
- heading: 混合搜尋
  description: 結合關鍵字搜尋與語意搜尋技術，提升相關性
  link: /vector-search/ai-search/hybrid-search/
- heading: 多模態搜尋
  description: 支援跨不同類型的資料進行搜尋，例如文字與影像
  link: /vector-search/ai-search/multimodal-search/
- heading: 神經稀疏搜尋
  description: 使用稀疏向量表示與深度學習模型，實現高效率的檢索
  link: /vector-search/ai-search/neural-sparse-search/
- heading: 使用 RAG 的對話式搜尋
  description: 結合自然對話與檢索增強生成，提供符合上下文的回答
  link: /vector-search/ai-search/conversational-search/
other:
- heading: 向量操作
  description: 了解如何產生嵌入並最佳化向量儲存空間
  link: /tutorials/vector-search/vector-operations/
- heading: 語意搜尋
  description: 使用各種機器學習模型實作語意搜尋
  link: /tutorials/vector-search/semantic-search/
- heading: 使用語意醒目提示
  description: 了解如何在結果中醒目提示語意最相關的句子
  link: /tutorials/vector-search/semantic-highlighting-tutorial/
---

# 向量搜尋教學

探索下列教學，了解如何使用 OpenSearch 向量資料庫實作向量搜尋應用程式。如需進一步了解如何將 OpenSearch 用作向量資料庫，請參閱[向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/)。

## 向量搜尋基礎

{% include cards.html cards=page.vector_search_101 %}

## AI 搜尋類型

{% include cards.html cards=page.ai_search_types %}

## 向量搜尋應用程式

{% include cards.html cards=page.other %}