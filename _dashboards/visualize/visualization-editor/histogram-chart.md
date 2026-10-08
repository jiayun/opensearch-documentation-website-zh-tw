---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "直方圖"
parent: Visualization types
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 35
---

# 視覺化編輯器中的直方圖

直方圖會將值分組至區間（桶 (bucket)），並以垂直長條顯示每個區間中的值數量，藉此呈現數值欄位的分布情形。

## 建立直方圖

下列範例示範基本的直方圖視覺化。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/#prerequisites)。

### 基本直方圖

首先使用一個依數值欄位分組並計算值數量的查詢：

```sql
source = opensearch_dashboards_sample_data_flights | stats count() by AvgTicketPrice
```
{% include copy.html %}

執行此查詢後，選取 **Histogram** 作為圖表類型。編輯器會依下列方式對應欄位：

- **X-Axis** 會顯示 `AvgTicketPrice` 欄位。

結果會是一個顯示票價分布情形的直方圖，如下圖所示。

![顯示平均票價分布情形的直方圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/histogram-chart-basic-result.png){: width="100%" }

## 設定直方圖

您可以在組態面板中設定下列設定。

### 欄位

在 **Fields** 區段中，設定各軸上顯示的欄位。

| 欄位 | 說明 |
| --- | --- |
| **X-Axis** | 選取要沿水平軸分配至各桶的數值欄位。 |
| **Y-Axis** | 選取垂直軸使用的數值欄位。若保留空白，圖表會顯示每個桶中的值數量。 |

### 分割

在 **Split by** 下拉式清單中，選取一個欄位，依其值將圖表分割為個別元素。如需詳細資訊，請參閱[分割]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#split)。

### 桶

下列設定可控制資料分組至區間的方式。

| 設定 | 說明 |
| --- | --- |
| **Bucket Size** | 設定每個區間的寬度。請輸入數值，或保留為 **auto**，讓編輯器計算適當的大小。 |
| **Bucket count** | 設定要顯示的區間數量上限。 |

### 閾值

如需設定閾值的相關資訊，請參閱[閾值]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/thresholds/)。

### 標準選項

如需設定單位、單位後綴、小數精確度，以及最小值與最大值的相關資訊，請參閱[標準選項]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/standard-options/)。

### 軸

X 軸與 Y 軸共用相同的組態選項。如需詳細資訊，請參閱[軸]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#axes)。

### 直方圖

使用下列設定自訂直方圖的外觀。

| 設定 | 說明 |
| --- | --- |
| **Use threshold colors** | 啟用時，會依據閾值範圍為長條著色。 |
| **Show border** | 啟用時，會在每個長條周圍加上框線。 |

### 工具提示

切換 **Show tooltip** 選取器，即可啟用或停用工具提示。
