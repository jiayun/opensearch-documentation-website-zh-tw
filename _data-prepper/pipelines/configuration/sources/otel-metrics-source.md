---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OTel 指標"
parent: Sources
grand_parent: Pipelines
nav_order: 70
---

# OTel 指標來源

`otel_metrics_source` 是收集指標資料的 OpenTelemetry Collector 來源。下表說明可用來設定 `otel_metrics_source` 來源的選項。 

## 組態

您可以使用下列選項設定 `otel_metrics_source` 來源。 

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`port` | 否 | 整數 | OpenTelemetry 指標來源執行時使用的連接埠。預設值為 `21891`。
`request_timeout` | 否 | 整數 | 請求逾時時間，以毫秒為單位。預設值為 `10000`。
`health_check_service` | 否 | 布林值 | 在 `grpc.health.v1/Health/Check` 下啟用 gRPC 健康檢查服務。預設值為 `false`。
`proto_reflection_service` | 否 | 布林值 | 為 Protobuf 服務啟用反射服務（請參閱 [gRPC 反射](https://github.com/grpc/grpc/blob/master/doc/server-reflection.md)與 [gRPC 伺服器反射教學](https://github.com/grpc/grpc-java/blob/master/documentation/server-reflection-tutorial.md)文件）。預設值為 `false`。
`unframed_requests` | 否 | 布林值 | 啟用未使用 gRPC 傳輸協定進行訊框封裝的請求。
`thread_count` | 否 | 整數 | 在 `ScheduledThreadPool` 中保留的執行緒數量。預設值為 `200`。
`max_connection_count` | 否 | 整數 | 允許開啟的連線數量上限。預設值為 `500`。
| `output_format` | 字串 | 指定所產生事件的輸出格式。有效值為 `otel` 或 `opensearch`。預設值為 `opensearch`。 |
`max_request_length` | 否 | ByteCount | 單一 gRPC 或 HTTP 請求的承載資料所允許的位元組數上限。預設值為 `10mb`。
`ssl` | 否 | 布林值 | 啟用透過 TLS/SSL 連線至 OpenTelemetry 來源連接埠。預設值為 `true`。
`sslKeyCertChainFile` | 視條件而定 | 字串 | 安全性憑證的檔案系統路徑或 Amazon Simple Storage Service（Amazon S3）路徑（例如 `"config/demo-data-prepper.crt"` 或 `"s3://my-secrets-bucket/demo-data-prepper.crt"`）。若 `ssl` 設為 `true`，則為必要項目。
`sslKeyFile` | 視條件而定 | 字串 | 安全性金鑰的檔案系統路徑或 Amazon S3 路徑（例如 `"config/demo-data-prepper.key"` 或 `"s3://my-secrets-bucket/demo-data-prepper.key"`）。若 `ssl` 設為 `true`，則為必要項目。
`useAcmCertForSSL` | 否 | 布林值 | 是否使用 AWS Certificate Manager（ACM）的憑證和私密金鑰來啟用 TLS/SSL。預設值為 `false`。
`acmCertificateArn` | 視條件而定 | 字串 | 代表 ACM 憑證 ARN。ACM 憑證的優先順序高於 S3 或本機檔案系統憑證。若 `useAcmCertForSSL` 設為 `true`，則為必要項目。
`awsRegion` | 視條件而定 | 字串 | 代表 ACM 或 Amazon S3 使用的 AWS 區域。若 `useAcmCertForSSL` 設為 `true`，或 `sslKeyCertChainFile` 與 `sslKeyFile` 為 Amazon S3 路徑，則為必要項目。
`authentication` | 否 | 物件 | 驗證組態。預設會為管線建立未啟用驗證的伺服器。這會使用 HTTPS 的可插拔式驗證。若要使用基本驗證，請定義 `http_basic` 外掛程式，並設定 `username` 和 `password`。若要提供自訂驗證，請使用或建立實作 [GrpcAuthenticationProvider](https://github.com/opensearch-project/data-prepper/blob/1.2.0/data-prepper-plugins/armeria-common/src/main/java/com/amazon/dataprepper/armeria/authentication/GrpcAuthenticationProvider.java) 的外掛程式。

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

