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

# keyword 欄位類型
**於 1.0 版導入**
{: .label .label-purple }

keyword 欄位類型包含未經分析的字串。OpenSearch 會將整個值以單一詞元編製索引，因此查詢只有在欄位包含完全相同的值時才會相符。除非您設定 [normalizer]({{site.url}}{{site.baseurl}}/analyzers/normalizers/)（例如將值轉換為小寫），否則比對會區分大小寫。

keyword 欄位適用於需要篩選、排序或彙總的結構化值，例如識別碼、電子郵件地址、主機名稱、狀態碼、郵遞區號和標籤。例如，keyword 欄位可讓您找出所有狀態為 `shipped` 的訂單，或依狀態統計訂單數量。

預設情況下，keyword 欄位會同時編製索引（因為 `index` 已啟用）並儲存在磁碟上（因為 `doc_values` 已啟用）。若要減少磁碟空間，您可以將 `index` 設定為 `false`，指定不為 keyword 欄位編製索引。

如果您需要將欄位用於全文搜尋，請改為將其對應為 [`text`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/text/)。
{: .note }

## 範例：停用 keyword 欄位的索引編製

下列請求會建立包含 keyword 欄位的對應。將 `index` 設為 `false` 可避免為 `genre` 欄位建立搜尋索引，藉此節省磁碟空間。欄位值仍會儲存在 doc values 中，因此您可以依 `genre` 排序及彙總：

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

## 對應數值識別碼

數值識別碼（例如商店編號、ISBN 或產品 ID）通常更適合對應為 `keyword`，而不是 [numeric]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/) 類型。數值欄位類型針對 `range` 查詢進行最佳化，而 keyword 欄位則針對 `term` 和其他[詞彙層級查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/index/)進行最佳化，後者通常是查詢識別碼的方式。

如果您以精確值查詢數值識別碼，且不會對它執行範圍查詢，請將它對應為 `keyword`。keyword 欄位上的範圍查詢會以字串方式按字母順序比較值。例如，查詢大於或等於 `"50"` 的值會符合 `"9"`，但不會符合 `"100"`。如果您同時需要精確查詢和數值範圍查詢，請使用 [`fields`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/fields/) 將該值同時對應為 `keyword` 和數值欄位。

## 參數

下表列出 keyword 欄位類型可接受的參數。所有參數皆為選用。

| 參數 | 說明 | 預設值 | 可動態更新 |
| :--- | :--- | :--- | :--- |
| `boost` | 一個浮點數值，用來指定此欄位對相關性分數的權重。高於 `1.0` 的值會提高欄位的相關性。介於 `0.0` 與 `1.0` 之間的值會降低欄位的相關性。如需更多資訊，請參閱 [Boost]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/boost/)。 | `1.0` | 是 |
| `doc_values` | 一個布林值，用來指定是否應將欄位儲存在磁碟上，以便用於彙總、排序或指令碼。如需更多資訊，請參閱 [Doc values]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/)。 | `true` | 否 |
| `eager_global_ordinals` | 指定是否應在重新整理時預先載入全域序數。如果此欄位經常被用於彙總，則應將此參數設為 `true`。如需更多資訊，請參閱 [Eager global ordinals]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/eager_global_ordinals/)。 | `false` | 是 |
| `fields` | 若要以多種方式為同一個字串編製索引（例如同時作為 keyword 與 text），請提供 fields 參數。您可以指定欄位的其中一個版本用於搜尋，另一個版本用於排序與彙總。如需更多資訊，請參閱 [Fields]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/fields/)。 | 無 | 否 |
| `ignore_above` | 一個整數值，用來指定字串長度上限。較長的字串既不會被編製索引，也不會寫入 doc values，因此不會符合任何查詢，也不會出現在彙總中。該值仍會保留在 `_source` 中。預設動態對應會建立一個 keyword 子欄位，並將其 `ignore_above` 設為 `256`。如需更多資訊，請參閱 [Ignore above]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/ignore-above/)。 | `2147483647` | 是 |
| `index` | 一個布林值，用來指定此欄位是否可供搜尋。若要減少磁碟空間，請將 `index` 設為 `false`。如需更多資訊，請參閱 [Index]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-parameter/)。 | `true` | 否 |
| `index_options` | 要儲存在索引中、且會在計算相關性分數時納入考量的資訊。可設為 `freqs` 以計算詞彙頻率。如需更多資訊，請參閱 [Index options]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-options/)。 | `docs` | 否 |
| `meta` | 接受此欄位的中繼資料。如需更多資訊，請參閱 [Meta]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/meta/)。 | 無 | 是 |
| `normalizer` | 指定在編製索引前如何前置處理此欄位（例如將其轉為小寫）。如需更多資訊，請參閱 [Normalizer]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/normalizer/)。 | `null`（不進行前置處理） | 否 |
| `norms` | 一個布林值，用來指定計算相關性分數時是否應使用欄位長度。如需更多資訊，請參閱 [Norms]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/norms/)。 | `false` | 是 |
| `null_value` | 用來替代 `null` 的值。其類型必須與欄位相同。若未指定此參數，當欄位值為 `null` 時，該欄位會被視為缺少值。如需更多資訊，請參閱 [Null value]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/null-value/)。 | `null` | 否 |
| `similarity` | 用於計算相關性分數的排名演算法。如需更多資訊，請參閱 [Similarity]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/similarity/)。 | 索引的 `similarity` 設定（預設為 `BM25`） | 否 |
| `use_similarity` | 決定是否計算相關性分數。預設為 `false`，其使用 `constant_score` 以加快查詢速度。將此參數設為 `true` 會啟用評分，但可能增加搜尋延遲。請參閱 [The use_similarity parameter ](#the-use_similarity-parameter)。 | `false` | 是 |
| `split_queries_on_whitespace` | 一個布林值，用來指定全文查詢是否應以空白字元分割。 | `false` | 是 |
| `store` | 一個布林值，用來指定是否應儲存欄位值，且可與 `_source` 欄位分開擷取。如需更多資訊，請參閱 [Store]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/store/)。 | `false` | 否 |

## use_similarity 參數 

`use_similarity` 參數控制 OpenSearch 在查詢 `keyword` 欄位時是否計算相關性分數。預設值為 `false`，透過使用 `constant_score` 來提升效能。將其設為 `true` 可啟用基於所設定的相似度演算法（通常是 BM25）的評分，但可能會增加查詢延遲。

建立一個包含 `brand` keyword 欄位的索引：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "brand": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

為四份文件編製索引，其中兩份具有相同的 `brand` 值：

```json
POST /products/_bulk?refresh=true
{ "index": { "_id": "1" } }
{ "brand": "Acme" }
{ "index": { "_id": "2" } }
{ "brand": "Acme" }
{ "index": { "_id": "3" } }
{ "brand": "Globex" }
{ "index": { "_id": "4" } }
{ "brand": "Initech" }
```
{% include copy-curl.html %}

在 `brand` 欄位上執行 `term` 查詢，該欄位的 `use_similarity` 已停用（預設）：

```json
GET /products/_search
{
  "query": {
    "term": {
      "brand": "Acme"
    }
  },
  "_source": false
}
```
{% include copy-curl.html %}

所有符合的文件都會得到 `1` 的固定相關性分數：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "products",
        "_id": "1",
        "_score": 1
      },
      {
        "_index": "products",
        "_id": "2",
        "_score": 1
      }
    ]
  }
}
```

若要為 `brand` 欄位啟用使用預設 BM25 演算法的評分，請在索引對應中設定 `use_similarity` 參數。由於 `use_similarity` 可動態更新，您可以在現有索引上變更它：

```json
PUT /products/_mapping
{
  "properties": {
    "brand": {
      "type": "keyword",
      "use_similarity": true
    }
  }
}
```
{% include copy-curl.html %}

再次執行相同的 `term` 查詢時，文件會得到 BM25 相關性分數，而不是固定分數。由於 keyword 欄位只包含單一詞彙，所有符合相同值的文件都會得到相同的分數。：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.31506687,
    "hits": [
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.31506687
      },
      {
        "_index": "products",
        "_id": "2",
        "_score": 0.31506687
      }
    ]
  }
}
```

## 衍生的來源

當索引使用[衍生的來源]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/#derived-source)時，OpenSearch 可能會在來源重建期間排序 keyword 值，並移除多重值 keyword 欄位中的重複項目。

建立一個啟用衍生的來源並設定 `tags` 欄位的索引：

```json
PUT tagged-products
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
      "tags": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

將含有重複項目的多個 keyword 值文件編製索引至該索引：

```json
PUT tagged-products/_doc/1
{
  "tags": ["sale", "clearance", "new-arrival", "sale"]
}
```
{% include copy-curl.html %}

在 OpenSearch 重建 `_source` 之後，衍生的 `_source` 會移除重複項目並依字母順序排序這些值：

```json
{
  "tags": ["clearance", "new-arrival", "sale"]
}
```

如果欄位對應定義了[`null_value`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/null-value/)，則在重建期間，任何匯入的 null 值都會被取代為該值。下列範例示範 `null_value` 如何影響衍生的來源輸出。

建立一個啟用衍生的來源並為 `tags` 欄位設定 `null_value` 的索引：

```json
PUT tagged-products-null
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
      "tags": {
        "type": "keyword",
        "null_value": "untagged"
      }
    }
  }
}
```
{% include copy-curl.html %}

將含有 null 值的文件編製索引至該索引：

```json
PUT tagged-products-null/_doc/1
{
  "tags": [null, "sale", "clearance"]
}
```
{% include copy-curl.html %}

在 OpenSearch 重建 `_source` 之後，衍生的 `_source` 會取代 null 值並依字母順序排序這些值：

```json
{
  "tags": ["clearance", "sale", "untagged"]
}
```
