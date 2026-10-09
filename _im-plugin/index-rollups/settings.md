---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定"
parent: Index rollups
nav_order: 20
---

# 索引彙總設定

我們不建議變更這些設定；預設值應適用於大多數使用情境。

所有設定皆可透過 OpenSearch `_cluster/settings` 操作取得。這些設定都不需要重新啟動，且全都可以標記為 `persistent` 或 `transient`。若要進一步了解靜態與動態設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

設定 | 預設 | 說明
:--- | :--- | :---
`plugins.rollup.search.backoff_millis` | 1000 milliseconds | 失敗的彙總工作重試之間的退避時間。
`plugins.rollup.search.backoff_count` | 5 | 外掛程式應針對失敗的彙總工作嘗試的重試次數。
`plugins.rollup.search.search_all_jobs` | false | OpenSearch 是否應傳回符合所有指定搜尋詞彙的所有工作。若停用，OpenSearch 只會傳回符合搜尋詞彙的其中一個工作，而非全部。
`plugins.rollup.dashboards.enabled` | true | 是否在 OpenSearch Dashboards 中啟用彙總。
`plugins.rollup.enabled` | true | 是否啟用彙總外掛程式。
`plugins.rollup.ingest.backoff_millis` | 1000 milliseconds | 彙總工作的資料匯入操作之間的退避時間。
`plugins.rollup.ingest.backoff_count` | 5 | 外掛程式應針對失敗的匯入操作嘗試的重試次數。
