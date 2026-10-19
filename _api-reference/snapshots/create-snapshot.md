---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立快照"
parent: Snapshot APIs
nav_order: 50
---

# Create Snapshot API
**於 1.0 版導入**
{: .label .label-purple }

在現有的儲存庫中建立快照。若要檢視已註冊儲存庫的清單，請使用 [Get Snapshot Repository API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot-repository/)。

快照是增量的：每個快照只會複製先前快照尚未儲存在儲存庫中的索引檔案。快照進行期間，編製索引與搜尋請求仍可繼續。快照包含快照開始時已存在的資料，因此在該時間點之後編製索引的文件不會包含在內。

預設情況下，快照包含叢集中所有開啟的索引與資料串流，包括隱藏索引。關閉的索引只有在您於 `indices` 欄位中指定時才會包含。

## 端點

```json
PUT /_snapshot/{repository}/{snapshot}
POST /_snapshot/{repository}/{snapshot}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`repository` | 字串 | 儲存快照的儲存庫名稱。
`snapshot` | 字串 | 要建立的快照名稱。

快照名稱在儲存庫中必須是唯一的。若要在名稱中包含目前日期，請使用日期數學運算式並進行 URL 編碼。範例請參閱[在快照名稱中使用日期數學的請求](#request-using-date-math-in-the-snapshot-name)。

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`wait_for_completion` | 布林值 | 是否在繼續之前等待快照建立完成。若為 `true`，請求會在快照完成後回傳快照定義。若為 `false`，請求會在快照開始時回傳 `{"accepted": true}`。在大型儲存庫中，即使 `wait_for_completion` 為 `false`，請求也可能需要一些時間才會回傳，因為 OpenSearch 會在快照開始時載入現有快照的資訊。預設為 `false`。
`cluster_manager_timeout` | 時間 | 等待叢集管理員節點回應的時間量。預設為 `30s`。

## 請求本文欄位

請求本文為選用。下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`indices` | 字串或字串陣列 | 您要包含在快照中的資料串流與索引。您可以使用 `,` 建立索引清單、使用 `*` 指定索引模式，以及使用 `-` 排除特定索引。項目之間請勿加入空格。您也可以將索引指定為字串陣列。預設為所有索引。
`ignore_unavailable` | 布林值 | 若 `indices` 清單中的索引不存在，是否忽略它而不是使快照失敗。預設為 `false`。
`include_global_state` | 布林值 | 是否在快照中包含叢集狀態。叢集狀態包括持續性叢集設定、索引範本、舊版索引範本，以及資料匯入管線。暫時性叢集設定與已註冊的快照儲存庫不會包含在內。有關還原叢集狀態的資訊，請參閱 [Restore Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/restore-snapshot/)。預設為 `true`。
`partial` | 布林值 | 是否允許部分快照。若為 `false`，只要快照中任一索引並非所有主要分片皆可用，整個快照就會失敗。若為 `true`，OpenSearch 會對可用的分片建立快照、將快照的 `state` 設為 `PARTIAL`，並在 `failures` 陣列中列出無法使用的分片。預設為 `false`。
`metadata` | 物件 | 要與快照一起儲存的自訂資訊，例如建立快照的使用者以及建立原因。此中繼資料會由 [Get Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot/) 回傳。必須小於 1,024 位元組。

## 範例請求

下列範例示範如何建立快照。

### 不含本文的請求

下列請求會在名為 `my-s3-repository` 的 S3 儲存庫中建立名為 `my-first-snapshot` 的快照。由於請求本文為選用，因此未包含請求本文。

<!-- spec_insert_start
component: example_code
rest: POST /_snapshot/my-s3-repository/my-first-snapshot
-->
{% capture step1_rest %}
POST /_snapshot/my-s3-repository/my-first-snapshot
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.create(
  repository = "my-s3-repository",
  snapshot = "my-first-snapshot"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 含本文的請求

您也可以加入請求本文，以包含或排除特定索引或指定其他設定。下列請求也會在 `metadata` 物件中儲存快照的自訂資訊：

<!-- spec_insert_start
component: example_code
rest: PUT /_snapshot/my-s3-repository/pre-upgrade
body: |
{
  "indices": "opensearch_dashboards*,my-index*,-my-index-2016",
  "ignore_unavailable": true,
  "include_global_state": false,
  "partial": false,
  "metadata": {
    "taken_by": "ops-team",
    "reason": "Backup before upgrading to 3.9"
  }
}
-->
{% capture step1_rest %}
PUT /_snapshot/my-s3-repository/pre-upgrade
{
  "indices": "opensearch_dashboards*,my-index*,-my-index-2016",
  "ignore_unavailable": true,
  "include_global_state": false,
  "partial": false,
  "metadata": {
    "taken_by": "ops-team",
    "reason": "Backup before upgrading to 3.9"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.create(
  repository = "my-s3-repository",
  snapshot = "pre-upgrade",
  body =   {
    "indices": "opensearch_dashboards*,my-index*,-my-index-2016",
    "ignore_unavailable": true,
    "include_global_state": false,
    "partial": false,
    "metadata": {
      "taken_by": "ops-team",
      "reason": "Backup before upgrading to 3.9"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 在快照名稱中使用日期數學的請求

下列請求會建立名稱包含目前日期的快照，例如 `nightly-2026.10.12`。未編碼的快照名稱為 `<nightly-{now/d}>`。`<`、`{`、`/`、`}` 與 `>` 字元必須在請求路徑中進行 URL 編碼：

```json
PUT /_snapshot/my-s3-repository/%3Cnightly-%7Bnow%2Fd%7D%3E
```
{% include copy-curl.html %}

有關日期數學運算式的更多資訊，請參閱[日期數學]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#date-math)。

## 範例回應

成功時，回應內容取決於 `wait_for_completion` 查詢參數的值。

<!-- vale off -->
### wait_for_completion 為 false
<!-- vale on -->

```json
{
  "accepted": true
}
```

若要驗證快照是否已建立，請使用 [Get Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot/)，並將快照名稱作為 `snapshot` 路徑參數傳入。
{: .note}

<!-- vale off -->
### wait_for_completion 為 true
<!-- vale on -->

下列回應是[含本文的請求](#request-with-a-body)範例所回傳的結果：

```json
{
  "snapshot" : {
    "snapshot" : "pre-upgrade",
    "uuid" : "AsDQXjhOQViYaPzbSo8nJw",
    "version_id" : 137307827,
    "version" : "3.9.0",
    "remote_store_index_shallow_copy" : false,
    "indices" : [
      "opensearch_dashboards_sample_data_logs",
      "opensearch_dashboards_sample_data_flights",
      "opensearch_dashboards_sample_data_ecommerce"
    ],
    "data_streams" : [ ],
    "include_global_state" : false,
    "metadata" : {
      "taken_by" : "ops-team",
      "reason" : "Backup before upgrading to 3.9"
    },
    "state" : "SUCCESS",
    "start_time" : "2026-10-12T18:33:50.705Z",
    "start_time_in_millis" : 1791830030705,
    "end_time" : "2026-10-12T18:33:50.906Z",
    "end_time_in_millis" : 1791830030906,
    "duration_in_millis" : 201,
    "failures" : [ ],
    "shards" : {
      "total" : 3,
      "failed" : 0,
      "successful" : 3
    }
  }
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `snapshot` | 字串 | 快照名稱。 |
| `uuid` | 字串 | 快照的通用唯一識別碼（UUID）。 |
| `version_id` | 整數 | 建立快照的 OpenSearch 版本建置 ID。 |
| `version` | 字串 | 建立快照的 OpenSearch 版本。 |
| `indices` | 陣列 | 快照中的索引。 |
| `data_streams` | 陣列 | 快照中的資料串流。 |
| `include_global_state` | 布林值 | 目前的叢集狀態是否包含在快照中。 |
| `metadata` | 物件 | 與快照一起儲存的自訂資訊。僅在請求包含 `metadata` 時回傳。 |
| `start_time` | 字串 | 快照建立程序開始的日期與時間。 |
| `start_time_in_millis` | 長整數 | 快照建立程序開始的時間（毫秒）。 |
| `end_time` | 字串 | 快照建立程序結束的日期與時間。 |
| `end_time_in_millis` | 長整數 | 快照建立程序結束的時間（毫秒）。 |
| `duration_in_millis` | 長整數 | 快照建立程序持續的總時間（毫秒）。 |
| `failures` | 陣列 | 快照建立期間發生的失敗（如果有的話）。 |
| `shards` | 物件 | 建立的分片總數，以及成功與失敗的分片數量。 |
| `state` | 字串 | 快照狀態。可能的值：`IN_PROGRESS`、`SUCCESS`、`FAILED`、`PARTIAL`。 |
| `remote_store_index_shallow_copy` | 布林值 | 遠端儲存空間索引的快照是否以淺層複本方式擷取。預設為 `false`。 |
| `pinned_timestamp` | 長整數 | 由快照固定的時間戳記（毫秒），用於隱含鎖定快照所參照的遠端儲存空間檔案。 |

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`cluster:admin/snapshot/create`。
