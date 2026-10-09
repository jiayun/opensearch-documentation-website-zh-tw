---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "更新模型群組"
parent: Model group APIs
grand_parent: ML Commons APIs
nav_order: 20
---

# 更新模型群組 API

若要更新模型群組，請向 `model_groups` 端點傳送 `PUT` 請求，並提供您要更新之模型群組的 ID。

更新模型群組時，適用下列限制：

- 模型擁有者或管理員使用者可以更新所有欄位。任何與模型群組共用一或多個後端角色的使用者，則只能更新 `name` 和 `description` 欄位。
- 將 `access_mode` 更新為 `restricted` 時，您必須指定 `backend_roles` 或 `add_all_backend_roles` 其中之一，但不可同時指定兩者。
- 更新 `name` 時，請確保該名稱在叢集中是全域唯一的。

如需更多資訊，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。

## 路徑與 HTTP 方法

```json
PUT /_plugins/_ml/model_groups/{model_group_id}
```

## 請求本文欄位

請求欄位的說明請參閱[請求欄位](#request-body-fields)。

## 範例請求

```json
PUT /_plugins/_ml/model_groups/{model_group_id}
{
    "name": "model_group_test",
    "description": "This is the updated description",
    "add_all_backend_roles": true
}
```
{% include copy-curl.html %}

## 在停用模型存取控制的叢集中更新模型群組

如果您的叢集已停用模型存取控制（未符合其中一項[先決條件](ml-commons-plugin/model-access-control/#model-access-control-prerequisites)），您只能更新模型群組的 `name` 和 `description`，而無法更新任何存取參數（`model_access_name`、`backend_roles` 或 `add_backend_roles`）。 