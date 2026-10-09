---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "警示安全性"
nav_order: 10
parent: Alerting
has_children: false
redirect_from:
  - /monitoring-plugins/alerting/security/
---

# 警示安全性

如果您同時使用 Security 外掛程式與警示功能，您可能會想將特定使用者限制為特定動作。例如，您可能會想讓某些使用者只能檢視和確認警示，而其他使用者則可以修改監視器和目的地。

## 基本權限

Security 外掛程式有三個內建角色，涵蓋大多數警示使用案例：`alerting_read_access`、`alerting_ack_alerts` 和 `alerting_full_access`。如需各角色的說明，請參閱[預先定義的角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles#predefined-roles)。

如果這些角色不符合您的需求，您可以混合搭配個別的警示[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)以符合您的使用案例。每個動作都對應 REST API 中的一項操作。例如，`cluster:admin/opensearch/alerting/destination/delete` 權限可讓您刪除目的地。

## 監視器如何存取資料

監視器會以建立或上次修改該監視器的使用者權限來執行。例如，假設有位使用者 `jdoe` 在一間連鎖零售商店工作。`jdoe` 有兩個角色。這兩個角色合起來可允許讀取三個索引：`store1-returns`、`store2-returns` 和 `store3-returns`。

`jdoe` 建立了一個監視器，當這三個索引的退貨總數每小時超過 40 筆時，就會傳送電子郵件給管理階層。

後來，使用者 `psantos` 想要編輯該監視器，讓它每兩小時執行一次，但 `psantos` 只能存取 `store1-returns`。若要進行這項變更，`psantos` 有兩個選項：

- 更新監視器，讓它只檢查 `store1-returns`。
- 向管理員要求其他兩個索引的讀取權限。

進行變更後，監視器現在會以與 `psantos` 相同的權限執行，包括任何[文件層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/document-level-security/)查詢、[排除的欄位]({{site.url}}{{site.baseurl}}/security/access-control/field-level-security/)和[遮蔽的欄位]({{site.url}}{{site.baseurl}}/security/access-control/field-masking/)。如果您使用擷取查詢來定義監視器，請使用 **Run** 按鈕以確保回應包含您需要的欄位。

一旦建立監視器，即使建立該監視器的使用者權限遭到移除，Alerting 外掛程式仍會繼續執行該監視器。只有具備正確叢集權限的使用者才能手動停用或刪除監視器，以停止其執行：

- 停用監視器：`cluster:admin/opendistro/alerting/monitor/write`
- 刪除監視器：`cluster:admin/opendistro/alerting/monitor/delete`

如果您的監視器觸發程序已設定通知，無論目的地類型為何，Alerting 外掛程式都會繼續傳送通知。若要停止通知，使用者必須在觸發程序的動作中手動刪除這些通知。

### 關於警示與精細存取控制的注意事項

當觸發程序產生警示時，監視器組態、警示本身，以及傳送至頻道的任何通知，都可能包含描述所查詢索引的中繼資料。根據設計，此外掛程式必須擷取資料並將其儲存為索引外的中繼資料。[文件層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/document-level-security/) (DLS) 和[欄位層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/field-level-security/) (FLS) 存取控制旨在保護索引中的資料。但一旦資料以中繼資料的形式儲存在索引之外，能夠存取監視器組態、警示及其通知的使用者就能檢視這些中繼資料，並可能推斷索引中資料的內容與品質，而這些資料原本會受到 DLS 和 FLS 存取控制的保護。

為降低非預期使用者檢視可能描述索引之中繼資料的機會，我們建議管理員啟用以角色為基礎的存取控制，並在將權限指派給目標使用者群組時，將這類設計要素納入考量。詳情請參閱[依後端角色限制存取](#advanced-limit-access-by-backend-role)。

## (進階) 依後端角色限制存取

Alerting 外掛程式預設沒有所有權的概念。例如，如果您有 `cluster:admin/opensearch/alerting/monitor/write` 權限，您就可以編輯*所有*監視器，無論您是否為建立者。如果是由少數受信任的使用者管理您的監視器和目的地，這種缺乏所有權的設計通常不成問題。較大型的組織可能需要依後端角色來區隔存取權。

首先，請確認您的使用者具備適當的[後端角色]({{site.url}}{{site.baseurl}}/security/access-control/index/)。後端角色通常來自 [LDAP 伺服器]({{site.url}}{{site.baseurl}}/security/configuration/ldap/)或 [SAML 提供者]({{site.url}}{{site.baseurl}}/security/configuration/saml/)。不過，如果您使用內部使用者資料庫，則可以使用 REST API，透過建立使用者操作來手動新增這些角色。若要將後端角色新增至建立使用者請求，請依照 Security 外掛程式 API 文件中的[建立使用者]({{site.url}}{{site.baseurl}}/security/api/users/create-user/)指示操作。

接著，啟用下列設定：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.alerting.filter_by_backend_roles": "true"
  }
}
```

現在，當使用者在 OpenSearch Dashboards 中檢視警示資源 (或進行 REST API 呼叫) 時，他們只會看到由*至少共用一個*後端角色的使用者所建立的監視器和目的地。例如，假設有三位都擁有警示完整存取權的使用者：`jdoe`、`jroe` 和 `psantos`。

`jdoe` 和 `jroe` 在工作上屬於同一個團隊，且都擁有 `analyst` 後端角色。`psantos` 則擁有 `human-resources` 後端角色。

如果 `jdoe` 建立了監視器，`jroe` 可以檢視和修改它，但 `psantos` 不行。如果該監視器產生了警示，情況也相同：`jroe` 可以檢視和確認它，但 `psantos` 不行。如果 `psantos` 建立了目的地，`jdoe` 和 `jroe` 都無法檢視或修改它。

### 設定後端角色存取權

`plugins.alerting.filter_by_backend_roles_access_strategy` 設定可控制如何將使用者的後端角色與監視器相關聯的後端角色進行比較，以判斷該使用者是否可以存取該監視器。

此設定支援下列值：

- `intersect` (預設) -- 如果使用者與建立物件之使用者至少共用一個後端角色，則可存取通知物件。
- `exact` -- 如果使用者的後端角色與建立物件之使用者的後端角色完全相同 (沒有額外角色)，則可存取通知物件。
- `all` -- 如果使用者的後端角色包含建立物件之使用者的所有後端角色，則可存取通知物件。

下列範例使用一個與 `analyst` 和 `human-resources` 後端角色相關聯的監視器，以及四位具有不同後端角色的使用者：

- 使用者 `jdoe` 具有後端角色 `analyst`。
- 使用者 `jroe` 具有後端角色 `analyst` 和 `supervisor`。
- 使用者 `psantos` 具有後端角色 `analyst` 和 `human-resources`。
- 使用者 `bwayne` 具有後端角色 `analyst`、`human-resources` 和 `batman`。

下表顯示每個使用者在各設定值下是否可以存取該監視器。

| 使用者 | `intersect` | `exact` | `all`
:-- | :-- | :-- | :--
`jdoe` | 可存取 | 無法存取 | 無法存取
`jroe` | 可存取 | 無法存取 | 無法存取
`psantos` | 可存取 | 可存取 | 可存取
`bwayne` | 可存取 | 無法存取 | 可存取

<!-- ## (Advanced) Limit access by individual

If you only want users to be able to see and modify their own monitors and destinations, duplicate the `alerting_full_access` role and add the following [DLS query]({{site.url}}{{site.baseurl}}/security/access-control/document-level-security/) to it:

```json
{
  "bool": {
    "should": [{
      "match": {
        "monitor.created_by": "${user.name}"
      }
    }, {
      "match": {
        "destination.created_by": "${user.name}"
      }
    }]
  }
}
```

Then, use this new role for all alerting users. -->

### 指定 RBAC 後端角色

您可以在使用 Alerting API 建立或更新監視器時，指定以角色為基礎的存取控制 (RBAC) 後端角色。

在建立監視器的情境中，請依照下列準則指定角色：

使用者類型  | 角色是否由使用者指定 (Y/N) | 如何使用 RBAC 角色
:--- | :--- | :---
管理員使用者 | 是 | 使用所有指定的後端角色來關聯至監視器。
一般使用者 | 是 | 從該使用者有權限使用的後端角色清單中，使用所有指定的後端角色來關聯至監視器。
一般使用者 | 否 | 複製使用者的後端角色並將其關聯至監視器。

在更新監視器的情境中，請依照下列準則指定角色：

使用者類型  | 角色是否由使用者指定 (Y/N) | 如何使用 RBAC 角色
:--- | :--- | :---
管理員使用者 | 是 | 移除所有關聯至監視器的後端角色，然後使用所有指定且關聯至監視器的後端角色。
一般使用者 | 是 | 移除該使用者有權存取但未指定、且已關聯至監視器的後端角色。然後從該使用者有權限使用的後端角色清單中，將所有其他指定的後端角色新增至監視器。
一般使用者 | 否 | 不要更新監視器上的後端角色。

- 對於管理員使用者，空清單視為等同於移除該使用者擁有的所有權限。如果非管理員使用者傳入空清單，將會擲回例外狀況，因為非管理員使用者不允許這麼做。
- 如果使用者嘗試關聯他們沒有權限使用的角色，將會擲回例外狀況。
{: .note }

若要建立 RBAC 角色，請依照 Security 外掛程式 API 文件中的指示[建立角色]({{site.url}}{{site.baseurl}}/security/api/roles/create-role/)。

### 建立具有 RBAC 角色的監視器

當您使用 Alerting API 建立監視器時，您可以在請求本文底部指定 RBAC 角色。請使用 `rbac_roles` 參數。

下列範例顯示由 RBAC 參數指定的 RBAC 角色：

```json
...
  "rbac_roles": ["role1", "role2"]
}
```

若要查看完整的請求範例，請參閱[建立查詢層級監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/api/#create-a-query-level-monitor)。
