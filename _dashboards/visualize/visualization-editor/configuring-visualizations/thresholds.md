---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "閾值"
parent: Configuring visualizations
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 10
---

# 視覺化編輯器中的閾值

閾值是一個邊界值，當資料點達到或超過此值時，會觸發顏色的視覺變化。使用閾值來定義有意義的範圍，以便您能立即了解數值是否處於正常、警告或危急區域。

每個閾值定義了一個數值範圍。基礎閾值適用於所有低於第一個閾值的數值，而每個額外的閾值則從其設定的數值開始，並適用直到下一個閾值開始。例如，如果基礎顏色是綠色，`50` 的閾值是黃色，而 `80` 的閾值是紅色，那麼低於 50 的數值為綠色，50 到低於 80 的數值為黃色，而 80 或更高的數值則為紅色。

## 支援的圖表類型

閾值可用於以下圖表類型：

- [區域圖 (Area chart)]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/area-chart/)
- [長條圖 (Bar chart)]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/bar-chart/)
- [長條儀表圖 (Bar gauge chart)]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/bar-gauge-chart/)
- [儀表圖 (Gauge chart)]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/gauge-chart/)
- [熱圖 (Heatmap)]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/heatmap-chart/)
- [直方圖 (Histogram)]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/histogram-chart/)
- [折線圖 (Line chart)]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/line-chart/)
- [指標圖 (Metric chart)]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/metric-chart/)
- [散佈圖 (Scatter plot)]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/scatter-chart/)
- [狀態時間軸 (State timeline)]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/state-timeline-chart/)
- [表格 (Table)]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/table-chart/)

## 設定閾值

若要新增閾值，請開啟組態面板中的 **Thresholds** 區段，然後選取 **+ Add threshold**。針對每個閾值，設定以下設定。

| 設定 | 說明 |
| :--- | :--- |
| **Color** | 選取要套用於落在該閾值範圍內之數值的顏色。可選取預設顏色或自訂顏色。 |
| **Value** | 輸入此閾值開始的數值邊界。等於或大於此數值（且低於下一個閾值）的數值將以該顏色顯示。 |

OpenSearch Dashboards 會自動按數值對閾值進行排序。基礎閾值始終存在，且代表所有低於其他閾值之數值的起始顏色。您可以更改基礎顏色，但不能刪除基礎閾值或為其設定數值。若要刪除任何其他閾值，請選取其旁邊的垃圾桶圖示。

## 各圖表類型的閾值效果

閾值的套用方式根據圖表類型而有所不同。某些視覺化使用閾值來為圖表標記著色，某些將閾值作為參考線，而某些則需要額外的圖表特定設定，例如 **Use threshold colors** 或 **Cell style**。下表說明了閾值在每種圖表類型中的套用方式。

| 圖表類型 | 閾值效果 | 額外設定 |
| :--- | :--- | :--- |
| Gauge | 根據閾值範圍為儀表弧線著色。當開啟 **Use threshold colors** 時，顯示的數值也會使用對應的閾值顏色。 | 開啟 **Use threshold colors**。 |
| Bar gauge | 根據閾值範圍為長條儀表著色。視覺結果還取決於所選的顯示樣式，例如漸變 (gradient)、堆疊 (stack) 或基本 (basic)。 | 無。 |
| Metric | 根據指標數值和所選的顏色模式，為指標數值或背景著色。 | 設定 **Color mode**，然後開啟 **Use threshold colors**。 |
| Line and area | 將閾值數值顯示為水平參考線。線條或區域標記本身不會改變顏色。 | 將 **Threshold lines mode** 設定為 **Solid lines**、**Dashed lines** 或 **Dotted lines**。 |
| Bar and histogram | 當開啟閾值顏色時，根據數值範圍為長條著色。您也可以顯示閾值參考線。 | 開啟 **Use threshold colors** 以為長條著色。設定 **Threshold lines mode** 以顯示參考線。 |
| Heatmap | 根據數值範圍為儲存格著色，覆蓋所選的顏色方案。 | 開啟 **Use threshold colors**。 |
| Scatter | 當開啟閾值顏色時，根據數值範圍為點著色。您也可以顯示閾值參考線。 | 開啟 **Use threshold colors** 以為點著色。設定 **Threshold lines mode** 以顯示參考線。 |
| State timeline | 根據數值範圍為狀態區域著色，覆蓋數值對應 (value mapping) 的顏色。 | 開啟 **Use threshold color**。 |
| Table | 根據數值範圍為數值表格儲存格著色。 | 在 **Cell style** 中，選取一個數值欄位，然後選取 **Colored Text** 或 **Colored Background**。 |

狀態時間軸圖表還包含根據時間閾值來斷開數值和連接 null 數值的設定。這些設定控制時間軸中的間隙，不會影響本頁面所述的顏色閾值。
{: .note}

## 閾值範例

以下範例顯示如何使用 OpenSearch Dashboards 範例資料將閾值套用到每種支援的圖表類型。

### 儀表圖

在儀表圖中，閾值直接為弧線著色。**Standard options** 下的 **Min** 和 **Max** 控制項定義了刻度範圍，而閾值將該刻度劃分為彩色段。若要將閾值套用到儀表圖，請執行以下步驟：

1. 選取 `opensearch_dashboards_sample_data_logs` 資料集。
1. 輸入以下查詢並選取 **Update**：

   ```sql
   | stats avg(bytes) by span(`@timestamp`, 5m)
   ```
   {% include copy.html %}

1. 選取 **Gauge** 作為視覺化類型。
1. 在 **Gauge** 區段中，開啟 **Use threshold colors**。
1. 開啟 **Thresholds** 區段並選取 **+ Add threshold**。
1. 將基礎顏色設定為綠色，並在 `6000`、`8000` 和 `10000` 建立閾值。

弧線會根據每個範圍使用閾值顏色，且顯示的數值會使用對應的閾值顏色，如下圖所示。

![具有閾值著色弧線且數值以對應閾值顏色顯示的儀表圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/gauge-chart-threshold-result.png){: width="100%" }

### 長條儀表圖

在長條儀表圖中，閾值定義了每個長條的彩色範圍。結果取決於所選的顯示樣式：

- **Gradient** 顯示跨閾值顏色的平滑過渡。
- **Stack** 將長條劃分為不同的閾值段。
- **Basic** 使用包含該數值的閾值範圍為長條著色。

若要將閾值套用到長條儀表圖，請執行以下步驟：

1. 選取 `opensearch_dashboards_sample_data_logs` 資料集。
1. 輸入以下查詢並選取 **Update**：

   ```sql
   | stats avg(bytes) by span(`@timestamp`, 5m), extension
   ```
   {% include copy.html %}

1. 選取 **Bar Gauge** 作為視覺化類型。
1. 在 **Fields** 區段中，將 **X-Axis** 設定為 `extension`，將 **Y-Axis** 設定為 `AVG(bytes)`。
1. 在 **Thresholds** 區段中，將閾值設定為 `3000`、`5000` 和 `8000`。
1. 在 **Bar Gauge** 區段中，選取 **Display style**。

每個長條會根據包含其數值的閾值範圍著色，如下圖所示。

![每個長條根據其閾值範圍著色的長條儀表圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/bar-gauge/bar-gauge-threshold-result.png){: width="100%" }

### 指標圖表

在指標圖表中，閾值會根據所選的 **Color mode** 為顯示的值或其背景著色。若要將閾值套用至指標圖表，請依照下列步驟操作：

1. 選取 `opensearch_dashboards_sample_data_logs` 資料集。
1. 輸入下列查詢，然後選取 **Update**：

   ```sql
   | stats avg(bytes) by span(`@timestamp`, 5m), extension
   ```
   {% include copy.html %}

1. 選取 **Metric** 作為視覺化類型。
1. 在 **Metric** 區段中，將 **Color mode** 設為 **Background gradient**，並開啟 **Use threshold colors**。
1. 在 **Thresholds** 區段中，將閾值設為 `4000`、`6000` 和 `8000`。

每個指標的背景會使用包含該指標值的閾值範圍顏色，如下圖所示。

![將閾值顏色套用至每個指標背景的指標圖表]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/metric-chart-threshold-result.png){: width="100%" }

### 折線圖與面積圖

在折線圖與面積圖中，閾值會以橫跨圖表的水平參考線形式顯示。線條或面積標記本身不會改變顏色。若要在折線圖或面積圖中新增閾值線，請依照下列步驟操作：

1. 選取 `opensearch_dashboards_sample_data_logs` 資料集。
1. 輸入下列查詢，然後選取 **Update**：

   ```sql
   | stats avg(bytes) by span(`@timestamp`, 5m)
   ```
   {% include copy.html %}

1. 選取 **Line** 作為視覺化類型。
1. 開啟 **Thresholds** 區段，然後選取 **+ Add threshold**。
1. 將閾值設為 `5000` 和 `8000`。
1. 將 **Threshold lines mode** 設為 **Dashed lines**。

每個閾值會出現一條水平虛線，如下圖所示。

![每個閾值處皆有水平虛線參考線的折線圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/line-area-threshold-lines.png){: width="100%" }

使用 **Threshold lines mode** 設定來控制線條外觀：

- **Off**：不顯示閾值線。
- **Solid lines**：在每個閾值處繪製水平實線。
- **Dashed lines**：在每個閾值處繪製水平虛線。
- **Dotted lines**：在每個閾值處繪製水平點線。

### 長條圖與直方圖

在長條圖與直方圖中，閾值可根據每個長條的值為其著色。這些圖表類型也可以顯示閾值參考線。若要將閾值顏色套用至長條圖，請依照下列步驟操作：

1. 選取 `opensearch_dashboards_sample_data_logs` 資料集。
1. 輸入下列查詢，然後選取 **Update**：

   ```sql
   | stats avg(bytes) by extension
   ```
   {% include copy.html %}

1. 選取 **Bar** 作為視覺化類型。
1. 在 **Fields** 區段中，將 **X-Axis** 設為 `extension`，將 **Y-Axis** 設為 `AVG(bytes)`。
1. 在 **Bar** 區段中，開啟 **Use threshold colors**。
1. 在 **Thresholds** 區段中，將閾值設為 `2000`、`4000` 和 `6000`。
1. 將 **Threshold lines mode** 設為 **Off**。

每個長條會依據包含其值的閾值範圍著色，如下圖所示。

![每個長條皆依其閾值範圍著色的長條圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/bar-histogram-threshold-result.png){: width="100%" }

### 熱圖

在熱圖中，閾值會依據值範圍為儲存格著色，並覆寫所選的色彩配置。若要將閾值套用至熱圖，請依照下列步驟操作：

1. 選取 `opensearch_dashboards_sample_data_logs` 資料集。
1. 輸入下列查詢，然後選取 **Update**：

   ```sql
   | stats avg(bytes) by extension, `machine.os`
   ```
   {% include copy.html %}

1. 選取 **Heatmap** 作為視覺化類型。
1. 在 **Fields** 區段中，將 **X-Axis** 設為 `extension`，將 **Y-Axis** 設為 `machine.os`，並將 **Value** 設為 `AVG(bytes)`。
1. 在 **Heatmap** 區段中，開啟 **Use threshold colors**。
1. 在 **Thresholds** 區段中，將閾值設為 `4000`、`6000` 和 `8000`。

每個儲存格會依據包含其值的閾值範圍著色，如下圖所示。

![每個儲存格皆依其閾值範圍著色的熱圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/heatmap/heatmap-threshold-colors.png){: width="100%" }

### 散佈圖

在散佈圖中，閾值可依據每個點的值為點著色。散佈圖也可以顯示閾值參考線。若要將閾值套用至散佈圖，請依照下列步驟操作：

1. 選取 `opensearch_dashboards_sample_data_flights` 資料集，然後選取 **Update**。
1. 選取 **Scatter** 作為視覺化類型。
1. 在 **Fields** 區段中，將 **X-Axis** 設為 `DistanceMiles`，將 **Y-Axis** 設為 `AvgTicketPrice`。
1. 開啟 **Thresholds** 區段，然後選取 **+ Add threshold**。
1. 將閾值設為 `400`、`600` 和 `800`。

每個點會依據包含其票價之閾值範圍著色，如下圖所示。

![每個點皆依其票價之閾值範圍著色的散佈圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/scatter-threshold-result.png){: width="100%" }

### 狀態時間軸

在狀態時間軸中，閾值會依據數值範圍為狀態區域著色。當顏色代表一個範圍（例如成功、警告和錯誤的回應碼）而非單一值時，請使用閾值。若要將閾值套用至狀態時間軸，請依照下列步驟操作：

1. 選取 `opensearch_dashboards_sample_data_logs` 資料集。
1. 輸入下列查詢，然後選取 **Update**：

   ```sql
   | FIELDS @timestamp, response
   ```
   {% include copy.html %}

1. 選取 **State Timeline** 作為視覺化類型。
1. 在 **Fields** 區段中，將 **X-Axis** 設為 `@timestamp`，將 **Color** 設為 `response`。由於 `response` 欄位是數值，OpenSearch Dashboards 可以將其劃分為閾值範圍。
1. 在 **Thresholds** 區段中，將基礎顏色保持為綠色，並將閾值設為 `400` 和 `500`。
1. 在 **State Timeline** 區段中，開啟 **Use threshold color**。若要僅顯示閾值著色區域，請保持 **Show display text** 關閉。

時間軸區域會依據回應碼範圍著色：值從 `0` 到小於 `400`、值從 `400` 到小於 `500`，以及值為 `500` 或更大，如下圖所示。

![區域依回應碼範圍著色的狀態時間軸]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/state-timeline/state-timeline-threshold-colors.png){: width="100%" }

### 表格

在表格中，閾值會為數值儲存格著色。若要將閾值套用至表格，請依照下列步驟操作：

1. 選取 `opensearch_dashboards_sample_data_flights` 資料集。
1. 輸入下列查詢，然後選取 **Update**：

   ```sql
   | FIELDS AvgTicketPrice, Carrier, Dest, Origin
   ```
   {% include copy.html %}

1. 選取 **Table** 作為視覺化類型。
1. 在 **Table** 區段中，將 **Cell style** 設為 `AvgTicketPrice` 並選取 **Colored Background**。
1. 在 **Threshold** 區段中，將閾值設為 `400`、`600` 和 `1000`。

每個 `AvgTicketPrice` 儲存格背景會依據包含其值的閾值範圍著色，如下圖所示。

![數值儲存格背景依閾值範圍著色的表格]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/table-threshold-cells.png){: width="100%" }
