---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分散式追蹤"
parent: Telemetry
grand_parent: Monitoring your cluster
nav_order: 20
redirect_from:
  - /observing-your-data/trace/distributed-tracing/
---

# 分散式追蹤

這是實驗性功能，不建議在生產環境中使用。如需了解此功能的最新進度，或想提供意見回饋，請參閱相關的 [GitHub issue](https://github.com/opensearch-project/OpenSearch/issues/6750)。
{: .warning}

分散式追蹤會記錄請求在 OpenSearch 叢集中移動的路徑。_追蹤 (trace)_ 是單一請求的完整路徑。追蹤包含一系列 _span_，每個 span 會記錄一項作業的開始與結束時間，並可包含屬性與事件等中繼資料。您可以使用分散式追蹤，找出增加請求延遲的作業以及錯誤的來源。

分散式追蹤會追蹤 OpenSearch 處理的請求。若要分析您自有應用程式的追蹤，請參閱[追蹤分析]({{site.url}}{{site.baseurl}}/observing-your-data/trace/index/)。

## 啟用分散式追蹤

若要啟用分散式追蹤，請先啟用遙測功能旗標並安裝 `telemetry-otel` 外掛程式。如需詳細資訊，請參閱[啟用遙測]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/telemetry/index/#enabling-telemetry)。

接著啟用追蹤：

1. 在每個節點的 `opensearch.yml` 中新增下列設定，然後重新啟動節點：

   ```yaml
   telemetry.feature.tracer.enabled: true
   ```
   {% include copy.html %}

2. 更新動態的 `telemetry.tracer.enabled` 設定，以在執行中的叢集啟用追蹤器：

   ```json
   PUT _cluster/settings
   {
     "persistent": {
       "telemetry.tracer.enabled": true
     }
   }
   ```
   {% include copy-curl.html %}

## 設定追蹤匯出

OpenSearch 會為 HTTP 請求及一部分傳輸請求產生追蹤。OpenSearch 將已完成的 span 保存在記憶體中，並分批傳送至匯出器。若要設定匯出，請在 `opensearch.yml` 中指定下列靜態設定。

設定 | 說明
:--- | :---
`telemetry.otel.tracer.exporter.max_queue_size` | 保存在記憶體中的 span 數量上限。當佇列已滿時，OpenSearch 會捨棄新的 span。預設為 `2048`。
`telemetry.otel.tracer.exporter.batch_size` | 單一批次傳送至匯出器的 span 數量上限。必須小於 `telemetry.otel.tracer.exporter.max_queue_size`。預設為 `512`。
`telemetry.otel.tracer.exporter.delay` | OpenSearch 將 span 傳送至匯出器的間隔時間，即使批次未滿也會傳送。預設為 `2s`。
`telemetry.otel.tracer.span.exporter.class` | 持久化 span 的匯出器。有效值為 `io.opentelemetry.exporter.logging.LoggingSpanExporter`，它會將 span 寫入 logs 目錄中的 `<cluster-name>_otel_traces.log` 檔案；以及 `io.opentelemetry.exporter.otlp.trace.OtlpGrpcSpanExporter`，它會使用 gRPC 將 span 傳送至 OpenTelemetry Collector。預設為 `io.opentelemetry.exporter.logging.LoggingSpanExporter`。

若要將 span 傳送至 OpenTelemetry Collector，請在每個節點上執行 collector，並將下列設定加入 `opensearch.yml`。預設情況下，匯出器會將 span 傳送至 `http://localhost:4317/` 端點。透過 collector，您可以將 span 傳送至追蹤後端，例如 Jaeger 或 OpenSearch：

```yaml
telemetry.otel.tracer.span.exporter.class: io.opentelemetry.exporter.otlp.trace.OtlpGrpcSpanExporter
```
{% include copy.html %}

## 取樣

追蹤每個請求都會消耗系統資源。為了減少 OpenSearch 記錄的追蹤數量，OpenSearch 會對請求進行取樣。屬於既有追蹤的跨度會遵循該追蹤中第一個跨度的取樣決策。對於啟動新追蹤的請求，OpenSearch 會在建立第一個跨度之前，依照下列順序做出取樣決策：

1. 如果請求包含 `trace` HTTP 標頭，OpenSearch 會使用其值。值為 `true` 時會記錄追蹤，值為 `false` 時則會捨棄追蹤，不受取樣機率影響。
1. 否則，OpenSearch 會依照動態 `telemetry.tracer.sampler.probability` 設定中所設定的機率記錄追蹤。此設定接受 0 到 1 之間的值。預設值為 `0.01`，會對 1% 的請求進行取樣。啟動新追蹤的傳輸請求（例如節點之間的內部請求）會以較低的比率取樣。

例如，下列請求會對 5% 的請求進行取樣：

```json
PUT _cluster/settings
{
  "persistent": {
    "telemetry.tracer.sampler.probability": 0.05
  }
}
```
{% include copy-curl.html %}

若要對特定請求進行偵錯，請將其 `trace` 標頭設為 `true` 後傳送：

```bash
curl -H "trace: true" "http://localhost:9200/_search"
```
{% include copy.html %}

OpenSearch 不支援尾端取樣，也就是在追蹤完成後才做出取樣決策。若要使用尾端取樣，請將所有跨度匯出至 OpenTelemetry Collector，並在收集器中設定尾端取樣。如需詳細資訊，請參閱 [OpenTelemetry 取樣文件](https://opentelemetry.io/docs/concepts/sampling/#tail-sampling)。
