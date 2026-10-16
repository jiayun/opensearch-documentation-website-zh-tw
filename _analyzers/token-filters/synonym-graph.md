---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "同義詞圖"
parent: Token filters
nav_order: 420
---

# 同義詞圖詞元篩選器

`synonym_graph` 詞元篩選器是 `synonym` 詞元篩選器的進階版本。它支援多詞同義詞，並可跨多個詞元處理同義詞，因此非常適合用於片語或詞元之間關係重要的情境。

請僅在[搜尋分析器]({{site.url}}{{site.baseurl}}/analyzers/search-analyzers/#specifying-a-search-analyzer-in-the-mappings)中使用 `synonym_graph` 篩選器。在編製索引時，OpenSearch 會忽略每個詞元的 `positionLength`，因此多詞同義詞會使其後詞元的位置發生位移。例如，如果索引分析器將 `ev` 對應至 `electric car`，則文字 `ev charger` 中的 `charger` 會在位置 2 編製索引，而針對 `ev charger` 的 `match_phrase` 查詢將不再符合該文件。若要在編製索引時套用同義詞，請使用 [`synonym`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/synonym/) 詞元篩選器。
{: .note}

## 參數

`synonym_graph` 詞元篩選器可以使用下列參數進行組態。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`synonyms` | 必須指定 `synonyms` 或 `synonyms_path` 其中之一 | 字串 | 直接在組態中定義的同義詞規則清單。
`synonyms_path` | 必須指定 `synonyms` 或 `synonyms_path` 其中之一 | 字串 | 包含同義詞規則之檔案的檔案路徑（絕對路徑或相對於 config 目錄的路徑）。
`lenient` | 選用 | 布林值 | 載入規則組態時是否忽略例外。若為 `true`，OpenSearch 會略過無法解析的同義詞詞彙，並保留規則的其餘部分。如需更多資訊，請參閱[包含停用詞的同義詞規則](#synonym-rules-containing-stop-words)。預設為 `false`。
`format` | 選用 | 字串 | 指定用來決定 OpenSearch 如何定義與解譯同義詞的格式。有效值為：<br>- `solr` <br>- [`wordnet`](https://wordnet.princeton.edu/)。 <br> 預設為 `solr`。
`expand` | 選用 | 布林值 |  是否展開等效的同義詞規則。預設為 `true`。<br><br>例如： <br>若 `synonyms` 定義為 `"quick, fast"`，且 `expand` 設定為 `true`，則同義詞規則的組態如下：<br>- `quick => quick`<br>- `quick => fast`<br>- `fast => quick`<br>- `fast => fast`<br><br>若 `expand` 設定為 `false`，則同義詞規則的組態如下：<br>- `quick => quick`<br>- `fast => quick`
`synonym_analyzer` | 選用 | 字串 | 用來解析同義詞規則的分析器名稱。可指定索引可用的任何分析器：內建分析器（例如 `standard`、`simple`、`stop`、`whitespace` 或 `keyword`）、語言分析器、由外掛程式註冊的分析器，或在同一索引中定義的自訂分析器。若指定的分析器無法解析，OpenSearch 會使用定義此篩選器的分析鏈來解析規則，且不會回傳錯誤。預設會使用分析鏈。如需更多資訊，請參閱[解析同義詞規則](#parsing-synonym-rules)。

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

使用下列請求來檢查使用分析器所產生的詞元：

```json
GET /my-index/_analyze
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

使用下列請求來檢視透過分析器產生的詞元：

```json
GET /my-wordnet-index/_analyze
{
  "analyzer": "my_synonym_graph_analyzer",
  "text": "I just bought a sports car and it is a fast car."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

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

## 解析同義詞規則

除非您指定 `synonym_analyzer`，否則 OpenSearch 會使用分析器中位於 `synonym_graph` 之前的斷詞器和詞元篩選器來解析同義詞規則。這會對規則套用與文字相同的處理。例如，如果 `porter_stem` 篩選器位於 `synonym_graph` 之前，則規則 `running shoes, trainers` 會儲存為 `run shoe, trainer`。接著該規則會同時符合 `running shoes` 和 `run shoe`。

同義詞規則在每個位置只能包含一個詞元，因此當會在同一位置產生多個詞元的詞元篩選器位於 `synonym_graph` 之前時，其處理方式如下：

- 有些篩選器在解析規則時只會產生每個詞元的一個版本。例如，將 `preserve_original` 設為 `true` 的 [`asciifolding`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/asciifolding/) 篩選器只會產生折疊後的詞元。給定規則 `café, coffee shop`，文字 `coffee shop` 會產生同義詞 `cafe`，而非 `café`。
- [`word_delimiter_graph`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/word-delimiter-graph/)、[`ngram`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/ngram/)、[`edge_ngram`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/edge-ngram/)、[`shingle`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/shingle/) 和 [`multiplexer`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/multiplexer/) 篩選器無法解析同義詞規則。如果其中一個位於 `synonym_graph` 之前，OpenSearch 會拒絕建立索引的請求。

若要在與 `synonym_graph` 相同的分析器中使用其中一個篩選器，請將 `synonym_analyzer` 設為不包含該篩選器的分析器。接著 OpenSearch 會使用該分析器解析規則，並僅將該篩選器套用至文字。

## 包含停用詞的同義詞規則

如果 [`stop`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/stop/) 篩選器位於 `synonym_graph` 之前，它也會從同義詞規則中移除停用詞。預設情況下，如果規則中的詞彙包含停用詞，OpenSearch 會拒絕建立索引的請求。如果您將 `lenient` 設為 `true`，OpenSearch 會略過每個包含停用詞的詞彙，並保留規則的其餘部分。

下列範例請求會建立一個索引，其中包含會移除 `the` 的 `stop` 篩選器，以及規則中包含詞彙 `the flask` 的 `synonym_graph` 篩選器：

```json
PUT /drinkware
{
  "settings": {
    "analysis": {
      "filter": {
        "my_stop_filter": {
          "type": "stop",
          "stopwords": ["the"]
        },
        "my_synonym_graph_filter": {
          "type": "synonym_graph",
          "lenient": true,
          "synonyms": ["flask, the flask, thermos"]
        }
      },
      "analyzer": {
        "my_synonym_graph_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_stop_filter",
            "my_synonym_graph_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

OpenSearch 會略過 `the flask`，並保留 `flask` 和 `thermos` 作為同義詞。使用下列請求分析文字 `thermos`：

```json
GET /drinkware/_analyze
{
  "analyzer": "my_synonym_graph_analyzer",
  "text": "thermos"
}
```
{% include copy-curl.html %}

回應包含同義詞 `flask`：

```json
{
  "tokens": [
    {
      "token": "flask",
      "start_offset": 0,
      "end_offset": 7,
      "type": "SYNONYM",
      "position": 0
    },
    {
      "token": "thermos",
      "start_offset": 0,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 0
    }
  ]
}
```

如果略過的詞彙是其他詞彙對應的目標，該規則就不會新增任何同義詞。下表顯示當 `lenient` 為 `true` 且 `the` 為停用詞時，OpenSearch 如何處理其他規則。

規則 | `expand` | 結果
:--- | :--- | :---
`flask, thermos => the flask` | `true` | 不會新增任何同義詞，因為替代詞彙包含停用詞。
`the flask, flask, thermos` | `false` | 不會新增任何同義詞，因為當 `expand` 為 `false` 時，所有詞彙都會對應至第一個詞彙，而該詞彙包含停用詞。
`flask, the flask, thermos` | `false` | `thermos` 對應至 `flask`。

如果 `stop` 篩選器位於 `synonym_graph` 之後，停用詞會在同義詞比對後從同義詞圖中移除，導致圖結構損壞。例如，假設有規則 `thermos, the flask`，且 `stop` 篩選器位於 `synonym_graph` 之後，則針對 `the flask` 的 `match` 查詢只會搜尋 `thermos`，而不會比對到包含 `flask` 的文件。請從同義詞規則中移除這類詞彙，或將 `stop` 篩選器放在 `synonym_graph` 之前。
{: .warning}
