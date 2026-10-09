---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指令碼分數"
parent: Specialized queries
nav_order: 60
---

# Script score 查詢

使用 `script_score` 查詢，透過指令碼自訂分數計算。對於成本高昂的評分函式，您可以使用 `script_score` 查詢，僅為已篩選的回傳文件計算分數。

## 範例

例如，下列請求會建立一個包含一份文件的索引：

```json
PUT testindex1/_doc/1
{
  "name": "John Doe",
  "multiplier": 0.5
}
```
{% include copy-curl.html %}

您可以使用 `match` 查詢，回傳 `name` 欄位中包含 `John` 的所有文件：

```json
GET testindex1/_search
{
  "query": {
    "match": {
      "name": "John"
    }
  }
}
```
{% include copy-curl.html %}

在回應中，文件 1 的分數為 `0.2876821`：

```json
{
  "took": 7,
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
    "max_score": 0.2876821,
    "hits": [
      {
        "_index": "testindex1",
        "_id": "1",
        "_score": 0.2876821,
        "_source": {
          "name": "John Doe",
          "multiplier": 0.5
        }
      }
    ]
  }
}
```

現在讓我們使用一個指令碼來變更文件分數，該指令碼將分數計算為 `_score` 欄位的值乘以 `multiplier` 欄位的值。在下列查詢中，您可以在 `_score` 變數中存取文件的目前相關性分數，並以 `doc['multiplier'].value` 存取 `multiplier` 值：

```json
GET testindex1/_search
{
  "query": {
    "script_score": {
      "query": {
        "match": { 
            "name": "John" 
        }
      },
      "script": {
        "source": "_score * doc['multiplier'].value"
      }
    }
  }
}
```
{% include copy-curl.html %}

在回應中，文件 1 的分數是原始分數的一半：

```json
{
  "took": 8,
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
    "max_score": 0.14384104,
    "hits": [
      {
        "_index": "testindex1",
        "_id": "1",
        "_score": 0.14384104,
        "_source": {
          "name": "John Doe",
          "multiplier": 0.5
        }
      }
    ]
  }
}
```

## 參數

`script_score` 查詢支援下列頂層參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`query` | 物件 | 用於搜尋的查詢。必要。
`script` | 物件 | 用於計算 `query` 所回傳文件分數的指令碼。必要。
`min_score` | 浮點數 | 從結果中排除分數低於 `min_score` 的文件。選用。
`boost` | 浮點數 | 以給定的乘數提高文件分數。小於 1.0 的值會降低相關性，大於 1.0 的值會提高相關性。預設為 1.0。 

`script_score` 查詢計算出的相關性分數不能為負數。 
{: .important}

## 使用內建函式自訂分數計算

若要自訂分數計算，您可以使用其中一個內建 Painless 函式。對於每個函式，OpenSearch 都提供一或多個您可以在 script score 情境中存取的 Painless 方法。您可以直接呼叫下列章節所列的 Painless 方法，無需使用類別名稱或執行個體名稱限定詞。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

### 飽和函式

飽和函式將飽和度計算為 `score = value /(value + pivot)`，其中 `value` 是欄位值，`pivot` 的選擇方式是使分數在 `value` 大於 `pivot` 時大於 0.5，在 `value` 小於 `pivot` 時小於 0.5。分數位於 (0, 1) 範圍內。若要套用飽和函式，請呼叫下列 Painless 方法：

- `double saturation(double <field-value>, double <pivot>)`
    
#### 範例

下列範例查詢在 `articles` 索引中搜尋文字 `neural search`。它將文件的原始相關性分數與 `article_rank` 值結合，該值會先以飽和函式轉換：

```json
GET articles/_search
{
  "query": {
    "script_score": {
      "query": {
        "match": { "article_name": "neural search" }
      },
      "script" : {
        "source" : "_score + saturation(doc['article_rank'].value, 11)"
      }
    }
  }
}
```
{% include copy-curl.html %}

### S 型函式

與飽和函式類似，S 型函式將分數計算為 `score = value^exp/ (value^exp + pivot^exp)`，其中 `value` 是欄位值，`exp` 是指數縮放因子，`pivot` 的選擇方式是使分數在 `value` 大於 `pivot` 時大於 0.5，在 `value` 小於 `pivot` 時小於 0.5。若要套用 S 型函式，請呼叫下列 Painless 方法：

- `double sigmoid(double <field-value>, double <pivot>, double <exp>)`

#### 範例

下列範例查詢在 `articles` 索引中搜尋文字 `neural search`。它將文件的原始相關性分數與 `article_rank` 值結合，該值會先以 sigmoid 函式轉換：

```json
GET articles/_search
{
  "query": {
    "script_score": {
      "query": {
        "match": { "article_name": "neural search" }
      },
      "script" : {
        "source" : "_score + sigmoid(doc['article_rank'].value, 11, 2)"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 隨機分數

隨機分數函式會產生在 [0, 1) 範圍內均勻分布的隨機分數。若要了解此函式的運作方式，請參閱 [隨機分數函式]({{site.url}}{{site.baseurl}}/query-dsl/compound/function-score#the-random-score-function)。若要套用隨機分數函式，請呼叫下列其中一個 Painless 方法：

- `double randomScore(int <seed>)`：使用內部 Lucene 文件 ID 作為種子值。
- `double randomScore(int <seed>, String <field-name>)`

#### 範例

下列查詢使用 `random_score` 函式搭配 `seed` 和 `field`：

```json
GET articles/_search
{
  "query": {
    "script_score": {
      "query": {
        "match": { "article_name": "neural search" }
      },
      "script" : {
          "source" : "randomScore(20, '_seq_no')"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 衰減函式

透過衰減函式，您可以根據接近度或新近度為結果評分。若要了解更多，請參閱 [衰減函式]({{site.url}}{{site.baseurl}}/query-dsl/compound/function-score#decay-functions)。您可以使用指數、高斯或線性衰減曲線來計算分數。若要套用衰減函式，請根據欄位類型呼叫下列其中一個 Painless 方法：

- [數值]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/) 欄位： 
    - `double decayNumericGauss(double <origin>, double <scale>, double <offset>, double <decay>, double <field-value>)`
    - `double decayNumericExp(double <origin>, double <scale>, double <offset>, double <decay>, double <field-value>)`
    - `double decayNumericLinear(double <origin>, double <scale>, double <offset>, double <decay>, double <field-value>)`
- [地理點]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-point/) 欄位： 
    - `double decayGeoGauss(String <origin>, String <scale>, String <offset>, double <decay>, GeoPoint <field-value>)`
    - `double decayGeoExp(String <origin>, String <scale>, String <offset>, double <decay>, GeoPoint <field-value>)`
    - `double decayGeoLinear(String <origin>, String <scale>, String <offset>, double <decay>, GeoPoint <field-value>)`
- [日期]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/) 欄位： 
    - `double decayDateGauss(String <origin>, String <scale>, String <offset>, double <decay>, JodaCompatibleZonedDateTime <field-value>)`
    - `double decayDateExp(String <origin>, String <scale>, String <offset>, double <decay>, JodaCompatibleZonedDateTime <field-value>)`
    - `double decayDateLinear(String <origin>, String <scale>, String <offset>, double <decay>, JodaCompatibleZonedDateTime <field-value>)`

#### 範例：數值欄位

下列查詢會在數值欄位上使用指數衰減函式：

```json
GET articles/_search
{
  "query": {
    "script_score": {
      "query": {
        "match": {
          "article_name": "neural search"
        }
      },
      "script": {
        "source": "decayNumericExp(params.origin, params.scale, params.offset, params.decay, doc['article_rank'].value)",
        "params": {
          "origin": 50,
          "scale": 20,
          "offset": 30,
          "decay": 0.5
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 範例：地理點欄位

下列查詢會在地理點欄位上使用高斯衰減函式：

```json
GET hotels/_search
{
  "query": {
    "script_score": {
      "query": {
        "match": {
          "name": "hotel"
        }
      },
      "script": {
        "source": "decayGeoGauss(params.origin, params.scale, params.offset, params.decay, doc['location'].value)",
        "params": {
          "origin": "40.71,74.00",
          "scale":  "300ft",
          "offset": "200ft",
          "decay": 0.25
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 範例：日期欄位

下列查詢會在日期欄位上使用線性衰減函式：

```json
GET blogs/_search
{
  "query": {
    "script_score": {
      "query": {
        "match": {
          "name": "opensearch"
        }
      },
      "script": {
        "source": "decayDateLinear(params.origin, params.scale, params.offset, params.decay, doc['date_posted'].value)",
        "params": {
          "origin":  "2022-04-24",
          "scale":  "6d",
          "offset": "1d",
          "decay": 0.25
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 詞彙頻率函式

詞彙頻率函式會在評分指令碼來源中公開詞彙層級的統計資料。您可以使用這些統計資料來實作自訂的資訊檢索與排名演算法，例如依熱門程度在查詢時進行乘法或加法的分數加成。若要套用詞彙頻率函式，請呼叫下列其中一個 Painless 方法：

- `int termFreq(String <field-name>, String <term>)`：擷取特定詞彙在欄位內的詞彙頻率。
- `long totalTermFreq(String <field-name>, String <term>)`：擷取特定詞彙在欄位內的總詞彙頻率。
- `long sumTotalTermFreq(String <field-name>)`：擷取欄位內總詞彙頻率的總和。

#### 範例

下列查詢會將分數計算為 `fields` 清單中每個欄位的總詞彙頻率乘以 `multiplier` 值：

```json
GET /demo_index_v1/_search
{
  "query": {
    "function_score": {
      "query": {
        "match_all": {}
      },
      "script_score": {
        "script": {
          "source": """
            for (int x = 0; x < params.fields.length; x++) {
              String field = params.fields[x];
              if (field != null) {
                return params.multiplier * totalTermFreq(field, params.term);
              }
            }
            return params.default_value;
            
          """,
          "params": {
              "fields": ["title", "description"],
              "term": "ai",
              "multiplier": 2,
              "default_value": 1
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 後期互動分數

`lateInteractionScore` 函式是一種 Painless 指令碼評分函式，會使用詞元層級的向量比對來計算文件相關性。它會將每個查詢向量與所有文件向量進行比較，找出每個查詢向量的最大相似度，並將這些最大分數加總，以產生最終的文件分數。

**分數計算範例**：
- 查詢向量：`[[0.8, 0.1], [0.2, 0.9]]`
- 文件向量：`[[0.7, 0.2], [0.1, 0.8], [0.3, 0.4]]`
- 查詢向量 1 → 在文件向量中找出最佳符合項目 → 分數 A
- 查詢向量 2 → 在文件向量中找出最佳符合項目 → 分數 B
- 最終分數 = A + B

此方法可讓查詢與文件之間進行細緻的語意比對，因此特別適合用來重新排序搜尋結果。

#### 索引對應需求

向量欄位必須對應為 `object` (建議) 或 `float` 類型。

我們建議將向量欄位對應為具有 `"enabled": false` 的 `object`，因為它會儲存原始向量而不進行解析，可提升效能：

```json
{
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "object",
        "enabled": false
      }
    }
  }
}
```

或者，您也可以將向量欄位對應為 `float`：

```json
{
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "float"
      }
    }
  }
}
```

#### 範例

下列範例示範如何使用 `lateInteractionScore` 函式搭配餘弦相似度，根據方向而非距離來衡量向量相似度：

```json
GET my_index/_search
{
  "query": {
    "script_score": {
      "query": { "match_all": {} },
      "script": {
        "source": "lateInteractionScore(params.query_vectors, 'my_vector', params._source, params.space_type)",
        "params": {
          "query_vectors": [[1.0, 0.0], [0.0, 1.0]],
          "space_type": "cosinesimil"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 參數

`lateInteractionFunction` 支援下列參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `query_vectors` | 陣列的陣列 | 是 | 用於相似度比對的查詢向量 |
| `vector_field` | 字串 | 是 | 包含向量的文件欄位名稱 |
| `doc` | Map | 是 | 文件來源（請使用 `params._source`） |
| `space_type` | 字串 | 否 | 相似度計量。預設：`"l2"` |

`space_type` 參數會決定相似度的計算方式，並接受下列有效值。

| 空間類型 | 說明 | 分數越高代表 |
| :--- | :--- | :--- |
| `innerproduct` | 點積 | 向量越相似 |
| `cosinesimil` | 餘弦相似度 | 方向越相似 |
| `l2`（預設） | 歐幾里得距離 | 向量越接近（反轉） |

如需完整範例，請參閱[使用外部託管的後期互動模型依欄位重新排序]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-by-field-late-interaction/)。

如果 [`search.allow_expensive_queries`]({{site.url}}{{site.baseurl}}/query-dsl/index/#expensive-queries) 設為 `false`，則不會執行 `script_score` 查詢。
{: .important}