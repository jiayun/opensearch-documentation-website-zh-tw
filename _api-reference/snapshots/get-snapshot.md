---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得快照"
parent: Snapshot APIs
nav_order: 6
---

# Get Snapshot API
**於 1.0 版推出**
{: .label .label-purple }

擷取快照的相關資訊。

## 端點

```json
GET _snapshot/{repository}/{snapshot}/
```

## 路徑參數

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `repository` | 字串 | 包含要擷取之快照的儲存庫。 |
| `snapshot` | 字串 | 要擷取的快照。

## 查詢參數

| 參數 | 資料類型 | 說明 | 
:--- | :--- | :---
| `verbose` | 布林值 | 當值為 `true` 時，傳回每個快照的其他資訊，例如建立快照的 OpenSearch 版本、快照的開始與結束時間，以及快照包含的分片數量。當值為 `false` 時，僅傳回快照名稱及其包含的索引。當快照位於雲端儲存庫，而每次讀取 blob 都涉及成本或效能考量時，此參數相當實用。選用。預設為 `true`。|
| `ignore_unavailable` | 布林值 | 如何處理無法使用的快照（已損毀或因其他原因暫時無法傳回）。若值為 `true` 且快照無法使用，請求不會傳回該快照。若值為 `false` 且快照無法使用，請求會傳回錯誤。選用。預設為 `false`。|

## 請求範例

下列請求會擷取位於 `my-opensearch-repo` 儲存庫中的 `my-first-snapshot` 的相關資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_snapshot/my-opensearch-repo/my-first-snapshot
-->
{% capture step1_rest %}
GET /_snapshot/my-opensearch-repo/my-first-snapshot
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.get(
  repository = "my-opensearch-repo",
  snapshot = "my-first-snapshot"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

成功時，回應會傳回快照資訊：

````json
{
  "snapshots" : [
    {
      "snapshot" : "my-first-snapshot",
      "uuid" : "3P7Qa-M8RU6l16Od5n7Lxg",
      "version_id" : 136217927,
      "version" : "2.0.1",
      "indices" : [
        ".opensearch-observability",
        ".opendistro-reports-instances",
        ".opensearch-notifications-config",
        "shakespeare",
        ".opendistro-reports-definitions",
        "opensearch_dashboards_sample_data_flights",
        ".kibana_1"
      ],
      "data_streams" : [ ],
      "include_global_state" : true,
      "state" : "SUCCESS",
      "start_time" : "2022-08-11T20:30:00.399Z",
      "start_time_in_millis" : 1660249800399,
      "end_time" : "2022-08-11T20:30:14.851Z",
      "end_time_in_millis" : 1660249814851,
      "duration_in_millis" : 14452,
      "failures" : [ ],
      "shards" : {
        "total" : 7,
        "failed" : 0,
        "successful" : 7
      }
    }
  ]
}
````
## 回應本文欄位

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- | 
| `snapshot` | 字串 | 快照名稱。 |
| `uuid` | 字串 | 快照的通用唯一識別碼（UUID）。 |
| `version_id` | 整數 | 建立快照的 OpenSearch 版本之建置 ID。 |
| `version` | 浮點數 | 建立快照的 OpenSearch 版本。 |
| `indices` | 陣列 | 快照中的索引。 |
| `data_streams` | 陣列 | 快照中的資料串流。 |
| `include_global_state` | 布林值 | 快照是否包含目前的叢集狀態。 |
| `start_time` | 字串 | 快照建立程序開始的日期／時間。 |
| `start_time_in_millis` | 長整數 | 快照建立程序開始的時間（以毫秒為單位）。 |
| `end_time` | 字串 | 快照建立程序結束的日期／時間。 |
| `end_time_in_millis` | 長整數 | 快照建立程序結束的時間（以毫秒為單位）。 |
| `duration_in_millis` | 長整數 | 快照建立程序持續的總時間（以毫秒為單位）。 |
| `failures` | 陣列 | 快照建立期間發生的失敗（若有）。 |
| `shards` | 物件 | 建立的分片總數，以及成功與失敗的分片數量。 |
| `state` | 字串 | 快照狀態。可能的值：`IN_PROGRESS`、`SUCCESS`、`FAILED`、`PARTIAL`。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:admin/snapshot/get`。
