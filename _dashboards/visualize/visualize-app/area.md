---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "區域圖"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 30
redirect_from:
  - /dashboards/visualize/area/
---

# 區域圖

區域圖是一種折線圖，折線下方的區域會以顏色填滿。您可以堆疊多個桶 (bucket)，以顯示變數累計絕對值的相對比例；也可以疊加多個桶或不同的變數，以便在 X 軸的桶或時間值內進行比較。

## 何時使用區域圖

使用區域圖可同時呈現趨勢模式與比例關係。區域圖能揭示貢獻模式，顯示哪些組成部分推動了整體總計，以及這些模式在何時發生變化。

## 建立區域圖

本頁的範例使用 **Sample flight data** 資料集，且各範例會依序延續前一個範例。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要建立顯示航班數量隨時間變化的區域圖，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **Area**，然後選取您的索引模式（例如 **opensearch_dashboards_sample_data_flights**）。
2. 在 **Metrics** 下，展開 **Y-axis Count**，並將 **Aggregation** 設定為 **Count**。

   `Count` 指標沒有 Field 選項，因為 `Count` 表示的是文件數量，而非欄位值。

3. 在 **Buckets** 下，選取 **Add** > **X-axis**。
4. 將 **Aggregation** 設定為 **Date Histogram**，並將 **Field** 設定為 **timestamp**。

   timestamp 欄位是範例航班資料中唯一可用的日期時間欄位。
   {: .note}

5. 選取 **Update**。

   圖表會依自動決定的桶大小（例如一天）產生文件數量的鋸齒狀時間序列圖。

6. 拖曳選取圖表中包含資料的部分。請在資料兩側保留一些邊界，以免截斷任何資料。

   資料會擴展以填滿圖表的整個寬度。由於空間變大，自動計算的桶大小會縮小為 12 小時。

7. 在 **Buckets** 下，選取 **Add** > **Split series**。
8. 將 **Sub aggregation** 設定為 **Terms**，並將 **Field** 設定為 **Cancelled**。
9. 選取 **Update**。

   圖表會在時間軸上疊加顯示已取消與未取消航班的數量，如下圖所示。

   ![疊加航班取消狀態的區域圖]({{site.url}}{{site.baseurl}}/images/dashboards/example-area-normal-count.png)

   請注意下列事項：
   - 已取消（`Cancelled = true`）與未取消航班的數量會疊加顯示在圖表上。已取消的航班數量平均約為未取消航班的 10%。
   - 航班數量隨時間呈週期性變化，每週會有一天下降。

### 堆疊區域圖

根據預設，分割序列會以疊加方式顯示（Normal 模式）。若要將各區域彼此堆疊以顯示總量：

1. 選取 **Metrics & axes** 索引標籤。
2. 在 **Metrics** 下，展開 **Count** 序列。
3. 將 **Mode** 從 **Normal** 變更為 **Stacked**。
4. 選取 **Update**。

現在各區域已堆疊，可同時顯示個別類別的數量與合計總量，如下圖所示。

![顯示航班取消狀態的堆疊區域圖]({{site.url}}{{site.baseurl}}/images/dashboards/example-area-stacked-count.png)

### 多個指標

新增第二個 Y 軸指標，以便在同一張圖表上比較不同的測量值：

1. 在 **Metrics** 下，選取 **Add**。
2. 將 **Aggregation** 設定為 **Average**，並將 **Field** 設定為 **AvgTicketPrice**。
3. 選取 **Update**。

圖表現在會將平均票價疊加在數量之上。若要讓第二個指標使用自己的刻度，請前往 **Metrics & axes** 索引標籤，展開新的指標，並將其指派給新的數值軸。

## 設定區域圖

區域圖編輯器有三個組態索引標籤。

### Data 索引標籤

**Data** 索引標籤定義要顯示的資料。

#### Metrics

指標定義 Y 軸的值。每個指標會針對每個桶中的文件計算一個彙總。

| 設定 | 說明 |
| :--- | :--- |
| **Aggregation** | 彙總函式。支援的值：**Count**、**Average**、**Sum**、**Min**、**Max**、**Unique Count**、**Median**、**Percentiles**、**Percentile Ranks**、**Top Hit**、**Standard Deviation**。 |
| **Field** | 要彙總的數值欄位（**Count** 不需要此項）。 |

選取 **Add** 可在同一張圖表上繪製多個指標。

#### Buckets

桶定義資料的分組方式。

| 桶類型 | 說明 |
| :--- | :--- |
| **X-axis** | 沿水平軸將資料分組。通常對時間型資料使用 **Date Histogram**，對數值範圍使用 **Histogram**。 |
| **Split series** | 依欄位的值將資料分割為多個堆疊（或疊加）的區域。使用 **Terms**、**Filters** 或其他桶彙總。 |
| **Split chart** | 為每個桶值建立個別的圖表面板（小型多圖）。可依列或欄分割。 |

### Metrics & axes 索引標籤

**Metrics & axes** 索引標籤控制每個指標的呈現方式，以及座標軸的設定方式。

#### 序列設定

每個指標序列都有下列選項。

| 設定 | 說明 |
| :--- | :--- |
| **Value axis** | 此序列所對應繪製的 Y 軸。選取 **New axis** 可建立次要 Y 軸。 |
| **Chart type** | 覆寫此序列的圖表類型。支援的值：**Line**、**Area**、**Bar**。 |
| **Mode** | 控制堆疊行為。**Stacked** 會將區域彼此層疊。**Normal** 會讓區域重疊。 |
| **Line mode** | 控制線條內插方式。**Straight** 繪製直線線段。**Smoothed** 套用曲線。**Stepped** 建立階梯狀圖樣。 |

#### Y 軸

每個 Y 軸都有下列選項。

| 設定 | 說明 |
| :--- | :--- |
| **Position** | 座標軸顯示的位置。支援的值：**Left**、**Right**。 |
| **Mode** | 控制 Y 軸的刻度模式。**Normal** 顯示原始值。**Percentage** 將堆疊區域正規化為 100%。**Wiggle** 與 **Silhouette** 是串流圖的版面配置變體。 |
| **Scale type** | 決定刻度。支援的值：**Linear**、**Log**、**Square root**。 |
| **Show** | 顯示或隱藏座標軸線與標籤。 |
| **Labels** | 控制標籤旋轉方式。支援的值：**Horizontal**、**Vertical**、**Angled**。 |

#### X 軸

| 設定 | 說明 |
| :--- | :--- |
| **Position** | 座標軸顯示的位置。支援的值：**Top**、**Bottom**。 |
| **Show** | 顯示或隱藏座標軸線與標籤。 |
| **Filter labels** | 啟用後，重疊的標籤會自動隱藏。 |
| **Align** | 控制標籤旋轉方式。支援的值：**Horizontal**、**Vertical**、**Angled**。 |
| **Truncate** | 設定標籤在截斷前的最大像素寬度。 |

### Panel settings 索引標籤

**Panel settings** 索引標籤控制圖表的整體外觀。

#### 設定

| 設定 | 說明 |
| :--- | :--- |
| **Legend position** | 圖例顯示的位置。支援的值：**Top**、**Left**、**Right**、**Bottom**。 |
| **Show tooltip** | 啟用後，滑鼠游標停留時會顯示數值。 |
| **Order buckets by sum** | 啟用後，分割序列會依其總值排序，而非依字母順序排序。 |

#### 格線

| 設定 | 說明 |
| :--- | :--- |
| **Show X-axis lines** | 啟用後，會在每個 X 軸刻度處顯示垂直格線。 |
| **Y-axis lines** | 選取 Y 軸以顯示水平格線，或選取 **Don't show** 將其隱藏。 |

#### 閾值線

| 設定 | 說明 |
| :--- | :--- |
| **Show threshold line** | 啟用後，會在指定值處繪製一條水平參考線。 |
| **Threshold value** | 繪製線條所在的 Y 軸值。 |
| **Line width** | 閾值線的粗細（以像素為單位）。 |
| **Line style** | 線條樣式。支援的值：**Full**（實線）、**Dashed**、**Dot-dashed**。 |
| **Line color** | 閾值線的顏色。 |

## 後續步驟

- 若要選擇其他視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
