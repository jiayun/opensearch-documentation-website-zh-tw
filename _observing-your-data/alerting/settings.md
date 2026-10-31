---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "警示設定"
parent: Alerting
nav_order: 70
redirect_from:
  - /monitoring-plugins/alerting/settings/
---

# 警示設定

下列各節說明警示索引與設定。

## 警示索引

警示功能會建立數個索引和一個別名。Security 外掛程式的示範指令碼會將它們設定為[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)，以提供額外一層保護。請勿在未使用警示 API 的情況下刪除這些索引或修改其內容。

索引 | 用途
:--- | :---
`.opendistro-alerting-alerts` | 儲存進行中的警示。
`.opendistro-alerting-alert-history-<date>` | 儲存已完成警示的歷程記錄。
`.opendistro-alerting-config` | 儲存監視器、觸發條件及目的地。為此索引[建立快照]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore/)，以備份您的警示組態。
`.opendistro-alerting-alert-history-write`（別名） | 為 `.opendistro-alerting-alert-history-<date>` 索引提供一致的 URI。

所有警示索引預設皆為隱藏。若要查看摘要，請提出下列請求：

```json
GET _cat/indices?expand_wildcards=open,hidden
```
{% include copy-curl.html %}

## 設定

我們不建議變更這些設定；預設值應能滿足大多數使用案例的需求。

所有設定皆可透過 OpenSearch `_cluster/settings` API 使用。這些設定皆不需要重新啟動，且皆可標記為 `persistent` 或 `transient`。若要進一步瞭解靜態與動態設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

OpenSearch 支援下列警示設定：

- `plugins.scheduled_jobs.enabled`（動態，布林值）：是否啟用 Alerting 外掛程式。若停用，所有監視器會立即停止執行。預設值為 `true`。

- `plugins.alerting.index_timeout`（動態，時間單位）：使用 REST API 建立監視器與目的地的逾時時間。預設值為 `60s`。

- `plugins.alerting.request_timeout`（動態，時間單位）：外掛程式發出的其他請求的逾時時間。預設值為 `10s`。

- `plugins.alerting.action_throttle_max_value`（動態，時間單位）：您可為動作節流設定的最長時間。依預設，此值在 OpenSearch Dashboards 中顯示為 1440 分鐘。預設值為 `24h`。

- `plugins.alerting.input_timeout`（動態，時間單位）：監視器可用於發出搜尋請求的時間長度。預設值為 `30s`。

- `plugins.alerting.bulk_timeout`（動態，時間單位）：監視器可用於將警示寫入警示索引的時間長度。預設值為 `120s`。

- `plugins.alerting.alert_backoff_count`（動態，整數）：寫入警示時，在判定作業失敗前的重試次數。預設值為 `2`。

- `plugins.alerting.alert_backoff_millis`（動態，時間單位）：重試之間的等待時間，每次重試失敗後皆以指數方式增加。預設值為 `50ms`。

- `plugins.alerting.alert_history_rollover_period`（動態，時間單位）：檢查 `.opendistro-alerting-alert-history-write` 別名是否應輪替至新的歷程索引，以及 Alerting 外掛程式是否應刪除任何歷程索引的頻率。預設值為 `12h`。

- `plugins.alerting.move_alerts_backoff_millis`（動態，時間單位）：重試之間的等待時間，每次重試失敗後皆以指數方式增加。預設值為 `250ms`。

- `plugins.alerting.move_alerts_backoff_count`（動態，整數）：監視器或觸發條件刪除後，將其警示移至已刪除狀態的重試次數。預設值為 `3`。

- `plugins.alerting.monitor.max_monitors`（動態，整數）：使用者可建立的監視器數量上限。預設值為 `1000`。

- `plugins.alerting.alert_history_max_age`（動態，時間單位）：建立新索引之前，`.opendistro-alert-history-<date>` 索引中儲存的文件所允許的最長存留時間。若此期間的警示數量未超過 `alert_history_max_docs`，警示功能會在每個期間建立一個歷程索引（例如，每 30 天建立一個索引）。預設值為 `30d`。

- `plugins.alerting.alert_history_max_docs`（動態，長整數）：建立新索引之前，`.opendistro-alert-history-<date>` 索引中可儲存的警示數量上限。預設值為 `1000`。

- `plugins.alerting.alert_history_enabled`（動態，布林值）：是否建立 `.opendistro-alerting-alert-history-<date>` 索引。預設值為 `true`。

- `plugins.alerting.alert_history_retention_period`（動態，時間單位）：自動刪除歷程索引之前的儲存時間。預設值為 `60d`。

- `plugins.alerting.destination.allow_list`（動態，清單）：允許的目的地清單。若您不想允許使用者使用某種目的地類型，可以將其從此清單中移除，但我們建議保留此設定的原始值。預設值為 `["chime", "slack", "custom_webhook", "email", "test_action"]`。

- `plugins.alerting.filter_by_backend_roles`（動態，布林值）：依後端角色限制監視器的存取權。請參閱[警示安全性]({{site.url}}{{site.baseurl}}/monitoring-plugins/alerting/security/)。預設值為 `false`。

- `plugins.alerting.filter_by_backend_roles_access_strategy`（動態，字串）：控制如何比較使用者的後端角色與監視器相關聯的後端角色，以判斷使用者是否可存取該監視器。有效值為 `all`、`exact` 及 `intersect`。請參閱[警示安全性文件中有關依後端角色篩選的說明]({{site.url}}{{site.baseurl}}/monitoring-plugins/alerting/security/#advanced-limit-access-by-backend-role)。預設值為 `intersect`。

- `plugins.alerting.cross_cluster_monitoring_enabled`（動態，布林值）：切換叢集指標監視器是否支援針對遠端叢集執行。預設值為 `true`。

- `plugins.scheduled_jobs.sweeper.period`（動態，時間單位）：警示功能使用其「作業掃描器」元件定期檢查新增或更新的作業。此設定指定掃描器檢查是否有任何作業（監視器）已變更且需要重新排程的頻率。預設值為 `5m`。

- `plugins.scheduled_jobs.sweeper.page_size`（動態，整數）：掃描器的分頁大小。您應該不需要變更此值。預設值為 `100`。

- `plugins.scheduled_jobs.sweeper.backoff_millis`（動態，時間單位）：掃描器在重試之間的等待時間，每次重試失敗後皆以指數方式增加。預設值為 `50ms`。

- `plugins.scheduled_jobs.retry_count`（動態，整數）：掃描器在擲回錯誤之前應重試的總次數。預設值為 `3`。

- `plugins.scheduled_jobs.request_timeout`（動態，時間單位）：掃描分片以尋找作業的請求逾時時間。預設值為 `10s`。

- `plugins.alerting.comments_enabled`（動態，布林值）：啟用或停用 Alerting 外掛程式的留言功能。預設值為 `true`。

- `plugins.alerting.comments_history_max_docs`（動態，長整數）：建立新索引之前，`.opensearch-alerting-comments-history-<date>` 索引中可儲存的留言數量上限。預設值為 `1000`。

- `plugins.alerting.comments_history_max_age`（動態，時間單位）：建立新索引之前，`.opensearch-alerting-comments-history-<date>` 索引中儲存的文件所允許的最長存留時間。若指定期間的留言數量未超過 `comments_history_max_docs`，則每個期間會建立 1 個索引（例如，每 30 天建立 1 個）。預設值為 `30d`。

- `plugins.alerting.comments_history_rollover_period`（動態，時間單位）：判斷 `.opensearch-alerting-comments-history-write` 別名是否應輪替至新索引，以及是否應刪除舊留言歷程索引的頻率。預設值為 `12h`。

- `plugins.alerting.comments_history_retention_period`（動態，時間單位）：自動刪除留言歷程索引之前的保留時間。預設值為 `60d`。

- `plugins.alerting.max_comment_character_length`（動態，長整數）：留言的字元數上限。預設值為 `2000`。

- `plugins.alerting.max_comments_per_alert`（動態，長整數）：可在單一警示上張貼的留言數量上限。預設值為 `500`。

- `plugins.alerting.max_comments_per_notification`（動態，整數）：警示通知的 `ctx` Mustache 範本變數中，每個警示可包含的留言數量上限。預設值為 `3`。

### PPL 監視器設定

如需 PPL 監視器設定的資訊，請參閱 [PPL 監視器設定]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/ppl-monitors/)。