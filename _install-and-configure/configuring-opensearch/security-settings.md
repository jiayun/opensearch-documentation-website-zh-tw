---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安全性設定"
parent: Configuring OpenSearch
nav_order: 40
---

# 安全性設定

Security 外掛程式提供多個 YAML 組態檔案，用於儲存必要的設定，這些設定定義 Security 外掛程式如何管理叢集中的使用者、角色與活動。如需 Security 外掛程式組態檔案的完整清單，請參閱[修改 YAML 檔案]({{site.url}}{{site.baseurl}}/security/configuration/yaml/)。

以下各節說明 `opensearch.yml` 中與安全性相關的設定。您可以在 `<OPENSEARCH_HOME>/config/opensearch.yml` 中找到 `opensearch.yml`。若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 一般設定

Security 外掛程式支援下列一般設定：

-  `plugins.security.nodes_dn`（靜態）：指定一份辨別名稱 (DN) 清單，用以表示叢集中的其他節點。此設定支援萬用字元與規則運算式。當 `plugins.security.nodes_dn_dynamic_config_enabled` 為 `true` 時，除了 YAML 組態之外，**還會**從安全性索引讀取 DN 清單。若此設定未正確設定，叢集將無法形成，因為節點之間無法互相信任，並會產生下列錯誤：`Transport client authentication no longer supported`。

- `plugins.security.nodes_dn_dynamic_config_enabled`（靜態）：適用於 `cross_cluster` 使用案例，即需要管理允許清單中的 `nodes_dn`，而不必在每次設定新的 `cross_cluster` 遠端時重新啟動節點。
  將 `nodes_dn_dynamic_config_enabled` 設定為 `true` 會啟用**可由超級管理員呼叫**的 Distinguished Names API，這些 API 提供動態更新或擷取 `nodes_dn` 的方法。此設定僅在未設定 `plugins.security.cert.intercluster_request_evaluator_class` 時才會生效。預設為 `false`。

- `plugins.security.authcz.admin_dn`（靜態）：定義應獲指派管理員權限的憑證 DN。必要。

- `plugins.security.roles_mapping_resolution`（靜態）：定義後端角色如何對應至 Security 角色。支援下列值：
    - `MAPPING_ONLY`（預設）：必須在 `roles_mapping.yml` 中明確設定對應。
    - `BACKENDROLES_ONLY`：後端角色會直接對應至安全性角色。`roles_mapping.yml` 中的設定不會生效。
    - `BOTH`：後端角色會同時直接對應以及透過 `roles_mapping.yml` 對應至安全性角色。

- `plugins.security.dls.mode`（靜態）：設定文件層級安全性 (DLS) 的評估模式。預設為 `adaptive`。請參閱[如何設定 DLS 評估模式]({{site.url}}{{site.baseurl}}/security/access-control/document-level-security/#how-to-set-the-dls-evaluation-mode-in-opensearchyml)。

- `plugins.security.compliance.salt`（靜態）：為欄位遮罩產生雜湊值時使用的 salt。長度至少須為 32 個字元。僅允許 ASCII 字元。選用。

- `plugins.security.compliance.immutable_indices`（靜態）：標記為不可變更的索引中的文件遵循「一次寫入、多次讀取」模式。在這些索引中建立的文件無法變更，因此是不可變更的。

- `config.dynamic.http.anonymous_auth_enabled`（靜態）：啟用匿名驗證。這會使所有 HTTP 驗證器都不發出驗證挑戰。預設為 `false`。

- `http.detailed_errors.enabled`（靜態）：為針對 OpenSearch 叢集執行的 REST 呼叫啟用詳細錯誤訊息。若設定為 `true`，會連同錯誤程式碼一併提供 `root_cause`。預設為 `true`。

## REST 管理 API 設定

Security 外掛程式支援下列 REST 管理 API 設定：

- `plugins.security.restapi.roles_enabled`（靜態）：為列出的角色啟用以角色為基礎的 REST 管理 API 存取權。角色之間以逗號分隔。預設為空白清單（不允許任何角色存取 REST 管理 API）。請參閱[API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。

- `plugins.security.restapi.endpoints_disabled.<role>.<endpoint>`（靜態）：針對角色停用特定端點及其 HTTP 方法。此設定的值由 HTTP 方法陣列組成。例如：`plugins.security.restapi.endpoints_disabled.all_access.ACTIONGROUPS: ["PUT","POST","DELETE"]`。預設會允許所有端點與方法。若要為每個角色停用某個端點，請使用 `global` 取代角色名稱。如需有效的 `<endpoint>` 值，請參閱[端點值]({{site.url}}{{site.baseurl}}/security/access-control/api/#endpoint-values)。

- `plugins.security.restapi.admin.enabled`（靜態）：啟用 `restapi:admin/*` 叢集權限，這些權限會授予角色存取允許清單、辨別名稱與憑證 API 的權限。當此設定為 `false` 時，這些權限不會生效，且只有使用管理員憑證才能存取這些 API。預設為 `false`。請參閱 [REST API 管理員權限]({{site.url}}{{site.baseurl}}/security/access-control/api/#rest-api-admin-permissions)。

- `plugins.security.restapi.max_string_length`（靜態）：設定 Security REST API 請求本文中任何單一字串值允許的最大字元數。有效值介於 `1` 與 `50000000` 之間（含）。預設為 `4096`。若您透過 REST API 提交大型自由格式值，例如文件層級安全性 (DLS) 查詢，請增加此值。

- `plugins.security.restapi.password_validation_regex`（靜態）：指定規則運算式，用以設定登入密碼的條件。如需詳細資訊，請參閱[密碼設定]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#password-settings)。

- `plugins.security.restapi.password_validation_error_message`（靜態）：指定密碼未通過驗證時載入的錯誤訊息。此設定需與 `plugins.security.restapi.password_validation_regex` 搭配使用。

- `plugins.security.restapi.password_min_length`（靜態）：設定使用以分數為基礎的密碼強度估算器時，密碼長度的最小字元數。預設為 8，這也是最小值。如需詳細資訊，請參閱[密碼設定]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#password-settings)。

- `plugins.security.restapi.password_score_based_validation_strength`（靜態）：設定用於判斷密碼強弱的門檻。有效值為 `fair`、`good`、`strong` 與 `very_strong`。此設定需與 `plugins.security.restapi.password_min_length` 搭配使用。

- `plugins.security.unsupported.restapi.allow_securityconfig_modification`（靜態）：允許對組態 API 使用 PUT 與 PATCH 方法。

## 進階設定

安全性外掛程式支援下列進階設定：

- `plugins.security.authcz.impersonation_dn`（靜態）：啟用傳輸層身分冒用。這可讓 DN 以其他使用者的身分執行操作。請參閱[使用者身分冒用]({{site.url}}{{site.baseurl}}/security/access-control/impersonation/)。

- `plugins.security.authcz.rest_impersonation_user`（靜態）：啟用 REST 層身分冒用。這可讓使用者以其他使用者的身分執行操作。請參閱[使用者身分冒用]({{site.url}}{{site.baseurl}}/security/access-control/impersonation/)。

- `plugins.security.allow_default_init_securityindex`（靜態）：設定為 `true` 時，若組態索引不存在，OpenSearch Security 會自動使用 `/config` 目錄中的檔案初始化組態索引。

  這會使用眾所周知的預設密碼。請僅在私人網路／環境中使用。
  {: .warning}

- `plugins.security.allow_unsafe_democertificates`（靜態）：設定為 `true` 時，OpenSearch 會使用示範憑證啟動。這些憑證僅供示範用途核發。

  這些憑證廣為人知，因此不適合用於生產環境。請僅在私人網路／環境中使用。
  {: .warning}

- `plugins.security.ccs.ignore_source_security_roles`（動態）：設定為 `true` 時，遠端叢集會忽略跨叢集搜尋請求中由協調叢集傳遞的安全性角色，並僅使用其本身的 `roles_mapping.yml` 組態來評估存取權。預設為 `false`。請參閱[遠端叢集角色評估]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/#remote-cluster-role-evaluation)。

- `plugins.security.system_indices.permission.enabled`（靜態）：啟用系統索引權限功能。設定為 `true` 時，此功能會啟用，且具有修改角色權限的使用者可以建立包含授予系統索引存取權之權限的角色。設定為 `false` 時，此權限會停用，只有持有管理員憑證的管理員才能變更系統索引。在新叢集中，此權限預設設定為 `false`。

## 專家級設定

專家級設定只應由完全了解該功能的管理員設定與部署。對功能的誤解可能導致安全性風險、使 Security 外掛程式無法正常運作，或造成資料遺失。
{: .warning}

Security 外掛程式支援下列專家級設定：

- `plugins.security.config_index_name`（靜態）：`.opendistro_security` 儲存其組態的索引名稱。

- `plugins.security.cert.oid`（靜態）：定義伺服器節點憑證的物件識別碼 (OID)。

- `plugins.security.cert.intercluster_request_evaluator_class`（靜態）：指定用於評估跨叢集請求的 `org.opensearch.security.transport.InterClusterRequestEvaluator` 實作。`org.opensearch.security.transport.InterClusterRequestEvaluator` 的執行個體必須實作一個接受 `org.opensearch.common.settings.Settings` 物件的單一引數建構函式。

- `plugins.security.enable_snapshot_restore_privilege`（靜態）：設為 `false` 時，此設定會停用一般使用者的快照還原功能。在此情況下，只會接受由管理員 TLS 憑證簽署的快照還原請求。設為 `true`（預設）時，一般使用者若具有 `cluster:admin/snapshot/restore`、`indices:admin/create` 和 `indices:data/write/index` 權限，即可還原快照。

  只有在快照不包含全域狀態，且不會還原 `.opendistro_security` 索引時，才能還原該快照。
  {: .note}

- `plugins.security.check_snapshot_restore_write_privileges`（靜態）：設為 `false` 時，會略過額外的索引檢查。設為預設值 `true` 時，會針對 `indices:admin/create` 和 `"indices:data/write/index` 評估還原快照的嘗試。

- `plugins.security.cache.ttl_minutes`（靜態）：決定驗證快取的逾時時間。驗證快取會暫時儲存從後端傳回的使用者物件，使 Security 外掛程式不需重複發出請求來取得這些物件，藉此加快驗證速度。請以分鐘為單位設定此值。預設為 `60`。將此值設為 `0` 即可停用快取。

- `plugins.security.disabled`（靜態）：停用 OpenSearch Security。

  停用此外掛程式可能會使您的組態（包括密碼）公開暴露。
  {:warning}

- `plugins.security.protected_indices.enabled`（靜態）：若設為 `true`，則啟用受保護的索引。受保護的索引比一般索引更安全。這些索引與其他傳統索引一樣需要角色才能存取，此外還需要另一個角色才能看見。此設定需搭配 `plugins.security.protected_indices.roles` 和 `plugins.security.protected_indices.indices` 設定使用。

- `plugins.security.protected_indices.roles`（靜態）：指定使用者必須對應到的角色清單，才能存取受保護的索引。

- `plugins.security.protected_indices.indices`（靜態）：指定要標記為受保護的索引清單。這些索引只對對應到 `plugins.security.protected_indices.roles` 中所指定角色的使用者可見。滿足此要求後，使用者仍需對應到用於授予該索引存取權限的傳統角色。

- `plugins.security.system_indices.enabled`（靜態）：若設為 `true`，則啟用系統索引。系統索引與安全性索引類似，差別在於其內容未經加密。設定為系統索引的索引，可由超級管理員或具有包含[系統索引權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/#system-index-permissions)之角色的使用者存取。如需系統索引的詳細資訊，請參閱[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)。

- `plugins.security.system_indices.indices`（靜態）：要作為系統索引使用的索引清單。此設定由 `plugins.security.system_indices.enabled` 設定控制。

- `plugins.security.allow_default_init_securityindex`（靜態）：設為 `true` 時，若 OpenSearch 啟動時建立安全性索引的嘗試失敗，會將 Security 外掛程式設為其預設安全性設定。預設安全性設定儲存在 `opensearch-project/security/config` 目錄中的 YAML 檔案內。預設為 `false`。

- `plugins.security.cert.intercluster_request_evaluator_class`（靜態）：用於評估跨叢集通訊的類別。

- `plugins.security.enable_snapshot_restore_privilege`（靜態）：啟用授予快照還原權限的功能。選用。預設為 `true`。

- `plugins.security.check_snapshot_restore_write_privileges`（靜態）：在建立快照時強制執行寫入權限評估。預設為 `true`。

若您變更下列任何密碼雜湊屬性，則必須重新雜湊所有內部密碼，以確保相容性與安全性。
{: .warning}

- `plugins.security.password.hashing.algorithm`：（靜態）：指定要使用的密碼雜湊演算法。支援下列值：  
  - `BCrypt`（預設）
  - `PBKDF2`（符合 FIPS 140-2 與 FIPS 140-3）
  - `Argon2`

- `plugins.security.password.hashing.bcrypt.rounds`（靜態）：指定使用 `BCrypt` 進行密碼雜湊時的回合數。有效值介於 `4` 與 `31` 之間（含）。預設為 `12`。

- `plugins.security.password.hashing.bcrypt.minor`（靜態）：指定用於密碼雜湊的 `BCrypt` 演算法次要版本。支援下列值：
  - `A`
  - `B`
  - `Y`（預設）

- `plugins.security.password.hashing.pbkdf2.function`（靜態）：指定套用至密碼的偽隨機函式。支援下列值：
  - `SHA1`
  - `SHA224`
  - `SHA256`（預設）
  - `SHA384`
  - `SHA512`

- `plugins.security.password.hashing.pbkdf2.iterations`（靜態）：指定將偽隨機函式套用至密碼的次數。預設為 `600,000`。

- `plugins.security.password.hashing.pbkdf2.length`（靜態）：指定最終衍生金鑰的所需長度。預設為 `256`。

- `plugins.security.password.hashing.argon2.iterations`：指定演算法對記憶體執行的處理次數。增加此值會提高 CPU 運算時間，並增強對暴力破解攻擊的抵抗力。預設：`3`。

- `plugins.security.password.hashing.argon2.memory`：指定雜湊期間使用的記憶體量（以 KiB 為單位）。預設：`65536` (64 MiB)。

- `plugins.security.password.hashing.argon2.parallelism`：指定用於運算的平行執行緒數。預設：`1`。

- `plugins.security.password.hashing.argon2.length`：指定產生之雜湊輸出的長度（以位元組為單位）。預設：`32`。

- `plugins.security.password.hashing.argon2.type`：指定要使用的 Argon2 變體。支援下列值：
  - `Argon2i`
  - `Argon2d`
  - `Argon2id`（預設）

- `plugins.security.password.hashing.argon2.version`：指定要使用的 Argon2 版本。支援下列值：
  - `16`
  - `19`（預設）



## 稽核記錄檔設定

Security 外掛程式支援下列稽核記錄檔設定：

- `plugins.security.audit.enable_rest`（動態）：啟用或停用 REST 請求記錄。預設為 `true`（啟用）。

- `plugins.security.audit.enable_transport`（動態）：啟用或停用傳輸層級的請求記錄。預設為 `false`（停用）。

- `plugins.security.audit.resolve_bulk_requests`（動態）：啟用或停用大量 (bulk) 請求記錄。啟用時，也會記錄大量請求中的每個個別請求。預設為 `false`（停用）。

- `plugins.security.audit.config.disabled_categories`（動態）：停用指定的事件類別。

- `plugins.security.audit.ignore_requests`（動態）：將指定的請求排除在記錄之外。允許使用包含動作或 REST 請求路徑的萬用字元和規則運算式。

- `plugins.security.audit.threadpool.size`（靜態）：決定用於記錄事件之執行緒集區中的執行緒數量。預設為 `10`。將此值設為 `0` 會停用執行緒集區，這表示外掛程式會以同步方式記錄事件。

- `plugins.security.audit.threadpool.max_queue_len`（靜態）：設定每個執行緒的最大佇列長度。預設為 `100000`。

- `plugins.security.audit.ignore_users`（動態）：使用者陣列。不會記錄清單中使用者的稽核請求。

- `plugins.security.audit.type`（靜態）：稽核記錄檔事件的目的地。有效值為 `internal_opensearch`、`external_opensearch`、`debug` 和 `webhook`。

- `plugins.security.audit.enable_standalone`（靜態）：為未使用細粒度存取控制（僅 SSL 或停用安全性模式）執行的叢集啟用獨立稽核記錄。請將此設定設為 `true`，並同時設定 `plugins.security.audit.type`，以啟用獨立稽核記錄。預設為 `false`。如需更多資訊，請參閱[獨立稽核記錄]({{site.url}}{{site.baseurl}}/security/audit-logs/standalone/)。

- `plugins.security.audit.config.body_logging_exclusions`（動態）：動作群組名稱或原始動作與路徑模式的清單，系統會針對這些項目略過請求本文記錄。預設為 `[]`，即記錄所有請求本文。如需更多資訊，請參閱[本文記錄排除項目]({{site.url}}{{site.baseurl}}/security/audit-logs/index/#body-logging-exclusions)。

- `plugins.security.audit.config.action_groups.<NAME>`（靜態）：定義具名的動作與路徑模式群組，以搭配 `body_logging_exclusions` 使用。每個群組都是以逗號分隔的字串，內容為傳輸動作模式、REST 路徑，或兩者皆有。支援萬用字元。

- `plugins.security.audit.config.log4j.enable_mdc_routing`（靜態）：為 Log4j 稽核接收端啟用對應診斷內容 (Mapped Diagnostic Context, MDC) 路由。啟用時，稽核事件會設定 `audit_category`、`audit_action`、`audit_user` 和 `audit_request_type` MDC 鍵，供 Log4j 路由附加器 (appender) 使用。預設為 `false`。

- `plugins.security.audit.config.http_endpoints`（靜態）：`localhost` 的端點清單。

- `plugins.security.audit.config.index`（靜態）：稽核記錄檔索引。預設為依日期輪替的模式 `"'security-auditlog-'YYYY.MM.dd"`，每天會產生一個新索引（例如 `security-auditlog-2023.06.15`）。您也可以改為指定固定的索引名稱。無論哪種情況，請務必妥善保護該索引。

- `plugins.security.audit.config.type`（靜態）：將稽核記錄檔類型指定為 `auditlog`。

- `plugins.security.audit.config.username`（靜態）：稽核記錄檔組態的使用者名稱。

- `plugins.security.audit.config.password`（靜態）：稽核記錄檔組態的密碼。

- `plugins.security.audit.config.enable_ssl`（靜態）：為稽核記錄啟用或停用 SSL。

- `plugins.security.audit.config.verify_hostnames`（靜態）：啟用或停用 SSL/TLS 憑證的主機名稱驗證。預設為 `true`（啟用）。

- `plugins.security.audit.config.enable_ssl_client_auth`（靜態）：啟用或停用 SSL/TLS 用戶端驗證。預設為 `false`（停用）。

- `plugins.security.audit.config.cert_alias`（靜態）：用於存取稽核記錄檔之憑證的別名。

- `plugins.security.audit.config.pemkey_filepath`（靜態）：用於稽核記錄之 Privacy Enhanced Mail (PEM) 金鑰的 `/config` 相對檔案路徑。

- `plugins.security.audit.config.pemkey_content`（靜態）：用於稽核記錄之 PEM 金鑰的 Base64 編碼內容。此為 `...config.pemkey_filepath` 的替代方案。

- `plugins.security.audit.config.pemkey_password`（靜態）：用戶端所使用之 PEM 格式私密金鑰的密碼。

- `plugins.security.audit.config.pemcert_filepath`（靜態）：用於稽核記錄之 PEM 憑證的 `/config` 相對檔案路徑。

- `plugins.security.audit.config.pemcert_content`（靜態）：用於稽核記錄之 PEM 憑證的 Base64 編碼內容。此為使用 `...config.pemcert_filepath` 指定檔案路徑的替代方案。

- `plugins.security.audit.config.pemtrustedcas_filepath`（靜態）：受信任根憑證授權單位的 `/config` 相對檔案路徑。

- `plugins.security.audit.config.pemtrustedcas_content`（靜態）：根憑證授權單位的 Base64 編碼內容。此為 `...config.pemtrustedcas_filepath` 的替代方案。

- `plugins.security.audit.config.webhook.url`（靜態）：Webhook URL。

- `plugins.security.audit.config.webhook.format`（靜態）：Webhook 所使用的格式。有效值為 `URL_PARAMETER_GET`、`URL_PARAMETER_POST`、`TEXT`、`JSON` 和 `SLACK`。

- `plugins.security.audit.config.webhook.ssl.verify`（靜態）：啟用或停用對隨任何 webhook 請求傳送之 SSL/TLS 憑證的驗證。預設為 `true`（啟用）。

- `plugins.security.audit.config.webhook.ssl.pemtrustedcas_filepath`（靜態）：用於驗證 webhook 請求之受信任憑證授權單位的 `/config` 相對檔案路徑。

- `plugins.security.audit.config.webhook.ssl.pemtrustedcas_content`（靜態）：用於驗證 webhook 請求之憑證授權單位的 Base64 編碼內容。此為 `...config.pemtrustedcas_filepath` 的替代方案。

- `plugins.security.audit.config.log4j.logger_name`（靜態）：Log4j 記錄器的自訂名稱。

- `plugins.security.audit.config.log4j.level`（靜態）：為 Log4j 記錄器提供預設記錄層級。有效值為 `OFF`、`FATAL`、`ERROR`、`WARN`、`INFO`、`DEBUG`、`TRACE` 和 `ALL`。預設為 `INFO`。

- `opendistro_security.audit.config.disabled_rest_categories`（動態）：記錄器要忽略的 REST 類別清單。有效值為 `AUTHENTICATED` 和 `GRANTED_PRIVILEGES`。

- `opendistro_security.audit.config.disabled_transport_categories`（動態）：記錄器要忽略的傳輸層類別清單。有效值為 `AUTHENTICATED` 和 `GRANTED_PRIVILEGES`。

啟用細粒度存取控制 (FGAC) 時，更新動態稽核篩選設定或任何 `plugins.security.audit.compliance.*` 設定的 `PUT _cluster/settings` 請求都會遭到拒絕，除非呼叫者具有 `plugins.security.restapi.roles_enabled` 中列出的角色。在僅 SSL 或停用安全性模式下，不會強制執行此限制。`plugins.security.audit.config.body_logging_exclusions` 和 `plugins.security.audit.config.action_groups.<NAME>` 設定為例外，不需要具備提升權限的角色。

下表說明在各模式下，呼叫者可使用 `GET _cluster/settings` 讀取的稽核設定。

模式 | 設定回應中可見的稽核設定
:--- | :---
僅 SSL | 任何呼叫者都可以讀取 `plugins.security.audit.config.*` 和 `plugins.security.audit.compliance.*` 下的非機密動態組態。含有認證資訊的接收端設定仍會保持隱藏。
停用安全性 | 不會篩選任何 `plugins.security.audit.*` 設定，因此接收端認證資訊和 PEM 內容可能會被看見。
FGAC | 整個 `plugins.security.audit.*` 子樹會針對所有呼叫者進行篩選。此篩選並非以角色為依據。

## 主機名稱驗證與 DNS 查詢設定

Security 外掛程式支援下列主機名稱驗證與 DNS 查詢設定：

- `transport.ssl.enforce_hostname_verification`（靜態）：是否在傳輸層驗證主機名稱。選用。預設為 `true`。

- `transport.ssl.resolve_hostname`（靜態）：是否在傳輸層透過 DNS 解析主機名稱。選用。預設為 `true`。僅在啟用主機名稱驗證時有效。

如需更多資訊，請參閱[主機名稱驗證與 DNS 查詢]({{site.url}}{{site.baseurl}}/security/configuration/tls/#advanced-hostname-verification-and-dns-lookup)。

## 用戶端驗證設定

Security 外掛程式支援下列用戶端驗證設定：

- `plugins.security.ssl.http.clientauth_mode`（靜態）：要使用的 TLS 用戶端驗證模式。有效值為 `OPTIONAL`（預設）、`REQUIRE` 和 `NONE`。選用。

如需更多資訊，請參閱[用戶端驗證]({{site.url}}{{site.baseurl}}/security/configuration/tls/#advanced-client-authentication)。

## 已啟用的加密套件與通訊協定設定

Security 外掛程式支援下列已啟用的加密套件與通訊協定設定。每個設定都必須以陣列表示：

- `plugins.security.ssl.http.enabled_ciphers`（靜態）：REST 層已啟用的 TLS 加密套件。僅支援 Java 格式。

- `plugins.security.ssl.http.enabled_protocols`（靜態）：REST 層已啟用的 TLS 通訊協定。僅支援 Java 格式。

- `plugins.security.ssl.transport.enabled_ciphers`（靜態）：傳輸層已啟用的 TLS 加密套件。僅支援 Java 格式。

- `plugins.security.ssl.transport.enabled_protocols`（靜態）：傳輸層已啟用的 TLS 通訊協定。僅支援 Java 格式。

如需更多資訊，請參閱[已啟用的加密套件與通訊協定]({{site.url}}{{site.baseurl}}/security/configuration/tls/#advanced-enabled-ciphers-and-protocols)。

## 金鑰儲存區與信任儲存區檔案---傳輸層 TLS 設定

Security 外掛程式支援下列傳輸層 TLS 金鑰儲存區與信任儲存區設定：

- `plugins.security.ssl.transport.keystore_type`（靜態）：金鑰儲存區檔案的類型。選用。有效值為 `JKS` 或 `PKCS12/PFX`。預設為 `JKS`。

- `plugins.security.ssl.transport.keystore_filepath`（靜態）：金鑰儲存區檔案的路徑，該檔案必須位於 `config` 目錄下，並以相對路徑指定。必要。

- `plugins.security.ssl.transport.keystore_alias`（靜態）：金鑰儲存區別名。選用。預設為第一個別名。

- `plugins.security.ssl.transport.keystore_password`（靜態）：金鑰儲存區密碼。預設為 `changeit`。

- `plugins.security.ssl.transport.truststore_type`（靜態）：信任儲存區檔案的類型。選用。有效值為 `JKS` 或 `PKCS12/PFX`。預設為 `JKS`。

- `plugins.security.ssl.transport.truststore_filepath`（靜態）：信任儲存區檔案的路徑，該檔案必須位於 `config` 目錄下，並以相對路徑指定。必要。

- `plugins.security.ssl.transport.truststore_alias`（靜態）：信任儲存區別名。選用。預設為所有憑證。

- `plugins.security.ssl.transport.truststore_password`（靜態）：信任儲存區密碼。預設為 `changeit`。

如需有關金鑰儲存區與信任儲存區檔案的更多資訊，請參閱[傳輸層 TLS]({{site.url}}{{site.baseurl}}/security/configuration/tls/#transport-layer-tls-1)。

## 金鑰儲存區與信任儲存區檔案---REST 層 TLS 設定

Security 外掛程式支援下列 REST 層 TLS 金鑰儲存區與信任儲存區設定：

- `plugins.security.ssl.http.enabled`（靜態）：是否在 REST 層啟用 TLS。若啟用，則僅允許 HTTPS。選用。預設為 `false`。

- `plugins.security.ssl.http.keystore_type`（靜態）：金鑰儲存區檔案的類型。選用。有效值為 `JKS` 或 `PKCS12/PFX`。預設為 `JKS`。

- `plugins.security.ssl.http.keystore_filepath`（靜態）：金鑰儲存區檔案的路徑，該檔案必須位於 `config` 目錄下，並以相對路徑指定。必要。

- `plugins.security.ssl.http.keystore_alias`（靜態）：金鑰儲存區別名。選用。預設為第一個別名。

- `plugins.security.ssl.http.keystore_password`：金鑰儲存區密碼。預設為 `changeit`。

- `plugins.security.ssl.http.truststore_type`：信任儲存區檔案的類型。選用。有效值為 `JKS` 或 `PKCS12/PFX`。預設為 `JKS`。

- `plugins.security.ssl.http.truststore_filepath`：信任儲存區檔案的路徑，該檔案必須位於 `config` 目錄下，並以相對路徑指定。必要。

- `plugins.security.ssl.http.truststore_alias`（靜態）：信任儲存區別名。選用。預設為所有憑證。

- `plugins.security.ssl.http.truststore_password`（靜態）：信任儲存區密碼。預設為 `changeit`。

如需更多資訊，請參閱[REST 層 TLS]({{site.url}}{{site.baseurl}}/security/configuration/tls/#rest-layer-tls-1)。

## X.509 PEM 憑證與 PKCS #8 金鑰---傳輸層 TLS 設定

Security 外掛程式支援下列與 X.509 PEM 憑證及 PKCS #8 金鑰相關的傳輸層 TLS 設定：

- `plugins.security.ssl.transport.pemkey_filepath`（靜態）：憑證金鑰檔案（PKCS #8）的路徑，該檔案必須位於 `config` 目錄下，並以相對路徑指定。必要。

- `plugins.security.ssl.transport.pemkey_password`（靜態）：金鑰密碼。若金鑰沒有密碼，請省略此設定。選用。

- `plugins.security.ssl.transport.pemcert_filepath`（靜態）：X.509 節點憑證鏈（PEM 格式）的路徑，該檔案必須位於 `config` 目錄下，並以相對路徑指定。必要。

- `plugins.security.ssl.transport.pemtrustedcas_filepath`（靜態）：根憑證授權單位（PEM 格式）的路徑，該檔案必須位於 `config` 目錄下，並以相對路徑指定。必要。

如需更多資訊，請參閱[REST 層 TLS]({{site.url}}{{site.baseurl}}/security/configuration/tls/#transport-layer-tls)。

## X.509 PEM 憑證與 PKCS #8 金鑰---REST 層 TLS 設定

Security 外掛程式支援下列與 X.509 PEM 憑證及 PKCS #8 金鑰相關的 REST 層 TLS 設定：

- `plugins.security.ssl.http.enabled`（靜態）：是否在 REST 層啟用 TLS。若啟用，則僅允許 HTTPS。選用。預設為 `false`。

- `plugins.security.ssl.http.pemkey_filepath`（靜態）：憑證金鑰檔案（PKCS #8）的路徑，該檔案必須位於 `config` 目錄下，並以相對路徑指定。必要。

- `plugins.security.ssl.http.pemkey_password`（靜態）：金鑰密碼。若金鑰沒有密碼，請省略此設定。選用。

- `plugins.security.ssl.http.pemcert_filepath`（靜態）：X.509 節點憑證鏈（PEM 格式）的路徑，該檔案必須位於 `config` 目錄下，並以相對路徑指定。必要。

-  `plugins.security.ssl.http.pemtrustedcas_filepath`：根憑證授權單位（PEM 格式）的路徑，該檔案必須位於 config 目錄下，並以相對路徑指定。必要。

如需更多資訊，請參閱[REST 層 TLS]({{site.url}}{{site.baseurl}}/security/configuration/tls/#rest-layer-tls)。

## 傳輸層安全性設定

Security 外掛程式支援下列傳輸層安全性設定：

- `plugins.security.ssl.transport.enabled`（靜態）：是否在 REST 層啟用 TLS。

- `plugins.security.ssl.transport.client.pemkey_password`（靜態）：傳輸用戶端所使用之 PEM 格式私密金鑰的密碼。

- `plugins.security.ssl.transport.keystore_keypassword`（靜態）：金鑰儲存區內金鑰的密碼。

- `plugins.security.ssl.transport.server.keystore_keypassword`（靜態）：伺服器金鑰儲存區內金鑰的密碼。

- `plugins.sercurity.ssl.transport.server.keystore_alias`（靜態）：伺服器金鑰儲存區的別名。

- `plugins.sercurity.ssl.transport.client.keystore_alias`（靜態）：用戶端金鑰儲存區的別名。

- `plugins.sercurity.ssl.transport.server.truststore_alias`（靜態）：伺服器信任儲存區的別名。

- `plugins.sercurity.ssl.transport.client.truststore_alias`（靜態）：用戶端信任儲存區的別名。

- `plugins.security.ssl.client.external_context_id`（靜態）：為傳輸用戶端提供用於外部 SSL 內容的 ID。

- `plugins.secuirty.ssl.transport.principal_extractor_class`（靜態）：指定實作擷取器的類別，以便將憑證的自訂部分用作主體。

- `plugins.security.ssl.http.crl.file_path`（靜態）：憑證撤銷清單檔案的檔案路徑。

- `plugins.security.ssl.http.crl.validate`（靜態）：啟用憑證撤銷清單 (CRL) 驗證。預設為 `false`（停用）。

- `plugins.security.ssl.http.crl.prefer_crlfile_over_ocsp`（靜態）：當憑證同時包含 CRL 憑證項目與線上憑證狀態通訊協定 (OCSP) 項目時，是否優先使用 CRL 憑證項目。選用。預設為 `false`。

- `plugins.security.ssl.http.crl.check_only_end_entitites`（靜態）：設為 `true` 時，僅驗證末端憑證。預設為 `true`。

- `plugins.security.ssl.http.crl.disable_ocsp`（靜態）：停用 OCSP。預設為 `false`（OCSP 為啟用狀態）。  

- `plugins.security.ssl.http.crl.disable_crldp`（靜態）：停用憑證中的 CRL 端點。預設為 `false`（CRL 端點為啟用狀態）。

- `plugins.security.ssl.allow_client_initiated_renegotiation`（靜態）：啟用或停用用戶端重新交涉。預設為 `false`（不允許由用戶端發起的重新交涉）。

- `plugins.security_config.ssl_dual_mode_enabled`（靜態）：啟用雙模式 SSL，讓節點可在傳輸層同時接受加密 (TLS) 與未加密的流量。設為 `true` 時，節點可使用 SSL 或非 SSL 連線與其他節點通訊。此設定專為過渡情境而設計，例如透過滾動重新啟動程序，將叢集從停用安全性遷移至啟用安全性。請勿在生產環境中無限期使用此設定。請僅在遷移期間暫時使用，並在叢集中所有節點都使用相同的安全性組態後將其停用。預設為 `false`。

## 安全性外掛程式設定範例

```yml
# Common configuration settings
plugins.security.nodes_dn:
  - "CN=*.example.com, OU=SSL, O=Test, L=Test, C=DE"
  - "CN=node.other.com, OU=SSL, O=Test, L=Test, C=DE"
  - "CN=node.example.com, OU=SSL\\, Inc., L=Test, C=DE" # escape additional comma with `\\`
plugins.security.authcz.admin_dn:
  - CN=kirk,OU=client,O=client,L=test, C=de
plugins.security.roles_mapping_resolution: MAPPING_ONLY
plugins.security.ssl.transport.pemcert_filepath: esnode.pem
plugins.security.ssl.transport.pemkey_filepath: esnode-key.pem
plugins.security.ssl.transport.pemtrustedcas_filepath: root-ca.pem
transport.ssl.enforce_hostname_verification: false
plugins.security.ssl.http.enabled: true
plugins.security.ssl.http.pemcert_filepath: esnode.pem
plugins.security.ssl.http.pemkey_filepath: esnode-key.pem
plugins.security.ssl.http.pemtrustedcas_filepath: root-ca.pem
plugins.security.allow_unsafe_democertificates: true
plugins.security.allow_default_init_securityindex: true
plugins.security.nodes_dn_dynamic_config_enabled: false
plugins.security.cert.intercluster_request_evaluator_class: # need example value for this.
plugins.security.audit.type: internal_opensearch
plugins.security.enable_snapshot_restore_privilege: true
plugins.security.check_snapshot_restore_write_privileges: true
plugins.security.cache.ttl_minutes: 60
plugins.security.restapi.roles_enabled: ["all_access", "security_rest_api_access"]
plugins.security.system_indices.enabled: true
plugins.security.system_indices.indices: [".opendistro-alerting-config", ".opendistro-alerting-alert*", ".opendistro-anomaly-results*", ".opendistro-anomaly-detector*", ".opendistro-anomaly-checkpoints", ".opendistro-anomaly-detection-state", ".opendistro-reports-*", ".opendistro-notifications-*", ".opendistro-notebooks", ".opendistro-asynchronous-search-response*"]
node.max_local_storage_nodes: 3
plugins.security.restapi.password_validation_regex: '(?=.*[A-Z])(?=.*[^a-zA-Z\d])(?=.*[0-9])(?=.*[a-z]).{8,}'
plugins.security.restapi.password_validation_error_message: "Password must be minimum 8 characters long and must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
plugins.security.allow_default_init_securityindex: true
plugins.security.cache.ttl_minutes: 60
#
# REST Management API configuration settings
plugins.security.restapi.roles_enabled: ["all_access","xyz_role"]
plugins.security.restapi.endpoints_disabled.all_access.ACTIONGROUPS: ["PUT","POST","DELETE"] # Alternative example: plugins.security.restapi.endpoints_disabled.xyz_role.INTERNALUSERS: ["DELETE"] #
# Audit log configuration settings
plugins.security.audit.enable_rest: true
plugins.security.audit.enable_transport: false
plugins.security.audit.resolve_bulk_requests: false
plugins.security.audit.config.disabled_categories: ["AUTHENTICATED","GRANTED_PRIVILEGES"]
plugins.security.audit.ignore_requests: ["indices:data/read/*","*_bulk"]
plugins.security.audit.threadpool.size: 10
plugins.security.audit.threadpool.max_queue_len: 100000
plugins.security.audit.ignore_users: ['kibanaserver','some*user','/also.*regex possible/']
plugins.security.audit.type: internal_opensearch
#
# external_opensearch settings
plugins.security.audit.config.http_endpoints: ['localhost:9200','localhost:9201','localhost:9202']
plugins.security.audit.config.index: "'security-auditlog-'2023.06.15"
plugins.security.audit.config.type: auditlog
plugins.security.audit.config.username: auditloguser
plugins.security.audit.config.password: auditlogpassword
plugins.security.audit.config.enable_ssl: false
plugins.security.audit.config.verify_hostnames: false
plugins.security.audit.config.enable_ssl_client_auth: false
plugins.security.audit.config.cert_alias: mycert
plugins.security.audit.config.pemkey_filepath: key.pem
plugins.security.audit.config.pemkey_content: <...pem base 64 content>
plugins.security.audit.config.pemkey_password: secret
plugins.security.audit.config.pemcert_filepath: cert.pem
plugins.security.audit.config.pemcert_content: <...pem base 64 content>
plugins.security.audit.config.pemtrustedcas_filepath: ca.pem
plugins.security.audit.config.pemtrustedcas_content: <...pem base 64 content>
#
# Webhook settings
plugins.security.audit.config.webhook.url: "http://mywebhook/endpoint"
plugins.security.audit.config.webhook.format: JSON
plugins.security.audit.config.webhook.ssl.verify: false
plugins.security.audit.config.webhook.ssl.pemtrustedcas_filepath: ca.pem
plugins.security.audit.config.webhook.ssl.pemtrustedcas_content: <...pem base 64 content>
#
# log4j settings
plugins.security.audit.config.log4j.logger_name: auditlogger
plugins.security.audit.config.log4j.level: INFO
#
# Advanced configuration settings
plugins.security.authcz.impersonation_dn:
  "CN=spock,OU=client,O=client,L=Test,C=DE":
    - worf
  "cn=webuser,ou=IT,ou=IT,dc=company,dc=com":
    - user2
    - user1
plugins.security.authcz.rest_impersonation_user:
  "picard":
    - worf
  "john":
    - steve
    - martin
plugins.security.allow_default_init_securityindex: false
plugins.security.allow_unsafe_democertificates: false
plugins.security.cache.ttl_minutes: 60
plugins.security.restapi.password_validation_regex: '(?=.*[A-Z])(?=.*[^a-zA-Z\d])(?=.*[0-9])(?=.*[a-z]).{8,}'
plugins.security.restapi.password_validation_error_message: "A password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
plugins.security.restapi.password_min_length: 8
plugins.security.restapi.password_score_based_validation_strength: very_strong
#
# Advanced SSL settings - use only if you understand SSL ins and outs
plugins.security.ssl.transport.client.pemkey_password: superSecurePassword1
plugins.security.ssl.transport.keystore_keypassword: superSecurePassword2
plugins.security.ssl.transport.server.keystore_keypassword: superSecurePassword3
plugins.security.ssl.http.keystore_keypassword: superSecurePassword4
plugins.security.ssl.http.clientauth_mode: REQUIRE
plugins.security.ssl.transport.enabled: true
plugins.security.ssl.transport.server.keystore_alias: my_alias
plugins.security.ssl.transport.client.keystore_alias: my_other_alias
plugins.security.ssl.transport.server.truststore_alias: trustore_alias_1
plugins.security.ssl.transport.client.truststore_alias: trustore_alias_2
plugins.security.ssl.client.external_context_id: my_context_id
plugins.security.ssl.transport.principal_extractor_class: org.opensearch.security.ssl.ExampleExtractor
plugins.security.ssl.http.crl.file_path: ssl/crl/revoked.crl
plugins.security.ssl.http.crl.validate: true
plugins.security.ssl.http.crl.prefer_crlfile_over_ocsp: true
plugins.security.ssl.http.crl.check_only_end_entitites: false
plugins.security.ssl.http.crl.disable_ocsp: true
plugins.security.ssl.http.crl.disable_crldp: true
plugins.security.ssl.allow_client_initiated_renegotiation: true
#
# Expert settings - use only if you understand their use completely: accidental values can potentially cause security risks or failures to OpenSearch Security.
plugins.security.config_index_name: .opendistro_security
plugins.security.cert.oid: '1.2.3.4.5.5'
plugins.security.cert.intercluster_request_evaluator_class: org.opensearch.security.transport.DefaultInterClusterRequestEvaluator
plugins.security.enable_snapshot_restore_privilege: true
plugins.security.check_snapshot_restore_write_privileges: true
plugins.security.cache.ttl_minutes: 60
plugins.security.disabled: false
plugins.security.protected_indices.enabled: true
plugins.security.protected_indices.roles: ['all_access']
plugins.security.protected_indices.indices: []
plugins.security.system_indices.enabled: true
plugins.security.system_indices.indices: ['.opendistro-alerting-config', '.opendistro-ism-*', '.opendistro-reports-*', '.opensearch-notifications-*', '.opensearch-notebooks', '.opensearch-observability', '.opendistro-asynchronous-search-response*', '.replication-metadata-store']
```
{% include copy.html %}
