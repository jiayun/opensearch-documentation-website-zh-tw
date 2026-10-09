---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理式 AI"
parent: Generative AI
has_children: true
has_toc: false
nav_order: 20
redirect_from:
  - /tutorials/gen-ai/agents/
flows:
- heading: 建置流程代理程式
  link: /ml-commons-plugin/agents-tools/agents-tools-tutorial/
  description: 了解如何為 RAG 建置流程代理程式
  list:
  - <b>平台：</b> OpenSearch
  - <b>模型：</b> Anthropic Claude
  - <b>部署：</b> Amazon Bedrock
- heading: 建置規劃-執行-反思代理程式
  link: /tutorials/gen-ai/agents/build-plan-execute-reflect-agent/
  description: 了解如何建置功能強大的 <i>規劃－執行－反思</i> 代理程式，以解決複雜問題
  list:
  - <b>平台：</b> OpenSearch
  - <b>模型：</b> Anthropic Claude 3.7 Sonnet
  - <b>部署：</b> Amazon Bedrock
---

# 代理式 AI 教學

了解如何建置以 OpenSearch 作為知識庫與工具提供者的 AI 代理程式，實現自主查詢規劃、擷取與回應產生。

{% include cards.html cards=page.flows %}