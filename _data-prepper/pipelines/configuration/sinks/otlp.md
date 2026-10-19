---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OTLP
parent: Sinks
grand_parent: Pipelines
nav_order: 52
---

# OTLP 接收端

這是一項實驗性功能，不建議在正式環境中使用。若要了解此功能的進度或提供意見回饋，請參閱 OpenSearch Data Prepper 儲存庫中的 [`otlp` sink 外掛程式](https://github.com/opensearch-project/data-prepper/tree/main/data-prepper-plugins/otlp-sink)。
{: .warning}

`otlp` sink 會將追蹤、指標與記錄資料匯出至透過 HTTP 接受 [OpenTelemetry Protocol (OTLP)](https://opentelemetry.io/docs/specs/otlp/) 請求的端點。它會將每個批次編碼為 Protobuf，使用 `gzip` 壓縮，並以 AWS Signature Version 4 (SigV4) 簽署請求。若要將資料傳送至接受 SigV4 簽署請求的端點，請將 `service_name` 設定為該端點的簽署名稱。由於此 sink 會簽署每個請求且需要 AWS 憑證，因此專為使用 AWS 驗證的端點而設計。

此 sink 會根據事件的類型判斷每個事件的訊號類型：跨度 (span) 事件會匯出為 OTLP 追蹤資料，指標事件會匯出為指標資料，記錄事件則會匯出為記錄資料。此 sink 僅接受跨度、指標與記錄事件，例如 [`otlp` 來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/otlp-source/)所產生的事件。任何其他事件都會被捨棄，並計入 `failedRecordsCount` 指標。

此 sink 會為每種訊號類型維護一個獨立的緩衝區，因此每種訊號類型會各自獨立批次處理。每個請求包含單一訊號類型的一批事件，並依照[閾值組態](#threshold-configuration)組裝。一個批次可以包含來自多個追蹤的跨度，而單一追蹤的跨度也可以透過不同的請求傳送。

每個 sink 會將所有訊號傳送至 `endpoint` 中設定的單一 URL。由於 OTLP/HTTP 端點會為每種訊號使用不同的路徑（`/v1/traces`、`/v1/metrics` 與 `/v1/logs`），因此請為每種訊號設定一個 `otlp` sink，並在管線承載多種訊號類型時使用[條件路由]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines#conditional-routing)。範例請參閱[路由混合訊號類型](#routing-mixed-signal-types)。

## 必要條件

若要使用 `otlp` sink，請在 `data-prepper-config.yaml` 中啟用實驗性的 `otlp` 外掛程式：

```yaml
experimental:
  enabled_plugins:
    sink:
      - otlp
```
{% include copy.html %}

## 用法

下列範例針對不同情境設定 `otlp` sink。

### 將追蹤傳送至 AWS X-Ray

下列管線會將 span 傳送至 AWS X-Ray OTLP 端點。由於端點主機名稱包含區域，因此可以省略 `aws.region`：

```yaml
trace-pipeline:
  source:
    otlp:
      ssl: false
  sink:
    - otlp:
        endpoint: "https://xray.us-east-1.amazonaws.com/v1/traces"
        aws:
          sts_role_arn: "arn:aws:iam::123456789012:role/data-prepper-otlp-role"
```
{% include copy.html %}

### 設定自訂簽署值與標頭

下列管線會將記錄資料傳送至接受 SigV4 簽署請求但並非 AWS X-Ray 的端點。它將 `service_name` 設定為端點的 Signature Version 4 簽署名稱，由於端點主機名稱不包含區域，因此明確設定 `aws.region`，並為每個請求新增自訂標頭：

```yaml
log-pipeline:
  source:
    http:
      port: 2021
      path: "/logs"
  sink:
    - otlp:
        endpoint: "https://my-otlp-endpoint.example.com:443/v1/logs"
        service_name: "my-service"
        max_retries: 3
        threshold:
          max_events: 100
          flush_timeout: 5s
        aws:
          region: "us-east-1"
          sts_role_arn: "arn:aws:iam::123456789012:role/data-prepper-otlp-role"
        additional_headers:
          x-custom-header: "my-value"
```
{% include copy.html %}

### 路由混合訊號類型

下列管線會從 [`otlp` 來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/otlp-source/)接收全部三種訊號類型，並將每種訊號路由至設定了對應訊號路徑的 sink：

```yaml
otlp-pipeline:
  source:
    otlp:
      ssl: false
  route:
    - traces: 'getEventType() == "TRACE"'
    - metrics: 'getEventType() == "METRIC"'
    - logs: 'getEventType() == "LOG"'
  sink:
    - otlp:
        routes:
          - traces
        endpoint: "https://xray.us-east-1.amazonaws.com/v1/traces"
        aws:
          region: "us-east-1"
    - otlp:
        routes:
          - metrics
        endpoint: "https://my-otlp-endpoint.example.com/v1/metrics"
        service_name: "my-service"
        aws:
          region: "us-east-1"
    - otlp:
        routes:
          - logs
        endpoint: "https://my-otlp-endpoint.example.com/v1/logs"
        service_name: "my-service"
        aws:
          region: "us-east-1"
```
{% include copy.html %}

## 組態

使用下列選項來設定 `otlp` sink。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`endpoint` | 是 | 字串 | OTLP/HTTP 端點 URL，包含訊號路徑，例如 `https://xray.us-east-1.amazonaws.com/v1/traces`。
`aws` | 是 | [AWS 組態](#aws-configuration) | 用於 SigV4 簽署的 AWS 組態。所有請求都會被簽署，因此此區塊必須存在，即使它是空的。
`service_name` | 否 | 字串 | 請求所使用的 SigV4 簽署名稱，例如 `logs` 或 `osis`。預設為 `xray`。
`max_retries` | 否 | 整數 | 失敗請求的最大重試次數。此 sink 會使用帶抖動的指數退避策略重試 `429`、`502`、`503` 與 `504` 狀態碼。預設為 `5`。
`threshold` | 否 | [閾值組態](#threshold-configuration) | 批次處理與排清組態。
`additional_headers` | 否 | 對應 | 新增至每個請求的 HTTP 標頭。預設為空的對應。

此版本必須提供 `aws` 區塊。尚未支援不使用 Signature Version 4 簽署的 OTLP 端點。
{: .note}

`additional_headers` 中的標頭會在請求簽署後新增，因此不屬於 Signature Version 4 簽章的一部分。為了保持簽署有效，此 sink 會拒絕 `Authorization`、`Host`、`Content-Type`、`Content-Encoding` 與 `Content-Length` 標頭，以及任何名稱以 `x-amz-` 開頭的標頭。設定其中任一標頭的管線將無法啟動。
{: .note}

## 閾值組態

當達到任一閾值時，此 sink 便會排清批次。使用下列選項來設定批次處理與排清。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`max_events` | 否 | 整數 | 一個批次中的最大事件數。設定為 `0` 可僅依據 `max_batch_size` 與 `flush_timeout` 排清。預設為 `512`。
`max_batch_size` | 否 | 字串 | 未壓縮批次酬載的最大大小。預設為 `1mb`。
`flush_timeout` | 否 | 持續時間 | 排清批次前的最長等待時間。必須至少為 `1ms`。預設為 `200ms`。

此 sink 會將 HTTP 回應逾時設定為 `flush_timeout` 值的兩倍，範圍介於 3 到 10 秒之間。當 `flush_timeout` 為 1.5 秒或更短時，回應逾時為 3 秒。當 `flush_timeout` 介於 1.5 到 5 秒之間時，回應逾時為 `flush_timeout` 的兩倍。當 `flush_timeout` 為 5 秒或更長時，回應逾時為 10 秒。
{: .note}

每種訊號類型都使用自己的事件佇列，等待批次處理。佇列容量為 `max_events` 的 10 倍，最少 2,000 個事件，因此當您增加 `max_events` 時，佇列會隨之成長。當佇列已滿時，此 sink 會對管線施加背壓，而不會捨棄事件。

## AWS 組態

使用 `aws` 區塊中的下列選項來設定憑證與簽署。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`region` | 否 | 字串 | 用於 SigV4 簽署與憑證的 AWS 區域。若未指定，此 sink 會從 `endpoint` 中的主機名稱解析區域，若主機名稱不包含有效的區域，則會在啟動時失敗。
`sts_role_arn` | 否 | 字串 | 請求所擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null`，它會使用[預設憑證提供者鏈](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`sts_external_id` | 否 | 字串 | 擔任 AWS STS 角色時使用的外部 ID。

## 限制

`otlp` sink 有下列限制：

- 追蹤只能傳送至與 AWS X-Ray 相容的端點（`https://xray.<region>.amazonaws.com/v1/traces`）。指標與記錄資料可以傳送至任何接受 SigV4 簽署 Protobuf 請求的 OTLP 端點。
- 僅支援透過 HTTP 的 OTLP。不支援透過 gRPC 的 OTLP。
- 當 `max_retries` 中設定的重試次數用盡時，該批次會被捨棄，並記錄與計入失敗。由於此 sink 會在收到可重試的狀態碼後重試批次，因此端點可能會收到同一批次多次。不支援死信佇列 (DLQ) 傳送。

## 指標

`otlp` sink 除了[常見 sink 指標]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/monitoring/)之外，還提供下列指標。

### 計數器

下列計數器會追蹤 `otlp` sink 所處理的記錄與回應。

指標 | 說明
:--- | :---
`recordsOut` | 端點接受的記錄數。
`rejectedRecordsCount` | 端點拒絕或無法傳送的記錄數。
`failedRecordsCount` | 此 sink 無法處理的記錄數，包括非跨度、指標或記錄的事件。
`rejectedSpansCount`、`rejectedMetricsCount`、`rejectedLogsCount` | 每種訊號類型被拒絕的記錄數。
`failedSpansCount`、`failedMetricsCount`、`failedLogsCount` | 每種訊號類型失敗的記錄數。
`errorsCount` | 非預期的工作執行緒錯誤數。
`http2xxResponses`、`http4xxResponses`、`http5xxResponses` | 每個狀態碼類別收到的回應數。

### 計時器

下列計時器會追蹤 `otlp` sink 中的請求延遲。

指標 | 說明
:--- | :---
`httpLatency` | 從端點接收回應所花費的時間。

### 分布摘要

下列分布摘要會追蹤 `otlp` sink 中的酬載大小。

指標 | 說明
:--- | :---
`payloadSize` | 未壓縮請求酬載大小的分布，單位為位元組。
`payloadGzipSize` | `gzip` 壓縮請求酬載大小的分布，單位為位元組。

### 量測計

下列量測計會追蹤 `otlp` sink 中每種訊號類型的佇列。

指標 | 說明
:--- | :---
`queueSize` | 等待傳送的事件數。
`queueCapacity` | 佇列的總容量。

## 相關文件

- [OTLP 來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/otlp-source/)
- [getEventType()]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/get-eventtype/)
- [條件路由]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines#conditional-routing)
