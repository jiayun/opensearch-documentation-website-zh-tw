---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "長條圖"
parent: Visualization types
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 15
---

# 視覺化編輯器中的長條圖

長條圖以垂直或水平長條顯示資料。使用長條圖來比較離散類別。選取 **Color** 欄位可將類別分割為子群組，並可新增閾值線來標示高於或低於目標的值。

## 建立長條圖

以下範例會逐步延伸，從基本圖表開始，再逐漸增加複雜度。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/#prerequisites)。

### 基本長條圖

首先使用依類別計算事件數量的彙總查詢：

```sql
source = opensearch_dashboards_sample_data_flights | stats count() by Carrier
```
{% include copy.html %}

執行此查詢後，視覺化編輯器會自動選取 **Bar** 圖表並對應欄位：

- **X-Axis** 顯示 `Carrier` 欄位。
- **Y-Axis** 顯示 `count()` 欄位。

結果是一張比較各航空公司事件數量的長條圖，如下圖所示。

![依航空公司顯示數量的基本長條圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/bar-chart-basic-result.png){: width="100%" }

### 群組長條圖

在查詢中新增第二個維度，將每個類別分割為子群組：

```sql
source = opensearch_dashboards_sample_data_flights | stats count() by Carrier, Cancelled
```
{% include copy.html %}

此查詢會同時依航空公司和 `Cancelled` 欄位將數量分組。選取 `Cancelled` 作為 **Color** 欄位，即可在每家航空公司中為每種取消狀態分別呈現一個長條。

結果是一張群組長條圖，其中每家航空公司都有兩個並排的長條，一個代表未取消的航班，另一個代表已取消的航班，方便您比較每種取消狀態的航班數量，如下圖所示。

![依航空公司和取消狀態顯示數量的群組長條圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/bar-chart-grouped-result.png){: width="100%" }

### 新增閾值

使用閾值可新增參考線，並根據目標值為長條設定顏色。

沿用前一個範例中的群組長條圖，設定設定面板：

1. 在 **Bar** 區段中，啟用 **Use threshold colors**。
1. 在 **Thresholds** 區段中，選取 **+ Add threshold**。
1. 將基本顏色設為綠色（`#00BD6B`），並在值 `200` 新增一個紅色（`#F13939`）閾值。
1. 將 **Threshold lines mode** 設為 **Dashed lines**，如下圖所示。

![閾值設定為 200 的長條圖設定]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/bar-chart-threshold-settings.png){: width="400" }

結果會依據閾值規則為長條著色：低於 200 的長條顯示為綠色，高於 200 的長條則顯示為紅色。位於 200 的虛線參考線提供清楚的視覺基準，如下圖所示。

![具有閾值著色及位於 200 之虛線參考線的長條圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/bar-chart-threshold-result.png){: width="100%" }

## 設定長條圖

您可以在組態面板中設定下列設定。

### 欄位

在 **Fields** 區段中，設定各軸上顯示的欄位。

| 欄位 | 說明 |
| --- | --- |
| **X-Axis** | 選取類別或日期欄位，用以定義沿水平軸排列的群組（例如 `Carrier`）。 |
| **Y-Axis** | 選取一或多個數值欄位，用以決定長條的高度。選取多個欄位時，每個欄位會在每個類別群組中呈現為個別的長條。 |
| **Color** | 選取類別欄位，將每個類別分割為群組長條，每個長條以不同顏色呈現。例如，使用 `Cancelled` 欄位，在每家航空公司中分別顯示已取消和未取消航班的長條。 |

### 分割

在 **Split by** 下拉式清單中，選取一個欄位，依值將圖表分割為個別元素。如需詳細資訊，請參閱[分割]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#split)。


### 長條

下列設定控制長條的顯示樣式和大小。

| 設定 | 說明 |
| --- | --- |
| **Stack** | 控制多個數列的顯示方式。**None** 會重疊顯示數列而不堆疊。**Stack** 會將數列值相加。**Percentage** 會以占總計的百分比堆疊數列。 |
| **Fill opacity** | 設定長條的不透明度。 |
| **Size** | 控制長條寬度。**Auto** 會自動調整長條大小。**Manual** 會設定特定的寬度百分比（1–100）。 |
| **Radius** | 以像素為單位設定每個長條的圓角。 |
| **Show values** | 在圖表上顯示值標籤。 |
| **Use threshold colors** | 啟用時，圖表會依據 **Thresholds** 區段中定義的閾值規則為長條著色。 |
| **Show border** | 啟用時，會在每個長條周圍加上框線。 |
| **Border width** | 以像素為單位設定框線粗細。啟用 **Show border** 時才能使用此設定。 |
| **Border color** | 設定框線顏色。啟用 **Show border** 時才能使用此設定。 |

### 桶

下列設定控制如何在每個長條中彙總資料。

| 設定 | 說明 |
| --- | --- |
| **Type** | 用於計算每個桶 (bucket) 值的彙總類型。支援的值：**Sum**、**Average**、**Min**、**Max**、**Count**。 |
| **Interval** | 將資料分組到桶中的時間間隔。支援的值：**Auto**、**Month**、**Day**、**Hour**、**Minute**、**Second**。 |

### 閾值

如需設定閾值的相關資訊，請參閱[閾值]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/thresholds/)。

### 標準選項

如需設定單位、單位後綴、小數精確度以及最小值和最大值的相關資訊，請參閱[標準選項]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/standard-options/)。

### 軸

X 軸和 Y 軸共用相同的組態選項。如需詳細資訊，請參閱[軸]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#axes)。

### 圖例

如需設定圖例的相關資訊，請參閱[圖例]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#legend)。

### 工具提示

切換 **Show tooltip** 選取器以啟用或停用工具提示。
