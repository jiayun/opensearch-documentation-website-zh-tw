---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得租用戶"
parent: Tenant APIs
grand_parent: Security APIs
nav_order: 30
---

# 取得租用戶 API
**於 1.0 版推出**
{: .label .label-purple }

擷取租用戶。指定租用戶名稱以擷取單一租用戶，或省略租用戶名稱以擷取所有租用戶。

<!-- spec_insert_start
api: security.get_tenants
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/tenants
```
<!-- spec_insert_end -->
<!-- spec_insert_start
api: security.get_tenant
component: endpoints
omit_header: true
-->
```json
GET /_plugins/_security/api/tenants/{tenant}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `tenant` | 字串 | 否 | 要擷取的租用戶名稱。若省略，則會傳回所有租用戶。 |

## 範例請求

下列請求會擷取所有租用戶：

```json
GET _plugins/_security/api/tenants
```
{% include copy-curl.html security=true %}

下列請求會擷取 `human_resources` 租用戶：

```json
GET _plugins/_security/api/tenants/human_resources
```
{% include copy-curl.html security=true %}

## 範例回應

針對所有租用戶之請求的回應會包含預設租用戶，以及您建立的任何租用戶：

```json
{
  "global_tenant": {
    "description": "Global tenant",
    "hidden": false,
    "reserved": true,
    "static": true
  },
  "admin_tenant": {
    "description": "Demo tenant for admin user",
    "hidden": false,
    "reserved": false,
    "static": false
  },
  "test-tenant": {
    "description": "A tenant for the test team.",
    "hidden": false,
    "reserved": false,
    "static": false
  },
  "human_resources": {
    "description": "A tenant for the human resources team.",
    "hidden": false,
    "reserved": false,
    "static": false
  }
}
```

當您擷取單一租用戶時，回應只會包含該租用戶：

```json
{
  "human_resources": {
    "description": "A tenant for the human resources team.",
    "hidden": false,
    "reserved": false,
    "static": false
  }
}
```
