---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立控制器"
parent: Controller APIs
grand_parent: ML Commons APIs
nav_order: 10
---

# 建立或更新控制器 API
**2.12 版推出**
{: .label .label-purple }

使用此 API 為模型建立或更新控制器。一個模型可能由多位使用者共用。控制器會針對使用者可對該模型進行的 [Predict API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/) 呼叫次數設定速率限制。控制器由一組適用於不同使用者的速率限制器組成。  

您必須先註冊模型並取得模型 ID，才能為該模型建立控制器。
{: .tip}

POST 方法會建立新的控制器。PUT 方法會更新現有的控制器。 

若要了解如何在模型層級為所有使用者設定速率限制，請參閱 [Update Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/update-model/)。速率限制會採用模型層級限制或使用者層級限制中較嚴格的一項。例如，若模型層級限制為每分鐘 2 個請求，而使用者層級限制為每分鐘 4 個請求，則整體限制將設為每分鐘 2 個請求。

## 端點

```json
POST /_plugins/_ml/controllers/{model_id}
PUT /_plugins/_ml/controllers/{model_id}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`model_id` | 字串 | 您要設定速率限制之模型的模型 ID。必要。

## 請求本文欄位

下表列出可用的請求欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:---  | :--- | :--- | :---
`user_rate_limiter`| 物件 | 必要 | 限制使用者可對該模型呼叫 Predict API 的次數。如需詳細資訊，請參閱[限制推論呼叫的速率]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#rate-limiting-inference-calls)。

`user_rate_limiter` 物件包含每位使用者的物件，以使用者名稱指定。使用者物件包含下列欄位。

欄位 | 資料類型 | 說明
:---  | :--- | :--- 
`limit` | 整數 | 使用者在每 `unit` 時間內可對該模型呼叫 Predict API 的最大次數。預設情況下，Predict API 的呼叫次數沒有限制。一旦設定限制，就無法將其重設為無限制。作為替代方案，您可以指定較高的限制值與較小的時間單位，例如每奈秒 1 個請求。
`unit` | 字串 | 速率限制器的時間單位。有效值為 `DAYS`、`HOURS`、`MICROSECONDS`、`MILLISECONDS`、`MINUTES`、`NANOSECONDS` 和 `SECONDS`。


## 請求範例：建立控制器

```json
POST _plugins/_ml/controllers/mtw-ZI0B_1JGmyB068C0
{
  "user_rate_limiter": {
    "user1": {
      "limit": 4,
      "unit": "MINUTES"
    },
    "user2": {
      "limit": 4,
      "unit": "MINUTES"
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "model_id": "mtw-ZI0B_1JGmyB068C0",
  "status": "CREATED"
}
```

## 請求範例：更新單一使用者的速率限制

若要更新 `user1` 的限制，請傳送 PUT 請求並指定更新後的資訊：

```json
PUT _plugins/_ml/controllers/mtw-ZI0B_1JGmyB068C0
{
  "user_rate_limiter": {
    "user1": {
      "limit": 6,
      "unit": "MINUTES"
    }
  }
}
```
{% include copy-curl.html %}

這只會更新 `user1` 物件，其他所有使用者的限制將維持不變：

```json
{
  "model_id": "mtw-ZI0B_1JGmyB068C0",
  "user_rate_limiter": {
    "user1": {
      "limit": "6",
      "unit": "MINUTES"
    },
    "user2": {
      "limit": "4",
      "unit": "MINUTES"
    }
  }
}
```

## 回應範例

```json
{
  "_index": ".plugins-ml-controller",
  "_id": "mtw-ZI0B_1JGmyB068C0",
  "_version": 2,
  "result": "updated",
  "forced_refresh": true,
  "_shards": {
    "total": 2,
    "successful": 2,
    "failed": 0
  },
  "_seq_no": 1,
  "_primary_term": 1
}
```

## 請求範例：刪除單一使用者的速率限制

若要刪除 `user2` 的限制，請傳送包含其他所有使用者限制的 POST 請求： 

```json
POST _plugins/_ml/controllers/mtw-ZI0B_1JGmyB068C0
{
  "user_rate_limiter": {
    "user1": {
      "limit": 6,
      "unit": "MINUTES"
    }
  }
}
```
{% include copy-curl.html %}

這會以新的資訊覆寫控制器：

```json
{
  "model_id": "mtw-ZI0B_1JGmyB068C0",
  "user_rate_limiter": {
    "user1": {
      "limit": "6",
      "unit": "MINUTES"
    }
  }
}
```

## 回應範例

```json
{
  "_index": ".plugins-ml-controller",
  "_id": "mtw-ZI0B_1JGmyB068C0",
  "_version": 2,
  "result": "updated",
  "forced_refresh": true,
  "_shards": {
    "total": 2,
    "successful": 2,
    "failed": 0
  },
  "_seq_no": 1,
  "_primary_term": 1
}
```

## 必要權限

若您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:admin/opensearch/ml/controllers/create` 和 `cluster:admin/opensearch/ml/controllers/update`。