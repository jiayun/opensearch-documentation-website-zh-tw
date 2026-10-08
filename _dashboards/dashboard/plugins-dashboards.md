---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將外掛程式整合至儀表板"
parent: Observability
nav_order: 5
---

# 將外掛程式整合至儀表板

Observability 是一組外掛程式與應用程式，可讓您使用 [Piped Processing Language]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) 探索、發掘及查詢儲存在 OpenSearch 中的資料，藉此將資料驅動的事件視覺化。Observability 提供統一的體驗，讓您從常見的資料來源收集並監視指標、記錄檔與追蹤。透過將資料收集與監視整合在同一處，您可以對整個基礎架構實現全端、端對端的可觀測性。

您可以使用 **Observability Dashboards** 或 **Dashboard** 來管理您的可觀測性外掛程式，而無需使用外掛程式頁面。此功能為您提供：

- **立即存取已安裝的外掛程式：**儀表板會在同一處顯示所有已安裝的外掛程式。
- **提升效率：**透過儀表板隨時可用的外掛程式清單，您可以在 OpenSearch Dashboards 中啟用、停用、更新或移除外掛程式。
- **更有效的疑難排解：**從儀表板檢視外掛程式清單，可協助您快速找出可能造成問題的外掛程式。
- **強化安全性：**透過儀表板隨時可用的外掛程式清單，您可以輕鬆查看是否有過時或有弱點的外掛程式，並快速移除或更新它們，將安全性風險降至最低或加以避免。
- **提升網站效能：**從儀表板檢視外掛程式清單，可協助您找出任何可能拖慢網站速度或造成效能問題的外掛程式。

請觀看以下影片，在 20 秒內了解從 Dashboards 應用程式管理外掛程式的基本概念。

![使用 Dashboards 查看可觀測性外掛程式清單的示範](https://user-images.githubusercontent.com/105296784/234345611-50beb9a6-6118-449a-b015-b9f9e90b525e.gif)

## 查看已安裝的外掛程式清單

若要從 Dashboards 應用程式查看已安裝的外掛程式清單，請執行以下步驟：

1. 從 OpenSearch Dashboards 主選單中，選取 **Dashboards**。
2. 查看項目清單並選取您的外掛程式。外掛程式會自動被歸類為 Observability Dashboard 資料類型，您可以透過篩選來專注於特定項目。

## 新增與移除外掛程式

若要從 Dashboards 應用程式新增外掛程式，請執行以下步驟：

1. 從 OpenSearch Dashboards 主選單中，選取 **Dashboards**。
2. 在 **Dashboards** 視窗中，選取 **Create** > **Dashboard**。
3. 在 **Create operational panel** 視窗中，在 **Name** 欄位輸入名稱，然後選取 **Create**。該外掛程式將同時新增至 Observability 應用程式與 Dashboards 應用程式。

您可以透過選取 **Actions** 欄位下方的編輯圖示，然後選取 **Delete** 來從 Dashboards 應用程式移除外掛程式。

## 掌握 OpenSearch Dashboards 外掛程式的最新動態

GitHub 上的 [OpenSearch plugins repository](https://github.com/opensearch-project/opensearch-plugins) 是追蹤並貢獻任務、功能、增強功能與錯誤的絕佳方式。OpenSearch Project 團隊歡迎您的建議。
