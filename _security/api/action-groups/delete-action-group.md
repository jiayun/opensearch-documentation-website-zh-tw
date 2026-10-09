---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除動作群組"
parent: Action group APIs
grand_parent: Security APIs
nav_order: 40
---

# Delete Action Group API
**1.0 版推出**
{: .label .label-purple }

刪除指定的動作群組。

<!-- spec_insert_start
api: security.delete_action_group
component: endpoints
-->
## 端點
```json
DELETE /_plugins/_security/api/actiongroups/{action_group}
```
<!-- spec_insert_end -->

## 請求範例

```json
DELETE _plugins/_security/api/actiongroups/custom_action_group
```
{% include copy-curl.html security=true %}

## 回應範例

```json
{
  "status": "OK",
  "message": "'custom_action_group' deleted."
}
```
