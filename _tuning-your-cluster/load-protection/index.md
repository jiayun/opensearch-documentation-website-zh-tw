---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "負載保護"
nav_order: 50
has_children: true
has_toc: true
redirect_from:
  - /tuning-your-cluster/load-protection/
---

# 負載保護

當節點或叢集管理員收到的工作量超過其所能完成時，OpenSearch 可以拒絕或取消請求。搜尋背壓會取消耗用大量資源的搜尋請求，分片編製索引背壓會拒絕過載分片上的編製索引請求，並行限制會限制某個動作同時進行中的請求數量，而叢集管理員任務節流則會限制節點提交給叢集管理員的任務。
