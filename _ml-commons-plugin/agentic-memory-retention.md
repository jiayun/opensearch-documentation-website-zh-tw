---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理程式記憶保留"
parent: Agentic memory
grand_parent: Memory and context
nav_order: 30
---

# 代理程式記憶保留
**於 3.8 版推出**
{: .label .label-purple }

這是實驗性功能，不建議在正式環境中使用。如需功能進展的最新消息，或想提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)的討論。
{: .warning}

根據預設，代理程式記憶會無限期累積，這會增加儲存空間用量，並可能導致代理程式擷取到過期的記憶。若要自動刪除舊的或多餘的記憶，請為[記憶容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#memory-containers)定義_保留原則_。保留原則會為每種記憶類型指定存留期限、數量上限，或同時指定兩者。背景工作會依排程強制執行該原則。它會刪除超過數量上限的 `sessions`、`long-term` 和 `history` 記憶，或刪除超過存留期限的 `sessions` 和 `long-term` 記憶。相對地，`working` 記憶不受保留原則約束，並會在其父工作階段不存在時遭到刪除。若要控制 `working` 記憶的保留時間長度，請為 `sessions` 設定保留。

您可以將 `sessions` 和 `long-term` 記憶釘選，將其排除在保留原則之外。如需詳細資訊，請參閱[釘選記憶](#pinning-memories)。

## 啟用記憶保留

保留功能預設為停用。若要在整個叢集啟用，請設定下列動態叢集設定：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.ml_commons.memory.retention_enabled": true
  }
}
```
{% include copy-curl.html %}

## 定義保留原則

`retention_policy` 物件指定於容器的 `configuration` 物件中，並將每種記憶類型對應至該類型的保留限制。請將 `{memory_type}` 取代為 `sessions`、`long-term` 或 `history`：

```json
"configuration": {
  "retention_policy": {
    "{memory_type}": {
      "retention_days": 90,
      "max_count": 5000
    }
  }
}
```

每個 `{memory_type}` 物件接受下列選用欄位。當兩個欄位都設定時，只要記憶違反任一規則就會遭到刪除。

欄位 | 資料類型 | 支援的記憶類型 | 說明
:--- | :--- | :--- | :---
`retention_days` | 整數 | `sessions`、`long-term` | 刪除早於此天數的記憶，天數從記憶的 `last_updated_time` 起算。
`max_count` | 整數 | `sessions`、`long-term`、`history` | 最多保留此數量的記憶，並優先刪除最舊的。工作階段和長期記憶依 `last_updated_time` 排序；歷程記錄依 `created_time` 排序。

保留規則只有在容器儲存該記憶類型時才會生效。若要儲存 `long-term` 和 `history` 記憶，您必須設定 `strategies`；否則，這些類型的保留規則不會有任何作用。如需詳細資訊，請參閱[建立的索引]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/#the-created-indexes)。
{: .note}

### 設定保留原則

若要在建立記憶容器時設定原則，請在建立請求中加入 `retention_policy` 欄位。下列範例會建立具有工作階段追蹤、策略和保留原則的容器，該原則會保留最多 5,000 個工作階段達 90 天，並將長期記憶限制為 2,000 筆項目：

```json
POST /_plugins/_ml/memory_containers/_create
{
  "name": "my-agent-memory",
  "configuration": {
    "embedding_model_type": "TEXT_EMBEDDING",
    "embedding_model_id": "your-embedding-model-id",
    "embedding_dimension": 1024,
    "llm_id": "your-llm-model-id",
    "strategies": [
      {
        "type": "SEMANTIC",
        "namespace": ["user_id"]
      }
    ],
    "retention_policy": {
      "sessions": {
        "retention_days": 90,
        "max_count": 5000
      },
      "long-term": {
        "max_count": 2000
      }
    }
  }
}
```
{% include copy-curl.html %}

您也可以隨時在更新請求中傳送 `retention_policy` 物件，為現有容器新增保留原則：

```json
PUT /_plugins/_ml/memory_containers/{memory_container_id}
{
  "configuration": {
    "retention_policy": {
      "sessions": {
        "retention_days": 90,
        "max_count": 5000
      },
      "long-term": {
        "max_count": 2000
      }
    }
  }
}
```
{% include copy-curl.html %}

原則會套用至容器中的所有記憶，包括在您新增原則之前建立的記憶。例如，為含有 10,000 個工作階段的容器新增 `max_count` 為 100，會刪除最近更新時間最舊的 9,900 個工作階段。若要保留特定記憶，請在新增原則之前將其[釘選](#pinning-memories)。
{: .warning}

### 檢視保留原則

若要檢視已儲存的原則，請使用 [Get Memory Container API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/get-memory-container/) 擷取容器：

```json
GET /_plugins/_ml/memory_containers/{memory_container_id}
```
{% include copy-curl.html %}

### 更新保留原則

更新 `retention_policy` 會將您的變更合併至現有原則，而不是取代它。您省略的記憶類型和欄位會保持不變。

若要移除單一欄位，請將其設為 `null`。例如，下列請求會更新[設定保留原則](#configuring-a-retention-policy)範例中的原則，從 `sessions` 移除 `retention_days`，同時保留 5,000 的 `max_count`：

```json
PUT /_plugins/_ml/memory_containers/{memory_container_id}
{
  "configuration": {
    "retention_policy": {
      "sessions": {
        "retention_days": null
      }
    }
  }
}
```
{% include copy-curl.html %}

### 停用容器的保留功能

若要停用整個容器的保留功能，請將 `retention_policy` 設為 `null`：

```json
PUT /_plugins/_ml/memory_containers/{memory_container_id}
{
  "configuration": {
    "retention_policy": null
  }
}
```
{% include copy-curl.html %}

將 `retention_policy` 設為 `null` 與省略它不同。省略原則會讓容器適用[叢集層級預設設定](#default-settings)；將其設為 `null` 則會讓容器豁免於這些預設值。即使叢集層級的保留功能已停用，您仍可傳送此請求。

## 釘選記憶

釘選記憶可使其免於依容器的[保留原則](#defining-a-retention-policy)遭到刪除。您可以釘選 `sessions` 和 `long-term` 記憶。釘選 `sessions` 會保留其所有 `working` 記憶。由於釘選的記憶永遠不會遭到刪除，因此可能會隨時間累積。若要縮小容器大小，請取消釘選不再需要保護的 `sessions`。

釘選可保護記憶免於遭到刪除，但不會變更其存留時間。記憶的存留時間從其 `last_updated_time` 起算，只有在內容變更時才會推進，例如將 `working` 記憶新增至工作階段，或更新 `long-term` 記憶時。釘選不會更新此時間戳記，因此如果您之後取消釘選該記憶，其存留時間仍會反映上次內容變更的時間，並可能立即符合刪除條件。

請使用下列請求欄位來釘選記憶。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`pinned` | 布林值 | 設為 `true` 可釘選記憶，設為 `false` 則可取消釘選。適用於 `sessions` 和 `long-term` 記憶。

下列範例會釘選記憶（將 `sessions` 或 `long-term` 指定為 `memory_type`）：

```json
PUT /_plugins/_ml/memory_containers/{memory_container_id}/memories/{memory_type}/{memory_id}
{
  "pinned": true
}
```
{% include copy-curl.html %}

## 保留作業

背景作業會依照[排程](#retention-job-schedule)執行保留原則（預設為每 24 小時一次）。由於原則是依排程執行，而非持續執行，因此超過存留時間或數量限制的記憶仍會出現在搜尋結果中，直到作業下次執行並將其刪除。

記憶會依據下列限制進行評估：

- `retention_days` 從記憶的 `last_updated_time` 起算。將 `working` 記憶新增至工作階段會更新該工作階段的時間戳記，因此進行中的對話會予以保留。釘選記憶不會更新此時間戳記。
- `max_count` 不受存留時間影響。如果容器中某種類型的未釘選記憶數量超過 `max_count`，就會刪除最舊的記憶，直到剩下 `max_count` 筆為止，即使這些記憶比 `retention_days` 更新也一樣。
- 當某種記憶類型同時設定這兩項限制時，只要記憶超過其中任一項限制，就會遭到刪除。

執行 `max_count` 時，每次執行最多會針對容器中的每種記憶類型刪除 50,000 筆記憶。較大量的待刪除記憶會在後續多次執行中逐步減少，因此遠超過其 `max_count` 的容器可能需要執行數次才能達到限制。依據 `retention_days` 進行的刪除沒有數量上限。

當作業移除 `sessions` 記憶時，會先刪除其 `working` 記憶，以免產生孤立記憶。手動刪除 `sessions` 記憶不會刪除其 `working` 記憶，因而使這些記憶成為孤立記憶。執行原則後，作業會移除自 `created_time` 起已超過 `orphan_ttl_days` 天的孤立 `working` 記憶。作業第一次檢查容器是否有孤立記憶時，會記錄基準且不刪除任何記憶，因此該容器中的孤立記憶會在記錄基準後經過 `orphan_ttl_days` 才開始刪除。

孤立記憶清理只會針對具有保留原則，且建立時將 `disable_session` 設為 `false`（預設值）的容器執行。在沒有保留原則的容器中，孤立的 `working` 記憶會無限期保留。

建立時將 `disable_session` 設為 `true` 的容器不會儲存 `sessions` 記憶，因此上述兩種機制都不適用。其 `working` 記憶只會由 `plugins.ml_commons.memory.working_memory_ttl_days` 設定刪除，而此設定預設為停用。在您將其設為正值之前，這些容器會無限期保留 `working` 記憶。如需詳細資訊，請參閱[記憶保留設定](#memory-retention-settings)。

啟用多租用戶功能時，此作業會停用。在此情況下，即使容器具有原則，也不會執行任何保留原則。

## 暫停保留

若要暫停保留作業並保留已設定的保留原則，請將 `plugins.ml_commons.memory.retention_enabled` 設為 `false`。將其設回 `true` 即可恢復執行。

## 記憶保留設定

您可以使用下列動態叢集設定自訂保留行為：

- `plugins.ml_commons.memory.retention_enabled`（布林值）：在整個叢集啟用保留功能。當此設定為 `false` 時，保留作業不會刪除任何記憶，且容器 API 會拒絕 `retention_policy`。預設值為 `false`。

- `plugins.ml_commons.memory.retention_job_throttle_seconds`（整數）：指定保留作業處理完已刪除記憶的容器後，在繼續處理下一個容器之前暫停的時間。提高此值可降低叢集負載。有效值介於 `[1, 60]` 範圍內。預設值為 `5`。

- `plugins.ml_commons.memory.working_memory_ttl_days`（整數）：在 `working` 記憶建立後經過此天數時將其刪除。僅適用於建立時將 `disable_session` 設為 `true` 的容器。由於這些容器不會儲存 `sessions` 記憶，因此此設定是刪除其 `working` 記憶的唯一機制。有效值介於 `[1, 365]` 範圍內。預設值為 `-1`（停用）。

- `plugins.ml_commons.memory.orphan_ttl_days`（整數）：刪除其父層 `sessions` 記憶已不存在的 `working` 記憶，時間從 `working` 記憶的 `created_time` 起算。如需詳細資訊，請參閱[保留作業](#retention-job)。有效值介於 `[1, 365]` 範圍內。預設值為 `7`。

### 預設設定

預設設定適用於任何尚未設定自身保留原則的容器。這些設定只有在[叢集啟用保留功能](#enabling-memory-retention)後才會生效；在此之前，設定會儲存，但不會產生作用。啟用保留功能後，下一次排程作業會將這些設定套用至沒有原則的容器，並刪除任何超過預設值的記憶，包括您設定預設值之前建立的記憶。

預設值只會套用至容器一次；之後變更這些設定，不會更新已套用預設值的容器。若要讓容器不受預設值影響，請將其 `retention_policy` 設為 `null`。若要在套用預設值後更新容器的原則，請使用 [Update Memory Container API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/update-memory-container/)。

下列每個動態設定各自提供[保留原則](#defining-a-retention-policy)中一個欄位的預設值。預設值 `-1` 表示不為該欄位套用任何預設值：

- `plugins.ml_commons.memory.default_session_retention_days`（整數）：設定 `sessions` 記憶的預設 `retention_days`。有效值介於 `[1, 3650]` 範圍內。預設值為 `-1`。

- `plugins.ml_commons.memory.default_session_max_count`（整數）：設定 `sessions` 記憶的預設 `max_count`。有效值介於 `[1, 1000000]` 範圍內。預設值為 `-1`。

- `plugins.ml_commons.memory.default_long_term_max_count`（整數）：設定 `long-term` 記憶的預設 `max_count`。有效值介於 `[1, 1000000]` 範圍內。預設值為 `-1`。

- `plugins.ml_commons.memory.default_history_max_count`（整數）：設定 `history` 記憶的預設 `max_count`。有效值介於 `[1, 10000000]` 範圍內。預設值為 `-1`。

### 保留作業排程

<!-- TODO: When this feature goes GA, revisit the retention_job_interval_hours behavior (currently static-like; dynamic interval updates are planned for a future release). -->

下列設定控制保留作業的排程。請在啟動叢集前於 `opensearch.yml` 中設定。作業只會在啟動時首次排定排程時讀取此設定一次；在執行中的叢集上透過 Cluster Settings API 更新此設定不會生效：

- `plugins.ml_commons.memory.retention_job_interval_hours`（整數）：指定保留作業的執行間隔，以小時為單位。有效值介於 `[1, 168]` 範圍內。預設值為 `24`。

## 後續步驟

- 如需記憶容器與代理式記憶的詳細資訊，請參閱[代理式記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/)。
- 如需容器建立 API 的參考資料，請參閱 [Create Memory Container API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/)。
