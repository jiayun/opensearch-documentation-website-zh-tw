---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用偵測器"
parent: Using Security Analytics
nav_order: 30
---

# 使用偵測器

建立偵測器後，它會與其他已儲存至系統的偵測器一同顯示在「威脅偵測器」頁面上。接著您可以對每個偵測器執行多項操作，從編輯其詳細資料到變更其狀態皆可。請參閱下列各節，以瞭解可用操作的說明。

![威脅偵測器頁面]({{site.url}}{{site.baseurl}}/images/Security/threat-detector.png){: width="60%" }

---
## 威脅偵測器清單

威脅偵測器清單包含搜尋列、**Status** 下拉式清單，以及 **Log type** 下拉式清單。
* 使用搜尋列依偵測器名稱篩選。
* 選取 **Status** 下拉式清單，依 Active 和 Inactive 狀態篩選清單中的偵測器。
* 選取 **Log type** 下拉式清單，依清單中出現的任何記錄檔類型篩選偵測器（選項取決於清單中現有的偵測器及其記錄檔類型）。

### 編輯偵測器

若要編輯偵測器，請先選取清單中「Detector name」欄內該偵測器的連結。偵測器的詳細資料視窗會開啟，並顯示偵測器組態的詳細資料。

![用於編輯偵測器的偵測器詳細資料視窗]({{site.url}}{{site.baseurl}}/images/Security/detector-details.png){: width="50%" }

* 在視窗左上方，詳細資料視窗會顯示偵測器的名稱及其狀態，即 Active 或 Inactive。
* 在視窗右上角，您可以選取 **View alerts** 前往「Alerts」視窗，或選取 **View findings** 前往「Findings」視窗。您也可以選取 **Actions** 來執行偵測器的操作。請參閱[偵測器操作]({{site.url}}{{site.baseurl}}/security-analytics/usage/detectors/#detector-actions)。
* 在視窗下方，選取「Detector details」或「Detection rules」的 **Edit** 按鈕，以進行相應的變更。
* 最後，您可以選取 **Field mappings** 索引標籤，以編輯偵測器的欄位對應；或選取 **Alert triggers** 索引標籤，以編輯與偵測器相關聯的警示。

![Field mappings 和 Alert triggers 索引標籤]({{site.url}}{{site.baseurl}}/images/Security/detector-details2.png){: width="40%" }

選取 **Alert triggers** 索引標籤後，您也可以選擇在頁面底部選取 **Add another alert condition**，為偵測器新增其他警示。
{: .tip }

### 威脅情報饋送

威脅情報饋送是一種即時、持續的資料串流，會收集與風險或威脅相關的資訊。戰術威脅情報饋送中若有一則資訊指出您的叢集可能已遭入侵，例如來自未知使用者或位置的登入，或讀取量增加等異常活動，即稱為*入侵指標 (indicator of compromise, IOC)*。調查人員可利用這些 IOC 協助隔離安全事件。

您可以為與惡意 IP 位址相關的 Sigma 規則啟用威脅情報。

若要啟用威脅情報饋送，請選取 **Enable threat intelligence-based detection** 選項。

威脅情報饋送僅適用於 **standard** 記錄檔類型。

---
## 偵測器操作

威脅偵測器操作可讓您停止和啟動偵測器，或刪除偵測器。若要啟用操作，請先選取清單中一或多個偵測器旁的核取方塊。

![威脅偵測器操作]({{site.url}}{{site.baseurl}}/images/Security/detector-action.png){: width="50%" }

### 變更偵測器狀態

1.  選取清單中您要變更狀態的一或多個偵測器。**Actions** 下拉式清單隨即啟用。
1.  視偵測器目前為使用中或未使用中，選取 **Stop detector** 或 **Start detector**。稍後，偵測器狀態的變更會以 Inactive 或 Active 顯示在偵測器清單中。

### 刪除偵測器

1. 選取清單中您要刪除的一或多個偵測器。**Actions** 下拉式清單隨即啟用。
1. 在下拉式清單中選取 **Delete**。「Delete detector」彈出式視窗會開啟，並要求您確認是否要刪除所選偵測器。
1. 選取 **Cancel** 以拒絕此操作。選取 **Delete detector** 以從清單中永久刪除所選偵測器。

## 相關文件
[建立偵測器]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/detectors-config/)