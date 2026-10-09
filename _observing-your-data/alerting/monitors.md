---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "監視器"
nav_order: 1
parent: Alerting
has_children: true
redirect_from:
  - /monitoring-plugins/alerting/monitors/
---

# 警示監視器

使用 Alerting 與 Anomaly Detection 中提供的功能，在 OpenSearch 中主動監視您的資料。例如，您可以將 Anomaly Detection 與 Alerting 搭配使用，確保在偵測到異常時立即收到通知。您可以設定偵測器以自動偵測串流資料中的離群值，並設定監視器以在資料超過特定閾值時透過通知警示您。

## 監視器類型

Alerting 外掛程式提供下列監視器類型：

1. **每次查詢 (per query)**：執行查詢並根據符合條件產生警示通知。關於建立及使用此監視器類型的資訊，請參閱[每次查詢監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/per-query-bucket-monitors/)。
1. **每個桶 (per bucket)**：執行查詢，根據資料集中的彙總值評估觸發條件。關於建立及使用此監視器類型的資訊，請參閱[每個桶監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/per-query-bucket-monitors/)。
1. **PPL**：執行 Piped Processing Language (PPL) 查詢，並根據結果數量或自訂條件產生警示。關於建立及使用此監視器類型的資訊，請參閱[PPL 監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/ppl-monitors/)。
1. **每個叢集指標 (per cluster metrics)**：在叢集上執行 API 請求以監視其健康狀態。關於建立及使用此監視器類型的資訊，請參閱[每個叢集指標監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/per-cluster-metrics-monitors/)。
1. **每份文件 (per document)**：執行查詢（或多個以標籤合併的查詢），傳回符合警示通知觸發條件的個別文件。關於建立及使用此監視器類型的資訊，請參閱[每份文件監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/per-document-monitors/)。
1. **複合監視器 (composite monitor)**：在單一工作流程中執行多個監視器，並根據多個觸發條件產生單一警示。關於建立及使用此監視器類型的資訊，請參閱[複合監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/composite-monitors/)。

您可以建立的監視器數量上限為 1,000 個。您可以使用[叢集設定 API]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/settings/) 更新 `plugins.alerting.monitor.max_monitors` 設定，以變更叢集的預設警示數量上限。
{: .tip}

## 監視器排程

監視器會以固定間隔執行，例如每小時或每天，或依您以 cron 運算式定義的排程執行。當間隔無法描述您需要監視器執行的時間時（例如每個平日 11:30 AM），請使用 cron 運算式。關於語法，請參閱[Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions)。

關於使用 cron 運算式的監視器，請參閱[建立查詢層級監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/api/#example-request-2)。

## 監視器變數

下表列出可用於自訂監視器的變數。

變數 | 資料類型 | 說明
:--- | :--- | :---
`ctx.monitor` | 物件 | 包含 `ctx.monitor.name`、`ctx.monitor.type`、`ctx.monitor.enabled`、`ctx.monitor.enabled_time`、`ctx.monitor.schedule`、`ctx.monitor.inputs`、`triggers` 及 `ctx.monitor.last_update_time`。
`ctx.monitor.user` | 物件 | 包含建立該監視器之使用者的相關資訊。包含 `ctx.monitor.user.backend_roles` 及 `ctx.monitor.user.roles`，這兩者為陣列，內含指派給該使用者的後端角色及角色。如需詳細資訊，請參閱[警示安全性]({{site.url}}{{site.baseurl}}/monitoring-plugins/alerting/security/)。
`ctx.monitor.enabled` | 布林值 | 監視器是否已啟用。
`ctx.monitor.enabled_time` | 毫秒 | 監視器上次啟用時間的 Unix epoch 時間。
`ctx.monitor.schedule` | 物件 | 包含監視器應以何種頻率或於何時執行的排程。
`ctx.monitor.schedule.period.interval` | 整數 | 監視器執行的間隔。
`ctx.monitor.schedule.period.unit` | 字串 | 間隔的時間單位。
`ctx.monitor.inputs` | 陣列 | 包含用於建立監視器之索引及定義的陣列。
`ctx.monitor.inputs.search.indices` | 陣列 | 包含監視器所觀察之索引的陣列。
`ctx.monitor.inputs.search.query` | 不適用 | 用於定義監視器的定義。

下表列出可搭配監視器使用的其他變數。

變數 | 資料類型 | 說明
:--- | :--- | :---
`ctx.results` | 陣列 | 包含一個元素的陣列，例如 `ctx.results[0]`。包含查詢結果。如果觸發條件無法擷取結果，此變數會是空的。請參閱 `ctx.error`。
`ctx.last_update_time` | 毫秒 | 監視器上次更新時間的 Unix epoch 時間。
`ctx.periodStart` | 字串 | 警示觸發期間開始時間的 Unix 時間戳記。例如，如果監視器每 10 分鐘執行一次，期間可能從 10:40 開始，並於 10:50 結束。
`ctx.periodEnd` | 字串 | 警示觸發期間的結束時間。
`ctx.error` | 字串 | 觸發條件無法擷取結果或無法評估觸發條件時的錯誤訊息，通常是由編譯錯誤或 null 指標例外狀況所致。否則為 null。
`ctx.alert` | 物件 | 目前作用中的警示（如果存在）。包含 `ctx.alert.id`、`ctx.alert.version` 及 `ctx.alert.isAcknowledged`。如果沒有作用中的警示，則為 null。僅適用於查詢層級監視器。
`ctx.dedupedAlerts` | 物件 | 已觸發的警示。OpenSearch 會保留現有警示，以防止外掛程式無止盡地建立相同的警示。僅適用於桶層級監視器。
`ctx.newAlerts` | 物件 | 新建立的警示。僅適用於桶層級監視器。
`ctx.completedAlerts` | 物件 | 已不再持續的警示。僅適用於桶層級監視器。
`bucket_keys` | 字串 | 監視器桶索引鍵值的逗號分隔清單。僅適用於 `ctx.dedupedAlerts`、`ctx.newAlerts` 及 `ctx.completedAlerts`。透過 `ctx.dedupedAlerts[0].bucket_keys` 存取。
`parent_bucket_path` | 字串 | 觸發警示之桶的父桶路徑。透過 `ctx.dedupedAlerts[0].parent_bucket_path` 存取。

