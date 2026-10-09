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

資料串流是您寫入及搜尋的單一名稱，背後由一系列 OpenSearch 為您輪替的隱藏索引所支援。索引請求會傳送至目前的寫入索引，而搜尋請求則會傳送至所有後端索引。

資料串流適用於持續產生的時間序列資料，例如記錄資料、事件及指標，這類資料的文件會快速累積，且較舊的文件永遠不會更新。將這類資料當作一般索引來管理，意味著要建立輪替別名、指定寫入索引，並為每個新索引重複相同的對應與設定。資料串流只需一個索引範本就能完成這些事。

資料串流具有下列特性：

- 每份文件都必須包含時間戳記欄位。沒有時間戳記欄位的文件會被拒絕。
- 資料串流僅能附加。您無法透過資料串流名稱更新或刪除個別文件；您必須直接指定後端索引。
- 後端索引的名稱為 `.ds-<data-stream>-<generation>` 且為隱藏。世代編號會隨著每次輪替而增加。
- 資料串流只能從包含 `data_stream` 物件的索引範本建立。

附加 [Index State Management (ISM)]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/) 政策，即可根據後端索引的年齡、大小或文件數量，自動輪替及刪除後端索引。該政策會在每個後端索引建立時套用至該索引，因此將政策附加至資料串流只會影響其未來的後端索引。您不需要提供 `rollover_alias` 設定，因為該政策會從後端索引取得該資訊。

若要為資料串流定義精細的權限，請像使用索引名稱一樣使用其名稱。如需更多資訊，請參閱[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)。

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

資料串流範本會獨佔其索引模式。當此範本存在時，建立名稱開頭為 `logs-` 的一般索引會失敗並出現 `cannot create index with name [...], because it matches with template [logs-template] that creates data streams only`。請選擇足夠狹窄的模式，使其不與您的一般索引重疊。
{: .note}

索引至從此範本建立之資料串流的文件必須包含 `@timestamp` 欄位。若要使用不同的欄位名稱，請在 `timestamp_field` 中指定。`template` 物件接受與一般索引範本相同的設定、對應及別名，並將其套用至每個後端索引：

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

明確建立資料串流以初始化其第一個後端索引：

```json
PUT _data_stream/logs-redis
```
{% include copy-curl.html %}

您也可以略過此步驟並開始編製索引。由於符合的範本包含 `data_stream` 物件，OpenSearch 會在第一個索引請求時建立資料串流：

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

`refresh=true` 參數可讓文件立即可供搜尋，以便下一節的搜尋能傳回該文件。在正式環境中請省略此參數，由[重新整理間隔]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/)處理。

資料串流僅接受 `create` 作業。會覆寫文件的 `index` 作業，或指定至資料串流名稱的更新或刪除，都會被拒絕。

## 搜尋資料串流

搜尋資料串流的方式與搜尋索引或別名相同。請求會涵蓋所有後端索引：

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

每個命中項目的 `_index` 欄位包含存放該文件之後端索引的名稱：

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

您也可以使用[非同步搜尋]({{site.url}}{{site.baseurl}}/search-plugins/async/index/)、[SQL]({{site.url}}{{site.baseurl}}/search-plugins/sql/index/) 或 [PPL]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) 查詢資料串流，並像在索引或別名上那樣在其上建立視覺化。

## 輪替資料串流

輪替會建立新的後端索引，並使其成為資料串流的寫入索引。使用下列請求手動輪替：

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

資料串流的世代編號會隨著每次輪替而增加。如需輪替條件與參數，請參閱 [Roll Over API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/rollover/)。若要自動輪替，請使用 [ISM 政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies/)。

## 檢查資料串流

下表列出常見的資料串流請求。取得請求的回應包含時間戳記欄位名稱、後端索引、世代編號、建立該資料串流的範本，以及其狀態，也就是其後端索引中最低的狀態。

| 工作 | 請求 |
| :--- | :--- |
| 列出所有資料串流 | `GET _data_stream` |
| 取得一個資料串流 | `GET _data_stream/logs-redis` |
| 取得資料串流的統計資料 | `GET _data_stream/logs-redis/_stats` |
| 刪除資料串流及其後端索引 | `DELETE _data_stream/logs-redis` |

例如，下列請求會在輪替一次後傳回 `logs-redis` 資料串流：

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

您可以使用萬用字元來指定多個資料串流。刪除資料串流會刪除其後端索引且無法復原；若要依排程移除資料，請改用 ISM 政策。
{: .warning}

如需所有資料串流作業及其參數，請參閱[資料串流 API]({{site.url}}{{site.baseurl}}/api-reference/data-stream/)。

## 修改資料串流的後端索引

使用 [Modify Data Stream API]({{site.url}}{{site.baseurl}}/api-reference/data-stream/modify-data-stream/) 新增或移除現有資料串流的後端索引。此操作僅涉及中繼資料，因此您可以將現有的一般索引遷移至資料串流，或將後端索引與資料串流分離而不刪除其資料。若要在還原快照時將還原的後端索引附加至資料串流，請在 [Restore Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/restore-snapshot/) 中將 `attach_to_data_stream` 設為 `true`。

## OpenSearch Dashboards 中的資料串流

若要前往 **Index Management** 頁面，請在頂端選單中前往 **Management > Index Management**。選取 **Data streams**，以列出叢集中的資料串流。

**Data streams** 表格包含下列欄位。

| 欄位 | 說明 |
| :--- | :--- |
| **Data stream name** | 資料串流的名稱。 |
| **Status** | 資料串流後端索引中最低的健康狀態：如果所有主要分片和副本分片都已指派，則為綠色；如果至少有一個副本分片未指派，則為黃色；如果至少有一個主要分片未指派，則為紅色。 |
| **Template** | 建立資料串流的索引範本。 |
| **Backing indexes count** | 儲存資料的後端索引數量。 |
| **Total size** | 資料串流的所有主要分片和副本分片使用的儲存空間。 |

下圖顯示 **Data streams** 頁面。

![資料串流頁面]({{site.url}}{{site.baseurl}}/images/admin-ui-index/data-streams-list.png)

### 檢視資料串流

在 **Data stream name** 欄位中選取資料串流。**Data stream details** 會顯示其名稱、狀態、範本、後端索引數量及時間戳記欄位名稱。**Backing indexes** 會列出每個後端索引及其健康狀態、狀態、大小、文件數量、分片數量、是否為寫入索引，以及是否由 ISM 原則管理。選取後端索引，即可檢視其詳細資訊，呈現形式與一般索引相同。如需詳細資訊，請參閱[檢視索引詳細資訊]({{site.url}}{{site.baseurl}}/im-plugin/index-operations/#viewing-index-details)。

### 在 Indexes 清單中檢視後端索引

預設情況下，**Indexes** 表格會隱藏後端索引：

1. 在 **Index Management** 中，選取 **Indexes**。
1. 選取 **Show data stream indexes**。表格會新增 **Data stream** 欄位，顯示每個後端索引所屬的資料串流，並在表格標頭新增 **Data streams** 清單。
1. 您可以選擇從 **Data streams** 清單中選取一個或多個資料串流，以僅顯示其後端索引。

### 建立資料串流

資料串流只能從類型為 **Data streams** 的索引範本建立。若要建立這類範本，請參閱[建立索引範本]({{site.url}}{{site.baseurl}}/im-plugin/index-templates/#creating-an-index-template-1)。

1. 在 **Index Management** 中，選取 **Data streams**，然後選取 **Create data stream**。
1. 在 **Data stream name** 中，開始輸入名稱。輸入時，會出現符合的索引模式及其索引範本清單。
1. 從清單中選取索引模式，然後完成名稱，使其符合該模式。

   **Matching template** 會顯示包含該模式的索引範本。**Inherited settings from template** 中的值為唯讀。

1. 選取 **Create data stream**。

### 刪除資料串流

1. 在 **Index Management** 中，選取 **Data streams**。
1. 勾選您要刪除的每個資料串流旁的核取方塊。
1. 選取 **Actions**，然後選取 **Delete**。
1. 在確認對話方塊中輸入 `delete`，然後選取 **Delete**。

刪除資料串流會刪除其後端索引。資料無法復原。
{: .warning}

### 輪替資料串流

1. 在 **Index Management** 中，選取 **Data streams**。
1. 選取 **Actions**，然後選取 **Roll over**。
1. 在 **Configure source** 中，選取要輪替的資料串流。
1. 選取 **Roll over**。

資料串流詳細資訊頁面上的 **Backing indexes** 表格會包含新的寫入索引。

您也可以從 **Data streams** 頁面執行重新整理、排清、清除快取及強制合併，這些操作會套用至所選資料串流的後端索引。如需這些操作的程序，請參閱 [OpenSearch Dashboards 中的索引維護]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/#index-maintenance-in-opensearch-dashboards)。

## 相關文件

- [資料串流 API]({{site.url}}{{site.baseurl}}/api-reference/data-stream/)
- [索引範本]({{site.url}}{{site.baseurl}}/im-plugin/index-templates/)
- [索引狀態管理]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/)
- [索引維護]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/)
