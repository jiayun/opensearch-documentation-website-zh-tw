---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "追蹤"
nav_order: 30
parent: Application performance monitoring
grand_parent: Observability workspace apps
---

# 在 Discover 中分析追蹤
**3.5 版推出**
{: .label .label-purple }

OpenSearch Dashboards 中的 Discover **Traces** 頁面提供強化方式，讓您在可觀測性工作區中探索與分析追蹤資料。此頁面透過專為追蹤資料設計的專屬功能，延伸傳統的 Discover 體驗。

## 先決條件

使用 **Traces** 頁面前，請確認您已符合下列先決條件：

1. **啟用功能旗標**：將下列設定新增至您的 `opensearch_dashboards.yml` 檔案：

   ```yaml
   workspace.enabled: true
   explore.enabled: true
   explore.discoverTraces.enabled: true
   ```
   {% include copy.html %}

   更新組態檔案後，請重新啟動 OpenSearch Dashboards 讓變更生效。

2. **建立可觀測性工作區**：您必須在可觀測性工作區中作業。**Traces** 頁面僅在此工作區類型中提供。

   注意：工作區與多租用戶不相容。若要啟用工作區，您必須先設定 `opensearch_security.multitenancy.enabled: false` 以停用多租用戶。
   {: .note}

3. **設定追蹤資料集**：您必須至少設定一個追蹤資料集。如需詳細指示，請參閱[資料集]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/datasets/)。

## 存取追蹤頁面

若要存取 **Traces** 頁面：

1. 在 OpenSearch Dashboards 中瀏覽至 **Observability** 工作區。
2. 在左側導覽中，選取 **Application performance** > **Traces**。

![導覽中的 Discover Traces 頁面]({{site.url}}{{site.baseurl}}/images/discover-traces/trace-page.png)

## 設定追蹤資料集

若要設定追蹤資料集，請使用下列其中一個選項。

### 自動建立資料集

若您的資料來源遵循 OpenTelemetry 命名慣例，**Traces** 頁面可透過搜尋符合下列命名模式的索引，自動從您的資料建立追蹤與記錄檔資料集：

- **追蹤**：`otel-v1-apm-span*`
- **相關記錄檔**：`logs-otel-v1*`

偵測到這些索引後，請選取 **Create Trace Datasets** 按鈕（如下圖所示），以自動產生資料集並建立追蹤與記錄檔之間的關聯關係。

![自動建立追蹤資料集]({{site.url}}{{site.baseurl}}/images/discover-traces/trace-auto-create.png)

### 手動建立資料集

若您的索引使用不同的命名慣例，您必須手動建立資料集，並設定追蹤與記錄檔之間的關聯關係。瀏覽至 **Datasets** 索引標籤，並建立信號類型為 **Trace** 的資料集。

## 探索追蹤資料

**Traces** 頁面提供完整的工具，可分析 span 資料並瞭解追蹤效能，包括：

- **RED 指標**：在頁面頂端檢視速率、錯誤與持續時間（RED）指標，以快速評估追蹤效能與健康狀態。
- **多面向欄位**：使用多面向欄位篩選器，篩選並分析追蹤的特定層面。
- **Span 表格**：使用可排序的欄瀏覽 span，並快速存取詳細資訊。

### 檢視特定 span

若要檢視特定 span 的詳細資訊，請選取 span 表格中的時間戳記。這會開啟 **Trace Details** 飛出視窗，如下圖所示。

![追蹤詳細資料飛出視窗]({{site.url}}{{site.baseurl}}/images/discover-traces/trace-details-flyout.png)

**Trace Details** 飛出視窗會顯示下列資訊：

- 所選 span 在其父追蹤中的關係。
- 顯示該 span 與同一追蹤中其他 span 關係的階層結構。
- span 屬性與中繼資料。

### 追蹤詳細資料頁面

若要從 **Trace Details** 飛出視窗存取完整的追蹤詳細資料頁面，請使用下列其中一個選項：

- 從 **Traces** 頁面表格中選取 **span ID**。
- 從飛出視窗中選取 **Open full page**。

完整頁面檢視提供擴充的介面，可進行更深入的追蹤分析，包含顯示階層式 span 關係與持續時間的時間軸視覺化，以及側邊面板中的詳細 span 資訊，如下圖所示。

![含 RED 指標與多面向欄位的 Discover Traces 頁面]({{site.url}}{{site.baseurl}}/images/discover-traces/trace-detail-page.png)

## 將追蹤與記錄檔建立關聯

**Traces** 頁面可與記錄資料順暢整合，讓您從追蹤導覽至相關記錄檔，同時保留適當的脈絡。

### 檢視相關記錄檔

若要檢視相關記錄檔，請依照下列步驟：

1. 在 **Trace Details** 飛出視窗中，找到 **Related logs** 區段。 
1. 選取 **View in Discover Logs** 按鈕，導覽至所選追蹤的相關記錄項目，如下圖所示。

![追蹤詳細資料中的相關記錄檔按鈕]({{site.url}}{{site.baseurl}}/images/discover-traces/related-logs.png)

### 帶有脈絡的記錄檔重新導向

當您選取 **View in Discover Logs** 時，OpenSearch Dashboards 會自動將您重新導向至已套用追蹤脈絡的 **Logs** 頁面，如下圖所示。 

![帶有追蹤脈絡的 Discover Logs 頁面]({{site.url}}{{site.baseurl}}/images/discover-traces/logs-redirection.png)

記錄檔會經過篩選，僅顯示與所選追蹤相關的項目，讓您更輕鬆地疑難排解問題，並瞭解追蹤事件的完整脈絡。保留脈絡可透過提供遙測資料的統一檢視來簡化偵錯流程，協助您找出根本原因，並掌握應用程式行為的完整全貌。
