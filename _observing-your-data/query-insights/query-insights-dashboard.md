---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
title: "查詢深入解析儀表板"
layout: default
parent: Query insights
nav_order: 60
---

# 查詢深入解析儀表板

您可以在 OpenSearch Dashboards 中與查詢深入解析功能互動。這能為您提供即時與歷史的查詢效能洞察，透過分析與監控協助您改善叢集中查詢的執行方式。

## 導覽

登入 OpenSearch Dashboards 後，前往 **OpenSearch Plugins** > **Query insights** 即可找到 **Query insights** 頁面。

如果您已啟用[多個資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/multi-data-sources/)，請前往 **Data administration** > **Performance** > **Query insights** 來找到 **Query insights** 頁面。
{: .note}

**Query insights** 儀表板包含下列頁面：

- [Top N queries](#top-n-queries)：顯示熱門查詢的查詢指標與詳細資料。
- [Query details](#query-details)：顯示個別查詢與查詢群組的詳細資料。
- [Configuration](#configuration)：自訂查詢深入解析功能的所有監控與資料保留設定。
- [Live queries](#live-queries)：即時監控目前正在執行的查詢。


## 前 N 大查詢

**Top N queries** 頁面提供對系統資源或效能影響最大的查詢的詳細概覽。您可以在該頁面分析 **latency**、**CPU time** 與 **memory usage** 等查詢指標。

以下 **Top N queries** 頁面的圖片包含每個元件的字母標籤。

![前 N 大查詢介面]({{site.url}}{{site.baseurl}}/images/Query-Insights/QueryInsights.png)

每個標籤對應下列元件：

- [A. 導覽分頁](#a-navigation-tabs)
- [B. 查詢搜尋列](#b-search-queries-bar)
- [C. 篩選條件](#c-filters)
- [D. 日期範圍選取器](#d-date-range-selector)
- [E. 重新整理按鈕](#e-refresh-button)
<!-- vale off -->
- [F. 統計資料與視覺化](#f-stats--visualizations)
<!-- vale on -->
- [G. 指標表格](#g-metrics-table)

### A. 導覽分頁

導覽分頁可讓您在 **Live Queries**、**Top N Queries** 與 **Configuration** 頁面之間切換。

### B. 查詢搜尋列

搜尋查詢列可依據 **query type** 或 **indexes** 等特定屬性篩選查詢。您可以使用[篩選條件](#c-filters)章節所示的其他篩選條件。

### C. 篩選條件

篩選下拉選單可讓您選取下列查詢篩選條件。

| 篩選條件                  | 說明                                                         | 範例            |
|-------------------------|---------------------------------------------------------------------|--------------------|
| **Type**                | 依查詢類型篩選。                                               | `query`, `group`   |
| **Indexes**             | 依特定 OpenSearch 索引篩選查詢。                | `index1`, `index2` |
| **Search Type**         | 依搜尋執行方式篩選。                                  | `query then fetch` |
| **Coordinating Node ID** | 專注於由特定協調節點執行的查詢。           | `node-1`, `node-2` |
| **WLM Group**           | 依工作負載管理群組篩選查詢。                        | `default`          |
| **Time Range**          | 調整所顯示查詢的時間範圍。                    | `last 1 day`       |

### D. 日期範圍選取器

**日期範圍選取器**會分析在設定期間內送出的查詢。您也可以選取 **Show dates**，為每筆查詢提供詳細的時間戳記。

### E. 重新整理按鈕

**Refresh** 按鈕會根據選取的篩選條件與時間範圍重新載入查詢資料。

<!-- vale off -->
### F. 統計資料與視覺化
<!-- vale on -->

**Stats & Visualizations** 區段是 **Top N queries** 頁面上的可摺疊面板，可提供一目瞭然的效能指標，以及查詢的互動式視覺化分解。您可以使用面板右上角的按鈕，在 **Query** 與 **Group** 檢視之間切換。

所有視覺化僅適用於個別查詢；不支援群組查詢的視覺化。
{: .note}

#### P90 與 P99 指標

面板頂列會顯示下列指標在所選時間範圍內的 P90 與 P99 統計資料：

| 指標          | 說明                                                        |
|:----------------|:-------------------------------------------------------------------|
| **P90 Latency** | 第 90 百分位數的查詢延遲。                                 |
| **P90 CPU Time**| 查詢所耗用 CPU 時間的第 90 百分位數。                  |
| **P90 Memory**  | 各查詢記憶體用量的第 90 百分位數。                   |
| **P99 Latency** | 第 99 百分位數的查詢延遲。                                 |
| **P99 CPU Time**| 查詢所耗用 CPU 時間的第 99 百分位數。                  |
| **P99 Memory**  | 各查詢記憶體用量的第 99 百分位數。                   |

#### 依維度分類的查詢

**Queries by** 區段會顯示互動式圓餅圖與對應的表格，依所選維度將查詢分佈分類。您可以使用下拉選單在下列維度之間切換：

- **Node** -- 依協調節點將查詢分組。
- **Index** -- 依目標索引將查詢分組。
- **Username** -- 依送出查詢的使用者將查詢分組。
- **WLM Group** -- 依工作負載管理群組將查詢分組。

圓餅圖具有互動功能：將滑鼠游標移到扇形區塊上時，會顯示維度值、查詢數量與百分比。為減少視覺雜亂，較小的扇形區塊會合併為 **Other** 部分。隨附的表格會顯示每個維度值及其 **Query Count** 與 **Percentage**，並支援排序與分頁。

下圖顯示 P90/P99 指標，以及包含互動式圓餅圖與分頁表格的 Queries by Index 分解。

![統計資料、視覺化與依索引分類的查詢]({{site.url}}{{site.baseurl}}/images/Query-Insights/StatsAndVisualizations.png)

#### 效能分析

**Performance Analysis** 區段可讓您更深入了解查詢指標如何隨時間以及在不同元件之間變化。您可以使用切換按鈕在 **Line Chart** 與 **Heatmap** 檢視之間切換。

##### 折線圖

折線圖會針對所選指標，在選定的時間期間內顯示 **Max**、**Avg** 與 **Min** 三條線，並劃分為 10 個等距的時間桶。使用 **Metric** 下拉選單可選擇 **Latency**、**CPU Time** 或 **Memory**。

下圖顯示 Performance Analysis 的折線圖檢視。

![效能分析折線圖]({{site.url}}{{site.baseurl}}/images/Query-Insights/PerformanceAnalysisLineChart.png)

##### 熱度圖

熱度圖提供以格線為基礎的檢視，顯示指標值在時間與元件值之間的分佈，並劃分為 30 個等距的時間桶。顏色深淺表示指標大小，從低（淺色）到高（深色）。

使用下拉選單可選取下列選項：

- **Dimension**：可選擇 **Index**、**Node**、**Username**、**User Roles** 或 **WLM Group**。
- **Metric**：可選擇 **Latency**、**CPU Time**、**Memory** 或 **Count**。
- **Aggregation**：可選擇 **Max**、**Avg** 或 **Min**。

下圖顯示依索引分組的 Performance Analysis 熱度圖檢視。

![效能分析熱度圖]({{site.url}}{{site.baseurl}}/images/Query-Insights/PerformanceAnalysisHeatmap.png)

### G. 指標表格

指標表格會根據您選取的 **Type** 篩選條件（**Query**、**Group** 或兩者）動態調整。動態欄位只會顯示各查詢類型相關的資料，藉此提升清晰度。

當您只選取**查詢**時，表格會顯示個別指標，包括 **Latency**、**CPU Time** 和 **Memory Usage**。此時不會顯示 **Query Count** 欄，因為每一列代表單一查詢，如下圖所示。

![選取查詢時的欄位顯示]({{site.url}}{{site.baseurl}}/images/Query-Insights/OnlyQueryColDisplay.png)

當您只選取**群組**時，表格會顯示彙總指標，包括 **Average Latency**、**Average CPU Time** 和 **Average Memory Usage**。**Query Count** 欄會顯示每個群組中有多少查詢，如下圖所示。

![選取群組時的欄位顯示]({{site.url}}{{site.baseurl}}/images/Query-Insights/OnlyGroupColDisplay.png)

當您同時選取**群組**與**查詢**時，表格會顯示合併指標，同時包含平均值和原始值，如下圖所示。

![兩者皆選取時的欄位顯示]({{site.url}}{{site.baseurl}}/images/Query-Insights/BothColDisplay.png)

下表提供各指標的說明，以及選取時該指標相關的查詢和群組。

| 欄位名稱 | 說明  | 選取查詢 | 選取群組 | 選取查詢 + 群組 |
| :--- | :--- | :--- | :--- | :--- |
| **ID**                  | 查詢或群組的唯一識別碼。 | `ID`   | `ID`   | `ID`  |
| **Type**                | 指出該項目是查詢還是群組。 | `Type`  | `Type` | `Type`  |
| **Query Count**         | 群組中彙總的查詢數目。  | 不顯示  | `Query Count`        | `Query Count`   |
| **Timestamp**           | 查詢或群組的記錄時間（群組可能為空）。 | `Timestamp`     | 不顯示            | `Timestamp`    |
| **Latency**             | 個別查詢執行所花費的時間。  | `Latency`          | `Average Latency`    | `Avg Latency/Latency`          |
| **CPU Time**            | 消耗的 CPU 資源數量。 | `CPU Time`         | `Average CPU Time`   | `Avg CPU Time/CPU Time`        |
| **Memory Usage**        | 執行期間使用的記憶體數量。  | `Memory Usage`     | `Average Memory Usage` | `Avg Memory Usage/Memory Usage` |
| **Indexes**             | 查詢或群組涉及的索引清單。 | `Indexes`  | 不顯示            | `Indexes`    |
| **Search Type**         | 使用的搜尋執行方法（例如 `query` 或 `fetch`）。  | `Search Type`      | 不顯示            | `Search Type`  |
| **Coordinating Node ID** | 協調查詢的節點。  | `Coordinating Node ID` | 不顯示         | `Coordinating Node ID` |
| **WLM Group**           | 與查詢相關的工作負載管理群組。 | `WLM Group`        | 不顯示            | `WLM Group`     |
| **Total Shards**        | 查詢處理涉及的分片數目。   | `Total Shards`     | 不顯示            | `Total Shards`  |

當您選取 **Query + Group** 時：

- 如果顯示的所有列都是查詢，則表格會依照**選取查詢**的方式顯示。
- 如果顯示的所有列都是群組，則表格會依照**選取群組**的方式顯示。

## 查詢詳細資料

**Query details** 頁面提供查詢行為、效能和結構的深入解析。您可以選取查詢 ID 來存取查詢詳細資料頁面，如下圖所示：

![查詢深入解析清單]({{site.url}}{{site.baseurl}}/images/Query-Insights/Querieslist.png){: width="400"}

### 檢視個別查詢詳細資料

您可以選取查詢 ID（例如 `51c68a1a-7507-4b3e-aea1-32ddd74dbac4`）來存取單一查詢的詳細資訊。查詢詳細資料頁面將會出現，如下圖所示。

![個別查詢詳細資料]({{site.url}}{{site.baseurl}}/images/Query-Insights/IndividualQueryDetails.png)

在查詢詳細資料檢視中，您可以檢視 **Timestamp**、**CPU Time**、**Memory Usage**、**Indexes**、**Search Type**、**Coordinating Node ID** 和 **Total Shards** 等資訊。

如果查詢來源因大小限制而被截斷，則會以字串而非格式化 JSON 顯示。

### 檢視查詢群組詳細資料

查詢群組詳細資料檢視提供一組類似查詢的彙總指標深入解析。

若要檢視查詢群組詳細資料，請在 **Top N queries** 清單中選取標示為「group」的查詢 ID。查詢群組詳細資料檢視提供下列資訊：

![查詢群組詳細資料]({{site.url}}{{site.baseurl}}/images/Query-Insights/GroupQueryDetails.png)

- **Aggregate summary for queries** 區段提供整個群組的關鍵查詢指標檢視，包括 **Average latency**、**Average CPU time**、**Average memory usage** 和 **Group by** 準則。
- **Sample query details** 區段提供單一代表性查詢的資訊，包括其 **Timestamp**、**Indexes**、**Search Type**、**Coordinating Node ID** 和 **Total Shards**。
- **Latency** 區段以圖形呈現查詢的執行階段。

## 組態

**Query insights - Configuration** 頁面旨在讓您控制查詢深入解析功能收集、監視、分組及保留資料的方式。下圖顯示組態頁面。

![組態]({{site.url}}{{site.baseurl}}/images/Query-Insights/Configuration.png)

在組態頁面上，您可以設定下列各節所述的設定。

**適用於正式環境部署**：當 Dashboard 應用程式在具有網路存取限制的個別節點上執行時，請考慮使用 [Query Insights Settings API]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/settings-api/) 來啟用安全組態。Query Insights Settings API 提供精細的存取控制，讓您可以在查詢深入解析組態中安全地使用允許清單，而不需授予廣泛的叢集設定權限。
{: .tip}

### 前 N 大查詢監視

**Top n queries monitoring configuration settings** 可讓您追蹤查詢效能指標，例如 **Latency**、**CPU Usage** 和 **Memory**，以分析和最佳化查詢效能。組態介面提供結構化、功能表驅動的設定，讓您可以定義要監視的特定指標、設定分析閾值，以及自訂監視持續時間。

請執行下列步驟來設定前 N 大查詢設定：

1. 在 **Query insights** 頁面上，瀏覽至 **Configuration** 索引標籤。
2. 選取指標類型：**Latency**、**CPU Usage** 或 **Memory**。
3. 切換 **Enabled** 設定，為選取的指標開啟或關閉前 N 大查詢功能。
4. 指定監視 **Window size**，這會決定收集查詢以進行分析的時間長度。
5. 輸入 **N** 的值，這會定義每個時間範圍內要追蹤的排名前幾的查詢數目。
6. 選取 **Save**。
7. 查看 **Statuses for configuration metrics** 面板，以了解已啟用的指標。

### 前 N 大查詢分組

**Top n queries group configuration settings** 用於設定查詢的分組設定。

使用下列步驟設定特定的分組屬性：

1. 在 **Group By** 下選取分組選項，例如 **Similarity**。
2. 選取 **Save**。
3. 檢查 **Statuses for group by** 面板，確認是否已啟用 **Group by** 條件。

### 資料匯出與保留

若要設定資料匯出與保留，請使用 **Query insights export and data retention settings** 面板。您可以在該面板中設定下列設定：

1. 在 **Exporter** 下，選擇資料的目的地，例如 **Local index**。
2. 在 **Delete After (days)** 欄位中設定資料保留期間。
3. 選取 **Save**。
4. 在 **Statuses for data retention** 面板中，確認已啟用 **Exporter** 設定。

### 遠端儲存庫匯出器

**Remote repository exporter settings** 面板可讓您將前 N 大查詢的深入解析資料匯出至遠端 Amazon Simple Storage Service（Amazon S3）儲存庫，以較低成本長期儲存。此匯出器獨立於本機匯出器和資料保留設定運作。由於其運作獨立，您可以同時執行遠端儲存庫匯出器與本機索引匯出器，將資料同時匯出至兩個目的地。

遠端儲存庫匯出器需要在叢集上安裝 [`repository-s3` 外掛程式]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#amazon-s3)。若要設定匯出器，請遵循外掛程式安裝指示。

#### 註冊 S3 儲存庫

啟用匯出器之前，您必須先註冊至少一個 S3 儲存庫。 

請確認您的 AWS 憑證、AWS 區域和儲存貯體均已正確設定。
{: .note}

若要註冊新的 S3 儲存庫，請使用下列步驟：

1. 在 **Remote repository exporter settings** 面板中，選取 **Repository** 欄位旁的 **Register new**。
2. 在 **Register S3 repository** 滑出面板中，設定下列欄位：
   - **Repository name**：儲存庫的唯一名稱，例如 `query-insights-repository`。
   - **S3 bucket**：用於儲存匯出資料的 S3 儲存貯體名稱，例如 `query-insights-exports`。
   - **Base path**（選用）：儲存貯體內用於儲存庫資料的路徑。將此欄位留空即可使用儲存貯體的根目錄。
3. 選取 **Register repository**。

註冊儲存庫後，即可在 **Repository** 下拉式選單中選取該儲存庫。

#### 啟用遠端匯出器

若要啟用遠端儲存庫匯出器，請使用下列步驟：

1. 切換 **Enabled** 設定以啟用遠端儲存庫匯出器。
2. 從 **Repository** 下拉式清單中選取已註冊的 S3 儲存庫。
3. 在 **Path** 欄位中，指定儲存庫內用於整理匯出檔案的路徑。預設為 `query-insights`。此路徑與註冊時設定的 **Base path** 不同，後者定義儲存庫在儲存貯體中儲存資料的位置。
4. 選取 **Save**。
5. 在 **Statuses for remote exporter** 面板中，確認遠端匯出器的狀態為 **Enabled**。

### 組態最佳實務

設定查詢深入解析功能時，請記住下列最佳實務：

- 先為 N（數量）設定較小的值，再根據系統負載增加。
- 請謹慎選擇 **Window size**。較長的時間視窗可節省運算資源，因為所取得的洞察粒度較粗。反之，較短的時間視窗可產生更全面的查詢洞察，但會使用更多資源。
- 設定資料保留期間時，可考慮較短的保留期間，以節省儲存空間，但這會減少長期洞察的數量。
- 根據您的監控需求啟用指標。監控較少的指標可避免系統過載。

## 即時查詢

**Live queries** 頁面可即時顯示目前在您的 OpenSearch 叢集中執行的搜尋查詢。此頁面可讓您主動監控、快速偵錯，並深入瞭解查詢負載如何分布於各節點與索引。

下圖顯示即時查詢檢視。

![即時查詢儀表板]({{site.url}}{{site.baseurl}}/images/Query-Insights/Live_Queries.png)

### 指標概覽

即時查詢檢視的頂端面板會顯示下列主要即時指標。

| 面板                    | 說明                                                                 |
| :---                     |:----------------------------------------------------------------------------|
| **Active queries**        | 目前在叢集中執行的查詢總數。             |
| **Avg. elapsed time**     | 所有執行中查詢的平均執行時間。                       |
| **Longest running query** | 目前執行時間最長的查詢之查詢 ID 與已耗用時間。     |
| **Total CPU time**        | 所有執行中查詢耗用的累計 CPU 時間。                     |
| **Total memory usage**    | 所有執行中查詢耗用的記憶體總量。                            |
| **Total completions**     | 已成功完成的查詢數量。                     |
| **Total cancellations**   | 已取消的查詢數量。           |
| **Total rejections**      | 已拒絕的查詢數量。 |


### 分布圖表

兩個視覺化圖表提供查詢負載的分布資訊：

- **By node** – 顯示各節點上執行的查詢數量。
- **By index** – 顯示以各索引為目標的查詢數量。

![即時查詢視覺化圖表]({{site.url}}{{site.baseurl}}/images/Query-Insights/Live_queries_visuailization.png)

您可以使用圖表類型切換開關，在 **Donut** 與 **Bar** 圖表格式之間切換。

圖表僅個別顯示前 9 個項目；其餘值會歸入 **Others** 類別。

### 即時查詢表格

即時查詢表格會列出每個即時查詢的下列資訊。


| 欄位              | 說明                                                                                                                                                               |
| :---                |:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Timestamp**        | 查詢開始執行的時間。                                                                                                                              |
| **Task ID**          | 查詢工作的唯一識別碼。                                                                                                                                 |
| **Index**            | 查詢所針對的一個或多個索引。                                                                                                                               |
| **Node**             | 目前執行查詢的節點。                                                                                                                                   |
| **Time elapsed**     | 查詢目前的執行時間，以秒為單位。                                                                                                                      |
| **CPU usage**        | 查詢耗用的累計 CPU 時間。                                                                                                                            |
| **Memory usage**     | 查詢執行期間耗用的記憶體量。                                                                                                              |
| **Search type**      | 搜尋執行方式，例如 `query_then_fetch`。                                                                                                                  |
| **Coordinating node** | 協調查詢執行的節點。                                                                                                                            |
| **WLM Group**        | 與查詢關聯的工作負載群組。若停用工作負載管理（WLM），則顯示為純文字；若啟用 WLM，則顯示為可點選的連結，連至與該查詢關聯的 **WLM Group Details** 頁面。 |
| **Status**           | 查詢目前的狀態。值為 `running` 或 `cancelled`。                                                                                                         |
| **Actions**          | 可對查詢執行的動作，例如取消執行。                                                                                                       |

您可以使用篩選列，依文字或特定欄位值搜尋查詢，例如節點 ID、索引名稱或 Task ID，並透過表格分頁更有效地分析特定查詢。下圖顯示即時查詢表格檢視。

![即時查詢表格]({{site.url}}{{site.baseurl}}/images/Query-Insights/Live_Queries_Table.png)

即時查詢表格提供下列即時監控控制項：
- **Auto-refresh toggle** – 啟用或停用定期資料重新整理。
- **Refresh interval** – 選擇重新整理頻率。此選項僅在啟用 **Auto-refresh** 時可用。
- **Manual refresh** – 選取 **Refresh** 按鈕以立即更新。

### 工作負載群組選取器

**工作負載群組選取器**可讓您依工作負載群組篩選及分析作用中的查詢：

- 預設情況下，選取器設定為 **All Workload Groups**，顯示整個叢集的查詢。
- 當 **WLM 已停用**時，僅提供 `DEFAULT_WORKLOAD_GROUP` 選項。
- 當 **WLM 已啟用**時，下拉式選單會列出所有可用的工作負載群組。
- 選取特定群組後，儀表板會篩選為僅顯示在該工作負載群組下執行的查詢。
- [指標](#metrics-overview)面板與圖表會更新為僅顯示所選的工作負載群組。

### 取消即時查詢

即時查詢表格提供直接的控制功能，可取消目前正在叢集中執行的查詢。這讓您能立即停止有問題或耗用大量資源的搜尋，而無需等待它們完成。您可以透過下列方式取消即時查詢：

1. 取消個別查詢：
   - 在您要停止之查詢的 **Actions** 欄中，選取垃圾桶圖示。
   - 出現提示時，確認取消。
   取消成功後，查詢狀態會變更為 `Cancelled`。

2. 大量取消多個查詢：
   - 若要選取多個查詢，請使用表格左側的核取方塊。若要選取所有查詢，請使用表格標頭中的 **Select all** 核取方塊。
   - 選取表格上方的 **Cancel selected** 按鈕。
   - 確認取消所有選取的查詢。
   所有選取的查詢都會停止，且其狀態會更新。








