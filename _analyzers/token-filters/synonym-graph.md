---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "同義詞圖"
parent: Token filters
nav_order: 420
---

# 同義詞圖詞元篩選器

`synonym_graph` 詞元篩選器是 `synonym` 詞元篩選器的進階版本。它支援多字詞同義詞，並可跨多個詞元處理同義詞，因此非常適合用於片語，或詞元之間關係很重要的情境。

## 參數

`synonym_graph` 詞元篩選器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`synonyms` | 必須指定 `synonyms` 或 `synonyms_path` 其中之一 | 字串 | 直接在組態中定義的同義詞規則清單。
`synonyms_path` | 必須指定 `synonyms` 或 `synonyms_path` 其中之一 | 字串 | 包含同義詞規則之檔案的檔案路徑（可以是絕對路徑，或相對於 config 目錄的路徑）。
`lenient` | 選用 | 布林值 | 載入規則組態時是否忽略例外狀況。預設為 `false`。
`format` | 選用 | 字串 | 指定用於決定 OpenSearch 如何定義及解譯同義詞的格式。有效值為：<br>- `solr` <br>- [`wordnet`](https://wordnet.princeton.edu/)。<br> 預設為 `solr`。
`expand` | 選用 | 布林值 |  是否展開等效同義詞規則。預設為 `true`。<br><br>例如：<br>若 `synonyms` 定義為 `"quick, fast"`，且 `expand` 設定為 `true`，則同義詞規則會設定如下：<br>- `quick => quick`<br>- `quick => fast`<br>- `fast => quick`<br>- `fast => fast`<br><br>若 `expand` 設定為 `false`，則同義詞規則會設定如下：<br>- `quick => quick`<br>- `fast => quick`
`synonym_analyzer` | 選用 | 字串 | 用於剖析同義詞規則的分析器名稱。您可以指定該索引可用的任何分析器：內建分析器（例如 `standard`、`simple`、`stop`、`whitespace` 或 `keyword`）、語言分析器、由外掛程式註冊的分析器，或在同一索引中定義的自訂分析器。若無法解析指定名稱的分析器，OpenSearch 會使用定義此篩選器的分析鏈來剖析規則，且不會傳回錯誤。預設會使用分析鏈。

## 範例：Solr 格式

下列範例請求會建立名為 `my-index` 的新索引，並設定一個使用 `synonym_graph` 篩選器的分析器。此篩選器使用預設的 `solr` 規則格式進行設定：

```json
PUT /my-index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_synonym_graph_filter": {
          "type": "synonym_graph",
          "synonyms": [
            "sports car, race car",
            "fast car, speedy vehicle",
            "luxury car, premium vehicle",
            "electric car, EV"
          ]
        }
      },
      "analyzer": {
        "my_synonym_graph_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_synonym_graph_filter"
          ]
        }
      }
    }
  }
}

```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用該分析器所產生的詞元：

```json
GET /my-car-index/_analyze
{
  "analyzer": "my_synonym_graph_analyzer",
  "text": "I just bought a sports car and it is a fast car."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "i","start_offset": 0,"end_offset": 1,"type": "<ALPHANUM>","position": 0},
    {"token": "just","start_offset": 2,"end_offset": 6,"type": "<ALPHANUM>","position": 1},
    {"token": "bought","start_offset": 7,"end_offset": 13,"type": "<ALPHANUM>","position": 2},
    {"token": "a","start_offset": 14,"end_offset": 15,"type": "<ALPHANUM>","position": 3},
    {"token": "race","start_offset": 16,"end_offset": 26,"type": "SYNONYM","position": 4},
    {"token": "sports","start_offset": 16,"end_offset": 22,"type": "<ALPHANUM>","position": 4,"positionLength": 2},
    {"token": "car","start_offset": 16,"end_offset": 26,"type": "SYNONYM","position": 5,"positionLength": 2},
    {"token": "car","start_offset": 23,"end_offset": 26,"type": "<ALPHANUM>","position": 6},
    {"token": "and","start_offset": 27,"end_offset": 30,"type": "<ALPHANUM>","position": 7},
    {"token": "it","start_offset": 31,"end_offset": 33,"type": "<ALPHANUM>","position": 8},
    {"token": "is","start_offset": 34,"end_offset": 36,"type": "<ALPHANUM>","position": 9},
    {"token": "a","start_offset": 37,"end_offset": 38,"type": "<ALPHANUM>","position": 10},
    {"token": "speedy","start_offset": 39,"end_offset": 47,"type": "SYNONYM","position": 11},
    {"token": "fast","start_offset": 39,"end_offset": 43,"type": "<ALPHANUM>","position": 11,"positionLength": 2},
    {"token": "vehicle","start_offset": 39,"end_offset": 47,"type": "SYNONYM","position": 12,"positionLength": 2},
    {"token": "car","start_offset": 44,"end_offset": 47,"type": "<ALPHANUM>","position": 13}
  ]
}
```

## 範例：WordNet 格式

下列範例請求會建立名為 `my-wordnet-index` 的新索引，並設定一個使用 `synonym_graph` 篩選器的分析器。此篩選器使用 [`wordnet`](https://wordnet.princeton.edu/) 規則格式進行設定：

```json
PUT /my-wordnet-index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_synonym_graph_filter": {
          "type": "synonym_graph",
          "format": "wordnet",
          "synonyms": [
            "s(100000001, 1, 'sports car', n, 1, 0).",
            "s(100000001, 2, 'race car', n, 1, 0).",
            "s(100000001, 3, 'fast car', n, 1, 0).",
            "s(100000001, 4, 'speedy vehicle', n, 1, 0)."
          ]
        }
      },
      "analyzer": {
        "my_synonym_graph_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_synonym_graph_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用該分析器所產生的詞元：

```json
GET /my-wordnet-index/_analyze
{
  "analyzer": "my_synonym_graph_analyzer",
  "text": "I just bought a sports car and it is a fast car."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "i","start_offset": 0,"end_offset": 1,"type": "<ALPHANUM>","position": 0},
    {"token": "just","start_offset": 2,"end_offset": 6,"type": "<ALPHANUM>","position": 1},
    {"token": "bought","start_offset": 7,"end_offset": 13,"type": "<ALPHANUM>","position": 2},
    {"token": "a","start_offset": 14,"end_offset": 15,"type": "<ALPHANUM>","position": 3},
    {"token": "race","start_offset": 16,"end_offset": 26,"type": "SYNONYM","position": 4},
    {"token": "fast","start_offset": 16,"end_offset": 26,"type": "SYNONYM","position": 4,"positionLength": 2},
    {"token": "speedy","start_offset": 16,"end_offset": 26,"type": "SYNONYM","position": 4,"positionLength": 3},
    {"token": "sports","start_offset": 16,"end_offset": 22,"type": "<ALPHANUM>","position": 4,"positionLength": 4},
    {"token": "car","start_offset": 16,"end_offset": 26,"type": "SYNONYM","position": 5,"positionLength": 4},
    {"token": "car","start_offset": 16,"end_offset": 26,"type": "SYNONYM","position": 6,"positionLength": 3},
    {"token": "vehicle","start_offset": 16,"end_offset": 26,"type": "SYNONYM","position": 7,"positionLength": 2},
    {"token": "car","start_offset": 23,"end_offset": 26,"type": "<ALPHANUM>","position": 8},
    {"token": "and","start_offset": 27,"end_offset": 30,"type": "<ALPHANUM>","position": 9},
    {"token": "it","start_offset": 31,"end_offset": 33,"type": "<ALPHANUM>","position": 10},
    {"token": "is","start_offset": 34,"end_offset": 36,"type": "<ALPHANUM>","position": 11},
    {"token": "a","start_offset": 37,"end_offset": 38,"type": "<ALPHANUM>","position": 12},
    {"token": "sports","start_offset": 39,"end_offset": 47,"type": "SYNONYM","position": 13},
    {"token": "race","start_offset": 39,"end_offset": 47,"type": "SYNONYM","position": 13,"positionLength": 2},
    {"token": "speedy","start_offset": 39,"end_offset": 47,"type": "SYNONYM","position": 13,"positionLength": 3},
    {"token": "fast","start_offset": 39,"end_offset": 43,"type": "<ALPHANUM>","position": 13,"positionLength": 4},
    {"token": "car","start_offset": 39,"end_offset": 47,"type": "SYNONYM","position": 14,"positionLength": 4},
    {"token": "car","start_offset": 39,"end_offset": 47,"type": "SYNONYM","position": 15,"positionLength": 3},
    {"token": "vehicle","start_offset": 39,"end_offset": 47,"type": "SYNONYM","position": 16,"positionLength": 2},
    {"token": "car","start_offset": 44,"end_offset": 47,"type": "<ALPHANUM>","position": 17}
  ]
}
```
