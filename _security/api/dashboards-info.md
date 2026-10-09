---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Dashboards 資訊"
parent: Security APIs
nav_order: 160
redirect_from:
  - /security/api/dashboards-info/get-dashboards-info/
  - /security/api/dashboards-info/post-dashboards-info/
---

# Dashboards Info API
**於 1.0 版推出**
{: .label .label-purple }

擷取 OpenSearch Dashboards 動態安全性設定的目前值。

## 端點

```json
GET  /_plugins/_security/dashboardsinfo
POST /_plugins/_security/dashboardsinfo
```

兩種方法都不需要請求本文，且會傳回相同的回應。

## 範例請求

```json
GET _plugins/_security/dashboardsinfo
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "user_name": "admin",
  "not_fail_on_forbidden_enabled": false,
  "opensearch_dashboards_mt_enabled": true,
  "opensearch_dashboards_index": ".kibana",
  "opensearch_dashboards_server_user": "kibanaserver",
  "multitenancy_enabled": true,
  "preferred_tenants": [],
  "private_tenant_enabled": true,
  "default_tenant": "Global",
  "sign_in_options": [],
  "password_validation_error_message": "Password should be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.",
  "password_validation_regex": "(?=.*[A-Z])(?=.*[^a-zA-Z\\d])(?=.*[0-9])(?=.*[a-z]).{8,}",
  "resource_sharing_enabled": false,
  "api_tokens_enabled": false,
  "max_duration_seconds": 7776000
}
```

## 回應本文欄位

回應本文是含有下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `user_name` | 字串 | 目前使用者的名稱。 |
| `not_fail_on_forbidden_enabled` | 布林值 | OpenSearch 是否從搜尋回應中省略使用者無法存取的結果，而非傳回錯誤。 |
| `multitenancy_enabled` | 布林值 | 是否啟用多租用戶。 |
| `opensearch_dashboards_mt_enabled` | 布林值 | 是否為 OpenSearch Dashboards 啟用多租用戶。 |
| `opensearch_dashboards_index` | 字串 | OpenSearch Dashboards 儲存其已儲存物件的索引名稱。 |
| `opensearch_dashboards_server_user` | 字串 | OpenSearch Dashboards 用來連線至 OpenSearch 的使用者名稱。 |
| `default_tenant` | 字串 | OpenSearch Dashboards 預設開啟的租用戶。 |
| `private_tenant_enabled` | 布林值 | 使用者是否可以使用其私人租用戶。 |
| `preferred_tenants` | 字串陣列 | 在租用戶選取器中依偏好順序列在其他租用戶之前的租用戶。 |
| `sign_in_options` | 字串陣列 | OpenSearch Dashboards 提供的登入方法。 |
| `password_validation_regex` | 字串 | 新密碼必須符合的正規表示式。 |
| `password_validation_error_message` | 字串 | 當密碼不符合 `password_validation_regex` 時，OpenSearch Dashboards 顯示的訊息。 |
| `resource_sharing_enabled` | 布林值 | 是否啟用資源共用功能。 |
| `api_tokens_enabled` | 布林值 | 是否啟用 API 金鑰 API。 |
| `max_duration_seconds` | 整數 | API 金鑰可被授予的最長存續時間 (以秒為單位)。 |
