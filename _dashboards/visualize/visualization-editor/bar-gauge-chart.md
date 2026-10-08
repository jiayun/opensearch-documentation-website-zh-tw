---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "長條量表圖"
parent: Visualization types
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 20
---

# 視覺化編輯器中的長條量表圖

長條量表圖會將數值顯示為對照刻度的水平或垂直長條，並將每個欄位簡化為單一值。與長條圖不同，長條量表圖的設計目的是將數值與定義的閾值進行比較。

## 建立長條量表圖

下列範例逐步延伸，從基本圖表開始，再逐漸增加複雜度。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/#prerequisites)。

### 基本長條量表圖

首先使用依類別欄位將數值指標分組的查詢：

```sql
source = opensearch_dashboards_sample_data_logs | stats avg(bytes) by machine.os
```
{% include copy.html %}

執行此查詢後，選取 **Bar Gauge** 作為圖表類型。欄位的對應方式如下：

- **X-Axis** 顯示 `machine.os` 欄位（類別）。
- **Y-Axis** 顯示 `avg(bytes)` 欄位（數值）。

結果是一組垂直長條，每個作業系統各一個，顯示各作業系統的平均位元組數。**Show unfilled area** 切換開關預設為啟用，會在每個長條後方顯示灰色背景，以表示距離最大值的剩餘差距，如下圖所示。

![依作業系統顯示平均位元組數的基本長條量表]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/bar-gauge/bar-gauge-initial.png){: width="100%" }

### 新增閾值與顯示樣式

開啟 **Thresholds** 區段並定義斷點，以便用顏色標示長條。例如：

- 基礎顏色：綠色（低於 3000 的值）
- 3000 的閾值：橘色（中等範圍）
- 5000 的閾值：紅色（高範圍）

接著在 **Bar Gauge** 區段中切換 **Display style**，以查看不同的視覺呈現方式：

**Gradient**---每個長條會以平滑的顏色漸變填滿，依序經過其所跨越的閾值，如下圖所示。

![使用漸層顯示樣式的長條量表]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/bar-gauge/bar-gauge-gradient.png){: width="100%" }

**Stack**---每個長條會在閾值邊界處分割為不同顏色的區段，如下圖所示。

![使用堆疊顯示樣式的長條量表]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/bar-gauge/bar-gauge-stack.png){: width="100%" }

**Basic**---每個長條會根據數值所達到的最高閾值，使用單一純色，如下圖所示。

![使用基本顯示樣式的長條量表]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/bar-gauge/bar-gauge-basic.png){: width="100%" }

## 設定長條量表圖

您可以在組態面板中設定下列設定。

### 欄位

在 **Fields** 區段中，設定各軸上顯示的欄位。

| 欄位 | 說明 |
| --- | --- |
| **X-Axis** | 選取類別欄位（用於類別標籤）或數值欄位（用於長條值）。 |
| **Y-Axis** | 選取互補的欄位。若 X-Axis 為類別欄位，請為 Y-Axis 選取數值欄位（反之亦然）。 |

### 分割

在 **Split by** 下拉式清單中，選取一個欄位，依其值將圖表分割為個別元素。如需詳細資訊，請參閱[分割]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#split)。

### 值選項

| 設定 | 說明 |
| --- | --- |
| **Calculation** | 決定如何將同一類別的多個資料點簡化為單一值。支援的值：**Last \***、**Last**、**First \***、**First**、**Min**、**Max**、**Mean**、**Median**、**Variance**、**Count**、**Distinct count**、**Total**。如需詳細資訊，請參閱[值計算]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/value-calculations/)。 |

### 閾值

如需設定閾值的相關資訊，請參閱[閾值]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/thresholds/)。

### 標準選項

如需設定單位、單位後綴、小數精確度，以及最小值和最大值的相關資訊，請參閱[標準選項]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/standard-options/)。

### 長條量表

| 設定 | 說明 |
| --- | --- |
| **Display style** | 控制長條填滿的呈現方式。**Gradient** 會以根據閾值產生的平滑顏色漸層填滿長條。**Stack** 會為每個閾值範圍顯示不同顏色的區段。**Basic** 會以符合之閾值的單一純色填滿長條。 |
| **Value display** | 控制數值標籤的顏色。**Value Color** 會以對應的閾值顏色為文字著色。**Text Color** 使用預設文字顏色。**Hidden** 會完全隱藏數值。 |
| **Show unfilled area** | 啟用時，會在每個長條已填滿部分的後方顯示灰色背景，讓您更容易看出距離最大值的剩餘差距。 |

### 工具提示

切換 **Show tooltip** 選取器，以啟用或停用工具提示。
