---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋"
nav_order: 1
has_children: false
has_toc: false
nav_exclude: true
permalink: /search-plugins/
redirect_from:
  - /search-plugins/index/
search_methods:
- heading: 關鍵字 (BM25) 搜尋
  description: 使用 BM25 演算法的詞彙文字搜尋，根據詞頻與文件長度比對文件並排序。透過傳統文字搜尋找出精確與相近的比對結果。
  link: /search-plugins/keyword-search/
- heading: 向量搜尋
  description: 使用稠密與稀疏向量嵌入的相似度 (k 最近鄰) 搜尋，支援語意搜尋、檢索增強生成 (RAG) 與多模態影像搜尋。
  link: /vector-search/
- heading: AI 搜尋
  description: 超越向量嵌入的 AI 驅動搜尋功能。結合任何 AI 服務來豐富搜尋與匯入流程，支援完整的 AI 強化搜尋使用情境。
  link: /vector-search/ai-search/
---

# 搜尋

OpenSearch 支援關鍵字 (BM25) 搜尋、向量搜尋與 AI 驅動搜尋，並提供調校相關性、重新排序結果以及建立自訂搜尋管線的工具。

## 搜尋方法

OpenSearch 支援多種搜尋方法，以滿足不同的使用情境與需求。

{% include cards.html cards=page.search_methods %}

## 查詢語言

在 OpenSearch 中，您可以使用下列查詢語言來擷取資料。

語言 | 可使用的位置 | 說明
:--- | :--- | :---
[查詢領域專屬語言（Query DSL）]({{site.url}}{{site.baseurl}}/query-dsl/index/) | Search API、Dev Tools | OpenSearch 的主要查詢語言，支援建立複雜且完全可自訂的查詢。
[查詢字串查詢語言]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/) | Search API 的 `q` 參數、Discover 與 Dashboard 搜尋列 | 一種精簡的查詢語言，其語法以 Apache Lucene 為基礎。
[SQL]({{site.url}}{{site.baseurl}}/search-plugins/sql/sql/index/) | SQL API、Query Workbench | 一種傳統查詢語言，可銜接關聯式資料庫概念與 OpenSearch 以文件為導向的資料儲存之間的落差。
[Piped Processing Language (PPL)]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) | PPL API、Query Workbench | OpenSearch 中用於可觀測性的主要語言。PPL 使用管線 (pipe) 語法，將指令串連成查詢。

如需在 OpenSearch Dashboards 中查詢資料的相關資訊 (包括 Dashboards Query Language (DQL))，請參閱[使用 Discover 分析資料]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/)。

## 自訂搜尋結果

OpenSearch 提供適用於所有搜尋類型的基本結果處理功能。您可以自訂結果導覽 (分頁、排序)、結果格式化 (醒目提示、欄位選取)、查詢強化 (自動完成、您是不是要找) 以及結果篩選。如需更多資訊，請參閱[自訂搜尋結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/)。

## 最佳化搜尋品質

OpenSearch 提供完整的工具與功能，協助您測量、分析並改善搜尋結果的品質。這些整合功能會協同運作，根據使用者行為與機器學習來最佳化搜尋相關性。如需更多資訊，請參閱[最佳化搜尋品質]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/)。

## 搜尋管線

搜尋管線是支援 OpenSearch AI 與向量搜尋功能的基礎架構。它們提供模組化的處理器，可轉換查詢 (文字轉向量轉換、ML 推論、查詢改寫)、強化結果 (重新排序、RAG、欄位操作)，並協調複雜的 AI 工作流程。如需更多資訊，請參閱[搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/)。

## 改善搜尋效能

OpenSearch 提供多種功能來最佳化搜尋效能，從基礎的快取技術到專門的最佳化皆有涵蓋。如需更多資訊，請參閱[改善搜尋效能]({{site.url}}{{site.baseurl}}/search-plugins/improving-search-performance/)。

## 跨叢集搜尋

OpenSearch 支援跨多個叢集搜尋，讓您能為大型部署擴充搜尋基礎架構。如需更多資訊，請參閱[跨叢集搜尋]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/)。
