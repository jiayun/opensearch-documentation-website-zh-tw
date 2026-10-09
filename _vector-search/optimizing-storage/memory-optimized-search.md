---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "記憶體最佳化搜尋"
parent: Optimizing vector storage
nav_order: 30
---

# 記憶體最佳化搜尋
於 3.1 版導入
{: .label .label-purple }

記憶體最佳化搜尋可讓 Faiss 引擎在不必將整個向量索引載入堆外記憶體的情況下高效執行。若沒有這項最佳化，Faiss 通常會將完整索引載入記憶體，當索引大小超過可用的實體記憶體時，這種做法可能難以維持。透過記憶體最佳化搜尋，引擎會將索引檔案進行記憶體對映，並依靠作業系統的檔案快取來處理搜尋請求。這種方式可避免不必要的 I/O，並讓重複讀取直接由系統快取提供服務。

記憶體最佳化搜尋僅影響搜尋作業。索引編製行為維持不變。
{: .note }

## 限制

下列限制適用於 OpenSearch 中的記憶體最佳化搜尋：

- **對於在 OpenSearch 2.19 之前建立的索引，無論是否啟用記憶體最佳化模式，引擎都會將資料載入記憶體**。
- 記憶體最佳化搜尋僅支援搭配 [HNSW 方法]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#hnsw-parameters-1) 的 [Faiss 引擎]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#faiss-engine)。
- 記憶體最佳化搜尋不支援 [IVF]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#ivf-parameters) 或 [產品量化 (PQ)]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/faiss-product-quantization)。
- 啟用或停用記憶體最佳化搜尋需要重新啟動索引。

如果您使用 IVF 或 PQ，無論是否啟用記憶體最佳化模式，引擎都會將資料載入記憶體。
{: .important }

## 組態

若要啟用記憶體最佳化搜尋，請在建立索引時將 `index.knn.memory_optimized_search` 設定為 `true`：

```json
PUT /test_index
{
  "settings": {
    "index.knn": true,
    "index.knn.memory_optimized_search": true
  },
  "mappings": {
    "properties": {
      "vector_field": {
        "type": "knn_vector",
        "dimension": 128,
        "method": {
          "name": "hnsw",
          "engine": "faiss"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

若要在現有索引上啟用記憶體最佳化搜尋，您必須先關閉索引、更新設定，然後重新開啟索引：

```json
POST /test_index/_close
```
{% include copy-curl.html %}

```json
PUT /test_index/_settings
{
  "index.knn.memory_optimized_search": true
}
```
{% include copy-curl.html %}

```json
POST /test_index/_open
```
{% include copy-curl.html %}

## 與磁碟型搜尋整合

當您為欄位設定 `on_disk` 模式與 `1x` 壓縮時，即使索引層級未啟用記憶體最佳化，該欄位也會自動啟用記憶體最佳化搜尋。如需更多資訊，請參閱 [記憶體最佳化向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/)。


記憶體最佳化搜尋與 [磁碟型搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/disk-based-vector-search/) 不同，因為它不使用壓縮或量化。它只會改變搜尋期間向量資料的載入與存取方式。
{: .note }

## 效能最佳化

啟用記憶體最佳化搜尋時，[預熱 API]({{site.url}}{{site.baseurl}}/vector-search/performance-tuning-search/#warm-up-the-index) 只會載入搜尋作業所需的基本資訊，例如開啟底層 Faiss 索引檔案的串流。這種最小化的預熱可帶來：
- 更快的初始搜尋。
- 降低記憶體負擔。
- 更有效率的資源利用。

對於停用記憶體最佳化搜尋的欄位，預熱程序會將向量載入堆外記憶體。

## 後續步驟

- [磁碟型向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/disk-based-vector-search/)
- [向量量化]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/knn-vector-quantization/)
- [效能調校]({{site.url}}{{site.baseurl}}/vector-search/performance-tuning/)
