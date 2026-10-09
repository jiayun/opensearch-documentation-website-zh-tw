---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得代理程式"
parent: Agent APIs
grand_parent: ML Commons APIs
nav_order: 30
---

# Get Agent API
**2.13 版新增**
{: .label .label-purple }

您可以使用 `agent_id` 擷取代理程式資訊。

## 端點

```json
GET /_plugins/_ml/agents/{agent_id}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `agent_id` | String | 要擷取之代理程式的代理程式 ID。 |


## 範例請求

```json
GET /_plugins/_ml/agents/N8AE1osB0jLkkocYjz7D
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "name": "Test_Agent_For_RAG",
  "type": "flow",
  "description": "this is a test agent",
  "tools": [
    {
      "type": "VectorDBTool",
      "parameters": {
        "input": "${parameters.question}",
        "source_field": """["text"]""",
        "embedding_field": "embedding",
        "index": "my_test_data",
        "model_id": "zBRyYIsBls05QaITo5ex"
      },
      "include_output_in_agent_response": false
    },
    {
      "type": "MLModelTool",
      "description": "A general tool to answer any question",
      "parameters": {
        "model_id": "ygAzT40Bdo8gePIqxk0H",
        "prompt": """

Human:You are a professional data analyst. You will always answer question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say don't know. 

 Context:
${parameters.VectorDBTool.output}

Human:${parameters.question}

Assistant:"""
      },
      "include_output_in_agent_response": false
    }
  ],
  "created_time": 1706821658743,
  "last_updated_time": 1706821658743
}
```

## 回應本文欄位

回應欄位的說明請參閱 [Register Agent API 請求欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent#request-body-fields)。