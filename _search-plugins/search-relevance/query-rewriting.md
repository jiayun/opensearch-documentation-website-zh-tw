---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "查詢重寫"
parent: Optimizing search quality
has_children: true
nav_order: 30
has_toc: false
---

# 查詢重寫

查詢重寫是在執行使用者查詢之前，轉換或修改該查詢的過程。查詢重寫的目標是透過處理拼字錯誤、同義詞、語意模糊的詞彙或效率不彰的查詢結構等問題，來改善搜尋準確度、相關性或效能。查詢重寫常用於搜尋系統中，以提升搜尋結果的品質。

您可以在 OpenSearch 中使用下列功能來執行查詢重寫：

- [範本查詢]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/template-query/)：建立含有動態預留位置的查詢，並在查詢執行期間解析，適用於機器學習推論與執行階段參數產生。

- [Querqy]({{site.url}}{{site.baseurl}}/search-plugins/querqy/)：社群外掛程式，可透過規則進行進階查詢重寫，以提升、埋沒、篩選及重新導向搜尋結果。
