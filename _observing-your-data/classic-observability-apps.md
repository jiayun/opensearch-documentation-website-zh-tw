---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "傳統可觀測性應用程式"
nav_order: 40
has_children: true
has_toc: false
---

# 傳統可觀測性應用程式

在傳統導覽中，OpenSearch Dashboards 會在 **Observability** 選單中提供可觀測性應用程式。這些應用程式不需要工作區，也不需要在 `opensearch_dashboards.yml` 中進行其他設定。

下表說明這些應用程式，並列出每個應用程式在單一資料來源下，以及啟用[多個資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/multi-data-sources/)時是否可用。

| 應用程式 | 說明 | 單一資料來源 | 多個資料來源 |
|:---|:---|:---|:---|
| [事件分析]({{site.url}}{{site.baseurl}}/observing-your-data/event-analytics/) | 使用 Piped Processing Language (PPL) 查詢記錄事件，並根據結果建立視覺化。 | 是 | 否 |
| [追蹤分析]({{site.url}}{{site.baseurl}}/observing-your-data/trace/index/) | 檢視追蹤與服務的儀表板，包括延遲、錯誤率和輸送量。 | 是 | 是 |
| [指標分析]({{site.url}}{{site.baseurl}}/observing-your-data/prometheusmetrics/) | 查詢並視覺化儲存在 Prometheus 或 OpenSearch 中 OpenTelemetry 指標索引內的指標。 | 是 | 是 |
| [應用程式分析]({{site.url}}{{site.baseurl}}/observing-your-data/app-analytics/) | 將應用程式的記錄檔、追蹤和指標合併成單一健康狀態檢視。 | 是 | 否 |
| [操作面板]({{site.url}}{{site.baseurl}}/observing-your-data/operational-panels/) | 將 PPL 視覺化整理成儀表板。 | 是 | 否 |
| [筆記本]({{site.url}}{{site.baseurl}}/dashboards/notebooks/) | 將 Markdown 文字、SQL 與 PPL 查詢以及視覺化合併成報告和執行手冊。 | 是 | 是 |
