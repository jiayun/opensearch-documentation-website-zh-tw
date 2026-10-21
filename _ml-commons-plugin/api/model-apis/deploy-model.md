---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "部署模型"
parent: Model APIs
grand_parent: ML Commons APIs
nav_order: 20
---

# 部署模型 API

部署模型操作會從模型索引讀取模型的分塊，然後建立模型執行個體以快取於記憶體中。此操作需要 `model_id`。

[外部託管的模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/) 在您第一次傳送 Predict API 請求時，預設會自動部署。若要停用外部託管模型的自動部署，請將 `plugins.ml_commons.model_auto_deploy.enable` 設為 `false`：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.model_auto_deploy.enable": "false"
  }
}
```
{% include copy-curl.html %}

如需此 API 使用者存取權的相關資訊，請參閱[模型存取控制考量]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/#model-access-control-considerations)。

## 端點

```json
POST /_plugins/_ml/models/{model_id}/_deploy
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `model_id` | 字串 | 要部署的模型 ID。必要。 |

## 請求本文欄位

下表列出可用的請求本文欄位。請求本文為選用。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `node_ids` | 陣列 | 要在其上部署模型的節點 ID 清單。若省略，模型會部署到所有符合條件的 ML 節點。需要將 `plugins.ml_commons.allow_custom_deployment_plan` 設為 `true`。如需詳細資訊，請參閱 [ML Commons 叢集設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/)。 |

## 範例請求：部署至所有可用的 ML 節點

在此範例請求中，OpenSearch 會將模型部署至任何可用的 OpenSearch ML 節點：

```json
POST /_plugins/_ml/models/WWQI44MBbzI2oUKAvNUt/_deploy
```
{% include copy-curl.html %}

## 範例請求：部署到特定節點

如果您想保留叢集中其他 ML 節點的記憶體，可以在請求本文中指定 `node_ids`，將模型部署到特定節點。此選項需要將 `plugins.ml_commons.allow_custom_deployment_plan` 設定為 `true`：

```json
POST /_plugins/_ml/models/WWQI44MBbzI2oUKAvNUt/_deploy
{
    "node_ids": ["4PLK7KJWReyX0oWKnBA8nA"]
}
```
{% include copy-curl.html %}

## 範例回應

部署模型 API 會傳回 `task_id`，您可以用來監視部署進度：

```json
{
  "task_id": "hA8P44MBhyWuIwnfvTKP",
  "task_type": "DEPLOY_MODEL",
  "status": "CREATED"
}
```

## 監視部署狀態

若要檢查模型部署的狀態，並在部署完成時擷取模型 ID，請使用 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)，並提供傳回的 `task_id` 作為路徑參數：

```json
GET /_plugins/_ml/tasks/hA8P44MBhyWuIwnfvTKP
```
{% include copy-curl.html %}

Get ML Task API 會依部署進行中或已完成，傳回不同的回應格式。如需所有可能回應格式的詳細資訊，請參閱 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/#example-responses)。

如果叢集或節點重新啟動，您就必須重新部署模型。若要瞭解如何設定自動重新部署，請參閱[模型部署設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/#model-deployment-settings)。
{: .tip} 