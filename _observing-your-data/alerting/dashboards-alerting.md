---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "警示儀表板與視覺化"
parent: Alerting
nav_order: 50
has_children: true
---

# 警示儀表板與視覺化
於 2.9 版推出
{: .label .label-purple }

在單一整合檢視中建立、管理警示並採取行動，快速識別並解決問題。使用 **Dashboard** 介面來：

- 設定、新增及調整觸發警示與通知的規則和條件。
- 建立顯示趨勢與模式的圖表，並建置直覺的儀表板，即時掌握重要指標與資料點。
- 透過一覽式檢視在同一處監視您的警示。

下圖為 Dashboard 介面的快照。

![警示視覺化範例]({{site.url}}{{site.baseurl}}/images/dashboards/alerting-dashboard.png){: width="800" height="800" }

## 入門

開始之前，您必須具備：

- 已安裝 OpenSearch 與 OpenSearch Dashboards 2.9 或更新版本。請參閱[安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/)。
- 已安裝 Alerting 與 Notifications Dashboards 外掛程式。請參閱[管理 OpenSearch Dashboards 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/plugins/)以開始使用。

## 設定管理員設定

使用者只能存取、建立或管理其擁有權限之資源的警示。警示儀表板與視覺化的存取權由 OpenSearch 與 OpenSearch Dashboards 權限控制。此功能預設為啟用，並顯示為 **Dashboards Management** > **Advanced Settings** > **Visualization** 下的功能。若停用該設定，則不會顯示。您可以在叢集層級的 `opensearch-dashboards.yml` 檔案中停用該設定。

## 警示視覺化的一般需求

警示視覺化會以時間序列圖表顯示，讓您一覽警示、警示狀態、上次更新時間及警示原因。圖表上最多可顯示 10 個指標，每個數列可在圖表上顯示為一條線。

設定或建立警示視覺化時，請留意下列需求。該視覺化：

- 必須是[折線圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/line-charts/)，其中每個數列都顯示為一條線
- 必須至少包含一個 Y 軸指標彙總
- 不得有非 Y 軸的指標彙總類型
- X 軸桶必須使用日期直方圖彙總類型
- 底部必須有 X 軸
- 必須定義一個 X 軸彙總桶
- 必須有有效的時間型 X 軸

## 建立警示監視器

根據預設，當您開始使用 Dashboard 介面建立警示監視器工作流程時，會看到選單導向的介面。此介面提供一系列選項，以全螢幕、彈出式視窗、下拉式選單或下拉式清單顯示。這些選項可讓您定義可監視的指標、設定閾值、自訂自動化工作流程的觸發條件，並在符合條件時產生動作。您只能建立[依查詢監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/)。

若要建立警示監視器：

1. 從 OpenSearch Dashboards 主選單選擇 **Dashboard**。
2. 在 **Dashboards** 視窗中，選取 **Create**，然後選擇 **Dashboard**。
3. 選取 **Add an existing**，然後從 **Add panels** 清單中選取適當的警示視覺化。該視覺化即會新增至儀表板。
4. 在視覺化面板中，選擇省略號圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/ellipsis-icon.png" class="inline-icon" alt="ellipsis icon"/>{:/})。
5. 在 **Options** 選單中，選取 **Add alerting monitor**。
6. 輸入 **Monitor details** 與 **Triggers** 的資訊。
7. 選擇 **Create monitor**。監視器即會新增至視覺化。

下列螢幕擷取畫面顯示這些步驟的範例。

![建立監視器介面]({{site.url}}{{site.baseurl}}/images/dashboards/create-monitor-menu.png){: width="400" height="400" }

## 關聯監視器

您可以使用 Dashboard 介面而非外掛程式頁面，將特定監視器類型與視覺化關聯，讓您透過單一介面新增、檢視及編輯監視器資料。

延續上一節建立的警示視覺化與儀表板，依照下列步驟將現有監視器與視覺化關聯：

1. 在視覺化面板中，選擇省略號圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/ellipsis-icon.png" class="inline-icon" alt="ellipsis icon"/>{:/})。
2. 選取 **Associated monitors**。
3. 在 **Select monitor to associate** 下拉式選單中，選取監視器。下拉式選單中只會列出符合資格的監視器。
4. 檢視監視器的基本資訊。若要檢視完整詳細資料，請選取 **View monitor page** 以開啟 Alerting 外掛程式頁面。
5. 選取 **Associate monitor**。現有監視器即會與視覺化關聯。

## 探索警示監視器詳細資料

建立或關聯警示監視器後，請依照下列步驟確認監視器正在產生警示，並探索警示詳細資料：

1. 開啟警示儀表板。警示會以三角形圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards/triangle-icon.png" class="inline-icon" alt="triangle icon"/>{:/}) 標示在視覺化上。
2. 將游標停留在三角形圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards/triangle-icon.png" class="inline-icon" alt="triangle icon"/>{:/}) 上，以檢視高階資料，例如警示數量。若要調查警示詳細資料，請選取三角形圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards/triangle-icon.png" class="inline-icon" alt="triangle icon"/>{:/}) 以開啟飛出式視窗，顯示更詳細的監視器資訊。或者，在視覺化面板中選取省略號圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/ellipsis-icon.png" class="inline-icon" alt="ellipsis icon"/>{:/})，然後選擇 **View events**。
3. 選取省略號圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/ellipsis-icon.png" class="inline-icon" alt="ellipsis icon"/>{:/})，然後選取 **Alerting** > **Associated monitors**。
4. 從清單中選擇警示監視器。歷史記錄、警示及關聯的視覺化等資訊會顯示在視覺化面板中。
5. 取消連結或編輯監視器。
   1. 選取 **Actions** 下方的連結圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/link-icon.png" class="inline-icon" alt="link icon"/>{:/})，將監視器與視覺化取消連結。這只會將監視器與視覺化解除關聯，不會刪除監視器。
   2. 選取編輯圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/edit-icon.png" class="inline-icon" alt="edit icon"/>{:/}) 以編輯監視器的指標。

## 後續步驟

- [進一步瞭解 Dashboard 應用程式]({{site.url}}{{site.baseurl}}/dashboards/dashboard/index/)。
- [進一步瞭解警示]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/index/)。
