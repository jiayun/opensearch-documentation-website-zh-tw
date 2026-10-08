---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: run
nav_order: 90
parent: Command reference
grand_parent: Reference
redirect_from:
  - /benchmark/commands/execute-test/
  - /benchmark/reference/commands/execute-test/
---

<!-- vale off -->
# run 命令
<!-- vale on -->

無論您是使用內建的 [OpenSearch Benchmark 工作負載](https://github.com/opensearch-project/opensearch-benchmark-workloads)或[自訂工作負載]({{site.url}}{{site.baseurl}}/benchmark/creating-custom-workloads/)，都可以使用 `run` 命令，根據所選的工作負載收集 OpenSearch 叢集的效能資料。

## 用法

下列範例以測試模式使用 `geonames` 工作負載執行測試：

```
opensearch-benchmark run --workload=geonames --test-mode
```

測試執行完成後，OpenSearch Benchmark 會回應基準測試指標的摘要：

```
------------------------------------------------------
    _______             __   _____
   / ____(_)___  ____ _/ /  / ___/_________  ________
  / /_  / / __ \/ __ `/ /   \__ \/ ___/ __ \/ ___/ _ \
 / __/ / / / / / /_/ / /   ___/ / /__/ /_/ / /  /  __/
/_/   /_/_/ /_/\__,_/_/   /____/\___/\____/_/   \___/
------------------------------------------------------

|                         Metric |                 Task |     Value |   Unit |
|-------------------------------:|---------------------:|----------:|-------:|
|            Total indexing time |                      |   28.0997 |    min |
|               Total merge time |                      |   6.84378 |    min |
|             Total refresh time |                      |   3.06045 |    min |
|               Total flush time |                      |  0.106517 |    min |
|      Total merge throttle time |                      |   1.28193 |    min |
|               Median CPU usage |                      |     471.6 |      % |
|             Total Young Gen GC |                      |    16.237 |      s |
|               Total Old Gen GC |                      |     1.796 |      s |
|                     Index size |                      |   2.60124 |     GB |
|                  Total written |                      |   11.8144 |     GB |
|         Heap used for segments |                      |   14.7326 |     MB |
|       Heap used for doc values |                      |  0.115917 |     MB |
|            Heap used for terms |                      |   13.3203 |     MB |
|            Heap used for norms |                      | 0.0734253 |     MB |
|           Heap used for points |                      |    0.5793 |     MB |
|    Heap used for stored fields |                      |  0.643608 |     MB |
|                  Segment count |                      |        97 |        |
|                 Min Throughput |         index-append |   31925.2 | docs/s |
|              Median Throughput |         index-append |   39137.5 | docs/s |
|                 Max Throughput |         index-append |   39633.6 | docs/s |
|      50.0th percentile latency |         index-append |   872.513 |     ms |
|      90.0th percentile latency |         index-append |   1457.13 |     ms |
|      99.0th percentile latency |         index-append |   1874.89 |     ms |
|       100th percentile latency |         index-append |   2711.71 |     ms |
| 50.0th percentile service time |         index-append |   872.513 |     ms |
| 90.0th percentile service time |         index-append |   1457.13 |     ms |
| 99.0th percentile service time |         index-append |   1874.89 |     ms |
|  100th percentile service time |         index-append |   2711.71 |     ms |
|                           ...  |                  ... |       ... |    ... |
|                           ...  |                  ... |       ... |    ... |
|                 Min Throughput |     painless_dynamic |   2.53292 |  ops/s |
|              Median Throughput |     painless_dynamic |   2.53813 |  ops/s |
|                 Max Throughput |     painless_dynamic |   2.54401 |  ops/s |
|      50.0th percentile latency |     painless_dynamic |    172208 |     ms |
|      90.0th percentile latency |     painless_dynamic |    310401 |     ms |
|      99.0th percentile latency |     painless_dynamic |    341341 |     ms |
|      99.9th percentile latency |     painless_dynamic |    344404 |     ms |
|       100th percentile latency |     painless_dynamic |    344754 |     ms |
| 50.0th percentile service time |     painless_dynamic |    393.02 |     ms |
| 90.0th percentile service time |     painless_dynamic |   407.579 |     ms |
| 99.0th percentile service time |     painless_dynamic |   430.806 |     ms |
| 99.9th percentile service time |     painless_dynamic |   457.352 |     ms |
|  100th percentile service time |     painless_dynamic |   459.474 |     ms |

-------------------------------------
[INFO] ✅ SUCCESS (took 2634 seconds)
-------------------------------------
```

## 選項

請使用下列選項，依您的使用情境自訂 `run` 命令。本節的選項依使用情境分類。

## 一般設定

下列選項會影響每個測試的執行方式以及結果的呈現方式：

- `--test-mode`：以測試模式執行指定的工作負載，適合用於檢查工作負載是否有錯誤。
- `--user-tag`：定義要在指標記錄中作為中繼資訊的使用者專屬鍵值對，例如 `intention:baseline-ticket-12345`。
- `--results-format`：定義命令列結果的輸出格式，可為 `markdown` 或 `csv`。預設為 `markdown`。
- `--results-number-align`：定義 `compare` 命令輸出結果時的欄位數字對齊方式。預設為 `right`。
- `--results-file`：提供檔案路徑時，將比較結果寫入該路徑所指的檔案。
- `--show-in-results`：決定是否在結果檔案中包含比較內容。


### 發行版本

下列選項設定基準測試所使用的 OpenSearch 版本及 OpenSearch 外掛程式：

- `--distribution-version`：根據版本號下載指定的 OpenSearch 發行版本。如需已發布的 OpenSearch 版本清單，請參閱 [Version history]({{site.url}}{{site.latesturl}}/version-history/)。
- `--distribution-repository`：定義下載 OpenSearch 發行版本的儲存庫。預設為 `release`。
- `--revision`：定義執行基準測試時要使用的目前原始碼修訂版本。預設為 `current`。
   - `current`：使用原始碼樹中根據您 OpenSearch 發行版本所決定的目前修訂版本。
   - `latest`：從原始碼樹的 main 分支擷取最新修訂版本。
   - 您也可以使用原始碼樹的時間戳記或 commit ID。使用時間戳記時，請指定 `@ts`，其中 "ts" 是有效的 ISO 8601 時間戳記，例如 `@2013-07-27T10:37:00Z`。
-  `--opensearch-plugins`：定義要安裝哪些 [OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。預設不安裝任何外掛程式。
- `--plugin-params:` 定義以逗號分隔的 key:value 配對清單，這些配對會原封不動地以變數形式注入所有外掛程式。
- `--runtime-jdk`：要使用的 JDK 主要版本。
- `--client-options`：定義以逗號分隔的用戶端清單。所有選項都會傳遞給 OpenSearch Python 用戶端。預設為 `timeout:60`。

### 叢集

下列選項與基準測試的目標叢集有關。

- `--target-hosts`：定義以逗號分隔的主機-連接埠配對清單，在使用管線 `benchmark-only` 時應以這些配對為目標。預設為 `localhost:9200`。


### 分散式工作負載產生

下列選項協助想要使用多部主機對基準測試叢集產生負載的使用者：

- `--worker-ips`：定義以逗號分隔、負責協調負載的主機清單。預設為 `localhost`。
- `--enable-worker-coordinator-profiling`：啟用對 OpenSearch Benchmark 工作協調器效能的分析。預設為 `false`。

### 佈建

下列選項協助自訂 OpenSearch Benchmark 佈建 OpenSearch 與工作負載的方式：

- `--cluster-config-repository`：定義 OpenSearch Benchmark 載入 `cluster-configs` 與 `cluster-config-instances` 的儲存庫。
- `--cluster-config-path`：定義 `--cluster-config-instance` 及任何要使用之 OpenSearch 外掛程式組態的路徑。
- `--cluster-config-revision`：定義 OpenSearch Benchmark 應使用之 `cluster-config` 中的特定 Git 修訂版本。
- `--cluster-config-instance`：定義要使用的 `--cluster-config-instance`。您可以使用命令 `opensearch-benchmark list cluster-config-instances` 查看可能的組態執行個體。
- `--cluster-config-instance-params`：以逗號分隔的鍵值對清單，會原封不動地以變數形式注入 `cluster-config-instance`。


### 工作負載

下列選項決定執行測試時使用哪個工作負載：

- `--workload-repository`：定義 OpenSearch Benchmark 載入工作負載的儲存庫。
- `--workload-path`：定義已下載或自訂工作負載的路徑。
- `--workload-revision`：定義 OpenSearch Benchmark 應使用之工作負載原始碼樹中的特定修訂版本。
- `--workload`：根據工作負載名稱定義要使用的工作負載。您可以使用 `opensearch-benchmark list workloads` 找到預先載入的工作負載清單。

### 測試程序

下列選項定義測試所使用的測試程序，以及程序中包含哪些作業：

- `--test-execution-id`：定義此次測試執行的唯一 ID。
定義每個工作負載要使用的測試程序。您可以在 `info` 命令中指定工作負載，例如 `opensearch-benchmark info --workload=<workload_name>`，以找出該工作負載支援的測試程序清單。若要查詢特定測試程序的資訊，請使用命令 `opensearch-benchmark info --workload=<workload_name> --test-procedure=<test-procedure>`。
- `--include-tasks`：定義要執行的測試程序工作清單（以逗號分隔）。預設會執行測試程序陣列中列出的所有工作。
- `--exclude-tasks`：定義不要執行的測試程序工作清單（以逗號分隔）。
- `--enable-assertions`：為工作啟用斷言檢查。預設為 `false`。

### 管線

`--pipeline` 選項用於選擇要執行的管線。您可以執行 `opensearch-benchmark list pipelines` 找出 OpenSearch Benchmark 支援的管線清單。


### 遙測

下列選項可在 OpenSearch Benchmark 上啟用遙測裝置：

- `--telemetry`：當裝置以逗號分隔清單提供時，啟用這些遙測裝置。您可以使用 `opensearch-benchmark list telemetry` 找出可用的遙測裝置清單。
- `--telemetry-params`：定義以逗號分隔的鍵值對清單，這些配對會原封不動地以參數形式注入遙測裝置。


### 錯誤

下列選項設定 OpenSearch Benchmark 執行測試時處理錯誤的方式：

- `--on-error`：控制 OpenSearch Benchmark 對錯誤的回應方式。預設為 `continue`。
  - `continue`：即使發生錯誤仍繼續執行測試。
  - `abort`：發生錯誤時中止測試。
- `--preserve-install`：保留 Benchmark 候選及其索引。預設為 `false`。
- `--kill-running-processes`：設為 `true` 時，會停止目前正在執行的所有 OpenSearch Benchmark 處理程序，並允許 OpenSearch Benchmark 繼續執行。預設為 `false`。
