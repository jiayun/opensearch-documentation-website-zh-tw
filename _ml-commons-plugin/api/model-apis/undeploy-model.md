---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取消部署模型"
parent: Model APIs
grand_parent: ML Commons APIs
nav_order: 45
---

# Undeploy Model API

若要從記憶體中取消部署模型，請使用 undeploy 操作。

如需此 API 的使用者存取權限資訊，請參閱[模型存取控制注意事項]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/#model-access-control-considerations)。

### 端點

```json
POST /_plugins/_ml/models/{model_id}/_undeploy
```

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

## 請求範例：從所有節點取消部署特定模型

```json
{
  "model_ids": ["KDo2ZYQB-v9VEDwdjkZ4"]
}
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "sv7-3CbwQW-4PiIsDOfLxQ" : {
    "stats" : {
      "KDo2ZYQB-v9VEDwdjkZ4" : "UNDEPLOYED"
    }
  }
}
```
### 根據 TTL 自動取消部署模型

模型可以根據預先定義的存留時間（TTL），從最後一次存取或使用模型的時間起算，自動從記憶體中取消部署。若要定義可自動取消部署模型的 TTL，請在您的機器學習（ML）模型中加入下列 `ModelDeploySetting`。請注意，`syn_up` cron 工作會定期檢查模型的 TTL，因此模型保留在記憶體中的最長時間可能是 TTL 加上 `sync_up_job_` 間隔。預設 cron 工作間隔為 10 秒。若要更新 cron 工作的內部設定，請使用下列叢集設定：

```json
PUT /_cluster/settings
{
    "persistent": {
        "plugins.ml_commons.sync_up_job_interval_in_seconds": 10
    }
}
```

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

## 請求範例：在模型已取消部署時更新模型的 TTL
```json
PUT /_plugins/_ml/models/COj7K48BZzNMh1sWedLK
{
    "deploy_setting": {"model_ttl_minutes" : 100}
}
```
