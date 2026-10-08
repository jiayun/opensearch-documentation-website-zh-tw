---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "標準選項"
parent: Configuring visualizations
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 30
---

# 標準選項

標準選項控制視覺化中數值的格式。您可以使用這些選項設定單位、自訂後綴、小數精確度；對於具有刻度的圖表，還可設定最小值與最大值。

## 支援的圖表類型

下表列出各視覺化類型支援的標準選項。

| 視覺化類型 | 最小值與最大值 | 單位 | 單位後綴 | 小數位數 |
| --- | --- | --- | --- | --- |
| [區域圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/area-chart/) | 是 | 是 | 是 | 是 |
| [長條圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/bar-chart/) | 是 | 是 | 是 | 是 |
| [長條量表圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/bar-gauge-chart/) | 是 | 是 | 是 | 是 |
| [量表圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/gauge-chart/) | 是 | 是 | 是 | 是 |
| [熱度圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/heatmap-chart/) | 否 | 是 | 是 | 是 |
| [直方圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/histogram-chart/) | 是 | 是 | 是 | 是 |
| [折線圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/line-chart/) | 是 | 是 | 是 | 是 |
| [指標圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/metric-chart/) | 否 | 是 | 是 | 是 |
| [圓餅圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/pie-chart/) | 否 | 是 | 是 | 是 |
| [散佈圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/scatter-chart/) | 是 | 是 | 是 | 是 |
| [狀態時間軸]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/state-timeline-chart/) | 否 | 否 | 否 | 否 |
| [表格]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/table-chart/) | 否 | 否 | 否 | 否 |

## 選項

下表說明可用的標準選項。

| 設定 | 說明 |
| --- | --- |
| **Min** | 數值刻度的下限。對於笛卡兒圖表，此設定會設定數值軸的最小值。對於量表圖與長條量表圖，此設定會設定刻度的最小值。 |
| **Max** | 數值刻度的上限。對於笛卡兒圖表，此設定會設定數值軸的最大值。對於量表圖與長條量表圖，此設定會設定刻度的最大值。 |
| **Units** | 與數值一起顯示的單位。部分單位（例如貨幣符號）會顯示在數值之前。其他單位則會顯示在數值之後，或自動換算數值。 |
| **Unit suffix** | 附加在單位或數值之後的自訂文字，例如 `/sec`。使用此設定可顯示自訂單位或速率。 |
| **Decimals** | 要顯示的小數位數。將此設定留空即可使用自動精確度。 |

## 單位

**Units** 選單將常用格式分組，例如數字、百分比、貨幣、資料單位、時間單位、重量單位與長度單位。

對於支援換算的單位群組，所選單位會作為輸入單位，視覺化會將數值轉換為同一群組中最易讀的單位。例如，若 **Units** 設為 `bytes(B)`，則數值 `1000` 會顯示為 `1 KB`。

部分單位只會變更顯示的標籤或符號。例如，貨幣單位可在數值之前顯示符號，而百分比單位則會附加 `%`。

下列指標圖在 **Units** 設為 `bytes(B)` 時，顯示底層數值 `7911`。

![單位設為位元組時，指標圖將底層數值 7911 顯示為 7.91 KB]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/metric-chart-unit-byte.png)

## 單位後綴

使用 **Unit suffix** 可在格式化後的數值之後附加自訂文字。這對於速率或自訂單位很有用。

例如，若要在指標圖中顯示位元組速率，請將 **Units** 設為 `bytes(B)`，並將 **Unit suffix** 設為 `/sec`。當 **Decimals** 設為自動精確度時，總位元組數為 `14074` 的底層數值會顯示為 `14.07 KB/sec`。

![單位設為位元組且單位後綴為 /sec 時，指標圖將底層數值 14074 顯示為 14.07 KB/sec]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/metric-chart-unit-byte-suffix.png)

## 小數位數

使用 **Decimals** 可控制數值精確度。例如，輸入 `2` 即可顯示兩位小數。將此設定留空，即可讓視覺化自動選擇精確度。

下列長條圖的 **Units** 設為 `bits(b)`，**Decimals** 設為 `1`。對於笛卡兒圖表，單位格式也會套用至軸標籤。

![單位設為位元且小數位數設為 1 的長條圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/bar-chart-unit-bit-decimal-1.png)

## 最小值與最大值

使用 **Min** 與 **Max** 可定義顯示的數值範圍。

對於笛卡兒圖表（例如區域圖、長條圖、直方圖、折線圖與散佈圖），**Min** 與 **Max** 會設定數值軸的範圍。

下列長條圖的 **Min** 設為 `100`，**Max** 設為 `300`。長條的基準線從 `100` 開始，因此低於此範圍的數值會被截斷，而數值軸會延伸至 `300`。

![最小值設為 100 且最大值設為 300 的長條圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/bar-chart-min-100-max-300.png)

對於量表圖與長條量表圖，**Min** 與 **Max** 會定義刻度邊界。臨界值與填滿範圍都會在此範圍內計算。若留空，視覺化會自動計算範圍。

下圖顯示一個臨界值組態，其中包含基礎色彩，以及位於 `1000`、`1100`、`1700`、`1800`、`1900` 與 `2100` 的級距。

![包含基礎色彩及位於 1000、1100、1700、1800、1900 與 2100 級距的臨界值組態]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/standard-options-threshold-config.png){: width="40%" }

下列量表圖使用該臨界值組態，數值為 `2000`，**Min** 設為 `1200`，**Max** 設為 `2200`。量表刻度會使用此範圍來定位各臨界值區段。

![最小值設為 1200 且最大值設為 2200 時，顯示數值 2000 的量表圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/gauge-min-1200-max-2200.png)
