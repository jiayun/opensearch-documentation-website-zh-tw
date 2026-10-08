---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Stop
parent: Token filters
nav_order: 410
---

# Stop 詞元篩選器

`stop` 詞元篩選器用於在分析期間從詞元串流中移除常用字詞（也稱為_停用詞_）。停用詞通常是冠詞和介系詞，例如 `a` 或 `for`。這些字詞在搜尋查詢中沒有顯著意義，通常會被排除，以提升搜尋效率和相關性。

預設的英文停用詞清單包含下列字詞：`a`、`an`、`and`、`are`、`as`、`at`、`be`、`but`、`by`、`for`、`if`、`in`、`into`、`is`、`it`、`no`、`not`、`of`、`on`、`or`、`such`、`that`、`the`、`their`、`then`、`there`、`these`、`they`、`this`、`to`、`was`、`will` 和 `with`。

## 參數

`stop` 詞元篩選器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`stopwords` | 選用 | 字串 | 指定自訂的停用詞陣列，或[特定語言的預先定義停用詞集](#predefined-stopword-sets-by-language)。預設為 `_english_`。
`stopwords_path` | 選用 | 字串 | 指定包含自訂停用詞之檔案的檔案路徑（絕對路徑或相對於 config 目錄的路徑）。
`ignore_case` | 選用 | 布林值 | 若為 `true`，則比對停用詞時不區分大小寫。預設為 `false`。
`remove_trailing` | 選用 | 布林值 | 若為 `true`，則會在分析期間移除結尾的停用詞。預設為 `true`。

## 範例

下列範例請求會建立名為 `my-stopword-index` 的新索引，並設定一個分析器，其中包含使用英文預先定義停用詞清單的 `stop` 篩選器：

```json
PUT /my-stopword-index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_stop_filter": {
          "type": "stop",
          "stopwords": "_english_"
        }
      },
      "analyzer": {
        "my_stop_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_stop_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
GET /my-stopword-index/_analyze
{
  "analyzer": "my_stop_analyzer",
  "text": "A quick dog jumps over the turtle"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "quick",
      "start_offset": 2,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "dog",
      "start_offset": 8,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "jumps",
      "start_offset": 12,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "over",
      "start_offset": 18,
      "end_offset": 22,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "turtle",
      "start_offset": 27,
      "end_offset": 33,
      "type": "<ALPHANUM>",
      "position": 6
    }
  ]
}
```

## 依語言區分的預先定義停用詞集

以下是依語言區分的所有可用預先定義停用詞集清單：

- [`_arabic_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/ar/stopwords.txt)
- [`_armenian_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/hy/stopwords.txt)
- [`_basque_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/eu/stopwords.txt)
- [`_bengali_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/bn/stopwords.txt)
- [`_brazilian_`（巴西葡萄牙文）](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/br/stopwords.txt) 
- [`_bulgarian_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/bg/stopwords.txt)
- [`_catalan_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/ca/stopwords.txt)
- [`_cjk_`（中文、日文和韓文）](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/cjk/stopwords.txt)
- [`_czech_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/cz/stopwords.txt)
- [`_danish_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/danish_stop.txt)
- [`_dutch_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/dutch_stop.txt)
- [`_english_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/java/org/apache/lucene/analysis/en/EnglishAnalyzer.java#L48)
- [`_estonian_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/et/stopwords.txt)
- [`_finnish_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/finnish_stop.txt)
- [`_french_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/french_stop.txt)
- [`_galician_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/gl/stopwords.txt)
- [`_german_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/german_stop.txt)
- [`_greek_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/el/stopwords.txt)
- [`_hindi_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/hi/stopwords.txt)
- [`_hungarian_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/hungarian_stop.txt)
- [`_indonesian_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/id/stopwords.txt)
- [`_irish_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/irish_stop.txt)
- [`_italian_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/italian_stop.txt)
- [`_latvian_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/lv/stopwords.txt)
- [`_lithuanian_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/lt/stopwords.txt)
- [`_norwegian_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/norwegian_stop.txt)
- [`_persian_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/fa/stopwords.txt)
- [`_portuguese_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/portuguese_stop.txt)
- [`_romanian_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/ro/stopwords.txt)
- [`_russian_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/russian_stop.txt)
- [`_sorani_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/ckb/stopwords.txt)
- [`_spanish_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/spanish_stop.txt)
- [`_swedish_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/swedish_stop.txt)
- [`_thai_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/th/stopwords.txt)
- [`_turkish_`](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/tr/stopwords.txt)