---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "註冊模型群組"
parent: Model group APIs
grand_parent: ML Commons APIs
nav_order: 10
---

# 註冊模型群組 API

若要註冊模型群組，請向 `_register` 端點傳送 `POST` 請求。您可以在 `public`、`private` 或 `restricted` 存取模式下註冊模型群組。

叢集中的每個模型群組名稱都必須是全域唯一的。
{: .important}

如需更多資訊，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。

## 路徑與 HTTP 方法

```json
POST /_plugins/_ml/model_groups/_register
```

## 請求本文欄位

下表列出可用的請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`name` | 字串 | 模型群組名稱。必要。
`model_group_id` | 字串 | 模型群組的唯一識別碼。選用。若省略，OpenSearch 會自動產生。
`description` | 字串 | 模型群組描述。選用。
`access_mode` | 字串 | 此模型的存取模式。有效值為 `public`、`private` 和 `restricted`。當此參數設為 `restricted` 時，您必須指定 `backend_roles` 或 `add_all_backend_roles` 其中之一，但不可同時指定兩者。選用。若您未指定任何安全性參數（`access_mode`、`backend_roles` 和 `add_all_backend_roles`），預設的 `access_mode` 為 `private`。
`backend_roles` | 陣列 | 要新增至模型的模型擁有者後端角色清單。僅能在 `access_mode` 為 `restricted` 時指定。不可與 `add_all_backend_roles` 同時指定。選用。
`add_all_backend_roles` | 布林值 | 若為 `true`，模型擁有者的所有後端角色都會新增至模型群組。預設為 `false`。不可與 `backend_roles` 同時指定。管理員使用者不可將此參數設為 `true`。選用。

## 範例請求

```json
POST /_plugins/_ml/model_groups/_register
{
    "name": "test_model_group_public",
    "description": "This is a public model group",
    "access_mode": "public"
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
    "model_group_id": "GDNmQ4gBYW0Qyy5ZcBcg",
    "status": "CREATED"
}
```

## 回應本文欄位

下表列出可用的回應欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`model_group_id` | 字串 | 模型群組 ID，您可用它來存取此模型群組。
`status` | 字串 | 操作狀態。

## 註冊公開模型群組

若您以 `public` 存取模式註冊模型群組，此模型群組中的任何模型都可供具有叢集存取權的任何使用者存取。下列請求會註冊一個公開模型群組：

```json
POST /_plugins/_ml/model_groups/_register
{
    "name": "test_model_group_public",
    "description": "This is a public model group",
    "access_mode": "public"
}
```
{% include copy-curl.html %}

## 註冊受限模型群組

若要依後端角色限制存取，您必須以 `restricted` 存取模式註冊模型群組。

註冊模型群組時，您必須使用下列其中一種方法（不可同時使用兩種）將您的一或多個後端角色附加至模型：
    - 在 `backend_roles` 參數中提供後端角色清單。
    - 將 `add_all_backend_roles` 參數設為 `true`，以將您的所有後端角色新增至模型群組。此選項不適用於管理員使用者。

任何與模型群組共用後端角色的使用者，都可以存取此模型群組中的任何模型。這會授與該使用者對應至該後端角色的使用者角色所包含的權限。

管理員使用者可以存取所有模型群組，無論其存取模式為何。
{: .note}

## 範例請求：後端角色清單

下列請求會註冊一個受限模型群組，僅有具備 `IT` 後端角色的使用者可以存取：

```json
POST /_plugins/_ml/model_groups/_register
{
    "name": "model_group_test",
    "description": "This is an example description",
    "access_mode": "restricted",
    "backend_roles" : ["IT"]
}
```
{% include copy-curl.html %}

## 範例請求：所有後端角色

下列請求會註冊一個受限模型群組，並將使用者的所有後端角色新增至模型群組：

```json
POST /_plugins/_ml/model_groups/_register
{
    "name": "model_group_test",
    "description": "This is an example description",
    "access_mode": "restricted",
    "add_all_backend_roles": "true"
}
```
{% include copy-curl.html %}

## 註冊私有模型群組

若您以 `private` 存取模式註冊模型群組，此模型群組中的任何模型僅供您和管理員使用者存取。下列請求會註冊一個私有模型群組：

```json
POST /_plugins/_ml/model_groups/_register
{
    "name": "model_group_test",
    "description": "This is an example description",
    "access_mode": "private"
}
```
{% include copy-curl.html %}

若您未指定 `access_mode`、`backend_roles` 或 `add_all_backend_roles` 任何一項，模型將具有 `private` 存取模式：

```json
POST /_plugins/_ml/model_groups/_register
{
    "name": "model_group_test",
    "description": "This is an example description"
}
```
{% include copy-curl.html %}

## 在停用模型存取控制的叢集中註冊模型群組

若您的叢集已停用模型存取控制（未符合其中一項[先決條件](ml-commons-plugin/model-access-control/#model-access-control-prerequisites)），您仍可以註冊具有 `name` 和 `description` 的模型群組，但無法指定任何存取參數（`model_access_name`、`backend_roles` 或 `add_backend_roles`）。在此類叢集中，所有模型群組預設皆為公開。