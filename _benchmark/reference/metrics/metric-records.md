---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指標記錄"
nav_order: 30
parent: Metrics reference
grand_parent: Reference
redirect_from:
  - /benchmark/metrics/metric-records/
---

# 指標記錄

OpenSearch Benchmark 會將指標儲存在 `benchmark-metrics-*` 索引中。每個月都會建立一個新索引。以下是儲存在 `benchmark-metrics-2023-08` 索引中的指標記錄範例：

```json
{
  "_index": "benchmark-metrics-2023-08",
  "_id": "UiNY4YkBpMtdJ7uj2rUe",
  "_version": 1,
  "_score": null,
  "_source": {
    "@timestamp": 1691702842821,
    "relative-time-ms": 65.90720731765032,
    "test-execution-id": "8c43ee4c-cb34-494b-81b2-181be244f832",
    "test-execution-timestamp": "20230810T212711Z",
    "environment": "local",
    "workload": "geonames",
    "test_procedure": "append-no-conflicts",
    "cluster-config-instance": "external",
    "name": "service_time",
    "value": 607.8001195564866,
    "unit": "ms",
    "sample-type": "normal",
    "meta": {
      "source_revision": "unknown",
      "distribution_version": "1.1.0",
      "distribution_flavor": "oss",
      "index": "geonames",
      "took": 13,
      "success": true,
      "success-count": 125,
      "error-count": 0
    },
    "task": "index-append",
    "operation": "index-append",
    "operation-type": "bulk"
  },
  "fields": {
    "@timestamp": [
      "2023-08-10T21:27:22.821Z"
    ],
    "test-execution-timestamp": [
      "2023-08-10T21:27:11.000Z"
    ]
  },
  "highlight": {
    "workload": [
      "@opensearch-dashboards-highlighted-field@geonames@/opensearch-dashboards-highlighted-field@"
    ],
    "meta.index": [
      "@opensearch-dashboards-highlighted-field@geonames@/opensearch-dashboards-highlighted-field@"
    ]
  },
  "sort": [
    1691702831000
  ]
}
```

指標記錄的 `_source` 區段中的下列欄位，可以在 `opensearch-benchmarks-metrics-*` 檔案中設定。

<!-- vale off -->
## @timestamp
<!-- vale on -->

取樣時間的時間戳記，以自 epoch 起算的毫秒數表示。對於與請求相關的指標，例如 `latency` 或 `service_time`，此值為 OpenSearch Benchmark 發出請求時的時間戳記。

<!-- vale off -->
## relative-time-ms
<!-- vale on -->

自基準測試開始以來的相對時間，以毫秒為單位。這對於比較多個測試的時間序列圖表很有用。例如，您可以比較多個測試中索引處理量隨時間的變化。

<!-- vale off -->
## test-execution-id
<!-- vale on -->

每次叫用工作負載時都會變更的 UUID，用於將同一次基準測試執行的所有樣本分組。

<!-- vale off -->
## test-execution-timestamp
<!-- vale on -->

叫用工作負載時的時間戳記（一律為 UTC）。

<!-- vale off -->
## environment
<!-- vale on -->

`environment` 描述指標記錄的來源。此值是在初次[設定]({{site.url}}{{site.baseurl}}/benchmark/configuring-benchmark/) OpenSearch Benchmark 時定義的。您可以為不同的基準測試使用不同的環境，但將指標記錄儲存在同一個索引中。

<!-- vale off -->
## workload, test_procedure, cluster-config-instance
<!-- vale on -->

產生這些指標的工作負載、測試程序和組態執行個體。

<!-- vale off -->
## name, value, unit
<!-- vale on -->

實際的指標名稱和值，以及選用的單位。根據指標的性質，指標可能由 OpenSearch Benchmark 定期取樣（例如 CPU 使用率或查詢延遲），也可能只測量一次（例如索引的最終大小）。

<!-- vale off -->
## sample-type
<!-- vale on -->

透過將其設定為 `warmup` 或 `normal`，決定是否將基準測試設定為以暖機模式執行。只有 `normal` 樣本會納入所報告的結果中。

<!-- vale off -->
## meta
<!-- vale on -->

每筆指標記錄的中繼資訊，包括下列項目：

- CPU 資訊：實體核心與邏輯核心的數量，以及型號名稱。
- 作業系統資訊：作業系統的名稱和版本。
- 主機名稱。
- 節點名稱：OpenSearch Benchmark 佈建叢集時，為每個節點指定的唯一名稱。
- 原始碼修訂版本：進行基準測試的 OpenSearch 版本的 Git 雜湊值。
- 發行版本：進行基準測試的 OpenSearch 發行版本。
- 自訂標籤：您可以使用命令列旗標 `--user-tags` 定義自訂標籤。標籤會加上 `tag_` 前置詞，以避免意外與 OpenSearch Benchmark 內部標籤衝突。
- 作業特定資訊：作業的選用子結構。對於大量請求，這可能是文件數量；對於搜尋，則是命中數。

根據指標記錄的不同，部分中繼資訊可能會缺少。

## 後續步驟

- 如需有關如何存取 OpenSearch Benchmark 指標的詳細資訊，請參閱[指標]({{site.url}}{{site.baseurl}}/benchmark/metrics/index/)。
- 如需有關 OpenSearch Benchmark 中所儲存指標的詳細資訊，請參閱[指標鍵]({{site.url}}{{site.baseurl}}/benchmark/metrics/metric-keys/)。
