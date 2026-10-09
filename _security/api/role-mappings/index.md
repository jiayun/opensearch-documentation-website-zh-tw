---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "角色對應 API"
parent: Security APIs
nav_order: 50
has_children: true
has_toc: false
redirect_from:
  - /security/api/role-mappings/
---

# 角色對應 API

角色對應 API 會將使用者、後端角色及主機對應至安全性角色。

OpenSearch 支援下列角色對應 API。

| API | 說明 |
| :--- | :--- |
| [Create or Update Role Mapping API]({{site.url}}{{site.baseurl}}/security/api/role-mappings/create-role-mapping/) | 建立或取代指定的角色對應。 |
| [Patch Role Mappings API]({{site.url}}{{site.baseurl}}/security/api/role-mappings/patch-role-mappings/) | 更新單一角色對應的個別屬性，或在單次呼叫中建立、更新或刪除多個角色對應。 |
| [Get Role Mappings API]({{site.url}}{{site.baseurl}}/security/api/role-mappings/get-role-mappings/) | 擷取單一角色或所有角色對應的對應關係。 |
| [Delete Role Mapping API]({{site.url}}{{site.baseurl}}/security/api/role-mappings/delete-role-mapping/) | 刪除指定的角色對應。 |
