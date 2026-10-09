---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "神經稀疏搜尋"
parent: AI search
nav_order: 50
has_children: true
redirect_from:
  - /search-plugins/neural-sparse-search/
  - /search-plugins/sparse-search/
---

# 神經稀疏搜尋
Introduced 2.11
{: .label .label-purple }

[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/) 依賴以文字嵌入模型為基礎的稠密檢索。然而，稠密方法使用 k-NN 搜尋，會耗用大量記憶體與 CPU 資源。作為語意搜尋的替代方案，神經稀疏搜尋使用倒排索引實作，因此效率與 BM25 相當。神經稀疏搜尋由稀疏嵌入模型提供支援。當您執行神經稀疏搜尋時，它會建立稀疏向量（一組 `token: weight` 鍵值對，代表一個項目及其權重），並將資料匯入 rank features 索引。

若要進一步提升搜尋相關性，您可以使用[混合查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/hybrid/)將神經稀疏搜尋與稠密[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)結合。

您可以使用下列方式設定神經稀疏搜尋：

- 自動產生向量嵌入：設定資料匯入管線，在匯入時從文件文字產生並儲存稀疏向量嵌入。查詢時，輸入純文字，系統會自動將其轉換為向量嵌入以進行搜尋。如需完整的設定步驟，請參閱[自動產生稀疏向量嵌入]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-with-pipelines/)。
- 匯入原始稀疏向量，並直接使用稀疏向量進行搜尋。如需完整的設定步驟，請參閱[使用原始向量的神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-with-raw-vectors/)。

若要進一步了解如何將長文字分割為段落以進行神經稀疏搜尋，請參閱[文字分段]({{site.url}}{{site.baseurl}}/search-plugins/text-chunking/)。

## 加速神經稀疏搜尋

您可以建立含有 `neural_sparse_two_phase_processor` 的搜尋管線，大幅加速搜尋程序。

若要建立含有神經稀疏搜尋兩階段處理器的搜尋管線，請使用下列請求：

```json
PUT /_search/pipeline/two_phase_search_pipeline
{
  "request_processors": [
    {
      "neural_sparse_two_phase_processor": {
        "tag": "neural-sparse",
        "description": "Creates a two-phase processor for neural sparse search."
      }
    }
  ]
}
```
{% include copy-curl.html %}

接著選擇您要使用搜尋管線設定的索引，並將 `index.search.default_pipeline` 設為管線名稱，如下列範例所示：

```json
PUT /my-nlp-index/_settings 
{
  "index.search.default_pipeline" : "two_phase_search_pipeline"
}
```
{% include copy-curl.html %}

如需 `two_phase_search_pipeline` 的相關資訊，請參閱[神經稀疏查詢兩階段處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/neural-sparse-query-two-phase-processor/)。

## 文字分段

如需在產生嵌入之前將大型文件分割為較小段落的相關資訊，請參閱[文字分段]({{site.url}}{{site.baseurl}}/vector-search/ingesting-data/text-chunking/)。

## 神經稀疏 ANN 搜尋
**Introduced 3.3**
{: .label .label-purple }

您可以執行神經稀疏近似最近鄰 (ANN) 搜尋，以更高的查詢召回率 (>0.9) 達到更好的查詢效能。如需詳細資訊，請參閱[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)。

您可以為 `sparse_vector` 欄位選擇兩種引擎：Lucene 引擎（預設）與原生引擎。您可以在欄位對應中選擇引擎，兩者的查詢語法相同。如需詳細資訊，請參閱[引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#engines)。

## 延伸閱讀

- 在[使用稀疏語意編碼器改善文件檢索](https://opensearch.org/blog/improving-document-retrieval-with-sparse-semantic-encoders/)中，進一步了解稀疏編碼模型的運作方式，並探索 OpenSearch 神經稀疏搜尋基準測試。
- 在[深入探討 OpenSearch 2.12 中更快速的語意稀疏檢索](https://opensearch.org/blog/A-deep-dive-into-faster-semantic-sparse-retrieval-in-OS-2.12/)中，了解神經稀疏搜尋的基本原理及其效率。
- 探索我們的[教學]({{site.url}}{{site.baseurl}}/vector-search/tutorials/)，了解如何建置 AI 搜尋應用程式。 
