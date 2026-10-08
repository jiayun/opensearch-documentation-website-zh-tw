---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "散佈圖"
parent: Visualization types
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 55
---

# 視覺化編輯器中的散佈圖

散佈圖可將兩個數值變數之間的關係視覺化。圖表上的每個點代表資料集中的一筆觀測值，其位置由這兩個變數的值決定。您可以依類別欄位分割資料，以比較不同群組在相同維度上的分布情形。

## 建立散佈圖

以下範例會逐步延伸，先從基本的雙變數散佈圖開始，再加入其他維度。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/#prerequisites)。

### 基本散佈圖

首先使用會傳回兩個數值欄位的查詢：

```sql
source = opensearch_dashboards_sample_data_flights | fields AvgTicketPrice, DistanceMiles
```
{% include copy.html %}

執行此查詢後，選取 **Scatter** 作為圖表類型。欄位的對應方式如下：

- **X-Axis** 顯示 `AvgTicketPrice` 欄位。
- **Y-Axis** 顯示 `DistanceMiles` 欄位。

結果會產生一張顯示機票價格與飛行距離之間關係的散佈圖。每個點代表一個航班，如下圖所示。

![顯示平均機票價格與距離比較的基本散佈圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/scatter/scatter-two-num-fields.png){: width="100%" }

### 使用閾值

若要套用閾值，請在 **Scatter** 區段中啟用 **Use threshold colors**。接著開啟 **Thresholds** 區段，並新增 `6000` 的閾值以醒目標示長途航班，如下圖所示。

![閾值為 6000 並醒目標示長途航班的散佈圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/scatter/scatter-with-threshold.png){: width="100%" }

如需更多資訊，請參閱[閾值]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/thresholds/)。

### 新增色彩維度

新增類別欄位，將資料點分割成以色彩區分的群組：

```sql
source = opensearch_dashboards_sample_data_flights | fields AvgTicketPrice, DistanceMiles, DestWeather
```
{% include copy.html %}

此查詢會傳回兩個數值欄位：`AvgTicketPrice` 和 `DistanceMiles`。選取 `DestWeather` 作為 **Color** 欄位。

結果會產生一張資料點分割成以色彩區分群組的散佈圖，每種天氣狀況都以不同的色彩呈現，如下圖所示。

![以色彩區分天氣類別的散佈圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/scatter/scatter-two-numerical-one-cate-fields.png){: width="100%" }

### 新增大小維度

新增第三個數值欄位以控制點的大小，藉此建立泡泡圖：

```sql
source = opensearch_dashboards_sample_data_flights | fields AvgTicketPrice, DistanceMiles, DestWeather, FlightDelayMin
```
{% include copy.html %}

此查詢會傳回三個數值欄位：`AvgTicketPrice`、`DistanceMiles` 和 `FlightDelayMin`。選取 `DestWeather` 作為 **Color** 欄位，並將 `FlightDelayMin` 對應至 **Size** 欄位。

現在各點的大小會有所不同，較大的泡泡代表較長的延誤時間。每種色彩仍代表一種天氣狀況，因此您可以判斷特定天氣類型是否同時與較高的價格及較長的延誤相關，如下圖所示。

![以大小表示航班延誤分鐘數的散佈圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/scatter/scatter-two-numerical-one-cate-fields-one-size.png){: width="100%" }

## 設定散佈圖

您可以在組態面板中設定下列設定。

### 欄位

在 **Fields** 區段中，設定各軸上顯示的欄位。

| 組態 | 欄位 | 說明 |
| :---| :---| :---|
| **兩個數值** | X-Axis (數值)、Y-Axis (數值) | 選取兩個數值欄位，以顯示呈現兩個數值變數之間關係的資料點。 |
| **兩個數值 + 一個類別** | X-Axis (數值)、Y-Axis (數值)、Color (類別) | 選取兩個數值欄位和一個類別 Color 欄位，以顯示分割成以色彩區分群組的資料點。 |
| **三個數值 + 一個類別** | X-Axis (數值)、Y-Axis (數值)、Size (數值)、Color (類別) | 選取三個數值欄位和一個類別 Color 欄位，以顯示用色彩表示類別、並由第三個數值欄位控制點大小的資料點。 |

### 分割

在 **Split by** 下拉式清單中，選取一個欄位，依值將圖表分割成不同的元素。如需更多資訊，請參閱[分割]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#split)。

### 散佈

使用下列設定自訂散佈圖的外觀。

| 設定 | 說明 |
| :---| :---|
| **Point size** | 控制未對應 Size 欄位時資料點的預設大小。 |
| **Shape** | 控制每個資料點的形狀。支援的值：**Circle**、**Square**、**Diamond**、**Cross**。 |
| **Filled** | 啟用時，資料點會填滿色彩。停用時，只會呈現外框。 |
| **Angle** | 控制每個資料點的顯示角度 (以度為單位)。支援 0–360 範圍內的值。 |

### 閾值

如需設定閾值的相關資訊，請參閱[閾值]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/thresholds/)。

### 標準選項

如需設定單位、單位後綴、小數精確度以及最小值和最大值的相關資訊，請參閱[標準選項]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/standard-options/)。

### 座標軸

X 軸和 Y 軸共用相同的組態選項。如需更多資訊，請參閱[座標軸]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#axes)。

### 圖例

圖例彙整了圖表中使用的視覺色彩編碼。

| 設定 | 說明 |
| :---| :---|
| **Show legend** | 顯示或隱藏圖例。 |
| **Position** | 控制圖例相對於圖表的顯示位置。支援的值：**Left**、**Right**、**Top**、**Bottom**。 |

### 工具提示

切換 **Show tooltip** 選取器以啟用或停用工具提示。
