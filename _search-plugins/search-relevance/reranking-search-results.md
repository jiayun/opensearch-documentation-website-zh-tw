---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新排序搜尋結果"
parent: Optimizing search quality
has_children: true
nav_order: 50
---

# 重新排序搜尋結果
**於 2.12 版推出**
{: .label .label-purple }

您可以使用 [`rerank` 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/) 重新排序搜尋結果，以改善搜尋相關性。若要實作重新排序，您需要設定一個在搜尋時執行的 [搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/)。搜尋管線會攔截搜尋結果，並對其套用 `rerank` 處理器。`rerank` 處理器會評估搜尋結果，並根據新的分數加以排序。

您可以透過下列方式重新排序結果：

- [使用 cross-encoder 模型]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-cross-encoder/)
- [依據文件欄位]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-by-field/)
- [依據使用 cross-encoder 的欄位]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-by-field-cross-encoder/)
- [依據使用 late interaction 模型的欄位]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-by-field-late-interaction/)

## 代理程式搜尋中的重新排序

如果您使用代理程式搜尋，請參閱[重新排序代理程式搜尋結果]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/rerank-agentic-search-results/)，以瞭解在代理程式搜尋管線中重新排序搜尋結果的相關資訊。

## 同時使用 rerank 與 normalization 處理器

當您將 rerank 處理器與 [normalization 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/)及混合查詢搭配使用時，rerank 處理器會改變最終的文件分數。這是因為在搜尋管線中，rerank 處理器是在 normalization 處理器之後執行。
{: .note}

處理順序如下：

- Normalization 處理器：此處理器會根據設定的 normalization 方法將文件分數標準化。如需更多資訊，請參閱 [normalization 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/)。
- Rerank 處理器：在 normalization 之後，rerank 處理器會進一步調整文件分數。此調整可能會大幅影響搜尋結果的最終排序。

此處理順序具有下列影響：

- 分數修改：rerank 處理器會修改先前由 normalization 處理器調整過的分數，可能導致與最初預期不同的排序結果。
- 混合查詢：在混合查詢的情境中，多種查詢類型與評分機制會結合在一起，此行為尤其值得注意。初始查詢產生的合併分數會先標準化，然後再重新排序，形成兩階段的分數修改。

