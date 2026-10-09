---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "辨別名稱 API"
parent: Security APIs
nav_order: 130
has_children: true
has_toc: false
redirect_from:
  - /security/api/distinguished-names/
---

# 辨別名稱 API

辨別名稱 API 可讓超級管理員（或具有足夠權限可存取這些 API 的使用者）在允許清單中新增、擷取、更新或刪除任何辨別名稱，以啟用叢集或節點之間的通訊。

在您可以使用這些 API 設定允許清單之前，必須將下列這一行新增至 `opensearch.yml`：

```yml
plugins.security.nodes_dn_dynamic_config_enabled: true
```
{% include copy.html %}

OpenSearch 支援下列辨別名稱 API。

| API | 說明 |
| :--- | :--- |
| [Create or Update Distinguished Name API]({{site.url}}{{site.baseurl}}/security/api/distinguished-names/update-distinguished-name/) | 新增或更新指定叢集或節點允許清單中的辨別名稱。 |
| [Patch Distinguished Names API]({{site.url}}{{site.baseurl}}/security/api/distinguished-names/patch-distinguished-names/) | 更新單一叢集的辨別名稱，或跨叢集進行大量更新。 |
| [Get Distinguished Names API]({{site.url}}{{site.baseurl}}/security/api/distinguished-names/get-distinguished-names/) | 擷取單一叢集或節點，或所有叢集和節點允許清單中的辨別名稱。 |
| [Delete Distinguished Name API]({{site.url}}{{site.baseurl}}/security/api/distinguished-names/delete-distinguished-name/) | 刪除指定叢集或節點允許清單中的所有辨別名稱。 |

## 必要權限

辨別名稱 API 僅限超級管理員使用。僅對應至 `plugins.security.restapi.roles_enabled` 中列出的角色並不足夠：具有 `all_access` 角色的使用者會收到 `403 Forbidden`。若要呼叫這些 API，請使用下列其中一種方式：

- 使用管理員憑證進行驗證。如需詳細資訊，請參閱[設定管理員憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/#configuring-admin-certificates)。
- 授予角色 `restapi:admin/nodesdn` 叢集權限，並在 `opensearch.yml` 中將 `plugins.security.restapi.admin.enabled` 設為 `true`。此權限為獨立授權，因此該角色不需要同時列於 `plugins.security.restapi.roles_enabled` 中。

保留的 `security_rest_api_full_access` 角色包含 `restapi:admin/nodesdn`。包含任何 `restapi:admin` 權限的角色都無法透過 [Role APIs]({{site.url}}{{site.baseurl}}/security/api/roles/) 建立或修改，因此請在 `roles.yml` 中定義您自己的此類角色，並使用 `securityadmin.sh` 套用。如需詳細資訊，請參閱[套用組態檔案的變更]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)。

若要防止角色使用這些 API，請使用 `plugins.security.restapi.endpoints_disabled` 為該角色停用 `NODESDN` 端點。
