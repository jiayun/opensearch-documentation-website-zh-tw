---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "可觀測性工作區應用程式"
nav_order: 50
has_children: true
has_toc: false
description: "設定可觀測性工作區，以便在 Discover 中探索記錄檔、追蹤和指標，並使用應用程式效能監控、服務層級目標與代理程式監控。"
redirect_from:
  - /observing-your-data/exploring-observability-data/
---

# 可觀測性工作區應用程式
**於 3.5 版首次推出**
{: .label .label-purple }

在可觀測性[工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/index/)中，OpenSearch Dashboards 提供多種應用程式，可用於在 Discover 中探索記錄檔、追蹤和指標、監控應用程式效能、追蹤服務層級目標 (SLO)，以及監控生成式 AI 代理程式。每個應用程式都由 `opensearch_dashboards.yml` 中的一項設定啟用，該設定會列在應用程式的頁面上。

## 必要條件

若要啟用所有可觀測性工作區應用程式，請將下列設定新增至 `opensearch_dashboards.yml`，然後重新啟動 OpenSearch Dashboards：

```yaml
workspace.enabled: true
explore.enabled: true                  # Logs
explore.discoverTraces.enabled: true   # Traces, APM, and SLOs
explore.discoverMetrics.enabled: true  # Metrics and APM
explore.agentTraces.enabled: true      # Agent monitoring
datasetManagement.enabled: true        # Datasets and Correlations
observability.slo.enabled: true        # SLOs
```
{% include copy.html %}

若只要啟用部分應用程式，請參閱每個應用程式頁面的必要條件章節，以了解該應用程式所需的設定。

工作區還有其他需求，例如停用多租用戶。如需更多資訊，請參閱[啟用工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace/#enabling-workspaces)。

## 建立可觀測性工作區

若要建立可觀測性工作區，請依照下列步驟操作：

1. 在 OpenSearch Dashboards 首頁的 **My workspaces** 中，選取 **Observability** 卡片上的 **Create workspace**。
1. 在 **Workspace details** 中，輸入 **Name**，並可選擇性地輸入 **Description**。
1. 在 **Use case and features** 中，確認已選取 **Observability**。
1. 如果您使用多個資料來源，請選取要與工作區建立關聯的資料來源。
1. 選取 **Create workspace**。

如需更多資訊，請參閱[建立工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/create-workspace/)。

## 探索與監控您的資料

建立工作區後，請依照下列方式使用這些應用程式：

1. 連接您的資料：
   - 為您的記錄檔索引和追蹤索引建立[資料集]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/datasets/)。Logs 與 Traces 頁面、Correlations 及 APM 會使用資料集來尋找您的資料。
   - 若要使用 Metrics、APM 或 SLO，請連接 [Prometheus 資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/connect-prometheus/)。
1. 探索您的資料：
   - 使用 [Logs]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-logs/) 以 Piped Processing Language (PPL) 搜尋、篩選並視覺化記錄資料。
   - 使用 [Traces]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-traces/) 搜尋與篩選追蹤區段（span），並將單一追蹤顯示為其追蹤區段的時間軸。
   - 使用 [Metrics]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-metrics/) 以 PromQL 查詢並視覺化 Prometheus 指標。
   - 使用 [Correlations]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/correlations/) 將追蹤資料集連結至記錄檔資料集，以便檢視與某個追蹤相關的記錄檔項目。
1. 監控您的應用程式：
   - 使用[應用程式效能監控 (APM)]({{site.url}}{{site.baseurl}}/observing-your-data/apm/) 檢視每個服務的速率、錯誤與持續時間 (RED) 指標，以及服務相依性的拓撲圖。
   - 使用 [SLO]({{site.url}}{{site.baseurl}}/observing-your-data/slo/) 為您的服務定義可用性與延遲目標，並追蹤其錯誤預算。
1. 監控您的 AI 代理程式：
   - 使用 [Agent monitoring]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/) 檢視生成式 AI 代理程式的 LLM 呼叫、工具叫用與詞元用量。
1. 分享您的結果：
   - 將 Logs 頁面中的視覺化新增至[儀表板]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-logs/#adding-visualizations-to-dashboards)。
   - 使用 [Notebooks]({{site.url}}{{site.baseurl}}/dashboards/notebooks/) 將 Markdown 文字、SQL 與 PPL 查詢以及視覺化組合成報告與操作手冊。

## 相關文件

- 若要了解記錄檔、追蹤和指標如何送達 OpenSearch，請參閱[匯入可觀測性資料]({{site.url}}{{site.baseurl}}/observing-your-data/ingesting-observability-data/)。
- 若要在顯示追蹤資料的應用程式之間做選擇，請參閱[選擇追蹤工具]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-data/#choosing-a-trace-tool)。