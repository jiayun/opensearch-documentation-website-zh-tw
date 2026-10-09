---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "架構"
nav_order: 15
permalink: /classic/migration-assistant/architecture/
---

# Migration Assistant (classic) 架構

Migration Assistant (classic) 架構是以使用 AWS 雲端基礎設施為基礎，但大多數工具的設計皆與雲端無關。此解決方案也提供本機容器化版本。

部署於 AWS 的設計採用下列架構。

![遷移架構概觀]({{site.url}}{{site.baseurl}}/images/migrations/migrations-architecture-overview.png)

圖中的每個節點對應至遷移程序中的下列步驟：

1. 用戶端流量會導向至現有叢集。
2. 具有擷取代理的 Application Load Balancer 會將流量轉送至來源，同時將資料複寫至 Amazon Managed Streaming for Apache Kafka (Amazon MSK)。
3. 使用 Migration Console 取得特定時間點的快照。快照完成後，會使用 Metadata Migration Tool 在目標叢集上建立索引、範本、元件範本及別名。在持續擷取流量到位的情況下，`Reindex-from-Snapshot` 會從來源遷移資料。
4. `Reindex-from-Snapshot` 完成後，Traffic Replayer 會將擷取的流量從 Amazon Managed Streaming for Apache Kafka (Amazon MSK) 重播至目標叢集。
5. 透過檢閱記錄檔與指標，比較傳送至來源與目標叢集的流量效能及行為。
6. 確認目標叢集的功能符合預期後，會將用戶端重新導向至新的目標。
