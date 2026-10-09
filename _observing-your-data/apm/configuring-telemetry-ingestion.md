---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定遙測資料匯入"
nav_order: 10
parent: Application Performance Monitoring
---

# 設定遙測資料匯入
**於 3.6 版推出**
{: .label .label-purple }

若要使用 APM，您需要透過 OpenTelemetry Collector 和 Data Prepper 管線，將應用程式追蹤和記錄檔匯入 OpenSearch。如需完整 APM 架構的概觀，請參閱 [APM 架構]({{site.url}}{{site.baseurl}}/observing-your-data/apm/#apm-architecture)。

本頁說明如何設定 OpenTelemetry Collector 和 Data Prepper，以處理遙測資料並將其路由至 OpenSearch 和 Prometheus。

## 設定 OpenTelemetry Collector

[OpenTelemetry (OTel) Collector](https://opentelemetry.io/docs/collector/) 是所有應用程式遙測資料的進入點。它透過 OpenTelemetry Protocol (OTLP) 接收資料，並將追蹤和記錄檔路由至 Data Prepper，同時將指標傳送至 Prometheus。

下列範例顯示將遙測資料路由至 Data Prepper 和 Prometheus 的主要匯出器與管線組態：

```yaml
exporters:
  otlp/opensearch:
    endpoint: "data-prepper:21893"
    tls:
      insecure: true
      insecure_skip_verify: true

  otlphttp/prometheus:
    endpoint: "http://prometheus:9090/api/v1/otlp"
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [resourcedetection, memory_limiter, transform, batch]
      exporters: [otlp/opensearch]

    metrics:
      receivers: [otlp]
      processors: [resourcedetection, memory_limiter, batch]
      exporters: [otlphttp/prometheus]

    logs:
      receivers: [otlp]
      processors: [resourcedetection, memory_limiter, transform, batch]
      exporters: [otlp/opensearch]
```
{% include copy.html %}

`otlp/opensearch` 匯出器會將追蹤和記錄檔傳送至 Data Prepper。`otlphttp/prometheus` 匯出器會將指標直接傳送至 Prometheus。如需包含接收器、處理器和遙測設定的完整 OTel Collector 組態範例，請參閱 [observability-stack 儲存庫](https://github.com/opensearch-project/observability-stack/blob/main/docker-compose/otel-collector/config.yaml)。
{: .note}

## 設定 Data Prepper 管線

Data Prepper 會從 OTel Collector 接收遙測資料，並將其處理成 APM 所需的格式。管線架構會將資料路由至專門處理記錄檔與追蹤，以及產生服務對應圖的子管線。

下列範例顯示完整的 Data Prepper 管線組態：

```yaml
# Main OTLP pipeline - receives all telemetry and routes by type
otlp-pipeline:
  source:
    otlp:
      ssl: false
  route:
    - logs: "getEventType() == \"LOG\""
    - traces: "getEventType() == \"TRACE\""
  sink:
    - pipeline:
        name: "otel-logs-pipeline"
        routes:
          - "logs"
    - pipeline:
        name: "otel-traces-pipeline"
        routes:
          - "traces"

# Log processing pipeline
otel-logs-pipeline:
  workers: 5 # config example to set workers 
  delay: 10 # config example to set delay 
  source:
    pipeline:
      name: "otlp-pipeline"
  buffer:
    bounded_blocking:
  sink:
    - opensearch:
        hosts: ["https://<opensearch-host>:9200"]
        username: <username>
        password: <password>
        insecure: true
        index_type: log-analytics-plain

# Trace processing pipeline
otel-traces-pipeline:
  source:
    pipeline:
      name: "otlp-pipeline"
  sink:
    - pipeline:
        name: "traces-raw-pipeline"
    - pipeline:
        name: "service-map-pipeline"

# Raw trace storage pipeline
traces-raw-pipeline:
  source:
    pipeline:
      name: "otel-traces-pipeline"
  processor:
    - otel_traces:
  sink:
    - opensearch:
        hosts: ["https://<opensearch-host>:9200"]
        username: <username>
        password: <password>
        insecure: true
        index_type: trace-analytics-plain-raw

# Service map and APM metrics pipeline
service-map-pipeline:
  source:
    pipeline:
      name: "otel-traces-pipeline"
  processor:
    - otel_apm_service_map:
        group_by_attributes: [telemetry.sdk.language] # Add any resource attribute to group by
  route:
    - otel_apm_service_map_route: 'getEventType() == "SERVICE_MAP"'
    - service_processed_metrics: 'getEventType() == "METRIC"'
  sink:
    - opensearch:
        hosts: ["https://<opensearch-host>:9200"]
        username: <username>
        password: <password>
        index_type: otel-v2-apm-service-map
        routes: [otel_apm_service_map_route]
        insecure: true
    - prometheus:
        url: "http://prometheus:9090/api/v1/write"
        routes: [service_processed_metrics]
```
{% include copy.html %}

### 管線架構

Data Prepper 管線透過下列步驟處理遙測資料：

1. 入口管線（`otlp-pipeline`）會在連接埠 21893 接收所有遙測資料，並將記錄檔和追蹤路由至各自的子管線。
2. 記錄檔管線（`otel-logs-pipeline`）會將 `time` 欄位對應至 `@timestamp`，並使用 `log-analytics-plain` 索引類型將記錄檔寫入 OpenSearch。
3. 追蹤管線（`otel-traces-pipeline`）會將追蹤分送至原始資料儲存管線和服務對應圖管線。
4. 原始追蹤管線（`traces-raw-pipeline`）會使用 `otel_traces` 處理器處理個別追蹤跨度，並使用 `trace-analytics-plain-raw` 索引類型將其儲存在 OpenSearch 中。
5. 服務對應圖管線（`service-map-pipeline`）會使用 `otel_apm_service_map` 處理器產生服務相依性對應圖和 RED 指標。服務對應圖的拓撲資料會寫入 OpenSearch，而 RED 指標則透過遠端寫入匯出至 Prometheus。

`otel_apm_service_map` 處理器的兩個主要組態選項為 `group_by_attributes`（決定服務在應用程式對應圖中的分組方式）和 `window_duration`（設定彙總追蹤資料的時間範圍）。如需完整的組態詳細資訊，請參閱 [APM 服務對應圖處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/otel-apm-service-map/)。
{: .note}

## 驗證匯入

設定 OTel Collector 和 Data Prepper 後，請驗證資料是否正常流動：

1. 驗證您的 OpenSearch 叢集中是否已建立下列索引：
   - `otel-v1-apm-span-*`：原始追蹤跨度。
   - `otel-v2-apm-service-map`：服務拓撲資料。
   - `logs-otel-v1-*`：應用程式記錄檔。

2. 驗證 Data Prepper 的遠端寫入目標在您的 Prometheus 執行個體中是否處於作用中狀態。

3. 在 OpenSearch Dashboards 中，前往 **Observability** > **APM**，確認您的服務出現在[服務]({{site.url}}{{site.baseurl}}/observing-your-data/apm/services/)目錄和[應用程式對應圖]({{site.url}}{{site.baseurl}}/observing-your-data/apm/application-map/)中。

請確保 OTel Collector、Data Prepper、OpenSearch 和 Prometheus 之間的所有連接埠對應皆正確。連接埠不符是匯入失敗的常見原因。
{: .warning}

## 後續步驟

- [在 OpenSearch Dashboards 中設定 APM]({{site.url}}{{site.baseurl}}/observing-your-data/apm/configuring-apm/)：建立資料集、索引模式，並設定 APM 設定，即可開始使用 APM 功能。
