---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: KStem
parent: Token filters
nav_order: 220
---

# KStem 詞元篩選器

`kstem` 詞元篩選器是一種詞幹提取篩選器，用於將單字還原為其字根形式。此篩選器是專為英文設計的輕量級演算法詞幹提取器，會執行下列詞幹提取操作：

- 將複數形式還原為單數形式。
- 將不同的動詞時態轉換為其基本形式。
- 移除常見的衍生字尾，例如「-ing」或「-ed」。

`kstem` 詞元篩選器等同於以 `light_english` 語言設定的 `stemmer` 篩選器。與 `porter_stem` 等其他詞幹提取篩選器相比，它提供較為保守的詞幹提取。

`kstem` 詞元篩選器以 Lucene KStemFilter 為基礎。如需更多資訊，請參閱 [Lucene 文件](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/en/KStemFilter.html)。

## 範例

下列範例請求會建立名為 `my_kstem_index` 的新索引，並設定具有 `kstem` 篩選器的分析器：

```json
PUT /my_kstem_index
{
  "settings": {
    "analysis": {
      "filter": {
        "kstem_filter": {
          "type": "kstem"
        }
      },
      "analyzer": {
        "my_kstem_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "kstem_filter"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "my_kstem_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
POST /my_kstem_index/_analyze
{
  "analyzer": "my_kstem_analyzer",
  "text": "stops stopped"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "stop",
      "start_offset": 0,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "stop",
      "start_offset": 6,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```