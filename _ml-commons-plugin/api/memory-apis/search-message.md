---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋訊息"
parent: Memory APIs
grand_parent: ML Commons APIs
nav_order: 60
---

# Search Message API
**於 2.12 版推出**
{: .label .label-purple }

擷取[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)的訊息資訊。您可以將查詢傳送至 `_search` 端點，以在記憶中搜尋相符的訊息。

啟用 Security 外掛程式時，所有記憶都處於 `private` 安全性模式。只有建立記憶的使用者可以與該記憶及其訊息互動。
{: .important}

## 端點

```json
POST /_plugins/_ml/memory/{memory_id}/_search
GET /_plugins/_ml/memory/{memory_id}/_search
```

### 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`memory_id` | 字串 | 用來搜尋符合查詢之訊息的記憶 ID。

## 回應本文欄位

下表列出可用的回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `memory_id` | 字串 | 記憶 ID。 |
| `message_id` | 字串 | 訊息 ID。 |
| `create_time` | 字串 | 建立訊息的時間。 |
| `updated_time` | 字串 | 上次更新訊息的時間。 |
| `input` | 字串 | 訊息中的問題 (人類輸入)。 |
| `prompt_template` | 字串 | 用於訊息的提示範本。 |
| `response` | 字串 | 問題的答案 (生成式 AI 輸出)。 |
| `origin` | 字串 | 產生回應的 AI 或其他系統名稱。 |
| `additional_info` | 物件 | 傳送至 `origin` 的任何其他資訊。 |
| `parent_message_id` | 字串 | 父訊息的 ID (用於追蹤訊息)。 |
| `trace_number` | 整數 | 追蹤編號 (用於追蹤訊息)。 |

## 範例請求

```json
GET /_plugins/_ml/memory/gW8Aa40BfUsSoeNTvOKI/_search
{
  "query": {
    "match": {
      "input": "interaction"
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "took": 5,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.47000366,
    "hits": [
      {
        "_index": ".plugins-ml-memory-message",
        "_id": "BW8ha40BfUsSoeNT8-i3",
        "_version": 1,
        "_seq_no": 0,
        "_primary_term": 1,
        "_score": 0.47000366,
        "_source": {
          "input": "How do I make an interaction?",
          "memory_id": "gW8Aa40BfUsSoeNTvOKI",
          "trace_number": null,
          "create_time": "2024-02-02T18:43:23.566994302Z",
          "updated_time": "2024-02-02T18:43:23.566994302Z",
          "additional_info": {
            "suggestion": "api.openai.com"
          },
          "response": "Hello, this is OpenAI. Here is the answer to your question.",
          "origin": "MyFirstOpenAIWrapper",
          "parent_message_id": null,
          "prompt_template": "Hello OpenAI, can you answer this question?"
        }
      }
    ]
  }
}
```
