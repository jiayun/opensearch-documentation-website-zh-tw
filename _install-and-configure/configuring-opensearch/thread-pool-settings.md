---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行緒集區設定"
parent: Configuring OpenSearch
nav_order: 110
---

# 執行緒集區設定

OpenSearch 使用多個執行緒集區來管理記憶體耗用量，並有效率地處理不同類型的操作。您可以設定執行緒集區，根據叢集的工作負載模式來最佳化效能。

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 節點處理器設定

OpenSearch 會自動偵測可用的處理器數量，並據此設定執行緒集區。您可以覆寫此偵測結果：

- `node.processors`（靜態，整數）：明確設定 OpenSearch 在計算執行緒集區大小時應使用的處理器數量。當您在同一部主機上執行多個 OpenSearch 執行個體，或自動偵測的處理器數量不正確時，此設定很有用。設定後，執行緒集區大小會根據此值計算，而非偵測到的處理器數量。預設為自動偵測到的處理器數量。

## 執行緒集區類型

OpenSearch 支援下列執行緒集區類型。每種類型支援不同的參數。

### 固定執行緒集區

固定執行緒集區會維持固定數量的執行緒，並使用佇列存放待處理的請求。 

OpenSearch 支援下列固定執行緒集區：

- `get`：用於文件擷取操作（固定類型）
- `analyze`：用於 Analyze API 請求（固定類型）
- `write`：用於編製索引、刪除、更新及大量操作（固定類型）
- `force_merge`：用於強制合併操作（固定類型）
- `search`：用於搜尋操作（固定類型）
- `search_throttled`：用於受節流的搜尋操作（固定類型）

固定執行緒集區支援下列設定：

- `thread_pool.<pool_name>.size`（靜態，整數）：設定執行緒集區中的執行緒數量。無論工作負載為何，執行緒數量都保持不變。

- `thread_pool.<pool_name>.queue_size`（靜態，整數）：控制所有執行緒都忙碌時，用於存放待處理請求的佇列大小。設為 `-1` 表示佇列無上限。佇列已滿時，新的請求會遭到拒絕。預設值依執行緒集區類型而異。

### 可調整規模的執行緒集區

可調整規模的執行緒集區會根據工作負載動態調整執行緒數量。

OpenSearch 支援下列可調整規模的執行緒集區：

- `generic`：用於一般背景操作，例如節點探索（可調整規模類型）
- `snapshot`：用於快照與還原操作（可調整規模類型）
- `warmer`：用於索引預熱操作（可調整規模類型）  
- `refresh`：用於索引重新整理操作（可調整規模類型）
- `flush`：用於 `flush` 與 `fsync` 操作（可調整規模類型）
- `management`：用於叢集管理操作（可調整規模類型）
- `fetch_shard_started`：用於分片狀態操作（可調整規模類型）
- `fetch_shard_store`：用於分片存放區操作（可調整規模類型）

可調整規模的執行緒集區支援下列設定：

- `thread_pool.<pool_name>.core`（靜態，整數）：設定集區中即使閒置也要保留的最少執行緒數量。

- `thread_pool.<pool_name>.max`（靜態，整數）：設定集區中可建立的最多執行緒數量。

- `thread_pool.<pool_name>.keep_alive`（靜態，時間單位）：決定閒置執行緒在終止前保留於集區中的時間長度。超過核心大小的執行緒在閒置達此時間後會被終止。

### Fork-join 執行緒集區
**3.2 版推出**
{: .label .label-purple }

Fork-join 執行緒集區使用 Java `ForkJoinPool`，為受益於工作竊取 (work stealing) 與任務分割的工作負載提供有效率的平行處理。這對運算密集的操作很有用。在 OpenSearch 中，fork-join 執行緒集區支援仰賴平行運算的功能，例如可加速索引建置的 [`opensearch-jvector` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/)。

Fork-join 執行緒集區支援下列設定：

- `thread_pool.<pool_name>.parallelism`（靜態，整數）：設定集區的目標平行處理程度（工作執行緒數量）。此值通常與可用處理器數量相同，但可針對特定工作負載進行調整。
- `thread_pool.<pool_name>.async_mode`（靜態，布林值）：若設為 `true`，則 fork-join 集區排程會使用非同步模式。
- `thread_pool.<pool_name>.queue_size`（靜態，整數）：設定任務提交佇列的大小。將此值設為 `-1` 表示佇列大小無上限。


## 組態範例

若要設定固定執行緒集區，請依下列方式更新組態檔案：

```yaml
thread_pool:
  write:
    size: 30
    queue_size: 1000
```
{% include copy.html %}

若要設定可調整規模的執行緒集區，請依下列方式更新組態檔案：

```yaml
thread_pool:
  warmer:
    core: 1
    max: 8
    keep_alive: 2m
```
{% include copy.html %}

若要設定 fork-join 執行緒集區，請依下列方式更新組態檔案：

```yaml
thread_pool:
  fork_join:
    parallelism: 8
```
{% include copy.html %}

若要設定自訂的處理器數量，請依下列方式更新組態檔案：

```yaml
node.processors: 8
```
{% include copy.html %}

## 執行緒集區計時設定

OpenSearch 支援下列執行緒集區計時設定：

- `thread_pool.estimated_time_interval`（靜態，時間單位）：設定更新快取時間值的時間間隔，這些值供執行緒集區及其他對時間敏感的操作使用。此設定控制 OpenSearch 更新內部時間快取的頻率，以減少頻繁呼叫系統時間所產生的額外負荷。較小的間隔可提供更精確的時間測量，但較頻繁的時間更新會增加 CPU 額外負荷。將此值設為 `0` 會停用快取，並在每個請求時直接呼叫系統時間（通常用於測試）。預設為 `200ms`。最小值為 `0ms`。

## 叢集層級執行緒集區設定

OpenSearch 支援叢集層級的動態設定，讓您能覆寫叢集中所有節點的執行緒集區組態：

- `cluster.thread_pool.generic.max`（動態，整數）：設定叢集中所有節點的一般執行緒集區最大大小。這會覆寫 `opensearch.yml` 中指定的預設執行緒集區組態。一般執行緒集區負責處理輕量操作與背景任務。使用此設定可在不重新啟動節點的情況下動態調整執行緒集區大小。

- `cluster.thread_pool.snapshot.max`（動態，整數）：設定叢集中所有節點的快照執行緒集區最大大小。這會覆寫快照操作的預設執行緒集區組態。快照執行緒集區負責處理快照建立與還原操作。使用此設定可在高負載期間調整快照並行數。

- `cluster.thread_pool.<fixed-threadpool>.size`（動態，整數）：控制固定與可調整大小佇列執行緒集區的大小。覆寫 `opensearch.yml` 中提供的預設值。

- `cluster.thread_pool.<scaling-threadpool>.max`（動態，整數）：設定可調整規模執行緒集區的最大大小。覆寫 `opensearch.yml` 中提供的預設值。

- `cluster.thread_pool.<scaling-threadpool>.core`（動態，整數）：指定可調整規模執行緒集區的核心大小。覆寫 `opensearch.yml` 中提供的預設值。

在動態調整執行緒集區設定之前，請注意這些是專家層級的設定，可能會使您的叢集不穩定。修改執行緒集區設定會將相同的執行緒集區大小套用至所有節點，因此不建議用於相同角色卻使用不同硬體的叢集。同樣地，請避免調整由資料節點與叢集管理員節點共用的執行緒集區。進行這些變更後，建議您監控叢集，確保其維持穩定並如預期運作。
{: .warning}

## 最佳做法

更新執行緒集區設定時，請遵循下列最佳做法：

- 監控執行緒集區使用情況：使用 [Nodes Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/) 監控執行緒集區指標。
- 避免過度配置：執行緒集區大小設得過高，可能導致記憶體壓力與內容切換的額外負荷。
- 考量工作負載模式：根據叢集特定的讀取／寫入模式調整執行緒集區大小。
- 測試組態變更：請務必先在非正式環境中測試執行緒集區的修改。