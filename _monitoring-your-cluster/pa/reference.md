---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指標參考"
parent: Performance Analyzer
nav_order: 3
redirect_from:
  - /monitoring-plugins/pa/reference/
---

# Performance Analyzer 指標參考

Performance Analyzer 提供多項指標，協助您評估效能。下表說明可用的指標，並依與該指標最相關的維度分組。所有指標都支援 `avg`、`sum`、`min` 與 `max` 彙總，但對某些指標而言，無論彙總類型為何，測得的數值都相同。

有關各維度的資訊，請參閱本主題稍後的[維度參考](#dimensions-reference)。

## 相關維度：`ShardID`、`IndexName`、`Operation`、`ShardRole`

| 指標 | 說明 |
| :--- | :--- |
| `CPU_Utilization` | CPU 使用率。過去五秒內相關執行緒所使用的 CPU 時間（毫秒），除以 5000 毫秒。 |
| `Paging_MajfltRate` | 過去五秒內每秒的主要錯誤次數。主要錯誤需要處理程序從磁碟載入記憶體分頁。 |
| `Paging_MinfltRate` | 過去五秒內每秒的次要錯誤次數。次要錯誤不需要處理程序從磁碟載入記憶體分頁。 |
| `Paging_RSS` | 處理程序在實際記憶體中擁有的分頁數---即計入文字、資料或堆疊空間的分頁。此數字不包括尚未依需求載入或已換出的分頁。 |
| `Sched_Runtime` | 每次內容切換在 CPU 上執行所花費的時間（秒）。 |
| `Sched_Waittime` | 每次內容切換在執行佇列上等待所花費的時間（秒）。 |
| `Sched_CtxRate` | 過去五秒內每秒在 CPU 上執行的次數。 |
| `Heap_AllocRate` | 過去 5 秒內每秒配置的堆積記憶體近似值（位元組）。 |
| `IO_ReadThroughput` | 過去五秒內每秒讀取的位元組數。 |
| `IO_WriteThroughput` | 過去五秒內每秒寫入的位元組數。 |
| `IO_TotThroughput` | 過去五秒內每秒讀取或寫入的位元組數。 |
| `IO_ReadSyscallRate` | 過去五秒內每秒的讀取系統呼叫次數。 |
| `IO_WriteSyscallRate` | 過去五秒內每秒的寫入系統呼叫次數。 |
| `IO_TotalSyscallRate` | 過去五秒內每秒的讀取與寫入系統呼叫次數。 |
| `Thread_Blocked_Time` | 相關執行緒被阻擋而無法進入或重新進入監視器的平均時間（秒）。 |
| `Thread_Blocked_Event` | 相關執行緒被阻擋而無法進入或重新進入監視器的總次數（亦即執行緒處於 `blocked` 狀態的次數）。 |
| `Thread_Waited_Time` | 相關執行緒等待進入或重新進入監視器的平均時間（秒）（亦即執行緒處於 `WAITING` 或 `TIMED_WAITING` 狀態的時間）"。 |
| `Thread_Waited_Event` | 相關執行緒等待進入或重新進入監視器的總次數（亦即執行緒處於 `WAITING` 或 `TIMED_WAITING` 狀態的次數）。 |
| `ShardEvents` | 過去五秒內在分片上執行的事件總數。 |
| `ShardBulkDocs` | 過去五秒內編製索引的文件總數。 |

## 相關維度：`ShardID`、`IndexName` 

| 指標 | 說明 |
| :--- | :--- |
| `Indexing_ThrottleTime` | 過去五秒內該索引處於合併節流控制下的時間（毫秒）。 |
| `Cache_Query_Hit` | 過去五秒內查詢快取中成功查閱的次數。 |
| `Cache_Query_Miss` | 過去五秒內查詢快取中未能擷取 `DocIdSet` 的查閱次數。`DocIdSet` 是 Lucene 中的一組文件 ID。 |
| `Cache_Query_Size` | 查詢快取的記憶體大小（位元組）。 |
| `Cache_FieldData_Eviction` | 過去五秒內 OpenSearch 從 `fielddata` 堆積空間驅逐資料的次數（在堆積空間已滿時發生）。 |
| `Cache_FieldData_Size` | `fielddata` 的記憶體大小（位元組）。 |
| `Cache_Request_Hit` | 過去五秒內分片請求快取中成功查閱的次數。 |
| `Cache_Request_Miss` | 過去五秒內請求快取中未能擷取搜尋請求結果的查閱次數。 |
| `Cache_Request_Eviction` | 過去五秒內 OpenSearch 從分片請求快取驅逐資料的次數（在請求快取已滿時發生）。 |
| `Cache_Request_Size` | 分片請求快取的記憶體大小（位元組）。 |

## 相關維度：`ShardID`、`IndexName`、`IndexingStage`  
  
| 指標 | 說明 |
| :--- | :--- |
| `Indexing_Pressure_Current_Limits` | 在特定索引階段（Coordinating、Primary 或 Replica）中，可供索引分片使用的總堆積大小（位元組）。 |
| `Indexing_Pressure_Current_Bytes` | 在特定索引階段（Coordinating、Primary 或 Replica）中，索引分片所佔用的總堆積大小（位元組）。 |
| `Indexing_Pressure_Last_Successful_Timestamp` | 在特定索引階段（Coordinating、Primary 或 Replica）中，索引分片成功請求的時間戳記。 |
| `Indexing_Pressure_Rejection_Count` | 在特定索引階段（Coordinating、Primary 或 Replica）中，OpenSearch 對索引分片執行的拒絕總數。 |
| `Indexing_Pressure_Average_Window_Throughput` | 在特定索引階段（Coordinating、Primary 或 Replica）中，索引分片最近 n 個請求的平均輸送量（n 的值由 `shard_indexing_pressure.secondary_parameter.throughput.request_size_window` 設定決定）。 |
    
## 相關維度：`Operation`、`Exception`、`Indices`、`HTTPRespCode`、`ShardID`、`IndexName`、`ShardRole`    
   
 | 指標 | 說明 |
| :--- | :--- |
| `Latency` | 請求的延遲（毫秒）。 |

## 相關維度：`MemType`   
   
 | 指標 | 說明 |
| :--- | :--- |
| `GC_Collection_Event` | 過去五秒內發生的垃圾收集次數。 |
| `GC_Collection_Time` | 過去五秒內發生的所有垃圾收集的累計時間近似值（毫秒）。 |
| `Heap_Committed` | 已配置供 JVM 使用的記憶體量（位元組）。 |
| `Heap_Init` | JVM 為記憶體管理最初向作業系統要求的記憶體量（位元組）。 |
| `Heap_Max` | 可用於記憶體管理的最大記憶體量（位元組）。 |
| `Heap_Used` | 已使用的記憶體量（位元組）。 |

## 相關維度：`DiskName`   
   
 | 指標 | 說明 |
| :--- | :--- |
| `Disk_Utilization` | 磁碟使用率：過去五秒內 OpenSearch 處理程序讀取與寫入所花費的磁碟時間百分比。 |
| `Disk_WaitTime` | 過去五秒內讀取與寫入作業的平均持續時間（毫秒）。 |
| `Disk_ServiceRate` | 服務速率：過去五秒內每秒讀取或寫入的 MB 數。此指標假設每個磁碟磁區儲存 512 位元組。 |

## 相關維度：`DestAddr`   
   
 | 指標 | 說明 |
| :--- | :--- |
| `Net_TCP_NumFlows` | 已收集的樣本數。Performance Analyzer 每 5 秒收集 1 個樣本。 |
| `Net_TCP_TxQ` | 傳送緩衝區中 TCP 封包的平均數量。 |
| `Net_TCP_RxQ` | 接收緩衝區中 TCP 封包的平均數量。 |
| `Net_TCP_Lost` | 未復原的重複逾時平均次數。當復原完成或 `SND.UNA` 前進時，此數字會重設。`SND.UNA` 是已傳送但尚未確認的第一個資料位元組的序號。 |
| `Net_TCP_SendCWND` | 傳送擁塞視窗的平均大小（位元組）。 |
| `Net_TCP_SSThresh` | 慢速啟動大小閾值的平均大小（位元組）。 |

## 相關維度：`Direction`    
   
 | 指標 | 說明 |
| :--- | :--- |
| `Net_PacketRate4` | 每秒從介面傳送／接收的 IPv4 資料封包總數，包括傳送或接收時發生錯誤的資料封包。 |
| `Net_PacketDropRate4` | 每秒傳送或接收時發生錯誤的 IPv4 資料封包總數。 |
| `Net_PacketRate6` | 每秒從介面傳送／接收的 IPv6 資料封包總數，包括傳送或接收時發生錯誤的資料封包。 |
| `Net_PacketDropRate6` | 每秒傳送或接收時發生錯誤的 IPv6 資料封包總數。 |
| `Net_Throughput` | 所有網路介面每秒傳送或接收的位元數。 |


## 相關維度：`ThreadPoolType`   
   
 | 指標 | 說明 |
| :--- | :--- |
| `ThreadPool_QueueSize` | 工作佇列的大小。 |
| `ThreadPool_RejectedReqs` | 遭拒絕的執行次數。 |
| `ThreadPool_TotalThreads` | 集區中目前的執行緒數。 |
| `ThreadPool_ActiveThreads` | 正在積極執行工作的執行緒約略數目。 |
| `ThreadPool_QueueLatency` | 工作佇列的延遲。 |
| `ThreadPool_QueueCapacity` | 工作佇列目前的容量。 |

## 相關維度：`ClusterManager_PendingTaskType`  
   
 | 指標 | 說明 |
| :--- | :--- |
| `ClusterManager_PendingQueueSize` | 叢集狀態更新執行緒中目前待處理工作的數目。每個節點都有一個叢集狀態更新執行緒，負責提交叢集狀態更新工作，例如建立索引、更新對應、配置分片及使分片失敗。 |

## 相關維度：`Operation`、`Exception`、`Indices`、`HTTPRespCode`   
   
| 指標 | 說明 |
| :--- | :--- |
| `HTTP_RequestDocs` | 請求中的項目數（僅適用於 `_bulk` 請求類型）。 |
| `HTTP_TotalRequests` | 過去 5 秒內完成的請求數。 |

## 相關維度：`CBType` 
  
| 指標 | 說明 |
| :--- | :--- |
| `CB_EstimatedSize` | 目前預估的位元組數。 |
| `CB_TrippedEvents` | 斷路器觸發的次數。 |
| `CB_ConfiguredSize` | 作業可使用的記憶體量上限，以位元組為單位。 |

## 相關維度：`ClusterManagerTaskInsertOrder`、`ClusterManagerTaskPriority`、`ClusterManagerTaskType`、`ClusterManagerTaskMetadata`
 
| 指標 | 說明 |
| :--- | :--- |
| `ClusterManager_Task_Queue_Time` | 叢集管理員工作在佇列中花費的時間，以毫秒為單位。 |
| `ClusterManager_Task_Run_Time` | 叢集管理員工作已執行的時間，以毫秒為單位。 |
     
## 相關維度：`CacheType` 
  
| 指標 | 說明 |
| :--- | :--- |
| `Cache_MaxSize` | 快取的大小上限，以位元組為單位。 |

## 相關維度：`ControllerName` 
| 指標 | 說明 |
| :--- | :--- |
| `AdmissionControl_RejectionCount` | 允入控制器 (Controller of Admission Control) 執行的拒絕總次數。 |
| `AdmissionControl_CurrentValue` | 允入控制器 (Controller of Admission Control) 目前的值。 |
| `AdmissionControl_ThresholdValue` | 允入控制器 (Controller of Admission Control) 的閾值。 |

## 相關維度：`NodeID` 
  
| 指標 | 說明 |
| :--- | :--- |
| `Data_RetryingPendingTasksCount` | 資料節點正在積極重試的受節流待處理工作數。這是依目前時間戳記測量的絕對指標。 |
| `ClusterManager_ThrottledPendingTasksCount` | 遭叢集管理員節點節流的待處理工作總數加總。這是累計指標，因此請務必檢查 max 彙總。 |

## 相關維度：N/A
下列指標與整個叢集相關，不需要特定維度。

| 指標 | 說明 |
| :--- | :--- |
| `Election_Term` | 每次叢集管理員選舉時單調遞增的數字。 |
| `PublishClusterState_Latency` | 節點法定人數發佈新叢集狀態所花費的時間。此指標適用於目前的叢集管理員。 |
| `PublishClusterState_Failure` | 新叢集狀態在叢集管理員節點上發佈失敗的次數。 |
| `ClusterApplierService_Latency` | 每個節點套用叢集管理員所傳送之叢集狀態所花費的時間。 |
| `ClusterApplierService_Failure` | 每個節點上套用叢集狀態動作失敗的次數。 |

## 相關維度：`IndexName`、`NodeName`、`ShardType`、`ShardID`
  
| 指標 | 說明 |
| :--- | :--- |
| `Shard_State` | 每個分片的狀態，例如 `STARTED`、`UNASSIGNED` 或 `RELOCATING`。 |

## 相關維度：`NodeID`、`searchbp_mode`

| 指標 | 說明 |
| :--- | :--- |
| `SearchBP_Shard_Stats_CancellationCount` | 在分片工作層級標記為取消的工作數。 |
| `SearchBP_Shard_Stats_LimitReachedCount` | 在分片工作層級，可取消工作總數超過所設定取消閾值的次數。 |
| `SearchBP_Shard_Stats_Resource_Heap_Usage_CancellationCount` | 自節點上次重新啟動以來，在分片工作層級因堆積使用量過高而標記為取消的工作數。 |
| `SearchBP_Shard_Stats_Resource_Heap_Usage_CurrentMax` | 在分片工作層級目前執行中工作的堆積使用量最大值。 |
| `SearchBP_Shard_Stats_Resource_Heap_Usage_RollingAvg` | 在分片工作層級，最近 `n` 個工作的移動平均堆積使用量。`n` 的預設值為 `100`。 |
| `SearchBP_Shard_Stats_Resource_CPU_Usage_CancellationCount` | 自節點上次重新啟動以來，在分片工作層級因 CPU 使用量過高而標記為取消的工作數。 |
| `SearchBP_Shard_Stats_Resource_CPU_Usage_CurrentMax` | 在分片工作層級，節點上目前執行中所有工作的 CPU 時間最大值。 |
| `SearchBP_Shard_Stats_Resource_CPU_Usage_CurrentAvg` | 在分片工作層級，節點上目前執行中所有工作的平均 CPU 時間。 |
| `SearchBP_Shard_Stats_Resource_ElaspedTime_Usage_CancellationCount` | 自節點上次重新啟動以來，在分片工作層級因經過時間過長而標記為取消的工作數。 |
| `SearchBP_Shard_Stats_Resource_ElaspedTime_Usage_CurrentMax` | 在分片工作層級，節點上目前執行中所有工作的經過時間最大值。 |
| `SearchBP_Shard_Stats_Resource_ElaspedTime_Usage_CurrentAvg` | 在分片工作層級，節點上目前執行中所有工作的平均經過時間。 |
| `Searchbp_Task_Stats_CancellationCount` | 在搜尋工作層級標記為取消的工作數。 |
| `SearchBP_Task_Stats_LimitReachedCount` | 在搜尋工作層級，可取消工作總數超過所設定取消閾值的次數。 |
| `SearchBP_Task_Stats_Resource_Heap_Usage_CancellationCount` | 自節點上次重新啟動以來，在搜尋工作層級因堆積使用量過高而標記為取消的工作數。 |
| `SearchBP_Task_Stats_Resource_Heap_Usage_CurrentMax` | 在搜尋工作層級目前執行中工作的堆積使用量最大值。 |
| `SearchBP_Task_Stats_Resource_Heap_Usage_RollingAvg` | 在搜尋工作層級，最近 `n` 個工作的移動平均堆積使用量。`n` 的預設值為 `10`。 |
| `SearchBP_Task_Stats_Resource_CPU_Usage_CancellationCount` | 自節點上次重新啟動以來，在搜尋工作層級因 CPU 使用量過高而標記為取消的工作數。 |
| `SearchBP_Task_Stats_Resource_CPU_Usage_CurrentMax` | 在搜尋工作層級，節點上目前執行中所有工作的 CPU 時間最大值。 |
| `SearchBP_Task_Stats_Resource_CPU_Usage_CurrentAvg` | 在搜尋工作層級，節點上目前執行中所有工作的平均 CPU 時間。 |
| `SearchBP_Task_Stats_Resource_ElaspedTime_Usage_CancellationCount` | 自節點上次重新啟動以來，在搜尋工作層級因經過時間過長而標記為取消的工作數。 |
| `SearchBP_Task_Stats_Resource_ElaspedTime_Usage_CurrentMax` | 在搜尋工作層級，節點上目前執行中所有工作的經過時間最大值。 |
| `SearchBP_Task_Stats_Resource_ElaspedTime_Usage_CurrentAvg` | 在搜尋工作層級，節點上目前執行中所有工作的平均經過時間。 | 


## 維度參考

| 維度            | 回傳值                                   |
|----------------------|-------------------------------------------------|
| `ShardID`              | 分片的 ID，例如 `1`。           |
| `IndexName`            | 索引的名稱，例如 `my-index`。   |
| `Operation`            | 操作的類型，例如 `shardbulk`。  |
| `ShardRole`            | 分片角色，例如 `primary` 或 `replica`。                            |
| `Exception`            | OpenSearch 例外，例如 `org.opensearch.index_not_found_exception`。 |
| `Indices`              | 請求 URL 中的索引清單。        |
| `HTTPRespCode`         | OpenSearch 回應碼，例如 `200`。 |
| `MemType`              | 記憶體類型，例如 `totYoungGC`、`totFullGC`、`Survivor`、`PermGen`、`OldGen`、`Eden`、`NonHeap` 或 `Heap`。 |
| `DiskName`             | 磁碟的名稱，例如 `sda1`。        |
| `DestAddr`             | 目的地位址，例如 `010015AC`。 |
| `Direction`            | 方向，例如 `in` 或 `out`。                                    |
| `ThreadPoolType`       | OpenSearch 執行緒集區，例如 `index`、`search` 或 `snapshot`。 |
| `CBType`               | 斷路器類型，例如 `accounting`、`fielddata`、`in_flight_requests`、`parent` 或 `request`。 |
| `ClusterManagerTaskInsertOrder`| 工作插入的順序，例如 `3691`。 |
| `ClusterManagerTaskPriority`   | 工作的優先順序，例如 `URGENT`。OpenSearch 會先執行優先順序較高的工作，再執行優先順序較低的工作，無論 `insert_order` 為何。 |
| `ClusterManagerTaskType`       | 工作類型，例如 `shard-started`、`create-index`、`delete-index`、`refresh-mapping`、`put-mapping`、`CleanupSnapshotRestoreState` 或 `Update snapshot state`。 |
| `ClusterManagerTaskMetadata`   | 工作的中繼資料（如果有的話）。                 |
| `CacheType`            | 快取類型，例如 `Field_Data_Cache`、`Shard_Request_Cache` 或 `Node_Query_Cache`。 |
| `NodeID`               | 節點的 ID。                                |
| `Searchbp_mode`        | 搜尋回壓模式，例如 `monitor_only`（預設）、`enforced` 或 `disabled`。 |
