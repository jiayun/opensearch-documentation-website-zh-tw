---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定"
parent: Index State Management
nav_order: 50
---

# ISM 設定

我們不建議變更這些設定；預設值應能滿足大多數使用情境。

索引狀態管理 (Index State Management, ISM) 將其組態儲存在 `.opendistro-ism-config` 索引中。請勿在未使用 [ISM API 操作]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/)的情況下修改此索引。

所有設定都可以透過 OpenSearch 的 `_cluster/settings` 操作存取。這些設定都不需要重新啟動，且全部都可以標記為 `persistent` 或 `transient`。若要進一步了解靜態與動態設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

由於 ISM 設定屬於叢集設定，持久的 ISM 設定是全域叢集狀態的一部分，並且會包含在 `include_global_state` 設為 `true` 時所建立的快照中。暫時設定則不會包含在內。ISM 政策儲存在 `.opendistro-ism-config` 索引中，而不是叢集狀態中，因此快照只有在包含該索引時才會包含這些政策。如需更多資訊，請參閱[全域叢集狀態]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#global-cluster-state)。

這些設定僅適用於 ISM 工作。執行 ISM 工作的 Job Scheduler 外掛程式有另外的設定，適用於所有外掛程式的排程工作。如需更多資訊，請參閱[排程工作設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/scheduled-jobs/index/#scheduled-job-settings)。

設定 | 預設值 | 說明
:--- | :--- | :---
`plugins.index_state_management.enabled` | True | 指定是否啟用 ISM。
`plugins.index_state_management.job_interval` | 5 | 受管理索引工作執行的間隔時間 (以分鐘為單位)。
`plugins.index_state_management.jitter` | 0.6 | 加入工作基本執行時間的隨機延遲，以避免所有索引同時產生活動高峰。值為 0.6 表示會在工作間隔中加入 0 至 60% 的延遲。例如，如果基本間隔時間為 30 分鐘，值為 0.6 表示會在工作間隔中加入 0 到 18 分鐘之間的任意時間。最大值為 1，表示額外加入 100% 的間隔時間。此最大值不能超過 `plugins.jobscheduler.jitter_limit`，該設定的預設值也是 0.6。例如，如果 `plugins.index_state_management.jitter` 設為 0.8，ISM 會改用 `plugins.jobscheduler.jitter_limit` 為 0.6。
`plugins.index_state_management.coordinator.sweep_period` | 10m | 例行背景清掃的執行頻率。
`plugins.index_state_management.coordinator.backoff_millis` | 50ms | `ManagedIndexCoordinator` 中發生失敗時 (例如更新受管理索引時) 重試之間的退避時間。
`plugins.index_state_management.coordinator.backoff_count` | 2 | `ManagedIndexCoordinator` 中發生失敗時的重試次數。
`plugins.index_state_management.history.enabled` | True | 指定是否啟用稽核歷程記錄。ISM 產生的記錄會自動編製索引至記錄文件中。
`plugins.index_state_management.history.max_docs` | 2500000 | 稽核歷程記錄索引在輪替之前的最大文件數。
`plugins.index_state_management.history.max_age` | 24h | 稽核歷程記錄索引在輪替之前的最大存在時間。
`plugins.index_state_management.history.rollover_check_period` | 8h | 稽核歷程記錄索引兩次輪替檢查之間的時間。
`plugins.index_state_management.history.rollover_retention_period` | 30d | 稽核歷程記錄索引的保留時間。
`plugins.index_state_management.allow_list` | `alias`, `allocation`, `close`, `convert_index_to_remote`, `delete`, `force_merge`, `index_priority`, `notification`, `open`, `read_only`, `read_write`, `replica_count`, `rollover`, `rollup`, `search_only`, `shrink`, `snapshot`, `stop_replication`, `transform` | 政策可以使用的動作。從此清單中移除某個動作會導致所有使用該動作的政策失敗。
`plugins.index_state_management.action_validation.enabled` | False | 指定 ISM 是否在執行動作前先進行驗證。如需更多資訊，請參閱 [ISM 錯誤預防]({{site.url}}{{site.baseurl}}/im-plugin/ism/error-prevention/index/)。
`plugins.index_state_management.coordinator.sweep_skip_period` | 5m | 協調器在失敗後再次清掃受管理索引之前等待的時間。
`plugins.index_state_management.history.number_of_shards` | 1 | 稽核歷程記錄索引的主要分片數量。
`plugins.index_state_management.history.number_of_replicas` | 1 | 稽核歷程記錄索引的副本數量。
`plugins.index_state_management.snapshot.deny_list` | 空清單 | `snapshot` 動作無法寫入的快照儲存庫。
