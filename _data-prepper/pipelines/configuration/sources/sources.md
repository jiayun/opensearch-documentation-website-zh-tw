---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "來源"
parent: Pipelines
has_children: true
nav_order: 110
redirect_from:
  - /data-prepper/pipelines/configuration/sources/
---

# Data Prepper 來源

`source` 是一種輸入元件，用來指定 OpenSearch Data Prepper 管線如何匯入事件。每條管線只有一個來源，該來源會透過 HTTP(S) 接收事件，或從外部端點讀取，例如 OpenTelemetry Collector 或 Amazon Simple Storage Service (Amazon S3)。來源具有可設定的選項，取決於事件格式（字串、JSON、Amazon CloudWatch 記錄檔、OpenTelemtry 追蹤）。來源會取用事件，並將其傳遞至 [`buffer`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/buffers/buffers/) 元件。


