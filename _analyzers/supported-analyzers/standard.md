---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "標準分析器"
parent: Analyzers
nav_order: 50
---

# 標準分析器

`standard` 分析器是 OpenSearch 中用於一般用途全文搜尋的內建預設分析器。它的設計目的是透過有效率地將文字拆解為可搜尋的詞彙，提供一致且不受語言限制的文字處理。

`standard` 分析器會執行下列操作：

- **斷詞**：使用 [`standard`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/standard/) 斷詞器，依據 Unicode 文字分段規則將文字拆分為單字，並處理空格、標點符號及常見的分隔符號。
- **轉換為小寫**：套用 [`lowercase`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/lowercase/) 詞元篩選器，將所有詞元轉換為小寫，確保不論輸入的大小寫為何，都能一致地進行比對。

這樣的組合使 `standard` 分析器非常適合用於為各種自然語言內容編製索引，而不需要針對特定語言進行自訂。


## 範例：使用標準分析器建立索引

您可以在建立索引時，將 `standard` 分析器指派給文字欄位：

```json
PUT /my_standard_index
{
  "mappings": {
    "properties": {
      "my_field": {
        "type": "text",
        "analyzer": "standard"
      }
    }
  }
}
```
{% include copy-curl.html %}


## 參數

`standard` 分析器支援下列選用參數。

| 參數 | 資料類型 | 預設 | 說明 |
|:----------|:-----|:--------|:------------|
| `max_token_length` | 整數 | `255` | 詞元在被拆分之前可具有的最大長度。 |
| `stopwords` | 字串或字串清單 | 無 | 在分析期間要移除的停用詞清單，或[某種語言的預先定義停用詞集]({{site.url}}{{site.baseurl}}/analyzers/token-filters/stop/#predefined-stopword-sets-by-language)。例如：`_english_`。 |
| `stopwords_path` | 字串 | 無 | 包含分析期間所使用之停用詞的檔案路徑。 |

請只使用 `stopwords` 或 `stopwords_path` 其中一個參數。若同時使用兩者，不會傳回錯誤，但只會套用 `stopwords` 參數。
{: .note}

## 範例：含參數的分析器

下列範例會建立 `products` 索引，並設定 `max_token_length` 和 `stopwords` 參數：

```json
PUT /animals
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_manual_stopwords_analyzer": {
          "type": "standard",
          "max_token_length": 10,
          "stopwords": [
            "the", "is", "and", "but", "an", "a", "it"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列 `_analyze` API 請求，查看 `my_manual_stopwords_analyzer` 如何處理文字：

```json
POST /animals/_analyze
{
  "analyzer": "my_manual_stopwords_analyzer",
  "text": "The Turtle is Large but it is Slow"
}
```
{% include copy-curl.html %}

傳回的詞元：

- 已依空格拆分。
- 已轉換為小寫。
- 已移除停用詞。

```json
{
  "tokens": [
    {
      "token": "turtle",
      "start_offset": 4,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "large",
      "start_offset": 14,
      "end_offset": 19,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "slow",
      "start_offset": 30,
      "end_offset": 34,
      "type": "<ALPHANUM>",
      "position": 7
    }
  ]
}
```
