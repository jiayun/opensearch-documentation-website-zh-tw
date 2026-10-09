---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引管理安全性"
nav_order: 90
has_children: false
---

# 索引管理安全性

搭配使用 Security 外掛程式與索引管理，可讓您將非管理員使用者限制於特定動作。例如，您可能希望設定安全性，讓某群使用者只能讀取 ISM 政策，而其他使用者可以建立、刪除或變更政策。

所有索引管理資料都以系統索引的形式受到保護，只有超級管理員或持有傳輸層安全性 (TLS) 憑證的管理員才能存取系統索引。如需更多資訊，請參閱 [系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)。

## 基本權限

Security 外掛程式內建一個提供索引管理完整存取權的角色：`index_management_full_access`。有關該角色權限的說明，請參閱 [預先定義的角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles#predefined-roles)。

啟用安全性後，使用者不僅需要正確的索引管理權限，還需要對相關索引執行動作的權限。例如，如果使用者想使用 REST API 將執行 rollup 工作的政策附加到名為 `system-logs` 的索引，則需要附加政策與執行 rollup 工作的權限，以及對 `system-logs` 的存取權。

最後，除了 Create Policy、Get Policy 與 Delete Policy 之外，使用者還需要 `indices:admin/opensearch/ism/managedindex` 權限才能執行 [ISM APIs]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/)。

## (進階) 依後端角色限制存取

您可以使用後端角色來設定對索引管理政策與動作的細微存取控制。例如，組織中不同部門的使用者，可能會依據被指派的角色與權限而看到不同的政策。

首先，請確保您的使用者具有適當的[後端角色]({{site.url}}{{site.baseurl}}/security/access-control/index/)。後端角色通常來自 [LDAP 伺服器]({{site.url}}{{site.baseurl}}/security/configuration/ldap/)或 [SAML 提供者]({{site.url}}{{site.baseurl}}/security/configuration/saml/)。不過，如果您使用內部使用者資料庫，可以使用 REST API [手動新增]({{site.url}}{{site.baseurl}}/security/api/users/create-user/)。

使用 REST API 啟用以下設定：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.index_management.filter_by_backend_roles": "true"
  }
}
```
{% include copy-curl.html %}

請只在已啟用 Security 外掛程式的叢集上啟用此設定。在停用安全性的叢集上，該設定會被接受，但之後每個索引管理寫入請求都會失敗並傳回 `403 Filter by user backend roles in IndexManagement is not supported with security disabled`。
{: .warning}

啟用安全性後，只有共用至少一個後端角色的使用者，才能查看並執行與其角色相關的政策與動作。

例如，考慮一個包含三位使用者的情境：`John` 與 `Jill` 擁有後端角色 `helpdesk_staff`，而 `Jane` 擁有後端角色 `phone_operator`。`John` 想建立一個在名為 `airline_data` 的索引上執行 rollup 工作的政策，因此 `John` 需要一個具有存取該索引、建立相關政策並執行相關動作權限的後端角色，而 `Jill` 將能夠存取相同的索引、政策與工作。然而，`Jane` 無法存取或編輯這些資源或動作。
