---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "批次匯入"
has_children: true
has_toc: false
nav_order: 80
parent: Connecting to externally hosted models 
grand_parent: Integrating ML models
---

# 使用外部託管的 ML 模型進行批次匯入

**2.15 版新增**
{: .label .label-purple }

如果您要匯入多份文件，並透過呼叫外部託管的模型來產生嵌入，可以使用批次匯入來提升效能。

當您使用 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 匯入文件時，支援批次匯入的處理器會將文件分成多個批次，並以單一請求將每批文件傳送至外部託管的模型。

[`text_embedding`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-embedding/) 與 [`sparse_encoding`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/sparse-encoding/) 處理器支援批次匯入。


## 步驟 1：註冊模型群組

您可以透過兩種方式註冊模型：

* 您可以使用 `model_group_id` 將模型版本註冊到現有的模型群組。
* 如果您不使用 `model_group_id`，ML Commons 會以新的模型群組建立模型。

若要註冊模型群組，請傳送以下請求：

```json
POST /_plugins/_ml/model_groups/_register
{
  "name": "remote_model_group",
  "description": "A model group for external models"
}
```
{% include copy-curl.html %}

回應中包含模型群組 ID，您將使用它把模型註冊到此模型群組：

```json
{
 "model_group_id": "wlcnb4kBJ1eYAeTMHlV6",
 "status": "CREATED"
}
```

若要進一步了解模型群組，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。

## 步驟 2：建立連接器

您可以建立獨立連接器，供 OpenSearch 中多個共用相同外部端點與組態的模型註冊重複使用。或者，您也可以在建立模型時指定連接器，使其僅供該模型使用。如需更多資訊與範例連接器，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

Connectors Create API（`/_plugins/_ml/connectors/_create`）會建立連接器，協助在 OpenSearch 中註冊與部署外部模型。透過 `endpoint` 參數，您可以使用特定 API 端點將 ML Commons 連接到任何支援的 ML 工具。例如，您可以使用 `api.openai.com` 端點連接到 ChatGPT 模型：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "OpenAI Chat Connector",
    "description": "The connector to public OpenAI model service for gpt-4o-mini",
    "version": 1,
    "protocol": "http",
    "parameters": {
        "endpoint": "api.openai.com",
        "model": "gpt-4o-mini",
        "input_docs_processed_step_size": 100
    },
    "credential": {
        "openAI_key": "..."
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "url": "https://${parameters.endpoint}/v1/chat/completions",
            "headers": {
                "Authorization": "Bearer ${credential.openAI_key}"
            },
            "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": ${parameters.messages} }"
        }
    ]
}
```
{% include copy-curl.html %}

`parameters.input_docs_processed_step_size` 參數用於設定傳送至遠端伺服器的文件批次大小上限。您可以將此參數設定為遠端伺服器支援的最大批次大小，或設定為較小的數值以獲得最佳效能。

回應中包含新建連接器的連接器 ID：

```json
{
  "connector_id": "a1eMb4kBJ1eYAeTMAljY"
}
```

## 步驟 3：註冊外部託管的模型

若要將外部託管的模型註冊到步驟 1 建立的模型群組，請在以下請求中提供步驟 1 的模型群組 ID 與步驟 2 的連接器 ID。您必須將 `function_name` 指定為 `remote`：

```json
POST /_plugins/_ml/models/_register
{
    "name": "openAI-gpt-4o-mini",
    "function_name": "remote",
    "model_group_id": "wlcnb4kBJ1eYAeTMHlV6",
    "description": "test model",
    "connector_id": "a1eMb4kBJ1eYAeTMAljY"
}
```
{% include copy-curl.html %}

OpenSearch 會傳回註冊作業的任務 ID：

```json
{
  "task_id": "cVeMb4kBJ1eYAeTMFFgj",
  "status": "CREATED"
}
```

若要檢查作業狀態，請將任務 ID 提供給 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)：

```json
GET /_plugins/_ml/tasks/cVeMb4kBJ1eYAeTMFFgj
```
{% include copy-curl.html %}

當作業完成時，狀態會變更為 `COMPLETED`：

```json
{
  "model_id": "cleMb4kBJ1eYAeTMFFg4",
  "task_type": "REGISTER_MODEL",
  "function_name": "REMOTE",
  "state": "COMPLETED",
  "worker_node": [
    "XPcXLV7RQoi5m8NI_jEOVQ"
  ],
  "create_time": 1689793598499,
  "last_update_time": 1689793598530,
  "is_async": false
}
```

請記下傳回的 `model_id`，因為部署模型時需要用到它。

## 步驟 4：部署模型

當您第一次傳送 Predict API 請求時，外部託管的模型會自動部署。若要停用外部託管模型的自動部署，請將 `plugins.ml_commons.model_auto_deploy.enable` 設定為 `false`：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.model_auto_deploy.enable" : "false"
  }
}
```
{% include copy-curl.html %}

若要取消部署模型，請使用 [Undeploy API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/undeploy-model/)：

```json
POST /_plugins/_ml/models/cleMb4kBJ1eYAeTMFFg4/_deploy
```
{% include copy-curl.html %}

回應中包含任務 ID，您可以用它來檢查部署作業的狀態：

```json
{
  "task_id": "vVePb4kBJ1eYAeTM7ljG",
  "status": "CREATED"
}
```

如同上一個步驟，請呼叫 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 來檢查作業狀態：

```json
GET /_plugins/_ml/tasks/vVePb4kBJ1eYAeTM7ljG
```
{% include copy-curl.html %}

當作業完成時，狀態會變更為 `COMPLETED`：

```json
{
  "model_id": "cleMb4kBJ1eYAeTMFFg4",
  "task_type": "DEPLOY_MODEL",
  "function_name": "REMOTE",
  "state": "COMPLETED",
  "worker_node": [
    "n-72khvBTBi3bnIIR8FTTw"
  ],
  "create_time": 1689793851077,
  "last_update_time": 1689793851101,
  "is_async": true
}
```

## 步驟 5：建立資料匯入管線

以下範例請求會建立一個包含 `text_embedding` 處理器的資料匯入管線。該處理器會將 `passage_text` 欄位中的文字轉換為文字嵌入，並將嵌入儲存在 `passage_embedding` 中：

```json
PUT /_ingest/pipeline/nlp-ingest-pipeline
{
  "description": "A text embedding pipeline",
  "processors": [
    {
      "text_embedding": {
        "model_id": "cleMb4kBJ1eYAeTMFFg4",
        "field_map": {
          "passage_text": "passage_embedding"
        },
        "batch_size": 5
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 步驟 6：執行大量編製索引

若要大量匯入文件，請呼叫 Bulk API 並提供 `pipeline` 參數。如果您未提供 `pipeline` 參數，則會使用該索引的預設資料匯入管線進行匯入：

```json
POST _bulk?batch_size=5&pipeline=nlp-ingest-pipeline
{ "create": { "_index": "testindex1", "_id": "2" } }
{ "passage_text": "hello world" }
{ "create": { "_index": "testindex1", "_id": "3" } }
{ "passage_text": "big apple" }
{ "create": { "_index": "testindex1", "_id": "4" } }
{ "passage_text": "golden gate bridge" }
{ "create": { "_index": "testindex1", "_id": "5" } }
{ "passage_text": "fine tune" }
{ "create": { "_index": "testindex1", "_id": "6" } }
{ "passage_text": "random test" }
{ "create": { "_index": "testindex1", "_id": "7" } }
{ "passage_text": "sun and moon" }
{ "create": { "_index": "testindex1", "_id": "8" } }
{ "passage_text": "windy" }
{ "create": { "_index": "testindex1", "_id": "9" } }
{ "passage_text": "new york" }
{ "create": { "_index": "testindex1", "_id": "10" } }
{ "passage_text": "fantastic" }

```
{% include copy-curl.html %}

