---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Edge n-gram
parent: Tokenizers
nav_order: 40
---

# Edge n-gram 斷詞器

`edge_ngram` 斷詞器會從每個單字的開頭產生部分單字詞元，也就是 _n-gram_。它會依據指定的字元分割文字，並在定義的最小與最大長度範圍內產生詞元。此斷詞器特別適合用來實作即打即搜 (search-as-you-type) 功能。

Edge n-gram 非常適合單字順序可能不同的自動完成搜尋，例如搜尋產品名稱或地址時。如需詳細資訊，請參閱[自動完成]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/autocomplete/)。不過，對於順序固定的文字，例如電影或歌曲名稱，completion suggester 可能會更精確。

根據預設，`edge n-gram` 斷詞器產生的詞元最小長度為 `1`，最大長度為 `2`。例如，分析文字 `OpenSearch` 時，預設組態會產生 `O` 和 `Op` 這兩個 n-gram。這類短 n-gram 通常會比對到太多不相關的詞彙，因此必須設定斷詞器以調整 n-gram 長度。

## 使用範例

下列範例請求會建立名為 `my_index` 的新索引，並設定使用 `edge_ngram` 斷詞器的分析器。此斷詞器會產生長度為 3 至 6 個字元的詞元，並將字母和符號都視為有效的詞元字元：

```json
PUT /edge_n_gram_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": {
          "tokenizer": "my_custom_tokenizer"
        }
      },
      "tokenizer": {
        "my_custom_tokenizer": {
          "type": "edge_ngram",
          "min_gram": 3,
          "max_gram": 6,
          "token_chars": [
            "letter"          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用此分析器產生的詞元：

```json
POST /edge_n_gram_index/_analyze
{
  "analyzer": "my_custom_analyzer",
  "text": "Code 42 rocks!"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "Cod",
      "start_offset": 0,
      "end_offset": 3,
      "type": "word",
      "position": 0
    },
    {
      "token": "Code",
      "start_offset": 0,
      "end_offset": 4,
      "type": "word",
      "position": 1
    },
    {
      "token": "roc",
      "start_offset": 8,
      "end_offset": 11,
      "type": "word",
      "position": 2
    },
    {
      "token": "rock",
      "start_offset": 8,
      "end_offset": 12,
      "type": "word",
      "position": 3
    },
    {
      "token": "rocks",
      "start_offset": 8,
      "end_offset": 13,
      "type": "word",
      "position": 4
    }
  ]
}
```

## 參數

| 參數           | 必要/選用 | 資料類型        | 說明    |
|:-------|:--------|:------|:---|
| `min_gram`          | 選用          | 整數          | 最小詞元長度。預設值為 `1`。                                                    |
| `max_gram`          | 選用          | 整數          | 最大詞元長度。預設值為 `2`。                                                    |
| `custom_token_chars`| 選用          | 字串           | 定義要視為詞元一部分的自訂字元 (例如 `+-_`)。                    |
| `token_chars`       | 選用          | 字串陣列 | 定義要包含在詞元中的字元類別。詞元會在不屬於這些類別的字元處分割。預設包含所有字元。可用的類別包括：<br> - `letter`：字母字元 (例如 `a`、`ç` 或 `京`) <br> - `digit`：數字字元 (例如 `3` 或 `7`) <br>- `punctuation`：標點符號 (例如 `!` 或 `?`) <br> - `symbol`：其他符號 (例如 `$` 或 `√`) <br> - `whitespace`：空白或換行字元 <br> - `custom`：可讓您在 `custom_token_chars` 設定中指定自訂字元。 |

<!-- vale off -->
## max_gram 參數的限制
<!-- vale on -->

`max_gram` 參數會設定斷詞器所產生詞元的最大長度。當搜尋查詢超過此長度時，可能無法比對到索引中的任何詞彙。

例如，若將 `max_gram` 設為 `4`，則在編製索引期間，查詢 `explore` 會被斷詞為 `expl`。因此，搜尋完整詞彙 `explore` 將不會比對到已編製索引的詞元 `expl`。

若要解決此限制，您可以套用 `truncate` 詞元篩選器，將搜尋詞彙縮短至最大詞元長度。不過，這種做法需要有所取捨。將 `explore` 截斷為 `expl` 可能會比對到不相關的詞彙，例如 `explosion` 或 `explicit`，進而降低搜尋精確度。

建議您謹慎權衡 `max_gram` 的值，以確保有效率的斷詞，同時盡量減少不相關的比對結果。若精確度至關重要，請考慮其他策略，例如調整查詢分析器或微調篩選器。

## 最佳實務

建議您僅在編製索引時使用 `edge_ngram` 斷詞器，以確保儲存部分單字詞元。在搜尋時，應使用基本的分析器來比對所有查詢詞彙。

## 設定即打即搜功能

若要實作即打即搜功能，請在編製索引期間使用 `edge_ngram` 斷詞器，並在搜尋時使用僅執行最少處理的分析器。下列範例示範了此做法。

建立使用 `edge_ngram` 斷詞器的索引：


```json
PUT /my-autocomplete-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "autocomplete": {
          "tokenizer": "autocomplete",
          "filter": [
            "lowercase"
          ]
        },
        "autocomplete_search": {
          "tokenizer": "lowercase"
        }
      },
      "tokenizer": {
        "autocomplete": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 10,
          "token_chars": [
            "letter"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "autocomplete",
        "search_analyzer": "autocomplete_search"
      }
    }
  }
}
```
{% include copy-curl.html %}

將包含 `product` 欄位的文件編製索引，並重新整理索引：

```json
PUT my-autocomplete-index/_doc/1?refresh
{
  "title": "Laptop Pro"
}
```
{% include copy-curl.html %}

此組態可確保 `edge_ngram` 斷詞器將「Laptop」之類的詞彙拆分為 `La`、`Lap` 和 `Lapt` 等詞元，讓搜尋時能進行部分比對。在搜尋時，`standard` 斷詞器會簡化查詢，同時由於小寫篩選器的作用，確保比對不區分大小寫。

現在，搜尋 `laptop Pr` 或 `lap pr` 時，都能根據部分比對擷取相關文件：

```json
GET my-autocomplete-index/_search
{
  "query": {
    "match": {
      "title": {
        "query": "lap pr",
        "operator": "and"
      }
    }
  }
}
```
{% include copy-curl.html %}

如需詳細資訊，請參閱[即打即搜]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/autocomplete/#search-as-you-type)。