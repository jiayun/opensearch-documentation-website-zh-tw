---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理程式工具"
has_children: false
has_toc: false
nav_order: 10
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# 代理程式工具
**於 2.13 版推出**
{: .label .label-purple }
<!-- vale on -->

`AgentTool` 可執行任何代理程式。

## 步驟 1：設定供 AgentTool 執行的代理程式

設定任何代理程式。例如，依照 [ML Model Tool 文件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/ml-model-tool/)中的步驟，設定執行 `MLModelTool` 的流程代理程式，並從[步驟 3]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/ml-model-tool/#step-3-register-a-flow-agent-that-will-run-the-mlmodeltool) 取得其代理程式 ID：

```json
{
  "agent_id": "9X7xWI0Bpc3sThaJdY9i"
}
```

## 步驟 2：註冊將執行 AgentTool 的流程代理程式

流程代理程式會依序執行一系列工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求，並提供上一步取得的代理程式 ID：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test agent tool",
  "type": "flow",
  "description": "this is a test agent",
  "tools": [
    {
      "type": "AgentTool",
      "description": "A general agent to answer any question",
      "parameters": {
        "agent_id": "9X7xWI0Bpc3sThaJdY9i"
      }
    }
  ]
}
```
{% include copy-curl.html %} 

如需參數說明，請參閱[註冊參數](#register-parameters)。

OpenSearch 會回應代理程式 ID：

```json
{
  "agent_id": "EQyyZ40BT2tRrkdmhT7_"
}
```

## 步驟 3：執行代理程式

傳送下列請求以執行代理程式：

```json
POST /_plugins/_ml/agents/EQyyZ40BT2tRrkdmhT7_/_execute
{
  "parameters": {
    "question": "what's the population increase of Seattle from 2021 to 2023"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會傳回推論結果：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": " I do not have direct data on the population increase of Seattle from 2021 to 2023 in the context provided. As a data analyst, I would need to research population statistics from credible sources like the US Census Bureau to analyze population trends and make an informed estimate. Without looking up actual data, I don't have enough information to provide a specific answer to the question."
        }
      ]
    }
  ]
}
```

## 註冊參數

下表列出註冊代理程式時可用的所有工具參數。

參數	| 類型 | 必要/選用 | 說明	
:--- | :--- | :--- | :---
`agent_id` | 字串 | 必要 | 要執行的代理程式之代理程式 ID。

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

參數	| 類型 | 必要/選用 | 說明	
:--- | :--- | :--- | :---
`question` | 字串 | 必要 | 要傳送給 LLM 的自然語言問題。 

## 測試工具

您可以將此工具作為代理程式工作流程的一部分執行，也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 可用於測試個別工具或執行獨立操作。