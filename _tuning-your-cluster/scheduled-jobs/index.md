---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "排程工作"
nav_order: 65
has_children: true
has_toc: false
redirect_from:
  - /tuning-your-cluster/scheduled-jobs/
---

# 排程工作

大多數會依排程執行工作的 OpenSearch 外掛程式，都會使用 Job Scheduler 外掛程式來執行這些工作。例如，Index State Management 使用排程工作將政策套用到索引，快照管理使用排程工作建立與刪除快照，異常偵測使用排程工作執行偵測器，而報告功能則使用排程工作產生排程報告。

警示監視器不使用 Job Scheduler。Alerting 外掛程式使用自己的排程器執行監視器，該排程器是透過 `plugins.scheduled_jobs.*` 設定進行設定。如需詳細資訊，請參閱[警示設定]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/settings/)。

Job Scheduler 會將每個工作儲存在建立該工作的外掛程式的工作索引中。背景掃描會定期搜尋這些索引，找出要排程的工作。為了確保整個叢集中同一時間只有一個工作執行個體在執行，Job Scheduler 會在執行工作前先取得鎖定。

## 監視排程工作

如果排程工作（例如 Index State Management 政策或快照政策）停止執行，請使用下列 API 檢視其工作的狀態：

- [Jobs API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/scheduled-jobs/jobs/) 會列出叢集上的工作，並顯示每個工作是否已啟用及排程。
- [Locks API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/scheduled-jobs/locks/) 會列出工作目前持有的鎖定。

## 排程工作設定

Job Scheduler 支援下列設定。所有設定皆為動態設定。如需動態設定的詳細資訊，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

設定 | 資料類型 | 說明
:--- | :--- | :---
`plugins.jobscheduler.jitter_limit` | Double | Job Scheduler 隨機延遲每次工作執行時間的最大比例（相對於工作的間隔）。隨機延遲可避免許多工作同時啟動並一起耗用資源。例如，如果某個工作每 10 分鐘執行一次，且抖動上限為 `0.6`，則每次執行會隨機延遲 0 到 6 分鐘。預設值為 `0.6`。
`plugins.jobscheduler.sweeper.period` | 時間單位 | 背景掃描搜尋工作索引以找出要排程工作的間隔。預設值為 `5m`。
`plugins.jobscheduler.sweeper.page_size` | 整數 | 背景掃描在每次搜尋請求中擷取的工作數量。預設值為 `100`。
`plugins.jobscheduler.request_timeout` | 時間單位 | 背景掃描傳送至工作索引之搜尋請求的逾時時間。預設值為 `10s`。
`plugins.jobscheduler.retry_count` | 整數 | 背景掃描重試工作索引搜尋失敗的次數。預設值為 `3`。
`plugins.jobscheduler.sweeper.backoff_millis` | 時間單位 | 背景掃描重試工作索引搜尋失敗前的初始等待時間。等待時間會隨著每次重試呈指數增加。預設值為 `50ms`。
`plugins.jobscheduler.sweeper.orphan_reconciliation.enabled` | 布林值 | 背景掃描是否停止工作文件已遭刪除的工作。在使用[遠端後端儲存空間]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/index/)的叢集中，儲存工作索引副本的節點不會偵測到文件刪除，因此已刪除的工作可能會在該節點上繼續執行。例如，Index State Management 政策在您從索引中移除後，可能仍會繼續執行。在設定為遠端後端儲存空間的節點上，預設值為 `true`；在所有其他節點上，預設值為 `false`。

## 相關文件

- [Job Scheduler]({{site.url}}{{site.baseurl}}/developer-documentation/job-scheduler/index/)：建置使用 Job Scheduler 排程工作的外掛程式。
