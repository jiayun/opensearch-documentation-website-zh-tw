---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenSearch Benchmark
nav_order: 1
has_children: false
nav_exclude: true
has_toc: false
permalink: /benchmark/
redirect_from:
  - /benchmark/index/
  - /benchmark/tutorials/index/
tutorial_cards:
- heading: 開始使用 OpenSearch Benchmark
  description: 執行您的第一個 OpenSearch Benchmark 工作負載並取得效能指標
  link: /benchmark/quickstart/
- heading: 選擇工作負載
  description: 根據您叢集的使用案例選擇基準測試工作負載
  link: /benchmark/choosing-a-workload/
more_cards:
- heading: 使用者指南
  description: 了解如何對您的叢集進行效能基準測試
  link: /benchmark/user-guide/index/
- heading: 參考資料
  description: 了解 OpenSearch Benchmark 的命令與選項
  link: /benchmark/reference/index/
items:
- heading: 安裝及設定 OpenSearch Benchmark
  description: 安裝 OpenSearch Benchmark 並設定您的使用體驗
  link: /benchmark/user-guide/install-and-configure/installing-benchmark/
- heading: 執行工作負載
  description: 執行工作負載並取得效能指標
  link: /benchmark/running-workloads/
- heading: 分析效能指標
  description: 檢視您的基準測試報告並分析指標
  link: /benchmark/reference/summary-report/
description: "OpenSearch Benchmark 是 OpenSearch Project 提供的巨觀基準測試公用程式。您可以使用 OpenSearch Benchmark 從 OpenSearch 叢集收集效能指標。"
---

# ![Benchmark 圖示]({{site.url}}{{site.baseurl}}/images/icons/OpenSearch-PerformanceBenchmarks-Icon-1.png){: .heading-icon} OpenSearch Benchmark

本頁反映 OpenSearch Benchmark `2.X` 中更新後的術語。`1.15` 是 `1.X` 系列中最後一個受支援的版本。如需變更內容的詳細資訊，請參閱[版本歷程記錄頁面]({{site.url}}{{site.baseurl}}/benchmark/version-history/)。如需遷移協助，請參閱[遷移協助頁面]({{site.url}}{{site.baseurl}}/benchmark/migration-assistance/)。
{: .important }

OpenSearch Benchmark 是 [OpenSearch Project](https://github.com/opensearch-project) 提供的巨觀基準測試公用程式。您可以使用 OpenSearch Benchmark 從 OpenSearch 叢集收集效能指標，用於多種用途，包括：

- 追蹤 OpenSearch 叢集的整體效能。
- 協助決定何時將叢集升級至新版本。
- 判斷工作流程的變更（例如修改對應或查詢）可能對叢集造成的影響。

## 入門

{% include list.html list_items=page.items%}




## 資源

{% include cards.html cards=page.tutorial_cards %}
{% include cards.html cards=page.more_cards %}
