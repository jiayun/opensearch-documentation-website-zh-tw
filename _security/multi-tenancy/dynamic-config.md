---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenSearch Dashboards 中的動態組態"
parent: OpenSearch Dashboards multi-tenancy
nav_order: 147
---


# OpenSearch Dashboards 中的動態組態

多租用戶功能在 OpenSearch Dashboards 中包含動態組態選項，讓您可以管理常見的租用戶設定，而不必變更每個節點上的組態 YAML 檔案，然後重新啟動叢集。您可以透過 Dashboards 介面或 REST API 來使用這項功能。下列清單包含目前動態組態所涵蓋選項的說明：

- **停用或啟用多租用戶**：管理員可以動態停用和啟用多租用戶。停用多租用戶不會有資料遺失的風險。當管理員選擇重新啟用租用戶時，所有先前儲存的物件都會保留並可供使用。預設值為 `multitenancy_enabled: true`。
  
  此設定不會影響全域租用戶，全域租用戶一律保持啟用。
  {: .note }

- **停用或啟用私人租用戶**：此選項可讓管理員啟用和停用私人租用戶。與啟用多租用戶設定一樣，當私人租用戶重新啟用時，所有先前儲存的物件都會保留並可供使用。
- **預設租用戶**：此選項可讓管理員在使用者登入時，選擇全域、私人或自訂租用戶作為預設租用戶。如果使用者無權存取預設租用戶 (例如，將使用者無法使用的自訂租用戶指定為預設租用戶)，預設租用戶會改為偏好租用戶，也就是由 `opensearch-dashboards.yml` 檔案中的 `opensearch_security.multitenancy.tenants.preferred` 設定所指定。如需此設定的詳細資訊，請參閱[多租用戶組態]({{site.url}}{{site.baseurl}}/security/multi-tenancy/multi-tenancy-config/)。

視使用動態組態對多租用戶所做的特定變更而定，部分使用者在儲存變更後可能會被登出 Dashboards 工作階段。例如，如果管理員使用者停用多租用戶，選取私人或自訂租用戶作為其租用戶的使用者將會被登出，且必須重新登入。同樣地，如果管理員使用者停用私人租用戶，選取私人租用戶的使用者將會被登出，且必須重新登入。

然而，全域租用戶是特殊情況。由於此租用戶永遠不會停用，選取全域租用戶作為其作用中租用戶的使用者，其工作階段不會中斷。此外，變更預設租用戶不會影響使用者的工作階段。


## 在 OpenSearch Dashboards 中設定多租用戶

若要在 Dashboards 中設定多租用戶，請依照下列步驟操作：

1. 首先，在 Dashboards 首頁功能表中選取 **Security**。然後在畫面左側的 Security 功能表中選取 **Tenancy**。畫面會顯示 **Multi-tenancy** 頁面。
1. 依預設會顯示 **Manage** 索引標籤。選取 **Configure** 索引標籤，以顯示多租用戶的動態設定。
   * 在 **Multi-tenancy** 欄位中，選取 **Enable tenancy** 核取方塊以啟用多租用戶。清除核取方塊以停用此功能。預設值為 `true`。
   * 在 **Tenants** 欄位中，您可以為使用者啟用或停用私人租用戶。依預設會選取核取方塊並啟用此功能。
   * 在 **Default tenant** 欄位中，使用下拉式功能表選取預設租用戶。此功能表包含 Global、Private 以及使用者可使用的任何其他自訂租用戶。
1. 進行您偏好的變更後，選取視窗右下角的 **Save changes**。畫面會出現快顯視窗，列出您已變更的組態項目，並要求您檢閱變更。
1. 選取您要確認之項目旁的核取方塊，然後選取 **Apply changes**。變更會以動態方式實作。


## 使用 REST API 設定多租用戶

除了使用 Dashboards 介面之外，您也可以使用 REST API 管理動態組態。

### 取得租用戶組態

GET 呼叫會擷取動態組態的設定：

```json
GET /_plugins/_security/api/tenancy/config
```
{% include copy-curl.html security=true %}

#### 範例回應

```json
{
    "mulitenancy_enabled": true,
    "private_tenant_enabled": true,
    "default_tenant": "global tenant"
}
```

### 更新租用戶組態

PUT 呼叫會更新動態組態的設定：

```json
PUT /_plugins/_security/api/tenancy/config
{
    "default_tenant": "custom tenant 1",
    "private_tenant_enabled": false,
    "mulitenancy_enabled": true
}
```
{% include copy-curl.html security=true %}

### 範例回應

```json
{
    "mulitenancy_enabled": true,
    "private_tenant_enabled": false,
    "default_tenant": "custom tenant 1"
}
```

### Dashboards Info API

您也可以使用 `dashboardsinfo` API，為登入 Dashboards 的使用者擷取多租用戶設定的狀態：

```json
GET /_plugins/_security/dashboardsinfo
```
{% include copy-curl.html security=true %}

### 範例回應

```json
{
  "user_name" : "admin",
  "not_fail_on_forbidden_enabled" : false,
  "opensearch_dashboards_mt_enabled" : true,
  "opensearch_dashboards_index" : ".kibana",
  "opensearch_dashboards_server_user" : "kibanaserver",
  "multitenancy_enabled" : true,
  "private_tenant_enabled" : true,
  "default_tenant" : "Private"
}
```

