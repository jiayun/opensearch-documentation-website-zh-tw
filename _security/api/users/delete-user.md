---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除使用者"
parent: Internal user APIs
grand_parent: Security APIs
nav_order: 40
---

# 刪除使用者 API
**於 1.0 版導入**
{: .label .label-purple }

刪除指定的內部使用者。

<!-- spec_insert_start
api: security.delete_user
component: endpoints
-->
## 端點
```json
DELETE /_plugins/_security/api/internalusers/{username}
```
<!-- spec_insert_end -->

## 範例請求

```json
DELETE _plugins/_security/api/internalusers/kirk
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "status": "OK",
  "message": "'kirk' deleted."
}
```
