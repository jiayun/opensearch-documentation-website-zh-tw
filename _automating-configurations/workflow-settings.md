---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作流程設定"
nav_order: 30
---

# 工作流程設定

下列索引鍵代表可設定的工作流程設定。

|設定	|資料類型	|預設值	|說明	|
|:---	|:---	|:---	|:---	|
|`plugins.flow_framework.enabled`	|布林值	|`false`	|是否啟用 Flow Framework API。	|
|`plugins.flow_framework.max_workflows`	|整數	|`1000`	| 您可以建立的工作流程數量上限。當上限超過 1,000 時，基於效能考量，現有工作流程的數量會定義為下限，因此實際的上限可能會略微超過此值。	|
|`plugins.flow_framework.max_workflow_steps`	|整數	|`50`	|一個工作流程可包含的步驟數量上限。	|
|`plugins.flow_framework.request_timeout`	|時間單位	|`10s`	|REST 請求的預設逾時時間，適用於內部搜尋查詢。	|
|`plugins.flow_framework.task_request_retry_duration`	|時間單位	|`5s`	| 當步驟對應到會產生 `task_id` 的 API 時，OpenSearch 會以此間隔重試這些步驟，直到完成為止。	|
|`plugins.flow_framework.workflow_thread_pool_size`	|整數	|`4`	|用於輪詢重試的工作流程執行緒集區大小上限。 |
|`plugins.flow_framework.provision_thread_pool_size`	|整數	|`8`	|佈建工作流程執行緒集區的大小上限。 |
|`plugins.flow_framework.deprovision_thread_pool_size`	|整數	|`4`	|取消佈建工作流程執行緒集區的大小上限。 |
