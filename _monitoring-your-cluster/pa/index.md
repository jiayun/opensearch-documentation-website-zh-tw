---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Performance Analyzer
nav_order: 58
has_children: true
redirect_from:
  - /monitoring-plugins/pa/
  - /monitoring-plugins/pa/index/
  - /monitoring-your-cluster/pa/
---

# Performance Analyzer

Performance Analyzer 是一個外掛程式，內含代理程式與 REST API，可讓您查詢眾多叢集效能指標，包括這些指標的彙總。

OpenSearch 2.0 及更新版本預設會安裝 Performance Analyzer 外掛程式。若您想在停用 Performance Analyzer 的情況下使用 OpenSearch 2.0 或更新版本，請參閱[停用 Performance Analyzer](#disable-performance-analyzer)。
{: .note }

## 先決條件

在搭配 OpenSearch 使用 Performance Analyzer 之前，請先檢閱下列先決條件。

### 儲存空間

Performance Analyzer 使用 `/dev/shm` 作為暫時性的儲存空間。在叢集工作負載繁重時，Performance Analyzer 最多可能使用 1 GB 的空間。

不過，Docker 的 `/dev/shm` 預設大小為 64 MB。若要變更此值，您可以使用 `docker run --shm-size 1gb` 旗標或 [Docker Compose 中的類似設定](https://docs.docker.com/compose/compose-file#shm_size)。

若您未使用 Docker，可以使用 `df -h` 檢查 `/dev/shm` 的大小。預設值應已足夠，但若您需要變更其大小，請在 `/etc/fstab` 中新增下列這一行：

```bash
tmpfs /dev/shm tmpfs defaults,noexec,nosuid,size=1G 0 0
```

接著重新掛載檔案系統：

```bash
mount -o remount /dev/shm
```

### 安全性

Performance Analyzer 支援請求的傳輸中加密，但*不*支援請求的用戶端或伺服器驗證。若要啟用傳輸中加密，請編輯 `$OPENSEARCH_HOME` 目錄中的 `performance-analyzer.properties`：

```properties
vi $OPENSEARCH_HOME/config/opensearch-performance-analyzer/performance-analyzer.properties
```

變更下列幾行以設定傳輸中加密。請注意，`certificate-file-path` 必須是伺服器的憑證，而不是根憑證授權單位 (CA)。

````properties
https-enabled = true

#Setup the correct path for certificates
certificate-file-path = specify_path

private-key-file-path = specify_path
````

## 安裝 Performance Analyzer

[Docker]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/) 與 [tarball]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/tar/) 安裝中已包含 Performance Analyzer 外掛程式，但您也可以手動安裝此外掛程式。

若要手動安裝 Performance Analyzer 外掛程式，請從 [Maven](https://central.sonatype.com/namespace/org.opensearch.plugin) 下載外掛程式，並使用標準的[外掛程式安裝]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)程序進行安裝。Performance Analyzer 會在叢集中的每個節點上執行。

若要在 tarball 安裝上啟動 Performance Analyzer 根本原因分析 (RCA) 代理程式，請執行下列命令：
      
````bash
OPENSEARCH_HOME=~/opensearch-{{ site.opensearch_version }} OPENSEARCH_JAVA_HOME=~/opensearch-{{ site.opensearch_version }}/jdk OPENSEARCH_PATH_CONF=~/opensearch-{{ site.opensearch_version }}/bin ./performance-analyzer-agent-cli
````

下列命令會啟用 Performance Analyzer 外掛程式。

````bash
curl -XPOST localhost:9200/_plugins/_performanceanalyzer/cluster/config -H 'Content-Type: application/json' -d '{"enabled": true}'
````

## 停用 Performance Analyzer

若您希望節省記憶體，並在停用 Performance Analyzer 外掛程式的情況下執行本機 OpenSearch 執行個體，請執行下列步驟：

1. 在停用 Performance Analyzer 之前，請使用下列命令停止任何目前正在執行的 RCA 代理程式動作：

  ```bash
  curl -XPOST localhost:9200/_plugins/_performanceanalyzer/rca/cluster/config -H 'Content-Type: application/json' -d '{"enabled": false}'
  ```

2. 執行下列命令以關閉 Performance Analyzer RCA 代理程式：

  ```bash
  kill $(ps aux | grep -i 'PerformanceAnalyzerApp' | grep -v grep | awk '{print $2}')
  ```

3. 執行下列命令以停用 Performance Analyzer 外掛程式：

  ```bash
  curl -XPOST localhost:9200/_plugins/_performanceanalyzer/cluster/config -H 'Content-Type: application/json' -d '{"enabled": false}'
  ```

4. 執行下列命令以解除安裝 Performance Analyzer 外掛程式：

  ```bash
  bin/opensearch-plugin remove opensearch-performance-analyzer
  ```

## 設定 Performance Analyzer

若要設定 Performance Analyzer 外掛程式，請編輯 `config/opensearch-performance-analyzer/` 目錄中的 `performance-analyzer.properties` 組態檔案。請務必取消註解 `#webservice-bind-host` 這一行，並將其設為 `0.0.0.0`。您可以參考下列組態範例。

````bash
# ======================== OpenSearch Performance Analyzer plugin config =========================

# NOTE: this is an example for Linux. Please modify the config accordingly if you are using it under other OS.

# WebService bind host; default to all interfaces
webservice-bind-host = 0.0.0.0

# Metrics data location
metrics-location = /dev/shm/performanceanalyzer/

# Metrics deletion interval (minutes) for metrics data.
# Interval should be between 1 to 60.
metrics-deletion-interval = 1

# If set to true, the system cleans up the files behind it. So at any point, we should expect only 2
# metrics-db-file-prefix-path files. If set to false, no files are cleaned up. This can be useful, if you are archiving
# the files and wouldn't like for them to be cleaned up.
cleanup-metrics-db-files = true

# WebService exposed by App's port
webservice-listener-port = 9600

# Metric DB File Prefix Path location
metrics-db-file-prefix-path = /tmp/metricsdb_

https-enabled = false

#Setup the correct path for certificates
#certificate-file-path = specify_path

#private-key-file-path = specify_path

# Plugin Stats Metadata file name, expected to be in the same location
plugin-stats-metadata = plugin-stats-metadata

# Agent Stats Metadata file name, expected to be in the same location
agent-stats-metadata = agent-stats-metadata
````
若要啟動 Performance Analyzer RCA 代理程式，請執行下列命令：

````bash
OPENSEARCH_HOME=~/opensearch-{{ site.opensearch_version }} OPENSEARCH_JAVA_HOME=~/opensearch-{{ site.opensearch_version }}/jdk OPENSEARCH_PATH_CONF=~/opensearch-{{ site.opensearch_version }}/bin ./performance-analyzer-agent-cli
````


## 為 RPM/YUM 安裝啟用 Performance Analyzer

若您是從 RPM 發行版安裝 OpenSearch，可以使用 `systemctl` 啟動及停止 Performance Analyzer：

```bash
# Start OpenSearch Performance Analyzer
sudo systemctl start opensearch-performance-analyzer.service
# Stop OpenSearch Performance Analyzer
sudo systemctl stop opensearch-performance-analyzer.service
```

## API 查詢與回應範例

以下是 Performance Analyzer API 查詢範例。此查詢會擷取與您的 OpenSearch 叢集相關的效能指標：
  
````bash
GET localhost:9600/_plugins/_performanceanalyzer/metrics/units
````

以下是回應範例：

````json
{"Disk_Utilization":"%","Cache_Request_Hit":"count", 
"Refresh_Time":"ms","ThreadPool_QueueLatency":"count",
"Merge_Time":"ms","ClusterApplierService_Latency":"ms",
"PublishClusterState_Latency":"ms",
"Cache_Request_Size":"B","LeaderCheck_Failure":"count",
"ThreadPool_QueueSize":"count","Sched_Runtime":"s/ctxswitch","Disk_ServiceRate":"MB/s","Heap_AllocRate":"B/s","Indexing_Pressure_Current_Limits":"B",
"Sched_Waittime":"s/ctxswitch","ShardBulkDocs":"count",
"Thread_Blocked_Time":"s/event","VersionMap_Memory":"B",
"Master_Task_Queue_Time":"ms","IO_TotThroughput":"B/s",
"Indexing_Pressure_Current_Bytes":"B",
"Indexing_Pressure_Last_Successful_Timestamp":"ms",
"Net_PacketRate6":"packets/s","Cache_Query_Hit":"count",
"IO_ReadSyscallRate":"count/s","Net_PacketRate4":"packets/s","Cache_Request_Miss":"count",
"ThreadPool_RejectedReqs":"count","Net_TCP_TxQ":"segments/flow","Master_Task_Run_Time":"ms",
"IO_WriteSyscallRate":"count/s","IO_WriteThroughput":"B/s",
"Refresh_Event":"count","Flush_Time":"ms","Heap_Init":"B",
"Indexing_Pressure_Rejection_Count":"count",
"CPU_Utilization":"cores","Cache_Query_Size":"B",
"Merge_Event":"count","Cache_FieldData_Eviction":"count",
"IO_TotalSyscallRate":"count/s","Net_Throughput":"B/s",
"Paging_RSS":"pages",
"AdmissionControl_ThresholdValue":"count",
"Indexing_Pressure_Average_Window_Throughput":"count/s",
"Cache_MaxSize":"B","IndexWriter_Memory":"B",
"Net_TCP_SSThresh":"B/flow","IO_ReadThroughput":"B/s",
"LeaderCheck_Latency":"ms","FollowerCheck_Failure":"count",
"HTTP_RequestDocs":"count","Net_TCP_Lost":"segments/flow",
"GC_Collection_Event":"count","Sched_CtxRate":"count/s",
"AdmissionControl_RejectionCount":"count","Heap_Max":"B",
"ClusterApplierService_Failure":"count",
"PublishClusterState_Failure":"count",
"Merge_CurrentEvent":"count","Indexing_Buffer":"B",
"Bitset_Memory":"B","Net_PacketDropRate4":"packets/s",
"Heap_Committed":"B","Net_PacketDropRate6":"packets/s",
"Thread_Blocked_Event":"count","GC_Collection_Time":"ms",
"Cache_Query_Miss":"count","Latency":"ms",
"Shard_State":"count","Thread_Waited_Event":"count",
"CB_ConfiguredSize":"B","ThreadPool_QueueCapacity":"count",
"CB_TrippedEvents":"count","Disk_WaitTime":"ms",
"Data_RetryingPendingTasksCount":"count",
"AdmissionControl_CurrentValue":"count",
"Flush_Event":"count","Net_TCP_RxQ":"segments/flow",
"Shard_Size_In_Bytes":"B","Thread_Waited_Time":"s/event",
"HTTP_TotalRequests":"count",
"ThreadPool_ActiveThreads":"count",
"Paging_MinfltRate":"count/s","Net_TCP_SendCWND":"B/flow",
"Cache_Request_Eviction":"count","Segments_Total":"count",
"FollowerCheck_Latency":"ms","Heap_Used":"B",
"Master_ThrottledPendingTasksCount":"count",
"CB_EstimatedSize":"B","Indexing_ThrottleTime":"ms",
"Master_PendingQueueSize":"count",
"Cache_FieldData_Size":"B","Paging_MajfltRate":"count/s",
"ThreadPool_TotalThreads":"count","ShardEvents":"count",
"Net_TCP_NumFlows":"count","Election_Term":"count"}
````

## 根本原因分析

[根本原因分析]({{site.url}}{{site.baseurl}}/monitoring-plugins/pa/rca/index/) (RCA) 框架會使用 Performance Analyzer 的資訊，通知叢集管理員其叢集所發生效能與可用性問題的根本原因。

### 啟用 RCA 框架

若要啟用 RCA 框架，請執行以下命令：

```bash
curl -XPOST http://localhost:9200/_plugins/_performanceanalyzer/rca/cluster/config -H 'Content-Type: application/json' -d '{"enabled": true}'
```

如果您收到 `curl: (52) Empty reply from server` 回應，請執行以下命令以啟用 RCA：

```bash
curl -XPOST https://localhost:9200/_plugins/_performanceanalyzer/rca/cluster/config -H 'Content-Type: application/json' -d '{"enabled": true}' -u 'admin:<custom-admin-password>' -k
```

### API 查詢與回應範例

若要請求所有可用的 RCA，請執行以下命令：

````bash
GET localhost:9600/_plugins/_performanceanalyzer/rca
````

若要請求特定的 RCA，請執行以下命令：

````bash
GET localhost:9600/_plugins/_performanceanalyzer/rca?name=HighHeapUsageClusterRCA
````

以下為回應範例：

```json
{
  "HighHeapUsageClusterRCA": [{
    "RCA_name": "HighHeapUsageClusterRCA",
    "state": "unhealthy",
    "timestamp": 1587426650942,
    "HotClusterSummary": [{
      "number_of_nodes": 2,
      "number_of_unhealthy_nodes": 1,
      "HotNodeSummary": [{
        "host_address": "192.168.144.2",
        "node_id": "JtlEoRowSI6iNpzpjlbp_Q",
        "HotResourceSummary": [{
          "resource_type": "old gen",
          "threshold": 0.65,
          "value": 0.81827232588145373,
          "avg": NaN,
          "max": NaN,
          "min": NaN,
          "unit_type": "heap usage in percentage",
          "time_period_seconds": 600,
          "TopConsumerSummary": [{
              "name": "CACHE_FIELDDATA_SIZE",
              "value": 590702564
            },
            {
              "name": "CACHE_REQUEST_SIZE",
              "value": 28375
            },
            {
              "name": "CACHE_QUERY_SIZE",
              "value": 12687
            }
          ],
        }]
      }]
    }]
  }]
}
```


### 相關連結

有關 Performance Analyzer 與 RCA 使用的更多文件，請參閱以下連結：

- [Performance Analyzer API]({{site.url}}{{site.baseurl}}/monitoring-your-cluster/pa/api/)
- [根本原因分析]({{site.url}}{{site.baseurl}}/monitoring-your-cluster/pa/rca/index/)
- [根本原因分析]({{site.url}}{{site.baseurl}}/monitoring-your-cluster/pa/rca/api/)。
- [RFC：根本原因分析](https://github.com/opensearch-project/performance-analyzer-rca/blob/main/docs/rfc-rca.pdf)

## 常見問題

Performance Analyzer 可能會記錄 `Illegal reflective access operation` 警告。這是已知問題，不會影響功能。
