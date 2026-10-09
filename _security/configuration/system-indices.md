---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "系統索引"
parent: Configuration
nav_order: 60
redirect_from:
 - /security-plugin/configuration/system-indices/
---

# 系統索引

系統索引儲存由 OpenSearch 或 OpenSearch 外掛程式管理的狀態，例如安全性組態、非同步工作結果，以及外掛程式中繼資料。系統索引通常以句點 (`.`) 開頭，但以句點為前綴的索引不一定是系統索引。OpenSearch 依據 OpenSearch 及其外掛程式註冊的描述器來識別系統索引。

系統索引與一般索引的差異如下：

- 即使 `action.auto_create_index` 為 `false`，或其模式原本會排除該索引，OpenSearch 仍允許已註冊的系統索引自動建立。註冊系統索引並不會立即建立它；擁有該索引的元件通常會在首次儲存資料時建立。
- 僅針對系統索引的操作會使用 `system_read` 與 `system_write` 執行緒集區來處理支援的讀取與寫入路徑。這可將內部元件的工作與一般的搜尋及寫入流量隔離。混合系統索引與一般索引的請求可能會使用一般的執行緒集區。
- 系統索引應透過其擁有元件的 API 存取。當 Security 外掛程式啟用時，它會加入 [Security 外掛程式保護](#security-plugin-protection) 所描述的存取控制。

請勿直接修改系統索引。請使用擁有該索引之元件提供的 API。直接變更可能會損毀元件狀態，或在升級後變得不相容。
{: .warning}

## 標準發行版中的系統索引模式

下表列出標準 OpenSearch 發行版中各元件在啟動時註冊的描述器。擁有元件通常只在其功能首次儲存資料時才建立索引，因此索引不必存在也能註冊為系統索引。確切的集合可能隨 OpenSearch 版本而異，也可能取決於外掛程式設定。

| 元件 | 已註冊的索引模式 |
| :--- | :--- |
| OpenSearch task management | `.tasks*` |
| OpenSearch Dashboards | `.opensearch_dashboards`<br>`.opensearch_dashboards_*`<br>`.reporting-*`<br>`.apm-agent-configuration`<br>`.apm-custom-link` |
| Security plugin | `.opendistro_security` (可設定)<br>`.opensearch_security_api_tokens`<br>`.opendistro-anomaly-detectors-sharing`<br>`.opensearch-forecasters-sharing`<br>`.plugins-ml-model-group-sharing`<br>`.plugins-flow-framework-templates-sharing`<br>`.plugins-flow-framework-state-sharing`<br>`.opendistro-reports-definitions-sharing`<br>`.opendistro-reports-instances-sharing` |
| Alerting | `.opendistro-alerting-config`<br>`.opendistro-alerting-alert*`<br>`.opensearch-alerting-comments*` |
| Anomaly Detection and Forecasting | `.opendistro-anomaly-detectors`<br>`.opendistro-anomaly-detector-jobs`<br>`.opendistro-anomaly-results*`<br>`.opendistro-anomaly-checkpoints`<br>`.opendistro-anomaly-detection-state`<br>`.opensearch-forecasters`<br>`.opensearch-forecast-checkpoints`<br>`.opensearch-forecast-state` |
| Asynchronous Search | `.opendistro-asynchronous-search-response` |
| Cross-cluster Replication | `.replication-metadata-store` |
| Flow Framework | `.plugins-flow-framework-config`<br>`.plugins-flow-framework-templates`<br>`.plugins-flow-framework-state` |
| Geospatial | `.geospatial-ip2geo-data*`<br>`.scheduler-geospatial-ip2geo-datasource` |
| Index Management | `.opendistro-ism-config`<br>`.opendistro-ism-managed-index-history*`<br>`.opensearch-control-center` |
| Job Scheduler | `.opendistro-job-scheduler-lock`<br>`.job-scheduler-history` |
| k-NN | `.opensearch-knn-models` |
| Learning to Rank | `.ltrstore*` |
| ML Commons | `.plugins-ml-model`<br>`.plugins-ml-model-group`<br>`.plugins-ml-task`<br>`.plugins-ml-agent`<br>`.plugins-ml-connector`<br>`.plugins-ml-config`<br>`.plugins-ml-controller`<br>`.plugins-ml-jobs`<br>`.plugins-ml-am*`<br>`.plugins-ml-memory-meta`<br>`.plugins-ml-memory-message`<br>`.plugins-ml-mcp-tools`<br>`.plugins-ml-mcp-session-management`<br>`.plugins-ml-context-management-templates`<br>`.plugins-ml-stop-words` |
| Notifications | `.opensearch-notifications-config` |
| Observability | `.opensearch-observability`<br>`.opensearch-notebooks` |
| Reporting | `.opendistro-reports-definitions`<br>`.opendistro-reports-instances` |
| Search Relevance | `.plugins-search-relevance-experiment`<br>`.plugins-search-relevance-judgment-cache` |
| Security Analytics | `.opensearch-sap-correlation-alerts`<br>`.opensearch-sap-threat-intel` |
| SQL | `.ql-datasources`<br>`.query_execution_request*` |

由外掛程式建立或管理的索引不一定是系統索引。有些外掛程式建立的索引是一般索引，因為其內容是設計給使用者搜尋的。例如，Forecasting 外掛程式的結果索引是一般索引，即使該外掛程式的組態、檢查點與狀態索引是系統索引。同樣地，當 Security 外掛程式的稽核記錄儲存在 OpenSearch 中時，其索引或資料串流可供使用者搜尋，而不會註冊為系統索引。

## Security 外掛程式保護

Security 外掛程式預設一律保護其組態索引 `.opendistro_security`。當系統索引保護啟用時，該外掛程式也會保護向 OpenSearch 註冊的索引，以及在 `plugins.security.system_indices.indices` 中設定的任何舊版模式。

示範安全性組態會啟用系統索引保護：

```yml
plugins.security.system_indices.enabled: true
```

### 寫入保護

一般索引權限 (包括 `*` 的廣泛權限) 不會授予受保護系統索引的寫入存取權。只有在下列其中一種情況下才允許寫入：

- 註冊該系統索引的外掛程式以其外掛程式身分執行操作。
- 超級管理員使用[管理員憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/#configuring-admin-certificates)進行驗證。
- 已啟用系統索引權限，且某個角色明確授予該索引模式 `system:admin/system_index` 權限。此選項不會授予 Security 外掛程式組態索引的存取權。

請盡可能使用擁有該索引之外掛程式的 API，包括以超級管理員身分驗證時。例如，請使用 Security REST API 或 `securityadmin.sh` 來變更 Security 外掛程式組態，而不是將文件直接編製索引到 `.opendistro_security`。

### 讀取保護與經過濾的結果

讀取保護不會對每個 API 產生相同的回應。對於沒有系統索引存取權的使用者，Security 外掛程式可以將底層索引讀取器替換為空讀取器。因此：

- 搜尋可能會傳回 `200 OK` 且零個命中結果，即使存在符合的文件。
- get 請求的行為可能如同文件不存在。
- 無法安全篩選的操作可能會傳回 `403 Forbidden`。

請勿將成功的回應或空結果解讀為呼叫者具有系統索引存取權的證明。當 `plugins.security.system_indices.permission.enabled` 啟用時，來自沒有必要系統索引權限之使用者的明確請求通常會被拒絕，而不是傳回經過濾的搜尋結果。

`.tasks*` 系列是例外。Security 外掛程式允許讀取，讓獲得授權的使用者可以使用工作 API 並讀取已儲存的工作結果。OpenSearch 仍會保護對該索引的寫入。

若要直接讀取 Security 組態索引，請使用管理員憑證進行驗證：

```bash
curl -k --cert ./kirk.pem --key ./kirk-key.pem \
  -X GET 'https://localhost:9200/.opendistro_security/_search'
```
{% include copy.html %}

### 稽核記錄

當 Security 稽核記錄啟用時，存取 Security 外掛程式組態索引或其他受保護系統索引而被拒絕的嘗試，會記錄在 `OPENDISTRO_SECURITY_INDEX_ATTEMPT` 稽核類別中。此檢查與一般索引權限以及文件層級或欄位層級安全性是分開的，因此授予廣泛的索引權限無法繞過此保護或其稽核事件。如需稽核組態與排除類別的資訊，請參閱[稽核記錄]({{site.url}}{{site.baseurl}}/security/audit-logs/index/)。

## 設定其他系統索引

`plugins.security.system_indices.indices` 設定可以保護其他索引模式，但已不建議使用。現有部署可以在將外掛程式擁有的索引遷移至系統索引描述器時繼續使用它。由於它是靜態節點設定，每個節點都必須使用相同的值，並且在變更後必須重新啟動：

```yml
plugins.security.system_indices.enabled: true
plugins.security.system_indices.indices:
  - ".example-plugin-*"
```
{% include copy.html %}

如需授予使用者明確存取權的資訊，請參閱[系統索引權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/#system-index-permissions)。

## 供外掛程式開發人員使用的系統索引

擁有內部索引的外掛程式應向 OpenSearch 註冊這些索引，而不是要求管理員將模式加入 `plugins.security.system_indices.indices`。若要向 OpenSearch 註冊外掛程式的系統索引，請依照下列步驟：

1. 實作 `SystemIndexPlugin`，並為每個索引模式傳回一個 `SystemIndexDescriptor`。模式必須以 `.` 開頭，且不得與其他外掛程式註冊的描述器重疊。
2. 提供外掛程式專屬的動作與 REST API 來存取資料，而不是要求呼叫者使用標準索引 API。
3. 實作 `IdentityAwarePlugin`，並保留所獲指派的 `PluginSubject`。
4. 以獲指派的主體執行內部用戶端操作。`FilterClient` 包裝器可以一致地套用 `PluginSubject`，並在叫用非同步監聽器之前還原呼叫者的執行緒上下文。

當 Security 外掛程式已安裝時，僅呼叫 `ThreadContext.stashContext()` 並不足夠：暫存上下文會移除呼叫者的上下文，但不會建立授權存取該外掛程式所註冊系統索引所需的外掛程式身分。
{: .important}

如需實作範例，請參閱 Security 外掛程式的 [`PluginClient` 範例](https://github.com/opensearch-project/security/blob/main/sample-resource-plugin/src/main/java/org/opensearch/sample/utils/PluginClient.java) 與 [`SampleResourcePlugin`](https://github.com/opensearch-project/security/blob/main/sample-resource-plugin/src/main/java/org/opensearch/sample/SampleResourcePlugin.java)。
