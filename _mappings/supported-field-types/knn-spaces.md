---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "空間"
parent: k-NN vector
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/knn-spaces/
nav_order: 10
has_math: true
---

# 向量空間

在向量搜尋中，_空間_ (space) 定義了兩個向量之間距離（或相似度）的計算方式。空間的選擇會影響搜尋作業期間最近鄰的判定方式。

## 距離計算

空間定義了用來測量兩點之間距離的函式，以判定 k 個最近鄰。在 k-NN 搜尋中，分數越低代表結果越近、越好。這與 OpenSearch 為結果評分的方式相反，在 OpenSearch 中分數越高代表結果越好。OpenSearch 支援下列空間。

並非每種方法/引擎組合都支援每個空間。如需支援的空間清單，請參閱[方法文件]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/)中特定引擎的章節。
{: .note}

| 空間類型 | 搜尋類型 | 距離函式 ($$d$$ ) | OpenSearch 分數 |
| :--- | :--- | :--- |
| `l1`  | 近似、精確 | $$ d(\mathbf{x}, \mathbf{y}) = \sum_{i=1}^n \lvert x_i - y_i \rvert $$ | $$ score = {1 \over {1 + d} } $$ |
| `l2`  | 近似、精確 | $$ d(\mathbf{x}, \mathbf{y}) = \sum_{i=1}^n (x_i - y_i)^2 $$ | $$ score = {1 \over 1 + d } $$ |
| `linf` | 近似、精確 | $$ d(\mathbf{x}, \mathbf{y}) = max(\lvert x_i - y_i \rvert) $$ | $$ score = {1 \over 1 + d } $$ |
| `cosinesimil` | 近似、精確 | $$ d(\mathbf{x}, \mathbf{y}) = 1 - cos { \theta } = 1 - {\mathbf{x} \cdot \mathbf{y} \over \lVert \mathbf{x}\rVert \cdot \lVert \mathbf{y}\rVert}$$$$ = 1 - {\sum_{i=1}^n x_i y_i \over \sqrt{\sum_{i=1}^n x_i^2} \cdot \sqrt{\sum_{i=1}^n y_i^2}}$$，<br> 其中 $$\lVert \mathbf{x}\rVert$$ 與 $$\lVert \mathbf{y}\rVert$$ 分別代表向量 $$\mathbf{x}$$ 與 $$\mathbf{y}$$ 的範數。 | $$ score = {2 - d \over 2} $$ |
| `innerproduct`（Lucene 自 OpenSearch 2.13 版起支援） | 近似 | **NMSLIB** 與 **Faiss**：<br> $$ d(\mathbf{x}, \mathbf{y}) = - {\mathbf{x} \cdot \mathbf{y}} = - \sum_{i=1}^n x_i y_i $$  <br><br>**Lucene**：<br> $$ d(\mathbf{x}, \mathbf{y}) = {\mathbf{x} \cdot \mathbf{y}} = \sum_{i=1}^n x_i y_i $$ | **NMSLIB** 與 **Faiss**：<br> $$ \text{If} d \ge 0,  score = {1 \over 1 + d }$$ <br> $$\text{If} d < 0, score = −d + 1$$  <br><br>**Lucene:**<br> $$ \text{If} d > 0, score = d + 1 $$ <br> $$\text{If} d \le 0, score = {1 \over 1 + (-1 \cdot d) }$$ |
| `innerproduct`（Lucene 自 OpenSearch 2.13 版起支援） | 精確 | $$ d(\mathbf{x}, \mathbf{y}) = - {\mathbf{x} \cdot \mathbf{y}} = - \sum_{i=1}^n x_i y_i $$ | $$ \text{If} d \ge 0,  score = {1 \over 1 + d }$$ <br> $$\text{If} d < 0, score = −d + 1$$ |
| `hamming`（二進位向量自 OpenSearch 2.16 版起支援） | 近似、精確 | $$ d(\mathbf{x}, \mathbf{y}) = \text{countSetBits}(\mathbf{x} \oplus \mathbf{y})$$ | $$ score = {1 \over 1 + d } $$ |
| `hammingbit`（支援二進位向量與 long 類型向量） | 精確 | $$ d(\mathbf{x}, \mathbf{y}) = \text{countSetBits}(\mathbf{x} \oplus \mathbf{y})$$ | $$ score = {1 \over 1 + d } $$ |

餘弦相似度公式不包含 `1 -` 前綴。不過，由於相似度搜尋程式庫將較低的分數視為更近的結果，因此它們會在餘弦相似度空間中傳回 `1 - cosineSimilarity`——這就是距離函式中包含 `1 -` 的原因。
{: .note }

使用餘弦相似度時，不可傳入零向量 (`[0, 0, ...]`) 作為輸入。這是因為此類向量的量值為 0，會在對應的公式中引發 `divide by 0` 例外。包含零向量的請求將被拒絕，並擲回對應的例外。
{: .note }

`hamming` 空間類型自 OpenSearch 2.16 版起支援二進位向量。如需更多資訊，請參閱[二進位 k-NN 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized#binary-vectors)。
{: .note}

搭配 Faiss 引擎使用 `cosinesimil` 時，向量會在編製索引期間自動正規化為單位長度，因為 Faiss 內部會對已正規化的向量使用內積。如果您的向量已經正規化，請考慮改用 `innerproduct` 而非 `cosinesimil`，以取得等效結果並明確控制正規化。
{: .important}

## 指定空間類型

空間類型是在建立索引時指定的。

您可以在欄位對應的最上層指定空間類型：

```json
PUT /test-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector1": {
        "type": "knn_vector",
        "dimension": 3,
        "space_type": "l2"
      }
    }
  }
}
```
{% include copy-curl.html %}

或者，如果定義方法，您可以在 `method` 物件內指定空間類型：

```json
PUT test-index
{
  "settings": {
    "index": {
      "knn": true,
      "knn.algo_param.ef_search": 100
    }
  },
  "mappings": {
    "properties": {
      "my_vector1": {
        "type": "knn_vector",
        "dimension": 1024,
        "method": {
          "name": "hnsw",
          "space_type": "l2",
          "engine": "nmslib",
          "parameters": {
            "ef_construction": 128,
            "m": 24
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}
