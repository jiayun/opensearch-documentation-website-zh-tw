---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "生成式 AI"
has_children: true
has_toc: false
nav_order: 30
redirect_from:
  - /tutorials/gen-ai/
cards:
- heading: RAG
  description: 建置檢索增強生成與對話式搜尋應用程式
  link: /tutorials/gen-ai/rag/
- heading: 代理式 AI
  description: 使用代理程式建置您的生成式 AI 應用程式
  link: /tutorials/gen-ai/agents/
- heading: 聊天機器人
  description: 使用聊天機器人建置您的生成式 AI 應用程式
  link: /tutorials/gen-ai/chatbots/
- heading: AI 搜尋工作流程
  link: /tutorials/gen-ai/ai-search-flows/
  description: 在 OpenSearch Dashboards 中以視覺化方式建立與設定 AI 搜尋應用程式
- heading: 模型防護機制
  description: 為您的模型新增安全界線，以確保回應受到控制
  link: /tutorials/gen-ai/model-controls/
---

# 生成式 AI 教學

探索下列教學，了解如何使用 OpenSearch 向量資料庫實作生成式 AI 應用程式。如需 OpenSearch 生成式 AI 功能的更多資訊，請參閱[向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/)與[機器學習]({{site.url}}{{site.baseurl}}/ml-commons-plugin/)。

{% include cards.html cards=page.cards %}
