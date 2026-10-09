---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Search Relevance Workbench
nav_order: 20
parent: Optimizing search quality
has_children: true
---

# Search Relevance Workbench
3.1 版引進
{: .label .label-purple }

在搜尋應用程式中，調校相關性是一項持續且反覆進行的工作，目的是為終端使用者提供正確的搜尋結果。Search Relevance Workbench 中的工具可協助搜尋相關性工程師與業務使用者為應用程式使用者打造最佳的搜尋體驗。它不會隱藏內部資訊，讓工程師能夠視需要進行實驗並調查細節。

Search Relevance Workbench 包含一個[前端元件](https://github.com/opensearch-project/dashboards-search-relevance)，可簡化評估搜尋品質的流程。
該前端使用 [OpenSearch Search Relevance 外掛程式](https://github.com/opensearch-project/search-relevance)作為後端，以管理每個工具的資源。例如，大多數使用情境都涉及建立與使用搜尋組態、查詢集和判斷清單。這些資源全部都由 Search Relevance 外掛程式建立、更新、刪除與維護。當您對相關性改善感到滿意時，可以將實驗的輸出手動部署到您的搜尋應用程式中。

在進行更結構化的實驗之前，您可以使用[單一查詢比較 UI]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/compare-search-results/) 快速分析單一查詢。

## 關鍵相關性概念

Search Relevance Workbench 針對它所提供的不同實驗類型，依賴不同的元件：

* [查詢集]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/query-sets/)：_查詢集_ 是查詢的集合。這些查詢會在實驗中用於搜尋相關性評估。
* [搜尋組態]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/search-configurations/)：_搜尋組態_ 描述實驗中執行查詢時所使用的模式。
* [判斷清單]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/judgments/)：_判斷_ 是一種評分，描述某個特定文件對於指定查詢的相關性。多個判斷會被歸組成判斷清單。
* [實驗]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/experiments/)：_實驗_ 是一種受控測試，旨在評估演算法的有效性。系統提供多種實驗類型。

## 可用的搜尋結果品質實驗

Search Relevance Workbench 提供三種實驗類型：

* [搜尋結果比較]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/comparing-search-results/)：比較兩個搜尋組態的結果。
* [搜尋品質評估]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/evaluate-search-quality/)：根據擷取的結果與判斷清單計算搜尋品質指標，以評估某個特定搜尋組態的擷取品質。
* [混合搜尋最佳化]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/optimize-hybrid-search/)：為您的混合搜尋查詢找出最佳參數組合。

## 建立查詢集

若要比較搜尋組態，請建立一組查詢來執行搜尋。如果您有權存取符合 User Behavior Insights (UBI) 規格的搜尋行為資料，可以傳送請求至 `_plugins/search_relevance/query_sets/create` 端點。

以下範例請求會將手動定義的查詢集上傳至 Search Relevance Workbench：


```json
PUT _plugins/_search_relevance/query_sets
{
  "name": "TVs",
  "description": "TV queries",
  "sampling": "manual",
  "querySetQueries": [
    {
      "queryText": "tv"
    },
    {
      "queryText": "led tv"
    }
  ]
}
```
{% include copy-curl.html %}


回應包含您要用於實驗的查詢集 `query_set_id`：

```json
{
  "query_set_id": "1856093f-9245-449c-b54d-9aae7650551a",
  "query_set_result": "CREATED"
}
```

## 建立搜尋組態

搜尋組態會指定查詢集中的每個查詢如何執行。若要建立搜尋組態，您可以傳送搜尋請求至 `_plugins/search_relevance/search_configurations` 端點。
每個搜尋組態都包含一個 `search_configuration_name` 和一個 `query_body`。

### 範例：建立兩個搜尋組態

在您的第一個實驗中，您將探索為 `title` 欄位新增權重 `10` 會如何影響您的搜尋組態。首先，將您目前的搜尋組態上傳至 OpenSearch：

```json
PUT _plugins/_search_relevance/search_configurations
{
  "name": "my_production_config",
  "query": "{\"query\":{\"multi_match\":{\"query\":\"%SearchText%\",\"fields\":[\"id\",\"title\",\"category\",\"bullets\",\"description\",\"attrs.Brand\",\"attrs.Color\"]}}}",
  "index": "ecommerce"
}
```
{% include copy-curl.html %}

回應包含搜尋組態 ID：

```json
{
  "search_configuration_id": "122fbde8-d593-4d71-96d4-cbe3b4977468",
  "search_configuration_result": "CREATED"
}
```

接著，建立另一個搜尋組態，並為 `title` 欄位套用權重 `10`：

```json
PUT _plugins/_search_relevance/search_configurations
{
  "name": "title_boost",
  "query": "{\"query\":{\"multi_match\":{\"query\":\"%SearchText%\",\"fields\":[\"id\",\"title^10\",\"category\",\"bullets\",\"description\",\"attrs.Brand\",\"attrs.Color\"]}}}",
  "index": "ecommerce"
}
```
{% include copy-curl.html %}

回應包含已調升權重之搜尋組態的 ID，並指出是否成功建立：

```json
{
  "search_configuration_id": "0d687614-df5b-4b6b-8110-9d8c6d407963",
  "search_configuration_result": "CREATED"
}
```

## 執行搜尋結果清單比較實驗

若要執行您的第一個實驗，您需要一個查詢集和兩個搜尋組態（以及對應的索引）。透過比較搜尋結果，您可以評估修改搜尋組態對搜尋結果的影響。若要建立實驗，請傳送請求至 `_plugins/search_relevance/experiments` 端點：


```json
PUT _plugins/_search_relevance/experiments
{
 "querySetId": "1856093f-9245-449c-b54d-9aae7650551a",
 "searchConfigurationList": ["122fbde8-d593-4d71-96d4-cbe3b4977468", "0d687614-df5b-4b6b-8110-9d8c6d407963"],
 "size": 10,
 "type": "PAIRWISE_COMPARISON"
}
```
{% include copy-curl.html %}

回應包含實驗 ID：

```json
{
  "experiment_id": "dbae9786-6ea0-413d-a500-a14ef69ef7e1",
  "experiment_result": "CREATED"
}
```

若要擷取實驗結果，請使用傳回的 `experiment_id`：

```json
GET _plugins/_search_relevance/experiments/dbae9786-6ea0-413d-a500-a14ef69ef7e1
```
{% include copy-curl.html %}

回應會提供詳細的實驗結果：

<details open markdown="block">
<summary>
    回應
</summary>

```json
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": ".plugins-search-relevance-experiment",
        "_id": "dbae9786-6ea0-413d-a500-a14ef69ef7e1",
        "_score": 1,
        "_source": {
          "id": "dbae9786-6ea0-413d-a500-a14ef69ef7e1",
          "timestamp": "2025-06-14T14:02:17.347Z",
          "type": "PAIRWISE_COMPARISON",
          "status": "COMPLETED",
          "querySetId": "1856093f-9245-449c-b54d-9aae7650551a",
          "searchConfigurationList": [
            "122fbde8-d593-4d71-96d4-cbe3b4977468",
            "0d687614-df5b-4b6b-8110-9d8c6d407963"
          ],
          "judgmentList": [],
          "size": 10,
          "results": [
            {
              "snapshots": [
                {
                  "searchConfigurationId": "0d687614-df5b-4b6b-8110-9d8c6d407963",
                  "docIds": [
                    "B01M1D0KL1",
                    "B07YSMD3Z9",
                    "B07V4CY9GZ",
                    "B074KFP426",
                    "B07S8XNWWF",
                    "B07XBJR7GY",
                    "B075FDWSHT",
                    "B01N2Z17MS",
                    "B07F1T4JFB",
                    "B07S658ZLH"
                  ]
                },
                {
                  "searchConfigurationId": "122fbde8-d593-4d71-96d4-cbe3b4977468",
                  "docIds": [
                    "B07Q45SP9P",
                    "B074KFP426",
                    "B07JKVKZX8",
                    "B07THVCJK3",
                    "B0874XJYW8",
                    "B08LVPWQQP",
                    "B07V4CY9GZ",
                    "B07X3BS3DF",
                    "B074PDYLCZ",
                    "B08CD9MKLZ"
                  ]
                }
              ],
              "queryText": "led tv",
              "metrics": [
                {
                  "metric": "jaccard",
                  "value": 0.11
                },
                {
                  "metric": "rbo50",
                  "value": 0.03
                },
                {
                  "metric": "rbo90",
                  "value": 0.13
                },
                {
                  "metric": "frequencyWeighted",
                  "value": 0.2
                }
              ]
            },
            {
              "snapshots": [
                {
                  "searchConfigurationId": "0d687614-df5b-4b6b-8110-9d8c6d407963",
                  "docIds": [
                    "B07X3S9RTZ",
                    "B07WVZFKLQ",
                    "B00GXD4NWE",
                    "B07ZKCV5K5",
                    "B07ZKDVHFB",
                    "B086VKT9R8",
                    "B08XLM8YK1",
                    "B07FPP6TB5",
                    "B07N1TMNHB",
                    "B09CDHM8W7"
                  ]
                },
                {
                  "searchConfigurationId": "122fbde8-d593-4d71-96d4-cbe3b4977468",
                  "docIds": [
                    "B07Q7VGW4Q",
                    "B00GXD4NWE",
                    "B07VML1CY1",
                    "B07THVCJK3",
                    "B07RKSV7SW",
                    "B010EAW8UK",
                    "B07FPP6TB5",
                    "B073G9ZD33",
                    "B07VXRXRJX",
                    "B07Q45SP9P"
                  ]
                }
              ],
              "queryText": "tv",
              "metrics": [
                {
                  "metric": "jaccard",
                  "value": 0.11
                },
                {
                  "metric": "rbo50",
                  "value": 0.07
                },
                {
                  "metric": "rbo90",
                  "value": 0.16
                },
                {
                  "metric": "frequencyWeighted",
                  "value": 0.2
                }
              ]
            }
          ]
        }
      }
    ]
  }
}
```

</details>

## 在 OpenSearch Dashboards 中使用 Search Relevance Workbench

您可以在 OpenSearch Dashboards 中建立所有 Search Relevance Workbench 元件，並將實驗結果視覺化。
在此範例中，您將建立相同的實驗並檢閱其結果。

在左側導覽窗格中，選取 **OpenSearch Plugins** > **Search Relevance**，然後選取 **Query Set Comparison**，如下圖所示。

![選取 Query Set Comparison 實驗]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/select_query_set_comparison.png)

選取您建立的查詢集 (`TVs`) 以及搜尋組態 (`my_production_config`、`title_boost`)，然後選取 **Start Evaluation**，如下圖所示。

![定義 Query Set Comparison 實驗]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/query_set_comparison_experiment_definition.png)

系統會自動將您導向實驗總覽表格，如下圖所示。

![實驗總覽表格]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/experiment_table_overview.png)

若要檢閱結果，請選取最上方 (最近) 的實驗。實驗檢視頁面會顯示三個元素：
1. 實驗參數。
2. 實驗產生的彙總指標，如下圖所示。
![比較實驗的彙總指標]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/aggregate_metrics_comparison_experiment.png)
3. 每個查詢的個別指標。

若要視覺化評估兩個結果集之間的差異，請選取查詢事件。
