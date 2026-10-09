---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "可觀測性"
nav_order: 1
has_children: true
has_toc: false
nav_exclude: true
permalink: /observing-your-data/
redirect_from:
  - /observability-plugin/index/
  - /observing-your-data/index/
---

# 可觀測性

OpenSearch 提供可觀測性功能，可用於監控應用程式、基礎架構與 AI 代理程式。請選擇符合您使用情境的路徑。

---

## 匯入可觀測性資料

在探索資料之前，您需要先將資料匯入 OpenSearch。使用 [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 將非結構化的記錄資料轉換為結構化資料，以改善查詢與篩選。

<span class="centering-container">
[開始使用記錄匯入]({{site.url}}{{site.baseurl}}/observing-your-data/log-ingestion/){: .btn-dark-blue}
</span>

---

## 探索與分析可觀測性資料

OpenSearch 提供下列工具來探索與分析可觀測性資料：

- [事件分析]({{site.url}}{{site.baseurl}}/observing-your-data/event-analytics/) -- 使用 [Piped Processing Language (PPL)]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/) 將資料驅動的事件轉換為視覺化。
- [應用程式分析]({{site.url}}{{site.baseurl}}/observing-your-data/app-analytics/) -- 建立自訂的可觀測性應用程式，以檢視系統可用性狀態。
- [追蹤分析]({{site.url}}{{site.baseurl}}/observing-your-data/trace/index/) -- 將應用程式的分散式追蹤視覺化並加以分析。
- [指標分析]({{site.url}}{{site.baseurl}}/observing-your-data/prometheusmetrics/) -- 查詢並將 Prometheus 指標資料視覺化。
- [使用 Discover 進行可觀測性分析]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/) -- 在可觀測性工作區中使用專用介面來分析記錄、指標與追蹤。

---

## 監控應用程式

針對特定的應用程式監控，OpenSearch 提供兩種專用解決方案：適用於傳統微服務的 Application Performance Monitoring (APM)，以及適用於 AI/LLM 應用程式的代理程式追蹤。

|  | APM | 代理程式追蹤 |
|---------|-----|--------------|
| **用途** | 監控微服務與 Web 應用程式 | 監控 AI 代理程式與大型語言模型 (LLM) |
| **指標** | RED 指標 (Rate、Errors、Duration) | 詞元用量、模型呼叫、代理程式步驟 |
| **視覺化** | 服務對應圖、延遲圖表、錯誤追蹤 | 執行圖 (DAG)、追蹤樹、時間軸 |
| **慣例** | OpenTelemetry 標準慣例 | OpenTelemetry 生成式 AI 語意慣例 |
| **最適合** | API、微服務、Web 服務 | 聊天機器人、AI 代理程式、LLM 應用程式 |

### APM

[APM]({{site.url}}{{site.baseurl}}/observing-your-data/apm/) 使用服務拓撲、RED 指標與效能追蹤來監控分散式應用程式。APM 需要下列元件：

- 一個 OpenSearch 叢集，以及已啟用[工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/)的 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/)。
- 一個 OpenTelemetry Collector。
- [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/)。
- 用於儲存指標的 Prometheus。
- 已導入 OpenTelemetry 監測功能的應用程式。

### 代理程式追蹤

[代理程式追蹤]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/)使用專為 AI 工作負載設計的追蹤功能，來觀測生成式 AI 應用程式與 LLM 代理程式。代理程式追蹤需要下列元件：

- 一個 OpenSearch 叢集與 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/)。
- 用於追蹤處理的 [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/)。
- 依照 OpenTelemetry 生成式 AI 語意慣例導入追蹤功能的應用程式。

<span class="centering-container">
[開始使用代理程式追蹤]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/){: .btn-dark-blue}
</span>

---

## 查詢效能

使用 [Query Insights]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/) 來監控並最佳化叢集中執行之查詢的效能。找出慢速查詢、分析查詢模式，並改善叢集效率。

<span class="centering-container">
[開始使用 Query Insights]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/){: .btn-dark-blue}
</span>

---

## 整理視覺化

建立視覺化之後，請將其整理至儀表板與報告中，以便與團隊分享：

- [Notebooks]({{site.url}}{{site.baseurl}}/observing-your-data/notebooks/) -- 結合視覺化、程式碼區塊與敘述文字，以建立報告、操作手冊與文件。
- [操作面板]({{site.url}}{{site.baseurl}}/observing-your-data/operational-panels/) -- 將 PPL 視覺化整理至儀表板中，以進行監控與分析。

---

## 警示與偵測

OpenSearch 提供用於偵測問題與傳送通知的工具：

- [警示]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/) -- 建立會依排程查詢資料的監視器、定義警示條件的觸發程序，並在警示觸發時執行動作。
- [異常偵測]({{site.url}}{{site.baseurl}}/observing-your-data/ad/) -- 使用機器學習與 Random Cut Forest (RCF) 演算法，自動偵測時間序列資料中的異常。
- [預測]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/) -- 使用 RCF 模型預測時間序列資料的未來值，以便在超出閾值之前預先因應。
- [服務等級目標]({{site.url}}{{site.baseurl}}/observing-your-data/slo/) (實驗性) -- 為您的服務定義可用性與延遲目標，並依據與 Prometheus 相容的 ruler 追蹤錯誤預算與耗用率。
- [通知]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/) -- 設定透過 Slack、電子郵件、Amazon SNS、Webhook 及其他通訊服務傳送警示的管道。

---

## OpenSearch Observability Stack

OpenSearch Observability Stack 提供一套完整且預先設定好的可觀測性平台，您可以使用 Docker Compose 在本機執行。Observability Stack 包含：

- 所有 APM 與代理程式追蹤功能。
- 用於在 Python 或 TypeScript 應用程式中導入監測功能的 GenAI SDK。
- 用於本機偵錯與評估的 Agent Health 工具。
- 包含範例應用程式的 Docker Compose 設定。
- 預先設定好的 OpenTelemetry Collector、[OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 與 Prometheus。

<span class="centering-container">
[進一步了解 Observability Stack](https://observability.opensearch.org/){: .btn-dark-blue}
</span>
