---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "租用戶 API"
parent: Security APIs
nav_order: 80
has_children: true
has_toc: false
redirect_from:
  - /security/api/tenants/
---

# 租用戶 API

租用戶 API 用於建立、擷取、修改及刪除租用戶，以在不同使用者群組之間隔離 OpenSearch Dashboards 資源。

OpenSearch 支援下列租用戶 API。

| API | 說明 |
| :--- | :--- |
| [Create or Update Tenant API]({{site.url}}{{site.baseurl}}/security/api/tenants/create-tenant/) | 建立或取代指定的租用戶。 |
| [Patch Tenants API]({{site.url}}{{site.baseurl}}/security/api/tenants/patch-tenants/) | 在單一呼叫中更新某個租用戶的個別屬性，或新增、刪除或修改多個租用戶。 |
| [Get Tenants API]({{site.url}}{{site.baseurl}}/security/api/tenants/get-tenants/) | 擷取單一租用戶或所有租用戶。 |
| [Delete Tenant API]({{site.url}}{{site.baseurl}}/security/api/tenants/delete-tenant/) | 刪除指定的租用戶。 |
