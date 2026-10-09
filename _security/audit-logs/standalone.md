---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "獨立稽核記錄"
parent: Audit logs
nav_order: 133
---

# 獨立稽核記錄

---

<details markdown="block">
  <summary>
    目錄
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

獨立稽核記錄可為未使用細微存取控制 (FGAC) 的 OpenSearch 叢集啟用稽核記錄。這包括以僅限 SSL 模式 (`plugins.security.ssl_only: true`) 執行或停用安全性 (`plugins.security.disabled: true`) 的叢集。

在此情境中，*獨立*是指獨立於細微存取控制運作的稽核記錄。它在 Security 外掛程式內執行，並使用與標準模式相同的稽核基礎架構 (接收端、路由與非同步執行緒集區)，但不依賴驗證或授權來產生事件。

不需要驗證或授權的叢集，仍可能需要稽核軌跡以符合 SOC 2、HIPAA、PCI DSS 和 GDPR 等合規框架。獨立稽核記錄會記錄這些叢集中每個請求的來源、動作與時間。

## 必要條件

若要啟用獨立稽核記錄，請在每個節點的 `opensearch.yml` 中加入以下兩個設定：

```yml
plugins.security.audit.enable_standalone: true
plugins.security.audit.type: log4j
```
{% include copy.html %}

兩個設定皆為必要：

- `plugins.security.audit.enable_standalone: true` 會啟用獨立稽核子系統。
- `plugins.security.audit.type: <sink>` 會指定稽核接收端，也就是稽核事件的目的地。

加入這些設定後，請重新啟動每個節點以啟用獨立稽核記錄。

下列類別在獨立模式下永遠不會產生事件，因為不會發生任何驗證或授權決策：`FAILED_LOGIN`、`AUTHENTICATED`、`GRANTED_PRIVILEGES`、`MISSING_PRIVILEGES`、`OPENDISTRO_SECURITY_INDEX_ATTEMPT`、`API_TOKEN_WRITE`、`RESOURCE_ACCESS_GRANTED`、`RESOURCE_ACCESS_DENIED` 和 `RESOURCE_SHARING_CHANGED`。啟動時，若這些類別中有任何一個尚未被其他設定停用，就會記錄一則警告。由於 `AUTHENTICATED` 和 `GRANTED_PRIVILEGES` 預設為停用，預設的啟動警告不會提及它們。
{: .warning }

## 支援的稽核接收端

獨立稽核記錄支援與標準模式相同的接收端。下表說明可用的接收端類型。

接收端類型 | 說明
:--- | :---
`internal_opensearch` | 將稽核事件寫入目前 OpenSearch 叢集上的索引。
`log4j` | 將事件寫入 Log4j 記錄器。您可以使用任何 Log4j appender (檔案、SNMP、JDBC、Kafka)。
`webhook` | 以 JSON 格式將事件傳送至任意 HTTP 端點。
`external_opensearch` | 寫入遠端 OpenSearch 叢集上的稽核索引。
`debug` | 將事件列印至 `stdout`。僅適用於開發與疑難排解。

如需接收端專屬的組態選項，請參閱 [稽核記錄儲存類型]({{site.url}}{{site.baseurl}}/security/audit-logs/storage-types/)。

## 追蹤的事件

獨立稽核記錄為沒有驗證的叢集新增了兩個請求追蹤類別。下表說明這些類別。

類別 | 來源 | 說明
:--- | :--- | :---
`REQUEST_AUDIT` | REST | 擷取源自 REST 的請求，包括來源 IP、目標索引、請求本文與 HTTP 標頭。這是獨立模式的主要事件。
`TRANSPORT_AUDIT` | Transport | 擷取節點之間源自傳輸層的請求，包括分片層級作業 (`bulk[s][p]`、`search[phase/query]`)、副本寫入與轉送的請求。

`REQUEST_AUDIT` 源自 REST (`audit_request_origin: REST`)，但事件本身會以 `audit_request_layer: TRANSPORT` 記錄。因此，它可能會被 `disabled_categories`、`disabled_transport_categories` 或 `disabled_rest_categories` 中的任何一個所抑制---在這些設定中的任何一個加入 `REQUEST_AUDIT` 即可抑制該事件。
{: .note}

這些類別不代表任何驗證或授權語意。它們只記錄某個請求已被接收並處理。

除了這些請求追蹤類別之外，當啟用[合規追蹤](#compliance-tracking)時，獨立稽核記錄也會發出標準的文件層級合規類別。下表說明這些類別。

類別 | 說明
:--- | :---
`COMPLIANCE_DOC_WRITE` | 文件被寫入受監看的索引。如需更多資訊，請參閱[文件寫入追蹤](#document-write-tracking)。
`COMPLIANCE_DOC_READ` | 從受監看的索引讀取了受監看的欄位。如需更多資訊，請參閱[文件讀取追蹤](#document-read-tracking)。

合規事件僅受合規設定 (`compliance.enabled` 以及受監看的索引與欄位) 管控。它們不受 `disabled_categories` 影響，後者適用於所有 REST 層與傳輸層類別，例如 `REQUEST_AUDIT` 和 `TRANSPORT_AUDIT`。

### 事件欄位

每個 `REQUEST_AUDIT` 事件包括：

- `@timestamp` --- 事件發生的時間
- `audit_cluster_name`、`audit_node_name`、`audit_node_id` --- 叢集與節點識別
- `audit_request_privilege` --- 受稽核的傳輸動作 (例如 `indices:data/write/index`)
- `audit_request_body` --- 請求本文 (可設定)
- `audit_request_remote_address` --- 用戶端來源 IP
- `audit_trace_indices` --- 目標索引 (原始模式)
- `audit_trace_resolved_indices` --- 解析後的具體索引 (當 `resolve_indices: true` 時)
- `audit_transport_request_type` --- 傳輸請求類別 (例如 `IndexRequest` 或 `SearchRequest`)
- `audit_request_layer` --- `REQUEST_AUDIT` 事件的 `TRANSPORT`
- `audit_rest_request_headers` --- HTTP 標頭 (排除敏感性標頭)

### 獨立模式中的識別

稽核事件中擷取的識別資訊取決於安全性模式。下表說明每種模式中擷取的識別。

安全性模式 | 擷取的識別
:--- | :---
僅限 SSL 且使用 mTLS | 用戶端憑證的主體辨別名稱 (DN)，記錄為 `audit_request_effective_user` (例如 `CN=my-app,OU=engineering,O=myorg`)。
僅限 SSL 但不使用 mTLS | 僅來源 IP 位址。
停用安全性 | 僅來源 IP 位址。

## 組態

請在 `opensearch.yml` 中設定初始的獨立稽核設定。動態設定可使用 [Cluster Settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) 在執行階段更新。靜態設定，包括 `enable_standalone`、`action_groups.<NAME>` 與接收端連線設定，則需要重新啟動節點。不需要任何安全性索引。

獨立模式不使用 [Audit log APIs]({{site.url}}{{site.baseurl}}/security/api/audit/) 或 `audit.yml`。這兩者都會管理安全性索引，且需要細微存取控制。在獨立模式中，請改用 Cluster Settings API。

### 動態組態

大多數篩選與合規設定可以在不重新啟動叢集的情況下於執行階段變更。若要變更設定，請傳送 `PUT _cluster/settings` 請求：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.security.audit.config.log_request_body": false
  }
}
```
{% include copy.html %}

動態設定會覆寫 `opensearch.yml` 中的值，並在叢集重新啟動後持續保留。

若 `PUT _cluster/settings` 請求變更了不支援動態更新的設定，該請求會成功並儲存新值，但該值永遠不會被套用，而且不會有任何錯誤指出此次更新沒有效果。
{: .warning}

### 動態設定參考

下列設定已註冊為動態叢集設定。類型以預留位置顯示：

```yml
# Global toggle
plugins.security.audit.enabled: <bool>

# Filter settings
plugins.security.audit.config.log_request_body: <bool>
plugins.security.audit.config.resolve_indices: <bool>
plugins.security.audit.config.resolve_bulk_requests: <bool>
plugins.security.audit.config.exclude_sensitive_headers: <bool>
plugins.security.audit.config.enable_rest: <bool>
plugins.security.audit.config.enable_transport: <bool>
plugins.security.audit.config.disabled_categories: <list[string]>
plugins.security.audit.config.disabled_rest_categories: <list[string]>
plugins.security.audit.config.disabled_transport_categories: <list[string]>
plugins.security.audit.config.ignore_users: <list[string]>
plugins.security.audit.config.ignore_requests: <list[string]>
plugins.security.audit.config.ignore_headers: <list[string]>
plugins.security.audit.config.body_logging_exclusions: <list[string]>

# Compliance settings
plugins.security.audit.compliance.enabled: <bool>
plugins.security.audit.compliance.write_metadata_only: <bool>
plugins.security.audit.compliance.write_log_diffs: <bool>
plugins.security.audit.compliance.write_watched_indices: <list[string]>
plugins.security.audit.compliance.write_ignore_users: <list[string]>
plugins.security.audit.compliance.read_metadata_only: <bool>
plugins.security.audit.compliance.read_watched_fields: <list[string]>
plugins.security.audit.compliance.read_ignore_users: <list[string]>
plugins.security.audit.compliance.external_config: <bool>
plugins.security.audit.compliance.internal_config: <bool>
```
{% include copy.html %}

關於這些設定可指定的位置，請注意以下幾點：

- `plugins.security.audit.enabled` 設定僅能在執行時期使用。在 `opensearch.yml` 中設定它沒有效果。在獨立模式下，請使用 `PUT _cluster/settings` 進行變更。
- 合規性設定在 `opensearch.yml` 與 `PUT _cluster/settings` 中使用不同的鍵名。只有 `plugins.security.audit.compliance.enabled` 在兩者中使用相同名稱。其餘合規性設定在 `opensearch.yml` 中僅接受舊版的 `opendistro_security.compliance.history.*` 鍵。下表將每個合規性叢集設定對應到 `opensearch.yml` 中相應的鍵。

叢集設定 | `opensearch.yml` 中的鍵
:--- | :---
`plugins.security.audit.compliance.enabled` | `plugins.security.audit.compliance.enabled`
`plugins.security.audit.compliance.write_metadata_only` | `opendistro_security.compliance.history.write.metadata_only`
`plugins.security.audit.compliance.read_metadata_only` | `opendistro_security.compliance.history.read.metadata_only`
`plugins.security.audit.compliance.write_log_diffs` | `opendistro_security.compliance.history.write.log_diffs`
`plugins.security.audit.compliance.write_watched_indices` | `opendistro_security.compliance.history.write.watched_indices`
`plugins.security.audit.compliance.read_watched_fields` | `opendistro_security.compliance.history.read.watched_fields`
`plugins.security.audit.compliance.write_ignore_users` | `opendistro_security.compliance.history.write.ignore_users`
`plugins.security.audit.compliance.read_ignore_users` | `opendistro_security.compliance.history.read.ignore_users`
`plugins.security.audit.compliance.external_config` | `opendistro_security.compliance.history.external_config_enabled`
`plugins.security.audit.compliance.internal_config` | `opendistro_security.compliance.history.internal_config_enabled`

靜態設定（`enable_standalone`、`action_groups.<NAME>`、`log4j.enable_mdc_routing`、接收端連線設定，以及執行緒集區設定）需要重新啟動節點，且無法使用 Cluster Settings API 變更。

### 可用的篩選設定

下表說明控制記錄內容的設定。可動態更新的設定可以在執行時期使用 [Cluster Settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) 變更。其餘設定請在 `opensearch.yml` 中設定。

設定 | 預設值 | 可動態更新 | 說明
:--- | :--- | :--- | :---
`plugins.security.audit.config.enable_rest` | `true` | 是 | 啟用 REST 層的稽核事件。
`plugins.security.audit.config.enable_transport` | `true` | 是 | 啟用傳輸層的稽核事件。
`plugins.security.audit.config.log_request_body` | `true` | 是 | 在稽核事件中包含請求本文。
`plugins.security.audit.config.resolve_indices` | `true` | 是 | 將萬用字元索引模式解析為具體索引。
`plugins.security.audit.config.resolve_bulk_requests` | `false` | 是 | 記錄 bulk 請求中的個別子作業。
`plugins.security.audit.config.exclude_sensitive_headers` | `true` | 是 | 從稽核事件中排除敏感標頭（例如 `Authorization`）。
`plugins.security.audit.config.disabled_categories` | `[]` | 是 | 要停用的請求追蹤類別（例如 `["REQUEST_AUDIT"]`）。不影響 `COMPLIANCE_*` 類別。
`plugins.security.audit.config.disabled_rest_categories` | `["AUTHENTICATED", "GRANTED_PRIVILEGES", "RESOURCE_ACCESS_GRANTED", "RESOURCE_ACCESS_DENIED", "RESOURCE_SHARING_CHANGED"]` | 是 | 要停用的 REST 層類別。已棄用。請改用 `disabled_categories`。
`plugins.security.audit.config.disabled_transport_categories` | `["AUTHENTICATED", "GRANTED_PRIVILEGES", "RESOURCE_ACCESS_GRANTED", "RESOURCE_ACCESS_DENIED", "RESOURCE_SHARING_CHANGED", "CLUSTER_SETTINGS_CHANGED", "INDEX_SETTINGS_CHANGED"]` | 是 | 要停用的傳輸層類別。已棄用。請改用 `disabled_categories`。
`plugins.security.audit.config.ignore_users` | `["kibanaserver"]` | 是 | 其請求不會被記錄的使用者。
`plugins.security.audit.config.ignore_requests` | `[]` | 是 | 要排除的動作模式或 REST 路徑（例如 `["cluster:monitor/*"]`）。
`plugins.security.audit.config.ignore_headers` | `[]` | 否 | 要從稽核事件中排除的 HTTP 標頭。

設定 `disabled_rest_categories` 或 `disabled_transport_categories` 會取代整個預設清單，而不是在其中新增項目。如果您將其中任一設定為自訂清單，請包含上表中您仍想停用的類別。任何省略的類別都會在無警告的情況下重新啟用。
{: .warning }

### 在執行時期啟用與停用稽核記錄

您可以在不重新啟動叢集的情況下啟用或停用稽核記錄：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.security.audit.enabled": false
  }
}
```
{% include copy.html %}

將值設為 `true` 即可重新啟用稽核記錄。

## 合規性追蹤

文件層級的合規性追蹤在獨立模式下同時支援讀取與寫入。

### 文件寫入追蹤

若要追蹤對特定索引的寫入，請設定要監看的索引：

```yml
plugins.security.audit.compliance.enabled: true
opendistro_security.compliance.history.write.watched_indices:
  - "sensitive-data-*"
  - "financial-records"
```
{% include copy.html %}

寫入事件會以 `COMPLIANCE_DOC_WRITE` 類別記錄，並包含文件 ID、索引名稱與分片 ID。當 `write_log_diffs: true` 時，事件會包含先前與目前文件內容之間的差異。

### 文件讀取追蹤

若要追蹤特定索引中特定欄位的讀取，請設定 `read_watched_fields`。作為叢集設定，這是一份字串清單——每個項目是以逗號分隔的字串，其第一個詞元是索引模式，其餘詞元則是欄位模式。若某個索引未指定任何欄位模式，則會監看所有欄位 (`*`)：

```yml
plugins.security.audit.compliance.enabled: true
opendistro_security.compliance.history.read.watched_fields:
  - "sensitive-data-*,ssn,credit_card"
  - "hr-records,salary,performance_rating"
```
{% include copy.html %}

讀取事件會以 `COMPLIANCE_DOC_READ` 類別記錄，並包含所存取的欄位值。

### 合規設定

下表說明合規設定。可動態更新的設定可在執行階段使用 [Cluster Settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) 變更。其餘設定請在 `opensearch.yml` 中設定。

設定 | 預設 | 可動態更新 | 說明
:--- | :--- | :--- | :---
`plugins.security.audit.compliance.enabled` | `true` | 是 | 啟用合規追蹤。合規事件只會針對受監看設定中所設定的索引與欄位產生。
`plugins.security.audit.compliance.write_metadata_only` | `false` | 是 | 寫入事件只記錄中繼資料 (不記錄文件內容)。
`plugins.security.audit.compliance.read_metadata_only` | `false` | 是 | 讀取事件只記錄中繼資料 (不記錄欄位值)。
`plugins.security.audit.compliance.write_log_diffs` | `false` | 是 | 包含新舊文件內容之間的差異。
`plugins.security.audit.compliance.write_watched_indices` | `[]` | 是 | 要監看寫入合規事件的索引模式。
`plugins.security.audit.compliance.read_watched_fields` | `[]` | 是 | 要監看讀取合規事件的索引與欄位模式。每個項目是以逗號分隔的字串：`<index-pattern>,<field-pattern>,...`。
`plugins.security.audit.compliance.write_ignore_users` | `["kibanaserver"]` | 否 | 其文件寫入不受合規追蹤的使用者。
`plugins.security.audit.compliance.read_ignore_users` | `["kibanaserver"]` | 否 | 其文件讀取不受合規追蹤的使用者。
`plugins.security.audit.compliance.external_config` | `false` | 否 | 在啟動時記錄一次外部組態 (`opensearch.yml` 與環境)。
`plugins.security.audit.compliance.internal_config` | `false` | 否 | 記錄內部安全性組態的變更。

## 範例組態

以下範例說明如何在僅 SSL 與停用安全性的模式下設定獨立稽核記錄。

### 僅 SSL 模式搭配 Log4j 接收器

此組態會在僅 SSL 的叢集中啟用稽核記錄，並將事件寫入 Log4j 記錄器：

```yml
plugins.security.ssl_only: true

# TLS configuration
plugins.security.ssl.transport.pemcert_filepath: node-cert.pem
plugins.security.ssl.transport.pemkey_filepath: node-key.pem
plugins.security.ssl.transport.pemtrustedcas_filepath: root-ca.pem
plugins.security.ssl.http.enabled: true
plugins.security.ssl.http.pemcert_filepath: node-cert.pem
plugins.security.ssl.http.pemkey_filepath: node-key.pem
plugins.security.ssl.http.pemtrustedcas_filepath: root-ca.pem

# Standalone audit logging
plugins.security.audit.enable_standalone: true
plugins.security.audit.type: log4j

# Audit filter settings
plugins.security.audit.config.log_request_body: true
plugins.security.audit.config.resolve_indices: true
plugins.security.audit.config.exclude_sensitive_headers: true
plugins.security.audit.config.ignore_requests:
  - "cluster:monitor/*"
  - "indices:monitor/*"
```
{% include copy.html %}

### 停用安全性模式搭配內部索引接收器

此組態會在停用安全性的叢集中啟用稽核記錄，並將事件儲存在內部 OpenSearch 索引中：

```yml
plugins.security.disabled: true

# Standalone audit logging
plugins.security.audit.enable_standalone: true
plugins.security.audit.type: internal_opensearch

# Audit filter settings
plugins.security.audit.config.log_request_body: true
plugins.security.audit.config.resolve_indices: true
plugins.security.audit.config.resolve_bulk_requests: true

# Compliance tracking
plugins.security.audit.compliance.enabled: true
opendistro_security.compliance.history.write.watched_indices:
  - "financial-*"
  - "pii-*"
```
{% include copy.html %}

使用此組態時，稽核事件預設會寫入名為 `security-auditlog-YYYY.MM.dd` 的每日輪替索引。
