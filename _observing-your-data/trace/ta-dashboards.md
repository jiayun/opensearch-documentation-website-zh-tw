---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenSearch Dashboards 的 Trace Analytics 外掛程式"
parent: Trace analytics
nav_order: 50
redirect_from:
  - /observability-plugin/trace/ta-dashboards/
  - /monitoring-plugins/trace/ta-dashboards/
---

# OpenSearch Dashboards 中的 Trace Analytics

Trace Analytics 外掛程式以 [OpenTelemetry (OTel)](https://opentelemetry.io/) 通訊協定資料為基礎，讓您一眼掌握應用程式效能；該通訊協定將雲端原生軟體收集遙測資料所需的插樁方式標準化。

## 安裝外掛程式

請參閱[獨立 OpenSearch Dashboards 外掛程式安裝]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/plugins/)，了解如何安裝 Trace Analytics 外掛程式。

## 設定 OpenTelemetry 示範

[OpenTelemetry Demo with OpenSearch](https://github.com/opensearch-project/opentelemetry-demo) 會模擬一個產生即時遙測資料的分散式應用程式，提供您一個實用的環境，讓您在實際於自己的環境中實作 Trace Analytics 外掛程式之前，先探索其可用功能。

### 步驟 1：設定 OpenTelemetry 示範

- 複製 [OpenTelemetry Demo with OpenSearch](https://github.com/opensearch-project/opentelemetry-demo) 儲存庫：`git clone https://github.com/opensearch-project/opentelemetry-demo`。
- 依照[入門](https://github.com/opensearch-project/opentelemetry-demo/tree/main?tab=readme-ov-file#running-this-demo)指示，使用 Docker 部署示範應用程式，該應用程式會執行多個產生遙測資料的微服務。

### 步驟 2：匯入遙測資料

- 使用[既有設定](https://github.com/opensearch-project/opentelemetry-demo/tree/main/src/otel-collector)，設定 OTel 收集器以將遙測資料 (追蹤、指標、記錄檔) 傳送至您的 OpenSearch 叢集。
- 確認已設定 [Data Prepper](https://github.com/opensearch-project/opentelemetry-demo/tree/main/src/dataprepper) 來處理傳入的資料、處理追蹤分析與服務地圖管線、將資料提交至必要的索引，並執行預先彙總的計算。

### 步驟 3：在 OpenSearch Dashboards 中探索追蹤分析

**Trace Analytics** 應用程式包含兩個選項：**Services** 與 **Traces**：

- **Services** 會列出應用程式中的所有服務，並提供互動式地圖，顯示各種服務之間的連線方式。與儀表板 (可依作業協助找出問題) 不同，**Service map** 可協助您依服務並根據錯誤率與延遲來找出問題。若要存取此選項，請前往 **Trace Analytics** > **Services**。
- **Traces** 會依 HTTP 方法與路徑將追蹤分組，讓您查看與特定作業相關的平均延遲、錯誤率及趨勢。若想獲得更聚焦的檢視，請嘗試依追蹤群組名稱篩選。若要存取此選項，請前往 **Trace Analytics** > **Traces**。您可以從 **Trace Groups** 面板檢閱追蹤群組中的追蹤。您可以從 **Traces** 面板分析個別追蹤，以取得詳細摘要。

### 步驟 4：執行關聯分析

選取 **Services correlation** 以顯示遙測訊號之間的關係。此功能可協助您從邏輯服務層級，瀏覽至特定服務的相關指標與記錄檔。

Trace Analytics 外掛程式支援將 span、追蹤與服務和其對應的記錄檔建立關聯。這可讓您在 Trace Analytics 介面中，直接從追蹤或 span 移至相關的記錄項目，或從服務移至其相關的記錄檔。關聯功能提供遙測資料的統一檢視，簡化疑難排解，讓您更容易找出根本原因並了解應用程式內容。

使用下列選項執行關聯：

- **Trace-to-log correlation**：在追蹤詳細資料頁面上，選取 **View associated logs**。
- **Span-to-log correlation**：在 span 詳細資料飛出視窗中 (透過在甘特圖或 span 表格中選取 span ID 開啟)，選取 **View associated logs**。
- **Service-to-log correlation**：在服務頁面上，選取所需服務旁的 **Discover** 圖示。
- **Service-to-service correlation**：在服務頁面上，使用服務地圖中的 **Focus on** 選項，以檢視服務及其相依性。

---

## 結構描述相依性與假設

此外掛程式要求您使用 [Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 來處理及視覺化 OTel 資料，並依賴下列 Data Prepper 管線來進行 OTel 關聯與服務地圖計算：

- [追蹤分析管線]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/trace-analytics/)
- [服務地圖管線]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/service-map/)

### 標準化遙測資料

此外掛程式要求遙測資料遵循 OTel 結構描述慣例，包括 OTel 所指定的 span、追蹤與指標的結構與命名，並使用 [Simple Schema for Observability]({{site.url}}{{site.baseurl}}/observing-your-data/ss4o/) 來實作。

### 服務名稱與相依性對應

為進行準確的服務對應與關聯分析，請遵循下列準則：

- 服務名稱必須是唯一的，並在應用程式元件之間一致使用。
- `serviceName` 欄位必須使用 Data Prepper 管線填入。
- 匯入服務時，必須一併匯入預先定義的上游與下游相依性，才能建構準確的服務地圖並了解服務關係。

### 追蹤與 span ID

追蹤與 span 必須在分散式系統中一致地產生並維護唯一識別碼，才能進行端對端追蹤並取得準確的效能見解。

### 遵循 RED 指標

此外掛程式預期指標資料會包含每個服務的速率、錯誤與持續時間（RED）指標，這些指標可透過 Data Prepper 管線預先彙總，或根據 span 動態計算。這可讓您有效計算並顯示關鍵效能指標。

### 關聯欄位

必須有特定欄位 (例如 `serviceName`) 才能執行關聯分析。這些欄位可讓外掛程式連結相關的遙測資料，並提供服務互動與相依性的整體檢視。

### 關聯索引

若要從服務對話方塊瀏覽至其對應的追蹤或記錄檔，必須有相互關聯的欄位，且目標索引 (例如記錄檔) 必須遵循指定的命名慣例，如 [Simple Schema for Observability]({{site.url}}{{site.baseurl}}/observing-your-data/ss4o/) 所述。

---

## 使用 OTel 通訊協定分析的追蹤分析

於 2.15 版推出
{: .label .label-purple }

使用 OTel 通訊協定分析的追蹤分析可提供分散式系統的完整見解。您可以視覺化並分析下列資產：

- [服務](https://opentelemetry.io/docs/specs/semconv/resource/#service)：分散式應用程式的元件。這些元件是重要的邏輯詞彙，用於測量及監視應用程式的建構組塊，以驗證系統的健康狀態。
- [追蹤](https://opentelemetry.io/docs/concepts/signals/traces/)：請求跨服務路徑的視覺化呈現，將其轉化為請求跨服務的歷程，可深入了解延遲與效能問題。
- [RED 指標](https://opentelemetry.io/docs/specs/otel/metrics/api/)：服務健康狀態與效能的指標，以每秒請求數 (rate)、失敗的請求 (errors) 及請求處理時間 (duration) 來衡量。

### 追蹤分析視覺化

**Services** 視覺化 (例如表格或地圖) 可協助您以邏輯方式分析服務行為與準確性。下列視覺化可協助您識別異常與錯誤：

- **服務表格**

  - 每個表格欄位都會顯示 RED 指標，以及連接的上游與下游服務和其他動作。下圖顯示 **Services** 表格範例。

  ![服務表格]({{site.url}}{{site.baseurl}}/images/trace-analytics/services-table.png)

  - 通用篩選選擇用於組合欄位或篩選條件。下圖顯示此篩選器。

  ![服務篩選選擇]({{site.url}}{{site.baseurl}}/images/trace-analytics/services-filter-selection.png)

  - **Services** 輸送量工具提示可讓您一目了然地檢視服務過去 24 小時的傳入請求趨勢。下圖顯示工具提示範例。

  ![服務輸送量工具提示]({{site.url}}{{site.baseurl}}/images/trace-analytics/service-throughput-tooltip.png)

  - **Services** 相關性對話視窗可讓您一目了然地檢視服務的詳細資訊，包括其 24 小時輸送量趨勢。您可以使用這些詳細資訊，根據 `serviceName` 欄位進行篩選，以分析相互關聯的記錄檔或追蹤。下圖顯示此視窗。

  ![服務相關性對話視窗]({{site.url}}{{site.baseurl}}/images/trace-analytics/single-service-correlation-dialog.png)

  - **Services** RED 指標對話視窗可讓您一目了然地檢視服務的 RED 指標，包括 24 小時的錯誤、持續時間與輸送率。下圖顯示此視窗。

  ![服務持續時間的 RED 指標]({{site.url}}{{site.baseurl}}/images/trace-analytics/single-service-RED-metrics.png)

  - **Span details** 對話視窗提供追蹤的詳細資訊。您可以使用這些資訊進一步分析追蹤的元素，例如屬性與相關聯的記錄檔。下圖顯示此視窗。

  ![服務 Span 詳細資料對話視窗]({{site.url}}{{site.baseurl}}/images/trace-analytics/span-details-fly-out.png)

- **Service map**

  - **Service map** 顯示各個節點，每個節點代表一項服務。節點顏色表示該服務及其相依項目的 RED 指標嚴重程度。下圖顯示一個地圖。

  ![服務地圖工具提示]({{site.url}}{{site.baseurl}}/images/trace-analytics/service-details-tooltip.png)

  - 您可以選取節點，開啟其相關聯服務的詳細對話視窗。此互動式地圖可視覺化服務之間的相互連接，協助您依服務識別問題，不同於依操作識別問題的儀表板。您可以依錯誤率或延遲排序，以找出潛在的問題區域。

  - 在 **Service map** 對話視窗中，節點代表相依於所選服務的已連接下游服務。節點顏色表示該服務及其下游相依項目的 RED 指標嚴重程度。下圖顯示此對話視窗。

  ![服務地圖對話視窗]({{site.url}}{{site.baseurl}}/images/trace-analytics/single-service-fly-out.png)

- **追蹤群組**

  - 追蹤會依其 HTTP API 名稱分組，以便依業務功能單位將追蹤歸類。追蹤會依 HTTP 方法與路徑分組，顯示與特定操作相關聯的平均延遲、錯誤率與趨勢。您可以依追蹤群組名稱篩選。下圖顯示 **Trace Groups** 視窗。

  ![追蹤群組視窗]({{site.url}}{{site.baseurl}}/images/trace-analytics/trace-group-RED-metrics.png)

  - 在 **Trace Groups** 視窗中，您可以依群組名稱與其他條件篩選。您也可以分析相關聯的追蹤。若要深入檢視組成群組的追蹤，請選取右側欄位中的追蹤數量，然後選擇個別追蹤以查看詳細摘要。

  ![追蹤群組對話視窗]({{site.url}}{{site.baseurl}}/images/ta-dashboard.png)

  - **Trace details** 視窗顯示單一追蹤的細部分解，包括其對應的 span、相關聯的服務名稱，以及 span 時間與持續時間互動的瀑布圖。下圖顯示此檢視。

  ![追蹤詳細資料視窗]({{site.url}}{{site.baseurl}}/images/ta-trace.png)

## 支援自訂索引名稱與跨叢集索引

於 3.1 版推出  
{: .label .label-purple }

OpenSearch 3.1 的 Trace Analytics 擴充了對自訂索引名稱與跨叢集索引的支援，為分散式環境提供更大的彈性與擴充性。現在提供下列強化功能：

- 您可以為 Observability 的 span、服務與記錄索引設定自訂索引名稱。這可讓索引命名符合您組織的慣例，並更有效地管理多個環境之間的資料。您也可以設定相互關聯的記錄索引，並為 `timestamp`、`serviceName`、`spanId` 與 `traceId` 對應其相應的欄位。如果您的記錄檔不符合 OpenTelemetry (OTel) 格式且需要自訂欄位對應，此功能特別有用。自訂 span 索引必須遵循 Data Prepper 的 span 索引對應。

  下圖顯示 Observability 設定面板中的自訂索引名稱組態介面。

  ![自訂索引名稱組態介面]({{site.url}}{{site.baseurl}}/images/ta-index-settings.png)

- **Trace details** 頁面現在包含相關聯記錄檔面板，可協助您分析與特定追蹤相互關聯的記錄檔，以改善疑難排解與根本原因分析。下圖顯示記錄檔面板。

  ![含相關聯記錄檔面板的追蹤詳細資料頁面]({{site.url}}{{site.baseurl}}/images/ta-trace-logs-correlation.png)

- 新的下拉式選單可讓您檢視所有 span、根 span、服務進入 span 或追蹤。自訂資料格線提供進階排序與顯示選項，包括便於探索資料的全螢幕模式，如下圖所示。

  ![Trace Analytics 中的下拉式選單與自訂資料格線]({{site.url}}{{site.baseurl}}/images/ta-span-kind.png)

- 服務地圖現在顯示在 **Trace Analytics** 頁面的追蹤表格下方，在您分析追蹤資料時，可立即提供服務關係與相依性的視覺化內容。

  ![顯示在追蹤表格下方的服務地圖]({{site.url}}{{site.baseurl}}/images/ta-traces-page.png)

- **Trace details** 頁面新增了樹狀檢視，可顯示 span 的階層式分解。版面配置已更新，將圓餅圖放置在概觀面板旁邊，以更直觀地摘要追蹤指標，如下圖所示。

  ![含樹狀檢視與圓餅圖版面配置的甘特圖]({{site.url}}{{site.baseurl}}/images/ta-hierarchial-view.png)

- 甘特圖現在包含可選取的迷你地圖，讓您能快速導覽並聚焦於追蹤時間軸的特定區段，如下圖所示。

  ![含可選取迷你地圖的甘特圖]({{site.url}}{{site.baseurl}}/images/ta-gantt-mini-map.png)

- 服務地圖已重新設計，以更妥善支援大型節點群組，讓複雜的服務拓撲更容易視覺化。您現在可以聚焦於特定服務以檢視其相依項目，並視需要重設地圖，如下圖所示。

  ![重新設計的大型節點群組服務地圖]({{site.url}}{{site.baseurl}}/images/ta-service-map-dependencies.png)

- 服務檢視表格現在包含更多快速選取圖示，讓您可以在對應的檢視中查看相互關聯的追蹤與記錄檔，並傳入正確的脈絡資訊；您也可以不離開頁面，就在目前脈絡中查看服務詳細資訊，如下圖所示。

  ![服務表格快速選取圖示]({{site.url}}{{site.baseurl}}/images/ta-service-table-icons.png)

## 可設定的服務地圖限制
於 3.2 版推出  
{: .label .label-purple }

OpenSearch 為服務地圖的呈現提供預設限制。您可以提高這些限制，以更完整地呈現大型拓撲，或降低限制，在專注於較小檢視時改善用戶端效能。這在擁有大量服務或緊密互連的環境中尤其重要，因為預設限制可能導致地圖不完整。


### 服務地圖組態設定

有兩項 **Advanced Settings** 可控制服務地圖查詢所產生地圖的大小與複雜度：

- `observability:traceAnalyticsServiceMapMaxNodes`：顯示的服務節點數量上限。預設為 500。 
- `observability:traceAnalyticsServiceMapMaxEdges`：顯示的邊（服務之間的連線）數量上限。預設為 1,000。

若要在 OpenSearch Dashboards 中設定這些設定，請依照下列步驟操作：
1. 從主選單選取 **Management** > **Dashboard Management** > **Advanced Settings**。
1. 在搜尋方塊中搜尋 `Observability`。在 **Observability** 區段中，找到 **Trace analytics service map maximum edges** 與 *Trace analytics service map maximum nodes** 設定。根據您的環境與效能需求調整數值，然後儲存變更。較高的數值可能會增加瀏覽器的記憶體與 CPU 用量。


