---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "權限"
parent: Access control
nav_order: 75
redirect_from:
  - /security-plugin/access-control/permissions/
---

# 安全性權限

Security 外掛程式中的每個權限會控制對 OpenSearch 叢集可執行之特定動作的存取，例如將文件編製索引或檢查叢集健康狀態。

大多數權限的名稱本身即說明其用途。例如，`cluster:admin/ingest/pipeline/get` 可讓您擷取資料匯入管線的相關資訊。_在許多情況下_，權限會對應到特定的 REST API 操作，例如 `GET _ingest/pipeline`。

儘管有此對應關係，權限**不會**直接對應到 REST API 操作。`POST _bulk` 和 `GET _msearch` 等操作可在單一請求中存取多個索引並執行多個動作。即使是像 `GET _cat/nodes` 這樣的簡單請求，也會執行多個動作才能產生其回應。

簡而言之，僅控制對 REST API 的存取並不足夠。反之，Security 外掛程式控制的是對底層 OpenSearch 動作的存取。

例如，請考慮下列 `_bulk` 請求：

```json
POST _bulk
{ "delete": { "_index": "test-index", "_id": "tt2229499" } }
{ "index": { "_index": "test-index", "_id": "tt1979320" } }
{ "title": "Rush", "year": 2013 }
{ "create": { "_index": "test-index", "_id": "tt1392214" } }
{ "title": "Prisoners", "year": 2013 }
{ "update": { "_index": "test-index", "_id": "tt0816711" } }
{ "doc" : { "title": "World War Z" } }

```

若要讓此請求成功，您必須具備 `test-index` 的下列權限：

- `indices:data/write/bulk*`
- `indices:data/write/delete`
- `indices:data/write/index`
- `indices:data/write/update`

這些權限也可讓您新增、更新或刪除文件（例如 `PUT test-index/_doc/tt0816711`），因為它們控管的是將文件編製索引及刪除文件等底層 OpenSearch 動作，而非特定的 API 路徑與 HTTP 方法。


## 測試權限

如果您想讓使用者只擁有執行某項功能所需的絕對最低權限組合——即[最小權限原則](https://en.wikipedia.org/wiki/Principle_of_least_privilege)——最好的做法是以新的測試使用者身分，將具代表性的請求傳送至您的叢集。發生權限錯誤時，Security 外掛程式會非常明確地指出缺少哪些權限。請考慮下列請求和回應：

```json
GET _cat/shards?v

{
  "error": {
    "root_cause": [{
      "type": "security_exception",
      "reason": "no permissions for [indices:monitor/stats] and User [name=test-user, backend_roles=[], requestedTenant=null]"
    }]
  },
  "status": 403
}
```

上述請求會執行實際操作來測試權限。若要在不執行操作的情況下模擬檢查，請將 `perform_permission_check` 查詢參數設為 `true`：

```json
PUT /my_index/_doc/1?perform_permission_check=true
{
   "title": "Test Document"
}
```
{% include copy-curl.html security=true %}

回應會指出使用者是否具備足夠權限可執行該操作，並列出任何缺少的權限。此選項特別適合安全地測試 `POST`、`PUT` 和 `DELETE` 等操作。

當使用者具備足夠權限時，回應會類似下列內容：

```json
{
   "accessAllowed": true,
   "missingPrivileges": []
}
```

當使用者不具備足夠權限時，回應會列出缺少的權限：

```json
{
   "accessAllowed": false,
   "missingPrivileges": ["indices:data/write/index"]
}
```

[建立使用者和角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/)、將角色對應到使用者，然後開始使用 cURL、Postman 或任何其他用戶端傳送已簽署的請求。接著在遇到錯誤時，逐步將權限新增至角色。即使您解決了一個權限錯誤，同一個請求仍可能產生新的錯誤；此外掛程式只會傳回它遇到的第一個錯誤，因此請持續嘗試，直到請求成功為止。

您通常可以使用預設動作群組的組合來達成所需的安全性態勢，而不必逐一設定個別權限。如需各群組所授予權限的說明，請參閱[預設動作群組]({{site.url}}{{site.baseurl}}/security/access-control/default-action-groups/)。
{: .tip }


## 系統索引權限

系統索引權限與其他權限不同之處，在於它們會將部分傳統上僅限管理員使用的存取權延伸給非管理員使用者。這些權限可讓一般使用者修改其對應角色中所指定的任何系統索引。唯一的例外是安全性系統索引 `.opendistro_security`，該索引用於儲存 Security 外掛程式的組態 YAML 檔案，且僅供持有管理員憑證的管理員存取。

除了標準索引權限之外，您還可以在 `roles.yml` 組態檔的 `index_permissions` 下指定系統索引權限（請參閱 [roles.yml]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#rolesyml)）。這涉及兩個步驟：1) 在 `index_patterns` 區段中新增系統索引，以及 2) 在角色的 `allowed_actions` 區段中指定 `system:admin/system_index`。

例如，授予使用者修改儲存 Alerting 外掛程式組態之系統索引權限的系統索引權限，是由索引模式 `.opendistro-alerting-config` 所定義，而其允許的動作則定義為 `system:admin/system_index`。下列角色顯示此系統索引權限如何與其他屬性一起設定：

```yml
alerting-role:
  reserved: true
  hidden: false
  cluster_permissions:
    - 'cluster:admin/opendistro/alerting/alerts/ack'
    - 'cluster:admin/opendistro/alerting/alerts/get'
  index_permissions:
    - index_patterns:
        - .opendistro-alerting-config
    - allowed_actions:
        - 'system:admin/system_index'
```
{% include copy.html %}

系統索引權限也可搭配萬用字元使用，以包含部分系統索引名稱的所有變化形式。這可能很有用，但應謹慎使用，以免無意間授予系統索引的存取權。為角色指定系統索引時，請留意下列考量事項：

* 指定系統索引的完整名稱會將存取權限制為僅該索引：`.opendistro-alerting-config`。
* 指定系統索引的部分名稱並搭配萬用字元，會授予開頭為該名稱之所有系統索引的存取權：`.opendistro-anomaly-detector*`。
* 雖然不建議——因為此角色定義會授予廣泛的存取權——但使用 `*` 作為索引模式並以 `system:admin/system_index` 作為允許的動作，會授予所有系統索引的存取權。

  僅在 `allowed_actions` 下輸入萬用字元 `*` 並不會自動授予系統索引的存取權。必須明確新增允許的動作 `system:admin/system_index`。
  {: .note }

下列範例顯示授予所有系統索引存取權的角色：

```yml
index_permissions:
    - index_patterns:
        - '*'
    - allowed_actions:
        - 'system:admin/system_index'
```


### 驗證系統索引存取

您可以使用 [CAT indices]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-indices/) 操作，查看與權限組態中任何索引模式相關聯的所有索引，並驗證權限是否提供您預期的存取權。例如，如果您想驗證包含開頭為前置詞 `.kibana` 之系統索引的權限，可以執行 `GET /_cat/indices/.kibana*` 呼叫，以傳回與該前置詞相關聯的所有索引。

下列範例回應顯示與索引模式 `.kibana*` 相關聯的三個系統索引：

```json
health | status | index | uuid | pri | rep | docs.count | docs.deleted | store.size | pri.store.size
green open .kibana_1 XmTePICFRoSNf5O5uLgwRw 1 1 220 0 468.3kb 232.1kb
green open .kibana_2 XmTePICFRoSNf5O5uLgwRw 1 1 220 0 468.3kb 232.1kb
green open .kibana_3 XmTePICFRoSNf5O5uLgwRw 1 1 220 0 468.3kb 232.1kb
```


### 啟用系統索引權限

具有 [`restapi:admin/roles`]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api) 權限的使用者，可以在 `roles.yml` 檔案中，使用與叢集或索引權限相同的方式，將系統索引權限對應至所有使用者。不過，為了保留對此權限的一定控制，`plugins.security.system_indices.permission.enabled` 設定可讓您啟用或停用系統索引權限功能。此設定預設為停用。若要啟用系統索引權限功能，請將 `plugins.security.system_indices.permissions.enabled` 設為 `true`。如需此設定的詳細資訊，請參閱[啟用使用者對系統索引的存取權]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#enabling-user-access-to-system-indexes)。

請留意，啟用此功能並將系統索引權限對應至一般使用者，會讓這些使用者能夠存取可能包含敏感資訊及對叢集健全狀態至關重要之組態的索引。我們也建議您在將使用者對應至 `restapi:admin/roles` 時謹慎操作，因為此權限不僅讓使用者能將系統索引權限指派給其他使用者，也能自行指派任何系統索引的存取權給自己。
{: .warning }

### `do_not_fail_on_forbidden`

如果使用者嘗試查詢多個索引，但沒有其中部分索引的權限，依預設，他們會在 OpenSearch Dashboards 中收到 `error`，或在使用 `cURL` 或 API 時收到 `exception`。如果您希望使用者收到他們_確實_具有權限之索引的搜尋結果，可以在 `config.yml` 中將 `do_not_fail_on_forbidden` 選項設為 `true`。請參閱下列範例：

```
_meta:
  type: "config"
  config_version: 2
config:
  dynamic:
    http:
      anonymous_auth_enabled: false
      xff:
        enabled: false
        internalProxies: "192\\.168\\.0\\.10|192\\.168\\.0\\.11"
    do_not_fail_on_forbidden: true
    authc:
      basic_internal_auth_domain:
      ...
```
請務必記住，如果此選項設為 `true`，提供給使用者的資料會被視為完整資料集。系統不會顯示任何提示，告知使用者可能有部分資料遭到省略。
{: .warning }

### `do_not_fail_on_forbidden_empty`

當使用者嘗試檢視其沒有索引權限的視覺化時，會看到 `error` 取代該視覺化。若要變更此行為以顯示 `No results displayed because all values equal 0.`，您可以在 `config.yml` 中將 `do_not_fail_on_forbidden_empty` 設為 `true`。只有在 `do_not_fail_on_forbidden` 也設為 `true` 時，此選項才有效。請參閱下列範例：

```
_meta:
  type: "config"
  config_version: 2
config:
  dynamic:
    http:
      anonymous_auth_enabled: false
      xff:
        enabled: false
        internalProxies: "192\\.168\\.0\\.10|192\\.168\\.0\\.11"
    do_not_fail_on_forbidden: true
    do_not_fail_on_forbidden_empty: true
    authc:
      basic_internal_auth_domain:
      ...
```

## 叢集權限

這些權限適用於叢集，無法以細粒度套用。例如，您只有具備或不具備建立快照（`cluster:admin/snapshot/create`）的權限這兩種情況。因此，叢集權限無法授予使用者為特定一組索引建立快照的權限，同時禁止使用者為其他索引建立快照。

以下權限中提供的 API 文件交叉參照，僅旨在協助您瞭解這些權限。如本節開頭所述，權限通常與 API 相關，但並非直接對應至 API。
{: .note }


### 全叢集索引權限

| **權限** | **說明** |
| :--- | :--- |
| `indices:admin/template/delete` |  [刪除索引範本]({{site.url}}{{site.baseurl}}/api-reference/index-apis/delete-index-template/)的權限。 |
| `indices:admin/template/get` |  [取得索引範本]({{site.url}}{{site.baseurl}}/api-reference/index-apis/get-index-template/)的權限。 |
| `indices:admin/template/put` |  [建立索引範本]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index-template/)的權限。 |
| `indices:data/read/scroll` |  捲動瀏覽資料的權限。此設定必須同時設定為叢集層級及索引層級的權限。 |
| `indices:data/read/scroll/clear` | 清除捲動物件的權限。此設定必須同時設定為叢集層級及索引層級的權限。 |
| `indices:data/read/mget` |  在一個請求中執行[多個 GET 操作]({{site.url}}{{site.baseurl}}/api-reference/document-apis/multi-get/)的權限。 |
| `indices:data/read/mget*` |  在一個請求中執行多個 GET 操作的權限。此設定必須同時設定為叢集層級及索引層級的權限。 |
| `indices:data/read/msearch` |  在單一 API 請求中執行[多個搜尋]({{site.url}}{{site.baseurl}}/api-reference/multi-search/)請求的權限。此設定必須同時設定為叢集層級及索引層級的權限。 |
| `indices:data/read/msearch/template` |  將[多個搜尋範本]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/index/#multiple-search-templates)組合起來，並在單一請求中傳送至您的 OpenSearch 叢集的權限。此設定必須同時設定為叢集層級及索引層級的權限。 |
| `indices:data/read/mtv` |  透過單一請求擷取多個詞彙向量的權限。此設定必須同時設定為叢集層級及索引層級的權限。 |
| `indices:data/read/mtv*` |  透過單一請求擷取多個詞彙向量的權限。此設定必須同時設定為叢集層級及索引層級的權限。 |
| `indices:data/read/search/template/render` |  呈現搜尋範本的權限。此設定必須同時設定為叢集層級及索引層級的權限。 |
| `indices:data/write/bulk` |  執行 [bulk]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 請求的權限。此設定必須同時設定為叢集層級及索引層級的權限。 |
| `indices:data/write/bulk*` |  執行 bulk 請求的權限。此設定必須同時設定為叢集層級及索引層級的權限。 |
| `indices:data/write/reindex` |  執行[重新編製索引]({{site.url}}{{site.baseurl}}/im-plugin/reindex-data/)操作的權限。 |

### Ingest API 權限

請參閱 [Ingest APIs]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/)。

- `cluster:admin/ingest/pipeline/delete`
- `cluster:admin/ingest/pipeline/get`
- `cluster:admin/ingest/pipeline/put`
- `cluster:admin/ingest/pipeline/simulate`
- `cluster:admin/ingest/processor/grok/get`

### 異常偵測權限

請參閱 [Anomaly Detection API]({{site.url}}{{site.baseurl}}/observing-your-data/ad/api/)。

- `cluster:admin/opendistro/ad/detector/delete`
- `cluster:admin/opendistro/ad/detector/info`
- `cluster:admin/opendistro/ad/detector/jobmanagement`
- `cluster:admin/opendistro/ad/detector/preview`
- `cluster:admin/opendistro/ad/detector/run`
- `cluster:admin/opendistro/ad/detector/search`
- `cluster:admin/opendistro/ad/detector/stats`
- `cluster:admin/opendistro/ad/detector/write`
- `cluster:admin/opendistro/ad/detector/validate`
- `cluster:admin/opendistro/ad/detectors/get`
- `cluster:admin/opendistro/ad/result/search`
- `cluster:admin/opendistro/ad/result/topAnomalies`
- `cluster:admin/opendistro/ad/tasks/search`

### 警示權限

請參閱 [Alerting API]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/api/)。

- `cluster:admin/opendistro/alerting/alerts/ack`
- `cluster:admin/opendistro/alerting/alerts/get`
- `cluster:admin/opendistro/alerting/destination/delete`
- `cluster:admin/opendistro/alerting/destination/email_account/delete`
- `cluster:admin/opendistro/alerting/destination/email_account/get`
- `cluster:admin/opendistro/alerting/destination/email_account/search`
- `cluster:admin/opendistro/alerting/destination/email_account/write`
- `cluster:admin/opendistro/alerting/destination/email_group/delete`
- `cluster:admin/opendistro/alerting/destination/email_group/get`
- `cluster:admin/opendistro/alerting/destination/email_group/search`
- `cluster:admin/opendistro/alerting/destination/email_group/write`
- `cluster:admin/opendistro/alerting/destination/get`
- `cluster:admin/opendistro/alerting/destination/write`
- `cluster:admin/opendistro/alerting/monitor/delete`
- `cluster:admin/opendistro/alerting/monitor/execute`
- `cluster:admin/opendistro/alerting/monitor/get`
- `cluster:admin/opendistro/alerting/monitor/search`
- `cluster:admin/opendistro/alerting/monitor/write`
- `cluster:admin/opensearch/alerting/remote/indexes/get`

### 非同步搜尋權限

請參閱 [非同步搜尋]({{site.url}}{{site.baseurl}}/search-plugins/async/index/)。

- `cluster:admin/opendistro/asynchronous_search/stats`
- `cluster:admin/opendistro/asynchronous_search/delete`
- `cluster:admin/opendistro/asynchronous_search/get`
- `cluster:admin/opendistro/asynchronous_search/submit`

### 索引狀態管理權限

請參閱 [ISM API]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/)。

- `cluster:indices:admin/opensearch/ism/managedindex`
- `cluster:admin/opendistro/ism/managedindex/add`
- `cluster:admin/opendistro/ism/managedindex/change`
- `cluster:admin/opendistro/ism/managedindex/remove`
- `cluster:admin/opendistro/ism/managedindex/explain`
- `cluster:admin/opendistro/ism/managedindex/retry`
- `cluster:admin/opendistro/ism/policy/write`
- `cluster:admin/opendistro/ism/policy/get`
- `cluster:admin/opendistro/ism/policy/search`
- `cluster:admin/opendistro/ism/policy/delete`

### 索引 rollup 權限

請參閱 [Index rollups API]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/rollup-api/)。

- `cluster:admin/opendistro/rollup/index`
- `cluster:admin/opendistro/rollup/get`
- `cluster:admin/opendistro/rollup/search`
- `cluster:admin/opendistro/rollup/delete`
- `cluster:admin/opendistro/rollup/start`
- `cluster:admin/opendistro/rollup/stop`
- `cluster:admin/opendistro/rollup/explain`

### 報告權限

請參閱 [使用 Dashboards 介面建立報告]({{site.url}}{{site.baseurl}}/dashboards/reporting/)。

- `cluster:admin/opendistro/reports/definition/create`
- `cluster:admin/opendistro/reports/definition/update`
- `cluster:admin/opendistro/reports/definition/on_demand`
- `cluster:admin/opendistro/reports/definition/delete`
- `cluster:admin/opendistro/reports/definition/get`
- `cluster:admin/opendistro/reports/definition/list`
- `cluster:admin/opendistro/reports/instance/list`
- `cluster:admin/opendistro/reports/instance/get`
- `cluster:admin/opendistro/reports/menu/download`

### 轉換任務權限

請參閱 [Transforms API]({{site.url}}{{site.baseurl}}/im-plugin/index-transforms/transforms-apis/)

- `cluster:admin/opendistro/transform/index`
- `cluster:admin/opendistro/transform/get`
- `cluster:admin/opendistro/transform/preview`
- `cluster:admin/opendistro/transform/delete`
- `cluster:admin/opendistro/transform/start`
- `cluster:admin/opendistro/transform/stop`
- `cluster:admin/opendistro/transform/explain`

### 可觀測性權限

請參閱 [可觀測性安全性]({{site.url}}{{site.baseurl}}/observing-your-data/observability-security/)。

- `cluster:admin/opensearch/observability/create`
- `cluster:admin/opensearch/observability/update`
- `cluster:admin/opensearch/observability/delete`
- `cluster:admin/opensearch/observability/get`

### 跨叢集複寫

請參閱 [跨叢集複寫安全性]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/permissions/)。

- `cluster:admin/plugins/replication/autofollow/update`

### 重新索引

請參閱 [Reindex 文件]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/)。

- `cluster:admin/reindex/rethrottle`

### 快照儲存庫權限

請參閱 [Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/index/)。

- `cluster:admin/repository/delete`
- `cluster:admin/repository/get`
- `cluster:admin/repository/put`
- `cluster:admin/repository/verify`

### 重新路由

請參閱 [叢集管理員任務節流]({{site.url}}{{site.baseurl}}/tuning-your-cluster/cluster-manager-task-throttling/)。

- `cluster:admin/reroute`

### 指令碼權限

請參閱 [Script API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/index/)。

- `cluster:admin/script/delete`
- `cluster:admin/script/get`
- `cluster:admin/script/put`

### 更新設定權限

請參閱 Index API 頁面上的 [更新設定]({{site.url}}{{site.baseurl}}/api-reference/index-apis/update-settings/)。

- `cluster:admin/settings/update`

### 快照權限

請參閱 [Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/index/)。

- `cluster:admin/snapshot/create`
- `cluster:admin/snapshot/delete`
- `cluster:admin/snapshot/get`
- `cluster:admin/snapshot/restore`
- `cluster:admin/snapshot/status`
- `cluster:admin/snapshot/status*`

### 任務權限

請參閱 API Reference 章節中的 [Tasks]({{site.url}}{{site.baseurl}}/api-reference/tasks/)。

- `cluster:admin/tasks/cancel`
- `cluster:admin/tasks/test`
- `cluster:admin/tasks/testunblock`

### 資料來源權限

請參閱 [資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/)

- `cluster:admin/opensearch/ql/datasources/create`
- `cluster:admin/opensearch/ql/datasources/read`
- `cluster:admin/opensearch/ql/datasources/update`
- `cluster:admin/opensearch/ql/datasources/delete`
- `cluster:admin/opensearch/ql/datasources/patch`
- `cluster:admin/opensearch/ql/async_query/create`
- `cluster:admin/opensearch/ql/async_query/result`
- `cluster:admin/opensearch/ql/async_query/delete`

### 安全性分析權限

請參閱 [API 工具]({{site.url}}{{site.baseurl}}/security-analytics/api-tools/index/)。

| **權限** | **說明** |
| :--- | :--- |
| `cluster:admin/opensearch/securityanalytics/alerts/get` | 取得警示的權限 |
| `cluster:admin/opensearch/securityanalytics/alerts/ack` | 確認警示的權限 |
| `cluster:admin/opensearch/securityanalytics/detector/get` | 取得偵測器的權限 |
| `cluster:admin/opensearch/securityanalytics/detector/search` | 搜尋偵測器的權限 |
| `cluster:admin/opensearch/securityanalytics/detector/write` | 建立及更新偵測器的權限 |
| `cluster:admin/opensearch/securityanalytics/detector/delete` | 刪除偵測器的權限 |
| `cluster:admin/opensearch/securityanalytics/findings/get` | 取得發現項目的權限 |
| `cluster:admin/opensearch/securityanalytics/mapping/get` | 依索引取得欄位對應的權限 |
| `cluster:admin/opensearch/securityanalytics/mapping/view/get` | 依索引取得欄位對應並檢視已對應與未對應欄位的權限 |
| `cluster:admin/opensearch/securityanalytics/mapping/create` | 建立欄位對應的權限 |
| `cluster:admin/opensearch/securityanalytics/mapping/update` | 更新欄位對應的權限 |
| `cluster:admin/opensearch/securityanalytics/rules/categories` | 取得所有規則類別的權限 |
| `cluster:admin/opensearch/securityanalytics/rule/write` | 建立及更新規則的權限 |
| `cluster:admin/opensearch/securityanalytics/rule/search` | 搜尋規則的權限 |
| `cluster:admin/opensearch/securityanalytics/rules/validate` | 驗證規則的權限 |
| `cluster:admin/opensearch/securityanalytics/rule/delete` | 刪除規則的權限 |

### 監控權限

用於監控叢集的叢集權限適用於唯讀作業，例如檢查叢集健康狀態，以及取得節點使用情況或叢集中執行之任務的相關資訊。

請參閱 [REST API 參考]({{site.url}}{{site.baseurl}}/api-reference/index/)。

- `cluster:monitor/allocation/explain`
- `cluster:monitor/health`
- `cluster:monitor/main`
- `cluster:monitor/nodes/hot_threads`
- `cluster:monitor/nodes/info`
- `cluster:monitor/nodes/liveness`
- `cluster:monitor/nodes/stats`
- `cluster:monitor/nodes/usage`
- `cluster:monitor/remote/info`
- `cluster:monitor/state`
- `cluster:monitor/stats`
- `cluster:monitor/task`
- `cluster:monitor/task/get`
- `cluster:monitor/tasks/lists`

### 索引範本

索引範本權限雖然針對索引，但會全域套用至叢集。

請參閱[索引範本]({{site.url}}{{site.baseurl}}/im-plugin/index-templates/)。

- `indices:admin/index_template/delete`
- `indices:admin/index_template/get`
- `indices:admin/index_template/put`
- `indices:admin/index_template/simulate`
- `indices:admin/index_template/simulate_index`


## 索引權限

這些權限適用於索引或索引模式。您可能希望使用者擁有所有索引的讀取權限（即 `*`），但只擁有少數索引的寫入權限（例如 `web-logs` 和 `product-catalog`）。

| **權限** | **說明** |
| :--- | :--- |
| `indices:admin/aliases` |  [索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)的權限。 |
| `indices:admin/aliases/get` |  取得[索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)的權限。 |
| `indices:admin/analyze` |  使用 [Analyze API]({{site.url}}{{site.baseurl}}/api-reference/analyze-apis/) 的權限。 |
| `indices:admin/cache/clear` |  [清除快取]({{site.url}}{{site.baseurl}}/api-reference/index-apis/clear-index-cache/)的權限。 |
| `indices:admin/close` |  [關閉索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/close-index/)的權限。 |
| `indices:admin/close*` |  [關閉索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/close-index/)的權限。 |
| `indices:admin/create` |  [建立索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/)的權限。 |
| `indices:admin/data_stream/create` |  建立[資料串流]({{site.url}}{{site.baseurl}}/api-reference/data-stream/create-data-stream/)的權限。 |
| `indices:admin/data_stream/delete` |  [刪除資料串流]({{site.url}}{{site.baseurl}}/api-reference/data-stream/delete-data-stream/)的權限。 |
| `indices:admin/data_stream/get` |  [取得資料串流]({{site.url}}{{site.baseurl}}/api-reference/data-stream/data-stream-info/)的權限。 |
| `indices:admin/delete` |  [刪除索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/delete-index/)的權限。 |
| `indices:admin/exists` |  使用 [exists 查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/exists/)的權限。 |
| `indices:admin/flush` |  [排清索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/flush/)的權限。 |
| `indices:admin/flush*` |  [排清索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/flush/)的權限。 |
| `indices:admin/forcemerge` |  強制合併索引和資料串流的權限。 |
| `indices:admin/get` |  取得索引和對應的權限。 |
| `indices:admin/mapping/put` |  將新對應和欄位新增至索引的權限。 |
| `indices:admin/mappings/fields/get` |  取得對應欄位的權限。 |
| `indices:admin/mappings/fields/get*` |  取得對應欄位的權限。 |
| `indices:admin/mappings/get` |  [取得對應]({{site.url}}{{site.baseurl}}/security-analytics/api-tools/mappings-api/#get-mappings)的權限。  |
| `indices:admin/open` |  [開啟索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/open-index/)的權限。 |
| `indices:admin/plugins/replication/index/setup/validate` |  驗證與[遠端叢集]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/getting-started/#set-up-a-cross-cluster-connection)之連線的權限。 |
| `indices:admin/plugins/replication/index/start` |  [啟動跨叢集複寫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/getting-started/#start-replication)的權限。 |
| `indices:admin/plugins/replication/index/pause` |  暫停跨叢集複寫的權限。 |
| `indices:admin/plugins/replication/index/resume` |  繼續跨叢集複寫的權限。 |
| `indices:admin/plugins/replication/index/stop` |  停止跨叢集複寫的權限。 |
| `indices:admin/plugins/replication/index/update` |  更新跨叢集複寫設定的權限。 |
| `indices:admin/plugins/replication/index/status_check` |  檢查跨叢集複寫狀態的權限。 |
| `indices:admin/refresh` |  使用 [Refresh Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/refresh/) 的權限。 |
| `indices:admin/refresh*` |  使用索引重新整理 API 的權限。 |
| `indices:admin/resolve/index` |  解析索引名稱、索引別名和資料串流的權限。 |
| `indices:admin/rollover` |  執行[索引輪替]({{site.url}}{{site.baseurl}}/api-reference/index-apis/rollover/)的權限。 |
| `indices:admin/seq_no/global_checkpoint_sync` | 執行全域檢查點同步的權限。 |
| `indices:admin/settings/update` |  [更新索引設定]({{site.url}}{{site.baseurl}}/api-reference/index-apis/update-settings/)的權限。 |
| `indices:admin/shards/search_shards` |  執行[跨叢集搜尋]({{site.url}}{{site.baseurl}}/security/access-control/cross-cluster-search/)的權限。 |
| `indices:admin/upgrade` | 供管理員執行升級的權限。 |
| `indices:admin/validate/query` |  驗證特定查詢的權限。 |
| `indices:data/read/explain` |  執行 [Explain API]({{site.url}}{{site.baseurl}}/api-reference/explain/) 的權限。 |
| `indices:data/read/field_caps` |  執行 [Field Capabilities API]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/alias/#using-aliases-in-field-capabilities-api-operations) 的權限。 |
| `indices:data/read/field_caps*` |  執行 Field Capabilities API 的權限。 |
| `indices:data/read/get` |  讀取索引資料的權限。 |
| `indices:data/read/mget` |  在單一請求中執行[多個 GET 作業]({{site.url}}{{site.baseurl}}/api-reference/document-apis/multi-get/)的權限。 |
| `indices:data/read/mget*` |  在單一請求中執行多個 GET 作業的權限。此設定必須同時設定為叢集層級和索引層級權限。 |
| `indices:data/read/msearch` |  在單一請求中執行[多個搜尋]({{site.url}}{{site.baseurl}}/api-reference/multi-search/)請求的權限。此設定必須同時設定為叢集層級和索引層級權限。 |
| `indices:data/read/msearch/template` |  將[多個搜尋範本]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/index/#multiple-search-templates)組合在一起，並以單一請求傳送至您的 OpenSearch 叢集的權限。此設定必須同時設定為叢集層級和索引層級權限。 |
| `indices:data/read/mtv` |  以單一請求擷取多個詞彙向量 (term vector) 的權限。此設定必須同時設定為叢集層級和索引層級權限。 |
| `indices:data/read/mtv*` |  以單一請求擷取多個詞彙向量 (term vector) 的權限。此設定必須同時設定為叢集層級和索引層級權限。 |
| `indices:data/read/plugins/replication/file_chunk` | 在分段複寫期間檢查檔案的權限。 |
| `indices:data/read/plugins/replication/changes` | 變更分段複寫設定的權限。 |
| `indices:data/read/scroll` |  捲動瀏覽資料的權限。此設定必須同時設定為叢集層級和索引層級權限。 |
| `indices:data/read/scroll/clear` | 清除 scroll 物件的權限。此設定必須同時設定為叢集層級和索引層級權限。 |
| `indices:data/read/search` |  [搜尋]({{site.url}}{{site.baseurl}}/api-reference/search/)資料的權限。 |
| `indices:data/read/search*` |  搜尋資料的權限。 |
| `indices:data/read/search/template` |  讀取搜尋範本的權限。 |
| `indices:data/read/tv` |  擷取特定文件欄位中詞彙之資訊與統計資料的權限。 |
| `indices:data/write/delete` |  [刪除文件]({{site.url}}{{site.baseurl}}/api-reference/document-apis/delete-document/)的權限。 |
| `indices:data/write/delete/byquery` |  刪除所有[符合查詢]({{site.url}}{{site.baseurl}}/api-reference/document-apis/delete-by-query/)之文件的權限。 |
| `indices:data/write/plugins/replication/changes` |  變更索引內資料複寫組態與設定的權限。 |
| `indices:data/write/bulk` |  執行 [bulk]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 請求的權限。此設定必須同時設定為叢集層級和索引層級權限。 |
| `indices:data/write/bulk*` |  執行 bulk 請求的權限。此設定必須同時設定為叢集層級和索引層級權限。 |
| `indices:data/write/index` |  將文件新增至現有索引的權限。另請參閱[將文件編製索引]( {{site.url}}{{site.baseurl}}/api-reference/document-apis/index-document/ )。 |
| `indices:data/write/update` | 更新索引的權限。 |
| `indices:data/write/update/byquery` |  執行指令碼以更新所有[符合查詢]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-by-query/)之文件的權限。 |
| `indices:monitor/data_stream/stats` | 串流統計資料的權限。  |
| `indices:monitor/recovery` | 存取復原統計資料的權限。 |
| `indices:monitor/segments` |  存取分段統計資料的權限。 |
| `indices:monitor/settings/get` | 取得監視器設定的權限。  |
| `indices:monitor/shard_stores` |  存取分片儲存區統計資料的權限。 |
| `indices:monitor/stats` | 存取監控統計資料的權限。  |
| `indices:monitor/upgrade` | 存取升級統計資料的權限。  |

## 安全性 REST 權限

允許存取這些端點可能會觸發叢集中的營運變更。請謹慎操作。
{: .warning }

下列 REST API 權限控制對端點的存取。授予任何這些 API 的存取權，即允許使用者變更安全性外掛程式的基本營運元件：

- `restapi:admin/actiongroups`
- `restapi:admin/allowlist`
- `restapi:admin/internalusers`
- `restapi:admin/nodesdn`
- `restapi:admin/roles`
- `restapi:admin/rolesmapping`
- `restapi:admin/ssl/certs/info`
- `restapi:admin/ssl/certs/reload`
- `restapi:admin/tenants`
