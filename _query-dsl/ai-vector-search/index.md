---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "AI 與向量搜尋查詢"
has_children: true
nav_order: 55
has_toc: false
redirect_from:
  - /query-dsl/ai-vector-search/
---

# AI 與向量搜尋查詢

AI 與向量搜尋查詢會使用機器學習模型來轉換或增強搜尋作業。這些查詢會將文字或其他輸入轉換為向量表示以進行相似度搜尋，或在執行階段使用 AI 服務產生查詢參數。

| 查詢類型 | 說明 |
| :--- | :--- |
| [Agentic]({{site.url}}{{site.baseurl}}/query-dsl/specialized/agentic/) | 使用 AI 代理程式動態規劃並執行搜尋策略。 |
| [k-NN]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/) | 使用向量嵌入執行近似或精確的最近鄰搜尋。 |
| [Neural]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural/) | 在查詢時將文字轉換為稠密向量嵌入，以進行語意搜尋。 |
| [Neural sparse]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural-sparse/) | 在查詢時將文字轉換為稀疏向量嵌入，以進行語意搜尋。 |
| [Template]({{site.url}}{{site.baseurl}}/query-dsl/specialized/template/) | 包含預留位置變數，由 ML 推論處理器在查詢時解析。 |
