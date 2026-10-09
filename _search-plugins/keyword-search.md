---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "關鍵字搜尋"
has_children: false
nav_order: 10
---

# 關鍵字搜尋

根據預設，OpenSearch 會使用 [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25) 演算法計算文件分數。BM25 是一種以關鍵字為基礎的演算法，會針對查詢中出現的詞彙執行詞彙搜尋。

在判斷文件的相關性時，BM25 會考量[詞頻／逆文件頻率 (TF/IDF)](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)：

- _詞頻_ 指出搜尋詞彙出現頻率越高的文件越相關。

- _逆文件頻率_ 會降低語料庫中所有文件常見詞彙（例如「the」這類冠詞）的權重。

## 範例

下列範例查詢會在 `shakespeare` 索引中搜尋 `long live king` 這些詞彙：

```json
GET shakespeare/_search
{
  "query": {
    "match": {
      "text_entry": "long live king"
    }
  }
}
```
{% include copy-curl.html %}

回應會包含相符的文件，每份文件在 `_score` 欄位中都有相關性分數：

```json
{
  "took": 113,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2352,
      "relation": "eq"
    },
    "max_score": 18.781435,
    "hits": [
      {
        "_index": "shakespeare",
        "_id": "32437",
        "_score": 18.781435,
        "_source": {
          "type": "line",
          "line_id": 32438,
          "play_name": "Hamlet",
          "speech_number": 3,
          "line_number": "1.1.3",
          "speaker": "BERNARDO",
          "text_entry": "Long live the king!"
        }
      },
      {
        "_index": "shakespeare",
        "_id": "83798",
        "_score": 16.523308,
        "_source": {
          "type": "line",
          "line_id": 83799,
          "play_name": "Richard III",
          "speech_number": 42,
          "line_number": "3.7.242",
          "speaker": "BUCKINGHAM",
          "text_entry": "Long live Richard, Englands royal king!"
        }
      },
      {
        "_index": "shakespeare",
        "_id": "82994",
        "_score": 15.588365,
        "_source": {
          "type": "line",
          "line_id": 82995,
          "play_name": "Richard III",
          "speech_number": 24,
          "line_number": "3.1.80",
          "speaker": "GLOUCESTER",
          "text_entry": "live long."
        }
      },
      {
        "_index": "shakespeare",
        "_id": "7199",
        "_score": 15.586321,
        "_source": {
          "type": "line",
          "line_id": 7200,
          "play_name": "Henry VI Part 2",
          "speech_number": 12,
          "line_number": "2.2.64",
          "speaker": "BOTH",
          "text_entry": "Long live our sovereign Richard, Englands king!"
        }
      }
      ...
    ]
  }
}
```

## 相似度演算法

下表列出支援的相似度演算法。

演算法 | 說明
`BM25` | 預設的 OpenSearch [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25) 相似度演算法。
`LegacyBM25` (已棄用) | 較舊的 [LegacyBM25Similarity](https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/lucene/similarity/LegacyBM25Similarity.java) 實作。為回溯相容性而保留。
`boolean` | 為詞彙指派等於其 boost 值的分數。當您希望文件分數取決於詞彙是否相符的二元值時，請使用 `boolean` 相似度。


### OpenSearch 3.0 中 BM25 計分的重要變更

在 OpenSearch 3.0 中，預設相似度演算法已從 `LegacyBM25Similarity` 變更為 Lucene 原生的 `BM25Similarity`。

這項變更提升了與 Lucene 標準的一致性，並簡化了計分行為，但引進了一項重要差異：

- 在 `LegacyBM25Similarity` 中，分數在 `BM25` 公式的分子中包含了額外的常數因子 `k₁ + 1`。

- 在 `BM25Similarity` 中，此常數已移除，以獲得更簡潔的正規化（請參閱 [BM25](https://en.wikipedia.org/wiki/Okapi_BM25) 及對應的 [Lucene GitHub 問題](https://github.com/apache/lucene/issues/9609)）。

- `BM25Similarity` 產生的分數低於 `LegacyBM25Similarity` 產生的分數，通常相差約 `2.2` 倍。

- 排名不受影響，因為此常數因子不會改變文件的相對順序。

- 若要保留舊的計分行為，請明確地將您的欄位或索引設定為使用 `LegacyBM25`（請參閱[設定舊版 BM25 相似度](#configuring-legacy-bm25-similarity)）。


## 指定相似度

您可以在欄位層級設定對應時，於 `similarity` 參數中指定相似度演算法。

例如，下列查詢會為 `boolean_field` 指定 `boolean` 相似度。`bm25_field` 則會指派預設的 `BM25` 相似度：

```json
PUT /testindex
{
  "mappings": {
    "properties": {
      "bm25_field": { 
        "type": "text"
      },
      "boolean_field": {
        "type": "text",
        "similarity": "boolean" 
      }
    }
  }
}
```
{% include copy-curl.html %}

## 設定 BM25 相似度

您可以在索引層級設定 BM25 相似度參數，如下所示：

```json
PUT /testindex
{
  "settings": {
    "index": {
      "similarity": {
        "custom_similarity": {
          "type": "BM25",
          "k1": 1.2,
          "b": 0.75,
          "discount_overlaps": "true"
        }
      }
    }
  }
}
```

`BM25` 相似度支援下列參數。

參數 | 資料類型 | 說明
`k1` | 浮點數 | 決定非線性詞頻正規化（飽和）屬性。預設值為 `1.2`。
`b` | 浮點數 | 決定文件長度將 TF 值正規化的程度。預設值為 `0.75`。
`discount_overlaps` | 布林值 | 決定計算正規化值時是否忽略重疊詞元（位置增量為零的詞元）。預設為 `true`（計算正規化值時不計入重疊詞元）。


## 設定舊版 BM25 相似度

如果您想保留較舊的相似度行為，請將 `LegacyBM25` 指定為相似度 `type`：

```json
PUT /testindex
{
  "settings": {
    "index": {
      "similarity": {
        "default": {
          "type": "LegacyBM25",
          "k1": 1.2,
          "b": 0.75
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

---

## 後續步驟

- 瞭解[查詢與篩選情境]({{site.url}}{{site.baseurl}}/query-dsl/query-filter-context/)。
- 瞭解 OpenSearch 支援的[查詢類型]({{site.url}}{{site.baseurl}}/query-dsl/index/)。