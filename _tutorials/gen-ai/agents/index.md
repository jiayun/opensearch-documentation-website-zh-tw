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
- heading: 建立流程代理程式
  link: /ml-commons-plugin/agents-tools/agents-tools-tutorial/
  description: 了解如何為 RAG 建立流程代理程式 (flow agent)
  list:
  - <b>平台：</b> OpenSearch
  - <b>模型：</b> Anthropic Claude
  - <b>部署：</b> Amazon Bedrock
- heading: 建立規劃-執行-反思代理程式
  link: /tutorials/gen-ai/agents/build-plan-execute-reflect-agent/
  description: 了解如何建立強大的 <i>規劃-執行-反思</i> 代理程式 (plan-execute-reflect agent) 來解決複雜問題
  list:
  - <b>平台：</b> OpenSearch
  - <b>模型：</b> Anthropic Claude Sonnet 4.6
  - <b>部署：</b> Amazon Bedrock
- heading: 搭配 Strands Agents 使用代理記憶
  link: /tutorials/gen-ai/agents/agentic-memory-strands/
  description: 了解如何使用 OpenSearch 代理記憶 (agentic memory) 為 Strands Agents 代理程式提供長期記憶
  list:
  - <b>平台：</b> OpenSearch、Strands Agents
  - <b>模型：</b> Anthropic Claude Sonnet 4.6、Amazon Titan Text Embeddings V2
  - <b>部署：</b> Amazon Bedrock
---

# 代理式 AI 教學

了解如何建立以 OpenSearch 作為知識庫與工具提供者的 AI 代理程式，實現自主的查詢規劃、擷取與回應生成。

{% include cards.html cards=page.flows %}