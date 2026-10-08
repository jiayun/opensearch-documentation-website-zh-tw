---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管理儀表板"
parent: Creating dashboards
nav_order: 40
has_children: false
---

# 管理儀表板

您可以從 **Dashboards** 應用程式主頁（如下圖所示）管理 OpenSearch Dashboards 中的儀表板。

![Dashboards landing page]({{site.url}}{{site.baseurl}}/images/dashboards/dash-landing-page.png)

您可以執行以下操作：

- [儲存儀表板](#saving-a-dashboard)。
- 建立與編輯儀表板。請參閱 [開啟儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/opening-a-dashboard/)。
- [將儀表板匯出至檔案](#exporting-a-dashboard)。
- [刪除儀表板](#deleting-dashboards)。

## 儲存儀表板

您可以儲存新建立的儀表板，或儲存對現有儀表板的變更。

### 儲存新儀表板

若要儲存新儀表板，請按照以下步驟操作：

1. 在應用程式選單中，選取 **Save**。

   應用程式會顯示 **Save dashboard** 對話方塊。

1. 在 **Title** 欄位中輸入儀表板的標題。

1. (選用) 輸入 **Description**。

1. (選用) 若要儲存目前的時間篩選器，以便在重新開啟儀表板時套用，請選取 **Store time with dashboard**。

1. 選取 **Save**。

### 儲存現有儀表板

您可以隨時儲存儀表板。

若要儲存現有儀表板：

1. 選取 **Create** 面板右上角的 **Save**。

   應用程式會顯示 **Save dashboard** 對話方塊。如果您之前已儲存過該儀表板，**Title** 欄位將包含該儀表板的標題。

1. (選用) 若要變更儀表板名稱，請在 **Title** 欄位中為儀表板輸入新標題。

   在未選取 **Save as new dashboard** 的情況下儲存現有儀表板，會覆寫該儀表板之前的狀態，即使您已重新命名儀表板也是如此。
   {: .warning}

1. (選用) 更新 **Description**。

1. (選用) 若要將儲存的儀表板保持在目前狀態，並將變更儲存為新儀表板，請選取 **Save as new dashboard**。

1. (選用) 若要儲存目前的時間篩選器，以便在重新開啟儀表板時套用，請選取 **Store time with dashboard**。

1. 選取 **Save** 按鈕。


## 匯出儀表板

您可以將儀表板匯出為 PDF 檔案或 PNG 圖片檔案。

匯出儀表板是一項 Reporting 功能。您必須啟用 Reporting 外掛程式才能匯出檔案。
{: .note}

此功能需要 Reporting 外掛程式。有關報告的更多資訊，請參閱 [Reporting using OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/reporting/report-dashboard-index/)。

1. 從應用程式選單中選取 **Reporting**。

1. 從下拉選單中，選取 **Download PDF** 或 **Download PNG**。

   應用程式會顯示 **Generating report** 對話方塊。報告可能需要幾秒鐘才能產生。

1. 根據您的瀏覽器偏好設定，報告將在瀏覽器中開啟或直接下載。


## 刪除儀表板

若要刪除一個或多個儀表板，請按照以下步驟操作：

1. 在 [導覽面板]({{site.url}}{{site.baseurl}}/dashboards/navigating-ui/#the-left-navigation-panel) 中，選取 **OpenSearch Dashboards** > **Dashboards**。

1. 從 **Dashboards** 表格的清單中，選取所有您要刪除的儀表板旁的核取方塊。

1. 在 **Dashboards** 面板的 **Search** 欄位左側，選擇 **Delete N Dashboards** 按鈕（其中 **N** 為已勾選的方塊數量）。

1. 在確認對話方塊中，選擇 **Delete**。
