---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "AI 與機器學習"
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
- heading: 將本機模型部署至您的叢集
  link: /ml-commons-plugin/using-ml-models/
  list:
  - <b>預先訓練的模型</b>：使用 OpenSearch 提供的模型，立即開始實作
  - <b>自訂模型</b>：上傳並提供您自己的模型
- heading: 連線至外部託管的模型
  link: /ml-commons-plugin/remote-models/
  description: 連線至託管於 Amazon Bedrock、Amazon SageMaker、OpenAI、Cohere、DeepSeek 及其他平台上的模型
more_cards:
- heading: 開始使用 AI 搜尋
  description: 透過這份實作教學，建立您的第一個語意搜尋應用程式
  link: /vector-search/tutorials/neural-search-tutorial/
- heading: AI 搜尋
  description: 探索 AI 搜尋，從 <b>語意搜尋</b>、<b>混合搜尋</b>與 <b>多模態搜尋</b>到 <b>RAG</b>
  link: /vector-search/ai-search/
- heading: 教學
  description: 依照逐步教學，將 AI 功能整合至您的應用程式
  link: /vector-search/tutorials/
- heading: ML API 參考
  description: 探索機器學習 API 操作的完整說明文件
  link: /ml-commons-plugin/api/
agents:
- heading: 代理程式
  link: /ml-commons-plugin/agents-tools/agents/
  description: 了解各種代理程式類型，並為您的使用情境選擇合適的類型
- heading: 工具
  link: /ml-commons-plugin/agents-tools/tools/
  description: 賦予代理程式特定能力，例如執行搜尋或列出索引
- heading: 代理程式與工具教學
  link: /ml-commons-plugin/agents-tools/agents-tools-tutorial/
  description: 使用代理程式與工具建立檢索增強生成 (RAG) 應用程式
- heading: OpenSearch Assistant Toolkit
  link: /ml-commons-plugin/opensearch-assistant/
  description: 為 OpenSearch Dashboards 建立以 AI 驅動的助理
mcp:
- heading: MCP 連接器
  link: /ml-commons-plugin/agents-tools/mcp/
  description: 讓 OpenSearch 代理程式呼叫託管於外部 MCP 伺服器上的工具
- heading: 叢集內 MCP 伺服器
  link: /ml-commons-plugin/mcp/in-cluster-mcp-server/
  description: 讓外部 MCP 用戶端呼叫您叢集中註冊的工具
- heading: 獨立 MCP 伺服器
  link: /ai-agent-integrations/mcp-server/
  description: 在叢集之外執行 OpenSearch MCP Server，讓 AI 助理查詢 OpenSearch
memory:
- heading: 代理記憶 (agentic memory)
  link: /ml-commons-plugin/agentic-memory/
  description: 在代理程式對話之間儲存與擷取資訊，例如使用者偏好
- heading: 脈絡管理
  link: /ml-commons-plugin/context-management/
  description: 截斷、摘要或限制代理程式傳送給 LLM 的脈絡
algorithms:
- heading: 支援的演算法
  link: /ml-commons-plugin/algorithms/
  description: 了解原生支援的分群、模式偵測與統計分析演算法
---

# AI 與機器學習

OpenSearch 提供機器學習 (ML) 演算法、模型整合、模型推論、代理程式及相關 AI 功能。您可以整合 ML 模型來產生嵌入或文字、建立使用模型與工具執行多步驟任務的代理程式，或執行內建演算法來分析您的資料。

## 互動式示範

{% include cards.html cards=page.demo_cards %}

## ML 模型

OpenSearch 支援 ML 模型，可用於透過語意理解提升搜尋相關性。您可以直接在 OpenSearch 叢集內部署模型，或連線至託管於外部平台上的模型。這些模型可將文字轉換為向量嵌入以啟用語意搜尋功能，或提供文字生成與問答等進階功能。如需更多資訊，請參閱[整合 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/)。

{% include cards.html cards=page.models %}

## 代理程式與工具

_代理程式_ 使用大型語言模型 (LLM) 來規劃並執行多步驟任務，例如回答有關您資料的問題，或從自然語言產生查詢。為了執行這些任務，代理程式會呼叫_工具_，每個工具執行特定操作，例如執行搜尋或列出索引。如需更多資訊，請參閱[代理程式與工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/index/)。

{% include cards.html cards=page.agents %}

## MCP 伺服器與用戶端

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 是一項開放標準，定義 AI 應用程式如何探索與呼叫工具。OpenSearch 可以作為 MCP 用戶端，讓其代理程式呼叫外部工具；也可以作為 MCP 伺服器，讓外部 AI 應用程式呼叫 OpenSearch 工具。如需更多資訊，請參閱[MCP 伺服器與用戶端]({{site.url}}{{site.baseurl}}/ml-commons-plugin/mcp/)。

{% include cards.html cards=page.mcp %}

## 記憶與脈絡

代理程式可以在對話之間保留資訊，並控制傳送給 LLM 的脈絡量。如需更多資訊，請參閱[記憶與脈絡]({{site.url}}{{site.baseurl}}/ml-commons-plugin/memory-and-context/)。

{% include cards.html cards=page.memory %}

## 用於資料分析的內建演算法

OpenSearch 內建可直接在叢集內分析資料的演算法，讓您無需外部 ML 模型即可執行異常偵測、資料分群與預測分析等任務。

{% include cards.html cards=page.algorithms %}

## 建置您的解決方案

{% include cards.html cards=page.more_cards %}