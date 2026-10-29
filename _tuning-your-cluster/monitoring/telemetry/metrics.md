---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指標"
parent: Telemetry
grand_parent: Monitoring your cluster
nav_order: 10
redirect_from:
  - /monitoring-your-cluster/metrics/
  - /monitoring-your-cluster/metrics/getting-started/
---

# 指標

這是一項實驗性功能，不建議在生產環境中使用。若要了解此功能的最新進度或提供意見回饋，請參閱相關的 [GitHub issue](https://github.com/opensearch-project/OpenSearch/issues/10141)。
{: .warning}

指標框架會記錄叢集作業的計數器、直方圖與量表，並透過 `telemetry-otel` 外掛程式匯出。直方圖支援百分位數，這是 Stats API 未提供的功能，因此您可以找出延遲與資源使用量中的離群值。外掛程式與擴充功能可以使用指標框架 API 新增自己的指標。

## 啟用指標

若要啟用指標，請先啟用遙測功能旗標並安裝 `telemetry-otel` 外掛程式。如需更多資訊，請參閱[啟用遙測]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/telemetry/index/#enabling-telemetry)。

然後在每個節點的 `opensearch.yml` 中新增下列設定，並重新啟動節點：

```yaml
telemetry.feature.metrics.enabled: true
```
{% include copy.html %}

## 設定指標匯出

`telemetry-otel` 外掛程式會在本機彙總指標，並以設定的間隔匯出。若要設定匯出，請在 `opensearch.yml` 中指定下列靜態設定。

設定 | 說明
:--- | :---
`telemetry.otel.metrics.publish.interval` | 匯出指標的間隔。預設為 `60s`。
`telemetry.otel.metrics.exporter.class` | 持久化指標的匯出器。有效值為 `io.opentelemetry.exporter.logging.LoggingMetricExporter`（將指標寫入 logs 目錄中的 `<cluster-name>_otel_metrics.log` 檔案）與 `io.opentelemetry.exporter.otlp.metrics.OtlpGrpcMetricExporter`（使用 gRPC 將指標傳送至 OpenTelemetry Collector）。預設為 `io.opentelemetry.exporter.logging.LoggingMetricExporter`。

若要將指標傳送至 OpenTelemetry Collector，請在每個節點上安裝收集器，並在 `opensearch.yml` 中新增下列設定。預設情況下，匯出器會將指標傳送至 `http://localhost:4317/` 端點：

```yaml
telemetry.otel.metrics.exporter.class: io.opentelemetry.exporter.otlp.metrics.OtlpGrpcMetricExporter
```
{% include copy.html %}

## 支援的指標類型

指標框架支援下列指標類型。

類型 | 說明
:--- | :---
計數器（Counter） | 記錄只會增加的值，例如錯誤數、已處理的位元組數或請求總數。
增減計數器（UpDown counter） | 記錄可增加或減少的值，例如開啟的連線數或作用中的請求數。
直方圖（Histogram） | 記錄值的分佈，例如請求延遲，讓您可以計算百分位數並找出離群值。
非同步量表（Asynchronous gauge） | 每次讀取指標時記錄目前的值，例如 CPU 或記憶體使用率。

## 監控機器學習工作流程
**於 3.1 版推出**
{: .label .label-purple }

ML Commons 會將[機器學習（ML）]({{site.url}}{{site.baseurl}}/ml-commons-plugin/)作業的指標發布至指標框架。每 5 分鐘，一個週期性工作也會收集並匯出叢集中模型與代理程式的狀態。

週期性工作會擷取下列屬性。

資源 | 擷取的屬性
:--- | :---
模型 | 部署類型（遠端、預訓練或自訂）、服務供應商、演算法、模型名稱與模型類型
代理程式 | 大型語言模型（LLM）介面、模型部署類型、服務供應商、模型類型、記憶類型與模型識別碼

以下為擷取的模型指標範例：

```text
{is_hidden=false, service_provider=openai, model=gpt-4o-mini, type=llm, deployment=remote, algorithm=REMOTE}
```

以下為擷取的代理程式指標範例：

```text
{_llm_interface=bedrock/converse/claude, model_deployment=remote, is_hidden=false, model_service_provider=bedrock, model_type=llm, memory_type=conversation_index, model=us.anthropic.claude-sonnet-4-6, type=CONVERSATIONAL}
```

若要啟用 ML 指標，請先[啟用指標](#enabling-metrics)。然後在 `opensearch.yml` 中新增下列設定，並重新啟動節點：

```yaml
plugins.ml_commons.metrics_collection_enabled: true
plugins.ml_commons.metrics_static_collection_enabled: true
```
{% include copy.html %}

`plugins.ml_commons.metrics_collection_enabled` 設定會啟用 ML 作業指標，屬於靜態設定。`plugins.ml_commons.metrics_static_collection_enabled` 設定會啟用週期性工作，屬於動態設定，因此您也可以使用 [Cluster Settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) 進行更新。
