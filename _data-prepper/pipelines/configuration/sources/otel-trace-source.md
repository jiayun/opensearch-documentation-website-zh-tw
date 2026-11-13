---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OTel 追蹤"
parent: Sources
grand_parent: Pipelines
nav_order: 80
redirect_from:
  - /data-prepper/pipelines/configuration/sources/otel-trace/
---


# OTel 追蹤來源 

`otel_trace_source` 是 OpenTelemetry Collector 的來源。下表說明您可用來設定 `otel_trace_source` 來源的選項。

## 組態

您可以使用下列選項設定 `otel_trace_source` 來源。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`port` | 否 | 整數 | `otel_trace_source` 來源執行時使用的連接埠。預設值為 `21890`。
`request_timeout` | 否 | 整數 | 請求逾時時間，以毫秒為單位。預設值為 `10000`。
`health_check_service` | 否 | 布林值 | 在 `grpc.health.v1/Health/Check` 下啟用 gRPC 健康檢查服務。預設值為 `false`。
`unauthenticated_health_check` | 否 | 布林值 | 決定健康檢查端點是否需要驗證。若未定義驗證，OpenSearch Data Prepper 會忽略此選項。預設值為 `false`。
`proto_reflection_service` | 否 | 布林值 | 為 Protobuf 服務啟用反射服務（請參閱 [gRPC 反射](https://github.com/grpc/grpc/blob/master/doc/server-reflection.md)與 [gRPC 伺服器反射教學](https://github.com/grpc/grpc-java/blob/master/documentation/server-reflection-tutorial.md)文件）。預設值為 `false`。
`unframed_requests` | 否 | 布林值 | 啟用未以 gRPC 線路協定封裝的請求。
`thread_count` | 否 | 整數 | ScheduledThreadPool 中保留的執行緒數量。預設值為 `200`。
`max_connection_count` | 否 | 整數 | 允許的最大開啟連線數。預設值為 `500`。
`max_connection_age` | 否 | 持續時間 | 用戶端連線可保持開啟的最長時間。當連線達到此存續時間時，來源會正常關閉該連線，用戶端必須開啟新連線。當多個 Data Prepper 節點在以 DNS 為基礎的負載平衡後方執行時，請使用此設定：gRPC 用戶端只會在開啟連線時解析 DNS，因此定期關閉連線可讓用戶端連線至新加入的節點。必須介於 1 秒到 24 小時之間。預設情況下，連線沒有最長存續時間。
`connection_drain_duration` | 否 | 持續時間 | 來源正常關閉連線時（例如連線達到 `max_connection_age` 之後），等待處理中請求完成的時間長度。必須介於 0 秒到 1 小時之間。
| `output_format` | 字串 | 指定所產生事件的輸出格式。有效值為 `otel` 或 `opensearch`。預設為 `opensearch`。 |
`max_request_length` | 否 | ByteCount | 單一 gRPC 或 HTTP 請求的承載中允許的最大位元組數。預設值為 `10mb`。
`path` | 否 | 字串 | 追蹤匯出服務的自訂路徑，例如 `/v1/traces`。必須以 `/` 開頭。設定後，來源會在此路徑接收 gRPC 及未封裝的請求，並停用預設的 `/opentelemetry.proto.collector.trace.v1.TraceService/Export` 路徑。路徑可包含 `${pipelineName}` 預留位置，該預留位置會替換為管線名稱。
`compression` | 否 | 字串 | 套用於用戶端請求承載的壓縮類型。有效值為 `none` 與 `gzip`。使用 `gzip` 可對傳入的請求套用 gzip 解壓縮。預設為 `none`。
`retry_info` | 否 | 物件 | 設定來源在 `RESOURCE_EXHAUSTED` 回應中傳回給用戶端的重試延遲，例如在緩衝區已滿或請求逾時時。支援 `min_delay`（預設 `100ms`）與 `max_delay`（預設 `2s`）選項。建議的延遲從 `min_delay` 開始，每次連續拒絕時加倍，最多至 `max_delay`。
`ssl` | 否 | 布林值 | 啟用透過 TLS/SSL 連線至 OTel 來源連接埠。預設為 `true`。
sslKeyCertChainFile | 視條件而定 | 字串 | 安全性憑證的檔案系統路徑或 Amazon Simple Storage Service (Amazon S3) 路徑（例如 `"config/demo-data-prepper.crt"` 或 `"s3://my-secrets-bucket/demo-data-prepper.crt"`）。若 `ssl` 設為 `true`，則為必要。
`sslKeyFile` | 視條件而定 | 字串 | 安全性金鑰的檔案系統路徑或 Amazon S3 路徑（例如 `"config/demo-data-prepper.key"` 或 `"s3://my-secrets-bucket/demo-data-prepper.key"`）。若 `ssl` 設為 `true`，則為必要。
`useAcmCertForSSL` | 否 | 布林值 | 是否使用來自 AWS Certificate Manager (ACM) 的憑證與私密金鑰啟用 TLS/SSL。預設值為 `false`。
`acmCertificateArn` | 視條件而定 | 字串 | 代表 ACM 憑證 ARN。ACM 憑證的優先順序高於 S3 或本機檔案系統憑證。若 `useAcmCertForSSL` 設為 `true`，則為必要。
`acmPrivateKeyPassword` | 否 | 字串 | 用於解密從 ACM 匯出之私密金鑰的密碼。若未提供，Data Prepper 會產生隨機密碼。
`acmCertIssueTimeOutMillis` | 否 | 整數 | Data Prepper 等待從 ACM 擷取憑證的最長時間，以毫秒為單位。預設值為 `120000`。
`awsRegion` | 視條件而定 | 字串 | 代表 ACM 或 Amazon S3 使用的 AWS 區域。若 `useAcmCertForSSL` 設為 `true`，或 `sslKeyCertChainFile` 與 `sslKeyFile` 為 Amazon S3 路徑，則為必要。
`authentication` | 否 | 物件 | 驗證組態。預設情況下，會為管線建立未經驗證的伺服器。此參數對 HTTPS 使用可插拔式驗證。若要使用基本驗證，請以 `username` 與 `password` 定義 `http_basic` 外掛程式。若要提供自訂驗證，請使用或建立實作 [GrpcAuthenticationProvider](https://github.com/opensearch-project/data-prepper/blob/1.2.0/data-prepper-plugins/armeria-common/src/main/java/com/amazon/dataprepper/armeria/authentication/GrpcAuthenticationProvider.java) 的外掛程式。

## 用法

若要使用 `otel-metrics` 來源，請建立下列 `pipeline.yaml` 檔案，並以 `otel_metrics_source` 作為來源：

```yaml
source:
  otel_trace_source:
```
{% include copy.html %}

若您想讓輸出使用 OpenTelemetry 格式，請將 `output_format` 設為 `otel`，如下列範例所示：

```yaml
source:
  otel_trace_source:
    output_format: otel
```
{% include copy.html %}

## 範例

下列範例顯示 Data Prepper 透過 HTTPS 使用 PEM 憑證與金鑰，以自訂路徑上的未框架 HTTP 匯入 OTLP 追蹤、接受 gzip 壓縮的酬載、保留 OpenTelemetry 文件結構，並將其編製索引至 OpenSearch：

```yaml
otel-traces-https:
  source:
    otel_trace_source:
      ssl: true
      sslKeyFile: /usr/share/data-prepper/certs/dp-key.pem
      sslKeyCertChainFile: /usr/share/data-prepper/certs/dp-cert.pem
      unframed_requests: true
      path: /ingest/${pipelineName}/v1/traces
      compression: gzip
      output_format: otel
      request_timeout: 15000
      health_check_service: true
      proto_reflection_service: true
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        index: otel-traces-https
        username: admin
        password: "<custom-admin-password>"
        insecure: true
```
{% include copy.html %}

您可以使用下列命令來測試管線：

```bash
cat > /tmp/otel-trace3.json <<'JSON'
{
  "resourceSpans": [{
    "resource": {"attributes":[
      {"key":"service.name","value":{"stringValue":"billing"}},
      {"key":"service.version","value":{"stringValue":"2.1.0"}}
    ]},
    "scopeSpans": [{
      "scope": {"name":"manual-https"},
      "spans": [{
        "traceId": "1234567890abcdef1234567890abcdef",
        "spanId":  "feedfacecafebeef",
        "name": "PUT /invoice/42",
        "startTimeUnixNano": "1739999999000000000",
        "endTimeUnixNano":   "1740000000000000000",
        "attributes": [
          {"key":"region","value":{"stringValue":"eu-west-1"}},
          {"key":"retry.count","value":{"intValue":"1"}}
        ]
      }]
    }]
  }]
}
JSON

gzip -c /tmp/otel-trace3.json > /tmp/otel-trace3.json.gz

curl -s -X POST "https://localhost:21890/ingest/otel-traces-https/v1/traces" \
  -H 'Content-Type: application/json' \
  -H 'Content-Encoding: gzip' \
  --insecure \
  --data-binary @/tmp/otel-trace3.json.gz
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
        "_index": "otel-traces-https",
        "_id": "V_5RBpoBqZ1V_u-TvYXf",
        "_score": 1,
        "_source": {
          "traceId": "d76df8e7aefcf7469b71d79fd76df8e7aefcf7469b71d79f",
          "droppedLinksCount": 0,
          "instrumentationScope": {
            "name": "manual-https",
            "droppedAttributesCount": 0
          },
          "resource": {
            "schemaUrl": "",
            "attributes": {
              "service.name": "billing",
              "service.version": "2.1.0"
            },
            "droppedAttributesCount": 0
          },
          "kind": "SPAN_KIND_UNSPECIFIED",
          "droppedEventsCount": 0,
          "flags": 0,
          "parentSpanId": "",
          "schemaUrl": "",
          "spanId": "7de79d7da71e71a7de6de79f",
          "traceState": "",
          "name": "PUT /invoice/42",
          "startTime": "2025-02-19T21:19:59Z",
          "attributes": {
            "retry.count": 1,
            "region": "eu-west-1"
          },
          "links": [],
          "endTime": "2025-02-19T21:20:00Z",
          "droppedAttributesCount": 0,
          "durationInNanos": 1000000000,
          "events": [],
          "status": {
            "code": 0,
            "message": ""
          }
        }
      }
    ]
  }
}
```

## 指標

`otel_trace_source` 來源包含下列指標。

### 計數器

- `requestTimeouts`：測量逾時的請求總數。
- `requestsReceived`：測量 `otel_trace` 來源收到的請求總數。
- `successRequests`：測量 `otel_trace` 來源外掛程式成功處理的請求總數。
- `badRequests`：測量 `otel_trace` 來源外掛程式處理的格式無效請求總數。
- `requestsTooLarge`：測量追蹤區段（span）數量超過緩衝區容量的請求總數。
- `internalServerError`：測量 `otel_trace` 來源以自訂例外類型處理的請求總數。

### 計時器

- `requestProcessDuration`：測量 `otel_trace` 來源外掛程式處理請求的延遲，單位為秒。

### 分佈摘要

- `payloadSize`：測量傳入請求酬載大小的分佈，單位為位元組。
