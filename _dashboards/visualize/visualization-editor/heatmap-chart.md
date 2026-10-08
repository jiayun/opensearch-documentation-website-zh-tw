---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "熱圖"
parent: Visualization types
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 30
---

# 視覺化編輯器中的熱圖

熱圖使用顏色來表示資料集中數值的大小。圖中的每個儲存格對應兩個維度的一種組合，而儲存格的顏色深淺則反映該組合所對應的數值。

## 建立熱圖

以下範例逐步延伸，從基本熱圖開始，並逐漸增加複雜度。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/#prerequisites)。

### 基本熱圖

首先使用一個依兩個類別欄位彙總數值指標的查詢：

```sql
source = opensearch_dashboards_sample_data_flights | where FlightDelay = true | stats avg(FlightDelayMin) as avg_delay by OriginWeather, DestWeather
```
{% include copy.html %}

執行此查詢後，選取 **Heatmap** 作為圖表類型。欄位的對應方式如下：

- **X-Axis** 顯示 `OriginWeather` 欄位。
- **Y-Axis** 顯示 `DestWeather` 欄位。
- **Value** 顯示 `avg_delay` 欄位。

結果會是一個由彩色儲存格組成的網格，其中每個儲存格代表特定出發地與目的地天氣組合的平均航班延誤分鐘數。顏色越深的儲存格表示數值越高，如下圖所示。

![依天氣狀況顯示平均航班延誤分鐘數的基本熱圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/heatmap/heatmap-initial.png){: width="100%" }

### 自訂色彩配置與比例尺

為了更清楚地區分數值，請變更色彩設定：

1. 在 **Heatmap** 區段中，將 **Color schema** 變更為其他色盤（例如 **Yellow to Orange**）以提高對比度。
2. 啟用 **Scale to data bounds**，將色彩範圍對應至資料的實際最小值與最大值，而非計算出的邊界。
3. 變更 **Max number of colors** 以增加或減少色彩區間的精細程度，如下圖所示。

![使用自訂色彩配置與比例尺的熱圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/heatmap/heatmap-custom-colors.png){: width="100%" }

### 啟用標籤

若要在每個儲存格內顯示數值，請啟用 **Show labels**。如果儲存格較窄，請啟用 **Rotate** 將標籤傾斜，以提高可讀性，如下圖所示。

![在儲存格中顯示數值標籤的熱圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/heatmap/heatmap-with-labels.png){: width="100%" }

## 設定熱圖

您可以在組態面板中設定下列設定。

### 欄位

在 **Fields** 區段中，設定每個座標軸上顯示的欄位。

| 欄位 | 說明 |
| --- | --- |
| **X-Axis** | 選取要沿水平軸顯示的類別欄位。每個唯一值都會成為熱圖網格中的一欄。 |
| **Y-Axis** | 選取要沿垂直軸顯示的類別欄位。每個唯一值都會成為熱圖網格中的一列。 |
| **Value** | 選取一個數值欄位，其大小決定每個儲存格的顏色深淺。每個儲存格代表一個 X-Axis 類別與一個 Y-Axis 類別的交集。 |

### 分割

在 **Split by** 下拉式清單中，選取一個欄位，依其值將圖表分割為個別元素。如需詳細資訊，請參閱[分割]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#split)。


### 熱圖

使用下列設定自訂熱圖的外觀。

| 設定 | 說明 |
| --- | --- |
| **Use threshold colors** | 啟用時，儲存格顏色會依閾值範圍決定，而非依所選的色彩配置。 |
| **Color schema** | 控制用於表示各儲存格數值的色彩主題。支援的值：**Greens**、**Blues**、**Reds**、**Greys**、**Green to Blue**、**Yellow to Orange**。 |
| **Reverse schema** | 啟用時，色彩對應會反轉：較高的數值以較淺的顏色表示，較低的數值則以較深的顏色表示。 |
| **Color scale** | 定義資料值對應至顏色的方式。支援的值：**Linear**、**Log**、**Sqrt**。 |
| **Scale to data bounds** | 啟用時，會從資料集計算最小值與最大值，並據此對應色彩比例尺。 |
| **Percentage mode** | 啟用時，數值會轉換為百分比，且色彩比例尺會正規化至 0 到 1 之間。 |
| **Max number of colors** | 控制色彩比例尺中使用的離散色彩區間數量上限。 |
| **Show labels** | 啟用時，會在每個儲存格內以標籤顯示數值。 |

啟用 **Show labels** 時，可使用下列設定。

| 設定 | 說明 |
| --- | --- |
| **Rotate** | 啟用時，會將數值標籤旋轉 45 度，以提高窄儲存格中的可讀性。 |
| **Overwrite automatic color** | 啟用時，會設定自訂標籤顏色。 |
| **Color** | 在啟用 **Overwrite automatic color** 時設定自訂標籤顏色。 |

### 閾值

如需設定閾值的相關資訊，請參閱[閾值]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/thresholds/)。

### 標準選項

如需設定單位、單位後綴與小數精確度的相關資訊，請參閱[標準選項]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/standard-options/)。

### 座標軸

X 軸與 Y 軸共用相同的組態選項。如需詳細資訊，請參閱[座標軸]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#axes)。

### 圖例

圖例彙整了圖表中使用的視覺色彩編碼。

| 設定 | 說明 |
| --- | --- |
| **Show legend** | 顯示或隱藏圖例。 |
| **Position** | 控制圖例相對於圖表的顯示位置。支援的值：**Left**、**Right**、**Top**、**Bottom**。 |

### 工具提示

切換 **Show tooltip** 選取器以啟用或停用工具提示。
