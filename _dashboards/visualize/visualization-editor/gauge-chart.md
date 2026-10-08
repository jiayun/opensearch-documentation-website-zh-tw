---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "儀表圖"
parent: Visualization types
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 25
---

# 視覺化編輯器中的儀表圖

儀表圖會在半圓形弧線上顯示單一數值。使用儀表圖可呈現指標與所定義的臨界值或目標範圍相比的情況。

## 建立儀表圖

下列範例會逐步累加，從基本的儀表開始，再逐步增加複雜度。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/#prerequisites)。

### 基本儀表圖

首先使用一個會傳回單一數值彙總的查詢：

```sql
source = opensearch_dashboards_sample_data_flights | FIELDS AvgTicketPrice
```
{% include copy.html %}

執行此查詢後，選取 **Gauge** 作為圖表類型。視覺化會自動套用 **Last** 計算方式，將數列縮減為單一值以供顯示。編輯器會依下列方式對應欄位：

- **Value** 欄位會顯示 `AvgTicketPrice` 欄位（預設使用 **Last** 計算方式）。

結果會是一個以預設綠色弧線顯示最後一筆票價值的儀表，如下圖所示。

![顯示最後一筆平均票價的初始儀表圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/gauge/gauge-initial-look.png){: width="100%" }

### 新增臨界值

定義臨界值斷點，將儀表弧線劃分為不同顏色的範圍，以表示數值的健康狀態。

使用與上一個範例相同的查詢，在設定面板中開啟 **Thresholds** 區段並新增臨界值。例如：

- 基本顏色：綠色（低於 500 的值）
- 臨界值 500：黃色（中等價格範圍）
- 臨界值 800：紅色（高價格範圍）

弧線現在會顯示不同顏色的色帶：500 以下為綠色、500 至 800 為黃色、800 以上為紅色。啟用 **Use threshold colors** 可將相符的臨界值顏色套用至所顯示的數值文字與弧線，如下圖所示。

![具有依顏色區分之臨界值色帶的儀表圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/gauge/gauge-with-thresholds.png){: width="100%" }

### 自訂儀表刻度

若要以代表完整預期範圍的固定刻度來監控票價，請開啟 **Standard options** 區段並設定：

- **Min**：`500`
- **Max**：`1200`

儀表現在一律會涵蓋 500 至 1200 的範圍，讓您更容易在分割的面板之間進行比較，如下圖所示。

![具有自訂最小值/最大值刻度的儀表圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/gauge/gauge-custom-scale.png){: width="100%" }

## 設定儀表圖

您可以在組態面板中設定下列設定。

### 欄位

在 **Fields** 區段中設定資料欄位。

| 欄位 | 說明 |
| --- | --- |
| **Value** | 選取一個數值欄位，其值會使用所設定的計算方式縮減為單一數字。結果會顯示為儀表的目前值。 |

### 分割

在 **Split by** 下拉式清單中選取一個欄位，依其值將圖表分割為個別的元素。如需詳細資訊，請參閱[分割]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#split)。

### 儀表

| 設定 | 說明 |
| --- | --- |
| **Use threshold colors** | 啟用時，中央的數值會採用目前值所在之臨界值範圍的顏色。 |
| **Show title** | 在數值下方顯示標籤。預設為欄位名稱，但您可以使用自訂文字加以覆寫。 |
| **Title** | 啟用 **Show title** 時顯示於數值下方的自訂標題文字。若保留空白，則會使用欄位名稱。 |

### 值選項

| 設定 | 說明 |
| --- | --- |
| **Calculation** | 決定如何將多個資料點縮減為儀表上顯示的單一值。支援的值：**Last \***、**Last**、**First \***、**First**、**Min**、**Max**、**Mean**、**Median**、**Variance**、**Count**、**Distinct count**、**Total**。如需詳細資訊，請參閱[值計算]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/value-calculations/)。 |

### 臨界值

如需設定臨界值的相關資訊，請參閱[臨界值]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/thresholds/)。

### 標準選項

如需設定單位、單位後綴、小數精確度以及最小值與最大值的相關資訊，請參閱[標準選項]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/standard-options/)。
