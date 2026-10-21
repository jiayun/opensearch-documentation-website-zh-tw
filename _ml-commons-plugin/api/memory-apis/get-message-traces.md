---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得訊息追蹤"
parent: Memory APIs
grand_parent: ML Commons APIs
nav_order: 70
---

# 取得訊息追蹤 API
**2.12 版新增**
{: .label .label-purple }

使用此 API 來擷取[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)的訊息追蹤資訊。這對除錯很有幫助。

對於每則訊息，代理程式可能需要執行不同的工具。您可以使用 Get Traces API 來取得某則訊息的所有追蹤資料。追蹤資料包含訊息執行的詳細步驟。

使用[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/index/#unified-registration-method)註冊的代理程式不會記錄追蹤資料，因此此 API 對其訊息會傳回空的 `traces` 陣列。

當 Security 外掛程式啟用時，所有記憶都存在於 `private` 安全性模式中。只有建立記憶的使用者才能與該記憶及其訊息互動。
{: .important}


## 端點

```json
GET /_plugins/_ml/memory/message/{message_id}/traces
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`message_id` | 字串 | 要追蹤的訊息 ID。

## 查詢參數

使用下列查詢參數來自訂結果。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`max_results` | 整數 | 要傳回的追蹤數量上限。預設為 `10`。
`next_token` | 整數 | 要傳回的追蹤清單中第一筆追蹤的索引，清單依 `trace_number` 排序。預設為 `0`。

## 回應本文欄位

下表列出可用的回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `memory_id` | 字串 | 記憶 ID。 |
| `message_id` | 字串 | 訊息 ID。 |
| `create_time` | 字串 | 訊息建立的時間。 |
| `updated_time` | 字串 | 訊息最後更新的時間。 |
| `input` | 字串 | 訊息中的問題（人類輸入）。在工具追蹤中，則是傳送給工具的輸入。 |
| `prompt_template` | 字串 | 該訊息所使用的提示詞範本。 |
| `response` | 字串 | 問題的答案（生成式 AI 輸出）。在追蹤中，則是 LLM 回應或工具輸出。 |
| `origin` | 字串 | 產生該回應的 AI 或其他系統的名稱。 |
| `additional_info` | 物件 | 傳送給 `origin` 的任何其他資訊。 |
| `parent_message_id` | 字串 | 上層訊息的 ID（適用於追蹤訊息）。 |
| `trace_number` | 整數 | 追蹤編號（適用於追蹤訊息）。 |
| `next_token` | 整數 | 下一頁結果中第一個要傳回的追蹤索引。僅在可能還有更多結果時才會出現。 |

沒有值的欄位會從回應中省略。

## 範例請求

```json
GET /_plugins/_ml/memory/message/TAuCZY0BT2tRrkdmCPqZ/traces
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "traces": [
    {
      "memory_id": "7Qt4ZY0BT2tRrkdmSPlo",
      "message_id": "TQuCZY0BT2tRrkdmEvpp",
      "create_time": "2026-10-15T18:56:22.771010828Z",
      "updated_time": "2026-10-15T18:56:22.771010828Z",
      "input": "Which index has most documents",
      "response": "{\"metrics\":{\"latencyMs\":816},\"output\":{\"message\":{\"content\":[{\"text\":\"I'll check all the indices in the OpenSearch cluster to find which one has the most documents.\"},{\"toolUse\":{\"input\":{\"indices\":[]},\"name\":\"ListIndexTool\",\"toolUseId\":\"tooluse_0f8V4bl1yDthOP38a0b1Oo\",\"type\":\"tool_use\"}}],\"role\":\"assistant\"}},\"stopReason\":\"tool_use\",\"usage\":{\"cacheReadInputTokenCount\":0,\"cacheReadInputTokens\":0,\"cacheWriteInputTokenCount\":0,\"cacheWriteInputTokens\":0,\"inputTokens\":748,\"outputTokens\":75,\"serverToolUsage\":{},\"totalTokens\":823}}",
      "origin": "LLM",
      "parent_message_id": "TAuCZY0BT2tRrkdmCPqZ",
      "trace_number": 1
    },
    {
      "memory_id": "7Qt4ZY0BT2tRrkdmSPlo",
      "message_id": "TguCZY0BT2tRrkdmEvp7",
      "create_time": "2026-10-15T18:56:22.775631733Z",
      "updated_time": "2026-10-15T18:56:22.775631733Z",
      "input": "{\"indices\":[]}",
      "response": """row,health,status,index,uuid,pri(number of primary shards),rep(number of replica shards),docs.count(number of available documents),docs.deleted(number of deleted documents),store.size(store size of primary and replica shards),pri.store.size(store size of primary shards)
1,green,open,.plugins-ml-model-group,lHgGEgJhT_mpADyOZoXl2g,1,0,7,3,61.1kb,61.1kb
2,green,open,.plugins-ml-memory-message,wTNBU4BBQVSFcFhNlUdfBQ,1,0,21,2,55.9kb,55.9kb
...
10,green,open,opensearch_dashboards_sample_data_ecommerce,wnE6r7OvSPqc5YHj8wHSLA,1,0,4675,0,4.9mb,4.9mb
""",
      "origin": "ListIndexTool",
      "parent_message_id": "TAuCZY0BT2tRrkdmCPqZ",
      "trace_number": 2
    },
    {
      "memory_id": "7Qt4ZY0BT2tRrkdmSPlo",
      "message_id": "UwuCZY0BT2tRrkdmHPos",
      "create_time": "2026-10-15T18:56:24.876003692Z",
      "updated_time": "2026-10-15T18:56:24.876003692Z",
      "input": "Which index has most documents",
      "response": "Based on the results, **`opensearch_dashboards_sample_data_ecommerce`** index has the most documents with **4,675 documents**.\n\nHere's a summary of the top indices by document count:\n1. **opensearch_dashboards_sample_data_ecommerce** - 4,675 documents\n2. **top_queries-2026.10.15-59495** - 231 documents\n...",
      "origin": "LLM",
      "parent_message_id": "TAuCZY0BT2tRrkdmCPqZ",
      "trace_number": 3
    }
  ]
}
```