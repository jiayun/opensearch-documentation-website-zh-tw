---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Kuromoji 基本形"
parent: Token filters
nav_order: 230
---

# Kuromoji 基本形詞元篩選器

`kuromoji_baseform` 詞元篩選器會將經過詞形變化的日文詞元替換為其辭典基本形，作用如同詞形還原器 (lemmatizer)。

此篩選器適用於帶有 Kuromoji 斷詞器所提供之辭典形資訊的詞元。不具辭典資訊的詞元（例如未知詞）會原封不動地傳遞。

請注意，Kuromoji 斷詞器會在此篩選器執行之前，將部分活用形分割為多個詞元。例如，過去式的*い*形容詞 美しかった（曾經很美）會被分割為 美しかっ 和 た。此篩選器會將 美しかっ 正規化為 美しい，但 た 仍會保留為獨立的詞元。若要移除 た 等助動詞詞元，請將 [`kuromoji_part_of_speech`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-part-of-speech/) 和 [`ja_stop`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/ja-stop/) 加入篩選器鏈。

## 安裝

`kuromoji_baseform` 詞元篩選器需要 `analysis-kuromoji` 外掛程式。如需安裝說明，請參閱 [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)。

## 參數

`kuromoji_baseform` 詞元篩選器沒有可設定的參數。

## 範例

下列範例會建立一個索引，其中包含使用 `kuromoji_baseform` 的自訂分析器：

```json
PUT /kuromoji-baseform-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "baseform_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": ["kuromoji_baseform"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用包含活用動詞的句子（意思為「我吃了壽司並喝了茶」）測試分析器：

```json
POST /kuromoji-baseform-index/_analyze
{
  "analyzer": "baseform_analyzer",
  "text": "寿司を食べてお茶を飲んだ"
}
```
{% include copy-curl.html %}

回應顯示活用動詞已正規化為其基本形。由於此分析器僅使用 `kuromoji_baseform`，因此助詞 を、て 以及助動詞 だ 都會保留：

```json
{
  "tokens": [
    {
      "token": "寿司",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": "を",
      "start_offset": 2,
      "end_offset": 3,
      "type": "word",
      "position": 1
    },
    {
      "token": "食べる",
      "start_offset": 3,
      "end_offset": 5,
      "type": "word",
      "position": 2
    },
    {
      "token": "て",
      "start_offset": 5,
      "end_offset": 6,
      "type": "word",
      "position": 3
    },
    {
      "token": "お茶",
      "start_offset": 6,
      "end_offset": 8,
      "type": "word",
      "position": 4
    },
    {
      "token": "を",
      "start_offset": 8,
      "end_offset": 9,
      "type": "word",
      "position": 5
    },
    {
      "token": "飲む",
      "start_offset": 9,
      "end_offset": 11,
      "type": "word",
      "position": 6
    },
    {
      "token": "だ",
      "start_offset": 11,
      "end_offset": 12,
      "type": "word",
      "position": 7
    }
  ]
}
```

て形 食べて 和過去式 飲んだ 會被替換為其基本形 食べる 和 飲む。助詞 を、て 以及助動詞 だ 仍保留在詞元串流中，因為 `kuromoji_baseform` 只會正規化詞形變化，而不會移除文法詞元。

## 範例：與詞性篩選器和停用詞篩選器搭配使用

若也要移除助詞和助動詞，請將 `kuromoji_part_of_speech` 和 `ja_stop` 加入篩選器鏈。下列範例會建立一個包含組合分析器的索引：

```json
PUT /kuromoji-baseform-full-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "baseform_full_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": ["kuromoji_baseform", "kuromoji_part_of_speech", "ja_stop"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用組合分析器處理相同的句子：

```json
POST /kuromoji-baseform-full-index/_analyze
{
  "analyzer": "baseform_full_analyzer",
  "text": "寿司を食べてお茶を飲んだ"
}
```
{% include copy-curl.html %}

回應僅顯示實詞。助詞 を、て 以及助動詞 だ 已被移除，並以位置間隙標示其原本所在的位置：

```json
{
  "tokens": [
    {
      "token": "寿司",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": "食べる",
      "start_offset": 3,
      "end_offset": 5,
      "type": "word",
      "position": 2
    },
    {
      "token": "お茶",
      "start_offset": 6,
      "end_offset": 8,
      "type": "word",
      "position": 4
    },
    {
      "token": "飲む",
      "start_offset": 9,
      "end_offset": 11,
      "type": "word",
      "position": 6
    }
  ]
}
```

## 相關文件

- [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)
- [Kuromoji 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/kuromoji/)
- [Kuromoji 詞性詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-part-of-speech/)
- [日文停用詞詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/ja-stop/)
