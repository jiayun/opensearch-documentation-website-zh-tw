---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "視覺化類型"
parent: Creating visualizations in the Visualize application
grand_parent: Building data visualizations
nav_order: 5
has_children: true
has_toc: false
description: "在 OpenSearch Dashboards 中使用 Visualize 應用程式建立資料視覺化時建議使用的視覺化類型，包括圖表、表格和地圖。"
redirect_from:
  - /dashboards/visualize/viz-types/
---

# 視覺化類型

**Visualize** 應用程式支援下列視覺化類型，並依類別分組。每項說明都提供指引，說明該視覺化類型在何種情況下最有效。如需詳細資訊，請參閱各視覺化類型的個別頁面。

## 文字視覺化

文字視覺化使用文字和數字而非圖形元素來顯示資料。這類視覺化可提供細節，並讓關鍵資料在儀表板上更加醒目。

| 視覺化類型 | 說明 |
| :--- | :--- |
| [**指標視覺化**]({{site.url}}{{site.baseurl}}/dashboards/visualize/metric/) <br><br> ![指標]({{site.url}}{{site.baseurl}}/images/dashboards/metric-chart-1.png){: width="400" } | 醒目地顯示單一數值。適用於 KPI 和摘要統計資料。 |
| [**標籤雲**]({{site.url}}{{site.baseurl}}/dashboards/visualize/tag-cloud/) <br><br> ![標籤雲]({{site.url}}{{site.baseurl}}/images/dashboards/word-cloud-1.png){: width="400" } | 依頻率或其他指標決定文字大小來顯示文字。 |
| [**資料表**]({{site.url}}{{site.baseurl}}/dashboards/visualize/data-table/) <br><br> ![資料表]({{site.url}}{{site.baseurl}}/images/data-table-1.png){: width="400" } | 以表格形式顯示原始或彙總後的資料。 |

## 一維視覺化

一維視覺化顯示單一經過分桶的資料欄位，用於比較各類別的值或顯示比例。

| 視覺化類型 | 說明 |
| :--- | :--- |
| [**儀表視覺化**]({{site.url}}{{site.baseurl}}/dashboards/visualize/gauge/) <br><br> ![儀表]({{site.url}}{{site.baseurl}}/images/dashboards/gauge-1.png){: width="400" } | 在刻度盤上顯示單一數值，並對照已定義的範圍或閾值。 |
| [**目標視覺化**]({{site.url}}{{site.baseurl}}/dashboards/visualize/goal/) <br><br> ![目標]({{site.url}}{{site.baseurl}}/images/dashboards/example-goal-total-km.png){: width="400" } | 在進度列上顯示單一數值，並對照目標值。 |
| [**圓餅圖**]({{site.url}}{{site.baseurl}}/dashboards/visualize/pie-charts/) <br><br> ![圓餅圖]({{site.url}}{{site.baseurl}}/images/dashboards/pie-1.png){: width="400" } | 以圓形的扇區顯示比例資料。適用於部分與整體的比較。 |

## 多維視覺化

多維視覺化將一個或多個資料欄位顯示為另一個資料欄位的函數。用於將資料分桶的彙總使用數值，而非類別值。

| 視覺化類型 | 說明 |
| :--- | :--- |
| [**長條圖**]({{site.url}}{{site.baseurl}}/dashboards/visualize/bar-charts/) <br><br> ![垂直長條圖]({{site.url}}{{site.baseurl}}/images/dashboards/bar-chart-1.png){: width="400" } | 以垂直或水平長條比較類別資料。適用於排名或比較各類別的值。 |
| [**區域圖**]({{site.url}}{{site.baseurl}}/dashboards/visualize/area/) <br><br> ![區域圖]({{site.url}}{{site.baseurl}}/images/dashboards/area-chart-1.png){: width="400" } | 以線條與座標軸之間的填色區域顯示資料。適用於顯示隨時間變化的數量或比較堆疊的類別。 |
| [**熱度圖**]({{site.url}}{{site.baseurl}}/dashboards/visualize/heat-map/) <br><br> ![熱度圖]({{site.url}}{{site.baseurl}}/images/dashboards/heat-map-1.png){: width="400" } | 使用顏色深淺來表示兩個類別維度上的值。 |
| [**折線圖**]({{site.url}}{{site.baseurl}}/dashboards/visualize/line-charts/) <br><br> ![折線圖]({{site.url}}{{site.baseurl}}/images/dashboards/line-1.png){: width="400" } | 繪製以線條連接的資料點。適用於將趨勢和隨時間的變化視覺化。 |

## 地圖視覺化

地圖視覺化依據地理區域或座標繪製資料。

| 視覺化類型 | 說明 |
| :--- | :--- |
| [**座標地圖**]({{site.url}}{{site.baseurl}}/dashboards/visualize/coordinate-maps/) <br><br> ![座標地圖]({{site.url}}{{site.baseurl}}/images/dashboards/coordinate-map-example.png){: width="400" } | 使用經緯度座標在地圖上繪製地理資料點。 |
| [**區域地圖**]({{site.url}}{{site.baseurl}}/dashboards/visualize/region-maps/) <br><br> ![區域地圖]({{site.url}}{{site.baseurl}}/images/dashboards/map-1.png){: width="400" } | 依彙總值為地理區域著色。支援自訂 GeoJSON 向量地圖。 |
| [**Maps 應用程式**]({{site.url}}{{site.baseurl}}/dashboards/visualize/maps/) <br><br> ![Maps]({{site.url}}{{site.baseurl}}/images/dashboards/coordinate-1.png){: width="400" } | 獨立的地圖工具，提供多種圖層類型、工具提示、篩選器和標籤。 |

## 公用程式視覺化

公用程式視覺化不會直接顯示資料，而是在儀表板中輔助其他視覺化。

| 視覺化類型 | 說明 |
| :--- | :--- |
| [**Markdown 視覺化**]({{site.url}}{{site.baseurl}}/dashboards/visualize/markdown/) <br><br> ![Markdown]({{site.url}}{{site.baseurl}}/images/dashboards/markdown.png){: width="400" } | 在資料視覺化旁轉譯 Markdown 文字，以提供背景資訊和操作說明。 |
| [**控制項**]({{site.url}}{{site.baseurl}}/dashboards/visualize/controls/) <br><br> ![控制項]({{site.url}}{{site.baseurl}}/images/dashboards/controls-1.png){: width="400" } | 在儀表板中新增互動式篩選器面板（下拉式清單或範圍滑桿）。 |

## 其他工具

下列視覺化工具使用專用介面，而非標準的彙總式編輯器。

| 視覺化類型 | 說明 |
| :--- | :--- |
| [**PPL 視覺化**]({{site.url}}{{site.baseurl}}/dashboards/visualize/ppl/) <br><br> ![PPL]({{site.url}}{{site.baseurl}}/images/dashboards/ppl-example.png){: width="400" } | 直接輸入 PPL 查詢來建立視覺化。 |
| [**TSVB 視覺化**]({{site.url}}{{site.baseurl}}/dashboards/visualize/tsvb/) <br><br> ![TSVB]({{site.url}}{{site.baseurl}}/images/dashboards/TSVB-1.png){: width="400" } | 建立詳細的時間序列視覺化，支援 Area、Line、Metric、Gauge、Markdown 和 Data Table 類型。 |
| [**Vega 視覺化**]({{site.url}}{{site.baseurl}}/dashboards/visualize/vega/) <br><br> ![Vega]({{site.url}}{{site.baseurl}}/images/dashboards/vega-1.png){: width="400" } | 使用 Vega 和 Vega-Lite 宣告式語法建立自訂視覺化。 |
| [**VisBuilder**]({{site.url}}{{site.baseurl}}/dashboards/visualize/visbuilder/) <br><br> ![VisBuilder]({{site.url}}{{site.baseurl}}/images/dashboards/vis-builder-2.png){: width="400" } | 拖放式工具，不需事先選取圖表類型即可建立視覺化。 |
| [**Timeline 視覺化**]({{site.url}}{{site.baseurl}}/dashboards/visualize/timeline/) <br><br> ![Timeline]({{site.url}}{{site.baseurl}}/images/dashboards/timeline-1.png){: width="400" } | 使用文字型運算式語法建立時間序列視覺化。 |
