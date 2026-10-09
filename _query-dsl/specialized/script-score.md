---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指令碼分數"
parent: Specialized queries
nav_order: 60
---

# 指令碼分數查詢

使用 `script_score` 查詢，將每個相符文件的相關性分數替換為由指令碼計算出的值。被包裝的查詢會決定哪些文件相符，而指令碼只會在這些文件上執行。這使得 `script_score` 查詢非常適合用於對整個索引執行成本過高的評分邏輯。

在下列情境中使用 `script_score` 查詢：

- 將文字相關性與文件中儲存的數值訊號（例如熱門程度、評分或排名）結合。
- 使用衰減函式，讓日期、位置或數值接近目標值的文件獲得較高分數。
- 根據詞彙統計資料或向量相似度實作自訂排名公式。
- 在單一指令碼中重現 [`function_score`]({{site.url}}{{site.baseurl}}/query-dsl/compound/function-score/) 查詢的評分函式。

## 範例

下列請求會建立包含一份文件的索引：

```json
PUT testindex1/_doc/1
{
  "name": "John Doe",
  "multiplier": 0.5
}
```
{% include copy-curl.html %}

下列 `match` 查詢會傳回所有在 `name` 欄位中包含 `John` 的文件：

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

在回應中，文件 1 的分數為 `0.13076457`：

```json
{
  "took": 1,
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
    "max_score": 0.13076457,
    "hits": [
      {
        "_index": "testindex1",
        "_id": "1",
        "_score": 0.13076457,
        "_source": {
          "name": "John Doe",
          "multiplier": 0.5
        }
      }
    ]
  }
}
```

若要變更文件分數，請將 `match` 查詢包裝在 `script_score` 查詢中。在指令碼內，`_score` 變數會保存被包裝查詢所計算出的相關性分數，而 `doc['multiplier'].value` 會讀取 `multiplier` 欄位值。下列查詢會將這兩個值相乘：

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
  "took": 2,
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
    "max_score": 0.06538229,
    "hits": [
      {
        "_index": "testindex1",
        "_id": "1",
        "_score": 0.06538229,
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

`script_score` 查詢支援下列最上層參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`query` | 物件 | 選取要評分之文件的查詢。必要。
`script` | 物件 | 用來計算 `query` 所傳回文件分數的指令碼。支援內嵌與已儲存的指令碼。如需更多資訊，請參閱[如何使用指令碼]({{site.url}}{{site.baseurl}}/scripting/using-scripts/)。必要。
`min_score` | 浮點數 | 從結果中排除分數低於 `min_score` 的文件。分數會在套用 `boost` 之後與 `min_score` 比較。選用。
`boost` | 浮點數 | 將指令碼傳回的分數相乘。小於 1.0 的值會降低相關性，大於 1.0 的值會提高相關性。預設為 1.0。

請透過 `params` 物件將會變動的值傳入指令碼，並避免將這些值寫入 `source`。OpenSearch 會依原始碼快取已編譯的指令碼，因此原始碼維持不變的指令碼只會編譯一次，即使其參數值變更也一樣。如需更多資訊，請參閱[編譯限制與快取]({{site.url}}{{site.baseurl}}/scripting/using-scripts/#compilation-limits-and-caching)。

`script_score` 查詢所計算出的相關性分數不能為負數。如果指令碼傳回負值，搜尋會失敗並出現類似 `script_score script returned an invalid score [-1.0] for doc [0]. Must be a non-negative score!` 的錯誤。
{: .important}

如果指令碼讀取文件中缺少的欄位，`doc['<field>'].value` 會擲回錯誤。若要處理缺少的值，請在讀取值之前檢查 `doc['<field>'].size() == 0`。如需範例，請參閱[欄位值因子函式](#the-field-value-factor-function)。

## 使用內建函式自訂分數計算

若要自訂分數計算，您可以使用其中一個內建的 Painless 函式。針對每個函式，OpenSearch 會提供一或多個您可以在指令碼分數情境中存取的 Painless 方法。您可以直接呼叫下列各節所列的 Painless 方法，而不需要使用類別名稱或執行個體名稱限定詞。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

當內建函式涵蓋您的使用情境時，請優先使用它，而非以 Painless 撰寫的等效公式。內建函式是以 Java 實作，而衰減函式只會剖析其 origin、scale 與 offset 一次，不會對每份文件重複此工作。

### 飽和

飽和函式的計算方式為 `score = value /(value + pivot)`，其中 `value` 是欄位值，而 `pivot` 的選擇會使得當 `value` 大於 `pivot` 時分數大於 0.5，且當 `value` 小於 `pivot` 時分數小於 0.5。分數會落在 (0, 1) 範圍內。若要套用飽和函式，請呼叫下列 Painless 方法：

- `double saturation(double <field-value>, double <pivot>)`
    
#### 範例

下列範例查詢會在 `articles` 索引中搜尋文字 `neural search`。它會將原始文件相關性分數與 `article_rank` 值結合，而該值會先以飽和函式轉換：

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

### S 型

與飽和函式類似，S 型函式的計算方式為 `score = value^exp/ (value^exp + pivot^exp)`，其中 `value` 是欄位值，`exp` 是指數縮放因子，而 `pivot` 的選擇會使得當 `value` 大於 `pivot` 時分數大於 0.5，且當 `value` 小於 `pivot` 時分數小於 0.5。若要套用 S 型函式，請呼叫下列 Painless 方法：

- `double sigmoid(double <field-value>, double <pivot>, double <exp>)`

#### 範例

下列範例查詢會在 `articles` 索引中搜尋文字 `neural search`。它會將原始文件相關性分數與 `article_rank` 值結合，而該值會先以 S 型函式轉換：

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

隨機分數函式會產生均勻分布於 [0, 1) 範圍內的隨機分數。若要了解此函式的運作方式，請參閱[隨機分數函式]({{site.url}}{{site.baseurl}}/query-dsl/compound/function-score#the-random-score-function)。若要套用隨機分數函式，請呼叫下列其中一個 Painless 方法：

- `double randomScore(int <seed>)`：使用內部 Lucene 文件 ID 作為隨機性來源。
- `double randomScore(int <seed>, String <field-name>)`：使用指定欄位的值作為隨機性來源。

請根據以下考量選擇隨機性來源：

- 內部 Lucene 文件 ID 讀取速度快，但分段合併可能會重新編號。因此，相同的種子隨著時間可能產生不同的順序。
- 同一分片中具有相同欄位值的文件會得到相同的分數，因此請選擇在每個分片內值皆唯一的欄位。
- `_seq_no` 欄位在分片內是唯一的，但其值在每次文件更新時都會改變。因此，更新後的文件會得到新的隨機分數。

#### 範例

下列查詢使用 `random_score` 函式搭配 `seed` 與 `field`：

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

透過衰減函式，您可以根據接近度或新近度為結果評分。若要了解更多，請參閱[衰減函式]({{site.url}}{{site.baseurl}}/query-dsl/compound/function-score#decay-functions)。您可以使用指數、高斯或線性衰減曲線來計算分數。若要套用衰減函式，請依欄位類型呼叫下列其中一個 Painless 方法：

- [數值]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)欄位：
    - `double decayNumericGauss(double <origin>, double <scale>, double <offset>, double <decay>, double <field-value>)`
    - `double decayNumericExp(double <origin>, double <scale>, double <offset>, double <decay>, double <field-value>)`
    - `double decayNumericLinear(double <origin>, double <scale>, double <offset>, double <decay>, double <field-value>)`
- [地理點]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-point/)欄位：
    - `double decayGeoGauss(String <origin>, String <scale>, String <offset>, double <decay>, GeoPoint <field-value>)`
    - `double decayGeoExp(String <origin>, String <scale>, String <offset>, double <decay>, GeoPoint <field-value>)`
    - `double decayGeoLinear(String <origin>, String <scale>, String <offset>, double <decay>, GeoPoint <field-value>)`
- [日期]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/)欄位：
    - `double decayDateGauss(String <origin>, String <scale>, String <offset>, double <decay>, JodaCompatibleZonedDateTime <field-value>)`
    - `double decayDateExp(String <origin>, String <scale>, String <offset>, double <decay>, JodaCompatibleZonedDateTime <field-value>)`
    - `double decayDateLinear(String <origin>, String <scale>, String <offset>, double <decay>, JodaCompatibleZonedDateTime <field-value>)`

#### 範例：數值欄位

下列查詢對數值欄位使用指數衰減函式：

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

下列查詢對地理點欄位使用高斯衰減函式：

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

下列查詢對日期欄位使用線性衰減函式：

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

日期衰減函式有下列限制：

- 起點必須是固定日期。不支援使用 `now` 的日期數學運算式，否則會導致搜尋失敗並出現 `could not read the current timestamp` 錯誤。若要依新近度評分，請在您的應用程式中計算目前日期，並透過 `params.origin` 傳入。
- 起點必須使用預設的 `strict_date_optional_time||epoch_millis` 格式，即使日期欄位是使用自訂的 `format` 進行對應也一樣。沒有時區偏移的起點會被解讀為 UTC。

### 向量函式

k-NN 外掛程式提供用於計算查詢向量與向量欄位之間距離或相似度的 Painless 函式，例如 `l2Squared`、`cosineSimilarity` 與 `hamming`。請在 `script_score` 查詢中使用這些函式，對被包裝查詢所回傳的文件執行精確 k-NN 搜尋。如需更多資訊，請參閱 [Painless 擴充功能]({{site.url}}{{site.baseurl}}/vector-search/vector-search-techniques/painless-functions/)。

### 詞頻函式

詞頻函式會在分數指令碼來源中公開詞元層級的統計資料。您可以使用這些統計資料實作自訂的資訊檢索與排名演算法，例如在查詢時依熱門程度進行乘法或加法的分數提升。若要套用詞頻函式，請呼叫下列其中一個 Painless 方法：

- `int termFreq(String <field-name>, String <term>)`：擷取該詞元在目前文件欄位中出現的次數。
- `long totalTermFreq(String <field-name>, String <term>)`：擷取該詞元在分片中所有文件的欄位中出現的次數。此值對分片中的每份文件都相同。
- `long sumTotalTermFreq(String <field-name>)`：擷取分片中所有文件的欄位中的詞元總數。此值對分片中的每份文件都相同。

#### 範例

下列查詢會迭代 `fields` 清單，並找出第一個不是 `null` 的欄位名稱。接著將分數計算為詞元 `ai` 在該欄位中的總詞頻乘以 `multiplier` 值。如果找不到欄位名稱，指令碼會回傳 `default_value`：

```json
GET /demo_index_v1/_search
{
  "query": {
    "script_score": {
      "query": {
        "match_all": {}
      },
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
```
{% include copy-curl.html %}

### 延遲互動分數

`lateInteractionScore` 函式是一種 Painless 指令碼評分函式，會使用詞元層級的向量比對來計算文件相關性。它會將每個查詢向量與所有文件向量進行比較，為每個查詢向量找出最大相似度，並將這些最大分數加總，以產生最終的文件分數。

**分數計算範例**：
- 查詢向量：`[[0.8, 0.1], [0.2, 0.9]]`
- 文件向量：`[[0.7, 0.2], [0.1, 0.8], [0.3, 0.4]]`
- 查詢向量 1 → 在文件向量中找出最佳相符項 → 分數 A
- 查詢向量 2 → 在文件向量中找出最佳相符項 → 分數 B
- 最終分數 = A + B

此方法可在查詢與文件之間進行細緻的語意比對，因此特別適合用於重新排序搜尋結果。

#### 索引對應需求

向量欄位必須對應為 `object` (建議) 或 `float` 類型。

我們建議將向量欄位對應為 `object` 搭配 `"enabled": false`，因為它會儲存原始向量而不進行剖析，可提升效能：

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

`lateInteractionScore` 函式支援下列參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `query_vectors` | 陣列的陣列 | 是 | 用於相似度比對的查詢向量。 |
| `vector_field` | 字串 | 是 | 包含向量的文件欄位名稱。 |
| `doc` | Map | 是 | 文件來源 (使用 `params._source`)。 |
| `space_type` | 字串 | 否 | 相似度計量。預設為 `l2`。 |

`space_type` 參數會決定相似度的計算方式，並接受下列有效值。

| 空間類型 | 說明 | 分數越高代表 |
| :--- | :--- | :--- |
| `innerproduct` | 點積 | 向量越相似 |
| `cosinesimil` | 餘弦相似度 | 方向越相似 |
| `l2` (預設) | 歐幾里得距離 | 向量越接近 (反轉) |

如需完整範例，請參閱[使用外部託管的延遲互動模型依欄位重新排序]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-by-field-late-interaction/)。

## 重現 function_score 的評分函式

[`function_score`]({{site.url}}{{site.baseurl}}/query-dsl/compound/function-score/) 查詢的每個評分函式都有對應的 `script_score`。當您需要在同一個公式中合併多個這類函式時，請使用下列對應：

- `script_score`：將 `script_score` 函式的指令碼原封不動地複製到 `script_score` 查詢的 `script` 參數中。
- `weight`：將相關性分數乘以一個常數，例如 `params.weight * _score`。
- `random_score`：呼叫 [`randomScore` 函式](#random-score)。
- `field_value_factor`：讀取欄位值，並在 Painless 中套用因子與修飾子。如需詳細資訊，請參閱[欄位值因子函式](#the-field-value-factor-function)。
- 衰減函式：呼叫對應的[衰減函式](#decay-functions)。

### 欄位值因數函式

下列查詢會重現一個 `field_value_factor` 函式，其 `factor` 為 `5`、修飾子為 `log`，且 `missing` 值為 `1`。對於沒有 `likes` 值的文件，指令碼會使用 `1`：

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
        "source": "Math.log10((doc['likes'].size() == 0 ? 1 : doc['likes'].value) * params.factor)",
        "params": {
          "factor": 5
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

`field_value_factor` 函式會將欄位值乘以 `factor`，然後套用修飾子。下表列出每個修飾子對應的 Painless 運算式，其中 `v` 為 `params.factor * doc['<field>'].value`。

修飾子 | Painless 運算式
:--- | :---
`none` | `v`
`log` | `Math.log10(v)`
`log1p` | `Math.log10(v + 1)`
`log2p` | `Math.log10(v + 2)`
`ln` | `Math.log(v)`
`ln1p` | `Math.log(v + 1)`
`ln2p` | `Math.log(v + 2)`
`square` | `Math.pow(v, 2)`
`sqrt` | `Math.sqrt(v)`
`reciprocal` | `1.0 / v`

## 解說指令碼分數

[Explain API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/explain/) 會顯示文件分數的計算方式。根據預設，`script_score` 查詢的解說只包含指令碼原始碼。若要新增可讀的計算說明，請在指令碼中呼叫 `explanation.set()`。

`explanation` 變數只會在解說請求中設定。在一般搜尋請求中，它會是 `null`，而呼叫 `explanation.set()` 會導致搜尋失敗。呼叫 `explanation.set()` 之前，請務必先檢查 `null`。

下列請求會解說文章 1 的分數：

```json
GET articles/_explain/1
{
  "query": {
    "script_score": {
      "query": {
        "match": {
          "article_name": "neural search"
        }
      },
      "script": {
        "source": """
          long likes = doc['likes'].value;
          double normalizedLikes = likes / 10.0;
          if (explanation != null) {
            explanation.set('normalized likes = likes / 10 = ' + likes + ' / 10 = ' + normalizedLikes);
          }
          return normalizedLikes;
        """
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會包含指令碼所設定的說明：

```json
{
  "_index" : "articles",
  "_id" : "1",
  "matched" : true,
  "explanation" : {
    "value" : 12.0,
    "description" : "normalized likes = likes / 10 = 120 / 10 = 12.0",
    "details" : [ ]
  }
}
```

## 更快的替代方案

`script_score` 查詢會針對符合所包裝查詢的每份文件執行其指令碼。下列查詢可略過無法進入頂端結果的文件，因此對於常見的加權任務而言速度更快：

- 若要根據靜態數值 (例如熱門程度或頁面排名) 為文件加權，請使用 [`rank_feature`]({{site.url}}{{site.baseurl}}/query-dsl/specialized/rank-feature/) 查詢。
- 若要為接近某個日期或地理點的文件加權，請使用 [`distance_feature`]({{site.url}}{{site.baseurl}}/query-dsl/specialized/distance-feature/) 查詢。

如果 [`search.allow_expensive_queries`]({{site.url}}{{site.baseurl}}/query-dsl/index/#expensive-queries) 設為 `false`，則不會執行 `script_score` 查詢。
{: .important}