---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "記錄檔"
parent: Configuring OpenSearch
nav_order: 190
redirect_from:
  - /opensearch/logs/
  - /monitoring-your-cluster/logs/
---

# 記錄檔

OpenSearch 記錄檔包含寶貴的資訊，可用於監控叢集作業及疑難排解。記錄檔的位置會因安裝類型而異：

- 在 Docker 上，OpenSearch 會將大部分記錄檔寫入主控台，其餘則儲存在 `opensearch/logs/`。tarball 安裝同樣使用 `opensearch/logs/`。
- 在大多數 Linux 安裝中，OpenSearch 會將記錄檔寫入 `/var/log/opensearch/`。

記錄檔提供 `.log`（純文字）與 `.json` 檔案兩種格式。OpenSearch 記錄檔的權限預設為 `-rw-r--r--`，表示節點上的任何使用者帳戶都能讀取這些記錄檔。您可以在 `log4j2.properties` 中使用 `filePermissions` 選項，_針對每種記錄檔類型_ 變更此行為。例如，您可以新增 `appender.rolling.filePermissions = rw-r-----` 來變更 JSON 伺服器記錄檔的權限。如需詳細資訊，請參閱 [Log4j 2 文件](https://logging.apache.org/log4j/2.x/manual/appenders.html#RollingFileAppender)。


## 應用程式記錄檔

OpenSearch 的應用程式記錄檔使用 [Apache Log4j 2](https://logging.apache.org/log4j/2.x/) 及其內建的記錄層級（由最不嚴重到最嚴重）。下表說明記錄設定。

| 設定 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `logger.org.opensearch.discovery` | 字串 | 記錄器接受 Log4j2 的內建記錄層級：`OFF`、`FATAL`、`ERROR`、`WARN`、`INFO`、`DEBUG` 和 `TRACE`。預設為 `INFO`。 |

與其變更預設記錄層級（`logger.level`），不如變更個別 OpenSearch 模組的記錄層級：

```json
PUT /_cluster/settings
{
  "persistent" : {
    "logger.org.opensearch.index.reindex" : "DEBUG",
    "logger.org.opensearch.indices.recovery": "TRACE"
  }
}
```
{% include copy-curl.html %}

常見類別可參閱[常見核心記錄類別](#common-core-logging-categories)與[外掛程式記錄器類別](#plugin-logger-categories)；不過，識別模組最簡單的方式不是查看記錄檔（記錄檔會縮寫路徑，例如 `o.o.i.r`），而是查看 [OpenSearch 原始碼](https://github.com/opensearch-project/opensearch/tree/master/server/src/main/java/org/opensearch)。
{: .tip }

完成此範例變更後，OpenSearch 在重新編製索引作業期間會輸出更詳細的記錄檔：

```
[2019-10-18T16:52:51,184][DEBUG][o.o.i.r.TransportReindexAction] [node1] [1626]: starting
[2019-10-18T16:52:51,186][DEBUG][o.o.i.r.TransportReindexAction] [node1] executing initial scroll against [some-index]
[2019-10-18T16:52:51,291][DEBUG][o.o.i.r.TransportReindexAction] [node1] scroll returned [3] documents with a scroll id of [DXF1Z==]
[2019-10-18T16:52:51,292][DEBUG][o.o.i.r.TransportReindexAction] [node1] [1626]: got scroll response with [3] hits
[2019-10-18T16:52:51,294][DEBUG][o.o.i.r.WorkerBulkByScrollTaskState] [node1] [1626]: preparing bulk request for [0s]
[2019-10-18T16:52:51,297][DEBUG][o.o.i.r.TransportReindexAction] [node1] [1626]: preparing bulk request
[2019-10-18T16:52:51,299][DEBUG][o.o.i.r.TransportReindexAction] [node1] [1626]: sending [3] entry, [222b] bulk request
[2019-10-18T16:52:51,310][INFO ][o.e.c.m.MetaDataMappingService] [node1] [some-new-index/R-j3adc6QTmEAEb-eAie9g] create_mapping [_doc]
[2019-10-18T16:52:51,383][DEBUG][o.o.i.r.TransportReindexAction] [node1] [1626]: got scroll response with [0] hits
[2019-10-18T16:52:51,384][DEBUG][o.o.i.r.WorkerBulkByScrollTaskState] [node1] [1626]: preparing bulk request for [0s]
[2019-10-18T16:52:51,385][DEBUG][o.o.i.r.TransportReindexAction] [node1] [1626]: preparing bulk request
[2019-10-18T16:52:51,386][DEBUG][o.o.i.r.TransportReindexAction] [node1] [1626]: finishing without any catastrophic failures
[2019-10-18T16:52:51,395][DEBUG][o.o.i.r.TransportReindexAction] [node1] Freed [1] contexts
```

DEBUG 與 TRACE 層級的輸出極為冗長。如果您為了疑難排解而啟用其中任一層級，請在完成後將其停用。

還有其他方式可以變更記錄層級：

1. 在 `opensearch.yml` 中新增幾行：

   ```yml
   logger.org.opensearch.index.reindex: debug
   ```
   {% include copy.html %}

   如果您想在多個叢集之間重複使用記錄組態，或針對單一節點偵錯啟動問題，修改 `opensearch.yml` 是最合適的做法。

2. 修改 `log4j2.properties`：

   ```properties
   # Define a new logger with unique ID of reindex
   logger.reindex.name = org.opensearch.index.reindex
   # Set the log level for that ID
   logger.reindex.level = debug
   ```
   {% include copy.html %}

   此方法極具彈性，但需要熟悉 [Log4j 2 屬性檔案語法](https://logging.apache.org/log4j/2.x/manual/configuration.html#Properties)。一般而言，其他選項提供較簡單的組態體驗。

   如果您檢查組態目錄中預設的 `log4j2.properties` 檔案，可以看到幾個 OpenSearch 特有的變數：

   ```properties
   appender.console.layout.pattern = [%d{ISO8601}][%-5p][%-25c{1.}] [%node_name]%marker %m%n
   appender.rolling_old.fileName = ${sys:opensearch.logs.base_path}${sys:file.separator}${sys:opensearch.logs.cluster_name}.log
   ```

   - `${sys:opensearch.logs.base_path}` 是記錄檔的目錄（例如 `/var/log/opensearch/`）。
   - `${sys:opensearch.logs.cluster_name}` 是叢集的名稱。
   - `${sys:opensearch.logs.node_name}` 是節點的名稱。
   - `[%node_name]` 是節點的名稱。

### 常見核心記錄類別

下表列出常見的核心記錄類別。

| 記錄器金鑰前置詞             | 說明  | 
| :--------- | :------- 
| `org.opensearch.action`       | 傳輸動作，例如 `index`、`bulk`、`get` 或 `cluster` 動作。適用於追蹤跨節點的請求執行。        |
| `org.opensearch.cluster`      | 叢集狀態發布、路由及中繼資料更新。處理叢集形成、路由及配置問題時可啟用。     |
| `org.opensearch.discovery`    | 節點探索與叢集協調。在叢集形成或網路分割測試期間很有幫助。子套件包含雲端探索。   |
| `org.opensearch.gateway`      | Gateway、ClusterState、復原與配置。適用於節點重新啟動、分片配置，以及從本機磁碟與遠端儲存空間復原分片。       |
| `org.opensearch.http`         | 低階 HTTP 層的請求處理。用於處理 HTTP 通訊與設定相關問題。       |
| `org.opensearch.index`        | 個別索引的內部運作，例如引擎、translog 或分片作業。用於偵錯分片／引擎行為。     |
| `org.opensearch.indices`      | 跨索引服務，例如復原、儲存或叢集狀態服務。在分析分片復原與索引壓力時啟用。   |
| `org.opensearch.ingest`       | 資料匯入管線與處理器。偵錯管線執行時可啟用。        |
| `org.opensearch.node`         | 節點生命週期與啟動程序。適用於處理開機問題。   |
| `org.opensearch.repositories` | 快照／還原儲存庫互動，例如與 Amazon Simple Storage Service (Amazon S3)、Amazon Elastic File System (Amazon EFS) 等的互動。用於處理儲存庫錯誤與快照協調。    |
| `org.opensearch.rest`         | REST 處理常式及至動作的路由。有助於了解 REST API 處理細節。      |
| `org.opensearch.script`       | 指令碼引擎。用於偵錯指令碼編譯與執行。     |
| `org.opensearch.search`       | 搜尋階段，例如 `query`、`fetch` 或 `rewrite`。偵錯查詢執行時可啟用。      |
| `org.opensearch.snapshots`    | 快照與還原的協調作業。用於診斷快照生命週期。        |
| `org.opensearch.threadpool`   | 執行緒集區執行。有助於了解佇列與集區飽和情形。     |
| `org.opensearch.transport`    | 節點間傳輸 TCP 層。用於處理節點對節點的通訊問題。         |
| `org.opensearch.deprecation`  | 淘汰警告。在升級期間可用於找出已淘汰的 API 與設定。        |


### 外掛程式記錄器類別

下表列出常見的外掛程式記錄器類別。

| 外掛程式           | 記錄器前置詞範例            | 說明           |
| :--------- | :------- | :------ |
| Security         | `org.opensearch.security`        | 用於對 Security 外掛程式中的驗證、授權和 TLS 進行偵錯。  |
| k-NN             | `org.opensearch.knn`             | 用於對 k-NN 索引建置、搜尋和記憶體管理進行偵錯。     |
| ML Commons       | `org.opensearch.ml`              | 用於模型註冊、推論和任務執行器。  |
| Alerting         | `org.opensearch.alerting`        | 用於監視執行和通知。     |
| Index Management | `org.opensearch.indexmanagement` | 用於 Index State Management (ISM) 原則、彙整 (rollup) 和轉換 (transform)。    |
| Discovery -- Amazon Elastic Compute Cloud (Amazon EC2)  | `org.opensearch.discovery.ec2`   | 雲端探索資訊。       |



## 錯誤記錄檔

OpenSearch 會記錄 `WARN`、`ERROR` 和 `FATAL` 層級的錯誤。此外，也會記錄 `DEBUG` 層級的某些例外狀況，包括下列項目：

- `org.opensearch.index.mapper.MapperParsingException`
- `org.opensearch.index.query.QueryShardException`
- `org.opensearch.action.search.SearchPhaseExecutionException`
- `org.opensearch.common.util.concurrent.OpenSearchRejectedExecutionException`
- `java.lang.IllegalArgumentException`

錯誤記錄檔可協助您在許多情況下進行疑難排解，包括下列情況：

- Painless 指令碼編譯問題
- 無效的查詢
- 編製索引問題
- 快照失敗
- Index State Management 遷移失敗

### Mapper 剖析例外狀況的範圍

只有在由明確的對應請求 (例如 [Put Mapping API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/put-mapping/) 請求) 觸發時，才會記錄 Mapper 剖析例外狀況。若是由文件編製索引作業 (例如 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 或 [Index API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/index-document/) 請求) 觸發，則不會記錄。例如，若文件包含與索引對應衝突的欄位值 (例如在整數欄位中傳送字串值)，Bulk API 會在回應本文中傳回 `mapper_parsing_exception`，但此錯誤不會寫入錯誤記錄檔。若要找出在大量編製索引期間造成 `mapper_parsing_exception` 的文件，請檢查 Bulk API 回應中的錯誤，而不要依賴錯誤記錄檔。

## 搜尋請求慢速記錄檔

OpenSearch 自 2.12 版起提供搜尋的請求層級慢速記錄檔。這些記錄檔依據閾值來定義何謂「慢速」。所有超過閾值的請求都會被記錄。

搜尋請求慢速記錄檔是透過 [Cluster Settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) 動態啟用的。與分片慢速記錄檔不同，搜尋請求慢速記錄檔的閾值是針對請求的總耗用時間 (took time) 設定的。記錄檔預設為停用 (所有閾值皆設為 `-1`)。

```json
PUT /_cluster/settings
{
"persistent" : {
      "cluster.search.request.slowlog.level" : "TRACE",
      "cluster.search.request.slowlog.threshold.warn": "10s",
      "cluster.search.request.slowlog.threshold.info": "5s",
      "cluster.search.request.slowlog.threshold.debug": "2s",
      "cluster.search.request.slowlog.threshold.trace": "10ms"
}
}
```
{% include copy-curl.html %}

`opensearch_index_search_slowlog.log` 中的一行內容可能如下所示：

```plaintext
[2023-10-30T15:47:42,630][TRACE][c.s.r.slowlog] [runTask-0] took[80.8ms], took_millis[80], phase_took_millis[{expand=0, query=39, fetch=22}], total_hits[4 hits], search_type[QUERY_THEN_FETCH], shards[{total: 10, successful: 10, skipped: 0, failed: 0}], indices[index_1, index_2, my_index_*], source[{"query":{"match_all":{"boost":1.0}}}], id[]
```

若您設定較低的閾值，搜尋請求慢速記錄檔可能會佔用大量磁碟空間並影響效能。建議您僅在疑難排解或效能調校時暫時啟用。若要停用搜尋請求慢速記錄檔，請將所有閾值恢復為 `-1`。
{: .important}

## 分片慢速記錄檔

OpenSearch 有兩種*分片慢速記錄檔*，可協助您找出效能問題：搜尋慢速記錄檔和編製索引慢速記錄檔。

這些記錄檔依據閾值來定義何謂「慢速」搜尋或「慢速」編製索引作業。例如，您可以決定若查詢需要超過 15 秒才能完成，就視為慢速。與針對模組設定的應用程式記錄檔不同，慢速記錄檔是針對索引設定的。這兩種記錄檔預設皆為停用 (所有閾值皆設為 `-1`)。

與搜尋請求慢速記錄檔不同，分片慢速記錄檔的閾值是針對個別分片的耗用時間 (took time) 設定的。

```json
GET {some-index}/_settings?include_defaults=true
{
  "indexing": {
    "slowlog": {
      "reformat": "true",
      "threshold": {
        "index": {
          "warn": "-1",
          "trace": "-1",
          "debug": "-1",
          "info": "-1"
        }
      },
      "source": "1000",
      "level": "TRACE"
    }
  },
  "search": {
    "slowlog": {
      "level": "TRACE",
      "threshold": {
        "fetch": {
          "warn": "-1",
          "trace": "-1",
          "debug": "-1",
          "info": "-1"
        },
        "query": {
          "warn": "-1",
          "trace": "-1",
          "debug": "-1",
          "info": "-1"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

若要啟用這些記錄檔，請提高一或多個閾值：

```json
PUT {some-index}/_settings
{
  "indexing": {
    "slowlog": {
      "threshold": {
        "index": {
          "warn": "15s",
          "trace": "750ms",
          "debug": "3s",
          "info": "10s"
        }
      },
      "source": "500",
      "level": "INFO"
    }
  }
}
```
{% include copy-curl.html %}

在此範例中，OpenSearch 會以 WARN 層級記錄耗時 15 秒以上的編製索引作業，並以 INFO 層級記錄耗時介於 10 到 14.*x* 秒之間的作業。若您將閾值設為 0 秒，OpenSearch 會記錄所有作業，這有助於測試慢速記錄檔是否確實已啟用。

- `reformat` 指定是將文件的 `_source` 欄位記錄為單行 (`true`)，還是允許跨越多行 (`false`)。
- `source` 是要記錄的文件 `_source` 欄位字元數。
- `level` 是要納入的最低記錄層級。

`opensearch_index_indexing_slowlog.log` 中的一行內容可能如下所示：

```plaintext
node1 | [2019-10-24T19:48:51,012][WARN][i.i.s.index] [node1] [some-index/i86iF5kyTyy-PS8zrdDeAA] took[3.4ms], took_millis[3], type[_doc], id[1], routing[], source[{"title":"Your Name", "Director":"Makoto Shinkai"}]
```

若您設定較低的閾值，分片慢速記錄檔可能會佔用大量磁碟空間並影響效能。其產生的記錄比[搜尋請求慢速記錄檔](#search-request-slow-logs)更為詳細。建議您僅在疑難排解或效能調校時暫時啟用。若要停用分片慢速記錄檔，請將所有閾值恢復為 `-1`。
{: .important}

## 任務記錄檔

啟用任務資源取用者後，OpenSearch 可以記錄前 N 個最耗用記憶體的搜尋任務的 CPU 時間與記憶體使用率。預設情況下，任務資源取用者會每隔 60 秒記錄前 10 個搜尋任務。這些值可以在 `opensearch.yml` 中設定。

任務記錄可透過 [Cluster Settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) 動態啟用：

```json
PUT _cluster/settings
{
  "persistent" : {
    "task_resource_consumers.enabled" : "true"
  }
}
```
{% include copy-curl.html %}

啟用任務資源取用者可能會影響搜尋延遲。
{:.tip}

啟用後，記錄檔會寫入 `logs/opensearch_task_detailslog.json` 和 `logs/opensearch_task_detailslog.log`。

若要設定記錄間隔及要記錄的搜尋任務數量，請將下列幾行新增至 `opensearch.yml`：

```yaml
# Number of expensive search tasks to log
cluster.task.consumers.top_n.size:100

# Logging interval
cluster.task.consumers.top_n.frequency:30s
```
{% include copy.html %}

## 棄用記錄檔

棄用記錄檔會記錄用戶端何時對您的叢集發出已棄用的 API 呼叫。這些記錄檔可協助您在升級至新的主要版本之前找出並修正問題。預設情況下，OpenSearch 會以 WARN 層級記錄已棄用的 API 呼叫，這適用於幾乎所有使用案例。如有需要，可使用 `_cluster/settings`、`opensearch.yml` 或 `log4j2.properties` 設定 `logger.deprecation.level`。
