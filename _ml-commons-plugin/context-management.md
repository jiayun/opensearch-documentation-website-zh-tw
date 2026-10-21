---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "脈絡管理"
parent: Memory and context
nav_order: 20
---

# 脈絡管理
**於 3.5 版導入**
{: .label .label-purple }

脈絡管理讓 OpenSearch 代理程式能夠在向大型語言模型（LLM）傳送請求之前，動態最佳化其脈絡。這項彈性功能有助於防止脈絡視窗溢出、減少詞元用量，並透過智慧化管理對話歷史、工具互動及其他脈絡資訊，支援長時間執行的代理程式。

使用脈絡管理，您可以建置能夠執行下列動作的 AI 代理程式：

- 在接近詞元上限時自動截斷過長的工具輸出。
- 摘要冗長的工具互動以保留重要資訊。
- 套用滑動視窗方式以維持最近的脈絡。
- 依據特定使用案例實作自訂的脈絡最佳化策略。
- 在代理程式執行的不同階段掛鉤以轉換脈絡。

脈絡管理採用以掛鉤為基礎的系統，允許可插拔的脈絡管理器在特定執行點檢查並轉換代理程式的脈絡。您可以嘗試不同的組態與組合，為您的特定使用案例找出最佳設定。

## 設定脈絡管理

脈絡管理 (context management) 會組織多個_脈絡管理器_，在代理程式生命週期中的特定執行點協同最佳化代理程式的脈絡。此系統具有高度可組態性，讓您能依特定需求調整其行為。

每個脈絡管理可以使用下列元件進行設定：

- **名稱**：脈絡管理的唯一識別碼。
- **描述**：以人類可讀方式描述脈絡管理的用途。
- **掛鉤**：脈絡管理器運作的各種執行點。
- **脈絡管理器**：執行特定脈絡轉換的個別元件。
- **啟用規則**：決定脈絡管理器何時執行的條件。

您可以混合搭配不同的脈絡管理器、調整其參數，並實驗各種啟用門檻，以在您的使用情境中達到最佳效能。

例如，若要建立名為 `token-aware-truncation` 且包含 `ToolsOutputTruncateManager` 與 `SlidingWindowManager` 的脈絡管理，請傳送下列請求：

```json
POST /_plugins/_ml/context_management/token-aware-truncation
{
  "description": "Context management that truncates tool outputs longer than 100,000 characters and applies sliding window to keep last 6 messages when tokens exceed 200,000",
  "hooks": {
    "POST_TOOL": [
      {
        "type": "ToolsOutputTruncateManager",
        "config": {
          "max_output_length": 100000
        }
      }
    ],
    "PRE_LLM": [
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

脈絡管理採用掛鉤式架構，讓多組脈絡管理器能在代理程式執行期間的特定時點執行。支援的掛鉤如下：

- `PRE_LLM` -- 在將請求傳送給 LLM 之前執行。
- `POST_TOOL` -- 在工具執行完成後執行。

掛鉤名稱區分大小寫，且必須為大寫。Create Context Management API 接受任何掛鉤名稱，但以小寫名稱（例如 `post_tool`）設定的脈絡管理器永遠不會執行。代理程式註冊請求中的行內 `context_management` 組態會拒絕小寫掛鉤名稱。
{: .important}

為各掛鉤註冊的脈絡管理器，會依其在脈絡管理組態中定義的順序執行。

OpenSearch 的[對話式代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational/)與[規劃-執行-反思代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/plan-execute-reflect/)支援這些掛鉤。 

## 啟用規則

啟用規則決定脈絡管理器在代理程式互動期間何時執行。這些規則可協助您控制資源使用量，並只在需要時觸發脈絡最佳化，以提升效能。若未指定啟用規則，脈絡管理器會在其設定的掛鉤 (hook) 上於每次互動時執行。

脈絡管理器支援下列啟用規則，可單獨使用或合併使用。

### 訊息數量門檻

使用 `message_count_exceed` 在對話歷史超過指定的訊息數量時啟動脈絡管理器：

```json
{
  "activation": {
    "message_count_exceed": 20
  }
}
```

當對話變得冗長時，此規則適合用來套用滑動視窗或摘要等脈絡最佳化策略。

### 詞元數量門檻

使用 `tokens_exceed` 在整個脈絡視窗的估計詞元數量超過門檻時啟動脈絡管理器。脈絡視窗包含系統提示、使用者提示、聊天歷史（記憶）以及工具互動：

```json
{
  "activation": {
    "tokens_exceed": 200000
  }
}
```

此規則有助於防止脈絡視窗溢出，並在超過模型上限之前觸發最佳化策略，以管理 LLM API 成本。

### 合併多項規則

您可以使用 AND 邏輯合併多項啟用規則。脈絡管理器只有在所有指定條件都符合時才會執行：

```json
{
  "activation": {
    "message_count_exceed": 15,
    "tokens_exceed": 200000
  }
}
```

此範例只有在訊息數量超過 15 且詞元數量超過 200,000 時才啟動脈絡管理器，可對最佳化發生的時機提供精細控制。

## 脈絡管理器類型

OpenSearch 提供下列脈絡管理器類型。如需完整的組態參數詳細資訊，請參閱[脈絡管理器組態]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/create-context-management/#context-manager-configurations)。

### SlidingWindowManager

實作滑動視窗方式，僅保留最近的 N 次互動，以防止脈絡視窗溢出。此範例展示一個滑動視窗管理器，保留最近的 6 則訊息，並在對話超過 12 則訊息時啟動：

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

在接近詞元上限時摘要冗長的對話或工具互動。此範例展示一個摘要管理器，在保留最近 10 則訊息的同時摘要 30% 的對話歷史，並在脈絡超過 200,000 個詞元時啟動：

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

當工具輸出超過指定限制時，會將其截斷，以避免脈絡溢位。請為 `POST_TOOL` 掛鉤設定此管理器。它會處理每次工具呼叫的輸出，無論代理程式是否使用函式呼叫（`_llm_interface`）。如果輸出長度超過 `max_output_length` 個字元，管理器會保留前 `max_output_length` 個字元，並附加 `... [Output truncated - original length: <length> characters]`。代理程式會將截斷後的輸出傳送給 LLM，並儲存在代理程式的追蹤記錄中。此範例顯示一個截斷管理器，會將工具輸出限制為 40,000 個字元，並在脈絡超過 150,000 個詞元時啟用：

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

脈絡管理可以在代理程式註冊期間或代理程式執行期間套用至代理程式。

### 在代理程式註冊期間

若要在代理程式註冊期間將脈絡管理套用至代理程式，請在註冊代理程式時加入現有脈絡管理的名稱：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "customer-service-agent",
  "type": "conversational",
  "llm": {
    "model_id": "<llm_model_id>"
  },
  "tools": [
    {
      "type": "ListIndexTool"
    }
  ],
  "context_management_name": "token-aware-truncation"
}
```
{% include copy-curl.html %}

### 代理程式執行期間

若要在代理程式執行期間對代理程式套用脈絡管理 (context management)，請在執行請求的 `parameters` 物件中指定脈絡管理名稱。如果您在執行請求中指定的脈絡管理名稱與代理程式註冊時設定的名稱不同，執行請求將覆寫已註冊的設定：

```json
POST /_plugins/_ml/agents/{agent_id}/_execute
{
  "parameters": {
    "question": "How can I help you today?",
    "context_management_name": "token-aware-truncation"
  }
}
```
{% include copy-curl.html %}

## 使用案例範例

下列範例示範如何使用脈絡管理。

### 長對話

為了支援長對話，請設定脈絡管理，以維持近期對話流程並避免脈絡溢滿：

- 使用 `SlidingWindowManager` 保留最近 N 則訊息。
- 掛接 `PRE_LLM`，在呼叫 LLM 前進行最佳化。

### 工具密集型代理程式

為使用大量工具的代理程式設定脈絡管理：

- 使用 `ToolsOutputTruncateManager` 限制工具輸出大小。
- 對工具互動歷程套用 `SlidingWindowManager`。
- 掛接 `POST_TOOL`，以便在工具執行後進行清理。

### 大量使用工具並搭配摘要的代理程式

為大量與工具互動的代理程式設定脈絡管理：

- 使用 `ToolsOutputTruncateManager` 限制工具輸出大小。
- 對工具互動歷程套用 `SlidingWindowManager`。
- 使用 `SummarizationManager` 摘要先前的工具互動。
- 掛接至 `PRE_LLM`，以在呼叫 LLM 前進行最佳化。

## 入門

若要在您的代理程式中實作脈絡管理：

1. **[建立脈絡管理]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/create-context-management/)**，包含適當的管理器與掛鉤。
2. **[註冊代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/)** 時帶入脈絡管理，或在執行時指定。
3. **[執行代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/)**，並觀察脈絡最佳化的實際運作。
4. **[監控與調整]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/update-context-management/)** 脈絡管理組態，依據效能進行調整。

從保守的設定開始，逐步調整門檻、管理器組合與啟用規則，為您的特定工作負載與效能需求找出最佳組態。
{: .tip}

## 後續步驟

- 探索[脈絡管理組態]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/create-context-management/)選項。
- 檢閱完整的[脈絡管理 API 參考]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/)。
- 了解[代理程式整合]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/)與脈絡管理的搭配使用。