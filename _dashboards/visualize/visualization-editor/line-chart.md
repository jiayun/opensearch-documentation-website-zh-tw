---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "折線圖"
parent: Visualization types
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 40
---

# 視覺化編輯器中的折線圖

折線圖會繪製以線條相連的資料點。使用折線圖可呈現隨時間變化的趨勢與變動。您可以在同一時間軸上比較多個數列，並使用次要 Y 軸來關聯刻度不同的指標。

## 建立折線圖

以下範例循序漸進，從基本圖表開始，逐步增加複雜度。這些範例使用範例網頁記錄資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/#prerequisites)。

### 基本折線圖

首先使用一個計算隨時間變化之事件數量的彙總查詢：

```sql
source = opensearch_dashboards_sample_data_logs | stats count() by SPAN(@timestamp, 1h)
```
{% include copy.html %}

執行此查詢後，視覺化編輯器會自動選取 **Line** 圖表並對應欄位：

- **X-Axis** 顯示 `SPAN(@timestamp, 1h)` 欄位。
- **Y-Axis** 顯示 `count()` 欄位。

結果是一條顯示每小時事件數量的線條，如下圖所示。

![顯示每小時事件數量的基本折線圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/line-chart-basic-result.png){: width="100%" }

### 多數列折線圖

在查詢中加入第三個維度，依類別將資料分割為多個數列：

```sql
source = opensearch_dashboards_sample_data_logs | stats count() by SPAN(@timestamp, 1h), response
```
{% include copy.html %}

此查詢會同時依時間與 `response` 欄位（HTTP 狀態碼）將計數分組。選取 `response` 作為 **Color** 欄位，即可為每個狀態碼值（例如 200、404、503）各繪製一條獨立的線條。

結果是一張多數列折線圖，每個 HTTP 回應碼都以不同顏色顯示，如下圖所示。

![依 HTTP 回應碼顯示計數的多數列折線圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/line-chart-multi-series.png){: width="100%" }

### 多個 Y 軸欄位

當您的查詢計算多個指標時，您可以將它們全部繪製在同一張圖表上：

```sql
source = opensearch_dashboards_sample_data_logs | stats avg(bytes), max(bytes) by SPAN(@timestamp, 1h)
```
{% include copy.html %}

此查詢會傳回兩個數值欄位：`avg(bytes)` 和 `max(bytes)`。在 **Y-Axis** 欄位清單中選取 `avg(bytes)` 和 `max(bytes)`，即可將它們以相同刻度繪製為不同的線條。

結果會顯示隨時間變化的平均與最大位元組值，如下圖所示。

![將兩個 Y 軸指標繪製在一起的折線圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/line-chart-multiple-y-result.png){: width="100%" }

### 次要 Y 軸（雙軸）

當兩個指標的刻度差異很大時，將它們繪製在同一軸上可能會使其中一個看起來呈平坦狀。使用 **Y-Axis (2nd)** 欄位，可讓第二個指標在圖表右側擁有自己的刻度。

使用與上一個範例相同的查詢：

```sql
source = opensearch_dashboards_sample_data_logs | stats avg(bytes), max(bytes) by SPAN(@timestamp, 1h)
```
{% include copy.html %}

這次將 `avg(bytes)` 指派給 **Y-Axis**，並將 `max(bytes)` 指派給 **Y-Axis (2nd)**。

結果是一張雙軸圖表。左軸依 `avg(bytes)` 調整刻度，右軸依 `max(bytes)` 調整刻度，如下圖所示。

![以線條顯示 avg(bytes)、以長條顯示 max(bytes) 的雙軸圖表]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/line-chart-dual-axis-result.png){: width="100%" }

## 設定折線圖

您可以在組態面板中設定下列設定。

### 欄位

在 **Fields** 區段中，設定每個軸上顯示的欄位。

| 欄位 | 說明 |
| --- | --- |
| **X-Axis** | 為水平軸選取日期或數值欄位。此欄位定義繪製資料所依據的桶 (bucket)（例如 `SPAN(@timestamp, 1h)`）。 |
| **Y-Axis** | 選取一或多個數值欄位，以繪製為不同的線條。選取多個欄位時，每個欄位會以相同刻度繪製成各自的線條。 |
| **Y-Axis (2nd)** | 選取一個數值欄位，以疊加在擁有自己刻度的次要軸上。當兩個指標的單位或數量級不同時，請使用此選項。 |
| **Color** | 選取一個類別欄位，將資料分割為多個數列，每個數列以不同顏色繪製。 |

### 分割

在 **Split by** 下拉式清單中，選取一個欄位，依值將圖表分割為不同的元素。如需詳細資訊，請參閱[分割]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#split)。


### 線條

下表說明線條樣式設定。

| 設定 | 說明 |
| --- | --- |
| **Line style** | 控制圖表要顯示帶有資料點的線條（**Default**）、僅顯示線條（**Line only**），或僅顯示資料點（**Dots only**）。 |
| **Line dash style** | 將線條樣式設為 **Solid**、**Dashed** 或 **Dotted**。 |
| **Interpolation** | 決定資料點的連接方式。**Straight** 會在資料點之間繪製直線。**Smooth** 會套用曲線。**Stepped** 會建立階梯狀樣式，適用於以離散間隔變化的資料。 |
| **Line width** | 以像素為單位設定線條粗細。支援 1–10 範圍內的值。 |
| **Point size** | 設定資料點的大小。此設定僅在顯示資料點時可用。 |
| **Show values** | 在圖表上顯示數值標籤。 |
| **Show current time marker** | 顯示代表目前時間的垂直標記。此設定僅在 X 軸使用日期欄位時可用。 |

### 閾值

如需設定閾值的相關資訊，請參閱[閾值]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/thresholds/)。

### 標準選項

如需設定單位、單位後綴、小數精確度以及最小值和最大值的相關資訊，請參閱[標準選項]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/standard-options/)。

### 軸

X 軸與 Y 軸共用相同的組態選項。如需詳細資訊，請參閱[軸]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#axes)。

### 圖例

如需設定圖例的相關資訊，請參閱[圖例]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#legend)。

### 工具提示

切換 **Show tooltip** 選取器，即可啟用或停用工具提示。 
