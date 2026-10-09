---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "允許清單 API"
parent: Security APIs
nav_order: 100
has_children: true
has_toc: false
redirect_from:
  - /security/api/allowlist/
---

# 允許清單 API

允許清單 API 可控制不具管理員權限的使用者可以存取哪些 API。

OpenSearch 支援下列允許清單 API。

| API | 說明 |
| :--- | :--- |
| [建立或更新允許清單 API]({{site.url}}{{site.baseurl}}/security/api/allowlist/create-allowlist/) | 建立或取代允許清單組態。 |
| [修補允許清單 API]({{site.url}}{{site.baseurl}}/security/api/allowlist/patch-allowlist/) | 更新允許清單組態中的個別欄位。 |
| [取得允許清單 API]({{site.url}}{{site.baseurl}}/security/api/allowlist/get-allowlist/) | 擷取目前的允許清單組態。 |

## 必要權限

允許清單 API 僅限超級管理員使用。僅對應至 `plugins.security.restapi.roles_enabled` 中列出的角色並不足夠：具有 `all_access` 角色的使用者會收到 `403 Forbidden`。若要呼叫這些 API，請使用下列其中一種方法：

- 使用管理員憑證進行驗證。如需詳細資訊，請參閱[設定管理員憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/#configuring-admin-certificates)。
- 授予角色 `restapi:admin/allowlist` 叢集權限，並在 `opensearch.yml` 中將 `plugins.security.restapi.admin.enabled` 設為 `true`。此權限是獨立授予的，因此該角色不需要同時列在 `plugins.security.restapi.roles_enabled` 中。

保留的 `security_rest_api_full_access` 角色包含 `restapi:admin/allowlist`。包含任何 `restapi:admin` 權限的角色無法透過[角色 API]({{site.url}}{{site.baseurl}}/security/api/roles/) 建立或修改，因此請在 `roles.yml` 中定義您自己的這類角色，並使用 `securityadmin.sh` 套用。如需詳細資訊，請參閱[將變更套用至組態檔案]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)。

若要防止角色使用這些 API，請使用 `plugins.security.restapi.endpoints_disabled` 為該角色停用 `ALLOWLIST` 端點。
