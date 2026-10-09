---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "可觀測性安全性"
nav_order: 160
has_children: false
redirect_from:
  - /observing-your-data/security/
---

# 可觀測性安全性

您可以在 OpenSearch 中將 Security 外掛程式與可觀測性功能搭配使用，以限制非管理員使用者只能執行特定動作。例如，您可能希望某些使用者只能檢視視覺化、筆記本及其他可觀測性物件，而其他使用者則可以建立和修改這些物件。

## 基本權限

Security 外掛程式內建兩個涵蓋大多數可觀測性使用案例的角色：`observability_full_access` 和 `observability_read_access`。各角色的說明請參閱 [預先定義的角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles#predefined-roles)。如果您在 OpenSearch Dashboards 中看不到這些預先定義的角色，可以使用下列命令建立：

```json
PUT _plugins/_security/api/roles/observability_read_access
{
  "cluster_permissions": [
    "cluster:admin/opensearch/observability/get"
  ]
}
```

```json
PUT _plugins/_security/api/roles/observability_full_access
{
  "cluster_permissions": [
    "cluster:admin/opensearch/observability/*"
  ]
}
```

如果這些角色不符合您的需求，可以依據您的使用案例混合搭配個別的可觀測性 [權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)。例如，`cluster:admin/opensearch/observability/create` 權限可讓您建立可觀測性物件（視覺化、營運面板和筆記本）。

以下是一個提供可觀測性存取權的角色範例：

```json
PUT _plugins/_security/api/roles/observability_permissions
{
  "cluster_permissions": [
    "cluster:admin/opensearch/observability/create",
    "cluster:admin/opensearch/observability/update",
    "cluster:admin/opensearch/observability/delete",
    "cluster:admin/opensearch/observability/get"
    ],
  "index_permissions": [{
    "index_patterns": [".opensearch-observability"],
    "allowed_actions": ["write", "read", "search"]
  }],
  "tenant_permissions": [{
    "tenant_patterns": ["global_tenant"],
    "allowed_actions": ["opensearch_dashboards_all_write"]
  }]
}
```
