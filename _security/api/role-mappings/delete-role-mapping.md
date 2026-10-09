---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除角色對應"
parent: Role mapping APIs
grand_parent: Security APIs
nav_order: 40
---

# 刪除角色對應 API
**於 1.0 版推出**
{: .label .label-purple }

刪除指定的角色對應。

<!-- spec_insert_start
api: security.delete_role_mapping
component: endpoints
-->
## 端點
```json
DELETE /_plugins/_security/api/rolesmapping/{role}
```
<!-- spec_insert_end -->

## 範例請求

```json
DELETE _plugins/_security/api/rolesmapping/test-role
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "status": "OK",
  "message": "'test-role' deleted."
}
```
