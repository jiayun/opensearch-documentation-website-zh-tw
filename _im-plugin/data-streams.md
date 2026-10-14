---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料串流"
nav_order: 25
redirect_from:
  - /opensearch/data-streams/
  - /dashboards/im-dashboards/datastream/
  - /dashboards/admin-ui-index/datastream/
---

# 資料串流

資料串流是您寫入與搜尋的單一名稱，背後由一系列隱藏索引支援，OpenSearch 會為您執行輪替。索引請求會送往目前的寫入索引，搜尋請求則會送往所有後端索引。

資料串流適用於持續產生的時間序列資料，例如記錄檔、事件與指標，這類資料的文件會快速累積，且較舊的文件永遠不會更新。以一般索引管理這類資料，意味著要建立輪替別名、指定寫入索引，並為每個新索引重複相同的對應與設定。資料串流只需一個索引範本就能完成這些事。

資料串流具有下列特性：

- 每份文件都必須包含時間戳記欄位。沒有時間戳記欄位的文件會被拒絕。
- 資料串流僅可附加。傳送至資料串流名稱的索引請求只能建立新文件。若要更新或刪除現有文件，請使用 update by query 或 delete by query 請求，或將請求傳送至包含該文件的後端索引。如需更多資訊，請參閱[更新與刪除資料串流中的文件](#updating-and-deleting-documents-in-a-data-stream)。
- 後端索引的名稱為 `.ds-<data-stream>-<generation>`，且為隱藏。每次輪替時，世代編號會遞增。
- 資料串流只能從包含 `data_stream` 物件的索引範本建立。

附加 [Index State Management (ISM)]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/) 原則，即可根據後端索引的存留時間、大小或文件數量，自動執行輪替與刪除。該原則會在每個後端索引建立時套用至該索引，因此將原則附加至資料串流只會影響其未來的後端索引。您不需要提供 `rollover_alias` 設定，因為該原則會從後端索引取得該資訊。

若要為資料串流定義精細權限，請像使用索引名稱一樣使用其名稱。如需更多資訊，請參閱[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)。

## 為資料串流建立索引範本

資料串流是由包含 `data_stream` 物件的索引範本所定義。範本的索引模式必須符合您打算建立的資料串流名稱：

```json
PUT _index_template/logs-template
{
  "index_patterns": [
    "logs-*"
  ],
  "data_stream": {},
  "priority": 100
}
```
{% include copy-curl.html %}

資料串流範本會獨佔其索引模式。只要此範本存在，建立名稱開頭為 `logs-` 的一般索引就會失敗，並出現 `cannot create index with name [...], because it matches with template [logs-template] that creates data streams only`。請選擇範圍夠窄、不會與您的一般索引重疊的模式。
{: .note}

索引至此範本所建立之資料串流的文件必須包含 `@timestamp` 欄位。若要使用不同的欄位名稱，請在 `timestamp_field` 中指定。`template` 物件接受與一般索引範本相同的設定、對應與別名，並將其套用至每個後端索引：

```json
PUT _index_template/logs-nginx-template
{
  "index_patterns": [
    "logs-nginx"
  ],
  "data_stream": {
    "timestamp_field": {
      "name": "request_time"
    }
  },
  "priority": 200,
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  }
}
```
{% include copy-curl.html %}

名稱 `logs-nginx` 同時符合這兩個範本。OpenSearch 會套用 `logs-nginx-template`，因為其優先順序較高。如需更多資訊，請參閱[索引範本]({{site.url}}{{site.baseurl}}/im-plugin/index-templates/)。

## 建立資料串流

明確建立資料串流，以初始化其第一個後端索引：

```json
PUT _data_stream/logs-redis
```
{% include copy-curl.html %}

您也可以略過此步驟並開始編製索引。由於符合的範本包含 `data_stream` 物件，OpenSearch 會在第一次索引請求時建立資料串流：

```json
POST logs-staging/_doc
{
  "message": "login attempt failed",
  "@timestamp": "2013-03-01T00:00:00"
}
```
{% include copy-curl.html %}

## 將資料匯入資料串流

使用與一般索引相同的 [Document APIs]({{site.url}}{{site.baseurl}}/api-reference/document-apis/index/)，依名稱將文件編製索引至資料串流。每份文件都必須包含範本所定義的時間戳記欄位：

```json
POST logs-redis/_doc?refresh=true
{
  "message": "login attempt",
  "@timestamp": "2013-03-01T00:00:00"
}
```
{% include copy-curl.html %}

`refresh=true` 參數會讓文件立即可供搜尋，以便下一節的搜尋能傳回該文件。在正式環境中請省略此參數，由[重新整理間隔]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/)處理。

資料串流只接受操作類型為 `create` 的寫入請求。使用自動產生文件 ID 的 `POST <data-stream>/_doc` 請求屬於 `create` 操作。若要指定文件 ID，請使用 `_create` 端點，或設定 `op_type=create` 查詢參數。不含 `op_type=create` 的 `PUT <data-stream>/_doc/<id>` 請求屬於 `index` 操作，會被拒絕。下列請求會建立 ID 為 `1` 的文件：

```json
PUT logs-redis/_create/1?refresh=true
{
  "message": "logout",
  "@timestamp": "2013-03-01T00:05:00"
}
```
{% include copy-curl.html %}

在 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 請求中，請為每份文件使用 `create` 動作。資料串流會拒絕 `index` 動作：

```json
POST _bulk?refresh=true
{ "create": { "_index": "logs-redis", "_id": "2" } }
{ "message": "session expired", "@timestamp": "2013-03-01T00:10:00" }
{ "create": { "_index": "logs-redis", "_id": "3" } }
{ "message": "password reset", "@timestamp": "2013-03-01T00:15:00" }
```
{% include copy-curl.html %}

回應中的每個項目都會顯示儲存該文件的後端索引，例如 `"_index": ".ds-logs-redis-000001"`。

## 搜尋資料串流

像搜尋索引或別名一樣搜尋資料串流。請求會涵蓋所有後端索引：

```json
GET logs-redis/_search
{
  "query": {
    "match": {
      "message": "login"
    }
  }
}
```
{% include copy-curl.html %}

每個命中項目的 `_index` 欄位會包含存放該文件之後端索引的名稱：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.13076457,
    "hits": [
      {
        "_index": ".ds-logs-redis-000001",
        "_id": "iCnxtaABPpBDXMo4kFWl",
        "_score": 0.13076457,
        "_source": {
          "message": "login attempt",
          "@timestamp": "2013-03-01T00:00:00"
        }
      }
    ]
  }
}
```
</details>

您也可以使用[非同步搜尋]({{site.url}}{{site.baseurl}}/search-plugins/async/index/)、[SQL]({{site.url}}{{site.baseurl}}/search-plugins/sql/index/) 或 [PPL]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) 查詢資料串流，並像在索引或別名上一樣在其上建立視覺化。

## 更新與刪除資料串流中的文件

傳送至資料串流名稱的單一文件更新與刪除請求會被拒絕。若要變更資料串流中的文件，請使用下列其中一種方法。

### 依查詢更新或刪除文件

[Update by Query]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-by-query/) 與 [Delete by Query]({{site.url}}{{site.baseurl}}/api-reference/document-apis/delete-by-query/) API 接受資料串流名稱，並處理其所有後端索引中符合條件的文件。下列請求會變更包含 `expired` 的文件的 message 欄位：

```json
POST logs-redis/_update_by_query?refresh=true
{
  "query": {
    "match": {
      "message": "expired"
    }
  },
  "script": {
    "source": "ctx._source.message = \"session timed out\""
  }
}
```
{% include copy-curl.html %}

下列請求會刪除包含 `password` 的文件：

```json
POST logs-redis/_delete_by_query?refresh=true
{
  "query": {
    "match": {
      "message": "password"
    }
  }
}
```
{% include copy-curl.html %}

### 更新或刪除單一文件

若要更新或刪除單一文件，請將請求傳送至包含該文件的後端索引。若要找出後端索引，請在資料串流中搜尋該文件。下列請求會傳回 ID 為 `1` 的文件，以及其序號與主要分片任期：

```json
GET logs-redis/_search?seq_no_primary_term=true
{
  "query": {
    "ids": {
      "values": ["1"]
    }
  }
}
```
{% include copy-curl.html %}

命中結果的 `_index` 欄位包含後端索引的名稱：

```json
{
  ...
  "hits": {
    "hits": [
      {
        "_index": ".ds-logs-redis-000001",
        "_id": "1",
        "_seq_no": 1,
        "_primary_term": 1,
        "_score": 1.0,
        "_source": {
          "message": "logout",
          "@timestamp": "2013-03-01T00:05:00"
        }
      }
    ]
  }
}
```

將更新請求傳送至該後端索引。為避免覆寫您搜尋之後所做的變更，請在請求中包含搜尋回應中的 `if_seq_no` 與 `if_primary_term` 值：

```json
POST .ds-logs-redis-000001/_update/1?if_seq_no=1&if_primary_term=1&refresh=true
{
  "doc": {
    "message": "logout requested"
  }
}
```
{% include copy-curl.html %}

同樣地，若要刪除文件，請將請求傳送至後端索引：

```json
DELETE .ds-logs-redis-000001/_doc/1?refresh=true
```
{% include copy-curl.html %}

## 輪替資料串流

輪替會建立新的後端索引，並將其設為資料串流的寫入索引。使用下列請求手動執行輪替：

```json
POST logs-redis/_rollover
```
{% include copy-curl.html %}

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "old_index": ".ds-logs-redis-000001",
  "new_index": ".ds-logs-redis-000002",
  "rolled_over": true,
  "dry_run": false,
  "conditions": {}
}
```
</details>

資料串流的世代編號會隨每次輪替增加。有關輪替條件與參數，請參閱 [Roll Over API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/rollover/)。若要自動輪替，請使用 [ISM 政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies/)。

## 檢視資料串流

下表列出常見的資料串流請求。get 請求的回應包含時間戳記欄位名稱、後端索引、世代編號、建立該資料串流的範本，以及其狀態（即其後端索引中最低的狀態）。

| 工作 | 請求 |
| :--- | :--- |
| 列出所有資料串流 | `GET _data_stream` |
| 取得單一資料串流 | `GET _data_stream/logs-redis` |
| 取得資料串流的統計資料 | `GET _data_stream/logs-redis/_stats` |
| 刪除資料串流及其後端索引 | `DELETE _data_stream/logs-redis` |

例如，下列請求會在執行一次輪替後傳回 `logs-redis` 資料串流：

```json
GET _data_stream/logs-redis
```
{% include copy-curl.html %}

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "data_streams": [
    {
      "name": "logs-redis",
      "timestamp_field": {
        "name": "@timestamp"
      },
      "indices": [
        {
          "index_name": ".ds-logs-redis-000001",
          "index_uuid": "Xq04oCQ-TiCjIL81Q_ZL9g"
        },
        {
          "index_name": ".ds-logs-redis-000002",
          "index_uuid": "UBX0UhE9TFKTi-jB5mB7tQ"
        }
      ],
      "generation": 2,
      "status": "YELLOW",
      "template": "logs-template"
    }
  ]
}
```
</details>

您可以使用萬用字元來指定多個資料串流。刪除資料串流會一併刪除其後端索引，且無法復原；若要依排程移除資料，請改用 ISM 政策。
{: .warning}

有關所有資料串流作業及其參數，請參閱[資料串流 API]({{site.url}}{{site.baseurl}}/api-reference/data-stream/)。

## 修改資料串流的後端索引

使用 [Modify Data Stream API]({{site.url}}{{site.baseurl}}/api-reference/data-stream/modify-data-stream/) 新增或移除現有資料串流的後端索引。這是僅涉及中繼資料的作業，因此您可以將現有的一般索引遷移至資料串流，或在不刪除資料的情況下分離後端索引。若要在快照還原期間將還原的後端索引附加至資料串流，請在 [Restore Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/restore-snapshot/) 中將 `attach_to_data_stream` 設為 `true`。

## OpenSearch Dashboards 中的資料串流

若要前往 **Index Management** 頁面，請在頂端選單前往 **Management > Index Management**。選取 **Data streams** 以列出叢集中的資料串流。

**Data streams** 表格包含下列欄位。

| 欄位 | 說明 |
| :--- | :--- |
| **Data stream name** | 資料串流的名稱。 |
| **Status** | 資料串流後端索引中最低的健康狀態：若所有主要與副本分片皆已指派則為綠色，若至少有一個副本分片未指派則為黃色，若至少有一個主要分片未指派則為紅色。 |
| **Template** | 建立該資料串流的索引範本。 |
| **Backing indexes count** | 儲存資料的後端索引數量。 |
| **Total size** | 資料串流在所有主要與副本分片上使用的儲存空間。 |

下圖顯示 **Data streams** 頁面。

![資料串流頁面]({{site.url}}{{site.baseurl}}/images/admin-ui-index/data-streams-list.png)

### 檢視資料串流

在 **Data stream name** 欄位中選取資料串流。**Data stream details** 會顯示其名稱、狀態、範本、後端索引數量與時間戳記欄位名稱。**Backing indexes** 會列出每個後端索引的健康狀態、狀態、大小、文件數、分片數、是否為寫入索引，以及是否有 ISM 政策管理。選取一個後端索引，即可查看其詳細資訊，形式與一般索引相同。如需更多資訊，請參閱[檢視索引詳細資訊]({{site.url}}{{site.baseurl}}/im-plugin/index-operations/#viewing-index-details)。

### 在 Indexes 清單中檢視後端索引

後端索引預設會隱藏於 **Indexes** 表格中：

1. 在 **Index Management** 中，選取 **Indexes**。
1. 選取 **Show data stream indexes**。表格會新增一個 **Data stream** 欄位，顯示每個後端索引所屬的資料串流，且表格標題會新增一個 **Data streams** 清單。
1. 您可以選擇性地從 **Data streams** 清單中選取一個或多個資料串流，以僅顯示其後端索引。

### 建立資料串流

資料串流只能從類型為 **Data streams** 的索引範本建立。若要建立，請參閱[建立索引範本]({{site.url}}{{site.baseurl}}/im-plugin/index-templates/#creating-an-index-template-1)。

1. 在 **Index Management** 中，選取 **Data streams**，然後選取 **Create data stream**。
1. 在 **Data stream name** 中，開始輸入名稱。當您輸入時，會出現符合的索引模式清單及其索引範本。
1. 從清單中選取索引模式，然後完成名稱，使其符合該模式。

   **Matching template** 會顯示包含該模式的索引範本。**Inherited settings from template** 中的值是唯讀的。

1. 選取 **Create data stream**。

### 刪除資料串流

1. 在 **Index Management** 中，選取 **Data streams**。
1. 選取您要刪除之每個資料串流旁的核取方塊。
1. 選取 **Actions**，然後選取 **Delete**。
1. 在確認對話方塊中輸入 `delete`，然後選取 **Delete**。

刪除資料串流會刪除其後端索引。資料無法復原。
{: .warning}

### 輪替資料串流

1. 在 **Index Management** 中，選取 **Data streams**。
1. 選取 **Actions**，然後選取 **Roll over**。
1. 在 **Configure source** 中，選取要輪替的資料串流。
1. 選取 **Roll over**。

資料串流詳細資料頁面上的 **Backing indexes** 表格會包含新的寫入索引。

您也可以從 **Data streams** 頁面執行重新整理、排清、清除快取及強制合併，這些操作會套用至所選資料串流的後端索引。如需這些程序，請參閱[在 OpenSearch Dashboards 中進行索引維護]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/#index-maintenance-in-opensearch-dashboards)。

## 相關文件

- [資料串流 API]({{site.url}}{{site.baseurl}}/api-reference/data-stream/)
- [索引範本]({{site.url}}{{site.baseurl}}/im-plugin/index-templates/)
- [索引狀態管理]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/)
- [索引維護]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/)
