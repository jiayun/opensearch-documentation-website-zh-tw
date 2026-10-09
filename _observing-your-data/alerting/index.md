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

## 重要術語

下表列出 OpenSearch 及警示文件中常用的警示術語。

術語 | 定義
:--- | :---
監視器 | 依照定義的排程執行並查詢 OpenSearch 索引的工作。這些查詢的結果隨後會作為一或多個觸發條件的輸入。
觸發條件 | 若符合即產生警示的條件。請參閱[觸發條件]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/triggers/)。
警示 | 與觸發條件相關聯的事件。建立警示後，觸發條件會執行動作，包括傳送通知。
動作 | 警示被觸發時所執行的特定工作。請參閱[動作]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/actions/)。
通知 | 警示被觸發時傳送給使用者的訊息。請參閱[通知]({{site.url}}{{site.baseurl}}/notifications-plugin/index/)。

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

您可以依照下列基本步驟建立警示監視器：

1. 在 **OpenSearch Plugins** 主選單中，選擇 **Alerting**。
1. 選擇 **Create monitor**。監視器類型的詳細資訊請參閱[監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/)。
1. 輸入 **Monitor details**，包括監視器類型、方法與排程。  
1. 從下拉式清單中選取資料來源。
1. 在 Query 區段中定義指標。
1. 新增觸發條件。觸發條件的詳細資訊請參閱[觸發條件]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/triggers/)。
1. 新增動作。動作的詳細資訊請參閱[動作]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/actions/)。
1. 選取 **Create**。

各種特定監視器類型的建立方式，請參閱其各自的說明文件以了解更多資訊。
