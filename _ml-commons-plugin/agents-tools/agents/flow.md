---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "流程代理程式"
has_children: false
has_toc: false
nav_order: 10
parent: Agents
grand_parent: Agents and tools
---

# 流程代理程式
**於 2.13 版導入**
{: .label .label-purple }

流程代理程式 (flow agent) 由一組工具組成，並依序執行這些工具。例如，下列代理程式會先執行 `VectorDBTool`，再執行 `MLModelTool`。代理程式會協調這些工具，讓某個工具的輸出可以成為另一個工具的輸入。在此範例中，`VectorDBTool` 會查詢 k-NN 索引，代理程式則將其輸出 `${parameters.VectorDBTool.output}` 作為上下文，連同 `${parameters.question}` 一併傳遞給 `MLModelTool` (請參閱 `prompt` 參數)：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_RAG",
  "type": "flow",
  "description": "this is a test agent",
  "tools": [
    {
      "type": "VectorDBTool",
      "parameters": {
        "model_id": "YOUR_TEXT_EMBEDDING_MODEL_ID",
        "index": "my_test_data",
        "embedding_field": "embedding",
        "source_field": ["text"],
        "input": "${parameters.question}"
      }
    },
    {
      "type": "MLModelTool",
      "description": "A general tool to answer any question",
      "parameters": {
        "model_id": "YOUR_LLM_MODEL_ID",
        "prompt": "\n\nHuman:You are a professional data analyst. You will always answer a question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say you don't know. \n\n Context:\n${parameters.VectorDBTool.output}\n\nHuman:${parameters.question}\n\nAssistant:"
      }
    }
  ]
}
```
{% include copy-curl.html %}

如需 Register Agent API 請求欄位的詳細資訊，請參閱 [Request body fields]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/#request-body-fields)。

如需逐步教學，請參閱 [Agents and tools tutorial]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents-tools-tutorial/)。

## 使用外部 MCP 工具
**於 3.8 版導入**
{: .label .label-purple }

流程代理程式可以在固定管線中呼叫外部 MCP 伺服器工具，並與 `MLModelTool` 等 OpenSearch 工具並用。請設定 `parameters.mcp_connectors`，並使用 `McpStreamableHttpTool` 或 `McpSseTool` 在 `tools` 陣列中明確宣告每個 MCP 工具。如需設定步驟與範例，請參閱 [Using MCP tools with flow agents and conversational flow agents]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/mcp-connector/#flow-agents-and-conversational-flow-agents)。

## 後續步驟

- 若要進一步了解如何註冊代理程式，請參閱 [Register Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/)。
- 如需支援的工具清單，請參閱 [Tools]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。
- 如需逐步教學，請參閱 [Agents and tools tutorial]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents-tools-tutorial/)。
- 如需支援的 API，請參閱 [Agent APIs]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/)。
- 若要在組態自動化中使用代理程式與工具，請參閱 [Automating configurations]({{site.url}}{{site.baseurl}}/automating-configurations/index/)。