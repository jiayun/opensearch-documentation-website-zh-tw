---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 MMR 重新排序的向量搜尋"
nav_order: 60
parent: Specialized vector search
has_children: false
has_math: true
---

# 使用 MMR 重新排序的向量搜尋
**於 3.3 版導入**
{: .label .label-purple }

最大邊際相關性 (MMR) 搜尋有助於在搜尋結果中平衡相關性與多樣性。MMR 不只傳回最相似的文件，而是選取既與查詢相關、彼此又互不相同的結果。這能改善結果集的涵蓋範圍並減少重複，在向量搜尋情境中特別有用。

MMR 重新排序會平衡兩個相互競爭的目標：

 - 相關性：文件與查詢的符合程度。

 - 多樣性：文件與已選取文件之間的差異程度。

此演算法使用下列公式為每個候選文件計算分數：

$$MMR = (1 − \lambda) \times \text{relevance_score} - \lambda \times max(\text{similarity_with_selected_docs})$$,

其中：

 - $$\lambda$$ 是多樣性參數（越接近 1 代表多樣性越高）。

 - $$\text{relevance_score}$$ 衡量查詢向量與候選文件向量之間的相似度。

 - $$\text{similarity_with_selected_docs}$$ 衡量候選文件與已選取文件之間的相似度。

透過調整 $$\lambda$$，您可以控制高相關性結果與結果集更多樣化涵蓋範圍之間的取捨。

# 必要條件

若要使用 MMR，您必須啟用[系統產生的搜尋處理器工廠]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/system-generated-search-processors/)。將 `cluster.search.enabled_system_generated_factories` 設定（預設為空清單）設為 `*`（所有工廠），或明確加入所需的工廠：

```json
PUT _cluster/settings
{
  "persistent": {
    "cluster.search.enabled_system_generated_factories": [
      "mmr_over_sample_factory",
      "mmr_rerank_factory"
    ]
  }
}
```
{% include copy-curl.html %}

# 參數

`mmr` 物件提供於 Search API 請求本文的 `ext` 物件中，並支援下列參數。

| 參數                 | 資料類型 | 必要/選用                                 | 說明                                                                                                                                                                                 |
| ------------------------- | --------- | ----------------------------------------- |---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `diversity`               | Float     | 選用                                        | 控制重新排序過程中多樣性 ($$\lambda$$) 的權重。有效值範圍為 `0` 至 `1`（含端點）。值為 `1` 時優先考量最大多樣性；`0` 則停用多樣性。預設為 `0.5`。 |
| `candidates`              | Integer   | 選用                                        | 在套用 MMR 重新排序之前要擷取的候選文件數量。預設為 `3 * size`，其中 `size` 是查詢的 `size` 參數（要求傳回的結果數量）。                                                                                        |
| `vector_field_path`       | String    | 選用（遠端索引為必要） | 用於 MMR 重新排序的向量欄位路徑。若未提供，OpenSearch 會自動從搜尋請求中解析。                                                            |
| `vector_field_data_type`  | String    | 選用（遠端索引為必要） | 向量欄位的資料類型。用於解析欄位並計算相似度。若未提供，OpenSearch 會從索引對應中解析。                                            |
| `vector_field_space_type` | String    | 選用（遠端索引為必要） | 用於決定向量欄位的相似度函式，例如餘弦相似度或歐氏距離。若未提供，OpenSearch 會從索引對應中解析。有效值請參閱[距離計算]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-spaces/#distance-calculation)。             |
| `explain`                 | Boolean   | 選用                               | 當設為 `true` 時，會在每個所選命中的 `_source` 中加入一個 `mmr_explain` 物件，其中包含每個命中的 MMR 評分詳細資訊。預設為 `false`。請參閱[說明 MMR 評分](#explain-mmr-scoring)。 |


# 範例請求

下列範例示範如何在 `knn` 查詢中使用 `mmr` 參數：

```json
POST /my-index/_search
{
  "query": {
    "knn": {
      "my_vector_field": {
        "vector": [0.12, 0.54, 0.91],
        "k": 10
      }
    }
  },
  "ext": {
    "mmr": {
      "diversity": 0.7
    }
  }
}
```
{% include copy-curl.html %}

下列範例示範如何在 `neural` 查詢中使用 `mmr` 參數：

```json
POST /my-index/_search
{
  "query": {
    "neural": {
      "my_vector_field": {
        "query_text": "query text",
        "model_id": "<your model id>"
      }
    }
  },
  "ext": {
    "mmr": {
      "diversity": 0.6,
      "candidates": 50,
      "vector_field_path": "my_vector_field",
      "vector_field_data_type": "float",
      "vector_field_space_type": "l2"
    }
  }
}
```
{% include copy-curl.html %}

查詢多個索引時，所有向量欄位必須具有相符的資料類型與空間類型。這些設定會決定文件比較所使用的相似度函式。
{: .note}

# 說明 MMR 評分
**於 3.7 版導入**
{: .label .label-purple }

當 `explain` 設為 `true` 時，每個所選命中的 `_source` 會包含一個 `mmr_explain` 物件，說明文件被選取的原因。這對於偵錯及了解 MMR 重新排序行為很有幫助。

`mmr_explain` 物件包含下列欄位。

| 欄位 | 說明 |
|-------|-------------|
| `original_score` | 來自 k-NN 或神經搜尋的原始相關性分數。 |
| `max_similarity_to_selected` | 此文件與任何已選取文件之間的最大向量相似度。對於第一個選取的文件，此值為 `0.0`。 |
| `mmr_score` | 選取當下使用公式 `(1 - diversity) * original_score - diversity * max_similarity_to_selected` 計算出的 MMR 分數。 |
| `mmr_formula` | 以實際值代入後的 MMR 公式之人類可讀表示。 |

選取順序與先前選取的文件可從每個命中在結果清單中的位置推斷。
{: .note}

下列範例示範如何使用 `explain` 參數：

```json
POST /my-index/_search
{
  "query": {
    "knn": {
      "my_vector_field": {
        "vector": [0.12, 0.54, 0.91],
        "k": 10
      }
    }
  },
  "ext": {
    "mmr": {
      "diversity": 0.5,
      "explain": true
    }
  }
}
```
{% include copy-curl.html %}

回應會在每個命中的 `_source` 中包含一個 `mmr_explain` 物件：

```json
{
  "hits": {
    "hits": [
      {
        "_id": "doc1",
        "_score": 1.0,
        "_source": {
          "text": "...",
          "mmr_explain": {
            "original_score": 1.0,
            "max_similarity_to_selected": 0.0,
            "mmr_score": 0.5,
            "mmr_formula": "(1 - 0.5000) * 1.0000 - 0.5000 * 0.0000 = 0.5000"
          }
        }
      },
      {
        "_id": "doc2",
        "_score": 0.95,
        "_source": {
          "text": "...",
          "mmr_explain": {
            "original_score": 0.95,
            "max_similarity_to_selected": 0.9,
            "mmr_score": 0.025,
            "mmr_formula": "(1 - 0.5000) * 0.9500 - 0.5000 * 0.9000 = 0.0250"
          }
        }
      }
    ]
  }
}
```

# 限制

下列限制適用於使用 MMR 重新排序的向量搜尋：

- **支援的查詢類型**：MMR 僅支援 `knn` 或 `neural` 查詢作為搜尋請求中的頂層查詢。若 `knn` 或 `neural` 查詢巢狀於其他查詢類型內（例如 `bool` 查詢或 `hybrid` 查詢），則不支援 MMR。

- **遠端索引需求**：查詢遠端索引時，您必須明確提供向量欄位資訊（`vector_field_path`、`vector_field_data_type` 與 `vector_field_space_type`）。不同於本機索引可由 OpenSearch 自動從索引對應中解析此中繼資料，系統無法可靠地從遠端叢集取得這些資訊。提供這些詳細資訊可確保正確解析向量資料並準確計算相似度。

## 相關文件

- [系統產生的搜尋處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/system-generated-search-processors/)