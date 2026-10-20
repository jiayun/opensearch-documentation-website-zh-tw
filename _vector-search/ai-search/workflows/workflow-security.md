---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作流程範本安全性"
parent: AI search workflows
grand_parent: AI search
has_children: true
nav_order: 50
redirect_from:
  - /automating-configurations/workflow-security/
---

# 工作流程範本安全性

在 OpenSearch 中，自動化工作流程組態由 Flow Framework 外掛程式提供。您可以搭配使用 Security 外掛程式與 Flow Framework 外掛程式，將非管理員使用者限制為只能執行特定動作。例如，您可能希望某些使用者只能建立、更新或刪除工作流程，而其他使用者只能檢視工作流程。

所有 Flow Framework 索引都是受保護的系統索引。只有超級管理員使用者或具有 TLS 憑證的管理員使用者才能存取系統索引。如需更多資訊，請參閱[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)。

Flow Framework 安全性的設定方式與[異常偵測的安全性]({{site.url}}{{site.baseurl}}/monitoring-plugins/ad/security/)類似。

## 基本權限

身為管理員使用者，您可以使用安全性外掛程式，依據使用者需要存取的 API，為他們指派特定權限。如需支援的 Flow Framework API 清單，請參閱[工作流程 API]({{site.url}}{{site.baseurl}}/vector-search/ai-search/workflows/api/index/)。

安全性外掛程式內建兩個角色，涵蓋大多數 Flow Framework 使用案例：`flow_framework_full_access` 和 `flow_framework_read_access`。如需各角色的說明，請參閱[預先定義的角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles#predefined-roles)。

如果這些角色不符合您的需求，您可以為使用者指派個別的 Flow Framework [權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)，以符合您的使用案例。每個動作都對應 REST API 中的一項操作。例如，`cluster:admin/opensearch/flow_framework/workflow/search` 權限可讓您搜尋工作流程。

### 細緻的存取控制

為降低非預期使用者檢視索引描述中繼資料的機會，我們建議管理員在將權限指派給預期的使用者群組時，啟用以角色為基礎的存取控制。如需更多資訊，請參閱[依後端角色限制存取](#advanced-limit-access-by-backend-role)。

## （進階）依後端角色限制存取

使用後端角色，根據角色設定個別工作流程的細微存取控制。例如，組織中不同部門的使用者可以檢視所屬部門擁有的工作流程。

首先，請確認您的使用者具有適當的[後端角色]({{site.url}}{{site.baseurl}}/security/access-control/index/)。後端角色通常來自 [LDAP 伺服器]({{site.url}}{{site.baseurl}}/security/configuration/ldap/)或 [SAML 提供者]({{site.url}}{{site.baseurl}}/security/configuration/saml/)，但如果您使用內部使用者資料庫，則可以[使用 API 手動建立使用者]({{site.url}}{{site.baseurl}}/security/api/users/create-user/)。

接著，啟用下列設定：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.flow_framework.filter_by_backend_roles": "true"
  }
}
```
{% include copy-curl.html %}

現在，當使用者在 OpenSearch Dashboards 中檢視工作流程資源（或呼叫 REST API）時，只會看到由與其至少有一個共同後端角色的使用者所建立的工作流程。

例如，假設有兩位使用者：`alice` 和 `bob`。

`alice` 具有 `analyst` 後端角色：

```json
PUT _plugins/_security/api/internalusers/alice
{
  "password": "alice",
  "backend_roles": [
    "analyst"
  ],
  "attributes": {}
}
```

`bob` 具有 `human-resources` 後端角色：

```json
PUT _plugins/_security/api/internalusers/bob
{
  "password": "bob",
  "backend_roles": [
    "human-resources"
  ],
  "attributes": {}
}
```

`alice` 和 `bob` 都具有 Flow Framework API 的完整存取權限：

```json
PUT _plugins/_security/api/rolesmapping/flow_framework_full_access
{
  "backend_roles": [],
  "hosts": [],
  "users": [
    "alice",
    "bob"
  ]
}
```

由於後端角色不同，`alice` 和 `bob` 無法檢視彼此的工作流程或其結果。

沒有後端角色的使用者，只要具有 `flow_framework_read_access`，仍可檢視其他使用者的工作流程結果。這也適用於具有 `flow_framework_full_access` 的使用者，因為此權限包含 `flow_framework_read_access` 的所有權限。 

管理員應告知使用者，`flow_framework_read_access` 權限可讓他們檢視叢集中任何工作流程的結果，包括他們無法直接存取的資料。若要限制對特定工作流程結果的存取，管理員應在建立工作流程時套用後端角色篩選條件。這可確保只有具有相符後端角色的使用者才能存取該工作流程的結果。

## 後續步驟

若要授予特定使用者、角色或後端角色存取個別工作流程的權限，請參閱[工作流程存取控制]({{site.url}}{{site.baseurl}}/vector-search/ai-search/workflows/workflow-access-control/)。
