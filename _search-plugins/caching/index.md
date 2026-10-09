---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "快取"
parent: Improving search performance
has_children: true
nav_order: 10
redirect_from:
  - /search-plugins/caching/
---

# 快取

OpenSearch 依賴不同的堆內快取類型來加速資料擷取，大幅改善搜尋延遲。然而，快取大小受限於節點上可用的記憶體量。在處理可能被快取的較大資料集時，快取大小限制會導致許多資料被從快取中移除或無法被快取，造成查詢不完整。這會影響效能，因為 OpenSearch 需要重新處理查詢，導致高度資源消耗。

了解您的資料如何使用快取，有助於改善叢集的效能，並避免使用過多記憶體，降低查詢資料的成本。

## 支援的堆內快取類型

OpenSearch 支援下列堆內快取類型：

- [**索引請求快取**]({{site.url}}{{site.baseurl}}/search-plugins/caching/request-cache/)：在每個分片上快取本機結果。這讓經常使用且可能耗用大量資源的搜尋請求幾乎能立即傳回結果。
- **查詢快取**：在分片層級快取來自相似查詢的共同資料。查詢快取比請求快取更細緻，可以快取資料以在不同查詢中重複使用。
- [**欄位資料快取**]({{site.url}}{{site.baseurl}}/search-plugins/caching/field-data-cache/)：快取欄位資料與全域序數，兩者都用於支援特定欄位類型的彙總。

## 其他快取儲存區

**2.14 版新增**
{: .label .label-purple }

除了現有的 OpenSearch 自訂堆內快取儲存區之外，快取外掛程式還提供下列快取儲存區：

- **磁碟快取**：將查詢的預先計算結果儲存在磁碟上。只要磁碟延遲在可接受的範圍內，即可使用磁碟快取來快取大得多的資料集。
- **分層快取**：一種多層級快取，其中每一層都有自己的特性與效能等級。例如，分層快取可以同時包含堆內層與磁碟層。透過結合不同的層，您可以在快取效能與大小之間取得平衡。若要了解更多，請參閱 [分層快取]({{site.url}}{{site.baseurl}}/search-plugins/caching/tiered-cache/)。

在 OpenSearch 2.14 中，請求快取已與快取外掛程式整合。您可以使用分層快取或磁碟快取作為請求層級快取。
{: .note}
