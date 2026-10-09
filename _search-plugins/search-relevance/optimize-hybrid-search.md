---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "最佳化混合搜尋"
nav_order: 60
parent: Search Relevance Workbench
grand_parent: Optimizing search quality
has_children: false
---

# 最佳化混合搜尋

在 OpenSearch 中使用混合搜尋的一項關鍵挑戰，是如何有效地結合詞彙搜尋與向量搜尋的結果。OpenSearch 提供多種技術與各種參數，讓您可以實驗並找出最適合應用程式的組態。然而，什麼設定最有效，很大程度上取決於您的資料、使用者行為與應用程式領域——並沒有放諸四海皆準的解決方案。

Search Relevance Workbench 可協助您有系統地找出符合需求的理想參數組合。

## 需求

在內部，最佳化混合搜尋涉及執行多個搜尋品質評估實驗。進行這些實驗時，您需要一組查詢集、判斷結果與搜尋組態。
Search Relevance Workbench 支援混合搜尋最佳化，但僅限於恰好兩個查詢子句。雖然混合搜尋通常結合向量與詞彙查詢，您也可以使用兩個詞彙查詢子句執行混合搜尋最佳化：

```json
PUT _plugins/_search_relevance/search_configurations
{
  "name": "hybrid_query_lexical",
  "query": "{\"query\":{\"hybrid\":{\"queries\":[{\"match\":{\"title\":\"%SearchText%\"}},{\"match\":{\"category\":\"%SearchText%\"}}]}}}",
  "index": "ecommerce"
}
```
{% include copy-curl.html %}

混合搜尋最佳化在結合詞彙搜尋與向量搜尋結果時最有價值。為獲得最佳結果，請將混合搜尋查詢設定為兩個子句：一個文字查詢子句與一個 neural 查詢子句。您不需要設定搜尋管線來結合結果，因為混合搜尋最佳化程序會自動處理。以下是一個適合混合搜尋最佳化的搜尋組態範例：

```json
PUT _plugins/_search_relevance/search_configurations
{
  "name": "hybrid_query_text",
  "query": "{\"query\":{\"hybrid\":{\"queries\":[{\"multi_match\":{\"query\":\"%SearchText%\",\"fields\":[\"id\",\"title\",\"category\",\"bullets\",\"description\",\"attrs.Brand\\\",\"attrs.Color\"]}},{\"neural\":{\"title_embedding\":{\"query_text\":\"%SearchText%\",\"k\":100,\"model_id\":\"lRFFb5cBHkapxdNcFFkP\"}}}]}},\"size\":10}",
  "index": "ecommerce"
}
```
{% include copy-curl.html %}

`query` 中指定的模型 ID，必須是已在 OpenSearch 中部署之模型的有效模型 ID。目標索引必須包含用於神經搜尋嵌入的欄位（在本範例中為 `title_embedding`）。

如需端對端範例，請參閱 [`search-relevance` 儲存庫](https://github.com/opensearch-project/search-relevance)。

## 執行混合搜尋最佳化實驗

您可以透過呼叫 Search Relevance Workbench 的 `experiments` 端點來建立混合搜尋最佳化實驗。

### 端點

```json
PUT _plugins/_search_relevance/experiments
```

### 範例請求

```json
PUT _plugins/_search_relevance/experiments
{
  "querySetId": "b16a6a2b-ed6e-49af-bb2b-fc739dcf24e6",
  "searchConfigurationList": ["508a8812-27c9-45fc-999a-05f859f9b210"],
  "judgmentList": ["1b944d40-e95a-43f6-9e92-9ce00f70de79"],
  "size": 10,
  "type": "HYBRID_OPTIMIZER"
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "experiment_id": "0f4eff05-fd14-4e85-ab5e-e8e484cdac73",
  "experiment_result": "CREATED"
}
```

## 實驗流程

混合搜尋最佳化實驗會評估查詢集中每個查詢的下列參數變體的所有組合，並根據判斷清單為結果評分：

- 分數型變體：
  - 正規化技術：`l2`、`min_max` 與 `z_score`。由於 [正規化處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/#request-body-fields) 的限制，`z_score` 技術只能與 `arithmetic_mean` 結合使用。
  - 結合技術：`arithmetic_mean`、`harmonic_mean` 與 `geometric_mean`。
  - 詞彙與神經搜尋權重範圍從 `0.0` 到 `1.0`，以 `0.1` 為遞增單位。

- 排名型變體：
  - `rrf` ([Reciprocal Rank Fusion (RRF)]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/score-ranker-processor/)) 結合技術，使用 `rank_constant` 值 `1`、`5`、`10`、`20` 與 `60` 進行評估。RRF 變體在所有子查詢中使用相等權重。

## 評估結果

每次評估的結果都會儲存。您可以在 OpenSearch Dashboards 中，從過去實驗的概覽畫面選取對應的實驗來檢視結果，如下圖所示。

![比較搜尋結果]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/experiment_overview_hybrid_search_optimization.png)

畫面會顯示所有已執行的查詢及其計算出的搜尋指標，如下圖所示。

![比較搜尋結果]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/hybrid_search_optimization_query_overview.png)

若要檢視查詢變體，請選取其中一個查詢，如下圖所示。

![比較搜尋結果]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/hybrid_search_optimization_variant_parameters.png)

您也可以使用下列 SQL 搜尋陳述式並提供您的 `experimentId` 來擷取這項資訊：

```json
POST _plugins/_sql
{
  "query": "SELECT ev.parameters.normalization, ev.parameters.combination, ev.parameters.weights, ev.results.evaluationResultId, ev.experimentId, er.id, er.metrics, er.searchText FROM search-relevance-experiment-variant ev JOIN search-relevance-evaluation-result er ON ev.results.evaluationResultId = er.id WHERE ev.experimentId = '814e2378-901c-4273-9873-9b758a33089d'"
}
```
{% include copy-curl.html %}

若要以視覺化方式檢視這些結果，請參閱 [探索搜尋評估結果]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/explore-experiment-results/)。
