---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "比較搜尋結果"
nav_order: 11
parent: Search Relevance Workbench
grand_parent: Optimizing search quality
---

# 比較搜尋結果

在 OpenSearch Dashboards 中比較搜尋結果（也稱為 _成對實驗_）可讓您比較多種搜尋組態的結果。使用此工具有助於評估對查詢套用不同搜尋組態時，結果會如何變化。

例如，您可以查看套用下列其中一項查詢變更時，結果會如何變化：

- 以不同方式加權欄位
- 不同的詞幹提取或詞形還原策略
- 產生詞元組合

## 比較單一查詢的搜尋結果

比較單一查詢搜尋結果的 UI 可讓您為個別查詢定義兩種不同的搜尋組態，以便並排檢視與比較結果。具體來說，您可以了解結果清單中有多少共用與唯一的文件，以及它們的位置如何變化，如下圖所示。

![比較搜尋結果]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/comparing_search_results.png)

如需有關使用單一查詢搜尋結果比較工具的更多資訊，請參閱 [比較單一查詢]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/compare-search-results/)。

## 比較查詢集的搜尋結果

一般而言，檢視兩種組態的搜尋結果變化是測試流程的第一步。接著，您可以在 Search Relevance Workbench 中從單一查詢擴展到多個查詢。您可以將查詢分組為查詢集、建立 [搜尋組態]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/search-configurations/)，並透過檢視所有查詢的彙總指標，以更大規模比較搜尋結果，如下圖所示。

![比較搜尋結果]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/comparing-search-results-query-sets.png)

如需有關使用查詢集搜尋結果比較工具的更多資訊，請參閱 [比較單一查詢]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/compare-query-sets/)。
