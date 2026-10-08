---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引操作"
parent: Index APIs
nav_order: 30
has_children: true
has_toc: false
---

# 索引操作

索引操作 API 提供進階功能，可維護及最佳化您 OpenSearch 叢集中的索引。這些操作可協助您管理索引效能、資料組織方式及叢集效率。

## 可用的 API

OpenSearch 支援下列索引操作 API。

| API | 說明 |
|-----|-------------|
| [清除索引快取]({{site.url}}{{site.baseurl}}/api-reference/index-apis/clear-index-cache/) | 清除與一或多個索引相關聯的快取。 |
| [複製索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/clone/) | 複製現有索引。 |
| [排清]({{site.url}}{{site.baseurl}}/api-reference/index-apis/flush/) | 排清一或多個索引。 |
| [強制合併]({{site.url}}{{site.baseurl}}/api-reference/index-apis/force-merge/) | 對一或多個索引執行強制合併。 |
| [索引復原]({{site.url}}{{site.baseurl}}/api-reference/index-apis/recover/) | 傳回進行中及已完成的分片復原資訊。 |
| [重新整理]({{site.url}}{{site.baseurl}}/api-reference/index-apis/refresh/) | 重新整理一或多個索引。 |
| [輪替]({{site.url}}{{site.baseurl}}/api-reference/index-apis/rollover/) | 在索引符合特定條件時進行輪替。 |
| [調整規模]({{site.url}}{{site.baseurl}}/api-reference/index-apis/scale/) | 調整一或多個索引的副本數量。 |
| [索引區段]({{site.url}}{{site.baseurl}}/api-reference/index-apis/segment/) | 傳回一或多個索引的區段資訊。 |
| [索引分片儲存區]({{site.url}}{{site.baseurl}}/api-reference/index-apis/shard-stores/) | 傳回分片複本及其儲存位置的資訊。 |
| [縮減索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/shrink-index/) | 縮減現有索引。 |
| [分割]({{site.url}}{{site.baseurl}}/api-reference/index-apis/split/) | 分割現有索引。 |
| [索引統計資料]({{site.url}}{{site.baseurl}}/api-reference/index-apis/stats/) | 傳回一或多個索引的統計資料。 |