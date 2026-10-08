---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "區域圖"
parent: Visualization types
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 10
---

# 視覺化編輯器中的區域圖

區域圖會繪製以線條相連的資料點，並填滿每條線下方的區域。使用區域圖可呈現隨時間變化的數量與組成。堆疊多個數列，即可查看每個類別對總計的貢獻。

## 建立區域圖

以下範例會逐步延伸，從基本圖表開始，再逐漸增加複雜度。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/#prerequisites)。

### 基本區域圖

首先使用彙總查詢，計算隨時間變化的事件數量：

```sql
source = opensearch_dashboards_sample_data_logs | stats count() by SPAN(@timestamp, 1d)
```
{% include copy.html %}

執行此查詢後，視覺化編輯器會自動對應欄位：

- **X-Axis** 會顯示 `SPAN(@timestamp, 1d)` 欄位。
- **Y-Axis** 會顯示 `count()` 欄位。

結果是一個顯示每日事件數量的單一填色區域，如下圖所示。

![顯示隨時間變化之數量的基本區域圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/area-chart-basic-result.png){: width="100%" }

### 堆疊區域圖

在查詢中加入第三個維度，依類別將資料分割為多個堆疊數列：

```sql
source = opensearch_dashboards_sample_data_logs | stats count() by SPAN(@timestamp, 1d), response
```
{% include copy.html %}

此查詢會同時依時間與 `response` 欄位（HTTP 狀態碼）將數量分組。選取 `response` 作為 **Color** 欄位，即可為每個狀態碼值（例如 200、404、503）繪製個別的堆疊區域。

結果是以不同顏色顯示每個 HTTP 回應碼的堆疊區域圖。圖表會將各區域上下堆疊，同時呈現各個類別的數量以及所有類別的總計，如下圖所示。

![依 HTTP 回應碼顯示數量的堆疊區域圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/area-chart-stacked-result.png){: width="100%" }

## 設定區域圖

您可以在組態面板中設定下列設定。

### 欄位

在 **Fields** 區段中，設定每個軸上顯示的欄位。

| 欄位 | 說明 |
| --- | --- |
| **X-Axis** | 為水平軸選取日期或數值欄位，用以定義繪製資料所依據的桶 (bucket)（例如 `SPAN(@timestamp, 1d)`）。 |
| **Y-Axis** | 選取一個或多個數值欄位，以個別區域的形式繪製。選取多個欄位時，每個欄位都會繪製為各自的區域圖層。 |
| **Color** | 選取類別欄位，將資料分割為多個堆疊數列，每個數列以不同顏色繪製。例如，使用 `response` 狀態碼欄位，為每個 HTTP 狀態碼顯示個別的堆疊區域。 |

### 分割

在 **Split by** 下拉式清單中選取欄位，即可依值將圖表分割為個別元素。如需更多資訊，請參閱[分割]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#split)。

### 區域

下列設定可控制區域填色、線條樣式與數值顯示。

| 設定 | 說明 |
| --- | --- |
| **Stack** | 控制多個數列的顯示方式。**None** 會重疊顯示數列而不堆疊。**Stack** 會將數列值相加。**Percentage** 會以占總計的百分比堆疊數列。 |
| **Fill opacity** | 設定線條下方填色區域的不透明度。 |
| **Gradient mode** | 控制填色漸層。**None** 使用純色填色。**Opacity** 會使填色朝基準線逐漸淡化。**Hue** 會朝基準線使用較淺的顏色。 |
| **Line style** | 控制圖表要顯示帶有資料點的線條（**Default**）、僅顯示線條（**Line only**），或僅顯示資料點（**Dots only**）。 |
| **Line dash style** | 將線條樣式設定為 **Solid**、**Dashed** 或 **Dotted**。 |
| **Interpolation** | 決定資料點的連接方式。**Straight** 會在資料點之間繪製直線。**Smooth** 會套用曲線。**Stepped** 會建立階梯狀樣式。 |
| **Line width** | 設定線條的粗細（以像素為單位）。支援 1–10 範圍內的值。 |
| **Show values** | 在圖表上顯示數值標籤。 |
| **Show current time marker** | 顯示代表目前時間的垂直標記。只有在 X 軸使用日期欄位時，才能使用此設定。 |

### 閾值

如需設定閾值的相關資訊，請參閱[閾值]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/thresholds/)。

### 標準選項

如需設定單位、單位後綴、小數精確度以及最小值與最大值的相關資訊，請參閱[標準選項]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/standard-options/)。

### 座標軸

X 軸與 Y 軸共用相同的組態選項。如需更多資訊，請參閱[座標軸]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#axes)。

### 圖例

如需設定圖例的相關資訊，請參閱[圖例]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#legend)。

### 工具提示

切換 **Show tooltip** 選取器，即可啟用或停用工具提示。
