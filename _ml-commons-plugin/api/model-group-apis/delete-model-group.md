---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除模型群組"
parent: Model group APIs
grand_parent: ML Commons APIs
nav_order: 50
---

# 刪除模型群組 API

只有在不包含任何模型版本的情況下，您才能刪除模型群組。
{: .important}

如果您的叢集已啟用模型存取控制，則只有擁有者或具有相符後端角色的使用者可以刪除該模型群組。任何使用者都可以刪除任何公開的模型群組。

如果您的叢集已停用模型存取控制，則具有 `delete model group API` 權限的使用者可以刪除任何模型群組。

管理員使用者可以刪除任何模型群組。
{: .note}

當您刪除模型群組中的最後一個模型版本時，該模型群組會自動從索引中刪除。
{: .important}

如需更多資訊，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。

## 範例請求

```json
DELETE _plugins/_ml/model_groups/{model_group_id}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "_index": ".plugins-ml-model-group",
  "_id": "l8nnQogByXnLJ-QNpEk2",
  "_version": 5,
  "result": "deleted",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 70,
  "_primary_term": 23
}
```

## 不存在模型群組的回應

如果您嘗試刪除不存在的模型群組，刪除作業會成功並傳回 `"result": "not_found"`：

```json
{
  "_index": ".plugins-ml-model-group",
  "_id": "l8nnQogByXnLJ-QNpEk2",
  "_version": 1,
  "result": "not_found",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 5,
  "_primary_term": 25
}
```

這種冪等行為可確保刪除作業可以安全地重試，而不會產生錯誤。
