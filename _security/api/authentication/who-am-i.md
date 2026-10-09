---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "我是誰"
parent: Authentication APIs
grand_parent: Security APIs
nav_order: 20
---

# Who Am I API
**2.0 版導入**
{: .label .label-purple }

傳回目前使用者的身分資訊。

<!-- spec_insert_start
api: security.who_am_i
component: endpoints
-->
## 端點
```json
GET  /_plugins/_security/whoami
POST /_plugins/_security/whoami
```
<!-- spec_insert_end -->

## 範例請求

```json
GET _plugins/_security/whoami
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "dn": null,
  "is_admin": false,
  "is_node_certificate_request": false
}
```
