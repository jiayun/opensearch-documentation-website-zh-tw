---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "稀疏向量"
nav_order: 92
has_children: false
parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/sparse-vector/
---

# 稀疏向量
**於 3.3 版推出**
{: .label .label-purple }

`sparse_vector` 欄位支援[神經稀疏近似最近鄰 (ANN) 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)，可在維持相關性的同時提升搜尋效率。`sparse_vector` 會以映射形式儲存，其中每個鍵代表一個詞元，每個值則是一個正的 [`float`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/numeric/) 值，表示該詞元的權重。
    
## 參數

`sparse_vector` 欄位需要一個 `method` 物件，用來指定演算法、實作該演算法的引擎，以及演算法參數。

### 方法參數

`method` 物件支援下列參數。

| 參數       | 類型   | 必要 | 說明                                                                                                                                                                                                      | 預設值    | 有效值           | 
|-----------------|--------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|------------------------|
| `name`          | 字串 | 是      | 神經稀疏 ANN 搜尋演算法。                                                                                                                                                                          | -          | `seismic`              | 
| `engine`        | 字串 | 否       | 用於建立及搜尋索引的引擎。如需詳細資訊，請參閱[引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#engines)。  | `lucene`   | `lucene`, `native`     | 
| `parameters`    | 物件 | 否       | 演算法參數。請參閱[演算法參數](#algorithm-parameters)。                                                                                                                                     | -          | -                      | 

欄位建立後即無法更新 `method` 物件。若要變更引擎或任何演算法參數，請以所需的對應建立新索引，並將您的資料重新編製索引。
{: .important}

### 演算法參數

`method.parameters` 物件支援下列參數。

| 參數               | 類型    | 必要 | 說明                                   | 預設值               | 範圍       | 
|-------------------------|---------|----------|-----------------------------------------------|-----------------------|-------------|
| `n_postings`            | 整數 | 否 | 每個張貼清單中要保留的文件數量上限。            | `0.0005 * doc_count`¹ | (0, ∞) | 
| `cluster_ratio`         | 浮點數   | 否 | 每個張貼清單中用來決定叢集數量的文件比例。             | `0.1`                 | (0, 1)      | 
| `summary_prune_ratio`   | 浮點數   | 否 | 修剪叢集摘要向量時要保留的總詞元權重比例。例如，若 `summary_prune_ratio` 設為 `0.5`，則會保留貢獻總權重前 50% 的詞元。因此，對於叢集摘要 `{"100": 1, "200": 2, "300": 3, "400": 6}`，修剪後的摘要為 `{"400": 6}`。 | `0.4`                 | (0, 1]      | 
| `approximate_threshold` | 整數 | 否 | 分段中要啟用神經稀疏 ANN 搜尋所需的最少文件數量。     | `1000000`           | [0, ∞) | 
| `quantization_ceiling_search`  | 浮點數   | 否 | 搜尋期間用於量化之詞元權重上限。 | `16`                  | (0, ∞) | 
| `quantization_ceiling_ingest` | 浮點數 | 否 | 匯入期間用於量化之詞元權重上限。 | `3`                   | (0, ∞)     | 
| `clustering_batch_size` | 整數 | 否 | 將每個倒排清單分成多少批次以進行分群。僅原生引擎支援。當此參數大於 `1` 時，分群作業會分別對各批次執行，而非對整個語料庫執行；這可減少建立索引時的記憶體用量，但會延長建立時間。 | `1`                   | [1, 10000]     | 
| `forward_index`         | 字串  | 否 | 正向索引的儲存方式。僅支援原生引擎。`shared` 會為該欄位儲存一個連續的正向索引。`per_block` 會將每個區塊的向量內嵌於該區塊中，這可降低查詢延遲，但會使用更多磁碟空間。 | `shared`              | `shared`, `per_block` | 

若您將 `engine` 設為 `lucene`，並指定 `shared` 以外的 `forward_index` 值，則該請求會被拒絕。
{: .warning}


¹`doc_count` 代表分段內的文件數量。推導出的值絕不會低於 `160`。

如需參數設定，請參閱[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)。  
{: .note }

為提升搜尋效率並降低記憶體耗用量，`sparse_vector` 欄位會自動對詞元權重執行量化。您可以依據不同的詞元權重分布調整 `quantization_ceiling_search` 與 `quantization_ceiling_ingest` 參數。對於僅文件查詢，我們建議將 `quantization_ceiling_search` 設為預設值（`16`）。對於雙編碼器查詢，我們建議將 `quantization_ceiling_search` 設為 `3`。如需僅文件與雙編碼器查詢模式的詳細資訊，請參閱[自動產生稀疏向量嵌入]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-with-pipelines/)。
{: .note}

## 範例

下列範例示範如何使用 `sparse_vector` 欄位類型。

### 步驟 1：建立索引

將 `index.sparse` 設為 `true` 以建立稀疏索引，並在索引對應中定義 `sparse_vector` 欄位：

```json
PUT sparse-vector-index
{
  "settings": {
    "index": {
      "sparse": true
    }
  },
  "mappings": {
    "properties": {
      "sparse_embedding": {
        "type": "sparse_vector",
        "method": {
          "name": "seismic",
          "parameters": {
            "n_postings": 300,
            "cluster_ratio": 0.1,
            "summary_prune_ratio": 0.4,
            "approximate_threshold": 1000000
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

此範例使用預設的 Lucene 引擎。若要改將欄位對應至原生引擎，請在叢集層級啟用該引擎，然後將 `engine` 設為 `native`。如需詳細資訊，請參閱[引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#engines)。

### 步驟 2：將資料匯入索引

將三份包含 `sparse_vector` 欄位的文件匯入您的索引：

```json
PUT sparse-vector-index/_doc/1
{
  "sparse_embedding" : {
    "1000": 0.1
  }
}
```
{% include copy-curl.html %}

```json
PUT sparse-vector-index/_doc/2
{
  "sparse_embedding" : {
    "2000": 0.2
  }
}
```
{% include copy-curl.html %}

```json
PUT sparse-vector-index/_doc/3
{
  "sparse_embedding" : {
    "3000": 0.3
  }
}
```
{% include copy-curl.html %}

### 步驟 3：搜尋索引

您可以使用原始向量或自然語言，透過 [`neural_sparse` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural-sparse/) 來查詢稀疏索引。

#### 使用原始向量查詢

若要使用原始向量查詢，請提供 `query_tokens` 參數：

```json
GET sparse-vector-index/_search
{
  "query": {
    "neural_sparse": {
      "sparse_embedding": {
        "query_tokens": {
          "1000": 5.5
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

#### 使用自然語言查詢

若要使用自然語言查詢，請提供 `query_text` 與 `model_id` 參數：

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

## 相關文件

- [神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)
- [神經稀疏查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural-sparse/)
- [神經稀疏 ANN 搜尋效能調校]({{site.url}}{{site.baseurl}}/vector-search/performance-tuning-sparse/)
