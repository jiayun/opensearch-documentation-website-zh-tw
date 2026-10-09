---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "批次預測"
parent: Model APIs
grand_parent: ML Commons APIs
nav_order: 70
---

# Batch Predict API

ML Commons 可使用部署在外部模型伺服器上的模型，以離線非同步模式對大型資料集執行推論。若要使用 Batch Predict API，您必須提供外部託管模型的 `model_id`。Amazon SageMaker、Cohere 和 OpenAI 是目前僅有經過驗證且支援此 API 的外部伺服器。

如需此 API 的使用者存取權相關資訊，請參閱[模型存取控制注意事項]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/#model-access-control-considerations)。

如需外部託管模型的相關資訊，請參閱[連線至外部託管模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。 

如需設定批次推論和連接器藍圖的操作說明，請參閱下列內容：

- [Amazon SageMaker 批次預測連接器藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/batch_inference_sagemaker_connector_blueprint.md)

- [OpenAI 批次預測連接器藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/batch_inference_openAI_connector_blueprint.md)

## 端點

```json
POST /_plugins/_ml/models/{model_id}/_batch_predict
```

## 先決條件

使用 Batch Predict API 之前，您需要建立連接至外部託管模型的連接器。針對每個動作，指定用於描述該動作的 `action_type` 參數：

- `batch_predict`：執行批次預測作業。
- `batch_predict_status`：檢查批次預測作業的狀態。
- `cancel_batch_predict`：取消批次預測作業。

例如，若要建立連接至 OpenAI `text-embedding-ada-002` 模型的連接器，請傳送下列請求。`cancel_batch_predict` 動作為選用，支援取消在 OpenAI 上執行的批次工作：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "OpenAI Embedding model",
  "description": "OpenAI embedding model for testing offline batch",
  "version": "1",
  "protocol": "http",
  "parameters": {
    "model": "text-embedding-ada-002",
    "input_file_id": "<your input file id in OpenAI>",
    "endpoint": "/v1/embeddings"
  },
  "credential": {
    "openAI_key": "<your openAI key>"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://api.openai.com/v1/embeddings",
      "headers": {
        "Authorization": "Bearer ${credential.openAI_key}"
      },
      "request_body": "{ \"input\": ${parameters.input}, \"model\": \"${parameters.model}\" }",
      "pre_process_function": "connector.pre_process.openai.embedding",
      "post_process_function": "connector.post_process.openai.embedding"
    },
    {
      "action_type": "batch_predict",
      "method": "POST",
      "url": "https://api.openai.com/v1/batches",
      "headers": {
        "Authorization": "Bearer ${credential.openAI_key}"
      },
      "request_body": "{ \"input_file_id\": \"${parameters.input_file_id}\", \"endpoint\": \"${parameters.endpoint}\", \"completion_window\": \"24h\" }"
    },
    {
      "action_type": "batch_predict_status",
      "method": "GET",
      "url": "https://api.openai.com/v1/batches/${parameters.id}",
      "headers": {
        "Authorization": "Bearer ${credential.openAI_key}"
      }
    },
    {
      "action_type": "cancel_batch_predict",
      "method": "POST",
      "url": "https://api.openai.com/v1/batches/${parameters.id}/cancel",
      "headers": {
        "Authorization": "Bearer ${credential.openAI_key}"
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應包含連接器 ID，您將在後續步驟中使用此 ID：

```json
{
  "connector_id": "XU5UiokBpXT9icfOM0vt"
}
```

接著，註冊外部託管模型，並提供已建立連接器的連接器 ID：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "OpenAI model for realtime embedding and offline batch inference",
    "function_name": "remote",
    "description": "OpenAI text embedding model",
    "connector_id": "XU5UiokBpXT9icfOM0vt"
}
```
{% include copy-curl.html %}

回應包含註冊作業的任務 ID：

```json
{
  "task_id": "rMormY8B8aiZvtEZIO_j",
  "status": "CREATED",
  "model_id": "lyjxwZABNrAVdFa9zrcZ"
}
```

若要檢查作業狀態，請將任務 ID 提供給 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)。註冊完成後，任務的 `state` 會變更為 `COMPLETED`。

## 請求範例

完成先決條件步驟後，您就可以呼叫 Batch Predict API。批次預測請求中的參數會覆寫連接器中定義的參數：

```json
POST /_plugins/_ml/models/lyjxwZABNrAVdFa9zrcZ/_batch_predict
{
  "parameters": {
    "model": "text-embedding-3-large"
  }
}
```
{% include copy-curl.html %}

## 回應範例

回應包含批次預測作業的任務 ID：

```json
{
  "task_id": "KYZSv5EBqL2d0mFvs80C",
  "status": "CREATED"
}
```

若要檢查批次預測工作的狀態，請將任務 ID 提供給 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)。您可以在任務的 `remote_job` 欄位中找到工作詳細資訊。預測完成後，任務的 `state` 會變更為 `COMPLETED`。

## 請求範例

```json
GET /_plugins/_ml/tasks/KYZSv5EBqL2d0mFvs80C
```
{% include copy-curl.html %}

## 回應範例

回應的 `remote_job` 欄位包含批次預測作業的詳細資訊：

```json
{
  "model_id": "JYZRv5EBqL2d0mFvKs1E",
  "task_type": "BATCH_PREDICTION",
  "function_name": "REMOTE",
  "state": "RUNNING",
  "input_type": "REMOTE",
  "worker_node": [
    "Ee5OCIq0RAy05hqQsNI1rg"
  ],
  "create_time": 1725491751455,
  "last_update_time": 1725491751455,
  "is_async": false,
  "remote_job": {
    "cancelled_at": null,
    "metadata": null,
    "request_counts": {
      "total": 3,
      "completed": 3,
      "failed": 0
    },
    "input_file_id": "file-XXXXXXXXXXXX",
    "output_file_id": "file-XXXXXXXXXXXXX",
    "error_file_id": null,
    "created_at": 1725491753,
    "in_progress_at": 1725491753,
    "expired_at": null,
    "finalizing_at": 1725491757,
    "completed_at": null,
    "endpoint": "/v1/embeddings",
    "expires_at": 1725578153,
    "cancelling_at": null,
    "completion_window": "24h",
    "id": "batch_XXXXXXXXXXXXXXX",
    "failed_at": null,
    "errors": null,
    "object": "batch",
    "status": "in_progress"
  }
}
```

如需結果中各欄位的定義，請參閱 [OpenAI Batch API](https://platform.openai.com/docs/guides/batch)。批次推論完成後，您可以呼叫 [OpenAI Files API](https://platform.openai.com/docs/api-reference/files)，並提供回應的 `id` 欄位中指定的檔案名稱，以下載輸出。

### 取消批次預測工作

您也可以使用批次預測請求傳回的任務 ID，取消在遠端平台上執行的批次預測作業。若要新增此功能，請在建立連接器時，於連接器組態中將 `action_type` 設為 `cancel_batch_predict`。  

## 請求範例

```json
POST /_plugins/_ml/tasks/KYZSv5EBqL2d0mFvs80C/_cancel_batch
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "status": "OK"
}
```
