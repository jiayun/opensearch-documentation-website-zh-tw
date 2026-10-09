---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Discover 探索可觀測性資料"
nav_order: 60
has_children: true
has_toc: false
description: "了解如何在可觀測性工作區中，使用專門的介面探索記錄檔、指標與追蹤資料。這些強化的資料探索功能提供查詢、分析及關聯不同類型遙測資料的工具。"
redirect_from:
  - /observing-your-data/exploring-observability-data/
---

# 使用 Discover 探索可觀測性資料
**於 3.5 版導入**
{: .label .label-purple }

OpenSearch 提供與資料集及關聯性搭配運作的介面，帶來完整的可觀測性體驗，讓您能快速識別問題、了解系統行為，並對分散式應用程式中的問題進行疑難排解。

系統提供專門的介面，用於探索可觀測性資料的三大支柱：

- **記錄檔**：使用 Piped Processing Language (PPL) 查詢與分析記錄資料。
- **指標**：使用 PromQL 查詢探索時間序列指標資料。
- **追蹤**：調查分散式追蹤與跨度關係。

## 先決條件

若要使用這些資料探索功能，您需要：

- **建立可觀測性工作區**：這些功能僅在 Observability 工作區內可用。若要了解如何啟用及建立工作區，請參閱 [OpenSearch Dashboards 工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace/)。
- **啟用功能旗標**：在您的 `opensearch_dashboards.yml` 檔案中設定必要的設定。每個功能頁面都會提供所需的特定組態。
- **設定資料來源**：為您的記錄檔、指標與追蹤設定適當的資料來源。組態指引請參閱 [資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/)。

### 建立可觀測性工作區

若要建立可觀測性工作區，請依照下列步驟操作：

1. 啟用工作區。如需更多資訊，請參閱 [啟用工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace/#enabling-workspaces)。
2. 在 OpenSearch Dashboards 首頁上，選取 **Create Workspace** 並選擇 **Observability**。或者，也可以選取 **Observability** 卡片上的加號來建立新的可觀測性工作區。
3. 在 **Workspace details** 中，輸入工作區的 **Name** 與選用的 **Description**。
4. 選取 **Observability** 作為使用案例，然後選取 **Create workspace**。

詳細說明請參閱 [建立工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/create-workspace/)。

## 入門

建立可觀測性工作區後，請依照下列步驟開始使用：

1. **[資料集]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/datasets/)** -- 了解如何將可觀測性資料整理成易於管理的資料集。
1. **[探索記錄資料]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-logs/)** -- 使用 PPL 查詢與視覺化探索記錄資料。
1. **[探索追蹤資料]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-traces/)** -- 分析分散式追蹤與跨度關係。
1. **[探索指標資料]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-metrics/)** -- 使用 PromQL 查詢並視覺化時間序列指標。
1. **[關聯性]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/correlations/)** -- 了解如何連結追蹤與記錄資料集，以進行統一分析。