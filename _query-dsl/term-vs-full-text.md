---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "詞彙層級查詢與全文查詢的比較"
nav_order: 10
redirect_from:
  - /query-dsl/query-dsl/term-vs-full-text/
  - /opensearch/query-dsl/term-vs-full-text/
---

# 詞彙層級查詢與全文查詢的比較

您可以使用詞彙層級查詢和全文查詢來搜尋文字，但詞彙層級查詢通常用於搜尋結構化資料，而全文查詢則用於全文搜尋。詞彙層級查詢與全文查詢的主要差異在於，詞彙層級查詢會在文件中搜尋完全相符的指定詞彙，而全文查詢則會[分析]({{site.url}}{{site.baseurl}}/analyzers/)查詢字串。下表摘要說明詞彙層級查詢與全文查詢之間的差異。

| | 詞彙層級查詢 | 全文查詢
:--- | :--- | :---
*說明* | 詞彙層級查詢回答哪些文件符合查詢。 | 全文查詢回答文件與查詢的相符程度。
*分析器* | 搜尋詞彙不會經過分析。這表示詞彙查詢會依搜尋詞彙的原樣進行搜尋。  | 搜尋詞彙會由該特定文件欄位在編製索引時所使用的相同分析器進行分析。這表示您的搜尋詞彙會經歷與文件欄位相同的分析流程。
*相關性* | 詞彙層級查詢會傳回相符的文件，而不會根據相關性分數加以排序。它們仍會計算相關性分數，但此分數對所有傳回的文件都相同。 | 全文查詢會為每個相符項目計算相關性分數，並依相關性遞減的順序排序結果。
*使用案例* | 當您想要比對數字、日期或標籤等確切值，且不需要依相關性排序相符項目時，請使用詞彙層級查詢。 | 當您要比對文字欄位，並在考量大小寫與詞幹變化等因素後依相關性排序時，請使用全文查詢。

OpenSearch 使用 BM25 排名演算法來計算相關性分數。若要深入瞭解，請參閱 [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25)。
{: .note }

## 我應該使用全文查詢還是詞彙層級查詢

為了釐清全文查詢與詞彙層級查詢之間的差異，請考量下列兩個搜尋特定文字詞組的範例。莎士比亞全集已編製索引至 OpenSearch 叢集中。

### 範例：詞組搜尋

在此範例中，您將在 `text_entry` 欄位中，於莎士比亞全集中搜尋「To be, or not to be」這個詞組。 

首先，使用**詞彙層級查詢**進行此搜尋：

```json
GET shakespeare/_search
{
  "query": {
    "term": {
      "text_entry": "To be, or not to be"
    }
  }
}
```

回應中沒有任何相符項目，由零個 `hits` 表示：

```json
{
  "took" : 3,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 0,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  }
}
```

這是因為「To be, or not to be」這個詞彙會在反向索引中以字面方式搜尋，而反向索引中只會儲存文字欄位經過分析的值。詞彙層級查詢不適合用來搜尋經過分析的文字欄位，因為它們經常產生非預期的結果。處理文字資料時，請僅針對對應為 `keyword` 的欄位使用詞彙層級查詢。

現在使用**全文查詢**搜尋相同的詞組：

```json
GET shakespeare/_search
{
  "query": {
    "match": {
      "text_entry": "To be, or not to be"
    }
  }
}
```

搜尋查詢「To be, or not to be」會經過分析並斷詞為詞元陣列，與文件的 `text_entry` 欄位相同。全文查詢會對所有文件取得搜尋查詢與 `text_entry` 欄位之間詞元的交集，然後依相關性分數排序結果：

```json
{
  "took" : 19,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10000,
      "relation" : "gte"
    },
    "max_score" : 17.419369,
    "hits" : [
      {
        "_index" : "shakespeare",
        "_id" : "34229",
        "_score" : 17.419369,
        "_source" : {
          "type" : "line",
          "line_id" : 34230,
          "play_name" : "Hamlet",
          "speech_number" : 19,
          "line_number" : "3.1.64",
          "speaker" : "HAMLET",
          "text_entry" : "To be, or not to be: that is the question:"
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "109930",
        "_score" : 14.883024,
        "_source" : {
          "type" : "line",
          "line_id" : 109931,
          "play_name" : "A Winters Tale",
          "speech_number" : 23,
          "line_number" : "4.4.153",
          "speaker" : "PERDITA",
          "text_entry" : "Not like a corse; or if, not to be buried,"
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "103117",
        "_score" : 14.782743,
        "_source" : {
          "type" : "line",
          "line_id" : 103118,
          "play_name" : "Twelfth Night",
          "speech_number" : 53,
          "line_number" : "1.3.95",
          "speaker" : "SIR ANDREW",
          "text_entry" : "will not be seen; or if she be, its four to one"
        }
      }
    ]
  }
}
...
```

如需所有全文查詢的清單，請參閱[全文查詢]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/full-text/index/)。

### 範例：確切詞彙搜尋

如果您想要在 `speaker` 欄位中搜尋「HAMLET」這類確切詞彙，且不需要依相關性分數排序結果，則詞彙層級查詢更有效率：

```json
GET shakespeare/_search
{
  "query": {
    "term": {
      "speaker": "HAMLET"
    }
  }
}
```

回應中包含相符的文件：

```json
{
  "took" : 5,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1582,
      "relation" : "eq"
    },
    "max_score" : 4.2540946,
    "hits" : [
      {
        "_index" : "shakespeare",
        "_id" : "32700",
        "_score" : 4.2540946,
        "_source" : {
          "type" : "line",
          "line_id" : 32701,
          "play_name" : "Hamlet",
          "speech_number" : 9,
          "line_number" : "1.2.66",
          "speaker" : "HAMLET",
          "text_entry" : "[Aside]  A little more than kin, and less than kind."
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "32702",
        "_score" : 4.2540946,
        "_source" : {
          "type" : "line",
          "line_id" : 32703,
          "play_name" : "Hamlet",
          "speech_number" : 11,
          "line_number" : "1.2.68",
          "speaker" : "HAMLET",
          "text_entry" : "Not so, my lord; I am too much i' the sun."
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "32709",
        "_score" : 4.2540946,
        "_source" : {
          "type" : "line",
          "line_id" : 32710,
          "play_name" : "Hamlet",
          "speech_number" : 13,
          "line_number" : "1.2.75",
          "speaker" : "HAMLET",
          "text_entry" : "Ay, madam, it is common."
        }
      }
    ]
  }
}
...
```

詞彙層級查詢提供確切的相符項目。因此，如果您搜尋「Hamlet」，不會取得任何相符項目，因為「HAMLET」是 keyword 欄位，會以字面方式儲存在 OpenSearch 中，而非以經過分析的形式儲存。
搜尋查詢「HAMLET」也會以字面方式搜尋。因此，若要讓此欄位相符，我們需要輸入完全相同的字元。
