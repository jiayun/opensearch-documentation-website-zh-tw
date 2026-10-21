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

您可以使用下列選項來設定 `otel_trace_source` 來源。 

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`port` | 否 | 整數 | `otel_trace_source` 來源執行所在的連接埠。預設值為 `21890`。
`request_timeout` | 否 | 整數 | 請求逾時時間，單位為毫秒。預設值為 `10000`。
`health_check_service` | 否 | 布林值 | 在 `grpc.health.v1/Health/Check` 下啟用 gRPC 健康狀態檢查服務。預設值為 `false`。
`unauthenticated_health_check` | 否 | 布林值 | 決定健康狀態檢查端點是否需要驗證。若未定義驗證，OpenSearch Data Prepper 會忽略此選項。預設值為 `false`。
`proto_reflection_service` | 否 | 布林值 | 為 Protobuf 服務啟用反射服務（請參閱 [gRPC 反射](https://github.com/grpc/grpc/blob/master/doc/server-reflection.md) 與 [gRPC 伺服器反射教學](https://github.com/grpc/grpc-java/blob/master/documentation/server-reflection-tutorial.md) 文件）。預設值為 `false`。
`unframed_requests` | 否 | 布林值 | 啟用未使用 gRPC 線路協定框架封裝的請求。
`thread_count` | 否 | 整數 | ScheduledThreadPool 中保留的執行緒數量。預設值為 `200`。
`max_connection_count` | 否 | 整數 | 允許的最大開啟連線數。預設值為 `500`。
| `output_format` | 字串 | 指定所產生事件的輸出格式。有效值為 `otel` 或 `opensearch`。預設為 `opensearch`。 |
`max_request_length` | 否 | ByteCount | 單一 gRPC 或 HTTP 請求的酬載所允許的最大位元組數。預設值為 `10mb`。
`ssl` | 否 | 布林值 | 啟用透過 TLS/SSL 連線至 OTel 來源連接埠。預設為 `true`。
sslKeyCertChainFile | 視情況而定 | 字串 | 安全憑證的檔案系統路徑或 Amazon Simple Storage Service (Amazon S3) 路徑（例如 `"config/demo-data-prepper.crt"` 或 `"s3://my-secrets-bucket/demo-data-prepper.crt"`）。當 `ssl` 設為 `true` 時為必要。
`sslKeyFile` | 視情況而定 | 字串 | 安全金鑰的檔案系統路徑或 Amazon S3 路徑（例如 `"config/demo-data-prepper.key"` 或 `"s3://my-secrets-bucket/demo-data-prepper.key"`）。當 `ssl` 設為 `true` 時為必要。
`useAcmCertForSSL` | 否 | 布林值 | 是否使用 AWS Certificate Manager (ACM) 的憑證與私密金鑰來啟用 TLS/SSL。預設值為 `false`。
`acmCertificateArn` | 視情況而定 | 字串 | 代表 ACM 憑證 ARN。ACM 憑證的優先順序高於 S3 或本機檔案系統憑證。當 `useAcmCertForSSL` 設為 `true` 時為必要。
`awsRegion` | 視情況而定 | 字串 | 代表 ACM 或 Amazon S3 所使用的 AWS 區域。當 `useAcmCertForSSL` 設為 `true` 或 `sslKeyCertChainFile` 且 `sslKeyFile` 為 Amazon S3 路徑時為必要。
`authentication` | 否 | 物件 | 驗證組態。預設情況下，會為管線建立未經驗證的伺服器。此參數使用適用於 HTTPS 的可插拔驗證。若要使用基本驗證，請定義包含 `username` 與 `password` 的 `http_basic` 外掛程式。若要提供自訂驗證，請使用或建立實作 [GrpcAuthenticationProvider](https://github.com/opensearch-project/data-prepper/blob/1.2.0/data-prepper-plugins/armeria-common/src/main/java/com/amazon/dataprepper/armeria/authentication/GrpcAuthenticationProvider.java) 的外掛程式。

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
- `requestsTooLarge`：測量 span 數量超過緩衝區容量的請求總數。
- `internalServerError`：測量 `otel_trace` 來源以自訂例外類型處理的請求總數。

### 計時器

- `requestProcessDuration`：測量 `otel_trace` 來源外掛程式處理請求的延遲，單位為秒。

### 分佈摘要

- `payloadSize`：測量傳入請求酬載大小的分佈，單位為位元組。
