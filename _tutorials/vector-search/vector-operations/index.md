---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "向量操作"
parent: Vector search
has_children: true
has_toc: false
nav_order: 10
redirect_from:
  - /vector-search/tutorials/vector-operations/
  - /tutorials/vector-search/vector-operations/
vector_operations:
- heading: 從物件陣列產生嵌入
  list:
  - <b>平台</b>：OpenSearch
  - <b>模型</b>：Amazon Titan
  - <b>部署</b>：Amazon Bedrock
  link: /tutorials/vector-search/vector-operations/generate-embeddings/
- heading: 使用位元組量化向量進行語意搜尋
  list:
  - <b>平台：</b> OpenSearch
  - <b>模型：</b> Cohere Embed
  - <b>部署：</b> Provider API
  link: /tutorials/vector-search/vector-operations/semantic-search-byte-vectors/
- heading: 使用 Cohere 壓縮嵌入最佳化向量搜尋
  list:
  - <b>平台：</b> OpenSearch
  - <b>模型：</b> Cohere Embed Multilingual v3
  - <b>部署：</b> Amazon Bedrock
  link: /tutorials/vector-search/vector-operations/optimize-compression/
---

# 向量操作教學

了解如何在 OpenSearch 中執行向量操作，包括從結構化資料產生嵌入、將向量編製索引，以及執行向量搜尋。

{% include cards.html cards=page.vector_operations %}