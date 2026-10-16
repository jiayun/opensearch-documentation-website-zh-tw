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

`synonym` 詞元篩選器可以使用下列參數進行組態。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`synonyms` | 必須指定 `synonyms` 或 `synonyms_path` 其中之一 | 字串 | 直接在組態中定義的同義詞規則清單。
`synonyms_path` | 必須指定 `synonyms` 或 `synonyms_path` 其中之一 | 字串 |  包含同義詞規則的檔案路徑（絕對路徑或相對於 config 目錄的路徑）。
`lenient` | 選用 | 布林值 | 載入規則組態時是否忽略例外。若為 `true`，OpenSearch 會略過無法解析的同義詞詞元，並保留規則的其餘部分。如需更多資訊，請參閱[包含停用詞的同義詞規則](#synonym-rules-containing-stop-words)。預設為 `false`。
`format` | 選用 | 字串 | 指定 OpenSearch 用來定義與解譯同義詞的格式。有效值為：<br>- `solr` <br>- [`wordnet`](https://wordnet.princeton.edu/)。 <br> 預設為 `solr`。
`expand` | 選用 | 布林值 |  是否展開等價的同義詞規則。預設為 `true`。<br><br>範例： <br>若 `synonyms` 定義為 `"quick, fast"`，且 `expand` 設為 `true`，則同義詞規則的組態如下：<br>- `quick => quick`<br>- `quick => fast`<br>- `fast => quick`<br>- `fast => fast`<br><br>若 `expand` 設為 `false`，則同義詞規則的組態如下：<br>- `quick => quick`<br>- `fast => quick`
`synonym_analyzer` | 選用 | 字串 | 用來解析同義詞規則的分析器名稱。可指定索引可用的任何分析器：內建分析器（例如 `standard`、`simple`、`stop`、`whitespace` 或 `keyword`）、語言分析器、由外掛程式註冊的分析器，或在同一索引中定義的自訂分析器。若指定的分析器無法解析，OpenSearch 會使用定義此篩選器的分析鏈來解析規則，且不會回傳錯誤。預設會使用分析鏈。如需更多資訊，請參閱[解析同義詞規則](#parsing-synonym-rules)。

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

使用下列請求來檢查使用分析器所產生的詞元：

```json
GET /my-wordnet-index/_analyze
{
  "analyzer": "my_wordnet_analyzer",
  "text": "I have a fast car"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

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

## 解析同義字規則

除非您指定 `synonym_analyzer`，否則 OpenSearch 會使用分析器中位於 `synonym` 之前的斷詞器與詞元篩選器來解析同義字規則。這會對規則套用與文字相同的處理。例如，若 `porter_stem` 篩選器位於 `synonym` 之前，規則 `running shoes, trainers` 會儲存為 `run shoe, trainer`。該規則隨後會同時比對 `running shoes` 與 `run shoe`。

同義字規則在每個位置只能包含一個詞元，因此當會在同一位置產生多個詞元的詞元篩選器位於 `synonym` 之前時，會依下列方式處理：

- 有些篩選器在解析規則時，每個詞元只會產生一個版本。例如，將 `preserve_original` 設為 `true` 的 [`asciifolding`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/asciifolding/) 篩選器只會產生摺疊後的詞元。給定規則 `café, coffee shop`，文字 `coffee shop` 會產生同義字 `cafe`，而不是 `café`。
- [`word_delimiter`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/word-delimiter/)、[`word_delimiter_graph`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/word-delimiter-graph/)、[`ngram`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/ngram/)、[`edge_ngram`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/edge-ngram/)、[`shingle`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/shingle/) 與 [`multiplexer`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/multiplexer/) 篩選器無法解析同義字規則。若其中任何一個位於 `synonym` 之前，OpenSearch 會拒絕建立索引的請求。

若要在與 `synonym` 相同的分析器中使用這些篩選器之一，請將 `synonym_analyzer` 設定為不包含該篩選器的分析器。OpenSearch 隨後會使用該分析器解析規則，並僅對文字套用該篩選器。

## 包含停用詞的同義詞規則

如果 [`stop`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/stop/) 篩選器排在 `synonym` 之前，它也會從同義詞規則中移除停用詞。根據預設，如果規則中的詞彙包含停用詞，OpenSearch 會拒絕建立索引的請求。如果您將 `lenient` 設為 `true`，OpenSearch 會略過每個包含停用詞的詞彙，並保留規則的其餘部分。

下列範例請求會建立一個索引，其中包含會移除 `the` 的 `stop` 篩選器，以及規則包含詞彙 `the flask` 的 `synonym` 篩選器：

```json
PUT /kitchenware
{
  "settings": {
    "analysis": {
      "filter": {
        "my_stop_filter": {
          "type": "stop",
          "stopwords": ["the"]
        },
        "my_synonym_filter": {
          "type": "synonym",
          "lenient": true,
          "synonyms": ["flask, the flask, thermos"]
        }
      },
      "analyzer": {
        "my_synonym_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_stop_filter",
            "my_synonym_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

OpenSearch 會略過 `the flask`，並保留 `flask` 和 `thermos` 作為同義詞。使用下列請求來分析文字 `thermos`：

```json
GET /kitchenware/_analyze
{
  "analyzer": "my_synonym_analyzer",
  "text": "thermos"
}
```
{% include copy-curl.html %}

回應包含同義詞 `flask`：

```json
{
  "tokens": [
    {
      "token": "thermos",
      "start_offset": 0,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "flask",
      "start_offset": 0,
      "end_offset": 7,
      "type": "SYNONYM",
      "position": 0
    }
  ]
}
```

如果略過的詞彙是其他詞彙對應到的目標，則該規則不會新增任何同義詞。下表顯示當 `lenient` 為 `true` 且 `the` 是停用詞時，OpenSearch 如何處理其他規則。

規則 | `expand` | 結果
:--- | :--- | :---
`flask, thermos => the flask` | `true` | 不會新增同義詞，因為取代詞彙包含停用詞。
`the flask, flask, thermos` | `false` | 不會新增同義詞，因為當 `expand` 為 `false` 時，所有詞彙都會對應到第一個詞彙，而該詞彙包含停用詞。
`flask, the flask, thermos` | `false` | `thermos` 會對應到 `flask`。
