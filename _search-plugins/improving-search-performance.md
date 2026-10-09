---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "改善搜尋效能"
nav_order: 220
has_children: true
has_toc: false
---

# 改善搜尋效能

OpenSearch 提供多種改善搜尋效能的方式，從基礎最佳化到專門技術：

- 使用[快取]({{site.url}}{{site.baseurl}}/search-plugins/caching/)將經常存取的資料儲存在記憶體中，以加快擷取速度。

- 使用[並行分段搜尋]({{site.url}}{{site.baseurl}}/search-plugins/concurrent-segment-search/)同時搜尋多個分段，以提升資源使用率。

- 使用[搜尋分片路由]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/search-shard-routing/)控制分片選取，以最佳化查詢路由。

- 針對時間序列工作負載，使用[索引層級搜尋剪枝]({{site.url}}{{site.baseurl}}/search-plugins/index-level-search-pruning/)略過不可能包含符合文件之索引。

- 使用[非同步搜尋]({{site.url}}{{site.baseurl}}/search-plugins/async/)以非同步方式執行資源密集的查詢，避免逾時。

- 針對分析工作負載，使用[星狀樹索引]({{site.url}}{{site.baseurl}}/search-plugins/star-tree-index/)改善彙總效能。
