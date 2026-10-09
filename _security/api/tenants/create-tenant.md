---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新租用戶"
parent: Tenant APIs
grand_parent: Security APIs
nav_order: 10
---

# 建立或更新租用戶 API
**於 1.0 版推出**
{: .label .label-purple }

建立或取代指定的租用戶。

<!-- spec_insert_start
api: security.create_tenant
component: endpoints
-->
## 端點
```json
PUT /_plugins/_security/api/tenants/{tenant}
```
<!-- spec_insert_end -->

## 請求本文欄位

請求本文為必要項目。其為包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `description` | 字串 | 租用戶的說明。 | 否 |

## 請求範例

```json
PUT _plugins/_security/api/tenants/test-tenant
{
  "description": "A tenant for the test team."
}
```
{% include copy-curl.html security=true %}

## 回應範例

```json
{
  "status": "CREATED",
  "message": "'test-tenant' created."
}
```
