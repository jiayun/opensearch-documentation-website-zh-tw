---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "小寫"
parent: Token filters
nav_order: 260
---

# 小寫詞元篩選器

`lowercase` 詞元篩選器用於將詞元串流中的所有字元轉換為小寫，讓搜尋不區分大小寫。

## 參數

`lowercase` 詞元篩選器可使用下列參數進行設定。

參數 | 必要／選用 | 說明
:--- | :--- | :---
 `language` | 選用 | 指定特定語言的詞元篩選器。有效值為：<br>- [`greek`](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/el/GreekLowerCaseFilter.html) <br>-  [`irish`](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/ga/IrishLowerCaseFilter.html) <br>-  [`turkish`](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/tr/TurkishLowerCaseFilter.html)。<br> 預設為 [Lucene LowerCaseFilter](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/core/LowerCaseFilter.html)。 

## 範例

下列範例請求會建立名為 `custom_lowercase_example` 的新索引。此請求會設定使用 `lowercase` 篩選器的分析器，並將 `language` 指定為 `greek`：

```json
PUT /custom_lowercase_example
{
  "settings": {
    "analysis": {
      "analyzer": {
        "greek_lowercase_example": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["greek_lowercase"]
        }
      },
      "filter": {
        "greek_lowercase": {
          "type": "lowercase",
          "language": "greek"
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
GET /custom_lowercase_example/_analyze
{
  "analyzer": "greek_lowercase_example",
  "text": "Αθήνα ΕΛΛΑΔΑ"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "αθηνα",
      "start_offset": 0,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "ελλαδα",
      "start_offset": 6,
      "end_offset": 12,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```
