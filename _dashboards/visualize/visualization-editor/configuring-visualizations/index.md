---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定視覺化"
parent: Creating visualizations using queries
grand_parent: Building data visualizations
nav_order: 90
has_children: true
has_toc: false
redirect_from:
  - /dashboards/visualize/visualization-editor/configuring-visualizations/
---

# 在視覺化編輯器中設定視覺化

視覺化編輯器提供適用於多種視覺化類型的共用組態選項。各視覺化類型的頁面會說明其專屬選項。以下組態是大多數視覺化共通的選項。

## 欄位

**Fields** 面板會將查詢結果的欄對應到圖表座標軸。請選取要用於 X 軸、Y 軸以及選用維度（例如顏色或大小）的欄位。可用的欄位對應取決於圖表類型。

## 分割

當您的資料維度多於單一圖表所能顯示的維度時，請使用 **Split** 選項。例如，如果您的查詢傳回三個維度，但折線圖只能顯示兩個維度（X 軸和 Y 軸），請使用 Split 沿著第三個維度分割資料，以建立多個圖表。產生的每個圖表都顯示相同的座標軸，但會依分割欄位的不同值進行篩選。

若要建立分割視覺化，請依照下列步驟操作：

1. 在儀表板中，選取 **Create new** > **Add visualization**。
1. 選取 `opensearch_dashboards_sample_data_logs` 作為資料集。
1. 在查詢編輯器中，輸入下列查詢並選取 **Update**：

   ```sql
   | stats count() by span(`@timestamp`, 1h), extension, `machine.os`
   ```
   {% include copy.html %}

1. 在時間篩選器中，選取 **Last 15 days**。
1. 將 **Visualization type** 設為 **Line**。
1. 在 **Fields** 中，設定下列設定：
   - **X-Axis**：選取 `span(@timestamp,1h)`。
   - **Y-Axis**：選取 `count()`。
1. 在 **Split** 中，設定下列設定：
   - **Split by**：選取 `machine.os`。
   - 將 **Show labels** 切換為開啟。

此視覺化會針對每個 `machine.os` 值（例如 `win xp`、`osx`、`win 7`、`win 8`、`ios`）分別顯示一個折線圖，每個圖表都顯示事件數量隨時間的變化，如下圖所示。

![針對每個 machine.os 值分別顯示折線圖的分割視覺化]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/split-example.png)

## 座標軸

X 軸和 Y 軸共用相同的組態選項。每個座標軸都可以個別自訂。

| 設定 | 說明 |
| --- | --- |
| **Show axis** | 顯示或隱藏座標軸。 |
| **Title** | 座標軸的自訂標籤。 |
| **Position** | 控制座標軸相對於圖表的位置。支援的值：X 軸：**Top**、**Bottom**。Y 軸：**Left**、**Right**。 |
| **Show grid lines** | 啟用時，會顯示從座標軸延伸至圖表區域的格線。 |
| **Show labels** | 啟用時，會沿著座標軸顯示類別標籤。 |
| **Alignment** | 控制座標軸標籤的旋轉角度：**Horizontal**（0°）、**Vertical**（90°）或 **Angled**（45°）。 |
| **Truncate after** | 設定座標軸標籤在截斷前的最大字元長度。 |

座標軸適用於區域圖、長條圖、熱度圖、直方圖、折線圖、散佈圖和狀態時間軸圖。

## 工具提示

**Tooltip** 面板控制當您將游標停留在資料點上時所顯示的資訊。選項包括顯示所有數列的值，或只顯示游標所在的數列。

工具提示適用於區域圖、長條圖、長條量表圖、熱度圖、直方圖、折線圖、圓餅圖、散佈圖和狀態時間軸圖。

## 圖例

**Legend** 面板控制圖表圖例的顯示方式與位置。選項包括顯示或隱藏圖例，以及選取其位置（上、下、左或右）。

圖例適用於熱度圖、圓餅圖、散佈圖和狀態時間軸圖。

## 標準選項

標準選項控制視覺化中數值的格式。如需詳細資訊，請參閱[標準選項]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/standard-options/)。

## 值選項

值選項控制單一值視覺化中值的計算與顯示方式。

| 設定 | 說明 |
| --- | --- |
| **Calculation** | 用於將數列縮減為單一值的函式（例如 Last、Mean、Max、Min）。如需詳細資訊，請參閱[值計算]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/value-calculations/)。 |
| **Show** | 控制要顯示計算值、值名稱，或兩者皆顯示。 |

值選項適用於長條量表圖、量表圖和指標圖。

## 臨界值

臨界值定義以顏色標示的界限，用於指出值何時跨越重要界限。如需詳細資訊，請參閱[臨界值]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/thresholds/)。

## 值計算

值計算決定如何將一系列的值縮減為單一數字以供顯示（例如 Last、Mean、Sum、Min、Max）。如需詳細資訊，請參閱[值計算]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/value-calculations/)。
