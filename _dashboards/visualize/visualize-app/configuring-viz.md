---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定視覺化"
parent: Creating visualizations in the Visualize application
grand_parent: Building data visualizations
nav_order: 200
redirect_from:
  - /dashboards/visualize/viz-tool-ref/
---

# 設定視覺化

組態面板位於 **Visualize** 應用程式的右側。視所編輯的視覺化類型而定，組態面板會包含兩個以上的索引標籤。如需術語定義，請參閱[概念]({{site.url}}{{site.baseurl}}/dashboards/getting-started/concepts/)。

組態面板包含下列索引標籤：

- **Data** 索引標籤可讓您將指標和資料桶 (bucket) 新增至視覺化。
- **Metrics and axes** 索引標籤控制顯示選項，例如座標軸、標籤和刻度的顯示方式；文字的顯示和對齊方式，以及視覺化專屬的選項。對於某些視覺化類型，此索引標籤會標示為 **Options**。
- **Panel settings** 索引標籤包含適用於整個面板的設定選項，例如圖例、工具提示和格線。

## Data 索引標籤

**Data** 索引標籤使用[彙總]({{site.url}}{{site.baseurl}}/aggregations/)來決定要顯示哪些資料，以及資料的分組方式。當您設定視覺化時，OpenSearch Dashboards 會根據您的選擇自動產生彙總查詢。如需實際操作的逐步說明，請參閱[建立以彙總為基礎的視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/aggregation-based-viz/)。

下列視覺化類型使用搭配彙總的 **Data** 索引標籤：**Area**、**Horizontal Bar**、**Vertical Bar**、**Coordinate Map**、**Data Table**、**Gauge**、**Goal**、**Heat Map**、**Line**、**Metric**、**Pie**、**Region Map** 和 **Tag Cloud**。
{: .note}

下圖顯示典型的 **Data** 索引標籤。

![視覺化工具的 Data 設定]({{site.url}}{{site.baseurl}}/images/dashboards/viz-tools-data.png){: width="600" }

**Data** 索引標籤通常包含兩種類型的面板，用於將元素新增至視覺化：

- **Y-axis**、**Data** 或 **Metrics** 面板，用於選擇要顯示的一個或多個欄位
- **X-axis** 或 **Buckets** 面板，用於選擇如何分割資料以供顯示

**Metrics** 和 **Buckets** 面板都使用 _漸進式揭露_，也就是說，您後續可用的選項取決於您在面板中的上一個選擇。選擇指標或桶的典型順序如下：

1. 從可用選項的下拉式清單中選取彙總類型，例如平均值、計數、最大值或最小值。

1. 從下拉式清單中選取欄位。可選取的欄位僅限於您所選彙總可套用的資料類型。例如，**Count** 彙總適用於整份文件，因此不會顯示欄位選項。**Date Histogram** 彙總僅適用於時間戳記欄位。

1. 視需要選取其他選項，例如範圍間隔，或用於在視覺化中標示該欄位的自訂名稱。

1. 視需要新增更多欄位或桶。例如，在選擇直方圖作為 _X-axis_ 桶類型，以長條圖顯示各產品類別的成本變數之後，您可以新增 _split chart_ 桶，為每種顧客性別分別顯示一張長條圖。

### 指標彙總

指標彙總會出現在 **Metrics** 面板中，並成為圖表中的 Y 軸值。下表列出可用的指標彙總。

| 指標 | 說明 | 需要欄位 |
| :--- | :--- | :--- |
| `Count` | 計算每個桶中的文件數量。這是新視覺化的預設指標，不需要選取欄位。在彙總 API 中，每個[桶彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/)回應都包含 `doc_count` 欄位，其中包含該桶中的文件數量，而 `Count` 會顯示此值。 | 否 |
| [`Average`]({{site.url}}{{site.baseurl}}/aggregations/metric/average/) | 計算數值欄位的平均值。 | 是 |
| [`Max`]({{site.url}}{{site.baseurl}}/aggregations/metric/maximum/) | 傳回數值欄位的最大值。 | 是 |
| [`Median`]({{site.url}}{{site.baseurl}}/aggregations/metric/percentile/) | 傳回數值欄位的第 50 百分位數值。在彙總 API 中，這會使用第 50 等級的 `percentiles` 彙總。 | 是 |
| [`Min`]({{site.url}}{{site.baseurl}}/aggregations/metric/minimum/) | 傳回數值欄位的最小值。 | 是 |
| [`Percentile Ranks`]({{site.url}}{{site.baseurl}}/aggregations/metric/percentile-ranks/) | 傳回指定值在數值欄位中的百分位等級。選取後，請在 **Values** 清單中輸入閾值，以定義要計算等級的位置點。 | 是 |
| [`Percentiles`]({{site.url}}{{site.baseurl}}/aggregations/metric/percentile/) | 傳回數值欄位在指定百分位等級的值。選取後，請設定 **Percents** 清單，以定義要計算的百分位數。預設值為 1、5、25、50、75、95 和 99。每個百分位數會在視覺化中顯示為個別的數列。 | 是 |
| [`Standard Deviation`]({{site.url}}{{site.baseurl}}/aggregations/metric/extended-stats/) | 計算數值欄位的標準差。在彙總 API 中，這會使用 `extended_stats` 彙總。 | 是 |
| [`Sum`]({{site.url}}{{site.baseurl}}/aggregations/metric/sum/) | 計算數值欄位的總和。 | 是 |
| [`Top Hit`]({{site.url}}{{site.baseurl}}/aggregations/metric/top-hits/) | 傳回欄位中依指定指標排序的一個或多個最高值。選取後，請設定 **Aggregate with**（多個值的合併方式：`Concat`、`Min`、`Max`、`Sum` 或 Average）、**Size**（要傳回的最高值數量）、**Sort on**（排序依據的欄位）和 **Order**（遞增或遞減）。 | 是 |
| [`Unique Count`]({{site.url}}{{site.baseurl}}/aggregations/metric/cardinality/) | 計算欄位中相異值的數量。在彙總 API 中，這對應於 `cardinality` 彙總。 | 是 |

### 父管線彙總

父管線彙總會根據同一個桶內另一個指標的輸出計算值。這些彙總會出現在 **Metrics** 面板中基本指標彙總的下方。

選取父管線彙總後，請使用 **Metric** 下拉式清單選擇要運算的指標。您可以從 Y 軸選取現有指標，或選取 **Custom metric** 以內嵌方式定義新指標（這會顯示一個巢狀彙總選取器，您可以在其中設定任何基本指標彙總）。

| 指標 | 說明 |
| :--- | :--- |
| [`Cumulative Sum`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/cumulative-sum/) | 計算指標在依序排列的各桶之間的累計總和。 |
| [`Derivative`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/derivative/) | 計算指標在連續桶之間的變化率。 |
| [`Moving Avg`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/moving-avg/) | 計算指標在桶的滑動視窗上的移動平均值。 |
| [`Serial Diff`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/serial-diff/) | 計算指標值與數列中較早值之間的差異。 |

### 同層級管線彙總

同層級管線彙總會從同層級彙總的所有桶計算出單一值，並將其與其他指標一起顯示。這些彙總會出現在 **Metrics** 面板中父管線彙總的下方。

與父管線彙總相同，同層級管線彙總也使用 **Metric** 下拉式清單選取要運算的指標。您可以選取現有指標，或選取 **Custom metric** 以內嵌方式定義指標。

| 指標 | 說明 |
| :--- | :--- |
| [`Average Bucket`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/avg-bucket/) | 計算指標在所有桶中的平均值。 |
| [`Max Bucket`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/max-bucket/) | 傳回指標在所有桶中的最大值。 |
| [`Min Bucket`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/min-bucket/) | 傳回指標在所有桶中的最小值。 |
| [`Sum Bucket`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/sum-bucket/) | 計算指標在所有桶中的總和。 |

### 桶彙總

桶彙總會顯示在 **Buckets** 面板中，用來決定資料的分組方式。當您在 **Buckets** 面板中選取 **Add** 時，首先要選擇桶 (bucket) 類型：

| 桶類型 | 說明 |
| :--- | :--- |
| X-axis | 沿著圖表的水平軸將資料分組。 |
| Split series | 在同一張圖表中建立多個數列（折線、長條或區域），每個數列代表不同的群組。 |
| Split chart | 為每個群組建立個別的圖表，並以列或欄的版面配置顯示。 |

選擇桶類型後，您需要選取桶彙總來定義資料的分組方式。下表列出可用的桶彙總。

| 彙總 | 說明 |
| :--- | :--- |
| [`Date Histogram`]({{site.url}}{{site.baseurl}}/aggregations/bucket/date-histogram/) | 將文件分組至時間間隔（例如每小時、每天或每週）。需要日期欄位。 |
| [`Date Range`]({{site.url}}{{site.baseurl}}/aggregations/bucket/date-range/) | 將文件分組至您定義的自訂日期範圍。需要日期欄位。 |
| [`Filters`]({{site.url}}{{site.baseurl}}/aggregations/bucket/filters/) | 依您定義的自訂查詢篩選條件將文件分組。每個篩選條件會建立一個桶。 |
| [`Histogram`]({{site.url}}{{site.baseurl}}/aggregations/bucket/histogram/) | 將數值分組至固定大小的間隔。需要數值欄位。 |
| [`IPv4 Range`]({{site.url}}{{site.baseurl}}/aggregations/bucket/ip-range/) | 將文件分組至自訂的 IP 位址範圍。需要 IP 欄位。 |
| [`Range`]({{site.url}}{{site.baseurl}}/aggregations/bucket/range/) | 將數值分組至您定義的自訂範圍。需要數值欄位。 |
| [`Significant Terms`]({{site.url}}{{site.baseurl}}/aggregations/bucket/significant-terms/) | 找出在所選資料集中出現頻率高於整體索引的詞彙。需要 keyword 或 text 欄位。 |
| [`Terms`]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms/) | 依欄位的唯一值將文件分組。需要 keyword、數值、IP 或布林值欄位。 |

如需桶彙總類型的詳細資訊，請參閱[桶彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/)。


## 指標與座標軸索引標籤

下圖顯示典型的 **Metrics** 索引標籤。

![視覺化工具的指標與座標軸設定]({{site.url}}{{site.baseurl}}/images/dashboards/viz-tools-metrics.png){: width="600" }

與 **Data** 索引標籤相同，**Metrics and axes**（或 **Options**）索引標籤的內容取決於視覺化類型以及您所選取資料的具體特性。選項差異很大，但通常可分為以下類別。此清單並未列出所有選項：


### 指標選項

指標或顯示選項包括：

- 圖形的外觀形式，例如量表的 Circle 或 Arc；或 Line/Bar/Area 圖表類型
- 視覺化專屬選項，例如 Stacked 或 Normal（重疊）區域圖
- 是否在折線圖中顯示線條與點、線條寬度，以及線條樣式（例如直線或平滑）
- 範圍寬度
- 色彩配置（例如用於熱度圖）


### 座標軸選項

X 軸與 Y 軸選項包括：

- 座標軸的位置
- 模式，例如一般刻度或百分比刻度
- 是否顯示或截斷標籤，以及標籤的對齊方式
- 座標軸的自訂標題
- 是否顯示座標軸線與刻度線


## 面板設定

下圖顯示典型的 **Panel settings** 索引標籤。

![視覺化工具的面板設定]({{site.url}}{{site.baseurl}}/images/dashboards/viz-tools-panel.png){: width="600" }

**Panel settings** 索引標籤可控制整個面板的顯示選項，例如：

- 變更圖例的位置
- 顯示閾值線
- 在時間軸上醒目提示目前時間
- 顯示或隱藏垂直或水平格線
- 在圖表上標示數值


## 圖例色彩

在以色彩表示範圍、類別或文字變數的圖表中，圖例會顯示色彩對照。

您可以使用圖例來變更圖形元素的色彩。若要變更色彩，請依照下列步驟操作：

1. 選取圖例中的項目。

2. 從出現的調色盤中選擇色彩。

![視覺化圖例]({{site.url}}{{site.baseurl}}/images/dashboards/legend-colors.png){: width="300" }

## 後續步驟

- 如需實作教學，請參閱[建立以彙總為基礎的視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/aggregation-based-viz/)。 