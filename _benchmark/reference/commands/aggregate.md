---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: aggregate
nav_order: 10
parent: Command reference
grand_parent: Reference
redirect_from:
  - /benchmark/commands/aggregate/
---

<!-- vale off -->
# aggregate 命令
<!-- vale on -->

`aggregate` 命令會將多次測試執行合併為單一彙總結果，讓您能以更精簡的方式進行並分析多次測試執行。彙總方法有兩種：

- [自動彙總](#auto-aggregation)
- [手動彙總](#manual-aggregation)

## 自動彙總

自動彙總方法會以單一命令執行多次基準測試迭代，並自動彙總結果。您可以搭配 `execute` 命令使用本節所列的旗標。

### 使用方式

下列範例會執行 `geonames` 工作負載兩次並彙總結果：

```bash
opensearch-benchmark execute --test-iterations=2 --aggregate=true --workload=geonames --target-hosts=127.0.0.1:9200
```
{% include copy-curl.html %}

### 自動彙總旗標

下列新旗標可用於自訂自動彙總方法：

- `--test-iterations`：指定執行工作負載的次數（預設為 `1`）。
- `--aggregate`：決定是否彙總多次測試執行的結果（預設為 `true`）。
- `--sleep-timer`：指定開始下一次測試執行前要暫停的秒數（預設為 `5`）。
- `--cancel-on-error`：設定此旗標後，若任一次測試迭代發生錯誤，便會停止執行測試（預設為 `false`）。

## 手動彙總

您可以使用 `aggregate` 命令手動彙總多次測試執行的結果。

### 使用方式

若要手動彙總多次測試執行，請指定您要彙總的 `test_run_ids`，如下列範例所示：

```bash
opensearch-benchmark aggregate --test-executions=<test_run_id1>,<test_run_id2>,...
```
{% include copy-curl.html %}

### 回應

OpenSearch Benchmark 會傳回下列回應：

```
   ____                  _____                      __       ____                  __                         __
  / __ \____  ___  ____ / ___/___  ____ ___________/ /_     / __ )___  ____  _____/ /_  ____ ___  ____ ______/ /__
 / / / / __ \/ _ \/ __ \\__ \/ _ \/ __ `/ ___/ ___/ __ \   / __  / _ \/ __ \/ ___/ __ \/ __ `__ \/ __ `/ ___/ //_/
/ /_/ / /_/ /  __/ / / /__/ /  __/ /_/ / /  / /__/ / / /  / /_/ /  __/ / / / /__/ / / / / / / / / /_/ / /  / ,<
\____/ .___/\___/_/ /_/____/\___/\__,_/_/   \___/_/ /_/  /_____/\___/_/ /_/\___/_/ /_/_/ /_/ /_/\__,_/_/  /_/|_|
    /_/

Aggregate test run ID:  aggregate_results_geonames_9aafcfb8-d3b7-4583-864e-4598b5886c4f

----------------------------------
[INFO] ✅ SUCCESS (took 1 seconds)
----------------------------------
```

結果會彙總為單一測試執行，並以輸出中顯示的 ID 儲存。

### 其他選項
- `--test-execution-id`：為彙總後的測試執行定義唯一 ID。
- `--results-file`：將彙總結果寫入所提供的檔案。
- `--workload-repository`：定義 OpenSearch Benchmark 載入工作負載的儲存庫（預設為 `default`）。

## 彙總結果

彙總結果包含下列資訊：

- **相對標準差 (RSD)**：每個指標都會額外提供一個 `mean_rsd` 值，顯示各次測試執行結果的離散程度。
- **整體最小值／最大值**：彙總結果不會將最小值與最大值取平均，而是包含 `overall_min` 與 `overall_max`，反映所有測試執行中真正的最小值／最大值。
- **儲存空間**：彙總後的測試結果會儲存在獨立的 `aggregated_results` 資料夾中，與 `test-runs` 資料夾並列。

下列範例顯示彙總結果：

```json
    "throughput": {
     "overall_min": 29056.890292903263,
     "mean": 50115.8603858536,
     "median": 50099.54349684457,
     "overall_max": 72255.15946248993,
     "unit": "docs/s",
     "mean_rsd": 59.426059705973664
    },
```
