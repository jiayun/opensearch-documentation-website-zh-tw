---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "異常偵測安全性"
nav_order: 10
parent: Anomaly detection
has_children: false
redirect_from: 
  - /monitoring-plugins/ad/security/
---

# 異常偵測安全性

您可以在 OpenSearch 中搭配異常偵測使用 Security 外掛程式，將非管理員使用者限制為特定動作。例如，您可能會希望某些使用者只能建立、更新或刪除偵測器，而其他使用者只能檢視偵測器。

所有異常偵測索引都會受到保護，做為系統索引。只有超級管理員使用者，或具有 TLS 憑證的管理員使用者，才能存取系統索引。如需詳細資訊，請參閱[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)。


異常偵測的安全性運作方式與[警示的安全性]({{site.url}}{{site.baseurl}}/monitoring-plugins/alerting/security/)相同。

## 基本權限

身為管理員使用者，您可以根據使用者需要存取哪些 API，使用 Security 外掛程式指派特定權限給他們。如需支援的 API 清單，請參閱[異常偵測 API]({{site.url}}{{site.baseurl}}/monitoring-plugins/ad/api/)。

Security 外掛程式有兩個內建角色，涵蓋大多數異常偵測使用案例：`anomaly_full_access` 和 `anomaly_read_access`。如需各角色的說明，請參閱[預先定義的角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles#predefined-roles)。

如果您使用 OpenSearch Dashboards 建立異常偵測器，即使具有 `anomaly_full_access`，仍可能會遇到存取問題。此問題已在 OpenSearch 2.17 中解決，但若為較早的版本，則需要新增下列額外權限：

- `indices:data/read/search` -- 您需要此權限，因為 Anomaly Detection 外掛程式需要搜尋資料來源，以驗證是否有足夠的資料可訓練模型。
- `indices:admin/mappings/fields/get` 和 `indices:admin/mappings/fields/get*` -- 您需要這些權限，以驗證指定的資料來源是否具有有效的時間戳記欄位和類別欄位 (在建立高基數偵測器的情況下)。

如果這些角色不符合您的需求，您可以混合搭配個別的異常偵測[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)以符合您的使用案例。每個動作都對應 REST API 中的一項操作。例如，`cluster:admin/opensearch/ad/detector/delete` 權限可讓您刪除偵測器。

### 關於警示與精細存取控制的注意事項

當觸發條件產生警示時，偵測器和監視器組態、警示本身，以及傳送至頻道的任何通知，都可能包含描述所查詢索引的中繼資料。依設計，此外掛程式必須擷取資料，並將其儲存為索引外的中繼資料。[文件層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/document-level-security/) (DLS) 和[欄位層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/field-level-security/) (FLS) 存取控制旨在保護索引中的資料。但一旦資料以中繼資料形式儲存在索引外，有權存取偵測器和監視器組態、警示及其通知的使用者，就能檢視此中繼資料，並可能推斷索引中資料的內容和品質，而這些資料原本會受到 DLS 和 FLS 存取控制的保護。

為降低非預期使用者檢視可能描述索引之中繼資料的機會，我們建議管理員啟用以角色為基礎的存取控制，並在將權限指派給目標使用者群組時，將這類設計要素納入考量。如需詳細資訊，請參閱[依後端角色限制存取](#advanced-limit-access-by-backend-role)。

### 使用精細存取控制選取遠端索引

若要使用遠端索引做為偵測器的資料來源，請參閱[跨叢集搜尋]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/)中[驗證流程]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/#authentication-flow)的設定步驟。您必須使用同時存在於遠端和本機叢集中的角色。遠端叢集必須將所選角色對應至與本機叢集中相同的使用者名稱。

---

#### 範例：在本機叢集上建立新使用者

1. 在本機叢集上建立新使用者，以供建立偵測器使用：

```
curl -XPUT -k -u 'admin:<custom-admin-password>' 'https://localhost:9200/_plugins/_security/api/internalusers/anomalyuser' -H 'Content-Type: application/json' -d '{"password":"password"}'
```
{% include copy.html %}

2. 將新使用者對應至 `anomaly_full_access` 角色：

```
curl -XPUT -k -u 'admin:<custom-admin-password>' -H 'Content-Type: application/json' 'https://localhost:9200/_plugins/_security/api/rolesmapping/anomaly_full_access' -d '{"users" : ["anomalyuser"]}'
```
{% include copy.html %}

3. 在遠端叢集上，建立相同的使用者，並將 `anomaly_full_access` 對應至該角色：

```
curl -XPUT -k -u 'admin:<custom-admin-password>' 'https://localhost:9250/_plugins/_security/api/internalusers/anomalyuser' -H 'Content-Type: application/json' -d '{"password":"password"}'
curl -XPUT -k -u 'admin:<custom-admin-password>' -H 'Content-Type: application/json' 'https://localhost:9250/_plugins/_security/api/rolesmapping/anomaly_full_access' -d '{"users" : ["anomalyuser"]}'
```
{% include copy.html %}

---

### 自訂結果索引

若要使用自訂結果索引，您需要 OpenSearch Security 外掛程式所提供預設角色中未包含的額外權限。若要新增這些權限，請參閱[異常偵測]({{site.url}}{{site.baseurl}}/observing-your-data/ad/index/)文件中的[步驟 1：定義偵測器]({{site.url}}{{site.baseurl}}/observing-your-data/ad/index/#step-1-define-a-detector)。

## (進階) 依後端角色限制存取

使用後端角色，根據角色設定個別偵測器的精細存取權。例如，組織中不同部門的使用者可以檢視自己部門所擁有的偵測器。

首先，請確認您的使用者具有適當的[後端角色]({{site.url}}{{site.baseurl}}/security/access-control/index/)。後端角色通常來自 [LDAP 伺服器]({{site.url}}{{site.baseurl}}/security/configuration/ldap/)或 [SAML 提供者]({{site.url}}{{site.baseurl}}/security/configuration/saml/)，但如果您使用內部使用者資料庫，則可以使用 REST API [手動新增它們]({{site.url}}{{site.baseurl}}/security/api/users/create-user/)。

接著，啟用下列設定：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.anomaly_detection.filter_by_backend_roles": "true"
  }
}
```

現在，當使用者在 OpenSearch Dashboards 中檢視異常偵測資源 (或進行 REST API 呼叫) 時，他們只會看到由至少共用一個後端角色的使用者所建立的偵測器。
例如，假設有兩個使用者：`alice` 和 `bob`。

`alice` 具有 analyst 後端角色：

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

`bob` 具有 human-resources 後端角色：

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

`alice` 和 `bob` 都擁有異常偵測的完整存取權：

```json
PUT _plugins/_security/api/rolesmapping/anomaly_full_access
{
  "backend_roles": [],
  "hosts": [],
  "users": [
    "alice",
    "bob"
  ]
}
```

由於他們具有不同的後端角色，`alice` 和 `bob` 無法檢視彼此的偵測器或其結果。

如果使用者沒有後端角色，只要他們具有 `anomaly_read_access`，仍然可以檢視其他使用者的異常偵測結果。具有 `anomaly_full_access` 的使用者也是如此，因為它包含與 `anomaly_read_access` 相同的所有權限。管理員應告知使用者，具有 `anomaly_read_access` 可檢視叢集中任何偵測器的結果，包括他們無法直接存取的資料。若要限制偵測器結果的存取，管理員應在建立偵測器時使用後端角色篩選條件。這可確保只有具有相符後端角色的使用者，才能存取這些特定偵測器的結果。