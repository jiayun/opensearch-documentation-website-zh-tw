---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定"
parent: Asynchronous search
grand_parent: Improving search performance
nav_order: 4
---

# 非同步搜尋設定

Asynchronous Search 外掛程式為標準的 OpenSearch 叢集設定新增了數項設定。這些設定是動態的，因此您無需重新啟動叢集即可變更外掛程式的預設行為。若要進一步了解靜態與動態設定，請參閱 [設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

您可以將設定標記為 `persistent` 或 `transient`。

例如，若要更新結果索引的保留期間：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.asynchronous_search.max_wait_for_completion_timeout": "5m"
  }
}
```

設定 | 預設值 | 說明
:--- | :--- | :---
`plugins.asynchronous_search.max_search_running_time` | 12 小時 | 搜尋的最長執行時間，超過後搜尋將被終止。
`plugins.asynchronous_search.node_concurrent_running_searches` | 20 | 每個協調節點同時執行的搜尋數量。
`plugins.asynchronous_search.max_keep_alive` | 5 天 | 搜尋結果可在叢集中儲存的最長時間。
`plugins.asynchronous_search.max_wait_for_completion_timeout` | 1 分鐘 | `wait_for_completion_timeout` 參數的最大值。
`plugins.asynchronous_search.persist_search_failures` | false | 將以搜尋失敗結束的非同步搜尋結果保存在系統索引中。
