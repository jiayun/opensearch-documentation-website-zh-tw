---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定 OpenSearch Data Prepper"
parent: Managing OpenSearch Data Prepper
nav_order: 5
redirect_from:
 - /clients/data-prepper/data-prepper-reference/
 - /monitoring-plugins/trace/data-prepper-reference/
---

# 設定 OpenSearch Data Prepper

您可以編輯 Data Prepper 安裝中的 `data-prepper-config.yaml` 檔案，以自訂 OpenSearch Data Prepper 組態。下列組態選項與管線組態選項彼此獨立。

## Data Prepper 組態

請使用下列選項自訂 Data Prepper 組態。

選項 | 必要 | 類型 | 說明
:--- | :--- |:--- | :---
`ssl` | 否 | 布林值 | 指出伺服器 API 是否應使用 TLS。預設為 `true`。
`keyStoreFilePath` | 否 | 字串 | `.jks` 或 `.p12` 金鑰儲存區檔案的路徑。若 `ssl` 為 `true`，則為必要。
`keyStorePassword` | 否 | 字串 | 金鑰儲存區的密碼。選用；預設為空字串。
`privateKeyPassword` | 否 | 字串 | 金鑰儲存區中私密金鑰的密碼。選用；預設為空字串。
`serverPort` | 否 | 整數 | 伺服器 API 使用的連接埠號碼。預設為 `4900`。
`metricRegistries` | 否 | 清單 | 用於發布所產生指標的指標註冊表。目前支援 **Prometheus** 與 **Amazon CloudWatch**。預設為 **Prometheus**。
`metricTags` | 否 | Map | 最多包含三組鍵值對的 Map，用於定義指標註冊表的共用指標標籤。`serviceName` 鍵為保留鍵（預設為 `DataPrepper`）。您可以設定環境變數 `DATAPREPPER_SERVICE_NAME` 來覆寫此值。若 `metricTags` 中包含 `serviceName`，則以其為優先。
`authentication` | 否 | 物件 | 伺服器 API 的驗證組態。有效值為 `http_basic`，需要 `username` 與 `password`。若未定義，伺服器不會執行驗證。
`processorShutdownTimeout` | 否 | 持續時間 | 允許處理器完成處理傳輸中資料並正常關閉的時間長度。預設為 `30s`。
`sinkShutdownTimeout` | 否 | 持續時間 | 允許接收器清除傳輸中資料並正常關閉的時間長度。預設為 `30s`。
`peer_forwarder` | 否 | 物件 | Peer Forwarder 組態。請參閱 [Peer Forwarder 選項](#peer-forwarder-options)。
`circuit_breakers` | 否 | [circuit_breakers](#circuit-breakers) | 設定一或多個斷路器以控制傳入的資料。
`extensions` | 否 | 物件 | 由多個管線共用的擴充外掛程式組態。請參閱[擴充外掛程式](#extension-plugins)。

### Peer Forwarder 選項

本節詳細說明對等轉送的各項組態選項。

#### 對等轉送的一般選項

下表列出對等轉送的一般組態。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`port` | 否 | 整數 | 對等轉送伺服器的連接埠（`0`–`65535`）。預設為 `4994`。
`request_timeout` | 否 | 整數 | Peer Forwarder HTTP 伺服器的請求逾時，以毫秒為單位。預設為 `10000`。
`server_thread_count` | 否 | 整數 | Peer Forwarder 伺服器使用的執行緒數量。預設為 `200`。
`client_thread_count` | 否 | 整數 | Peer Forwarder 用戶端使用的執行緒數量。預設為 `200`。
`max_connection_count` | 否 | 整數 | Peer Forwarder 伺服器的最大開啟連線數。預設為 `500`。
`max_pending_requests` | 否 | 整數 | `ScheduledThreadPool` 工作佇列中的最大工作數。預設為 `1024`。
`discovery_mode` | 否 | 字串 | 對等探索模式。有效值為 `local_node`（在本機處理）、`static`（固定的對等清單）、`dns`（DNS A 記錄）或 `aws_cloud_map`（AWS 服務註冊表）。預設為 `local_node`。
`static_endpoints` | 視情況 | 清單 | 所有 Data Prepper 執行個體的端點。若 `discovery_mode` 設為 `static`，則為必要。
`domain_name` | 視情況 | 字串 | 用於 DNS 探索的網域名稱（支援多筆 A 記錄）。若 `discovery_mode` 設為 `dns`，則為必要。
`aws_cloud_map_namespace_name` | 視情況 | 字串 | AWS Cloud Map 命名空間。若 `discovery_mode` 設為 `aws_cloud_map`，則為必要。
`aws_cloud_map_service_name` | 視情況 | 字串 | AWS Cloud Map 服務名稱。若 `discovery_mode` 設為 `aws_cloud_map`，則為必要。
`aws_cloud_map_query_parameters` | 否 | Map | 套用至 AWS Cloud Map 執行個體屬性的鍵值篩選條件。
`buffer_size` | 否 | 整數 | 緩衝區可容納的最大未檢查記錄數，包括已寫入及尚未儲存至檢查點的傳輸中記錄。預設為 `512`。
`batch_size` | 否 | 整數 | 單次讀取作業傳回的最大記錄數。預設為 `48`。
`aws_region` | 視情況 | 字串 | 與 AWS Certificate Manager (ACM)、Amazon Simple Storage Service (Amazon S3) 或 AWS Cloud Map 搭配使用的 AWS 區域。在下列情況下為必要：<br> - `use_acm_certificate_for_ssl: true`。<br> - `ssl_certificate_file` 或 `ssl_key_file` 為 S3 路徑。<br> - `discovery_mode` 設為 `aws_cloud_map`。
`drain_timeout` | 否 | 持續時間 | 允許 Peer Forwarder 在關閉前完成處理的時間長度。預設為 `10s`。

#### Peer Forwarder 的 TLS/SSL 選項

請使用下列選項為 Peer Forwarder 啟用並設定 TLS/SSL，包括憑證來源（檔案、S3 或 ACM）及驗證行為。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`ssl` | 否 | 布林值 | 啟用 TLS/SSL。預設為 `true`。
`ssl_certificate_file` | 視情況 | 字串 | SSL 憑證鏈檔案路徑或 S3 路徑（`s3://<bucket>/<path>`）。若 `ssl: true` 且 `use_acm_certificate_for_ssl: false`，則為必要。預設為 `config/default_certificate.pem`。請參閱 Data Prepper 儲存庫中的[組態範例](https://github.com/opensearch-project/data-prepper/blob/17c3e290676e6c774cb8a0d4d8eaec7ae8bd696a/data-prepper-core/src/test/resources/valid_peer_forwarder_config_with_mutual_tls.yml)。
`ssl_key_file` | 視情況 | 字串 | SSL 私密金鑰檔案路徑或 S3 路徑。若 `ssl` 設為 `true` 且 `use_acm_certificate_for_ssl` 設為 `false`，則為必要。預設為 `config/default_private_key.pem`。
`ssl_insecure_disable_verification` | 否 | 布林值 | 停用伺服器 TLS 憑證鏈的驗證。預設為 `false`。
`ssl_fingerprint_verification_only` | 否 | 布林值 | 若為 `true`，則僅驗證憑證指紋（停用憑證鏈驗證）。預設為 `false`。
`use_acm_certificate_for_ssl` | 否 | 布林值 | 若為 `true`，則使用來自 ACM 的憑證與私密金鑰啟用 TLS/SSL。預設為 `false`。
`acm_certificate_arn` | 視情況 | 字串 | ACM 憑證的 Amazon Resource Name (ARN)。若 `use_acm_certificate_for_ssl` 設為 `true`，則為必要。
`acm_private_key_password` | 否 | 字串 | 用於解密 ACM 私密金鑰的密碼。若未提供，Data Prepper 會產生隨機密碼。
`acm_certificate_timeout_millis` | 否 | 整數 | 擷取 ACM 憑證的逾時，以毫秒為單位。預設為 `120000`。
`aws_region` | 視情況 | 字串 | 與 ACM、S3 或 AWS Cloud Map 搭配使用的 AWS 區域。若 `use_acm_certificate_for_ssl` 設為 `true`、`ssl_certificate_file` 或 `ssl_key_file` 為 S3 路徑，或 `discovery_mode` 設為 `aws_cloud_map`，則為必要。

#### Peer Forwarder 的驗證選項

使用下列選項來指定 Peer Forwarder 在對等節點之間驗證請求的方式。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`authentication` | 否 | 對應表 | 驗證方法。有效值為 `mutual_tls` (mTLS) 或 `unauthenticated` (不進行驗證)。預設為 `unauthenticated`。

## 斷路器

Data Prepper 內建斷路器，可協助防止 Java heap 記憶體耗盡。這對使用有狀態處理器的管線特別有用，因為這類處理器會在緩衝區之外將資料保留在記憶體中。

當斷路器被觸發時，Data Prepper 會拒絕路由進緩衝區的傳入資料，直到斷路器重設為止。

下表列出可用的斷路器組態區塊。

選項 | 必要 | 類型 | 說明
:--- | :--- |:---| :---
`heap` | 否 | [heap](#heap-circuit-breaker) | 啟用 heap 斷路器。預設為停用。

### Heap 斷路器

`heap` 斷路器會設定 Data Prepper，在 JVM heap 達到指定的使用量閾值時拒絕傳入資料。`heap` 參數支援下列值。

選項 | 必要 | 類型 | 說明
:--- |:---|:---| :---
`usage` | 是 | 位元組 | 觸發斷路器的 JVM heap 使用量 (例如 `6.5gb`)。若目前使用量超過此值，斷路器就會被觸發。
`check_interval` | 否 | 持續時間 | 檢查 heap 大小以判斷是否應啟動斷路器的時間間隔。預設為 `500ms`。
`reset` | 否  | 持續時間 | 斷路器在啟動後，必須維持啟動狀態的最短時間，之後新的 heap 大小檢查才能嘗試將其停用。預設為 `1s`。

## 延伸外掛程式

Data Prepper 支援使用者可設定的延伸外掛程式。延伸外掛程式提供可重複使用的組態，可在管線外掛程式 (來源、緩衝區、處理器或匯出端) 之間共用。

### AWS 延伸外掛程式

`aws` 延伸提供 `secrets` 組態，可與 [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html) 整合，以安全管理管線中的敏感組態值。以下範例顯示基本組態：

```yaml
extensions:
  aws:
    secrets:
      <YOUR_SECRET_CONFIG_ID_1>:
        secret_id: <YOUR_SECRET_ID_1>
        region: <YOUR_REGION_1>
        sts_role_arn: <YOUR_STS_ROLE_ARN_1>
        refresh_interval: <YOUR_REFRESH_INTERVAL>
        disable_refresh: false
      <YOUR_SECRET_CONFIG_ID_2>:
        # ...
```
{% include copy.html %}

### 機密資料

`secrets` 組態支援下列參數。

選項 | 必要 | 類型 | 說明
:--- |:---|:---| :---
`secret_id`  | 是 | 字串 | AWS 機密資料名稱或 ARN。
`region` | 否 | 字串 | 包含該機密資料的 AWS Region。預設為 `us-east-1`。
`sts_role_arn` | 否 | 字串 | 用於 Secrets Manager 請求時擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null` (標準 SDK 憑證行為)。
`refresh_interval` | 否 | 持續時間 | 重新整理機密資料值的輪詢間隔。預設為 `PT1H`。請參閱[自動重新整理機密資料](#automatically-refreshing-secrets)。
`disable_refresh` | 否 | 布林值 | 停用定期輪詢最新機密資料值。預設為 `false`。當設定為 `true` 時，`refresh_interval` 會被忽略。

#### 參照機密資料

在 `pipelines.yaml` 中，使用下列方式在外掛程式設定中參照機密資料值：

* 純文字：`{% raw %}${{aws_secrets:<YOUR_SECRET_CONFIG_ID>}}{% endraw %}`
* JSON 金鑰：`{% raw %}${{aws_secrets:<YOUR_SECRET_CONFIG_ID>:<YOUR_KEY>}}{% endraw %}`

您可以使用下列設定類型進行機密資料替換：string、number、long、short、integer、double、float、Boolean 或 character。

以下是一個 `data-prepper-config.yaml` 範例，包含兩個機密資料組態 ID (`host-secret-config` 和 `credential-secret-config`)：

```yaml
extensions:
  aws:
    secrets:
      host-secret-config:
        secret_id: <YOUR_SECRET_ID_1>
        region: <YOUR_REGION_1>
        sts_role_arn: <YOUR_STS_ROLE_ARN_1>
        refresh_interval: <YOUR_REFRESH_INTERVAL_1>
      credential-secret-config:
        secret_id: <YOUR_SECRET_ID_2>
        region: <YOUR_REGION_2>
        sts_role_arn: <YOUR_STS_ROLE_ARN_2>
        refresh_interval: <YOUR_REFRESH_INTERVAL_2>
```
{% include copy.html %}

接著，您可以在 `pipelines.yaml` 中如下參照這些機密資料：

```yaml
sink:
  - opensearch:
      hosts: [{% raw %}"${{aws_secrets:host-secret-config}}"{% endraw %}]
      username: {% raw %}"${{aws_secrets:credential-secret-config:username}}"{% endraw %}
      password: {% raw %}"${{aws_secrets:credential-secret-config:password}}"{% endraw %}
      index: "test-migration"
```
{% include copy.html %}

#### 自動重新整理機密資料

對於每個機密資料組態，Data Prepper 會以固定間隔輪詢最新值，以支援在 AWS Secrets Manager 中輪替機密資料。重新整理後的值會由能夠重新整理其連線/驗證的外掛程式 (例如匯出端) 使用。若有多個機密資料組態，在初始輪詢時會對所有組態套用最多 `60s` 的抖動。
