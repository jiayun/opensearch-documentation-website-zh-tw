---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "匯入可觀測性資料"
nav_order: 20
---

# 匯入可觀測性資料

在 OpenSearch Dashboards 中分析可觀測性資料之前，您的應用程式必須先將資料傳送至 OpenSearch，或傳送至 OpenSearch 可查詢的後端。記錄檔與追蹤會儲存在 OpenSearch 索引中。指標則儲存在 Prometheus 中（OpenSearch 透過 Prometheus 資料來源查詢），或儲存在 OpenSearch 索引中。

本文件所述的設定使用下列元件：

- 使用 [OpenTelemetry](https://opentelemetry.io/docs/) SDK 加入遙測埋點的應用程式會產生追蹤、指標與記錄檔。
- 記錄收集器（例如 [Fluent Bit](https://docs.fluentbit.io/manual/)）會讀取記錄檔並傳送記錄行。
- [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) 會接收來自應用程式的資料，並依類型進行路由。
- [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 會剖析並擴充記錄檔與追蹤，然後將其寫入 OpenSearch 索引。
- [Prometheus](https://prometheus.io/) 會儲存指標。OpenSearch 透過 [Prometheus 資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/connect-prometheus/)查詢 Prometheus，因此 Prometheus 伺服器必須可從 OpenSearch 節點連線。

## 匯入路徑

下表列出可觀測性資料傳送至 OpenSearch 或 Prometheus 的典型路徑。請找出您要匯入的資料類型，然後依照其路徑的設定指示操作。

| 資料 | 路徑 | 設定 |
|:---|:---|:---|
| 記錄檔 | 記錄收集器或 OpenTelemetry Collector → Data Prepper → OpenSearch 索引 <br><br> 或 <br><br> 記錄收集器 → OpenSearch 索引 | [開始使用記錄檔分析]({{site.url}}{{site.baseurl}}/observing-your-data/log-ingestion/)（Fluent Bit 教學）<br> [將記錄資料匯入 OpenSearch]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/ingesting-log-data/) <br> [記錄檔分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/log-analytics/) <br> [OTel 記錄檔來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/otel-logs-source/) <br> [Fluent Bit OpenSearch 輸出](https://docs.fluentbit.io/manual/pipeline/outputs/opensearch) <br> [Logstash]({{site.url}}{{site.baseurl}}/tools/logstash/index/) |
| 追蹤 | 已加入遙測埋點的應用程式 → OpenTelemetry Collector → Data Prepper → OpenSearch span 與服務地圖（service map）索引 | [開始使用追蹤分析]({{site.url}}{{site.baseurl}}/observing-your-data/trace/getting-started/)（Jaeger HotROD 教學）<br> [使用 Data Prepper 進行追蹤分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/trace-analytics/) <br> [OTel 追蹤來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/otel-trace-source/) |
| 指標 | 已加入遙測埋點的應用程式 → OpenTelemetry Collector → Prometheus <br><br> 或 <br><br> 已加入遙測埋點的應用程式 → OpenTelemetry Collector → Data Prepper → OpenSearch 索引 | [將 Prometheus 連線至 OpenSearch]({{site.url}}{{site.baseurl}}/dashboards/management/connect-prometheus/) <br> [指標分析]({{site.url}}{{site.baseurl}}/observing-your-data/prometheusmetrics/) <br> [OTel 指標來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/otel-metrics-source/) |
| APM 的記錄檔、追蹤與指標 | 已加入遙測埋點的應用程式 → OpenTelemetry Collector → Data Prepper → OpenSearch 索引（記錄檔與追蹤）及 Prometheus（指標） | [設定遙測資料匯入]({{site.url}}{{site.baseurl}}/observing-your-data/apm/configuring-telemetry-ingestion/) |
| 代理程式追蹤 | 使用 OpenSearch 生成式 AI 可觀測性 SDK 加入遙測埋點的應用程式 → OpenTelemetry Collector → Data Prepper → OpenSearch 索引 | [為您的應用程式加入遙測埋點]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/instrument/) |

追蹤分析與 APM 需要其 Data Prepper 管線所建立的資料，因此請依照您打算使用之應用程式的設定指示操作。

## 相關文件

- 若要為常見資料來源安裝預先設定的儀表板與視覺化，請參閱[整合]({{site.url}}{{site.baseurl}}/dashboards/integrations/index/)。
- 如需部分傳統可觀測性應用程式所需的索引命名慣例與欄位對應，請參閱[可觀測性簡易結構描述]({{site.url}}{{site.baseurl}}/observing-your-data/ss4o/)。
