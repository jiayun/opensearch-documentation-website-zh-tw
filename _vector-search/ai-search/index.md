---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "AI 搜尋"
nav_order: 45
has_children: true
has_toc: false
redirect_from: 
  - /neural-search-plugin/index/
  - /search-plugins/neural-search/
  - /vector-search/ai-search/
model_cards:
- heading: 使用 OpenSearch 提供的預訓練模型
  link: /ml-commons-plugin/pretrained-models/
- heading: 將您自己的模型上傳至 OpenSearch
  link: /ml-commons-plugin/custom-local-models/
- heading: 連線至外部平台上託管的模型
  link: /ml-commons-plugin/remote-models/index/
tutorial_cards:
- heading: 語意與混合搜尋入門
  description: 了解如何實作語意與混合搜尋
  link: /vector-search/tutorials/neural-search-tutorial/
search_method_cards:
- heading: 語意搜尋
  description: 使用以文字嵌入模型為基礎的稠密檢索來搜尋文字資料。
  link: /vector-search/ai-search/semantic-search/
- heading: 混合搜尋
  description: 結合關鍵字與語意搜尋，以提升搜尋相關性。
  link: /vector-search/ai-search/hybrid-search/
- heading: 多模態搜尋
  description: 使用多模態嵌入模型來搜尋文字與影像資料。
  link: /vector-search/ai-search/multimodal-search/
- heading: 神經稀疏搜尋
  description: 使用以稀疏嵌入模型為基礎的稀疏檢索來搜尋文字資料。
  link: /vector-search/ai-search/neural-sparse-search/
- heading: 神經稀疏 ANN 搜尋
  description: 對稀疏向量使用近似最近鄰技術，以在大規模環境中提升效能。
  link: /vector-search/ai-search/neural-sparse-ann/
- heading: 使用 RAG 的對話式搜尋
  description: 使用檢索增強生成 (RAG) 與對話記憶，以提供能感知情境的回應。
  link: /vector-search/ai-search/conversational-search/
---

# AI 搜尋

AI 搜尋會自動產生嵌入，藉此簡化您的工作流程。OpenSearch 會在編製索引與查詢期間將文字轉換為向量。它會為文件建立並編製向量嵌入的索引，接著將查詢文字處理為嵌入，以找出並傳回最相關的結果。

## 先決條件

使用 AI 搜尋之前，您必須設定用於產生嵌入的 ML 模型。選擇模型時，您有下列選項：

- 使用 OpenSearch 提供的預訓練模型。如需詳細資訊，請參閱 [OpenSearch 提供的預訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/)。

- 將您自己的模型上傳至 OpenSearch。如需詳細資訊，請參閱 [自訂本機模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/custom-local-models/)。

- 連線至外部平台上託管的基礎模型。如需詳細資訊，請參閱 [連線至外部託管的模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。

---

## 教學

{% include cards.html cards=page.tutorial_cards %}

---

## AI 搜尋方法

設定好 ML 模型後，請選擇下列其中一種搜尋方法。

{% include cards.html cards=page.search_method_cards %}