---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenSearch Assistant Toolkit
has_children: false
has_toc: false
nav_order: 50
---

# OpenSearch Assistant Toolkit
**於 2.13 版推出**
{: .label .label-purple }

OpenSearch Assistant Toolkit 可協助您為 OpenSearch Dashboards 建立 AI 驅動的助理。此工具組包含下列元素：

- [**代理程式與工具**]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/index/)：_代理程式_ 會與大型語言模型 (LLM) 互動，並執行高階工作，例如摘要，或從自然語言產生 Piped Processing Language (PPL) 查詢。代理程式的高階工作由稱為_工具_的低階工作組成，這些工具可供多個代理程式重複使用。
- [**組態自動化**]({{site.url}}{{site.baseurl}}/automating-configurations/index/)：使用範本為人工智慧與機器學習 (AI/ML) 應用程式設定基礎架構。例如，您可以自動設定要用於聊天或從自然語言產生 PPL 查詢的代理程式。
- [**OpenSearch Dashboards 的 OpenSearch Assistant**]({{site.url}}{{site.baseurl}}/dashboards/dashboards-assistant/index/)：這是 AI 驅動助理的 OpenSearch Dashboards 網頁式介面。助理的工作流程會以各種代理程式與工具進行設定。
 
## 啟用 OpenSearch Assistant

若要啟用 OpenSearch Assistant，請執行下列步驟：

- 透過設定下列設定來啟用代理程式架構與檢索增強生成 (RAG)：
    ```yaml
    plugins.ml_commons.agent_framework_enabled: true
    plugins.ml_commons.rag_pipeline_feature_enabled: true
    ```
    {% include copy.html %}
- 透過設定下列設定來啟用助理：
    ```yaml
    assistant.chat.enabled: true
    observability.query_assist.enabled: true
    ```
    {% include copy.html %}

## 後續步驟

- 如需 OpenSearch Assistant UI 的詳細資訊，請參閱 [OpenSearch Dashboards 的 OpenSearch Assistant]({{site.url}}{{site.baseurl}}/dashboards/dashboards-assistant/index/)