---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行代理程式"
parent: Agent APIs
grand_parent: ML Commons APIs
nav_order: 20
---

# 執行 Agent API
**於 2.13 版推出**
{: .label .label-purple }

執行代理程式時，它會執行其設定中所配置的工具。您可以將 `async` 查詢參數設為 `true`，以非同步方式執行代理程式。

使用[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)建立的代理程式支援標準化的 `input` 欄位，可接受純文字、多模態內容或訊息式對話。這需要啟用 `plugins.ml_commons.unified_agent_api_enabled` 叢集設定。
{: .note}

## 端點

```json
POST /_plugins/_ml/agents/{agent_id}/_execute
```

## 查詢參數

下表列出可用的查詢參數。

參數 | 資料類型 | 必要/選用 | 說明
:---  | :--- | :--- 
`async` | 布林值 | 選用 | 若為 `true`，則以非同步方式執行代理程式，並傳回 `task_id` 以追蹤執行情形。若要檢查任務狀態，請使用 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)。預設值為 `false`。

## 請求本文欄位

下表列出可用的請求欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:---  | :--- | :--- | :---
`parameters`| 物件 | 選用 | 代理程式所需的參數。註冊期間所設定的任何代理程式參數，皆可使用此欄位覆寫。請搭配[一般註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/)使用。
`parameters.question`| 字串 | 選用 | 要向代理程式提出的問題。請搭配[一般註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/)使用。
`parameters.verbose`| 布林值 | 選用 | 提供詳細輸出。
`parameters.memory_id` | 字串 | 選用 | 用於接續現有對話的記憶體工作階段 ID。此欄位支援對話式記憶體後端，包括 `conversation_index` 與 `agentic_memory`。若要開始新的工作階段，請省略此參數。
`parameters.memory_container_id` | 字串 | 選用 | 當代理程式使用 `agentic_memory` 時，針對此次執行覆寫所設定的記憶體容器。
`parameters.include_token_usage` | 布林值 | 選用 | 設為 `true` 時，會在回應中包含每次大型語言模型 (LLM) 呼叫的詳細詞元用量指標。支援 `conversational` (v1)、`plan-execute-reflect` 與 `AG-UI` 代理程式。`conversational_v2` 代理程式一律會在其回應格式中包含詞元用量，不需要此參數。預設值為 `false`。請參閱[追蹤詞元用量](#tracking-token-usage)。
`input` | 字串或陣列 | 選用 | 標準化輸入欄位，支援純文字、多模態內容區塊或訊息式對話。請搭配[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)使用。

> 設定 `conversation_index` 或 `agentic_memory` 時，回應會包含 `memory_id`。若要接續相同的工作階段，請在後續請求中包含 `memory_id`。省略 `memory_id` 即可開始新的工作階段。
>
> 使用 `agentic_memory` 時，您也必須提供記憶體容器 ID。請在代理程式註冊期間 (`memory.memory_container_id`) 或每次請求中 (`parameters.memory_container_id`) 指定。若未提供記憶體容器 ID，請求會失敗。
{: .note}

## 一般代理程式執行

對於使用一般註冊方法（[Register Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/) 多步驟程序）建立的代理程式，請使用 `parameters` 欄位：

```json
POST /_plugins/_ml/agents/879v9YwBjWKCe6Kg12Tx/_execute
{
  "parameters": {
    "question": "what's the population increase of Seattle from 2021 to 2023"
  }
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "inference_results": [
    {
      "output": [
        {
          "result": """ Based on the given context, the key information is:

The metro area population of Seattle in 2021 was 3,461,000.
The metro area population of Seattle in 2023 is 3,519,000.

To calculate the population increase from 2021 to 2023:

Population in 2023 (3,519,000) - Population in 2021 (3,461,000) = 58,000

Therefore, the population increase of Seattle from 2021 to 2023 is 58,000."""
        }
      ]
    }
  ]
}
```

## 回應欄位

下表列出代理程式執行的基本回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `inference_results` | 陣列 | 包含代理程式的執行結果。 |
| `inference_results.output` | 陣列 | 包含具有名稱值對的輸出物件。 |
| `inference_results.output.name` | 字串 | 輸出欄位名稱。常見值：`response`、`memory_id`、`parent_interaction_id`、`token_usage`。 |
| `inference_results.output.result` | 字串 | 簡單字串結果的輸出值（當 `name` 為 `response`、`memory_id` 或 `parent_interaction_id` 時會出現）。 |
| `inference_results.output.dataAsMap` | 物件 | 結構化結果的輸出值。請參閱[詞元用量回應欄位](#token-usage-response-fields)與[`conversational_v2` 代理程式回應格式](#the-conversational_v2-agent-response-format)。 |

## 統一代理程式執行
**於 3.5 版推出**
{: .label .label-purple }

對於使用[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)建立的代理程式，請使用 `input` 欄位。支援的輸入格式取決於代理程式類型：

- **`conversational` 與其他 V1 代理程式類型**：僅支援純文字輸入。
- **`conversational_v2`**（於 3.6 版推出）：支援全部三種輸入格式 — 純文字、多模態內容區塊與訊息式對話。

### 純文字輸入

所有統一代理程式皆支援純文字輸入。若為簡單的文字提示，請直接將字串傳遞至 `input` 欄位：

```json
POST /_plugins/_ml/agents/{agent_id}/_execute
{
  "input": "What tools do you have access to?"
}
```
{% include copy-curl.html %}

#### 範例回應：純文字輸入

```json
{
  "inference_results": [
    {
      "output": [
        {
          "result": "I have access to the following tools:\n\n1. ListIndexTool - Lists all indices in the cluster\n2. SearchIndexTool - Searches within OpenSearch indices\n3. IndexMappingTool - Retrieves index mapping information"
        }
      ]
    }
  ]
}
```

### 多模態內容區塊

使用[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)時，多模態內容區塊與訊息式輸入需要 `conversational_v2` 代理程式。所有其他統一代理程式類型僅接受純文字輸入。使用[一般註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#regular-registration-method)時，若連接器設定為將多模態內容傳遞至 LLM，則可支援多模態，輸入格式取決於連接器組態。
{: .note}

若為多模態輸入（文字、圖片、文件），請使用內容區塊陣列：

```json
POST /_plugins/_ml/agents/{agent_id}/_execute
{
  "input": [
    {
      "type": "text",
      "text": "What can you see in this image?"
    },
    {
      "type": "image",
      "source": {
        "type": "base64",
        "format": "png",
        "data": "iVBORw0KGgoAAAANSUhEUgAA..."
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 支援的內容類型

下表列出支援的內容類型。

| 內容類型 | 說明 | 欄位 |
| :--- | :--- | :--- |
| `text` | 純文字內容 | `text`：文字字串。|
| `image` | 影像資料 | `image.type`：來源類型。有效值為 `base64`。<br>`image.format`：影像格式 (例如 `jpeg`、`png`、`gif` 或 `webp`)。<br>`image.data`：Base64 編碼的影像資料。 |
| `video` | 影片資料 | `video.type`：來源類型。有效值為 `base64`。<br>`video.format`：影片格式 (例如 `mp4`、`mov` 或 `avi`)。<br>`video.data`：Base64 編碼的影片資料。 |
| `document` | 文件資料 | `document.type`：來源類型。有效值為 `base64`。<br>`document.format`：文件格式 (例如 `pdf`、`docx` 或 `txt`)。<br>`document.data`：Base64 編碼的文件資料。 |

### 以訊息為基礎的對話

若為多輪對話，請提供含有角色的訊息陣列：

```json
POST /_plugins/_ml/agents/{agent_id}/_execute
{
  "input": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "I like the color red"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "Thanks for telling me that! I'll remember it."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What color do I like?"
        }
      ]
    }
  ]
}
```
{% include copy-curl.html %}

這些訊息會儲存在代理程式的記憶體中。

#### 訊息欄位

下表列出支援的訊息欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `role` | 字串 | 必要 | 訊息角色。有效值：`user`、`assistant`。 |
| `content` | 陣列 | 必要 | 內容區塊的陣列 (文字、影像等)。 |

#### 範例回應：以訊息為基礎的對話

代理程式會記住先前訊息的內容：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "memory_id",
          "result": "iEgpJZwBZx9B0F4spD5v"
        },
        {
          "name": "parent_interaction_id",
          "result": "ikgpJZwBZx9B0F4spT61"
        },
        {
          "name": "response",
          "result": "You like the color red, which you mentioned earlier in our conversation."
        }
      ]
    }
  ]
}
```

### `conversational_v2` 代理程式回應格式

`conversational_v2` 代理程式會傳回下列標準化回應格式：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "stop_reason": "end_turn",
            "message": {
              "role": "assistant",
              "content": [
                {
                  "text": "Here is what I found..."
                }
              ]
            },
            "memory_id": "abc123xyz",
            "metrics": {
              "total_usage": {
                "inputTokens": 1234,
                "outputTokens": 567,
                "totalTokens": 1801
              }
            }
          }
        }
      ]
    }
  ]
}
```

下表列出 `conversational_v2` 代理程式回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `stop_reason` | 字串 | 代理程式停止產生回應的原因。有效值為 `end_turn` (正常完成)、`max_iterations` (已達反覆運算上限)，以及 `tool_use` (在叫用工具時停止)。 |
| `message` | 物件 | 助理的最終回應訊息。 |
| `message.role` | 字串 | 一律為 `assistant`。 |
| `message.content` | 陣列 | 包含回應文字或其他內容的內容區塊陣列。 |
| `memory_id` | 字串 | 記憶體工作階段 ID。請在後續請求的 `parameters.memory_id` 欄位中包含此 ID，以繼續對話。 |
| `metrics.total_usage.inputTokens` | 整數 | 取用的輸入詞元數。 |
| `metrics.total_usage.outputTokens` | 整數 | 產生的輸出詞元數。 |
| `metrics.total_usage.totalTokens` | 整數 | 使用的詞元總數。 |

如需統一註冊方法和輸入格式的詳細資訊，請參閱[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)。

## 追蹤詞元使用量
**於 3.6 版推出**
{: .label .label-purple }

當 `include_token_usage` 設為 `true` 時，回應會包含詳細的詞元耗用指標，協助您監控成本、偵錯效能，以及比較模型效率。此參數支援使用一般和統一註冊方法的 `conversational` (v1)、`plan-execute-reflect` 和 `AG-UI` 代理程式。

`conversational_v2` 代理程式會透過 `metrics` 欄位自動在其回應格式中包含詞元使用量，不需要此參數。如需詳細資訊，請參閱[`conversational_v2` 代理程式回應格式](#the-conversational_v2-agent-response-format)。
{: .note}

### 範例請求：一般註冊
**於 3.6 版推出**
{: .label .label-purple }

若為使用一般註冊建立的代理程式，請在 `parameters` 物件中將 `include_token_usage` 設為 `true`。

此範例示範多輪代理程式執行，其中代理程式是使用 `WebSearchTool` 設定的對話式代理程式。會發生多輪執行是因為代理程式：
1. **第 1 輪**：收到問題，推斷需要哪些資訊，並決定使用 `WebSearchTool` 尋找人口資料。
2. **第 2 輪**：收到工具結果，並透過分析和綜合搜尋結果產生最終答案。

```json
POST /_plugins/_ml/agents/879v9YwBjWKCe6Kg12Tx/_execute
{
  "parameters": {
    "question": "what's the population increase of Seattle from 2021 to 2023",
    "include_token_usage": true
  }
}
```
{% include copy-curl.html %}

### 範例請求：統一註冊
**於 3.6 版推出**
{: .label .label-purple }

若為使用統一註冊建立的代理程式，請同時傳遞 `input` 欄位和 `parameters` 物件，並將 `include_token_usage` 設為 `true`：

```json
POST /_plugins/_ml/agents/{agent_id}/_execute
{
  "input": "What tools do you have access to?",
  "parameters": {
    "include_token_usage": true
  }
}
```
{% include copy-curl.html %}

### 範例回應：追蹤詞元使用量

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """ Based on the given context, the key information is:

The metro area population of Seattle in 2021 was 3,461,000.
The metro area population of Seattle in 2023 is 3,519,000.

To calculate the population increase from 2021 to 2023:

Population in 2023 (3,519,000) - Population in 2021 (3,461,000) = 58,000

Therefore, the population increase of Seattle from 2021 to 2023 is 58,000."""
        },
        {
          "name": "token_usage",
          "dataAsMap": {
            "per_turn_usage": [
              {
                "turn": 1,
                "model_id": "rk6okJwB_kOxOUbO6853",
                "model_name": "Sonnet 4",
                "model_url": "https://bedrock-runtime.us-east-1.amazonaws.com/model/us.anthropic.claude-sonnet-4-20250514-v1:0/converse",
                "input_tokens": 1042,
                "output_tokens": 69,
                "total_tokens": 1111,
                "cache_read_input_tokens": 0,
                "cache_creation_input_tokens": 0
              },
              {
                "turn": 2,
                "model_id": "rk6okJwB_kOxOUbO6853",
                "model_name": "Sonnet 4",
                "model_url": "https://bedrock-runtime.us-east-1.amazonaws.com/model/us.anthropic.claude-sonnet-4-20250514-v1:0/converse",
                "input_tokens": 1541,
                "output_tokens": 269,
                "total_tokens": 1810,
                "cache_read_input_tokens": 0,
                "cache_creation_input_tokens": 0
              }
            ],
            "per_model_usage": [
              {
                "model_id": "rk6okJwB_kOxOUbO6853",
                "model_name": "Sonnet 4",
                "model_url": "https://bedrock-runtime.us-east-1.amazonaws.com/model/us.anthropic.claude-sonnet-4-20250514-v1:0/converse",
                "call_count": 2,
                "input_tokens": 2583,
                "output_tokens": 338,
                "total_tokens": 2921,
                "cache_read_input_tokens": 0,
                "cache_creation_input_tokens": 0
              }
            ]
          }
        }
      ]
    }
  ]
}
```

### 詞元使用量輸出回應欄位

`token_usage` 輸出包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `per_turn_usage` | 陣列 | 單次代理程式執行中，每次 LLM 呼叫 (回合) 的詞元使用量記錄陣列。當代理程式需要推理、使用工具，然後產生最終回應時，會發生多個回合——每次 LLM 互動都算一個回合。請參閱[詞元使用量回應欄位](#token-usage-response-fields)。 |
| `per_model_usage` | 陣列 | 依模型分組的彙總詞元使用量。請參閱[詞元使用量回應欄位](#token-usage-response-fields)。 |

### 詞元使用量回應欄位

下表列出 `per_turn_usage` 和 `per_model_usage` 陣列中出現的欄位。

欄位 | 資料類型 | 出現於 | 說明
:---  | :--- | :--- | :---
`input_tokens` | 整數 | 兩者 | 傳送給模型之輸入/提示中的詞元數。
`output_tokens` | 整數 | 兩者 | 模型輸出/完成內容中的詞元數。
`total_tokens` | 整數 | 兩者 | 詞元總數 (輸入 + 輸出)。
`cache_read_input_tokens` | 整數 | 兩者 | 由提示快取提供的輸入詞元數。支援 Anthropic (透過 Bedrock)、OpenAI 和 Gemini。快取的詞元通常比一般輸入詞元便宜。
`cache_creation_input_tokens` | 整數 | 兩者 | 用於建立新快取項目的詞元數。支援 Anthropic (透過 Bedrock)。
`reasoning_tokens` | 整數 | 兩者 | 用於推理或思考的詞元數。僅針對 OpenAI 模型 (從 `completion_tokens_details.reasoning_tokens`) 和 Gemini 模型 (從 `thoughtsTokenCount`) 擷取。
`turn` | 整數 | `per_turn_usage` | 此 LLM 呼叫在代理程式執行中的序號。
`call_count` | 整數 | `per_model_usage` | 使用此模型進行的 LLM 呼叫總數。
`model_id` | 字串 | 兩者 | 內部 OpenSearch 模型 ID。
`model_name` | 字串 | 兩者 | 人類可讀的模型名稱 (例如 `Sonnet 4`、`GPT-4`)。
`model_url` | 字串 | 兩者 | 模型服務的端點 URL。

### 詞元如何計算

詞元計數由模型供應商計算，並可能因斷詞方法而異。如需詞元計算方式的詳細資訊，請參閱您的模型供應商說明文件：
- [Amazon Bedrock TokenUsage](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_TokenUsage.html)
- [OpenAI tokenization](https://platform.openai.com/docs/guides/tokenization)
- [Google Gemini token counting](https://ai.google.dev/gemini-api/docs/tokens)