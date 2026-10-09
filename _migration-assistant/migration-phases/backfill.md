---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "回填"
nav_order: 60
parent: Migration workflows
has_children: true
permalink: /migration-assistant/migration-phases/backfill/
redirect_from:
  - /migration-phases/backfill/
  - /migration-assistant/migration-phases/create-snapshot/
  - /migration-phases/create-snapshot/
---

# 回填

回填是快照工作流程中的文件遷移階段。Migration Assistant 會建立或重複使用來源快照、遷移中介資料，然後使用 Reindex-from-Snapshot (RFS) 將文件載入至目標。

RFS 會從快照讀取分片資料，而非從即時來源叢集 API 讀取，因此具有良好的擴展性，並在文件階段減輕來源叢集的負載。

## 回填程序

典型的快照遷移包含：

1. 建立快照，或參照現有的快照
2. 評估中介資料
3. 遷移中介資料
4. 使用 RFS 執行文件回填
5. 在切換或重播之前驗證目標

您可以在單一工作流程中定義這些項目，並讓平台進行協調。

## 試行遷移

在完整遷移之前，先執行小規模的試行。使用受限的快照範圍，或小型的中介資料與 RFS 允許清單，以確認：

- 快照建立正確。
- 來源 Amazon S3 存取正確。
- 對應可正確遷移。
- 目標索引容量充足。
- 在執行完整遷移之前，已解決任何文件層級的錯誤。

## 設定工作流程

請一律從版本相符的範例開始：

```bash
workflow configure sample --load
workflow configure edit
```
{% include copy.html %}

然後為您的來源、目標和快照儲存庫設定快照遷移區段。

當您開啟組態時，請設定 `documentBackfillConfig.failedDocumentStreamS3Bucket` 以啟用失敗文件串流。此串流預設為關閉，且必須在回填執行之前啟用，才能記錄哪些文件未送達目標。如需更多資訊，請參閱[追蹤與補救失敗的文件]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/tracking-failed-documents/)。
{: .tip }

## 允許清單類型

Migration Assistant 使用三個不同的允許清單，每個會在不同的階段進行評估。使用錯誤的允許清單是常見的錯誤來源，因此請仔細檢閱下列差異。

### 快照允許清單

快照建立允許清單會在建立快照時由來源叢集進行評估。它使用來源叢集原生的多重索引運算式語法，例如：

- `logs-*`
- `orders-2024-*`
- `-*-archive`

### 中介資料允許清單

中介資料允許清單會在快照存在之後進行評估。它支援確切名稱和 `regex:` 模式，例如：

- `orders`
- `regex:logs-.*`

### RFS 允許清單

RFS 允許清單同樣會在快照存在之後進行評估，並使用相同的確切名稱或 `regex:` 模式格式。

如果索引已從快照中排除，中介資料和 RFS 允許清單便無法將其還原。繼續之前，請先驗證您的快照允許清單。
{: .warning }

## 使用現有快照

如果您已在工作流程之外建立快照，請使用 `workflow configure sample --load` 確認您所安裝版本的確切結構，然後在工作流程組態中設定下列參數：

```text
snapshotConfig.snapshotNameConfig.externallyManagedSnapshotName
```

## 執行及監視工作流程

若要提交工作流程並監視進度，請執行下列命令：

```bash
workflow submit
workflow manage
```
{% include copy.html %}

下列命令提供額外的監視資訊：

```bash
workflow status
workflow log all --follow
```
{% include copy.html %}

## 核准

如果已啟用核准，工作流程會在有意義的檢查點暫停，讓您可以在繼續之前進行驗證。典型的關卡包括：

- **在 `evaluateMetadata` 之後** -- Migration Assistant 已計算出它將套用的對應、範本和設定。請檢閱評估器輸出，並在讓 `migrateMetadata` 將其寫入目標之前，判斷計劃的變更是否安全。
- **在 `migrateMetadata` 之後** -- 中介資料已寫入目標。在回填寫入文件之前，請使用下列命令檢查目標。
- **在文件回填開始之前** -- 在 RFS pod 開始編製索引之前，最後一次驗證計數、允許清單和目標容量的機會。
- **在 RFS 完成之後** -- 在解除封鎖工作流程的其餘部分（切換、重播或移除）之前，比較來源和目標文件計數，並抽查幾個查詢。

當關卡開啟時，請執行下列驗證命令：

```bash
# What did metadata migration write?
console clusters curl target /_cat/indices?v
console clusters curl target /_cat/templates?v
console clusters curl target /_cat/aliases?v
console clusters curl target /<index>/_mapping

# How is RFS progressing?
workflow status --live-status
workflow log all --follow

# Does a sample of the target look right?
console clusters curl target /<index>/_count
console clusters curl target /<index>/_search?size=5&pretty
```
{% include copy.html %}

若要以互動方式核准關卡，請使用 `workflow manage`。終端機使用者介面 (TUI) 會在其步驟輸出旁顯示待處理的關卡，並允許您就地核准。若為指令碼和 CI，請使用下列 CLI 形式：

```bash
workflow approve step <STEP_NAME>
```
{% include copy.html %}

## 效能模型

RFS 效能取決於下列因素：

- 資料總量
- 主要分片數
- 可用的 Kubernetes 資源
- 目標叢集匯入容量

由於 RFS 會從快照儲存空間讀取，因此增加 worker 數量不會對來源叢集增加讀取負載；而是會增加目標叢集的寫入壓力。

## 常見的調校與復原選項

下表說明可用於調校與復原的 RFS 設定。

| 設定 | 說明 | 預設 |
|:--------|:------------|:--------|
| `podReplicas` | 平行執行的 RFS pod 數量（每個 pod 一個分片）。 | N/A |
| `maxConnections` | 對目標的 bulk-indexer 並行處理數。 | N/A |
| `documentsPerBulkRequest` | 大量批次大小。 | N/A |
| `maxShardSizeBytes` | 支援的最大分片大小。較大的分片必須在回填之前縮減（強制合併或分割）。 | 80 GiB |
| `initialLeaseDuration` | 每個 worker 在重新取得之前持有分片租約的 ISO-8601 持續時間。 | `PT1H` |
| `allowedDocExceptionTypes` | 目標回應中例外類別名稱的清單，這些例外會計為該文件成功，而不會重試。請謹慎使用；相符的錯誤會視為該文件成功遷移。此設定與 Replayer 的 `nonRetryableDocExceptionTypes` 不同，後者會將相符的例外視為不應重試的確定性失敗。如需重播端的資訊，請參閱[重播擷取的流量]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/replay-captured-traffic/)。 | N/A |
| `allowLooseVersionMatching` | 略過嚴格的來源/目標版本相容性檢查。 | `true` |

## 回填後驗證

工作流程完成後，比較來源和目標：

```bash
console clusters cat-indices
console clusters curl target /<index>/_count
```
{% include copy.html %}

如果目標文件計數低於來源計數，表示個別文件編製索引失敗。如需更多資訊，請參閱[追蹤與補救失敗的文件]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/tracking-failed-documents/)。

若為零停機遷移，請在重播開始最終同步步驟之前完成回填驗證。

{% include migration-phase-navigation.html %}
