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

下表列出可用的請求本文欄位。所有欄位皆為選用。

欄位 |資料類型 | 說明 
:--- | :--- | :---
`name` | String | 模型群組名稱。在叢集中必須是唯一的。
`description` | String | 模型群組的描述。
`access_mode` | String | 此模型群組的存取模式。有效值為 `public`、`private` 與 `restricted`。當此參數設為 `restricted` 時，您必須指定 `backend_roles` 或 `add_all_backend_roles` 其中之一，但不可同時指定兩者。將存取模式變更為 `public` 或 `private` 會移除模型群組的後端角色。
`backend_roles` | Array | 要加入模型群組的模型擁有者後端角色清單。僅能在 `access_mode` 為 `restricted` 或省略時指定。若您指定 `backend_roles` 而未指定 `access_mode`，存取模式會變更為 `restricted`。不可與 `add_all_backend_roles` 同時指定。
`add_all_backend_roles` | Boolean | 若為 `true`，模型擁有者的所有後端角色都會加入模型群組。若您將此參數設為 `true` 而未指定 `access_mode`，存取模式會變更為 `restricted`。不可與 `backend_roles` 同時指定。管理員使用者不可將此參數設為 `true`。

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

## 範例回應

```json
{
  "status": "Updated"
}
```

## 在停用模型存取控制的叢集中更新模型群組

如果您的叢集已停用模型存取控制（未滿足其中一項[先決條件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/#model-access-control-prerequisites)），您只能更新模型群組的 `name` 和 `description`，無法更新任何存取參數（`access_mode`、`backend_roles` 或 `add_all_backend_roles`）。 