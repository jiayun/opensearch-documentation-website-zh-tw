---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "更新記憶容器"
parent: Agentic memory APIs
grand_parent: ML Commons APIs
nav_order: 15
---

# 更新記憶容器 API
**於 3.3 版推出**
{: .label .label-purple }

使用此 API 更新現有記憶容器的屬性，例如名稱、描述、組態及存取權限。

## 端點

```json
PUT /_plugins/_ml/memory_containers/{memory_container_id}
```

## 路徑參數

| 參數 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `memory_container_id` | 字串 | 必要 | 要更新的記憶容器 ID。 |

## 請求欄位

| 欄位 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `name` | 字串 | 選用 | 記憶容器更新後的名稱。 |
| `description` | 字串 | 選用 | 記憶容器更新後的描述。 |
| `configuration` | 物件 | 選用 | 包含策略與嵌入設定的組態物件。請參閱[組態物件](#the-configuration-object)。 |

### 組態物件

`configuration` 物件支援下列欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `llm_id` | 字串 | 選用 | 用於擷取事實的大型語言模型 (LLM) ID。 |
| `strategies` | 陣列 | 選用 | 用於記憶處理的策略物件陣列。 |
| `embedding_model_id` | 字串 | 選用 | 嵌入模型 ID。僅在沒有長期記憶索引時才能更新。 |
| `embedding_model_type` | 字串 | 選用 | 嵌入模型類型。僅在沒有長期記憶索引時才能更新。 |
| `embedding_dimension` | 整數 | 選用 | 嵌入維度。僅在沒有長期記憶索引時才能更新。 |

## 更新行為

請注意下列更新行為。

### 策略更新

- 若要更新特定策略，請指定策略 `id`。
- 若要建立新策略，請指定不含 `id` 的策略。

### 後端角色更新

- 新增 `backend_roles` 中的角色，會授予具備這些角色的新使用者讀取或寫入存取權。
- 新的 `backend_roles` 欄位會覆寫現有欄位，因此若您想保留原始角色，請一併包含這些角色。

### 命名空間更新

- `strategies` 物件中的 `namespace` 欄位會以覆寫方式更新。若您想保留原始命名空間，請一併包含該命名空間。

### 嵌入模型限制

- `embedding_model_id`、`embedding_model_type` 及 `embedding_dimension` 欄位僅在此記憶容器尚未建立長期記憶索引時才能更新。一旦建立了具有指定 `index_prefix` 的長期記憶索引，就無法更新這些嵌入欄位。

## 範例請求

```json
PUT /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU
{
  "name": "opensearch-agents-memory",
  "description": "Updated memory container for OpenSearch agents",
  "backend_roles": ["admin", "ml_user"],
  "configuration": {
    "strategies": [
      {
        "id": "existing_strategy_id",
        "type": "summarization",
        "namespace": "updated_namespace"
      },
      {
        "type": "keyword_extraction"
      }
    ],
    "embedding_model_id": "new_embedding_model",
    "embedding_model_type": "dense",
    "embedding_dimension": 768
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "result": "updated",
  "_id": "HudqiJkB1SltqOcZusVU",
  "_version": 2,
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  }
}
```

## 回應欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `result` | 字串 | 更新作業的結果。 |
| `_id` | 字串 | 更新後記憶容器的 ID。 |
| `_version` | 整數 | 更新後記憶容器的版本號碼。 |
| `_shards` | 物件 | 作業所涉及分片的相關資訊。 |
