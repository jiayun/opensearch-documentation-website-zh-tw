---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Kuromoji 疊字記號"
parent: Character filters
nav_order: 115
---

# Kuromoji 疊字記號字元篩選器

`kuromoji_iteration_mark` 字元篩選器會將日文的水平疊字記號（odoriji）正規化，方法是將每個記號取代為其所重複的字元。日文書寫中使用疊字記號作為重複字元的簡寫：

- 々（漢字疊字記號）-- 原樣重複前一個漢字字元，因此 佐々木 會變成 佐佐木。
- ゝ（平假名疊字記號）-- 原樣重複前一個平假名字元，因此 かゝ 會變成 かか。
- ゞ（平假名濁音疊字記號）-- 重複前一個平假名字元並加上濁音（dakuten）。前一個字元必須為清音，因此 みすゞ 會變成 みすず，其中 す 濁音化為 ず。
- ヽ（片假名疊字記號）-- 原樣重複前一個片假名字元，因此 コヽア 會變成 ココア。
- ヾ（片假名濁音疊字記號）-- 重複前一個片假名字元並加上濁音（dakuten）。前一個字元必須為清音，因此 カヾ 會變成 カガ。

在斷詞之前展開這些記號，可確保無論原始文字使用疊字記號，還是直接寫出重複的字元，產生的詞元都會保持一致。

## 安裝

`kuromoji_iteration_mark` 字元篩選器需要 `analysis-kuromoji` 外掛程式。如需安裝指示，請參閱 [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)。

## 參數

下表列出 `kuromoji_iteration_mark` 字元篩選器的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`normalize_kanji` | 布林值 | 當 `true` 時，會將漢字疊字記號（々）正規化。預設為 `true`。
`normalize_kana` | 布林值 | 當 `true` 時，會將假名疊字記號（ゞ、ヾ、ゝ 及 ヽ）正規化。預設為 `true`。

## 範例

下列範例會建立一個索引，其中包含使用 `kuromoji_iteration_mark` 字元篩選器的自訂分析器：

```json
PUT /iteration-mark-index
{
  "settings": {
    "analysis": {
      "char_filter": {
        "iteration_mark_filter": {
          "type": "kuromoji_iteration_mark",
          "normalize_kanji": true,
          "normalize_kana": true
        }
      },
      "analyzer": {
        "iteration_mark_analyzer": {
          "type": "custom",
          "char_filter": ["iteration_mark_filter"],
          "tokenizer": "kuromoji_tokenizer"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用包含漢字疊字記號的文字測試分析器。名稱 佐々木（Sasaki）使用 々 來重複前一個漢字 佐：

```json
POST /iteration-mark-index/_analyze
{
  "analyzer": "iteration_mark_analyzer",
  "text": "佐々木さんは元気です"
}
```
{% include copy-curl.html %}

字元篩選器會在斷詞之前將 佐々木 展開為 佐佐木：

```json
{
  "tokens": [
    {
      "token": "佐佐木",
      "start_offset": 0,
      "end_offset": 3,
      "type": "word",
      "position": 0
    },
    {
      "token": "さん",
      "start_offset": 3,
      "end_offset": 5,
      "type": "word",
      "position": 1
    },
    {
      "token": "は",
      "start_offset": 5,
      "end_offset": 6,
      "type": "word",
      "position": 2
    },
    {
      "token": "元気",
      "start_offset": 6,
      "end_offset": 8,
      "type": "word",
      "position": 3
    },
    {
      "token": "です",
      "start_offset": 8,
      "end_offset": 10,
      "type": "word",
      "position": 4
    }
  ]
}
```

## 相關文件

- [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)
- [Kuromoji 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/kuromoji/)
