---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "入門"
parent: Trace analytics
nav_order: 1
redirect_from:
  - /observability-plugin/trace/get-started/
  - /monitoring-plugins/trace/get-started/
---

# 追蹤分析入門

OpenSearch 追蹤分析由兩個元件組成：Data Prepper 和 Trace Analytics OpenSearch Dashboards 外掛程式。Data Prepper 儲存庫包含數個可協助您入門的[範例應用程式](https://github.com/opensearch-project/data-prepper/tree/main/examples)。

## 基本資料流程

![從分散式應用程式到 OpenSearch 的資料流程圖]({{site.url}}{{site.baseurl}}/images/ta.svg)

1. 追蹤分析需要您在應用程式中加入檢測機制並產生追蹤資料。[OpenTelemetry 文件](https://opentelemetry.io/docs/)包含多種程式語言的範例應用程式，可協助您入門，包括 Java、Python、Go 和 JavaScript。

   （在下列 [Jaeger HotROD](#jaeger-hotrod) 範例中，額外的元件 Jaeger 代理程式會與應用程式一同執行，並將資料傳送至 OpenTelemetry Collector，但概念相似。）

1. [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/getting-started/) 從應用程式接收資料，並將其格式化為 OpenTelemetry 資料。

1. [Data Prepper]({{site.url}}{{site.baseurl}}/clients/data-prepper/index/) 處理 OpenTelemetry 資料，將其轉換為可供 OpenSearch 使用的格式，並在 OpenSearch 叢集上為其編製索引。

1. [Trace Analytics OpenSearch Dashboards 外掛程式]({{site.url}}{{site.baseurl}}/observing-your-data/trace/ta-dashboards/) 以近乎即時的方式，透過一系列圖表和表格顯示資料，重點呈現服務架構、延遲、錯誤率和輸送量。

## Jaeger HotROD

Jaeger HotROD 示範程式是追蹤分析的範例應用程式之一，可模擬資料在分散式應用程式中的流動。

下載或複製 [Data Prepper 儲存庫](https://github.com/opensearch-project/data-prepper)。接著前往 `examples/jaeger-hotrod/`，並在文字編輯器中開啟 `docker-compose.yml`。此檔案包含[基本資料流程](#basic-flow-of-data)中每個元素各自的容器：

- 搭配 Jaeger 代理程式（`jaeger-agent`）的分散式應用程式（`jaeger-hot-rod`）
- [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/getting-started/)（`otel-collector`）
- Data Prepper（`data-prepper`）
- 單一節點的 OpenSearch 叢集（`opensearch`）
- OpenSearch Dashboards（`opensearch-dashboards`）。

關閉檔案並執行 `docker compose up --build`。容器啟動後，在網頁瀏覽器中前往 `http://localhost:8080`。

![HotROD 網頁介面]({{site.url}}{{site.baseurl}}/images/hot-rod.png)

按一下網頁介面中的任一按鈕，將請求傳送至應用程式。每個請求都會在組成應用程式的各項服務中啟動一系列作業。從主控台記錄檔中，您可以看到這些作業具有相同的 `trace-id`，讓您能將請求中的所有作業視為單一*追蹤*來追蹤：

```
jaeger-hot-rod  | http://0.0.0.0:8081/customer?customer=392
jaeger-hot-rod  | 2020-11-19T16:29:53.425Z	INFO	frontend/server.go:92	HTTP request received	{"service": "frontend", "trace_id": "12091bd60f45ea2c", "span_id": "12091bd60f45ea2c", "method": "GET", "url": "/dispatch?customer=392&nonse=0.6509021735471818"}
jaeger-hot-rod  | 2020-11-19T16:29:53.426Z	INFO	customer/client.go:54	Getting customer{"service": "frontend", "component": "customer_client", "trace_id": "12091bd60f45ea2c", "span_id": "12091bd60f45ea2c", "customer_id": "392"}
jaeger-hot-rod  | 2020-11-19T16:29:53.430Z	INFO	customer/server.go:67	HTTP request received	{"service": "customer", "trace_id": "12091bd60f45ea2c", "span_id": "252ff7d0e1ac533b", "method": "GET", "url": "/customer?customer=392"}
jaeger-hot-rod  | 2020-11-19T16:29:53.430Z	INFO	customer/database.go:73	Loading customer{"service": "customer", "component": "mysql", "trace_id": "12091bd60f45ea2c", "span_id": "252ff7d0e1ac533b", "customer_id": "392"}
```

這些作業也具有 `span_id`。*跨度*是單一服務中的工作單位。每個追蹤都包含若干個跨度。應用程式開始處理請求後不久，您就可以看到 OpenTelemetry Collector 開始匯出跨度：

```
otel-collector  | 2020-11-19T16:29:53.781Z	INFO	loggingexporter/logging_exporter.go:296	TraceExporter	{"#spans": 1}
otel-collector  | 2020-11-19T16:29:53.787Z	INFO	loggingexporter/logging_exporter.go:296	TraceExporter	{"#spans": 3}
```

接著，Data Prepper 會處理來自 OpenTelemetry Collector 的資料，並為其編製索引：

```
data-prepper  | 1031918 [service-map-pipeline-process-worker-2-thread-1] INFO  com.amazon.dataprepper.pipeline.ProcessWorker  –  service-map-pipeline Worker: Processing 3 records from buffer
data-prepper  | 1031923 [entry-pipeline-process-worker-1-thread-1] INFO  com.amazon.dataprepper.pipeline.ProcessWorker  –  entry-pipeline Worker: Processing 1 records from buffer
```

最後，您可以看到 OpenSearch 節點回應索引編製請求。

```
node-0.example.com  | [2020-11-19T16:29:55,064][INFO ][o.e.c.m.MetadataMappingService] [9fb4fb37a516] [otel-v1-apm-span-000001/NGYbmVD9RmmqnxjfTzBQsQ] update_mapping [_doc]
node-0.example.com  | [2020-11-19T16:29:55,267][INFO ][o.e.c.m.MetadataMappingService] [9fb4fb37a516] [otel-v1-apm-span-000001/NGYbmVD9RmmqnxjfTzBQsQ] update_mapping [_doc]
```

在新的終端機視窗中執行下列命令，查看 OpenSearch 叢集中的其中一份原始文件：

```bash
curl -X GET -u 'admin:<custom-admin-password>' -k 'https://localhost:9200/otel-v1-apm-span-000001/_search?pretty&size=1'
```

在網頁瀏覽器中前往 `http://localhost:5601`，並選取 **Trace Analytics**。您可以看到在 Jaeger HotROD 網頁介面中按一下按鈕所產生的結果：每個 API 和 HTTP 方法的追蹤數量、延遲趨勢、以顏色區分的服務架構圖，以及可用來深入查看個別作業的追蹤 ID 清單。

如果您沒有看到自己的追蹤，請調整 OpenSearch Dashboards 中的時間範圍。如需使用此外掛程式的詳細資訊，請參閱 [OpenSearch Dashboards 外掛程式]({{site.url}}{{site.baseurl}}/observing-your-data/trace/ta-dashboards/)。
