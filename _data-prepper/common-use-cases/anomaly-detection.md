---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "異常偵測"
parent: Common use cases
nav_order: 5
---

# 使用 Data Prepper 進行異常偵測

您可以使用 OpenSearch Data Prepper 對時間序列彙總事件進行模型訓練，並近乎即時地產生異常。您可以針對管線內產生的事件，或直接進入管線的事件 (例如 OpenTelemetry 指標) 產生異常。您可以將這些跳動視窗彙總的時間序列事件饋送至 [`anomaly_detector` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/anomaly-detector/)，該處理器會訓練模型並產生附有評分的異常。接著，您可以設定管線，將異常寫入獨立的索引，以建立文件監視器並快速觸發警示。

## 來自記錄檔的指標

下列管線會從 HTTP 來源 (例如 FluentBit) 接收記錄檔，透過將 `log` 索引鍵的值與 [Grok Apache Common Log Format](https://httpd.apache.org/docs/2.4/logs.html#accesslog) 進行比對，從記錄檔中擷取重要值，然後將 grok 處理後的記錄檔轉送至 `log-to-metrics-pipeline` 管線以及名為 `logs` 的 OpenSearch 索引。

`log-to-metrics-pipeline` 管線會從 `apache-log-pipeline-with-metrics` 管線接收 grok 處理後的記錄檔，將其彙總，並根據 `clientip` 和 `request` 索引鍵的值衍生直方圖指標。接著，它會將直方圖指標傳送至名為 `histogram_metrics` 的 OpenSearch 索引，以及 `log-to-metrics-anomaly-detector-pipeline` 管線。

`log-to-metrics-anomaly-detector-pipeline` 管線會從 `log-to-metrics-pipeline` 管線接收彙總的直方圖指標，並將其傳送至 `anomaly_detector` 處理器，以使用 Random Cut Forest 演算法偵測異常。如果演算法偵測到異常，便會將其傳送至名為 `log-metric-anomalies` 的 OpenSearch 索引。

```json
apache-log-pipeline-with-metrics:
  source:
    http:
      # Provide the path for ingestion. ${pipelineName} will be replaced with pipeline name configured for this pipeline.
      # In this case it would be "/apache-log-pipeline-with-metrics/logs". This will be the FluentBit output URI value.
      path: "/${pipelineName}/logs"
  processor:
    - grok:
        match:
          log: [ "%{COMMONAPACHELOG_DATATYPED}" ]
  sink:
    - opensearch:
        ...
        index: "logs"
    - pipeline:
        name: "log-to-metrics-pipeline"

log-to-metrics-pipeline:
  source:
    pipeline:
      name: "apache-log-pipeline-with-metrics"
  processor:
    - aggregate:
        # Specify the required identification keys
        identification_keys: ["clientip", "request"]
        action:
          histogram:
            # Specify the appropriate values for each the following fields
            key: "bytes"
            record_minmax: true
            units: "bytes"
            buckets: [0, 25000000, 50000000, 75000000, 100000000]
        # Pick the required aggregation period
        group_duration: "30s"
  sink:
    - opensearch:
        ...
        index: "histogram_metrics"
    - pipeline:
        name: "log-to-metrics-anomaly-detector-pipeline"

log-to-metrics-anomaly-detector-pipeline:
  source:
    pipeline:
      name: "log-to-metrics-pipeline"
  processor:
    - anomaly_detector:
        # Specify the key on which to run anomaly detection
        keys: [ "bytes" ]
        mode:
          random_cut_forest:
  sink:
    - opensearch:
        ...
        index: "log-metric-anomalies"
```
{% include copy-curl.html %}

## 來自追蹤的指標

您可以從追蹤衍生指標，並在這些指標中尋找異常。在此範例中，`entry-pipeline` 管線會從 OpenTelemetry Collector 接收追蹤資料，並將其轉送至下列管線：

- `span-pipeline` –- 從追蹤中擷取原始 span。此管線會將原始 span 傳送至任何以 `otel-v1-apm-span` 為前置詞的 OpenSearch 索引。

- `service-map-pipeline` –- 彙總並分析追蹤，以建立代表服務之間連線的文件。此管線會將這些文件傳送至名為 `otel-v1-apm-service-map` 的 OpenSearch 索引。接著，您可以透過 OpenSearch Dashboards 的 [Trace Analytics]({{site.url}}{{site.baseurl}}/observing-your-data/trace/index/) 外掛程式，查看服務對應的視覺化。

- `trace-to-metrics-pipeline` -- 根據 `serviceName` 的值，彙總並從追蹤衍生直方圖指標。接著，此管線會將衍生的指標傳送至名為 `metrics_for_traces` 的 OpenSearch 索引，以及 `trace-to-metrics-anomaly-detector-pipeline` 管線。

`trace-to-metrics-anomaly-detector-pipeline` 管線會從 `trace-to-metrics-pipeline` 接收彙總的直方圖指標，並將其傳送至 `anomaly_detector` 處理器，以使用 Random Cut Forest 演算法偵測異常。如果演算法偵測到任何異常，便會將其傳送至名為 `trace-metric-anomalies` 的 OpenSearch 索引。

```json
entry-pipeline:
  source:
    otel_trace_source:
      # Provide the path for ingestion. ${pipelineName} will be replaced with pipeline name configured for this pipeline.
      # In this case it would be "/entry-pipeline/v1/traces". This will be endpoint URI path in OpenTelemetry Exporter 
      # configuration.
      # path: "/${pipelineName}/v1/traces"
  processor:
    - trace_peer_forwarder:
  sink:
    - pipeline:
        name: "span-pipeline"
    - pipeline:
        name: "service-map-pipeline"
    - pipeline:
        name: "trace-to-metrics-pipeline"

span-pipeline:
  source:
    pipeline:
      name: "entry-pipeline"
  processor:
    - otel_traces:
  sink:
    - opensearch:
        ...
        index_type: "trace-analytics-raw"

service-map-pipeline:
  source:
    pipeline:
      name: "entry-pipeline"
  processor:
    - service_map:
  sink:
    - opensearch:
        ...
        index_type: "trace-analytics-service-map"

trace-to-metrics-pipeline:
  source:
    pipeline:
      name: "entry-pipeline"
  processor:
    - aggregate:
        # Pick the required identification keys
        identification_keys: ["serviceName"]
        action:
          histogram:
            # Pick the appropriate values for each the following fields
            key: "durationInNanos"
            record_minmax: true
            units: "seconds"
            buckets: [0, 10000000, 50000000, 100000000]
        # Pick the required aggregation period
        group_duration: "30s"
  sink:
    - opensearch:
        ...
        index: "metrics_for_traces"
    - pipeline:
        name: "trace-to-metrics-anomaly-detector-pipeline"

trace-to-metrics-anomaly-detector-pipeline:
  source:
    pipeline:
      name: "trace-to-metrics-pipeline"
  processor:
    - anomaly_detector:
        # Below Key will find anomalies in the max value of histogram generated for durationInNanos.
        keys: [ "max" ]
        mode:
          random_cut_forest:
  sink:
    - opensearch:
        ...
        index: "trace-metric-anomalies"
```
{% include copy-curl.html %}

## OpenTelemetry 指標

您可以建立管線，以接收 OpenTelemetry 指標並偵測這些指標中的異常。在此範例中，`entry-pipeline` 會從 OpenTelemetry Collector 接收指標。如果指標的類型為 `GAUGE`，且指標名稱為 `totalApiBytesSent`，則處理器會將其傳送至 `ad-pipeline` 管線。

`ad-pipeline` 管線會從進入管線接收指標，並使用 [`anomaly_detector` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/anomaly-detector/) 對指標值執行異常偵測。

```json
entry-pipeline:
  source:
    otel_metrics_source:
  processor:
    - otel_metrics:
  route:
    - gauge_route: '/kind = "GAUGE" and /name = "totalApiBytesSent"'
  sink:
    - pipeline:
        name: "ad-pipeline"
        routes:
          - gauge_route
    - opensearch:
        ...
        index: "otel-metrics"

ad-pipeline:
  source:
    pipeline:
      name: "entry-pipeline"
    processor:
      - anomaly_detector:
        # Use "value" as the key on which anomaly detector needs to be run
        keys: [ "value" ]
        mode:
          random_cut_forest:
    sink:
      - opensearch:
        ...
        index: otel-metrics-anomalies                     
```
{% include copy-curl.html %}
