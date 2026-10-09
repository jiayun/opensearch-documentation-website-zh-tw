---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作負載類型"
nav_order: 20
has_children: true
has_toc: false
---

# 工作負載類型

[`opensearch-benchmark-workloads`](https://github.com/opensearch-project/opensearch-benchmark-workloads) 儲存庫包含您可以在叢集上執行的預先封裝工作負載。本頁說明每個工作負載的資料、叢集需求以及查詢類型。若要判斷哪一個適合您的叢集，請參閱[選擇工作負載]({{site.url}}{{site.baseurl}}/benchmark/choosing-a-workload/)。

## 一般搜尋使用案例：`nyc_taxis`

若要對專為一般搜尋使用案例建置的叢集進行基準測試，請從 [nyc_taxis](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/nyc_taxis) 工作負載開始。它包含下列內容：

- **資料類型**：2015 年紐約市黃色計程車的乘車資料。
- **叢集需求**：適合小型至中型叢集。

此工作負載會測試下列查詢與搜尋功能：

- 範圍查詢
- 對各種欄位的詞項查詢
- 地理距離查詢
- 彙總

## 向量資料：`vectorsearch`

[`vectorsearch`](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/vectorsearch) 工作負載專為對向量搜尋功能進行基準測試而設計，包括效能與準確度。它包含下列內容：

- **資料類型**：高維度向量資料，通常代表文字或影像的嵌入。
- **叢集需求**：需要已啟用[向量搜尋功能]({{site.url}}{{site.baseurl}}/vector-search/)的叢集。

此工作負載會測試下列查詢與搜尋功能：

- k-NN 向量搜尋
- 結合向量相似度與中繼資料篩選的混合搜尋
- 高維度向量資料的編製索引效能

如需支援的參數、測試程序及範例結果，請參閱[向量搜尋工作負載]({{site.url}}{{site.baseurl}}/benchmark/workloads/vectorsearch/)。

## 全方位搜尋解決方案：`big5`

[big5](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/big5) 工作負載是一套全方位的基準測試套件，用於測試搜尋引擎效能的各個層面，包括跨多個使用案例的整體搜尋引擎效能。它包含下列內容：

- **資料類型**：混合不同資料類型，包括文字、數值及結構化資料。
- **叢集需求**：適合中型至大型叢集，因為其設計目的是對各種元件進行壓力測試。

此工作負載會測試下列查詢與搜尋功能：

- 全文搜尋效能
- 彙總效能
- 複雜的布林值查詢
- 排序與分頁
- 各種資料類型的編製索引效能

## Percolator 查詢：`percolator`

[percolator](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/percolator) 工作負載專為測試 `percolator` 查詢類型的效能而設計。它包含下列內容：

- **資料類型**：一組已儲存的查詢，以及要與這些查詢比對的文件。
- **叢集需求**：適合大量使用 [percolator]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/percolator/) 功能的叢集。

此工作負載會測試下列查詢與搜尋功能：

- 儲存查詢的編製索引效能
- percolator 查詢的比對效能
- 隨著已儲存查詢數量增加的可擴充性

## 記錄資料：`http_logs`

若要對使用記錄資料進行編製索引與搜尋的叢集進行基準測試，請使用 [http_logs](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/http_logs) 工作負載。它包含下列內容：

- **資料類型**：來自 1998 年世界盃網站的 HTTP 存取記錄。
- **叢集需求**：適合針對時間序列資料與記錄分析最佳化的叢集。

此工作負載會測試下列查詢與搜尋功能：

- 時間範圍查詢
- 對 `status-code` 或 `user-agent` 等欄位的詞項查詢
- 針對請求計數與平均回應大小等指標的彙總
- 對 `ip-address` 等欄位的基數彙總。

## 後續步驟

- 若要將這些工作負載與您叢集的使用案例進行比較，請參閱[選擇工作負載]({{site.url}}{{site.baseurl}}/benchmark/choosing-a-workload/)。
- 若要為沒有預先封裝工作負載可對應的資料建置工作負載，請參閱[建立自訂工作負載]({{site.url}}{{site.baseurl}}/benchmark/creating-custom-workloads/)。
