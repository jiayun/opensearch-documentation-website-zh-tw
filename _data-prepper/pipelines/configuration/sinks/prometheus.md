---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Prometheus
parent: Sinks
grand_parent: Pipelines
nav_order: 59
---

# Prometheus 輸出端

Prometheus 輸出端會緩衝 OpenTelemetry 指標，並使用 Remote Write API 以 Prometheus 時間序列格式匯出。它同時支援開源 Prometheus 與 Amazon Managed Service for Prometheus (AMP)。

`prometheus` 輸出端僅處理指標資料。所有其他資料類型都會傳送至 [DLQ 管線]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/dlq/)（若有設定）。

為確保相容性，Prometheus 輸出端會在傳送至伺服器前，先在每個批次內依時間戳記排序指標。它也支援亂序視窗，允許匯入具有較舊時間戳記的指標。

## 使用方式

下列範例針對不同的部署情境設定 Prometheus sink。

### 無驗證的開源 Prometheus

若要使用開源 Prometheus 執行個體，請提供 `https://` URL。若要使用 `http://`，請將 `insecure` 設定為 `true`。不需要 `aws` 區塊。Prometheus 必須以 `--web.enable-remote-write-receiver` 旗標啟動：

```yaml
pipeline:
  ...
  sink:
    - prometheus:
        url: "http://localhost:9090/api/v1/write"
        insecure: true
        threshold:
          max_events: 1000
          flush_interval: PT5S
```
{% include copy.html %}

### 使用 HTTP Basic 驗證的開源 Prometheus

若要使用 HTTP Basic 憑證進行驗證（例如當 Prometheus 位於啟用基本驗證的反向代理伺服器後方時），請使用 `authentication` 區塊：

```yaml
pipeline:
  ...
  sink:
    - prometheus:
        url: "https://localhost:9090/api/v1/write"
        authentication:
          http_basic:
            username: "promuser"
            password: "prompass"
```
{% include copy.html %}

### AMP

若要使用 AMP，請提供 `aws` 組態區塊。使用 AWS 驗證時需要 `https://` URL：

```yaml
pipeline:
  ...
  sink:
    - prometheus:
        url: "https://aps-workspaces.us-east-2.amazonaws.com/workspaces/ws-xxxxxxxx-xxxx/api/v1/remote_write"
        aws:
          region: "us-east-2"
          sts_role_arn: "arn:aws:iam::123456789012:role/data-prepper-prometheus-role"
        threshold:
          max_events: 1000
          flush_interval: PT5S
```
{% include copy.html %}

## IAM 權限

使用 AMP 時，請設定 AWS Identity and Access Management (IAM)，以授予 OpenSearch Data Prepper 寫入 Amazon Managed Service for Prometheus 的權限。您可以使用類似下列 JSON 組態的設定：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "amp-access",
            "Effect": "Allow",
            "Action": [
                "aps:RemoteWrite"
            ],
            "Resource": "arn:aws:aps:<region>:<account-id:workspace>/<workspace-id>"
        }
    ]
}
```
{% include copy.html %}

## 組態

自訂 `prometheus` 輸出端時，請使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`url` | 是 | 字串 | Prometheus Remote Write 端點 URL。預設支援 `https://`。若要使用 `http://`，請將 `insecure` 設定為 `true`。設定 `aws` 時，`https://` 為必要。
`insecure` | 否 | 布林值 | 設定為 `true` 時，允許 `http://` URL。預設僅允許 `https://` URL。預設值為 `false`。
`encoding` | 否 | 字串 | 請求所使用的壓縮格式。僅支援 `snappy`。預設值為 `snappy`。
`remote_write_version` | 否 | 字串 | Prometheus remote write 協定的版本。僅支援 `0.1.0`。
`content_type` | 否 | 字串 | 本文的 MIME 類型。僅支援 `application/x-protobuf`。
`out_of_order_time_window` | 否 | 持續時間 | 允許延遲抵達資料點的時間視窗。相對於最新資料點，早於此視窗的資料將被捨棄。預設值為 `10s`。
`sanitize_names` | 否 | 布林值 | 決定是否清理指標與標籤名稱，以符合 Prometheus 命名慣例。預設值為 `true`。
`connection_timeout` | 否 | 持續時間 | 建立 HTTP 連線所允許的最長時間。預設值為 `60s`。
`idle_timeout` | 否 | 持續時間 | 閒置 HTTP 連線在關閉前可保持開啟的最長時間。預設值為 `60s`。
`request_timeout` | 否 | 持續時間 | 完成整個端對端 HTTP 請求所允許的最長時間。預設值為 `60s`。
`threshold` | 否 | [閾值組態](#threshold-configuration) | 批次處理與排清時間序列資料的組態。
`max_retries` | 否 | 整數 | 匯入請求失敗時的最多嘗試次數。對於 `retryable` 狀態碼（`429`、`502`、`503` 或 `504`），會使用帶抖動的指數退避。預設值為 `5`。
`aws` | 否 | [AWS 組態](#aws-configuration) | 用於 AWS Signature Version 4 簽署的 AWS 組態。存在時，請求會以 AWS 憑證簽署。不可與 `authentication` 併用。
`authentication` | 否 | [驗證組態](#authentication-configuration) | HTTP Basic 驗證憑證。不可與 `aws` 併用。

## 閾值組態

使用下列選項設定 Prometheus sink 的批次處理與排清行為。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`max_events` | 否 | 整數 | 排清至 Prometheus 前可累積的最大事件數。預設值為 `1000`。
`max_request_size` | 否 | 字串 | 排清前請求承載的最大大小。預設值為 `1mb`。
`flush_interval` | 否 | 持續時間 | 排清事件前可等待的最長時間。預設值為 `10s`。

## AWS 組態

當存在 `aws` 區塊時，請求會自動以 Signature Version 4 簽署。需要 `https://` URL。AWS 組態支援下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`region` | 否 | 字串 | 用於憑證的 AWS 區域。預設採用[判斷區域的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串 | 對 AWS 發出請求時要擔任的 STS 角色。預設為 `null`，其使用[標準 SDK 憑證行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`sts_header_overrides` | 否 | 對應 | 擔任 IAM 角色時要套用的標頭覆寫對應。
`sts_external_id` | 否 | 字串 | 擔任 IAM 角色時可使用的選用外部 ID。

## 驗證組態

`authentication` 區塊支援 HTTP Basic 驗證。不可與 `aws`（Signature Version 4 簽署）併用。驗證組態支援下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`http_basic.username` | 是 | 字串 | HTTP Basic 驗證的使用者名稱。
`http_basic.password` | 是 | 字串 | HTTP Basic 驗證的密碼。
