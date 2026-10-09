---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "應用程式效能監控"
nav_order: 45
has_children: true
has_toc: false
redirect_from:
   - /observing-your-data/apm/
---

# 應用程式效能監控
**3.6 版新增**
{: .label .label-purple }

應用程式效能監控 (Application Performance Monitoring, APM) 結合服務拓撲資料與 Rate、Errors、Duration (RED) 指標，為您的分散式應用程式提供即時監控。APM 提供服務健康狀態的統一檢視，讓您能快速識別微服務架構中的效能瓶頸與故障。

## APM 架構

下圖顯示 APM 架構。

![APM 架構]({{site.url}}{{site.baseurl}}/images/apm/architecture.png)

APM 使用下列資料管線來收集、處理及視覺化應用程式遙測資料：

1. **[OpenTelemetry SDKs](https://opentelemetry.io/docs/instrumentation/)** 會對您的應用程式程式碼進行埋設，以產生追蹤、記錄檔與指標。
2. **[OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)** 透過 OTLP (連接埠 4317 上的 gRPC 或連接埠 4318 上的 HTTP) 接收遙測資料，進行處理後將其路由至 Data Prepper 與 Prometheus。
3. **[OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/)** 處理追蹤資料，並使用 [`otel_apm_service_map` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/otel-apm-service-map/) 產生服務地圖與 RED 指標。
4. **OpenSearch** 儲存追蹤資料、記錄檔與服務拓撲資訊。
5. **Prometheus** 透過遠端寫入儲存時間序列 RED 指標。
6. **OpenSearch Dashboards** 提供用於視覺化與分析的 APM 使用者介面。

## 設定 APM

若要設定 APM，請完成下列步驟：

1. **建立可觀測性工作區**：APM 功能僅在 Observability 工作區內可用。若要瞭解如何啟用與建立工作區，請參閱 [OpenSearch Dashboards 工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace/)。

2. **啟用功能旗標**：將下列設定新增至您的 `opensearch_dashboards.yml` 檔案：

   ```yaml
   workspace.enabled: true
   data_source.enabled: true
   explore.enabled: true
   explore.discoverTraces.enabled: true
   explore.discoverMetrics.enabled: true
   ```
   {% include copy.html %}

3. **對應用程式進行埋設**：將 [OpenTelemetry SDKs](https://opentelemetry.io/docs/instrumentation/) 整合至您的應用程式程式碼，以產生追蹤與記錄資料。

4. **設定遙測資料匯入**：設定 OpenTelemetry Collector 與 Data Prepper，以處理遙測資料並將其路由至 OpenSearch 與 Prometheus。請參閱 [設定遙測資料匯入]({{site.url}}{{site.baseurl}}/observing-your-data/apm/configuring-telemetry-ingestion/)。

5. **在 OpenSearch Dashboards 中設定 APM**：在您的 Observability 工作區中建立資料集、索引模式，並連接資料來源。請參閱 [在 OpenSearch Dashboards 中設定 APM]({{site.url}}{{site.baseurl}}/observing-your-data/apm/configuring-apm/)。

## 使用 APM

完成設定步驟後，請使用下列 APM 頁面來監控您的服務：

- [**Services**]({{site.url}}{{site.baseurl}}/observing-your-data/apm/services/)：檢視所有已埋設服務的集中式目錄，包含關鍵效能指標、每個作業的指標與相依性資訊。
- [**Application map**]({{site.url}}{{site.baseurl}}/observing-your-data/apm/application-map/)：探索由追蹤資料自動產生的互動式拓撲視覺化，並在每個服務節點上疊加 RED 指標。

APM 與較舊的 [Application analytics]({{site.url}}{{site.baseurl}}/observing-your-data/app-analytics/) 及 [Trace analytics]({{site.url}}{{site.baseurl}}/observing-your-data/trace/index/) 功能不同。APM 提供更整合的體驗，將服務拓撲、RED 指標與情境內關聯性結合為單一工作流程。
{: .note}

## 後續步驟

- [設定遙測資料匯入]({{site.url}}{{site.baseurl}}/observing-your-data/apm/configuring-telemetry-ingestion/)：設定 OpenTelemetry Collector 與 Data Prepper，以處理遙測資料並將其路由至 OpenSearch 與 Prometheus。