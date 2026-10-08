---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遙測裝置"
nav_order: 45
parent: Reference
redirect_from:
  - /benchmark/user-guide/understanding-results/telemetry/
  - /benchmark/user-guide/telemetry/
---

# 遙測裝置

遙測裝置可為基準測試結果提供額外的深入解析。

遙測結果不會出現在摘要報告中。若要將其視覺化，請將資料匯入 OpenSearch，並在 OpenSearch Dashboards 中將資料視覺化。

若要檢視可用遙測裝置的清單，請使用 `opensearch-benchmark list telemetry` 命令。選取支援的遙測裝置後，您可以在執行測試時提供 `--telemetry` 命令旗標來啟用該裝置。例如，若要搭配 `geonames` 工作負載使用 `jfr` 裝置，請執行下列命令：

```json
opensearch-benchmark workload --workload=geonames --telemetry=jfr
```
{% include copy-curl.html %}

所有具有 `--stats` 的遙測裝置都可以用於非由 OpenSearch Benchmark 佈建的叢集。這些裝置稱為 **執行階段等級遙測裝置**。另一方面，**設定等級遙測裝置** 則涵蓋只有在 OpenSearch Benchmark 佈建叢集時才能使用的裝置。

本頁列出 OpenSearch Benchmark 支援的遙測裝置。

<!-- vale off -->
## jfr
<!-- vale on -->

`jfr` 遙測裝置會在基準測試候選端啟用 [Java Flight Recorder (JFR)](https://docs.oracle.com/javacomponents/jmc-5-5/jfr-runtime-guide/index.html)。在 Java Development Kit (JDK) 11 之前，JFR 僅隨 Oracle JDK 提供。OpenSearch Benchmark 假設基準測試使用 Oracle JDK。如果您在 JDK 11 或更新版本上執行基準測試，[JFR](https://jdk.java.net/jmc/) 也可在 OpenJDK 上使用。

若要啟用 `jfr`，請使用命令 `opensearch-benchmark workload --workload=pmc --telemetry jfr` 叫用 **Workload**。接著 `jfr` 會寫入一個可在 Java Mission Control 中開啟的飛行記錄檔。OpenSearch Benchmark 會在命令列上印出飛行記錄檔的位置。

`jfr` 裝置支援下列參數：


- `recording-template`：自訂飛行記錄範本的名稱。您必須自行負責在每台目標機器上正確安裝這些記錄範本。若未指定，則使用預設的 JFR 記錄範本。
- `jfr-delay`：開始記錄前的等待時間長度。選用。
- `jfr-duration`：記錄的時間長度。選用。

<!-- vale off -->
## jit
<!-- vale on -->

`jit` 遙測裝置會為基準測試候選端啟用 JIT 編譯器記錄。如果 HotSpot 反組譯程式庫可用，記錄將包含反組譯的 JIT 編譯器輸出，可用於低階分析。

<!-- vale off -->
## gc
<!-- vale on -->

`gc` 遙測裝置會為基準測試候選端啟用垃圾收集器 (GC) 記錄。您可以使用 `GCViewer` 等工具來分析 GC 記錄。

如果執行階段 JDK 為 Java 9 或更高版本，您可以指定 `gc-log-config` 參數。GC 記錄組態由標籤與等級的清單組成，例如預設值 `gc*=info,safepoint=info,age*=trace`。執行 `java -Xlog:help` 可檢視可用等級與標籤的清單。

<!-- vale off -->
## heapdump
<!-- vale on -->

`heapdump` 遙測裝置會在基準測試完成後、且在節點關閉之前擷取堆積傾印。

<!-- vale off -->
## node-stats
<!-- vale on -->

`node-stats` 遙測裝置會定期呼叫叢集 [Node Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/)，並記錄下列統計資料及其相關鍵值的指標：

- 索引統計：`indices`
- 執行緒集區統計：`thread_pool`
- JVM 緩衝集區統計：`jvm.buffer_pools`
- JVM `gc` 統計：`jvm.gc`
- 作業系統記憶體統計：`os.mem`
- 作業系統 `cgroup` 統計：`os.cgroup`
- JVM 記憶體統計：`jvm.mem`
- 斷路器統計：`breakers`
- 網路相關統計：`transport`
- 程序 CPU 統計：`process.cpu`

`node-stats` 裝置支援下列參數：

- `node-stats-sample-interval`：大於零的正數，表示取樣間隔 (以秒為單位)。預設為 `1`。
- `node-stats-include-indices`：布林值，指出是否應包含索引統計。預設為 `false`。
- `node-stats-include-indices-metrics`：以逗號分隔的字串，指定要包含的索引統計指標。例如，這可用於限制所收集的索引統計指標。指定此參數會隱含啟用索引統計的收集，因此您不需要另外指定 `node-stats-include-indices: true.`。例如，`--telemetry-params="node-stats-include-indices-metrics:'docs'"` 將會收集索引統計中的 docs 指標。如果您想使用多個欄位，請將 JSON 檔案傳遞給 `telemetry-params`。預設為 `docs,store,indexing,search,merges,query_cache,fielddata,segments,translog,request_cache`。
- `node-stats-include-thread-pools`：布林值，指出是否應包含執行緒集區統計。預設為 `true`。
- `node-stats-include-buffer-pools`：布林值，指出是否應包含緩衝集區統計。預設為 `true`。
- `node-stats-include-breakers`：布林值，指出是否應包含斷路器統計。預設為 `true`。
- `node-stats-include-gc`：布林值，指出是否應包含 JVM GC 統計。預設為 `true`。
- `node-stats-include-mem`：布林值，指出是否應同時包含 JVM 堆積與作業系統記憶體統計。預設為 `true`。
- `node-stats-include-cgroup`：布林值，用於包含作業系統 `cgroup` 統計。記憶體統計會被省略，因為 OpenSearch 以字串值輸出這些資料。請改用 `os_mem_*` 欄位。預設為 `true`。
- `node-stats-include-network`：布林值，指出是否應包含網路相關統計。預設為 `true`。
- `node-stats-include-process`：布林值，指出是否應包含程序 CPU 統計。預設為 `true`。
- `node-stats-include-indexing-pressure`：布林值，指出是否應包含索引壓力統計。預設為 `true`。

<!-- vale off -->
## recovery-stats
<!-- vale on -->

`recovery-stats` 遙測裝置會定期呼叫 [CAT Recovery API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-recovery/)，並為每個分片記錄一份指標文件。

`recovery-stats` 遙測裝置支援下列參數。

| 參數 | 資料類型 | 描述 |
| :--- | :--- | :--- |
| `recovery-stats-indices` | 字串或 JSON 物件 | 指定要從中收集復原統計資料的索引。有效值為：<br>- 指定索引模式的字串。<br>- 當使用 `--target-hosts` 定義多個叢集時，將叢集名稱對應至索引模式的 JSON 物件。<br><br>若未設定，則會為所有索引收集復原統計資料。預設為 `None`。 |
| `recovery-stats-sample-interval` | 數字 | 正數，表示取樣間隔 (以秒為單位)。預設為 `1`。 |

<!-- vale off -->
## shard-stats
<!-- vale on -->

`shard-stats` 遙測裝置會使用 `level=shard` 叢集參數定期呼叫叢集 [Node Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/)，並為每個分片記錄一份指標文件。

此裝置支援 `shard-stats-sample-interval` 參數，該參數定義取樣間隔 (以秒為單位)。預設為 `60`。

<!-- vale off -->
## data-stream-stats
<!-- vale on -->

`data-stream-stats` 遙測裝置會定期呼叫 [Get Data Stream Stats API]({{site.url}}{{site.baseurl}}/api-reference/data-stream/data-stream-stats/)，並為叢集層級統計 (`_all`) 記錄一份指標文件，並為每個資料串流各記錄一份指標文件。

以下是在叢集中有兩個資料串流時所記錄文件的範例：

```json
{
  "data_streams" : [
    {
      "name" : "logs-nginx",
      "timestamp_field" : {
        "name" : "request_time"
      },
      "indices" : [
        {
          "index_name" : ".ds-logs-nginx-000001",
          "index_uuid" : "-VhmuhrQQ6ipYCmBhn6vLw"
        }
      ],
      "generation" : 1,
      "status" : "GREEN",
      "template" : "logs-template-nginx"
    }
  ]
},
{
  "name": "data-stream-stats",
  "data_stream": "my-data-stream-1",
  "backing_indices": 1,
  "store_size_bytes": 439137,
  "maximum_timestamp": 1579936446448
},
{
  "name": "data-stream-stats",
  "data_stream": "my-data-stream-2",
  "backing_indices": 1,
  "store_size_bytes": 439199,
  "maximum_timestamp": 1579936446448
}
```

此遙測裝置支援 `data-stream-stats-sample-interval` 參數，該參數定義取樣間隔 (以秒為單位)。預設為 `10`。

<!-- vale off -->
## ingest-pipeline-stats
<!-- vale on -->

`ingest-pipeline-stats` 遙測裝置會在基準測試開始與結束時呼叫 Node Stats API，並以下列文件的形式記錄差異：

- 每個叢集三份結果文件：`ingest_pipeline_cluster_count`、`ingest_pipeline_cluster_time`、`ingest_pipeline_cluster_failed`
- 每個節點各自的統計一份指標文件：`ingest_pipeline_node_count`、`ingest_pipeline_node_time`、`ingest_pipeline_node_failed`
- 每條管線各自的統計一份指標文件：`ingest_pipeline_pipeline_count`、`ingest_pipeline_pipeline_time`、`ingest_pipeline_pipeline_failed`
- 每個管線處理器各自的統計一份指標文件：`ingest_pipeline_processor_count`、`ingest_pipeline_processor_time`、`ingest_pipeline_processor_failed`


以下範例顯示在單一叢集、單一節點與單一管線的情況下，每份文件的記錄：

```json
{
    "name": "ingest_pipeline_cluster_count",
    "value": 1001,
    "meta": {
      "cluster_name": "docker-cluster"
    }
},
{
    "name": "ingest_pipeline_node_count",
    "value": 1001,
    "meta": {
      "cluster_name": "docker-cluster",
      "node_name": "node-001"
    }
},
{
    "name": "ingest_pipeline_pipeline_count",
    "value": 1001,
    "meta": {
      "cluster_name": "docker-cluster",
      "node_name": "node-001",
      "ingest_pipeline": "test-pipeline-1"
    }
},
{
    "name": "ingest_pipeline_processor_count",
    "value": 1001,
    "meta": {
      "cluster_name": "docker-cluster",
      "node_name": "node-001",
      "ingest_pipeline": "test-pipeline-1",
      "processor_name": "uppercase_1",
      "type": "uppercase"
    }
}
```




