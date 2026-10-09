---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分數排名器"
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
nav_order: 117
---

# 分數排名器處理器
於 2.19 版推出
{: .label .label-purple }

`score-ranker-processor` 是以排名為基礎的搜尋階段結果處理器，會在搜尋執行的查詢階段與擷取階段之間執行。它會攔截查詢階段的結果，然後使用倒數排名融合 (RRF) 演算法，將 [`hybrid` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/hybrid/) 的查詢子句合併成最終的搜尋結果排名清單。RRF 會依據每份文件在各查詢子句結果中的排名倒數來為其評分，然後將這些分數相加，因此個別查詢子句的相關性分數永遠不需要位於可比較的尺度上。如需更多資訊，請參閱[倒數排名融合]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/rrf/)。

## 請求本文欄位

下表列出所有可用的請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`combination.technique` | 字串 | 用於合併分數的技術。有效值為 `rrf`。選用。預設為 `rrf`。
`combination.rank_constant` | 整數 | 在計算倒數分數之前，加到每份文件排名上的常數。有效值位於 [1, 10000] 範圍內。較大的排名常數會讓分數更為一致，降低排名最高結果的影響力。較小的排名常數會讓各排名之間的分數差距更大，使排名最高的項目獲得更高的權重。選用。預設為 `60`。
`combination.parameters.weights` | 浮點數值陣列 | 指定要用於每個查詢子句的權重。有效值位於 [0.0, 1.0] 範圍內，代表十進位百分比。權重越接近 1.0，賦予該查詢子句的權重就越高。`weights` 陣列中的值數量必須等於查詢子句的數量。陣列中的值總和必須等於 1.0。選用。若未提供，則所有查詢子句會獲得相同的權重。

## 範例

下列請求會建立一個搜尋管線，其中包含使用 `rrf` 合併技術且排名常數為預設值 `60` 的 `score-ranker-processor`：

```json
PUT /_search/pipeline/rrf-pipeline
{
  "description": "Post processor for hybrid RRF search",
  "phase_results_processors": [
    {
      "score-ranker-processor": {
        "combination": {
          "technique": "rrf"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

下列請求會將 `rank_constant` 設為 `40`，並為每個查詢子句套用自訂權重。查詢子句 1 的權重為 0.7，查詢子句 2 的權重為 0.3：

```json
PUT /_search/pipeline/rrf-pipeline
{
  "description": "Post processor for hybrid RRF search",
  "phase_results_processors": [
    {
      "score-ranker-processor": {
        "combination": {
          "technique": "rrf",
          "rank_constant": 40,
          "parameters": {
            "weights": [
              0.7,
              0.3
            ]
          }
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

若要使用此管線，請在包含 `hybrid` 查詢的搜尋請求中指定它：

```json
GET /my-nlp-index/_search?search_pipeline=rrf-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "passage_text": "running shoes"
          }
        },
        {
          "neural": {
            "passage_embedding": {
              "query_text": "running shoes",
              "model_id": "aVeif4oB5Vm0Tdw8zYO2",
              "k": 5
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

## 相關文件

- [倒數排名融合]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/rrf/)
- [混合搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/)
- [正規化處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/)
