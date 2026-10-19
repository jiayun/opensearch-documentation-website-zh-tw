---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OTLP
parent: Sources
grand_parent: Pipelines
nav_order: 85
---

# OTLP 來源

`otlp` 來源是統一的 OpenTelemetry 來源，遵循 [OpenTelemetry Protocol (OTLP) 規格](https://opentelemetry.io/docs/specs/otlp/)，可透過單一端點接收記錄檔、指標與追蹤。此來源整合了個別 `otel_logs_source`、`otel_metrics_source` 與 `otel_trace_source` 來源的功能，提供更精簡的方式來匯入所有 OpenTelemetry 遙測訊號。

`otlp` 來源同時支援 `OTLP/gRPC` 與 `OTLP/HTTP` 通訊協定。對於 `OTLP/HTTP`，僅支援 Protobuf 編碼。這使其能與各式各樣的 OpenTelemetry 收集器及遙測資料蒐集程式庫相容。
{: .note}

## 組態

您可以使用下列選項來設定 `otlp` 來源。

| 選項 | 類型 | 說明 |
| :--- | :--- | :--- |
| `port` | 整數 | `otlp` 來源監聽的連接埠。預設為 `21893`。 |
| `logs_path` | 字串 | 用於傳送記錄檔未框架 HTTP 請求的路徑。必須以 `/` 開頭，且長度至少為 1。預設為 `/opentelemetry.proto.collector.logs.v1.LogsService/Export`。 |
| `metrics_path` | 字串 | 用於傳送指標未框架 HTTP 請求的路徑。必須以 `/` 開頭，且長度至少為 1。預設為 `/opentelemetry.proto.collector.metrics.v1.MetricsService/Export`。 |
| `traces_path` | 字串 | 用於傳送追蹤未框架 HTTP 請求的路徑。必須以 `/` 開頭，且長度至少為 1。預設為 `/opentelemetry.proto.collector.trace.v1.TraceService/Export`。 |
| `request_timeout` | 持續時間 | 請求逾時時間。預設為 `10s`。 |
| `retry_info` | 物件 | 設定重試行為。支援 `min_delay`（預設 `100ms`）與 `max_delay`（預設 `2s`）參數，以控制指數退避。請參閱[重試資訊](#retry-information)。|
| `health_check_service` | 布林值 | 在 `grpc.health.v1.Health/Check` 下啟用 gRPC 健康檢查服務。當 `unframed_requests` 為 `true` 時，在 `/health` 啟用 HTTP 健康檢查。預設為 `false`。 |
| `proto_reflection_service` | 布林值 | 為 Protobuf 服務啟用反射服務（請參閱 [ProtoReflectionService](https://grpc.github.io/grpc-java/javadoc/io/grpc/protobuf/services/ProtoReflectionService.html) 與 [gRPC 反射](https://github.com/grpc/grpc-java/blob/master/documentation/server-reflection-tutorial.md)）。預設為 `false`。 |
| `unframed_requests` | 布林值 | 啟用未使用 gRPC 線路通訊協定框架的請求。預設為 `false`。 |
| `thread_count` | 整數 | 排程執行緒集區中保留的執行緒數。預設為 `200`。 |
| `max_connection_count` | 整數 | 允許開啟的連線數上限。預設為 `500`。 |
| `max_request_length` | 字串 | 單一 gRPC 或 HTTP 請求承載中允許的位元組數上限。預設為 `10mb`。 |
| `compression` | 字串 | 套用至用戶端請求承載的壓縮類型。有效值為 `none`（不壓縮）或 `gzip`（套用 `gzip` 解壓縮）。預設為 `none`。 |
| `output_format` | 字串 | 若未設定個別輸出格式選項，則指定所有訊號（記錄檔、指標與追蹤）的解碼輸出格式。有效值為 `otel`（OpenTelemetry 格式）與 `opensearch`（OpenSearch 格式）。預設為 `otel`。 |
| `logs_output_format` | 字串 | 專門指定記錄檔的解碼輸出格式。對記錄檔而言，優先於 `output_format`。有效值為 `otel` 與 `opensearch`。預設為 `otel`。 |
| `metrics_output_format` | 字串 | 專門指定指標的解碼輸出格式。對指標而言，優先於 `output_format`。有效值為 `otel` 與 `opensearch`。預設為 `otel`。 |
| `traces_output_format` | 字串 | 專門指定追蹤的解碼輸出格式。對追蹤而言，優先於 `output_format`。有效值為 `otel` 與 `opensearch`。預設為 `otel`。 |

若設定了個別輸出格式（例如 `logs_output_format`），對該訊號類型而言，其優先於通用的 `output_format`。若兩者皆未設定，預設為 `otel`。
{: .note}

### SSL/TLS 組態

您可以使用下列選項在 `otlp` 來源中設定 SSL/TLS。

| 選項 | 類型 | 說明 |
| :--- | :--- | :--- |
| `ssl` | 布林值 | 啟用 SSL/TLS。預設為 `true`。 |
| `ssl_certificate_file` | 字串 | SSL 憑證鏈檔案路徑或 Amazon Simple Storage Service (Amazon S3) 路徑（例如 `s3://<bucketName>/<path>`）。若 `ssl` 設為 `true` 則為必要。 |
| `ssl_key_file` | 字串 | SSL 金鑰檔案路徑或 Amazon S3 路徑（例如 `s3://<bucketName>/<path>`）。若 `ssl` 設為 `true` 則為必要。 |
| `use_acm_cert_for_ssl` | 布林值 | 使用 AWS Certificate Manager (ACM) 的憑證與私密金鑰啟用 SSL/TLS。預設為 `false`。 |
| `acm_certificate_arn` | 字串 | ACM 憑證的 Amazon Resource Name (ARN)。ACM 憑證優先於 Amazon S3 或本機檔案系統憑證。若 `use_acm_cert_for_ssl` 設為 `true` 則為必要。 |
| `acm_private_key_password` | 字串 | 用於解密私密金鑰的 ACM 私密金鑰密碼。若未提供，OpenSearch Data Prepper 會使用未加密的私密金鑰。 |
| `aws_region` | 字串 | ACM 或 Amazon S3 使用的 AWS 區域。若 `use_acm_cert_for_ssl` 設為 `true`，或 `ssl_certificate_file` 與 `ssl_key_file` 為 Amazon S3 路徑，則為必要。 |

### 驗證組態

依預設，`otlp` 來源在未啟用驗證的情況下執行。您可以使用下列選項來設定驗證。

若要明確停用驗證，請指定下列設定：

```yaml
source:
  otlp:
    authentication:
      unauthenticated:
```
{% include copy.html %}

若要啟用 HTTP 基本驗證，請指定下列設定：

```yaml
source:
  otlp:
    authentication:
      http_basic:
        username: my-user
        password: my_s3cr3t
```
{% include copy.html %}

此外掛程式對 gRPC 伺服器使用可插拔式驗證。若要提供自訂驗證，請建立實作 [`GrpcAuthenticationProvider`](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-plugins/armeria-common/src/main/java/org/opensearch/dataprepper/armeria/authentication/GrpcAuthenticationProvider.java) 的外掛程式。

### 重試資訊

您可以使用 `retry_info` 設定來設定重試行為，指定發生背壓時等待下一個請求的時間長度。重試機制會套用指數退避，並可設定最大延遲：

```yaml
source:
  otlp:
    retry_info:
      min_delay: 100ms  # defaults to 100ms
      max_delay: 2s     # defaults to 2s
```
{% include copy.html %}

## 使用方式

下列範例示範如何在各種情境中設定及使用 `otlp` 來源。

### 基本組態

若要開始使用 `otlp` 來源，請建立包含下列最小組態的 `pipeline.yaml` 檔案：

```yaml
pipeline:
  source:
    otlp:
      ssl: false
  sink:
    - stdout:
```
{% include copy.html %}

### 路由遙測訊號

`otlp` 來源的關鍵功能之一，是能依您的特定需求，將不同的遙測訊號（記錄檔、指標與追蹤）路由至不同的處理器或接收端。路由由使用 `getEventType()` 函式的中繼資料決定：

```yaml
version: "2"
otel-telemetry:
  source:
    otlp:
      ssl: false
  route:
    - traces: 'getEventType() == "TRACE"'
    - logs: 'getEventType() == "LOG"'
    - metrics: 'getEventType() == "METRIC"'
  sink:
    - opensearch:
        routes:
          - logs
        hosts: [ "https://opensearch:9200" ]
        index: logs-%{yyyy.MM.dd}
        username: admin
        password: yourStrongPassword123!
        insecure: true
    - pipeline:
        name: traces-raw
        routes:
          - traces
    - pipeline:
        name: otel-metrics
        routes:
          - metrics

traces-raw:
  source:
    pipeline:
      name: otel-telemetry
  processor:
    - otel_trace_raw:
  sink:
    - opensearch:
        hosts: [ "https://opensearch:9200" ]
        index_type: trace-analytics-raw
        username: admin
        password: yourStrongPassword123!
        insecure: true

otel-metrics:
  source:
    pipeline:
      name: otel-telemetry
  processor:
    - otel_metrics:
        calculate_histogram_buckets: true
        calculate_exponential_histogram_buckets: true
        exponential_histogram_max_allowed_scale: 10
        flatten_attributes: false
  sink:
    - opensearch:
        hosts: [ "https://opensearch:9200" ]
        index: metrics-otel-%{yyyy.MM.dd}
        username: admin
        password: yourStrongPassword123!
        insecure: true
```
{% include copy.html %}

### 使用 OpenSearch 輸出格式

若要為所有遙測訊號產生 OpenSearch 格式的資料，請指定以下設定：

```yaml
source:
  otlp:
    output_format: opensearch
```
{% include copy.html %}

若要為不同的訊號類型使用不同的輸出格式，請指定以下設定：

```yaml
source:
  otlp:
    logs_output_format: opensearch
    metrics_output_format: otel
    traces_output_format: opensearch
```
{% include copy.html %}

### 使用 SSL/TLS 進行組態設定

若要使用本機憑證啟用 SSL/TLS，請指定以下設定：

```yaml
source:
  otlp:
    ssl: true
    ssl_certificate_file: "/path/to/certificate.crt"
    ssl_key_file: "/path/to/private-key.key"
```
{% include copy.html %}

若要使用 ACM，請指定以下設定：

```yaml
source:
  otlp:
    ssl: true
    use_acm_cert_for_ssl: true
    acm_certificate_arn: "arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012"
    aws_region: "us-east-1"
```
{% include copy.html %}

## 指標

`otlp` 來源包含下列指標，用於監控其效能與健康狀態。

### 計數器

下列計數器追蹤 `otlp` 來源中的請求活動與錯誤。

| 指標 | 說明 |
| :--- | :--- |
| `requestTimeouts` | 逾時的請求總數。 |
| `requestsReceived` | `otlp` 來源收到的請求總數。 |
| `successRequests` | `otlp` 來源成功處理的請求總數。 |
| `badRequests` | `otlp` 來源處理的格式無效請求總數。 |
| `requestsTooLarge` | 超過允許大小上限的請求總數。 |
| `internalServerError` | `otlp` 來源處理且具有自訂例外類型的請求總數。 |

### 計時器

下列計時器追蹤 `otlp` 來源中的請求活動與錯誤。

| 指標 | 說明 |
| :--- | :--- |
| `requestProcessDuration` | `otlp` 來源處理的請求延遲，單位為秒。 |

### 分佈摘要

下列分佈摘要追蹤 `otlp` 來源中的請求活動與錯誤。

| 指標 | 說明 |
| :--- | :--- |
| `payloadSize` | 傳入請求承載大小的分佈，單位為位元組。 |

## 從個別的 OpenTelemetry 來源遷移

如果您使用的是獨立的 `otel_logs_source`、`otel_metrics_source` 或 `otel_trace_source` 來源，可以依照下列步驟遷移至統一的 `otlp` 來源：

1. 將這三個來源全部替換為單一的 `otlp` 來源。
2. 使用[路由組態](#routing-telemetry-signals)將不同的訊號類型導向其適當的管線。
3. 視需要變更連接埠號碼（`otlp` 來源預設使用連接埠 `21893`）。

### 遷移範例

下列範例示範如何將個別的 OpenTelemetry 記錄檔、指標與追蹤來源整合為單一的 `otlp` 來源。

假設有一個將記錄檔、指標與追蹤分別設定的環境：

```yaml
logs-pipeline:
  source:
    otel_logs_source:
      port: 21892
  sink:
    - opensearch:
        index: logs
```
```yaml
metrics-pipeline:
  source:
    otel_metrics_source:
      port: 21891
  sink:
    - opensearch:
        index: metrics
```
```yaml
traces-pipeline:
  source:
    otel_trace_source:
      port: 21890
  sink:
    - opensearch:
        index: traces
```

您可以依照下列方式將記錄檔、指標與追蹤整合為單一的 `otlp` 來源：

```yaml
otlp-pipeline:
  source:
    otlp:
      port: 21893
  route:
    - logs: 'getEventType() == "LOG"'
    - metrics: 'getEventType() == "METRIC"'
    - traces: 'getEventType() == "TRACE"'
  sink:
    - opensearch:
        routes: 
          - logs
        index: logs
    - opensearch:
        routes:
          - metrics
        index: metrics
    - opensearch:
        routes:
          - traces
        index: traces
```
{% include copy.html %}

## 相關文件

- [OTel 記錄檔來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/otel-logs-source/)
- [OTel 指標來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/otel-metrics-source/)
- [OTel 追蹤來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/otel-trace-source/)
- [getEventType()]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/get-eventtype/)