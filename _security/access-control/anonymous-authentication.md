---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "匿名驗證"
parent: Access control
nav_order: 130
---

# 匿名驗證

Security 外掛程式支援匿名驗證，讓使用者無需提供憑證即可存取叢集。當您希望讓大量使用者以一組共同的權限存取叢集時，這項功能非常實用。

## 組態

若要啟用匿名驗證，您需要修改叢集 `opensearch-security` 組態子目錄中的 `config.yml` 檔案。

在 `config.yml` 檔案中，有一個 `http` 區段，其中包含 `anonymous_auth_enabled` 設定：

```yml
http:
  anonymous_auth_enabled: <true|false>
  ...
```

下表說明 `anonymous_auth_enabled` 設定。如需更多資訊，請參閱[組態]({{site.url}}{{site.baseurl}}/security/configuration/configuration/)檔案概觀。

| 設定 | 說明                                                                                                                                                                                                                                                                                   |
| :--- |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `anonymous_auth_enabled` | 啟用或停用匿名驗證。當您啟用匿名驗證時，所有已定義的 HTTP 驗證器都是非質詢型。請參閱[質詢設定]({{site.url}}{{site.baseurl}}/security/authentication-backends/basic-authc/#the-challenge-setting)。 |

如果您停用匿名驗證，則必須提供至少一個 `authc`，Security 外掛程式才能成功初始化。
{: .important }

## OpenSearch Dashboards 組態

若要為 OpenSearch Dashboards 啟用匿名驗證，您需要修改 OpenSearch Dashboards 安裝目錄中組態目錄內的 `opensearch_dashboards.yml` 檔案。

將以下設定加入 `opensearch_dashboards.yml`：

```yml
opensearch_security.auth.anonymous_auth_enabled: true
```

OpenSearch Dashboards 的匿名登入需要在 OpenSearch 叢集上啟用匿名驗證。
{: .important}

## 定義匿名驗證權限

啟用匿名驗證後，您定義的 HTTP 驗證器仍會嘗試在 HTTP 請求中尋找使用者憑證。如果找到憑證，該使用者就會通過驗證。如果找不到任何憑證，該使用者會以 `anonymous` 使用者的身分通過驗證。

所有匿名使用者的使用者名稱都是 `anonymous`，並且擁有一個名為 `anonymous_backendrole` 的單一角色。

您可以在 [roles.yml]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/) 檔案中設定與 `opendistro_security_anonymous_backendrole` 相關聯的權限。

我們建議您定義的角色應具有非常有限的權限。一般而言，匿名使用者**絕不**應該能夠寫入您的叢集。
{: .important}

以下是 `anonymous_users_role` 的角色定義範例。您可以將此範例作為參考，在 `roles.yml` 檔案中定義您自己的角色：

```yaml
anonymous_users_role:
  reserved: false
  hidden: false
  cluster_permissions:
  - "OPENDISTRO_SECURITY_CLUSTER_COMPOSITE_OPS"
  index_permissions:
  - index_patterns:
    - "public_index_*"
    allowed_actions:
    - "read"
```
{% include copy.html %}

接著，在 `roles_mapping.yml` 檔案中，您可以為這個新角色定義適當的對應：

```yaml
anonymous_users_role:
  reserved: false
  hidden: false
  backend_roles: ["opendistro_security_anonymous_backendrole"]
  hosts: []
```
{% include copy.html %}

請注意，該角色被對應至 `opendistro_security_anonymous_backendrole`，這表示所有具有匿名使用者後端角色的使用者都將擁有這些權限。

或者，您也可以使用 REST API 或 OpenSearch Dashboards 完成這些步驟。 

