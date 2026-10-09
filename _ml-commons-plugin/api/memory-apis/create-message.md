---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新訊息"
parent: Memory APIs
grand_parent: ML Commons APIs
nav_order: 40
---

# 建立或更新訊息 API
**於 2.12 版推出**
{: .label .label-purple }

使用此 API 在[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)的對話記憶中建立或更新訊息。記憶會儲存目前對話的對話歷程。訊息代表對話中的一組問答。

建立訊息後，您會將其 `message_id` 提供給其他 API。

POST 方法會建立新訊息。PUT 方法會更新現有訊息。

您只能更新訊息的 `additional_info` 欄位。
{: .note}

啟用 Security 外掛程式時，所有記憶都處於 `private` 安全性模式。只有建立記憶的使用者可以與該記憶及其訊息互動。
{: .important}

## 端點

```json
POST /_plugins/_ml/memory/{memory_id}/messages
PUT /_plugins/_ml/memory/message/{message_id}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`memory_id` | 字串 | 要新增訊息的記憶 ID。POST 方法為必要。
`message_id` | 字串 | 要更新的訊息 ID。PUT 方法為必要。

## 請求本文欄位

下表列出可用的請求欄位。

欄位 | 資料類型 | 必要／選用 | 可更新 | 說明
:--- | :--- | :--- | :--- | :---
`input` | 字串 | 選用 | 否 | 訊息中的問題 (人類輸入)。 |
`prompt_template` | 字串 | 選用 | 否 | 用於該訊息的提示範本。範本可能包含傳送給大型語言模型的指示或範例。 |
`response` | 字串 | 選用 | 否 | 問題的答案 (生成式 AI 輸出)。 |
`origin` | 字串 | 選用 | 否 | 產生回應的 AI 或其他系統名稱。 |
`additional_info` | 物件 | 選用 | 是 | 傳送給 `origin` 的任何其他資訊。 |

若要成功建立或更新訊息，您必須至少提供上述其中一個欄位。提供的欄位不能為 null 或空白。
{: .note}

## 回應本文欄位

下表列出可用的回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `memory_id` | 字串 | 記憶 ID。 |
| `message_id` | 字串 | 訊息 ID。 |
| `create_time` | 字串 | 建立訊息的時間。 |
| `updated_time` | 字串 | 上次更新訊息的時間。 |
| `input` | 字串 | 訊息中的問題 (人類輸入)。 |
| `prompt_template` | 字串 | 用於該訊息的提示範本。 |
| `response` | 字串 | 問題的答案 (生成式 AI 輸出)。 |
| `origin` | 字串 | 產生回應的 AI 或其他系統名稱。 |
| `additional_info` | 物件 | 傳送給 `origin` 的任何其他資訊。 |
| `parent_message_id` | 字串 | 父訊息的 ID (用於追蹤訊息)。 |
| `trace_number` | 整數 | 追蹤編號 (用於追蹤訊息)。 |

## 範例請求：建立訊息

```json
POST /_plugins/_ml/memory/SXA2cY0BfUsSoeNTz-8m/messages
{
    "input": "How do I make an interaction?",
    "prompt_template": "Hello OpenAI, can you answer this question?",
    "response": "Hello, this is OpenAI. Here is the answer to your question.",
    "origin": "MyFirstOpenAIWrapper",
    "additional_info": {
      "suggestion": "api.openai.com"
    }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "message_id": "WnA3cY0BfUsSoeNTI-_J"
}
```

## 範例請求：新增欄位至 `additional_info`

```json
PUT /_plugins/_ml/memory/message/WnA3cY0BfUsSoeNTI-_J
{
  "additional_info": {
    "feedback": "positive"
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "_index": ".plugins-ml-memory-message",
  "_id": "WnA3cY0BfUsSoeNTI-_J",
  "_version": 2,
  "result": "updated",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 45,
  "_primary_term": 1
}
```

更新後的訊息包含額外的 `feedback` 欄位：

```json
{
  "memory_id": "SXA2cY0BfUsSoeNTz-8m",
  "message_id": "WnA3cY0BfUsSoeNTI-_J",
  "create_time": "2024-02-03T23:04:15.554370024Z",
  "updated_time": "2024-02-03T23:05:20.123456789Z",
  "input": "How do I make an interaction?",
  "prompt_template": "Hello OpenAI, can you answer this question?",
  "response": "Hello, this is OpenAI. Here is the answer to your question.",
  "origin": "MyFirstOpenAIWrapper",
  "additional_info": {
    "feedback": "positive",
    "suggestion": "api.openai.com"
  }
}
```

## 範例請求：變更 `additional_info` 中的欄位

```json
PUT /_plugins/_ml/memory/message/WnA3cY0BfUsSoeNTI-_J
{
  "additional_info": {
    "feedback": "negative"
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "_index": ".plugins-ml-memory-message",
  "_id": "WnA3cY0BfUsSoeNTI-_J",
  "_version": 3,
  "result": "updated",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 46,
  "_primary_term": 1
}
```

更新後的訊息包含已更新的 `feedback` 欄位：

```json
{
  "memory_id": "SXA2cY0BfUsSoeNTz-8m",
  "message_id": "WnA3cY0BfUsSoeNTI-_J",
  "create_time": "2024-02-03T23:04:15.554370024Z",
  "updated_time": "2024-02-03T23:06:45.987654321Z",
  "input": "How do I make an interaction?",
  "prompt_template": "Hello OpenAI, can you answer this question?",
  "response": "Hello, this is OpenAI. Here is the answer to your question.",
  "origin": "MyFirstOpenAIWrapper",
  "additional_info": {
    "feedback": "negative",
    "suggestion": "api.openai.com"
  }
}
```