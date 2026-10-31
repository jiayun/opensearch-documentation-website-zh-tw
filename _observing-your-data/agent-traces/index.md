---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理程式監控"
parent: Observability workspace apps
nav_order: 60
has_children: true
has_toc: false
redirect_from:
  - /observing-your-data/agent-traces/
---

# 代理程式監控
**於 3.6 版導入**
{: .label .label-purple }

代理程式監控為生成式 AI 應用程式與大型語言模型 (LLM) 代理程式提供可觀測性。它使用代理程式追蹤（agent traces），依循 OpenTelemetry 的[生成式 AI 語意慣例](https://opentelemetry.io/docs/specs/semconv/gen-ai/)記錄 LLM 呼叫、詞元用量、工具叫用，以及代理程式的推理流程。

## 必要條件

代理程式監控需要下列元件：

- 一個 OpenSearch 叢集，將追蹤資料儲存在 `otel-v1-apm-span-*` 索引中。
- OpenSearch Dashboards，須具備一個 Observability 工作區，並將 `explore.enabled` 與 `explore.agentTraces.enabled` 設定設為 `true`。如需更多資訊，請參閱 [可觀測性工作區應用程式]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/)。
- 一個 [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)。
- [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/)，用於處理追蹤資料並寫入 OpenSearch。
- 使用 OpenTelemetry [生成式 AI 語意慣例](https://opentelemetry.io/docs/specs/semconv/gen-ai/)進行檢測的應用程式。如需更多資訊，請參閱 [為您的應用程式加入遙測]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/instrument/)。

## 代理程式追蹤的工作流程

代理程式追蹤的工作流程包含下列階段：

1. **檢測**：為您的 AI 應用程式加入可觀測性：
   - 使用 [GenAI SDK](https://observability.opensearch.org/docs/send-data/ai-agents/)，其中包含裝飾器、擴充函式，以及針對 OpenAI、Anthropic、Amazon Bedrock 與 LangChain 等程式庫的自動 LLM 檢測。

2. **標準化**：OpenTelemetry Collector 使用[生成式 AI 語意慣例](https://opentelemetry.io/docs/specs/semconv/gen-ai/)標準化跨度（span），確保各供應商的屬性名稱一致。

3. **使用本機工具**（選用）：在開發過程中使用 [Agent Health](https://observability.opensearch.org/docs/agent-health/) 進行本機除錯、評分與評估。

4. **處理**：[OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 將 OpenTelemetry Protocol (OTLP) 資料路由至 OpenSearch，建立服務地圖、關聯追蹤，並彙總指標。

5. **檢視**：[OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/agent-tracing/) 以階層樹狀圖、有向非循環圖 (DAG) 與時間軸呈現代理程式追蹤，並提供用於生產環境監控的指標。

代理程式追蹤支援下列框架與供應商：

- **框架**：Strands Agents、LangGraph、CrewAI,以及 OpenAI Agents SDK。
- **供應商**：OpenAI、Anthropic、Amazon Bedrock、LangChain、LlamaIndex，以及其他 LLM 供應商。

## 入門

若要開始使用代理程式追蹤，請探索下列主題：

- [檢測您的應用程式]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/instrument/) — 安裝 SDK 並為您的 AI 代理程式加入追蹤。
- [檢視代理程式追蹤]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/agent-tracing/) — 在 OpenSearch Dashboards 中設定與探索代理程式追蹤。
