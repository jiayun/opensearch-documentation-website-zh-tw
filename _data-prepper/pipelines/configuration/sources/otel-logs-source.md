---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OTel 記錄檔"
parent: Sources
grand_parent: Pipelines
nav_order: 60
---

# OTel logs 來源


`otel_logs_source` 來源是一種 OpenTelemetry 來源，遵循 [OpenTelemetry 協定規格](https://github.com/open-telemetry/oteps/blob/master/text/0035-opentelemetry-protocol.md)，並以 `ExportLogsServiceRequest` 記錄的形式接收來自 OTel Collector 的記錄檔。

此來源支援 `OTLP/gRPC` 協定。
{: .note}

## 組態

您可以使用下列選項來設定 `otel_logs_source` 來源。

| 選項 | 類型 | 說明 |
| :--- | :--- | :--- |
| port | 整數 | 代表 `otel_logs_source` 來源執行所在的連接埠。預設值為 `21892`。 |
| path | 字串 | 代表傳送未框架 HTTP 請求的路徑。您可以使用此選項，透過 HTTP 慣用路徑將未框架的 gRPC 請求支援到可設定的路徑。路徑應以 `/` 開頭，且長度至少為 1。若已設定路徑，則 `/opentelemetry.proto.collector.logs.v1.LogsService/Export` 端點對 gRPC 與 HTTP 請求皆停用。路徑可包含 `${pipelineName}` 佔位符，該佔位符會被替換為管線名稱。若值為空且 `unframed_requests` 為 `true`，則來源會提供路徑 `/opentelemetry.proto.collector.logs.v1.LogsService/Export`。 |
| max_request_length | 字串 | 單一 gRPC 或 HTTP 請求的酬載所允許的最大位元組數。預設值為 `10mb`。 |
| request_timeout | 整數 | 代表請求逾時時間長度（毫秒）。預設值為 `10000`。 |
| health_check_service | 布林值 | 在 `grpc.health.v1/Health/Check` 下啟用 gRPC 健康狀態檢查服務。預設值為 `false`。 |
| proto_reflection_service | 布林值 | 為 Protobuf 服務啟用反映服務（請參閱 [ProtoReflectionService](https://grpc.github.io/grpc-java/javadoc/io/grpc/protobuf/services/ProtoReflectionService.html) 與 [gRPC 反映](https://github.com/grpc/grpc-java/blob/master/documentation/server-reflection-tutorial.md)）。預設值為 `false`。 |
| unframed_requests | 布林值 | 啟用未使用 gRPC 線路協定框架化的請求。預設值為 `false`。 |
| thread_count  | 整數 | `ScheduledThreadPool` 中保留的執行緒數量。預設值為 `500`。 |
| max_connection_count | 整數 | 允許的開啟連線數量上限。預設值為 `500`。 |
| compression | 字串 | 套用至用戶端請求酬載的壓縮類型。有效值為 `none` 或 `gzip`。使用 `gzip` 可對傳入的請求套用 gzip 解壓縮。預設為 `none`（無壓縮）。 |
| output_format | 字串 | 指定所產生事件的輸出格式。有效值為 `otel` 或 `opensearch`。預設為 `opensearch`。 |

### SSL

您可以在 `otel_logs_source` 來源中使用下列選項來設定 SSL。

| 選項 | 類型 | 說明 |
| :--- | :--- | :--- |
| `ssl` | 布林值 | 啟用 TLS/SSL。預設值為 `true`。 |
| `sslKeyCertChainFile` | 字串 | 代表 SSL 憑證鏈檔案路徑或 Amazon Simple Storage Service (Amazon S3) 路徑。例如，請參閱 Amazon S3 路徑 `s3://<bucketName>/<path>`。當 `ssl` 設定為 `true` 時為必要。 |
| `sslKeyFile` | 字串 | 代表 SSL 金鑰檔案路徑或 Amazon S3 路徑。例如，請參閱 Amazon S3 路徑 `s3://<bucketName>/<path>`。當 `ssl` 設定為 `true` 時為必要。 |
| `useAcmCertForSSL` | 布林值 | 使用 AWS Certificate Manager (ACM) 的憑證與私密金鑰來啟用 TLS/SSL。預設值為 `false`。 |
| `acmCertificateArn` | 字串 | 代表 ACM 憑證的 Amazon Resource Name (ARN)。ACM 憑證的優先順序高於 Amazon S3 或本機檔案系統憑證。當 `useAcmCertForSSL` 設定為 `true` 時為必要。 |
| `awsRegion` | 字串 | 代表 ACM 或 Amazon S3 所使用的 AWS 區域。當 `useAcmCertForSSL` 設定為 `true` 或 `sslKeyCertChainFile`，或 `sslKeyFile` 為 Amazon S3 路徑時為必要。 |

## 用法

若要開始使用，請建立一個 `pipeline.yaml` 檔案，並新增 `otel_logs_source` 作為來源：

```yaml
source:
  otel_logs_source:
```
{% include copy.html %}

若要產生 OpenTelemetry 格式的資料，請將 `output_format` 設定設為 `otel`，如下列範例所示：

```yaml
source:
  otel_logs_source:
    output_format: otel
```
{% include copy.html %}

## 範例

下列管線顯示 Data Prepper 使用 PEM 憑證與金鑰透過 HTTPS 接收 OTLP 記錄檔，在自訂路徑上使用未框架 HTTP，接受 gzip 壓縮的酬載，並使用 OpenTelemetry 欄位結構描述將其編製索引至 OpenSearch：

```yaml
otel-logs-otel-output:
  source:
    otel_logs_source:
      ssl: true
      sslKeyFile: /usr/share/data-prepper/certs/dp-key.pem
      sslKeyCertChainFile: /usr/share/data-prepper/certs/dp-cert.pem
      unframed_requests: true
      path: /ingest/${pipelineName}/v1/logs
      compression: gzip
      output_format: otel
      request_timeout: 15000
      health_check_service: true
      proto_reflection_service: true
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        index: otel-logs-otel-output
        username: admin
        password: admin_pass
        insecure: true
```
{% include copy.html %}

您可以使用下列命令來測試此管線：

```bash
cat > /tmp/otel-log3.json <<'JSON'
{
  "resourceLogs": [{
    "resource": {"attributes":[
      {"key":"service.name","value":{"stringValue":"checkout"}},
      {"key":"service.version","value":{"stringValue":"1.4.2"}}
    ]},
    "scopeLogs": [{
      "scope": {"name":"manual-gzip"},
      "logRecords": [{
        "timeUnixNano": "1739999999000000000",
        "severityText": "ERROR",
        "body": {"stringValue":"payment gateway timeout"},
        "attributes":[
          {"key":"region","value":{"stringValue":"eu-west-1"}},
          {"key":"latency_ms","value":{"doubleValue":1234.5}}
        ]
      }]
    }]
  }]
}
JSON

gzip -c /tmp/otel-log3.json > /tmp/otel-log3.json.gz

curl -s -X POST "https://localhost:21892/ingest/otel-logs-otel-output/v1/logs" \
  -H 'Content-Type: application/json' \
  -H 'Content-Encoding: gzip' \
  --insecure \
  --data-binary @/tmp/otel-log3.json.gz
```
{% include copy.html %}

儲存在 OpenSearch 中的文件包含下列資訊：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "otel-logs-otel-output",
        "_id": "l24NBpoBk9xzgdmMXFDm",
        "_score": 1,
        "_source": {
          "traceId": "",
          "instrumentationScope": {
            "name": "manual-gzip",
            "droppedAttributesCount": 0
          },
          "resource": {
            "attributes": {
              "service.name": "checkout",
              "service.version": "1.4.2"
            },
            "schemaUrl": "",
            "droppedAttributesCount": 0
          },
          "flags": 0,
          "severityNumber": 0,
          "body": "payment gateway timeout",
          "schemaUrl": "",
          "spanId": "",
          "severityText": "ERROR",
          "attributes": {
            "region": "eu-west-1",
            "latency_ms": 1234.5
          },
          "time": "2025-02-19T21:19:59Z",
          "droppedAttributesCount": 0,
          "observedTimestamp": "1970-01-01T00:00:00Z"
        }
      }
    ]
  }
}
```

## 指標

您可以在 `otel_logs_source` 來源中使用下列指標。

| 選項 | 類型 | 說明 |
| :--- | :--- | :--- | 
| `requestTimeouts` | 計數器 | 測量逾時的請求總數。 | 
| `requestsReceived` | 計數器 | 測量 `otel_logs_source` 來源所接收的請求總數。 |
| `badRequests` | 計數器 | 測量無法剖析的請求總數。 |
| `requestsTooLarge` | 計數器 | 測量超過允許大小上限的請求總數。表示寫入緩衝區的資料大小超過緩衝區的最大容量。 |
| `internalServerError` | 計數器 | 測量因 `requestTimeouts` 或 `requestsTooLarge` 以外的錯誤而失敗的請求總數。 |
| `successRequests` | 計數器 | 測量成功寫入緩衝區的請求總數。 |
| `payloadSize` | 分佈摘要 | 測量所有傳入酬載大小的分佈。 |
| `requestProcessDuration` | 計時器 | 測量請求處理的持續時間。 |
