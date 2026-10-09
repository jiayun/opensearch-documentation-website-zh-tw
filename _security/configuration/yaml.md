---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "修改 YAML 檔案"
parent: Configuration
nav_order: 15
redirect_from: 
  - /security-plugin/configuration/yaml/
---

# 修改安全性 YAML 檔案

Security 安裝提供多個 YAML 組態檔案，用來儲存必要的設定，這些設定定義了 Security 外掛程式如何管理叢集內的使用者、角色和活動。這些設定涵蓋範圍從驗證後端的組態，到允許的端點和 HTTP 請求清單。

在執行 [`securityadmin.sh`]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/) 將設定載入 `.opendistro_security` 索引之前，請先對 YAML 檔案進行初始組態。這些檔案位於 `config/opensearch-security` 目錄中。備份這些檔案也是良好的做法，如此一來，您就能在其他叢集中重複使用這些檔案。

我們建議的 YAML 檔案使用方式，是先設定[保留和隱藏的資源]({{site.url}}{{site.baseurl}}/security/access-control/api#reserved-and-hidden-resources)，例如 `admin` 和 `kibanaserver` 使用者。之後，您可以使用 OpenSearch Dashboards 或 REST API 建立其他使用者、角色、對應、動作群組和租用戶。

## action_groups.yml

此檔案包含您的安全性組態所需的任何角色對應。您可以在 `<OPENSEARCH_HOME>/config/opensearch-security/roles_mapping.yml` 中找到 `role_mapping.yml` 檔案。

除了部分中繼資料之外，預設檔案是空的，因為 Security 外掛程式有許多會自動新增的靜態動作群組。這些靜態動作群組涵蓋各式各樣的使用案例，是開始使用此外掛程式的絕佳方式。

```yml
---
my-action-group:
  reserved: false
  hidden: false
  allowed_actions:
  - "indices:data/write/index*"
  - "indices:data/write/update*"
  - "indices:admin/mapping/put"
  - "indices:data/write/bulk*"
  - "read"
  - "write"
  static: false
_meta:
  type: "actiongroups"
  config_version: 2
```

## allowlist.yml

您可以使用 `allowlist.yml` 將任何端點和 HTTP 請求新增至允許的端點和請求清單。若已啟用，除了超級管理員之外，所有使用者都只能存取指定的端點和 HTTP 請求，而與該端點相關的所有其他 HTTP 請求都會遭到拒絕。例如，若將 GET `_cluster/settings` 新增至允許清單，使用者便無法向 `_cluster/settings` 提交 PUT 請求來更新叢集設定。

您可以在 `<OPENSEARCH_HOME>/config/opensearch-security/allowlist.yml` 中找到 `allowlist.yml` 檔案。

請注意，雖然您可以透過這種方式設定端點的存取權，但在大多數情況下，最好還是使用 Security 外掛程式的使用者和角色來設定權限，因為它們具有更精細的設定。

```yml
---
_meta:
  type: "allowlist"
  config_version: 2

# Description:
# enabled - feature flag.
# if enabled is false, all endpoints are accessible.
# if enabled is true, all users except the SuperAdmin can only submit the allowed requests to the specified endpoints.
# SuperAdmin can access all APIs.
# SuperAdmin is defined by the SuperAdmin certificate, which is configured with the opensearch.yml setting plugins.security.authcz.admin_dn:
# Refer to the example setting in opensearch.yml to learn more about configuring SuperAdmin.
#
# requests - map of allow listed endpoints and HTTP requests

#this name must be config
config:
  enabled: true
  requests:
    /_cluster/settings:
      - GET
    /_cat/nodes:
      - GET
```

若要啟用對叢集設定的 PUT 請求，請將 PUT 新增至 `/_cluster/settings` 下的允許操作清單。

```yml
requests:
  /_cluster/settings:
    - GET
    - PUT
```

您也可以將自訂索引新增至允許清單。`allowlist.yml` 不支援萬用字元，因此您必須手動指定所有要新增的索引。

```yml
requests: # Only allow GET requests to /sample-index1/_doc/1 and /sample-index2/_doc/1
  /sample-index1/_doc/1:
    - GET
  /sample-index2/_doc/1:
    - GET
```

## internal_users.yml

此檔案包含您要新增至 Security 外掛程式內部使用者資料庫的任何初始使用者。您可以在 `<OPENSEARCH_HOME>/config/opensearch-security/internal_users.yml` 中找到此檔案。

此檔案格式需要雜湊處理過的密碼。若要產生雜湊密碼，請執行 `plugins/opensearch-security/tools/hash.sh -p <new-password>`。若您決定保留任何示範使用者，請*變更其密碼*，並重新執行 [securityadmin.sh]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/) 以套用新密碼。

```yml
---
# This is the internal user database
# The hash value is a bcrypt hash and can be generated with plugin/tools/hash.sh

_meta:
  type: "internalusers"
  config_version: 2

# Define your internal users here
new-user:
  hash: "$2y$12$88IFVl6IfIwCFh5aQYfOmuXVL9j2hz/GusQb35o.4sdTDAEMTOD.K"
  reserved: false
  hidden: false
  opendistro_security_roles:
  - "specify-some-security-role-here"
  backend_roles:
  - "specify-some-backend-role-here"
  attributes:
    attribute1: "value1"
  static: false

## Demo users

admin:
  hash: "$2a$12$VcCDgh2NDk07JGN0rjGbM.Ad41qVR/YFJcgHp0UGns5JDymv..TOG"
  reserved: true
  backend_roles:
  - "admin"
  description: "Demo admin user"

kibanaserver:
  hash: "$2a$12$4AcgAt3xwOWadA5s5blL6ev39OXDNhmOesEoo33eZtrq2N0YrU3H."
  reserved: true
  description: "Demo user for the OpenSearch Dashboards server"

kibanaro:
  hash: "$2a$12$JJSXNfTowz7Uu5ttXfeYpeYE0arACvcwlPBStB1F.MI7f0U9Z4DGC"
  reserved: false
  backend_roles:
  - "kibanauser"
  - "readall"
  attributes:
    attribute1: "value1"
    attribute2: "value2"
    attribute3: "value3"
  description: "Demo read-only user for OpenSearch dashboards"

logstash:
  hash: "$2a$12$u1ShR4l4uBS3Uv59Pa2y5.1uQuZBrZtmNfqB3iM/.jL0XoV9sghS2"
  reserved: false
  backend_roles:
  - "logstash"
  description: "Demo logstash user"

readall:
  hash: "$2a$12$ae4ycwzwvLtZxwZ82RmiEunBbIPiAmGZduBAjKN0TXdwQFtCwARz2"
  reserved: false
  backend_roles:
  - "readall"
  description: "Demo readall user"

snapshotrestore:
  hash: "$2y$12$DpwmetHKwgYnorbgdvORCenv4NAK8cPUg8AI6pxLCuWf/ALc0.v7W"
  reserved: false
  backend_roles:
  - "snapshotrestore"
  description: "Demo snapshotrestore user"
```

## nodes_dn.yml

`nodes_dn.yml` 可讓您將憑證的[辨別名稱 (DN)]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/#add-distinguished-names-to-opensearchyml) 新增至允許清單，以啟用任意數量的節點或叢集之間的通訊。例如，允許清單中具有 DN `CN=node1.example.com` 的節點，會接受來自使用該 DN 的任何其他節點或憑證的通訊。

這些 DN 會編製索引至[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)，只有超級管理員或具有傳輸層安全性 (TLS) 憑證的管理員才能存取。若您想以程式設計方式將 DN 新增至允許清單，請使用 [REST API]({{site.url}}{{site.baseurl}}/security/api/distinguished-names/)。

```yml
---
_meta:
  type: "nodesdn"
  config_version: 2

# Define nodesdn mapping name and corresponding values
# cluster1:
#   nodes_dn:
#       - CN=*.example.com
```

## roles_mapping.yml

```yml
---
manage_snapshots:
  reserved: true
  hidden: false
  backend_roles:
  - "snapshotrestore"
  hosts: []
  users: []
  and_backend_roles: []
logstash:
  reserved: false
  hidden: false
  backend_roles:
  - "logstash"
  hosts: []
  users: []
  and_backend_roles: []
own_index:
  reserved: false
  hidden: false
  backend_roles: []
  hosts: []
  users:
  - "*"
  and_backend_roles: []
  description: "Allow full access to an index named like the username"
kibana_user:
  reserved: false
  hidden: false
  backend_roles:
  - "kibanauser"
  hosts: []
  users: []
  and_backend_roles: []
  description: "Maps kibanauser to kibana_user"
complex-role:
  reserved: false
  hidden: false
  backend_roles:
  - "ldap-analyst"
  hosts: []
  users:
  - "new-user"
  and_backend_roles: []
_meta:
  type: "rolesmapping"
  config_version: 2
all_access:
  reserved: true
  hidden: false
  backend_roles:
  - "admin"
  hosts: []
  users: []
  and_backend_roles: []
  description: "Maps admin to all_access"
readall:
  reserved: true
  hidden: false
  backend_roles:
  - "readall"
  hosts: []
  users: []
  and_backend_roles: []
kibana_server:
  reserved: true
  hidden: false
  backend_roles: []
  hosts: []
  users:
  - "kibanaserver"
  and_backend_roles: []
```

## roles.yml

此檔案包含您想新增至 Security 外掛程式的任何初始角色。預設情況下，此檔案包含預先定義的角色，這些角色會授權使用 OpenSearch 預設發行版中的外掛程式。Security 外掛程式也會自動新增多個靜態角色。

```yml
---
complex-role:
  reserved: false
  hidden: false
  cluster_permissions:
  - "read"
  - "cluster:monitor/nodes/stats"
  - "cluster:monitor/task/get"
  index_permissions:
  - index_patterns:
    - "opensearch_dashboards_sample_data_*"
    dls: "{\"match\": {\"FlightDelay\": true}}"
    fls:
    - "~FlightNum"
    masked_fields:
    - "Carrier"
    allowed_actions:
    - "read"
  tenant_permissions:
  - tenant_patterns:
    - "analyst_*"
    allowed_actions:
    - "kibana_all_write"
  static: false
_meta:
  type: "roles"
  config_version: 2
```

## tenants.yml

您可以使用此檔案指定並新增任意數量的 OpenSearch Dashboards 租用戶至您的 OpenSearch 叢集。如需租用戶的更多資訊，請參閱 [OpenSearch Dashboards 多租用戶]({{site.url}}{{site.baseurl}}/security/multi-tenancy/tenant-index/)。

與所有其他 YAML 檔案一樣，我們建議您使用 `tenants.yml` 來新增叢集中必須具備的租用戶，然後在需要進一步設定或建立其他租用戶時，使用 OpenSearch Dashboards 或 [REST API]({{site.url}}{{site.baseurl}}/security/api/tenants/)。

```yml
---
_meta:
  type: "tenants"
  config_version: 2
admin_tenant:
  reserved: false
  description: "Demo tenant for admin user"
```

## opensearch.yml

除了許多 OpenSearch 設定之外，`opensearch.yml` 檔案還包含 TLS 憑證及其屬性的路徑，例如辨別名稱與信任的憑證授權單位。您可以在 `<OPENSEARCH_HOME>/config/` 找到此檔案。

```yml
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
plugins.security.authcz.admin_dn:
  - CN=kirk,OU=client,O=client,L=test, C=de

plugins.security.audit.type: internal_opensearch
plugins.security.enable_snapshot_restore_privilege: true
plugins.security.check_snapshot_restore_write_privileges: true
plugins.security.cache.ttl_minutes: 60
plugins.security.restapi.roles_enabled: ["all_access", "security_rest_api_access"]
plugins.security.system_indices.enabled: true
plugins.security.system_indices.indices: [".opendistro-alerting-config", ".opendistro-alerting-alert*", ".opendistro-anomaly-results*", ".opendistro-anomaly-detector*", ".opendistro-anomaly-checkpoints", ".opendistro-anomaly-detection-state", ".opendistro-reports-*", ".opendistro-notifications-*", ".opendistro-notebooks", ".opendistro-asynchronous-search-response*"]
node.max_local_storage_nodes: 3
```

如需 `opensearch.yml` Security 外掛程式設定的完整清單，請參閱[安全性設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/security-settings/)。
{: .note}

### 微調您的組態

`plugins.security.allow_default_init_securityindex` 設定在設為 `true` 時，若 OpenSearch 啟動時建立安全性索引失敗，會將 Security 外掛程式設回其預設安全性設定。預設安全性設定儲存在 `opensearch-project/security/config` 目錄中的 YAML 檔案內。預設情況下，此設定為 `false`。

```yml
plugins.security.allow_default_init_securityindex: true
```

Security 外掛程式具有驗證快取，可透過暫時儲存從後端傳回的使用者物件來加速驗證，讓 Security 外掛程式不必重複請求這些物件。若要判斷快取逾時所需的時間，您可以使用 `plugins.security.cache.ttl_minutes` 屬性以分鐘為單位設定值。預設值為 `60`。您可以將值設為 `0` 來停用快取。

```yml
plugins.security.cache.ttl_minutes: 60
```

### 啟用使用者對系統索引的存取

將系統索引權限對應至使用者，可讓該使用者修改權限名稱中指定的系統索引（唯一的例外是 Security 外掛程式的[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)）。`plugins.security.system_indices.permission.enabled` 設定提供一種方式，讓管理員在角色對應中提供或隱藏此權限。

設為 `true` 時，此功能會啟用，具有修改角色權限的使用者可以建立包含授予系統索引存取權之權限的角色：

```yml
plugins.security.system_indices.permission.enabled: true
```

設為 `false` 時，此權限會停用，只有具備管理員憑證的管理員才能對系統索引進行變更。在新叢集中，此權限預設設為 `false`。

若要進一步了解系統索引權限，請參閱[系統索引權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/#system-index-permissions)。


### 密碼設定

如果您想對使用者的密碼執行某種驗證，請在此檔案中指定正規表示式 (regex)。您也可以加入密碼未通過驗證時載入的錯誤訊息。下列範例示範如何加入正規表示式，讓 OpenSearch 要求新密碼至少為八個字元，並且至少包含一個大寫字母、一個小寫字母、一個數字與一個特殊字元。

請注意，OpenSearch 只會驗證透過 OpenSearch Dashboards 或 REST API 建立的使用者與密碼。示範組態安裝程式所需的初始管理員密碼，會依據另一組固定的規則進行驗證。如需更多資訊，請參閱[管理員密碼要求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)與[管理密碼]({{site.url}}{{site.baseurl}}/security/configuration/passwords/)。

```yml
plugins.security.restapi.password_validation_regex: '(?=.*[A-Z])(?=.*[^a-zA-Z\d])(?=.*[0-9])(?=.*[a-z]).{8,}'
plugins.security.restapi.password_validation_error_message: "Password must be minimum 8 characters long and must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
```

此外，以分數為基礎的密碼強度估計器可讓您在建立新的內部使用者或更新使用者密碼時，設定密碼強度的門檻。此功能使用 [`zxcvbn` 程式庫](https://github.com/dropbox/zxcvbn)來套用一項政策，強調密碼的複雜度，而非其符合大寫字母、數字與特殊字元等傳統標準的能力。

如需定義使用者的資訊，請參閱[定義使用者]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#defining-users)。

此功能與指定為保留使用者的帳戶不相容。如需保留資源的資訊，請參閱[保留和隱藏的資源]({{site.url}}{{site.baseurl}}/security/access-control/api#reserved-and-hidden-resources)。
{: .important }

以分數為基礎的密碼強度需要兩個設定來組態此功能。下表說明這兩個設定。

| 設定 | 說明 |
| :--- | :--- |
| `plugins.security.restapi.password_min_length` | 設定密碼長度的最小字元數。預設值為 `8`。這也是最小值。 |
| `plugins.security.restapi.password_score_based_validation_strength` | 設定判斷密碼為強或弱的門檻。有四個值代表門檻的複雜度遞增。<br>`fair`--非常「容易猜測」的密碼：可防範受節流的線上攻擊。<br>`good`--稍微容易猜測的密碼：可防範未受節流的線上攻擊。<br>`strong`--安全地「難以猜測」的密碼：可對離線慢雜湊情境提供適度防護。<br>`very_strong`--非常難以猜測的密碼：可對離線慢雜湊情境提供強力防護。 |

下列範例顯示為 `opensearch.yml` 檔案設定的組態，以及啟用最少 10 個字元且門檻要求最高強度的密碼：

```yml
plugins.security.restapi.password_min_length: 10
plugins.security.restapi.password_score_based_validation_strength: very_strong
```

當您嘗試建立密碼未達指定門檻的使用者時，系統會產生「弱密碼」警告，指出必須先修改密碼才能儲存該使用者。

下列範例顯示密碼過弱時 [Create user]({{site.url}}{{site.baseurl}}/security/api/users/create-user/) API 的回應：

```json
{
  "status": "error",
  "reason": "Weak password"
}
```
