---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "監控"
parent: Managing OpenSearch Data Prepper
nav_order: 25
---
 
# 使用指標監控 OpenSearch Data Prepper

您可以使用 [Micrometer](https://micrometer.io/) 透過指標監控 OpenSearch Data Prepper。指標有兩種類型：JVM/系統指標與外掛程式指標。[Prometheus](https://prometheus.io/) 作為預設的指標後端。

## JVM 與系統指標

JVM 與系統指標是用於監控 Data Prepper 執行個體的執行時期指標。它們包括類別載入器、記憶體、垃圾回收、執行緒等相關指標。如需更多資訊，請參閱 [JVM 與系統指標](https://micrometer.io/?/docs/ref/jvm)。

### 命名

JVM 與系統指標遵循 [Micrometer](https://micrometer.io/?/docs/concepts#_naming_meters) 中預先定義的名稱。例如，記憶體使用量的 Micrometer 指標名稱為 `jvm.memory.used`。Micrometer 會變更名稱以符合指標系統。以同一個例子來說，`jvm.memory.used` 在 Prometheus 中回報為 `jvm_memory_used`，在 Amazon CloudWatch 中回報為 `jvm.memory.used.value`。

### 提供方式

預設情況下，指標以 Prometheus 抓取格式從 Data Prepper 伺服器上的 **/metrics/sys** 端點提供。您可以設定 Prometheus 從 Data Prepper URL 進行抓取。Prometheus 接著會輪詢 Data Prepper 以取得指標，並將其儲存在自己的資料庫中。若要將資料視覺化，您可以設定任何接受 Prometheus 指標的前端，例如 [Grafana](https://prometheus.io/docs/visualization/grafana/)。您可以更新組態，將指標提供給其他指標註冊服務 (registry)，例如 Amazon CloudWatch，它不需要也不會託管該端點，而是直接將指標發布到 CloudWatch。

## 外掛程式指標

外掛程式會回報自己的指標。Data Prepper 使用命名慣例來協助維持指標的一致性。外掛程式指標不使用維度 (dimension)。


1. `AbstractBuffer`
    - `Counter`
        - `recordsWritten`：寫入緩衝區的記錄數量
        - `recordsRead`：從緩衝區讀取的記錄數量
        - `recordsProcessed`：從緩衝區讀取並標記為已處理的記錄數量
        - `writeTimeouts`：緩衝區中的寫入逾時次數
    - `Gaugefir` 
        - `recordsInBuffer`：緩衝區中的記錄數量
        - `recordsInFlight`：從緩衝區讀取並正由下游元件 (例如處理器與輸出端) 處理的記錄數量
    - `Timer`
        - `readTimeElapsed`：從緩衝區讀取時所經過的時間
        - `checkpointTimeElapsed`：執行檢查點時所經過的時間
2. `AbstractProcessor`
    - `Counter`
        - `recordsIn`：進入處理器的記錄數量
        - `recordsOut`：從處理器輸出的記錄數量
    - `Timer`
        - `timeElapsed`：處理器啟動期間所經過的時間
3. `AbstractSink`
    - `Counter`
        - `recordsIn`：進入輸出端 (sink) 的記錄數量
    - `Timer`
        - `timeElapsed`：輸出端執行期間所經過的時間 

### 命名

指標遵循 `PIPELINE_NAME_PLUGIN_NAME_METRIC_NAME` 的命名慣例。例如，在名為 `output-pipeline` 的管線中，`opensearch-sink` 外掛程式的 `recordsIn` 指標，其完整名稱為 `output-pipeline_opensearch_sink_recordsIn`。

### 提供方式

預設情況下，指標以 Prometheus 抓取格式從 Data Prepper 伺服器上的 `/metrics/sys` 端點提供。您可以設定 Prometheus 從 Data Prepper URL 進行抓取。Data Prepper 伺服器連接埠的預設值為 `4900`，您可以修改此值，而且此連接埠可用於任何接受 Prometheus 指標的前端，例如 [Grafana](https://prometheus.io/docs/visualization/grafana/)。您可以更新組態，將指標提供給其他指標註冊服務 (registry)，例如 CloudWatch，它不需要也不會託管該端點，而是直接將指標發布到 CloudWatch。