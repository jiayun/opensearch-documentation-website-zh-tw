---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Prometheus
parent: Sinks
grand_parent: Pipelines
nav_order: 59
---

# Prometheus 接收器

這是實驗性功能，不建議在正式環境中使用。若要了解此功能的最新進度或提供意見回饋，請參閱 OpenSearch Data Prepper 儲存庫中的 [`prometheus` 接收器外掛程式](https://github.com/opensearch-project/data-prepper/tree/main/data-prepper-plugins/prometheus-sink)。
{: .warning}

Prometheus 接收器 (sink) 會緩衝 OpenTelemetry 指標，並使用 Remote Write API 將指標以 Prometheus 時間序列格式匯出。它同時支援開放原始碼的 Prometheus 與 Amazon Managed Service for Prometheus (AMP)。

`prometheus` 接收器只處理指標資料。若已設定 [DLQ 管線]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/dlq/)，所有其他資料類型都會傳送至該管線。

為確保相容性，Prometheus 接收器會先在每個批次內依時間戳記排序指標，再將其傳送至伺服器。它也支援亂序時間窗口 (out-of-order window)，可讓您匯入時間戳記較舊的指標。

## 先決條件

若要使用 `prometheus` 接收器 (sink)，請在 `data-prepper-config.yaml` 中啟用實驗性的 `prometheus` 外掛程式：

```yaml
experimental:
  enabled_plugins:
    sink:
      - prometheus
```
{% include copy.html %}

## 使用方式

下列範例針對不同的部署情境設定 Prometheus 接收器。

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

若要使用 HTTP Basic 認證資訊進行驗證（例如當 Prometheus 位於啟用基本驗證的反向代理伺服器後方時），請使用 `authentication` 區塊：

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

自訂 `prometheus` 接收器 (sink) 時，請使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`url` | 是 | 字串 | Prometheus Remote Write 端點 URL。預設支援 `https://`。若要使用 `http://`，請將 `insecure` 設為 `true`。設定 `aws` 時，`https://` 為必要項目。
`insecure` | 否 | 布林值 | 設為 `true` 時，允許使用 `http://` URL。預設僅允許 `https://` URL。預設值為 `false`。
`encoding` | 否 | 字串 | 請求所使用的壓縮格式。僅支援 `snappy`。預設值為 `snappy`。
`remote_write_version` | 否 | 字串 | Prometheus remote write 通訊協定的版本。僅支援 `0.1.0`。
`content_type` | 否 | 字串 | 本文的 MIME 類型。僅支援 `application/x-protobuf`。
`out_of_order_time_window` | 否 | 持續時間 | 允許延遲抵達之資料點的時間範圍。相對於最新的資料點，早於此時間範圍的資料將被捨棄。預設值為 `10s`。
`sanitize_names` | 否 | 布林值 | 決定是否清理指標名稱與標籤名稱，以符合 Prometheus 命名慣例。預設值為 `true`。
`instance_label` | 否 | 字串 | 標籤的名稱，用於在接收器寫入的每個時間序列中識別 Data Prepper 執行個體。當多個執行個體執行相同的管線時，請使用此選項。如需更多資訊，請參閱[執行個體標籤](#instance-label)。預設不會新增執行個體標籤。
`connection_timeout` | 否 | 持續時間 | 建立 HTTP 連線所允許的最長時間。必須介於 1 到 600 秒之間。預設值為 `60s`。
`idle_timeout` | 否 | 持續時間 | 閒置的 HTTP 連線在關閉前保持開啟的最長時間。必須介於 1 到 600 秒之間。預設值為 `60s`。
`request_timeout` | 否 | 持續時間 | 完整端對端 HTTP 請求完成所允許的最長時間。必須介於 1 到 600 秒之間。預設值為 `60s`。
`threshold` | 否 | [閾值組態](#threshold-configuration) | 用於批次處理及排清時間序列資料的組態。
`max_retries` | 否 | 整數 | 匯入請求失敗時的最大嘗試次數。遇到 `retryable` 狀態碼（`429`、`502`、`503` 或 `504`）時，會使用含隨機抖動 (jitter) 的指數退避。預設值為 `5`。
`aws` | 否 | [AWS 組態](#aws-configuration) | 用於 AWS Signature Version 4 簽署的 AWS 組態。若有提供，請求會使用 AWS 認證資訊進行簽署。不可與 `authentication` 搭配使用。
`authentication` | 否 | [驗證組態](#authentication-configuration) | HTTP Basic 驗證的認證資訊。不可與 `aws` 搭配使用。

## 執行個體標籤

當多個 Data Prepper 執行個體執行相同的管線組態時，它們會寫入相同的時間序列，而 Remote Write 端點對每個序列與時間戳記只會保留一個樣本。若要保留每個執行個體的樣本，請將 `instance_label` 設定為一個標籤名稱。接收器 (sink) 會將此標籤新增至其寫入的每個時間序列。標籤值是主機身分識別經截斷的 SHA-256 雜湊值，接收器會在啟動時根據本機主機名稱、`HOSTNAME` 環境變數或本機網路位址解析一次主機身分識別。如果無法解析任何主機身分識別，管線將無法啟動。共用同一個網路命名空間的執行個體會解析出相同的身分識別，除非它們具有不同的 `HOSTNAME` 值。

標籤名稱必須符合 `[a-zA-Z_][a-zA-Z0-9_]*`，不得以 `__` 開頭，且不能是 `le`、`ge` 或 `quantile`。如果某個序列已有相同名稱的標籤，則會保留現有的標籤值，且不會將執行個體標籤新增至該序列。此比較使用接收器最終產生的標籤名稱，其中包含屬性的前綴。例如，名為 `x` 的指標屬性會成為 `metric_attributes_x` 標籤，因此將 `instance_label` 設定為 `x` 會同時新增這兩個標籤。

下列範例會新增 `dp_instance` 標籤：

```yaml
sink:
  - prometheus:
      url: "http://localhost:9090/api/v1/write"
      instance_label: dp_instance
```
{% include copy.html %}

若要計算所有執行個體的總計，請在查詢中透過彙總移除此標籤，例如 `sum without (dp_instance) (my_metric)`。

## 閾值組態

使用下列選項設定 Prometheus 接收器的批次處理與排清行為。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`max_events` | 否 | 整數 | 排清至 Prometheus 前可累積的最大事件數。預設值為 `1000`。
`max_request_size` | 否 | 字串 | 排清前請求承載的最大大小。預設值為 `1mb`。
`flush_interval` | 否 | 持續時間 | 排清事件前可等待的最長時間。預設值為 `10s`。

## AWS 組態

當存在 `aws` 區塊時，請求會自動以 Signature Version 4 簽署。必須提供 `https://` URL。AWS 組態支援下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`region` | 否 | 字串 | 用於認證資訊的 AWS 區域。預設為[標準 SDK 決定區域的行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串 | 對 AWS 發出請求時要擔任的 STS 角色。預設為 `null`，即使用[標準 SDK 認證資訊行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`sts_header_overrides` | 否 | 對應表 | 擔任 IAM 角色時要套用的標頭覆寫對應表。最多 5 個標頭。
`sts_external_id` | 否 | 字串 | 擔任 IAM 角色時使用的選用外部 ID。長度必須介於 2 到 1,224 個字元之間。

## 驗證組態

`authentication` 區塊支援 HTTP Basic 驗證。不可與 `aws`（Signature Version 4 簽署）併用。驗證組態支援下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`http_basic.username` | 是 | 字串 | HTTP Basic 驗證的使用者名稱。
`http_basic.password` | 是 | 字串 | HTTP Basic 驗證的密碼。
