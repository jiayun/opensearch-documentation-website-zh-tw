---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "狀態時間軸"
parent: Visualization types
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 60
---

# 視覺化編輯器中的狀態時間軸

狀態時間軸會顯示一系列水平長條，用以呈現狀態隨時間的變化。每個長條稱為狀態區域，代表一個特定狀態，其長度表示該狀態持續的時間。

## 建立狀態時間軸

以下範例會逐步延伸，從基本的時間軸開始，再逐漸增加複雜度。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/#prerequisites)。

### 單一類別狀態時間軸

首先使用一個會傳回時間欄位與狀態欄位的查詢：

```sql
source = opensearch_dashboards_sample_data_logs | fields timestamp, response
```
{% include copy.html %}

執行此查詢後，選取 **State Timeline** 作為圖表類型。欄位的對應方式如下：

- **X-Axis** 顯示 `timestamp` 欄位。
- **Color** 顯示 `response` 欄位。

結果會是一列彩色區段，每個區段代表記錄到特定回應狀態碼的一段時間，如下圖所示。

![顯示請求隨時間變化的基本狀態時間軸]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/state-timeline/state-timeline-single-cate-field.png){: width="100%" }

### 套用值對應

使用值對應，為特定狀態值指派自訂標籤與色彩。例如，若要將 HTTP 回應碼分類為有意義的群組：

1. 在 **Value mappings** 區段中，選取 **Edit value mappings**。
1. 選取 **Add new mapping**，並選取 **Value** 作為對應類型。
1. 在 **Value** 欄位中輸入 `200`。在 **Display text** 欄位中輸入 `Successful`。選取綠色。
1. 對 `404` 重複上述步驟，使用標籤 `Error` 與橘色。
1. 對 `503` 重複上述步驟，使用標籤 `Error` 與紅色，如下圖所示，然後選取 **Save**。

或者，選取 **Range** 作為對應類型，將連續值分組為區間。例如，將 [400, 600) 範圍內的所有狀態碼對應為以紅色顯示「Error」。

![值對應選項]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/state-timeline/value-mapping-for-reponse.png){: width="400" }

時間軸現在會為每個資料值顯示使用者設定的標籤，並使用一致的色彩——成功的回應為綠色，錯誤為紅色，如下圖所示。

![已套用值對應的狀態時間軸]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/state-timeline/state-timeline-value-mapping.png){: width="100%" }

### 處理資料缺口

在狀態時間軸中，每個資料點的 `timestamp` 作為狀態區域的開始時間，而下一個資料點的 `timestamp` 則標示其結束時間。當資料有缺口（時間戳記之間缺少資料點）時，請使用 **Disconnect values** 或 **Connect null values** 設定來控制這些缺口的視覺化呈現方式。

**Disconnect values** 與 **Connect null values** 一次只能套用其中一項。
{: .note}

以下範例顯示設定 **Disconnect values** 閾值的效果：

![具有中斷閾值設定的狀態時間軸]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/state-timeline/disconnect-threshold.gif){: width="100%" }

### 多類別狀態時間軸

新增一個類別分組欄位，以顯示多列狀態時間軸：

```sql
source = opensearch_dashboards_sample_data_logs | fields timestamp, request, response
```
{% include copy.html %}

執行此查詢後，選取 **State Timeline** 作為圖表類型。欄位的對應方式如下：

- **X-Axis** 顯示 `timestamp` 欄位。
- **Y-Axis** 顯示 `request` 欄位。
- **Color** 欄位顯示 `response` 欄位。

結果會顯示每個請求路徑隨時間變化的回應狀態，讓您輕鬆找出哪些端點經常不穩定，如下圖所示。

![依請求分組的狀態時間軸]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/state-timeline/state-timeline-grouped.png){: width="100%" }

## 設定狀態時間軸

您可以在組態面板中設定下列設定。

### 欄位

在 **Fields** 區段中，設定每個軸上顯示的欄位。

| 欄位 | 說明 |
| --- | --- |
| **X-Axis** | 為水平軸選取日期欄位。每個資料點的時間戳記作為狀態區域的開始時間。 |
| **Y-Axis** | 選取類別欄位，將狀態時間軸分組為不同的列。每個唯一值會各自呈現為一列。單一類別時間軸可選用。 |
| **Color** | 選取類別或數值欄位，以定義每個時間點的狀態。類別欄位代表離散狀態（例如 `running`、`stopped` 或 `degraded`）。當每個值對應一個不同的狀態時（例如 HTTP 狀態碼 200、404、503），數值欄位也可以代表狀態。對於連續的數值，請使用[值對應](#value-mappings)將範圍定義為具名狀態。 |

### 分割

在 **Split by** 下拉式清單中，選取一個欄位，依值將圖表分割為不同的元素。如需更多資訊，請參閱[分割]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#split)。

### 值對應

值對應會以自訂標籤與色彩取代原始資料值。可用的對應類型如下。

**值對應**：將特定值（數值或類別）對應至自訂的顯示文字與色彩。例如，將 HTTP 狀態碼 `200` 對應為以綠色顯示「Success」，並將 `503` 對應為以紅色顯示「Error」。

**範圍對應**：將數值範圍對應至自訂的顯示文字與色彩。例如，將範圍 [0, 300) 對應為顯示「Low」，並將 [300, 800) 對應為顯示「Medium」。

每個對應項目都有下列選項。

| 設定 | 說明 |
| --- | --- |
| **Value/Range** | 要比對的目標值或數值範圍。若為值對應，請輸入特定值。若為範圍對應，請定義開始值與結束值（包含開始值，不包含結束值）。 |
| **Display text** | 用來取代原始值顯示的標籤。若保留空白，則會顯示原始值。 |
| **Color** | 對應值的自訂色彩。若未定義，則會自動指派色彩。 |

如需完整範例，請參閱[套用值對應](#applying-value-mappings)。

### 閾值

如需設定閾值的相關資訊，請參閱[閾值]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/thresholds/)。

### 軸

X 軸與 Y 軸共用相同的組態選項。如需更多資訊，請參閱[軸]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/#axes)。

### 狀態時間軸

使用下列設定來自訂狀態時間軸的外觀與行為。

| 設定 | 說明 |
| --- | --- |
| **Use threshold color** | 啟用時，狀態區域的色彩由閾值範圍決定，而非預設色彩或對應的色彩。 |
| **Show display text** | 啟用且已設定含有顯示文字的值對應時，對應的文字會顯示在每個狀態區域內。停用時，不會顯示任何文字。 |
| **Row height** | 控制每個狀態長條的高度。值為 0 時產生最小的長條寬度，值為 1 時產生最大的長條寬度。 |
| **Disconnect values** | 控制當缺口超過指定持續時間時，狀態區域是否在視覺上中斷。**Never** 會讓所有區域保持連接。**Threshold** 會在資料點之間的缺口超過所設定的閾值時中斷區域。 |
| **Threshold (disconnect)** | 設定中斷值的持續時間閾值。如果連續資料點之間的缺口超過此閾值，長條會呈現為各自分開的中斷區域。請以持續時間指定（例如 `1h` 或 `30m`）。 |
| **Connect null values** | 控制 null 值（資料中的缺口）在圖表上的呈現方式。**Never** 會讓缺口保持可見。**Threshold** 只會在缺口落在所設定的閾值內時連接缺口。 |
| **Threshold (connect)** | 設定連接 null 值的持續時間閾值。如果資料點之間的缺口落在此閾值內，這些資料點會被連接起來，填補缺口。請以持續時間指定（例如 `1h` 或 `30m`）。 |

### 圖例

圖例會彙總圖表中使用的視覺色彩編碼。

| 設定 | 說明 |
| --- | --- |
| **Show legend** | 顯示或隱藏圖例。 |
| **Position** | 控制圖例相對於圖表的顯示位置。支援的值：**Left**、**Right**、**Top**、**Bottom**。 |

### 工具提示

切換 **Show tooltip** 選取器，以啟用或停用工具提示。
