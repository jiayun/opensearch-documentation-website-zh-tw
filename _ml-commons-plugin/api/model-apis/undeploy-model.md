---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取消部署模型"
parent: Model APIs
grand_parent: ML APIs
nav_order: 45
---

# 取消部署模型 API

若要從記憶體中取消部署模型，請使用 undeploy 操作。

如需此 API 的使用者存取權限資訊，請參閱[模型存取控制注意事項]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/#model-access-control-considerations)。

## 端點

```json
POST /_plugins/_ml/models/{model_id}/_undeploy
POST /_plugins/_ml/models/_undeploy
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `model_id` | 字串 | 要取消部署的模型 ID。如果您使用 `/_plugins/_ml/models/_undeploy` 端點，請在 `model_ids` 請求本文欄位中提供模型 ID。 |

## 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `model_ids` | 陣列 | 要取消部署的模型 ID 清單。使用 `/_plugins/_ml/models/_undeploy` 端點時為必要。若已啟用模型存取控制，每個請求只能指定一個模型 ID。 |
| `node_ids` | 陣列 | 要從中取消部署模型的節點 ID 清單。若省略，則會從所有節點取消部署模型。需要將 `plugins.ml_commons.allow_custom_deployment_plan` 設定為 `true`。 |

## 請求範例：從所有 ML 節點取消部署模型

```json
POST /_plugins/_ml/models/MGqJhYMBbbh0ushjm8p_/_undeploy
```
{% include copy-curl.html %}

## 請求範例：從特定節點取消部署特定模型

```json
POST /_plugins/_ml/models/_undeploy
{
  "node_ids": ["sv7-3CbwQW-4PiIsDOfLxQ"],
  "model_ids": ["KDo2ZYQB-v9VEDwdjkZ4"]
}
```
{% include copy-curl.html %}

## 範例請求：從所有節點取消部署特定模型

```json
POST /_plugins/_ml/models/_undeploy
{
  "model_ids": ["KDo2ZYQB-v9VEDwdjkZ4"]
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "sv7-3CbwQW-4PiIsDOfLxQ" : {
    "stats" : {
      "KDo2ZYQB-v9VEDwdjkZ4" : "undeployed"
    }
  }
}
```

如果模型未部署在節點上，該模型的狀態為 `not_found`。

## 依據 TTL 自動取消部署模型

模型可以根據預先定義的存留時間 (TTL)，在模型最後一次被存取或使用後，自動從記憶體中取消部署。若要定義自動取消部署模型的 TTL，請在您的機器學習 (ML) 模型中包含以下 `ModelDeploySetting`。請注意，模型 TTL 會由 `sync_up` cron 工作定期檢查，因此模型存在於記憶體中的最長時間可能是 TTL 加上 `sync_up` 工作間隔。預設的 cron 工作間隔為 10 秒。若要在內部更新 cron 工作，請使用以下叢集設定：

```json
PUT /_cluster/settings
{
    "persistent": {
        "plugins.ml_commons.sync_up_job_interval_in_seconds": 10
    }
}
```
{% include copy-curl.html %}

## 請求範例：建立具有 TTL 的模型
```json
POST /_plugins/_ml/models/_register
 {
   "name": "Sample Model Name",
   "function_name": "remote",
   "description": "test model",
   "connector_id": "-g1nOo8BOaAC5MIJ3_4R",
   "deploy_setting": {"model_ttl_minutes": 100}
 }
```
{% include copy-curl.html %}

## 範例請求：在模型未部署時以 TTL 更新模型
```json
PUT /_plugins/_ml/models/COj7K48BZzNMh1sWedLK
{
    "deploy_setting": {"model_ttl_minutes" : 100}
}
```
{% include copy-curl.html %}
