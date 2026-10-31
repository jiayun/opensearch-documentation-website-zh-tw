---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "營運面板"
parent: Classic observability apps
nav_order: 50
redirect_from:
  - /observability-plugin/operational-panels/
---

# 營運面板

營運面板是包含使用 [Piped Processing Language]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) (PPL) 查詢所建立之視覺化的儀表板。您可以在 [Event analytics]({{site.url}}{{site.baseurl}}/observing-your-data/event-analytics/)、[Metric analytics]({{site.url}}{{site.baseurl}}/observing-your-data/prometheusmetrics/) 或 [Application analytics]({{site.url}}{{site.baseurl}}/observing-your-data/app-analytics/) 中建立視覺化，然後將其新增至面板。在 OpenSearch Dashboards 中，營運面板稱為 **Observability dashboards**。

營運面板是[經典可觀測性應用程式]({{site.url}}{{site.baseurl}}/observing-your-data/classic-observability-apps/)。啟用多個資料來源或新版首頁時，無法使用營運面板。

若要檢視營運面板，請在頂端功能表中前往 **Observability** > **Dashboards**。若要在不新增自有資料的情況下探索一組範例面板與視覺化，請選取 **Add samples**。

## 建立操作面板

若要建立操作面板，請依照下列步驟進行：

1. 在頂端選單中，前往 **Observability** > **Dashboards**。
1. 選取 **Create Dashboard**。
1. 在 **Name** 中輸入面板名稱，然後選取 **Create**。

## 新增視覺化

若要將視覺化新增至面板，請開啟該面板，選取 **Add visualization**，然後選取下列其中一個選項：

- **Select existing visualization**：從清單中選取已儲存的視覺化，然後選取 **Add**。
- **Create new visualization**：開啟 Event analytics 探索器。輸入 PPL 查詢，選取 **Run**，然後選取 **Visualizations** 索引標籤。若要將視覺化儲存至面板，請選取 **Save**，在 **Custom operational dashboards/application** 中選取該面板，輸入 **Name**，然後選取 **Save**。

操作面板會依時間篩選每個視覺化，因此視覺化查詢的索引必須包含 `date` 類型的欄位。若索引沒有 `date` 欄位，視覺化就會是空的。
{: .note}

## 篩選視覺化

若要篩選面板中的所有視覺化，請在面板頂端的搜尋列中輸入 PPL `where` 子句，例如 `where response = '404'`。若要變更所有視覺化的時間範圍，請使用時間選擇器，然後選取 **Refresh**。

## 管理面板

若要重新載入、重新命名、複製或刪除面板，請開啟該面板並選取 **Dashboard Actions**。若要刪除面板，請在確認對話方塊中輸入 `delete`。
