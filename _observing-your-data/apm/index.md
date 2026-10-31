---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "應用程式效能監控"
parent: Observability workspace apps
nav_order: 50
has_children: true
has_toc: false
redirect_from:
   - /observing-your-data/apm/
---

# 應用程式效能監控 (Application performance monitoring)
**於 3.6 版導入**
{: .label .label-purple }

應用程式效能監控 (Application Performance Monitoring, APM) 結合服務拓撲資料與 Rate、Errors、Duration (RED) 指標，為您的分散式應用程式提供即時監控。APM 提供統一的服務健康狀態檢視，讓您能快速識別微服務架構中的效能瓶頸與故障。

## 必要條件

APM 需要下列元件：

- 一個已啟用可觀測性工作區與 APM 設定的 OpenSearch 叢集及 OpenSearch Dashboards。如需詳細資訊，請參閱 [Observability workspace apps]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/)。
- 一個 [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)。
- [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/)。
- [Prometheus](https://prometheus.io/)，作為指標儲存空間，並以 [Prometheus 資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/connect-prometheus/)連接至 OpenSearch。
- 已使用 [OpenTelemetry](https://opentelemetry.io/docs/instrumentation/) 埋裝監控程式碼的應用程式。

## APM 架構

下圖顯示 APM 架構。

![APM architecture]({{site.url}}{{site.baseurl}}/images/apm/architecture.png)

APM 使用下列資料管線來收集、處理並視覺化應用程式遙測資料：

1. **[OpenTelemetry SDKs](https://opentelemetry.io/docs/instrumentation/)** 為您的應用程式程式碼埋裝監控程式碼，以產生追蹤、記錄檔與指標。
2. **[OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)** 透過 OTLP (gRPC 連接埠 4317 或 HTTP 連接埠 4318) 接收遙測資料，進行處理後路由至 Data Prepper 與 Prometheus。
3. **[OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/)** 處理追蹤資料，並使用 [`otel_apm_service_map` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/otel-apm-service-map/)產生服務地圖與 RED 指標。
4. **OpenSearch** 儲存追蹤資料、記錄檔與服務拓撲資訊。
5. **Prometheus** 透過遠端寫入儲存時間序列 RED 指標。
6. **OpenSearch Dashboards** 提供用於視覺化與分析的 APM 使用者介面。

## 設定 APM

若要設定 APM，請完成下列步驟：

1. **建立可觀測性工作區**：APM 功能僅可在可觀測性工作區內使用。若要了解如何啟用與建立工作區，請參閱 [Workspace for OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace/)。

2. **啟用功能旗標**：在您的 `opensearch_dashboards.yml` 檔案中加入以下設定：

   ```yaml
   workspace.enabled: true
   explore.enabled: true
   explore.discoverTraces.enabled: true
   explore.discoverMetrics.enabled: true
   ```
   {% include copy.html %}

3. **埋裝應用程式**：將 [OpenTelemetry SDKs](https://opentelemetry.io/docs/instrumentation/) 整合至您的應用程式程式碼，以產生追蹤與記錄資料。

4. **設定遙測匯入**：設定 OpenTelemetry Collector 與 Data Prepper，以處理遙測資料並路由至 OpenSearch 與 Prometheus。請參閱 [Configuring telemetry ingestion]({{site.url}}{{site.baseurl}}/observing-your-data/apm/configuring-telemetry-ingestion/)。

5. **在 OpenSearch Dashboards 中設定 APM**：在您的可觀測性工作區中建立資料集、索引模式，並連接資料來源。請參閱 [Configuring APM in OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/observing-your-data/apm/configuring-apm/)。

## 使用 APM

完成設定步驟後，使用下列 APM 頁面來監控您的服務：

- [**Services**]({{site.url}}{{site.baseurl}}/observing-your-data/apm/services/)：檢視所有已埋裝服務的集中式目錄，包含關鍵效能指標、每個 operation 的指標與相依性資訊。
- [**Topology map**]({{site.url}}{{site.baseurl}}/observing-your-data/apm/application-map/)：探索由追蹤資料自動產生的互動式拓撲視覺化，並在每個服務節點上疊加 RED 指標。

APM 與較舊的 [Application analytics]({{site.url}}{{site.baseurl}}/observing-your-data/app-analytics/) 及 [Trace analytics]({{site.url}}{{site.baseurl}}/observing-your-data/trace/index/) 功能不同。APM 提供更整合的體驗，將服務拓撲、RED 指標與脈絡內關聯合併為單一工作流程。
{: .note}

## 後續步驟

- [Configuring telemetry ingestion]({{site.url}}{{site.baseurl}}/observing-your-data/apm/configuring-telemetry-ingestion/)：設定 OpenTelemetry Collector 與 Data Prepper，以處理遙測資料並路由至 OpenSearch 與 Prometheus。