---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安全性組態 API"
parent: Security APIs
nav_order: 110
has_children: true
has_toc: false
redirect_from:
  - /api-reference/security/configuration/
  - /api-reference/security/configuration/index/
  - /security/api/configuration/
---

# 安全性組態 API

組態 API 可擷取、取代、修補及升級安全性外掛程式組態。

OpenSearch 支援下列組態 API。

| API | 說明 |
| :--- | :--- |
| [建立或更新安全性組態 API]({{site.url}}{{site.baseurl}}/security/api/configuration/update-configuration/) | 建立或取代安全性外掛程式組態。 |
| [修補安全性組態 API]({{site.url}}{{site.baseurl}}/security/api/configuration/patch-configuration/) | 更新安全性外掛程式組態的個別部分，而不取代整份組態文件。 |
| [取得安全性組態 API]({{site.url}}{{site.baseurl}}/security/api/configuration/get-configuration/) | 擷取目前的安全性外掛程式組態，包括其驗證與授權網域。 |
| [檢查安全性組態升級 API]({{site.url}}{{site.baseurl}}/security/api/configuration/upgrade-check/) | 檢查是否有任何組態元件需要升級，並列出可用的升級項目。 |
| [執行安全性組態升級 API]({{site.url}}{{site.baseurl}}/security/api/configuration/upgrade-perform/) | 套用「檢查升級 API」所識別的升級項目。 |

這些 API 可管理下列組態元件：

- 角色，定義使用者可執行的動作
- 角色對應，將使用者或後端角色對應至特定角色
- 動作群組，是用來簡化角色定義的權限集合
- 內部使用者，其認證資訊直接儲存在 OpenSearch 中
- 租用戶，是支援多租用戶的隔離工作區
- 安全性組態，包含全域安全性設定

## `authc`

驗證網域 (`authc`) 定義 OpenSearch 如何從驗證回應中擷取使用者資訊與後端角色。在與 SAML、OpenID Connect (OIDC) 或自訂驗證後端等外部系統整合時，這點尤其重要。

為支援角色對應，請使用下列組態索引鍵：

- `subject_key`：指定在驗證回應中何處尋找使用者識別碼。
- `roles_key`：指出在驗證回應中何處尋找後端角色。

OpenSearch 會使用擷取出的後端角色進行角色對應，以將角色指派給使用者。

下列範例設定一個驗證網域，從 JSON Web Token (JWT) 中的 `preferred_username` 擷取使用者名稱，並從 `groups` 擷取後端角色：

```json
{
  "authc": {
    "oidc_auth_domain": {
      "http_enabled": true,
      "transport_enabled": false,
      "order": 1,
      "http_authenticator": {
        "type": "openid",
        "challenge": false,
        "config": {
          "subject_key": "preferred_username",
          "roles_key": "groups",
          "openid_connect_url": "https://identity.example.com/.well-known/openid-configuration"
        }
      },
      "authentication_backend": {
        "type": "noop",
        "config": {}
      }
    }
  }
}
```
{% include copy.html %}

接著您可以在角色對應中使用擷取出的後端角色。下列組態會將 `analyst_role` 指派給驗證回應中包含 `analyst_group` 或 `data_scientist_group` 的使用者：

```json
{
  "role_mappings": {
    "analyst_role": {
      "backend_roles": ["analyst_group", "data_scientist_group"]
    }
  }
}
```
{% include copy.html %}

## `authz`

`authz` 區段會從 LDAP 等外部來源擷取後端角色來處理授權。這可讓 OpenSearch 透過一種方法 (例如基本驗證或 SAML) 驗證使用者，並根據儲存在另一個目錄中的角色資訊對其授權。此設定在身分識別由一個系統管理、角色由另一個系統管理的企業環境中很實用。

典型的 `authz` 組態包含下列元素：

- `roles_search_filter`：用來尋找使用者角色的 LDAP 搜尋篩選條件。
- `rolebase`：用來搜尋角色的辨別名稱 (DN)。
- `rolesearch`：尋找角色時所使用的搜尋模式。
- `rolename`：包含角色名稱的屬性。

下列範例會連線至 LDAP 目錄，使用 `rolesearch` 篩選條件尋找使用者群組，並使用 `rolename` 屬性將每個群組擷取為後端角色：

```json
{
  "authz": {
    "ldap_role_authz": {
      "http_enabled": true,
      "transport_enabled": true,
      "authorization_backend": {
        "type": "ldap",
        "config": {
          "rolebase": "ou=groups,dc=example,dc=com",
          "rolesearch": "(uniqueMember={0})",
          "rolename": "cn",
          "userbase": "ou=people,dc=example,dc=com",
          "usersearch": "(uid={0})",
          "username_attribute": "uid"
        }
      }
    }
  }
}
```
{% include copy.html %}

下列範例會將 LDAP 群組對應至 OpenSearch 角色。若使用者屬於 LDAP 群組 `cn=analysts,ou=groups,dc=example,dc=com`，則會擷取後端角色 `analysts` 並對應至 `data_access_role`：

```json
{
  "role_mappings": {
    "data_access_role": {
      "backend_roles": ["analysts", "researchers"]
    }
  }
}
```
{% include copy.html %}

## 最佳實務

使用組態 API 時，請遵循下列最佳實務：

- 進行變更前，請務必備份您的安全性組態。
- 使用「執行升級 API」之前，請先執行「檢查升級 API」。
- 部署至正式環境前，請先在非正式環境中測試變更。
- 將這些 API 整合至您例行的升級與維護工作流程中。
- 套用組態變更後，請驗證功能是否正常。
