---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "圓餅圖"
parent: Visualization types
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 50
---

# 視覺化編輯器中的圓餅圖

圓餅圖以圓形中依比例分配的扇形區塊顯示資料。使用圓餅圖來呈現部分與整體之間的關係。

## 建立圓餅圖

以下範例逐步延伸，從基本圖表開始，再加入自訂設定。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/#prerequisites)。

### 基本圓餅圖

首先使用依類別計算事件數量的彙總查詢：

```sql
source = opensearch_dashboards_sample_data_flights | stats count() by Carrier
```
{% include copy.html %}

執行此查詢後，視覺化編輯器會自動對應欄位：

- **Size** 顯示 `count()` 欄位。
- **Color** 顯示 `Carrier` 欄位。

預設的呈現方式為 **Donut** 圖。每家航空公司會以彩色扇形區塊顯示，其大小與事件數量成比例，如下圖所示。

![依航空公司顯示計數的環圈圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/pie-chart-donut-result.png){: width="100%" }

### 自訂圓餅圖

開啟 **Pie** 設定面板，並設定下列選項：

1. 將 **Show as** 從 **Donut** 變更為 **Pie**，以呈現中央沒有空心的完整圓形。
1. 啟用 **Show values**，以在每個扇形區塊上顯示計數。
1. 啟用 **Show labels**，以在每個扇形區塊旁顯示航空公司名稱。
1. 將 **Truncate after** 設為 `300`，以容納較長的標籤文字，如下圖所示。

![已啟用 Pie 模式、顯示數值與顯示標籤的圓餅圖設定]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/pie-chart-settings-custom.png){: width="400" }

結果是一個完整的圓餅圖，每個扇形區塊上都會顯示類別標籤與數值，如下圖所示。

![顯示標籤與數值的圓餅圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/pie-chart-labels-result.png){: width="100%" }

## 設定圓餅圖

您可以在組態面板中設定下列設定。

### 欄位

在 **Fields** 區段中，設定資料欄位。

| 欄位 | 說明 |
| --- | --- |
| **Size** | 選取決定每個扇形區塊大小的數值欄位。例如，`count()` 會使每個扇形區塊與該類別中的事件數量成比例。 |
| **Color** | 選取將資料分割成個別扇形區塊的類別欄位，每個區塊會以不同顏色呈現。例如，使用 `Carrier` 欄位為每家航空公司顯示一個扇形區塊。 |

### 分割

在 **Split by** 下拉式清單中，選取一個欄位，依其值將圖表分割為個別元素。如需詳細資訊，請參閱[分割]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#split)。


### 圓餅

下表說明圓餅圖的設定。

| 設定 | 說明 |
| --- | --- |
| **Show as** | 控制圖表要呈現為完整圓餅或 **Donut**（環圈）形狀。預設為 **Donut**。 |
| **Show values** | 啟用時，會在圖表上顯示每個扇形區塊的數值。 |
| **Show labels** | 啟用時，會在圖表上顯示每個扇形區塊的類別標籤。 |
| **Truncate after** | 設定標籤在截斷前的最大寬度（以像素為單位）。僅在啟用 **Show labels** 時顯示。 |

### 標準選項

如需設定單位、單位後綴與小數精確度的相關資訊，請參閱[標準選項]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/standard-options/)。

### 圖例

圖例彙總圖表中使用的視覺色彩編碼。

| 設定 | 說明 |
| --- | --- |
| **Show legend** | 顯示或隱藏圖例。 |
| **Position** | 控制圖例相對於圖表的顯示位置。支援的值：**Left**、**Right**、**Top**、**Bottom**。 |

### 工具提示

切換 **Show tooltip** 選取器，以啟用或停用工具提示。
