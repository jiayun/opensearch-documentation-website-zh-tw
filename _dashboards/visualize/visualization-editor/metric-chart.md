---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指標圖表"
parent: Visualization types
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 45
---

# 視覺化編輯器中的指標圖表

指標圖表會醒目地顯示單一數值。使用指標圖表來顯示關鍵績效指標 (KPI) 或摘要統計資料。

## 建立指標圖表

以下範例示範基本的指標視覺化。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/#prerequisites)。

### 基本指標圖表

從傳回數值欄位的查詢開始：

```sql
source = opensearch_dashboards_sample_data_flights | FIELDS AvgTicketPrice
```
{% include copy.html %}

執行此查詢後，選取 **Metric** 作為圖表類型。編輯器會依下列方式對應欄位：

- **Value** 欄位會顯示 `AvgTicketPrice` 欄位 (預設使用 **Last** 計算方式)。

結果是一個顯示最後一筆票價值的單一大型數字，如下圖所示。

![顯示最後一筆平均票價的指標圖表]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/metric-chart-basic-result.png){: width="100%" }

## 設定指標圖表

您可以在組態面板中設定下列設定。

### 欄位

在 **Fields** 區段中，設定資料欄位。

| 欄位 | 說明 |
| --- | --- |
| **Value** | 選取要顯示為指標值的數值欄位。此欄位會使用所設定的計算方式縮減為單一數字。 |

### 分割

在 **Split by** 下拉式清單中，選取一個欄位，依值將圖表分割為個別元素。如需詳細資訊，請參閱[分割]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#split)。

### 指標

| 設定 | 說明 |
| --- | --- |
| **Text display** | 控制與值一同顯示的文字。支援的值：**Value only**、**Name only**、**Value and Name**、**None**。 |
| **Color mode** | 控制如何將閾值色彩套用至指標。支援的值：**None** (無色彩)、**Value** (為值文字上色)、**Background gradient** (套用漸層背景)、**Background solid** (套用純色背景)。 |
| **Show percentage** | 啟用時，會將值顯示為最大值的百分比。 |
| **Use threshold colors** | 啟用時，會根據目前的值將閾值色彩套用至指標。 |

### 值選項

| 設定 | 說明 |
| --- | --- |
| **Calculation** | 決定如何將多個資料點縮減為單一值。支援的值：**Last \***、**Last**、**First \***、**First**、**Min**、**Max**、**Median**、**Variance**、**Distinct count**、**Count**、**Total**。如需詳細資訊，請參閱[值計算]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/value-calculations/)。 |

### 閾值

如需設定閾值的相關資訊，請參閱[閾值]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/thresholds/)。

### 標準選項

如需設定單位、單位後綴和小數精確度的相關資訊，請參閱[標準選項]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/standard-options/)。

### 文字大小

| 設定 | 說明 |
| --- | --- |
| **Value size** | 控制所顯示值的字型大小。 |
| **Title size** | 控制指標標題的字型大小。 |
| **Percentage size** | 控制百分比顯示的字型大小 (當 **Show percentage** 已啟用時)。 |
