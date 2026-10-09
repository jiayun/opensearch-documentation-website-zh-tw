---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "追蹤分析"
parent: Common use cases
nav_order: 60
---

# 使用 Data Prepper 進行追蹤分析

追蹤分析讓您能夠收集追蹤資料，並自訂一條管線來匯入及轉換資料，以供 OpenSearch 使用。以下內容概述 OpenSearch Data Prepper 中的追蹤分析工作流程、如何設定它，以及如何將追蹤資料視覺化。

## 簡介

當使用 Data Prepper 作為伺服器端元件來收集追蹤資料時，您可以自訂 Data Prepper 管線來匯入及轉換資料，以供 OpenSearch 使用。轉換完成後，您可以在 OpenSearch Dashboards 內透過 Observability 外掛程式將轉換後的追蹤資料視覺化。追蹤資料可讓您掌握應用程式的效能，並協助您取得更多關於個別追蹤的資訊。

下列流程圖說明追蹤分析的工作流程，從執行 OpenTelemetry Collector 到使用 OpenSearch Dashboards 進行視覺化。

![追蹤分析元件概觀]({{site.url}}{{site.baseurl}}/images/data-prepper/trace-analytics/trace-analytics-components.jpg)

若要監視追蹤分析，您需要在服務環境中設定下列元件：
- 在您的應用程式中加入 **instrumentation**（埋點），使其能夠產生遙測資料並傳送至 OpenTelemetry collector。
- 以 sidecar 或 `daemonset` 的形式為 Amazon Elastic Kubernetes Service (Amazon EKS) 執行 **OpenTelemetry collector**、為 Amazon Elastic Container Service (Amazon ECS) 使用 sidecar，或在 Amazon Elastic Compute Cloud (Amazon EC2) 上使用代理程式。您應設定 collector 將追蹤資料匯出至 Data Prepper。
- 部署 **Data Prepper** 作為 OpenSearch 的匯入 collector。設定它將豐富化後的追蹤資料傳送至您的 OpenSearch 叢集或 Amazon OpenSearch Service 網域。
- 使用 **OpenSearch Dashboards** 來視覺化並偵測分散式應用程式中的問題。

## 追蹤分析管線

為了在 Data Prepper 中監視追蹤分析，我們提供三條管線：`entry-pipeline`、`raw-trace-pipeline` 與 `service-map-pipeline`。下圖概述這些管線如何協同運作以監視追蹤分析。

![追蹤分析管線概觀]({{site.url}}{{site.baseurl}}/images/data-prepper/trace-analytics/trace-analytics-pipeline.jpg)


### OpenTelemetry 追蹤來源
 
[OpenTelemetry 來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/otel-traces/) 接受來自 OpenTelemetry Collector 的追蹤資料。此來源遵循 [OpenTelemetry Protocol](https://github.com/open-telemetry/opentelemetry-specification/tree/master/specification/protocol)，並正式支援透過 gRPC 傳輸以及使用業界標準加密 (TLS/HTTPS)。

### 處理器

追蹤分析功能有三個處理器：

* `otel_traces` -- `otel_traces` 處理器接收來自 [`otel-trace-source`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/otel-trace-source/) 的一組 [span](https://github.com/opensearch-project/data-prepper/blob/fa65e9efb3f8d6a404a1ab1875f21ce85e5c5a6d/data-prepper-api/src/main/java/org/opensearch/dataprepper/model/trace/Span.java) 記錄，並對追蹤群組相關欄位執行有狀態處理、擷取與補全。
* `otel_traces_group` -- `otel_traces_group` 處理器透過查詢 OpenSearch 後端，補齊 [span](https://github.com/opensearch-project/data-prepper/blob/298e7931aa3b26130048ac3bde260e066857df54/data-prepper-api/src/main/java/org/opensearch/dataprepper/model/trace/Span.java) 記錄集合中缺少的追蹤群組相關欄位。
* `service_map` -- `service_map` 處理器對追蹤資料執行必要的前置處理，並建立中繼資料以顯示 `service-map` 儀表板。


### OpenSearch 接收端

OpenSearch 提供一個通用的接收端，可將資料寫入作為目的地的 OpenSearch。[OpenSearch 接收端]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/opensearch/) 具有與 OpenSearch 叢集相關的組態選項，例如端點、SSL、使用者名稱/密碼、索引名稱、索引範本與索引狀態管理。

此接收端為追蹤分析功能提供特定組態。這些組態讓接收端能夠使用追蹤分析專用的索引與索引範本。下列 OpenSearch 索引是追蹤分析專用的：

* `otel-v1-apm-span` -- `otel-v1-apm-span` 索引儲存 [`otel_traces`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/otel-traces/) 處理器的輸出。
* `otel-v1-apm-service-map` -- `otel-v1-apm-service-map` 索引儲存 [`service_map`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/service-map/) 處理器的輸出。

## 追蹤調校

從 0.8.x 版開始，Data Prepper 支援追蹤分析的垂直與水平擴展。您可以調整單一 Data Prepper 執行個體的大小以符合工作負載需求，進行垂直擴展。

您可以使用核心 [Peer Forwarder]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/peer-forwarder/) 部署多個 Data Prepper 執行個體組成叢集，以進行水平擴展。這讓 Data Prepper 執行個體能夠與叢集中的其他執行個體通訊，而且是水平擴展部署的必要條件。

### 擴展建議

使用下列建議組態來擴展 Data Prepper。我們建議您根據需求調整參數。我們也建議您監視 Data Prepper 主機指標與 OpenSearch 指標，以確保組態如預期運作。

#### 緩衝區

Data Prepper 處理的追蹤請求總數等於 `otel-trace-pipeline` 與 `raw-trace-pipeline` 中 `buffer_size` 值的總和。傳送至 OpenSearch 的追蹤請求總數等於 `raw-trace-pipeline` 中 `batch_size` 與 `workers` 的乘積。如需 `raw-trace-pipeline` 的更多資訊，請參閱[追蹤分析管線]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines)。


我們建議在變更緩衝區設定時遵循下列原則：
 * `otel-trace-pipeline` 與 `raw-trace-pipeline` 中的 `buffer_size` 值應該相同。
 * `buffer_size` 應大於或等於 `raw-trace-pipeline` 中的 `workers` * `batch_size`。
 

#### 工作執行緒

`workers` 設定決定 Data Prepper 用來處理來自緩衝區的請求的執行緒數量。我們建議您根據 CPU 使用率來設定 `workers`。此值可以高於可用處理器的數量，因為 Data Prepper 在將資料傳送至 OpenSearch 時會耗費大量的輸入/輸出時間。

#### 堆積記憶體

透過設定 `JVM_OPTS` 環境變數來設定 Data Prepper 的堆積記憶體。我們建議您將堆積記憶體大小設定為至少 `4` * `batch_size` * `otel_send_batch_size` * `maximum size of indvidual span`。

如 [OpenTelemetry Collector](#opentelemetry-collector) 一節所述，請在您的 OpenTelemetry Collector 組態中將 `otel_send_batch_size` 設定為 `50`。

#### 本機磁碟

Data Prepper 使用本機磁碟來儲存服務對應處理所需的詮釋資料，因此我們建議只儲存下列關鍵欄位：`traceId`、`spanId`、`parentSpanId`、`spanKind`、`spanName` 和 `serviceName`。`service-map` 外掛程式只會儲存兩個檔案，每個檔案各儲存 `window_duration` 秒的資料。舉例來說，以 `3000 spans/second` 的輸送量進行測試時，磁碟總使用量為 `4 MB`。

Data Prepper 也會使用本機磁碟來寫入記錄檔。在最新版的 Data Prepper 中，您可以將記錄檔重新導向至偏好的路徑。


### AWS CloudFormation 範本與 Kubernetes/Amazon EKS 組態檔

[AWS CloudFormation](https://github.com/opensearch-project/data-prepper/blob/main/deployment-template/ec2/data-prepper-ec2-deployment-cfn.yaml) 範本提供方便使用的機制，可設定[追蹤調校](#trace-tuning)一節所述的擴展屬性。

[Kubernetes 組態檔](https://github.com/opensearch-project/data-prepper/blob/main/examples/dev/k8s/README.md)和 [Amazon EKS 組態檔](https://github.com/opensearch-project/data-prepper/blob/main/deployment-template/eks/README.md)可用於在叢集部署中設定這些屬性。

### 基準測試

基準測試是在 `r5.xlarge` EC2 執行個體上進行，組態如下：
 
 * `buffer_size`：4096
 * `batch_size`：256
 * `workers`：8
 * `Heap`：10 GB
 
此設定在 CPU 使用率 `20`% 時，可處理每秒 `2100` 個 span 的輸送量。

## 管線組態

下列各節提供不同類型管線的範例，以及如何設定每種類型。

### 範例：追蹤分析管線

下列範例示範如何建置支援 [OpenSearch Dashboards Observability 外掛程式]({{site.url}}{{site.baseurl}}/observability-plugin/trace/ta-dashboards/) 的管線。此管線會從 OpenTelemetry Collector 取得資料，並使用另外兩個管線做為接收端。這兩個不同的管線各有不同用途，並寫入不同的 OpenSearch 索引。第一個管線會準備 OpenSearch 的追蹤資料，並將 span 文件擴充及匯入至 OpenSearch 中的 span 索引。第二個管線會將追蹤彙總為服務對應，並將服務對應文件寫入 OpenSearch 中的服務對應索引。

從 Data Prepper 2.0 版開始，Data Prepper 不再支援 `otel_traces_prepper` 處理器。`otel_traces` 處理器會取代 `otel_traces_prepper` 和 `otel_trace_raw` 處理器，並支援 Data Prepper 近期部分資料模型的變更。以下是 YAML 檔組態範例：

```yaml
entry-pipeline:
  delay: "100"
  source:
    otel_trace_source:
      ssl: false
  buffer:
    bounded_blocking:
      buffer_size: 500000
      batch_size: 10000
  sink:
    - pipeline:
        name: raw-trace-pipeline
    - pipeline:
        name: service-map-pipeline
raw-trace-pipeline:
  source:
    pipeline:
      name: entry-pipeline
  buffer:
    bounded_blocking:
      buffer_size: 500000
      batch_size: 10000
  processor:
    - otel_traces:
  sink:
    - opensearch:
        hosts: ["https://localhost:9200"]
        insecure: true
        username: admin
        password: admin_password
        index_type: trace-analytics-raw
service-map-pipeline:
  delay: "100"
  source:
    pipeline:
      name: entry-pipeline
  buffer:
    bounded_blocking:
      buffer_size: 500000
      batch_size: 10000
  processor:
    - service_map:
  sink:
    - opensearch:
        hosts: ["https://localhost:9200"]
        insecure: true
        username: admin
        password: admin_password
        index_type: trace-analytics-service-map
```
{% include copy.html %}

若要維持類似的匯入輸送量與延遲，請依用戶端請求承載中預估的最大批次大小來調整 `buffer_size` 和 `batch_size`。{: .tip}

#### 範例：`otel trace`

以下是啟用 SSL 與基本驗證的 `otel-trace-source` .yaml 檔範例。請注意，您需要修改 `otel-collector-config.yaml` 檔，使其使用您自己的憑證。

```yaml
source:
  otel_trace_source:
    #record_type: event  # Add this when using Data Prepper 1.x. This option is removed in 2.0
    ssl: true
    sslKeyCertChainFile: /full/path/to/certfile.crt
    sslKeyFile: /full/path/to/keyfile.key
    authentication:
      http_basic:
        username: my-user
        password: my_s3cr3t
```
{% include copy.html %}

#### 範例：pipeline.yaml

以下是未啟用 SSL 與基本驗證的 `pipeline.yaml` 檔案範例，用於 `otel-trace-pipeline` 管線：

```yaml
otel-trace-pipeline:
  # workers is the number of threads processing data in each pipeline.
  # We recommend same value for all pipelines.
  # default value is 1, set a value based on the machine you are running Data Prepper
  workers: 8
  # delay in milliseconds is how often the worker threads should process data.
  # Recommend not to change this config as we want the entry-pipeline to process as quick as possible
  # default value is 3_000 ms
  delay: "100"
  source:
    otel_trace_source:
      #record_type: event  # Add this when using Data Prepper 1.x. This option is removed in 2.0
      ssl: false
      authentication:
        unauthenticated:
  buffer:
    bounded_blocking:
      # buffer_size is the number of ExportTraceRequest from otel-collector the Data Prepper should hold in memory. 
      # We recommend to keep the same buffer_size for all pipelines. 
      # Make sure you configure sufficient heap
      # default value is 512
      buffer_size: 500000
      # This is the maximum number of request each worker thread will process within the delay.
      # Default is 8.
      # Make sure buffer_size >= workers * batch_size
      batch_size: 10000
  sink:
    - pipeline:
        name: raw-trace-pipeline
    - pipeline:
        name: entry-pipeline

raw-trace-pipeline:
  # Configure same as the otel-trace-pipeline
  workers: 8
  # We recommend using the default value for the raw-trace-pipeline.
  delay: 3000
  source:
    pipeline: 
      name: otel-trace-pipeline
  buffer:
    bounded_blocking:
      # Configure the same value as in entry-pipeline
      # Make sure you configure sufficient heap
      # The default value is 512
      buffer_size: 500000
      # The raw processor does bulk request to your OpenSearch sink, so configure the batch_size higher.
      # If you use the recommended otel-collector setup each ExportTraceRequest could contain max 50 spans. https://github.com/opensearch-project/data-prepper/tree/v0.7.x/deployment/aws
      # With 64 as batch size each worker thread could process upto 3200 spans (64 * 50)
      batch_size: 10000
  processor:
    - otel_traces:
    # Optional: only if you want the group-filler stage.
    - otel_traces_group:
        hosts: [ "https://opensearch:9200" ]
        # Change to your credentials
        username: admin
        password: admin_password
        # Add a certificate file if you are accessing an OpenSearch cluster with a self-signed certificate  
        #cert: /path/to/cert
        # If you are connecting to an Amazon OpenSearch Service domain without
        # Fine-Grained Access Control, enable these settings. Comment out the
        # username and password above.
        #aws_sigv4: true
        #aws_region: us-east-1
  sink:
    - opensearch:
        hosts: [ "https://opensearch:9200" ]
        index_type: trace-analytics-raw
        # Change to your credentials
        username: admin
        password: admin_password
        # Add a certificate file if you are accessing an OpenSearch cluster with a self-signed certificate  
        #cert: /path/to/cert
        # If you are connecting to an Amazon OpenSearch Service domain without
        # Fine-Grained Access Control, enable these settings. Comment out the
        # username and password above.
        #aws_sigv4: true
        #aws_region: us-east-1

service-map-pipeline:
  workers: 8
  delay: 100
  source:
    pipeline: 
      name: otel-trace-pipeline
  processor:
    - service_map:
        # The window duration is the maximum length of time the data prepper stores the most recent trace data to evaluvate service-map relationships.
        # The default is 3 minutes, this means we can detect relationships between services from spans reported in last 3 minutes.
        # Set higher value if your applications have higher latency.
        window_duration: 180
  buffer:
    bounded_blocking:
      # buffer_size is the number of ExportTraceRequest from otel-collector the Data Prepper should hold in memory. 
      # We recommend to keep the same buffer_size for all pipelines. 
      # Make sure you configure sufficient heap
      # default value is 512
      buffer_size: 500000
      # This is the maximum number of request each worker thread will process within the delay.
      # Default is 8.
      # Make sure buffer_size >= workers * batch_size
      batch_size: 10000
  sink:
    - opensearch:
        hosts: [ "https://opensearch:9200" ]
        index_type: trace-analytics-service-map
        # Change to your credentials
        username: admin
        password: admin_password
        # Add a certificate file if you are accessing an OpenSearch cluster with a self-signed certificate  
        #cert: /path/to/cert
        # If you are connecting to an Amazon OpenSearch Service domain without
        # Fine-Grained Access Control, enable these settings. Comment out the
        # username and password above.
        #aws_sigv4: true
        #aws_region: us-east-1

```
{% include copy.html %}

您需要為 OpenSearch 叢集修改上述組態，使組態符合您的環境。請注意，其中有兩個需要修改的 `opensearch` 接收端。
{: .note}

您必須進行下列變更：
* `hosts` – 設為您的主機。
* `username` – 提供您的 OpenSearch 使用者名稱。
* `password` – 提供您的 OpenSearch 密碼。
* `aws_sigv4` – 如果您使用 Amazon OpenSearch Service 並採用 AWS 簽署，請將此值設為 `true`。它會使用預設 AWS 憑證提供者來簽署請求。
* `aws_region` – 如果您使用 Amazon OpenSearch Service 並採用 AWS 簽署，請將此值設為您的 AWS 區域。

如需 OpenSearch 接收端的其他可用組態，請參閱 [Data Prepper OpenSearch 接收端]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/opensearch/)。

## OpenTelemetry Collector

您需要在服務環境中執行 OpenTelemetry Collector。請依照[入門](https://opentelemetry.io/docs/collector/getting-started/#getting-started)安裝 OpenTelemetry collector。請確保您為 collector 設定了指向您 Data Prepper 執行個體的 exporter。以下範例 `otel-collector-config.yaml` 檔案會接收透過各種埋點產生的資料，並將其匯出至 Data Prepper。

### 使用 Docker compose 的範例設定

以下是使用 Docker 容器執行 OpenSearch、OpenSearch Dashboards、Data Prepper 與 OpenTelemetry Collector 的範例組態。

建立您要用於 Data Prepper 的憑證，並將其儲存在 `certs` 目錄中：

```bash
mkdir -p certs

# single self-signed server cert for Data Prepper; adds SAN=DNS:data-prepper
openssl req -x509 -nodes -newkey rsa:2048 \
  -keyout certs/dp.key \
  -out    certs/dp.crt \
  -days 365 \
  -subj "/CN=data-prepper" \
  -addext "subjectAltName = DNS:data-prepper"
```
{% include copy.html %}

建立下列檔案：

`docker-compose.yaml` 檔案：


```yaml
version: "3.8"

networks:
  opensearch-net:

services:
  opensearch:
    image: opensearchproject/opensearch:3.2.0
    environment:
      - discovery.type=single-node
      - OPENSEARCH_INITIAL_ADMIN_PASSWORD=<strong_password>
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g"
    ulimits:
      memlock: { soft: -1, hard: -1 }
      nofile: { soft: 65536, hard: 65536 }
    ports:
      - "9200:9200"
      - "9600:9600"
    networks: [opensearch-net]

  dashboards:
    image: opensearchproject/opensearch-dashboards:3.2.0
    environment:
      OPENSEARCH_HOSTS: '["https://opensearch:9200"]'
      OPENSEARCH_USERNAME: admin
      # password must match OpenSearch
      OPENSEARCH_PASSWORD: "<strong_password>"   
    ports:
      - "5601:5601"
    depends_on: [opensearch]
    networks: [opensearch-net]

  data-prepper:
    image: opensearchproject/data-prepper:latest
    command: ["/usr/share/data-prepper/bin/data-prepper"]
    volumes:
      - ./pipelines:/usr/share/data-prepper/pipelines:ro
      - ./config/data-prepper-config.yaml:/usr/share/data-prepper/config/data-prepper-config.yaml:ro
      - ./certs:/usr/share/data-prepper/certs:ro
    ports:
      # Data Prepper control API (HTTP)
      - "4900:4900"
      # OTLP gRPC (TLS)
      - "21890:21890"    
    depends_on: [opensearch]
    networks: [opensearch-net]

  otel-collector:
    image: otel/opentelemetry-collector:latest
    command: ["--config=/etc/otelcol/otel-collector.yaml"]
    volumes:
      - ./otel-collector.yaml:/etc/otelcol/otel-collector.yaml:ro
    depends_on: [data-prepper]
    networks: [opensearch-net]
    ports:
      # OTLP gRPC
      - "4317:4317"
      # OTLP HTTP (optional)
      - "4318:4318"
```
{% include copy.html %}


請依照[管理員密碼要求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)設定高強度的管理員密碼。
{: .note}

`pipelines/pipelines.yaml` 檔案：

```yaml
entry-pipeline:
  source:
    otel_trace_source:
      port: 21890
      ssl: true
      sslKeyCertChainFile: "certs/dp.crt"
      sslKeyFile: "certs/dp.key"
      authentication:
        unauthenticated:
  buffer:
    bounded_blocking:
      buffer_size: 500000
      batch_size: 10000
  sink:
    - pipeline:
        name: raw-trace-pipeline
    - pipeline: 
        name: service-map-pipeline

raw-trace-pipeline:
  source:
    pipeline: 
      name: entry-pipeline
  processor:
    - otel_traces:
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: <strong_password>
        index_type: trace-analytics-raw

service-map-pipeline:
  source:
    pipeline: 
      name: entry-pipeline
  processor:
    - service_map:
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: <strong_password>
        index_type: trace-analytics-service-map
```
{% include copy.html %}

`config/data-prepper-config.yaml` 檔案：

```yaml
# Disable TLS on the Data Prepper REST API (local only)
ssl: false
serverPort: 4900

peer_forwarder:
  ssl: false
  discovery_mode: local_node
```
{% include copy.html %}

`otel-collector.yaml` 檔案：

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

exporters:
  otlp:
    endpoint: data-prepper:21890
    tls:
      # TLS is enabled, but hostname/chain is not verified
      insecure_skip_verify: true   
  # optional: see incoming/outgoing spans in logs
  debug:
    verbosity: basic

processors:
  batch: {}

extensions:
  health_check: {}

service:
  extensions: [health_check]
  telemetry:
    logs:
      level: debug
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp, debug]
```
{% include copy.html %}

使用 `docker-compose up` 命令啟動所有容器。

執行下列命令以啟動 `telemetrygen`，它會在 30 秒內產生合成的 OpenTelemetry 追蹤（約每秒 50 個 span），並透過明文 gRPC 傳送至 `otel-collector:4317`：

```bash
docker run --rm --network anton_opensearch-net \
  ghcr.io/open-telemetry/opentelemetry-collector-contrib/telemetrygen:latest \
  traces \
  --otlp-endpoint=otel-collector:4317 \
  --otlp-insecure \
  --duration=30s \
  --rate=50
```
{% include copy.html %}

這會將範例遙測資料傳送至別名 `otel-v1-apm-span`，並將文件儲存在索引 `otel-v1-apm-span-000001` 中。儲存的文件將具有下列結構：

```json
"hits": [
  {
    "_index": "otel-v1-apm-span-000001",
    "_id": "b7446942445f1f0220cc9e3707dcd7d3/153de4602f5169d3",
    "_score": 1,
    "_source": {
      "traceId": "b7446942445f1f0220cc9e3707dcd7d3",
      "droppedLinksCount": 0,
      "kind": "SPAN_KIND_CLIENT",
      "droppedEventsCount": 0,
      "traceGroupFields": {
        "endTime": "2025-11-11T12:52:42.791867180Z",
        "durationInNanos": 123000,
        "statusCode": 0
      },
      "traceGroup": "lets-go",
      "serviceName": "telemetrygen",
      "parentSpanId": "",
      "spanId": "153de4602f5169d3",
      "traceState": "",
      "name": "lets-go",
      "startTime": "2025-11-11T12:52:42.791744180Z",
      "links": [],
      "endTime": "2025-11-11T12:52:42.791867180Z",
      "droppedAttributesCount": 0,
      "durationInNanos": 123000,
      "events": [],
      "span.attributes.network@peer@address": "1.2.3.4",
      "instrumentationScope.name": "telemetrygen",
      "span.attributes.peer@service": "telemetrygen-server",
      "resource.attributes.service@name": "telemetrygen",
      "status.code": 0
    }
  },
  ...
```

在服務環境中執行 OpenTelemetry 之後，您必須設定應用程式以使用 OpenTelemetry Collector。OpenTelemetry Collector 通常與您的應用程式一同執行。

## 後續步驟與更多資訊

[OpenSearch Dashboards Observability 外掛程式]({{site.url}}{{site.baseurl}}/observability-plugin/trace/ta-dashboards/)文件提供關於設定 OpenSearch 以在 OpenSearch Dashboards 中檢視追蹤分析的更多資訊。

如需如何為追蹤分析調校與擴充 Data Prepper 的詳細資訊，請參閱[追蹤調校](#trace-tuning)。

## 遷移至 Data Prepper 2.0

從 Data Prepper 1.4 版開始，追蹤處理採用 Data Prepper 的事件模型。這讓管線作者能設定其他處理器來修改 span 或 trace。為了提供遷移途徑，Data Prepper 1.4 版引進了下列變更：

* `otel_trace_source` 有一個選用的 `record_type` 參數，可設為 `event`。設定後，它會輸出事件物件。
* `otel_traces` 取代 `otel_traces_prepper`，用於以事件為基礎的 span。
* `otel_traces_group` 取代 `otel_traces_group_prepper`，用於以事件為基礎的 span。

在 Data Prepper 2.0 版中，`otel_trace_source` 只會輸出事件。Data Prepper 2.0 版也完全移除了 `otel_traces_prepper` 和 `otel_traces_group_prepper`。若要遷移至 Data Prepper 2.0 版，您可以使用事件模型來設定您的追蹤管線。
 
