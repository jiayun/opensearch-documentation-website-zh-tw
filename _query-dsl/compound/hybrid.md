---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "混合"
parent: Compound queries
nav_order: 70
---

# 混合查詢

您可以使用混合查詢，將多個查詢的相關性分數合併為指定文件的一個分數。混合查詢包含一或多個查詢的清單，並在分片層級為每個子查詢個別計算文件分數。子查詢改寫會在協調節點層級執行，以避免重複計算。

## 範例

請依照[混合搜尋]({{site.url}}{{site.baseurl}}/search-plugins/hybrid-search/)中的步驟，了解如何使用 `hybrid` 查詢。

如需完整的範例，請參閱[語意與混合搜尋入門]({{site.url}}{{site.baseurl}}/ml-commons-plugin/semantic-search#tutorial)。

## 參數

下表列出 `hybrid` 查詢支援的所有最上層參數。

參數 | 說明
:--- | :---
`queries` | 用於比對文件的一或多個查詢子句陣列。文件必須至少符合一個查詢子句，才會出現在結果中。所有查詢子句的文件相關性分數會套用[搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/)合併為一個分數。查詢子句的數量上限為 5。必要。
`filter` | 套用至混合查詢所有子查詢的篩選條件。此篩選條件必須是單一查詢物件。若要套用多個篩選條件，請將它們合併在[布林查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/)中。如需詳細資訊，請參閱[使用預先篩選的混合搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/pre-filtering/)。
`pagination_depth` | 每個子查詢從每個分片傳回的搜尋結果數量上限。這會限制搜尋管線正規化與合併的文件集合，因此會同時影響您可以分頁的深度以及產生的排序。有效值為從 `1` 到 [`index.max_result_window`]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/) 值的整數（預設為 10000）。若 `from` 大於 `0` 則為必要，否則為選用。若未提供，每個子查詢會從每個分片傳回最多 `size` 筆結果。如需詳細資訊，請參閱[混合查詢結果分頁]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/pagination/)。

### 重新評分混合查詢
於 2.18 版推出
{: .label .label-purple }

您可以在混合查詢中使用 [`rescore`]({{site.url}}{{site.baseurl}}/query-dsl/rescore/) 參數。不過，重新評分在混合查詢中的行為與標準查詢不同。

在標準查詢中，重新評分會在合併所有分片的結果之後，套用於**協調節點**。在混合查詢中，重新評分會在正規化與合併管線執行之前，**個別**套用於**分片層級**的每個子查詢結果。

使用重新評分的混合查詢，其處理順序如下：

1. 混合查詢中的每個子查詢會在分片上執行，產生各自的結果集。
2. 重新評分查詢會個別套用於每個子查詢的結果。
3. 重新評分後的結果會傳送至協調節點。
4. 搜尋管線（正規化處理器或分數排名處理器）會正規化並合併重新評分後的子查詢分數。

在混合查詢中使用重新評分時，請注意下列事項：

- `window_size` 會個別套用於每個子查詢的結果，而非套用於合併後的結果。
- 您無法將明確排序與重新評分搭配使用。若您嘗試在混合搜尋中將排序與重新評分查詢合併使用，OpenSearch 會傳回錯誤。
- 重新評分與[正規化處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/)和[分數排名處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/score-ranker-processor/)支援的所有分數式與排名式正規化及合併技術相容。

下列範例使用 `match_phrase` 重新評分查詢，在結合兩個欄位關鍵字比對的混合搜尋中，提升包含確切詞組「search engine」的文件：

```json
POST /my-index/_search?search_pipeline=nlp-search-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "title": "search engine"
          }
        },
        {
          "match": {
            "description": "search engine"
          }
        }
      ]
    }
  },
  "rescore": {
    "window_size": 50,
    "query": {
      "rescore_query": {
        "match_phrase": {
          "title": {
            "query": "search engine",
            "slop": 2
          }
        }
      },
      "query_weight": 0.7,
      "rescore_query_weight": 1.2
    }
  }
}
```
{% include copy-curl.html %}

回應包含的文件，其分數同時反映初始混合查詢比對與重新評分提升：

```json
{
  "took": 30,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 0.95,
    "hits": [
      {
        "_index": "my-index",
        "_id": "1",
        "_score": 0.95,
        "_source": {
          "title": "Building a search engine",
          "description": "A guide to modern search engine architecture"
        }
      },
      {
        "_index": "my-index",
        "_id": "2",
        "_score": 0.67,
        "_source": {
          "title": "Introduction to search",
          "description": "Learn about search engine basics"
        }
      },
      {
        "_index": "my-index",
        "_id": "3",
        "_score": 0.42,
        "_source": {
          "title": "Database engine tuning",
          "description": "How to optimize your search queries"
        }
      }
    ]
  }
}
```

在此範例中，文件 1 排名最高，因為重新評分 `match_phrase` 查詢提升了它的分數（其 `title` 欄位包含確切詞組「search engine」）。文件 2 僅在 `description` 欄位中包含該詞組，因此從 `title` 的詞組比對獲得較低的提升。文件 3 在不同欄位中符合個別詞彙「search」和「engine」，但並非確切詞組，因此獲得最小的提升。由於重新評分查詢會在正規化之前，於分片層級個別套用於每個子查詢的結果，詞組提升會影響最終合併的分數。

<!-- vale off -->
### 混合查詢的 min_score 支援
<!-- vale on -->

從 OpenSearch 3.5 開始，[`min_score`]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#request-body) 參數會在分數正規化與合併之後套用。它只能在依 `_score` 排序或未指定明確排序順序時使用。若將 `min_score` 與任何其他排序準則搭配使用，請求會導致錯誤。
{: .note}

從 OpenSearch 3.5 開始，您可以在具有超過 512 個分片的索引上使用混合查詢。OpenSearch 會自動停用批次縮減，以確保所有分片的分數正規化正確。不需要任何組態。請注意，對於分片數量龐大的索引，協調節點的記憶體使用量可能會較高。`_msearch` 端點不支援批次縮減的自動處理。若要在許多分片上使用混合查詢進行多重搜尋請求，請改用搭配索引模式或別名的 `_search` 端點。
{: .note}

## 限制

混合查詢的設計是在搜尋請求中作為最上層查詢。它無法巢狀於其他複合或包裝查詢中，例如 `function_score`、`constant_score`、`script_score` 或 `boosting`。此限制也適用於多層巢狀，例如包含 `function_score` 查詢的 `bool` 查詢，而該查詢本身又包含 `hybrid` 查詢。將混合查詢巢狀於這些包裝查詢中，可能會產生執行階段錯誤，或無聲地略過正規化管線。

混合查詢使用特殊的評分機制，與包裝查詢不相容。包裝查詢使用不同的內部評分器，會略過混合查詢的個別子查詢分數收集，而這是正規化與合併管線正確運作所必需的。

若要將分數提升函式套用至混合搜尋結果，請將 `hybrid` 查詢取代為 `bool` 查詢，並將您的子查詢移入 `should` 子句。此替代做法適用於所有支援混合查詢的 OpenSearch 版本。

例如，下列查詢不受支援：

```json
GET /my-index/_search?search_pipeline=my-pipeline
{
  "query": {
    "function_score": {
      "query": {
        "hybrid": {
          "queries": [
            {"match": {"title": "search terms"}},
            {"term": {"category": "books"}}
          ]
        }
      },
      "functions": [{"field_value_factor": {"field": "popularity"}}]
    }
  }
}
```

請改用下列等效查詢：

```json
GET /my-index/_search
{
  "query": {
    "function_score": {
      "query": {
        "bool": {
          "should": [
            {"match": {"title": "search terms"}},
            {"term": {"category": "books"}}
          ]
        }
      },
      "functions": [{"field_value_factor": {"field": "popularity"}}]
    }
  }
}
```
{% include copy-curl.html %}

當使用包含 `should` 子句的 `bool` 查詢，而非 `hybrid` 查詢時，不會套用搜尋管線的正規化與合併處理器。而是使用標準布林評分（符合子句的總和）來合併子查詢的分數。接著會將 `function_score` 函式套用至合併後的分數。
{: .note}

## 停用混合查詢

混合查詢預設為啟用。若要在您的叢集中停用混合查詢，請在 `opensearch.yml` 中將 `plugins.neural_search.hybrid_search_disabled` 設定設為 `true`。
