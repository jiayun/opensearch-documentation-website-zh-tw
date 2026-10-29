---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Performance Analyzer
parent: Telemetry
grand_parent: Monitoring your cluster
nav_order: 30
redirect_from:
  - /monitoring-plugins/pa/
  - /monitoring-plugins/pa/index/
  - /monitoring-your-cluster/pa/
  - /monitoring-your-cluster/pa/index/
  - /monitoring-plugins/pa/api/
  - /monitoring-your-cluster/pa/api/
  - /monitoring-plugins/pa/dashboards/
  - /monitoring-your-cluster/pa/dashboards/
  - /monitoring-plugins/pa/reference/
  - /monitoring-your-cluster/pa/reference/
  - /monitoring-plugins/pa/rca/index/
  - /monitoring-your-cluster/pa/rca/
  - /monitoring-your-cluster/pa/rca/index/
  - /monitoring-plugins/pa/rca/api/
  - /monitoring-your-cluster/pa/rca/api/
  - /monitoring-plugins/pa/rca/reference/
  - /monitoring-your-cluster/pa/rca/reference/
  - /monitoring-your-cluster/pa/rca/shard-hotspot/
---

# Performance Analyzer

這是實驗性功能，不建議在生產環境中使用。如需了解此功能的進展更新，或想提供意見回饋，請參閱相關的 [GitHub issue](https://github.com/opensearch-project/OpenSearch/issues/6750)。
{: .warning}

Performance Analyzer 外掛程式會收集每個節點上的 JVM、磁碟、執行緒集區、快取及每個分片的操作指標，並將其發布為 OpenSearch [指標]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/telemetry/metrics/)。OpenSearch 會將這些指標匯出至記錄檔或 OpenTelemetry Collector。

從 OpenSearch 3.0 開始，已移除 Performance Analyzer 的根本原因分析 (RCA) 代理程式。該代理程式原本在連接埠 9600 上提供 Performance Analyzer API，因此指標、批次指標與 RCA API 以及 PerfTop 儀表板皆無法使用。如需詳細資訊，請參閱[重大變更]({{site.url}}{{site.baseurl}}/breaking-changes/#performance-analyzer-plugin)。
{: .note}

## 必要條件

Performance Analyzer 外掛程式預設已安裝，但在 Windows 上除外，該平台不提供此外掛程式。

在啟用 Performance Analyzer 之前，請先在每個節點上啟用遙測與指標。如需更多資訊，請參閱[啟用遙測]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/telemetry/index/#enabling-telemetry)。

## 啟用 Performance Analyzer

Performance Analyzer 預設為停用。若要啟用它，請傳送下列請求：

```json
POST _plugins/_performanceanalyzer/cluster/config
{
  "enabled": true
}
```
{% include copy-curl.html %}

接著將 `collectorsSetting` 設定為 `1`，以設定 Performance Analyzer 使用指標架構發布其指標。預設值 `0` 不會使用指標架構發布指標：

```json
POST _plugins/_performanceanalyzer/cluster/config
{
  "collectorsSetting": 1
}
```
{% include copy-curl.html %}

若要驗證組態，請傳送下列請求：

```json
GET _plugins/_performanceanalyzer/cluster/config
```
{% include copy-curl.html %}

啟用 Performance Analyzer 後，`currentPerformanceAnalyzerClusterState` 為 `1`，且 `collectorsSetting` 為 `1`：

```json
{
  "currentPerformanceAnalyzerClusterState": 1,
  "shardsPerCollection": 0,
  "collectorsSetting": 1,
  "batchMetricsRetentionPeriodMinutes": 7
}
```

指標會在下一個指標發布間隔出現。使用預設匯出器時，OpenSearch 會將指標寫入 logs 目錄中的 `<cluster-name>_otel_metrics.log` 檔案。

## 停用 Performance Analyzer

若要停止收集指標，請傳送以下請求：

```json
POST _plugins/_performanceanalyzer/cluster/config
{
  "enabled": false
}
```
{% include copy-curl.html %}

## 指標

Performance Analyzer 會發布下列指標。

指標 | 說明
:--- | :---
`heap_used` | 已使用的堆積記憶體量。
`heap_max` | 堆積記憶體上限。
`gc_collection_event` | 垃圾回收事件次數。
`gc_collection_time` | 垃圾回收所花費的時間。
`disk_utilization` | 磁碟使用率。
`disk_wait_time` | 磁碟等待時間。
`disk_service_rate` | 磁碟服務率。
`threadpool_active_threads` | 執行緒集區中作用中的執行緒數。
`threadpool_total_threads` | 執行緒集區中的執行緒總數。
`threadpool_queue_size` | 執行緒集區佇列中的工作數。
`threadpool_queue_capacity` | 執行緒集區佇列的容量。
`threadpool_rejected_reqs` | 被執行緒集區拒絕的請求數。
`cache_field_data_size` | 欄位資料快取的大小。
`cache_max_size` | 快取的大小上限。
`cache_request_hit` | 請求快取命中次數。
`cache_request_miss` | 請求快取未命中次數。
`cache_request_size` | 請求快取的大小。
`shard_search_rate` | 每個分片的搜尋作業數。
`shard_search_latency` | 每個分片在各搜尋階段的搜尋延遲。
`shard_indexing_rate` | 每個分片的編製索引作業數。
`shard_indexing_latency` | 每個分片的編製索引延遲。
`shard_cpu_utilization` | 每個分片在特定作業中的 CPU 使用率。
`shard_heap_allocated` | 每個分片在特定作業中配置的堆積記憶體。
`cpu_utilization` | 每個分片在搜尋階段或作業中的 CPU 使用率。
`heap_allocated` | 每個分片在搜尋階段或作業中配置的堆積記憶體。

## 常見問題

節點啟動時，Performance Analyzer 會記錄錯誤，指出 `config/opensearch-performance-analyzer/` 目錄中缺少 `performance-analyzer.properties` 和 `plugin-stats-metadata` 檔案。缺少這些檔案時，Performance Analyzer 會使用其預設組態，因此這些錯誤不會妨礙其發布指標。
