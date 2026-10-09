---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "摘要報告"
nav_order: 40
parent: Reference
redirect_from:
  - /benchmark/user-guide/understanding-results/summary-reports/
  - /benchmark/user-guide/understanding-results/
---

# 摘要報告

每次測試執行結束時，OpenSearch Benchmark 都會列印一份摘要報告，其中包含服務時間、輸送量、延遲等指標。這些指標顯示所選工作負載在受基準測試的 OpenSearch 叢集上的表現。

## 輸出範例

下列範例顯示一份典型的摘要報告：

```bash
------------------------------------------------------
    _______             __   _____
   / ____(_)___  ____ _/ /  / ___/_________  ________
  / /_  / / __ \/ __ `/ /   \__ \/ ___/ __ \/ ___/ _ \
 / __/ / / / / / /_/ / /   ___/ / /__/ /_/ / /  /  __/
/_/   /_/_/ /_/\__,_/_/   /____/\___/\____/_/   \___/
------------------------------------------------------

|                                                         Metric |                                       Task |       Value |   Unit |
|---------------------------------------------------------------:|-------------------------------------------:|------------:|-------:|
|                     Cumulative indexing time of primary shards |                                            |     0.02655 |    min |
|             Min cumulative indexing time across primary shards |                                            |           0 |    min |
|          Median cumulative indexing time across primary shards |                                            |  0.00176667 |    min |
|             Max cumulative indexing time across primary shards |                                            |   0.0140333 |    min |
|                        Cumulative merge time of primary shards |                                            |   0.0102333 |    min |
|                                                     Store size |                                            | 0.000485923 |     GB |
|                                                  Segment count |                                            |          32 |        |
|                                                 Min Throughput |                                      index |     3008.97 | docs/s |
|                                                Mean Throughput |                                      index |     3008.97 | docs/s |
|                                              Median Throughput |                                      index |     3008.97 | docs/s |
|                                                 Max Throughput |                                      index |     3008.97 | docs/s |
|                                        50th percentile latency |                                      index |     351.059 |     ms |
|                                       100th percentile latency |                                      index |     365.058 |     ms |
|                                   50th percentile service time |                                      index |     351.059 |     ms |
|                                  100th percentile service time |                                      index |     365.058 |     ms |
|                                                     error rate |                                      index |           0 |      % |
|                                                 Min Throughput |                                  match_all |       36.09 |  ops/s |
|                                                Mean Throughput |                                  match_all |       36.09 |  ops/s |
|                                              Median Throughput |                                  match_all |       36.09 |  ops/s |
|                                                 Max Throughput |                                  match_all |       36.09 |  ops/s |
|                                       100th percentile latency |                                  match_all |     35.9822 |     ms |
|                                  100th percentile service time |                                  match_all |     7.93048 |     ms |
|                                                     error rate |                                  match_all |           0 |      % |
|                                                            ... |                                        ... |         ... |    ... |
```

叢集專屬的指標從 `index` 任務那一行開始。例如：

- 若要評估您的叢集能承受多少負載，`index` 任務指標會顯示工作負載執行期間匯入的文件數量，以及匯入錯誤率。
- 若要評估查詢延遲與服務時間，`match_all` 和 `term` 任務會顯示每秒執行的查詢操作數、可測量的查詢延遲，以及查詢操作錯誤率。

報告中顯示哪些值取決於 `--show-in-results` 旗標；請參閱[儲存結果](#storing-results)。

## 儲存結果

結果預設儲存在記憶體中。儲存在記憶體中時，結果會寫入 `~/.benchmark/benchmarks/test-runs/<test_run_id>/`，並以最近一次工作負載測試的 `test_run_id` 命名。

[執行測試]({{site.url}}{{site.baseurl}}/benchmark/reference/commands/run/#general-settings)時，下列旗標可自訂結果的儲存方式：

- `--results-file`：要寫入摘要報告的檔案路徑。
- `--results-format`：摘要的輸出格式。`markdown` 或 `csv`。預設為 `markdown`。
- `--show-in-results`：發布的報告中會出現哪些值。`available`、`all-percentiles` 或 `all`。預設為 `available`。
- `--user-tag`：與該次執行一起儲存為中繼資料的鍵值組（例如 `intention:baseline-ticket-12345`）。將指標儲存在外部儲存空間時很有用。

若要將結果儲存在 test-runs 目錄之外，請設定外部指標資料存放區。如需每晚發布的結果，請參閱 OpenSearch Benchmark [每夜測試儀表板](https://opensearch.org/benchmarks)。

## 指標參考

摘要報告中包含下列指標。

### 主要分片的累計索引時間

**對應的指標鍵**：`indexing_total_time`

由 Index Stats API 回報的索引累計耗用時間。請注意，這不是實際經過時間 (wall-clock time)，例如，若 M 個索引執行緒執行了 N 分鐘，則回報 M * N 分鐘，而非 N 分鐘。

### 跨主要分片的累計索引時間

**對應的指標鍵**：`indexing_total_time`（屬性：`per-shard`）

由 Index Stats API 回報的各主要分片索引累計耗用時間的最小值、中位數與最大值。

### 主要分片的累計索引節流時間

**對應的指標鍵**：`indexing_throttle_time`

由 Index Stats API 回報的索引受到節流的累計時間。請注意，這不是實際經過時間 (wall-clock time)，例如，若 M 個索引執行緒執行了 N 分鐘，則回報 M * N 分鐘，而非 N 分鐘。


### 跨主要分片的累計索引節流時間

**對應的指標鍵**：`indexing_throttle_time`（屬性：`per-shard`）

由 Index Stats API 回報的各主要分片索引受到節流之累計時間的最小值、中位數與最大值。


### 主要分片的累計合併時間

**對應的指標鍵**：`merges_total_time`

由 Index Stats API 回報的主要分片合併累計執行時間。請注意，這不是實際經過時間 (wall-clock time)。

### 主要分片的累計合併次數

**對應的指標索引鍵**：`merges_total_count`

主要分片的累計合併次數，由 Index Stats API 於 `_all/primaries` 下回報。


### 跨主要分片的累計合併時間

**對應的指標索引鍵**：`merges_total_time` (屬性：`per-shard`)

由 Index Stats API 回報的各主要分片合併累計時間之最小值、中位數與最大值。


### 主要分片的累計重新整理時間

**對應的指標索引鍵**：`refresh_total_time`

由 Index Stats API 回報的主要分片索引重新整理累計時間。請注意，這不是實際經過時間 (wall-clock time)。

### 主要分片的累計重新整理次數

**對應的指標索引鍵**：`refresh_total_count`

主要分片的累計重新整理次數，由 Index Stats API 於 `_all/primaries` 下回報。

### 跨主要分片的累計重新整理時間

**對應的指標索引鍵**：`refresh_total_time` (屬性：`per-shard`)

由 Index Stats API 回報的各主要分片索引重新整理累計時間之最小值、中位數與最大值。

### 主要分片的累計排清時間

**對應的指標索引鍵**：`flush_total_time`

由 Index Stats API 回報的主要分片索引排清累計時間。請注意，這不是實際經過時間 (wall-clock time)。

### 主要分片的累計排清次數

**對應的指標索引鍵**：`flush_total_count`

主要分片的累計排清次數，由 Index Stats API 於 `_all/primaries` 下回報。


### 跨主要分片的累計排清時間

**對應的指標索引鍵**：`flush_total_time` (屬性：`per-shard`)

由 Index Stats API 回報的各主要分片索引排清時間之最小值、中位數與最大值。

### 主要分片的累計合併節流時間

**對應的指標索引鍵**：`merges_total_throttled_time`

由 Index Stats API 回報的合併作業中已遭節流的累計時間。請注意，這不是實際經過時間 (wall-clock time)。

### 跨主要分片的累計合併節流時間

**對應的指標索引鍵**：`merges_total_throttled_time` (屬性：`per-shard`)

由 Index Stats API 回報的各主要分片合併作業已遭節流的累計時間之最小值、中位數與最大值。

### ML 處理時間

**對應的指標索引鍵**：`ml_processing_time`

機器學習 (ML) 作業處理單一桶 (bucket) 所花費時間的最小值、平均值、中位數與最大值，以毫秒為單位。


### 年輕世代 GC 總時間

**對應的指標索引鍵**：`node_total_young_gen_gc_time`

由 Node Stats API 回報的整個叢集年輕世代 (young gen) 垃圾收集 (GC) 總執行時間。

### 年輕世代 GC 總次數

**對應的指標索引鍵**：`node_total_young_gen_gc_count`

由 Node Stats API 回報的整個叢集年輕世代 GC 總次數。


### 老世代 GC 總時間

**對應的指標索引鍵**：`node_total_old_gen_gc_time`

由 Node Stats API 回報的整個叢集老世代 (old gen) GC 總執行時間。

### 老世代 GC 總次數

**對應的指標索引鍵**：`node_total_old_gen_gc_count`

由 Node Stats API 回報的整個叢集老世代 GC 總次數。

### ZGC 循環 GC 總時間

**對應的指標索引鍵**：`node_total_zgc_cycles_gc_count`

由 Node Stats API 回報的整個叢集 Z 垃圾收集器 (ZGC) 所執行的垃圾收集總次數。

### ZGC 暫停 GC 總時間

**對應的指標索引鍵**：`node_total_zgc_pauses_gc_time`

由 Node Stats API 回報的整個叢集 ZGC 花費在停止整個世界 (stop-the-world) 暫停的總時間。


### ZGC 暫停 GC 總次數

**對應的指標索引鍵**：`node_total_zgc_pauses_gc_count`

由 Node Stats API 回報的整個叢集 ZGC 所執行的停止整個世界 (stop-the-world) 暫停總次數。


### 儲存區大小

**對應的指標索引鍵**：`store_size_in_bytes`

由 Index Stats API 回報的索引大小，以位元組為單位 (不含 translog)。

### Translog 大小

**對應的指標索引鍵**：`translog_size_in_bytes`

由 Index Stats API 回報的 translog 大小，以位元組為單位。

### X 所使用的堆積記憶體

**對應的指標索引鍵**：`segments_*_in_bytes`

由 Index Stats API 回報的對應項目所使用的位元組數。該項目可以是下列任一項：

- Doc values
- Terms
- Norms
- Points
- Stored fields


### 分段數

**對應的指標索引鍵**：`segments_count`

由 Index Stats API 回報的分段總數。


### 資料匯入管線總次數

**對應的指標索引鍵**：`ingest_pipeline_cluster_count`

在競賽期間，叢集內所有節點所匯入的文件總數。

### 資料匯入管線總時間

**對應的指標索引鍵**：`ingest_pipeline_cluster_time`

在競賽期間，叢集內所有節點前置處理匯入文件所花費的總時間，以毫秒為單位。


### 資料匯入管線失敗總數

**對應的指標索引鍵**：`ingest_pipeline_cluster_failed`

在競賽期間，叢集內所有節點失敗的匯入作業總數。


### 輸送量

**對應的指標索引鍵**：`throughput`

回報每個任務的輸送量最小值、平均值、中位數與最大值。

OpenSearch 在特定時間內每秒可執行的作業數。報告包含每個任務的輸送量最小值、平均值、中位數與最大值。


### 延遲

**對應的指標索引鍵**：`latency`

從提交請求到收到完整回應之間的時間。其中包含請求在由 OpenSearch 處理之前所花費的等待時間。OpenSearch 會為每個任務回報數個百分位數。顯示哪些百分位數取決於 OpenSearch 在延遲期間內能擷取多少個請求。


### 服務時間

**對應的指標索引鍵**：`service_time`

從傳送請求到收到對應回應之間的時間。其中不包含等待時間。雖然許多負載測試工具將此指標稱為 _latency_，但兩者並不相同。OpenSearch 會為每個任務回報數個百分位數。顯示哪些百分位數取決於 OpenSearch 在延遲期間內能擷取多少個請求。



### 處理時間

只有在 OpenSearch Benchmark 組態檔中將設定 `output.processingtime` 設為 `true` 時，才會回報處理時間。
{: note.}

**對應的指標索引鍵**：`processing_time`


從開始處理請求到取得完整回應之間的時間。與 `service_time` 不同，此指標包含 OpenSearch 的用戶端處理額外負荷。`service_time` 與 `processing_time` 之間的差異越大，用戶端的額外負荷就越高。視您的處理目標而定，這可能指出有潛在的用戶端瓶頸需要調查。


### 錯誤率

**對應的指標索引鍵**：`service_time`。每筆 `service_time` 記錄都有一個 `meta.success` 旗標。

錯誤回應相對於回應總數的比例。Python OpenSearch 用戶端所擲回的任何例外狀況都視為錯誤，例如 HTTP 回應碼 4xx、5xx 或網路錯誤 (網路無法連線)。您可以檢查 OpenSearch 與 OpenSearch Benchmark 記錄檔並重新執行基準測試，以調查根本原因。


### 磁碟使用量

**對應的指標鍵**：`disk_usage_total`
**指標中繼資料**：`index` 與 `field`

單一欄位在磁碟上使用的位元組總數。Disk Usage API 回傳的每個欄位都會記錄此數值，即使總數為 `0`。
