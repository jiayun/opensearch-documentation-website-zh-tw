---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "時間軸視覺化"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 160
redirect_from:
  - /dashboards/visualize/timeline/
---

# 時間軸視覺化

**Timeline** 是 OpenSearch Dashboards 中以運算式為基礎的資料視覺化工具，可讓您使用簡單的運算式語言建立時間序列視覺化。其他視覺化類型使用圖形介面，**Timeline** 則使用文字型運算式語法來定義資料來源、轉換與顯示選項。透過此語法，您可以比較多個時間序列、套用數學函式，並疊加不同時段的資料。

## 何時使用時間軸視覺化

**Timeline** 專用於以時間為基礎的資料分析，特別適合透過其運算式語法呈現時間模式與事件順序。

**Timeline** 是舊版視覺化工具。若要建立新的時間型視覺化，請考慮使用 [TSVB]({{site.url}}{{site.baseurl}}/dashboards/visualize/tsvb/) 或 [Vega]({{site.url}}{{site.baseurl}}/dashboards/visualize/vega/)。
{: .note}

當您需要以運算式控制視覺化時，最適合使用 **Timeline**，例如使用位移比較不同時段的資料、對序列套用數學轉換，或在單一圖表上結合多個資料來源。
{: .tip}

## 先決條件

建立時間軸視覺化之前，請確認您已具備下列項目：

- 一個正在執行且可存取的 OpenSearch Dashboards 執行個體。
- 已載入範例資料，或有可用的時間序列索引。本文件中的範例使用電子商務範例資料集。若要了解如何新增範例資料集，請參閱[新增範例資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

## 建立時間軸視覺化

若要建立時間軸視覺化，請依照下列步驟操作：

1. 從頂端選單中，選取 **OpenSearch Dashboards > Visualize**。
1. 選取 **Create visualization**。
1. 選取 **Timeline**。

時間軸編輯器由下列元件組成：

- **Chart area**：顯示轉譯後的視覺化。
- **Interval**：設定資料彙總的時間桶 (bucket) 大小（例如 `1d`、`1h` 或 `auto`）。
- **Timeline expression**：文字編輯器，您可以在其中撰寫時間軸運算式，以定義視覺化的資料與外觀。
- **Update 與 Discard 按鈕**：套用或還原對運算式所做的變更。

下圖顯示時間軸編輯器，其中包含一個查詢電子商務資料的基本運算式。

![時間軸編輯器，顯示一個基本 OpenSearch 運算式，呈現隨時間變化的訂單數量]({{site.url}}{{site.baseurl}}/images/dashboards/timeline-basic-expression.png){: width="700" }

## 時間軸運算式語法

時間軸運算式由一個或多個以逗號分隔的函式鏈組成。每個函式鏈以資料來源函式開頭，後面接著使用點標記法串連的其他函式。多個函式鏈以逗號分隔，並會在同一張圖表上產生多個序列。

基本語法如下：

```js
.function1(arg1=value1, arg2=value2).function2(arg1=value1)
```
{% include copy.html %}

若要在同一張圖表上顯示多個序列，請以逗號分隔各運算式：

```js
.opensearch(index=my-index).label("Series 1"), .opensearch(index=my-index, metric=avg:price).label("Series 2")
```
{% include copy.html %}

## 資料來源函式

`.opensearch()` 函式是時間軸運算式的主要資料來源。它會從 OpenSearch 索引擷取時間序列資料。

<!-- vale off -->
### .opensearch() 參數
<!-- vale on -->

下表列出 `.opensearch()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `q` | 字串 | 使用 Apache Lucene [查詢字串]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)語法的查詢。預設為 `*`（符合全部）。 |
| `metric` | 字串 | OpenSearch 指標彙總：`avg`、`sum`、`min`、`max`、`percentiles` 或 `cardinality`，後面接著欄位名稱。例如 `sum:bytes` 或 `percentiles:bytes:95,99,99.9`。預設為 `count`。 |
| `split` | 字串 | 用於分割序列的欄位及數量上限。例如，`hostname:10` 會擷取前 10 個主機名稱。 |
| `index` | 字串 | 要查詢的索引。可使用萬用字元。若要使用指令碼欄位與欄位名稱建議，請提供索引模式名稱。 |
| `timefield` | 字串 | 用於 X 軸、類型為 `date` 的欄位。 |
| `offset` | 字串 | 依日期運算式位移序列擷取，例如使用 `-1M`，讓一個月前的事件看起來像是現在發生。使用 `timerange:-2` 可往過去位移整體圖表時間範圍的兩倍。 |
| `opensearchDashboards` | 布林值 | 設為 `true` 時，會套用 OpenSearch Dashboards 儀表板上的篩選條件。僅在儀表板上使用時有效。 |
| `data_source_name` | 字串 | 要查詢的資料來源。僅在啟用多個資料來源時有效。 |
| `fit` | 字串 | 用於將序列調整至目標時間範圍與間隔的演算法。可為 `average`、`carry`、`nearest`、`none` 或 `scale` 其中之一。 |

### 基本查詢範例

下列運算式會擷取電子商務範例資料索引中隨時間變化的文件數量：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date)
```
{% include copy.html %}

### 指標彙總範例

下列運算式會計算 `taxful_total_price` 欄位的平均值：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date, metric=avg:taxful_total_price)
```
{% include copy.html %}

### 查詢篩選範例

下列運算式使用 `q` 參數，以 Lucene 查詢語法篩選資料：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date, q="customer_gender:MALE").label("Male Orders"),
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date, q="customer_gender:FEMALE").label("Female Orders")
```
{% include copy.html %}

### 分割範例

下列運算式會依 `customer_gender` 欄位分割資料，並傳回前 2 個值：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date, split=customer_gender:2)
```
{% include copy.html %}

### 位移範例

下列運算式會將目前的時間範圍與一週前的資料疊加，以進行比較：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).label("This Week"),
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date, offset=-1w).label("Previous Week")
```
{% include copy.html %}

下圖顯示使用位移比較本週與前一週的結果。

![使用位移比較目前時段與前一週的時間軸視覺化]({{site.url}}{{site.baseurl}}/images/dashboards/timeline-offset.png){: width="700" }

## 顯示函式

顯示函式控制用於轉譯序列的圖表類型（線條、長條或點）。

<!-- vale off -->
### .lines()
<!-- vale on -->

將序列轉譯為線條。下表列出 `.lines()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `width` | 數字 | 線條粗細，以像素為單位。 |
| `fill` | 數字 | 介於 0 到 10 之間的數字，用於控制填滿不透明度。可用於建立面積圖。 |
| `stack` | 布林值 | 設為 `true` 時，會堆疊線條。 |
| `show` | 布林值 | 顯示或隱藏線條。 |
| `steps` | 布林值 | 設為 `true` 時，會將線條轉譯為階梯狀，而不在各點之間進行內插。 |

#### 範例

下列表達式會繪製具有自訂寬度與填滿效果的折線圖：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).lines(width=2, fill=1)
```
{% include copy.html %}

<!-- vale off -->
### .bars()
<!-- vale on -->

將數列繪製為長條。下表列出 `.bars()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `width` | 數字 | 長條寬度，以像素為單位。 |
| `stack` | 布林值 | 設為 `true` 時，會堆疊長條。預設為 `true`。 |

#### 範例

下列表達式會繪製總營收的長條圖：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date, metric=sum:taxful_total_price).bars(width=2)
```
{% include copy.html %}

<!-- vale off -->
### .points()
<!-- vale on -->

將數列繪製為資料點。下表列出 `.points()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `radius` | 數字 | 資料點的大小。 |
| `weight` | 數字 | 資料點周圍線條的粗細。 |
| `fill` | 數字 | 介於 0 到 10 之間的數字，表示填滿的不透明度。 |
| `fillColor` | 字串 | 用來填滿資料點的色彩。 |
| `symbol` | 字串 | 資料點的符號。可為 `triangle`、`cross`、`square`、`diamond` 或 `circle`。 |
| `show` | 布林值 | 顯示或隱藏資料點。 |

#### 範例

下列表達式會將資料繪製為十字形資料點：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date, metric=max:taxful_total_price).points(symbol=cross, radius=3)
```
{% include copy.html %}

## 樣式函式

樣式函式可控制數列的標籤、色彩與圖例，而不變更圖表類型。

<!-- vale off -->
### .label()
<!-- vale on -->

變更圖例中顯示的數列標籤。使用 `$1`、`$2` 等來參照正規表示式的擷取群組。下表列出 `.label()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `label` | 字串 | 數列的圖例值。使用 `$1`、`$2` 等來參照正規表示式的擷取群組。 |
| `regex` | 字串 | 支援擷取群組的正規表示式。 |

#### 範例

下列表達式會為數列設定自訂標籤：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).label("Daily Order Count")
```
{% include copy.html %}

<!-- vale off -->
### .color()
<!-- vale on -->

變更數列的色彩。接受十六進位色彩值。若要在多個數列之間建立漸層，請指定多個色彩，並以冒號分隔。

#### 範例

下列表達式會將數列色彩設為藍色：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).color(#1E88E5)
```
{% include copy.html %}

<!-- vale off -->
### .legend()
<!-- vale on -->

設定圖例的位置與樣式。下表列出 `.legend()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `position` | 字串或布林值 | 放置圖例的角落：`nw`、`ne`、`se` 或 `sw`。設為 `false` 可停用圖例。 |
| `columns` | 數字 | 將圖例分成的欄數。 |
| `showTime` | 布林值 | 設為 `true` 時，將滑鼠游標停留在圖形上會在圖例中顯示時間值。預設為 `true`。 |
| `timeFormat` | 字串 | moment.js 格式模式。預設為 `MMMM Do YYYY, HH:mm:ss.SSS`。 |

<!-- vale off -->
### .title()
<!-- vale on -->

在繪圖頂端新增標題。若對多個數列呼叫此函式，則使用最後一次呼叫的結果。下表列出 `.title()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `title` | 字串 | 繪圖的標題。 |

<!-- vale off -->
### .hide()
<!-- vale on -->

預設隱藏數列。數列仍會出現在圖例中，且可切換為顯示。下表列出 `.hide()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `hide` | 布林值 | 設為 `true` 時，會隱藏數列。預設為 `true`。 |

## Y 軸組態

您可以設定一或多個 y 軸，以控制刻度、位置與格式。

<!-- vale off -->
### .yaxis()
<!-- vale on -->

設定 y 軸選項。使用 `.yaxis(2)` 可將數列繪製在次要 y 軸上。下表列出 `.yaxis()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `yaxis` | 數字 | 用來繪製此數列的 y 軸編號。例如，`2` 代表次要 y 軸。 |
| `min` | 數字 | 最小值。 |
| `max` | 數字 | 最大值。 |
| `position` | 字串 | 軸的位置：`left` 或 `right`。 |
| `label` | 字串 | 軸的標籤。 |
| `color` | 字串 | 軸標籤的色彩。 |
| `units` | 字串 | y 軸標籤的格式。可為 `bits`、`bits/s`、`bytes`、`bytes/s`、`currency(:ISO 4217 code)`、`percent` 或 `custom(:prefix:suffix)`。 |
| `tickDecimals` | 數字 | y 軸刻度標籤的小數位數。 |

#### 範例

下列表達式會在左側 y 軸上以長條顯示營收，並在右側 y 軸上以折線顯示訂單數：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date, metric=sum:taxful_total_price).label("Total Revenue").bars(width=2),
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).label("Order Count").lines(fill=1, width=1).yaxis(2)
```
{% include copy.html %}

下圖顯示雙 y 軸視覺化，其中營收以長條呈現，訂單數以折線呈現。

![使用雙 y 軸的時間軸視覺化，以長條顯示總營收，並以折線顯示訂單數]({{site.url}}{{site.baseurl}}/images/dashboards/timeline-multi-series.png){: width="700" }

## 資料轉換函式

資料轉換函式可修改、平滑化或分析數列資料。

<!-- vale off -->
### .movingaverage()
<!-- vale on -->

計算指定視窗內的移動平均值。使用此函式可平滑化含有雜訊的數列。別名：`.mvavg()`。下表列出 `.movingaverage()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `window` | 數字或字串 | 用來計算平均值的資料點數量，或日期數學表達式（例如 `1d` 或 `1M`）。 |
| `position` | 字串 | 取平均值的資料點相對於結果時間的位置。可為 `left`、`right` 或 `center`。 |

#### 範例

下列表達式會在每日營收上疊加 7 天移動平均值：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date, metric=sum:taxful_total_price).label("Daily Revenue"),
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date, metric=sum:taxful_total_price).movingaverage(window=7).label("7-Day Moving Average").color(#F04E37).lines(width=3)
```
{% include copy.html %}

下圖顯示每日營收，並疊加 7 天移動平均值。

![顯示每日營收並疊加 7 天移動平均值的時間軸視覺化]({{site.url}}{{site.baseurl}}/images/dashboards/timeline-moving-average.png){: width="700" }

<!-- vale off -->
### .movingstd()
<!-- vale on -->

計算指定視窗內的移動標準差。別名：`.mvstd()`。下表列出 `.movingstd()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `window` | 數字 | 用來計算標準差的資料點數量。 |
| `position` | 字串 | 視窗切片相對於結果時間的位置。可為 `left`、`right` 或 `center` 其中之一。預設為 `left`。 |

#### 範例

下列運算式會計算 5 點移動標準差：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).movingstd(window=5).label("5-Point Std Dev")
```
{% include copy.html %}

<!-- vale off -->
### .derivative()
<!-- vale on -->

繪製數值隨時間的變化。

#### 範例

下列運算式會繪製訂單數量隨時間的變化：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).derivative().label("Change in Order Count")
```
{% include copy.html %}

<!-- vale off -->
### .trend()
<!-- vale on -->

使用指定的迴歸演算法繪製趨勢線。下表列出 `.trend()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `mode` | 字串 | 要使用的演算法。可為 `linear` 或 `log` 其中之一。 |
| `start` | 數字 | 開始計算的位置。負值表示從結尾起算。預設為 `0`。 |
| `end` | 數字 | 停止計算的位置。負值表示從結尾起算。預設為 `0`。 |

#### 範例

下列運算式會在訂單數量上疊加一條線性趨勢線：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).label("Order Count"),
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).trend(mode=linear).label("Trend").color(#E53935)
```
{% include copy.html %}

<!-- vale off -->
### .cusum()
<!-- vale on -->

從基準值開始，傳回序列的累計總和。下表列出 `.cusum()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `base` | 數字 | 起始的數值。此值會加到序列的開頭。 |

<!-- vale off -->
### .fit()
<!-- vale on -->

使用定義的擬合函式填補 null 值。下表列出 `.fit()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `mode` | 字串 | 要使用的演算法。可為 `average`、`carry`、`nearest`、`none` 或 `scale` 其中之一。 |

<!-- vale off -->
### .trim()
<!-- vale on -->

將序列開頭或結尾的 N 個桶 (bucket) 設為 null。使用此函式可處理不完整桶的問題。下表列出 `.trim()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `start` | 數字 | 要從開頭修剪的桶數量。預設為 `1`。 |
| `end` | 數字 | 要從結尾修剪的桶數量。預設為 `1`。 |

## 數學函式

Timeline 支援下列數學函式，用於合併或轉換序列。數學函式接受數字或另一個序列作為引數。

| 函式 | 說明 |
| :--- | :--- |
| `.add()`（別名：`.plus()`、`.sum()`） | 將一或多個序列的值加到輸入序列的每個位置。 |
| `.subtract()` | 從輸入序列的每個位置減去一或多個序列的值。 |
| `.multiply()` | 在輸入序列的每個位置乘以一或多個序列的值。 |
| `.divide()` | 在輸入序列的每個位置除以一或多個序列的值。 |
| `.abs()` | 傳回序列中每個值的絕對值。 |
| `.log()` | 傳回每個值的對數（預設底數：10）。 |
| `.min()` | 在每個位置傳回目前序列與所提供的序列或數字之間的最小值。 |
| `.max()` | 在每個位置傳回目前序列與所提供的序列或數字之間的最大值。 |
| `.precision()` | 將數值的小數部分截斷至指定的位數。 |
| `.scale_interval()` | 將數值（通常為總和或計數）換算為新的間隔，例如每秒速率。 |
| `.range()` | 變更序列的最大值與最小值，同時保持相同的形狀。 |

#### 範例

下列運算式會將總營收除以訂單數量，以計算每筆訂單的營收：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date, metric=sum:taxful_total_price).divide(value=.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date)).label("Revenue per Order")
```
{% include copy.html %}

## 條件函式

使用條件函式，根據比較邏輯設定數值。

<!-- vale off -->
### .condition()
<!-- vale on -->

使用運算子將每個資料點與某個數字或另一個序列中的相同資料點進行比較，若條件成立，則將其值設為結果。若省略 `else`，不符合條件的資料點會保留原始值。別名：`.if()`。下表列出 `.condition()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `operator` | 字串 | 比較運算子：`eq`、`ne`、`lt`、`lte`、`gt` 或 `gte`。 |
| `if` | 數字或 SeriesList | 每個資料點要比較的值。 |
| `then` | 數字或 SeriesList | 比較結果為 true 時要設定的值。 |
| `else` | 數字或 SeriesList | 比較結果為 false 時要設定的值。 |

#### 範例

下列運算式會將數值上限設為 150，並將較低的值設為 0：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).condition(operator=gte, if=150, then=150, else=0).label("Days Meeting Target")
```
{% include copy.html %}

## 靜態值

使用靜態值在圖表上繪製參考線，例如目標或閾值。

<!-- vale off -->
### .static()
<!-- vale on -->

將單一值繪製為橫跨圖表的水平線。別名：`.value()`。下表列出 `.static()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `value` | 數字或字串 | 要顯示的單一值。您可以傳入多個值，讓這些值在時間範圍內平均內插。 |
| `label` | 字串 | 序列的標籤。 |
| `offset` | 字串 | 依日期運算式位移序列的擷取時間。 |
| `fit` | 字串 | 用於擬合的演算法。可為 `average`、`carry`、`nearest`、`none` 或 `scale` 其中之一。 |

#### 範例

下列運算式會在 150 筆訂單處加入一條目標線：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).label("Order Count").lines(fill=2, width=1),
.static(value=150, label="Target").color(#E53935).lines(width=2)
```
{% include copy.html %}

下圖顯示訂單數量，以及位於 150 筆訂單處的靜態目標線。

![在 150 筆訂單處具有靜態目標線的 Timeline 視覺化]({{site.url}}{{site.baseurl}}/images/dashboards/timeline-static-line.png){: width="700" }

## 彙總函式

使用彙總函式將序列縮減為單一值，並以水平線顯示。

<!-- vale off -->
### .aggregate()
<!-- vale on -->

根據處理序列中所有資料點的結果建立靜態線條。下表列出 `.aggregate()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `function` | 字串 | `avg`、`cardinality`、`min`、`max`、`last`、`first` 或 `sum` 其中之一。 |

#### 範例

下列表達式顯示訂單數量，並以水平線顯示其平均值：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).label("Order Count"),
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).aggregate(function=avg).label("Average").color(#E53935)
```
{% include copy.html %}

## 預測函式

使用預測函式，根據序列中的歷史模式預測未來值。

<!-- vale off -->
### .holt()
<!-- vale on -->

對序列的起始部分取樣，並使用 Holt-Winters 三重指數平滑法，根據取樣資料預測未來值。使用此函式進行異常偵測。空值會以預測值填入。下表列出 `.holt()` 函式的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `alpha` | 數值 | 介於 0 到 1 的平滑權重。值越高，序列越貼近原始序列。 |
| `beta` | 數值 | 介於 0 到 1 的趨勢權重。值越高，上升或下降的線條會持續越久。 |
| `gamma` | 數值 | 介於 0 到 1 的季節性權重。值越高，近期季節性週期的重要性越高。 |
| `season` | 字串 | 季節性週期長度，例如，以 `1w` 表示每週模式。僅在搭配 `gamma` 時有用。 |
| `sample` | 數值 | 預測前要取樣的季節性週期數量。僅在搭配 `gamma` 時有用。預設為全部。 |

#### 範例

下列表達式使用 Holt-Winters 平滑法預測訂單數量：

```js
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).label("Actual"),
.opensearch(index=opensearch_dashboards_sample_data_ecommerce, timefield=order_date).holt(alpha=0.5, beta=0.5).label("Forecast").color(#E53935)
```
{% include copy.html %}

## 後續步驟

- 若要選擇不同的視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
