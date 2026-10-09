---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安全性分析設定"
nav_order: 100
has_children: false
---

<!-- vale off -->
# 安全性分析設定
<!-- vale on -->

安全性分析外掛程式支援下列設定。此清單中的所有設定都是動態設定：

`plugins.security_analytics.index_timeout`（時間值）：使用 REST API 建立偵測器、發現項目、規則和自訂記錄檔類型的逾時時間。預設為 60 秒。

`plugins.security_analytics.alert_history_enabled`（布林值）：指定是否建立 `.opensearch-sap-<detector_type>-alerts-history-<date>` 索引。預設為 `true`。

`plugins.security_analytics.alert_finding_enabled`（布林值）：指定是否建立 `.opensearch-sap-<detector_type>-findings-<date>` 索引。預設為 `true`。

`plugins.security_analytics.alert_history_rollover_period`（時間值）：指定輪替及刪除警示歷程索引的頻率。預設為 12 小時。

`plugins.security_analytics.alert_finding_rollover_period`（時間值）：指定輪替及刪除發現項目歷程索引的頻率。預設為 12 小時。

`plugins.security_analytics.correlation_history_rollover_period`（時間值）：指定輪替及刪除關聯歷程索引的頻率。預設為 12 小時。

`plugins.security_analytics.alert_history_max_age`（時間值）：建立新索引前，警示歷程索引中儲存的最舊文件所能達到的存留時間。如果此期間的警示數量未超過 `alert_history_max_docs`，則每個期間都會建立一個新的警示歷程索引（例如，每 30 天建立一個索引）。預設為 30 天。

`plugins.security_analytics.finding_history_max_age`（時間值）：建立新索引前，發現項目歷程索引中儲存的最舊文件所能達到的存留時間。如果此期間的發現項目數量未超過 `finding_history_max_docs`，則每個期間都會建立一個新的發現項目歷程索引（例如，每 30 天建立一個索引）。預設為 30 天。

`plugins.security_analytics.correlation_history_max_age`（時間值）：建立新索引前，關聯歷程索引中儲存的最舊文件所能達到的存留時間。如果此期間的關聯數量未超過 `correlation_history_max_docs`，則每個期間都會建立一個新的關聯歷程索引（例如，每 30 天建立一個索引）。預設為 30 天。

`plugins.security_analytics.alert_history_max_docs`（整數）：建立新索引前，警示歷程索引中可儲存的警示數量上限。預設為 1,000。

`plugins.security_analytics.alert_finding_max_docs`（整數）：建立新索引前，發現項目歷程索引中可儲存的發現項目數量上限。預設為 1,000。

`plugins.security_analytics.correlation_history_max_docs`（整數）：建立新索引前，關聯歷程索引中可儲存的關聯數量上限。預設為 1,000。

`plugins.security_analytics.alert_history_retention_period`（時間值）：自動刪除警示歷程索引前的保留時間。預設為 60 天。

`plugins.security_analytics.finding_history_retention_period`（時間值）：自動刪除發現項目歷程索引前的保留時間。預設為 60 天。

`plugins.security_analytics.correlation_history_retention_period`（時間值）：自動刪除關聯歷程索引前的保留時間。預設為 60 天。

`plugins.security_analytics.request_timeout`（時間值）：安全性分析外掛程式傳送至 OpenSearch 其他部分的所有請求的逾時時間。預設為 10 秒。

`plugins.security_analytics.action_throttle_max_value`（時間值）：您可為動作節流設定的時間上限。預設為 24 小時。（此值在 OpenSearch Dashboards 中顯示為 1440 分鐘。）

`plugins.security_analytics.filter_by_backend_roles`（布林值）：設為 `true` 並啟用時，依後端角色限制對偵測器、警示、發現項目和自訂記錄檔類型的存取。預設為 `false`。

`plugins.security_analytics.enable_workflow_usage`（布林值）：支援 Alerting 外掛程式工作流程與安全性分析的整合。決定在安全性分析中建立新的威脅偵測器後，是否為 Alerting 外掛程式產生複合監視器工作流程。設為 `true` 時，會啟用依據相關聯威脅偵測器組態建立的複合監視器工作流程。設為 `false` 時，會停用依據相關聯威脅偵測器組態建立的複合監視器工作流程。預設為 `true`。如需 Alerting 外掛程式工作流程與安全性分析整合的詳細資訊，請參閱[整合的 Alerting 外掛程式工作流程]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/detectors-config/#integrated-alerting-plugin-workflows)。 

`plugins.security_analytics.correlation_time_window`（時間值）：安全性分析會在時間範圍內產生關聯。此設定指定文件必須在何種時間範圍內編製索引至索引中，才能納入同一個關聯。預設為 5 分鐘。

`plugins.security_analytics.mappings.default_schema`（字串）：用於設定安全性分析偵測器欄位對應的預設對應結構描述。預設為 `ecs`。

`plugins.security_analytics.threatintel.tifjob.update_interval`（時間值）：威脅情報功能使用工作執行器定期擷取新的情報饋送。此設定指定執行器擷取及更新這些新情報饋送的頻率。預設為 1440 分鐘。

`plugins.security_analytics.threatintel.tifjob.batch_size`（整數）：在威脅情報饋送資料建立過程中，單一大量請求可匯入的文件數量上限。預設為 10,000。

`plugins.security_analytics.threat_intel_timeout`（時間值）：建立及刪除威脅情報饋送資料的逾時值。預設為 30 秒。

若要進一步瞭解靜態及動態設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。