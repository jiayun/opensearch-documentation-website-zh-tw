---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Faiss 乘積量化"
parent: Vector quantization
grand_parent: Optimizing vector storage
nav_order: 30
has_children: false
has_math: true
---

# Faiss 乘積量化

乘積量化 (PQ) 是一種使用可設定的位元數來表示向量的技術。一般而言，相較於位元組量化或純量量化，它可達到更高的壓縮程度。PQ 的運作方式是將向量分割成 _m_ 個子向量，並以 _code_size_ 個位元編碼每個子向量。因此，向量所需的記憶體總量為 `m*code_size` 個位元，外加額外負荷。如需參數的詳細資訊，請參閱 [PQ 參數]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#pq-parameters)。PQ 僅支援 _Faiss_ 引擎，且可搭配 _HNSW_ 或 _IVF_ 近似最近鄰 (ANN) 演算法使用。

## 使用 Faiss 乘積量化

為了將準確度的損失降到最低，PQ 需要一個 _訓練_ 步驟，根據將要搜尋的資料分布來建立模型。

乘積量化器會針對每個子向量空間，對一組訓練向量執行 k-means 分群來進行訓練，並擷取要用於編碼的質心。訓練向量可以是將要匯入的向量子集，或是與將要匯入的向量具有相同分布和維度的向量。

在 OpenSearch 中，訓練向量必須存在於索引中。一般而言，訓練資料量取決於所使用的 ANN 演算法，以及索引中將儲存的資料量。對於以 IVF 為基礎的索引，建議的訓練向量數量為 `max(1000*nlist, 2^code_size * 1000)`。對於以 HNSW 為基礎的索引，建議數量為 `2^code_size*1000`。如需有關計算這些數字所用方法的詳細資訊，請參閱 [Faiss 文件](https://github.com/facebookresearch/faiss/wiki/FAQ#how-many-training-points-do-i-need-for-k-means)。

對於 PQ，需要同時選取 _m_ 和 _code_size_。_m_ 決定向量應分割成多少個子向量以分別編碼。因此，_dimension_ 必須能被 _m_ 整除。_code_size_ 決定用於編碼每個子向量的位元數。一般而言，我們建議設定為 `code_size = 8`，然後調整 _m_，以在記憶體佔用量與召回率之間取得所需的取捨。

如需設定使用 PQ 之索引的範例，請參閱[從模型建立向量索引]({{site.url}}{{site.baseurl}}/search-plugins/knn/approximate-knn/#building-a-vector-index-from-a-model)教學。

## 記憶體估算

雖然 PQ 旨在以 `m*code_size` 個位元表示個別向量，但實際上索引會耗用更多空間。這主要是因為儲存特定編碼表和輔助資料結構的額外負荷。

部分記憶體公式取決於現有的分段數量。這通常無法事先得知，但建議的預設值為 300。
{: .note}

### HNSW 記憶體估算

使用 PQ 的 HNSW 所需記憶體估計為 `1.1*(((pq_code_size / 8) * pq_m + 24 + 8 * hnsw_m) * num_vectors + num_segments * (2^pq_code_size * 4 * d))` 個位元組。

舉例來說，假設您有 100 萬個維度為 256 的向量，`hnsw_m` 為 16，`pq_m` 為 32，`pq_code_size` 為 8，且有 100 個分段。記憶體需求可估算如下：

```r
1.1 * ((8 / 8 * 32 + 24 + 8 * 16) * 1000000 + 100 * (2^8 * 4 * 256)) ~= 0.215 GB
```

### IVF 記憶體估算

使用 PQ 的 IVF 所需記憶體估計為 `1.1*(((pq_code_size / 8) * pq_m + 24) * num_vectors  + num_segments * (2^code_size * 4 * d + 4 * ivf_nlist * d))` 個位元組。

例如，假設您有 100 萬個維度為 256 的向量，`ivf_nlist` 為 512，`pq_m` 為 32，`pq_code_size` 為 8，且有 100 個分段。記憶體需求可估算如下：

```r
1.1 * ((8 / 8 * 64 + 24) * 1000000  + 100 * (2^8 * 4 * 256 + 4 * 512 * 256))  ~= 0.171 GB
```

## 後續步驟

- [記憶體最佳化的向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/)
- [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)