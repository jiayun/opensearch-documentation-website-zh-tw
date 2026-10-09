---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得組態"
parent: Security configuration APIs
grand_parent: Security APIs
nav_order: 30
redirect_from:
  - /api-reference/security/configuration/get-configuration/
---

# 取得安全性組態 API
**於 2.10 版導入**
{: .label .label-purple }

Get Configuration API 會擷取目前的安全性組態。此組態包含驗證網域與其他安全性相關的組態。

<!-- spec_insert_start
api: security.get_configuration
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/securityconfig
```
<!-- spec_insert_end -->

## 範例請求

```json
GET /_plugins/_security/api/securityconfig
```
{% include copy-curl.html security=true %}

## 範例回應

回應在此經過刪節：

```json
{
  "config": {
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
}
```

## 回應本文欄位

回應本文是一個包含下列欄位的 JSON 物件。

| 屬性 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `config` | 物件 | 包含安全性組態的根物件。 |

<details markdown="block">
  <summary>
    回應本文欄位：<code>config</code>
  </summary>
  {: .text-delta}

`config` 是一個包含下列欄位的 JSON 物件。

| 屬性 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `dynamic` | 物件 | 包含所有安全性組態設定的主要組態物件。包括驗證網域 (`authc`)、授權設定 (`authz`) 以及各種安全性行為。 |

</details>

## 使用說明
