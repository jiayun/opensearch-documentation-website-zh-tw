---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋分析器"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/search-analyzer/
nav_order: 240
has_children: false
has_toc: false
---

# search_analyzer 對應參數

`search_analyzer` 對應參數可指定在搜尋時用於 [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 欄位的分析器。這讓編製索引時使用的分析器可以與搜尋時使用的分析器不同，從而對搜尋詞彙的解讀與比對方式提供更大的控制權。

預設情況下，編製索引與搜尋使用相同的分析器。不過，當您想在搜尋時套用較寬鬆或較嚴格的比對規則時，使用自訂的 `search_analyzer` 會很有幫助，例如使用 [`stemming`]({{site.url}}{{site.baseurl}}/analyzers/stemming/)，或只在搜尋時移除停用詞。如需更多資訊與使用案例，請參閱 [搜尋分析器]({{site.url}}{{site.baseurl}}/analyzers/search-analyzers/)。
{: .note}

## 範例

下列範例建立一個欄位，該欄位在編製索引時使用設定了 [`edge_ngram_tokenizer`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/edge-n-gram/) 的 `edge_ngram_analyzer`，並在搜尋時使用 [`standard` 分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/standard/)：

```json
PUT /articles
{
  "settings": {
    "analysis": {
      "analyzer": {
        "edge_ngram_analyzer": {
          "tokenizer": "edge_ngram_tokenizer",
          "filter": ["lowercase"]
        }
      },
      "tokenizer": {
        "edge_ngram_tokenizer": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 10,
          "token_chars": ["letter", "digit"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "edge_ngram_analyzer",
        "search_analyzer": "standard"
      }
    }
  }
}
```
{% include copy-curl.html %}

如需搜尋分析器運作方式的完整說明以及更多範例，請參閱 [搜尋分析器]({{site.url}}{{site.baseurl}}/analyzers/search-analyzers/)。
