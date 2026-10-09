---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "憑證 API"
parent: Security APIs
nav_order: 140
has_children: true
has_toc: false
redirect_from:
  - /security/api/certificates/
---

# 憑證 API

憑證 API 會傳回叢集上正在使用的憑證，並可在不重新啟動節點的情況下重新載入這些憑證。

OpenSearch 支援下列憑證 API。

| API | 說明 |
| :--- | :--- |
| [Get Certificates API]({{site.url}}{{site.baseurl}}/security/api/certificates/get-certificates/) | 傳回接收請求之節點上正在使用的 HTTP 與傳輸憑證。 |
| [Get All Certificates API]({{site.url}}{{site.baseurl}}/security/api/certificates/get-all-certificates/) | 傳回叢集中每個節點上正在使用的憑證。 |
| [Get Node Certificates API]({{site.url}}{{site.baseurl}}/security/api/certificates/get-node-certificates/) | 傳回指定節點上正在使用的憑證。 |
| [Reload Transport Certificates API]({{site.url}}{{site.baseurl}}/security/api/certificates/reload-transport-certificates/) | 在不重新啟動節點的情況下重新載入傳輸層憑證。 |
| [Reload HTTP Certificates API]({{site.url}}{{site.baseurl}}/security/api/certificates/reload-http-certificates/) | 在不重新啟動節點的情況下重新載入 HTTP 層憑證。 |

## 必要權限

憑證 API 僅限超級管理員使用。僅對應至 `plugins.security.restapi.roles_enabled` 中所列的角色並不足夠：具有 `all_access` 角色的使用者會收到 `403 Forbidden`。若要呼叫這些 API，請使用下列其中一種方法：

- 使用管理員憑證進行驗證。如需詳細資訊，請參閱[設定管理員憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/#configuring-admin-certificates)。
- 授予角色下列其中一項叢集權限，並在 `opensearch.yml` 中將 `plugins.security.restapi.admin.enabled` 設定為 `true`。這些權限是獨立授予的，因此該角色不需要同時列於 `plugins.security.restapi.roles_enabled` 中。

| 操作 | 必要權限 |
| :--- | :--- |
| 擷取憑證 | `restapi:admin/ssl/certs/info` |
| 重新載入憑證 | `restapi:admin/ssl/certs/reload` |

保留的 `security_rest_api_full_access` 角色包含這兩項權限。包含任何 `restapi:admin` 權限的角色無法透過 [Role API]({{site.url}}{{site.baseurl}}/security/api/roles/) 建立或修改，因此請在 `roles.yml` 中定義您自己的此類角色，並使用 `securityadmin.sh` 套用。如需詳細資訊，請參閱[套用組態檔案的變更]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)。

若要禁止某個角色使用這些 API，請使用 `plugins.security.restapi.endpoints_disabled` 為該角色停用 `SSL` 端點。
