---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Kuromoji
parent: Tokenizers
nav_order: 55
---

# Kuromoji 斷詞器

`kuromoji_tokenizer` 使用 Kuromoji 程式庫與 IPAdic 字典，對日文文字執行基於字典的形態分析。與以空格或標點符號分割的斷詞器不同，它能在日文句子中識別自然的字詞邊界，因為日文不使用空格來分隔字詞。

## 安裝

`kuromoji_tokenizer` 需要 `analysis-kuromoji` 外掛程式。安裝說明請參閱 [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)。

## 參數

下表列出 `kuromoji_tokenizer` 的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`mode` | 字串 | 斷詞模式。有效值為 `normal`、`search` (預設) 與 `extended`。詳細資訊請參閱[斷詞模式](#tokenization-modes)。
`discard_punctuation` | 布林值 | 設為 `true` 時，標點符號詞元會從輸出中捨棄。預設為 `true`。
`discard_compound_token` | 布林值 | 設為 `true` 時，在 `search` 模式下產生的複合詞元會被捨棄，僅保留子詞元。預設為 `false`。
`user_dictionary` | 字串 | 位於 OpenSearch config 目錄中的自訂使用者字典 CSV 檔案路徑。每一行必須遵循 `<text>,<subtokens>,<readings>,<part of speech>` 格式。選用。
`user_dictionary_rules` | 字串陣列 | 以與 `user_dictionary` 相同的 CSV 格式提供的內嵌自訂字典規則。選用。不可與 `user_dictionary` 一起使用。
`nbest_cost` | 整數 | 設為大於 `-1` 的值時，會啟用 n-best 斷詞，並傳回成本 (對數機率懲罰) 與最佳斷詞結果相差不超過此值的替代斷詞結果。預設為 `-1` (停用)。
`nbest_examples` | 字串 | 以逗號分隔的範例字詞清單，用於自動計算 `nbest_cost`。提供此參數時，斷詞器會找出同時將給定範例產生為詞元所需的最小額外成本。選用。

## 斷詞模式

斷詞模式控制斷詞器如何處理複合詞與未知詞。

| 模式 | 複合詞 | 未知詞 |
|:-----|:---------------|:--------------|
| `normal` | 保留為單一詞元 (例如，関西国際空港是一個詞元)。 | 保留為單一詞元。 |
| `search` (預設) | 除了複合形式外，再分割成子詞元 (例如，関西国際空港會產生関西、国際、空港與関西国際空港)。可提升搜尋查詢的召回率。 | 保留為單一詞元。 |
| `extended` | 保留為單一詞元 (與 `normal` 相同)。 | 分割成單字詞元 (個別字元)，確保每個字元都被編製索引。 |

## 範例：基本斷詞

下列範例建立一個索引，其自訂分析器使用預設 `search` 模式的 `kuromoji_tokenizer`：

```json
PUT /kuromoji-tokenizer-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "kuromoji_analyzer": {
          "tokenizer": "kuromoji_tokenizer"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用一句意為「關西國際機場是一座大型機場」的句子來測試斷詞器：

```json
POST /kuromoji-tokenizer-index/_analyze
{
  "analyzer": "kuromoji_analyzer",
  "text": "関西国際空港は大きな空港です"
}
```
{% include copy-curl.html %}

在 `search` 模式下，複合地名関西国際空港 (關西國際機場) 會被分割成其組成部分，同時也保留為複合詞元：

```json
{
  "tokens": [
    {
      "token": "関西",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": "関西国際空港",
      "start_offset": 0,
      "end_offset": 6,
      "type": "word",
      "position": 0,
      "positionLength": 3
    },
    {
      "token": "国際",
      "start_offset": 2,
      "end_offset": 4,
      "type": "word",
      "position": 1
    },
    {
      "token": "空港",
      "start_offset": 4,
      "end_offset": 6,
      "type": "word",
      "position": 2
    },
    {
      "token": "は",
      "start_offset": 6,
      "end_offset": 7,
      "type": "word",
      "position": 3
    },
    {
      "token": "大きな",
      "start_offset": 7,
      "end_offset": 10,
      "type": "word",
      "position": 4
    },
    {
      "token": "空港",
      "start_offset": 10,
      "end_offset": 12,
      "type": "word",
      "position": 5
    },
    {
      "token": "です",
      "start_offset": 12,
      "end_offset": 14,
      "type": "word",
      "position": 6
    }
  ]
}
```

## 範例：比較斷詞模式

下列範例顯示相同文字在不同模式下會如何以不同方式斷詞。為每個模式建立自訂斷詞器並比較輸出：

```json
PUT /kuromoji-mode-comparison
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "kuromoji_normal": {
          "type": "kuromoji_tokenizer",
          "mode": "normal"
        },
        "kuromoji_search": {
          "type": "kuromoji_tokenizer",
          "mode": "search"
        },
        "kuromoji_extended": {
          "type": "kuromoji_tokenizer",
          "mode": "extended"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用包含已知複合詞 (関西国際空港，意為「關西國際機場」) 與未知外來語 (アバクロンビー，意為「Abercrombie」) 的文字進行測試：

**`normal` 模式**

```json
POST /kuromoji-mode-comparison/_analyze
{
  "tokenizer": "kuromoji_normal",
  "text": "関西国際空港とアバクロンビー"
}
```
{% include copy-curl.html %}

在 `normal` 模式下，複合詞関西国際空港保留為單一詞元，未知外來語アバクロンビー也保留為單一詞元：

```json
{
  "tokens": [
    {
      "token": "関西国際空港",
      "start_offset": 0,
      "end_offset": 6,
      "type": "word",
      "position": 0
    },
    {
      "token": "と",
      "start_offset": 6,
      "end_offset": 7,
      "type": "word",
      "position": 1
    },
    {
      "token": "アバクロンビー",
      "start_offset": 7,
      "end_offset": 14,
      "type": "word",
      "position": 2
    }
  ]
}
```

**`search` 模式**

```json
POST /kuromoji-mode-comparison/_analyze
{
  "tokenizer": "kuromoji_search",
  "text": "関西国際空港とアバクロンビー"
}
```
{% include copy-curl.html %}

在 `search` 模式下，複合詞関西国際空港會被分割成子詞元 (関西、国際、空港)，同時也保留為 `positionLength: 3` 的複合詞元。未知外來語アバクロンビー保留為單一詞元，與 `normal` 模式相同：

```json
{
  "tokens": [
    {
      "token": "関西",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": "関西国際空港",
      "start_offset": 0,
      "end_offset": 6,
      "type": "word",
      "position": 0,
      "positionLength": 3
    },
    {
      "token": "国際",
      "start_offset": 2,
      "end_offset": 4,
      "type": "word",
      "position": 1
    },
    {
      "token": "空港",
      "start_offset": 4,
      "end_offset": 6,
      "type": "word",
      "position": 2
    },
    {
      "token": "と",
      "start_offset": 6,
      "end_offset": 7,
      "type": "word",
      "position": 3
    },
    {
      "token": "アバクロンビー",
      "start_offset": 7,
      "end_offset": 14,
      "type": "word",
      "position": 4
    }
  ]
}
```

**`extended` 模式**

```json
POST /kuromoji-mode-comparison/_analyze
{
  "tokenizer": "kuromoji_extended",
  "text": "関西国際空港とアバクロンビー"
}
```
{% include copy-curl.html %}

在 `extended` 模式下，已知複合詞関西国際空港的處理方式與 `search` 模式相同。未知外來語アバクロンビー會被分割成個別字元 (單字詞元)，確保每個字元都被編製索引：

```json
{
  "tokens": [
    {
      "token": "関西",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": "関西国際空港",
      "start_offset": 0,
      "end_offset": 6,
      "type": "word",
      "position": 0,
      "positionLength": 3
    },
    {
      "token": "国際",
      "start_offset": 2,
      "end_offset": 4,
      "type": "word",
      "position": 1
    },
    {
      "token": "空港",
      "start_offset": 4,
      "end_offset": 6,
      "type": "word",
      "position": 2
    },
    {
      "token": "と",
      "start_offset": 6,
      "end_offset": 7,
      "type": "word",
      "position": 3
    },
    {
      "token": "ア",
      "start_offset": 7,
      "end_offset": 8,
      "type": "word",
      "position": 4
    },
    {
      "token": "バ",
      "start_offset": 8,
      "end_offset": 9,
      "type": "word",
      "position": 5
    },
    {
      "token": "ク",
      "start_offset": 9,
      "end_offset": 10,
      "type": "word",
      "position": 6
    },
    {
      "token": "ロ",
      "start_offset": 10,
      "end_offset": 11,
      "type": "word",
      "position": 7
    },
    {
      "token": "ン",
      "start_offset": 11,
      "end_offset": 12,
      "type": "word",
      "position": 8
    },
    {
      "token": "ビ",
      "start_offset": 12,
      "end_offset": 13,
      "type": "word",
      "position": 9
    },
    {
      "token": "ー",
      "start_offset": 13,
      "end_offset": 14,
      "type": "word",
      "position": 10
    }
  ]
}
```

## 範例：使用者字典

您可以將自訂複合詞彙加入斷詞器的字典，以控制它們如何被分割成子詞元。內嵌規則使用 `user_dictionary_rules`，檔案則使用 `user_dictionary`。

下列範例將東京スカイツリー (東京晴空塔) 註冊為單一名詞：

```json
PUT /kuromoji-user-dict-index
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "kuromoji_with_user_dict": {
          "type": "kuromoji_tokenizer",
          "mode": "search",
          "user_dictionary_rules": [
            "東京スカイツリー,東京 スカイツリー,トウキョウ スカイツリー,カスタム名詞"
          ]
        }
      },
      "analyzer": {
        "user_dict_analyzer": {
          "tokenizer": "kuromoji_with_user_dict"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

每個 `user_dictionary_rules` 項目都是一個 CSV 字串，包含四個以逗號分隔的欄位，順序為 `<text>,<subtokens>,<readings>,<part of speech>`。下表說明每個欄位。

| 欄位 | 說明 |
|:---|:---|
| `<text>` | 文件中出現的文字 (例如，`東京スカイツリー`)。 |
| `<subtokens>` | 以空格分隔的子詞元，用於斷詞 (例如，`東京 スカイツリー`)。 |
| `<readings>` | 每個子詞元以空格分隔的片假名讀音 (例如，`トウキョウ スカイツリー`)。 |
| `<part of speech>` | 指派給該詞彙的 IPAdic 詞性標籤 (例如，`カスタム名詞`)。 |

使用分析器測試使用者字典項目：

```json
POST /kuromoji-user-dict-index/_analyze
{
  "analyzer": "user_dict_analyzer",
  "text": "東京スカイツリーに登る"
}
```
{% include copy-curl.html %}

使用者字典控制文字的分割方式。由於規則將 `東京 スカイツリー` 定義為兩個子詞元，斷詞器會輸出東京與スカイツリー作為個別詞元，而不是將東京スカイツリー保留為單一詞元：

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
      "token": "スカイツリー",
      "start_offset": 2,
      "end_offset": 8,
      "type": "word",
      "position": 1
    },
    {
      "token": "に",
      "start_offset": 8,
      "end_offset": 9,
      "type": "word",
      "position": 2
    },
    {
      "token": "登る",
      "start_offset": 9,
      "end_offset": 11,
      "type": "word",
      "position": 3
    }
  ]
}
```

若要將東京スカイツリー保留為單一詞元，請在規則中將它定義為單一子詞元：

```json
"東京スカイツリー,東京スカイツリー,トウキョウスカイツリー,カスタム名詞"
```

## 相關文件

- [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)
- [Kuromoji 詞性詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-part-of-speech/)
