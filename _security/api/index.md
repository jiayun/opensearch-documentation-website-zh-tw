---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安全性 API"
nav_order: 80
has_children: true
has_toc: false
redirect_from:
  - /security/api/
  - /api-reference/security/
  - /api-reference/security/index/
  - /api-reference/security-apis/
---

# 安全性 API

安全性 API 透過 REST 設定及檢查 Security 外掛程式。您可以使用這些 API 管理使用者、角色、角色對應、動作群組和租用戶；讀取及取代安全性組態；以及檢查憑證、快取和外掛程式的健康狀態。

所有安全性 API 皆使用基礎路徑 `_plugins/_security/`，後面接上各項操作的特定路徑。例如，Perform Upgrade API 的路徑為 `/_plugins/_security/api/_upgrade_perform`。

這些 API 大多會讀取及寫入安全性組態索引，因此其存取權受到限制。若要呼叫其中一個 API，提出請求的使用者必須對應到 `opensearch.yml` 中 `plugins.security.restapi.roles_enabled` 設定所列出的角色，或擁有相符的 [REST API 管理員權限]({{site.url}}{{site.baseurl}}/security/access-control/api/#rest-api-admin-permissions)。兩者皆不具備的使用者會收到 `403 Forbidden`，無論該使用者已獲授予哪些其他叢集權限。

有四個 API 不受此限制，因為它們只會公開提出請求之使用者本身的資訊：[帳戶 API]({{site.url}}{{site.baseurl}}/security/api/account/)、[Permissions Info API]({{site.url}}{{site.baseurl}}/security/api/authentication/permissions-info/)、[Dashboards Info API]({{site.url}}{{site.baseurl}}/security/api/dashboards-info/) 以及 [Security Plugin Health API]({{site.url}}{{site.baseurl}}/security/api/health/)。任何已通過驗證的使用者皆可呼叫這些 API。

對於三組 API 而言，僅具備 `plugins.security.restapi.roles_enabled` 角色並不足夠。[允許清單 API]({{site.url}}{{site.baseurl}}/security/api/allowlist/)、[辨別名稱 API]({{site.url}}{{site.baseurl}}/security/api/distinguished-names/) 和 [憑證 API]({{site.url}}{{site.baseurl}}/security/api/certificates/) 僅限超級管理員使用，各類別頁面會說明可讓角色改為存取這些 API 的叢集權限。如需更多資訊，請參閱 [API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/)。

下列範例以 `admin` 使用者身分使用 HTTP 基本驗證：

```bash
curl -k -XGET -u admin:<password> https://localhost:9200/_plugins/_security/api/roles/
```
{% include copy.html %}

Security 外掛程式隨附一份用於測試的示範組態。請勿在正式環境中使用示範組態。在正式環境部署時，請產生安全的認證資訊和憑證。
{: .warning}

## 支援的 API

安全性 API 依各自設定的資源進行分組。下表列出可用的群組。選取一個群組即可檢視其提供的操作。

| 群組 | 說明 |
| :--- | :--- |
| [驗證 API]({{site.url}}{{site.baseurl}}/security/api/authentication/) | 驗證 API 會傳回已通過驗證之使用者的相關資訊、授予該使用者的權限，以及用於發出請求的 TLS 連線。 |
| [帳戶 API]({{site.url}}{{site.baseurl}}/security/api/account/) | 帳戶 API 會傳回及修改目前已通過驗證之使用者本身帳戶的詳細資料。 |
| [內部使用者 API]({{site.url}}{{site.baseurl}}/security/api/users/) | 內部使用者 API 可在內部使用者資料庫中建立、擷取、修改及刪除使用者。 |
| [角色 API]({{site.url}}{{site.baseurl}}/security/api/roles/) | 角色 API 可建立、擷取、修改及刪除用於定義叢集、索引和文件權限的角色。 |
| [角色對應 API]({{site.url}}{{site.baseurl}}/security/api/role-mappings/) | 角色對應 API 可將使用者、後端角色和主機對應到安全性角色。 |
| [動作群組 API]({{site.url}}{{site.baseurl}}/security/api/action-groups/) | 動作群組 API 可建立、擷取、修改及刪除動作群組，動作群組是可重複使用的權限集合。 |
| [API 金鑰 API]({{site.url}}{{site.baseurl}}/security/api/api-keys/) | API 金鑰 API 可建立、列出及撤銷 API 金鑰，這些金鑰可用於在不需使用者名稱和密碼的情況下驗證請求。 |
| [租用戶 API]({{site.url}}{{site.baseurl}}/security/api/tenants/) | 租用戶 API 可建立、擷取、修改及刪除租用戶，租用戶可在不同使用者群組之間隔離 OpenSearch Dashboards 資源。 |
| [多租用戶組態 API]({{site.url}}{{site.baseurl}}/security/api/tenancy/) | 多租用戶組態 API 可設定 OpenSearch Dashboards 的多租用戶功能，並傳回目前使用者可用之租用戶的相關資訊。 |
| [允許清單 API]({{site.url}}{{site.baseurl}}/security/api/allowlist/) | 允許清單 API 可控制不具管理員權限的使用者能夠存取哪些 API。 |
| [組態 API]({{site.url}}{{site.baseurl}}/security/api/configuration/) | 組態 API 可擷取、取代、修補及升級 Security 外掛程式組態。 |
| [安全性組態版本 API]({{site.url}}{{site.baseurl}}/security/api/configuration-versions/) | 安全性組態版本 API 可追蹤 Security 外掛程式組態的歷程記錄，並還原其先前的版本。 |
| [稽核記錄檔 API]({{site.url}}{{site.baseurl}}/security/api/audit/) | 稽核記錄檔 API 可擷取及修改稽核記錄組態。 |
| [辨別名稱 API]({{site.url}}{{site.baseurl}}/security/api/distinguished-names/) | 辨別名稱 API 可管理用於跨叢集通訊之節點和用戶端憑證辨別名稱的允許清單。 |
| [憑證 API]({{site.url}}{{site.baseurl}}/security/api/certificates/) | 憑證 API 會傳回叢集上使用中的憑證，並可在不重新啟動節點的情況下重新載入憑證。 |
| [Flush Cache API]({{site.url}}{{site.baseurl}}/security/api/flush-cache/) | Flush Cache API 會排清 Security 外掛程式的使用者、驗證和授權快取。 |
| [Dashboards Info API]({{site.url}}{{site.baseurl}}/security/api/dashboards-info/) | Dashboards Info API 會傳回 OpenSearch Dashboards 呈現其介面所需的 Security 外掛程式設定。 |
| [Security Plugin Health API]({{site.url}}{{site.baseurl}}/security/api/health/) | Security Plugin Health API 會回報 Security 外掛程式是否已初始化，並已準備好授權請求。 |
