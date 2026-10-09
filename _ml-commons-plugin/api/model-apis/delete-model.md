---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除模型"
parent: Model APIs
grand_parent: ML Commons APIs
nav_order: 47
---

# 刪除模型 API

根據 `model_id` 刪除模型。

當您刪除模型群組中的最後一個模型版本時，該模型群組會自動從索引中刪除。
{: .important}

有關此 API 的使用者存取權資訊，請參閱 [模型存取控制注意事項]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/#model-access-control-considerations)。

## 端點

```json
DELETE /_plugins/_ml/models/{model_id}
```

## 範例請求

```json
DELETE /_plugins/_ml/models/MzcIJX8BA7mbufL6DOwl
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "_index" : ".plugins-ml-model",
  "_id" : "MzcIJX8BA7mbufL6DOwl",
  "_version" : 2,
  "result" : "deleted",
  "_shards" : {
    "total" : 2,
    "successful" : 2,
    "failed" : 0
  },
  "_seq_no" : 27,
  "_primary_term" : 18
}
```

## 錯誤回應

如果您嘗試刪除不存在的模型，OpenSearch 會傳回 404 Not Found 錯誤：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "status_exception",
        "reason": "Failed to find model"
      }
    ],
    "type": "status_exception",
    "reason": "Failed to find model"
  },
  "status": 404
}
```

## 安全地刪除模型
於 2.19 版推出
{: .label .label-purple }

為了防止意外刪除正在被代理程式、搜尋管線、資料匯入管線或其他元件使用的模型，您可以啟用安全檢查。如果已啟用安全檢查，而您嘗試刪除目前使用中的模型，OpenSearch 會傳回錯誤訊息。若要繼續刪除：

- 找出所有使用該模型的元件，並刪除它們或更新它們以改用其他模型。
- 當所有相依性都清除後，刪除該模型。

有關啟用此功能的資訊，請參閱 [功能設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/#feature-settings)。