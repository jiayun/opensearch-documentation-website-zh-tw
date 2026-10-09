---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "正規化"
nav_order: 70
has_children: false
has_math: true
parent: User-defined search processors
grand_parent: Search pipelines
---

# 正規化處理器
於 2.10 版推出
{: .label .label-purple }

`normalization-processor` 是一種搜尋階段結果處理器，會在搜尋執行的查詢階段與擷取階段之間執行。它會攔截查詢階段的結果，然後在將文件傳遞至擷取階段之前，正規化並合併來自不同查詢子句的文件分數。

## 分數正規化與合併

許多應用程式同時需要關鍵字比對與語意理解。舉例來說，BM25 能針對包含關鍵字的查詢準確提供相關的搜尋結果，而神經網路則在查詢需要自然語言理解時表現良好。因此，您可能會想將 BM25 的搜尋結果與 k-NN 或神經搜尋的結果合併。然而，BM25 與 k-NN 搜尋使用不同的尺度來計算相符文件的相關性分數。在合併來自多個查詢的分數之前，將它們正規化使它們位於相同尺度是有益的，如實驗資料所示。如需進一步了解分數正規化與合併（包括基準測試與各種技術），請參閱[這篇語意搜尋部落格文章](https://opensearch.org/blog/semantic-science-benchmarks/)。

## 正規化技術

OpenSearch 會個別正規化每個查詢子句。對於給定的子句，它只會從該子句本身的結果計算該技術所需的統計資料，然後重新調整該子句中每個分數的尺度。該子句未傳回的文件對其統計資料沒有任何貢獻。

由於統計資料是從傳回的結果而非整個索引衍生而來，正規化後的分數取決於每個子句傳回多少結果。如需更多資訊，請參閱[搜尋調校建議](#search-tuning-recommendations)。

### Min-max 正規化

Min-max 正規化會將查詢子句的分數重新調整至 [0.0, 1.0] 範圍，作法是減去該子句的最低分數，再除以該子句的分數範圍：

$$\text{n_score} = \frac {\text{score} - \text{min_score}} {\text{max_score} - \text{min_score}}$$

該子句中分數最高的文件會得到 `1.0` 的分數。OpenSearch 會將正好為 `0.0` 的正規化分數取代為 `0.001`，因為 `0.0` 的分數具有 `match_none` 的特殊意義，所以該子句中分數最低的文件會得到 `0.001`。如果子句中的每份文件分數都相同，包括只傳回一份文件的子句，則該子句的最低與最高分數相等，且該子句中的每份文件都會得到 `1.0`。

由於只有正好為 `0.0` 的分數會被取代，此取代可能會重新排序子句中分數較低的文件。任何正規化分數小於 `0.001` 的文件，其排名都會低於分數最低的文件，而該文件正好得到 `0.001`。舉例來說，某個子句傳回原始分數 `10000`、`9` 與 `8`，會將它們正規化為 `1.0`、`0.00010008` 與 `0.001`，因此分數為 `8` 的文件排名會高於分數為 `9` 的文件。當某份文件的分數超出子句最低分數的程度小於該子句分數範圍的 0.1% 時，該文件就會受到影響；這種情況發生在子句中某個分數大約是其他分數的 1,000 倍時。

若要依據固定閾值而非傳回結果的最低與最高分數進行正規化，請設定 `lower_bounds` 與 `upper_bounds` 參數。如需更多資訊，請參閱[請求本文欄位](#request-body-fields)。

### L2 正規化

L2 正規化會將查詢子句中的每個分數除以該子句中所有分數的歐幾里得範數：

$$\text{n_score}_i = \frac {\text{score}_i} {\sqrt{\text{score}_1^2 + \text{score}_2^2 + \dots + \text{score}_n^2}}$$

正規化後的分數會保留原始分數的比例，因此同一子句中分數為另一份文件兩倍的文件，在正規化後分數仍是兩倍。由於每個分數都除以相同的範數，且沒有任何單一分數能超過該範數，正規化後的分數會落在 [0.0, 1.0] 範圍內。與 min-max 正規化不同，L2 正規化不會將 `1.0` 指派給分數最高的文件。子句每多傳回一個結果就會增加範數，因而降低該子句中其他每份文件的正規化分數。只有當子句只傳回單一文件時，範數才會等於該文件的分數，且該文件會得到 `1.0`。

### Z-score 正規化

Z-score 正規化會從每個分數減去查詢子句分數的平均值，再將結果除以這些分數的樣本標準差：

$$\text{n_score} = \frac {\text{score} - \text{mean}} {\text{sd}}$$

分數低於所屬子句平均值的文件會產生負的 z-score。由於負值不是有效的相關性分數，OpenSearch 會將每個小於或等於 `0.0` 的正規化分數取代為 `0.001`。因此，所有分數低於查詢子句平均值的文件都會得到相同的正規化分數，且它們在該子句內的相對順序會遺失。分數高於平均值的文件則不受固定範圍限制，可能得到大於 `1.0` 的正規化分數。

分數正好等於所屬子句平均值的文件是特殊情況：它會得到該子句中最高的原始分數，而非 z-score。如果子句中的每份文件分數都相同，包括只傳回一份文件的子句，則每份文件都符合平均值，因此該子句的分數完全不會被重新調整。

`z_score` 技術只支援 `arithmetic_mean` 合併技術。

### 選擇正規化技術

請使用下表比較這三種技術。

| | `min_max` | `l2` | `z_score` |
| :--- | :--- | :--- | :--- |
| 輸出範圍 | [0.0, 1.0]，其中 `0.0` 會取代為 `0.001` | [0.0, 1.0] | 非固定範圍，其中所有小於或等於 `0.0` 的值都會取代為 `0.001` |
| 子句中分數最高文件的分數 | 一律為 `1.0` | 小於 `1.0`，除非該子句只傳回單一文件 | 不固定，且可能超過 `1.0` |
| 子句內的分數比例 | 不保留 | 保留 | 不保留 |
| 使用的統計資料 | 最低與最高分數 | 所有分數 | 所有分數 |
| 單一離群值對子句中其他文件的影響 | 壓縮它們的分數，但保持彼此不同 | 壓縮它們的分數，但保持彼此不同 | 將它們推至子句平均值以下，因此它們全都塌縮為 `0.001` |
| 子句中文件的排序 | 保留，但正規化分數低於 `0.001` 的文件排名會低於分數最低的文件 | 保留 | 對每份分數低於子句平均值的文件都會遺失 |
| 支援的合併技術 | 全部 | 全部 | `arithmetic_mean` |

下列指引適用於每種技術：

- 當您想要可預測尺度、可直接推論的正規化分數時，或當您想透過 `lower_bounds` 與 `upper_bounds` 參數依據固定閾值進行正規化時，請使用 `min_max`（預設值）。
- 當查詢子句內分數之間的比例帶有最終排名應反映的資訊時，請使用 `l2`。請注意，`l2` 並不會比 `min_max` 更分散其餘文件：由於子句的 L2 範數一律大於或等於其分數範圍，`l2` 分隔任兩份文件的程度會小於或等於 `min_max` 分隔它們的程度。
- 當查詢子句產生的分數分布主要差異在於離散程度時，請使用 `z_score`。當子句傳回的結果很少或包含離群值時請避免使用，因為每份分數低於子句平均值的文件都會塌縮為 `0.001`。單一高離群值可能會將平均值拉高至所有其餘分數之上，並抹除該子句中其他每份文件的排序。

### 範例：比較正規化技術

以下範例將三種技術全部套用至相同資料，讓您比較其輸出。此範例使用直接在各文件中指定的二維向量，讓您可以手動驗證運算，並使用單一分片，讓分數可以重現。

此範例使用與[倒數排名融合]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/rrf/)相同的索引和查詢，因此您也可以將這些結果與以排名為基礎的組合結果進行比較。
{: .note}

建立索引，其中包含用於關鍵字比對的文字欄位，以及用於語意比對的向量欄位：

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

分別執行時，兩個查詢子句會產生不同尺度的分數。針對 `running shoes` 的 `match` 子句會傳回兩份文件，而針對 `[0.9, 0.1]` 且將 `k` 設為 `3` 的 `knn` 子句會傳回三份文件：

| 文件 ID | `item_name` | 關鍵字分數 | 向量分數 |
| :--- | :--- | :--- | :--- |
| `1` | `kids running shoes` | 0.8167638 | -- |
| `2` | `mens lightweight running shoes for road racing` | 0.5356597 | 1.0 |
| `3` | `trail runners` | -- | 0.98039216 |
| `4` | `athletic socks` | -- | 0.7575758 |

為每種正規化技術各建立一個搜尋管線，將 `min_max` 分別替換為 `l2` 和 `z_score`，以建立另外兩個管線：

```json
PUT /_search/pipeline/min-max-pipeline
{
  "description": "Normalize with min_max and combine with arithmetic_mean",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": {
          "technique": "min_max"
        },
        "combination": {
          "technique": "arithmetic_mean"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

在 [`hybrid` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/hybrid/)中組合這兩個查詢子句，並套用其中一個管線：

```json
GET /products/_search?search_pipeline=min-max-pipeline
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

由於省略了 `weights` 參數，`arithmetic_mean` 會為兩個子句賦予相同權重。某個子句未傳回的文件會在分子中貢獻 `0`，但仍計入分母，因此僅符合兩個子句其中之一的文件，其正規化分數會減半。

使用 `min_max` 時，文件 `1` 會正規化為 `1.0`，因為它是關鍵字子句中分數最高的文件，而文件 `2` 會正規化為 `0.001`，因為它是該子句中分數最低的文件。文件 `2` 的整體排名仍為第一，但領先幅度很小：

| 文件 ID | 關鍵字正規化分數 | 向量正規化分數 | `_score` |
| :--- | :--- | :--- | :--- |
| `2` | 0.001 | 1.0 | 0.5005 |
| `1` | 1.0 | -- | 0.5 |
| `3` | -- | 0.9191176 | 0.4595588 |
| `4` | -- | 0.001 | 0.0005 |

使用 `l2` 時，各子句的分數會除以各自的範數：關鍵字子句為 0.97674686，向量子句為 1.5921966。沒有任何分數會被強制設為端點值，因此文件 `2` 保留了較大比例的關鍵字分數貢獻，且相較於文件 `1` 的領先幅度擴大：

| 文件 ID | 關鍵字正規化分數 | 向量正規化分數 | `_score` |
| :--- | :--- | :--- | :--- |
| `2` | 0.54841197 | 0.62806314 | 0.5882375 |
| `1` | 0.8362083 | -- | 0.41810414 |
| `3` | -- | 0.61574817 | 0.30787408 |
| `4` | -- | 0.47580546 | 0.23790273 |

使用 `z_score` 時，文件 `2` 和 `4` 的分數等於或低於各自子句的平均值，因此兩者在該子句中的分數都會設為 `0.001`。文件 `2` 因而失去大部分的關鍵字分數貢獻，而文件 `1` 排名第一：

| 文件 ID | 關鍵字正規化分數 | 向量正規化分數 | `_score` |
| :--- | :--- | :--- | :--- |
| `1` | 0.70710695 | -- | 0.35355347 |
| `2` | 0.001 | 0.6486226 | 0.32481128 |
| `3` | -- | 0.5030134 | 0.2515067 |
| `4` | -- | 0.001 | 0.0005 |

三種技術從相同輸入產生三種不同排名，而 `z_score` 會將另一份文件提升至第一名。請依據您自己的資料和相關性評判清單評估這些技術，而非根據這些結果選擇其中一種。如需詳細資訊，請參閱[最佳化混合搜尋]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/optimize-hybrid-search/)。

## 先查詢再擷取

OpenSearch 支援兩種搜尋類型：`query_then_fetch` 和 `dfs_query_then_fetch`。下圖概述先查詢再擷取的流程，其中包含正規化處理器。

![正規化處理器流程圖]({{site.url}}{{site.baseurl}}/images/normalization-processor.png)

當您將搜尋請求傳送至節點時，該節點會成為 _協調節點_。在搜尋的第一個階段，也就是 _查詢階段_，協調節點會將搜尋請求路由至索引中的所有分片，包括主要分片和副本分片。接著，每個分片會在本機執行搜尋查詢，並傳回符合條件文件的中繼資料，其中包含文件 ID 和相關性分數。然後，`normalization-processor` 會正規化並組合不同查詢子句的分數。協調節點會合併並排序各分片的本機結果清單，彙整出符合查詢且排名最高的文件全域清單。之後，搜尋執行會進入 _擷取階段_，協調節點會向全域清單中文件所在的分片請求這些文件。每個分片會將文件的 `_source` 傳回協調節點。最後，協調節點會將包含結果的搜尋回應傳回給您。

## 請求本文欄位

下表列出所有可用的請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`normalization.technique` | 字串 | 用於正規化分數的技術。有效值為 [`min_max`](https://en.wikipedia.org/wiki/Feature_scaling#Rescaling_(min-max_normalization))、[`l2`](https://en.wikipedia.org/wiki/Cosine_similarity#L2-normalized_Euclidean_distance) 和 [`z_score`](https://en.wikipedia.org/wiki/Standard_score)。選用。預設為 `min_max`。
 `normalization.parameters.lower_bounds` | 物件陣列 | 定義每個查詢的下限值（最低分數門檻）。陣列中的物件數量必須與查詢數量相同。選用。僅在正規化技術為 [`min_max`](https://en.wikipedia.org/wiki/Feature_scaling#Rescaling_(min-max_normalization)) 時適用。若未提供，OpenSearch 不會對任何子查詢套用下限，而是使用擷取結果中的實際最低分數進行正規化。
`normalization.parameters.lower_bounds.mode` | 字串 | 指定如何將下限套用至查詢。有效值為：<br> - `apply`：使用 `min_score` 進行正規化，不修改原始分數。公式：`min_max_score = if (score < lowerBoundScore) then (score - minScore) / (maxScore - minScore) else (score - lowerBoundScore) / (maxScore - lowerBoundScore)`。<br> - `clip`：將低於下限的分數替換為 `min_score`。公式：`min_max_score = if (score < lowerBoundScore) then 0.0 else (score - lowerBoundScore) / (maxScore - lowerBoundScore)`。<br> - `ignore`：不對此查詢套用下限，改用標準的 `min_max` 公式。<br> 選用。預設為 `apply`。 
`normalization.parameters.lower_bounds.min_score` | 浮點數 | 下限門檻。有效值範圍為 [-10000.0, 10000.0]。若 `mode` 設為 `ignore`，則此值不會產生作用。選用。預設為 `0.0`。
`normalization.parameters.upper_bounds` | 物件陣列 | 定義每個查詢的上限值（最高分數門檻）。陣列中的物件數量必須與查詢數量相同。選用。僅在 `normalization.technique` 設為 `min_max` 時適用。若未提供，OpenSearch 不會對任何子查詢套用上限，而是使用擷取結果中的實際最高分數進行正規化。
`normalization.parameters.upper_bounds.mode` | 字串 | 指定如何將上限套用至查詢。有效值為：<br> - `apply`：使用 `max_score` 進行正規化，不修改原始分數。公式：`min_max_score = if (score > upperBoundScore) then (score - minScore) / (maxScore - minScore) else (score - minScore) / (upperBoundScore - minScore)`。<br> - `clip`：將高於上限的分數替換為 `max_score`。公式：`min_max_score = if (score > upperBoundScore) then 1.0 else (score - minScore) / (upperBoundScore - minScore)`。<br> - `ignore`：不對此查詢套用上限，改用標準的 `min_max` 公式。<br> 選用。預設為 `apply`。 
`normalization.parameters.upper_bounds.max_score` | 浮點數 | 上限門檻。有效值範圍為 [-10000.0, 10000.0]。若 `mode` 設為 `ignore`，則此值不會產生作用。選用。預設為 `1.0`。 
`combination.technique` | 字串 | 用於組合分數的技術。有效值為 [`arithmetic_mean`](https://en.wikipedia.org/wiki/Arithmetic_mean)、[`geometric_mean`](https://en.wikipedia.org/wiki/Geometric_mean) 和 [`harmonic_mean`](https://en.wikipedia.org/wiki/Harmonic_mean)。選用。預設為 `arithmetic_mean`。`z_score` 僅支援 `arithmetic_mean`。
`combination.parameters.weights` | 浮點數值陣列 | 指定每個查詢使用的權重。有效值範圍為 [0.0, 1.0]，表示以小數表示的百分比。權重越接近 1.0，查詢獲得的權重就越高。`weights` 陣列中的值數量必須等於查詢數量。陣列中各值的總和必須等於 1.0。選用。若未提供，所有查詢都會獲得相同權重。
`tag` | 字串 | 處理器的識別碼。選用。
`description` | 字串 | 處理器的說明。選用。
`ignore_failure` | 布林值 | 此處理器會忽略此值。若處理器失敗，管線一律會失敗並傳回錯誤。 

## 範例 

下列範例示範如何使用含有 `normalization-processor` 的搜尋管線。 

如需完整範例，請參閱[語意與混合搜尋入門]({{site.url}}{{site.baseurl}}/ml-commons-plugin/semantic-search#tutorial)。

### 建立搜尋管線 

下列請求會建立一個搜尋管線，其中包含使用 `min_max` 正規化技術與 `arithmetic_mean` 組合技術的 `normalization-processor`。此組合技術為第一個查詢指派 30% 的權重，並為第二個查詢指派 70% 的權重：

```json
PUT /_search/pipeline/nlp-search-pipeline
{
  "description": "Post processor for hybrid search",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": {
          "technique": "min_max"
        },
        "combination": {
          "technique": "arithmetic_mean",
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

下列範例示範如何搭配 `min_max` 正規化技術使用 `lower_bounds` 與 `upper_bounds` 參數。此範例在組合技術中省略 `weights` 參數，因此查詢預設會以相等權重加權。在此範例中，`lower_bounds` 參數用於為混合搜尋中的每個查詢設定不同的下限，而 `upper_bounds` 參數用於設定不同的上限。第一個查詢套用 0.5 的下限，並將上限裁剪為 0.8。第二個查詢則同時忽略下限與上限。如此即可針對混合搜尋中的每個查詢微調正規化程序：

```json
PUT /_search/pipeline/nlp-search-pipeline
{
  "description": "Post processor for hybrid search",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": {
          "technique": "min_max",
          "parameters": {
            "lower_bounds": [
                {
                  "mode": "apply",
                  "min_score": 0.5
                },
                {
                  "mode": "ignore"
                }
              ],
            "upper_bounds": [
              {
                "mode": "clip",
                "max_score": 0.8
              },
              {
                "mode": "ignore"
              }
            ]
          }
        },
        "combination": {
          "technique": "arithmetic_mean"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 使用搜尋管線

請在 `hybrid` 查詢中提供您要合併的查詢子句，並套用上一節建立的搜尋管線，讓分數以所選技術合併：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "_source": {
    "exclude": [
      "passage_embedding"
    ]
  },
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "text": {
              "query": "horse"
            }
          }
        },
        {
          "neural": {
            "passage_embedding": {
              "query_text": "wild west",
              "model_id": "aVeif4oB5Vm0Tdw8zYO2",
              "k": 5
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

如需設定混合搜尋的更多資訊，請參閱[混合搜尋]({{site.url}}{{site.baseurl}}/search-plugins/hybrid-search/)。

## 搜尋調校建議

若要提升搜尋相關性，我們建議增加樣本大小。

如果混合查詢未傳回某些預期結果，可能是因為子查詢傳回的文件太少。`normalization-processor` 只會轉換各子查詢傳回的結果，不會執行任何額外的取樣。在我們的實驗中，我們使用 [nDCG@10](https://en.wikipedia.org/wiki/Discounted_cumulative_gain) 依據傳回的文件數量 (size) 來衡量資訊檢索品質。我們發現，對於最多 1,000 萬份文件的資料集，size 落在 [100, 200] 範圍內效果最佳。我們不建議將 size 增加到超過建議值，因為較高的 size 值不會提升搜尋相關性，反而會增加搜尋延遲。
