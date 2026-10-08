---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "表格"
parent: Visualization types
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 65
---

# 視覺化編輯器中的表格

表格以列和欄顯示查詢結果。使用表格來檢視原始資料或摘要統計資料。

## 建立表格

下列範例示範基本的表格視覺化。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/#prerequisites)。

### 基本表格

從傳回多個欄位的查詢開始：

```sql
source = opensearch_dashboards_sample_data_flights | fields Carrier, AvgTicketPrice, DistanceMiles, FlightDelayMin | head 20
```
{% include copy.html %}

執行此查詢後，選取 **Table** 作為圖表類型。結果會是一個將所選欄位顯示為欄的表格，如下圖所示。

![顯示航班資料的表格]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/table-chart-basic-result.png){: width="100%" }

## 設定表格

您可以在組態面板中設定下列設定。

### 表格

| 設定 | 說明 |
| --- | --- |
| **Max rows per page** | 設定每頁顯示的最大列數。 |
| **Cell alignment** | 控制儲存格內的文字對齊方式。支援的值：**Auto**、**Left**、**Center**、**Right**。 |
| **Cell style** | 選取 **Add new cell type**，將自訂樣式套用至特定欄。 |
| **Column filters** | 啟用時，會在欄標題中顯示篩選控制項，以進行互動式篩選。 |

### 閾值

如需設定閾值的相關資訊，請參閱[閾值]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/thresholds/)。

### 表格頁尾

| 設定 | 說明 |
| --- | --- |
| **Show footer** | 啟用時，會顯示頁尾列，其中包含每一欄的摘要計算結果。 |

### 資料連結

選取 **Add link**，在表格儲存格內建立可點選的連結。使用資料連結，根據儲存格的值導覽至外部 URL 或其他儀表板。
