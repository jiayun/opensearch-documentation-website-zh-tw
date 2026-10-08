---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指標鍵"
nav_order: 35
parent: Metrics reference
grand_parent: Reference
redirect_from:
  - /benchmark/metrics/metric-keys/
---

# 指標鍵

指標鍵是 OpenSearch Benchmark 根據 [metrics record]({{site.url}}{{site.baseurl}}/benchmark/metrics/metric-records/) 中的組態所儲存的指標。OpenSearch Benchmark 會儲存下列指標：


- `latency`：從提交請求到收到完整回應之間的時間。這也包含等待時間，例如請求等待 OpenSearch Benchmark 準備好提供服務所花費的時間。
- `service_time`：從傳送請求到收到對應回應之間的時間。此指標與延遲類似，但不包含等待時間。
- `processing_time`：從開始處理請求到收到完整回應之間的時間。與服務時間相反，此指標也包含 OpenSearch Benchmark 用戶端處理的額外負荷。服務時間與處理時間之間的巨大差異表示用戶端有很高的額外負荷，因此可能指向潛在的用戶端瓶頸，需要進一步調查。
- `throughput`：OpenSearch Benchmark 在特定時間範圍內可執行的作業數，通常以每秒為單位。作業類型的定義請參閱 [`operations`]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/operations/)。
- `disk_io_write_bytes`：基準測試期間寫入磁碟的位元組數。在 Linux 上，此指標僅對應 OpenSearch Benchmark 所寫入的位元組。在 macOS 上，則包含所有處理程序寫入的位元組數。
- `disk_io_read_bytes`：基準測試期間從磁碟讀取的位元組數。在 macOS 上，這包含所有處理程序寫入的位元組數。
- `node_startup_time`：從處理程序啟動到節點開始執行之間的時間量，以秒為單位。
- `node_total_young_gen_gc_time`：整個叢集中年輕代垃圾收集器的總執行時間，由 Nodes Stats API 回報。
- `node_total_young_gen_gc_count`：整個叢集中年輕代垃圾收集的總次數，由 Nodes Stats API 回報。
- `node_total_old_gen_gc_time`：整個叢集中舊生代垃圾收集器的總執行時間，由 Nodes Stats API 回報。
- `node_total_old_gen_gc_count`：整個叢集中舊生代垃圾收集的總次數，由 Nodes Stats API 回報。
- `node_total_zgc_cycles_gc_time`：整個叢集中 Z 垃圾收集器 (ZGC) 花費於垃圾收集的總時間，由 Nodes Stats API 回報。
- `node_total_zgc_cycles_gc_count`：整個叢集中 ZGC 執行垃圾收集的總次數，由 Nodes Stats API 回報。
- `node_total_zgc_pauses_gc_time`：整個叢集中 ZGC 花費於 Stop-The-World 暫停的總時間，由 Nodes Stats API 回報。
- `node_total_zgc_pauses_gc_count`：整個叢集中 ZGC 執行期間 Stop-The-World 暫停的總次數，由 Nodes Stats API 回報。
- `segments_count`：開啟區段的總數，由 Index Stats API 回報。
- `segments_memory_in_bytes`：所有開啟區段所使用的位元組總數，由 Index Stats API 回報。
- `segments_doc_values_memory_in_bytes`：文件值所使用的位元組數，由 Index Stats API 回報。
- `segments_stored_fields_memory_in_bytes`：已儲存欄位所使用的位元組數，由 Index Stats API 回報。
- `segments_terms_memory_in_bytes`：詞彙所使用的位元組數，由 Index Stats API 回報。
- `segments_norms_memory_in_bytes`：標準化因子所使用的位元組數，由 Index Stats API 回報。
- `segments_points_memory_in_bytes`：點所使用的位元組數，由 Index Stats API 回報。
- `merges_total_time`：主要分片合併的累計執行時間，由 Index Stats API 回報。請注意，此時間並非實際經過時間。如果 M 個合併執行緒執行了 N 分鐘，Benchmark 回報的時間量會是 M * N 分鐘，而非 N 分鐘。這些指標記錄有一個額外的 per-shard 屬性，其中包含陣列中各主要分片的時間。
- `merges_total_count`：主要分片合併的累計次數，由 Index Stats API 在 `_all/primaries` 下回報。
- `merges_total_throttled_time`：已節流之合併的累計時間，由 Index Stats API 回報。請注意，此時間並非實際經過時間。這些指標記錄有一個額外的 per-shard 屬性，其中包含陣列中各主要分片的時間。
- `indexing_total_time`：主要分片編製索引所使用的累計時間，由 Index Stats API 回報。請注意，這並非實際經過時間。這些指標記錄有一個額外的 per-shard 屬性，其中包含陣列中各主要分片的時間。
- `indexing_throttle_time`：編製索引遭到節流的累計時間，由 Index Stats API 回報。請注意，這並非實際經過時間。這些指標記錄有一個額外的 per-shard 屬性，其中包含陣列中各主要分片的時間。
- `refresh_total_time`：主要分片索引重新整理所使用的累計時間，由 Index Stats API 回報。請注意，這並非實際經過時間。這些指標記錄有一個額外的 per-shard 屬性，其中包含陣列中各主要分片的時間。
- `refresh_total_count`：主要分片重新整理的累計次數，由 Index Stats API 在 `_all/primaries` 下回報。
- `flush_total_time`：主要分片索引沖刷所使用的累計時間，由 Index Stats API 回報。請注意，這並非實際經過時間。這些指標記錄有一個額外的 per-shard 屬性，其中包含陣列中各主要分片的時間。
- `flush_total_count`：主要分片沖刷的累計次數，由 Index Stats API 在 `_all/primaries` 下回報。
- `final_index_size_bytes`：基準測試結束時，所有節點關閉後檔案系統上的最終索引大小，以位元組為單位。它包含節點資料目錄中的所有檔案，例如索引檔案和交易記錄。
- `store_size_in_bytes`：索引的大小，不含交易記錄，由 Index Stats API 回報，以位元組為單位。
- `translog_size_in_bytes`：交易記錄的大小，由 Index Stats API 回報，以位元組為單位。
- `ml_processing_time`：一個物件，包含每個機器學習作業的最小、平均、中位數和最大桶處理時間，以毫秒為單位。只有在對應的基準測試中已建立機器學習作業時，才能使用這些指標。
