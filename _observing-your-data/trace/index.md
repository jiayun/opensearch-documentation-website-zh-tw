---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "追蹤分析"
parent: Classic observability apps
nav_order: 20
has_children: true
has_toc: false
redirect_from:
  - /observability-plugin/trace/index/
  - /monitoring-plugins/trace/index/
  - /observing-your-data/trace/
---

# 追蹤分析

追蹤分析提供在 OpenSearch 中匯入及視覺化 [OpenTelemetry](https://opentelemetry.io/) 資料的方式。這些資料可協助您找出並修正分散式應用程式中的效能問題。

追蹤分析是[傳統可觀測性應用程式]({{site.url}}{{site.baseurl}}/observing-your-data/classic-observability-apps/)。在 Observability 工作區中，同時啟用 APM 和 Discover Traces 時，便無法使用追蹤分析。若要在 Observability 工作區中分析追蹤，請參閱[追蹤]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-traces/)和[應用程式效能監控]({{site.url}}{{site.baseurl}}/observing-your-data/apm/index/)。

單一操作（例如使用者選取按鈕）可能觸發一連串事件。前端可能呼叫後端服務，該服務再呼叫另一個服務，接著查詢資料庫、處理資料，並將資料傳送至原始服務，再由原始服務將確認訊息傳送至前端。

追蹤分析可協助您將這些事件的流程視覺化，並找出效能問題，如下圖所示。

![詳細追蹤檢視]({{site.url}}{{site.baseurl}}/images/ta-trace.png)

追蹤分析會分析來自您應用程式的追蹤。OpenSearch 也可以為其處理的請求產生追蹤。如需詳細資訊，請參閱[分散式追蹤]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/telemetry/distributed-tracing/)。

## 使用 Jaeger 資料的追蹤分析

追蹤分析支援 Jaeger 追蹤資料。如果您使用 OpenSearch 作為 Jaeger 追蹤資料的後端，即可使用內建的追蹤分析功能。

若要設定環境以使用追蹤分析，請參閱[分析 Jaeger 追蹤資料]({{site.url}}{{site.baseurl}}/observing-your-data/trace/trace-analytics-jaeger/)。
