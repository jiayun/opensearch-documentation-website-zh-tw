---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得訊息"
parent: Memory APIs
grand_parent: ML APIs
nav_order: 50
---

# 取得訊息 API
**於 2.12 版推出**
{: .label .label-purple }

使用此 API 來擷取[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)的訊息資訊。

若要擷取訊息資訊，您可以：

- [依 ID 取得訊息](#get-a-message-by-id)。
- [取得記憶內的所有訊息](#get-all-messages-within-a-memory)。

當 Security 外掛程式啟用時，所有記憶都存在於 `private` 安全性模式中。只有建立記憶的使用者才能與該記憶及其訊息互動。
{: .important}

## 依 ID 取得訊息

您可以使用 `message_id` 來擷取訊息資訊。

### 端點

```json
GET /_plugins/_ml/memory/message/{message_id}
```

### 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`message_id` | 字串 | 要擷取的訊息 ID。

## 範例請求

```json
GET /_plugins/_ml/memory/message/0m8ya40BfUsSoeNTj-pU
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "memory_id": "gW8Aa40BfUsSoeNTvOKI",
  "message_id": "0m8ya40BfUsSoeNTj-pU",
  "create_time": "2024-02-02T19:01:32.113621539Z",
  "updated_time": "2024-02-02T19:01:32.113621539Z",
  "response": "Hello, this is OpenAI. Here is the answer to your question.",
  "additional_info": {
    "suggestion": "api.openai.com"
  }
}
```

如需回應欄位的相關資訊，請參閱[建立訊息請求欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/create-message#request-body-fields)。

## 取得記憶內的所有訊息

使用此命令來取得特定記憶的訊息清單。

### 端點

```json
GET /_plugins/_ml/memory/{memory_id}/messages
```

### 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`memory_id` | 字串 | 要擷取訊息的記憶 ID。

### 查詢參數

使用下列查詢參數來自訂結果。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`max_results` | 整數 | 要傳回的訊息數量上限。預設為 `10`。
`next_token` | 整數 | 排序後訊息清單中要傳回的第一則訊息索引。訊息依 `create_time` 排序，從最舊的訊息開始。預設為 `0`。

結果不包含追蹤訊息。若要擷取追蹤訊息，請使用[取得訊息追蹤 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/get-message-traces/)。

## 回應本文欄位

下表列出可用的回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `memory_id` | 字串 | 記憶 ID。 |
| `message_id` | 字串 | 訊息 ID。 |
| `create_time` | 字串 | 訊息建立的時間。 |
| `updated_time` | 字串 | 訊息最後更新的時間。 |
| `input` | 字串 | 訊息中的問題 (人類輸入)。 |
| `prompt_template` | 字串 | 訊息所使用的提示範本。 |
| `response` | 字串 | 問題的答案 (生成式 AI 輸出)。 |
| `origin` | 字串 | 產生回應的 AI 或其他系統的名稱。 |
| `additional_info` | 物件 | 傳送至 `origin` 的任何其他資訊。 |
| `parent_message_id` | 字串 | 上層訊息的 ID (適用於追蹤訊息)。 |
| `trace_number` | 整數 | 追蹤編號 (適用於追蹤訊息)。 |
| `next_token` | 整數 | 下一頁結果中第一個要傳回的訊息索引。僅在可能還有更多結果時才會出現。 |

沒有值的欄位會從回應中省略。

## 範例請求

```json
GET /_plugins/_ml/memory/gW8Aa40BfUsSoeNTvOKI/messages
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "messages": [
    {
      "memory_id": "gW8Aa40BfUsSoeNTvOKI",
      "message_id": "BW8ha40BfUsSoeNT8-i3",
      "create_time": "2024-02-02T18:43:23.566994302Z",
      "updated_time": "2024-02-02T18:43:23.566994302Z",
      "input": "How do I make an interaction?",
      "prompt_template": "Hello OpenAI, can you answer this question?",
      "response": "Hello, this is OpenAI. Here is the answer to your question.",
      "origin": "MyFirstOpenAIWrapper",
      "additional_info": {
        "suggestion": "api.openai.com"
      }
    },
    {
      "memory_id": "gW8Aa40BfUsSoeNTvOKI",
      "message_id": "0m8ya40BfUsSoeNTj-pU",
      "create_time": "2024-02-02T19:01:32.113621539Z",
      "updated_time": "2024-02-02T19:01:32.113621539Z",
      "response": "Hello, this is OpenAI. Here is the answer to your question.",
      "additional_info": {
        "suggestion": "api.openai.com"
      }
    }
  ]
}
```
