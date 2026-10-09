---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "相似度"
parent: Tuning indexes
nav_order: 40
---

# 相似度

相似度定義了搜尋作業期間符合的文件如何計分及排名。OpenSearch 使用相似度演算法來計算相關性分數，以決定搜尋結果的順序。

每個欄位都可以有自己的相似度組態，讓您能精細控制不同類型的內容如何計分。您可以在索引層級的索引設定中定義自訂相似度演算法。設定完成後，您可以使用 [`similarity` 對應參數]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/similarity/) 將這些演算法套用至特定欄位。

設定自訂相似度設定是進階功能。內建相似度已足以因應大多數使用情境。

## 在索引層級設定相似度

OpenSearch 對所有欄位使用 BM25 作為預設相似度。您可以變更索引的預設相似度，將單一相似度演算法套用至該索引中的所有欄位。

### 在建立索引時設定預設相似度

您可以在建立索引時設定預設相似度：

```json
PUT /product_catalog
{
  "settings": {
    "index": {
      "similarity": {
        "default": {
          "type": "boolean"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

當您使用特殊的 `default` 名稱時，相似度會自動套用至索引中的所有欄位。您不需要在個別欄位對應中指定相似度。

### 在建立索引後變更預設相似度

相似度設定不是動態的，因此在開啟的索引上更新這些設定會失敗。若要在建立索引後變更預設相似度，請關閉索引、更新設定，然後重新開啟索引。

首先，關閉索引：

```json
POST /product_catalog/_close
```
{% include copy-curl.html %}

接著，更新預設相似度：

```json
PUT /product_catalog/_settings
{
  "index": {
    "similarity": {
      "default": {
        "type": "DFR",
        "basic_model": "g",
        "after_effect": "l",
        "normalization": "h2",
        "normalization.h2.c": "3.0"
      }
    }
  }
}
```
{% include copy-curl.html %}

最後，重新開啟索引：

```json
POST /product_catalog/_open
```
{% include copy-curl.html %}

若要確認預設相似度已變更，請傳送下列請求：

```json
GET /product_catalog/_settings
```
{% include copy-curl.html %}

回應會確認預設相似度已更新：

```json
{
  "product_catalog": {
    "settings": {
      "index": {
        "replication": {
          "type": "DOCUMENT"
        },
        "number_of_shards": "1",
        "provided_name": "product_catalog",
        "similarity": {
          "default": {
            "basic_model": "g",
            "type": "DFR",
            "normalization": "h2",
            "after_effect": "l",
            "normalization.h2": {
              "c": "3.0"
            }
          }
        },
        "creation_date": "1761328470322",
        "number_of_replicas": "1",
        "uuid": "YFr9ts8VSaSV-YkHZP3mYQ",
        "version": {
          "created": "137227827"
        }
      }
    }
  }
}
```

### 變更相似度類型時的參數持續性

從一種相似度類型變更為另一種時，OpenSearch 會保留先前組態的參數。如果新的相似度類型不支援這些參數，更新就會失敗。

例如，將預設相似度從 `DFR` 變更為 `boolean`。首先，關閉索引：

```json
POST /product_catalog/_close
```
{% include copy-curl.html %}

然後更新預設相似度：

```json
PUT /product_catalog/_settings
{
  "index": {
    "similarity": {
      "default": {
        "type": "boolean"
      }
    }
  }
}
```
{% include copy-curl.html %}

請求會失敗，因為 `DFR` 參數仍已設定：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "Unknown settings for similarity of type [boolean]: [normalization.h2.c, normalization, after_effect, basic_model]"
      }
    ],
    "type": "illegal_argument_exception",
    "reason": "Unknown settings for similarity of type [boolean]: [normalization.h2.c, normalization, after_effect, basic_model]"
  },
  "status": 400
}
```

若要解決此問題，請在同一個請求中將舊參數明確設為 `null`：

```json
PUT /product_catalog/_settings
{
  "index": {
    "similarity": {
      "default": {
        "type": "boolean",
        "basic_model": null,
        "after_effect": null,
        "normalization": null,
        "normalization.h2.c": null
      }
    }
  }
}
```
{% include copy-curl.html %}

然後重新開啟索引：

```json
POST /product_catalog/_open
```
{% include copy-curl.html %}

## 在欄位層級設定內建相似度

OpenSearch 提供內建相似度演算法 (`BM25` 和 `boolean`)，可直接用於欄位對應。若要在欄位層級設定相似度，請在建立索引時將其套用至欄位。下列範例將 `boolean` 相似度套用至 `content` 欄位：

```json
PUT /blog_posts_2/
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "similarity": "boolean"
      }
    }
  }
}
```
{% include copy-curl.html %}

在此範例中，只有 `content` 欄位使用 `boolean` 相似度。索引中的其他欄位將使用預設的 `BM25` 相似度。

## 設定自訂相似度

若為更進階的使用情境，您可以定義具名的自訂相似度，並將其套用至特定欄位。當索引中的不同欄位需要不同的計分演算法時，此做法可提供更大的彈性。

設定具名的自訂相似度需要兩個步驟：

1. 在索引設定中以自訂名稱定義相似度。
2. 在對應中將相似度套用至特定欄位。

### 步驟 1：定義自訂相似度

下列範例建立具有自訂 `DFR` 相似度組態的索引：

```json
PUT /blog_posts
{
  "settings": {
    "index": {
      "similarity": {
        "blog_similarity": {
          "type": "DFR",
          "basic_model": "g",
          "after_effect": "l",
          "normalization": "h2",
          "normalization.h2.c": "3.0"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 2：將自訂相似度套用至欄位

定義相似度之後，您必須在對應中明確地將其套用至特定欄位。與預設相似度不同，自訂相似度不會自動套用至所有欄位：

```json
PUT /blog_posts/_mapping
{
  "properties": {
    "content": {
      "type": "text",
      "similarity": "blog_similarity"
    }
  }
}
```
{% include copy-curl.html %}

在此範例中，只有 `content` 欄位使用自訂的 `blog_similarity`。索引中的其他欄位 (若有) 會繼續使用預設的 `BM25` 相似度，除非另有明確設定。

## 可用的相似度類型

OpenSearch 支援下列相似度類型。

### BM25 相似度 (預設)

`BM25` 相似度以 TF/IDF 為基礎，並包含內建的詞頻正規化。它適用於大多數文字欄位，尤其是標題和名稱等較短的欄位。

`BM25` 相似度支援下列參數。

| 參數 | 說明 | 預設 | 必要 |
|-----------|-------------|---------|----------|
| `k1` | 控制非線性的詞頻正規化 (飽和)。 | `1.2` | 否 |
| `b` | 控制文件長度對詞頻值的正規化程度。 | `0.75` | 否 |
| `discount_overlaps` | 決定計算範數時是否忽略重疊詞元 (位置增量為 0 的詞元)。 | `true` (計算範數時忽略重疊詞元) | 否 |

### 布林相似度

內建的 `boolean` 相似度會為所有相符文件指定相同的固定分數，適用於您只需要判斷文件是否相符，而不需要判斷其相關性高低的情況。此相似度會忽略詞頻、文件長度及其他評分因素。

`boolean` 相似度不支援參數。

### DFR 相似度

`DFR` 相似度實作了[偏離隨機性](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/DFRSimilarity.html)框架，用於文件評分。

`DFR` 相似度支援下列參數。

| 參數 | 說明 | 有效值 | 必要 |
|-----------|-------------|------------------|----------|
| `basic_model` | DFR 框架的基本模型。 | [`g`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/BasicModelG.html), [`if`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/BasicModelIF.html), [`in`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/BasicModelIn.html), [`ine`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/BasicModelIne.html) | 是 |
| `after_effect` | DFR 框架的後效模型。 | [`b`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/AfterEffectB.html), [`l`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/AfterEffectL.html) | 是 |
| `normalization` | DFR 框架的正規化模型。`h1`、`h2` 和 `h3` 接受選用的 `c` 參數，以 `normalization.h1.c`、`normalization.h2.c` 或 `normalization.h3.c` 指定。`z` 接受選用的 `z` 參數，以 `normalization.z.z` 指定，其值必須大於 0 且小於 0.5。`no` 不接受任何參數。 | [`no`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/Normalization.NoNormalization.html), [`h1`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/NormalizationH1.html), [`h2`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/NormalizationH2.html), [`h3`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/NormalizationH3.html), [`z`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/NormalizationZ.html) | 是 |

### DFI 相似度

`DFI` 相似度實作了[偏離獨立性（DFI）](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/DFISimilarity.html)模型。

`DFI` 相似度支援下列參數。

| 參數 | 說明 | 有效值 | 必要 |
|-----------|-------------|------------------|----------|
| `independence_measure` | DFI 模型的獨立性度量。 | [`standardized`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/IndependenceStandardized.html), [`saturated`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/IndependenceSaturated.html), [`chisquared`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/IndependenceChiSquared.html) | 是 |

使用 `DFI` 相似度時，請避免移除停用詞，以獲得最佳相關性。頻率低於預期的詞彙會得到 0 分。

### IB 相似度

`IB` 相似度使用[以資訊為基礎的模型](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/IBSimilarity.html)，此模型會分析符號分布中基本元素的重複使用情形。

`IB` 相似度支援下列參數。

| 參數 | 說明 | 有效值 | 必要 |
|-----------|-------------|------------------|----------|
| `distribution` | `IB` 框架的分布模型。 | [`ll`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/DistributionLL.html), [`spl`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/DistributionSPL.html) | 是 |
| `lambda` | `IB` 框架的 Lambda 模型。 | [`df`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/LambdaDF.html), [`ttf`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/LambdaTTF.html) | 是 |
| `normalization` | `IB` 框架的正規化模型。 | 與 `DFR` 相似度的選項相同 | 是 |

<!-- vale off -->
### LM Dirichlet 相似度
<!-- vale on -->

`LMDirichlet` 相似度使用採用 Dirichlet 平滑的[語言模型相似度](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/LMDirichletSimilarity.html)。

`LMDirichlet` 相似度支援下列參數。

| 參數 | 說明 | 預設 | 必要 |
|-----------|-------------|---------|----------|
| `mu` | 平滑參數。 | `2000` | 否 |

出現次數少於語言模型預測值的詞彙會得到 0 分。

<!-- vale off -->
### LM Jelinek Mercer 相似度
<!-- vale on -->

`LMJelinekMercer` 相似度使用採用 Jelinek-Mercer 平滑的[語言模型相似度](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/similarities/LMJelinekMercerSimilarity.html)。

`LMJelinekMercer` 相似度支援下列參數。

| 參數 | 說明 | 預設 | 必要 |
|-----------|-------------|---------|----------|
| `lambda` | 內插參數。接近 `0.1` 的值適用於標題查詢，而 `0.7` 更適合較長的查詢。 | `0.1` | 否 |

### 指令碼相似度

`scripted` 相似度可讓您使用 OpenSearch 的指令碼功能來自訂評分邏輯。

為 `scripted` 相似度撰寫指令碼時，您可以存取下列變數。這些變數可讓您根據詞頻、文件頻率、欄位統計資料及文件特性，實作自訂評分演算法。

| 變數 | 說明 |
|----------|-------------|
| `weight` | 與文件無關的權重（若有提供 `weight_script`，則從中取得，否則為 `1.0`）。 |
| `query.boost` | 套用至詞彙的查詢層級加權因子。 |
| `field.docCount` | 具有此欄位的文件總數。 |
| `field.sumDocFreq` | 此欄位中所有詞彙的文件頻率總和。 |
| `field.sumTotalTermFreq` | 此欄位中所有詞彙的總詞頻之和。 |
| `term.docFreq` | 包含此特定詞彙的文件數量。 |
| `term.totalTermFreq` | 此詞彙在所有文件中的出現總次數。 |
| `doc.freq` | 此詞彙在目前文件中的頻率。 |
| `doc.length` | 目前文件中的詞彙總數。 |

為確保搜尋行為正確，`scripted` 相似度必須遵循下列規則：

- 傳回的分數必須為正值。
- 當 `doc.freq` 增加且所有其他變數維持不變時，分數不得降低。
- 當 `doc.length` 增加且所有其他變數維持不變時，分數不得增加。

下列範例示範自訂的 TF-IDF 實作。

首先，建立索引並定義用於計算相似度的指令碼：

```json
PUT /research_papers
{
  "settings": {
    "number_of_shards": 1,
    "similarity": {
      "custom_tfidf": {
        "type": "scripted",
        "script": {
          "source": "double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "abstract": {
        "type": "text",
        "similarity": "custom_tfidf"
      }
    }
  }
}
```
{% include copy-curl.html %}

將範例文件編製索引：

```json
PUT /research_papers/_doc/1
{
  "abstract": "machine learning algorithms data mining"
}
```
{% include copy-curl.html %}

```json
PUT /research_papers/_doc/2
{
  "abstract": "data analysis statistical methods"
}
```
{% include copy-curl.html %}

重新整理索引：

```json
POST /research_papers/_refresh
```
{% include copy-curl.html %}

現在您可以搜尋索引並要求提供評分說明：

```json
GET /research_papers/_search?explain=true
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "abstract": "machine"
          }
        }
      ],
      "boost": 2.0
    }
  }
}
```
{% include copy-curl.html %}

回應會顯示自訂的 TF-IDF 計算結果，相符文件的分數為 `1.2570862`。`_explanation` 區段會顯示指令碼可使用的所有變數，以及這些變數在此次特定搜尋中的值：

```json
{
  "took": 6,
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
    "max_score": 1.2570862,
    "hits": [
      {
        "_shard": "[research_papers][0]",
        "_node": "KfEEGG7_SsKZVFqI4ko2FA",
        "_index": "research_papers",
        "_id": "1",
        "_score": 1.2570862,
        "_source": {
          "abstract": "machine learning algorithms data mining"
        },
        "_explanation": {
          "value": 1.2570862,
          "description": "weight(abstract:machine in 0) [PerFieldSimilarity], result of:",
          "details": [
            {
              "value": 1.2570862,
              "description": "score from ScriptedSimilarity(weightScript=[null], script=[Script{type=inline, lang='painless', idOrCode='double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;', options={}, params={}}]) computed from:",
              "details": [
                {
                  "value": 1.0,
                  "description": "weight",
                  "details": []
                },
                {
                  "value": 2.0,
                  "description": "query.boost",
                  "details": []
                },
                {
                  "value": 2,
                  "description": "field.docCount",
                  "details": []
                },
                {
                  "value": 9,
                  "description": "field.sumDocFreq",
                  "details": []
                },
                {
                  "value": 9,
                  "description": "field.sumTotalTermFreq",
                  "details": []
                },
                {
                  "value": 1,
                  "description": "term.docFreq",
                  "details": []
                },
                {
                  "value": 1,
                  "description": "term.totalTermFreq",
                  "details": []
                },
                {
                  "value": 1.0,
                  "description": "doc.freq",
                  "details": []
                },
                {
                  "value": 5,
                  "description": "doc.length",
                  "details": []
                }
              ]
            }
          ]
        }
      }
    ]
  }
}
```

您可以將與文件無關的計算分離到另一個名為 `weight_script` 的指令碼中，以改善效能。對於符合許多文件的查詢，`weight_script` 會針對每個詞彙執行一次，而主要的 `script` 則會針對每份文件執行一次。`weight_script` 產生的分數可在 `weight` 變數中取得：

```json
PUT /research_papers_optimized
{
  "settings": {
    "number_of_shards": 1,
    "similarity": {
      "optimized_tfidf": {
        "type": "scripted",
        "weight_script": {
          "source": "double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; return query.boost * idf;"
        },
        "script": {
          "source": "double tf = Math.sqrt(doc.freq); double norm = 1/Math.sqrt(doc.length); return weight * tf * norm;"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "abstract": {
        "type": "text",
        "similarity": "optimized_tfidf"
      }
    }
  }
}
```
{% include copy-curl.html %}

將相同的範例文件編製索引至 `research_papers_optimized`、重新整理索引，然後執行相同的查詢。回應會顯示最佳化相似度如何運作：

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
    "max_score": 1.2570862,
    "hits": [
      {
        "_shard": "[research_papers_optimized][0]",
        "_node": "KfEEGG7_SsKZVFqI4ko2FA",
        "_index": "research_papers_optimized",
        "_id": "1",
        "_score": 1.2570862,
        "_source": {
          "abstract": "machine learning algorithms data mining"
        },
        "_explanation": {
          "value": 1.2570862,
          "description": "weight(abstract:machine in 0) [PerFieldSimilarity], result of:",
          "details": [
            {
              "value": 1.2570862,
              "description": "score from ScriptedSimilarity(weightScript=[Script{type=inline, lang='painless', idOrCode='double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; return query.boost * idf;', options={}, params={}}], script=[Script{type=inline, lang='painless', idOrCode='double tf = Math.sqrt(doc.freq); double norm = 1/Math.sqrt(doc.length); return weight * tf * norm;', options={}, params={}}]) computed from:",
              "details": [
                {
                  "value": 2.8109303,
                  "description": "weight",
                  "details": []
                },
                {
                  "value": 2.0,
                  "description": "query.boost",
                  "details": []
                },
                {
                  "value": 2,
                  "description": "field.docCount",
                  "details": []
                },
                {
                  "value": 9,
                  "description": "field.sumDocFreq",
                  "details": []
                },
                {
                  "value": 9,
                  "description": "field.sumTotalTermFreq",
                  "details": []
                },
                {
                  "value": 1,
                  "description": "term.docFreq",
                  "details": []
                },
                {
                  "value": 1,
                  "description": "term.totalTermFreq",
                  "details": []
                },
                {
                  "value": 1.0,
                  "description": "doc.freq",
                  "details": []
                },
                {
                  "value": 5,
                  "description": "doc.length",
                  "details": []
                }
              ]
            }
          ]
        }
      }
    ]
  }
}
```

在這個最佳化範例中：

- `weight_script` 會計算 `2.8109303` 的分數 (IDF + 查詢加成，對所有文件都相同)。
- 主要的 `script` 會使用預先計算的 `weight` 值來計算各文件專屬的因子。
- 最終分數為 `1.2570862` (與單一指令碼方法相同，但更有效率)。

`weight_script` 參數名稱為保留名稱，無法變更。結果一律可在主要指令碼中的 `weight` 變數中取得。
{: .note}

## 相關文件

- [`similarity` 對應參數]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/similarity/)