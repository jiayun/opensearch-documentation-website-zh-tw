---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Who am I protected
parent: Authentication APIs
grand_parent: Security APIs
nav_order: 30
---

# Who Am I Protected API
**於 2.11 版推出**
{: .label .label-purple }

傳回目前使用者的身分資訊。與 Who Am I API 不同，此端點受 REST 層授權控管，因此使用者的角色必須授予存取此端點的權限。

<!-- spec_insert_start
api: security.who_am_i_protected
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/whoamiprotected
```
<!-- spec_insert_end -->

## 請求範例

```json
GET _plugins/_security/whoamiprotected
```
{% include copy-curl.html security=true %}

## 回應範例

```json
{
  "dn": null,
  "is_admin": false,
  "is_node_certificate_request": false
}
```
