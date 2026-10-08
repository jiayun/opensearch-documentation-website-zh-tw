---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "提取式匯入"
parent: Document APIs
has_children: true
nav_order: 90
---

# 提取式匯入 API
**3.0 版推出**
{: .label .label-purple }

提取式匯入可讓 OpenSearch 從 Apache Kafka 或 Amazon Kinesis 等串流來源匯入資料。在傳統的匯入方式中，用戶端會透過 REST API 主動將資料推送至 OpenSearch。提取式匯入則不同，它讓 OpenSearch 直接從串流來源擷取資料，藉此控制資料流。此方法提供原生的背壓 (backpressure) 處理機制，有助於在流量激增時避免伺服器過載。提取式匯入保證「至少一次」(at-least-once) 的匯入語意，並使用外部版本控制來確保資料一致性。

## 先決條件

使用提取式匯入之前，請確認已符合下列先決條件：

* 使用命令 `bin/opensearch-plugin install <plugin-name>` 為您的串流來源安裝匯入外掛程式。如需詳細資訊，請參閱[其他外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/index/)。OpenSearch 支援下列匯入外掛程式： 
  - `ingestion-kafka`
  - `ingestion-kinesis`（實驗性）
* 在[建立索引](#creating-an-index-for-pull-based-ingestion)時設定提取式匯入。您無法將現有的推送式索引轉換為提取式索引。

## 為提取式匯入建立索引

若要從串流來源匯入資料，請先建立具有提取式匯入設定的索引。下列請求會建立一個以區段複寫模式從 Kafka 主題提取資料的索引。如需其他可用的模式，請參閱[匯入模式](#ingestion-modes)：

```json
PUT /my-index
{
  "settings": {
    "ingestion_source": {
      "type": "kafka",
      "pointer.init.reset": "earliest",
      "param": {
        "topic": "test",
        "bootstrap_servers": "localhost:49353"
      }
    },
    "index.number_of_shards": 1,
    "index.number_of_replicas": 1,
    "index": {
      "replication.type": "SEGMENT"
    }
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      },
      "age": {
        "type": "integer"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 匯入來源設定

`ingestion_source` 設定控制 OpenSearch 如何從串流來源提取資料。_輪詢 (poll)_ 是 OpenSearch 主動向串流來源請求一批資料的作業。下表列出 `ingestion_source` 支援的所有設定。

動態設定可以使用[更新設定 API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/update-settings/) 進行更新，無需重新啟動匯入程序。靜態設定在建立索引後即無法變更。如需靜態與動態設定的詳細資訊，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。
{: .note}

| 設定 | 動態 | 說明 |
| :--- | :--- | :--- |
| `type` | 否 | 串流來源類型。必要。有效值為 `kafka` 或 `kinesis`。 |
| `pointer.init.reset` | 否 | 決定從串流的哪個位置開始讀取。選用。有效值為 `earliest`、`latest`、`reset_by_offset`、`reset_by_timestamp` 或 `none`。請參閱[串流位置](#stream-position)。 |
| `pointer.init.reset.value` | 否 | 僅在使用 `reset_by_offset` 或 `reset_by_timestamp` 時為必要。指定位移值或以毫秒為單位的時間戳記。請參閱[串流位置](#stream-position)。 |
| `error_strategy` | 是 | 處理失敗訊息的方式。選用。有效值為 `DROP`（略過失敗的訊息並繼續匯入）和 `BLOCK`（訊息失敗時停止匯入）。預設為 `DROP`。 |
| `poll.max_batch_size` | 是 | 每次輪詢作業所擷取的最大記錄數。選用。 |
| `poll.timeout` | 是 | 每次輪詢作業等待資料的最長時間。選用。 |
| `num_processor_threads` | 否 | 處理已匯入資料的執行緒數量。選用。預設為 1。 |
| `internal_queue_size` | 否 | 用於進階調整的內部阻塞佇列大小。有效值為 1 到 100,000（含）。選用。預設為 100。 |
| `all_active` | 否 | 是否啟用全主動 (all-active) 匯入模式。使用區段複寫模式的索引無法啟用此模式。預設為 `false`。請參閱[匯入模式](#ingestion-modes)。 |
| `pointer_based_lag_update_interval` | 否 | 計算指標式延遲的間隔。接受時間單位。預設為 `10s`。將此值設為 `0` 會停用指標式延遲計算。 |
| `warmup.timeout` | 是 | 在節點重新啟動或分片重新配置後的暖機階段，等待分片趕上串流來源的最長時間。在暖機完成或逾時之前，分片不會處理查詢。接受時間單位。選用。預設為 `-1`（停用）。 |
| `warmup.lag_threshold` | 是 | 暖機完成時可接受的指標式延遲閾值。當延遲等於或低於此值時，暖機即完成。值為 `0` 表示分片已與來源同步。選用。預設為 `100`。 |
| `mapper_type` | 否 | 定義輸入訊息格式的對應器。有效值為 `default` 和 `raw_payload`。請參閱[訊息格式](#message-format)。 |
| `param` | 是 | 來源專屬的組態參數。必要。<br>&ensp;&#x2022; `ingest-kafka` 外掛程式需要：<br>&ensp;&ensp;- `topic`：要從中取用資料的 Kafka 主題<br>&ensp;&ensp;- `bootstrap_servers`：Kafka 伺服器位址<br>&ensp;&ensp;您也可以選擇性地提供其他標準 Kafka 取用者參數（例如 `fetch.min.bytes`）。這些參數會直接傳遞給 Kafka 取用者。<br>&ensp;&#x2022; `ingest-kinesis` 外掛程式需要：<br>&ensp;&ensp;- `stream`：Kinesis 串流名稱<br>&ensp;&ensp;- `region`：AWS 區域<br>&ensp;&ensp;- `access_key`：AWS 存取金鑰<br>&ensp;&ensp;- `secret_key`：AWS 秘密金鑰<br>&ensp;&ensp;您也可以選擇性地提供 `endpoint_override`。 | 


### 其他設定

提取式匯入支援下列 OpenSearch 設定。

| 設定 | 動態 | 說明 |
| :--- | :--- | :--- |
| `index.periodic_flush_interval` | 是 | OpenSearch 觸發排清 (flush) 作業的間隔。提取式匯入索引的預設值為 `10m`。請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#periodic-flush-interval)。 |

### 匯入模式

提取式匯入支援下列模式。

#### 區段複寫模式

在區段複寫模式中，主要分片會從串流來源匯入事件，並將文件編製索引。提取式索引會設定為使用[區段複寫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/segment-replication/index/)，將區段檔案從主要分片複製到副本分片，如下圖所示。

![提取式匯入區段複寫模式]({{site.url}}{{site.baseurl}}/images/pull-based-ingestion/pull-based-segrep-mode.png){: width="50%" }

我們建議搭配[以遠端儲存空間為後端的儲存方式]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/index/)使用此模式。
{: .tip}

#### 全主動模式

啟用全主動模式後，主要分片與副本分片都可以獨立地從串流來源匯入並編製索引事件，如下圖所示。

![拉取式匯入的全主動模式]({{site.url}}{{site.baseurl}}/images/pull-based-ingestion/pull-based-all-active-mode.png){: width="50%" }

分片之間沒有複寫或協調機制，不過在引導程序期間，如果本機沒有可用的副本，副本分片可能會從主要分片擷取區段檔案。此模式不支援搭配區段複寫使用。

### 串流位置

建立索引時，您可以透過在 `ingestion_source` 參數中設定 `pointer.init.reset` 與 `pointer.init.reset.value` 設定，指定 OpenSearch 應從串流的哪個位置開始讀取。對於已存在的索引，OpenSearch 會從最後一次提交的位置繼續讀取。

下表列出有效的 `pointer.init.reset` 值及其對應的 `pointer.init.reset.value` 值。

| `pointer.init.reset` | 匯入起點 | `pointer.init.reset.value` | 
| :--- | :--- | :--- | 
| `earliest`           | 串流的起點 | None | 
| `latest`             | 串流目前的結尾 | None | 
| `reset_by_offset`    | 串流中的特定位移 | 正整數位移。必要。 | 
| `reset_by_timestamp` | 特定時間戳記 | 以毫秒為單位的 Unix 時間戳記。必要。<br> 對於 Kafka 串流，若在給定時間戳記找不到任何訊息，則預設採用 Kafka 的 `auto.offset.reset` 政策。 |
| `none`               | 已存在索引的最後提交位置 | None | 

### 串流分割

使用分割式串流（例如 Kafka 主題或 Kinesis 分片）時，請注意串流分割區與 OpenSearch 分片之間的下列關係：

- OpenSearch 分片與串流分割區一對一對應。
- 索引分片的數量必須大於或等於串流分割區的數量。
- 超出分割區數量的多餘分片會保持空白。
- 文件必須傳送到同一個分割區，更新才能成功。

使用拉取式匯入時，該索引的傳統 REST API 匯入方式會被停用。
{: .note}

### 更新錯誤政策

您可以使用 [Update Settings API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/update-settings/)，透過將 `index.ingestion_source.error_strategy` 設定為 `DROP` 或 `BLOCK` 來動態更新錯誤政策。

下列範例示範如何更新錯誤政策：

<!-- spec_insert_start
component: example_code
rest: PUT /my-index/_settings
body: |
{
  "index.ingestion_source.error_strategy": "DROP"
}
-->
{% capture step1_rest %}
PUT /my-index/_settings
{
  "index.ingestion_source.error_strategy": "DROP"
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_settings(
  index = "my-index",
  body =   {
    "index.ingestion_source.error_strategy": "DROP"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 訊息格式

串流來源中的訊息必須具備下列格式，才能被 OpenSearch 正確處理：

```json
{"_id":"1", "_version":"1", "_source":{"name": "alice", "age": 30}, "_op_type": "index"}
{"_id":"2", "_version":"2", "_source":{"name": "alice", "age": 30}, "_op_type": "delete"}
```

串流來源中的每個資料單元（Kafka 訊息或 Kinesis 記錄）都必須包含下列欄位，用於指定如何建立或修改 OpenSearch 文件。這是拉取式匯入支援的預設格式。

| 欄位 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `_id` | 字串 | 否 | 文件的唯一識別碼。若未提供，OpenSearch 會自動產生 ID。更新或刪除文件時必須提供。 |
| `_version` | 長整數 | 否 | 文件版本號，必須在外部維護。若有提供，OpenSearch 會捨棄版本早於目前文件版本的訊息。若未提供，則不進行版本檢查。 |
| `_op_type` | 字串 | 否 | 要執行的操作。有效值為：<br>- `index`：建立新文件或更新現有文件。<br>- `create`：以附加模式建立新文件。請注意，這不會更新現有文件。<br>- `delete`：軟刪除文件。 |
| `_source` | 物件 | 是 | 包含文件資料的訊息承載。 |

由於拉取式匯入提供至少一次的匯入語意，我們建議使用文件的 `_id` 欄位以避免重複。如果您的生產者無法保證事件順序，也請設定 `_version` 欄位以確保資料一致性。
{: .tip}

或者，拉取式匯入也支援在僅附加模式下直接編製原始承載的索引，而不進行轉換。若要啟用此行為，請將 `index.ingestion_source.mapper_type` 設定為 `raw_payload`。請注意，在此模式下，索引對應必須符合訊息結構，因為不支援動態對應。使用 `raw_payload` 時，您必須提供與傳入資料串流中完全一致的原始 JSON 物件，如下列範例所示：

```json
{"name": "alice", "age": 30}
{"name": "bob", "age": 30}
```

## 拉取式匯入指標

拉取式匯入提供可用於監控匯入程序的指標。`polling_ingest_stats` 指標可在分片層級取得。

下表列出可用的 `polling_ingest_stats` 指標。

| 指標 | 說明 |
| :--- | :--- |
| `message_processor_stats.total_processed_count` | 訊息處理器已處理的訊息總數。 |
| `message_processor_stats.total_invalid_message_count` | 遇到的無效訊息數量。 |
| `message_processor_stats.total_version_conflicts_count` | 因版本衝突而將被捨棄的舊版本訊息數量。 |
| `message_processor_stats.total_failed_count` | 處理期間發生錯誤的失敗訊息總數。 |
| `message_processor_stats.total_failures_dropped_count` | 在重試次數用盡後被捨棄的失敗訊息總數。請注意，只有在使用 DROP 錯誤政策時，訊息才會被捨棄。 |
| `message_processor_stats.total_processor_thread_interrupt_count` | 表示處理器執行緒上發生的執行緒中斷次數。 |
| `consumer_stats.total_polled_count` | 從串流消費者輪詢取得的訊息總數。 |
| `consumer_stats.total_consumer_error_count` | 消費者讀取嚴重錯誤的總數。 |
| `consumer_stats.total_poller_message_failure_count` | 輪詢器上的失敗訊息總數。 |
| `consumer_stats.total_poller_message_dropped_count` | 輪詢器上被捨棄的失敗訊息總數。 |
| `consumer_stats.lag_in_millis` | 以毫秒為單位的延遲，計算方式為自最後一個已處理訊息的時間戳記起經過的時間。 |
| `consumer_stats.pointer_based_lag` | 以 Apache Kafka 位移為基準的延遲，計算方式為最新可用位移與目前訊息位移之間的差異。此指標僅在使用 Apache Kafka 作為串流來源時適用。 |

若要擷取分片層級的拉取式匯入指標，請使用 [Nodes Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/)：

<!-- spec_insert_start
component: example_code
rest: GET /_nodes/stats/indices?level=shards&pretty
-->
{% capture step1_rest %}
GET /_nodes/stats/indices?level=shards&pretty
{% endcapture %}

{% capture step1_python %}


response = client.nodes.info(
  metric = "indices",
  node_id = "stats",
  params = { "level": "shards", "pretty": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 限制

使用拉取式匯入時，適用下列限制：

* [資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/) 與拉取式匯入不相容。
* 不支援[動態對應]({{site.url}}{{site.baseurl}}/mappings/)。
* 不支援[索引輪替]({{site.url}}{{site.baseurl}}/api-reference/index-apis/rollover/)。
* 不支援作業監聽器。