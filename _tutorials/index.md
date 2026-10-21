---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "教學"
has_children: true
has_toc: false
nav_order: 47
nav_exclude: true
permalink: /tutorials/
redirect_from:
  - /ml-commons-plugin/tutorials/
  - /ml-commons-plugin/tutorials/index/
getting_started_cards:
- heading: 搜尋資料基礎入門
  description: 學習搜尋的基本概念，並探索 OpenSearch 的查詢語言與類型
  link: /getting-started/search-data/
- heading: OpenSearch Dashboards
  description: 使用互動式儀表板與強大的分析工具，開始將資料視覺化
  link: /dashboards/getting-started/
tutorial_cards:
- heading: 向量搜尋
  description: 使用向量實作相似度搜尋，並透過 AI 能力強化搜尋結果
  link: /tutorials/vector-search/
- heading: 重新排名搜尋結果
  description: 使用機器學習模型智慧地重新排列結果，以提升搜尋相關性
  link: /tutorials/reranking/
- heading: 生成式 AI 應用程式
  description: 建立 AI 驅動的應用程式，例如 RAG、聊天機器人與進階對話系統
  link: /tutorials/gen-ai/
- heading: 切面搜尋
  description: 為電子商務或地點搜尋等應用程式建立可篩選的搜尋體驗
  link: /tutorials/faceted-search/
- heading: 語言識別
  description: 使用 ML 模型偵測匯入文字的語言，以支援多語言搜尋
  link: /tutorials/language-identification/
- heading: LLM-as-a-Judge
  description: 使用 LLM 自動化搜尋相關性評估
  link: /tutorials/llm-as-a-judge-tutorial/
---

# OpenSearch 教學

按照逐步教學開始使用 OpenSearch，並建立搜尋功能，包括語意搜尋、混合搜尋、檢索增強生成 (RAG) 與對話式搜尋。

## 入門

學習在 OpenSearch 中搜尋與視覺化資料的基本概念。

{% include cards.html cards=page.getting_started_cards %}

## 使用 OpenSearch 建立搜尋功能

端對端實作特定的搜尋功能。

{% include cards.html cards=page.tutorial_cards %}
