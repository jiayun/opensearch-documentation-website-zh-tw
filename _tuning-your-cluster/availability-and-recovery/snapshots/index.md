---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "快照"
nav_order: 5
has_children: true
parent: Availability and recovery
redirect_from:
  - /opensearch/snapshots/
  - /opensearch/snapshots/index/
  - /tuning-your-cluster/availability-and-recovery/snapshots/
has_toc: false
---

# 快照

快照是叢集索引與狀態的備份。狀態包括叢集設定、節點資訊、索引中繼資料（對應、設定或範本），以及分片分配。

快照有兩個主要用途：

- **從故障中復原**

  例如，當叢集健康狀態變為紅色時，您可以從快照還原處於紅色狀態的索引。

- **從一個叢集遷移到另一個叢集**

  例如，如果您要從概念驗證叢集移轉至生產環境叢集，可以先對前者製作快照，再於後者上還原。


您可以使用[快照 API]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore/) 來製作與還原快照。

如果您需要自動化快照的建立，可以使用[快照管理]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-management/)功能。
