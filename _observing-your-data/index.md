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
steps:
- heading: 匯入或連線您的資料
  description: 將記錄檔與追蹤傳送至 OpenSearch，或連線 Prometheus 資料來源以取得指標。
  link: /observing-your-data/ingesting-observability-data/
- heading: 選擇您的可觀測性應用程式
  description: 使用 **Observability** 選單中的傳統應用程式，或使用可觀測性工作區中的應用程式，為每項工作找到合適的應用程式。
  link: /observing-your-data/exploring-data/
- heading: 設定警示
  description: 若要自動偵測異常，請建立監視器，在您的資料符合條件時通知您。
  link: /observing-your-data/alerting/index/
detection_cards:
- heading: 警示
  description: 建立會依排程查詢您資料的監視器、定義警示條件的觸發條件，並在警示觸發時執行動作。
  link: /observing-your-data/alerting/index/
- heading: 異常偵測
  description: 使用 Random Cut Forest (RCF) 演算法的機器學習，偵測時間序列資料中的異常。
  link: /observing-your-data/ad/index/
- heading: 預測
  description: 使用 RCF 模型預測時間序列資料的未來值，在閾值超出發生前預先察覺。
  link: /observing-your-data/forecast/index/
- heading: 通知
  description: 設定管道，透過 Slack、電子郵件、Amazon SNS、Webhook 及其他通訊服務傳送警示。
  link: /observing-your-data/notifications/index/
getting_started_cards:
- heading: 開始使用記錄檔分析
  description: 使用 Fluent Bit 與 Data Prepper 將網頁記錄檔傳送至 OpenSearch，然後在 OpenSearch Dashboards 中查詢並視覺化這些記錄檔。
  link: /observing-your-data/log-ingestion/
- heading: 開始使用追蹤分析
  description: 執行會產生追蹤的範例應用程式，使用 Data Prepper 將追蹤傳送至 OpenSearch，並在 Trace analytics 中檢視。
  link: /observing-your-data/trace/getting-started/
- heading: 開始使用指標分析
  description: 將 OpenSearch 連線至 Prometheus 資料來源，然後在 Metric analytics 中使用 PPL 查詢並視覺化指標。
  link: /observing-your-data/prometheusmetrics/
---

# 可觀測性

OpenSearch 提供可觀測性功能，可監視應用程式、基礎設施與 AI 代理程式。您可以匯入記錄檔、追蹤與指標，在 OpenSearch Dashboards 中探索並視覺化這些資料，並設定警示以在發生問題時通知您。

---

## 入門

若要開始使用，請選擇您想探索的資料類型。記錄檔與追蹤分析教學會將範例資料匯入 OpenSearch，並在 OpenSearch Dashboards 中探索這些資料。

{% include cards.html cards=page.getting_started_cards %}

---

## 設定可觀測性

若要為您的應用程式設定可觀測性，請依照下列步驟操作。如果您的資料已在 OpenSearch 中，請從步驟 2 開始。

{% include list.html list_items=page.steps %}

---

## 監視應用程式

OpenSearch 提供兩種監視應用程式的方式：適用於微服務與網頁應用程式的應用程式效能監視 (APM)，以及適用於生成式 AI 應用程式的代理程式監視。

|  | APM | 代理程式監視 |
|---------|-----|--------------|
| **用途** | 監視微服務與網頁應用程式 | 監視 AI 代理程式與大型語言模型 (LLM) |
| **指標** | 速率、錯誤與持續時間 (RED) 指標 | 詞元用量、模型呼叫、代理程式步驟 |
| **視覺化** | 服務拓撲圖、延遲圖表、錯誤追蹤 | 執行圖 (DAG)、追蹤樹、時間軸 |
| **慣例** | OpenTelemetry 標準慣例 | OpenTelemetry 生成式 AI 語意慣例 |
| **最適合** | API、微服務、網頁服務 | 聊天機器人、AI 代理程式、LLM 應用程式 |

### APM

[APM]({{site.url}}{{site.baseurl}}/observing-your-data/apm/) 使用服務拓撲、RED 指標與效能追蹤來監視分散式應用程式。APM 需要可觀測性工作區、OpenTelemetry Collector、Data Prepper 與 Prometheus。

APM 也包含[服務等級目標 (SLO)]({{site.url}}{{site.baseurl}}/observing-your-data/slo/)，可讓您為服務定義可用性與延遲目標，並追蹤其錯誤預算。

### 代理程式監視

[代理程式監視]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/) 會追蹤生成式 AI 應用程式中的 LLM 呼叫、工具叫用與詞元用量。代理程式監視需要可觀測性工作區、OpenTelemetry Collector、Data Prepper，以及已依照 OpenTelemetry 生成式 AI 語意慣例加入遙測埋點的應用程式。

---

## 警示與偵測

OpenSearch 提供下列工具來偵測問題並傳送通知。這些工具可搭配 OpenSearch 中的任何索引使用，包括可觀測性資料。

{% include cards.html cards=page.detection_cards %}


---

## OpenSearch Observability Stack

[OpenSearch Observability Stack](https://observability.opensearch.org/) 提供完整且預先設定好的可觀測性平台，您可以使用 Docker Compose 在本機執行。Observability Stack 包含：

- 所有 APM 與代理程式追蹤功能。
- 用於在 Python 或 TypeScript 應用程式中加入遙測埋點的 GenAI SDK。
- 供本機偵錯與評估使用的 Agent Health 工具。
- 包含範例應用程式的 Docker Compose 設定。
- 預先設定好的 OpenTelemetry Collector、OpenSearch Data Prepper 與 Prometheus。

---

## 參考資料

- [可觀測性安全性]({{site.url}}{{site.baseurl}}/observing-your-data/observability-security/) -- 控制哪些使用者可以檢視與修改可觀測性物件，例如筆記本與視覺化。
- [Simple Schema for Observability]({{site.url}}{{site.baseurl}}/observing-your-data/ss4o/) -- 部分傳統可觀測性應用程式所需的索引命名慣例與欄位對應。