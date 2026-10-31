---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "異常偵測設定"
parent: Anomaly detection
nav_order: 70
redirect_from: 
  - /monitoring-plugins/ad/settings/
---

# 異常偵測設定

Anomaly Detection 外掛程式為標準 OpenSearch 叢集設定新增了數項設定。
這些設定是動態的，因此無需重新啟動叢集即可變更外掛程式的預設行為。若要進一步了解靜態與動態設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

您可以將設定標記為 `persistent` 或 `transient`。

例如，若要更新結果索引的保留期間：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.anomaly_detection.ad_result_history_retention_period": "5m"
  }
}
```
{% include copy-curl.html %}

OpenSearch 支援下列異常偵測設定：

- `plugins.anomaly_detection.enabled`（動態，布林值）：是否啟用 Anomaly Detection 外掛程式。若停用，所有偵測器會立即停止執行。預設為 `true`。

- `plugins.anomaly_detection.max_anomaly_detectors`（動態，整數）：叢集中的單一實體偵測器（沒有 category 欄位的偵測器）數量上限。預設為 `1000`。

- `plugins.anomaly_detection.max_multi_entity_anomaly_detectors`（動態，整數）：叢集中的高基數偵測器（有 category 欄位的偵測器）數量上限。預設為 `10`。

- `plugins.anomaly_detection.max_anomaly_features`（動態，整數）：單一偵測器的特徵數量上限。預設為 `5`。

- `plugins.anomaly_detection.ad_result_history_rollover_period`（動態，時間單位）：檢查 rollover（輪替）條件的頻率。當輪替條件符合時，Anomaly Detection 外掛程式會將結果索引輪替到新的索引。預設為 `12h`。

- `plugins.anomaly_detection.ad_result_history_max_docs_per_shard`（動態，整數）：結果索引單一分片中的文件數量上限。Anomaly Detection 外掛程式只計算主要分片中已重新整理的文件。預設為 `1350000000`。

- `plugins.anomaly_detection.max_entities_per_query`（動態，整數）：高基數偵測器在每個偵測間隔內的唯一值數量上限。預設情況下，如果 category 欄位在偵測間隔內的唯一值數目超過設定的值，Anomaly Detection 外掛程式會依類別值的自然排序排列（例如實體 `ab` 排在 `bc` 之前），然後選取前面的值。預設為 `1000000`。

- `plugins.anomaly_detection.max_entities_for_preview`（動態，整數）：高基數偵測器在預覽操作中顯示的唯一 category 欄位值數量上限。預設情況下，如果 category 欄位在偵測間隔內的唯一值數目超過設定的值，Anomaly Detection 外掛程式會依類別值的自然排序排列（例如實體 `ab` 排在 `bc` 之前），然後選取前面的值。預設為 `5`。

- `plugins.anomaly_detection.max_primary_shards`（動態，整數）：異常偵測索引可擁有的主要分片數量上限。預設為 `10`。

- `plugins.anomaly_detection.filter_by_backend_roles`（動態，布林值）：當您啟用 Security 外掛程式並將此設定設為 `true` 時，Anomaly Detection 外掛程式會根據使用者的後端角色篩選結果。預設為 `false`。

- `plugins.anomaly_detection.max_batch_task_per_node`（動態，整數）：啟動歷史分析會觸發一個批次任務。此設定是每個資料節點可執行的批次任務數量。您可以將此設定從 1 調整到 1,000。如果資料節點無法支援所有批次任務，而且您不確定資料節點是否能執行更多歷史分析，請新增更多資料節點，而不是將此設定調高。增加此值可能會為每個資料節點帶來更多負載。預設為 `10`。

- `plugins.anomaly_detection.max_old_ad_task_docs_per_detector`（動態，整數）：您可以對同一個偵測器多次執行歷史分析。每次執行時，Anomaly Detection 外掛程式都會建立一個新任務。此設定是外掛程式保留的先前任務數量。請將此值至少設為 1，以追蹤其最近一次執行。最多可保留 1,000 個舊任務，以避免使叢集不堪負荷。預設為 `1`。

- `plugins.anomaly_detection.batch_task_piece_size`（動態，整數）：歷史任務的日期範圍會被拆分為較小的片段，Anomaly Detection 外掛程式會逐片段執行任務。每個片段預設包含 1,000 個偵測間隔。例如，如果偵測間隔為 1 分鐘，而一個片段為 1,000 分鐘，則每 1,000 分鐘查詢一次特徵資料。您可以將此設定從 1 變更為 10,000。預設為 `1000`。

- `plugins.anomaly_detection.batch_task_piece_interval_seconds`（動態，整數）：同一個歷史分析任務的兩個片段之間的時間間隔，以秒為單位。此間隔可防止任務消耗過多可用資源，而使搜尋與大量索引等其他操作缺乏資源。您可以將此設定從 1 變更為 600 秒。預設為 `5`。

- `plugins.anomaly_detection.max_top_entities_for_historical_analysis`（動態，整數）：高基數偵測器歷史分析可執行的頂端實體數量上限。範圍為 1 到 10,000。預設為 `1000`。

- `plugins.anomaly_detection.max_running_entities_per_detector_for_historical_analysis`（動態，整數）：高基數偵測器分析可平行執行的實體任務數量。叢集上可用的任務插槽數量也會影響可平行執行的實體數量。如果叢集有 3 個資料節點，每個資料節點預設有 10 個任務插槽。假設您已有兩個高基數偵測器，且各自執行 10 個實體。如果您再啟動一個需要 1 個任務插槽的單一實體偵測器，可用的任務插槽數量為 `10 * 3 - 10 * 2 - 1 = 9`。此時如果您啟動新的高基數偵測器，該偵測器只能平行執行 9 個實體，而不是 10 個。您可以根據叢集的能力將此值從 1 調整到 1,000。若設為較高的值，Anomaly Detection 外掛程式會更快執行歷史分析，但也會消耗更多資源。預設為 `10`。

- `plugins.anomaly_detection.max_cached_deleted_tasks`（動態，整數）：您可以對單一偵測器任意多次重新執行歷史分析。Anomaly Detection 外掛程式只會保留有限數量的舊任務，預設為 1 個舊任務。如果您對某個偵測器執行歷史分析三次，最舊的任務就會被刪除。由於歷史分析會在短時間內產生大量異常結果，因此必須為已刪除的任務清理異常結果。透過此欄位，您可以設定最多可快取多少個已刪除的任務。外掛程式會在任務被刪除時清理其結果。如果外掛程式無法完成此清理作業，它會將該任務的結果加入快取，並由每小時執行一次的 cron 工作進行清理。您可以使用此設定限制放入快取的舊任務數量，以避免 DDoS 攻擊。一小時後，如果您仍在快取中發現舊任務的結果，請使用[刪除偵測器結果 API]({{site.url}}{{site.baseurl}}/observing-your-data/ad/api/#delete-detector-results)手動刪除該任務結果。您可以將此設定從 1 調整到 10,000。預設為 `1000`。

- `plugins.anomaly_detection.delete_anomaly_result_when_delete_detector`（動態，布林值）：當您刪除偵測器時，Anomaly Detection 外掛程式是否刪除異常結果。如果您想節省一些磁碟空間，尤其是當您有產生大量結果的高基數偵測器時，請將此設定設為 `true`。或者，您也可以使用[刪除偵測器結果 API]({{site.url}}{{site.baseurl}}/observing-your-data/ad/api/#delete-detector-results)手動刪除結果。預設為 `false`。

- `plugins.anomaly_detection.dedicated_cache_size`（動態，整數）：如果高基數偵測器的即時分析成功啟動，Anomaly Detection 外掛程式保證在每個節點的記憶體中保留 10 個（可透過此設定動態調整）實體的模型。如果實體數量超過此限制，外掛程式會將多出來的實體模型放到所有偵測器共用的記憶體空間。實際的實體數量會依您可用的記憶體與實體的頻率而有所不同。如果您希望外掛程式保證在記憶體中保留更多實體的模型，而且您的叢集有足夠的記憶體， 可以增加此設定的值。預設為 `10`。

- `plugins.anomaly_detection.max_concurrent_preview`（動態，整數）：可同時執行的預覽數量上限。您可以使用此設定來限制資源使用。預設為 `2`。

- `plugins.anomaly_detection.model_max_size_percent`（動態，浮點數）：模型記憶體百分比的上限。預設為 `0.1`。

- `plugins.anomaly_detection.door_keeper_in_cache.enabled`（動態，布林值）：設為 `true` 時，OpenSearch 會在非作用中實體快取前面放置一個 bloom filter，以篩選出不太可能出現超過一次的項目。預設為 `false`。

- `plugins.anomaly_detection.hcad_cold_start_interpolation.enabled`（動態，布林值）：設為 `true` 時，會在高基數異常偵測（HCAD）的初始冷啟動期間啟用內插。預設為 `false`。

- `plugins.anomaly_detection.jvm_heap_usage_threshold`（動態，整數）：停用異常偵測器的 JVM 記憶體使用量百分比閾值。有效值為 0--98。當 JVM heap 使用量達到此百分比時，偵測器會被停用。預設為 `95`。
