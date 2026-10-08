---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "命令旗標"
nav_order: 150
parent: Command reference
redirect_from:
  - /benchmark/commands/command-flags/
grand_parent: Reference
---

# 命令旗標
OpenSearch Benchmark 使用命令列旗標來變更 Benchmark 的行為。並非所有旗標都能搭配每個命令使用。若要了解特定命令支援哪些旗標，請輸入 `opensearch-benchmark <command> --h`。

所有命令旗標都使用下列語法加入命令中：

```bash
opensearch-benchmark <command> --<command-flag>
```

接受以逗號分隔值的旗標（例如 `--telemetry`）也可以接受 JSON 陣列。您可以傳入以 `.json` 結尾的檔案路徑，或以內嵌 JSON 字串的方式來定義。

- 以逗號分隔的值：`opensearch-benchmark ... --test-procedure="ingest-only,search-aggregations"`
- JSON 檔案：`opensearch-benchmark ... --workload-params="params.json"`
- 內嵌 JSON 字串：`opensearch-benchmark  ... --telemetry='["node-stats", "recovery-stats"]'`

<!-- vale off -->
## workload-path
<!-- vale on -->

這可以是包含 `workload.json` 檔案的目錄，或是名稱任意且包含工作負載規格的 `.json` 檔案。`--workload-path`、`--workload-repository` 以及 `--workload` 彼此互斥。

<!-- vale off -->
## workload-repositor
<!-- vale on -->

定義 OpenSearch Benchmark 載入工作負載的來源儲存庫。`--workload-path`、`--workload-repository` 以及 `--workload` 彼此互斥。

<!-- vale off -->
## workload-revision
<!-- vale on -->

定義 OpenSearch Benchmark 應使用的工作負載來源樹特定修訂版本。

<!-- vale off -->
## workload
<!-- vale on -->

依據工作負載的名稱定義要使用的工作負載。您可以使用 `opensearch-benchmark list workloads` 查看預先載入的工作負載清單。`--workload-path`、`--workload-repository` 以及 `--workload` 彼此互斥。

<!-- vale off -->
## workload-params
<!-- vale on -->

定義要注入工作負載的變數。注入的變數必須可在工作負載中使用。您可以將參數以 JSON 檔案、內嵌 JSON 或以逗號分隔的鍵值組傳入。如需詳細資訊（包括範本語法、優先順序以及各工作負載的常用參數），請參閱[工作負載參數]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/parameters/)。

<!-- vale off -->
## test-procedure
<!-- vale on -->

定義每個工作負載要使用的測試程序。您可以在 `info` 命令中指定工作負載，以查看該工作負載支援的測試程序清單，例如 `opensearch-benchmark info --workload=<workload_name>`。若要查詢特定測試程序的資訊，請使用命令 `opensearch-benchmark info --workload=<workload_name> --test-procedure=<test-procedure>`。

<!-- vale off -->
## test-execution-id
<!-- vale on -->

定義測試執行的唯一 ID。

<!-- vale off -->
## include-tasks
<!-- vale on -->

定義以逗號分隔的要執行測試程序任務清單。根據預設，會執行測試程序陣列中列出的所有任務。

任務會依照其在 `test-procedure` 中定義的順序執行，而非依照其在命令中定義的順序。

所有任務篩選條件都會區分大小寫。

<!-- vale off -->
## exclude-tasks
<!-- vale on -->

定義以逗號分隔的不執行測試程序任務清單。

<!-- vale off -->
## baseline
<!-- vale on -->

用來與競爭者 TestRun 比較的基準 TestRun ID。

<!-- vale off -->
## contender
<!-- vale on -->

要與基準進行比較的競爭者 TestRun ID。

<!-- vale off -->
## results-format
<!-- vale on -->

定義命令列結果的輸出格式，可為 `markdown` 或 `csv`。預設為 `markdown`。


<!-- vale off -->
## results-number-align
<!-- vale on -->

定義 `compare` 命令輸出結果時的欄位數字對齊方式。預設為 `right`。

<!-- vale off -->
## results-file
<!-- vale on -->

提供檔案路徑時，會將比較結果寫入路徑所指示的檔案。

<!-- vale off -->
## show-in-results
<!-- vale on -->

決定是否要在結果檔案中包含比較內容。

<!-- vale off -->
## cluster-config-repository
<!-- vale on -->

定義 OpenSearch Benchmark 載入 `cluster-configs` 和 `cluster-config-instances` 的來源儲存庫。

<!-- vale off -->
## cluster-config-revision
<!-- vale on -->

定義 OpenSearch Benchmark 應使用的 `cluster-config` 中特定 Git 修訂版本。

<!-- vale off -->
## cluster-config-path
<!-- vale on -->

定義要使用的 `--cluster-config-instance` 及任何 OpenSearch 外掛程式組態的路徑。

<!-- vale off -->
## distribution-version
<!-- vale on -->

根據版本號碼下載指定的 OpenSearch 發行版本。如需已發行的 OpenSearch 版本清單，請參閱[版本歷程記錄]({{site.url}}{{site.latesturl}}/version-history/)。

<!-- vale off -->
## distribution-repository
<!-- vale on -->

定義下載 OpenSearch 發行版本的來源儲存庫。預設為 `release`。

<!-- vale off -->
## cluster-config-instance
<!-- vale on -->

定義要使用的 `--cluster-config-instance`。您可以使用命令 `opensearch-benchmark list cluster-config-instances` 檢視可用的組態執行個體。

<!-- vale off -->
## cluster-config-instance-params
<!-- vale on -->

以逗號分隔的鍵值組清單，會以原樣作為變數注入 `cluster-config-instance`。

<!-- vale off -->
## target-hosts
<!-- vale on -->

定義使用管線 `benchmark-only` 時應作為目標、以逗號分隔的主機與連接埠組清單。預設為 `localhost:9200`。

<!-- vale off -->
## target-os
<!-- vale on -->

要下載 OpenSearch 成品的目標作業系統。預設為目前的作業系統。

<!-- vale off -->
## target-arch
<!-- vale on -->

要下載成品的 CPU 架構名稱。

<!-- vale off -->
## revision
<!-- vale on -->

定義執行基準測試時要使用的目前原始碼修訂版本。預設為 `current`。

此命令旗標可使用下列選項：

   - `current`：根據您的 OpenSearch 發行版本，使用來源樹的目前修訂版本。
   - `latest`：從來源樹的 main 分支擷取最新修訂版本。

您也可以使用來源樹中的時間戳記或 commit ID。使用時間戳記時，請指定 `@ts`，其中「ts」是有效的 ISO 8601 時間戳記，例如 `@2013-07-27T10:37:00Z`。

<!-- vale off -->
## opensearch-plugins
<!-- vale on -->

定義要安裝哪些 [OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。根據預設，不會安裝任何外掛程式。

<!-- vale off -->
## plugin-params
<!-- vale on -->

定義以逗號分隔的鍵值組清單，這些鍵值組會以原樣作為變數注入所有外掛程式。

<!-- vale off -->
## runtime-jdk
<!-- vale on -->

要使用的 JDK 主要版本。


<!-- vale off -->
## client-options
<!-- vale on -->

定義以逗號分隔的要使用用戶端清單。所有選項都會傳遞給 OpenSearch Python 用戶端。預設為 `timeout:60`。

<!-- vale off -->
## worker-ips
<!-- vale on -->

定義以逗號分隔的協調負載主機清單。預設為 `localhost`。

<!-- vale off -->
## enable-worker-coordinator-profiling
<!-- vale on -->

啟用 OpenSearch Benchmark 工作者協調器的效能分析。預設為 `false`。

<!-- vale off -->
## pipeline
<!-- vale on -->

`--pipeline` 選項會選取要執行的管線。您可以執行 `opensearch-benchmark list pipelines` 來查看 OpenSearch Benchmark 支援的管線清單。

<!-- vale off -->
## telemetry
<!-- vale on -->

以逗號分隔清單提供遙測裝置時，會啟用所提供的遙測裝置。您可以使用 `opensearch-benchmark list telemetry` 查看可用的遙測裝置清單。

<!-- vale off -->
## telemetry-params
<!-- vale on -->

可為遙測裝置設定參數。接受以逗號分隔的鍵值組清單（每組鍵值以冒號分隔），或 JSON 檔案名稱。

<!-- vale off -->
## on-error
<!-- vale on -->

控制 OpenSearch Benchmark 如何回應錯誤。預設為 `continue`。

您可以搭配此命令旗標使用下列選項：

- `continue`：即使發生錯誤仍繼續執行測試。
- `abort`：發生錯誤時中止測試。

<!-- vale off -->
## preserve-install
<!-- vale on -->

保留 Benchmark 候選項目及其索引。預設為 `false`。

<!-- vale off -->
## kill-running-processes
<!-- vale on -->

設為 `true` 時，會停止目前正在執行的所有 OpenSearch Benchmark 處理程序，並讓 Benchmark 繼續執行。預設為 `false`。

<!-- vale off -->
## chart-spec-path
<!-- vale on -->

設定包含圖表規格的 JSON 檔案路徑，這些規格可用來產生圖表。

<!-- vale off -->
## chart-type
<!-- vale on -->

產生指定的圖表類型，可為 `time-series` 或 `bar`。預設為 `time-series`。

<!-- vale off -->
## output-path
<!-- vale on -->

圖表輸出所使用的名稱與路徑。預設為 `stdout`。

<!-- vale off -->
## limit
<!-- vale on -->

限制近期測試執行的搜尋結果數量。預設為 `10`。

<!-- vale off -->
## latency-percentiles
<!-- vale on -->

指定以逗號分隔的延遲百分位數清單，在工作負載執行後回報。接受介於 `0` 與 `100` 之間（含）的 `ints` 或 `floats` 值。不接受 `min`、`median`、`mean` 或 `max`。預設為 `50,90,99,99.9,99.99,100`。

<!-- vale off -->
## throughput-percentiles
<!-- vale on -->

指定工作負載執行後要回報的輸送量百分位數清單。與 `--latency-percentiles` 相同，此設定接受介於 `0` 與 `100` 之間（含）的 `ints` 或 `floats` 值。不接受 `min`、`median`、`mean` 或 `max`。預設為 `None`。

<!-- vale off -->
## randomization-enabled
<!-- vale on -->

啟用 `range` 查詢中值的隨機化，這些值取自在工作負載 `workload.py` 檔案中以 `register_standard_value_source` 註冊的標準值函式。

標準值函式是不帶引數的函式，會為特定欄位產生一組隨機值，並以包含鍵 `"gte"`、`"lte"` 以及選用的 `"format"` 的 dict 傳回。

若此引數為 `True`，但某個搜尋作業沒有已註冊的標準值函式，OpenSearch Benchmark 會引發 `SystemSetupError`。預設為 `False`。


<!-- vale off -->
## randomization-repeat-frequency
<!-- vale on -->

設定隨機化查詢值中可重複的比例。接受介於 `0.0` 與 `1.0` 之間的值。預設為 `0.3`。未使用 `--randomization-enabled` 時，此設定不會生效。

<!-- vale off -->
## randomization-n
<!-- vale on -->

設定使用隨機化時，每個作業會產生多少組不同的可重複值組。預設為 `5000`。未使用 `--randomization-enabled` 時，此設定不會生效。

<!-- vale off -->
## test-iterations
<!-- vale on -->

指定執行工作負載的次數。預設為 `1`。

<!-- vale off -->
## aggregate
<!-- vale on -->

決定 OpenSearch Benchmark 是否應彙總多次測試執行的結果。

設為 `true` 時，OpenSearch Benchmark 會將所有反覆執行的結果合併成單一彙總報告。設為 `false` 時，會分別回報每次反覆執行的結果。

預設為 `true`。

<!-- vale off -->
## sleep-timer
<!-- vale on -->

指定開始下一次測試執行前要暫停的秒數。預設為 `5`。


<!-- vale off -->
## cancel-on-error
<!-- vale on -->

設定此旗標時，會指示 OpenSearch Benchmark 在任一次測試反覆執行發生錯誤時停止執行測試。預設為 `false`（未設定）。

