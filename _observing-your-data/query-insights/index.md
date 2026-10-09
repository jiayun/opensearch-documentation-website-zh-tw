---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "查詢洞察"
nav_order: 80
has_children: true
has_toc: false
redirect_from:
  - /query-insights/
  - /observing-your-data/query-insights/
---

# 查詢洞察
**於 2.12 版推出**
{: .label .label-purple }

若要監視及分析 OpenSearch 叢集中的搜尋查詢，您可以取得查詢洞察。查詢洞察功能的效能影響極小，旨在提供搜尋查詢執行的全方位洞察，讓您更了解查詢執行各階段的搜尋查詢特性、模式及系統行為。查詢洞察有助於強化查詢效能問題的偵測、診斷及預防，進而改善查詢處理效能、使用者體驗及整體系統復原能力。

查詢洞察功能的典型使用案例包括下列各項：

- 找出影響叢集最慢或最耗用資源的查詢。
- 偵錯延遲尖峰並了解查詢效能模式。
- 分析常見的慢速查詢結構，以找出最佳化機會。
- 監視進行中的即時查詢，以診斷立即的搜尋效能問題。

查詢洞察功能由 Query Insights 外掛程式提供，該外掛程式預設隨 OpenSearch 發行版一併提供。概括而言，這些功能包含下列元件：

* _收集器_：在搜尋查詢執行的各個階段收集效能相關的資料點。
* _處理器_：對收集器所收集的資料執行輕量彙總與處理。
* _匯出器_：將資料匯出至不同的接收端。


## 查詢洞察功能與設定

Query Insights 提供多種方式來監視及分析您的搜尋查詢：

-   **[前 N 筆查詢]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/top-n-queries/)**：根據各種效能指標，找出特定時間範圍內最耗用資源或最慢的查詢。
-   **[將前 N 筆查詢分組]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/grouping-top-n-queries/)**：根據查詢來源結構將類似的慢速查詢分組，以探索模式並加以分析。
-   **[即時查詢監視]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/live-queries/)**：即時掌握叢集中目前正在執行的搜尋查詢，以找出並偵錯目前長時間執行或耗用大量資源的查詢。
-   **[查詢洞察儀表板]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/query-insights-dashboard/)**：在 OpenSearch Dashboards 中以互動方式視覺化及設定前幾名的查詢洞察。
-   **[查詢指標]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/query-metrics/)**：了解每種查詢類型的特定效能指標。

## Query Insights 外掛程式健康狀態

如需監視 Query Insights 外掛程式健康狀態的相關資訊，請參閱 [Query Insights 外掛程式健康狀態]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/health/)。