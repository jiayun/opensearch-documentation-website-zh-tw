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
| `name` | 字串 | 選用 | 記憶容器的更新名稱。 |
| `description` | 字串 | 選用 | 記憶容器的更新說明。 |
| `backend_roles` | 陣列 | 選用 | 用於存取控制的後端角色清單。會覆寫現有清單。 |
| `configuration` | 物件 | 選用 | 包含策略與嵌入設定的組態物件。請參閱[組態物件](#the-configuration-object)。 |

### 組態物件

`configuration` 物件支援下列欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `llm_id` | 字串 | 選用 | 用於擷取事實的大型語言模型 (LLM) ID。 |
| `max_infer_size` | 整數 | 選用 | 記憶整併期間所擷取之相似既有記憶的最大數量。最大值為 `10`。若要更新此值，請在同一請求中包含 `llm_id`。 |
| `strategies` | 陣列 | 選用 | 用於記憶處理的策略物件陣列。每個策略支援 `id`、`type`、`namespace`、`enabled` 及 `configuration` 欄位。欄位說明請參閱[策略陣列]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/#the-strategies-array)。 |
| `embedding_model_id` | 字串 | 選用 | 嵌入模型 ID。僅在不存在長期記憶索引時才能更新。 |
| `embedding_model_type` | 字串 | 選用 | 嵌入模型類型。僅在不存在長期記憶索引時才能更新。 |
| `embedding_dimension` | 整數 | 選用 | 嵌入維度。僅在不存在長期記憶索引時才能更新。 |
| `retention_policy` | 物件 | 選用 | 各記憶類型的保留限制。變更會合併至現有原則。設為 `null` 可移除該原則。如需詳細資訊，請參閱[代理記憶保留]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory-retention/)。 |

## 更新行為

請注意下列更新行為。

### 策略更新

- 如要更新特定策略，請指定策略 `id`。系統只會更新您提供的欄位。您無法變更現有策略的 `type`。
- 如要建立新策略，請指定不含 `id` 的策略。
- 如要停用策略而不移除它，請將其 `enabled` 欄位設為 `false`。

### 後端角色更新

- 新增 `backend_roles` 中的角色，會授予具備這些角色的新使用者讀取或寫入存取權。
- 新的 `backend_roles` 欄位會覆寫現有欄位，因此若您想保留原始角色，請一併包含這些角色。

### 命名空間更新

- `strategies` 物件中的 `namespace` 欄位會以覆寫方式更新。若您想保留原始命名空間，請一併包含該命名空間。

### 嵌入模型限制

- `embedding_model_id`、`embedding_model_type` 及 `embedding_dimension` 欄位僅在此記憶容器尚未建立長期記憶索引時才能更新。一旦建立了具有指定 `index_prefix` 的長期記憶索引，就無法更新這些嵌入欄位。

## 請求範例

下列請求會更新現有策略的命名空間，並新增一個 `USER_PREFERENCE` 策略。若要查找現有策略的 ID，請使用 [Get Memory Container API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/get-memory-container/)：

```json
PUT /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU
{
  "name": "opensearch-agents-memory",
  "description": "Updated memory container for OpenSearch agents",
  "backend_roles": ["admin", "ml_user"],
  "configuration": {
    "strategies": [
      {
        "id": "semantic_53d1751c",
        "namespace": ["user_id", "session_id"]
      },
      {
        "type": "USER_PREFERENCE",
        "namespace": ["user_id"]
      }
    ]
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "_index": ".plugins-ml-am-memory-container",
  "_id": "HudqiJkB1SltqOcZusVU",
  "_version": 2,
  "result": "updated",
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 5,
  "_primary_term": 1
}
```

## 回應欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `_index` | 字串 | 儲存記憶容器的索引名稱。 |
| `result` | 字串 | 更新作業的結果。 |
| `_id` | 字串 | 已更新記憶容器的 ID。 |
| `_version` | 整數 | 已更新記憶容器的版本號碼。 |
| `_shards` | 物件 | 此作業所涉及分片的相關資訊。 |
| `_seq_no` | 長整數 | 指派給更新作業的序號。 |
| `_primary_term` | 長整數 | 索引的主要分片任期。 |
