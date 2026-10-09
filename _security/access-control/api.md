---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "API 權限"
parent: Access control
nav_order: 120
redirect_from:
 - /security-plugin/access-control/api/
---

# API 權限

安全性外掛程式的 REST API 可讓您以程式設計方式建立及管理使用者、角色、角色對應、動作群組和租用戶。本頁說明如何授予及限制對該 API 的存取，以及保留和隱藏資源如何影響它。如需端點參考，請參閱[安全性 API]({{site.url}}{{site.baseurl}}/security/api/)。

## API 的存取控制

對安全性外掛程式 REST API 的存取有兩層：

- 一般存取決定哪些角色可向安全性 API 傳送請求，以及這些角色可呼叫哪些端點和 HTTP 方法。
- REST API 管理員權限允許沒有管理員憑證的使用者呼叫原本僅限超級管理員使用的 API。

這兩層是獨立的授權。只要其中一層允許，請求就會被允許。

### 啟用一般 API 存取

若要授予角色對安全性 API 的一般存取權，請將該角色新增至 `opensearch.yml` 中的 `plugins.security.restapi.roles_enabled`：

```yml
plugins.security.restapi.roles_enabled: ["<role>", ...]
```
{% include copy.html %}

變更此靜態設定後，請重新啟動叢集。

列於此設定中的角色可以呼叫每個安全性 API，但允許清單、辨別名稱和憑證 API 除外，這些 API 僅限超級管理員使用。若使用者既未對應至這類角色，也未獲授與 [REST API 管理員權限](#rest-api-admin-permissions)，則無論該使用者擁有其他哪些叢集權限，都會收到 `403 Forbidden`。

若要防止角色存取特定 API，請為其停用個別端點：

```yml
plugins.security.restapi.endpoints_disabled.<role>.<endpoint>: ["<method>", ...]
```
{% include copy.html %}

若使用者對應至多個角色，則只有在該使用者所有具有 `endpoints_disabled` 項目的角色都停用某個端點或方法時，該端點或方法才會被停用。例如，若某個角色在 `ROLES` 上停用 `DELETE`，但該使用者的另一個角色並未停用，則該使用者仍可將 `DELETE` 請求傳送至角色 API。個別角色的項目也只會限制一般存取：獲授與相符 [REST API 管理員權限](#rest-api-admin-permissions) 的使用者仍可存取該端點。

若要為每個角色停用某個端點，包括列於 `plugins.security.restapi.roles_enabled` 中的角色，請使用 `global` 取代角色名稱：

```yml
plugins.security.restapi.endpoints_disabled.global.<endpoint>: ["<method>", ...]
```
{% include copy.html %}

與個別角色的項目不同，`global` 項目也會覆寫 REST API 管理員權限。

### REST API 管理員權限

`restapi:admin` 叢集權限會授予 `plugins.security.restapi.roles_enabled` 角色未提供的存取權：允許清單、辨別名稱和憑證 API，這些 API 原本僅限超級管理員使用；安全性組態本身的若干操作；以及對隱藏和保留資源的管理員層級存取。若要使用這些權限，請在 `opensearch.yml` 中啟用 REST API 管理員權限：

```yml
plugins.security.restapi.admin.enabled: true
```
{% include copy.html %}

變更此靜態設定後，請重新啟動叢集。然後授予該角色您希望其存取之端點的叢集權限。該角色不需要同時列於 `plugins.security.restapi.roles_enabled` 中。當 `plugins.security.restapi.admin.enabled` 為 `false` 時，OpenSearch 會忽略這些權限，且這些 API 仍只能透過管理員憑證存取。

您必須明確指派這些權限。`*` 和 `cluster:*` 等廣泛的叢集權限不會授予這些權限，且您無法透過動作群組授予這些權限。

包含任何 `restapi:admin` 權限的角色無法透過[角色 API]({{site.url}}{{site.baseurl}}/security/api/roles/) 建立或修改，即使是超級管理員也不行，這類角色的對應也無法透過[角色對應 API]({{site.url}}{{site.baseurl}}/security/api/role-mappings/) 建立或修改。請在 `roles.yml` 中定義角色，並在 `roles_mapping.yml` 中定義其對應，然後使用 `securityadmin.sh` 套用兩者。此限制連同動作群組限制，可防止使用者為自己授予對安全性 API 的額外存取權。如需詳細資訊，請參閱[將變更套用至組態檔]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)。
{: .note}

下表列出對應至安全性 API 的叢集權限。保留的 `security_rest_api_full_access` 角色包含所有這些權限，但 `restapi:admin/ratelimiters`、`restapi:admin/rollback_version` 和 `restapi:admin/view_version` 除外。由於該角色允許對安全性敏感的叢集變更，請僅將其對應至受信任的管理員。

| 權限 | 授予的 API | 說明 |
| :--- | :--- | :--- |
| `restapi:admin/actiongroups` | `/actiongroup` 和 `/actiongroups` | 擷取、建立、修改和刪除任何動作群組的權限，包括大量更新。 |
| `restapi:admin/allowlist` | `/allowlist` | 將端點和 HTTP 方法新增至允許清單的權限。 |
| `restapi:admin/config/update` | `/securityconfig` 上的 `PUT` 和 `PATCH` | 取代或修補安全性組態的權限。 |
| `restapi:admin/internalusers` | `/internaluser` 和 `/user` | 在叢集中新增、擷取、修改和刪除任何使用者的權限。 |
| `restapi:admin/nodesdn` | `/nodesdn` | 在允許清單中新增、擷取、更新和刪除辨別名稱的權限，該允許清單可啟用叢集與節點之間的通訊。 |
| `restapi:admin/ratelimiters` | `/authfailurelisteners` | 擷取和修改驗證速率限制組態的權限。 |
| `restapi:admin/resource_sharing/migrate` | `/resources/migrate` | 遷移外掛程式定義的資源共用記錄的權限。 |
| `restapi:admin/roles` | `/roles` | 在叢集中新增、擷取、修改和刪除任何角色的權限。 |
| `restapi:admin/rolesmapping` | `/rolesmapping` | 新增、擷取、修改和刪除任何角色對應的權限。 |
| `restapi:admin/rollback_version` | `/version/rollback` | 還原安全性組態先前版本的權限。 |
| `restapi:admin/ssl/certs/info` | `/certificates`、`/certificates/{node_id}` 和 `/ssl/certs` | 檢視目前傳輸和 HTTP 憑證的權限。 |
| `restapi:admin/ssl/certs/reload` | `/ssl/{cert_type}/reloadcerts` | 重新載入傳輸和 HTTP 憑證的權限。 |
| `restapi:admin/tenants` | `/tenants` | 擷取、建立、修改和刪除任何租用戶的權限。 |
| `restapi:admin/view_version` | `/versions` 和 `/version/{version_id}` | 列出安全性組態版本並擷取其中一個版本內容的權限。 |

上表中的路徑相對於 `_plugins/_security/api/`。若要一次授予角色所有這些權限，請將 `restapi:admin/*` 直接指派給該角色。

本表未列出的安全性 API 沒有自己的 `restapi:admin` 權限。列於 `plugins.security.restapi.roles_enabled` 中的角色已可呼叫它們。

一般存取已涵蓋既非隱藏也非保留的動作群組、內部使用者、角色、角色對應和租用戶資源。上表中相符的權限會將該存取權延伸至[保留和隱藏資源](#reserved-and-hidden-resources)。

例如，下列角色會授予對內部使用者 API 的管理員層級存取權。請在 `roles.yml` 中定義該角色：

```yml
manage_internal_users:
  reserved: true
  cluster_permissions:
    - "restapi:admin/internalusers"
```
{% include copy.html %}

在 `roles_mapping.yml` 中將使用者或後端角色對應至該角色：

```yml
manage_internal_users:
  reserved: true
  backend_roles:
    - "internal-user-api-operators"
  hosts: []
  users: []
  and_backend_roles: []
```
{% include copy.html %}

使用 [`securityadmin.sh`]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/) 套用這兩個檔案。此組態可存取內部使用者 API，而不會授予對任何其他安全性 API 的存取權。若要同時授予該角色一般存取權，也請將其列於 `plugins.security.restapi.roles_enabled` 中。

### 端點值

下表列出有效的 `endpoint` 值，以及每個值所涵蓋的 API。

| 值 | API |
| :--- | :--- |
| `ACTIONGROUPS` | 動作群組 API。 |
| `ALLOWLIST` | 允許清單 API。 |
| `APITOKENS` | API 金鑰 API。 |
| `AUDIT` | 稽核記錄 API。 |
| `AUTHTOKEN` | Authorization Token API。 |
| `CACHE` | Flush Cache API。 |
| `CONFIG` | 組態 API，包括升級檢查和升級操作。 |
| `INTERNALUSERS` | 內部使用者 API。 |
| `NODESDN` | 辨別名稱 API。 |
| `RATELIMITERS` | 設定驗證速率限制的 API。 |
| `RESOURCE_SHARING` | 遷移外掛程式定義的資源共用記錄的操作。 |
| `ROLES` | 角色 API。 |
| `ROLESMAPPING` | 角色對應 API。 |
| `ROLLBACK_VERSION` | 還原安全性組態先前版本的操作。 |
| `SSL` | 憑證 API。 |
| `TENANTS` | 租用戶 API 和多租用戶組態 API。 |
| `VIEW_VERSION` | 列出安全性組態版本並傳回其中一個版本內容的操作。 |

帳戶 API、Permissions Info API、Dashboards Info API 和 Security Plugin Health API 沒有 `endpoint` 值，因為任何已驗證的使用者都可以呼叫它們。

`method` 的可能值為：

- `GET`
- `PUT`
- `POST`
- `DELETE`
- `PATCH`

例如，下列組態會授予 `rest_api_user` 一般 API 存取權，但封鎖角色和內部使用者 API 上的所有方法：

```yml
plugins.security.restapi.roles_enabled: ["rest_api_user"]
plugins.security.restapi.endpoints_disabled.rest_api_user.ROLES: ["*"]
plugins.security.restapi.endpoints_disabled.rest_api_user.INTERNALUSERS: ["*"]
```
{% include copy.html %}

若要對[組態 API]({{site.url}}{{site.baseurl}}/security/api/configuration/) 使用 `PUT` 和 `PATCH` 方法，請將下列行新增至 `opensearch.yml`：

```yml
plugins.security.unsupported.restapi.allow_securityconfig_modification: true
```
{% include copy.html %}

## 保留和隱藏資源

您可以將使用者、角色、角色對應和動作群組標記為保留。將此旗標設為 true 的資源無法使用 REST API 或 OpenSearch Dashboards 變更。

若要將資源標記為保留，請新增下列旗標：

```yml
kibana_user:
  reserved: true
```
{% include copy.html %}

同樣地，您可以將使用者、角色、角色對應和動作群組標記為隱藏。將此旗標設為 true 的資源不會由 REST API 傳回，也不會顯示在 OpenSearch Dashboards 中：

```yml
kibana_user:
  hidden: true
```
{% include copy.html %}

隱藏資源會自動保留。

若要新增或移除這些旗標，請修改 `config/opensearch-security/internal_users.yml` 並執行 `plugins/opensearch-security/tools/securityadmin.sh`。

## 資源共用
**於 3.3 版推出**
{: .label .label-purple }

如需管理資源層級的存取控制，以及共用外掛程式定義的資源 (例如 ML 模型和異常偵測器)，請參閱[資源共用 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/)。
