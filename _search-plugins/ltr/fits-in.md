---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "外掛程式的範圍"
nav_order: 20
parent: Learning to Rank
grand_parent: Optimizing search quality
has_children: false
---

# 外掛程式的範圍

OpenSearch 的 Learning to Rank 外掛程式可協助您開發及使用以機器學習（ML）為基礎的排序模型，供應用程式的搜尋作業使用。以下各節說明此外掛程式如何融入整體 LTR 流程。

## 外掛程式提供的功能

此外掛程式提供開發及使用 LTR 模型所需的基本元件，讓您具備下列能力： 

1. **開發依查詢而定的特徵：** 建立自訂特徵，擷取搜尋查詢與文件之間的關係。這些特徵可以儲存在 OpenSearch 中。
2. **記錄特徵值：** 記錄搜尋結果所傳回文件的特徵值。記錄文件的特徵集後，您可以將這些資料與您建立的評判清單結合。這樣就能取得完整的訓練集，用來測試及訓練排序模型。接著，您可以使用 RankLib 或 XGBoost 等工具，開發出令人滿意的模型。
3. **部署及使用模型：** 將訓練完成的排序模型上傳至外掛程式，並使用這些模型重新排序搜尋結果。此外掛程式提供自訂的 OpenSearch Query DSL 基本元素，讓您能在搜尋過程中執行模型。

## 外掛程式未提供的功能

此外掛程式不支援建立評判清單。這項工作必須由您自行處理，因為它與特定領域有關。請參閱 [Wikimedia Foundation 部落格](https://blog.wikimedia.org/2017/09/19/search-relevance-survey/)，了解如何建立用於搜尋文章的評判清單範例方法。某些領域（例如電子商務）可能更著重於與轉換相關的訊號，其他領域則可能需要人工相關性評估人員（內部專家或群眾外包人員）參與。

此外掛程式不處理模型訓練或測試。這是離線流程，應使用適當的工具處理，例如 [XGBoost](https://xgboost.ai/) 和 [RankLib](https://lemurproject.org/ranklib.php)。此外掛程式可與這些外部模型建置工作流程整合。訓練及測試排序模型可能需要大量 CPU 資源，也需要資料科學專業知識與離線測試。大多數組織傾向讓資料科學家監督模型開發流程，而非直接在正式環境中執行此流程。

## 後續步驟

了解如何[使用特徵]({{site.url}}{{site.baseurl}}/search-plugins/ltr/working-with-features/)。
