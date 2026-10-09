---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "最佳化搜尋品質"
nav_order: 75
has_children: true
has_toc: false
redirect_from:
  - /search-plugins/search-relevance/
---

# 最佳化搜尋品質

_搜尋品質_是指搜尋結果符合使用者意圖與期望的程度。OpenSearch 提供多項功能與工具，協助您測量、分析並改善搜尋結果的品質。

OpenSearch 提供下列功能，協助您最佳化搜尋品質：

- **[User Behavior Insights (UBI)]({{site.url}}{{site.baseurl}}/search-plugins/ubi/)**：擷取並分析使用者行為資料，以了解使用者如何與搜尋結果互動，並找出可改善之處。

- **[Search Relevance Workbench]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/using-search-relevance-workbench/)**：一套完整的工具組，可透過查詢比較、結果評估與 A/B 測試來實驗並改善搜尋相關性。

- **[相關性代理程式]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/relevance-agent/)**：專為持續改善搜尋相關性而設計的專用代理程式。

- **[查詢改寫]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/query-rewriting/)**：轉換使用者查詢，以提升搜尋準確度，並處理同義詞、拼字錯誤及其他查詢變化。

- **[Learning to Rank (LTR)]({{site.url}}{{site.baseurl}}/search-plugins/ltr/)**：使用以行為資料訓練的機器學習模型，改善搜尋結果的排名。

- **[重新排序搜尋結果]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/reranking-search-results/)**：套用機器學習模型重新排序搜尋結果，以提升相關性。

## 搜尋品質工作流程

典型的搜尋品質改善工作流程包含：

1. **資料收集**：使用 UBI 擷取使用者行為與互動資料。
2. **分析**：分析使用者行為模式，找出搜尋品質問題。
3. **實驗**：使用 Search Relevance Workbench 測試不同方法。
4. **模型訓練**：使用行為資料訓練 LTR 模型，以改善排名。
5. **查詢強化**：套用查詢改寫規則，以提升查詢理解能力。
6. **重新排序**：套用以機器學習為基礎的重新排序，進一步最佳化結果。
7. **評估**：持續監視並評估搜尋效能。

## 相關文件

- [重新排序搜尋結果教學]({{site.url}}{{site.baseurl}}/tutorials/reranking/)：了解如何使用各種機器學習模型與平台實作搜尋結果重新排序。
