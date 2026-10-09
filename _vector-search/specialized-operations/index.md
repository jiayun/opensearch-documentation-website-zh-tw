---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "特殊向量搜尋"
nav_order: 50
has_children: true
has_toc: false
redirect_from:
  - /vector-search/specialized-operations/
cards:
- heading: 巢狀欄位向量搜尋
  description: 使用向量搜尋來搜尋巢狀欄位
  link: /vector-search/specialized-operations/nested-search-knn/
- heading: 徑向搜尋
  description: 搜尋向量空間中與查詢點距離在指定最大距離內，或分數高於最低分數閾值的所有點
  link: /vector-search/specialized-operations/radial-search-knn/
- heading: 使用 MMR 重新排序的向量搜尋
  description: 使用最大邊際相關性 (MMR) 自動依據相關性與多樣性重新排序，以改善向量搜尋結果
  link: /vector-search/specialized-operations/vector-search-mmr/
---

# 特殊向量搜尋

OpenSearch 支援下列特殊向量搜尋應用。

{% include cards.html cards=page.cards %}