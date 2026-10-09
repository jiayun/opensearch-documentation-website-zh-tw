---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "還原快照"
parent: Snapshot APIs

nav_order: 9
---

# Restore Snapshot API
**於 1.0 版推出**
{: .label .label-purple }

還原叢集或指定資料串流與索引的快照。 

* 如需索引與叢集的相關資訊，請參閱 [OpenSearch 簡介]({{site.url}}{{site.baseurl}}/opensearch/index/)。

* 如需資料串流的相關資訊，請參閱 [資料串流]({{site.url}}{{site.baseurl}}/opensearch/data-streams/)。

如果叢集中已存在與您要還原的索引同名且處於開啟狀態的索引，您必須關閉、刪除或重新命名這些索引。如需重新命名索引的相關資訊，請參閱 [請求範例](#example-requests)。如需關閉索引的相關資訊，請參閱 [關閉索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/close-index/)。
{: .note}

## 端點

```json
POST _snapshot/{repository}/{snapshot}/_restore
```

## 路徑參數

| 參數 | 資料類型 | 說明 |
:--- | :--- | :---
| `repository` | 字串 | 包含要還原之快照的儲存庫。 |
| `snapshot` | 字串 | 要還原的快照。 |

## 查詢參數

參數 | 資料類型 | 說明
:--- | :--- | :---
`wait_for_completion` | 布林值 |  是否等待快照還原完成後再繼續。 |

## 請求本文欄位

所有請求本文參數皆為選用。

| 參數 | 資料類型 | 說明 |
:--- | :--- | :--- 
| `attach_to_data_stream`（實驗性） | 布林值 | 是否將還原的後端索引附加至既有的同名資料串流。當值為 `true` 時，還原作業會將名稱符合 `.ds-<data_stream>-NNNNNN` 後端索引命名慣例的還原索引附加至既有的同名資料串流，並視需要推進串流世代。附加的索引必須將資料串流的時間戳記欄位對應為 `date`。當值為 `false` 時，索引會還原為獨立索引。預設為 `false`。請參閱 [將還原的後端索引附加至資料串流](#attach-a-restored-backing-index-to-a-data-stream)。|
| `ignore_unavailable` | 布林值 | 如何處理遺失或已關閉的資料串流或索引。如果值為 `false`，請求會針對任何遺失或已關閉的資料串流或索引傳回錯誤。如果值為 `true`，請求會忽略索引清單中遺失或已關閉的資料串流與索引。預設為 `false`。 |
| `ignore_index_settings` | 布林值 | 以逗號分隔的索引設定清單，列出您不想從快照還原的設定。 |
| `include_aliases` | 布林值 | 如何處理原始快照中的索引別名。如果值為 `true`，會還原原始快照中的索引別名。如果值為 `false`，則不會還原別名及其關聯的索引。預設為 `true`。 |
| `include_global_state` | 布林值 | 是否還原目前的叢集狀態<sup>1</sup>。如果值為 `false`，則不會還原叢集狀態。如果值為 true，則會還原目前的叢集狀態。預設為 `false`。|
| `index_settings` | 字串 | 以逗號分隔的設定清單，列出要在所有還原索引中新增或變更的設定。使用此參數可在快照還原期間覆寫索引設定。對於資料串流，這些索引設定會套用至還原的後端索引。 |
| `indices` | 字串 | 以逗號分隔的資料串流與索引清單，列出要從快照還原的項目。支援多索引語法。預設情況下，還原作業會包含快照中的所有資料串流與索引。如果提供此引數，還原作業只會包含您指定的資料串流與索引。 |
| `partial` | 布林值 | 當快照中的索引並非所有主要分片都可用時，還原作業的行為。如果值為 `false`，只要快照中有任何索引並非所有主要分片都可用，整個還原作業就會失敗。<br /> <br />如果值為 `true`，則允許還原含有不可用分片之索引的部分快照。只會還原成功納入快照的分片。所有遺失的分片都會重新建立為空白分片。預設情況下，只要快照中包含的一或多個索引並非所有主要分片都可用，整個還原作業就會失敗。若要變更此行為，請將 `partial` 設為 `true`。預設為 `false`。 |
| `rename_pattern` | 字串 | 要套用至還原資料串流與索引的模式。符合重新命名模式的資料串流與索引會依據 `rename_replacement` 設定重新命名。<br /><br /> 重新命名模式會依照支援參照原始文字的規則運算式定義套用。<br /> <br /> 如果兩個以上的資料串流或索引重新命名為相同名稱，請求就會失敗。如果您重新命名還原的資料串流，其後端索引也會重新命名。例如，如果您將 logs 資料串流重新命名為 `recovered-logs`，後端索引 `.ds-logs-1` 就會重新命名為 `.ds-recovered-logs-1`。<br /> <br /> 如果您重新命名還原的串流，請確保有索引範本符合新的串流名稱。如果沒有相符的索引範本名稱，串流就無法輪替，也不會建立新的後端索引。|
| `rename_replacement` | 字串 | 重新命名的替換字串。|
| `rename_alias_pattern` | 字串 | 要套用至還原別名的模式。符合重新命名模式的別名會依據 `rename_alias_replacement` 設定重新命名。<br /><br /> 重新命名模式會依照支援參照原始文字的規則運算式定義套用。<br /> <br /> 如果兩個以上的別名重新命名為相同名稱，這些別名就會合併為一個。|
| `rename_alias_replacement` | 字串 | 別名重新命名的替換字串。|
| `source_remote_store_repository` | 字串 | 正在還原之來源索引的遠端分段儲存庫名稱。只有在來源與目標叢集都使用以遠端儲存庫為後端的儲存空間，且兩者的遠端儲存庫不同時，才需要此參數。還原前，必須在目標叢集上將指定的儲存庫註冊為唯讀。如果未提供，Snapshot Restore API 會使用建立快照時註冊的儲存庫。
| `source_remote_translog_repository` | 字串 | 正在還原之來源索引的遠端 translog 儲存庫名稱。只有在來源與目標叢集都使用以遠端儲存庫為後端的儲存空間，且兩者的遠端儲存庫不同時，才需要此參數。還原前，必須在目標叢集上將指定的儲存庫註冊為唯讀。
| `wait_for_completion` | 布林值 | 是否在還原作業完成後傳回回應。如果值為 `false`，請求會在還原作業初始化時傳回回應。如果值為 `true`，請求會在還原作業完成時傳回回應。預設為 `false`。 |
`storage_type` | `local` 表示所有快照中繼資料與索引資料都會下載至本機儲存空間。<br /><br > `remote_snapshot` 表示快照中繼資料會下載至叢集，但遠端儲存庫仍會作為索引資料的權威儲存位置。系統會視需要下載並快取資料，以處理查詢。若要使用 `remote_snapshot` 類型還原快照，叢集中至少必須有一個節點設定了 [search 角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/)。<br /><br > 預設為 `local`。

<sup>1</sup>叢集狀態包含：
* 持續性叢集設定
* 索引範本
* 舊版索引範本
* 資料匯入管線
* 索引生命週期原則

## 範例請求

下列範例示範不同的快照還原情境。

### 基本還原

下列請求會從 `my-first-snapshot` 還原 `opendistro-reports-definitions` 索引。`rename_pattern` 與 `rename_replacement` 的組合會使索引重新命名為 `opendistro-reports-definitions_restored`，因為叢集中不允許有重複的開啟索引名稱。

<!-- spec_insert_start
component: example_code
rest: POST /_snapshot/my-opensearch-repo/my-first-snapshot/_restore
body: |
{
  "indices": "opendistro-reports-definitions",
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
  "indices": "opendistro-reports-definitions",
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
    "indices": "opendistro-reports-definitions",
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

### 使用遠端後端儲存空間的跨叢集還原

遠端後端儲存空間是一項功能，OpenSearch 會自動將分段與交易記錄備份至遠端儲存庫。當在**兩者皆使用遠端後端儲存空間**但遠端存放區儲存庫不同的叢集之間還原快照時，請同時使用 `source_remote_store_repository` 與 `source_remote_translog_repository` 參數。

下列範例會將來源叢集上取得的快照中的索引還原至目標叢集。在此範例中，`source-cluster-snapshots` 是包含來源叢集快照的快照儲存庫，`snapshot-1` 是快照名稱，`my-remote-index` 是要還原的索引，`source-remote-segment-repo` 是來源叢集的遠端分段儲存庫 (必須在目標叢集上註冊為唯讀)，而 `source-remote-translog-repo` 是來源叢集的遠端交易記錄儲存庫 (必須在目標叢集上註冊為唯讀)：

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

目標叢集會還原該索引，並將其設定為從來源叢集的遠端存放區儲存庫讀取遠端分段與交易記錄。

如需完整的逐步程序，請參閱[跨遠端後端叢集還原快照]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#restoring-snapshots-across-remote-backed-clusters)。

### 將還原的後端索引附加至資料串流
**於 3.8 版推出**
{: .label .label-purple }

這是實驗性功能，不建議在正式環境中使用。如需此功能進展的最新資訊，或想提供意見回饋，請參閱相關的 [GitHub 議題](https://github.com/opensearch-project/OpenSearch/issues/8271)。
{: .warning}

若要將還原的後端索引附加至同名的既有資料串流，請將 `attach_to_data_stream` 設為 `true`。還原的索引名稱必須符合 `.ds-<data_stream>-NNNNNN` 後端索引命名慣例，且該索引必須將串流的時間戳記欄位對應為 `date`。下列請求會還原 `.ds-logs-foo-000001` 後端索引並將其附加至既有的 `logs-foo` 資料串流，並視需要推進串流世代：

```json
POST /_snapshot/my-opensearch-repo/my-first-snapshot/_restore
{
  "indices": ".ds-logs-foo-000001",
  "attach_to_data_stream": true
}
```
{% include copy-curl.html %}

若要在不從快照還原索引的情況下新增或移除資料串流的後端索引，請使用 [Modify Data Stream API]({{site.url}}{{site.baseurl}}/api-reference/data-stream/modify-data-stream/)。

## 範例回應

成功時，回應會傳回下列 JSON 物件：

```json
{
  "snapshot" : {
    "snapshot" : "my-first-snapshot",
    "indices" : [ ],
    "shards" : {
      "total" : 0,
      "failed" : 0,
      "successful" : 0
    }
  }
}
```

除了快照名稱之外，所有屬性都是空的或為 `0`。這是因為在產生快照之後對磁碟區所做的任何變更都會遺失。不過，如果您呼叫 [Get snapshot]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot/) API 來檢查快照，則會傳回完整填入的快照物件。

## 回應本文欄位

下表列出所有可用的回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- | 
| `snapshot` | 字串 | 快照名稱。 |
| `indices` | 陣列 | 快照中的索引。 |
| `shards` | 物件 | 建立的分片總數，以及成功與失敗的分片數。 |

如果快照中的開啟索引已存在於叢集中，且您未將其刪除、關閉或重新命名，API 會傳回類似下列的錯誤：

```json
{
  "error" : {
    "root_cause" : [
      {
        "type" : "snapshot_restore_exception",
        "reason" : "[my-opensearch-repo:my-first-snapshot/dCK4Qth-TymRQ7Tu7Iga0g] cannot restore index [.opendistro-reports-definitions] because an open index with same name already exists in the cluster. Either close or delete the existing index or restore the index under a different name by providing a rename pattern and replacement name"
      }
    ],
    "type" : "snapshot_restore_exception",
    "reason" : "[my-opensearch-repo:my-first-snapshot/dCK4Qth-TymRQ7Tu7Iga0g] cannot restore index [.opendistro-reports-definitions] because an open index with same name already exists in the cluster. Either close or delete the existing index or restore the index under a different name by providing a rename pattern and replacement name"
  },
  "status" : 500
}
```

## 必要權限

如果您使用 Security 外掛程式，請確定您具有適當的權限：`cluster:admin/snapshot/restore`。
