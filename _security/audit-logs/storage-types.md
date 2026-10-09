---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "稽核記錄儲存類型"
parent: Audit logs
nav_order: 135
redirect_from:
  - /security-plugin/audit-logs/storage-types/
---

# 稽核記錄儲存類型

稽核記錄可能佔用相當大的空間，因此安全性外掛程式提供多種儲存位置的選項。

設定 | 說明
:--- | :---
`debug` | 輸出至 `stdout`。適用於測試與偵錯。
`internal_opensearch` | 寫入目前 OpenSearch 叢集上的稽核索引。
`internal_opensearch_data_stream` | 寫入目前 OpenSearch 叢集上的稽核記錄資料串流。
`external_opensearch` | 寫入遠端 OpenSearch 叢集上的稽核索引。
`webhook` | 將事件傳送至任意的 HTTP 端點。
`log4j` | 將事件寫入 Log4j 記錄器。您可以使用任何 Log4j [appender](https://logging.apache.org/log4j/2.x/manual/appenders.html)，例如 SNMP、JDBC、Cassandra 和 Kafka。

您可以在 `opensearch.yml` 中設定輸出位置：

```
plugins.security.audit.type: <debug|internal_opensearch|internal_opensearch_data_stream|external_opensearch|webhook|log4j>
```

`internal_opensearch_data_stream`、`external_opensearch`、`webhook` 和 `log4j` 可使用其他組態選項進行自訂。如需更多資訊，請參閱[內部 OpenSearch 資料串流](#internal-opensearch-data-streams)。


## 內部 OpenSearch 資料串流

您可以使用下列參數設定 `internal_opensearch_data_stream` 類型。


名稱 | 資料類型 | 說明
:--- | :--- | :---
`plugins.security.audit.config.data_stream.name` | String | 稽核記錄資料串流的名稱。預設為 `opensearch-security-auditlog`。

### 範本設定

名稱 | 資料類型 | 說明
:--- | :--- | :---
`plugins.security.audit.config.data_stream.template.manage` | Boolean | 當 `true` 時，資料串流的範本由 OpenSearch 管理。預設為 `true`。
`plugins.security.audit.config.data_stream.template.name` | String | 資料串流範本的名稱。預設為 `opensearch-security-auditlog`。
`plugins.security.audit.config.data_stream.template.number_of_replicas` | Integer | 資料串流的副本數。預設為 `0`。
`plugins.security.audit.config.data_stream.template.number_of_shards` | Integer | 資料串流的分片數。預設為 `1`。


## 外部 OpenSearch

`external_opensearch` 儲存類型需要一或多個具有主機/IP 位址與連接埠的 OpenSearch 端點。您也可以選擇提供索引名稱與文件類型。

```yml
plugins.security.audit.type: external_opensearch
plugins.security.audit.config.http_endpoints: [<endpoints>]
plugins.security.audit.config.index: <indexname>
plugins.security.audit.config.type: _doc
```

安全性外掛程式會使用 OpenSearch REST API 傳送事件，就像任何其他索引請求一樣。若為 `plugins.security.audit.config.http_endpoints`，請使用以逗號分隔的主機/IP 位址清單以及 REST 連接埠（預設為 9200）。

```
plugins.security.audit.config.http_endpoints: ['https://my-opensearch-cluster.company.com:9200', 'http://my-opensearch-cluster.company.com:9200', 'my-opensearch-cluster.company.com:9200', '192.168.178.1:9200', '192.168.178.2:9200']
```

如果您使用 `external_opensearch`，且遠端叢集也使用安全性外掛程式，則必須提供一些額外的參數以進行驗證。這些參數取決於您為遠端叢集設定的驗證類型。


### TLS 設定

名稱 | 資料類型 | 說明
:--- | :--- | :---
`plugins.security.audit.config.enable_ssl` | Boolean | 如果您在接收叢集上啟用了 SSL/TLS，請設為 true。預設為 `false`。
`plugins.security.audit.config.verify_hostnames` |  Boolean | 是否驗證接收叢集之 SSL/TLS 憑證的主機名稱。預設為 `true`。
`plugins.security.audit.config.pemtrustedcas_filepath` | String | 外部 OpenSearch 叢集的受信任根憑證，相對於 `config` 目錄。
`plugins.security.audit.config.pemtrustedcas_content` | String | 除了指定路徑（`plugins.security.audit.config.pemtrustedcas_filepath`）之外，您也可以直接設定 Base64 編碼的憑證內容。
`plugins.security.audit.config.enable_ssl_client_auth` | Boolean | 是否啟用 SSL/TLS 用戶端驗證。如果您將此設為 true，稽核記錄模組會隨請求一併傳送節點的憑證。接收叢集可使用此憑證來驗證呼叫方的身分。
`plugins.security.audit.config.pemcert_filepath` | String | 要傳送至外部 OpenSearch 叢集之 TLS 憑證的路徑，相對於 `config` 目錄。
`plugins.security.audit.config.pemcert_content` | String | 除了指定路徑（`plugins.security.audit.config.pemcert_filepath`）之外，您也可以直接設定 Base64 編碼的憑證內容。
`plugins.security.audit.config.pemkey_filepath` | String | 要傳送至外部 OpenSearch 叢集之 TLS 憑證私密金鑰的路徑，相對於 `config` 目錄。
`plugins.security.audit.config.pemkey_content` | String | 除了指定路徑（`plugins.security.audit.config.pemkey_filepath`）之外，您也可以直接設定 Base64 編碼的憑證內容。
`plugins.security.audit.config.pemkey_password` | String | 私密金鑰的密碼。


### 基本驗證設定

如果您在接收叢集上啟用了 HTTP 基本驗證，請使用這些設定來指定使用者名稱與密碼：

```yml
plugins.security.audit.config.username: <username>
plugins.security.audit.config.password: <password>
```


## Webhook

使用下列索引鍵來設定 `webhook` 儲存類型。

名稱 | 資料類型 | 說明
:--- | :--- | :---
`plugins.security.audit.config.webhook.url` | String | 要將記錄傳送至的 HTTP 或 HTTPS URL。
`plugins.security.audit.config.webhook.ssl.verify` | Boolean | 若為 true，則會驗證端點所提供的 TLS 憑證（若有）。若設為 false，則不執行驗證。如果您使用自我簽署憑證，可以停用此檢查。
`plugins.security.audit.config.webhook.ssl.pemtrustedcas_filepath` | String | 用來驗證 webhook TLS 憑證的受信任憑證路徑。
`plugins.security.audit.config.webhook.ssl.pemtrustedcas_content` | String | 與 `plugins.security.audit.config.webhook.ssl.pemtrustedcas_content` 相同，但您可以直接設定 Base64 編碼的憑證內容。
`plugins.security.audit.config.webhook.format` | String | 稽核記錄訊息的記錄格式，可為 `URL_PARAMETER_GET`、`URL_PARAMETER_POST`、`TEXT`、`JSON`、`SLACK` 其中之一。請參閱[格式](#formats)。


### 格式

格式 | 說明
:--- | :---
`URL_PARAMETER_GET` | 使用 HTTP GET 將記錄傳送至 webhook URL。所有記錄的資訊會以請求參數的形式附加至 URL。
`URL_PARAMETER_POST` | 使用 HTTP POST 將記錄傳送至 webhook URL。所有記錄的資訊會以請求參數的形式附加至 URL。
`TEXT` | 使用 HTTP POST 將記錄傳送至 webhook URL。請求本文包含純文字格式的稽核記錄訊息。
`JSON` | 使用 HTTP POST 將記錄傳送至 webhook URL。請求本文包含 JSON 格式的稽核記錄訊息。
`SLACK` | 使用 HTTP POST 將記錄傳送至 webhook URL。請求本文包含適合 Slack 取用的 JSON 格式稽核記錄訊息。預設實作會傳回 `"text": "<AuditMessage#toText>"`。


## Log4j

`log4j` 儲存類型可讓您指定記錄器的名稱與記錄層級。

```yml
plugins.security.audit.config.log4j.logger_name: audit
plugins.security.audit.config.log4j.level: INFO
```

根據預設，安全性外掛程式會使用記錄器名稱 `audit`，並以 `INFO` 層級記錄事件。稽核事件會以 JSON 格式儲存。

對於具有許多索引的叢集，您可以使用 `plugins.security.audit.config.log4j.maximum_index_characters_per_message` 設定來分割記錄訊息。這可避免 `audit_trace_indices` 與 `audit_trace_resolved_indices` 欄位超過每則訊息所設定的索引名稱字元數上限，並縮小記錄管線的記錄訊息大小。分割的訊息會包含 `audit_split_message_id` UUID 欄位，用來連結相關的訊息片段。此設定預設為 2,147,483,647（不分割）。
