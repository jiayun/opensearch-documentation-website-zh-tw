---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Kuromoji 詞幹提取器"
parent: Token filters
nav_order: 235
---

# Kuromoji 詞幹提取詞元篩選器

`kuromoji_stemmer` 詞元篩選器會正規化片假名單字，方法是從達到最小長度門檻的單字中移除結尾的長音符號 (ー)。日文中許多外來語是以片假名書寫，並以結尾的 ー 表示延長的最後母音（例如：コンピューター、プリンター）。實務上，日語使用者在非正式或技術性的文字中經常省略結尾的 ー，導致同一個單字出現兩種表面形式。此篩選器會將這些變體合併為單一的標準形式。

此篩選器會進行如下的轉換：

- コンピューター (computer) 會變成 コンピュータ。
- プリンター (printer) 會變成 プリンタ。

## 安裝

`kuromoji_stemmer` 詞元篩選器需要 `analysis-kuromoji` 外掛程式。如需安裝說明，請參閱 [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)。

## 參數

下表列出 `kuromoji_stemmer` 詞元篩選器的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`minimum_length` | 整數 | 詞元必須具備的最少字元數，達到此數量才會移除結尾的長音符號。短於此門檻的詞元會原封不動地傳遞。預設值為 `4`。

預設最小長度 `4` 可防止 カー (car，兩個字元) 等短單字被錯誤地提取詞幹為 カ。
{: .note}

## 範例

下列範例會建立一個索引，其中包含使用 `kuromoji_stemmer` 的自訂分析器：

```json
PUT /kuromoji-stemmer-index
{
  "settings": {
    "analysis": {
      "filter": {
        "katakana_stemmer": {
          "type": "kuromoji_stemmer",
          "minimum_length": 4
        }
      },
      "analyzer": {
        "stemmer_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": ["katakana_stemmer"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用片假名外來語測試分析器（意思為「我使用電腦和印表機」）：

```json
POST /kuromoji-stemmer-index/_analyze
{
  "analyzer": "stemmer_analyzer",
  "text": "コンピューターとプリンターを使う"
}
```
{% include copy-curl.html %}

回應顯示兩個單字結尾的長音符號皆已移除：

```json
{
  "tokens": [
    {
      "token": "コンピュータ",
      "start_offset": 0,
      "end_offset": 7,
      "type": "word",
      "position": 0
    },
    {
      "token": "と",
      "start_offset": 7,
      "end_offset": 8,
      "type": "word",
      "position": 1
    },
    {
      "token": "プリンタ",
      "start_offset": 8,
      "end_offset": 13,
      "type": "word",
      "position": 2
    },
    {
      "token": "を",
      "start_offset": 13,
      "end_offset": 14,
      "type": "word",
      "position": 3
    },
    {
      "token": "使う",
      "start_offset": 14,
      "end_offset": 16,
      "type": "word",
      "position": 4
    }
  ]
}
```

## 相關文件

- [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)
- [Kuromoji 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/kuromoji/)
- [Kuromoji 基本形式詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-baseform/)
