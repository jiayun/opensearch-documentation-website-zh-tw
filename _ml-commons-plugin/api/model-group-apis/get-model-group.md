---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得模型群組"
parent: Model group APIs
grand_parent: ML Commons APIs
nav_order: 30
---

# Get Model Group API

於 2.12 版推出
{: .label .label-purple }

Get Model Group API 會依據模型群組的 ID 傳回該群組的相關資訊。

若您的叢集已啟用模型存取控制，則只有擁有者或具有相符後端角色的使用者可以取得私有模型群組。任何使用者都可以取得任何公開模型群組。

若您的叢集已停用模型存取控制，則具有 `get model group API` 權限的使用者可以取得任何模型群組。

如需更多資訊，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。

## 路徑與 HTTP 方法

```json
GET /_plugins/_ml/model_groups/{model_group_id}
```

### 範例請求

下列範例請求會依據模型群組的 ID 取得該群組：

```json
GET /_plugins/_ml/model_groups/{model_group_id}
```
{% include copy-curl.html %}

### 範例回應

下列回應會傳回模型群組資訊，包括模型群組的名稱、版本、描述、存取層級及建立資訊：

```json
{
  "name": "test_model_group",
  "latest_version": 0,
  "description": "This is a public model group",
  "access": "public",
  "created_time": 1715112992748,
  "last_updated_time": 1715112992748
}
```
