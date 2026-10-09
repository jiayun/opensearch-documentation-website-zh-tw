---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "稽核記錄"
nav_order: 125
has_children: true
has_toc: false
redirect_from:
  - /security-plugin/audit-logs/index/
  - /security/audit-logs/
---

# 稽核記錄

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

稽核記錄可讓您追蹤對 OpenSearch 叢集的存取，對於法規遵循目的或安全性事件發生後的調查很有用。您可以設定要記錄的類別、記錄訊息的詳細程度，以及記錄的儲存位置。

OpenSearch 支援兩種稽核記錄模式。下表說明各模式及其設定方式。

模式 | 需求 | 組態
:--- | :--- | :---
Standard (預設) | 已啟用精細存取控制 (FGAC) 的 Security 外掛程式。 | 安全性索引中的 `audit.yml` 檔案與 REST API。
Standalone | 無 FGAC。以僅 SSL 模式 (`plugins.security.ssl_only: true`) 執行，或停用安全性 (`plugins.security.disabled: true`)。 | `opensearch.yml` 與動態叢集設定。

如需 standalone 模式的詳細資訊，請參閱 [Standalone 稽核記錄]({{site.url}}{{site.baseurl}}/security/audit-logs/standalone/)。

## 啟用稽核記錄 (standard 模式)

稽核記錄預設為停用。若要啟用稽核記錄：

1. 在每個節點的 `opensearch.yml` 中新增下列這一行：

   ```yml
   plugins.security.audit.type: internal_opensearch
   ```
   {% include copy.html %}

   此設定會將稽核記錄儲存在目前的叢集。如需其他儲存選項，請參閱 [稽核記錄儲存類型]({{site.url}}{{site.baseurl}}/security/audit-logs/storage-types/)。

2. 重新啟動每個節點。

稽核記錄需要兩項設定：`opensearch.yml` 中的儲存類型 (`plugins.security.audit.type`)，以及 `audit.yml` 中的 `config.enabled: true`。Security 外掛程式提供的 `audit.yml` 檔案預設會將 `config.enabled` 設為 `true`，因此在新叢集中稽核記錄可能看起來已啟用。在您指定儲存類型之前，Security 外掛程式無法為稽核記錄建立儲存端點，因此不會記錄任何事件，並在啟動時記錄一則警告，指出沒有可用的預設儲存空間。
{: .note}

完成此初始設定後，您可以使用 OpenSearch Dashboards 管理稽核記錄類別與其他設定。在 OpenSearch Dashboards 中，選取 **Security**，然後選取 **Audit logs**。或者，您可以在 `audit.yml` 與 `opensearch.yml` 檔案中指定稽核記錄的設定 (使用哪個檔案取決於設定---請參閱 [稽核記錄設定](#audit-log-settings))。您也可以使用 [稽核記錄 API]({{site.url}}{{site.baseurl}}/security/api/audit/) 來管理及更新設定。


## 追蹤的事件

稽核記錄會以兩種方式記錄事件：HTTP 請求 (REST) 與傳輸層。下表提供追蹤事件的說明，以及這些事件是否記錄於 REST 或傳輸層。

事件 | 記錄於 REST | 記錄於傳輸 | 說明
:--- | :--- | :--- | :---
`FAILED_LOGIN` | 是 | 是 | 無法驗證請求的認證資訊，最可能是因為使用者不存在或密碼不正確。
`AUTHENTICATED` | 是 | 是 | 使用者已成功通過驗證。
`MISSING_PRIVILEGES` | 否 | 是 | 使用者沒有提出請求所需的權限。
`GRANTED_PRIVILEGES` | 否 | 是 | 使用者成功向 OpenSearch 提出請求。
`SSL_EXCEPTION` | 是 | 是 | 有人嘗試在沒有有效 SSL/TLS 憑證的情況下存取 OpenSearch。
`opensearch_SECURITY_INDEX_ATTEMPT` | 否 | 是 | 有人嘗試在沒有必要權限或 TLS 管理員憑證的情況下，修改 Security 外掛程式的內部使用者與權限索引。
`BAD_HEADERS` | 是 | 是 | 有人嘗試使用 Security 外掛程式的內部標頭，假冒對 OpenSearch 的請求。
`CLUSTER_SETTINGS_CHANGED` | 否 | 是 | 永久性或暫時性叢集設定已變更。預設為停用。
`INDEX_SETTINGS_CHANGED` | 否 | 是 | 索引設定已變更。預設為停用。
`REQUEST_AUDIT` | 是 | 是 | 已接收並處理 REST 請求。僅在 [standalone 稽核記錄]({{site.url}}{{site.baseurl}}/security/audit-logs/standalone/) 模式中產生。如需抑制此事件的詳細資訊，請參閱 [抑制 `REQUEST_AUDIT` 事件](#request-audit-suppression)。
`TRANSPORT_AUDIT` | 否 | 是 | 節點上已接收到傳輸層請求。僅在 [standalone 稽核記錄]({{site.url}}{{site.baseurl}}/security/audit-logs/standalone/) 模式中產生。
`RESOURCE_ACCESS_GRANTED` | 否 | 是 | 已授予對共用資源的存取權。預設為停用。
`RESOURCE_ACCESS_DENIED` | 否 | 是 | 已拒絕對共用資源的存取權。預設為停用。
`RESOURCE_SHARING_CHANGED` | 否 | 是 | 資源共用組態已變更。預設為停用。

<p id="request-audit-suppression"></p>

`REQUEST_AUDIT` 源自 REST 請求 (`audit_request_origin: REST`)，但事件本身是以 `audit_request_layer: TRANSPORT` 記錄。因此，它可以由 `disabled_categories`、`disabled_transport_categories` 或 `disabled_rest_categories` 任一個抑制---將 `REQUEST_AUDIT` 新增至其中任一設定即可抑制該事件。
{: .note}

## 稽核記錄設定

下列預設記錄設定適用於大多數使用案例。不過，您可以變更設定以節省儲存空間，或調整資訊以完全符合您的需求。 


### audit.yml 中的設定

下列設定儲存在 `audit.yml` 檔案中。


#### 排除類別

若要排除類別，請將它們列在下列設定中：

```yml
config:
  audit:
    disabled_rest_categories: <disabled categories>
    disabled_transport_categories: <disabled categories>
```
{% include copy.html %}

例如：

```yml
config:
  audit:
    disabled_rest_categories:
      - AUTHENTICATED
      - GRANTED_PRIVILEGES
    disabled_transport_categories: [ GRANTED_PRIVILEGES ]
```
{% include copy.html %}

或者，您可以使用統一的 `disabled_categories` 設定，同時停用兩層上的類別：

```yml
config:
  audit:
    disabled_categories:
      - AUTHENTICATED
      - GRANTED_PRIVILEGES
```
{% include copy.html %}

當 `disabled_categories` 與 `disabled_rest_categories` 或 `disabled_transport_categories` 一起設定時，若某個類別出現在統一設定或該層專屬設定中，則該類別會在該層上停用。

當 `disabled_categories` 與各層專屬設定一起設定時，會記錄一則棄用警告，鼓勵您僅遷移至 `disabled_categories`。

例如，下列組態會停用兩層上的 `AUTHENTICATED` (使用 `disabled_categories`)，並僅停用 REST 層上的 `SSL_EXCEPTION`：

```yml
config:
  audit:
    disabled_categories:
      - AUTHENTICATED
    disabled_rest_categories:
      - SSL_EXCEPTION
```
{% include copy.html %}

根據預設，`CLUSTER_SETTINGS_CHANGED` 與 `INDEX_SETTINGS_CHANGED` 類別在傳輸層上為停用。若要啟用它們，請將它們從 `disabled_transport_categories` 中移除：

```yml
config:
  audit:
    disabled_transport_categories:
      - AUTHENTICATED
      - GRANTED_PRIVILEGES
```
{% include copy.html %}

如果您想要記錄所有類別的事件，請使用 `NONE`：

```yml
config:
  audit:
    disabled_rest_categories: NONE
    disabled_transport_categories: NONE
```
{% include copy.html %}


#### 停用 REST 或傳輸層

根據預設，安全性外掛程式會同時記錄 REST 與傳輸層的事件。您可以停用任一類型：

```yml
config:
  audit:
    enable_rest: false
    enable_transport: false
```
{% include copy.html %}

#### 停用請求本文記錄

根據預設，安全性外掛程式會包含 REST 與傳輸層的請求本文 (若有的話)。如果您不想或不需要請求本文，可以停用它：

```yml
config:
  audit:
    log_request_body: false
```
{% include copy.html %}

#### 記錄索引名稱

根據預設，安全性外掛程式會記錄請求所影響的所有索引。由於索引名稱可能是別名，且包含萬用字元/日期模式，安全性外掛程式會記錄使用者提交的索引名稱*以及*其解析後的實際索引名稱。

例如，如果您使用別名或萬用字元，稽核事件可能如下所示：

```json
audit_trace_indices: [
  "human*"
],
audit_trace_resolved_indices: [
  "humanresources"
]
```
{% include copy.html %}

您可以透過下列設定停用此功能：

```yml
config:
  audit:
    resolve_indices: false
```
{% include copy.html %}

只有在 `config.audit.log_request_body` 也設為 `false` 時，才會停用此功能。
{: .note }


#### 設定大量請求處理

大量請求可能包含許多編製索引作業。根據預設，安全性外掛程式只會記錄單一的大量請求，而非每個個別作業。

安全性外掛程式可設定為將每個編製索引作業記錄為個別事件：

```yml
config:
  audit:
    resolve_bulk_requests: true
```
{% include copy.html %}

這項變更可能會在稽核記錄中產生極大量的記錄檔事件，因此如果您經常使用 `_bulk` API，我們不建議啟用此設定。


#### 排除請求

若要從記錄中排除特定請求，請為傳輸請求、HTTP 請求路徑 (REST) 或兩者設定動作：

```yml
config:
  audit:
    ignore_requests: ["indices:data/read/*", "SearchRequest"]
```
{% include copy.html %}

#### 排除使用者

根據預設，安全性外掛程式會記錄所有使用者的事件，但會排除內部 OpenSearch Dashboards 伺服器使用者 `kibanaserver`。您可以排除其他使用者：

```yml
config:
  audit:
    ignore_users:
      - kibanaserver
      - admin
```
{% include copy.html %}

如果應記錄所有使用者的請求，請使用 `NONE`：

```yml
config:
  audit:
    ignore_users: NONE
```
{% include copy.html %}


#### 排除標頭

您可以排除敏感標頭，使其不包含在記錄中---例如 `Authorization:` 標頭：

```yml
config:
  audit:
    exclude_sensitive_headers: true
```
{% include copy.html %}


### opensearch.yml 中的設定

下列設定儲存在 `opensearch.yml` 檔案中。這些設定在執行階段套用的方式取決於稽核記錄模式：

- 在獨立模式 (僅 SSL 或已停用安全性) 下，大多數稽核篩選與合規設定可在執行階段使用 [Cluster Settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) 變更，無須重新啟動節點。這些設定包括 `log_request_body`、`resolve_indices`、`disabled_categories`、`enable_rest`、`enable_transport`、`ignore_users` 及 `ignore_requests`。

- 在搭配 FGAC 的標準模式下，稽核組態儲存在 `audit.yml` 中，而對應的 `plugins.security.audit.config.*` 與 `plugins.security.audit.compliance.*` 叢集設定不會更新它。`PUT _cluster/settings` 請求可能會成功，但不會變更稽核組態。`body_logging_exclusions` 設定是例外：在 FGAC 模式下，您可以使用 Cluster Settings API 更新它。

部分稽核設定是靜態的，需要重新啟動節點：`action_groups.<NAME>`、`log4j.enable_mdc_routing`、`config.index`、執行緒集區設定，以及接收端連線設定。

啟用 FGAC 時，更新動態稽核設定需要 `plugins.security.restapi.roles_enabled` 中列出的角色。在僅 SSL 或已停用安全性的模式下，不會強制執行此限制。`body_logging_exclusions` 設定無須提高權限的角色即可更新。

下表說明呼叫者在各模式下可使用 `GET _cluster/settings` 讀取的稽核設定。

模式 | 設定回應中可見的稽核設定
:--- | :---
獨立、僅 SSL | 任何呼叫者都可以讀取非機密的動態稽核組態 (`plugins.security.audit.config.*` 與 `plugins.security.audit.compliance.*`)。含有憑證的接收端設定仍會隱藏。
獨立、已停用安全性 | 不會篩選任何 `plugins.security.audit.*` 設定，因此接收端憑證與 PEM 內容可能會顯示。
FGAC | 對所有呼叫者都會篩選整個 `plugins.security.audit.*` 子樹。此篩選並非以角色為基礎。

`plugins.security.audit.enabled` 執行階段切換僅適用於獨立稽核記錄。如需操作說明，請參閱[獨立稽核記錄]({{site.url}}{{site.baseurl}}/security/audit-logs/standalone/)。
{: .note}

#### 排除類別

您可以使用 `plugins.security.audit.config` 前置詞，在 `opensearch.yml` 中設定已停用的類別。這對於非 FGAC 模式 (僅 SSL 或已停用安全性) 很有用，因為在這些模式下無法使用 `audit.yml` 安全性索引：

```yml
plugins.security.audit.config.disabled_categories:
  - AUTHENTICATED
  - GRANTED_PRIVILEGES
```
{% include copy.html %}

各層專屬設定 `disabled_rest_categories` 與 `disabled_transport_categories` 已棄用。請改用統一的 `disabled_categories` 設定。
{: .warning}

各層專屬設定也可使用：

```yml
plugins.security.audit.config.disabled_rest_categories:
  - AUTHENTICATED
  - GRANTED_PRIVILEGES
plugins.security.audit.config.disabled_transport_categories:
  - AUTHENTICATED
  - GRANTED_PRIVILEGES
```
{% include copy.html %}

當同時設定 `disabled_categories` 與各層專屬設定時，若某類別出現在任一設定中，即會在指定層上停用該類別。此外也會記錄棄用警告，建議您只使用 `disabled_categories`。

`disabled_categories` 設定只會抑制 REST 與傳輸類別。它們不會影響 `COMPLIANCE_*` 類別，因為這些類別僅由合規設定 (`compliance.enabled`、受監看的索引與欄位，以及合規忽略使用者設定) 控管。
{: .note}

#### 請求本文記錄排除項目

使用 `body_logging_exclusions` 可針對特定動作或 REST 路徑抑制請求本文，同時繼續記錄所有其他請求的本文。`log_request_body` 設定會套用至每個請求，因此無法選擇性地排除大量作業，例如大量匯入。

所有展開的動作群組模式與原始排除模式會形成單一合併的萬用字元比對器。對於每個稽核層，此比對器會針對下表所述的對應識別碼進行測試。找到相符項目時，稽核事件會省略請求本文欄位。所有其他欄位 (例如使用者、IP 位址、索引及時間戳記) 都會保留。

識別碼 | 說明 | 比對對象
:--- | :--- | :---
傳輸動作 | 內部動作名稱 (例如 `indices:data/write/bulk[s][p]`)。 | 傳輸層稽核事件。
REST 路徑 | HTTP 請求路徑 (例如 `/_bulk`)。REST 路徑一律以 `/` 開頭。 | REST 層稽核事件。

兩個識別碼都支援使用 `*` 的萬用字元模式 (例如 `indices:data/write/bulk*` 會比對 `indices:data/write/bulk[s][p]`)。

##### 設定動作群組

動作群組是具名的動作模式、REST 路徑或兩者的集合，以靜態方式定義於 `opensearch.yml` 中。群組名稱由您自行選擇，因此可使用任何對您的作業有意義的名稱：

```yml
plugins.security.audit.config.action_groups.BULK: "indices:data/write/bulk*,/_bulk"
plugins.security.audit.config.action_groups.SEARCH: "indices:data/read/search*,/_search"
plugins.security.audit.config.action_groups.INDEX_ADMIN: "indices:admin/*"
```
{% include copy.html %}

每個動作群組會將一個名稱對應到以逗號分隔的常值或萬用字元模式清單，例如 `indices:data/write/bulk*`、`/_bulk` 或 `indices:data/write/*`。所有模式都使用相同的比對器；`:`、`/` 和 `*` 等字元並不會將模式指派給特定的稽核層。

動作群組是靜態設定，變更時需要重新啟動節點。群組名稱本身會區分大小寫。

##### 設定本文記錄排除項目

`body_logging_exclusions` 設定會參照動作群組名稱或原始模式。若要設定初始的排除項目，請在 `opensearch.yml` 中設定此設定：

```yml
plugins.security.audit.config.body_logging_exclusions:
  - BULK
```
{% include copy.html %}

此設定為動態設定，因此您也可以在執行階段更新排除項目，而無需重新啟動叢集：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.security.audit.config.body_logging_exclusions": ["BULK", "SEARCH"]
  }
}
```
{% include copy.html %}

清單中的每個項目會依下列方式處理：

1. 如果項目符合已定義的動作群組名稱，則會展開該群組的模式。
2. 如果項目不符合任何群組名稱，則該項目會被視為原始模式（常值或萬用字元）。

對於不符合已定義群組名稱的項目，如果該項目不包含 `:`、不以 `/` 開頭，且不包含 `*`，系統會記錄一則警告，因為該項目不太可能符合任何動作或 REST 路徑。請注意，此檢查只會尋找開頭的 `/`，而不是項目中任何位置的 `/`：例如 `_bulk/items` 這樣的項目雖然包含 `/`，但並非以其開頭，因此仍會為其記錄警告。此檢查僅用於決定是否記錄警告；該項目仍會包含在合併後的比對器中。

##### 大量請求

設定 `resolve_bulk_requests: true`（記錄個別的大量子項目）時，排除檢查會使用上層大量動作字串。因此，排除 `BULK` 群組會隱藏該大量請求中每個子項目（index、update 和 delete）的本文。您無法在同一個大量請求中保留 index 項目的本文，同時捨棄 delete 項目的本文。

##### 與 `log_request_body` 的互動

本文記錄排除項目僅在 `log_request_body` 為 `true` 時適用。如果 `log_request_body` 為 `false`，則無論排除組態為何，都不會記錄任何本文。

##### 組態範例

下列組態定義了三個動作群組，並排除大量請求的請求本文：

```yml
# opensearch.yml

# Define action groups (static, requires restart)
plugins.security.audit.config.action_groups.BULK: "indices:data/write/bulk*,/_bulk"
plugins.security.audit.config.action_groups.SEARCH: "indices:data/read/search*,/_search"
plugins.security.audit.config.action_groups.MONITORING: "cluster:monitor/*,indices:monitor/*"

# Initial exclusions (can be updated at runtime using _cluster/settings)
plugins.security.audit.config.body_logging_exclusions:
  - BULK
```
{% include copy.html %}

下表說明使用此組態時，各種請求類型是否會記錄請求本文。

請求類型 | 是否記錄請求本文
:--- | :---
大量寫入 | 否，因為已排除 `BULK` 群組。
搜尋 | 是。
建立索引 | 是。
監控 | 是，除非您將 `MONITORING` 加入排除項目。

若要在執行階段新增搜尋排除項目，請傳送下列請求：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.security.audit.config.body_logging_exclusions": ["BULK", "SEARCH"]
  }
}
```
{% include copy.html %}

若要清除所有排除項目（恢復記錄所有本文）：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.security.audit.config.body_logging_exclusions": []
  }
}
```
{% include copy.html %}

#### Log4j MDC 路由

使用 `log4j` 稽核接收端時，請啟用對應診斷內容（Mapped Diagnostic Context，MDC）路由，讓 Log4j 根據事件屬性將稽核事件路由至不同的 appender：

```yml
plugins.security.audit.config.log4j.enable_mdc_routing: true
```
{% include copy.html %}

啟用後，每個稽核事件都會設定下列 MDC 鍵：

- `audit_category` --- 稽核事件類別（例如 `REQUEST_AUDIT` 或 `GRANTED_PRIVILEGES`）
- `audit_action` --- 動作名稱
- `audit_user` --- 有效使用者
- `audit_request_type` --- 請求類型

請在 `log4j2.properties` 中使用 Log4j 路由 appender，依類別、使用者或任何其他 MDC 鍵分割稽核記錄檔。

這是靜態設定，需要重新啟動節點。
{: .note}


#### 設定稽核記錄檔索引名稱

根據預設，Security 外掛程式會將稽核事件儲存在名為 `security-auditlog-YYYY.MM.dd` 的每日輪替索引中：

```yml
plugins.security.audit.config.index: myauditlogindex
```
{% include copy.html %}

在索引名稱中使用日期模式，即可設定每日、每週或每月輪替的索引：

```yml
plugins.security.audit.config.index: "'auditlog-'YYYY.MM.dd"
```
{% include copy.html %}

如需日期模式格式的參考資料，請參閱 [Joda DateTimeFormat 文件](https://www.joda.org/joda-time/apidocs/org/joda/time/format/DateTimeFormat.html)。


#### （進階）調整執行緒集區

Search 外掛程式會以非同步方式記錄事件，將對叢集效能的影響降至最低。此外掛程式使用固定的執行緒集區來記錄事件：

```yml
plugins.security.audit.config.threadpool.size: <integer>
```
{% include copy.html %}

預設設定為 `10`。將此值設為 `0` 會停用執行緒集區，這表示外掛程式會以同步方式記錄事件。若要設定每個執行緒的最大佇列長度：

```yml
plugins.security.audit.config.threadpool.max_queue_len: 100000
```
{% include copy.html %}

## 停用稽核記錄檔

若要在啟用稽核記錄檔後將其停用，請從 `opensearch.yml` 中移除 `plugins.security.audit.type: internal_opensearch` 設定，或在 OpenSearch Dashboards 中取消勾選 **Enable audit logging** 核取方塊。使用 Cluster Settings API 設定的 `plugins.security.audit.enabled` 執行階段切換開關僅適用於獨立稽核記錄；相關說明請參閱[獨立稽核記錄]({{site.url}}{{site.baseurl}}/security/audit-logs/standalone/)。

## 稽核使用者帳戶操作

若要針對安全性索引的變更（例如角色對應的變更，以及角色的建立或刪除）啟用稽核記錄，請在稽核記錄檔組態的 `compliance:` 部分中使用下列設定，如下列範例所示：

```yaml
_meta:
  type: "audit"
  config_version: 2

config:
  # enable/disable audit logging
  enabled: true

  ...


  compliance:
    # enable/disable compliance
    enabled: true

    # Log updates to internal security changes
    internal_config: true

    # Log only metadata of the document for write events
    write_metadata_only: false

    # Log only diffs for document updates
    write_log_diffs: true

    # List of indices to watch for write events. Wildcard patterns are supported
    # write_watched_indices: ["twitter", "logs-*"]
    write_watched_indices: [".opendistro_security"]
```
{% include copy.html %}
