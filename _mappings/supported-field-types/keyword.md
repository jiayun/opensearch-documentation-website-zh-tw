---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Keyword
nav_order: 25
has_children: false
parent: String field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/keyword/
  - /opensearch/supported-field-types/keyword/
  - /field-types/keyword/
---

# Keyword 欄位類型
**於 1.0 版導入**
{: .label .label-purple }

keyword 欄位類型包含未經分析的字串。它僅允許精確且區分大小寫的比對。

預設情況下，keyword 欄位既會編製索引（因為 `index` 已啟用），也會儲存在磁碟上（因為 `doc_values` 已啟用）。若要減少磁碟空間，您可以將 `index` 設定為 `false`，指定不為 keyword 欄位編製索引。

如果您需要使用某個欄位進行全文搜尋，請改將它對應為 [`text`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/text/)。
{: .note }

## 範例

下列查詢會建立一個包含 keyword 欄位的對應。將 `index` 設定為 `false` 表示將 `genre` 欄位儲存在磁碟上，並使用 `doc_values` 來擷取：

```json
PUT movies
{
  "mappings" : {
    "properties" : {
      "genre" : {
        "type" :  "keyword",
        "index" : false
      }
    }
  }
}
```
{% include copy-curl.html %}

## 參數

下表列出 keyword 欄位類型接受的參數。所有參數皆為選用。

| 參數 | 描述 | 預設值 | 可動態更新 |
| :--- | :--- | :--- | :--- |
| `boost` | 指定此欄位對相關性分數權重的浮點數值。高於 `1.0` 的值會提高欄位的相關性。介於 `0.0` 與 `1.0` 之間的值會降低欄位的相關性。 | `1.0` | 是 |
| `doc_values` | 指定欄位是否應儲存在磁碟上，以便用於彙總、排序或指令碼的布林值。 | `true` | 否 |
| `eager_global_ordinals` | 指定是否應在重新整理時立即載入全域序數。如果此欄位經常用於彙總，應將此參數設定為 `true`。 | `false` | 是 |
| `fields` | 若要以多種方式為相同字串編製索引（例如，同時作為 keyword 與 text），請提供 fields 參數。您可以指定一個版本的欄位用於搜尋，另一個版本用於排序與彙總。 | None | 否 |
| `ignore_above` | 長度超過此整數值的字串不應編製索引。預設動態對應會建立一個 keyword 子欄位，其 `ignore_above` 設定為 `256`。 | `2147483647` | 是 |
| `index` | 指定欄位是否應可搜尋的布林值。若要減少磁碟空間，請將 `index` 設定為 `false`。 | `true` | 否 |
| `index_options` | 儲存在索引中，於計算相關性分數時會納入考量的資訊。可設定為 `freqs` 以使用詞彙頻率。 | `docs` | 否 |
| `meta` | 接受此欄位的中繼資料。 | None | 是 |
| [`normalizer`]({{site.url}}{{site.baseurl}}/analyzers/normalizers/) | 指定在編製索引前如何前置處理此欄位（例如，轉為小寫）。 | `null`（無前置處理） | 否 |
| `norms` | 指定計算相關性分數時是否應使用欄位長度的布林值。 | `false` | 是 |
| [`null_value`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/index#null-value) | 用來取代 `null` 的值。必須與欄位屬於相同類型。若未指定此參數，當欄位值為 `null` 時，該欄位會被視為遺漏。 | `null` | 否 |
| `similarity` | 用於計算相關性分數的排名演算法。 | 索引的 `similarity` 設定（預設為 `BM25`） | 否 |
| `use_similarity` | 決定是否計算相關性分數。預設為 `false`，它使用 `constant_score` 以加快查詢速度。將此參數設定為 `true` 會啟用評分，但可能會增加搜尋延遲。請參閱 [use_similarity 參數](#the-use_similarity-parameter)。 | `false` | 是 |
| `split_queries_on_whitespace` | 指定全文查詢是否應以空白字元分割的布林值。 | `false` | 是 |
| `store` | 指定欄位值是否應儲存，並可與 `_source` 欄位分開擷取的布林值。 | `false` | 否 |

## use_similarity 參數

`use_similarity` 參數控制查詢 `keyword` 欄位時，OpenSearch 是否計算相關性分數。預設設定為 `false`，它會使用 `constant_score` 來提升效能。將其設定為 `true` 會啟用根據所設定的相似度演算法（通常為 BM25）進行評分，但可能會增加查詢延遲。

在 `use_similarity` 已停用（預設）的索引上執行 term 查詢：

```json
GET /big5/_search
{
  "size": 3,
  "explain": false,
  "query": {
    "term": {
      "process.name": "kernel"
    }
  },
  "_source": false
}
```
{% include copy-curl.html %}

查詢會快速傳回結果（10 毫秒），且所有文件都會收到 1.0 的固定相關性分數：

```json
{
  "took": 10,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "big5",
        "_id": "xDoCtJQBE3c7bAfikzbk",
        "_score": 1
      },
      {
        "_index": "big5",
        "_id": "xzoCtJQBE3c7bAfikzbk",
        "_score": 1
      },
      {
        "_index": "big5",
        "_id": "yDoCtJQBE3c7bAfikzbk",
        "_score": 1
      }
    ]
  }
}
```

若要為 `process.name` 欄位啟用使用預設 BM25 演算法的評分，請在索引對應中提供 `use_similarity` 參數：

```json
PUT /big5/_mapping
{
  "properties": {
    "process.name": {
      "type": "keyword",
      "use_similarity": true
    }
  }
}
```

當您在已設定的索引上執行相同的 term 查詢時，查詢需要較長時間執行（200 毫秒），且傳回的文件會依據詞彙頻率及其他 BM25 因素而具有不同的相關性分數：

```json
{
  "took" : 200,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10000,
      "relation" : "gte"
    },
    "max_score" : 0.8844931,
    "hits" : [
      {
        "_index" : "big5",
        "_id" : "xDoCtJQBE3c7bAfikzbk",
        "_score" : 0.8844931
      },
      {
        "_index" : "big5",
        "_id" : "xzoCtJQBE3c7bAfikzbk",
        "_score" : 0.8844931
      },
      {
        "_index" : "big5",
        "_id" : "yDoCtJQBE3c7bAfikzbk",
        "_score" : 0.8844931
      }
    ]
  }
}
```

## 衍生來源

當索引使用[衍生來源]({{site.url}}{{site.baseurl}}/field-types/metadata-fields/source/#derived-source)時，OpenSearch 在來源重建期間可能會排序 keyword 值，並移除多值 keyword 欄位中的重複項。

建立一個啟用衍生來源並設定 `name` 欄位的索引：

```json
PUT sample-index1
{
  "settings": {
    "index": {
      "derived_source": {
        "enabled": true
      }
    }
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "keyword"
      }
    }
  }
}
```

將一份包含多個 keyword 值（包括重複值）的文件編製索引至該索引：

```json
PUT sample-index1/_doc/1
{
  "name": ["ba", "ab", "ac", "ba"]
}
```

在 OpenSearch 重建 `_source` 之後，衍生的 `_source` 會移除重複項並依字母順序排序這些值：

```json
{
  "name": ["ab", "ac", "ba"]
}
```

如果欄位對應定義了 [`null_value`]({{site.url}}{{site.baseurl}}/field-types/mapping-parameters/null-value/)，任何匯入的空值都會在重建期間被取代為該值。下列範例示範 `null_value` 如何影響衍生來源的輸出。

建立一個啟用衍生來源，並為 `name` 欄位設定 `null_value` 的索引：

```json
PUT sample-index2
{
  "settings": {
    "index": {
      "derived_source": {
        "enabled": true
      }
    }
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "keyword",
        "null_value": "foo"
      }
    }
  }
}
```

將一份包含空值的文件編製索引至該索引：

```json
PUT sample-index2/_doc/1
{
  "name": [null, "ba", "ab"]
}
```

在 OpenSearch 重建 `_source` 之後，衍生的 `_source` 會取代空值並依字母順序排序這些值：

```json
{
  "name": ["ab", "ba", "foo"]
}
```
