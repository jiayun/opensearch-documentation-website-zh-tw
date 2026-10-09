---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用純量量化的精確搜尋"
parent: Vector quantization
grand_parent: Optimizing vector storage
nav_order: 15
has_children: false
has_math: true
---

# 使用純量量化的精確搜尋
**於 3.6 版導入**
{: .label .label-purple }

OpenSearch 支援 `flat` 量化方法，可對 32 位元浮點數向量執行純量量化。與 [Faiss]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/faiss-scalar-quantization/) 和 [Lucene]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/lucene-scalar-quantization/) 引擎的 HNSW 純量量化（會建立可導覽圖以進行近似最近鄰搜尋）不同，`flat` 方法會對量化後的向量執行精確（暴力式）k-NN 搜尋。這能提供完美的召回率，但代價是大型資料集的搜尋延遲較高。

`flat` 方法與引擎無關，且不接受 `engine` 參數。在方法層級或 `flat` 方法的欄位層級指定 `engine` 會導致索引建立失敗。在 OpenSearch 3.8 或更早版本中建立的索引不受影響。`flat` 方法也不接受任何編碼器或方法參數。
{: .important}

`flat` 方法最適合較小的資料集，或需要精確搜尋結果且篩選條件嚴格的使用情境。對於可接受近似結果的較大資料集，請考慮使用 [Faiss]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/faiss-scalar-quantization/) 或 [Lucene]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/lucene-scalar-quantization/) 引擎的 HNSW 純量量化。
{: .tip}

## 使用純量量化執行精確搜尋

若要使用純量量化執行精確搜尋，請在建立向量索引時，將 k-NN 向量欄位的 `method.name` 設定為 `flat`。您也可以選擇設定 `compression_level` 來選取每個維度的位元數。對於 `float` 欄位，有效值為 `32x`（1 位元）、`16x`（2 位元）和 `8x`（4 位元）；對於 `half_float` 欄位，有效值為 `16x`（1 位元）和 `1x`（不量化）。若未指定 `compression_level`，`flat` 預設為 1 位元量化：`float` 欄位為 `32x`，`half_float` 欄位為 `16x`，因為壓縮率是根據資料類型的儲存大小（每個維度 32 或 16 位元）來衡量：

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
        "dimension": 4,
        "space_type": "l2",
        "compression_level": "16x",
        "method": {
          "name": "flat"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

純量量化僅套用於 `float` 和 `half_float` 向量。對於 `half_float` 欄位，`compression_level` 設為 `16x`（預設值）時會套用 1 位元量化，而 `1x` 則會對未量化的 16 位元浮點數 (FP16) 向量執行精確搜尋。若在對應 [k-NN 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/) 時將 `data_type` 參數變更為 `byte` 或任何其他不支援的類型，則請求會被拒絕。
{: .warning}

## 搜尋

`flat` 方法會在量化後的向量上進行搜尋，因此預設會啟用重新評分以維持搜尋召回率。搜尋分兩個階段執行：先搜尋量化索引，然後使用全精度向量對結果重新評分。預設的 `oversample_factor` 取決於 `compression_level`。如需更多資訊，請參閱[將量化結果重新評分至全精度]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#rescoring-quantized-results-to-full-precision)。

若要搜尋 flat 量化索引，請傳送以下請求：

```json
GET /test-index/_search
{
  "query": {
    "knn": {
      "my_vector1": {
        "vector": [1.5, 2.5, 3.5, 4.5],
        "k": 5
      }
    }
  }
}
```
{% include copy-curl.html %}

若要自訂 `oversample_factor`，請在查詢中提供 `rescore` 參數。`oversample_factor` 是介於 `1.0` 與 `100.0` 之間（含端點）的浮點數。較高的值會在第一階段擷取更多候選結果，可提升召回率，但代價是搜尋延遲較高：

```json
GET /test-index/_search
{
  "query": {
    "knn": {
      "my_vector1": {
        "vector": [1.5, 2.5, 3.5, 4.5],
        "k": 5,
        "rescore": {
          "oversample_factor": 5.0
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

如需重新評分的更多資訊，請參閱[將量化結果重新評分至全精度]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#rescoring-quantized-results-to-full-precision)。

## 後續步驟

- [Faiss 純量量化]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/faiss-scalar-quantization/)
- [Lucene 純量量化]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/lucene-scalar-quantization/)
- [記憶體最佳化向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/)
- [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)
