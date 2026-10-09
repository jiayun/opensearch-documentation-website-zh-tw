---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "應用程式分析"
nav_order: 30
---

# 應用程式分析

您可以使用應用程式分析來建立自訂的可觀測性應用程式，以檢視系統的可用性狀態，並將記錄事件與追蹤及指標資料合併為整體系統健康狀況的單一檢視。這讓您能夠快速在記錄檔、追蹤與指標之間切換，深入調查任何問題的來源。

## 開始使用應用程式分析

若要開始使用，請選取 OpenSearch Dashboards 介面左上角的 Menu 按鈕。接著選取 **Observability**，然後選擇 **Application analytics**。

### 建立應用程式

1. 選擇 **Create application**。
2. 輸入應用程式的名稱，並可選擇性地新增描述。
3. 至少執行下列其中一項操作：

    - 使用 [PPL]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) 指定基礎查詢。

      應用程式建立後，您無法變更基礎查詢。
      {: .note }

    - 從下拉式選單或服務地圖選取 **Services & entities**。
    - 從下拉式選單或表格選取 **Trace groups**。

4. 選擇 **Create**。

### 建立視覺化

1. 選擇 **Log Events** 索引標籤。
1. 使用 [PPL]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) 在基礎查詢的基礎上繼續建置。
1. 選擇 **Visualizations** 索引標籤以檢視您的視覺化。
1. 展開 **Save** 下拉式選單，輸入視覺化的名稱，然後選擇 **Save**。

若要檢視您的視覺化，請選擇 **Panel** 索引標籤。

### 設定可用性

可用性是應用程式的狀態，由在[時間序列指標]({{site.url}}{{site.baseurl}}/observing-your-data/app-analytics/#time-series-metric)上設定的可用性層級決定。

若要建立可用性層級，您必須設定下列項目：
- color：首頁上可用性徽章的顏色。
- name：首頁上可用性徽章中的文字。
- expression：用於判斷可用性的比較運算子。
- value：計算可用性時使用的值。

![設定可用性]({{site.url}}{{site.baseurl}}/images/app_availability_level.gif)

預設情況下，應用程式分析會顯示資料最近 24 小時的結果。若要檢視不同時間範圍的資料，請使用日期與時間選取器。

#### 時間序列指標

時間序列指標是指任何查詢跨越時間戳記且為折線圖的視覺化。接著您可以使用 PPL 在記錄檔上定義任意條件，以建立隨時間變化的視覺化。

##### 範例
```
source = <index_name> | ... | ... | stats ... by span(<timestamp_field>, 1h)
```

在視覺化組態中選擇 **Line** 以建立時間序列指標。

![將視覺化變更為折線圖]({{site.url}}{{site.baseurl}}/images/visualization-line-type.gif)
