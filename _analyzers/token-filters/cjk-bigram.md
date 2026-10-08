---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CJK bigram
parent: Token filters
nav_order: 30
---

# CJK bigram 詞元篩選器

`cjk_bigram` 詞元篩選器專為處理東亞語言而設計，例如中文、日文和韓文 (CJK)，這些語言通常不使用空格分隔字詞。Bigram 是詞元字串中兩個相鄰元素組成的序列，這些元素可以是字元或字詞。對於 CJK 語言，bigram 有助於近似判斷字詞邊界，並擷取能傳達意義的重要字元組合。


## 參數

`cjk_bigram` 詞元篩選器可以使用兩個參數進行設定：`ignored_scripts` 和 `output_unigrams`。

### ignored_scripts

`cjk-bigram` 詞元篩選器會忽略所有非 CJK 文字系統 (例如拉丁字母或西里爾字母等書寫系統)，且只會將 CJK 文字斷詞為 bigram。使用此選項可指定要忽略的 CJK 文字系統。此選項接受下列有效值：

- `han`：`han` 文字系統用於處理漢字。[漢字](https://simple.wikipedia.org/wiki/Chinese_characters)是中國、日本和韓國書面語言中使用的語素文字。此篩選器有助於處理以中文、日文漢字 (kanji) 或韓文漢字 (Hanja) 撰寫之文字的斷詞、正規化或詞幹提取等文字處理工作。

- `hangul`：`hangul` 文字系統用於處理韓文字母 (Hangul)，這是韓文獨有的文字，不存在於其他東亞文字系統中。

- `hiragana`：`hiragana` 文字系統用於處理平假名，這是日文書寫系統中使用的兩種音節文字之一。
    平假名通常用於日文固有詞彙、文法元素以及某些形式的標點符號。

- `katakana`：`katakana` 文字系統用於處理片假名，這是另一種日文音節文字。
    片假名主要用於外來語、擬聲詞、學名以及某些日文詞彙。


### output_unigrams

此選項設為 `true` 時，會同時輸出 unigram (單一字元) 和 bigram。預設值為 `false`。

## 範例

下列範例請求會建立名為 `devanagari_example_index` 的新索引，並定義一個使用 `cjk_bigram_filter` 篩選器且將 `ignored_scripts` 參數設為 `katakana` 的分析器：

```json
PUT /cjk_bigram_example
{
  "settings": {
    "analysis": {
      "analyzer": {
        "cjk_bigrams_no_katakana": {
          "tokenizer": "standard",
          "filter": [ "cjk_bigrams_no_katakana_filter" ]
        }
      },
      "filter": {
        "cjk_bigrams_no_katakana_filter": {
          "type": "cjk_bigram",
          "ignored_scripts": [
            "katakana"
          ],
          "output_unigrams": true
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
POST /cjk_bigram_example/_analyze
{
  "analyzer": "cjk_bigrams_no_katakana",
  "text": "東京タワーに行く"
}
```
{% include copy-curl.html %}

範例文字：「東京タワーに行く」

    東京 (「東京」的漢字)
    タワー (「塔」的片假名)
    に行く (「前往」的平假名與漢字)

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "東",
      "start_offset": 0,
      "end_offset": 1,
      "type": "<SINGLE>",
      "position": 0
    },
    {
      "token": "東京",
      "start_offset": 0,
      "end_offset": 2,
      "type": "<DOUBLE>",
      "position": 0,
      "positionLength": 2
    },
    {
      "token": "京",
      "start_offset": 1,
      "end_offset": 2,
      "type": "<SINGLE>",
      "position": 1
    },
    {
      "token": "タワー",
      "start_offset": 2,
      "end_offset": 5,
      "type": "<KATAKANA>",
      "position": 2
    },
    {
      "token": "に",
      "start_offset": 5,
      "end_offset": 6,
      "type": "<SINGLE>",
      "position": 3
    },
    {
      "token": "に行",
      "start_offset": 5,
      "end_offset": 7,
      "type": "<DOUBLE>",
      "position": 3,
      "positionLength": 2
    },
    {
      "token": "行",
      "start_offset": 6,
      "end_offset": 7,
      "type": "<SINGLE>",
      "position": 4
    },
    {
      "token": "行く",
      "start_offset": 6,
      "end_offset": 8,
      "type": "<DOUBLE>",
      "position": 4,
      "positionLength": 2
    },
    {
      "token": "く",
      "start_offset": 7,
      "end_offset": 8,
      "type": "<SINGLE>",
      "position": 5
    }
  ]
}
```


