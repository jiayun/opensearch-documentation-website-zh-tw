---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "快取設定"
parent: Configuring OpenSearch
nav_order: 70
---

# 快取設定

OpenSearch 提供多種快取設定，可用來最佳化記憶體使用量與效能。這些設定控制 OpenSearch 如何管理快取的資料結構，以及快取作業的記憶體配置。

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 快取回收器設定

快取回收器負責管理記憶體頁面的重複使用，以降低記憶體回收 (garbage collection) 的額外負荷。OpenSearch 支援下列快取回收器設定：

- `cache.recycler.page.limit.heap`（靜態，位元組大小）：頁面快取回收器堆積使用量的記憶體大小上限。預設為堆積的 `10%`。

- `cache.recycler.page.weight.bytes`（靜態，倍精度浮點數）：快取回收器中位元組頁面回收的權重係數。預設為 `1.0`。最小值為 `0.0`。

- `cache.recycler.page.weight.ints`（靜態，倍精度浮點數）：快取回收器中整數頁面回收的權重係數。預設為 `1.0`。最小值為 `0.0`。

- `cache.recycler.page.weight.longs`（靜態，倍精度浮點數）：快取回收器中長整數頁面回收的權重係數。預設為 `1.0`。最小值為 `0.0`。

- `cache.recycler.page.weight.objects`（靜態，倍精度浮點數）：快取回收器中物件頁面回收的權重係數。物件頁面的用處較低，因此預設給予較低的權重。預設為 `0.1`。最小值為 `0.0`。