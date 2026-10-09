---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "上下文管理"
parent: Memory and context
nav_order: 20
---

# 上下文管理
**於 3.5 版導入**
{: .label .label-purple }

上下文管理讓 OpenSearch 代理程式能夠在向大型語言模型（LLM）傳送請求之前，動態最佳化其上下文。這項彈性功能有助於防止上下文視窗溢出、減少詞元用量，並透過智慧化管理對話歷史、工具互動及其他上下文資訊，支援長時間執行的代理程式。

使用上下文管理，您可以建置能夠執行下列動作的 AI 代理程式：

- 在接近詞元上限時自動截斷過長的工具輸出。
- 摘要冗長的工具互動以保留重要資訊。
- 套用滑動視窗方式以維持最近的上下文。
- 依據特定使用案例實作自訂的上下文最佳化策略。
- 在代理程式執行的不同階段掛鉤以轉換上下文。

上下文管理採用以掛鉤為基礎的系統，允許可插拔的上下文管理器在特定執行點檢查並轉換代理程式的上下文。您可以嘗試不同的組態與組合，為您的特定使用案例找出最佳設定。

## 設定上下文管理

上下文管理會將上下文管理器組成團隊，使其在代理程式生命週期的特定執行點共同最佳化上下文。此系統具有高度可設定性，可讓您依據特定需求調整其行為。

每個上下文管理可以使用下列元件進行設定：

- **名稱**：上下文管理的唯一識別碼。
- **描述**：以人類可讀方式描述上下文管理的用途。
- **掛鉤**：上下文管理器運作的各種執行點。
- **上下文管理器**：執行特定上下文轉換的個別元件。
- **啟動規則**：決定上下文管理器何時執行的條件。

您可以混搭不同的上下文管理器、調整其參數，並嘗試各種啟動門檻，以在您的使用案例中達到最佳效能。

例如，若要建立一個名為 `token-aware-truncation` 且包含 `ToolsOutputTruncateManager` 與 `SlidingWindowManager` 的上下文管理，請傳送下列請求：

```json
POST /_plugins/_ml/context_management/token-aware-truncation
{
  "description": "Context management that truncates tool outputs longer than 100,000 characters and applies sliding window to keep last 6 messages when tokens exceed 200,000",
  "hooks": {
    "post_tool": [
      {
        "type": "ToolsOutputTruncateManager",
        "config": {
          "max_output_length": 100000
        }
      }
    ],
    "pre_llm": [
      {
        "type": "SlidingWindowManager",
        "config": {
          "max_messages": 6,
          "activation": {
            "tokens_exceed": 200000
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

## 掛鉤系統

上下文管理採用以掛鉤為基礎的架構，讓上下文管理器團隊能在代理程式執行期間的特定時間點執行。支援的掛鉤如下：

- `pre_llm` -- 在向 LLM 傳送請求之前執行。
- `post_tool` -- 在工具執行完成之後執行。

為每個掛鉤註冊的上下文管理器，會依照其在上下文管理組態中定義的順序執行。

這些掛鉤在 OpenSearch 的[對話式代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational/)與[規劃與執行代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/plan-execute-reflect/)中均受支援。

## 啟動規則

啟動規則決定上下文管理器在代理程式互動期間何時執行。這些規則可協助您控制資源用量並最佳化效能，只在需要時才觸發上下文最佳化。若未指定任何啟動規則，上下文管理器會在其設定的掛鉤上於每次互動時執行。

上下文管理器支援數種啟動規則類型，可單獨使用或合併使用。

### 一律啟動

使用 `always` 規則類型，在其設定的掛鉤上於每次執行時啟動上下文管理器，無論對話狀態為何：

```json
{
  "activation": {
    "rule_type": "always"
  }
}
```

這等同於不指定任何啟動規則，當您想要明確控制啟動行為時非常實用。

### 訊息數量門檻

使用 `message_count_exceed` 在對話歷史超過指定的訊息數量時啟動上下文管理器：

```json
{
  "activation": {
    "message_count_exceed": 20
  }
}
```

當對話變得冗長時，此規則適合用來套用滑動視窗或摘要等上下文最佳化策略。

### 詞元數量門檻

使用 `tokens_exceed` 在整個上下文視窗的估計詞元數量超過門檻時啟動上下文管理器。上下文視窗包含系統提示、使用者提示、聊天歷史（對話記憶）以及工具互動：

```json
{
  "activation": {
    "tokens_exceed": 200000
  }
}
```

此規則有助於防止上下文視窗溢出，並在超過模型上限之前觸發最佳化策略，以管理 LLM API 成本。

### 合併多項規則

您可以使用 AND 邏輯合併多項啟動規則。上下文管理器只有在所有指定條件都符合時才會執行：

```json
{
  "activation": {
    "message_count_exceed": 15,
    "tokens_exceed": 200000
  }
}
```

此範例只有在訊息數量超過 15 且詞元數量超過 200,000 時才啟動上下文管理器，可對最佳化發生的時機提供精細控制。

## 上下文管理器類型

OpenSearch 提供下列上下文管理器類型。如需完整的組態參數詳細資訊，請參閱[上下文管理器組態]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/create-context-management/#context-manager-configurations)。

### SlidingWindowManager

實作滑動視窗方式，僅保留最近的 N 次互動，以防止上下文視窗溢出。此範例展示一個滑動視窗管理器，保留最近的 6 則訊息，並在對話超過 12 則訊息時啟動：

```json
{
  "type": "SlidingWindowManager",
  "config": {
    "max_messages": 6,
    "activation": {
      "message_count_exceed": 12
    }
  }
}
```

如需更多資訊，請參閱 [SlidingWindowManager]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/create-context-management/#slidingwindowmanager)。

### SummarizationManager

在接近詞元上限時摘要冗長的對話或工具互動。此範例展示一個摘要管理器，在保留最近 10 則訊息的同時摘要 30% 的對話歷史，並在上下文超過 200,000 個詞元時啟動：

```json
{
  "type": "SummarizationManager",
  "config": {
    "summary_ratio": 0.3,
    "preserve_recent_messages": 10,
    "summarization_model_id": "<your-summarization-model-id>",
    "activation": {
      "tokens_exceed": 200000
    }
  }
}
```

如需更多資訊，請參閱 [SummarizationManager]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/create-context-management/#summarizationmanager)。

### ToolsOutputTruncateManager

在工具輸出超過指定上限時加以截斷，以防止上下文溢出。此範例展示一個截斷管理器，將工具輸出限制為 40,000 個字元，並在上下文超過 150,000 個詞元時啟動：

```json
{
  "type": "ToolsOutputTruncateManager",
  "config": {
    "max_output_length": 40000,
    "activation": {
      "tokens_exceed": 150000
    }
  }
}
```

如需更多資訊，請參閱 [ToolsOutputTruncateManager]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/create-context-management/#toolsoutputtruncatemanager)。

## 代理程式整合

上下文管理可以在代理程式註冊期間或代理程式執行期間套用至代理程式。

### 在代理程式註冊期間

若要在代理程式註冊期間將上下文管理套用至代理程式，請在註冊代理程式時包含上下文管理名稱：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "customer-service-agent",
  "type": "conversational",
  "llm": {
    "model_id": "your-llm-model-id"
  },
  "context_management_name": "customer-service-context"
}
```
{% include copy-curl.html %}

### 在代理程式執行期間

若要在代理程式執行期間將上下文管理套用至代理程式，請在執行請求中指定上下文管理名稱。如果您在執行請求中指定的上下文管理名稱與代理程式註冊期間設定的名稱不同，執行請求會覆寫已註冊的設定：

```json
POST /_plugins/_ml/agents/agent-id/_execute
{
  "parameters": {
    "question": "How can I help you today?"
  },
  "context_management_name": "customer-service-context"
}
```
{% include copy-curl.html %}

## 使用案例範例

下列範例示範如何使用上下文管理。

### 長篇對話

若要支援長篇對話，請設定上下文管理以維持最近的對話流程，同時防止上下文溢出：

- 使用 `SlidingWindowManager` 保留最近的 N 則訊息。
- 掛鉤至 `pre_llm` 以在呼叫 LLM 之前進行最佳化。

### 大量使用工具的代理程式

為使用大量工具的代理程式設定上下文管理：

- 使用 `ToolsOutputTruncateManager` 限制工具輸出大小。
- 套用 `SlidingWindowManager` 處理工具互動歷史。
- 掛鉤至 `post_tool` 以在工具執行後進行清理。

### 大量使用工具並搭配摘要的代理程式

為具有大量工具互動的代理程式設定上下文管理：

- 使用 `ToolsOutputTruncateManager` 限制工具輸出大小。
- 套用 `SlidingWindowManager` 處理工具互動歷史。
- 使用 `SummarizationManager` 摘要較早的工具互動。
- 掛鉤至 `pre_llm` 以在呼叫 LLM 之前進行最佳化。

## 入門

若要在您的代理程式中實作上下文管理：

1. **[建立上下文管理]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/create-context-management/)**，包含適當的管理器與掛鉤。
2. **[註冊代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/)**，指定上下文管理或在執行時指定。
3. **[執行代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/)**，並觀察上下文最佳化的實際運作。
4. **[監控與調整]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/update-context-management/)** 上下文管理組態，依據效能進行調整。

從保守的設定開始，逐步調整門檻、管理器組合與啟動規則，為您的特定工作負載與效能需求找出最佳組態。
{: .tip}

## 後續步驟

- 探索[上下文管理組態]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/create-context-management/)選項。
- 檢閱完整的[上下文管理 API 參考]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/)。
- 了解[代理程式整合]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/)與上下文管理的搭配使用。