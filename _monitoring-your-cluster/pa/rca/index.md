---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "根本原因分析"
nav_order: 50
parent: Performance Analyzer
has_children: true
redirect_from:
  - /monitoring-plugins/pa/rca/index/
  - /monitoring-your-cluster/pa/rca/
---

# 根本原因分析

OpenSearch Performance Analyzer 外掛程式 (PA) 會擷取 OpenSearch 與 JVM 的活動，以及它們的底層資源使用情況（例如磁碟、網路、CPU 和記憶體）。根據這些量測資料，Performance Analyzer 會計算並提供診斷指標，讓管理員能夠測量並了解其 OpenSearch 叢集中的瓶頸。

根本原因分析框架 (RCA) 會使用 PA 的資訊，在叢集可能發生效能或可用性問題時，向管理員警示問題的根本原因。

簡而言之，此框架可協助您存取執行 Performance Analyzer 的 OpenSearch 節點所產生的資料串流。您可以撰寫 Java 程式碼片段，選擇您關注的串流，並根據特定門檻評估這些串流的 PA 指標。當 RCA 執行時，您可以使用 REST API 存取每項分析的狀態。

若要進一步了解根本原因分析，請參閱[其在 GitHub 上的儲存庫](https://github.com/opensearch-project/performance-analyzer-rca)。
