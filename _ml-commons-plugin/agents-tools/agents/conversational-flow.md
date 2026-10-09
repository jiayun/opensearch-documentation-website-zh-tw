---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "對話流程代理程式"
has_children: false
has_toc: false
nav_order: 20
parent: Agents
grand_parent: Agents and tools
---

# 對話流程代理程式
**於 2.13 版導入**
{: .label .label-purple }

與[流程代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/flow/)類似，對話流程代理程式會設定一組工具，並依序執行。兩者的差異在於對話流程代理程式會將對話儲存在索引中，例如以下範例中的 `conversation_index`。下列代理程式會先執行 `VectorDBTool`，再執行 `MLModelTool`：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "population data analysis agent",
  "type": "conversational_flow",
  "description": "This is a demo agent for population data analysis",
  "app_type": "rag",
  "memory": {
    "type": "conversation_index"
  },
  "tools": [
    {
      "type": "VectorDBTool",
      "name": "population_knowledge_base",
      "parameters": {
        "model_id": "YOUR_TEXT_EMBEDDING_MODEL_ID",
        "index": "test_population_data",
        "embedding_field": "population_description_embedding",
        "source_field": [
          "population_description"
        ],
        "input": "${parameters.question}"
      }
    },
    {
      "type": "MLModelTool",
      "name": "bedrock_claude_model",
      "description": "A general tool to answer any question",
      "parameters": {
        "model_id": "YOUR_LLM_MODEL_ID",
        "prompt": """

Human:You are a professional data analyst. You will always answer question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say don't know. 

Context:
${parameters.population_knowledge_base.output:-}

${parameters.chat_history:-}

Human:${parameters.question}

Assistant:"""
      }
    }
  ]
}
```
{% include copy-curl.html %}

如需 Register Agent API 請求欄位的詳細資訊，請參閱[請求本文欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/#request-body-fields)。

如需逐步教學，請參閱[代理程式與工具教學]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents-tools-tutorial/)。

## 使用外部 MCP 工具
**於 3.8 版導入**
{: .label .label-purple }

對話流程代理程式可以在固定管線中呼叫外部 MCP 伺服器工具，並與 `MLModelTool` 等 OpenSearch 工具並用。請設定 `parameters.mcp_connectors`，並使用 `McpStreamableHttpTool` 或 `McpSseTool` 在 `tools` 陣列中明確宣告每個 MCP 工具。如需設定步驟與範例，請參閱[在流程代理程式與對話流程代理程式中使用 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/mcp-connector/#flow-agents-and-conversational-flow-agents)。

## 後續步驟

- 若要進一步了解如何註冊代理程式，請參閱 [Register Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/)。
- 如需支援的工具清單，請參閱[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。
- 如需逐步教學，請參閱[代理程式與工具教學]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents-tools-tutorial/)。
- 如需支援的 API，請參閱[代理程式 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/)。
- 若要在組態自動化中使用代理程式與工具，請參閱[自動化組態]({{site.url}}{{site.baseurl}}/automating-configurations/index/)。