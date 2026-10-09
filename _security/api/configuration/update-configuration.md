---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新組態"
parent: Security configuration APIs
grand_parent: Security APIs
nav_order: 10
redirect_from:
  - /api-reference/security/configuration/update-configuration/
---

# 建立或更新安全性組態 API
**於 2.10 版推出**
{: .label .label-purple }

建立或更新組態 API 會直接透過 REST API 建立或更新安全性外掛程式的組態。此組態會管理核心安全性設定，包括驗證方法、授權規則及存取控制。

此操作很容易破壞您現有的安全性組態。我們強烈建議改用 `securityadmin.sh` 指令碼，其中包含驗證與防護機制，可避免組態錯誤。
{: .warning}

<!-- spec_insert_start
api: security.update_configuration
component: endpoints
-->
## 端點
```json
PUT /_plugins/_security/api/securityconfig/config
```
<!-- spec_insert_end -->

## 請求本文欄位

請求本文為**必要**。其為包含下列欄位的 JSON 物件。

| 屬性 | 必要性 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `dynamic` | **必要** | 物件 | 包含所有安全性組態設定的主要組態物件。 |

<details markdown="block">
<summary>
    請求本文欄位：<code>dynamic</code>
</summary>
{: .text-delta}

`dynamic` 是包含下列欄位的 JSON 物件。

| 屬性 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `auth_failure_listeners` | 物件 | 處理驗證失敗的組態，包括閾值與動作。 |
| `authc` | 物件 | 定義使用者如何通過驗證的驗證組態網域。如需更多資訊，請參閱 [`authc`]({{site.url}}{{site.baseurl}}/security/api/configuration/index/#authc)。 |
| `authz` | 物件 | 定義使用 LDAP 進行驗證時如何擷取後端角色的授權組態。如需更多資訊，請參閱 [`authz`]({{site.url}}{{site.baseurl}}/security/api/configuration/index/#authz)。 |
| `do_not_fail_on_forbidden` | 布林值 | 當 `true` 時，傳回空結果而非權限不足錯誤。失敗則會改為儲存在應用程式記錄檔中。 |
| `do_not_fail_on_forbidden_empty` | 布林值 | 類似於 `do_not_fail_on_forbidden`，但對空結果有特定行為。 |
| `filtered_alias_mode` | 字串 | 控制文件欄位篩選如何套用至別名。 |
| `hosts_resolver_mode` | 字串 | 決定安全性作業如何執行主機名稱解析。 |
| `http` | 物件 | HTTP 特定的安全性組態。 |
| `on_behalf_of` | 物件 | 為使用者的工作階段期間設定暫時存取權杖 (進階)。 |
| `kibana` | 物件 | OpenSearch Dashboards 整合的組態。 |
| `respect_request_indices_options` | 布林值 | 當 `true` 時，會遵循請求中指定的索引選項。 |

</details>

## 範例請求

```json
PUT /_plugins/_security/api/securityconfig/config
{
  "dynamic": {
    "api_tokens": {
      "enabled": false,
      "max_duration_seconds": 7776000,
      "max_tokens": 100
    },
    "auth_failure_listeners": {},
    "authc": {
      "jwt_auth_domain": {
        "authentication_backend": {
          "config": {},
          "type": "noop"
        },
        "description": "Authenticate via Json Web Token",
        "http_authenticator": {
          "challenge": false,
          "config": {
            "jwks_uri": "https://your-jwks-endpoint.com/.well-known/jwks.json",
            "signing_key": "base64 encoded HMAC key or public RSA/ECDSA pem key",
            "jwt_header": "Authorization",
            "jwt_clock_skew_tolerance_seconds": 30
          },
          "type": "jwt"
        },
        "http_enabled": false,
        "order": 0
      },
      "ldap": {
        "authentication_backend": {
          "config": {
            "enable_ssl": false,
            "enable_start_tls": false,
            "enable_ssl_client_auth": false,
            "verify_hostnames": true,
            "hosts": [
              "localhost:8389"
            ],
            "userbase": "ou=people,dc=example,dc=com",
            "usersearch": "(sAMAccountName={0})"
          },
          "type": "ldap"
        },
        "description": "Authenticate via LDAP or Active Directory",
        "http_authenticator": {
          "challenge": false,
          "config": {},
          "type": "basic"
        },
        "http_enabled": false,
        "order": 5
      },
      "basic_internal_auth_domain": {
        "authentication_backend": {
          "config": {},
          "type": "intern"
        },
        "description": "Authenticate via HTTP Basic against internal users database",
        "http_authenticator": {
          "challenge": true,
          "config": {},
          "type": "basic"
        },
        "http_enabled": true,
        "order": 4
      },
      "proxy_auth_domain": {
        "authentication_backend": {
          "config": {},
          "type": "noop"
        },
        "description": "Authenticate via proxy",
        "http_authenticator": {
          "challenge": false,
          "config": {
            "user_header": "x-proxy-user",
            "roles_header": "x-proxy-roles"
          },
          "type": "proxy"
        },
        "http_enabled": false,
        "order": 3
      },
      "clientcert_auth_domain": {
        "authentication_backend": {
          "config": {},
          "type": "noop"
        },
        "description": "Authenticate via SSL client certificates",
        "http_authenticator": {
          "challenge": false,
          "config": {
            "username_attribute": "cn"
          },
          "type": "clientcert"
        },
        "http_enabled": false,
        "order": 2
      },
      "kerberos_auth_domain": {
        "authentication_backend": {
          "config": {},
          "type": "noop"
        },
        "http_authenticator": {
          "challenge": true,
          "config": {
            "krb_debug": false,
            "strip_realm_from_principal": true
          },
          "type": "kerberos"
        },
        "http_enabled": false,
        "order": 6
      }
    },
    "authz": {
      "roles_from_another_ldap": {
        "authorization_backend": {
          "config": {},
          "type": "ldap"
        },
        "description": "Authorize via another Active Directory",
        "http_enabled": false
      },
      "roles_from_myldap": {
        "authorization_backend": {
          "config": {
            "enable_ssl": false,
            "enable_start_tls": false,
            "enable_ssl_client_auth": false,
            "verify_hostnames": true,
            "hosts": [
              "localhost:8389"
            ],
            "rolebase": "ou=groups,dc=example,dc=com",
            "rolesearch": "(member={0})",
            "userrolename": "disabled",
            "rolename": "cn",
            "resolve_nested_roles": true,
            "userbase": "ou=people,dc=example,dc=com",
            "usersearch": "(uid={0})"
          },
          "type": "ldap"
        },
        "description": "Authorize via LDAP or Active Directory",
        "http_enabled": false
      }
    },
    "disable_intertransport_auth": false,
    "disable_rest_auth": false,
    "do_not_fail_on_forbidden": false,
    "do_not_fail_on_forbidden_empty": false,
    "filtered_alias_mode": "warn",
    "hosts_resolver_mode": "ip-only",
    "http": {
      "anonymous_auth_enabled": false,
      "xff": {
        "enabled": false,
        "internalProxies": "192\\.168\\.0\\.10|192\\.168\\.0\\.11",
        "remoteIpHeader": "X-Forwarded-For"
      }
    },
    "kibana": {
      "default_tenant": "Global",
      "index": ".kibana",
      "multitenancy_enabled": true,
      "preferred_tenants": [],
      "private_tenant_enabled": true,
      "server_username": "kibanaserver"
    },
    "multi_rolespan_enabled": true,
    "on_behalf_of": {
      "enabled": true,
      "encryption_key": "mT9vgsqzrg9K52mtqDONUtnLufJw8eo0fjw2kvBdn3k=",
      "signing_key": "dCjVPWyFp5SEIWLOKC5DK5/8F5n/8/QoUWr+5b+yozIsISR9U3pqaA6F23HtDqF768GQA7r9RRtIh1R6ihot3A=="
    },
    "privileges_evaluation_ignore_unauthorized_indices": true,
    "respect_request_indices_options": false
  }
}
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "status": "OK",
  "message": "'config' updated."
}
```

## 回應本文欄位

回應本文為包含下列欄位的 JSON 物件。

| 屬性 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `status` | 字串 | 請求的狀態。成功的請求會傳回「OK」。 |
| `message` | 字串 | 描述作業結果的訊息。 |

## 使用注意事項

此 API 會直接修改安全性外掛程式的核心組態，因此具有下列風險：

- 在多數情況下，請使用 `securityadmin.sh` 指令碼，其中包含可避免組態錯誤的驗證與防護機制。
- 進行變更前，請先備份您目前的安全性組態。
- 僅將此 API 的存取權授予受信任的管理員。一個請求就可能停用整個叢集的安全性組態。
- 將安全性組態變更部署至正式環境前，請先在開發環境中測試。
- 提供完整的組態。部分更新會取代整個組態。
- 此 API 僅執行最少的驗證，因此不正確的組態可能要到造成作業問題時才會被發現。

## 啟用此 API

基於安全性理由，此 API 預設為停用。若要啟用，請將下列這一行新增至 `opensearch.yml`：

```yml
plugins.security.unsupported.restapi.allow_securityconfig_modification: true
```
{% include copy.html %}

如需授予安全性 API 存取權的詳細資訊，請參閱 [API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
