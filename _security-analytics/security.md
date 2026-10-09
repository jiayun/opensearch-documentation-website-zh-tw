---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Security Analytics 的 OpenSearch 安全性"
nav_order: 2
has_children: false
---

<!-- vale off -->
# Security Analytics 的 OpenSearch 安全性
<!-- vale on -->

您可以搭配 Security Analytics 使用 OpenSearch 安全性，指派使用者權限，並管理使用者可以與不能執行的動作。舉例來說，您可能會希望讓某個使用者群組能夠建立、更新或刪除偵測器，而另一個使用者群組只能檢視偵測器。您可能還希望另一個群組能夠接收並確認警示，但不得執行其他工作。OpenSearch Security 架構可讓您控制使用者對 Security Analytics 功能的存取層級。

---
## Security Analytics 系統索引

Security Analytics 索引會受到保護而成為系統索引，在叢集中的處理方式與其他索引不同。系統索引會儲存組態和其他系統設定，因此無法使用 REST API 或 OpenSearch Dashboards 介面加以修改。只有具備 TLS [管理員憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/#configuring-admin-certificates)的使用者才能存取系統索引。如需使用這類索引的詳細資訊，請參閱[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)。

---
## 基本權限

身為管理員，您可以根據使用者需要存取的特定 API，使用 OpenSearch Dashboards 或 Security REST API 將特定權限指派給使用者。如需支援的 API 清單，請參閱 [API 工具]({{site.url}}{{site.baseurl}}/security-analytics/api-tools/index/)。

OpenSearch Security 有三個內建角色，涵蓋大多數 Security Analytics 使用案例：`security_analytics_full_access`、`security_analytics_read_access` 和 `security_analytics_ack_alerts`。如需這些角色和其他角色的說明，請參閱[預先定義的角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles#predefined-roles)。

如果這些角色不符合您的需求，您可以混合搭配個別的 Security Analytics [權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/#security-analytics-permissions)以符合您的使用案例。每個動作都對應 REST API 中的一項操作。舉例來說，`cluster:admin/opensearch/securityanalytics/detector/delete` 權限可讓您刪除偵測器。

---
## (進階) 依後端角色限制存取

您可以使用後端角色，根據角色設定個別偵測器的精細存取權。舉例來說，您可以將後端角色指派給在組織不同部門工作的使用者，讓他們只能檢視其所屬部門擁有的偵測器。

首先，請確認您的使用者具備適當的[後端角色]({{site.url}}{{site.baseurl}}/security/access-control/index/)。後端角色通常來自 [LDAP 伺服器]({{site.url}}{{site.baseurl}}/security/configuration/ldap/)或 [SAML 提供者]({{site.url}}{{site.baseurl}}/security/configuration/saml/)。不過，如果您使用內部使用者資料庫，則可以使用 REST API [手動新增這些角色]({{site.url}}{{site.baseurl}}/security/api/users/create-user/)。

接著，啟用下列設定：

```json
PUT /_cluster/settings
{
  "transient": {
    "plugins.security_analytics.filter_by_backend_roles": "true"
  }
}
```
{% include copy-curl.html %}

現在，當使用者在 OpenSearch Dashboards 中檢視 Security Analytics 資源 (或進行 REST API 呼叫) 時，他們只會看到由至少共用一個後端角色的使用者所建立的偵測器。
舉例來說，假設有兩個使用者：`alice` 和 `bob`。

下列範例會將 `analyst` 後端角色指派給使用者 `alice`：

```json
PUT /_plugins/_security/api/internalusers/alice
{
  "password": "alice",
  "backend_roles": [
    "analyst"
  ],
  "attributes": {}
}
```
{% include copy-curl.html %}

下一個範例會將 `human-resources` 後端角色指派給使用者 `bob`：

```json
PUT /_plugins/_security/api/internalusers/bob
{
  "password": "bob",
  "backend_roles": [
    "human-resources"
  ],
  "attributes": {}
}
```
{% include copy-curl.html %}

最後，這個範例會將可完整存取 Security Analytics 的角色同時指派給 `alice` 和 `bob`：

```json
PUT /_plugins/_security/api/rolesmapping/security_analytics_full_access
{
  "backend_roles": [],
  "hosts": [],
  "users": [
    "alice",
    "bob"
  ]
}
```
{% include copy-curl.html %}

不過，由於 `alice` 和 `bob` 具有不同的後端角色，因此他們無法檢視彼此的偵測器或其結果。

---
## 搭配此外掛程式使用精細存取控制的注意事項

當觸發條件產生警示時，偵測器組態、警示本身，以及傳送至頻道的任何通知，都可能包含描述所查詢索引的中繼資料。根據設計，此外掛程式必須擷取資料，並將其以中繼資料的形式儲存在索引之外。[文件層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/document-level-security/) (DLS) 和[欄位層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/field-level-security/) (FLS) 存取控制旨在保護索引中的資料。但一旦資料以中繼資料的形式儲存在索引之外，可存取偵測器和監視器組態、警示及其通知的使用者，就能檢視此中繼資料，並可能推斷出索引中資料的內容和品質，而這些內容和品質原本會受到 DLS 和 FLS 存取控制的保護。

為降低非預期使用者檢視可能描述索引之中繼資料的機會，我們建議管理員啟用以角色為基礎的存取控制，並在將權限指派給目標使用者群組時，將這類設計要素納入考量。如需詳細資訊，請參閱[依後端角色限制存取](#advanced-limit-access-by-backend-role)。
