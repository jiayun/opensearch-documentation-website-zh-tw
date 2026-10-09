---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "向量搜尋 API"
nav_order: 80
has_children: true
has_toc: false
redirect_from:
  - /vector-search/api/knn/
  - /vector-search/api/
  - /search-plugins/knn/api/
---

# 向量搜尋 API

在 OpenSearch 中，向量搜尋功能由 k-NN 外掛程式與 Neural Search 外掛程式提供。k-NN 外掛程式提供基本的 k-NN 功能，而 Neural Search 外掛程式則在編製索引與搜尋時自動產生嵌入。

如需 k-NN 外掛程式的 API，請參閱 [k-NN API]({{site.url}}{{site.baseurl}}/vector-search/api/knn/)。

除了外掛程式專屬的 API 之外，下列 API 也支援向量搜尋功能：

- [k-NN 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/)
- [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)
- [神經查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural/)
- [神經稀疏查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural-sparse/)
- [資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)
- 資料匯入處理器：
    - [機器學習推論]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/ml-inference/)
    - [稀疏編碼]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/sparse-encoding/)
    - [文字分塊]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-chunking/)
    - [文字嵌入]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-embedding/)
    - [文字/影像嵌入]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-image-embedding/)
- [搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/)
- 搜尋處理器：
    - [機器學習推論（請求）]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/ml-inference-search-request/)
    - [機器學習推論（回應）]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/ml-inference-search-response/)
    - [神經查詢增強器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/neural-query-enricher/)
    - [兩階段神經稀疏查詢]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/neural-sparse-query-two-phase-processor/)
    - [正規化]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/)
    - [重新排序]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/)
    - [檢索增強生成]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rag-processor/)
    - [分數排序器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/score-ranker-processor/)