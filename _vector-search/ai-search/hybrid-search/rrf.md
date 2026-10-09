---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "倒數排名融合"
parent: Hybrid search
grand_parent: AI search
has_children: false
has_math: true
nav_order: 5
---

# 倒數排名融合
**於 2.19 版推出**
{: .label .label-purple }

倒數排名融合 (RRF) 會依據每份文件在各結果清單中的位置，而非其相關性分數，來合併多個查詢子句的結果。出現在多份結果清單前段的文件，其合併分數會高於僅出現在單一清單最前面的文件。

由於 RRF 只使用排名，個別查詢子句所產生的相關性分數永遠不需要具備可比性。BM25 分數 `12.4` 與向量相似度 `0.87` 衡量的是不同尺度上的不同量值，但排名 `1` 能同時指出兩份清單中的第一名結果。因此，當您尚未決定如何權衡關鍵字相關性與語意相關性時，RRF 是混合搜尋的合理起點。

OpenSearch 會依下列方式計算文件 $$d$$ 的 RRF 分數：

$$score(d) = \sum_{q \in Q} \frac{1}{k + rank_q(d)}$$

此公式使用下列變數：

- $$Q$$ 是 `hybrid` 查詢中的查詢子句集合。
- $$rank_q(d)$$ 是 $$d$$ 在查詢子句 $$q$$ 結果中的位置，從 `1` 開始計算。未出現 $$d$$ 的查詢子句不會有任何貢獻。
- $$k$$ 是排名常數，由 `rank_constant` 參數設定。

## 選擇合併方法

混合搜尋提供兩個搜尋階段結果處理器來合併子查詢結果。請使用下表判斷應設定哪一個。

| | 分數排名處理器 (以排名為基礎) | 正規化處理器 (以分數為基礎) |
| :--- | :--- | :--- |
| 合併輸入 | 文件排名 | 文件相關性分數 |
| 技術 | `rrf` | `arithmetic_mean`、`geometric_mean`、`harmonic_mean`，在 `min_max`、`l2` 或 `z_score` 正規化之後套用 |
| 分數量級 | 會捨棄，因此分數僅略高於下一名結果的文件，與分數大幅領先下一名結果的文件會被視為相同 | 會保留，因此兩份文件之間的差距會影響合併分數 |
| 調校參數 | `rank_constant` 與選用的 `weights` | 正規化技術、合併技術、`weights`，以及選用的分數界限 |
| 開始支援版本 | 2.19 | 2.10 |

當您想要一組不需先測量查詢子句分數分布就能運作的組態時，請從 RRF 開始。在下列情況下，RRF 通常是較佳的選擇：

- 查詢子句產生的分數位於無法直接比較的尺度上，例如多模態管線中文字相關性涵蓋的數值範圍很廣，而視覺相似度涵蓋的範圍很窄。
- 資料包含離群值或分數變異很大，科學語料庫與記錄資料經常如此。最小-最大正規化與 L2 正規化對極端值很敏感，而排名彙總可避免單一離群值扭曲合併後的排名。
- 相關性訊號稀疏，例如電子商務型錄中的點擊與購買資料。依位置排名可保留具有強烈語意或中繼資料相關性的利基商品之位置。
- 資料持續變動。正規化取決於目前結果集的分數分布，因此串流資料需要重新校正，而 RRF 不需要。
- 您想獎勵在多個查詢子句中排名良好的文件。L2 正規化沒有機制可優先處理出現在多份結果清單中的文件。

當分數差距所含的資訊必須保留在最終排名中時，請使用正規化處理器，例如某個查詢子句傳回一個強烈相符結果，其後接著微弱的相符結果，而最終排名必須反映該差異。這三種正規化技術會以不同方式保留這些差距。如需詳細資訊，請參閱[正規化技術]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/#normalization-techniques)。

RRF 的取捨是相關性會略微降低。在六個 BEIR 資料集的基準測試中，RRF 的 NDCG@10 平均比以分數為基礎的混合搜尋管線低 3.86%，而搜尋延遲與協調器節點 CPU 使用率則相當。如需完整結果，請參閱[為混合搜尋推出倒數排名融合](https://opensearch.org/blog/introducing-reciprocal-rank-fusion-hybrid-search/)。若要在您自己的資料與判斷清單上比較這兩個處理器，請使用 [Search Relevance Workbench]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/optimize-hybrid-search/)，其會在一系列參數值上評估兩者。

如需 `score-ranker-processor` 請求欄位的完整清單，請參閱[分數排名處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/score-ranker-processor/)。

## 範例：融合關鍵字與向量結果

下列範例會建立產品索引，分別執行關鍵字查詢子句與向量查詢子句以顯示各自的排名，然後以 RRF 融合兩者。

此範例使用二維向量，並直接在各文件中指定，以便您手動驗證計算結果。在正式環境的索引中，請使用機器學習模型產生嵌入。如需詳細資訊，請參閱[自動產生嵌入]({{site.url}}{{site.baseurl}}/vector-search/getting-started/auto-generated-embeddings/)。
{: .note}

此索引使用單一分片，以確保排名可重現。如需分片數量如何影響 RRF 的詳細資訊，請參閱[分片數量對 RRF 結果的影響](#the-effect-of-shard-count-on-rrf-results)。
{: .note}

### 步驟 1：建立索引

建立一個索引，其中包含用於關鍵字比對的文字欄位，以及用於語意比對的向量欄位：

```json
PUT /products
{
  "settings": {
    "index.knn": true,
    "number_of_shards": 1
  },
  "mappings": {
    "properties": {
      "item_name": {
        "type": "text"
      },
      "item_vector": {
        "type": "knn_vector",
        "dimension": 2,
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "lucene"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 2：匯入文件

將五項產品編製索引：

```json
POST /_bulk?refresh=true
{ "index": { "_index": "products", "_id": "1" } }
{ "item_name": "kids running shoes", "item_vector": [0.2, 0.8] }
{ "index": { "_index": "products", "_id": "2" } }
{ "item_name": "mens lightweight running shoes for road racing", "item_vector": [0.9, 0.1] }
{ "index": { "_index": "products", "_id": "3" } }
{ "item_name": "trail runners", "item_vector": [0.8, 0.2] }
{ "index": { "_index": "products", "_id": "4" } }
{ "item_name": "athletic socks", "item_vector": [0.5, 0.5] }
{ "index": { "_index": "products", "_id": "5" } }
{ "item_name": "winter parka", "item_vector": [0.0, 1.0] }
```
{% include copy-curl.html %}

### 步驟 3：分別執行每個查詢子句

單獨執行關鍵字查詢子句：

```json
GET /products/_search
{
  "_source": ["item_name"],
  "query": {
    "match": {
      "item_name": "running shoes"
    }
  }
}
```
{% include copy-curl.html %}

有兩份文件同時包含這兩個詞彙。文件 `1` 排名第一，因為其較短的 `item_name` 欄位產生較高的 BM25 分數：

| 排名 | 文件 ID | `item_name` | 分數 |
| :--- | :--- | :--- | :--- |
| 1 | `1` | kids running shoes | 0.81676 |
| 2 | `2` | mens lightweight running shoes for road racing | 0.53566 |

單獨執行向量查詢子句：

```json
GET /products/_search
{
  "_source": ["item_name"],
  "query": {
    "knn": {
      "item_vector": {
        "vector": [0.9, 0.1],
        "k": 3
      }
    }
  }
}
```
{% include copy-curl.html %}

由於 `k` 為 `3`，該查詢子句會傳回三份文件：

| 排名 | 文件 ID | `item_name` | 分數 |
| :--- | :--- | :--- | :--- |
| 1 | `2` | mens lightweight running shoes for road racing | 1.0 |
| 2 | `3` | trail runners | 0.98039 |
| 3 | `4` | athletic socks | 0.75758 |

文件 `2` 是兩個查詢子句都傳回的唯一文件，且兩者都未將其排在第一位。

### 步驟 4：建立搜尋管線

建立一個包含 `score-ranker-processor` 的搜尋管線，該處理器使用 `rrf` 組合技術。此範例將 `rank_constant` 設為 `1`，使產生的分數較易閱讀；預設值為 `60`：

```json
PUT /_search/pipeline/rrf-pipeline
{
  "description": "Post processor for hybrid RRF search",
  "phase_results_processors": [
    {
      "score-ranker-processor": {
        "combination": {
          "technique": "rrf",
          "rank_constant": 1
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 5：執行混合查詢

將兩個查詢子句合併在一個 [`hybrid` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/hybrid/) 中，並套用搜尋管線：

```json
GET /products/_search?search_pipeline=rrf-pipeline
{
  "_source": {
    "excludes": ["item_vector"]
  },
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "item_name": "running shoes"
          }
        },
        {
          "knn": {
            "item_vector": {
              "vector": [0.9, 0.1],
              "k": 3
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應包含融合後的排名：

```json
{
  "took": 5,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": 0.8333334,
    "hits": [
      {
        "_index": "products",
        "_id": "2",
        "_score": 0.8333334,
        "_source": {
          "item_name": "mens lightweight running shoes for road racing"
        }
      },
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.5,
        "_source": {
          "item_name": "kids running shoes"
        }
      },
      {
        "_index": "products",
        "_id": "3",
        "_score": 0.33333334,
        "_source": {
          "item_name": "trail runners"
        }
      },
      {
        "_index": "products",
        "_id": "4",
        "_score": 0.25,
        "_source": {
          "item_name": "athletic socks"
        }
      }
    ]
  }
}
```

每個 `_score` 都是該文件倒數排名的總和：

| 文件 ID | 關鍵字排名 | 向量排名 | RRF 計算 | `_score` |
| :--- | :--- | :--- | :--- | :--- |
| `2` | 2 | 1 | 1 / (1 + 2) + 1 / (1 + 1) | 0.8333334 |
| `1` | 1 | -- | 1 / (1 + 1) | 0.5 |
| `3` | -- | 2 | 1 / (1 + 2) | 0.33333334 |
| `4` | -- | 3 | 1 / (1 + 3) | 0.25 |

文件 `2` 排名第一，因為它是唯一同時被兩個查詢子句傳回的文件，即使它依關鍵字相關性排名第二，且其向量分數相較於文件 `3` 的領先幅度也很小。文件 `5` 未出現在回應中，因為沒有任何查詢子句傳回它；RRF 只對子查詢結果的聯集進行排名。

## 控制融合深度

只有當文件出現在每個結果清單中到達融合步驟的部分時，RRF 才能因文件出現在多個結果清單中而給予獎勵。有兩個設定限制了該部分：

- `knn` 查詢子句中的 `k` 值限制該子句在每個分片傳回的文件數量，因此也限制了獲得向量排名的文件數量。在上一個範例中，`k` 為 `3`，這就是文件 `1` 和 `5` 沒有向量排名的原因。
- `size` 限制每個查詢子句在每個分片貢獻的結果數量。預設情況下，每個查詢子句在融合前會被截斷為 `size` 個結果。

`size` 限制是最常產生非預期結果的一個。將 `size` 設為 `1` 後重新執行[上一個查詢](#step-5-run-the-hybrid-query)，會傳回文件 `1` 而非文件 `2`：

```json
GET /products/_search?search_pipeline=rrf-pipeline
{
  "size": 1,
  "_source": {
    "excludes": ["item_vector"]
  },
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "item_name": "running shoes"
          }
        },
        {
          "knn": {
            "item_vector": {
              "vector": [0.9, 0.1],
              "k": 3
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

每個查詢子句只貢獻其第一個結果，因此關鍵字子句提供文件 `1`，向量子句提供文件 `2`。兩份文件都未同時出現在兩個截斷後的清單中，兩者的分數都是 1 / (1 + 1) = 0.5，而平手判定有利於文件 `1`。原本在 `size: 10` 將文件 `2` 排名第一的兩個子句之間的一致性，不再能到達融合步驟。

若要將融合深度與分頁大小解耦，請在 `hybrid` 查詢中設定 `pagination_depth`。它定義每個查詢子句在每個分片貢獻的結果數量，不受 `size` 影響。下列查詢只傳回一個結果，但會融合每個子句的前 10 個結果，使文件 `2` 重新成為排名第一的結果：

```json
GET /products/_search?search_pipeline=rrf-pipeline
{
  "size": 1,
  "_source": {
    "excludes": ["item_vector"]
  },
  "query": {
    "hybrid": {
      "pagination_depth": 10,
      "queries": [
        {
          "match": {
            "item_name": "running shoes"
          }
        },
        {
          "knn": {
            "item_vector": {
              "vector": [0.9, 0.1],
              "k": 3
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

當您的應用程式只要求少量結果時，請將 `pagination_depth` 設定為高於應用程式使用的最大 `size` 值。較大的值可提升融合排名的品質，但需要 OpenSearch 在每個分片保留並處理更多結果。如需更多資訊，請參閱 [混合查詢結果分頁]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/pagination/)。

## 解讀 RRF 分數

RRF `_score` 是倒數排名的總和，因此它只反映文件在查詢子句結果中所佔的位置，與底層查詢子句的相關性分數無關。文件可獲得的最高分數是查詢子句權重總和除以 (`rank_constant` + 1)，只有當文件在每個查詢子句中都排名第一時才能獲得。在使用預設 `rank_constant` 為 `60` 的情況下，頂部結果的分數因此落在接近 1 / 61 的狹窄區間內，如 [排名常數](#tuning-the-rank-constant) 表格所示。這帶來兩個後果：

- 避免使用 `min_score` 門檻來排除 RRF 結果。OpenSearch 會將 `min_score` 套用至 RRF 分數，但該值取決於查詢子句的數量和排名常數，而非文件與查詢的符合程度。
- 避免跨查詢比較 RRF 分數。相同的分數對某個查詢可能代表高度符合，對另一個查詢卻可能代表低度符合。

若要查看每個查詢子句對某份文件貢獻的排名，請在搜尋管線中加入 [`hybrid_score_explanation` 回應處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/explanation-processor/)，並以 `explain=true` 執行查詢：

```json
PUT /_search/pipeline/rrf-explain-pipeline
{
  "description": "RRF pipeline with score explanation",
  "phase_results_processors": [
    {
      "score-ranker-processor": {
        "combination": {
          "technique": "rrf",
          "rank_constant": 1
        }
      }
    }
  ],
  "response_processors": [
    {
      "hybrid_score_explanation": {}
    }
  ]
}
```
{% include copy-curl.html %}

文件 `2` 的說明會針對每個查詢子句回報一項貢獻，以及決定其在該子句中排名的原始子查詢分數：

```json
{
  "_id": "2",
  "_score": 0.8333334,
  "_explanation": {
    "value": 0.8333334,
    "description": "rrf combination of:",
    "details": [
      {
        "value": 0.33333334,
        "description": "rrf, rank_constant [1] normalization of:",
        "details": [
          {
            "value": 0.5356597,
            "description": "sum of:"
          }
        ]
      },
      {
        "value": 0.5,
        "description": "rrf, rank_constant [1] normalization of:",
        "details": [
          {
            "value": 1.0,
            "description": "within top 3 docs"
          }
        ]
      }
    ]
  }
}
```

若沒有 `hybrid_score_explanation` 回應處理器，`_explanation` 物件會回報原始 Lucene 分數，而這些分數加總不等於 `_score`。如需更多資訊，請參閱 [混合搜尋說明]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/explain/)。

## 分片數量對 RRF 結果的影響

OpenSearch 會在合併每個查詢子句的分片層級結果後指派排名，但該合併的兩項輸入是依分片計算，因此相同的資料與相同的查詢，在分片數量不同的索引上可能產生不同的 RRF 分數：

- BM25 統計資料是依分片計算，因此關鍵字查詢子句排序文件的方式，可能取決於每份文件位於哪個分片。
- `knn` 查詢子句中的 `k` 值會依分片套用，因此具有三個分片的索引，從向量查詢子句傳回的文件數最多可達單一分片索引的三倍。每份額外的文件都會取得一個排名並進入融合。

在具有三個分片的索引上，對相同的五份文件執行[先前的範例](#step-5-run-the-hybrid-query)會傳回五個結果而非四個，且文件 `1` 與 `2` 的關鍵字排名會互換：

| 文件 ID | 關鍵字排名 | 向量排名 | RRF 計算 | `_score` |
| :--- | :--- | :--- | :--- | :--- |
| `2` | 1 | 1 | 1 / (1 + 1) + 1 / (1 + 1) | 1.0 |
| `1` | 2 | 4 | 1 / (1 + 2) + 1 / (1 + 4) | 0.53333336 |
| `3` | -- | 2 | 1 / (1 + 2) | 0.33333334 |
| `4` | -- | 3 | 1 / (1 + 3) | 0.25 |
| `5` | -- | 5 | 1 / (1 + 5) | 0.16666667 |

隨著每個分片的文件數增加，BM25 的影響會減弱，因為各分片的詞彙統計資料會收斂至整個索引的值。`k` 的影響則不會：向量查詢子句每個分片一律最多貢獻 `k` 份文件。當您調整 `rank_constant` 或 `weights` 時，請對與正式環境索引具有相同分片數量的索引執行實驗。

## 調整排名常數

`rank_constant` 參數控制文件的貢獻隨著排名下降而衰減的速度。有效值介於 [1, 10000] 範圍內。預設值為 `60`。

較小的排名常數會在相鄰排名之間產生較大的差距，將影響力集中在每個查詢子句的前幾個結果。較大的排名常數會縮小這些差距，使排名較低的結果幾乎與排名最高的結果具有相同的權重。以預設的 `rank_constant` 值 `60` 執行先前的範例，會產生相同的排序但分數更為壓縮，因為 1 / 61、1 / 62 與 1 / 63 之間的差異遠小於 1 / 2、1 / 3 與 1 / 4 之間的差異：

| 文件 ID | RRF 計算 | `_score` |
| :--- | :--- | :--- |
| `2` | 1 / (60 + 2) + 1 / (60 + 1) | 0.032522473 |
| `1` | 1 / (60 + 1) | 0.016393442 |
| `3` | 1 / (60 + 2) | 0.016129032 |
| `4` | 1 / (60 + 3) | 0.015873017 |

若要為您自己的資料選擇值，請執行混合搜尋實驗，針對判斷清單評估數個排名常數。如需更多資訊，請參閱[最佳化混合搜尋]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/optimize-hybrid-search/)。

## 加權查詢子句

根據預設，RRF 會對所有查詢子句賦予相同的權重。若要讓某個子句優先於另一個子句，請指定 `combination.parameters.weights`。權重的數量必須與查詢子句的數量相符，且權重總和必須為 `1.0`。每個權重會乘上對應子句的倒數排名：

$$score(d) = \sum_{q \in Q} w_q \cdot \frac{1}{k + rank_q(d)}$$

下列管線會將 30% 的權重指派給關鍵字查詢子句，並將 70% 指派給向量查詢子句：

```json
PUT /_search/pipeline/rrf-pipeline
{
  "description": "Post processor for hybrid RRF search",
  "phase_results_processors": [
    {
      "score-ranker-processor": {
        "combination": {
          "technique": "rrf",
          "rank_constant": 1,
          "parameters": {
            "weights": [
              0.3,
              0.7
            ]
          }
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

以這些權重重新執行[步驟 5](#step-5-run-the-hybrid-query)的查詢，會將文件 `1` 排在最後，因為它唯一的貢獻來自關鍵字子句，而該子句現在具有較低的權重：

| 文件 ID | RRF 計算 | `_score` |
| :--- | :--- | :--- |
| `2` | 0.3 &times; 1 / (1 + 2) + 0.7 &times; 1 / (1 + 1) | 0.45 |
| `3` | 0.7 &times; 1 / (1 + 2) | 0.23333333 |
| `4` | 0.7 &times; 1 / (1 + 3) | 0.175 |
| `1` | 0.3 &times; 1 / (1 + 1) | 0.15 |

加權會重新引入未加權 RRF 所避免的調校工作，因此只有在您能衡量其對相關性的影響時，才變更權重。

## 後續步驟

- [分數排名處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/score-ranker-processor/)
- [正規化處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/)
- [最佳化混合搜尋]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/optimize-hybrid-search/)
