---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "探索可觀測性資料"
nav_order: 30
---

# 探索可觀測性資料

OpenSearch Dashboards 提供兩組可觀測性應用程式。您使用哪一組，取決於 OpenSearch Dashboards 的組態方式：

- [傳統可觀測性應用程式]({{site.url}}{{site.baseurl}}/observing-your-data/classic-observability-apps/)可在傳統導覽的 **Observability** 選單中使用，不需要額外設定。
- [可觀測性工作區應用程式]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/)可在 Observability 工作區中使用。若要使用這些應用程式，請在 `opensearch_dashboards.yml` 中啟用工作區與可觀測性設定，然後建立 Observability 工作區。所需設定請參閱 [必要條件]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/index/#prerequisites)。應用程式效能監控 (APM)、服務等級目標 (SLO) 與代理程式監控只在工作區中提供。

下表列出每組應用程式中各項任務所使用的應用程式。

| 任務 | 傳統可觀測性應用程式 | Observability 工作區應用程式 |
|:---|:---|:---|
| 探索記錄資料 | [Event analytics]({{site.url}}{{site.baseurl}}/observing-your-data/event-analytics/) | [Logs]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-logs/) |
| 探索追蹤資料 | [Trace analytics]({{site.url}}{{site.baseurl}}/observing-your-data/trace/index/) | [Traces]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-traces/)、[Agent monitoring]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/) |
| 探索指標 | [Metric analytics]({{site.url}}{{site.baseurl}}/observing-your-data/prometheusmetrics/) | [Metrics]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-metrics/) |
| 監視應用程式 | [Application analytics]({{site.url}}{{site.baseurl}}/observing-your-data/app-analytics/) | [Application performance monitoring]({{site.url}}{{site.baseurl}}/observing-your-data/apm/)，包括 [Services]({{site.url}}{{site.baseurl}}/observing-your-data/apm/services/)、[Topology map]({{site.url}}{{site.baseurl}}/observing-your-data/apm/application-map/) 與 [SLOs]({{site.url}}{{site.baseurl}}/observing-your-data/slo/) |
| 建立儀表板 | [Operational panels]({{site.url}}{{site.baseurl}}/observing-your-data/operational-panels/) | [Dashboards]({{site.url}}{{site.baseurl}}/dashboards/dashboard/index/) |

## 選擇追蹤工具

多個應用程式都會顯示追蹤資料。下表說明每個應用程式及其可用位置。

| 應用程式 | 用途 | 可用位置 |
|:---|:---|:---|
| [Trace analytics]({{site.url}}{{site.baseurl}}/observing-your-data/trace/index/) | 檢視透過 Data Prepper 或 Jaeger 匯入的資料中，追蹤與服務的預先建置儀表板，包括延遲、錯誤率與輸送量。 | 傳統導覽與 Observability 工作區 |
| [Traces]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-traces/) | 搜尋與篩選跨度（span），並以時間軸檢視單一追蹤的各個跨度。 | Observability 工作區 |
| [Application performance monitoring]({{site.url}}{{site.baseurl}}/observing-your-data/apm/) | 檢視每個服務的速率、錯誤與持續時間 (RED) 指標，以及服務相依性的拓撲圖。 | Observability 工作區 |
| [Agent monitoring]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/) | 檢視生成式 AI 代理程式的步驟、工具呼叫與詞元用量。 | Observability 工作區 |

在 Observability 工作區中，當 APM 與 Discover Traces 同時啟用時，APM 會取代 Trace analytics。各應用程式所需的設定請參閱 [Observability 工作區應用程式]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/)。

關於 OpenSearch 為其處理的請求所產生的追蹤紀錄，請參閱 [分散式追蹤]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/telemetry/distributed-tracing/)。

## 視覺化您的資料

若要與團隊共用視覺化內容，請將其加入儀表板。在傳統導覽中使用 [operational panels]({{site.url}}{{site.baseurl}}/observing-your-data/operational-panels/)；在 Observability 工作區則從 Logs 頁面將其加入 [dashboards]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-logs/#adding-visualizations-to-dashboards)。若要將視覺化、查詢與文字合併成報表與執行手冊（runbook），請使用 [Notebooks]({{site.url}}{{site.baseurl}}/dashboards/notebooks/)，此功能在傳統導覽與 Observability 工作區皆可使用。
