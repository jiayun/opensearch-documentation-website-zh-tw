---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新動作群組"
parent: Action group APIs
grand_parent: Security APIs
nav_order: 10
---

# 建立或更新動作群組 API
**於 1.0 版推出**
{: .label .label-purple }

建立或取代指定的動作群組。

<!-- spec_insert_start
api: security.create_action_group
component: endpoints
-->
## 端點
```json
PUT /_plugins/_security/api/actiongroups/{action_group}
```
<!-- spec_insert_end -->

## 請求本文欄位

請求本文為必要。其為包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `allowed_actions` | 字串陣列 | 動作群組允許的動作。請指定個別動作，例如 `indices:data/write/index`，或其他動作群組的名稱。 | 是 |
| `type` | 字串 | 動作群組的範圍。有效值為 `cluster`、`index` 及 `kibana`。若省略，則動作群組可用於任何層級。 | 否 |
| `description` | 字串 | 動作群組的說明。 | 否 |
| `hidden` | 布林值 | 動作群組是否對 API 及 OpenSearch Dashboards 隱藏。預設為 `false`。 | 否 |
| `reserved` | 布林值 | 動作群組是否為唯讀且無法修改。預設為 `false`。 | 否 |

## 範例請求

```json
PUT _plugins/_security/api/actiongroups/custom_action_group
{
  "allowed_actions": [
    "indices:data/write/index*",
    "indices:data/write/update*",
    "indices:admin/mapping/put",
    "indices:data/write/bulk*",
    "read",
    "write"
  ]
}
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "status": "CREATED",
  "message": "'custom_action_group' created."
}
```
