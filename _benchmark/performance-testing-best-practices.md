---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "效能測試最佳實務"
nav_order: 70
redirect_from:
  - /benchmark/user-guide/optimizing-benchmarks/performance-testing-best-practices/
  - /benchmark/user-guide/optimizing-benchmarks/
---

# 效能測試最佳實務

使用 OpenSearch Benchmark 進行效能測試時，務必遵循一些關鍵的最佳實務，以確保結果準確、可靠且有意義。這些實務有助於建立貼近實際情況的測試情境、將可能使結果失真的外部因素降至最低，並產生可比較且可重現的基準測試。遵循這些準則，您就能深入瞭解叢集的效能，包括找出瓶頸，以及在叢集組態與最佳化方面做出有根據的決策。

## 環境設定

效能測試需要仔細留意測試環境。正確設定環境對於取得可靠且可重現的結果至關重要。

設定測試環境時，務必使用與正式環境高度相近的硬體。使用開發用或效能不足的硬體，無法提供可反映正式環境效能的有意義結果。本機通常具有有限的硬體資源，且本機開發程式庫可能與工作負載的程式庫衝突，導致基準測試無法有效執行。

為取得最佳結果，請確保您的負載產生主機或執行 OpenSearch Benchmark 的機器符合最低硬體需求：

- CPU：8 核心以上
- RAM：32 GB 以上
- 儲存空間：固態硬碟（SSD）/NVMe
- 網路：10 Gbps


我們建議佈建測試叢集，並調整其設定，以反映您最可能在正式環境中部署的組態。


## 測試組態

正確的測試組態包括為測試情境設定適當的參數，以及確保叢集已完成最佳化設定。

### 基本設定

以下範例顯示基本的基準測試組態檔案。此組態包含暖機時間、測試持續時間及用戶端數量等必要參數：

```json
     {
      "name": "my-benchmark-test-procedure",
      "description": "This test procedure runs term query against a cluster. It includes a 300-second warm-up, followed by a 3600-second benchmark using 8 concurrent clients.",
      "schedule": [
        {
          "operation": "term",
          "warmup-time=period": 300,
          "time-period": 3600,
          "clients": 8
        }
      ]
    }
```
{% include copy.html %}

### 索引設定

您的 OpenSearch 索引設定應針對特定使用案例進行最佳化。請盡可能將每個索引的分片數量設定為與正式環境叢集相同。不過，如果您是開發人員，希望專注於單一分片的效能並限制影響效能的變數，請使用單一主要分片，如以下 `index_settings` 範例所示：

```json
{
  "index_settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "refresh_interval": "30s"
  }
}
```

這些設定為您的文件和測試結果提供充足的儲存空間，每個索引有 3 個分片和 1 個副本。


## 執行測試

執行基準測試時，需要在測試期間監控系統，並確保各次測試執行的條件一致。

除了執行基本測試，您也可以使用其他[基準測試命令選項]({{site.url}}{{site.baseurl}}/benchmark/reference/commands/index/)來自訂測試執行方式。以下範例執行以特定主機為目標的 `geonames` 工作負載測試，並將測試結果輸出為 `csv`，以便進一步分析基準測試的指標：

```bash
opensearch-benchmark run \
  --workload=geonames \
  --target-hosts=localhost:9200 \
  --pipeline=benchmark-only \
  --test-procedure=default \
  --report-format=csv \
  --report-file=benchmark-results.csv
```
{% include copy.html %}

### 測試期間的監控

測試執行期間，務必監控各種系統指標，以確保測試正常執行並找出任何潛在瓶頸。以下命令可協助您監控系統效能的不同面向：

```bash
# Monitor system resources
vmstat 1

# Monitor OpenSearch metrics
curl localhost:9200/_cat/nodes?v
curl localhost:9200/_cat/indices?v

# Monitor cluster health
curl localhost:9200/_cluster/health?pretty
```
{% include copy.html %}

## 收集指標

收集並儲存適當的指標，對於分析測試結果及做出有根據的效能最佳化決策相當重要。

### 必要指標

請設定基準測試以收集完整的指標。以下組態範例示範如何設定指標收集，並使用檔案儲存：

```json
{
  "metrics": {
    "store_metrics": true,
    "detailed": true,
    "metrics_store": {
      "type": "file",
      "location": "/path/to/metrics"
    }
  }
}
```
{% include copy.html %}

### 要追蹤的指標範例

以下 Python 結構可用作範本，其中包含效能測試期間應追蹤的指標清單：

```python
metrics_to_track = {
    'latency': {
        'mean': 'ms',
        'median': 'ms',
        'p95': 'ms',
        'p99': 'ms'
    },
    'throughput': {
        'ops/sec': 'count',
        'mb/sec': 'bytes'
    },
    'system': {
        'cpu_usage': '%',
        'memory_used': 'bytes',
        'disk_io': 'iops'
    }
}
```
{% include copy.html %}

### 計算指標

OpenSearch Benchmark 計算指標的方式與傳統用戶端與伺服器系統不同。如需指標計算方式的詳細資訊，請參閱 [OpenSearch Benchmark 與傳統用戶端與伺服器系統的差異]({{site.url}}{{site.baseurl}}/benchmark/user-guide/concepts/#differences-between-opensearch-benchmark-and-a-traditional-client-server-system)。

## 與 OpenSearch Dashboards 整合

若要將 OpenSearch Benchmark 結果與 OpenSearch Dashboards 整合，請使用下列步驟：

1. [設定 OpenSearch Benchmark]({{site.url}}{{site.baseurl}}/benchmark/user-guide/install-and-configure/configuring-benchmark/)，將結果儲存在 OpenSearch 中。
2. 在 OpenSearch Dashboards 中為基準測試結果建立索引模式。
3. 建立視覺化和儀表板，以分析基準測試資料。


## 常見陷阱

使用 OpenSearch Benchmark 進行效能測試時，請留意一些可能導致結果不準確或具有誤導性的常見陷阱。

### 暖機時間

適當的暖機對於準確的效能測試至關重要。如果沒有足夠的暖機時間，您的測試結果可能會受到系統初始不穩定狀態或快取效應的影響而失真。

請勿在沒有暖機時間的情況下執行測試。

請務必在測試中納入足夠的暖機時間。這可讓系統在開始測量之前達到穩定狀態。以下範例為一次 `geonames` 執行設定了 `300s` 的暖機時間：

```python
opensearch-benchmark run --workload=geonames --workload-params="warmup_time_period:300"
```

適當的暖機時間可能因您的特定工作負載和系統組態而異。請先設定至少 5 分鐘（300 秒），再根據觀察結果視需要調整。

### 比較不同環境的結果

效能測試中最常見的錯誤之一，是比較不同環境的結果。由於硬體、網路條件及其他環境因素不同，從筆記型電腦或開發用機器取得的結果，無法與正式環境伺服器的結果相比。

請確保所有比較都使用同一個環境或完全相同的環境。如果您需要比較不同的組態，請務必一次只變更一個變數，同時保持環境一致。

### 記錄測試環境

妥善記錄測試環境對於重現測試及準確分析至關重要。若缺乏詳細的環境資訊，日後將難以解讀結果或重現測試。

請勿在測試報告中省略環境詳細資訊。

請務必完整記錄測試環境的詳細資訊。這應包含硬體規格、軟體版本及任何相關組態設定。以下範例示範如何在使用 Python 指令碼執行 OpenSearch Benchmark 時加入環境詳細資訊：

```python
# DO: Document environment details
def run_benchmark():
    environment = {
        'hardware': 'AWS m5.2xlarge',
        'os': 'Ubuntu 20.04',
        'kernel': '5.4.0-1018-aws',
        'opensearch': '2.0.0',
        'java': 'OpenJDK 11.0.11',
        'benchmark_version': '1.0.0'
    }
    results = opensearch_benchmark.run()
    return {'environment': environment, 'results': results}
```
{% include copy.html %}

記錄這些詳細資訊，可確保您的測試結果能被正確解讀，並在必要時重現測試。

### 使用記錄檔進行疑難排解

遇到問題或非預期的結果時，OpenSearch Benchmark 記錄檔可提供有價值的線索。以下說明如何有效使用記錄檔進行疑難排解：

1. 前往記錄檔所在位置。主要記錄檔通常位於 `~/.osb/logs/benchmark.log`。

2. 尋找錯誤訊息。搜尋包含「ERROR」或「WARNING」的行，以找出潛在問題。

3. 檢查效能瓶頸。尋找指出作業緩慢或資源受限的項目。

4. 檢閱組態詳細資訊，例如記錄檔。記錄檔通常包含測試組態的資訊，有助於驗證您預期的設定是否已正確套用。

5. 留意基準測試各階段的持續時間，包括暖機和測量期間。

仔細檢閱這些記錄檔，通常能找出效能問題或非預期基準測試結果的根本原因。如果您遇到不熟悉的記錄檔錯誤，請在 [OpenSearch Benchmark 儲存庫](https://github.com/opensearch-project/opensearch-benchmark)中建立議題。

## 安全性考量

在多數情況下，基本驗證通訊協定應足以滿足測試需求。不過，您可以在基準測試期間使用 SSL 進行安全通訊，如以下 `opensearch.yml` 組態範例所示：

```yaml
security:
  ssl: true
  verification_mode: full
  certificate_authorities:
    - /path/to/ca.crt
  client_certificate: /path/to/client.crt
  client_key: /path/to/client.key
```
{% include copy.html %}

## 維護

定期維護基準測試環境和工具，是長期維持一致且可靠測試的必要措施。

請使用以下命令，讓您的基準測試工具和工作負載保持最新：

```bash
# Update OpenSearch Benchmark
pip install --upgrade opensearch-benchmark

# Update workloads
opensearch-benchmark update-workload geonames

# Clean old data
opensearch-benchmark clean
```
{% include copy.html %}

## Amazon OpenSearch Serverless 考量

使用 Amazon OpenSearch Serverless 進行測試時，請注意，並非所有測試程序都受到支援。請務必檢查您使用的[工作負載](https://github.com/opensearch-project/opensearch-benchmark-workloads)中的 `README.md` 檔案，以確認其是否與 OpenSearch Serverless 相容。如果未提供相容性資訊，您可能需要逐一測試這些程序，以判斷哪些程序受到支援。
