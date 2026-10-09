---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Discover 中分析追蹤"
nav_order: 40
parent: Using Discover for observability
---

# 在 Discover 中分析追蹤
**於 3.5 版推出**
{: .label .label-purple }

OpenSearch Dashboards 中的 Discover **Traces** 頁面提供更完善的方式，可在 Observability 外掛程式中探索與分析追蹤資料。此頁面提供處理追蹤資料的專用功能，擴充了傳統的 Discover 體驗。

## 先決條件

使用 **Traces** 頁面之前，請確認您已滿足下列先決條件：

1. **啟用功能旗標**：將下列設定新增至您的 `opensearch_dashboards.yml` 檔案：

   ```yaml
   workspace.enabled: true
   data_source.enabled: true
   explore.enabled: true
   explore.discoverTraces.enabled: true
   ```
   {% include copy.html %}

   更新組態檔案後，請重新啟動 OpenSearch Dashboards，讓變更生效。

2. **建立可觀測性工作區**：您必須在可觀測性工作區中操作。**Traces** 頁面僅適用於此工作區類型。

   注意：工作區與多租用戶功能不相容。若要啟用工作區，您必須先設定 `opensearch_security.multitenancy.enabled: false`，以停用多租用戶功能。
   {: .note}

3. **設定多個資料來源**：您必須設定多個資料來源。如需操作說明，請參閱[多個資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/multi-data-sources/)。

## 存取追蹤頁面

若要存取 **Traces** 頁面：

1. 在 OpenSearch Dashboards 中前往 **Observability** 工作區。
2. 在左側導覽中，展開 **Discover** 並選取 **Traces**，如下圖所示。

![導覽中的 Discover Traces 頁面]({{site.url}}{{site.baseurl}}/images/discover-traces/trace-page.png)

## 設定追蹤資料集

若要設定追蹤資料集，請使用下列其中一個選項。

### 自動建立資料集

如果您的資料來源遵循 OpenTelemetry 命名慣例，**Traces** 頁面可以搜尋符合下列命名模式的索引，自動從您的資料建立追蹤與記錄檔資料集：

- **追蹤**：`otel-v1-apm-span*`
- **關聯記錄檔**：`logs-otel-v1*`

偵測到這些索引時，請選取 **Create Trace Datasets** 按鈕，如下圖所示，以自動產生資料集並建立追蹤與記錄檔之間的關聯關係。

![自動建立追蹤資料集]({{site.url}}{{site.baseurl}}/images/discover-traces/trace-auto-create.png)

### 手動建立資料集

如果您的索引使用不同的命名慣例，您必須手動建立資料集，並設定追蹤與記錄檔之間的關聯關係。前往 **Datasets** 索引標籤，並建立訊號類型為 **Trace** 的資料集。

## 探索追蹤資料

**Traces** 頁面提供完整的工具，可用來分析跨度資料並瞭解追蹤效能，包括：

- **RED 指標**：在頁面頂端檢視速率、錯誤與持續時間（RED）指標，以快速評估追蹤效能與健康狀態。
- **分面欄位**：使用分面欄位篩選器，篩選並分析追蹤的特定面向。
- **跨度表格**：使用可排序的欄與可快速存取詳細資訊的功能來瀏覽跨度。

### 檢視特定跨度

若要檢視特定跨度的詳細資訊，請選取跨度表格中的時間戳記。這會開啟 **Trace Details** 浮出面板，如下圖所示。

![追蹤詳細資訊浮出面板]({{site.url}}{{site.baseurl}}/images/discover-traces/trace-details-flyout.png)

**Trace Details** 浮出面板會顯示下列資訊：

- 所選跨度在其父追蹤中的關係。
- 顯示該跨度與同一追蹤中其他跨度之間關係的階層結構。
- 跨度屬性與中繼資料。

### 追蹤詳細資訊頁面

若要從 **Trace Details** 浮出面板存取完整的追蹤詳細資訊頁面，請使用下列其中一個選項：

- 在 **Traces** 頁面表格中選取 **span ID**。
- 在浮出面板中選取 **Open full page**。

完整頁面檢視提供更寬廣的介面，可進行更深入的追蹤分析，其中包含時間軸視覺化，顯示跨度之間的階層關係與持續時間，並在側邊面板中提供詳細的跨度資訊，如下圖所示。

![包含 RED 指標與面向欄位的 Discover Traces 頁面]({{site.url}}{{site.baseurl}}/images/discover-traces/trace-detail-page.png)

## 建立追蹤與記錄檔的關聯

**Traces** 頁面與記錄資料無縫整合，讓您能夠從追蹤前往相關記錄檔，同時保留適當的上下文。

### 檢視相關記錄檔

若要檢視相關記錄檔，請依照下列步驟操作：

1. 在 **Trace Details** 浮出面板中，找到 **Related logs** 區段。 
1. 選取 **View in Discover Logs** 按鈕，前往與所選追蹤關聯的記錄項目，如下圖所示。

![追蹤詳細資訊中的相關記錄檔按鈕]({{site.url}}{{site.baseurl}}/images/discover-traces/related-logs.png)

### 保留上下文的記錄檔重新導向

當您選取 **View in Discover Logs** 時，OpenSearch Dashboards 會自動將您重新導向至已套用追蹤上下文的 **Logs** 頁面，如下圖所示。 

![包含追蹤上下文的 Discover Logs 頁面]({{site.url}}{{site.baseurl}}/images/discover-traces/logs-redirection.png)

記錄檔經過篩選，只會顯示與所選追蹤相關的項目，讓您更容易排解問題並瞭解追蹤事件的完整上下文。保留上下文可提供遙測資料的統一檢視，簡化偵錯流程，協助您找出根本原因並全面瞭解應用程式的行為。
