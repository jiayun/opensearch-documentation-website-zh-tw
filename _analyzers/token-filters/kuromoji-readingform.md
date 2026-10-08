---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Kuromoji 讀音形式"
parent: Token filters
nav_order: 234
---

# Kuromoji 讀音形式詞元篩選器

`kuromoji_readingform` 詞元篩選器會將每個詞元取代為其讀音形式。日文字元（漢字）可能有多種讀法；此篩選器會使用 Kuromoji 斷詞器提供的讀音資訊，輸出每個詞元的讀音形式。此篩選器可以輸出片假名（日文表音文字）或羅馬字（拉丁字母轉寫）的讀音。

## 安裝

`kuromoji_readingform` 詞元篩選器需要 `analysis-kuromoji` 外掛程式。如需安裝說明，請參閱 [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)。

## 參數

下表列出 `kuromoji_readingform` 詞元篩選器的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`use_romaji` | 布林值 | 設為 `false`（預設）時，詞元會取代為其片假名讀音。設為 `true` 時，詞元會取代為其羅馬字（拉丁字母）轉寫。

## 範例：片假名讀音（預設）

下列範例會建立一個索引，其中包含輸出片假名讀音的分析器：

```json
PUT /kuromoji-reading-katakana-index
{
  "settings": {
    "analysis": {
      "filter": {
        "katakana_reading": {
          "type": "kuromoji_readingform",
          "use_romaji": false
        }
      },
      "analyzer": {
        "katakana_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": ["katakana_reading"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用意思為「東京是日本的首都」的句子測試分析器：

```json
POST /kuromoji-reading-katakana-index/_analyze
{
  "analyzer": "katakana_analyzer",
  "text": "東京は日本の首都です"
}
```
{% include copy-curl.html %}

回應顯示漢字詞元已取代為其片假名讀音：

```json
{
  "tokens": [
    {
      "token": "トウキョウ",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": "ハ",
      "start_offset": 2,
      "end_offset": 3,
      "type": "word",
      "position": 1
    },
    {
      "token": "ニッポン",
      "start_offset": 3,
      "end_offset": 5,
      "type": "word",
      "position": 2
    },
    {
      "token": "ノ",
      "start_offset": 5,
      "end_offset": 6,
      "type": "word",
      "position": 3
    },
    {
      "token": "シュト",
      "start_offset": 6,
      "end_offset": 8,
      "type": "word",
      "position": 4
    },
    {
      "token": "デス",
      "start_offset": 8,
      "end_offset": 10,
      "type": "word",
      "position": 5
    }
  ]
}
```

## 範例：羅馬字讀音

下列範例會建立輸出羅馬字轉寫的分析器：

```json
PUT /kuromoji-reading-romaji-index
{
  "settings": {
    "analysis": {
      "filter": {
        "romaji_reading": {
          "type": "kuromoji_readingform",
          "use_romaji": true
        }
      },
      "analyzer": {
        "romaji_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": ["romaji_reading"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用相同的句子進行測試：

```json
POST /kuromoji-reading-romaji-index/_analyze
{
  "analyzer": "romaji_analyzer",
  "text": "東京は日本の首都です"
}
```
{% include copy-curl.html %}

回應顯示拉丁字母轉寫結果：

```json
{
  "tokens": [
    {
      "token": "tōkyō",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": "ha",
      "start_offset": 2,
      "end_offset": 3,
      "type": "word",
      "position": 1
    },
    {
      "token": "nippon",
      "start_offset": 3,
      "end_offset": 5,
      "type": "word",
      "position": 2
    },
    {
      "token": "no",
      "start_offset": 5,
      "end_offset": 6,
      "type": "word",
      "position": 3
    },
    {
      "token": "shuto",
      "start_offset": 6,
      "end_offset": 8,
      "type": "word",
      "position": 4
    },
    {
      "token": "desu",
      "start_offset": 8,
      "end_offset": 10,
      "type": "word",
      "position": 5
    }
  ]
}
```

讀音形式篩選器會取代整個詞元內容。如果您同時需要原始形式和讀音，請改用 `kuromoji_completion` 詞元篩選器，該篩選器會將讀音變體作為額外的詞元新增至相同位置。
{: .tip}

## 相關文件

- [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)
- [Kuromoji 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/kuromoji/)
- [Kuromoji 自動完成詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-completion/)
