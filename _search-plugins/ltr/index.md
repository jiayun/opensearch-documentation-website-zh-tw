---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Learning to Rank
parent: Optimizing search quality
nav_order: 40
has_children: true
has_toc: false
redirect_from:
  - /search-plugins/ltr/
---

<!-- vale off -->
# Learning to Rank
<!-- vale on -->

OpenSearch 的 Learning to Rank 外掛程式可讓您使用機器學習 (ML) 與行為資料來微調文件的相關性。它使用來自 [XGBoost](https://xgboost.ai/) 與 [RankLib](https://lemurproject.org/ranklib.php) 程式庫的模型。這些模型會重新評分搜尋結果，並考量與查詢相關的特徵，例如點擊資料或欄位匹配，進一步提升相關性。

在 OpenSearch 文件中，_learning to rank_ 一詞在一般語境下縮寫為 LTR。外掛程式開發者文件請參閱 [`opensearch-learning-to-rank-base`](https://github.com/opensearch-project/opensearch-learning-to-rank-base)。
{: .note} 

## 入門

下列資源可協助您快速上手：

- 如果您是 LTR 新手，請從 [機器學習排序的核心概念]({{site.url}}{{site.baseurl}}/search-plugins/ltr/core-concepts/) 文件開始。
- 如需快速簡介，請參閱 [hello-ltr](https://github.com/o19s/hello-ltr) 中的示範。
- 如果您已熟悉 LTR，請從 [外掛程式的適用範圍]({{site.url}}{{site.baseurl}}/search-plugins/ltr/fits-in/) 文件開始。

## 核心概念與設定

在實作 LTR 之前，請先熟悉基礎概念與架構：

- [機器學習排序的核心概念]({{site.url}}{{site.baseurl}}/search-plugins/ltr/core-concepts/)：瞭解 Learning to Rank 背後的基本概念。
- [外掛程式的適用範圍]({{site.url}}{{site.baseurl}}/search-plugins/ltr/fits-in/)：瞭解 LTR 如何與您的 OpenSearch 基礎架構整合。

## 特徵工程與模型開發

使用下列工作流程建立並訓練您的排序模型：

- [特徵工程]({{site.url}}{{site.baseurl}}/search-plugins/ltr/feature-engineering/)：為您的排序模型設計有效的特徵。
- [使用特徵]({{site.url}}{{site.baseurl}}/search-plugins/ltr/working-with-features/)：建立並管理特徵集。
- [記錄特徵分數]({{site.url}}{{site.baseurl}}/search-plugins/ltr/logging-features/)：收集特徵資料以供模型訓練。
- [上傳已訓練模型]({{site.url}}{{site.baseurl}}/search-plugins/ltr/training-models/)：建立並訓練您的排序模型。

## 部署與進階主題

模型訓練完成後，即可部署至正式環境並探索進階功能：

- [使用 LTR 最佳化搜尋]({{site.url}}{{site.baseurl}}/search-plugins/ltr/searching-with-your-model/)：在正式環境搜尋中部署模型。
- [進階功能]({{site.url}}{{site.baseurl}}/search-plugins/ltr/advanced-functionality/)：探索進階的 LTR 功能與技術。
- [常見問題]({{site.url}}{{site.baseurl}}/search-plugins/ltr/faq/)：常見問題與疑難排解。
