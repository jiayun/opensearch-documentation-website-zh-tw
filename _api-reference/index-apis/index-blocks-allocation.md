---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引封鎖與配置"
parent: Index APIs
nav_order: 70
has_children: true
has_toc: false
---

# 索引封鎖與配置

索引封鎖與配置 API 可讓您控制索引存取限制與分片配置原則。這些 API 可協助您管理叢集資源，並控制索引在叢集節點之間的分散方式。

## 可用的 API

OpenSearch 支援下列索引封鎖與配置 API。

| API | 說明 |
|-----|-------------|
| [Blocks]({{site.url}}{{site.baseurl}}/api-reference/index-apis/blocks/) | 新增或移除限制索引操作的索引封鎖。 |
| [Shard allocation]({{site.url}}{{site.baseurl}}/api-reference/index-apis/shard-allocation/) | 控制索引的分片配置與路由。 |