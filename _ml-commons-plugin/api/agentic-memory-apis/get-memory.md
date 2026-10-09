---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得代理程式記憶"
parent: Agentic memory APIs
grand_parent: ML Commons APIs
nav_order: 51
---

# Get Agentic Memory API
**3.3 版新增**
{: .label .label-purple }

使用此 API 可依記憶的類型與 ID 擷取特定記憶。此統一 API 支援四種[記憶類型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#memory-types)：`sessions`、`working`、`long-term` 與 `history`。

## 端點

```json
GET /_plugins/_ml/memory_containers/{memory_container_id}/memories/{type}/{id}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `memory_container_id` | 字串 | 必要 | 要從中擷取記憶的記憶容器 ID。 |
| `type` | 字串 | 必要 | 記憶類型。有效值為 `sessions`、`working`、`long-term` 與 `history`。 |
| `id` | 字串 | 必要 | 要擷取的記憶 ID。 |

## 範例請求：取得工作記憶

```json
GET /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/working/XyEuiJkBeh2gPPwzjYWM
```
{% include copy-curl.html %}

## 範例回應：工作記憶

```json
{
  "memory_container_id": "HudqiJkB1SltqOcZusVU",
  "memory_type": "conversation",
  "messages": [
    {
      "role": "user",
      "content_text": "I'm Bob, I really like swimming."
    },
    {
      "role": "assistant",
      "content_text": "Cool, nice. Hope you enjoy your life."
    }
  ],
  "namespace": {
    "user_id": "bob",
    "session_id": "S-dqiJkB1SltqOcZ1cYO"
  },
  "metadata": {
    "status": "checkpoint",
    "branch": "{\"root_event_id\":\"228nadfs879mtgk\",\"branch_name\":\"high\"}"
  },
  "infer": true,
  "tags": {
    "topic": "personal info"
  },
  "created_time": 1758930326804,
  "last_updated_time": 1758930326804
}
```

## 範例請求：取得長期記憶

```json
GET /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/long-term/DcxjTpkBvwXRq366C1Zz
```
{% include copy-curl.html %}

## 範例回應：長期記憶 

```json
{
  "memory": "Kubernetes RBAC permission issues detected with CloudWatch agents experiencing persistent permission denials",
  "strategy_type": "SUMMARY",
  "tags": {
    "agent_type": "chat_agent",
    "conversation": "true"
  },
  "namespace": {
    "agent_id": "chat-agent"
  },
  "namespace_size": 1,
  "created_time": 1760052801773,
  "last_updated_time": 1760052801773,
  "memory_embedding": [0.018510794, 0.056366503, "..."],
  "owner_id": "admin",
  "strategy_id": "summary_96f04d97"
}
```

## 範例請求：取得工作階段

```json
GET /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/sessions/CcxjTpkBvwXRq366A1aE
```
{% include copy-curl.html %}

## 範例回應：工作階段

```json
{
  "memory_container_id": "HudqiJkB1SltqOcZusVU",
  "namespace": {
    "user_id": "bob"
  },
  "created_time": "2025-09-15T17:18:55.881276939Z",
  "last_updated_time": "2025-09-15T17:18:55.881276939Z"
}
```

## 範例請求：取得歷史記憶

```json
GET /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/history/eMxnTpkBvwXRq366hmAU
```
{% include copy-curl.html %}

## 範例回應：歷史 

```json
{
  "owner_id": "admin",
  "memory_container_id": "nrJBy5kByIxXWyhQjmqv",
  "memory_id": "4bJMy5kByIxXWyhQvGr9",
  "action": "ADD",
  "after": {
    "memory": "A comprehensive security investigation was performed across multiple data sources including 55 OpenSearch indices, 50 CloudTrail events, 22 VPC Flow logs, 38 WAF events, 74 CloudWatch log groups, active CloudWatch alarms, and OpenSearch cluster security configuration."
  },
  "namespace": {
    "agent_id": "chat-agent"
  },
  "namespace_size": 1,
  "tags": {
    "agent_type": "chat_agent",
    "conversation": "true"
  },
  "created_time": 1760052428089
}
```

## 回應欄位

回應欄位會依記憶類型而有所不同。

### 工作記憶回應欄位

下表列出所有工作記憶回應本文欄位。

| 欄位                 | 資料類型 | 說明                                             |
|:----------------------| :--- |:--------------------------------------------------------|
| `memory_container_id` | 字串 | 記憶容器的 ID。                         |
| `payload_type`        | 字串 | 負載類型。有效值為 `conversation` 與 `data`。          |
| `messages`            | 陣列 | 對話訊息的陣列 (僅適用於 `conversation` 記憶類型)。 | 
| `namespace`           | 物件 | 此記憶的命名空間上下文。                  |
| `metadata`            | 物件 | 與此記憶相關聯的其他中繼資料。         |
| `tags`                | 物件 | 用於分類的相關標籤。                     |
| `infer`               | 布林值 | 此記憶是否已啟用推論。          |
| `created_time`        | Long | 記憶建立的時間戳記。                  |
| `last_updated_time`   | Long | 記憶最後更新的時間戳記。             |

### 長期記憶回應欄位

下表列出所有長期記憶回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `memory` | 字串 | 擷取出的長期記憶事實。 |
| `strategy_type` | 字串 | 所使用的記憶策略類型 (例如 `SEMANTIC`、`SUMMARY` 或 `USER_PREFERENCE`)。 |
| `namespace` | 物件 | 此記憶的命名空間上下文。 |
| `namespace_size` | 整數 | 命名空間的數量。 |
| `tags` | 物件 | 用於分類的相關標籤。 |
| `created_time` | Long | 記憶建立的時間戳記。 |
| `last_updated_time` | Long | 記憶最後更新的時間戳記。 |
| `memory_embedding` | 陣列 | 記憶內容的向量嵌入 (顯示時會截斷)。 |
| `owner_id` | 字串 | 記憶擁有者的 ID。 |
| `strategy_id` | 字串 | 策略執行個體的唯一識別碼。 |

### 工作階段回應欄位

下表列出所有工作階段回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `memory_container_id` | 字串 | 記憶容器的 ID。 |
| `namespace` | 物件 | 此工作階段的命名空間上下文。 |
| `created_time` | 字串 | 工作階段建立的時間戳記。 |
| `last_updated_time` | 字串 | 工作階段最後更新的時間戳記。 |

### 歷史回應欄位

下表列出所有歷史回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `owner_id` | 字串 | 記憶擁有者的 ID。 |
| `memory_container_id` | 字串 | 記憶容器的 ID。 |
| `memory_id` | 字串 | 受影響記憶的 ID。 |
| `action` | 字串 | 操作類型：`ADD`、`UPDATE` 或 `DELETE`。 |
| `after` | 物件 | 操作後的記憶內容。 |
| `before` | 物件 | 操作前的記憶內容 (適用於 `UPDATE` 操作)。 |
| `namespace` | 物件 | 此記憶的命名空間上下文。 |
| `namespace_size` | 整數 | 命名空間的數量。 |
| `tags` | 物件 | 用於分類的相關標籤。 |
| `created_time` | Long | 操作發生的時間戳記。 |
