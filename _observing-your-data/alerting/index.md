---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "警示"
nav_order: 110
has_children: true
redirect_from:
  - /monitoring-plugins/alerting/
  - /monitoring-plugins/alerting/index/
  - /observing-your-data/alerting/
---

# 警示

警示功能可讓您監視資料，並在符合特定條件時自動傳送通知。若要建立警示，請執行下列步驟：

- 設定 _監視器_，這是依照定義的排程執行並查詢 OpenSearch 索引的工作。必要。
- 設定一或多個 _觸發條件_，用於定義產生事件的條件。選用。
- 設定 _動作_，也就是警示觸發後發生的行為。選用。

## 重要詞彙

下表列出 OpenSearch 中以及 Alerting 文件各處常用的警示術語。

術語 | 定義
:--- | :---
監視器 | 依定義排程執行並查詢 OpenSearch 索引的工作。這些查詢的結果接著會作為一或多個觸發條件的輸入。
觸發條件 | 符合時便會產生警示的條件。請參閱[觸發條件]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/triggers/)。
警示 | 與觸發條件相關聯的事件。建立警示時，觸發條件會執行各項動作，包括傳送通知。
動作 | 觸發警示時所執行的特定工作。請參閱[動作]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/actions/)。
通知 | 觸發警示時傳送給使用者的訊息。請參閱[通知]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/index/)。

## 警示狀態

下表列出警示的各種狀態。

狀態 | 說明
:--- | :---
Active | 警示仍在進行中且未經確認。警示會保持此狀態，直到您確認該警示、刪除與該警示相關聯的觸發條件，或完全刪除監視器為止。若觸發條件不再符合，警示也可能會離開 Active 狀態。例如，若某索引有 4,000 份文件，且觸發條件為 `numOfDocs > 5000`，則當索引新增 3,000 份文件時會產生 Active 警示。若隨後將新增的 3,000 份文件從索引中刪除，由於條件不再被觸發，警示會變更為 Completed 狀態。
Acknowledged | 警示已確認，但根本原因尚未修復。
Completed | 警示已不再進行中。當對應的觸發條件評估結果為 `false` 後，警示會進入此狀態。
Error | 執行觸發條件時發生錯誤---通常是觸發條件或目的地設定不當所致。
Deleted | 與此警示相關聯的監視器或觸發條件在警示進行期間被刪除。

## 建立警示監視器

以下範例建立一個監視器，當網站在一天內收到超過 100 個請求時會產生警示。此範例使用 OpenSearch Dashboards 的範例網路記錄檔。若要新增範例資料，請在 OpenSearch Dashboards 首頁選取 **Add sample data**，然後在 **Sample web logs** 卡片上選取 **Add data**。

若要建立監視器，請依照下列步驟操作：

1. 在頂端選單中，前往 **OpenSearch Plugins** > **Alerting**。
1. 選取 **Monitors** 分頁，然後選取 **Create monitor**。
1. 在 **Monitor details** 中，設定下列設定：
   - **Monitor name**：輸入 `Daily web traffic`。
   - **Monitor type**：選取 **Per query monitor**。如需監視器類型的詳細資訊，請參閱 [監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/)。
   - **Monitor defining method**：選取 **Visual editor**。
   - **Schedule**：保留預設值，即每分鐘執行一次監視器。
1. 在 **Select data** 中，於 **Indexes** 輸入 `opensearch_dashboards_sample_data_logs` 並按 Enter。在 **Time field** 中選取 `timestamp`。
1. 在 **Query** 中，保留 **COUNT OF documents** 指標。在 **Time range for the last** 中，輸入 `1` 並選取 **day(s)**。
1. 在 **Triggers** 中，選取 **Add trigger**，然後設定該觸發條件：
   - **Trigger name**：輸入 `More than 100 requests`。
   - **Severity level**：保留 **1 (Highest)**。
   - **Trigger condition**：選取 **IS ABOVE** 並輸入 `100`。

   觸發條件預覽會顯示所選時間範圍內的文件數量。如需詳細資訊，請參閱 [觸發條件]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/triggers/)。
1. （選用）在 **Actions** 中新增一個動作，於符合觸發條件時傳送通知。動作需要通知通道。如果您沒有通知通道，請選取 **Manage channels** 來建立一個。如需詳細資訊，請參閱 [動作]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/actions/) 與 [通知]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/index/)。
1. 選取 **Create**。

監視器每分鐘執行一次。由於範例網路記錄檔在一般一天內包含超過 100 個請求，因此觸發條件會被滿足，監視器會產生處於 **Active** 狀態的警示。若要檢視警示，請在 **Alerting** 頁面選取 **Alerts** 分頁。

如需各項設定的詳細資訊以及建立依桶監視器的方法，請參閱 [依查詢與依桶監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/per-query-bucket-monitors/)。若要建立其他類型的監視器，請參閱 [監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/)。
