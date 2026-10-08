---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行工作負載"
nav_order: 30
redirect_from:
  - /benchmark/user-guide/running-workloads/
  - /benchmark/user-guide/working-with-workloads/running-workloads/
  - /benchmark/user-guide/working-with-workloads/
---

# 執行工作負載

當您完整了解 OpenSearch Benchmark [工作負載]({{site.url}}{{site.baseurl}}/benchmark/anatomy-of-a-workload/)的各個元件之後，就可以執行您的第一個工作負載。

## 步驟 1：找出工作負載名稱

若要進一步了解 OpenSearch Benchmark 隨附的標準工作負載，請使用下列命令：

```
opensearch-benchmark list workloads
```
{% include copy.html %}

畫面會顯示 OpenSearch Benchmark 支援的所有工作負載清單。請檢視該清單，並選取與您叢集使用案例最相似的工作負載。

## 步驟 2：執行測試

選取工作負載後，您可以使用 `opensearch-benchmark run` 命令來叫用該工作負載。將 `--target-host` 替換為您叢集的 `host:port` 組合，並將 `--client-options` 替換為存取叢集所需的任何授權選項。下列範例會在本機主機上執行 `nyc_taxis` 工作負載以進行測試。

如果您想在外部叢集上執行測試，請參閱[在您自己的叢集上執行工作負載](#running-a-workload-on-an-external-cluster)。

```bash
opensearch-benchmark run --pipeline=benchmark-only --workload=nyc_taxis --target-host=https://localhost:9200 --client-options=basic_auth_user:admin,basic_auth_password:admin,verify_certs:false
```
{% include copy.html %}


測試結果會顯示在 `run` 命令中由 `--output-path` 選項所設定的目錄內。

### 測試模式

如果您想以測試模式執行測試，以確保工作負載如預期運作，請在 `run` 命令中加入 `--test-mode` 選項。測試模式只會匯入每個所提供索引的前 1,000 份文件，並針對這些文件執行查詢作業。

### 使用 `--workload-params`

您可以使用 `--workload-params` 選項傳遞工作負載專屬參數，以自訂工作負載的行為。此旗標接受以逗號分隔的鍵值對清單，用來覆寫工作負載 `workload.json` 檔案中定義的預設值。

例如，某些工作負載可讓您設定要編製索引的文件數量、用於執行查詢的用戶端數量，或索引名稱。這些參數對於依據您的特定使用案例或基礎架構限制來調整基準測試可能非常關鍵。

若要傳遞工作負載參數，請使用下列語法：

```bash
--workload-params="number_of_documents:100000,index_name:custom-index"
```

將此選項加入您的 `run` 命令，如下列範例所示：

```bash
opensearch-benchmark run \
--pipeline=benchmark-only \
--workload=nyc_taxis \
--target-host=https://localhost:9200 \
--client-options=basic_auth_user:admin,basic_auth_password:admin,verify_certs:false \
--workload-params="bulk_size:500,index_name:nyc_custom"
```

可用的工作負載參數可在 [OpenSearch Benchmark Workloads GitHub 儲存庫](https://github.com/opensearch-project/opensearch-benchmark-workloads)中每個工作負載的 `README` 內找到。
{: .tip}




## 步驟 3：驗證測試

執行 OpenSearch Benchmark 測試之後，請採取下列步驟來確認測試已正確執行：

1. 記下您打算執行基準測試的 OpenSearch 或 OpenSearch Dashboards 索引中的文件數量。
2. 在 OpenSearch Benchmark 傳回的結果中，比較您特定工作負載的 `workload.json` 檔案，並確認文件數量相符。例如，根據 [nyc_taxis](https://github.com/opensearch-project/opensearch-benchmark-workloads/blob/main/nyc_taxis/workload.json#L20) 的 `workload.json` 檔案，您的叢集中應該會有 `165346692` 份文件。

## 預期結果

基準測試完成後，OSB 會傳回下列回應：

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
|            Cumulative indexing throttle time of primary shards |                                            |           0 |    min |
|    Min cumulative indexing throttle time across primary shards |                                            |           0 |    min |
| Median cumulative indexing throttle time across primary shards |                                            |           0 |    min |
|    Max cumulative indexing throttle time across primary shards |                                            |           0 |    min |
|                        Cumulative merge time of primary shards |                                            |   0.0102333 |    min |
|                       Cumulative merge count of primary shards |                                            |           3 |        |
|                Min cumulative merge time across primary shards |                                            |           0 |    min |
|             Median cumulative merge time across primary shards |                                            |           0 |    min |
|                Max cumulative merge time across primary shards |                                            |   0.0102333 |    min |
|               Cumulative merge throttle time of primary shards |                                            |           0 |    min |
|       Min cumulative merge throttle time across primary shards |                                            |           0 |    min |
|    Median cumulative merge throttle time across primary shards |                                            |           0 |    min |
|       Max cumulative merge throttle time across primary shards |                                            |           0 |    min |
|                      Cumulative refresh time of primary shards |                                            |   0.0709333 |    min |
|                     Cumulative refresh count of primary shards |                                            |         118 |        |
|              Min cumulative refresh time across primary shards |                                            |           0 |    min |
|           Median cumulative refresh time across primary shards |                                            |  0.00186667 |    min |
|              Max cumulative refresh time across primary shards |                                            |   0.0511667 |    min |
|                        Cumulative flush time of primary shards |                                            |  0.00963333 |    min |
|                       Cumulative flush count of primary shards |                                            |           4 |        |
|                Min cumulative flush time across primary shards |                                            |           0 |    min |
|             Median cumulative flush time across primary shards |                                            |           0 |    min |
|                Max cumulative flush time across primary shards |                                            |  0.00398333 |    min |
|                                        Total Young Gen GC time |                                            |           0 |      s |
|                                       Total Young Gen GC count |                                            |           0 |        |
|                                          Total Old Gen GC time |                                            |           0 |      s |
|                                         Total Old Gen GC count |                                            |           0 |        |
|                                                     Store size |                                            | 0.000485923 |     GB |
|                                                  Translog size |                                            | 2.01873e-05 |     GB |
|                                         Heap used for segments |                                            |           0 |     MB |
|                                       Heap used for doc values |                                            |           0 |     MB |
|                                            Heap used for terms |                                            |           0 |     MB |
|                                            Heap used for norms |                                            |           0 |     MB |
|                                           Heap used for points |                                            |           0 |     MB |
|                                    Heap used for stored fields |                                            |           0 |     MB |
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
|                                                 Min Throughput |                   wait-until-merges-finish |       28.41 |  ops/s |
|                                                Mean Throughput |                   wait-until-merges-finish |       28.41 |  ops/s |
|                                              Median Throughput |                   wait-until-merges-finish |       28.41 |  ops/s |
|                                                 Max Throughput |                   wait-until-merges-finish |       28.41 |  ops/s |
|                                       100th percentile latency |                   wait-until-merges-finish |     34.7088 |     ms |
|                                  100th percentile service time |                   wait-until-merges-finish |     34.7088 |     ms |
|                                                     error rate |                   wait-until-merges-finish |           0 |      % |
|                                                 Min Throughput |     percolator_with_content_president_bush |       36.09 |  ops/s |
|                                                Mean Throughput |     percolator_with_content_president_bush |       36.09 |  ops/s |
|                                              Median Throughput |     percolator_with_content_president_bush |       36.09 |  ops/s |
|                                                 Max Throughput |     percolator_with_content_president_bush |       36.09 |  ops/s |
|                                       100th percentile latency |     percolator_with_content_president_bush |     35.9822 |     ms |
|                                  100th percentile service time |     percolator_with_content_president_bush |     7.93048 |     ms |
|                                                     error rate |     percolator_with_content_president_bush |           0 |      % |

[...]

|                                                 Min Throughput |          percolator_with_content_ignore_me |        16.1 |  ops/s |
|                                                Mean Throughput |          percolator_with_content_ignore_me |        16.1 |  ops/s |
|                                              Median Throughput |          percolator_with_content_ignore_me |        16.1 |  ops/s |
|                                                 Max Throughput |          percolator_with_content_ignore_me |        16.1 |  ops/s |
|                                       100th percentile latency |          percolator_with_content_ignore_me |     131.798 |     ms |
|                                  100th percentile service time |          percolator_with_content_ignore_me |     69.5237 |     ms |
|                                                     error rate |          percolator_with_content_ignore_me |           0 |      % |
|                                                 Min Throughput | percolator_no_score_with_content_ignore_me |       29.37 |  ops/s |
|                                                Mean Throughput | percolator_no_score_with_content_ignore_me |       29.37 |  ops/s |
|                                              Median Throughput | percolator_no_score_with_content_ignore_me |       29.37 |  ops/s |
|                                                 Max Throughput | percolator_no_score_with_content_ignore_me |       29.37 |  ops/s |
|                                       100th percentile latency | percolator_no_score_with_content_ignore_me |     45.5703 |     ms |
|                                  100th percentile service time | percolator_no_score_with_content_ignore_me |      11.316 |     ms |
|                                                     error rate | percolator_no_score_with_content_ignore_me |           0 |      % |



-----------------------------------
[INFO] ✅ SUCCESS (took 18 seconds)
-----------------------------------
```



## 在外部叢集上執行工作負載

既然您已熟悉如何在本機叢集上執行 OpenSearch Benchmark，接下來可以依照下列步驟，在您的外部叢集上執行：

1. 將 `https://localhost:9200` 取代為您的目標叢集端點。這可以是統一資源識別碼 (URI)，例如 `https://search.mydomain.com`，或是 `HOST:PORT` 規格。
2. 如果叢集已設定基本驗證，請將命令列中的使用者名稱和密碼取代為適當的認證資訊。
3. 如果您並未將 `localhost` 指定為目標叢集，請移除 `verify_certs:false` 指示詞。此指示詞僅適用於沒有 SSL 憑證的叢集。
4. 如果您使用 `HOST:PORT` 規格並打算使用 SSL 或 TLS，請指定 `https://`，或將 `use_ssl:true` 指示詞新增至 `--client-options` 字串選項。
5. 移除 `--test-mode` 旗標，以執行完整的工作負載，而非簡化版測試。

您可以複製下列命令範本，在您自己的終端機中使用：

```bash
opensearch-benchmark run --pipeline=benchmark-only --workload=nyc_taxis --target-host=<OpenSearch Cluster Endpoint> --client-options=basic_auth_user:admin,basic_auth_password:admin
```
{% include copy.html %}
