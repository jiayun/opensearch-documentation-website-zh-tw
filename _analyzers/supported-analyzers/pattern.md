---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Pattern 分析器"
parent: Analyzers
nav_order: 90
---

# Pattern 分析器

`pattern` 分析器可讓您定義自訂分析器，使用正規表示式（regex）將輸入文字分割成詞元。此正規表示式會比對詞元之間的分隔符號，而非詞元本身。它也提供套用 regex 旗標、將詞元轉換為小寫，以及篩除停用詞的選項。

`pattern` 分析器由 [`pattern`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/pattern/) 斷詞器，以及後續的 [`lowercase`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/lowercase/) 與 [`stop`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/stop/) 詞元篩選器組成。除非您指定 `stopwords` 或 `stopwords_path`，否則 `stop` 篩選器不會移除任何詞元。

## 參數

`pattern` 分析器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`pattern` | 選用 | 字串 | 用於將輸入內容斷詞的 [Java 正規表示式](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)。預設為 `\W+`。
`flags` | 選用 | 字串 | 包含以直線符號分隔之 [Java 正規表示式旗標](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html#field.summary) 的字串，用於修改正規表示式的行為。
`lowercase` | 選用 | 布林值 | 是否將詞元轉換為小寫。預設為 `true`。
`stopwords` | 選用 | 字串或字串清單 | 指定預先定義停用詞清單（例如 `_english_`）的字串，或指定自訂停用詞清單的陣列。預設為 `_none_`。
`stopwords_path` | 選用 | 字串 | 包含停用詞清單之檔案的路徑（絕對路徑或相對於組態目錄的路徑）。

撰寫不良的正規表示式可能會使分析變得非常緩慢，在極端情況下，甚至可能導致 `StackOverflowError` 而使節點停止運作。請避免使用能以多種方式比對相同文字的模式，例如 `(a+)+` 這類巢狀量詞，並使用 [Analyze API]({{site.url}}{{site.baseurl}}/api-reference/analyze-apis/) 在具代表性的文字上測試新模式。
{: .warning}

## 範例

使用下列命令建立名為 `my_pattern_index` 且具有 `pattern` 分析器的索引：

```json
PUT /my_pattern_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_pattern_analyzer": {
          "type": "pattern",
          "pattern": "\\W+",  
          "lowercase": true,                
          "stopwords": ["and", "is"]       
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "my_field": {
        "type": "text",
        "analyzer": "my_pattern_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢視使用此分析器所產生的詞元：

```json
POST /my_pattern_index/_analyze
{
  "analyzer": "my_pattern_analyzer",
  "text": "OpenSearch is fast and scalable"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "opensearch",
      "start_offset": 0,
      "end_offset": 10,
      "type": "word",
      "position": 0
    },
    {
      "token": "fast",
      "start_offset": 14,
      "end_offset": 18,
      "type": "word",
      "position": 2
    },
    {
      "token": "scalable",
      "start_offset": 23,
      "end_offset": 31,
      "type": "word",
      "position": 4
    }
  ]
}
```

## 範例：分割駝峰式大小寫識別字

由於 regex 會比對分隔符號，它也能比對兩個字元之間的零寬位置。這讓您能將原始碼中的識別字（例如類別與方法名稱）分割成個別單字。下列模式包含五個替代項，分別會在連續的非字母與非數字字元處、小寫字母與大寫字母之間、大寫縮寫最後一個字母且其後接小寫字母之前，以及字母與數字之間分割文字：

```json
PUT /source-code
{
  "settings": {
    "analysis": {
      "analyzer": {
        "camel_case_analyzer": {
          "type": "pattern",
          "pattern": "[^\\p{L}\\p{N}]+|(?<=\\p{Ll})(?=\\p{Lu})|(?<=\\p{Lu})(?=\\p{Lu}\\p{Ll})|(?<=\\p{L})(?=\\p{N})|(?<=\\p{N})(?=\\p{L})"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

在 JSON 中，模式內的每個反斜線都必須逸出為 `\\`。

使用下列請求來分析類別與方法名稱：

```json
POST /source-code/_analyze
{
  "analyzer": "camel_case_analyzer",
  "text": "XMLHttpRequest2Handler.sendJSONPayload"
}
```
{% include copy-curl.html %}

回應包含轉為小寫的個別單字：

```json
{
  "tokens": [
    {
      "token": "xml",
      "start_offset": 0,
      "end_offset": 3,
      "type": "word",
      "position": 0
    },
    {
      "token": "http",
      "start_offset": 3,
      "end_offset": 7,
      "type": "word",
      "position": 1
    },
    {
      "token": "request",
      "start_offset": 7,
      "end_offset": 14,
      "type": "word",
      "position": 2
    },
    {
      "token": "2",
      "start_offset": 14,
      "end_offset": 15,
      "type": "word",
      "position": 3
    },
    {
      "token": "handler",
      "start_offset": 15,
      "end_offset": 22,
      "type": "word",
      "position": 4
    },
    {
      "token": "send",
      "start_offset": 23,
      "end_offset": 27,
      "type": "word",
      "position": 5
    },
    {
      "token": "json",
      "start_offset": 27,
      "end_offset": 31,
      "type": "word",
      "position": 6
    },
    {
      "token": "payload",
      "start_offset": 31,
      "end_offset": 38,
      "type": "word",
      "position": 7
    }
  ]
}
```

## 在 pattern 分析器中加入詞元篩選器

若要套用 `pattern` 分析器未提供的詞元篩選器，請將它重建為自訂分析器，並將篩選器加入其 `filter` 陣列。下列請求會建立一個自訂分析器，產生與預設 `pattern` 分析器相同的詞元：

```json
PUT /custom-pattern-index
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "my_pattern_tokenizer": {
          "type": "pattern",
          "pattern": "\\W+"
        }
      },
      "analyzer": {
        "rebuilt_pattern": {
          "type": "custom",
          "tokenizer": "my_pattern_tokenizer",
          "filter": [
            "lowercase"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

在 `filter` 陣列中 `lowercase` 之後加入更多詞元篩選器。若要移除停用詞，請加入 [`stop`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/stop/) 篩選器。
