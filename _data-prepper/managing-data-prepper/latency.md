---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管線延遲調校指南"
parent: Managing OpenSearch Data Prepper
nav_order: 45
---

# 管線延遲調校指南

本節提供可有效降低端對端延遲的組態，並包含可直接使用的範例。

延遲分為兩種：

- **匯入延遲**：從來源接收到資料的那一刻起，直到接收端將資料傳送至 OpenSearch 或其他目的地為止所花費的時間。
- **可搜尋延遲**：資料在 OpenSearch 搜尋結果中變為可見之前所花費的時間。此延遲受索引的 `refresh_interval` 限制。

## 低延遲組態

下表列出可調整以改善延遲的組態。

元件 | 設定 | 重要性 | 低延遲起始值 | 取捨
:--- | :--- | :--- | :--- | :---
**管線迴圈** | 每個管線中的 `workers` | 提高平行處理可減少 CPU 或 I/O 密集管線中的佇列情形。 | 通常設為 CPU 核心數；若接收端為 I/O 密集，則可再調高。 | CPU 使用率提高，且傳送至接收端的並行請求增加。
**管線迴圈** | `delay` | 緩衝區讀取之間的暫停時間。 | `0`--`10ms`，以便盡快提取資料。 | 較短的延遲可降低延遲，但會增加輪詢額外負荷、上下文切換及 CPU 啟動次數。請調整以平衡延遲與 CPU 使用率。
**有界封鎖緩衝區** | `batch_size` | 決定每批次處理的記錄數；較小的批次會較快排清。 | 64--256 | 較小的批次會降低輸送量並增加請求數。
**Peer Forwarder** | `batch_size`、`request_timeout` | 批次大小與請求逾時會影響逐跳延遲。 | 將 `batch_size` 保持在適中值，例如 48--128。 | `batch_size` 太小會降低輸送量，而 `request_timeout` 太短則可能在負載下導致重試或逾時。
**Peer Forwarder** | `forwarder` [組態]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/peer-forwarder/#configuration) | 限制轉送前的佇列情形。 | 使用較短的逾時，例如 50–200 ms。 | 較短的逾時會增加進行中的請求與連線數，帶來 CPU、記憶體、TLS 握手及上下文切換的額外負荷。較長的逾時可能導致佇列累積及更高的尾端延遲。
**彙總處理器** | `group_duration` | 決定事件等待彙總視窗關閉的時間長度。 | 建議移除彙總；若有必要，請將視窗保持短暫，例如 `5s`。 | 較小的視窗可能破壞分組語意。
**OpenSearch 接收端** | `bulk_size` (MiB) | 決定大量請求的大小；較小的大量請求會較快排清。 | 1--5 MiB | `bulk_size` 非常小會增加大量請求數、增加 HTTP/TLS 額外負荷、造成更多執行緒集區競爭、產生較小的 Lucene 批次並降低輸送量。`bulk_size` 非常大則會增加填滿批次的時間，並可能造成記憶體暴增、更大的重試及更高的 p95/p99 延遲。
**OpenSearch 接收端** | `index.refresh_interval` | 控制已編製索引的資料變為可搜尋的頻率。 | `1s` (預設) | 較低的值會增加分段更替及索引額外負荷。

`delay` 處理器在設計上會增加延遲。在低延遲管線中請避免使用。
{: .note}

## 低延遲組態範例

以下為低延遲組態範例。

### 記錄檔：優先達到次秒級匯入

當您需要為 HTTP 記錄檔擷取達到次秒級的端對端匯入時，可以使用下列範例。此範例會盡量減少批次處理並避免使用繁重的處理器，讓事件快速排清至 OpenSearch，同時保持 CPU 成本可預測：

```yaml
logs-low-latency:
  workers: 4
  delay: 0
  source:
    http:
      port: 2021
      path: /logs
      ssl: true
      sslKeyCertChainFile: certs/dp.crt
      sslKeyFile: certs/dp.key
  buffer:
    bounded_blocking:
      buffer_size: 4096
      batch_size: 128
  processor: []   # keep light, avoid heavy aggregation
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        index_type: log-analytics
        bulk_size: 1         # MiB; smaller -> lower latency, lower throughput
        max_retries: 8
```
{% include copy.html %}

### 使用對等轉送將跨節點等待降至最低的追蹤

您可以使用下列範例組態，將分散式追蹤的跨節點等待降至最低。`data-prepper-config.yaml` 檔案會啟用低延遲、受 mTLS 保護且逾時設定較短的對等轉送；`pipelines.yml` 檔案則將匯入與原始資料的索引編製分開，讓轉送階段維持輕量。

建立下列 `data-prepper-config.yaml` 檔案：

```yaml

ssl: true
serverPort: 4900
keyStoreFilePath: certs/dp1-admin.p12   # or .jks
keyStorePassword: changeit
privateKeyPassword: changeit

# Or disable ssl on top-level admin/metrics server
#ssl: false
#serverPort: 4900

authentication:
  http_basic:
    username: myuser
    password: "mys3cr3t"
  # or disable http_basic authentication
  #unauthenticated:
  
peer_forwarder:

  ssl: true
  ssl_certificate_file: certs/dp1-peer.crt
  ssl_key_file: certs/dp1-peer.key
  authentication:
    mutual_tls: {}
  port: 4994 # Default
  # choose one discovery mode
  # Discovery mode: dns
  discovery_mode: dns
  domain_name: data-prepper.your-domain.local

  # discovery_mode: static
  #port: 4994
  #static_endpoints: ["dp1", "dp2"]

  # lower batching/wait
  batch_size: 96
  request_timeout: 1000   # ms
```
{% include copy.html %}

建立下列 `pipelines.yml` 檔案：

```yaml
traces-low-latency:
  workers: 4
  delay: 0
  source:
    otel_trace_source:
      port: 21890
      ssl: true
      sslKeyCertChainFile: certs/dp.crt
      sslKeyFile: certs/dp.key
  buffer:
    bounded_blocking:
      buffer_size: 4096
      batch_size: 96
  processor:
    - trace_peer_forwarder: {}
  sink:
    - pipeline:
        name: raw-trace-pipeline   # feed the next pipeline

raw-trace-pipeline:
  source:
    pipeline:
      name: traces-low-latency     # consumes from above
  processor:
    - otel_traces:
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_password
        index_type: trace-analytics-raw
```
{% include copy.html %}