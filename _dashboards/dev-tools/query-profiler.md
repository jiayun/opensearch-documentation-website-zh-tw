---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Query Profiler
parent: Using Dev Tools
grand_parent: Exploring data
nav_order: 30
---

# Query Profiler

使用 Dev Tools 中的 **Query Profiler** 索引標籤來測量搜尋查詢中每個元件執行所需的時間。Query Profiler 使用 [Profile API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/profile/) 執行您的查詢，並將結果以視覺化方式呈現，讓您能夠識別最耗時的查詢與彙總。

當您開啟 Query Profiler 時，編輯器包含下列預設查詢（其中包含 `profile` 參數），如隨後圖片所示。

![Query Profiler default query]({{site.url}}{{site.baseurl}}/images/dev-tools/query-profiler-default.png)

當您選取 **Visualize profile** 時，即使您的查詢不包含 `profile` 參數，Query Profiler 也會收集剖析資料。若要將剖析資料包含在回應窗格中，請在查詢中保留 `"profile": true`。
{: .note}

## 前置條件

本頁面的範例使用 **Sample eCommerce orders** 資料集。如果您使用的是本機安裝的 OpenSearch Dashboards 且尚未新增範例資料，請參閱 [Add sample data]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

## 剖析查詢

若要剖析查詢，請依照下列步驟操作：

1. 前往 **Dev Tools**，並在頁面頂端選取 **Query Profiler**。
1. 將編輯器窗格中的預設查詢取代為您要剖析的查詢。例如，輸入下列查詢，此查詢會搜尋電子商務範例資料，並計算平均訂單總額以及依顧客性別的細分結果：

   ```json
   GET opensearch_dashboards_sample_data_ecommerce/_search
   {
     "profile": true,
     "query": {
       "bool": {
         "must": [
           { "match": { "category": "Clothing" } },
           { "match": { "manufacturer": "Elitelligence" } }
         ],
         "filter": [
           { "range": { "taxful_total_price": { "gte": 50 } } }
         ]
       }
     },
     "aggs": {
       "avg_price": {
         "avg": { "field": "taxful_total_price" }
       },
       "by_gender": {
         "terms": { "field": "customer_gender" }
       }
     }
   }
   ```
   {% include copy-curl.html %}

1. 選取播放圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dev-tools/play-icon.png" class="inline-icon" alt="play icon"/>{:/}) 或按下 `Ctrl/Cmd+Enter` 來執行查詢。OpenSearch 會在右側窗格中顯示回應。
1. 選取 **Visualize profile**。

若要還原預設查詢並清除結果，請選取播放圖示旁的重設圖示。

## 審查分片時間

**Profile Results** 區段會列出處理該查詢的分片，以及每個分片的 **Search time** 與 **Aggregation time**，如隨後圖片所示。

![Query Profiler shard results]({{site.url}}{{site.baseurl}}/images/dev-tools/query-profiler-results.png)

條形圖的顏色表示每個分片消耗的最大時間比例：

- 綠色：50% 或更低 (低)
- 橘色：51--80% (中)
- 紅色：超過 80% (高)

若要變更這些百分比，請選取圖例旁的齒輪圖示，並更新 **Red (>80%)** 與 **Orange (>50%)** 的閾值。若要還原預設值，請選取 **Reset to defaults**。

您也可以在此區段執行下列操作：

- 若要尋找特定分片，請在 **Search shard** 欄位中輸入其名稱。
- 若要將清單依彙總時間而非搜尋時間排序，請選取 **Sort by: Search time**，然後選擇 **Sort by: Aggregation time**。
- 若要變更顯示的分片數量，請選取 **Rows per page**。

## 審查查詢時間

選取一個分片以顯示其查詢細分。左側窗格包含 **Search** 索引標籤與 **Aggregation** 索引標籤，每個標籤列出在該分片上執行的元件及其所需時間。選取元件旁的箭頭可展開其子查詢。

選取一個元件以顯示其詳細資訊，如隨後圖片所示。

![Query Profiler operation breakdown]({{site.url}}{{site.baseurl}}/images/dev-tools/query-profiler-breakdown.png)

詳細資訊窗格包含下列資訊：

- 元件名稱、其重寫後的 Lucene 查詢以及 **Total time**。
- **Query Hierarchy**：查詢及其子查詢的分層結構，以及各自佔總時間的百分比。
- **Operation Breakdown**：該元件執行的低階 Lucene 操作（例如 `Create Weight`、`Build Scorer` 與 `Next Doc`），包含以奈秒為單位的時間以及每項操作執行的次數。

若要在操作細分的圖表檢視與表格檢視之間切換，請選取 **Operation Breakdown** 標題右側的 **Visual breakdown** 或 **Raw data** 圖示。

## 匯入與匯出剖析結果

若要儲存剖析結果，請從頂端選單選取 **Export JSON**。Query Profiler 會將結果下載為 `profile.json` 檔案。

若要載入查詢或先前儲存的剖析結果，請從頂端選單選取 **Import**，在 **Import to** 中選擇下列其中一個選項，選取檔案，然後選取 **Import**：

- **Search query**：將搜尋查詢載入編輯器窗格。
- **Profile JSON**：載入剖析結果並顯示視覺化內容，而無需執行查詢。

## 更新 Query Profiler 設定

若要更新您的偏好設定，請從頂端選單選取 **Settings**。您可以設定下列項目：

- **Font Size**：設定編輯器的字體大小。
- **Wrap long lines**：對超過編輯器寬度的行進行自動換行。

若要查看 Query Profiler 的說明，請從頂端選單選取 **Help**。

## 後續步驟

- 有關 Query Profiler 所使用之 API 的資訊，請參閱 [Profile API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/profile/)。
- 有關撰寫查詢的資訊，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。
