---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "監視器"
nav_order: 10
parent: Alerting
has_children: true
redirect_from:
  - /monitoring-plugins/alerting/monitors/
---

# 警示監視器

監視器是一項依排程執行的工作，會查詢您的資料或叢集，並將結果傳遞給其觸發條件。當觸發條件符合時，監視器會產生警示，並可執行傳送通知等動作。本頁說明監視器類型、如何排程監視器，以及觸發條件與動作訊息中可用的變數。

若要從異常偵測結果產生警示，請使用 **Anomaly detector** 定義方法建立每次查詢監視器。如需詳細資訊，請參閱[每次查詢與每個桶監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/per-query-bucket-monitors/)。

## 監視器類型

警示功能提供下列監視器類型。

監視器類型 | 說明
:--- | :---
[每查詢監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/per-query-bucket-monitors/) (Per query monitor) | 執行查詢，並根據查詢結果產生警示。
[每桶監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/per-query-bucket-monitors/) (Per bucket monitor) | 執行查詢，根據資料集中的彙總值評估觸發條件。
[PPL 監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/ppl-monitors/) (PPL monitor) | 執行 Piped Processing Language (PPL) 查詢，並根據結果數量或自訂條件產生警示。
[每叢集指標監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/per-cluster-metrics-monitors/) (Per cluster metrics monitor) | 在叢集上執行 API 請求，以監控其健康狀態。
[每文件監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/per-document-monitors/) (Per document monitor) | 執行查詢（或多個以標籤組合的查詢），傳回符合觸發條件的個別文件。
[複合監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/composite-monitors/) (Composite monitor) | 在單一工作流程中執行多個監視器，並根據多個觸發條件產生單一警示。

預設情況下，您最多可以建立 1,000 個監視器。若要變更此限制，請使用 [Cluster Settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) 更新 `plugins.alerting.monitor.max_monitors` 設定。如需更多資訊，請參閱 [警示設定]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/settings/)。
{: .tip}

## 監視器排程

監視器會以固定間隔執行，例如每小時或每天，或依您以 cron 運算式定義的排程執行。當間隔無法描述您需要監視器執行的時間時（例如每個平日 11:30 AM），請使用 cron 運算式。關於語法，請參閱[Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/cron-expressions/)。

關於使用 cron 運算式的監視器，請參閱[建立查詢層級監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/api/#example-request-2)。

## 監視器變數

下表列出可用於自訂監視器的變數。

變數 | 資料類型 | 說明
:--- | :--- | :---
`ctx.monitor` | 物件 | 包含 `ctx.monitor.name`、`ctx.monitor.type`、`ctx.monitor.enabled`、`ctx.monitor.enabled_time`、`ctx.monitor.schedule`、`ctx.monitor.inputs`、`triggers` 及 `ctx.monitor.last_update_time`。
`ctx.monitor.user` | 物件 | 包含建立監視器之使用者的相關資訊。包含 `ctx.monitor.user.backend_roles` 及 `ctx.monitor.user.roles`，兩者為陣列，內含指派給該使用者的後端角色與角色。如需詳細資訊，請參閱[警示安全性]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/security/)。
`ctx.monitor.enabled` | 布林值 | 監視器是否已啟用。
`ctx.monitor.enabled_time` | 毫秒 | 監視器上次啟用的 Unix epoch 時間。
`ctx.monitor.schedule` | 物件 | 包含監視器應執行的頻率或時間排程。
`ctx.monitor.schedule.period.interval` | 整數 | 監視器執行的間隔。
`ctx.monitor.schedule.period.unit` | 字串 | 間隔的時間單位。
`ctx.monitor.inputs` | 陣列 | 陣列，包含用於建立監視器的索引與定義。
`ctx.monitor.inputs.search.indices` | 陣列 | 陣列，包含監視器所觀察的索引。
`ctx.monitor.inputs.search.query` | 物件 | 監視器執行的查詢。

下表列出可與監視器搭配使用的其他變數。

變數 | 資料類型 | 說明
:--- | :--- | :---
`ctx.results` | 陣列 | 僅含一個元素的陣列，例如 `ctx.results[0]`。包含查詢結果。若觸發條件無法擷取結果，此變數為空。請參閱 `ctx.error`。
`ctx.last_update_time` | 毫秒 | 監視器上次更新的 Unix epoch 時間。
`ctx.periodStart` | 字串 | 警示觸發期間開始時間的 Unix 時間戳記。例如，若監視器每 10 分鐘執行一次，期間可能從 10:40 開始，並於 10:50 結束。
`ctx.periodEnd` | 字串 | 警示觸發期間的結束時間。
`ctx.error` | 字串 | 若觸發條件無法擷取結果或無法評估觸發條件時的錯誤訊息，通常是因為編譯錯誤或空指標例外。否則為 Null。
`ctx.alert` | 物件 | 目前作用中的警示（若存在）。包含 `ctx.alert.id`、`ctx.alert.version` 及 `ctx.alert.isAcknowledged`。若無作用中的警示則為 Null。僅適用於查詢層級監視器。
`ctx.dedupedAlerts` | 物件 | 已觸發的警示。OpenSearch 會保留現有警示，以避免監視器重複建立相同的警示。僅適用於桶層級監視器。
`ctx.newAlerts` | 物件 | 新建立的警示。僅適用於桶層級監視器。
`ctx.completedAlerts` | 物件 | 已不再持續的警示。僅適用於桶層級監視器。
`bucket_keys` | 字串 | 以逗號分隔的監視器桶索引鍵值清單。僅適用於 `ctx.dedupedAlerts`、`ctx.newAlerts` 及 `ctx.completedAlerts`。透過 `ctx.dedupedAlerts[0].bucket_keys` 存取。
`parent_bucket_path` | 字串 | 觸發警示之桶的父桶路徑。透過 `ctx.dedupedAlerts[0].parent_bucket_path` 存取。

