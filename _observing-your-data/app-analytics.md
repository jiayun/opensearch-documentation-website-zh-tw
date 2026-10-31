---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "應用程式分析"
parent: Classic observability apps
nav_order: 40
---

# 應用程式分析

您可以使用應用程式分析建立自訂的可觀測性應用程式，以檢視系統的可用性狀態，並將記錄事件與追蹤及指標資料合併至單一整體系統健康狀態檢視中。這讓您可以在記錄、追蹤與指標之間快速切換，深入探究問題的根源。

應用程式分析是一種[傳統可觀測性應用程式]({{site.url}}{{site.baseurl}}/observing-your-data/classic-observability-apps/)。啟用多個資料來源時無法使用。若要在 Observability 工作區中監控應用程式，請參閱[應用程式效能監控]({{site.url}}{{site.baseurl}}/observing-your-data/apm/)。

## 開始使用應用程式分析

若要開始使用，請在頂端選單中前往 **Observability** > **Applications**。

### 建立應用程式

1. 選取 **Create application**。
2. 在 **Application information** 中，輸入 **Name**，並可選擇性輸入 **Description**。
3. 在 **Composition** 中，至少執行下列其中一項：

    - 在 **Log source** 中，使用 [PPL]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) 指定 **Base Query**，例如 `source = opensearch_dashboards_sample_data_logs`。

      建立應用程式後，您無法變更基礎查詢。
{: .note }

    - 從下拉式選單或服務地圖中選取 **Services & entities**。
    - 從下拉式選單或表格中選取 **Trace groups**。

4. 選取 **Create**。若要立即設定可用性，請選取 **Create and Set Availability**。

### 建立視覺化

1. 選取 **Log Events** 索引標籤。
1. 使用 [PPL]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) 在基礎查詢之上繼續建構。查詢編輯器已套用基礎查詢，因此請從下一個命令開始，例如 `stats count() by span(timestamp, 1h)`，然後選取 **Run**。
1. 選取 **Visualizations** 索引標籤以查看您的視覺化。
1. 展開 **Save** 下拉選單，輸入視覺化的名稱，然後選取 **Save**。

若要查看您的視覺化，請選取 **Panel** 索引標籤。

### 設定可用性

可用性是指應用程式的狀態，由[時間序列指標]({{site.url}}{{site.baseurl}}/observing-your-data/app-analytics/#time-series-metric)上設定的可用性層級決定。

若要為現有應用程式設定可用性，請選取 **Configuration** 索引標籤，然後選取 **Set Availability**。若要建立可用性層級，您必須設定下列項目：
- color：首頁上可用性徽章的色彩。
- name：首頁上可用性徽章中的文字。
- expression：用來判斷可用性的比較運算子。
- value：計算可用性時使用的值。

![設定可用性]({{site.url}}{{site.baseurl}}/images/app_availability_level.gif)

根據預設，應用程式分析會顯示您資料過去 24 小時的結果。若要查看不同時間範圍的資料，請使用日期與時間選擇器。

#### 時間序列指標

時間序列指標是指任何查詢跨越時間戳記且為折線圖的視覺化。接著您可以使用 PPL 在記錄檔上定義任意條件，以建立隨時間變化的視覺化。

##### 範例
```
source = <index_name> | ... | ... | stats ... by span(<timestamp_field>, 1h)
```

在視覺化組態中選擇 **Line** 以建立時間序列指標。

![將視覺化變更為折線圖]({{site.url}}{{site.baseurl}}/images/visualization-line-type.gif)
