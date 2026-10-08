---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Pattern
parent: Tokenizers
nav_order: 100
---

# Pattern 斷詞器

`pattern` 斷詞器是一種高度靈活的斷詞器，可讓您根據自訂的 Java 規則運算式將文字分割為詞元。與使用 Lucene 規則運算式的 `simple_pattern` 和 `simple_pattern_split` 斷詞器不同，`pattern` 斷詞器能處理更複雜、更精細的規則運算式模式，讓您更能掌控文字的斷詞方式。

## 使用範例

下列範例請求會建立名為 `my_index` 的新索引，並設定一個使用 `pattern` 斷詞器的分析器。此斷詞器會依據 `-`、`_` 或 `.` 字元分割文字：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "my_pattern_tokenizer": {
          "type": "pattern",
          "pattern": "[-_.]"
        }
      },
      "analyzer": {
        "my_pattern_analyzer": {
          "type": "custom",
          "tokenizer": "my_pattern_tokenizer"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "my_pattern_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_pattern_analyzer",
  "text": "OpenSearch-2024_v1.2"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "OpenSearch",
      "start_offset": 0,
      "end_offset": 10,
      "type": "word",
      "position": 0
    },
    {
      "token": "2024",
      "start_offset": 11,
      "end_offset": 15,
      "type": "word",
      "position": 1
    },
    {
      "token": "v1",
      "start_offset": 16,
      "end_offset": 18,
      "type": "word",
      "position": 2
    },
    {
      "token": "2",
      "start_offset": 19,
      "end_offset": 20,
      "type": "word",
      "position": 3
    }
  ]
}
```

## 參數

`pattern` 斷詞器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`pattern` | 選用 | 字串 | 用來將文字分割為詞元的模式，以 [Java 規則運算式](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)指定。預設為 `\W+`。
`flags` | 選用 | 字串 | 設定要套用至規則運算式、以管線符號分隔的[旗標](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html#field.summary)，例如 `"CASE_INSENSITIVE|MULTILINE|DOTALL"`。 
`group` | 選用 | 整數 | 指定要作為詞元的擷取群組。預設為 `-1`（依據相符項目分割）。

## 使用 group 參數的範例

下列範例請求設定了一個僅擷取第二個群組的 `group` 參數：

```json
PUT /my_index_group2
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "my_pattern_tokenizer": {
          "type": "pattern",
          "pattern": "([a-zA-Z]+)(\\d+)",
          "group": 2
        }
      },
      "analyzer": {
        "my_pattern_analyzer": {
          "type": "custom",
          "tokenizer": "my_pattern_tokenizer"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求來檢查使用此分析器產生的詞元：

```json
POST /my_index_group2/_analyze
{
  "analyzer": "my_pattern_analyzer",
  "text": "abc123def456ghi"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "123",
      "start_offset": 3,
      "end_offset": 6,
      "type": "word",
      "position": 0
    },
    {
      "token": "456",
      "start_offset": 9,
      "end_offset": 12,
      "type": "word",
      "position": 1
    }
  ]
}
```