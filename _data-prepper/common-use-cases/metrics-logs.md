---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "從記錄檔衍生指標"
parent: Common use cases
nav_order: 15
---

# 從記錄檔衍生指標

您可以使用 OpenSearch Data Prepper 從記錄檔衍生指標。

下列範例管線使用 [`http` 來源外掛程式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/http-source) 與 [`grok` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/grok/) 接收傳入的記錄檔，然後使用 [`aggregate` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/aggregate/) 擷取在 30 秒時間窗內彙總的指標位元組，並從結果衍生長條圖。

此管線將資料寫入兩個不同的 OpenSearch 索引：

- `logs`：此索引在經過 `grok` 處理器處理後，儲存原始、未彙總的記錄事件。
- `histogram_metrics`：此索引儲存使用 `aggregate` 處理器從記錄事件中擷取的衍生長條圖指標。

此管線包含兩個子管線：

- `apache-log-pipeline-with-metrics`：透過 FluentBit 等 HTTP 用戶端接收記錄檔，並使用 `grok` 透過比對記錄鍵中的值與 [Apache Common Log Format](https://httpd.apache.org/docs/2.4/logs.html#accesslog)，從記錄檔中擷取重要值。接著將經過 grok 處理的記錄檔轉送至兩個目的地：

 - 名為 `logs` 的 OpenSearch 索引，用於儲存原始記錄事件。
 - `log-to-metrics-pipeline`，用於進一步彙總與指標衍生。

- `log-to-metrics-pipeline`：從 `apache-log-pipeline-with-metrics` 管線接收經過 grok 處理的記錄檔，彙總這些記錄檔，並根據 `clientip` 與 `request` 鍵中的值衍生位元組的長條圖指標。最後，將衍生的長條圖指標傳送至名為 `histogram_metrics` 的 OpenSearch 索引。
  
#### 範例管線

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
            # Specify the appropriate values for each of the following fields
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
```
{% include copy-curl.html %}
