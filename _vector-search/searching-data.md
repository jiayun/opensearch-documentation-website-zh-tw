---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋資料"
nav_order: 35
---

# 搜尋向量資料

OpenSearch 支援多種搜尋向量資料的方法，並依向量的建立與編製索引方式而有所不同。本指南說明原始向量搜尋與自動產生嵌入搜尋的查詢語法與選項。

## 搜尋類型比較

下表比較各種向量搜尋方法的查詢語法與典型使用情境。

| 功能                          | 查詢類型  | 輸入格式 | 是否需要模型 | 使用情境     |
|----------------------------------|------------------|------------------|---------------------|----------------------------|
| **原始向量**     | [`knn`]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)            | 向量陣列     | 否                  | 原始向量搜尋          |
| **自動產生的嵌入** | [`neural`]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural/)       | 文字或圖片資料            | 是                 | [AI 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/)            |

## 搜尋原始向量

若要搜尋原始向量，請使用 `knn` 查詢類型，提供 `vector` 陣列作為輸入，並指定傳回的結果數量 `k`：

```json
GET /my-raw-vector-index/_search
{
  "query": {
    "knn": {
      "my_vector": {
        "vector": [0.1, 0.2, 0.3],
        "k": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

## 搜尋自動產生的嵌入

OpenSearch 支援 [AI 驅動的搜尋方法]({{site.url}}{{site.baseurl}}/vector-search/ai-search/)，包括語意搜尋、混合搜尋、多模態搜尋，以及搭配檢索增強生成 (RAG) 的對話式搜尋。這些方法會從查詢輸入自動產生嵌入。

若要執行 AI 驅動的搜尋，請使用 `neural` 查詢類型。指定 `query_text` 輸入、您在[資料匯入管線中設定]({{site.url}}{{site.baseurl}}/vector-search/creating-vector-index/#converting-data-to-embeddings-during-ingestion)的嵌入模型 ID，以及傳回的結果數量 `k`。若要排除搜尋結果中傳回的嵌入，請在 `_source.excludes` 參數中指定嵌入欄位：

```json
GET /my-ai-search-index/_search
{
  "_source": {
    "excludes": [
      "output_embedding"
    ]
  },
  "query": {
    "neural": {
      "output_embedding": {
        "query_text": "What is AI search?",
        "model_id": "mBGzipQB2gmRjlv_dOoB",
        "k": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

## 使用稀疏向量

OpenSearch 也支援稀疏向量。如需詳細資訊，請參閱[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-search/)。

## 後續步驟

- [開始使用語意與混合搜尋]({{site.url}}{{site.baseurl}}/vector-search/tutorials/neural-search-tutorial/)
- [篩選資料]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/)
- [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)
- [神經查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural/)
