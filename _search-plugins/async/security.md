---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "非同步搜尋安全性"
nav_order: 2
parent: Asynchronous search
grand_parent: Improving search performance
has_children: false
---

# 非同步搜尋安全性

您可以搭配非同步搜尋使用 Security 外掛程式，將非管理員使用者限制為只能執行特定動作。例如，您可能希望某些使用者只能提交或刪除非同步搜尋，而其他使用者只能檢視結果。

所有非同步搜尋索引都作為系統索引受到保護。只有超級管理員使用者或具有傳輸層安全性（TLS）憑證的管理員使用者才能存取系統索引。如需詳細資訊，請參閱[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)。

## 基本權限

身為管理員使用者，您可以使用 Security 外掛程式，根據使用者需要存取的 API 操作，為他們指派特定權限。如需支援的 API 操作清單，請參閱[非同步搜尋]({{site.url}}{{site.baseurl}}/)。

Security 外掛程式有兩個內建角色，涵蓋大多數非同步搜尋使用案例：`asynchronous_search_full_access` 和 `asynchronous_search_read_access`。如需各角色的說明，請參閱[預先定義的角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles#predefined-roles)。

如果這些角色無法滿足您的需求，請混合搭配個別非同步搜尋權限，以符合您的使用案例。每個動作都對應至 REST API 中的一項操作。例如，`cluster:admin/opensearch/asynchronous_search/delete` 權限可讓您刪除先前提交的非同步搜尋。

### 關於非同步搜尋與細緻存取控制的注意事項

依照設計，Asynchronous Search 外掛程式會從目標索引擷取資料，並將資料儲存在另一個索引中，讓具有適當權限的使用者能夠取得搜尋結果。雖然具有 `asynchronous_search_read_access` 或 `cluster:admin/opensearch/asynchronous_search/get` 權限的使用者無法提交非同步搜尋請求本身，但該使用者可以使用相關聯的搜尋 ID 取得並檢視搜尋結果。[文件層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/document-level-security/)（DLS）與[欄位層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/field-level-security/)（FLS）存取控制旨在保護目標索引中的資料。但是，一旦資料儲存在此索引之外，具有這些存取權限的使用者就能使用搜尋 ID 取得並檢視非同步搜尋結果，而這些結果可能包含原本由目標索引中的 DLS 與 FLS 存取控制隱藏的資料。

為了降低非預期使用者檢視可能揭露索引內容之搜尋結果的機會，我們建議管理員啟用以角色為基礎的存取控制，並在為預定的使用者群組指派權限時，將這類設計要素納入考量。如需詳細資訊，請參閱[依後端角色限制存取](#advanced-limit-access-by-backend-role)。

## （進階）依後端角色限制存取

使用後端角色，根據角色設定對非同步搜尋的細緻存取權限。例如，組織中不同部門的使用者可以檢視所屬部門擁有的非同步搜尋。

首先，請確認您的使用者具有適當的[後端角色]({{site.url}}{{site.baseurl}}/security/access-control/index/)。後端角色通常來自 [LDAP 伺服器]({{site.url}}{{site.baseurl}}/security/configuration/ldap/)或 [SAML 提供者]({{site.url}}{{site.baseurl}}/security/configuration/saml/)。不過，如果您使用內部使用者資料庫，就可以使用 REST API [手動新增後端角色]({{site.url}}{{site.baseurl}}/security/api/users/create-user/)。

現在，當使用者在 OpenSearch Dashboards 中檢視非同步搜尋資源（或呼叫 REST API）時，他們只會看到由後端角色為其後端角色子集的使用者所提交的非同步搜尋。
例如，假設有兩位使用者：`judy` 和 `elon`。

`judy` 具有 IT 後端角色：

```json
PUT _plugins/_security/api/internalusers/judy
{
  "password": "judy",
  "backend_roles": [
    "IT"
  ],
  "attributes": {}
}
```

`elon` 具有 admin 後端角色：

```json
PUT _plugins/_security/api/internalusers/elon
{
  "password": "elon",
  "backend_roles": [
    "admin"
  ],
  "attributes": {}
}
```

`judy` 和 `elon` 都具有非同步搜尋的完整存取權限：

```json
PUT _plugins/_security/api/rolesmapping/async_full_access
{
  "backend_roles": [],
  "hosts": [],
  "users": [
    "judy",
    "elon"
  ]
}
```

由於他們具有不同的後端角色，`elon` 無法看到 `judy` 提交的非同步搜尋，反之亦然。

`judy` 至少需要具有涵蓋 `elon` 所有角色的超集合，才能看到 `elon` 的非同步搜尋。

例如，如果 `judy` 具有五個後端角色，而 `elon` 具有其中一個角色，則 `judy` 可以看到 `elon` 提交的非同步搜尋，但 `elon` 無法看到 `judy` 提交的非同步搜尋。這表示 `judy` 可以對 `elon` 提交的非同步搜尋執行 GET 和 DELETE 操作，但反過來則不行。

如果所有使用者都沒有任何後端角色，這三位使用者都能看到其他人的搜尋。

例如，假設有三位使用者：`judy`、`elon` 和 `jack`。

`judy`、`elon` 和 `jack` 都未設定後端角色：

```json
PUT _plugins/_security/api/internalusers/judy
{
  "password": "judy",
  "backend_roles": [],
  "attributes": {}
}
```

```json
PUT _plugins/_security/api/internalusers/elon
{
  "password": "elon",
  "backend_roles": [],
  "attributes": {}
}
```

```json
PUT _plugins/_security/api/internalusers/jack
{
  "password": "jack",
  "backend_roles": [],
  "attributes": {}
}
```

`judy` 和 `elon` 都具有非同步搜尋的完整存取權限：

```json
PUT _plugins/_security/api/rolesmapping/async_full_access
{
  "backend_roles": [],
  "hosts": [],
  "users": ["judy","elon"]
}
```

`jack` 具有非同步搜尋結果的讀取權限：

```json
PUT _plugins/_security/api/rolesmapping/async_read_access
{
  "backend_roles": [],
  "hosts": [],
  "users": ["jack"]
}
```

由於所有使用者都沒有後端角色，他們可以看到彼此的非同步搜尋。因此，如果 `judy` 提交非同步搜尋，具有完整存取權限的 `elon` 就能看到該搜尋。具有讀取權限的 `jack` 也能看到 `judy` 的非同步搜尋。