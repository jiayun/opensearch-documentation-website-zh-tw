---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "從追蹤衍生指標"
parent: Common use cases
nav_order: 20
---

# 從追蹤衍生指標

您可以使用 OpenSearch Data Prepper 從 OpenTelemetry 追蹤衍生指標。下列範例管線會接收傳入的追蹤，並擷取名為 `durationInNanos` 的指標，以 30 秒的滾動視窗進行彙總。接著，它會從傳入的追蹤衍生直方圖。

此管線包含下列管線：

- `entry-pipeline` – 從 OpenTelemetry collector 接收追蹤資料，並將其轉送至 `trace_to_metrics_pipeline` 管線。

- `trace-to-metrics-pipeline` - 從 `entry-pipeline` 管線接收追蹤資料，進行彙總，並根據 `serviceName` 欄位的值從追蹤衍生 `durationInNanos` 的直方圖。接著，它會將衍生的指標傳送至名為 `metrics_for_traces` 的 OpenSearch 索引。

```json
entry-pipeline:
  source:
    otel_trace_source:
      # Provide the path for ingestion. ${pipelineName} will be replaced with pipeline name.
      # In this case it would be "/entry-pipeline/v1/traces". This will be endpoint URI path in OpenTelemetry Exporter configuration.
      path: "/${pipelineName}/v1/traces"
  sink:
    - pipeline:
        name: "trace-to-metrics-pipeline"

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
            # Pick the appropriate values for each of the following fields
            key: "durationInNanos"
            record_minmax: true
            units: "seconds"
            buckets: [0, 10000000, 50000000, 100000000]
        # Specify an aggregation period
        group_duration: "30s"
  sink:
    - opensearch:
        ...
        index: "metrics_for_traces"
```
{% include copy-curl.html %}
