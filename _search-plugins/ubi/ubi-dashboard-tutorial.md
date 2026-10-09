---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "UBI 儀表板教學"
parent: User Behavior Insights
grand_parent: Optimizing search quality
has_children: false
nav_order: 25
---


# UBI 儀表板教學

無論您已經收集使用者事件與查詢一段時間，或是[已上傳一些範例事件](https://github.com/o19s/chorus-OpenSearch-edition/blob/main/katas/003_import_preexisting_event_data.md)，您現在都可以在 OpenSearch 的儀表板中，將透過使用者行為洞察 (UBI) 收集到的資料視覺化。

> 本教學是學習如何製作自訂儀表板的好方法。

若想快速檢視儀表板而不完成整份教學，請執行下列步驟：
1. 下載並儲存[範例 UBI 儀表板]({{site.url}}{{site.baseurl}}/assets/examples/ubi-dashboard.ndjson)。
1. 在頂端功能表中，前往 **Management > Dashboard Management**。
1. 在 **Dashboards** 面板中，選擇 **Saved objects**。
1. 在右上角，選取 **Import**。
1. 在 **Select file** 面板中，選擇 **Import**。
1. 選取您下載的 UBI 儀表板檔案，然後選取 **Import** 按鈕。

## 1. 啟動 OpenSearch Dashboards

啟動 OpenSearch Dashboards。例如，前往 `http://{server}:5601/app/home#/`。如需更多資訊，請參閱 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/)。下圖顯示首頁。
![Dashboard Home]({{site.url}}{{site.baseurl}}/images/ubi/home.png)

## 2. 建立索引模式

在 OpenSearch Management 中，瀏覽至 **Dashboards Management > Index patterns**，或使用 URL 瀏覽，例如 `http://{server}:5601/app/management/OpenSearch-dashboards/indexPatterns`。

OpenSearch Dashboards 使用索引模式存取您的索引。若要將使用者的線上搜尋行為視覺化，您必須建立索引模式，才能存取 UBI 建立的索引。如需更多資訊，請參閱[索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)。

選取 **Create index pattern** 後，會顯示您 OpenSearch 執行個體中的索引清單。UBI 儲存區預設可能會隱藏，因此請務必選取 **Include system and hidden indexes**，如下圖所示。
![Index Patterns]({{site.url}}{{site.baseurl}}/images/ubi/index_pattern2.png)

您可以使用萬用字元，將索引分組到儀表板的同一個資料來源中。在本教學中，您會將查詢儲存區與事件儲存區合併為 `ubi_*` 模式。

OpenSearch Dashboards 會提示您依結構描述中的任何 `date` 欄位進行篩選，以便您查看例如過去 15 分鐘的熱門查詢等內容。不過，若這是您的第一個儀表板，請選取 **I don't want to use the time filter**，如下圖所示。
![Index Patterns]({{site.url}}{{site.baseurl}}/images/ubi/index_pattern3.png){: width="400" }


選取 **Create index pattern** 後，您就可以開始建立顯示 UBI 儲存區資料的儀表板。

## 3. 建立新儀表板

若要建立新儀表板，請在頂端功能表中選取 **OpenSearch Dashboards > Dashboards**，然後選取 **Create > Dashboard** > **Create new**。
如果您先前未曾建立儀表板，系統會提供您建立新儀表板的選項。否則，會顯示先前建立的儀表板。


在 **New Visualization** 視窗中，選取 **Pie** 以建立新的圓餅圖。然後選取您在步驟 2 建立的索引模式。

大多數視覺化都需要對桶/面向/可彙總欄位 (數值或關鍵字) 套用某種彙總函式。您會將 `Terms` 彙總新增至 `action_name` 欄位，以便檢視事件名稱的分佈。將 **Size** 變更為您要顯示的扇區數，如下圖所示。
![Pie Chart]({{site.url}}{{site.baseurl}}/images/ubi/pie.png)

儲存視覺化，以便將其新增至您的新儀表板。現在您的儀表板上已顯示視覺化，您可以儲存儀表板。

## 4. 新增標籤雲視覺化

現在您將以類似上一個步驟的方式建立新的視覺化，來新增熱門搜尋的文字雲。  

在 **New Visualization** 視窗中，選取 **Tag Cloud**，然後選取您在步驟 2 建立的索引模式。選擇 `message` 欄位中詞彙的標籤雲視覺化，JavaScript 用戶端會在該欄位記錄原始搜尋文字。注意：經 OpenSearch 處理 (含篩選、加權等) 後的真正查詢位於 `ubi_queries` 索引中。不過，您會檢視 `ubi_events` 索引的 `message` 欄位，JavaScript 用戶端會在該欄位擷取使用者實際輸入的文字。

下圖顯示 `message` 欄位上的標籤雲視覺化。
![Word Cloud]({{site.url}}{{site.baseurl}}/images/ubi/tag_cloud1.png)

基礎查詢可在 [SQL 熱門查詢]({{site.url}}{{site.baseurl}}/search-plugins/ubi/sql-queries/#trending-queries) 找到。
{: .note}


產生的視覺化可能包含與您所需不同的資訊。`message` 欄位會隨每個事件更新，因此可能包含錯誤訊息、偵錯訊息、點擊資訊及其他不需要的資料。
若只要檢視查詢事件的搜尋詞彙，您需要在視覺化中新增篩選條件。由於您在設定時為每個搜尋事件提供了 `QUERY` 的 `message_type`，您可以依該訊息類型進行篩選，以隔離特定使用者的搜尋。若要這麼做，請選取 **Add filter**，然後在 **Edit filter** 面板中選取 **QUERY**，如下圖所示。
![Word Cloud]({{site.url}}{{site.baseurl}}/images/ubi/tag_cloud2.png)

您的儀表板上現在應該會顯示兩個視覺化 (圓餅圖與標籤雲)，如下圖所示。
![UBI Dashboard]({{site.url}}{{site.baseurl}}/images/ubi/dashboard2.png)

## 5. 新增項目點擊的直方圖

現在您將以類似上一個步驟的方式，在儀表板中新增直方圖視覺化。在 **New Visualization** 視窗中，選取 **Vertical Bar**。然後選取您在步驟 2 建立的索引模式。

檢查 `event_attributes.position.ordinal` 資料欄位。此欄位包含使用者所選清單中項目的位置。在直方圖視覺化中，x 軸代表所選項目的序號 (n)。y 軸代表第 n 個項目被點擊的次數，如下圖所示。

![Vertical Bar Chart]({{site.url}}{{site.baseurl}}/images/ubi/histogram.png)

## 6. 篩選顯示的資料

現在您可以進一步篩選顯示的資料。例如，您可以查看發生購買時點擊位置的變化。選取 **Add filter**，然後選取 `action_name:product_purchase` 欄位，如下圖所示。
![Product Purchase]({{site.url}}{{site.baseurl}}/images/ubi/product_purchase.png)


您可以新增萬用字元，以篩選包含 `*laptop*` 一詞的事件訊息，如下圖所示。
![Laptop]({{site.url}}{{site.baseurl}}/images/ubi/laptop.png "Laptop")。
