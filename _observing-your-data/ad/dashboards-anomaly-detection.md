---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "異常偵測視覺化與儀表板"
parent: Anomaly detection
nav_order: 50
---

# 異常偵測儀表板與視覺化
於 2.9 版推出
{: .label .label-purple }

啟用異常偵測後，OpenSearch 提供自動化的方式來偵測有害的離群值並保護您的資料。套用至指標時，OpenSearch 會使用演算法持續分析系統與應用程式、判定正常基準，並呈現異常。 

您可以將資料視覺化連接至 OpenSearch 資料集，然後在 **Dashboard** 介面中，從視覺化建立、執行及檢視即時異常結果。只需幾個步驟，您就能整合追蹤、指標與記錄檔，讓您的應用程式與基礎架構具備完整的可觀測性。

## 入門 

開始之前，您必須：

- 已安裝 OpenSearch 與 OpenSearch Dashboards 2.9 或更新版本。請參閱[安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/)。
- 已安裝 Anomaly Detection 外掛程式 2.9 或更新版本。請參閱[安裝 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。
- 已安裝 Anomaly Detection Dashboards 外掛程式 2.9 或更新版本。請參閱[管理 OpenSearch Dashboards 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/plugins/)以開始使用。

## 異常偵測視覺化的一般需求

異常偵測視覺化會以時間序列圖表顯示，讓您快速掌握異常發生的時間點。您最多可在圖表上顯示 10 個指標，每個序列都可以在圖表上以一條線顯示。請注意，圖表上只會顯示即時異常。如需即時與歷史異常偵測的詳細資訊，請參閱[異常偵測，步驟 3：設定偵測器工作]({{site.url}}{{site.baseurl}}/observing-your-data/ad/index/#step-3-set-up-detector-jobs)。

設定或建立異常偵測視覺化時，請留意下列需求。視覺化：

- 必須是[折線圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/line-charts/)，且每個序列都以一條線顯示
- 必須至少包含一個 Y 軸指標彙總
- 不得包含非 Y 軸的指標彙總類型
- X 軸桶 (bucket) 必須使用日期長條圖 (date histogram) 彙總類型
- X 軸必須位於底部
- 必須定義一個 X 軸彙總桶
- 必須具有有效的時間型 X 軸

## 設定管理員設定

使用者只能存取、建立或管理其具有權限之資源的異常偵測器。異常偵測儀表板與視覺化的存取權由 OpenSearch 與 OpenSearch Dashboards 權限控制。此功能預設為啟用，並以功能形式顯示於 **Dashboards Management** > **Advanced Settings** > **Visualization** 下。若停用此設定，則不會顯示於 **Dashboards Management** 下。您可以在 `opensearch-dashboards.yml` 檔案中於叢集層級停用此設定。

## 建立異常偵測器

首先，請建立異常偵測器：

1. 從 OpenSearch Dashboards 主選單選取 **Dashboard**。
2. 在 **Dashboards** 視窗中，選取 **Create**，然後選擇 **Dashboard**。
3. 選取 **Add an existing**，然後從 **Add panels** 清單中選取適當的視覺化。該視覺化即會新增至儀表板。
4. 在視覺化面板中，選擇省略符號圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/ellipsis-icon.png" class="inline-icon" alt="ellipsis icon"/>{:/})。
5. 從 **Options** 選單中，選擇 **Anomaly Detection** > **Add anomaly detector**。
6. 選取 **Create new detector**。
7. 輸入 **Detector details** 與 **Model features** 的資訊。最多可設定五個模型特徵。 
8. 若要在飛出視窗中預覽視覺化，請切換 **Show visualization** 按鈕。
9. 選取 **Create detector**。建立新的偵測器後，該偵測器即會新增至視覺化，如下圖所示。  

![新增偵測器的介面]({{site.url}}{{site.baseurl}}/images/dashboards/add-detector.png){: width="800" height="800" }

## 將異常偵測器新增至視覺化

使用單一介面新增、檢視及編輯您要與視覺化建立關聯的異常偵測器。延續前述教學中的視覺化與儀表板，請依照下列步驟將異常偵測器與視覺化建立關聯：
 
1. 在視覺化面板中選取省略符號圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/ellipsis-icon.png" class="inline-icon" alt="ellipsis icon"/>{:/})，然後選取 **Anomaly Detection**。
2. 選取 **Associate a detector**。
3. 從 **Select detector to associate** 下拉式選單中選取偵測器。下拉式選單中只會列出符合資格的偵測器。
4. 檢視偵測器的基本資訊。若要檢視完整詳細資料，請選取 **View detector page** 以開啟 Anomaly Detection 外掛程式頁面。
5. 選取 **Associate detector**。現有的偵測器現在已與視覺化建立關聯，如下圖所示。

![建立偵測器關聯的介面與確認訊息]({{site.url}}{{site.baseurl}}/images/dashboards/anomaly-detect-dashboard.png){: width="800" height="800" }

## 重新整理視覺化

視覺化會依據閾值設定，以指定的間隔自動重新整理。若要手動重新整理視覺化，請選取 Dashboard 頁面上的 **Refresh** 按鈕。

## 後續步驟

- [深入了解 Dashboard 應用程式]({{site.url}}{{site.baseurl}}/dashboards/dashboard/index/)。
- [深入了解異常偵測]({{site.url}}{{site.baseurl}}/observing-your-data/ad/index/)。
