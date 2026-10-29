---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "追蹤分析"
nav_order: 40
has_children: true
has_toc: false
redirect_from:
  - /observability-plugin/trace/index/
  - /monitoring-plugins/trace/index/
  - /observing-your-data/trace/
---

# 追蹤分析

如需結合服務拓撲、RED 指標及脈絡內關聯分析的更整合監控體驗，請參閱[應用程式效能監控]({{site.url}}{{site.baseurl}}/observing-your-data/apm/index/)。
{: .note}

追蹤分析提供在 OpenSearch 中匯入並視覺化 [OpenTelemetry](https://opentelemetry.io/) 資料的方式。這些資料可協助您找出並修正分散式應用程式中的效能問題。

單一操作（例如使用者點選按鈕）可能觸發一連串的事件。前端可能呼叫某個後端服務，該服務再呼叫另一個服務，後者查詢資料庫、處理資料，並將資料傳回原始服務，原始服務再將確認訊息傳送至前端。

追蹤分析可協助您將這一連串的事件流程視覺化並識別效能問題，如下圖所示。

![詳細追蹤檢視]({{site.url}}{{site.baseurl}}/images/ta-trace.png)

追蹤分析會分析來自您應用程式的追蹤。OpenSearch 也可以為其處理的請求產生追蹤。如需詳細資訊，請參閱[分散式追蹤]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/telemetry/distributed-tracing/)。

## 使用 Jaeger 資料的追蹤分析

追蹤分析在 OpenSearch Observability 外掛程式中支援 Jaeger 追蹤資料。如果您使用 OpenSearch 作為 Jaeger 追蹤資料的後端，即可使用內建的追蹤分析功能。

若要設定環境以使用追蹤分析，請參閱 [分析 Jaeger 追蹤資料]({{site.url}}{{site.baseurl}}/observability-plugin/trace/trace-analytics-jaeger/)。
