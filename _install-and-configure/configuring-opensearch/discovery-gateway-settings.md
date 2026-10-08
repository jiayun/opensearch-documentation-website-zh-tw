---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "探索與閘道設定"
parent: Configuring OpenSearch
nav_order: 30
---

# 探索與閘道設定

以下是與探索及本機閘道相關的設定。

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 探索設定

探索程序會在叢集形成時使用。此程序包括探索節點及選出叢集管理員節點。如需探索與叢集形成設定的完整資訊，請參閱[探索與叢集形成設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/settings/)。

- `discovery.find_peers_interval_during_decommission`（靜態，時間單位）：設定節點處於停用汰除 (decommissioned) 狀態時，嘗試尋找所有對等節點的時間間隔。節點在停用汰除期間，會以此間隔持續探索其他節點，以便在停用汰除過程中維護叢集成員資訊。這有助於確保在受控移除節點時能適當協調。預設值為 `120s`（2 分鐘）。最小值為 `1000ms`。

- `discovery.unconfigured_bootstrap_timeout`（靜態，時間單位）：設定叢集形成期間未設定之啟動程序的逾時時間。此設定控制當叢集未正確設定時（例如未設定 `cluster.initial_cluster_manager_nodes` 時），節點在啟動階段要等待多久。超過此逾時時間後，節點將繼續執行啟動作業，或適當地失敗。此設定有助於避免節點在未設定的狀態下無限期等待。預設值為 `3s`。最小值為 `1ms`。


## 閘道設定

本機閘道會在磁碟上儲存叢集狀態與分片資料，供叢集重新啟動時使用。支援下列本機閘道設定：

- `gateway.recover_after_data_nodes`（靜態，整數）：叢集完全重新啟動後，必須執行中的資料節點最小數量，達到此數量後才能開始復原。
  - **預設值**：`0`
  - **建議**：設定為資料節點的相當比例（約為資料節點總數的 50–70%），以避免過早復原。

- `gateway.expected_data_nodes`（靜態，整數）：叢集中預期的資料節點數量。當所有節點都到齊時，即可立即開始復原本機分片。
  - **預設值**：`0`
  - **建議**：將此值設定為叢集中實際的資料節點數量，以便在所有資料節點都執行後立即開始復原。

- `gateway.recover_after_time`（靜態，時間單位）：若尚未達到預期的資料節點數量，在開始復原前等待的最長時間。超過此時間後，即會進行復原。
  - **預設值**：若已設定 `expected_data_nodes` 或 `recover_after_nodes`，則為 `5m`。否則停用。
  - **建議**：設定為略高於一般節點加入所需的時間；較大型的叢集通常需要較長的時間復原，並會根據觀察到的啟動行為進行調整。

- `gateway.write_dangling_indices_info`（靜態，布林值）：控制 OpenSearch 在保存叢集狀態時，是否將懸置 (dangling) 索引的相關資訊寫入磁碟。啟用時，系統會維護存在於磁碟上但不屬於目前叢集狀態之索引的中繼資料，有助於復原與疑難排解。預設值為 `true`。

- `gateway.auto_import_dangling_indices`（靜態，布林值）：控制 OpenSearch 是否自動匯入在叢集啟動期間發現的懸置索引。懸置索引是指存在於磁碟上但不屬於目前叢集狀態的索引，通常是在叢集未正確關閉或移除節點後遺留下來的。啟用時，這些孤立的索引會在啟動期間自動匯入回叢集狀態。停用時，懸置索引會保留在磁碟上，但不會自動匯入，需要透過 Dangling Indices API 手動處理。此設定有助於復原可能遺失的資料，但應謹慎使用，以免匯入不需要的索引。預設值為 `true`。

