---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "更新代理程式"
parent: Agent APIs
grand_parent: ML Commons APIs
nav_order: 15
---

# Update Agent API
**3.1 版引入**
{: .label .label-purple }

使用此 API 更新現有代理程式的組態。

## 端點

```json
PUT /_plugins/_ml/agents/{agent_id}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `agent_id` | 字串 | 要更新之代理程式的代理程式 ID。 |

## 請求本文欄位

下表列出可用的請求欄位。所有請求本文欄位皆為選用。

欄位 | 資料類型 | 代理程式類型 | 說明
:---  | :--- | :--- | :--- 
`name`| 字串 | 全部 | 代理程式名稱。 
`description` | 字串 | 全部 | 代理程式的說明。 
`tools` | 陣列 | 全部 | 代理程式可執行的一系列工具。 
`app_type` | 字串 | 全部 | 指定選用的代理程式類別。
`memory.type` | 字串 | `conversational_flow`, `conversational` | 指定交談記憶體的儲存位置。唯一支援的類型為 `conversation_index` (將記憶體儲存在交談系統索引中)。
`llm.model_id` | 字串 | `conversational` | 要傳送問題給大型語言模型 (LLM) 的模型 ID。
`llm.parameters.response_filter` | 字串 | `conversational` | 解析 LLM 回應的模式。
`llm.parameters.max_iteration` | 整數 | `conversational` | 要傳送給 LLM 的訊息數量上限。

## 範例請求：更新工具的提示詞

```json
PUT /_plugins/_ml/agents/N8AE1osB0jLkkocYjz7D
{
  "name": "Updated_Test_Agent_For_RAG",
  "description": "Updated description for test agent",
  "tools": [
    {
      "type": "MLModelTool",
      "description": "Updated general tool to answer any question",
      "parameters": {
        "model_id": "NWR9YIsBUysqmzBdifVJ",
        "prompt": "This is an updated prompt"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
    "_index": ".plugins-ml-agent",
    "_id": "ryN5jpcBfY4uTYhorKvh",
    "_version": 2,
    "result": "updated",
    "_shards": {
        "total": 1,
        "successful": 1,
        "failed": 0
    },
    "_seq_no": 1,
    "_primary_term": 1
}
```