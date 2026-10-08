---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Elision
parent: Token filters
nav_order: 130
---

# Elision 詞元篩選器

`elision` 詞元篩選器用於移除特定語言中單字的省略字元。省略 (elision) 通常出現在法文等語言中，這類語言的單字經常會縮寫並與後續單字結合，通常是省略一個母音，並以撇號取代。

`elision` 詞元篩選器已預先設定於下列[語言分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/)中：`catalan`、`french`、`irish` 和 `italian`。
{: .note}

## 參數

自訂 `elision` 詞元篩選器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`articles` | 若未設定 `articles_path` 則為必要 | 字串陣列 | 定義當冠詞或短字作為省略的一部分出現時，應移除哪些冠詞或短字。
`articles_path` | 若未設定 `articles` 則為必要 | 字串 | 指定自訂冠詞清單的路徑，清單中的冠詞會在分析過程中移除。
`articles_case` | 選用 | 布林值 | 指定篩選器在比對省略時是否區分大小寫。預設為 `false`。

## 範例

預設的法文省略集合為 `l'`、`m'`、`t'`、`qu'`、`n'`、`s'`、`j'`、`d'`、`c'`、`jusqu'`、`quoiqu'`、`lorsqu'` 和 `puisqu'`。您可以透過設定 `french_elision` 詞元篩選器來更新此集合。下列範例請求會建立名為 `french_texts` 的新索引，並設定一個使用 `french_elision` 篩選器的分析器：

```json
PUT /french_texts
{
  "settings": {
    "analysis": {
      "filter": {
        "french_elision": {
          "type": "elision",
          "articles": [ "l", "t", "m", "d", "n", "s", "j" ]
        }
      },
      "analyzer": {
        "french_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "french_elision"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "text": {
        "type": "text",
        "analyzer": "french_analyzer"
      }
    }
  }
}

```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用該分析器所產生的詞元：

```json
POST /french_texts/_analyze
{
  "analyzer": "french_analyzer",
  "text": "L'étudiant aime l'école et le travail."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "étudiant",
      "start_offset": 0,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "aime",
      "start_offset": 11,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "école",
      "start_offset": 16,
      "end_offset": 23,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "et",
      "start_offset": 24,
      "end_offset": 26,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "le",
      "start_offset": 27,
      "end_offset": 29,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "travail",
      "start_offset": 30,
      "end_offset": 37,
      "type": "<ALPHANUM>",
      "position": 5
    }
  ]
}
```
