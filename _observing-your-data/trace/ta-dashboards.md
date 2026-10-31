---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenSearch Dashboards 中的追蹤分析"
parent: Trace analytics
grand_parent: Classic observability apps
nav_order: 50
redirect_from:
  - /observability-plugin/trace/ta-dashboards/
  - /monitoring-plugins/trace/ta-dashboards/
---

# OpenSearch Dashboards 中的追蹤分析

追蹤分析可讓您一目了然地掌握應用程式效能，其基礎是 [OpenTelemetry (OTel)](https://opentelemetry.io/) 通訊協定資料，該協定針對從雲端原生軟體收集遙測資料的檢測作業提供標準化。

## 設定 OpenTelemetry 示範

[OpenTelemetry Demo with OpenSearch](https://github.com/opensearch-project/opentelemetry-demo) 會模擬一個分散式應用程式，即時產生遙測資料，提供您一個實用的環境，在將追蹤分析導入您的環境之前，先探索其可用的功能。

### 步驟 1：設定 OpenTelemetry 示範

- 複製 [OpenTelemetry Demo with OpenSearch](https://github.com/opensearch-project/opentelemetry-demo) 儲存庫：`git clone https://github.com/opensearch-project/opentelemetry-demo`。
- 依照 [Getting Started](https://github.com/opensearch-project/opentelemetry-demo/tree/main?tab=readme-ov-file#running-this-demo) 的說明，使用 Docker 部署示範應用程式，該應用程式會執行多個產生遙測資料的微服務。

### 步驟 2：匯入遙測資料

- 使用[現成的設定](https://github.com/opensearch-project/opentelemetry-demo/tree/main/src/otel-collector)，將 OTel 收集器設定為把遙測資料（追蹤、指標、記錄檔）傳送到您的 OpenSearch 叢集。
- 確認 [Data Prepper](https://github.com/opensearch-project/opentelemetry-demo/tree/main/src/dataprepper) 已設定妥當，能夠處理傳入的資料、處理追蹤分析與服務地圖管線、將資料提交至所需的索引，並執行預先彙總的計算。

### 步驟 3：在 OpenSearch Dashboards 中探索追蹤分析

**Trace Analytics** 應用程式提供兩個選項：**Services** 與 **Traces**：

- **Services** 會列出應用程式中的所有服務，並提供一張互動式地圖，顯示各個服務之間的連接方式。與儀表板（依操作協助識別問題）不同，**Service map** 可依據錯誤率與延遲，協助您按服務識別問題。若要存取此選項，請前往 **Trace Analytics** > **Services**。
- **Traces** 會依 HTTP 方法與路徑將追蹤分組，讓您檢視與特定操作相關的平均延遲、錯誤率與趨勢。若要取得更聚焦的檢視，可嘗試依追蹤群組名稱篩選。若要存取此選項，請前往 **Trace Analytics** > **Traces**。在 **Trace Groups** 面板中，您可以檢視某個追蹤群組內的追蹤。在 **Traces** 面板中，您可以分析個別追蹤，以取得詳細摘要。

### 步驟 4：執行關聯分析

選取 **Services correlation** 以顯示遙測訊號之間的關聯。此功能可協助您從邏輯服務層級導覽至特定服務相關的指標與記錄檔。

追蹤分析支援將追蹤區段（span）、追蹤與服務與其對應的記錄檔建立關聯。這讓您可以在 Trace Analytics 介面中，直接從某個追蹤或追蹤區段移至相關的記錄項目，或從某個服務移至其關聯的記錄檔。關聯功能提供遙測資料的統一檢視，簡化了疑難排解流程，讓您更容易找出根本原因並理解應用程式脈絡。

使用下列選項執行關聯：

- **Trace-to-log correlation**：在追蹤詳細資料頁面上，選取 **View associated logs**。
- **Span-to-log correlation**：在追蹤區段詳細資料彈出視窗（在甘特圖或追蹤區段表格中選取追蹤區段 ID 時開啟）中，選取 **View associated logs**。
- **Service-to-log correlation**：在服務頁面上，選取目標服務旁的 **Discover** 圖示。
- **Service-to-service correlation**：在服務頁面上，使用服務地圖中的 **Focus on** 選項，檢視某個服務及其相依項目。

---

## 結構描述相依性與假設

追蹤分析要求您使用 [Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 來處理並視覺化 OTel 資料，並依賴下列 Data Prepper 管線進行 OTel 關聯與服務地圖計算：

- [追蹤分析管線]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/trace-analytics/)
- [服務地圖管線]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/service-map/)

### 標準化的遙測資料

追蹤分析要求遙測資料遵循 OTel 結構描述慣例，包括 OTel 所指定的追蹤區段、追蹤與指標的結構與命名，並且必須以 [Simple Schema for Observability]({{site.url}}{{site.baseurl}}/observing-your-data/ss4o/) 實作。

### 服務名稱與相依性地圖

若要確保服務對應與關聯分析的準確性，請遵循下列準則：

- 服務名稱必須是唯一的，並且在應用程式各元件之間一致使用。
- `serviceName` 欄位必須透過 Data Prepper 管線填入。
- 必須在匯入服務時提供預先定義的上游與下游相依性，才能建立準確的服務地圖並理解服務之間的關係。

### 追蹤與追蹤區段 ID

追蹤與追蹤區段必須在分散式系統之間一致地產生並維護唯一識別碼，才能達成端對端追蹤並取得準確的效能洞見。

### 符合 RED 指標

追蹤分析預期指標資料會包含每個服務的速率（rate）、錯誤（error）與持續時間（duration）（RED）指標，這些指標可以是透過 Data Prepper 管線預先彙總，或依追蹤區段動態計算。如此一來，您就能有效計算並顯示關鍵效能指標。

### 關聯欄位

必須存在某些欄位（例如 `serviceName`），才能執行關聯分析。這些欄位讓追蹤分析能夠連結相關的遙測資料，並提供服務互動與相依性的整體檢視。

### 關聯索引

從服務對話框導覽至其對應的追蹤或記錄檔，需要有關聯欄位存在，並且目標索引（例如記錄檔）必須遵循指定的命名慣例，如 [Simple Schema for Observability]({{site.url}}{{site.baseurl}}/observing-your-data/ss4o/) 所述。

---

## 搭配 OTel 通訊協定分析的追蹤分析

於 2.15 版推出
{: .label .label-purple }

搭配 OTel 通訊協定分析的追蹤分析，可提供分散式系統的全面洞見。您可以視覺化並分析下列資產：

- [Service](https://opentelemetry.io/docs/specs/semconv/resource/#service)：分散式應用程式的組成元件。這些元件是用來衡量與監控應用程式建構基礎的重要邏輯詞彙，以驗證系統的健康狀態。
- [Traces](https://opentelemetry.io/docs/concepts/signals/traces/)：請求在各服務間流經路徑的視覺化呈現，深入揭示延遲與效能問題。
- [RED metrics](https://opentelemetry.io/docs/specs/otel/metrics/api/)：衡量服務健康狀態與效能的指標，以每秒請求數（rate）、失敗請求數（error）與請求處理時間（duration）來衡量。

### 追蹤分析視覺化

**Services** 視覺化（例如表格或地圖）可協助您以邏輯方式分析服務行為與準確性。下列視覺化可協助您找出異常與錯誤：

- **Services 表格**

  - 每個表格欄位都會顯示 RED 指標，以及相連的上游與下游服務和其他動作。下圖為 **Services** 表格的範例。

  ![Services 表格]({{site.url}}{{site.baseurl}}/images/trace-analytics/services-table.png)

  - 一般用途的篩選器選取可用於欄位或篩選條件組合。下圖顯示此篩選器。

  ![Services 篩選器選取]({{site.url}}{{site.baseurl}}/images/trace-analytics/services-filter-selection.png)

  - **Services** 輸送量工具提示可讓您一眼掌握服務過去 24 小時的傳入請求趨勢。下圖為工具提示的範例。

  ![Services 輸送量工具提示 ]({{site.url}}{{site.baseurl}}/images/trace-analytics/service-throughput-tooltip.png)

  - **Services** 關聯對話視窗可讓您一眼掌握服務的詳細資料，包括其 24 小時輸送量趨勢。您可以使用這些詳細資料，依 `serviceName` 欄位進行篩選，以分析相關的記錄檔或追蹤。下圖顯示此視窗。

  ![Services 關聯對話視窗]({{site.url}}{{site.baseurl}}/images/trace-analytics/single-service-correlation-dialog.png)

  - **Services** RED 指標對話視窗可讓您一眼掌握服務的 RED 指標，包括 24 小時的錯誤、持續時間與輸送量比率。下圖顯示此視窗。

  ![Services 持續時間的 RED 指標]({{site.url}}{{site.baseurl}}/images/trace-analytics/single-service-RED-metrics.png)

  - **Span details** 對話視窗提供追蹤的詳細資料。您可以使用此資訊進一步分析追蹤的元素，例如屬性與相關聯的記錄檔。下圖顯示此視窗。

  ![Services Span details 對話視窗]({{site.url}}{{site.baseurl}}/images/trace-analytics/span-details-fly-out.png)

- **服務地圖**

  - **服務地圖** 會顯示節點，每個節點代表一個服務。節點顏色表示該服務及其相依項目的 RED 指標嚴重程度。下圖顯示地圖。

  ![Services 地圖工具提示]({{site.url}}{{site.baseurl}}/images/trace-analytics/service-details-tooltip.png)

  - 您可以選取節點，開啟其相關服務的詳細對話視窗。此互動式地圖會視覺化呈現服務之間的互連關係，協助依服務找出問題，這與依作業找出問題的儀表板不同。您可以依錯誤率或延遲排序，以找出可能的問題區域。

  - 在 **服務地圖** 對話視窗中，節點代表相依於所選服務的相連下游服務。節點顏色表示該服務及其下游相依項目的 RED 指標嚴重程度。下圖顯示此對話視窗。

  ![服務地圖對話視窗]({{site.url}}{{site.baseurl}}/images/trace-analytics/single-service-fly-out.png)

- **追蹤群組**

  - 追蹤會依其 HTTP API 名稱分組，讓您依業務功能單位進行分群。追蹤會依 HTTP 方法與路徑分組，顯示特定作業相關的平均延遲、錯誤率與趨勢。您可以依追蹤群組名稱篩選。下圖顯示 **Trace Groups** 視窗。

  ![Trace Groups 視窗]({{site.url}}{{site.baseurl}}/images/trace-analytics/trace-group-RED-metrics.png)

  - 在 **Trace Groups** 視窗中，您可以依群組名稱及其他篩選器進行篩選。您也可以分析相關聯的追蹤。若要深入檢視組成群組的追蹤，請選取右側欄中的追蹤數量，然後選擇個別追蹤以查看詳細摘要。

  ![追蹤群組對話視窗]({{site.url}}{{site.baseurl}}/images/ta-dashboard.png)

  - **Trace details** 視窗會顯示單一追蹤的明細，包括其對應的追蹤區段、相關聯的服務名稱，以及追蹤區段時間與持續時間互動的瀑布圖。下圖顯示此檢視。

  ![Trace details 視窗]({{site.url}}{{site.baseurl}}/images/ta-trace.png)

## 支援自訂索引名稱與跨叢集索引

於 3.1 版推出  
{: .label .label-purple }

OpenSearch 3.1 的 Trace Analytics 擴充了對自訂索引名稱與跨叢集索引的支援，為分散式環境提供更大的彈性與擴充性。現已提供下列增強功能：

- 您可以為 Observability 的追蹤區段、服務與記錄檔索引設定自訂索引名稱。這可讓您將索引命名方式與組織慣例保持一致，並更有效地管理多個環境中的資料。您也可以設定相關聯的記錄檔索引，並對應其對應的 `timestamp`、`serviceName`、`spanId` 與 `traceId` 欄位。若您的記錄檔未遵循 OpenTelemetry (OTel) 格式且需要自訂欄位對應，此功能特別實用。自訂追蹤區段索引必須遵循 Data Prepper 的追蹤區段索引對應。

  下圖顯示 Observability 設定面板中的自訂索引名稱設定介面。

  ![自訂索引名稱設定 UI]({{site.url}}{{site.baseurl}}/images/ta-index-settings.png)

- **Trace details** 頁面現在包含相關聯的記錄檔面板，可協助您分析與特定追蹤相關聯的記錄檔，以改善疑難排解與根本原因分析。下圖顯示記錄檔面板。

  ![含相關聯記錄檔面板的 Trace details 頁面]({{site.url}}{{site.baseurl}}/images/ta-trace-logs-correlation.png)

- 新的下拉式功能表可讓您檢視所有追蹤區段、根追蹤區段、服務進入追蹤區段或追蹤。自訂資料格線提供進階排序與顯示選項，包括全螢幕模式，讓資料探索更輕鬆，如下圖所示。

  ![Trace Analytics 中的下拉式功能表與自訂資料格線]({{site.url}}{{site.baseurl}}/images/ta-span-kind.png)

- 服務地圖現在會顯示在 **Trace Analytics** 頁面的追蹤表格下方，讓您在分析追蹤資料時，立即以視覺化方式掌握服務關係與相依性。

  ![顯示在追蹤表格下方的服務地圖]({{site.url}}{{site.baseurl}}/images/ta-traces-page.png)

- **Trace details** 頁面提供新的樹狀檢視，可顯示追蹤區段的階層式明細。版面配置已更新，將圓餅圖移至概觀面板旁，讓追蹤指標摘要更直覺，如下圖所示。

  ![含樹狀檢視與圓餅圖版面配置的甘特圖]({{site.url}}{{site.baseurl}}/images/ta-hierarchial-view.png)

- 甘特圖現在包含可選取的迷你地圖，讓您快速瀏覽並聚焦於追蹤時間軸的特定區段，如下圖所示。

  ![含可選取迷你地圖的甘特圖]({{site.url}}{{site.baseurl}}/images/ta-gantt-mini-map.png)

- 服務地圖已重新設計，以更妥善支援大型節點群組，讓複雜的服務拓撲更容易視覺化。您現在可以聚焦於特定服務以檢視其相依性，並視需要重設地圖，如下圖所示。

  ![含大型節點群組的重新設計服務地圖]({{site.url}}{{site.baseurl}}/images/ta-service-map-dependencies.png)

- 服務檢視表格現在包含更多快速選取圖示，讓您在傳遞正確脈絡的情況下，於對應的檢視中查看相關聯的追蹤與記錄檔，並在不離開頁面的情況下查看脈絡中的服務詳細資料，如下圖所示。

  ![服務表格快速選取圖示]({{site.url}}{{site.baseurl}}/images/ta-service-table-icons.png)

## 可設定的服務地圖限制
自 3.2 版起推出  
{: .label .label-purple }

OpenSearch 為服務地圖的呈現提供預設限制。您可以調高這些限制，讓大型拓撲呈現得更完整；或在專注於較小檢視時調低限制，以改善用戶端效能。在服務眾多或互連密集的環境中，這點尤其重要，因為預設限制可能導致地圖不完整。


### 服務地圖組態設定

有兩項 **Advanced Settings** 可控制服務地圖查詢所產生之服務地圖的大小與複雜度：

- `observability:traceAnalyticsServiceMapMaxNodes`：顯示的服務節點數上限。預設為 500。 
- `observability:traceAnalyticsServiceMapMaxEdges`：顯示的邊緣（服務對服務連線）數上限。預設為 1,000。

若要在 OpenSearch Dashboards 中設定這些設定，請依照下列步驟操作：
1. 從主選單中，選取 **Management** > **Dashboard Management** > **Advanced Settings**。
1. 在搜尋方塊中搜尋 `Observability`。在 **Observability** 區段中，找到 **Trace analytics service map maximum edges** 與 *Trace analytics service map maximum nodes** 設定。依您的環境與效能需求調整值，然後儲存變更。值越高，瀏覽器記憶體與 CPU 使用量可能越高。


