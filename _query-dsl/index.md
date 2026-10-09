---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Query DSL
nav_order: 2
has_children: true
nav_exclude: true
has_toc: false
permalink: /query-dsl/
redirect_from:
  - /opensearch/query-dsl/
  - /opensearch/query-dsl/index/
  - /docs/opensearch/query-dsl/
  - /query-dsl/query-dsl/
  - /query-dsl/index/
---

{%- comment -%}The `/docs/opensearch/query-dsl/` redirect is specifically to support the UI links in OpenSearch Dashboards 1.0.0.{%- endcomment -%}

# Query DSL

OpenSearch 提供一種稱為*查詢領域特定語言 (query DSL)* 的搜尋語言，您可以用它來搜尋資料。Query DSL 是一種具有 JSON 介面的彈性語言。

使用 query DSL 時，您需要在搜尋的 `query` 參數中指定查詢。OpenSearch 中最簡單的搜尋之一是 `match_all` 查詢，它會比對索引中的所有文件：

```json
GET testindex/_search
{
  "query": {
     "match_all": { 
     }
  }
}
```

一個查詢可以由多個查詢子句組成。您可以組合查詢子句來產生複雜的查詢。

大致上，您可以將查詢分為兩類——*葉查詢*與*複合查詢*：

- **葉查詢**：葉查詢會在某個或多個欄位中搜尋指定的值。您可以單獨使用葉查詢。葉查詢包含下列查詢類型：

    - [全文查詢]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/full-text/index/)：使用全文查詢來搜尋文字文件。對於經過分析的文字欄位搜尋，全文查詢會使用欄位編製索引時所用的同一個分析器，將查詢字串拆解成詞元。對於精確值搜尋，全文查詢會直接尋找指定的值，不套用文字分析。

    - [詞彙層級查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/index/)：使用詞彙層級查詢來搜尋文件中的精確詞彙，例如 ID 或值的範圍。詞彙層級查詢不會分析搜尋詞彙，也不會依相關性分數排序結果。

    - [地理與 xy 查詢]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/geo-and-xy/index/)：使用地理查詢來搜尋包含地理資料的文件。使用 xy 查詢來搜尋包含二維座標系統中點與形狀的文件。

    - [連接查詢]({{site.url}}{{site.baseurl}}/query-dsl/joining/)：使用連接查詢來搜尋巢狀欄位，或傳回符合特定查詢的父文件與子文件。連接查詢的類型包括 `nested`、`has_child`、`has_parent` 與 `parent_id` 查詢。

    - [Span 查詢]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/span-query/)：使用 span 查詢來執行精確的位置搜尋。Span 查詢是低階的特定查詢，可控制指定查詢詞彙的順序與鄰近度。它們主要用於搜尋法律文件。

    - [特殊查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/index/)：特殊查詢包含所有其他查詢類型（`distance_feature`、`more_like_this`、`percolate`、`rank_feature`、`script`、`script_score` 與 `wrapper`）。

- **複合查詢**：複合查詢可作為多個葉子句或複合子句的外層包裝，用來合併它們的結果或修改它們的行為。複合查詢包含 Boolean、disjunction max、constant score、function score 與 boosting 查詢類型。若要了解更多，請參閱[複合查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/index/)。

## 關於文字欄位中 Unicode 特殊字元的注意事項

由於 Unicode 特殊字元具有字詞邊界的特性，當 [text 欄位類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/text/)的值包含這些特殊字元之一時，Unicode 標準分析器無法將其視為整體值來編製索引。因此，包含特殊字元的 text 欄位值會被標準分析器解析成以該特殊字元分隔的多個值，實際上等於將特殊字元兩側的不同元素斷詞。這可能導致文件被意外篩除，並可能危害其存取控制。

下列範例說明會被標準分析器錯誤解析的包含特殊字元的值。在此範例中，值中的連字號/減號使分析器無法區分 `user.id` 的兩個不同使用者，而將它們解讀為同一個使用者：

```json
{
  "bool": {
    "must": {
      "match": {
        "user.id": "User-1"
      }
    }
  }
}
```

```json
{
  "bool": {
    "must": {
      "match": {
        "user.id": "User-2"
      }
    }
  }
}
```

若要在使用 Query DSL 或 REST API 時避免這種情況，您可以使用自訂分析器，或將該欄位對應為 `keyword`，以執行精確比對搜尋。後一種選項請參閱 [Keyword 欄位類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/keyword/)。

有關使用 `text` 欄位類型時應避免的字元清單，請參閱 [字詞邊界](https://unicode.org/reports/tr29/#Word_Boundaries)。

## 昂貴的查詢

昂貴的查詢可能消耗大量記憶體，並導致叢集效能下降。下列查詢可能會消耗大量資源：

- [`fuzzy`]({{site.url}}{{site.baseurl}}/query-dsl/term/fuzzy/) 查詢
- [`prefix`]({{site.url}}{{site.baseurl}}/query-dsl/term/prefix/) 查詢
- 針對 [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 與 [`keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/keyword/) 欄位的 [`range`]({{site.url}}{{site.baseurl}}/query-dsl/term/range/) 查詢
- [`regexp`]({{site.url}}{{site.baseurl}}/query-dsl/term/regexp/) 查詢
- [`wildcard`]({{site.url}}{{site.baseurl}}/query-dsl/term/wildcard/) 查詢
- 內部被轉換為前綴查詢的 [`query_string`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/) 查詢
- 在以前綴樹儲存形狀的 geoshape 欄位上的 [`geo_shape`]({{site.url}}{{site.baseurl}}/query-dsl/geo-and-xy/geoshape/) 查詢

若要禁止昂貴的查詢，您可以如下停用 `search.allow_expensive_queries` 叢集設定：

```json
PUT _cluster/settings
{
  "persistent": {
    "search.allow_expensive_queries": false
  }
}
```
{% include copy-curl.html %}

若要追蹤昂貴的查詢，請啟用 [分片慢速記錄檔]({{site.url}}{{site.baseurl}}/monitoring-your-cluster/logs/#shard-slow-logs)。
{: .tip}