---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: HTTP
parent: Sources
grand_parent: Pipelines
nav_order: 30
redirect_from:
  - /data-prepper/pipelines/configuration/sources/http-source/
canonical_url: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/sources/http/
redirect_to: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/sources/http/
---

# HTTP 來源

`http` 外掛程式接受來自用戶端的 HTTP 請求。下表說明您可用來設定 `http` 來源的選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`port` | 否 | 整數 | 來源執行時使用的連接埠。預設值為 `2021`。有效值介於 `0` 與 `65535` 之間。
`path` | 否 | 字串 | 用於記錄匯入的 URI 路徑應以正斜線（/）開頭，例如 `/${pipelineName}/logs`。`${pipelineName}` 預留位置會被取代為管線名稱。預設值為 `/log/ingest`。
`health_check_service` | 否 | 布林值 | 在所定義連接埠的 `/health` 端點上啟用健康狀態檢查服務。預設值為 `false`。
`unauthenticated_health_check` | 否 | 布林值 | 決定健康狀態檢查端點是否需要驗證。若未定義任何驗證，OpenSearch Data Prepper 會忽略此選項。預設值為 `false`。
`request_timeout` | 否 | 整數 | 請求逾時，以毫秒為單位。預設值為 `10000`。
`thread_count` | 否 | 整數 | ScheduledThreadPool 中保留的執行緒數量。預設值為 `200`。
`max_connection_count` | 否 | 整數 | 允許的最大開啟連線數。預設值為 `500`。
`max_pending_requests` | 否 | 整數 | `ScheduledThreadPool` 工作佇列中允許的最大工作數量。預設值為 `1024`。
`max_request_length` | 否 | ByteCount | 單一 HTTP 請求承載中允許的最大位元組數。預設值為 `10mb`。
`metadata_headers` | 否 | 清單 | HTTP 請求標頭名稱的清單。來源會將這些標頭的值加入根據該請求所建立之每個事件的中繼資料。標頭名稱不區分大小寫。來源會將這些值儲存在 `headers` 中繼資料屬性中，格式為以小寫標頭名稱為鍵的對應表（map）。在單一請求中出現多次的標頭會儲存為值的清單。基於安全性考量，來源絕不會擷取 `Authorization`、`Proxy-Authorization`、`Cookie`、`Set-Cookie`、`WWW-Authenticate`、`Proxy-Authenticate`、`X-Api-Key`、`X-Csrf-Token`、`X-Xsrf-Token`、`X-Auth-Token`、`X-Amz-Security-Token` 和 `X-Amz-Credential` 標頭。當管線使用儲存原始位元組的緩衝區（例如 `kafka` 緩衝區）時，不會加入標頭。如需範例，請參閱[將請求標頭加入事件中繼資料](#adding-request-headers-to-event-metadata)。
`compression` | 否 | 字串 | 套用於用戶端請求承載的壓縮類型。有效值為 `none` 和 `gzip`。使用 `gzip` 可對包含 `Content-Encoding: gzip` 標頭的傳入請求套用 gzip 解壓縮。預設為 `none`。
`codec` | 否 | 物件 | 用於剖析請求本文的編解碼器（codec），例如 `ndjson` 或 `csv`。設定 `codec` 時，來源會為編解碼器剖析出的每一筆記錄建立一個事件。若未設定，請求本文必須是 JSON 陣列。當管線使用儲存原始位元組的緩衝區（例如 `kafka` 緩衝區）時，不會套用此選項。如需編解碼器設定，請參閱 [codec]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3/#codec)。
`authentication` | 否 | 物件 | 驗證組態。預設會為管線建立未經驗證的伺服器。此選項為 HTTPS 使用可插拔式驗證。若要使用基本驗證，請以 `username` 和 `password` 定義 `http_basic` 外掛程式。若要提供自訂驗證，請使用或建立實作 [ArmeriaHttpAuthenticationProvider](https://github.com/opensearch-project/data-prepper/blob/1.2.0/data-prepper-plugins/armeria-common/src/main/java/com/amazon/dataprepper/armeria/authentication/ArmeriaHttpAuthenticationProvider.java) 的外掛程式。
`ssl` | 否 | 布林值 | 啟用 TLS/SSL。預設值為 `false`。
`ssl_certificate_file` | 視條件而定 | 字串 | SSL 憑證鏈檔案路徑或 Amazon Simple Storage Service（Amazon S3）路徑（例如 `s3://<bucketName>/<path>`）。當 `ssl` 設為 `true` 且 `use_acm_certificate_for_ssl` 設為 `false` 時為必要。
`ssl_key_file` | 視條件而定 | 字串 | SSL 金鑰檔案路徑或 Amazon S3 路徑（例如 `s3://<bucketName>/<path>`）。當 `ssl` 設為 `true` 且 `use_acm_certificate_for_ssl` 設為 `false` 時為必要。
`use_acm_certificate_for_ssl` | 否 | 布林值 | 使用來自 AWS Certificate Manager（ACM）的憑證與私密金鑰啟用 TLS/SSL。預設為 `false`。
`acm_certificate_arn` | 視條件而定 | 字串 | ACM 憑證的 Amazon Resource Name（ARN）。ACM 憑證的優先順序高於 Amazon S3 或本機檔案系統中的憑證。當 `use_acm_certificate_for_ssl` 設為 true 時為必要。
`acm_private_key_password` | 否 | 字串 | 用於解密私密金鑰的 ACM 私密金鑰密碼。若未提供，Data Prepper 會產生隨機密碼。
`acm_certificate_timeout_millis` | 否 | 整數 | ACM 取得憑證的逾時時間，以毫秒為單位。預設值為 120000。
`aws_region` | 視條件而定 | 字串 | ACM 或 Amazon S3 使用的 AWS 區域。當 `use_acm_certificate_for_ssl` 設為 true，或 `ssl_certificate_file` 與 `ssl_key_file` 為 Amazon S3 路徑時為必要。

<!--- ## Configuration

Content will be added to this section.--->

## 匯入

用戶端應將 HTTP `POST` 請求傳送至端點 `/log/ingest`。

根據預設，`http` 來源接受包含物件陣列的 JSON UTF-8 請求本文，例如 `[{"key1": "value1"}, {"key2": "value2"}]`。若要接受其他格式，請設定 `codec`。

## 範例

下列範例示範可與 `http` 來源搭配使用的不同組態。

### 最小 HTTP 來源

以下是使用所有預設值的最小組態：

```yaml
minimal-http-pipeline:
  source:
    http:
  sink:
    - stdout: {}
```
{% include copy.html %}

您可以使用下列命令測試此管線：

```bash
curl -s "http://localhost:2021/log/ingest" \
  -H "Content-Type: application/json" \
  --data '[{"msg":"one"},{"msg":"two"}]'
```
{% include copy.html %}

您應該會在 Data Prepper 記錄檔中看到下列輸出：

```
{"msg":"one"}
{"msg":"two"}
```

### 使用管線名稱和健康狀態檢查的自訂路徑

下列範例使用自訂路徑、設定自訂連接埠，並啟用健康狀態檢查：

```yaml
audit-pipeline:
  source:
    http:
      port: 2022
      path: "/${pipelineName}/logs"  # -> /audit-pipeline/logs
      health_check_service: true
      unauthenticated_health_check: true
  sink:
    - stdout: {}
```
{% include copy.html %}

您可以使用下列命令檢查管線健康狀態：

```bash
curl -s "http://localhost:2022/health"
```
{% include copy.html %}

您可以使用下列命令匯入資料：

```bash
curl -s "http://localhost:2022/audit-pipeline/logs" \
  -H "Content-Type: application/json" \
  --data '[{"event":"login","user":"alice"}]'
```
{% include copy.html %}

### 來源上的基本驗證

下列範例設定自訂連接埠和路徑、啟用健康狀態檢查，並設定基本驗證：

```yaml
secure-intake-pipeline:
  source:
    http:
      port: 2023
      path: /ingest
      authentication:
        http_basic:
          username: ingest
          password: s3cr3t
      health_check_service: true
      unauthenticated_health_check: true
  sink:
    - stdout: {}
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: "<custom-admin-password>"
        index_type: custom
        index: demo-%{yyyy.MM.dd}
```
{% include copy.html %}

您可以使用下列命令測試此管線：

```bash
curl -s -u ingest:s3cr3t "http://localhost:2023/ingest" \
  -H "Content-Type: application/json" \
  --data '[{"service":"web","status":"ok"}]'
```
{% include copy.html %}

### 將請求標頭新增至事件中繼資料

下列範例會將 `X-Tenant-Id` 請求標頭新增至每個事件的中繼資料，然後使用 `add_entries` 處理器將標頭值複製到 `tenant` 欄位。若要讀取單一標頭，請使用 `headers/<lowercase-header-name>` 中繼資料索引鍵：

```yaml
tenant-pipeline:
  source:
    http:
      metadata_headers: ["X-Tenant-Id"]
  processor:
    - add_entries:
        entries:
          - key: tenant
            value_expression: 'getMetadata("headers/x-tenant-id")'
  sink:
    - stdout: {}
```
{% include copy.html %}

您可以使用下列命令測試此管線：

```bash
curl -s "http://localhost:2021/log/ingest" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: store-eu" \
  --data '[{"order":"1001"}]'
```
{% include copy.html %}

您應該會在 Data Prepper 記錄檔中看到下列輸出：

```
{"order":"1001","tenant":"store-eu"}
```

## 指標

`http` 來源包含下列指標。

### 計數器

- `requestsReceived`：測量 `/log/ingest` 端點接收的請求總數。
- `requestsRejected`：測量 HTTP 來源外掛程式拒絕的請求總數（429 回應狀態碼）。
- `successRequests`：測量 HTTP 來源外掛程式成功處理的請求總數（200 回應狀態碼）。
- `badRequests`：測量 HTTP 來源外掛程式處理的內容類型或格式無效的請求總數（400 回應狀態碼）。
- `requestTimeouts`：測量 HTTP 來源伺服器中逾時的請求總數（415 回應狀態碼）。
- `requestsTooLarge`：測量事件大小大於緩衝區容量的請求總數（413 回應狀態碼）。
- `internalServerError`：測量 HTTP 來源處理時發生自訂例外狀況類型的請求總數（500 回應狀態碼）。

### 計時器

- `requestProcessDuration`：測量 HTTP 來源外掛程式處理之請求的延遲，以秒為單位。

### 分佈摘要

- `payloadSize`：測量傳入請求承載的大小，以位元組為單位。
