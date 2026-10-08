---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "時間篩選器"
parent: Exploring data with Discover
grand_parent: Exploring data
nav_order: 10
redirect_from:
  - /dashboards/get-started/time-filter/
---

# 使用時間篩選器

時間篩選器位於 **Dashboard**、**Discover** 和 **Visualize** 應用程式的頂端。

使用時間篩選器來選取應用程式中顯示資料的時間間隔。該篩選器支援秒、分、時、日、週、月或年的間隔。

本頁面交替使用 _時間範圍 (time range)_ 和 _時間間隔 (time interval)_ 這兩個術語來泛指篩選間隔，無論其量級是秒還是年。_時間 (Time)_ 或 _時間值 (time value)_ 指的是相對時間間隔（以秒、分或時為單位）的端點，與以日、週、月或年為單位的日期值有所區分。
{: .note}

您可以選取 _相對_ 時間間隔（相對於 _現在 (now)_ 的固定時間視窗）或 _絕對_ 時間間隔（兩個固定時間之間）。_重新整理間隔 (refresh interval)_ 決定了相對時間間隔重新整理的頻率。重新整理間隔可設定，預設為一秒 (1 s)。絕對時間間隔不受重新整理間隔的影響。

雖然大多數應用程式（例如資料記錄檔）處理的是過去的日期和時間，但相對和絕對時間間隔可以同時包含過去和未來的日期和時間。例如，相對時間間隔可以設定為從 _現在_ 到未來 24 小時。

預設的時間範圍是相對間隔的 **Last 15 minutes**。您可以在 [**Dashboards Management** > **Advanced Settings** > **Time filter defaults**]({{site.url}}{{site.baseurl}}/dashboards/management/advanced-settings/#general-settings) 變更預設值，或按照 [Selecting a time range](#selecting-a-time-range) 中所述在應用程式層級選取時間範圍。
{: .note}

## 操作時間篩選器

![Time filter interface]({{site.url}}{{site.baseurl}}/images/dashboards/time-filter-callouts.png)

時間篩選器由下列元件組成：

- _捷徑選取器 (shortcut selector)_ (A) 會開啟一個對話方塊，您可以在其中選取相對時間間隔或最近使用的時間間隔，並設定時間重新整理間隔。
- _時間範圍顯示 (time range display)_ (B) 以絕對（例如：_Mar 22, 2024 @12:00:01.000 → now_）或相對（例如：_Last 2 years_）術語顯示選取的時間範圍。
- **Show dates** 連結 (C) 會強制 _時間範圍顯示_ 以 _from → to_ 格式顯示時間間隔。
- **Refresh** 按鈕 (D) 會根據新的篩選或查詢值更新應用程式中顯示的資料。**Refresh** 會更新查詢、資料篩選器以及時間篩選器。


## 選取時間範圍

您可以在應用程式層級選取 [相對](#selecting-a-relative-time-interval) 或 [絕對](#selecting-an-absolute-time-interval) 間隔作為時間範圍。或者，您可以使用 [捷徑選取器](#using-the-time-interval-shortcuts) 選取相對或絕對間隔。


### 選取絕對時間間隔

若要選取絕對時間間隔，請依照下列步驟操作：

1. 如有必要以 **from → to** 形式顯示間隔，請選取 **Show dates**。

1. 選取顯示的開始時間。

1. 在時間選取彈出視窗中，選擇 **Absolute** 索引標籤，如下圖所示。

   ![Absolute time filter]({{site.url}}{{site.baseurl}}/images/dashboards/absolute-time-filter.png){: width="56%" }

1. 使用日曆和時間捲動工具來選擇開始時間，或在 **Start date** 文字方塊中編輯開始時間。

1. 選取顯示的結束時間。

1. 在時間選取彈出視窗中，選擇 **Absolute** 索引標籤。

1. 使用日曆和時間捲動工具來選擇結束日期和時間，或在 **End date** 文字方塊中編輯結束日期和時間。

1. 選擇 **Update** 按鈕以套用變更。

   應用程式中顯示的資料表和視覺化會自動更新，以反映新的時間間隔篩選條件。


### 選取相對時間間隔

若要選取相對時間間隔，請依照下列步驟操作：

1. 如有必要以 **from → to** 形式顯示間隔，請選取 **Show dates**。

1. 選取顯示的開始時間。

1. 在時間選取彈出視窗中，選擇 **Relative** 索引標籤，如下圖所示。

   ![Relative time filter]({{site.url}}{{site.baseurl}}/images/dashboards/relative-time-filter.png){: width="56%" }

1. 在數字組合方塊中，選取或輸入間隔數量。

1. 在間隔下拉式選單中，選取相對間隔的開始時間位於過去 (**ago**) 或未來 (**from now**)。

   您可以選擇 **Now** 作為開始時間。在此情況下，相對結束時間必須位於未來 (**from now**)。
   {: .note}

1. （選用）啟用 **Round to** 切換開關。這會將開始時間捨入至指定間隔的開頭，而不是以系統時鐘的確切時間計算偏移量。

1. 選取顯示的結束時間。

1. 執行下列其中一項操作：

   許多（甚至可能是大多數）應用程式需要以目前時間結束的相對間隔。在這種情況下，請依照緊接在後的步驟操作。

   1. 選取 **Now** 索引標籤。

   1. 在 **Now** 彈出視窗中，選取 **Set end date and time to now**。

   如果您的應用程式需要的相對結束時間不是 **now**，請執行下列操作：

   1. 在時間選取彈出視窗中，選擇 **Relative** 索引標籤。

   1. 在數字組合方塊中，選取或輸入間隔數量。

   1. 在間隔下拉式選單中，選取相對間隔的開始時間位於過去 (**ago**) 或未來 (**from now**)。

      結束時間必須晚於開始時間。如果間隔不合法，會以紅色顯示。
      {: .note}

   1. （選用）啟用 **Round to ...** 切換開關。這會將開始時間捨入至指定間隔的開頭，而不是根據系統時鐘的確切時間計算。

1. 選擇 **Update** 按鈕以套用變更。

   應用程式會更新資料表和視覺化中的資料，以反映新的時間間隔篩選條件。


### 使用時間間隔捷徑

若要從常用或先前的間隔值選取時間間隔，請依照下列步驟操作：

1. 選取搜尋列右側的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/calendar-icon.png" class="inline-icon" alt="calendar icon"/>{:/}（日曆）或 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/clock-icon.png" class="inline-icon" alt="clock icon"/>{:/}（時鐘）圖示。

1. 從捷徑彈出視窗中，選取時間篩選選項之一，如下圖所示。

   ![Time range interface]({{site.url}}{{site.baseurl}}/images/dashboards/time-range.png){: width="59%" }

   - **Quick select**：選擇從 _現在_ 到過去 (**Last**) 或未來 (**Next**) 時間的間隔。

      1. 在 **Last/Next** 下拉式選單中，選取 **Last**（過去）或 **Next**（未來）。

      1. 在數字組合方塊中，選取或輸入間隔數量。

      1. 在間隔下拉式選單中，選取相對間隔的單位。

      1. 選擇 **Apply**。

   - **Commonly used**：選擇常用的時間範圍，例如 **Today**、**Last 7 days** 或 **Last 30 days**。

   - **Recently used date ranges**：選取先前使用過的時間範圍。時間範圍可以是相對或絕對的。

- （選用）變更重新整理間隔：

   1. 在 **Refresh every** 面板中，在數字組合方塊中選取或輸入間隔數量。

   1. 在間隔下拉式選單中，選取間隔單位 (**seconds**、**minutes** 或 **hours**)。

   1. 選取 **Refresh**。

## 開始和停止資料重新整理

若要開始或停止時間間隔重新整理，請依照下列步驟操作：

1. 在 OpenSearch Dashboards 應用程式 (**Discover**、**Dashboards** 或 **Visualize**) 中，選取搜尋列右側的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/calendar-icon.png" class="inline-icon" alt="calendar icon"/>{:/}（日曆）或 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/clock-icon.png" class="inline-icon" alt="clock icon"/>{:/}（時鐘）圖示。

1. 在 **Refresh every** 面板中，選取 **Start** 或 **Stop**。

   - 如果時間間隔是相對的：

      - 開始資料重新整理會使資料選取範圍大約每隔一個 _重新整理間隔_ 更新一次。
      - 停止資料重新整理會「凍結」選取間隔，直到重新開始資料重新整理為止。

   - 如果時間間隔是絕對的，則開始或停止資料重新整理對資料選取範圍沒有任何影響。

1. 選取 **Refresh**。

   如果時間間隔重新整理已停止，捷徑選取器會顯示 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/calendar-icon.png" class="inline-icon" alt="calendar icon"/>{:/}（日曆）圖示；如果時間間隔重新整理正在執行，則會顯示 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/clock-icon.png" class="inline-icon" alt="clock icon"/>{:/}（時鐘）圖示。
   {: .note}

## 設定時區

預設情況下，時間篩選器使用您的瀏覽器偵測到的時區。若要變更時區，請前往 **Dashboards Management** > **Advanced settings** 並更新 **Timezone for date formatting** (**dateFormat:tz**) 設定。如需更多資訊，請參閱 [Advanced settings]({{site.url}}{{site.baseurl}}/dashboards/management/advanced-settings/)。

## 相關文件

- [Advanced settings]({{site.url}}{{site.baseurl}}/dashboards/management/advanced-settings/)