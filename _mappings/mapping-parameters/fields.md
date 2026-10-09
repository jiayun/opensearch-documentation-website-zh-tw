---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "欄位"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/fields/
nav_order: 100
has_children: false
has_toc: false
---

# fields 對應參數

`fields` 對應參數可讓您透過定義額外的子欄位，以多種方式為同一個欄位編製索引。透過多欄位 (multi-fields)，主要欄位的值會依其主要對應方式儲存。此外，您可以為一或多個子欄位設定替代對應，例如不同的資料類型或分析器，以支援各種搜尋與彙總需求。

當您需要對資料的一種表示方式執行全文搜尋，並對另一種表示方式執行精確比對操作 (例如排序或彙總) 時，多欄位特別有用。此外，您可以使用不同的分析器為同一個欄位編製索引。例如，一個子欄位可能使用預設分析器進行一般文字搜尋，而另一個子欄位則使用自訂分析器產生 n-gram，以支援自動完成或模糊比對。

## 設定多欄位

在下列範例中，建立了一個名為 `articles` 的索引，其中包含一個以全文方式分析的 `title` 欄位。在 `fields` 之下定義了一個名為 `raw` 的子欄位，將相同的值儲存為 `keyword`，以進行精確比對查詢：

```json
PUT /articles
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "fields": {
          "raw": {
            "type": "keyword"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 使用不同的分析器

在下列範例中，同一個 `title` 欄位使用兩種不同的分析器編製索引。主要欄位使用預設分析器進行全文搜尋，而 `ngrams` 子欄位則使用自訂的 n-gram 分析器，以支援自動完成等功能：

```json
PUT /articles
{
  "settings": {
    "analysis": {
      "analyzer": {
        "ngram_analyzer": {
          "tokenizer": "ngram_tokenizer",
          "filter": [
            "lowercase"
          ]
        }
      },
      "tokenizer": {
        "ngram_tokenizer": {
          "type": "ngram",
          "min_gram": 3,
          "max_gram": 4,
          "token_chars": [
            "letter",
            "digit"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "fields": {
          "raw": {
            "type": "keyword"
          },
          "ngrams": {
            "type": "text",
            "analyzer": "ngram_analyzer"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 為文件編製索引

建立索引之後，您可以在其中為文件編製索引。`title` 欄位會依其對應定義的方式處理，其子欄位則會提供相同值的替代表示方式：

```json
PUT /articles/_doc/1
{
  "title": "Understanding Multi-Fields in Search"
}
```
{% include copy-curl.html %}

## 查詢多欄位

您可以在查詢中指定額外的子欄位，以符合不同的需求。例如，若要對 title 的精確值執行彙總，請使用下列請求查詢 `title.raw` 子欄位：

```json
POST /articles/_search
{
  "size": 0,
  "aggs": {
    "titles": {
      "terms": {
        "field": "title.raw"
      }
    }
  }
}
```
{% include copy-curl.html %}

`title.raw` 子欄位對應為 `keyword`，即使原始 title 欄位是以全文方式分析，仍可執行精確比對彙總：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "titles": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "Understanding Multi-Fields in Search",
          "doc_count": 1
        }
      ]
    }
  }
}
```

或者，若要使用自動完成功能，您可以對 `title.ngrams` 子欄位執行 `match` 查詢：

```json
POST /articles/_search
{
  "query": {
    "match": {
      "title.ngrams": "Und"
    }
  }
}
```
{% include copy-curl.html %}

`title.ngrams` 子欄位使用自訂的 n-gram 分析器，因此前綴 `Und` 可成功比對到單字 `Understanding` 的開頭：

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
          "title": "Understanding Multi-Fields in Search"
        }
      }
    ]
  }
}
```
