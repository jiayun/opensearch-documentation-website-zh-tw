---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "稽核記錄檔欄位參考"
parent: Audit logs
nav_order: 130
redirect_from:
  - /security-plugin/audit-logs/field-reference/
---

# 稽核記錄檔欄位參考

本頁包含所有稽核記錄檔欄位的說明。


## 共同屬性

下列屬性會記錄於所有事件類別，與層級無關。

名稱 | 說明
:--- | :---
`audit_format_version` | 稽核記錄檔訊息格式的版本。
`audit_category` | 稽核記錄檔類別。值包括 `FAILED_LOGIN`、`MISSING_PRIVILEGES`、`BAD_HEADERS`、`SSL_EXCEPTION`、`OPENSEARCH_SECURITY_INDEX_ATTEMPT`、`AUTHENTICATED`、`GRANTED_PRIVILEGES`、`CLUSTER_SETTINGS_CHANGED` 與 `INDEX_SETTINGS_CHANGED`。
`audit_node_id ` | 產生事件的節點 ID。
`audit_node_name` | 產生事件的節點名稱。
`audit_node_host_address` | 產生事件的節點主機位址。
`audit_node_host_name` | 產生事件的節點主機名稱。
`audit_request_layer` | 產生事件的層級，為 TRANSPORT 或 REST。
`audit_request_origin` | 事件來源的層級，為 TRANSPORT 或 REST。
`audit_request_effective_user_is_admin` | 若請求是以 TLS 管理員憑證發出則為 true，否則為 false。


## REST FAILED_LOGIN 屬性

下列屬性會記錄於 REST 層級的登入失敗事件。

名稱 | 說明
:--- | :---
`audit_request_effective_user` | 驗證失敗的使用者名稱。
`audit_rest_request_path` | REST 端點 URI。
`audit_rest_request_params` | HTTP 請求參數（若有的話）。
`audit_rest_request_headers` | HTTP 標頭（若有的話）。
`audit_request_initiating_user` | 發起請求的使用者。僅在與有效使用者不同時記錄。
`audit_request_body` | HTTP 請求本文（若有的話，且已啟用請求本文記錄）。
`audit_rest_request_method` | HTTP 請求方法。


## REST AUTHENTICATED 屬性

下列屬性會記錄於 REST 層級的驗證成功事件。

名稱 | 說明
:--- | :---
`audit_request_effective_user` | 驗證失敗的使用者名稱。
`audit_request_initiating_user` | 發起請求的使用者。僅在與有效使用者不同時記錄。
`audit_rest_request_path` | REST 端點 URI。
`audit_rest_request_params` | HTTP 請求參數（若有的話）。
`audit_rest_request_headers` | HTTP 標頭（若有的話）。
`audit_request_body` | HTTP 請求本文（若有的話，且已啟用請求本文記錄）。
`audit_rest_request_method` | HTTP 請求方法。


## REST SSL_EXCEPTION 屬性

下列屬性會記錄於 REST 層級的 SSL 例外事件。

名稱 | 說明
:--- | :---
`audit_request_exception_stacktrace` | SSL 例外的堆疊追蹤。


## REST BAD_HEADERS 屬性

下列屬性會記錄於 REST 層級的錯誤標頭事件。

名稱 | 說明
:--- | :---
`audit_rest_request_path` | REST 端點 URI。
`audit_rest_request_params` | HTTP 請求參數（若有的話）。
`audit_rest_request_headers` | HTTP 標頭（若有的話）。
`audit_request_body` | HTTP 請求本文（若有的話，且已啟用請求本文記錄）。


## Transport FAILED_LOGIN 屬性

下列屬性會記錄於傳輸層級的登入失敗事件。

名稱 | 說明
:--- | :---
`audit_trace_task_id` | 請求的 ID。
`audit_transport_headers` | 請求的標頭（若有的話）。
`audit_request_effective_user` | 驗證失敗的使用者名稱。
`audit_request_initiating_user` | 發起請求的使用者。僅在與有效使用者不同時記錄。
`audit_transport_request_type` | 請求類型（例如 `IndexRequest`）。
`audit_request_body` | HTTP 請求本文（若有的話，且已啟用請求本文記錄）。
`audit_trace_indices` | 請求中包含的索引名稱。可包含萬用字元、日期模式與別名。僅在 `resolve_indices` 為 true 時記錄。
`audit_trace_resolved_indices` | 受該請求影響的已解析索引名稱。僅在 `resolve_indices` 為 true 時記錄。
`audit_trace_doc_types` | 受該請求影響的文件類型。僅在 `resolve_indices` 為 true 時記錄。


## Transport AUTHENTICATED 屬性

下列屬性會記錄於傳輸層級的驗證成功事件。

名稱 | 說明
:--- | :---
`audit_trace_task_id` | 請求的 ID。
`audit_transport_headers` | 請求的標頭（若有的話）。
`audit_request_effective_user` | 驗證失敗的使用者名稱。
`audit_request_initiating_user` | 發起請求的使用者。僅在與有效使用者不同時記錄。
`audit_transport_request_type` | 請求類型（例如 `IndexRequest`）。
`audit_request_body` | HTTP 請求本文（若有的話，且已啟用請求本文記錄）。
`audit_trace_indices` | 請求中包含的索引名稱。可包含萬用字元、日期模式與別名。僅在 `resolve_indices` 為 true 時記錄。
`audit_trace_resolved_indices` | 受該請求影響的已解析索引名稱。僅在 `resolve_indices` 為 true 時記錄。
`audit_trace_doc_types` | 受該請求影響的文件類型。僅在 `resolve_indices` 為 true 時記錄。


## Transport MISSING_PRIVILEGES 屬性

下列屬性會記錄於傳輸層級的缺少權限事件。

名稱 | 說明
:--- | :---
`audit_trace_task_id` | 請求的 ID。
`audit_trace_task_parent_id` | 此請求的父系 ID（若有的話）。
`audit_transport_headers` | 請求的標頭（若有的話）。
`audit_request_effective_user` | 驗證失敗的使用者名稱。
`audit_request_initiating_user` | 發起請求的使用者。僅在與有效使用者不同時記錄。
`audit_transport_request_type` | 請求類型（例如 `IndexRequest`）。
`audit_request_privilege` | 請求所需的權限（例如 `indices:data/read/search`）。
`audit_request_body` | HTTP 請求本文（若有的話，且已啟用請求本文記錄）。
`audit_trace_indices` | 請求中包含的索引名稱。可包含萬用字元、日期模式與別名。僅在 `resolve_indices` 為 true 時記錄。
`audit_trace_resolved_indices` | 受該請求影響的已解析索引名稱。僅在 `resolve_indices` 為 true 時記錄。
`audit_trace_doc_types` | 受該請求影響的文件類型。僅在 `resolve_indices` 為 true 時記錄。


## Transport GRANTED_PRIVILEGES 屬性

下列屬性會記錄於傳輸層級的已授權權限事件。

名稱 | 說明
:--- | :---
`audit_trace_task_id` | 請求的 ID。
`audit_trace_task_parent_id` | 此請求的父系 ID（若有的話）。
`audit_transport_headers` | 請求的標頭（若有的話）。
`audit_request_effective_user` | 驗證失敗的使用者名稱。
`audit_request_initiating_user` | 發起請求的使用者。僅在與有效使用者不同時記錄。
`audit_transport_request_type` | 請求類型（例如 `IndexRequest`）。
`audit_request_privilege` | 請求所需的權限（例如 `indices:data/read/search`）。
`audit_request_body` | HTTP 請求本文（若有的話，且已啟用請求本文記錄）。
`audit_trace_indices` | 請求中包含的索引名稱。可包含萬用字元、日期模式與別名。僅在 `resolve_indices` 為 true 時記錄。
`audit_trace_resolved_indices` | 受該請求影響的已解析索引名稱。僅在 `resolve_indices` 為 true 時記錄。
`audit_trace_doc_types` | 受該請求影響的文件類型。僅在 `resolve_indices` 為 true 時記錄。


## Transport SSL_EXCEPTION 屬性

傳輸層 SSL 例外事件會記錄下列屬性。

名稱 | 說明
:--- | :---
`audit_request_exception_stacktrace` | SSL 例外的堆疊追蹤。


## Transport BAD_HEADERS 屬性

傳輸層錯誤標頭事件會記錄下列屬性。

名稱 | 說明
:--- | :---
`audit_trace_task_id` | 請求的 ID。
`audit_trace_task_parent_id` | 此請求的父 ID (如果有的話)。
`audit_transport_headers` | 請求的標頭 (如果有的話)。
`audit_request_effective_user` | 驗證失敗的使用者名稱。
`audit_request_initiating_user` | 發起請求的使用者。僅在與有效使用者不同時才會記錄。
`audit_transport_request_type` | 請求類型 (例如 `IndexRequest`)。
`audit_request_body` | HTTP 請求本文 (如果有的話，且已啟用請求本文記錄)。
`audit_trace_indices` | 請求中包含的索引名稱。可包含萬用字元、日期模式與別名。僅在 `resolve_indices` 為 true 時才會記錄。
`audit_trace_resolved_indices` | 受該請求影響的已解析索引名稱。僅在 `resolve_indices` 為 true 時才會記錄。
`audit_trace_doc_types` | 受該請求影響的文件類型。僅在 `resolve_indices` 為 true 時才會記錄。


## Transport opensearch_SECURITY_INDEX_ATTEMPT 屬性

當請求嘗試存取 OpenSearch 安全性索引時，會記錄下列屬性。

名稱 | 說明
:--- | :---
`audit_trace_task_id` | 請求的 ID。
`audit_transport_headers` | 請求的標頭 (如果有的話)。
`audit_request_effective_user` | 驗證失敗的使用者名稱。
`audit_request_initiating_user` | 發起請求的使用者。僅在與有效使用者不同時才會記錄。
`audit_transport_request_type` | 請求類型 (例如 `IndexRequest`)。
`audit_request_body` | HTTP 請求本文 (如果有的話，且已啟用請求本文記錄)。
`audit_trace_indices` | 請求中包含的索引名稱。可包含萬用字元、日期模式與別名。僅在 `resolve_indices` 為 true 時才會記錄。
`audit_trace_resolved_indices` | 受該請求影響的已解析索引名稱。僅在 `resolve_indices` 為 true 時才會記錄。
`audit_trace_doc_types` | 受該請求影響的文件類型。僅在 `resolve_indices` 為 true 時才會記錄。


## Transport CLUSTER_SETTINGS_CHANGED 屬性

當叢集設定變更時，會記錄下列屬性。

名稱 | 說明
:--- | :---
`audit_request_effective_user` | 進行設定變更的使用者。
`audit_transport_request_type` | 請求類型 (例如 `ClusterUpdateSettingsRequest`)。
`audit_transport_action` | 傳輸動作 (例如 `cluster:admin/settings/update`)。
`audit_settings_changes` | 設定變更物件的陣列，每個物件包含 `setting`、`old_value`、`new_value`、`operation` 與 `scope`。敏感性設定會自動遮蔽。

`audit_settings_changes` 中的每個物件包含下列欄位。

名稱 | 說明
:--- | :---
`setting` | 完整設定名稱 (例如 `cluster.max_shards_per_node`)。
`old_value` | 設定的先前值，若先前未設定則為 `null`。
`new_value` | 設定的新值，若設定已被移除則為 `null`。
`operation` | 為 `set` (值已被指派) 或 `removed` (值已重設為預設)。
`scope` | 為 `persistent` (重新啟動後仍保留) 或 `transient` (重新啟動後遺失)。


## Transport INDEX_SETTINGS_CHANGED 屬性

當索引設定變更時，會記錄下列屬性。

名稱 | 說明
:--- | :---
`audit_request_effective_user` | 進行設定變更的使用者。
`audit_transport_request_type` | 請求類型 (例如 `UpdateSettingsRequest`)。
`audit_transport_action` | 傳輸動作 (例如 `indices:admin/settings/update`)。
`audit_trace_indices` | 請求中包含的索引名稱。可包含萬用字元與別名。
`audit_trace_resolved_indices` | 受該請求影響的已解析具體索引名稱。
`audit_settings_changes` | 設定變更物件的陣列，每個物件包含 `setting`、`old_value`、`new_value`、`operation` 與 `scope`。敏感性設定會自動遮蔽。

`audit_settings_changes` 中的每個物件包含下列欄位。

名稱 | 說明
:--- | :---
`setting` | 完整設定名稱 (例如 `index.number_of_replicas`)。
`old_value` | 設定的先前值，若先前未設定則為 `null`。
`new_value` | 設定的新值，若設定已被移除則為 `null`。
`operation` | 為 `set` (值已被指派) 或 `removed` (值已重設為預設)。
`scope` | 索引設定變更時一律為 `index`。
