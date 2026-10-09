---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "向量搜尋"
parent: Workload types
nav_order: 10
---

# 向量搜尋工作負載

向量搜尋工作負載會針對編製索引與搜尋作業，對 OpenSearch 的向量引擎功能進行基準測試。它會測試各種向量搜尋演算法、量化方法與索引組態，以衡量輸送量、延遲與召回準確度等效能指標。此工作負載支援不同的資料集，並可評估已訓練與未訓練的向量搜尋方法。

此工作負載支援 `HDF5` 或 `BIG-ANN` 格式的資料集。若要下載資料集，請使用[此連結](http://corpus-texmex.irisa.fr/)。

## 支援的工作負載參數

向量搜尋工作負載支援下列工作負載參數。

| 名稱                                      | 說明                                                                                                                                     |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `target_index_name`                       | 要加入向量的索引名稱。                                                                                                           |
| `target_field_name`                       | 要加入向量的欄位名稱。使用 "." 表示巢狀欄位。                                                                     |
| `target_index_body`                       | 目標索引定義的路徑。                                                                                                        |
| `target_index_primary_shards`             | 目標索引的主要分片數量。                                                                                                              |
| `target_index_replica_shards`             | 目標索引的副本分片數量。                                                                                                              |
| `target_index_dimension`                  | 目標索引的維度。                                                                                                              |
| `target_index_space_type`                 | 目標索引的空間類型。                                                                                                                    |
| `target_index_bulk_size`                  | 目標索引的批次大小。                                                                                                                     |
| `target_index_bulk_index_data_set_format` | 向量資料集的格式。                                                                                                               |
| `target_index_bulk_index_data_set_path`   | 索引中向量資料集的路徑。                                                                                                   |
| `target_index_bulk_index_data_set_corpus` | 向量資料集的語料庫名稱。                                                                                                         |
| `target_index_bulk_index_clients`         | 用於大量匯入的用戶端數量。必須是資料集大小的因數。                                                                  |
| `target_index_max_num_segments`           | 開始搜尋前要合併至目標索引的分段數量。                                                              |
| `target_index_force_merge_timeout`        | 強制合併請求前的等待時間（以秒為單位）。                                                                          |
| `hnsw_ef_search `                         | `HNSW ef` 搜尋參數。                                                                                                                 |
| `hnsw_ef_construction`                      | `HNSW ef` 建構參數。                                                                                                           |
| `id_field_name`                           | 用於識別索引中文件的欄位名稱。                                                                      |
| `hnsw_m `                                 | `HNSW m` 參數。                                                                                                                         |
| `query_k`                                 | 搜尋要傳回的鄰居數量。`query_k`、`query_max_distance` 或 `query_min_score` 三者只能提供其中一個。          |
| `query_max_distance `                     | 向量搜尋要傳回的最大距離。`query_k`、`query_max_distance` 或 `query_min_score` 三者只能提供其中一個。 |
| `query_min_score`                         | 向量搜尋要傳回的最低分數。`query_k`、`query_max_distance` 或 `query_min_score` 三者只能提供其中一個。    |
| `query_data_set_format`                   | 查詢所使用的向量資料集格式。`query_k`、`query_max_distance` 或 `query_min_score` 三者只能提供其中一個。        |
| `query_data_set_path`                     | 查詢所使用的向量資料集路徑。                                                                                               |
| `query_count`                             | 搜尋作業所使用的查詢數量。                                                                                                 |
| `query_body`                              | 將與搜尋本文合併的 JSON 屬性。                                                                                        |
| `search_clients`                          | 用於執行查詢的用戶端數量。                                                                                               |
| `repetitions`                             | 資料集耗盡前完成的重複次數。預設為 `1`。                                                                      |
| `target_throughput`                       | 每個查詢作業的目標輸送量，以每秒請求數為單位。預設為 `10`。                                                         |
| `time_period`                             | 執行基準測試的時間長度，以秒為單位。預設為 `900`。                                                       |



## 測試程序

向量搜尋工作負載支援下列測試程序。

### 未訓練測試程序

未訓練測試程序會測試不需要訓練的向量搜尋索引。您可以將向量搜尋演算法的底層組態（例如指定特定的引擎或空間類型）定義為方法定義。

### 未訓練測試（僅編製索引）程序

未訓練測試（僅編製索引）程序用於為不需要訓練的向量搜尋索引編製索引。當您只想對編製索引作業進行基準測試時，這特別有用。

### 未訓練測試 (Amazon OpenSearch Serverless)

Amazon OpenSearch Serverless 的未訓練測試程序專門用於 OpenSearch Serverless 向量搜尋集合。此程序不包含 **refresh** 和 **warmup** 等操作，因為向量搜尋集合不支援這些操作。

### 強制合併索引程序

強制合併索引程序會執行強制合併操作，將分段數合併至指定的上限，藉此最佳化向量搜尋索引。對於大型資料集而言，強制合併是成本高昂的操作。因此，我們建議使用個別程序，依使用者需求偶爾觸發強制合併操作。

### 訓練測試程序

訓練測試程序會對需要訓練步驟的近似 k-NN 搜尋演算法進行基準測試。舉例來說，Faiss 反向檔案索引 (IVF) 技術需要訓練步驟才能擷取叢集向量。執行該步驟後，基準測試便能搜尋較少數量的叢集質心，而不必搜尋整個資料集。

### 搜尋程序

搜尋程序會對先前已編製索引的向量搜尋索引進行基準測試。當您想對大型向量搜尋索引進行基準測試，又不想每次都重新編製索引時，這項程序便很實用，因為大型資料集的載入時間可能相當可觀。此程序包含暖機操作，旨在避免向量搜尋期間發生冷啟動問題。

## 自訂執行器

向量搜尋工作負載僅支援一種自訂執行器：`warmup-knn-indices`。此執行器會暖機 k-NN 索引，並重試暖機直到成功為止。

## 執行工作負載

若要執行向量搜尋工作負載，請使用下列命令：

```bash
export ENDPOINT=<cluster-endpoint>
export PARAMS_FILE=<params-file-path>

opensearch-benchmark run \
    --target-hosts $ENDPOINT \
    --workload vectorsearch \
    --workload-params ${PARAMS_FILE} \
    --pipeline benchmark-only \
    --kill-running-processes
```
{% include copy.html %}

## 範例結果

使用向量搜尋工作負載時，您可以預期結果類似下列內容。

### 訓練測試程序

下列範例提供訓練測試程序的結果：


```
------------------------------------------------------
    _______             __   _____
   / ____(_)___  ____ _/ /  / ___/_________  ________
  / /_  / / __ \/ __ `/ /   \__ \/ ___/ __ \/ ___/ _ \
 / __/ / / / / / /_/ / /   ___/ / /__/ /_/ / /  /  __/
/_/   /_/_/ /_/\__,_/_/   /____/\___/\____/_/   \___/
------------------------------------------------------

|                                                         Metric |               Task |       Value |   Unit |
|---------------------------------------------------------------:|-------------------:|------------:|-------:|
|                     Cumulative indexing time of primary shards |                    |  0.00946667 |    min |
|             Min cumulative indexing time across primary shards |                    |           0 |    min |
|          Median cumulative indexing time across primary shards |                    |  0.00298333 |    min |
|             Max cumulative indexing time across primary shards |                    |  0.00336667 |    min |
|            Cumulative indexing throttle time of primary shards |                    |           0 |    min |
|    Min cumulative indexing throttle time across primary shards |                    |           0 |    min |
| Median cumulative indexing throttle time across primary shards |                    |           0 |    min |
|    Max cumulative indexing throttle time across primary shards |                    |           0 |    min |
|                        Cumulative merge time of primary shards |                    |           0 |    min |
|                       Cumulative merge count of primary shards |                    |           0 |        |
|                Min cumulative merge time across primary shards |                    |           0 |    min |
|             Median cumulative merge time across primary shards |                    |           0 |    min |
|                Max cumulative merge time across primary shards |                    |           0 |    min |
|               Cumulative merge throttle time of primary shards |                    |           0 |    min |
|       Min cumulative merge throttle time across primary shards |                    |           0 |    min |
|    Median cumulative merge throttle time across primary shards |                    |           0 |    min |
|       Max cumulative merge throttle time across primary shards |                    |           0 |    min |
|                      Cumulative refresh time of primary shards |                    |  0.00861667 |    min |
|                     Cumulative refresh count of primary shards |                    |          33 |        |
|              Min cumulative refresh time across primary shards |                    |           0 |    min |
|           Median cumulative refresh time across primary shards |                    |  0.00268333 |    min |
|              Max cumulative refresh time across primary shards |                    |  0.00291667 |    min |
|                        Cumulative flush time of primary shards |                    | 0.000183333 |    min |
|                       Cumulative flush count of primary shards |                    |           2 |        |
|                Min cumulative flush time across primary shards |                    |           0 |    min |
|             Median cumulative flush time across primary shards |                    |           0 |    min |
|                Max cumulative flush time across primary shards |                    | 0.000183333 |    min |
|                                        Total Young Gen GC time |                    |       0.075 |      s |
|                                       Total Young Gen GC count |                    |          17 |        |
|                                          Total Old Gen GC time |                    |           0 |      s |
|                                         Total Old Gen GC count |                    |           0 |        |
|                                                     Store size |                    |  0.00869293 |     GB |
|                                                  Translog size |                    | 2.56114e-07 |     GB |
|                                         Heap used for segments |                    |           0 |     MB |
|                                       Heap used for doc values |                    |           0 |     MB |
|                                            Heap used for terms |                    |           0 |     MB |
|                                            Heap used for norms |                    |           0 |     MB |
|                                           Heap used for points |                    |           0 |     MB |
|                                    Heap used for stored fields |                    |           0 |     MB |
|                                                  Segment count |                    |           9 |        |
|                                                 Min Throughput | custom-vector-bulk |       25527 | docs/s |
|                                                Mean Throughput | custom-vector-bulk |       25527 | docs/s |
|                                              Median Throughput | custom-vector-bulk |       25527 | docs/s |
|                                                 Max Throughput | custom-vector-bulk |       25527 | docs/s |
|                                        50th percentile latency | custom-vector-bulk |     36.3095 |     ms |
|                                        90th percentile latency | custom-vector-bulk |     52.2662 |     ms |
|                                       100th percentile latency | custom-vector-bulk |     68.6513 |     ms |
|                                   50th percentile service time | custom-vector-bulk |     36.3095 |     ms |
|                                   90th percentile service time | custom-vector-bulk |     52.2662 |     ms |
|                                  100th percentile service time | custom-vector-bulk |     68.6513 |     ms |
|                                                     error rate | custom-vector-bulk |           0 |      % |
|                                                 Min Throughput |       prod-queries |      211.26 |  ops/s |
|                                                Mean Throughput |       prod-queries |      213.85 |  ops/s |
|                                              Median Throughput |       prod-queries |      213.48 |  ops/s |
|                                                 Max Throughput |       prod-queries |      216.49 |  ops/s |
|                                        50th percentile latency |       prod-queries |     3.43393 |     ms |
|                                        90th percentile latency |       prod-queries |     4.01881 |     ms |
|                                        99th percentile latency |       prod-queries |     5.56238 |     ms |
|                                      99.9th percentile latency |       prod-queries |     9.95666 |     ms |
|                                     99.99th percentile latency |       prod-queries |     39.7922 |     ms |
|                                       100th percentile latency |       prod-queries |      62.415 |     ms |
|                                   50th percentile service time |       prod-queries |     3.43405 |     ms |
|                                   90th percentile service time |       prod-queries |      4.0191 |     ms |
|                                   99th percentile service time |       prod-queries |     5.56316 |     ms |
|                                 99.9th percentile service time |       prod-queries |     9.95666 |     ms |
|                                99.99th percentile service time |       prod-queries |     39.7922 |     ms |
|                                  100th percentile service time |       prod-queries |      62.415 |     ms |
|                                                     error rate |       prod-queries |           0 |      % |


------------------------------------
[INFO] ✅ SUCCESS (took 119 seconds)
------------------------------------
```

### Faiss 結果

下列範例輸出是使用 Faiss IVF 基準測試程序產生的。為求簡潔，測試使用了 100 個搜尋查詢，而非參數檔中指定的 10,000 個。所有其他參數與 `params/train` 資料夾中的設定相同。第一次執行展示未量化的結果，第二次執行展示純量量化，第三次執行展示乘積量化。請注意，量化可能導致搜尋召回率下降。

#### Faiss IVF 未量化/平面編碼


```
|                                                         Metric |                     Task |       Value |   Unit |
|---------------------------------------------------------------:|-------------------------:|------------:|-------:|
|                     Cumulative indexing time of primary shards |                          |     11.7662 |    min |
|             Min cumulative indexing time across primary shards |                          | 0.000266667 |    min |
|          Median cumulative indexing time across primary shards |                          |      0.1423 |    min |
|             Max cumulative indexing time across primary shards |                          |     11.6236 |    min |
|            Cumulative indexing throttle time of primary shards |                          |           0 |    min |
|    Min cumulative indexing throttle time across primary shards |                          |           0 |    min |
| Median cumulative indexing throttle time across primary shards |                          |           0 |    min |
|    Max cumulative indexing throttle time across primary shards |                          |           0 |    min |
|                        Cumulative merge time of primary shards |                          |     1.09872 |    min |
|                       Cumulative merge count of primary shards |                          |          21 |        |
|                Min cumulative merge time across primary shards |                          |           0 |    min |
|             Median cumulative merge time across primary shards |                          |     0.00045 |    min |
|                Max cumulative merge time across primary shards |                          |     1.09827 |    min |
|               Cumulative merge throttle time of primary shards |                          |    0.872417 |    min |
|       Min cumulative merge throttle time across primary shards |                          |           0 |    min |
|    Median cumulative merge throttle time across primary shards |                          |           0 |    min |
|       Max cumulative merge throttle time across primary shards |                          |    0.872417 |    min |
|                      Cumulative refresh time of primary shards |                          |    0.113733 |    min |
|                     Cumulative refresh count of primary shards |                          |          59 |        |
|              Min cumulative refresh time across primary shards |                          |     0.00235 |    min |
|           Median cumulative refresh time across primary shards |                          |  0.00516667 |    min |
|              Max cumulative refresh time across primary shards |                          |    0.106217 |    min |
|                        Cumulative flush time of primary shards |                          |     0.01685 |    min |
|                       Cumulative flush count of primary shards |                          |           8 |        |
|                Min cumulative flush time across primary shards |                          |           0 |    min |
|             Median cumulative flush time across primary shards |                          |  0.00791667 |    min |
|                Max cumulative flush time across primary shards |                          |  0.00893333 |    min |
|                                        Total Young Gen GC time |                          |       5.442 |      s |
|                                       Total Young Gen GC count |                          |        3739 |        |
|                                          Total Old Gen GC time |                          |           0 |      s |
|                                         Total Old Gen GC count |                          |           0 |        |
|                                                     Store size |                          |      1.3545 |     GB |
|                                                  Translog size |                          |   0.0304573 |     GB |
|                                         Heap used for segments |                          |           0 |     MB |
|                                       Heap used for doc values |                          |           0 |     MB |
|                                            Heap used for terms |                          |           0 |     MB |
|                                            Heap used for norms |                          |           0 |     MB |
|                                           Heap used for points |                          |           0 |     MB |
|                                    Heap used for stored fields |                          |           0 |     MB |
|                                                  Segment count |                          |          14 |        |
|                                                 Min Throughput | custom-vector-bulk-train |     32222.6 | docs/s |
|                                                Mean Throughput | custom-vector-bulk-train |     32222.6 | docs/s |
|                                              Median Throughput | custom-vector-bulk-train |     32222.6 | docs/s |
|                                                 Max Throughput | custom-vector-bulk-train |     32222.6 | docs/s |
|                                        50th percentile latency | custom-vector-bulk-train |     26.5199 |     ms |
|                                        90th percentile latency | custom-vector-bulk-train |     34.9823 |     ms |
|                                        99th percentile latency | custom-vector-bulk-train |     196.712 |     ms |
|                                       100th percentile latency | custom-vector-bulk-train |     230.342 |     ms |
|                                   50th percentile service time | custom-vector-bulk-train |     26.5158 |     ms |
|                                   90th percentile service time | custom-vector-bulk-train |     34.9823 |     ms |
|                                   99th percentile service time | custom-vector-bulk-train |     196.712 |     ms |
|                                  100th percentile service time | custom-vector-bulk-train |     230.342 |     ms |
|                                                     error rate | custom-vector-bulk-train |           0 |      % |
|                                                 Min Throughput |             delete-model |       10.58 |  ops/s |
|                                                Mean Throughput |             delete-model |       10.58 |  ops/s |
|                                              Median Throughput |             delete-model |       10.58 |  ops/s |
|                                                 Max Throughput |             delete-model |       10.58 |  ops/s |
|                                       100th percentile latency |             delete-model |     93.6958 |     ms |
|                                  100th percentile service time |             delete-model |     93.6958 |     ms |
|                                                     error rate |             delete-model |           0 |      % |
|                                                 Min Throughput |          train-knn-model |        0.63 |  ops/s |
|                                                Mean Throughput |          train-knn-model |        0.63 |  ops/s |
|                                              Median Throughput |          train-knn-model |        0.63 |  ops/s |
|                                                 Max Throughput |          train-knn-model |        0.63 |  ops/s |
|                                       100th percentile latency |          train-knn-model |     1577.49 |     ms |
|                                  100th percentile service time |          train-knn-model |     1577.49 |     ms |
|                                                     error rate |          train-knn-model |           0 |      % |
|                                                 Min Throughput |       custom-vector-bulk |       11055 | docs/s |
|                                                Mean Throughput |       custom-vector-bulk |     14163.8 | docs/s |
|                                              Median Throughput |       custom-vector-bulk |     12878.9 | docs/s |
|                                                 Max Throughput |       custom-vector-bulk |     33841.3 | docs/s |
|                                        50th percentile latency |       custom-vector-bulk |     81.6677 |     ms |
|                                        90th percentile latency |       custom-vector-bulk |     117.848 |     ms |
|                                        99th percentile latency |       custom-vector-bulk |     202.484 |     ms |
|                                      99.9th percentile latency |       custom-vector-bulk |     406.209 |     ms |
|                                     99.99th percentile latency |       custom-vector-bulk |     458.823 |     ms |
|                                       100th percentile latency |       custom-vector-bulk |     459.417 |     ms |
|                                   50th percentile service time |       custom-vector-bulk |     81.6621 |     ms |
|                                   90th percentile service time |       custom-vector-bulk |     117.843 |     ms |
|                                   99th percentile service time |       custom-vector-bulk |     202.294 |     ms |
|                                 99.9th percentile service time |       custom-vector-bulk |     406.209 |     ms |
|                                99.99th percentile service time |       custom-vector-bulk |     458.823 |     ms |
|                                  100th percentile service time |       custom-vector-bulk |     459.417 |     ms |
|                                                     error rate |       custom-vector-bulk |           0 |      % |
|                                                 Min Throughput |     force-merge-segments |         0.1 |  ops/s |
|                                                Mean Throughput |     force-merge-segments |         0.1 |  ops/s |
|                                              Median Throughput |     force-merge-segments |         0.1 |  ops/s |
|                                                 Max Throughput |     force-merge-segments |         0.1 |  ops/s |
|                                       100th percentile latency |     force-merge-segments |     10017.4 |     ms |
|                                  100th percentile service time |     force-merge-segments |     10017.4 |     ms |
|                                                     error rate |     force-merge-segments |           0 |      % |
|                                                 Min Throughput |           warmup-indices |        9.63 |  ops/s |
|                                                Mean Throughput |           warmup-indices |        9.63 |  ops/s |
|                                              Median Throughput |           warmup-indices |        9.63 |  ops/s |
|                                                 Max Throughput |           warmup-indices |        9.63 |  ops/s |
|                                       100th percentile latency |           warmup-indices |     103.228 |     ms |
|                                  100th percentile service time |           warmup-indices |     103.228 |     ms |
|                                                     error rate |           warmup-indices |           0 |      % |
|                                                 Min Throughput |             prod-queries |      120.06 |  ops/s |
|                                                Mean Throughput |             prod-queries |      120.06 |  ops/s |
|                                              Median Throughput |             prod-queries |      120.06 |  ops/s |
|                                                 Max Throughput |             prod-queries |      120.06 |  ops/s |
|                                        50th percentile latency |             prod-queries |     1.75219 |     ms |
|                                        90th percentile latency |             prod-queries |     2.29527 |     ms |
|                                        99th percentile latency |             prod-queries |     50.4419 |     ms |
|                                       100th percentile latency |             prod-queries |     97.9905 |     ms |
|                                   50th percentile service time |             prod-queries |     1.75219 |     ms |
|                                   90th percentile service time |             prod-queries |     2.29527 |     ms |
|                                   99th percentile service time |             prod-queries |     50.4419 |     ms |
|                                  100th percentile service time |             prod-queries |     97.9905 |     ms |
|                                                     error rate |             prod-queries |           0 |      % |
|                                                  Mean recall@k |             prod-queries |        0.96 |        |
|                                                  Mean recall@1 |             prod-queries |        0.99 |        |


------------------------------------
[INFO] ✅ SUCCESS (took 218 seconds)
------------------------------------
```

#### 使用純量量化的 Faiss IVF (100 次搜尋查詢)

```
|                                                         Metric |                     Task |       Value |   Unit |
|---------------------------------------------------------------:|-------------------------:|------------:|-------:|
|                     Cumulative indexing time of primary shards |                          |        11.5 |    min |
|             Min cumulative indexing time across primary shards |                          | 0.000283333 |    min |
|          Median cumulative indexing time across primary shards |                          |     0.10915 |    min |
|             Max cumulative indexing time across primary shards |                          |     11.3905 |    min |
|            Cumulative indexing throttle time of primary shards |                          |           0 |    min |
|    Min cumulative indexing throttle time across primary shards |                          |           0 |    min |
| Median cumulative indexing throttle time across primary shards |                          |           0 |    min |
|    Max cumulative indexing throttle time across primary shards |                          |           0 |    min |
|                        Cumulative merge time of primary shards |                          |     1.03638 |    min |
|                       Cumulative merge count of primary shards |                          |          22 |        |
|                Min cumulative merge time across primary shards |                          |           0 |    min |
|             Median cumulative merge time across primary shards |                          | 0.000266667 |    min |
|                Max cumulative merge time across primary shards |                          |     1.03612 |    min |
|               Cumulative merge throttle time of primary shards |                          |    0.798767 |    min |
|       Min cumulative merge throttle time across primary shards |                          |           0 |    min |
|    Median cumulative merge throttle time across primary shards |                          |           0 |    min |
|       Max cumulative merge throttle time across primary shards |                          |    0.798767 |    min |
|                      Cumulative refresh time of primary shards |                          |    0.107117 |    min |
|                     Cumulative refresh count of primary shards |                          |          61 |        |
|              Min cumulative refresh time across primary shards |                          |  0.00236667 |    min |
|           Median cumulative refresh time across primary shards |                          |  0.00543333 |    min |
|              Max cumulative refresh time across primary shards |                          |   0.0993167 |    min |
|                        Cumulative flush time of primary shards |                          |   0.0193167 |    min |
|                       Cumulative flush count of primary shards |                          |           9 |        |
|                Min cumulative flush time across primary shards |                          |           0 |    min |
|             Median cumulative flush time across primary shards |                          |  0.00871667 |    min |
|                Max cumulative flush time across primary shards |                          |      0.0106 |    min |
|                                        Total Young Gen GC time |                          |       5.267 |      s |
|                                       Total Young Gen GC count |                          |        3688 |        |
|                                          Total Old Gen GC time |                          |           0 |      s |
|                                         Total Old Gen GC count |                          |           0 |        |
|                                                     Store size |                          |     1.11609 |     GB |
|                                                  Translog size |                          |   0.0304573 |     GB |
|                                         Heap used for segments |                          |           0 |     MB |
|                                       Heap used for doc values |                          |           0 |     MB |
|                                            Heap used for terms |                          |           0 |     MB |
|                                            Heap used for norms |                          |           0 |     MB |
|                                           Heap used for points |                          |           0 |     MB |
|                                    Heap used for stored fields |                          |           0 |     MB |
|                                                  Segment count |                          |          18 |        |
|                                                 Min Throughput | custom-vector-bulk-train |     35950.5 | docs/s |
|                                                Mean Throughput | custom-vector-bulk-train |     35950.5 | docs/s |
|                                              Median Throughput | custom-vector-bulk-train |     35950.5 | docs/s |
|                                                 Max Throughput | custom-vector-bulk-train |     35950.5 | docs/s |
|                                        50th percentile latency | custom-vector-bulk-train |     22.8328 |     ms |
|                                        90th percentile latency | custom-vector-bulk-train |      34.864 |     ms |
|                                        99th percentile latency | custom-vector-bulk-train |      99.471 |     ms |
|                                       100th percentile latency | custom-vector-bulk-train |     210.424 |     ms |
|                                   50th percentile service time | custom-vector-bulk-train |      22.823 |     ms |
|                                   90th percentile service time | custom-vector-bulk-train |      34.864 |     ms |
|                                   99th percentile service time | custom-vector-bulk-train |      99.471 |     ms |
|                                  100th percentile service time | custom-vector-bulk-train |     210.424 |     ms |
|                                                     error rate | custom-vector-bulk-train |           0 |      % |
|                                                 Min Throughput |             delete-model |        8.39 |  ops/s |
|                                                Mean Throughput |             delete-model |        8.39 |  ops/s |
|                                              Median Throughput |             delete-model |        8.39 |  ops/s |
|                                                 Max Throughput |             delete-model |        8.39 |  ops/s |
|                                       100th percentile latency |             delete-model |     118.241 |     ms |
|                                  100th percentile service time |             delete-model |     118.241 |     ms |
|                                                     error rate |             delete-model |           0 |      % |
|                                                 Min Throughput |          train-knn-model |        0.64 |  ops/s |
|                                                Mean Throughput |          train-knn-model |        0.64 |  ops/s |
|                                              Median Throughput |          train-knn-model |        0.64 |  ops/s |
|                                                 Max Throughput |          train-knn-model |        0.64 |  ops/s |
|                                       100th percentile latency |          train-knn-model |     1564.44 |     ms |
|                                  100th percentile service time |          train-knn-model |     1564.44 |     ms |
|                                                     error rate |          train-knn-model |           0 |      % |
|                                                 Min Throughput |       custom-vector-bulk |     11313.1 | docs/s |
|                                                Mean Throughput |       custom-vector-bulk |     14065.7 | docs/s |
|                                              Median Throughput |       custom-vector-bulk |     12894.8 | docs/s |
|                                                 Max Throughput |       custom-vector-bulk |     30050.8 | docs/s |
|                                        50th percentile latency |       custom-vector-bulk |     81.4293 |     ms |
|                                        90th percentile latency |       custom-vector-bulk |     111.812 |     ms |
|                                        99th percentile latency |       custom-vector-bulk |      196.45 |     ms |
|                                      99.9th percentile latency |       custom-vector-bulk |     370.543 |     ms |
|                                     99.99th percentile latency |       custom-vector-bulk |     474.156 |     ms |
|                                       100th percentile latency |       custom-vector-bulk |     499.048 |     ms |
|                                   50th percentile service time |       custom-vector-bulk |     81.4235 |     ms |
|                                   90th percentile service time |       custom-vector-bulk |     111.833 |     ms |
|                                   99th percentile service time |       custom-vector-bulk |     197.125 |     ms |
|                                 99.9th percentile service time |       custom-vector-bulk |     370.543 |     ms |
|                                99.99th percentile service time |       custom-vector-bulk |     474.156 |     ms |
|                                  100th percentile service time |       custom-vector-bulk |     499.048 |     ms |
|                                                     error rate |       custom-vector-bulk |           0 |      % |
|                                                 Min Throughput |     force-merge-segments |         0.1 |  ops/s |
|                                                Mean Throughput |     force-merge-segments |         0.1 |  ops/s |
|                                              Median Throughput |     force-merge-segments |         0.1 |  ops/s |
|                                                 Max Throughput |     force-merge-segments |         0.1 |  ops/s |
|                                       100th percentile latency |     force-merge-segments |     10015.2 |     ms |
|                                  100th percentile service time |     force-merge-segments |     10015.2 |     ms |
|                                                     error rate |     force-merge-segments |           0 |      % |
|                                                 Min Throughput |           warmup-indices |          19 |  ops/s |
|                                                Mean Throughput |           warmup-indices |          19 |  ops/s |
|                                              Median Throughput |           warmup-indices |          19 |  ops/s |
|                                                 Max Throughput |           warmup-indices |          19 |  ops/s |
|                                       100th percentile latency |           warmup-indices |     52.1685 |     ms |
|                                  100th percentile service time |           warmup-indices |     52.1685 |     ms |
|                                                     error rate |           warmup-indices |           0 |      % |
|                                                 Min Throughput |             prod-queries |      159.49 |  ops/s |
|                                                Mean Throughput |             prod-queries |      159.49 |  ops/s |
|                                              Median Throughput |             prod-queries |      159.49 |  ops/s |
|                                                 Max Throughput |             prod-queries |      159.49 |  ops/s |
|                                        50th percentile latency |             prod-queries |     1.92377 |     ms |
|                                        90th percentile latency |             prod-queries |     2.63867 |     ms |
|                                        99th percentile latency |             prod-queries |      48.513 |     ms |
|                                       100th percentile latency |             prod-queries |      90.543 |     ms |
|                                   50th percentile service time |             prod-queries |     1.92377 |     ms |
|                                   90th percentile service time |             prod-queries |     2.63867 |     ms |
|                                   99th percentile service time |             prod-queries |      48.513 |     ms |
|                                  100th percentile service time |             prod-queries |      90.543 |     ms |
|                                                     error rate |             prod-queries |           0 |      % |
|                                                  Mean recall@k |             prod-queries |        0.96 |        |
|                                                  Mean recall@1 |             prod-queries |        0.98 |        |


------------------------------------
[INFO] ✅ SUCCESS (took 218 seconds)
------------------------------------
```

#### 使用乘積量化的 Faiss IVF（100 個搜尋查詢）

```
|                                                         Metric |                     Task |       Value |   Unit |
|---------------------------------------------------------------:|-------------------------:|------------:|-------:|
|                     Cumulative indexing time of primary shards |                          |     11.3862 |    min |
|             Min cumulative indexing time across primary shards |                          |      0.0003 |    min |
|          Median cumulative indexing time across primary shards |                          |     0.12735 |    min |
|             Max cumulative indexing time across primary shards |                          |     11.2586 |    min |
|            Cumulative indexing throttle time of primary shards |                          |           0 |    min |
|    Min cumulative indexing throttle time across primary shards |                          |           0 |    min |
| Median cumulative indexing throttle time across primary shards |                          |           0 |    min |
|    Max cumulative indexing throttle time across primary shards |                          |           0 |    min |
|                        Cumulative merge time of primary shards |                          |     1.50842 |    min |
|                       Cumulative merge count of primary shards |                          |          19 |        |
|                Min cumulative merge time across primary shards |                          |           0 |    min |
|             Median cumulative merge time across primary shards |                          | 0.000233333 |    min |
|                Max cumulative merge time across primary shards |                          |     1.50818 |    min |
|               Cumulative merge throttle time of primary shards |                          |     0.58095 |    min |
|       Min cumulative merge throttle time across primary shards |                          |           0 |    min |
|    Median cumulative merge throttle time across primary shards |                          |           0 |    min |
|       Max cumulative merge throttle time across primary shards |                          |     0.58095 |    min |
|                      Cumulative refresh time of primary shards |                          |      0.2059 |    min |
|                     Cumulative refresh count of primary shards |                          |          61 |        |
|              Min cumulative refresh time across primary shards |                          |  0.00238333 |    min |
|           Median cumulative refresh time across primary shards |                          |  0.00526667 |    min |
|              Max cumulative refresh time across primary shards |                          |     0.19825 |    min |
|                        Cumulative flush time of primary shards |                          |   0.0254667 |    min |
|                       Cumulative flush count of primary shards |                          |          10 |        |
|                Min cumulative flush time across primary shards |                          |           0 |    min |
|             Median cumulative flush time across primary shards |                          |   0.0118333 |    min |
|                Max cumulative flush time across primary shards |                          |   0.0136333 |    min |
|                                        Total Young Gen GC time |                          |       6.477 |      s |
|                                       Total Young Gen GC count |                          |        3565 |        |
|                                          Total Old Gen GC time |                          |           0 |      s |
|                                         Total Old Gen GC count |                          |           0 |        |
|                                                     Store size |                          |    0.892541 |     GB |
|                                                  Translog size |                          |   0.0304573 |     GB |
|                                         Heap used for segments |                          |           0 |     MB |
|                                       Heap used for doc values |                          |           0 |     MB |
|                                            Heap used for terms |                          |           0 |     MB |
|                                            Heap used for norms |                          |           0 |     MB |
|                                           Heap used for points |                          |           0 |     MB |
|                                    Heap used for stored fields |                          |           0 |     MB |
|                                                  Segment count |                          |          21 |        |
|                                                 Min Throughput | custom-vector-bulk-train |       31931 | docs/s |
|                                                Mean Throughput | custom-vector-bulk-train |       31931 | docs/s |
|                                              Median Throughput | custom-vector-bulk-train |       31931 | docs/s |
|                                                 Max Throughput | custom-vector-bulk-train |       31931 | docs/s |
|                                        50th percentile latency | custom-vector-bulk-train |     25.3297 |     ms |
|                                        90th percentile latency | custom-vector-bulk-train |     35.3864 |     ms |
|                                        99th percentile latency | custom-vector-bulk-train |     144.372 |     ms |
|                                       100th percentile latency | custom-vector-bulk-train |      209.37 |     ms |
|                                   50th percentile service time | custom-vector-bulk-train |     25.3226 |     ms |
|                                   90th percentile service time | custom-vector-bulk-train |     35.3864 |     ms |
|                                   99th percentile service time | custom-vector-bulk-train |     144.372 |     ms |
|                                  100th percentile service time | custom-vector-bulk-train |      209.37 |     ms |
|                                                     error rate | custom-vector-bulk-train |           0 |      % |
|                                                 Min Throughput |             delete-model |        8.65 |  ops/s |
|                                                Mean Throughput |             delete-model |        8.65 |  ops/s |
|                                              Median Throughput |             delete-model |        8.65 |  ops/s |
|                                                 Max Throughput |             delete-model |        8.65 |  ops/s |
|                                       100th percentile latency |             delete-model |     114.725 |     ms |
|                                  100th percentile service time |             delete-model |     114.725 |     ms |
|                                                     error rate |             delete-model |           0 |      % |
|                                                 Min Throughput |          train-knn-model |        0.03 |  ops/s |
|                                                Mean Throughput |          train-knn-model |        0.03 |  ops/s |
|                                              Median Throughput |          train-knn-model |        0.03 |  ops/s |
|                                                 Max Throughput |          train-knn-model |        0.03 |  ops/s |
|                                       100th percentile latency |          train-knn-model |     37222.2 |     ms |
|                                  100th percentile service time |          train-knn-model |     37222.2 |     ms |
|                                                     error rate |          train-knn-model |           0 |      % |
|                                                 Min Throughput |       custom-vector-bulk |     10669.3 | docs/s |
|                                                Mean Throughput |       custom-vector-bulk |     14468.6 | docs/s |
|                                              Median Throughput |       custom-vector-bulk |     12496.1 | docs/s |
|                                                 Max Throughput |       custom-vector-bulk |     35027.8 | docs/s |
|                                        50th percentile latency |       custom-vector-bulk |     74.2584 |     ms |
|                                        90th percentile latency |       custom-vector-bulk |     113.426 |     ms |
|                                        99th percentile latency |       custom-vector-bulk |     293.075 |     ms |
|                                      99.9th percentile latency |       custom-vector-bulk |     1774.41 |     ms |
|                                     99.99th percentile latency |       custom-vector-bulk |     1969.99 |     ms |
|                                       100th percentile latency |       custom-vector-bulk |     1971.29 |     ms |
|                                   50th percentile service time |       custom-vector-bulk |     74.2577 |     ms |
|                                   90th percentile service time |       custom-vector-bulk |     113.477 |     ms |
|                                   99th percentile service time |       custom-vector-bulk |     292.481 |     ms |
|                                 99.9th percentile service time |       custom-vector-bulk |     1774.41 |     ms |
|                                99.99th percentile service time |       custom-vector-bulk |     1969.99 |     ms |
|                                  100th percentile service time |       custom-vector-bulk |     1971.29 |     ms |
|                                                     error rate |       custom-vector-bulk |           0 |      % |
|                                                 Min Throughput |     force-merge-segments |        0.05 |  ops/s |
|                                                Mean Throughput |     force-merge-segments |        0.05 |  ops/s |
|                                              Median Throughput |     force-merge-segments |        0.05 |  ops/s |
|                                                 Max Throughput |     force-merge-segments |        0.05 |  ops/s |
|                                       100th percentile latency |     force-merge-segments |     20015.2 |     ms |
|                                  100th percentile service time |     force-merge-segments |     20015.2 |     ms |
|                                                     error rate |     force-merge-segments |           0 |      % |
|                                                 Min Throughput |           warmup-indices |       47.06 |  ops/s |
|                                                Mean Throughput |           warmup-indices |       47.06 |  ops/s |
|                                              Median Throughput |           warmup-indices |       47.06 |  ops/s |
|                                                 Max Throughput |           warmup-indices |       47.06 |  ops/s |
|                                       100th percentile latency |           warmup-indices |     20.6798 |     ms |
|                                  100th percentile service time |           warmup-indices |     20.6798 |     ms |
|                                                     error rate |           warmup-indices |           0 |      % |
|                                                 Min Throughput |             prod-queries |       87.76 |  ops/s |
|                                                Mean Throughput |             prod-queries |       87.76 |  ops/s |
|                                              Median Throughput |             prod-queries |       87.76 |  ops/s |
|                                                 Max Throughput |             prod-queries |       87.76 |  ops/s |
|                                        50th percentile latency |             prod-queries |     1.81677 |     ms |
|                                        90th percentile latency |             prod-queries |     2.80454 |     ms |
|                                        99th percentile latency |             prod-queries |     51.2039 |     ms |
|                                       100th percentile latency |             prod-queries |     98.2032 |     ms |
|                                   50th percentile service time |             prod-queries |     1.81677 |     ms |
|                                   90th percentile service time |             prod-queries |     2.80454 |     ms |
|                                   99th percentile service time |             prod-queries |     51.2039 |     ms |
|                                  100th percentile service time |             prod-queries |     98.2032 |     ms |
|                                                     error rate |             prod-queries |           0 |      % |
|                                                  Mean recall@k |             prod-queries |        0.62 |        |
|                                                  Mean recall@1 |             prod-queries |        0.52 |        |

------------------------------------
[INFO] ✅ SUCCESS (took 413 seconds)
------------------------------------
```
