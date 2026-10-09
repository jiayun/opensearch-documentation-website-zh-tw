---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新多租用戶組態"
parent: Multi-tenancy configuration APIs
grand_parent: Security APIs
nav_order: 10
---

# 建立或更新多租用戶組態 API
**於 2.7 版引進**
{: .label .label-purple }

建立或取代多租用戶組態。

<!-- spec_insert_start
api: security.create_update_tenancy_config
component: endpoints
-->
## 端點
```json
PUT /_plugins/_security/api/tenancy/config
```
<!-- spec_insert_end -->

## 請求本文欄位

請求本文為必要，且必須包含下列至少一個欄位。OpenSearch 會保留您省略之任何欄位的目前值，並拒絕任何未列出的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `multitenancy_enabled` | 布林值 | 是否啟用多租用戶。 |
| `private_tenant_enabled` | 布林值 | 使用者是否可以使用其私人租用戶。 |
| `default_tenant` | 字串 | OpenSearch Dashboards 預設開啟的租用戶。必須指定其中一個可用的租用戶，且不能是空字串。 |
| `sign_in_options` | 字串陣列 | OpenSearch Dashboards 提供的登入方法。有效值為 `BASIC`、`SAML`、`OPENID` 及 `ANONYMOUS`。每個值都必須對應至叢集上設定的驗證提供者。 |
| `preferred_tenants` | 字串陣列 | 在 OpenSearch Dashboards 租用戶選取器中，依偏好順序列在其他租用戶之前的租用戶。 |

## 範例請求

```json
PUT _plugins/_security/api/tenancy/config
{
  "multitenancy_enabled": true,
  "private_tenant_enabled": true,
  "default_tenant": "Global"
}
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "default_tenant": "Global",
  "private_tenant_enabled": true,
  "multitenancy_enabled": true,
  "sign_in_options": [],
  "preferred_tenants": []
}
```
