---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "新增代理記憶"
parent: Agentic memory APIs
grand_parent: ML Commons APIs
nav_order: 45
---

# 新增代理記憶（agentic memory）API
**3.3 版推出**
{: .label .label-purple }


使用此 API 將代理記憶新增至[記憶容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container)。您可以指定不同的[酬載類型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#payload-types)，並控制 OpenSearch 處理記憶時所使用的[推論模式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#inference-mode)。

建立代理記憶後，請將其 `memory_id` 提供給其他 API。

## 端點

```json
POST /_plugins/_ml/memory_containers/{memory_container_id}/memories
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `memory_container_id` | 字串 | 必要 | 要新增記憶的記憶容器 ID。 |

## 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`messages` | 陣列 | 視情況而定 | 用於 `conversational` 酬載的訊息清單。每則訊息都必須包含 `content` 欄位，其值指定為物件陣列。每個物件都必須包含 `type`（例如 `text`）及對應的內容。當 `infer` 設為 `true` 時，每則訊息可包含 `role`（通常是 `user` 或 `assistant`）。當 `payload_type` 為 `conversational` 時為必要。
`structured_data` | 物件 | 視情況而定 | 資料記憶的結構化資料內容。當 `payload_type` 為 `data` 時為必要。
`structured_data_blob` | 物件 | 選用 | 與記憶一併儲存但不會編製索引的結構化資料，因此無法搜尋。
`binary_data` | 字串 | 選用 | 二進位酬載的資料內容，以 Base64 字串編碼。
`payload_type` | 字串 | 選用 | 酬載的類型。有效值為 `conversational` 或 `data`。預設為 `conversational`。請參閱[酬載類型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#payload-types)。
`namespace` | 物件 | 選用 | 用於組織記憶的[命名空間]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#namespaces)脈絡（例如 `user_id`、`session_id` 或 `agent_id`）。若未在 `namespace` 欄位中指定 `session_id`、`payload_type` 為 `conversational`、記憶容器具有 `llm_id`，且 `disable_session` 為 `false`（預設值），則會建立具有新工作階段 ID 的新工作階段。LLM 會根據訊息產生工作階段摘要。
`metadata` | 物件 | 選用 | 記憶的其他中繼資料（例如 `status`、`branch` 或自訂欄位）。
`tags` | 物件 | 選用 | 用於分類及組織記憶的標籤。
`message_id` | 整數 | 選用 | 訊息在對話中的序號。代理程式會使用此欄位排序對話訊息。
`checkpoint_id` | 字串 | 選用 | 要與記憶一併儲存的檢查點識別碼。
`parameters` | 物件 | 選用 | 僅針對此請求覆寫記憶容器 [`parameters`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/#the-parameters-object) 的參數。
`infer` | 布林值 | 選用 | 是否使用大型語言模型（LLM）從訊息中擷取關鍵資訊。預設為 `false`。當 `true` 時，LLM 會從原始文字擷取關鍵資訊並儲存為記憶。需要記憶容器具有 `llm_id`。請參閱[推論模式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#inference-mode)。

此 API 會建立 `working` 記憶，這些記憶無法固定，因此請求會拒絕 `pinned` 欄位。若要將對話排除在保留原則之外，請在新增記憶後固定其工作階段。如需詳細資訊，請參閱[固定記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory-retention/#pinning-memories)。
{: .note}

## 範例請求：對話酬載

```json
POST /_plugins/_ml/memory_containers/SdjmmpgBOh0h20Y9kWuN/memories
{
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "text": "I'm Bob, I really like swimming.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Cool, nice. Hope you enjoy your life.",
          "type": "text"
        }
      ]
    }
  ],
  "namespace": {
    "user_id": "bob"
  },
  "metadata": {
    "status": "checkpoint",
    "branch": {
      "branch_name": "high",
      "root_event_id": "228nadfs879mtgk"
    }
  },
  "tags": {
    "topic": "personal info"
  },
  "infer": true,
  "payload_type": "conversational"
}
```
{% include copy-curl.html %}

## 回應範例：對話式酬載

```json
{
  "session_id": "XSEuiJkBeh2gPPwzjYVh",
  "working_memory_id": "XyEuiJkBeh2gPPwzjYWM"
}
```

## 範例請求：資料酬載

若要在工作記憶中儲存代理程式狀態，請傳送下列請求：

```json
POST /_plugins/_ml/memory_containers/SdjmmpgBOh0h20Y9kWuN/memories
{
  "structured_data": {
    "time_range": {
      "start": "2025-09-11",
      "end": "2025-09-15"
    }
  },
  "namespace": {
    "agent_id": "testAgent1"
  },
  "metadata": {
    "status": "checkpoint",
    "anyobject": "abc"
  },
  "tags": {
    "topic": "agent_state"
  },
  "infer": false,
  "payload_type": "data"
}
```
{% include copy-curl.html %}

## 範例回應：資料酬載

```json
{
  "working_memory_id": "Z8xeTpkBvwXRq366l0iA"
}
```

## 範例請求：儲存工具呼叫資料

若要在工作記憶中儲存代理程式追蹤資料，請傳送下列請求：

```json
POST /_plugins/_ml/memory_containers/SdjmmpgBOh0h20Y9kWuN/memories
{
  "structured_data": {
    "tool_invocations": [
      {
        "tool_name": "ListIndexTool",
        "tool_input": {
          "filter": "*,-.plugins*"
        },
        "tool_output": "green  open security-auditlog-2025.09.17..."
      }
    ]
  },
  "namespace": {
    "user_id": "bob",
    "agent_id": "testAgent1",
    "session_id": "123"
  },
  "metadata": {
    "status": "checkpoint",
    "branch": {
      "branch_name": "high",
      "root_event_id": "228nadfs879mtgk"
    },
    "anyobject": "abc"
  },
  "tags": {
    "topic": "personal info",
    "parent_memory_id": "o4-WWJkBFT7urc7Ed9hM",
    "data_type": "trace"
  },
  "infer": false,
  "payload_type": "data"
}
```
{% include copy-curl.html %}

## 範例回應：追蹤資料

```json
{
  "session_id": "123",
  "working_memory_id": "Z8xeTpkBvwXRq366l0iA"
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位           | 資料類型 | 說明                                                                                       |
| :-------------- | :-------- | :------------------------------------------------------------------------------------------------ |
| `session_id`    | 字串    | 與記憶相關聯的工作階段 ID。在建立工作階段時，或當 `namespace` 包含 `session_id` 時傳回。 |
| `working_memory_id` | 字串 | 所建立之工作記憶項目的唯一識別碼。 |
