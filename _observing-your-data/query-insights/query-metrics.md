---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "查詢指標"
parent: Query insights
nav_order: 30
---

# 查詢指標
**自 2.16 版起推出**
{: .label .label-purple }

關鍵查詢[指標](#metrics)，例如彙總類型、查詢類型、延遲，以及每種查詢類型的資源使用量，會透過 OpenTelemetry (OTel) 檢測架構沿著搜尋路徑擷取。遙測資料可使用 OTel 指標[匯出工具]({{site.url}}{{site.baseurl}}/observing-your-data/trace/distributed-tracing/#exporters)來取用。

## 設定查詢指標產生

若要設定查詢指標產生，請使用下列步驟。

### 步驟 1：安裝 OpenTelemetry 外掛程式

如需安裝 OpenTelemetry 外掛程式的相關資訊，請參閱[分散式追蹤]({{site.url}}{{site.baseurl}}/observing-your-data/trace/distributed-tracing/)。

### 步驟 2：啟用查詢指標

透過設定下列 `opensearch.yml` 設定來啟用查詢指標：

```yaml
telemetry.feature.metrics.enabled: true
search.query.metrics.enabled: true
```
{% include copy.html %}

以下是包含遙測設定的完整範例組態：

```yaml
# Enable query metrics feature
search.query.metrics.enabled: true
telemetry.feature.metrics.enabled: true

# OTel-related configuration
opensearch.experimental.feature.telemetry.enabled: true
telemetry.tracer.sampler.probability: 1.0
telemetry.feature.tracer.enabled: true
```
{% include copy.html %}

或者，您可以使用 API 來設定查詢指標產生：

```json
PUT _cluster/settings
{
  "persistent" : {
    "search.query.metrics.enabled" : true
  }
}
```
{% include copy-curl.html %}

使用 gRPC 匯出工具來設定指標與追蹤的匯出。如需詳細資訊，請參閱[匯出工具]({{site.url}}{{site.baseurl}}/observing-your-data/trace/distributed-tracing/#exporters)。如果您使用[預設記錄匯出工具](#default-logging-exporter)，則可以略過此步驟：

```yaml
telemetry.otel.tracer.span.exporter.class: io.opentelemetry.exporter.otlp.trace.OtlpGrpcSpanExporter
telemetry.otel.metrics.exporter.class: io.opentelemetry.exporter.otlp.metrics.OtlpGrpcMetricExporter
```
{% include copy.html %}

## 指標

查詢指標提供下列量測：

- 每種查詢類型的查詢數 (例如 `match` 或 `regex` 查詢的數量)
- 每種彙總類型的查詢數 (例如 `terms` 彙總查詢的數量)
- 每種排序順序的查詢數 (例如遞增與遞減 `sort` 查詢的數量)
- 每種查詢類型、彙總類型與排序順序的 `latency` 直方圖
- 每種查詢類型、彙總類型與排序順序的 `cpu` 直方圖
- 每種查詢類型、彙總類型與排序順序的 `memory` 直方圖

## 預設記錄匯出工具

根據預設，如果未設定任何 gRPC 匯出工具，則指標與追蹤會匯出至記錄檔。資料會儲存在 `opensearch/logs` 目錄中的下列檔案：

- `opensearch_otel_metrics.log`
- `opensearch_otel_traces.log`
