---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "追蹤對等轉送器"
parent: Processors
grand_parent: Pipelines
nav_order: 380
---

# 追蹤對等轉送器處理器

`trace_peer_forwarder` 處理器與[對等轉送器]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/peer-forwarder/)搭配使用，可將[追蹤分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/trace-analytics/)管線中轉送的事件數量減少一半。在追蹤分析中，每個事件從 `otel-trace-pipeline` 傳送至 `raw-pipeline` 和 `service-map-pipeline` 時，通常都會複製一份。當管線轉送事件時，這會導致核心對等轉送器針對同一個事件傳送多個 HTTP 請求。您可以使用 `trace peer forwarder`，透過 `otel-trace-pipeline` 將事件轉送一次，而非透過 `raw-pipeline` 和 `service-map-pipeline` 轉送，藉此避免不必要的 HTTP 請求。

當您有多個節點時，應在追蹤分析管線中使用 `trace_peer_forwarder`。

## 使用方式

若要開始使用 `trace_peer_forwarder`，請先設定[對等轉送器]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/peer-forwarder/)。接著建立 `pipeline.yaml` 檔案，並將 `trace peer forwarder` 指定為處理器。您可以在 `data-prepper-config.yaml` 檔案中設定 `peer forwarder`。如需更詳細的資訊，請參閱[設定 OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/#2-configuring-data-prepper)。

請參閱下列 `pipeline.yaml` 檔案範例： 

```yaml
otel-trace-pipeline:
  delay: "100"
  source:
    otel_trace_source:
  processor:
    - trace_peer_forwarder:
  sink:
    - pipeline:
        name: "raw-pipeline"
    - pipeline:
        name: "service-map-pipeline"
raw-pipeline:
  source:
    pipeline:
      name: "entry-pipeline"
  processor:
    - otel_traces:
  sink:
    - opensearch:
service-map-pipeline:
  delay: "100"
  source:
    pipeline:
      name: "entry-pipeline"
  processor:
    - service_map:
  sink:
    - opensearch:
```

在前述 `pipeline.yaml` 檔案中，事件會在 `otel-trace-pipeline` 中轉送至目標對等節點，而 `raw-pipeline` 或 `service-map-pipeline` 中不會執行轉送。此流程將事件（以 HTTP 請求的形式）轉送一次而非兩次，有助於提升網路效能。 