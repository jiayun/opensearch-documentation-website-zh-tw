---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "同義詞"
parent: Token filters
nav_order: 415
---

# 同義詞詞元篩選器

`synonym` 詞元篩選器可讓您將多個詞彙對應到單一詞彙，或在字詞之間建立等價群組，以提升搜尋的彈性。

## 參數

`synonym` 詞元篩選器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`synonyms` | 必須指定 `synonyms` 或 `synonyms_path` 其中之一 | 字串 | 直接在組態中定義的同義詞規則清單。
`synonyms_path` | 必須指定 `synonyms` 或 `synonyms_path` 其中之一 | 字串 |  包含同義詞規則之檔案的檔案路徑（可以是絕對路徑，或相對於 config 目錄的路徑）。
`lenient` | 選用 | 布林值 | 載入規則組態時是否忽略例外狀況。預設為 `false`。
`format` | 選用 | 字串 | 指定用來決定 OpenSearch 如何定義及解譯同義詞的格式。有效值為：<br>- `solr` <br>- [`wordnet`](https://wordnet.princeton.edu/)。<br> 預設為 `solr`。
`expand` | 選用 | 布林值 |  是否展開等價的同義詞規則。預設為 `true`。<br><br>例如：<br>若 `synonyms` 定義為 `"quick, fast"`，且 `expand` 設為 `true`，則同義詞規則的設定如下：<br>- `quick => quick`<br>- `quick => fast`<br>- `fast => quick`<br>- `fast => fast`<br><br>若 `expand` 設為 `false`，則同義詞規則的設定如下：<br>- `quick => quick`<br>- `fast => quick`
`synonym_analyzer` | 選用 | 字串 | 用來剖析同義詞規則的分析器名稱。您可以指定該索引可用的任何分析器：內建分析器（例如 `standard`、`simple`、`stop`、`whitespace` 或 `keyword`）、語言分析器、由外掛程式註冊的分析器，或在同一個索引中定義的自訂分析器。若無法解析指定名稱的分析器，OpenSearch 會使用定義此篩選器的分析鏈來剖析規則，且不會傳回錯誤。預設會使用該分析鏈。

## 範例：Solr 格式

下列範例請求會建立名為 `my-synonym-index` 的新索引，並設定一個使用 `synonym` 篩選器的分析器。此篩選器使用預設的 `solr` 規則格式進行設定：

```json
PUT /my-synonym-index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_synonym_filter": {
          "type": "synonym",
          "synonyms": [
            "car, automobile",
            "quick, fast, speedy",
            "laptop => computer"
          ]
        }
      },
      "analyzer": {
        "my_synonym_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_synonym_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器所產生的詞元：

```json
GET /my-synonym-index/_analyze
{
  "analyzer": "my_synonym_analyzer",
  "text": "The quick dog jumps into the car with a laptop"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "the",
      "start_offset": 0,
      "end_offset": 3,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "quick",
      "start_offset": 4,
      "end_offset": 9,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "fast",
      "start_offset": 4,
      "end_offset": 9,
      "type": "SYNONYM",
      "position": 1
    },
    {
      "token": "speedy",
      "start_offset": 4,
      "end_offset": 9,
      "type": "SYNONYM",
      "position": 1
    },
    {
      "token": "dog",
      "start_offset": 10,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "jumps",
      "start_offset": 14,
      "end_offset": 19,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "into",
      "start_offset": 20,
      "end_offset": 24,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "the",
      "start_offset": 25,
      "end_offset": 28,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "car",
      "start_offset": 29,
      "end_offset": 32,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "automobile",
      "start_offset": 29,
      "end_offset": 32,
      "type": "SYNONYM",
      "position": 6
    },
    {
      "token": "with",
      "start_offset": 33,
      "end_offset": 37,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "a",
      "start_offset": 38,
      "end_offset": 39,
      "type": "<ALPHANUM>",
      "position": 8
    },
    {
      "token": "computer",
      "start_offset": 40,
      "end_offset": 46,
      "type": "SYNONYM",
      "position": 9
    }
  ]
}
```

## 範例：WordNet 格式

下列範例請求會建立名為 `my-wordnet-index` 的新索引，並設定一個使用 `synonym` 篩選器的分析器。此篩選器使用 [`wordnet`](https://wordnet.princeton.edu/) 規則格式進行設定：

```json
PUT /my-wordnet-index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_wordnet_synonym_filter": {
          "type": "synonym",
          "format": "wordnet",
          "synonyms": [
            "s(100000001,1,'fast',v,1,0).",
            "s(100000001,2,'quick',v,1,0).",
            "s(100000001,3,'swift',v,1,0)."
          ]
        }
      },
      "analyzer": {
        "my_wordnet_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_wordnet_synonym_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器所產生的詞元：

```json
GET /my-wordnet-index/_analyze
{
  "analyzer": "my_wordnet_analyzer",
  "text": "I have a fast car"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "i",
      "start_offset": 0,
      "end_offset": 1,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "have",
      "start_offset": 2,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "a",
      "start_offset": 7,
      "end_offset": 8,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "fast",
      "start_offset": 9,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "quick",
      "start_offset": 9,
      "end_offset": 13,
      "type": "SYNONYM",
      "position": 3
    },
    {
      "token": "swift",
      "start_offset": 9,
      "end_offset": 13,
      "type": "SYNONYM",
      "position": 3
    },
    {
      "token": "car",
      "start_offset": 14,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 4
    }
  ]
}
```
