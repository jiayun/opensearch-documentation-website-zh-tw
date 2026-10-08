---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Kuromoji 詞性"
parent: Token filters
nav_order: 233
---

# Kuromoji 詞性詞元篩選器

`kuromoji_part_of_speech` 詞元篩選器會移除詞性 (POS) 標記與已設定之停用標記清單中某個項目相符的詞元。Kuromoji 斷詞器會為每個詞元指派一個 IPAdic 詞性標記。此篩選器會讀取該標記，並捨棄具有文法功能（例如助詞、助動詞和標點符號）而非內容功能的詞元。

## 安裝

`kuromoji_part_of_speech` 詞元篩選器需要 `analysis-kuromoji` 外掛程式。如需安裝說明，請參閱 [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)。

## 參數

下表列出 `kuromoji_part_of_speech` 詞元篩選器的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`stoptags` | 字串陣列 | 要移除的 IPAdic 詞性標記清單。詞性標記與此清單中某個項目完全相符的詞元會被捨棄。預設為內建的日文停用標記集。

如需可用停用標記的完整清單，請參閱 Lucene 儲存庫中的 [stoptags.txt](https://github.com/apache/lucene/blob/main/lucene/analysis/kuromoji/src/resources/org/apache/lucene/analysis/ja/stoptags.txt)。

## 範例：預設篩選器

下列範例會建立一個索引，其中包含使用預設停用標記清單的分析器：

```json
PUT /kuromoji-pos-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "pos_filter_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": ["kuromoji_part_of_speech"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用意思為「我在東京的餐廳吃壽司」的句子測試分析器：

```json
POST /kuromoji-pos-index/_analyze
{
  "analyzer": "pos_filter_analyzer",
  "text": "東京のレストランで寿司を食べる"
}
```
{% include copy-curl.html %}

回應顯示助詞 の（所有格）、で（處所格）和 を（受格）已被移除：

```json
{
  "tokens": [
    {
      "token": "東京",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": "レストラン",
      "start_offset": 3,
      "end_offset": 8,
      "type": "word",
      "position": 2
    },
    {
      "token": "寿司",
      "start_offset": 9,
      "end_offset": 11,
      "type": "word",
      "position": 4
    },
    {
      "token": "食べる",
      "start_offset": 12,
      "end_offset": 15,
      "type": "word",
      "position": 6
    }
  ]
}
```

## 範例：自訂停用標記

下列範例會建立一個篩選器，僅移除助動詞 (助動詞)，同時保留所有其他文法詞元：

```json
PUT /kuromoji-custom-pos-index
{
  "settings": {
    "analysis": {
      "filter": {
        "auxiliary_verb_filter": {
          "type": "kuromoji_part_of_speech",
          "stoptags": ["助動詞"]
        }
      },
      "analyzer": {
        "auxiliary_filter_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": ["auxiliary_verb_filter"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 相關文件

- [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)
- [Kuromoji 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/kuromoji/)
- [Kuromoji 基本形詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-baseform/)
- [日文停用詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/ja-stop/)
