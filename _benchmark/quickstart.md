---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "快速入門"
nav_order: 5
---

# OpenSearch Benchmark 快速入門

本頁說明如何快速安裝 OpenSearch Benchmark，並執行您的第一個 OpenSearch Benchmark 工作負載。

## 先決條件

若要執行快速入門的步驟，您必須符合下列先決條件：

- 目前作用中的 OpenSearch 叢集。如需建立 OpenSearch 叢集的指示，請參閱[建立叢集]({{site.url}}{{site.baseurl}}/tuning-your-cluster/index/)。
- Git 2.3 或更新版本。
- Python 3.8 或更新版本

## 設定 OpenSearch 叢集

如果您還沒有作用中的 OpenSearch 叢集，可以啟動新的 OpenSearch 叢集來搭配 OpenSearch Benchmark 使用。

- 使用 **Docker Compose**。如需使用 Docker Compose 的指示，請參閱 [OpenSearch 快速入門]({{site.url}}{{site.baseurl}}/quickstart/)。
- 使用 **Tar**。如需使用 Tar 安裝 OpenSearch 的指示，請參閱[安裝 OpenSearch > Tarball]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/tar#step-1-download-and-unpack-opensearch)。

OpenSearch Benchmark 尚未在 Windows 版 OpenSearch 上測試過。
{: .note}

安裝之後，您可以前往 `localhost:9200` 來確認 OpenSearch 正在執行。如果您在啟用 Security 外掛程式的情況下執行叢集，OpenSearch 會預期使用使用者名稱「admin」和密碼「admin」的 SSL 連線。不過，由於 localhost 位址並非唯一的公開位址，沒有任何憑證授權單位會為它核發 SSL 憑證，因此必須使用 `-k` 選項停用憑證檢查。

使用下列命令來確認 OpenSearch 正在執行且已停用 SSL 憑證檢查：

```bash
curl -k -u admin:<custom-admin-password> https://localhost:9200			# the "-k" option skips SSL certificate checks

{
  "name" : "147ddae31bf8.opensearch.org",
  "cluster_name" : "opensearch",
  "cluster_uuid" : "n10q2RirTIuhEJCiKMkpzw",
  "version" : {
    "distribution" : "opensearch",
    "number" : "2.10.0",
    "build_type" : "tar",
    "build_hash" : "eee49cb340edc6c4d489bcd9324dda571fc8dc03",
    "build_date" : "2023-09-20T23:54:29.889267151Z",
    "build_snapshot" : false,
    "lucene_version" : "9.7.0",
    "minimum_wire_compatibility_version" : "7.10.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
```

叢集執行後，您現在可以安裝 OpenSearch Benchmark。

## 安裝 OpenSearch Benchmark

若要使用 Docker 安裝 OpenSearch Benchmark，請參閱[安裝 OpenSearch Benchmark > 使用 Docker 安裝]({{site.url}}{{site.baseurl}}/benchmark/user-guide/installing-benchmark/#installing-with-docker)。
{: .tip}

若要從 PyPi 安裝 OpenSearch Benchmark，請輸入下列 `pip` 命令：

```bash
pip3 install opensearch-benchmark
```
{% include copy.html %}

安裝完成後，輸入下列命令來確認 OpenSearch Benchmark 正在執行：

```bash
opensearch-benchmark --help
```

如果成功，OpenSearch 會傳回下列回應：

```bash
$ opensearch-benchmark --help
usage: opensearch-benchmark [-h] [--version] {run,list,info,create-workload,generate,compare,download,install,start,stop} ...

   ____                  _____                      __       ____                  __                         __
  / __ \____  ___  ____ / ___/___  ____ ___________/ /_     / __ )___  ____  _____/ /_  ____ ___  ____ ______/ /__
 / / / / __ \/ _ \/ __ \\__ \/ _ \/ __ `/ ___/ ___/ __ \   / __  / _ \/ __ \/ ___/ __ \/ __ `__ \/ __ `/ ___/ //_/
/ /_/ / /_/ /  __/ / / /__/ /  __/ /_/ / /  / /__/ / / /  / /_/ /  __/ / / / /__/ / / / / / / / / /_/ / /  / ,<
\____/ .___/\___/_/ /_/____/\___/\__,_/_/   \___/_/ /_/  /_____/\___/_/ /_/\___/_/ /_/_/ /_/ /_/\__,_/_/  /_/|_|
    /_/

 A benchmarking tool for OpenSearch

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

subcommands:
  {run,list,info,create-workload,generate,compare,download,install,start,stop}
    run        Run a benchmark
    list                List configuration options
    info                Show info about a workload
    create-workload     Create a Benchmark workload from existing data
    generate            Generate artifacts
    compare             Compare two test-runs
    download            Downloads an artifact
    install             Installs an OpenSearch node locally
    start               Starts an OpenSearch node locally
    stop                Stops an OpenSearch node locally

Find out more about Benchmark at https://opensearch.org/docs
```

## 執行您的第一個基準測試

您現在可以執行您的第一個基準測試。下列基準測試使用 [percolator](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/percolator) 工作負載。


### 了解工作負載命令旗標

基準測試使用 [`run`]({{site.url}}{{site.baseurl}}/benchmark/reference/commands/run/) 命令搭配下列命令旗標來執行：

如需其他 `run` 命令旗標，請參閱 [run]({{site.url}}{{site.baseurl}}/benchmark/reference/commands/run/) 參考。一些常用的選項為 `--workload-params`、`--exclude-tasks` 和 `--include-tasks`。
{: .tip}

* `--pipeline=benchmark-only` ：告知 OSB 使用者想要提供自己的 OpenSearch 叢集。
- `workload=percolator`：OpenSearch Benchmark 所使用的工作負載名稱。
* `--target-host="<OpenSearch Cluster Endpoint>"`：指出將接受基準測試的目標叢集或主機。請在此輸入您 OpenSearch 叢集的端點。
* `--client-options="basic_auth_user:'<Basic Auth Username>',basic_auth_password:'<Basic Auth Password>'"`：您 OpenSearch 叢集的使用者名稱和密碼。
* `--test-mode`：允許使用者在未執行完整時段的情況下執行工作負載。當此旗標存在時，Benchmark 會執行工作負載中每個工作的前一千次操作。這僅用於基本檢查---所產生的指標沒有意義。
* `--distribution-version`：指出 Benchmark 在佈建時將使用的 OpenSearch 版本。執行時，`run` 命令會在連線至 OpenSearch 叢集時解析正確的發行版本。

### 執行工作負載

若要使用 OpenSearch Benchmark 執行 [percolator](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/percolator) 工作負載，請使用下列 `run` 命令：

```bash
opensearch-benchmark run --pipeline=benchmark-only --workload=percolator --target-host=https://localhost:9200 --client-options=basic_auth_user:admin,basic_auth_password:admin,verify_certs:false --test-mode
```
{% include copy.html %}

當 `run` 命令執行時，`percolator` 工作負載中的所有工作和操作會依序執行。

### 驗證測試

OpenSearch Benchmark 測試執行後，請採取下列步驟來確認它已正確執行：

- 記下您打算對其執行基準測試的 OpenSearch 或 OpenSearch Dashboards 索引中的文件數目。
- 在 OpenSearch Benchmark 傳回的結果中，比較您特定工作負載的 `workload.json` 檔案，並確認文件計數與文件數目相符。例如，根據 [percolator](https://github.com/opensearch-project/opensearch-benchmark-workloads/blob/main/percolator/workload.json#L19) 的 `workload.json` 檔案，您應該會預期在叢集中看到 `2000000` 份文件。

### 瞭解結果

OpenSearch Benchmark 在基準測試完成後會傳回以下回應：

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

`percolator` 工作負載執行的每個工作都代表測試執行時所執行的特定 OpenSearch API 操作，例如 Bulk 或 Search。輸出摘要中的每個工作包含以下資訊：

* **輸送量：** 每秒成功的 OpenSearch 操作次數。
* **延遲：** Benchmark 傳送與接收請求和回應所花費的時間，包括等待時間。
* **服務時間：** Benchmark 傳送與接收請求和回應所花費的時間，不包括等待時間。
* **錯誤率：** 工作期間執行的操作中，未成功或傳回 200 錯誤碼的操作百分比。

如需更多關於摘要報告產生方式的詳細資訊，請參閱[摘要報告]({{site.url}}{{site.baseurl}}/benchmark/reference/summary-report/)。


## 在您自己的叢集上執行 OpenSearch Benchmark

現在您已熟悉如何在叢集上執行 OpenSearch Benchmark，您可以在自己的叢集上執行 OpenSearch Benchmark，使用相同的 `run` 命令，但替換下列設定：

  * 將 `https://localhost:9200` 替換為您的目標叢集端點。這可以是像 `https://search.mydomain.com` 的 URI，或 `HOST:PORT` 規格。
  * 如果叢集設定了基本驗證，請將命令列中的使用者名稱和密碼替換為適當的認證資訊。
  * 如果您未指定 `localhost` 作為目標叢集，請移除 `verify_certs:false` 指示詞。只有在未設定 SSL 憑證的叢集上才需要此指示詞。
  * 如果您使用 `HOST:PORT`規格並打算使用 SSL/TLS，請指定 `https://`，或將 `use_ssl:true` 指示詞新增至 `--client-options` 字串選項。
  * 移除 `--test-mode` 旗標，以執行完整的工作負載，而非縮減的測試。

您可以複製下列命令範本，在您自己的終端機中使用：

```bash
opensearch-benchmark run --pipeline=benchmark-only --workload=percolator --target-host=<OpenSearch Cluster Endpoint> --client-options=basic_auth_user:admin,basic_auth_password:admin
```
{% include copy.html %}

## 後續步驟

請參閱下列資源，以進一步瞭解 OpenSearch Benchmark：

- [使用者指南]({{site.url}}{{site.baseurl}}/benchmark/user-guide/index/)：深入瞭解 OpenSearch Benchmark 如何協助您追蹤叢集的效能。
- [教學]({{site.url}}{{site.baseurl}}/benchmark/tutorials/index/)：使用逐步指南，瞭解更進階的 Benchmarking 組態與功能。
