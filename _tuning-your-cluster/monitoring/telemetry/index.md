---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遙測"
parent: Monitoring your cluster
nav_order: 10
has_children: true
has_toc: false
redirect_from:
  - /tuning-your-cluster/monitoring/telemetry/
---

# 遙測

這是一項實驗性功能，不建議在正式環境中使用。若要了解此功能的進度更新或提供意見回饋，請參閱相關的 [GitHub issue](https://github.com/opensearch-project/OpenSearch/issues/6750)。
{: .warning}

OpenSearch 可以產生自身運作的指標與追蹤，並使用 [OpenTelemetry](https://opentelemetry.io/) 匯出。您可以使用遙測來監控叢集效能，並找出耗用最多資源的請求與作業。

啟用遙測可能會耗用系統資源。啟用遙測之前，請先確認您有足夠的叢集資源可供配置。
{: .warning}

OpenSearch 提供下列遙測功能：

- [指標]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/telemetry/metrics/)是 OpenSearch 為叢集作業記錄的計數器、直方圖與量測計。
- [分散式追蹤]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/telemetry/distributed-tracing/)會記錄 HTTP 請求及部分傳輸請求在叢集中流動時的跨度 (span)。
- [Performance Analyzer]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/telemetry/performance-analyzer/) 會在 OpenSearch 記錄的指標之外，新增 JVM、磁碟、執行緒集區、快取與每個分片的作業指標。

## 啟用遙測

依照下列步驟啟用遙測並安裝 `telemetry-otel` 外掛程式，然後啟用指標、追蹤或兩者。

### 步驟 1：啟用遙測功能旗標

在每個節點上啟用 `opensearch.experimental.feature.telemetry.enabled` 功能旗標。例如，在 `opensearch.yml` 中加入以下一行：

```yaml
opensearch.experimental.feature.telemetry.enabled: true
```
{% include copy.html %}

若要了解啟用此旗標的其他方式，例如使用 Docker、`jvm.options` 或環境變數，請參閱[實驗性功能旗標]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/experimental/)。

### 步驟 2：安裝 telemetry-otel 外掛程式

`telemetry-otel` 外掛程式使用 OpenTelemetry Java SDK 實作遙測。此外掛程式並未包含在 OpenSearch 發行版本中。若要安裝，請在每個節點上執行以下命令：

```bash
bin/opensearch-plugin install telemetry-otel
```
{% include copy.html %}

### 步驟 3：啟用指標或追蹤

在 `opensearch.yml` 中加入以下設定，以啟用您想使用的遙測功能：

```yaml
telemetry.feature.metrics.enabled: true
telemetry.feature.tracer.enabled: true
```
{% include copy.html %}

然後重新啟動每個節點。各功能支援的設定，請參閱[指標]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/telemetry/metrics/)與[分散式追蹤]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/telemetry/distributed-tracing/)。

## 相關文件

- [追蹤分析]({{site.url}}{{site.baseurl}}/observing-your-data/trace/index/)：分析來自您自己應用程式的追蹤。
- [記錄檔]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/logs/)：設定 OpenSearch 記錄檔，包括慢速查詢記錄。
