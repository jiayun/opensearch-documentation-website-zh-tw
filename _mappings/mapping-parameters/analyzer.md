---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分析器"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/analyzer/
nav_order: 5
has_children: false
has_toc: false
---

# 分析器對應參數

`analyzer` 對應參數指定在為 `text` 欄位編製索引或搜尋該欄位時，用於文字分析的分析器。除非由 `search_analyzer` 對應參數覆寫，否則此分析器會同時處理索引時與搜尋時的分析。如需分析器的詳細資訊，請參閱[文字分析]({{site.url}}{{site.baseurl}}/analyzers/)。

只有 `text` 欄位支援 `analyzer` 對應參數。
{: .important}

無法使用 Update Mapping API 更新現有欄位的 `analyzer` 參數。若要變更現有欄位的分析器，您必須重新為資料編製索引。
{: .warning}

建議您先測試分析器，再將其部署至正式環境。
{: .tip}

## 搜尋引號分析器

`search_quote_analyzer` 參數可讓您專門為片語查詢指定不同的分析器。當您需要在片語搜尋與一般詞彙搜尋中以不同方式處理停用詞時，這項功能特別實用。

若要有效處理含有停用詞的片語查詢，請設定三項分析器設定：

1. 用於編製索引的 `analyzer`，保留所有詞彙，包括停用詞。
2. 用於一般查詢的 `search_analyzer`，篩除停用詞。
3. 用於片語查詢的 `search_quote_analyzer`，保留停用詞。

## 範例

以下範例示範如何使用 `search_quote_analyzer`，在片語查詢與詞彙查詢中以不同方式處理停用詞。

首先，建立具有全部三種分析器類型的索引。`index_analyzer` 會在編製索引時保留所有詞彙，包括「the」和「a」等停用詞。`search_analyzer` 會移除一般詞彙查詢中的停用詞。`search_quote_analyzer` 使用與文件編製索引時相同的分析器，確保精確片語比對能正確運作：

```json
PUT /product_catalog
{
  "settings": {
    "analysis": {
      "analyzer": {
        "index_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase"
          ]
        },
        "search_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "english_stop"
          ]
        }
      },
      "filter": {
        "english_stop": {
          "type": "stop",
          "stopwords": "_english_"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "product_name": {
        "type": "text",
        "analyzer": "index_analyzer",
        "search_analyzer": "search_analyzer",
        "search_quote_analyzer": "index_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

接著，將範例文件新增至索引：

```json
PUT /product_catalog/_doc/1
{
  "product_name": "The Smart Watch Pro"
}
```
{% include copy-curl.html %}

```json
PUT /product_catalog/_doc/2
{
  "product_name": "A Smart Watch Ultra"
}
```
{% include copy-curl.html %}

在您的索引中搜尋片語「the smart watch」（加上引號）：

```json
GET /product_catalog/_search
{
  "query": {
    "query_string": {
      "query": "\"the smart watch\"",
      "default_field": "product_name"
    }
  }
}
```
{% include copy-curl.html %}

由於查詢以引號括住，因此會成為片語查詢，等同於以下查詢：

```json
GET /product_catalog/_search
{
  "query": {
    "match_phrase": {
      "product_name": "the smart watch"
    }
  }
}
```

片語查詢使用 `search_quote_analyzer`，會保留停用詞。因此，查詢「the smart watch」只會比對包含該完整片語的文件，所以回應只包含第一份文件：

```json
{
  "took": 263,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.48081374,
    "hits": [
      {
        "_index": "product_catalog",
        "_id": "1",
        "_score": 0.48081374,
        "_source": {
          "product_name": "The Smart Watch Pro"
        }
      }
    ]
  }
}
```

現在，搜尋符合「the smart watch」的文字（不加引號）：

```json
GET /product_catalog/_search
{
  "query": {
    "query_string": {
      "query": "the smart watch",
      "default_field": "product_name"
    }
  }
}
```
{% include copy-curl.html %}

由於查詢未以引號括住，因此是詞彙層級查詢，等同於以下查詢：

```json
GET /product_catalog/_search
{
  "query": {
    "match": {
      "product_name": "the smart watch"
    }
  }
}
```

詞彙層級查詢使用 `search_analyzer`，會將文字斷詞並移除停用詞。因此，查詢會被分析成詞元 `[smart, watch]`，並比對到兩份文件：

```json
{
  "took": 38,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.16574687,
    "hits": [
      {
        "_index": "product_catalog",
        "_id": "1",
        "_score": 0.16574687,
        "_source": {
          "product_name": "The Smart Watch Pro"
        }
      },
      {
        "_index": "product_catalog",
        "_id": "2",
        "_score": 0.16574687,
        "_source": {
          "product_name": "A Smart Watch Ultra"
        }
      }
    ]
  }
}
```


## 相關文件

- [文字分析]({{site.url}}{{site.baseurl}}/analyzers/)
- [搜尋分析器]({{site.url}}{{site.baseurl}}/analyzers/search-analyzers/)
- [查詢字串查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)