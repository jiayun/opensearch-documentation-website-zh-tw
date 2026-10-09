---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理程式記憶"
parent: Memory and context
has_children: true
has_toc: false
nav_order: 10
---

# 代理程式記憶
**3.3 版新增**
{: .label .label-purple }

代理程式記憶 (agentic memory) 讓 AI 代理程式能夠跨對話學習、記住並推論結構化資訊。與僅儲存訊息歷程的簡單對話記憶不同，代理程式記憶提供持續性、智慧型的儲存，協助代理程式維持上下文、學習使用者偏好，並隨時間改善其回應。

使用代理程式記憶，您可以建立能執行下列工作的 AI 代理程式：

- 跨多個對話工作階段記住使用者偏好
- 從過往互動中學習，以提供更個人化的回應
- 維持超越簡單訊息歷程的對話上下文
- 儲存並檢索從對話中擷取的事實性知識
- 追蹤代理程式執行軌跡，以便除錯與分析
- 依不同使用者、工作階段或代理程式執行個體組織資訊

代理程式記憶設計為可與 OpenSearch 內部的 [代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/) 以及 LangChain 和 LangGraph 等外部代理程式框架整合。

>   **重要**：
>   
>   OpenSearch 的代理程式記憶功能是以框架形式提供，讓您能為 AI 代理程式建立與管理記憶。身為記憶容器的管理員或擁有者，您必須負責實作本身的組態、管理與安全性。
> 您須負責下列事項：
>   - 資料存取控制：對儲存在記憶容器內的對話資料，實作並執行所有必要的資料存取控制。這包括但不限於設定適當的索引層級權限、文件層級安全性 (DLS) 或其他限制存取的機制。當 use_system_index 選項設為 false 時，此責任尤其重要，因為資料將儲存在需要明確權限管理的標準索引中。
>   - 自訂系統提示管理：若您選擇使用自訂的系統提示而非預設提示，您須負責該提示的內容、管理與行為。OpenSearch 不對使用者定義的系統提示所產生的輸出或互動負責。
>   若未妥善設定並保護您的代理程式記憶實作，可能導致未經授權的資料存取、資料外洩或非預期的代理程式行為。
{: .warning}

## 記憶容器

代理程式記憶以_記憶容器_ (memory container) 組織，每個容器保存特定使用案例的所有記憶類型，例如聊天機器人、研究助理或客服代理程式。

每個容器可設定下列元件：

- 文字嵌入模型：用於語意搜尋功能。
- 大型語言模型 (LLM)：用於推論與知識擷取。
- [記憶處理策略](#memory-processing-strategies)：用於定義記憶的處理或擷取方式。
- [命名空間](#namespaces)：用於依上下文、使用者、代理程式或工作階段分割與隔離記憶。

例如，若要建立包含兩個策略的記憶容器，請傳送下列請求：

```json
POST /_plugins/_ml/memory_containers/_create
{
  "name": "customer-service-agent",
  "description": "Memory container for customer service agent",
  "configuration": {
    "embedding_model_type": "TEXT_EMBEDDING",
    "embedding_model_id": "your-embedding-model-id",
    "llm_id": "your-llm-model-id",
    "strategies": [
      {
        "type": "USER_PREFERENCE",
        "namespace": ["user_id"]
      },
      {
        "type": "SUMMARY",
        "namespace": ["user_id", "session_id"]
      }
    ]
  }
}
```
{% include copy-curl.html %}

## 記憶類型

每個記憶容器可儲存四種不同的記憶類型：

- `sessions` -- 管理對話工作階段及其中繼資料。每個工作階段代表使用者與代理程式之間一個獨立的互動上下文，包含工作階段專屬資訊，例如開始時間、參與者與工作階段狀態。

- `working` -- 儲存作用中的對話資料，以及代理程式在進行中互動所使用的結構化資訊。這包括最近的訊息、目前上下文、代理程式狀態、執行軌跡，以及立即處理所需的暫時性資料。

- `long-term` -- 包含從對話中隨時間擷取並處理過的知識與事實。當啟用推論時，LLM 會從工作記憶中擷取關鍵洞察、使用者偏好與重要資訊，並將其儲存為持續性知識。

- `history` -- 維護記憶容器內所有記憶操作 (新增、更新、刪除) 的稽核軌跡。這提供記憶隨時間演變與變更的完整記錄。

## 承載類型

新增記憶時，您可以指定不同的承載 (payload) 類型：

- `conversational` -- 儲存使用者與助理之間的對話訊息。
- `data` -- 儲存結構化的非對話資料，例如代理程式狀態、檢查點或參考資訊。

若要新增啟用推論的對話記憶，請傳送下列請求：

```json
POST /_plugins/_ml/memory_containers/{container_id}/memories
{
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "text": "I prefer email notifications over SMS",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "I've noted your preference for email notifications",
          "type": "text"
        }
      ]
    }
  ],
  "namespace": {
    "user_id": "user123",
    "session_id": "session456"
  },
  "payload_type": "conversational",
  "infer": true
}
```
{% include copy-curl.html %}

若要新增代理程式狀態資料，請傳送下列請求：

```json
POST /_plugins/_ml/memory_containers/{container_id}/memories
{
  "structured_data": {
    "agent_state": "researching",
    "current_task": "analyze customer feedback",
    "progress": 0.75
  },
  "namespace": {
    "agent_id": "research-agent-1",
    "session_id": "session456"
  },
  "payload_type": "data",
  "infer": false
}
```
{% include copy-curl.html %}

## 推論模式

您可以使用 `infer` 參數控制 OpenSearch 處理記憶的方式：

- `false` (預設) -- 將原始訊息與資料儲存在 `working` 記憶中，不經 LLM 處理。
- `true` -- 使用已設定的 LLM 從內容中擷取關鍵資訊與知識。

## 記憶處理策略

記憶容器可使用下列_策略_ (strategy) 自動處理與組織記憶：

- `SEMANTIC` -- 依意義與內容相似度將相關記憶分組。
- `USER_PREFERENCE` -- 從對話中擷取並儲存使用者偏好。
- `SUMMARY` -- 建立對話內容的精簡摘要。

策略為選用；若只需簡單的儲存需求，您可以建立不含策略的容器。

## 命名空間

_命名空間_ (namespace) 透過 `user_id`、`session_id` 或 `agent_id` 等識別碼將記憶分組，以在容器內組織記憶。這可讓您區分不同使用者或對話工作階段的記憶。

若要依命名空間搜尋記憶，請傳送下列請求：

```json
GET /_plugins/_ml/memory_containers/{container_id}/memories/long-term/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "namespace.user_id": "user123"
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

## 範例使用案例

下列範例示範如何使用代理程式記憶。

### 個人化聊天機器人

建立一個會隨時間學習使用者偏好的記憶容器：

- 在啟用推論的情況下，將對話儲存在 `working` 記憶中。
- 使用 `USER_PREFERENCE` 策略將使用者偏好擷取到 `long-term` 記憶中。
- 使用命名空間區分不同使用者的記憶。

### 研究助理代理程式

建立一個從研究工作階段累積知識的代理程式：

- 將研究查詢與結果儲存在 `working` 記憶中。
- 使用 `SEMANTIC` 策略將相關研究主題分組。
- 維護 `history` 以追蹤知識隨時間的演變。

### 客服代理程式

開發一個記得住客戶互動的代理程式：

- 儲存客戶對話並啟用推論，以擷取關鍵問題。
- 使用 `SUMMARY` 策略建立簡明的互動摘要。
- 使用命名空間依客戶 ID 組織。

## 入門

若要在您的代理程式中實作代理程式記憶：

1. 使用適當的模型與策略**[建立記憶容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/)**。
2. 在代理程式互動期間**[新增記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/add-memory/)**。
3. **[搜尋並擷取]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/search-memory/)**相關記憶，以提供代理程式回應所需的資訊。
4. 隨對話演變**[更新記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/update-memory/)**。

如需詳細的 API 文件，請參閱 [Agentic Memory APIs]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/)。

## 檢視記憶資料 (OpenSearch 代理程式)

執行已設定代理程式記憶的 OpenSearch 代理程式之後，您可以使用 [Get Memory API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/get-memory/) 或 [Search Memory API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/search-memory/) 檢視工作階段與軌跡資料：

1. 依 `memory_id` 擷取工作階段：

```json
GET /_plugins/_ml/memory_containers/{memory_container_id}/memories/sessions/{memory_id}
```
{% include copy-curl.html %}

2. 依互動 ID (代理程式執行輸出中的 `parent_interaction_id`) 擷取訊息：

```json
GET /_plugins/_ml/memory_containers/{memory_container_id}/memories/working/{interaction_id}
```
{% include copy-curl.html %}

3. 使用 `namespace.session_id = <memory_id>` 取得某個工作階段的完整工作記憶軌跡資料：

```json
GET /_plugins/_ml/memory_containers/{memory_container_id}/memories/working/_search
{
  "query": {
    "match": {
      "namespace.session_id": "<memory_id>"
    }
  },
  "sort": [
    {
      "created_time": {
        "order": "asc"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 後續步驟

- 了解 [代理程式記憶保留]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory-retention/)。
- 探索[記憶容器組態]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/)選項。
- 檢閱完整的 [Agentic Memory API 參考資料]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/)。