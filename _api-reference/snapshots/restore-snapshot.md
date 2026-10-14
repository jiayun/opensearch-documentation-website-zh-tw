---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "還原快照"
parent: Snapshot APIs
nav_order: 90
---

# Restore Snapshot API
**於 1.0 推出**
{: .label .label-purple }

還原叢集或指定資料串流與索引的快照。

如果您要還原的同名開放索引已存在於叢集中，您必須關閉、刪除或重新命名這些索引。您只能在已關閉的索引與快照中的索引具有相同分片數時，才可還原覆蓋該索引；還原操作會重新開啟該索引。如需重新命名索引的資訊，請參閱[範例請求](#example-requests)。如需關閉索引的資訊，請參閱[關閉索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/close-index/)。若要將快照還原至不同的叢集，請參閱[還原至不同的叢集]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#restoring-a-snapshot-to-a-different-cluster)。如需避免衝突的詳細資訊，請參閱[衝突與相容性]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#conflicts-and-compatibility)。
{: .note}

## 端點

```json
POST _snapshot/{repository}/{snapshot}/_restore
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `repository` | 字串 | 包含要還原之快照的儲存庫。 |
| `snapshot` | 字串 | 要還原的快照。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `wait_for_completion` | 布林值 | 是否在傳回回應前等待還原操作完成。若為 `false`，請求會在還原操作開始時傳回 `{"accepted": true}`。若為 `true`，請求會在還原操作完成後傳回包含已還原索引與分片計數的回應。預設為 `false`。 |

## 請求本文欄位

下表列出可用的請求本文欄位。所有請求本文欄位皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `attach_to_data_stream`（實驗性） | 布林值 | 是否將已還原的後端索引附加至同名的既有資料串流。當為 `true` 時，名稱符合 `.ds-<data_stream>-NNNNNN` 後端索引慣例的已還原索引，會在還原操作期間附加至同名的既有資料串流，並視需要推進串流世代。附加的索引必須將資料串流的時間戳記欄位對應為 `date`。當為 `false` 時，索引會還原為獨立索引。預設為 `false`。請參閱[將已還原的後端索引附加至資料串流](#attach-a-restored-backing-index-to-a-data-stream)。|
| `ignore_unavailable` | 布林值 | 如何處理遺失或已關閉的資料串流或索引。若為 `false`，請求會對任何遺失或已關閉的資料串流或索引傳回錯誤。若為 `true`，請求會忽略遺失或已關閉的資料串流與索引。預設為 `false`。 |
| `ignore_index_settings` | 字串或字串陣列 | 從快照還原時要排除的索引設定。排除的設定會重設為其預設值。請指定以逗號分隔的字串或字串陣列。某些設定（例如 `index.number_of_replicas`）無法排除。若要變更它們，請使用 `index_settings`。 |
| `include_aliases` | 布林值 | 如何處理原始快照中的索引別名。若為 `true`，會還原原始快照中的索引別名。若為 `false`，索引會在不含其別名的情況下還原。預設為 `true`。 |
| `include_global_state` | 布林值 | 是否還原儲存在快照中的叢集狀態<sup>1</sup>。當為 `true` 時，快照叢集狀態中的項目會取代叢集中同名的既有項目。預設為 `false`。|
| `index_settings` | 物件 | 包含要在所有已還原索引中新增或變更之設定的物件，例如 `{"index.number_of_replicas": 0}`。使用此參數可在快照還原期間覆寫索引設定。對於資料串流，這些索引設定會套用至已還原的後端索引。某些設定（例如 `index.number_of_shards`）無法在還原期間變更。 |
| `indices` | 字串 | 要從快照還原的資料串流與索引的逗號分隔清單。支援多重索引語法。根據預設，還原操作會包含快照中的所有資料串流與索引。若提供此引數，還原操作只會包含您指定的資料串流與索引。 |
| `partial` | 布林值 | 若快照中的索引未具備所有主要分片時，還原操作的行為。若為 `false`，當快照中的任何索引未具備所有主要分片時，整個還原操作會失敗。<br /> <br />若為 `true`，允許還原具有無法使用分片之索引的部分快照。只會還原成功包含在快照中的分片。所有遺失的分片會重新建立為空。預設為 `false`。 |
| `rename_pattern` | 字串 | 要套用至已還原資料串流與索引的模式。符合重新命名模式的資料串流與索引，會根據 `rename_replacement` 設定重新命名。<br /><br /> 重新命名模式是規則運算式。在 `rename_replacement` 中，使用 `$1`、`$2` 等來參照模式所擷取的群組，如 [Java `Matcher` 文件](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/regex/Matcher.html#appendReplacement(java.lang.StringBuilder,java.lang.String))所述。<br /> <br /> 若兩個或多個資料串流或索引重新命名為相同名稱，請求會失敗。若您重新命名已還原的資料串流，其後端索引也會一併重新命名。例如，若您將 logs 資料串流重新命名為 `recovered-logs`，後端索引 `.ds-logs-1` 會重新命名為 `.ds-recovered-logs-1`。<br /> <br /> 若您重新命名已還原的串流，請確保索引範本符合新的串流名稱。若沒有相符的索引範本名稱，串流就無法輪替，且不會建立新的後端索引。|
| `rename_replacement` | 字串 | 重新命名的取代字串。|
| `rename_alias_pattern` | 字串 | 要套用至已還原別名的模式。符合重新命名模式的別名會根據 `rename_alias_replacement` 設定重新命名。<br /><br /> 重新命名模式是規則運算式。在 `rename_alias_replacement` 中，使用 `$1`、`$2` 等來參照模式所擷取的群組。<br /> <br /> 若兩個或多個別名重新命名為相同名稱，這些別名會合併為一個。|
| `rename_alias_replacement` | 字串 | 別名重新命名的取代字串。|
| `source_remote_store_repository` | 字串 | 正在還原之來源索引的遠端分段儲存庫名稱。僅當來源與目標叢集皆使用以遠端儲存作為後端的儲存方式，且具有不同的遠端儲存庫時才需要。指定的儲存庫必須在還原前於目標叢集上註冊為唯讀。若未提供，Snapshot Restore API 會使用建立快照時所註冊的儲存庫。 |
| `source_remote_translog_repository` | 字串 | 正在還原之來源索引的遠端交易記錄儲存庫名稱。僅當來源與目標叢集皆使用以遠端儲存作為後端的儲存方式，且具有不同的遠端儲存庫時才需要。指定的儲存庫必須在還原前於目標叢集上註冊為唯讀。 |
| `storage_type` | 字串 | 已還原索引資料的儲存位置。有效值為：<br> - `local`：所有索引資料與快照中繼資料都會下載至本機儲存空間。<br> - `remote_snapshot`：快照中繼資料會下載至叢集，但遠端儲存庫仍是索引資料的權威存放區。資料會視需要下載並快取，以處理查詢。叢集中至少有一個節點必須具有 [`warm` 角色]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/searchable_snapshot/#configuring-a-node-to-use-searchable-snapshots)，才能使用 `remote_snapshot` 類型還原快照。<br><br>預設為 `local`。 |

<sup>1</sup>叢集狀態包含下列項目。當您還原叢集狀態時，這些項目會取代叢集中同名的既有項目：
* 持續性叢集設定
* 索引範本
* 舊版索引範本
* 資料匯入管線

索引狀態管理 (ISM) 原則儲存在索引中，而非叢集狀態中，因此不會隨叢集狀態一併還原。

## 請求範例

下列範例示範不同的快照還原情境。

### 基本還原

下列請求會從 `my-first-snapshot` 還原 `restore-test` 索引。`rename_pattern` 與 `rename_replacement` 的組合會將索引重新命名為 `restore-test_restored`，因為叢集中不允許有名稱重複的開啟索引。

<!-- spec_insert_start
component: example_code
rest: POST /_snapshot/my-opensearch-repo/my-first-snapshot/_restore
body: |
{
  "indices": "restore-test",
  "ignore_unavailable": true,
  "include_global_state": false,
  "rename_pattern": "(.+)",
  "rename_replacement": "$1_restored",
  "include_aliases": false
}
-->
{% capture step1_rest %}
POST /_snapshot/my-opensearch-repo/my-first-snapshot/_restore
{
  "indices": "restore-test",
  "ignore_unavailable": true,
  "include_global_state": false,
  "rename_pattern": "(.+)",
  "rename_replacement": "$1_restored",
  "include_aliases": false
}
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.restore(
  repository = "my-opensearch-repo",
  snapshot = "my-first-snapshot",
  body =   {
    "indices": "restore-test",
    "ignore_unavailable": true,
    "include_global_state": false,
    "rename_pattern": "(.+)",
    "rename_replacement": "$1_restored",
    "include_aliases": false
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 在還原期間變更索引設定

下列請求會將 `restore-test` 索引還原為名稱 `restore-test-settings`，將副本數量設為 `0`，並將 `index.refresh_interval` 設定重設為預設值。將快照還原至較小的叢集時，減少副本數量很有用：

```json
POST /_snapshot/my-opensearch-repo/my-first-snapshot/_restore?wait_for_completion=true
{
  "indices": "restore-test",
  "rename_pattern": "(.+)",
  "rename_replacement": "$1-settings",
  "index_settings": {
    "index.number_of_replicas": 0
  },
  "ignore_index_settings": [
    "index.refresh_interval"
  ]
}
```
{% include copy-curl.html %}

### 使用遠端儲存作為後端的跨叢集還原

以遠端儲存作為後端的儲存方式是一項讓 OpenSearch 自動將分段和交易記錄備份至遠端儲存庫的功能。在**皆使用以遠端儲存作為後端的儲存方式**且使用不同遠端儲存庫的叢集之間還原快照時，請同時使用 `source_remote_store_repository` 和 `source_remote_translog_repository` 參數。 

下列範例會將來源叢集上建立的快照中的索引還原至目標叢集。在此範例中，`source-cluster-snapshots` 是包含來源叢集快照的快照儲存庫，`snapshot-1` 是快照名稱，`my-remote-index` 是要還原的索引，`source-remote-segment-repo` 是來源叢集的遠端分段儲存庫（必須在目標叢集上註冊為唯讀），而 `source-remote-translog-repo` 是來源叢集的遠端交易記錄儲存庫（必須在目標叢集上註冊為唯讀）：

<!-- spec_insert_start
component: example_code
rest: POST /_snapshot/source-cluster-snapshots/snapshot-1/_restore
body: |
{
  "indices": "my-remote-index",
  "source_remote_store_repository": "source-remote-segment-repo",
  "source_remote_translog_repository": "source-remote-translog-repo"
}
-->
{% capture step1_rest %}
POST /_snapshot/source-cluster-snapshots/snapshot-1/_restore
{
  "indices": "my-remote-index",
  "source_remote_store_repository": "source-remote-segment-repo",
  "source_remote_translog_repository": "source-remote-translog-repo"
}
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.restore(
  repository = "source-cluster-snapshots",
  snapshot = "snapshot-1",
  body =   {
    "indices": "my-remote-index",
    "source_remote_store_repository": "source-remote-segment-repo",
    "source_remote_translog_repository": "source-remote-translog-repo"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

目標叢集會還原索引，並將其設定為從來源叢集的遠端儲存庫讀取遠端分段和交易記錄。

如需完整的逐步操作程序，請參閱[在以遠端儲存作為後端的叢集之間還原快照]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#restoring-snapshots-across-remote-backed-clusters)。

### 將還原的後端索引附加至資料串流
**於 3.8 推出**
{: .label .label-purple }

這是一項實驗性功能，不建議在正式環境中使用。如需此功能的最新進度，或想提供意見回饋，請參閱相關的 [GitHub 議題](https://github.com/opensearch-project/OpenSearch/issues/8271)。
{: .warning}

若要將還原的後端索引附加至同名的既有資料串流，請將 `attach_to_data_stream` 設為 `true`。還原的索引名稱必須符合 `.ds-<data_stream>-NNNNNN` 後端索引命名慣例，而且索引必須將串流的時間戳記欄位對應為 `date`。下列請求會還原 `.ds-logs-foo-000001` 後端索引，並將其附加至既有的 `logs-foo` 資料串流，視需要遞增串流世代：

```json
POST /_snapshot/my-opensearch-repo/my-first-snapshot/_restore
{
  "indices": ".ds-logs-foo-000001",
  "attach_to_data_stream": true
}
```
{% include copy-curl.html %}

若要新增或移除資料串流的後端索引，而不從快照還原索引，請使用 [Modify Data Stream API]({{site.url}}{{site.baseurl}}/api-reference/data-stream/modify-data-stream/)。

## 回應範例

依預設，請求會在還原作業開始時傳回下列回應：

```json
{
  "accepted": true
}
```

如果您將 `wait_for_completion` 設為 `true`，請求會在還原作業完成後傳回回應。[在還原期間變更索引設定](#change-index-settings-during-restore)範例會傳回下列回應：

```json
{
  "snapshot": {
    "snapshot": "my-first-snapshot",
    "indices": [
      "restore-test-settings"
    ],
    "shards": {
      "total": 1,
      "failed": 0,
      "successful": 1
    }
  }
}
```

若要檢視完整的快照詳細資訊，例如其中包含的所有索引，請使用 [Get Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot/)。

若要監控還原作業的進度，請使用 [CAT Recovery API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-recovery/)。正在從快照還原的分片，其復原類型為 `snapshot`：

```json
GET _cat/recovery/restore-test-settings?v&h=index,shard,type,stage,snapshot,repository,files_percent,bytes_percent
```
{% include copy-curl.html %}

回應會顯示每個分片還原所用的快照和儲存庫，以及目前已還原的檔案和位元組百分比：

```
index                 shard type     stage snapshot          repository         files_percent bytes_percent
restore-test-settings 0     snapshot done  my-first-snapshot my-opensearch-repo 100.0%        100.0%
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `accepted` | 布林值 | 當 `wait_for_completion` 為 `false` 時，會傳回此欄位，而非 `snapshot` 物件。表示還原作業已開始。 |
| `snapshot.snapshot` | 字串 | 快照名稱。 |
| `snapshot.indices` | 陣列 | 經過任何重新命名後，已還原索引的名稱。 |
| `snapshot.shards` | 物件 | 已還原分片的總數，以及成功與失敗的分片數。 |

若叢集中已有與快照中索引同名的開啟索引，且您未刪除、關閉或重新命名這些索引，API 會傳回類似下列內容的錯誤：

```json
{
  "error" : {
    "root_cause" : [
      {
        "type" : "snapshot_restore_exception",
        "reason" : "[my-opensearch-repo:my-first-snapshot/DdQp-ksUQ66Vd4H9S2fyKw] cannot restore index [restore-test] because an open index with same name already exists in the cluster. Either close or delete the existing index or restore the index under a different name by providing a rename pattern and replacement name"
      }
    ],
    "type" : "snapshot_restore_exception",
    "reason" : "[my-opensearch-repo:my-first-snapshot/DdQp-ksUQ66Vd4H9S2fyKw] cannot restore index [restore-test] because an open index with same name already exists in the cluster. Either close or delete the existing index or restore the index under a different name by providing a rename pattern and replacement name"
  },
  "status" : 500
}
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:admin/snapshot/restore`。
