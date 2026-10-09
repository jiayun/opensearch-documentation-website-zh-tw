---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Painless 擴充功能"
nav_order: 25
parent: Exact k-NN search with a scoring script
grand_parent: Vector search techniques
has_children: false
has_math: true
redirect_from:
  - /search-plugins/knn/painless-functions/ 
---

# Painless 指令碼擴充功能

透過 Painless 指令碼擴充功能，您可以直接在 Painless 指令碼中使用 k 最近鄰（k-NN）距離函式，對 `knn_vector` 欄位執行運算。為了確保指令碼的安全性，Painless 對每個情境允許使用的函式與類別有嚴格的限制。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。OpenSearch 為 [k-NN 評分指令碼]({{site.url}}{{site.baseurl}}/search-plugins/knn/knn-score-script/) 中使用的幾個距離函式加入了 Painless 指令碼擴充功能，讓您可以用它們自訂 k-NN 工作負載。

## 開始使用 k-NN Painless 指令碼函式

若要使用 k-NN Painless 指令碼函式，請先依照 [向量評分指令碼入門]({{site.url}}{{site.baseurl}}/search-plugins/knn/knn-score-script#getting-started-with-the-scoring-script-for-vectors) 的說明，建立一個含有 `knn_vector` 欄位的索引。建立索引並匯入一些資料之後，即可使用 Painless 擴充功能：

```json
GET my-knn-index-2/_search
{
  "size": 2,
  "query": {
    "script_score": {
      "query": {
        "bool": {
          "filter": {
            "term": {
              "color": "BLUE"
            }
          }
        }
      },
      "script": {
        "source": "1.0 + cosineSimilarity(params.query_value, doc[params.field])",
        "params": {
          "field": "my_vector",
          "query_value": [9.9, 9.9]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

`field` 必須對應到 `knn_vector` 欄位，而 `query_value` 必須是與 `field` 維度相同的浮點數陣列。

## 函式類型

下表說明 OpenSearch 提供的 Painless 函式。

函式名稱 | 函式簽章 | 說明
:--- | :---
`l2Squared` | `float l2Squared (float[] queryVector, doc['vector field'])` | 此函式計算給定查詢向量與文件向量之間的 L2 距離（歐氏距離）的平方。距離越短代表文件越相關，因此此範例會反轉 `l2Squared` 函式的回傳值。如果文件向量與查詢向量相符，結果為 `0`，因此此範例也在距離上加上 `1`，以避免除以零的錯誤。
`l1Norm` | `float l1Norm (float[] queryVector, doc['vector field'])` | 此函式計算給定查詢向量與文件向量之間的 L1 範數距離（曼哈頓距離）。
`cosineSimilarity` | `float cosineSimilarity (float[] queryVector, doc['vector field'])` | 餘弦相似度是查詢向量與文件向量的內積，兩者皆正規化為長度 `1`。如果查詢向量的大小在整個查詢過程中不變，您可以傳入查詢向量的大小以提升效能，而不必為每個篩選後的文件重複計算大小：<br /> `float cosineSimilarity (float[] queryVector, doc['vector field'], float normQueryVector)` <br />一般而言，餘弦相似度的範圍是 [-1, 1]。然而，在資訊檢索的情況下，兩份文件的餘弦相似度範圍是 `0` 到 `1`，因為 `tf-idf` 統計值不可能為負。因此，OpenSearch 加上 `1.0`，使餘弦相似度分數恆為正值。
`hamming` | `float hamming (float[] queryVector, doc['vector field'])` | 此函式計算給定查詢向量與文件向量之間的漢明距離。漢明距離是對應元素不同的位置數量。距離越短代表文件越相關，因此此範例會反轉漢明距離的回傳值。

OpenSearch 2.16 及之後版本支援二進位向量的 `hamming` 空間類型。如需更多資訊，請參閱 [二進位 k-NN 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized#binary-vectors)。
{: .note}

## 限制

1. 如果文件的 `knn_vector` 欄位維度與查詢不同，函式會擲回 `IllegalArgumentException`。

2. 如果向量欄位沒有值，函式會擲回 `IllegalStateException`。

   您可以先檢查文件的欄位是否含有值，以避免此問題：

   ```
   "source": "doc[params.field].size() == 0 ? 0 : 1 / (1 + l2Squared(params.query_value, doc[params.field]))",
   ```

   由於分數只能是正值，此指令碼會將含有向量欄位的文件排在沒有向量欄位的文件之前。

使用餘弦相似度時，傳入零向量 (`[0, 0, ...]`) 作為輸入是無效的。因為這類向量的大小為 0，會在對應的公式中引發 `divide by 0` 例外。包含零向量的請求將被拒絕，並擲回對應的例外。
{: .note }
