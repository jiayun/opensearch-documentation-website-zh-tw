---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OTel 指標"
parent: Sources
grand_parent: Pipelines
nav_order: 70
canonical_url: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/sources/otel-metrics-source/
redirect_to: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/sources/otel-metrics-source/
---

# OTel 指標來源

`otel_metrics_source` 是收集指標資料的 OpenTelemetry Collector 來源。下表說明可用來設定 `otel_metrics_source` 來源的選項。 

## 組態

您可以使用下列選項設定 `otel_metrics_source` 來源。 

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`port` | 否 | 整數 | OpenTelemetry 指標來源執行時使用的連接埠。預設值為 `21891`。
`request_timeout` | 否 | 整數 | 請求逾時時間，以毫秒為單位。預設值為 `10000`。
`health_check_service` | 否 | 布林值 | 在 `grpc.health.v1/Health/Check` 下啟用 gRPC 健康狀態檢查服務。預設值為 `false`。
`unauthenticated_health_check` | 否 | 布林值 | 決定健康狀態檢查端點是否需要驗證。如果未定義任何驗證，OpenSearch Data Prepper 會忽略此選項。預設值為 `false`。
`proto_reflection_service` | 否 | 布林值 | 為 Protobuf 服務啟用反射服務（請參閱 [gRPC 反射](https://github.com/grpc/grpc/blob/master/doc/server-reflection.md)與 [gRPC 伺服器反射教學](https://github.com/grpc/grpc-java/blob/master/documentation/server-reflection-tutorial.md)文件）。預設值為 `false`。
`unframed_requests` | 否 | 布林值 | 啟用未使用 gRPC 線路協定進行框架封裝的請求。
`thread_count` | 否 | 整數 | 要保留在 `ScheduledThreadPool` 中的執行緒數目。預設值為 `200`。
`max_connection_count` | 否 | 整數 | 允許的開啟連線數目上限。預設值為 `500`。
`max_connection_age` | 否 | 持續時間 | 用戶端連線可保持開啟的最長時間。當連線達到此存續時間時，來源會正常關閉該連線，用戶端必須開啟新的連線。當多個 Data Prepper 節點在以 DNS 為基礎的負載平衡後方執行時，請使用此設定：gRPC 用戶端只會在開啟連線時解析 DNS，因此定期關閉連線可讓用戶端連線至新加入的節點。值必須介於 1 秒到 24 小時之間。根據預設，連線沒有存續時間上限。
`connection_drain_duration` | 否 | 持續時間 | 來源正常關閉連線時（例如連線達到 `max_connection_age` 之後），等待進行中請求完成的時間。值必須介於 0 秒到 1 小時之間。
| `output_format` | 字串 | 指定所產生事件的輸出格式。有效值為 `otel` 或 `opensearch`。預設值為 `opensearch`。 |
`max_request_length` | 否 | ByteCount | 單一 gRPC 或 HTTP 請求的承載中允許的最大位元組數。預設值為 `10mb`。
`path` | 否 | 字串 | 指標匯出服務的自訂路徑，例如 `/v1/metrics`。必須以 `/` 開頭。設定後，來源會在此路徑接收 gRPC 請求與未框架封裝的請求，且預設的 `/opentelemetry.proto.collector.metrics.v1.MetricsService/Export` 路徑會停用。路徑可包含 `${pipelineName}` 預留位置，該預留位置會替換為管線名稱。
`compression` | 否 | 字串 | 套用至用戶端請求承載的壓縮類型。有效值為 `none` 和 `gzip`。使用 `gzip` 可對傳入的請求套用 gzip 解壓縮。預設值為 `none`。
`retry_info` | 否 | 物件 | 設定來源在 `RESOURCE_EXHAUSTED` 回應中傳回給用戶端的重試延遲，例如在緩衝區已滿或請求逾時的情況下。支援 `min_delay`（預設為 `100ms`）和 `max_delay`（預設為 `2s`）選項。建議的延遲從 `min_delay` 開始，每次連續遭到拒絕時加倍，最多為 `max_delay`。
`partition_keys` | 否 | 清單 | 當管線使用儲存原始位元組的緩衝區（例如 `kafka` 緩衝區）時，用來將每個請求分割為分割區的索引鍵。有效值為 `name` 和 `service_name`。清單必須包含 `name`，也可以包含 `service_name`。接著，來源會將指標寫入依指標名稱或依服務與指標名稱分割的緩衝區。
`ssl` | 否 | 布林值 | 啟用透過 TLS/SSL 連線至 OpenTelemetry 來源連接埠。預設值為 `true`。
`sslKeyCertChainFile` | 視條件而定 | 字串 | 安全性憑證的檔案系統路徑或 Amazon Simple Storage Service (Amazon S3) 路徑（例如 `"config/demo-data-prepper.crt"` 或 `"s3://my-secrets-bucket/demo-data-prepper.crt"`）。如果 `ssl` 設為 `true`，則為必要。
`sslKeyFile` | 視條件而定 | 字串 | 安全性金鑰的檔案系統路徑或 Amazon S3 路徑（例如 `"config/demo-data-prepper.key"` 或 `"s3://my-secrets-bucket/demo-data-prepper.key"`）。如果 `ssl` 設為 `true`，則為必要。
`useAcmCertForSSL` | 否 | 布林值 | 是否使用來自 AWS Certificate Manager (ACM) 的憑證與私密金鑰啟用 TLS/SSL。預設值為 `false`。
`acmCertificateArn` | 視條件而定 | 字串 | 代表 ACM 憑證 ARN。ACM 憑證的優先順序高於 S3 或本機檔案系統憑證。如果 `useAcmCertForSSL` 設為 `true`，則為必要。
`acmPrivateKeyPassword` | 否 | 字串 | 用來解密從 ACM 匯出之私密金鑰的密碼。如果未提供，Data Prepper 會產生隨機密碼。
`acmCertIssueTimeOutMillis` | 否 | 整數 | Data Prepper 等待從 ACM 擷取憑證的最長時間，以毫秒為單位。預設值為 `120000`。
`awsRegion` | 視條件而定 | 字串 | 代表 ACM 或 Amazon S3 使用的 AWS 區域。如果 `useAcmCertForSSL` 設為 `true`，或 `sslKeyCertChainFile` 且 `sslKeyFile` 為 Amazon S3 路徑，則為必要。
`authentication` | 否 | 物件 | 驗證組態。根據預設，系統會為管線建立未經驗證的伺服器。此選項為 HTTPS 使用可插拔式驗證。若要使用基本驗證，請定義包含 `username` 和 `password` 的 `http_basic` 外掛程式。若要提供自訂驗證，請使用或建立實作 [GrpcAuthenticationProvider](https://github.com/opensearch-project/data-prepper/blob/1.2.0/data-prepper-plugins/armeria-common/src/main/java/com/amazon/dataprepper/armeria/authentication/GrpcAuthenticationProvider.java) 的外掛程式。

## 使用方式

若要使用 `otel-metrics` 來源，請建立下列 `pipeline.yaml` 檔案，並以 `otel_metrics_source` 作為來源：

```yaml
source:
    - otel_metrics_source:
```
{% include copy.html %}

若要以 OpenTelemetry 格式輸出，請將 `output_format` 設為 `otel`，如下列範例所示：

```yaml
source:
    - otel_metrics_source:
        output_format: otel
```
{% include copy.html %}


## 指標

`otel_metrics_source` 來源包含下列指標。

### 計數器

- `requestTimeouts`：測量逾時的請求總數。
- `requestsReceived`：測量 OpenTelemetry 指標來源收到的請求總數。

