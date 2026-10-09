---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "更新稽核組態"
parent: Audit log APIs
grand_parent: Security APIs
nav_order: 10
---

# 更新稽核組態 API
**於 1.0 版導入**
{: .label .label-purple }

開啟或關閉稽核記錄，並取代稽核記錄與合規組態。

如需有關使用稽核記錄追蹤叢集存取的更多資訊，請參閱 [稽核記錄檔]({{site.url}}{{site.baseurl}}/security/audit-logs/index/)。

稽核記錄最初是在 `config/opensearch-security` 目錄中的 `audit.yml` 檔案內設定。之後，請使用此 API 或 OpenSearch Dashboards 來變更組態。
{: .note}

<!-- spec_insert_start
api: security.update_audit_configuration
component: endpoints
-->
## 端點
```json
PUT /_plugins/_security/api/audit/config
```
<!-- spec_insert_end -->

## 請求本文欄位

請求本文為必要。它是一個包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `enabled` | 布林值 | 稽核記錄是否開啟。預設為 `true`。 |
| `audit` | 物件 | 稽核記錄組態。 |
| `audit.enable_rest` | 布林值 | 是否稽核傳送至 REST 層的請求。預設為 `true`。 |
| `audit.enable_transport` | 布林值 | 是否稽核傳送至傳輸層的請求。預設為 `true`。 |
| `audit.disabled_rest_categories` | 字串陣列 | 要從 REST 層稽核中排除的類別。預設為 `["AUTHENTICATED", "GRANTED_PRIVILEGES"]`。 |
| `audit.disabled_transport_categories` | 字串陣列 | 要從傳輸層稽核中排除的類別。預設為 `["AUTHENTICATED", "GRANTED_PRIVILEGES"]`。 |
| `audit.ignore_users` | 字串陣列 | 要從稽核中排除的使用者。支援萬用字元模式，例如 `["test-user", "employee-*"]`。 |
| `audit.ignore_requests` | 字串陣列 | 要從稽核中排除的請求。支援萬用字元模式，例如 `["indices:data/read/*", "SearchRequest"]`。 |
| `audit.log_request_body` | 布林值 | 在 REST 層與傳輸層中，是否在可用時包含請求本文。預設為 `true`。 |
| `audit.resolve_indices` | 布林值 | 是否記錄請求影響的所有索引，並解析別名、萬用字元與日期模式。預設為 `true`。 |
| `audit.resolve_bulk_requests` | 布林值 | 是否記錄大量請求中的個別操作。預設為 `false`。 |
| `audit.exclude_sensitive_headers` | 布林值 | 是否從記錄檔中省略敏感性標頭。預設為 `true`。 |
| `compliance` | 物件 | 合規記錄組態。 |
| `compliance.enabled` | 布林值 | 合規記錄是否開啟。預設為 `true`。 |
| `compliance.write_log_diffs` | 布林值 | 是否只記錄文件更新的差異。預設為 `false`。 |
| `compliance.read_watched_fields` | 物件 | 要監視讀取事件的索引與欄位。索引名稱與欄位名稱皆支援萬用字元模式。 |
| `compliance.read_ignore_users` | 字串陣列 | 讀取事件要忽略的使用者。支援萬用字元模式，例如 `["test-user", "employee-*"]`。 |
| `compliance.read_metadata_only` | 布林值 | 讀取事件是否只記錄文件中繼資料。預設為 `true`。 |
| `compliance.write_watched_indices` | 字串陣列 | 要監視寫入事件的索引。支援萬用字元模式，例如 `["logs-*"]`。 |
| `compliance.write_ignore_users` | 字串陣列 | 寫入事件要忽略的使用者。支援萬用字元模式，例如 `["test-user", "employee-*"]`。 |
| `compliance.write_metadata_only` | 布林值 | 寫入事件是否只記錄文件中繼資料。預設為 `true`。 |
| `compliance.external_config` | 布林值 | 是否記錄節點的外部組態檔案。預設為 `false`。 |
| `compliance.internal_config` | 布林值 | 是否記錄內部安全性組態的更新。預設為 `true`。 |

`_readonly` 屬性無法修改。變更該屬性的請求會傳回 `409` 錯誤：

```json
{
  "status": "error",
  "reason": "Invalid configuration",
  "invalid_keys": {
    "keys": "_readonly,config"
  }
}
```

## 範例請求

```json
PUT _plugins/_security/api/audit/config
{
  "audit": {
    "disabled_categories": [],
    "disabled_rest_categories": [
      "AUTHENTICATED",
      "GRANTED_PRIVILEGES"
    ],
    "disabled_transport_categories": [
      "AUTHENTICATED",
      "GRANTED_PRIVILEGES",
      "CLUSTER_SETTINGS_CHANGED",
      "INDEX_SETTINGS_CHANGED"
    ],
    "enable_rest": true,
    "enable_transport": true,
    "exclude_sensitive_headers": true,
    "ignore_headers": [],
    "ignore_requests": [],
    "ignore_url_params": [],
    "ignore_users": [
      "kibanaserver"
    ],
    "log_request_body": true,
    "resolve_bulk_requests": false,
    "resolve_indices": true
  },
  "compliance": {
    "enabled": true,
    "external_config": false,
    "internal_config": true,
    "read_ignore_users": [
      "kibanaserver"
    ],
    "read_metadata_only": true,
    "read_watched_fields": {},
    "write_ignore_users": [
      "kibanaserver"
    ],
    "write_log_diffs": false,
    "write_metadata_only": true,
    "write_watched_indices": []
  },
  "enabled": true
}
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "status": "OK",
  "message": "'config' updated."
}
```

## 回應本文欄位

回應本文是一個包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `status` | 字串 | 請求的狀態。成功的請求會傳回 `OK`。 |
| `message` | 字串 | 描述操作結果的訊息。 |
