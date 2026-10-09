---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "神經稀疏"
parent: AI and vector search queries
has_children: true
nav_order: 55
redirect_from:
  - /query-dsl/specialized/neural-sparse/
---

# 神經稀疏查詢
**於 2.11 版推出**
{: .label .label-purple }

`neural_sparse` 查詢會針對神經稀疏功能執行向量欄位搜尋。您可以在兩種類型的向量欄位上執行此查詢：

- **`rank_features` 欄位**：用於傳統的[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-search/)
- **`sparse_vector` 欄位**：用於[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)

## 神經稀疏搜尋

在 `rank_features` 欄位上使用神經稀疏搜尋，以倒排索引的效率進行傳統稀疏向量搜尋。

您可以使用原始稀疏向量或文字來執行神經稀疏搜尋。文字可由內建分析器或斷詞器模型進行斷詞。

### 使用原始稀疏向量

直接提供稀疏向量嵌入以進行比對：

```json
"neural_sparse": {
  "<rank_features_field>": {
    "query_tokens": {
      "<token>": <weight>,
      ...
    }
  }
}
```

如需更多資訊，請參閱[使用原始向量的神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-with-raw-vectors/)。

### 使用文字與內建分析器

提供文字以使用內建 DL 模型分析器進行斷詞：

```json
"neural_sparse": {
  "<rank_features_field>": {
    "query_text": "<input text>",
    "analyzer": "bert-uncased"
  }
}
```

### 使用文字與自訂模型

提供文字以使用自訂斷詞器模型進行斷詞：

```json
"neural_sparse": {
  "<rank_features_field>": {
    "query_text": "<input text>",
    "model_id": "<model ID>"
  }
}
```

如需更多資訊，請參閱[自動產生稀疏向量嵌入]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-with-pipelines/)。

## 神經稀疏 ANN 搜尋
**於 3.3 版推出**
{: .label .label-purple }

在 `sparse_vector` 欄位上使用神經稀疏 ANN 搜尋，以提升查詢效能並維持高召回率。如需更多資訊，請參閱[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)。

神經稀疏 ANN 搜尋支援兩種引擎：Lucene 引擎與原生引擎。您可以在欄位對應中設定 `method.engine` 來選擇引擎。兩種引擎的查詢語法與所有支援的查詢參數皆相同。如需更多資訊，請參閱[引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#engines)。

您可以使用原始稀疏向量或文字來執行神經稀疏搜尋。

### 使用原始稀疏向量

```json
"neural_sparse": {
  "<sparse_vector_field>": {
    "query_tokens": {
      "<token>": <weight>,
      ...
    },
    "method_parameters": {
      "top_n": 10,
      "heap_factor": 1.0,
      "k": 10
    }
  }
}
```

### 使用文字與模型

```json
"neural_sparse": {
  "<sparse_vector_field>": {
    "query_text": "<input text>",
    "model_id": "<model ID>",
    "method_parameters": {
      "top_n": 10,
      "heap_factor": 1.0,
      "k": 10
    }
  }
}
```

## 請求本文欄位

最上層的欄位名稱會指定要對其執行搜尋查詢的向量欄位。您必須指定 `query_text` 或 `query_tokens` 來定義輸入。

### 一般欄位

這些欄位同時支援 `rank_features` 與 `sparse_vector` 欄位類型。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
|:--- |:--- |:--- |:--- |
| `query_text` | 字串 | 選用 | 要轉換為稀疏向量嵌入的查詢文字。必須指定 `query_text` 或 `query_tokens`。 |
| `query_tokens` | 詞元（字串）到權重（浮點數）的對應 | 選用 | 以詞元及其權重形式呈現的原始稀疏向量。用於直接輸入向量，作為 `query_text` 的替代方案。必須指定 `query_text` 或 `query_tokens`。 |
| `model_id` | 字串 | 選用 | 與 `query_text` 搭配使用。用於從查詢文字產生向量嵌入的稀疏編碼模型 ID（適用於雙編碼器模式）或斷詞器 ID（適用於僅文件模式）。模型/斷詞器必須先在 OpenSearch 中部署，才能在神經稀疏搜尋中使用。如需更多資訊，請參閱[在 OpenSearch 中使用自訂模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)與[自動產生稀疏向量嵌入]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-with-pipelines/)。如需在神經稀疏查詢中設定預設模型 ID 的資訊，請參閱[`neural_query_enricher`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/neural-query-enricher/)。不能與 `analyzer` 同時指定。 |
| `max_token_score` | 浮點數 | 選用 | （已棄用）此參數自 OpenSearch 2.12 起已棄用。僅為回溯相容性而保留，不再影響功能。請求中仍可提供此參數，但其值沒有任何影響。先前用於表示詞彙表中所有詞元分數的理論上限。|

### 僅適用於 rank_features 的欄位

| 欄位 | 資料類型 | 必要/選用 | 說明 |
|:--- |:--- |:--- |:--- |
| `analyzer` | 字串 | 選用 | 與 `query_text` 搭配使用。指定用於將查詢文字斷詞的內建 DL 模型分析器。有效值為 `bert-uncased` 與 `mbert-uncased`。預設為 `bert-uncased`。若 `model_id` 與 `analyzer` 均未指定，則使用預設分析器（`bert-uncased`）將文字斷詞。不能與 `model_id` 同時指定。如需更多資訊，請參閱[DL 模型分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/dl-model-analyzers/)。 |

### 僅適用於 sparse_vector 的欄位

| 欄位 | 資料類型 | 必要/選用 | 說明 |
|:--- |:--- |:--- |:--- |
| `method_parameters.top_n` | 整數 | 選用 | 指定要為近似稀疏查詢保留的權重最高查詢詞元數量。 |
| `method_parameters.heap_factor` | 浮點數 | 選用 | 控制召回率與效能之間的取捨。較高的值會提高召回率但降低查詢速度；較低的值會降低召回率但提升查詢速度。 |
| `method_parameters.k` | 整數 | 選用 | 指定近似神經搜尋演算法傳回的前 k 個最近結果數量。 |
| `method_parameters.filter` | 物件 | 選用 | 對查詢結果套用篩選條件。篩選條件的套用方式取決於為該欄位設定的引擎。請參閱[神經稀疏 ANN 搜尋中的篩選]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/filtering-in-sparse-search/)。 |

如果篩選條件相符的文件數少於 `k`，兩種引擎都會對篩選後的文件執行精確搜尋。超過該數量後，Lucene 引擎會在近似檢索後套用篩選條件，因此選擇性篩選可能產生少於 `k` 個結果，而原生引擎則會在篩選後的集合中進行檢索，可傳回完整的 `k` 個結果。此差異取決於欄位對應中設定的引擎。
{: .note}

## 範例

下列範例示範如何使用 `neural_sparse` 查詢。

### 在 rank_features 欄位上進行神經稀疏搜尋

您可以使用由分析器或模型斷詞的文字，或使用原始向量，在 `rank_features` 欄位上執行神經稀疏搜尋。

#### 使用由分析器斷詞的文字

若要使用由分析器斷詞的文字執行搜尋，請在請求中指定 `analyzer`。分析器必須與您在匯入時用於文字分析的模型相容：

```json
GET my-nlp-index/_search
{
  "query": {
    "neural_sparse": {
      "passage_embedding": {
        "query_text": "Hi world",
        "analyzer": "bert-uncased"
      }
    }
  }
}
```
{% include copy-curl.html %}

如需更多資訊，請參閱[DL 模型分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/dl-model-analyzers/)。

若未指定分析器，則會使用預設的 `bert-uncased` 分析器：

```json
GET my-nlp-index/_search
{
  "query": {
    "neural_sparse": {
      "passage_embedding": {
        "query_text": "Hi world"
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 使用由模型斷詞的文字

若要使用由斷詞器模型斷詞的文字進行搜尋，請在請求中提供模型 ID：

```json
GET my-nlp-index/_search
{
  "query": {
    "neural_sparse": {
      "passage_embedding": {
        "query_text": "Hi world",
        "model_id": "aP2Q8ooBpBj3wT4HVS8a"
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 使用原始向量

若要使用稀疏向量進行搜尋，請在 `query_tokens` 參數中提供稀疏向量：

```json
GET my-nlp-index/_search
{
  "query": {
    "neural_sparse": {
      "passage_embedding": {
        "query_tokens": {
          "hi" : 4.338913,
          "planets" : 2.7755864,
          "planet" : 5.0969057,
          "mars" : 1.7405145,
          "earth" : 2.6087382,
          "hello" : 3.3210192
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 在 sparse_vector 欄位上進行神經稀疏 ANN 搜尋

您可以使用文字或原始向量，在 `sparse_vector` 欄位上執行神經稀疏 ANN 搜尋。

#### 使用文字

若要使用自然語言進行搜尋，請提供 `query_text` 與已部署的稀疏編碼模型 ID：

```json
GET sparse-vector-index/_search
{
  "query": {
    "neural_sparse": {
      "sparse_embedding": {
        "query_text": "<input text>",
        "model_id": "<model ID>",
        "method_parameters": {
          "k": 10,
          "top_n": 10,
          "heap_factor": 1.0
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 使用原始向量與方法參數

若要使用預先計算的稀疏向量進行搜尋，請在 `query_tokens` 欄位中提供向量：

```json
GET sparse-vector-index/_search
{
  "query": {
    "neural_sparse": {
      "sparse_embedding": {
        "query_tokens": {
          "1055": 5.5
        },
        "method_parameters": {
          "heap_factor": 1.0,
          "top_n": 10,
          "k": 10
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 後續步驟

- 如需神經稀疏搜尋的更多資訊，請參閱[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-search/)。
- 如需神經稀疏 ANN 搜尋的更多資訊，請參閱[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)。
- 如需欄位類型資訊，請參閱[排名特徵]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/rank/)與[稀疏向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/sparse-vector/)。
- 如需篩選 `neural_sparse` 查詢結果的資訊，請參閱[神經稀疏 ANN 搜尋中的篩選]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/filtering-in-sparse-search/)。
