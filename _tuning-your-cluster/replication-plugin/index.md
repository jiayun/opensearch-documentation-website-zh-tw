---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "跨叢集複寫"
nav_order: 12
has_children: true
redirect_from:
  - /replication-plugin/
  - /replication-plugin/index/
  - /tuning-your-cluster/replication-plugin/
---

# 跨叢集複寫

跨叢集複寫 (CCR) 外掛程式可讓您將索引、對應與中繼資料從一個 OpenSearch 叢集複寫到另一個叢集。跨叢集複寫具有下列優點：
- 藉由複寫索引，您可以確保在中斷時仍能繼續處理搜尋請求。
- 在地理位置相距遙遠的資料中心之間複寫資料，可縮短資料與應用程式伺服器之間的距離，從而降低高昂的延遲。
- 您可以將多個較小叢集的資料複寫到集中式報告叢集，這在跨大型網路查詢效率不彰時特別有用。

複寫採用主動-被動模式，由跟隨者索引 (接收複寫資料的一方) 從領導者 (遠端) 索引提取資料。

複寫外掛程式支援使用萬用字元模式比對來複寫索引，並提供暫停、恢復與停止複寫的命令。一旦索引開始複寫，系統會在跟隨者叢集的所有主要分片上啟動持續性背景工作，持續向領導者叢集的對應分片輪詢更新。

您可以將複寫外掛程式與 Security 外掛程式搭配使用，透過節點對節點加密來加密跨叢集流量，並控制對複寫活動的存取。

若要開始使用，請參閱[跨叢集複寫入門]({{site.url}}{{site.baseurl}}/replication-plugin/get-started/)。
