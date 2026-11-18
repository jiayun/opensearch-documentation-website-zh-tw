---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ML 推論"
parent: Processors
grand_parent: Pipelines
nav_order: 210
canonical_url: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/processors/ml-inference/
redirect_to: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/processors/ml-inference/
---

# ML 推論處理器

`ml_inference` 處理器可讓您在 OpenSearch Data Prepper 中使用 OpenSearch 的機器學習 (ML) 功能。將 ML 模型整合至 Data Prepper 管線後，您可以在將資料匯入 Amazon OpenSearch Service 的過程中套用這些模型，以支援向量搜尋、語意搜尋或對話式搜尋等 AI 驅動的搜尋體驗。若要探索 OpenSearch 的 AI 搜尋類型，請參閱 [AI 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/)。

使用 `ml_inference` 處理器，您可以在 Data Prepper 管線中叫用由 OpenSearch 託管的 ML 模型來處理事件。此處理器同時支援即時叫用與非同步 (離線) 批次作業叫用。

若要使用 `ml_inference` 處理器，您的叢集必須安裝 ML Commons 外掛程式。標準 OpenSearch 發行版本預設已包含此外掛程式。如需詳細資訊，請參閱[管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。
{: .note}

## 組態欄位

下表說明 `ml_inference` 處理器的組態選項。

| 選項 | 必要 | 類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `host`             | 是      | 字串 | OpenSearch 主機的名稱。                                                                          |
| `action_type`      | 是      | 字串 | 要執行的動作類型。目前僅支援 `batch_predict`。預設值為 `batch_predict`。 |
| `model_id`         | 是      | 字串 | 要叫用的 ML 模型 ID。當 `service_name` 為 `bedrock` 時，您也可以將 `model_id` 設定為下列其中一個內建 Amazon Bedrock 模型 ID：`amazon.titan-embed-text-v2:0`、`amazon.titan-embed-image-v1` 或 `amazon.nova-2-multimodal-embeddings-v1:0`。若使用內建模型，處理器會直接在 Amazon Bedrock 中建立批次推論工作，而不會傳送請求至 OpenSearch 主機，且 `aws.job_sts_role_arn` 為必要項目。 |
| `output_path`      | 是      | 字串 | 離線批次工作結果要寫入的 [Amazon Simple Storage Service (Amazon S3)](https://aws.amazon.com/s3/) 位置。                                      |
| `aws.region`       | 是      | 字串 | OpenSearch Service 部署所在的 AWS 區域。                                                  |
| `aws.sts_role_arn` | 否       | 字串 | 要擔任的 AWS Identity and Access Management (IAM) 角色的 Amazon Resource Name (ARN)。                                  |
| `aws.sts_external_id` | 否    | 字串 | 擔任 IAM 角色時要使用的外部 ID。長度必須為 2--1224 個字元。 |
| `aws.sts_header_overrides` | 否 | 對應表  | 擔任 IAM 角色時要使用的標頭覆寫對應表。最多 5 個標頭。 |
| `aws.job_sts_role_arn` | 視情況 | 字串 | Amazon Bedrock 執行批次推論工作時所擔任之 IAM 角色的 ARN。當 `model_id` 為內建 Amazon Bedrock 模型 ID 時為必要項目。長度必須為 20--2048 個字元。 |
| `service_name`     | 否       | 字串 | 託管推論所用模型的 AI 服務名稱。預設值為 `sagemaker` (Amazon SageMaker)。  |
| `input_key`        | 否       | 字串 | 寫入批次工作結果時，要作為 S3 物件索引鍵名稱的事件欄位名稱。這可讓您根據事件資料動態命名輸出檔案。                                                              |
| `ml_when`          | 否       | 字串 | 決定何時叫用 `ml_inference` 處理器的條件運算式。                     |
| `tags_on_failure`  | 否       | 清單   | 當 `ml_inference` 處理器失敗或發生錯誤時，要新增至事件的標籤清單。             |
| `max_batch_size`   | 否       | 整數 | 適用於 `service_name` 為 `sagemaker` 時。單一批次工作中要包含的事件數量上限。當收集的事件數量達到此值，或 1 分鐘內沒有新事件抵達時，處理器會建立批次工作。預設值為 `100`。 |
| `retry_time_window` | 否      | 持續時間 | 批次工作請求遭到節流後，處理器保留事件以供重試的時間長度。無法在此時間範圍內處理的事件會被視為失敗。支援 ISO 8601 表示法字串（例如 `PT20.345S` 或 `PT15M`），以及以秒（`60s`）和毫秒（`1500ms`）表示的簡易表示法字串。預設值為 `PT10M`。 |
| `retry_interval`   | 否       | 持續時間 | 適用於 `service_name` 為 `bedrock` 時。重試遭到節流的批次工作請求之間的等待時間。支援 ISO 8601 表示法字串（例如 `PT1M`），以及以秒（`60s`）和毫秒（`1500ms`）表示的簡易表示法字串。有效值為 3 秒至 5 分鐘。預設值為 `60s`。 |
| `dlq`              | 否       | 物件 | 針對無法建立批次工作之事件的[死信佇列 (DLQ)]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/dlq/) 組態。若 DLQ 組態未指定 `region` 或 `sts_role_arn`，則會使用 `aws` 組態中的值。 |



#### 組態範例

以下範例展示 `map_to_list` 處理器的組態範例：

```yaml
  processor:
    - ml_inference:
        host: "https://search-ml-inference-test.us-west-2.es.amazonaws.com"
        action_type: "batch_predict"
        service_name: "sagemaker"
        model_id: "9t4AbpYBQB1BoSOe8g8N"
        output_path: "s3://test-bucket/output"
        aws:
          region: "us-west-2"
          sts_role_arn: "arn:aws:iam::123456789012:role/my-inference-role"
        ml_when: /bucket == "offlinebatch"

```
{% include copy.html %}

## 使用方式

此處理器支援 `batch_predict` 操作，此操作會叫用 [Batch Predict API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/batch-predict/) 進行離線批次處理。


## 行為

對於 `batch_predict` 操作，`ml_inference` 處理器搭配 [S3 來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3/) 使用效果最佳。若要將 S3 設定為僅處理中繼資料，請依下列方式設定 S3 掃描區塊：

```yaml
scan:
  buckets:
    - bucket:
        name: test-offlinebatch
        data_selection: metadata_only
```
{% include copy.html %}

啟用 `metadata_only` 時，處理器會接收下列格式的事件：

```json
{"bucket":"test-offlinebatch","length":6234,"time":1738108982.000000000,"key":"input_folder/batch_input_1.json"}
```

若要篩選特定記錄進行處理，請使用 `ml_when` 條件。


## 監控離線批次作業狀態

Data Prepper 管線建立離線批次作業後，您可以使用 AI 供應商 (Amazon SageMaker 或 Amazon Bedrock) 的原生主控台追蹤其狀態。

或者，您也可以呼叫 [Search ML Tasks API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/search-task/) 來檢查作業狀態。例如，若要搜尋所有目前正在執行的任務，請使用下列請求：

```json
GET /_plugins/_ml/tasks/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "state": "RUNNING"
          }
        }
      ]
    }
  },
  "_source": ["model_id", "state", "task_type", "create_time", "last_update_time"]
}
```
{% include copy-curl.html %}
