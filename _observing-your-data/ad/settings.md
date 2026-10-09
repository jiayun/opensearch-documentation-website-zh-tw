---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定"
parent: Anomaly detection
nav_order: 4
redirect_from: 
  - /monitoring-plugins/ad/settings/
---

# 異常偵測設定

Anomaly Detection 外掛程式會在標準的 OpenSearch 叢集設定中新增數項設定。
這些設定是動態的，因此您無需重新啟動叢集即可變更外掛程式的預設行為。若要進一步了解靜態與動態設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

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

設定 | 預設值 | 說明
:--- | :--- | :---
`plugins.anomaly_detection.enabled` | True | Anomaly Detection 外掛程式是否啟用。若停用，所有偵測器會立即停止執行。
`plugins.anomaly_detection.max_anomaly_detectors` | 1,000 | 使用者可建立的非高基數偵測器（無類別欄位）數量上限。
`plugins.anomaly_detection.max_multi_entity_anomaly_detectors` | 10 | 一個叢集中高基數偵測器（含類別欄位）的數量上限。
`plugins.anomaly_detection.max_anomaly_features` | 5 | 一個偵測器的特徵數量上限。
`plugins.anomaly_detection.ad_result_history_rollover_period` | 12h | 檢查輪替條件的頻率。若為 `true`，Anomaly Detection 外掛程式會將結果索引輪替至新索引。
`plugins.anomaly_detection.ad_result_history_max_docs_per_shard` | 1,350,000,000 | 結果索引單一分片中的文件數量上限。Anomaly Detection 外掛程式只會計算主要分片中已重新整理的文件。
`plugins.anomaly_detection.max_entities_per_query` | 1,000,000 | 高基數偵測器在每個偵測區間內的唯一值數量上限。預設情況下，若類別欄位在某個偵測區間內的唯一值超過設定的數量，Anomaly Detection 外掛程式會依類別值的自然排序排列（例如實體 `ab` 排在 `bc` 之前），然後選取前幾個值。
`plugins.anomaly_detection.max_entities_for_preview` | 5 | 高基數偵測器在預覽操作中顯示的唯一類別欄位值數量上限。預設情況下，若類別欄位在某個偵測區間內的唯一值超過設定的數量，Anomaly Detection 外掛程式會依類別值的自然排序排列（例如實體 `ab` 排在 `bc` 之前），然後選取前幾個值。
`plugins.anomaly_detection.max_primary_shards` | 10 | 一個異常偵測索引可擁有的主要分片數量上限。
`plugins.anomaly_detection.filter_by_backend_roles` | False | 當您啟用 Security 外掛程式並將此設定為 `true` 時，Anomaly Detection 外掛程式會根據使用者的後端角色篩選結果。
`plugins.anomaly_detection.max_batch_task_per_node` | 10 | 啟動歷史分析會觸發一個批次工作。此設定是每個資料節點可執行的批次工作數量。您可以將此設定調整為 1 到 1,000。如果資料節點無法支援所有批次工作，而您不確定資料節點是否有能力執行更多歷史分析，請新增更多資料節點，而不是將此設定調高。增加此值可能會為每個資料節點帶來更多負載。
`plugins.anomaly_detection.max_old_ad_task_docs_per_detector` | 1 | 您可以對同一個偵測器多次執行歷史分析。每次執行時，Anomaly Detection 外掛程式都會建立一個新工作。此設定是外掛程式保留的先前工作數量。請將此值至少設為 1，以追蹤其最後一次執行。您最多可保留 1,000 個舊工作，以避免叢集負載過重。
`plugins.anomaly_detection.batch_task_piece_size` | 1,000 | 歷史工作的日期範圍會被分割成較小的片段，Anomaly Detection 外掛程式會逐片執行該工作。每個片段預設包含 1,000 個偵測區間。例如，若偵測區間為 1 分鐘，一個片段為 1,000 分鐘，則每 1,000 分鐘查詢一次特徵資料。您可以將此設定變更為 1 到 10,000。
`plugins.anomaly_detection.batch_task_piece_interval_seconds` | 5 | 在同一個歷史分析工作的兩個片段之間加入時間間隔。此間隔可防止工作耗用過多可用資源，而使搜尋與大量編製索引等其他作業資源匱乏。您可以將此設定變更為 1 到 600 秒。
`plugins.anomaly_detection.max_top_entities_for_historical_analysis` | 1,000 | 高基數偵測器歷史分析可執行的頂端實體數量上限。範圍為 1 到 10,000。
`plugins.anomaly_detection.max_running_entities_per_detector_for_historical_analysis` | 10 | 高基數偵測器分析可平行執行的實體工作數量。叢集上可用的工作槽數量也會影響可平行執行的實體數量。若叢集有 3 個資料節點，每個資料節點預設有 10 個工作槽。假設您已有兩個高基數偵測器，且各自執行 10 個實體。若您啟動一個需要 1 個工作槽的單一實體偵測器，可用的工作槽數量為 `10 * 3 - 10 * 2 - 1 = 9`。若您此時啟動新的高基數偵測器，該偵測器只能平行執行 9 個實體，而不是 10 個。您可以根據叢集的能力將此值調整為 1 到 1,000。若設定較高的值，Anomaly Detection 外掛程式會更快完成歷史分析，但也會耗用更多資源。
`plugins.anomaly_detection.max_cached_deleted_tasks` | 1,000 | 您可以對單一偵測器任意多次重新執行歷史分析。Anomaly Detection 外掛程式只會保留有限數量的舊工作，預設為 1 個舊工作。若您對某個偵測器執行歷史分析三次，最舊的工作會被刪除。由於歷史分析會在短時間內產生大量異常結果，因此必須清理已刪除工作的異常結果。透過此欄位，您可以設定最多可快取多少個已刪除的工作。外掛程式會在工作被刪除時清理其結果。若外掛程式無法完成此清理，會將該工作的結果加入快取，並由每小時執行一次的 cron 工作進行清理。您可以使用此設定限制放入快取的舊工作數量，以避免 DDoS 攻擊。一小時後，若您仍在快取中發現舊工作結果，請使用[刪除偵測器結果 API]({{site.url}}{{site.baseurl}}/monitoring-plugins/ad/api/#delete-detector-results) 手動刪除該工作結果。您可以將此設定調整為 1 到 10,000。
`plugins.anomaly_detection.delete_anomaly_result_when_delete_detector` | False | 當您刪除偵測器時，Anomaly Detection 外掛程式是否刪除異常結果。若想節省一些磁碟空間，尤其是當您有產生大量結果的高基數偵測器時，請將此欄位設為 true。或者，您可以使用[刪除偵測器結果 API]({{site.url}}{{site.baseurl}}/monitoring-plugins/ad/api/#delete-detector-results) 手動刪除結果。
`plugins.anomaly_detection.dedicated_cache_size` | 10 | 若高基數偵測器的即時分析成功啟動，Anomaly Detection 外掛程式會保證在每個節點的記憶體中保留 10 個（可透過此設定動態調整）實體的模型。若實體數量超過此上限，外掛程式會將多出來的實體模型放入所有偵測器共用的記憶體空間。實際的實體數量會依您可用的記憶體以及實體的頻率而有所不同。若您希望外掛程式在記憶體中保證保留更多實體的模型，且您的叢集有足夠的記憶體，可以增加此設定的值。
`plugins.anomaly_detection.max_concurrent_preview` | 2 | 可同時進行的預覽數量上限。您可以使用此設定來限制資源使用量。
`plugins.anomaly_detection.model_max_size_percent` | 0.1 | 模型記憶體百分比的上限。
`plugins.anomaly_detection.door_keeper_in_cache.enabled` | False | 設為 `true` 時，OpenSearch 會在非作用中實體快取前面放置一個 bloom filter，以篩選掉不太可能出現超過一次的項目。
`plugins.anomaly_detection.hcad_cold_start_interpolation.enabled` | False | 設為 true 時，會在高基數異常偵測（HCAD）的初始冷啟動期間啟用內插。
`plugins.anomaly_detection.jvm_heap_usage_threshold` | 95 | 指定停用異常偵測器的 JVM 記憶體使用率門檻（以百分比表示）。預設值為 95%，表示當 JVM 堆積使用率達到 95% 時，偵測器將被停用。