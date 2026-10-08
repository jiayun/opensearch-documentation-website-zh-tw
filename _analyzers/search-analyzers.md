---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋分析器"
nav_order: 30
parent: Analyzers
---

# 搜尋分析器

搜尋分析器是在查詢時指定，當您對 [text]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 欄位執行全文查詢時，用於分析查詢字串。

## 決定要使用的搜尋分析器

為了決定在查詢時要對查詢字串使用哪個分析器，OpenSearch 會依序檢查下列參數：

1. 查詢的 `analyzer` 參數
1. 欄位的 `search_analyzer` 對應參數
1. `analysis.analyzer.default_search` 索引設定
1. 欄位的 `analyzer` 對應參數
1. `standard` 分析器（預設）

在大多數情況下，不需要指定與索引分析器不同的搜尋分析器，這麼做可能會對搜尋結果的相關性造成負面影響，或導致非預期的搜尋結果。
{: .warning}

## 在查詢時指定搜尋分析器

您可以在查詢中明確設定分析器，以覆寫預設的分析器行為。下列查詢使用 `english` 分析器對輸入詞彙進行詞幹提取：

```json
GET /shakespeare/_search
{
  "query": {
    "match": {
      "text_entry": {
        "query": "speak the truth",
        "analyzer": "english"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 在對應中指定搜尋分析器

定義對應時，您可以為任何 [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 欄位同時提供 `analyzer`（在編製索引時使用）和 `search_analyzer`（在查詢時使用）。

### 範例：編製索引和搜尋使用不同的分析器

下列組態允許編製索引和查詢時使用不同的斷詞策略：

```json
PUT /testindex
{
  "mappings": {
    "properties": {
      "text_entry": {
        "type": "text",
        "analyzer": "simple",
        "search_analyzer": "whitespace"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 範例：編製索引時使用 edge n-gram 分析器，搜尋時使用 standard 分析器

下列組態可實現類似[自動完成]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/autocomplete/)的行為，讓您輸入單字的開頭仍能取得相關的相符結果：

```json
PUT /articles
{
  "settings": {
    "analysis": {
      "analyzer": {
        "edge_ngram_analyzer": {
          "tokenizer": "edge_ngram_tokenizer",
          "filter": ["lowercase"]
        }
      },
      "tokenizer": {
        "edge_ngram_tokenizer": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 10,
          "token_chars": ["letter", "digit"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "edge_ngram_analyzer",
        "search_analyzer": "standard"
      }
    }
  }
}
```
{% include copy-curl.html %}

`edge_ngram_analyzer` 會在編製索引時套用，將輸入字串拆分為部分前綴（n-gram），讓索引能儲存「se」、「sea」、「sear」等片段。
使用下列請求將文件編製索引：

```json
PUT /articles/_doc/1
{
  "title": "Search Analyzer in Action"
}
```
{% include copy-curl.html %}

使用下列請求在 `title` 欄位中搜尋部分單字 `sear`：

```json
POST /articles/_search
{
  "query": {
    "match": {
      "title": "sear"
    }
  }
}
```
{% include copy-curl.html %}

回應顯示，包含「sear」的查詢與文件「Search Analyzer in Action」相符，因為編製索引時產生的 n-gram 詞元包含該前綴。這與[自動完成功能]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/autocomplete/)相同，輸入前綴即可擷取完整的相符結果：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.2876821,
    "hits": [
      {
        "_index": "articles",
        "_id": "1",
        "_score": 0.2876821,
        "_source": {
          "title": "Search Analyzer in Action"
        }
      }
    ]
  }
}
```

## 為索引設定預設搜尋分析器

指定 `analysis.analyzer.default_search`，為所有欄位定義搜尋分析器，除非另有覆寫：

```json
PUT /testindex
{
  "settings": {
    "analysis": {
      "analyzer": {
        "default": {
          "type": "simple"
        },
        "default_search": {
          "type": "whitespace"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

此組態可確保多個欄位之間的行為一致，尤其是在使用自訂分析器時。

如需有關支援的分析器的詳細資訊，請參閱[分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/index/)。
