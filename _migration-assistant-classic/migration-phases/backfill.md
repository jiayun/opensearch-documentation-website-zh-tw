---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "回填"
nav_order: 6
parent: Migration phases
permalink: /classic/migration-assistant/migration-phases/backfill/
---

# 使用回填

遷移叢集的[中繼資料]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/)後，您可以使用 Capture Proxy 資料複寫與快照，將資料回填至下一個叢集。

## 使用 RFS 遷移文件

您現在可以使用 RFS 從原始叢集遷移文件：

### 啟動回填

若要透過 RFS 啟動遷移，請使用下列命令啟動 `backfill`：

```bash
console backfill start
```
{% include copy.html %}

即使所有分片都已遷移，狀態仍會是 `Running`。

### 擴增工作節點群

_（選用）_ 若要加快遷移速度，請使用下列命令增加同時處理的文件數量：

```bash
console backfill scale <NUM_WORKERS>
```
{% include copy.html %}

若要加快傳輸速度，您可以增加工作節點的數量。這些額外的工作節點可能需要幾分鐘才會上線。下列命令會將工作節點群的規模更新為 10：

```shell
console backfill scale 5
```
{% include copy.html %}

我們建議您逐步擴增工作節點群，同時監控目標叢集的健康狀態指標，以避免使其過度飽和。[Amazon OpenSearch Service 網域](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/monitoring.html)提供多種指標與記錄檔，可用於此類監控。

### 監控回填

若要檢查文件回填的狀態，請使用下列命令：

```bash
console backfill status
```
{% include copy.html %}

使用下列命令詳細監控回填程序：

```bash
console backfill status --deep-check
```
{% include copy.html %}

您應該會收到下列輸出：

```json
BackfillStatus.RUNNING
Running=9
Pending=1
Desired=10
Shards total: 62
Shards completed: 46
Shards incomplete: 16
Shards in progress: 11
Shards unclaimed: 5
```

您可以在 Amazon CloudWatch 的 `OpenSearchMigrations` 記錄檔群組中取得記錄檔與指標。

如果您需要停止回填程序，請使用下列命令：

```bash
console backfill stop
```
{% include copy.html %}

### 暫停遷移

若要暫停遷移，請使用下列命令：

```shell
console backfill pause
```

這會停止所有現有工作節點的執行，同時讓回填作業維持在可重新啟動的狀態。當您想要重新啟動遷移時，請執行下列其中一項操作：

- 執行 `console backfill start`。
- 執行 `console backfill scale <worker_count>` 以增加工作節點數量。

### 停止遷移

完成回填程序需要手動停止遷移。停止遷移會關閉所有工作節點，並清除所有用於追蹤及協調遷移的中繼資料。當狀態檢查回報您的資料已完全遷移後，您可以使用下列命令停止遷移：

```shell
console backfill stop
```
{% include copy.html %}

Migration Assistant 應該會傳回下列回應：

```shell
Backfill stopped successfully.
Service migration-aws-integ-reindex-from-snapshot set to 0 desired count. Currently 0 running and 5 pending.
Archiving the working state of the backfill operation...
RFS Workers are still running, waiting for them to complete...
Backfill working state archived to: /shared-logs-output/migration-console-default/backfill_working_state/working_state_backup_20241115174822.json
```

您無法重新啟動已停止的遷移。您可以改用 `console backfill pause` 暫停回填程序。

### Amazon CloudWatch 指標與儀表板

Migration Assistant 會建立名為 `MigrationAssistant_ReindexFromSnapshot_Dashboard` 的 Amazon CloudWatch 儀表板，讓您以視覺化方式呈現回填程序的健康狀態與效能。此儀表板會整合回填工作節點的指標；若您遷移至 Amazon OpenSearch Service，也會整合目標叢集的指標。

您可以根據部署 Migration Assistant 的 AWS 區域，在 CloudWatch 主控台中找到回填儀表板。在您從儀表板頂端的下拉式選單選取要遷移至的 OpenSearch 網域之前，目標叢集的指標圖表會維持空白。

## 驗證回填

回填完成且工作節點停止後，請使用 [Refresh API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/refresh/) 與 [Flush API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/flush/) 檢查叢集的內容。下列範例使用主控台 CLI 搭配 Refresh API 來檢查回填狀態：

```shell
console clusters cat-indices --refresh
```
{% include copy.html %}

這會顯示目標叢集中各個索引的文件數量，如下列範例回應所示：

```shell
SOURCE CLUSTER
health status index                uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   my-index             -DqPQDrATw25hhe5Ss34bQ   1   0          3            0     12.7kb         12.7kb

TARGET CLUSTER
health status index                     uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .opensearch-observability 8HOComzdSlSWCwqWIOGRbQ   1   1          0            0       416b           208b
green  open   .plugins-ml-config        9tld-PCJToSUsMiyDhlyhQ   5   1          1            0      9.5kb          4.7kb
green  open   my-index                  bGfGtYoeSU6U6p8leR5NAQ   1   0          3            0      5.5kb          5.5kb
green  open   .migrations_working_state lopd47ReQ9OEhw4ZuJGZOg   1   1          2            0     18.6kb          6.4kb
green  open   .kibana_1
```

您可以對目標叢集執行其他查詢，以模擬正式環境的工作流程，並仔細檢查結果。

## 確認所有文件皆已遷移

在 CloudWatch Logs Insights 中使用下列查詢，找出遷移失敗的文件：

```bash
fields @message
| filter @message like "Bulk request succeeded, but some operations failed."
| sort @timestamp desc
| limit 10000
```
{% include copy.html %}

如果找到任何遷移失敗的文件，您可以直接將這些文件編製索引，而不使用 RFS。

{% include migration-phase-navigation.html %}
