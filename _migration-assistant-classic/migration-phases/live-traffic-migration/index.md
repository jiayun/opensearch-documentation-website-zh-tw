---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "即時流量遷移"
parent: Migration phases
nav_order: 99
permalink: /classic/migration-assistant/live-traffic-migration/
has_toc: false
has_children: true
---

# 即時流量遷移

即時流量遷移會攔截傳送到來源叢集的 HTTP 請求，並在轉送至來源叢集之前，將它們儲存在持久性串流中。接著，儲存的請求會被複製並重放到目標叢集。此程序會同步來源與目標叢集，同時突顯兩者之間的行為與效能差異。Kafka 用於管理資料流並重建 HTTP 請求。您可以透過 Amazon CloudWatch 指標與 [Migration Console]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-console/accessing-the-migration-console/) 監視複製程序，後者會以 JSON 格式提供結果以供分析。

若要開始使用即時流量遷移，請依照下列步驟操作：

1. [使用 Traffic Replayer]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/replay-captured-traffic/)
2. [將流量從來源叢集切換]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/reroute-traffic-from-capture-proxy-to-target/)
