---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分散式追蹤"
parent: Trace analytics
nav_order: 65
---

# 分散式追蹤
這是一項實驗性功能，不建議在生產環境中使用。如需此功能進展的最新資訊，或想提供意見回饋，請參閱相關的 [GitHub 議題](https://github.com/opensearch-project/OpenSearch/issues/6750)。    
{: .warning}

分散式追蹤用於監視及偵錯分散式系統。您可以追蹤請求在系統中的流動，並找出效能瓶頸與錯誤。_trace_ 是請求流經分散式系統時完整的端對端路徑。它代表特定作業在分散式架構中穿梭於各種元件與服務的歷程。在分散式追蹤中，單一 trace 包含一系列帶有標記的時間區間，稱為 _span_。Span 具有開始與結束時間，並可能包含其他中繼資料，例如記錄檔或標籤，以協助分類所發生的事件。

分散式追蹤的用途如下：

- **最佳化效能：** 找出並解決瓶頸，降低應用程式的延遲。
- **疑難排解錯誤：** 快速找出分散式系統中錯誤或非預期行為的來源。
- **配置資源：** 藉由了解不同服務的使用模式來最佳化資源配置。
- **視覺化服務相依性：** 將服務之間的相依性視覺化，協助您管理架構。

## 分散式追蹤管線

OpenSearch 提供分散式追蹤管線，可用來匯入、處理及視覺化追蹤資料，並具備查詢與警示功能。[OpenTelemetry](https://opentelemetry.io/) 是開放原始碼的可觀測性架構，提供一組 API、程式庫、代理程式及收集器，用於產生、擷取及匯出遙測資料。分散式追蹤管線包含下列元件：

- **追蹤插碼：** 使用 OpenTelemetry SDK，在您的應用程式碼中加入追蹤功能。
- **傳播：** 在請求於系統中傳播時，將追蹤上下文注入請求中。
- **收集：** 從您的應用程式收集追蹤資料。
- **處理：** 彙總來自多個來源的追蹤資料，並以其他中繼資料擴充。
- **匯出：** 將追蹤資料傳送至後端以進行儲存與分析。

OpenSearch 經常被選為儲存追蹤資料的接收端。

## 追蹤分析

OpenSearch 提供 `trace-analytics` 外掛程式，可即時視覺化追蹤資料。此外掛程式包含預先建置的儀表板，用於分析追蹤資料，例如服務地圖、延遲直方圖及錯誤率。透過 OpenSearch 的分散式追蹤管線，您可以快速找出應用程式中的瓶頸與錯誤。如需詳細資訊，請參閱 [追蹤分析]({{site.url}}{{site.baseurl}}/observing-your-data/trace/index/) 文件。

## 入門

分散式追蹤功能為實驗性功能。若要開始使用分散式追蹤功能，您必須先使用 `opensearch.experimental.feature.telemetry.enabled` 功能旗標啟用該功能，接著使用動態設定 `telemetry.tracer.enabled` 啟用追蹤器。啟用此功能時請務必謹慎，因為它可能會耗用系統資源。啟用及設定分散式追蹤的詳細資訊，包括隨需疑難排解與請求取樣，將於下列各節說明。

### 使用 tarball 在節點上啟用旗標

啟用旗標是透過新的 Java Virtual Machine (JVM) 參數來切換，該參數設定於 `OPENSEARCH_JAVA_OPTS` 或 `config/jvm.options` 中。

#### 選項 1：在 `opensearch.yml` 檔案中啟用實驗性功能旗標

1. 切換至 OpenSearch 安裝的頂層目錄：

   ```bash
   cd \path\to\opensearch
   ```

2. 開啟您的 OpenSearch 組態資料夾，然後以文字編輯器開啟 `opensearch.yml` 檔案。
3. 新增下列這一行：

   ```yaml
   opensearch.experimental.feature.telemetry.enabled: true
   ```
   {% include copy.html %}

4. 儲存您的變更並關閉檔案。

#### 選項 2：修改 jvm.options

在啟動 OpenSearch 程序之前，將下列這幾行新增至 `config/jvm.options`，以啟用此功能及其相依項目：

```bash
-Dopensearch.experimental.feature.telemetry.enabled=true
```
{% include copy.html %}

執行 OpenSearch：

```bash
./bin/opensearch
```
{% include copy.html %}

#### 選項 3：從環境變數啟用

除了直接修改 `config/jvm.options` 之外，您也可以使用環境變數來定義屬性。您可以在啟動 OpenSearch 時以單一命令啟用此功能，或透過設定環境變數來啟用。

若要在啟動 OpenSearch 時內嵌新增這些旗標，請執行下列命令：

```bash
OPENSEARCH_JAVA_OPTS="-Dopensearch.experimental.feature.telemetry.enabled=true" ./bin/opensearch
```
{% include copy.html %}

若要另外定義環境變數，請在執行 OpenSearch 之前執行下列命令：

```bash
export OPENSEARCH_JAVA_OPTS="-Dopensearch.experimental.feature.telemetry.enabled=true"
 ./bin/opensearch
```
{% include copy.html %}

### 使用 Docker 容器啟用

如果您執行 Docker，請在 `environment` 下的 `docker-compose.yml` 中新增下列這一行：

```bash
OPENSEARCH_JAVA_OPTS="-Dopensearch.experimental.feature.telemetry.enabled=true"
```
{% include copy.html %}

### 為 OpenSearch 開發啟用

若要啟用分散式追蹤功能，您必須先在建置 OpenSearch 之前，將正確的屬性新增至 `run.gradle`。如需如何使用 Gradle 建置 OpenSearch 的相關資訊，請參閱 [開發人員指南](https://github.com/opensearch-project/OpenSearch/blob/main/DEVELOPER_GUIDE.md#gradle-build)。

將下列屬性新增至 `run.gradle` 以啟用此功能：

```json
testClusters {
  runTask {
    testDistribution = 'archive'
 if (numZones > 1) numberOfZones = numZones
    if (numNodes > 1) numberOfNodes = numNodes
    systemProperty 'opensearch.experimental.feature.telemetry.enabled', 'true'
    }
 }
 ```
{% include copy.html %}

### 啟用分散式追蹤

啟用功能旗標後，請執行下列操作：

1. 在 `opensearch.yaml` 檔案中新增下列設定，以啟用追蹤架構功能：

   ```yaml
   telemetry.feature.tracer.enabled: true
   ```
   {% include copy.html %}

2. 更新動態 `telemetry.tracer.enabled` 設定，以在執行中的叢集啟用追蹤器：

   ```json
   PUT _cluster/settings
   {
     "persistent": {
       "telemetry.tracer.enabled": true
     }
   }
   ```
   {% include copy-curl.html %}

## 安裝 OpenSearch OpenTelemetry 外掛程式

OpenSearch 分散式追蹤架構旨在透過外掛程式支援各種遙測解決方案。OpenSearch OpenTelemetry 外掛程式 `telemetry-otel` 已可供使用，且必須安裝才能啟用追蹤。下列指南提供安裝指示。

### 匯出器

目前，分散式追蹤功能會為 HTTP 請求及部分傳輸請求產生 trace 與 span。這些 trace 與 span 最初會使用 OpenTelemetry `BatchSpanProcessor` 保留在記憶體中，然後根據已設定的設定值傳送至匯出器。以下是關鍵元件：

1. **Span 處理器：** 當 span 在請求路徑上結束時，OpenTelemetry 會將其提供給 `SpanProcessor` 進行處理與匯出。OpenSearch 分散式追蹤架構使用 `BatchSpanProcessor`，它會將 span 依特定可設定的間隔批次處理，然後傳送至匯出器。`BatchSpanProcessor` 可使用下列組態：
    - `telemetry.otel.tracer.exporter.max_queue_size`：定義佇列大小上限。當佇列達到此值時，便會寫入匯出器。預設為 `2048`。
    - `telemetry.otel.tracer.exporter.delay`：定義延遲，即經過一段時間後，即使佇列中的 span 不足以填滿 `max_queue_size`，仍會排清佇列中的 span。預設為 `2 seconds`。
    - `telemetry.otel.tracer.exporter.batch_size`：設定每次匯出的批次大小上限，以減少輸入/輸出。此值應一律小於 `max_queue_size`。預設為 `512`。
2. **匯出器：** 匯出器負責將資料持久化。OpenTelemetry 提供數個現成的匯出器，而 OpenSearch 支援下列項目：
    - `LoggingSpanExporter`：將 span 匯出至記錄檔，並在記錄目錄中產生獨立的 `_otel_traces.log` 檔案。預設為 `telemetry.otel.tracer.span.exporter.class=io.opentelemetry.exporter.logging.LoggingSpanExporter`。
    - `OtlpGrpcSpanExporter`：透過 gRPC 匯出 span。若要使用此匯出器，您需要在節點上安裝 `otel-collector`。根據預設，它會寫入 http://localhost:4317/ 端點。若要使用此匯出器，請設定下列靜態設定：`telemetry.otel.tracer.span.exporter.class=io.opentelemetry.exporter.otlp.trace.OtlpGrpcSpanExporter`。

### 取樣

分散式追蹤可能會產生大量 span，不必要地耗用系統資源。若要減少 trace 的數量（也稱為 _sample_），您可以設定不同的取樣閾值。根據預設，取樣設定為只包含所有 HTTP 請求的 1%。取樣有下列類型：

1. **起始取樣：** 取樣決策會在起始請求的根 span 之前做出。OpenSearch 支援兩種起始取樣方法：
    - **機率式：** 對傳入請求設定全面限制，可使用 `telemetry.tracer.sampler.probability` 設定動態調整。此設定的範圍介於 0 與 1 之間。預設為 0.01，表示會對 1% 的傳入請求進行取樣。
    - **隨需：** 若要偵錯特定請求，您可以將 `trace=true` 屬性做為 HTTP 標頭的一部分傳送，使這些請求不論機率式取樣設定為何都會被取樣。
2. **尾端取樣：** 若要設定尾端取樣，請依照 [OpenTelemetry 尾端取樣文件](https://opentelemetry.io/docs/concepts/sampling/#tail-sampling) 中的指示操作。組態取決於您選擇的收集器類型。

### 收集 span

`SpanProcessor` 會將 span 寫入匯出器，而匯出器的選擇會定義端點，端點可以是記錄檔或 gRPC。若要使用 gRPC 收集 span，您需要將收集器設定為在每個 OpenSearch 節點上執行的側車程序。收集器可將這些 span 寫入您選擇的接收端，例如 Jaeger、Prometheus、Grafana 或 FileStore，以進行進一步分析。
