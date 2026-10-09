---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "比較單一查詢"
nav_order: 10
parent: Search Relevance Workbench
grand_parent: Optimizing search quality
has_children: false
---

# 比較單一查詢

透過 OpenSearch Dashboards 中的 Compare Search Results，您可以並排比較兩個查詢的結果，判斷其中一個查詢是否產生比另一個更好的結果。使用此工具，您可以透過嘗試不同查詢來評估搜尋品質。

例如，您可以套用下列其中一種查詢變更，查看結果如何改變：

- 為欄位設定不同的權重
- 使用不同的詞幹提取或詞形還原策略
- 使用詞元組合（Shingling）

## 先決條件

開始之前，您必須在 OpenSearch 中將資料編製索引。若要瞭解如何建立新索引，請參閱[將資料編製索引]({{site.url}}{{site.baseurl}}/opensearch/index-data/)。

或者，您可以使用下列步驟，在 OpenSearch Dashboards 中新增範例資料：

1. 在頂端功能表列中，前往 **OpenSearch Dashboards > Overview**。
1. 選取 **View app directory**。
1. 選取 **Add sample data**。
1. 選擇其中一個內建資料集，然後選取 **Add data**。

<!-- vale off -->
## 在 OpenSearch Dashboards 中使用 Compare Search Results
<!-- vale on -->

若要在 OpenSearch Dashboards 中比較搜尋結果，請執行下列步驟。

**步驟 1：** 在頂端功能表列中，前往 **OpenSearch Plugins > Search Relevance**。

**步驟 2：** 在搜尋列中輸入搜尋文字。

**步驟 3：** 為 **Query 1** 選取索引，並以 [OpenSearch Query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/) 輸入查詢（僅限請求本文）。`GET` HTTP 方法與 `_search` 端點已隱含指定。使用 `%SearchText%` 變數來參照搜尋列中的文字。

以下是查詢範例：

```json
{
  "query": {
    "multi_match": {
      "query": "%SearchText%",
      "fields": [ "description", "item_name" ]
    }
  }
}
```

**步驟 4：** 為 **Query 2** 選取索引，並輸入查詢（僅限請求本文）。

下列查詢範例會提高搜尋結果中 `title` 欄位的權重：

```json
{
  "query": {
    "multi_match": {
      "query": "%SearchText%",
      "fields": [ "description", "item_name^3" ]
    }
  }
}
```

**步驟 5：** 選取 **Search**，並比較 **Result 1** 與 **Result 2**。

下列範例畫面顯示在 `description` 與 `item_name` 欄位中搜尋「cup」一詞時，提高與未提高 `item_name` 權重的結果。

![比較搜尋結果]({{site.url}}{{site.baseurl}}/images/search_relevance.png)

如果 Result 1 中的某個結果也出現在 Result 2 中，結果編號下方的 `Up` 與 `Down` 指標會表示，相較於 Result 2 中的相同結果，該結果向上或向下移動了多少個位置。在此範例中，ID 為 2 的文件在 Result 2 中的位置相較於 Result 1 為 `Up 1` 個位置，而在 Result 1 中的位置相較於 Result 2 為 `Down 1` 個位置。

## 變更結果數量

根據預設，OpenSearch 會傳回前 10 筆結果。若要將傳回的結果數量變更為其他值，請在查詢中指定 `size` 參數：

```json
{
  "size": 15,
  "query": {
    "multi_match": {
      "query": "%SearchText%",
      "fields": [ "title^3", "text" ]
    }
  }
}
```

將 `size` 設定為較高的值（例如超過 250 份文件）可能會降低效能。
{: .note}

您無法儲存特定比較以供日後使用，因此 Compare Search Results 不適合用於系統化測試。請改為參閱[搜尋結果比較]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/comparing-search-results/)實驗。
{: .note}

## 使用 Search Relevance Workbench 比較 OpenSearch 搜尋結果

[Search Relevance Workbench]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/using-search-relevance-workbench/) 提供更豐富的視覺化選項，讓您檢視兩個查詢之間的差異。

若要使用 Search Relevance Workbench，請依照步驟 1--4 操作。顯示的結果與檢視差異的選項如下圖所示。

![比較搜尋結果]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/comparing_search_results.png)

頂端區域提供結果摘要：擷取的結果中，有多少筆僅出現在左側查詢、有多少筆僅出現在右側查詢，以及有多少筆同時出現在兩個查詢中？

接下來是擷取結果的視覺化呈現。根據預設，會顯示唯一識別碼欄位（`_id`）。您可以在 **Display Field** 下拉式清單中選取其他欄位來變更此設定。
在並排檢視中，您可以查看兩份結果清單中所有共同文件的位置變化。
選取其中一個項目會顯示索引中所有已儲存的欄位，方便您識別文件。

最後，Search Relevance Workbench 可讓您從下拉式清單中選擇不同的視覺化樣式：

* **Default style**：使用不同顏色顯示兩份結果清單中的文件（各自獨有的結果在左側以黃色顯示，在右側以紫色顯示，共同結果則以綠色顯示）。
* **Ranking change color coding**：所有獨有文件皆以紫色顯示，共同結果則以綠色顯示，讓您專注於排名變化。
* **Ranking change color coding 2**：所有獨有文件皆以灰色顯示，共同結果則以綠色顯示，讓您專注於排名變化。
* **Venn diagram color coding**：所有獨有文件皆以紫色顯示，共同結果則以藍色顯示，與兩份結果清單頂端的文氏圖相同。

## 比較 OpenSearch 搜尋結果與重新排名後的結果

Compare Search Results 的其中一個使用案例，是比較原始 OpenSearch 結果與經重新排名應用程式處理後的相同結果。OpenSearch 目前整合了下列兩個重新排名工具：

- [Amazon Kendra Intelligent Ranking for OpenSearch](#reranking-results-with-amazon-kendra-intelligent-ranking-for-opensearch)
- [Amazon Personalize Search Ranking](#personalizing-search-results-with-amazon-personalize-search-ranking)

<!-- vale off -->
### 使用 Amazon Kendra Intelligent Ranking for OpenSearch 重新排名結果
<!-- vale on -->

重新排名工具的其中一個範例是由 Amazon Kendra 團隊貢獻的 **Amazon Kendra Intelligent Ranking for OpenSearch**。此外掛程式會取得 OpenSearch 的搜尋結果，並套用 Amazon Kendra 使用向量嵌入與其他語意搜尋技術計算出的語意相關性排名。對許多應用程式而言，這能提供更好的結果排名。

若要試用 Amazon Kendra Intelligent Ranking，您必須先設定 Amazon Kendra 服務。若要開始使用，請參閱 [Amazon Kendra](https://aws.amazon.com/kendra/)。如需詳細資訊，包括外掛程式設定說明，請參閱[適用於自行管理之 OpenSearch 的 Amazon Kendra Intelligent Ranking](https://docs.aws.amazon.com/kendra/latest/dg/opensearch-rerank.html)。

### 在 OpenSearch Dashboards 中比較搜尋結果與重新排名後的結果

若要在 OpenSearch Dashboards 中比較搜尋結果與重新排名後的結果，請在 **Query 1** 中輸入查詢，並在 **Query 2** 中輸入使用重新排名工具的相同查詢。接著比較 OpenSearch 結果與重新排名後的結果。

下列範例示範在 `abo` 索引中搜尋「snacking nuts」文字。索引中的文件在 `bullet_point` 陣列中包含零食描述。

![OpenSearch Intelligent Ranking 查詢]({{site.url}}{{site.baseurl}}/images/kendra_query.png)

1. 在搜尋列中輸入 `snacking nuts`。
1. 在 **Query 1** 中輸入下列查詢，在 `bullet_point` 欄位中搜尋「snacking nuts」文字：

    ```json
    {
      "query": {
        "match": {
          "bullet_point": "%SearchText%"
        }
      },
      "size": 25
    }
    ```
1. 在 **Query 2** 中輸入使用重新排名工具的相同查詢。此範例使用 Amazon Kendra Intelligent Ranking：

    ```json
    {
      "query" : {
        "match" : {
          "bullet_point": "%SearchText%"
        }
      },
      "size": 25,
      "ext": {
        "search_configuration":{
          "result_transformer" : {
            "kendra_intelligent_ranking": {
              "order": 1,
              "properties": {
                "title_field": "item_name",
                "body_field": "bullet_point"
              }
            }
          }
        }
      }
    }
    ```

    在上述查詢中，`body_field` 參照索引中文件的 body 欄位，Amazon Kendra Intelligent Ranking 會使用此欄位為結果排名。`body_field` 為必要項目，而 `title_field` 為選用項目。
1. 選取 **Search**，並比較 **Result 1** 與 **Result 2** 中的結果。

<!-- vale off -->
### 使用 Amazon Personalize Search Ranking 個人化搜尋結果
<!-- vale on -->

另一個重新排名工具的範例是由 Amazon Personalize 團隊貢獻的 **Amazon Personalize Search Ranking**。Amazon Personalize 使用機器學習（ML）技術，為您的使用者產生客製化推薦。此外掛程式會取得 OpenSearch 搜尋結果，並套用[搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/)，根據其 Amazon Personalize 排名重新排名。Amazon Personalize 排名以使用者過往的行為，以及搜尋項目和使用者的中繼資料為依據。此工作流程透過個人化搜尋結果，改善使用者的搜尋體驗。

若要試用 Amazon Personalize Search Ranking，您必須先設定 Amazon Personalize。若要開始使用，請參閱 [Amazon Personalize](https://docs.aws.amazon.com/personalize/latest/dg/setup.html)。如需詳細資訊，包括外掛程式設定說明，請參閱[個人化 OpenSearch 的搜尋結果](https://docs.aws.amazon.com/personalize/latest/dg/personalize-opensearch.html)。
