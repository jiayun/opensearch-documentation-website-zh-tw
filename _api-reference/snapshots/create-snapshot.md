---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立快照"
parent: Snapshot APIs
nav_order: 5
---

# 建立快照 API
**於 1.0 版推出**
{: .label .label-purple }

在現有的儲存庫中建立快照。

* 若要進一步了解快照，請參閱[快照]({{site.url}}{{site.baseurl}}/opensearch/snapshots/index/)。

* 若要檢視您的儲存庫清單，請參閱[取得快照儲存庫]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot-repository/)。

## 端點

```json
PUT /_snapshot/{repository}/{snapshot}
POST /_snapshot/{repository}/{snapshot}
```

## 路徑參數

參數 | 資料類型 | 說明
:--- | :--- | :---
`repository` | String | 用來儲存快照的儲存庫名稱。 |
`snapshot` | String | 要建立的快照名稱。 |

## 查詢參數

參數 | 資料類型 | 說明
:--- | :--- | :---
`wait_for_completion` | Boolean |  是否要等待快照建立完成後再繼續。若包含此參數，快照定義會在完成後傳回。 |

## 請求本文欄位

請求本文為選用。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`indices` | String | 您要包含在快照中的索引。您可以使用 `,` 建立索引清單、使用 `*` 指定索引模式，並使用 `-` 排除特定索引。項目之間請勿加入空格。預設為所有索引。
`ignore_unavailable` | Boolean | 若 `indices` 清單中的某個索引不存在，是否要忽略它，而不是讓快照失敗。預設為 `false`。
`include_global_state` | Boolean | 是否要在快照中包含叢集狀態。預設為 `true`。
`partial` | Boolean | 是否允許部分快照。預設為 `false`，若有一或多個分片儲存失敗，會使整個快照失敗

## 範例請求

下列範例示範如何建立快照。

### 不含本文的請求

下列請求會在名為 `my-s3-repository` 的 S3 儲存庫中建立名為 `my-first-snapshot` 的快照。由於請求本文為選用，因此未包含。

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
  snapshot = "my-first-snapshot",
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 含本文的請求

您也可以新增請求本文，以包含或排除特定索引，或指定其他設定：

<!-- spec_insert_start
component: example_code
rest: PUT /_snapshot/my-s3-repository/2
body: |
{
  "indices": "opensearch_dashboards*,my-index*,-my-index-2016",
  "ignore_unavailable": true,
  "include_global_state": false,
  "partial": false
}
-->
{% capture step1_rest %}
PUT /_snapshot/my-s3-repository/2
{
  "indices": "opensearch_dashboards*,my-index*,-my-index-2016",
  "ignore_unavailable": true,
  "include_global_state": false,
  "partial": false
}
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.create(
  repository = "my-s3-repository",
  snapshot = "2",
  body =   {
    "indices": "opensearch_dashboards*,my-index*,-my-index-2016",
    "ignore_unavailable": true,
    "include_global_state": false,
    "partial": false
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

成功時，回應內容取決於您是否包含 `wait_for_completion` 查詢參數。

<!-- vale off -->
##### 未包含 `wait_for_completion`
<!-- vale on -->

```json
{
  "accepted": true
}
```

若要確認快照已建立，請使用[取得快照]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot/) API，並將快照名稱傳入 `snapshot` 路徑參數。
{: .note}

<!-- vale off -->
### 包含 `wait_for_completion`
<!-- vale on -->

會傳回快照定義。

```json
{
  "snapshot" : {
    "snapshot" : "5",
    "uuid" : "ZRH4Zv7cSnuYev2JpLMJGw",
    "version_id" : 136217927,
    "version" : "2.0.1",
    "indices" : [
      ".opendistro-reports-instances",
      ".opensearch-observability",
      ".kibana_1",
      "opensearch_dashboards_sample_data_flights",
      ".opensearch-notifications-config",
      ".opendistro-reports-definitions",
      "shakespeare"
    ],
    "data_streams" : [ ],
    "include_global_state" : true,
    "state" : "SUCCESS",
    "start_time" : "2022-08-10T16:52:15.277Z",
    "start_time_in_millis" : 1660150335277,
    "end_time" : "2022-08-10T16:52:18.699Z",
    "end_time_in_millis" : 1660150338699,
    "duration_in_millis" : 3422,
    "failures" : [ ],
    "shards" : {
      "total" : 7,
      "failed" : 0,
      "successful" : 7
    }
  }
}
```

## 回應本文欄位

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- | 
| `snapshot` | String | 快照名稱。 |
| `uuid` | String | 快照的通用唯一識別碼 (UUID)。 |
| `version_id` | Integer | 建立此快照的 OpenSearch 版本組建 ID。 |
| `version` | Float | 建立此快照的 OpenSearch 版本。 |
| `indices` | Array | 快照中的索引。 |
| `data_streams` | Array | 快照中的資料串流。 |
| `include_global_state` | Boolean | 快照中是否包含目前的叢集狀態。 |
| `start_time` | String | 快照建立程序開始的日期/時間。 |
| `start_time_in_millis` | Long | 快照建立程序開始的時間 (毫秒)。 |
| `end_time` | String | 快照建立程序結束的日期/時間。 |
| `end_time_in_millis` | Long | 快照建立程序結束的時間 (毫秒)。 |
| `duration_in_millis` | Long | 快照建立程序持續的總時間 (毫秒)。 |
| `failures` | Array | 快照建立期間發生的失敗 (若有)。 |
| `shards` | Object | 建立的分片總數，以及成功與失敗的分片數。 |
| `state` | String | 快照狀態。可能的值：`IN_PROGRESS`、`SUCCESS`、`FAILED`、`PARTIAL`。 |
| `remote_store_index_shallow_copy` | Boolean | 遠端儲存索引的快照是否以淺層複本形式擷取。預設為 `false`。 |
| `pinned_timestamp` | Long | 快照為了隱含鎖定其參照的遠端儲存檔案所固定的時間戳記 (毫秒)。 |

## 必要權限

若您使用安全性外掛程式，請確認您具有適當的權限：`cluster:admin/snapshot/create`。
