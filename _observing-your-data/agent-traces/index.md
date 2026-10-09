---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理程式追蹤"
nav_order: 70
has_children: true
has_toc: false
redirect_from:
  - /observing-your-data/agent-traces/
---

# 代理程式追蹤
**3.6 版新增**
{: .label .label-purple }

代理程式追蹤為生成式 AI 應用程式與大型語言模型 (LLM) 代理程式提供可觀測性。與一般應用程式監控不同，代理程式追蹤專門使用[生成式 AI 語意慣例](https://opentelemetry.io/docs/specs/semconv/gen-ai/)來追蹤 LLM 呼叫、詞元使用量、工具叫用，以及代理程式的推理流程。

## 必要條件

若要使用代理程式追蹤，您需要下列項目：

- **OpenSearch 叢集** -- 將追蹤資料儲存在 `otel-v1-apm-span-*` 索引中。
- **[OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/)** -- 提供 **Agent Traces** 面板以進行視覺化。
- **[OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/)** -- 處理追蹤資料並儲存至 OpenSearch。

## 代理程式追蹤工作流程

代理程式追蹤工作流程包含下列階段：

1. **加入追蹤功能 (Instrument)**：為您的 AI 應用程式加入可觀測性：
   - 使用 [GenAI SDK](https://observability.opensearch.org/docs/send-data/ai-agents/)，其中包含裝飾器、擴充函式，以及可為 OpenAI、Anthropic、Amazon Bedrock 和 LangChain 等程式庫自動加入 LLM 追蹤功能的機制。

2. **標準化 (Normalize)**：OpenTelemetry Collector 使用[生成式 AI 語意慣例](https://opentelemetry.io/docs/specs/semconv/gen-ai/)將追蹤區段 (span) 標準化，確保各提供者之間的屬性名稱一致。

3. **使用本機工具** (選用)：在開發期間使用 [Agent Health](https://observability.opensearch.org/docs/agent-health/) 進行本機除錯、評分與評估。

4. **處理**：[OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 將 OpenTelemetry Protocol (OTLP) 資料路由至 OpenSearch，建立服務地圖、關聯追蹤，並彙總指標。

5. **檢視**：[OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/agent-tracing/) 以階層樹、有向非循環圖 (DAG) 與時間軸顯示代理程式追蹤，並提供用於生產環境監控的指標。

代理程式追蹤支援下列框架與提供者：

- **框架**：Strands Agents、LangGraph、CrewAI 以及 OpenAI Agents SDK。
- **提供者**：OpenAI、Anthropic、Amazon Bedrock、LangChain、LlamaIndex 以及其他 LLM 提供者。

## 入門

若要開始使用代理程式追蹤，請探索下列主題：

- [為您的應用程式加入追蹤功能]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/instrument/) -- 安裝 SDK 並為您的 AI 代理程式加入追蹤功能。
- [檢視代理程式追蹤]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/agent-tracing/) -- 在 OpenSearch Dashboards 中設定並探索代理程式追蹤。
