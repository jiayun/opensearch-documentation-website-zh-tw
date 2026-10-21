---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得模型"
parent: Model APIs
grand_parent: ML Commons APIs
nav_order: 30
---

# Get Model API

您可以使用 `model_id` 擷取模型資訊。

如需此 API 的使用者存取權資訊，請參閱[模型存取控制注意事項]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/#model-access-control-considerations)。

## 端點

```json
GET /_plugins/_ml/models/{model_id}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `model_id` | 字串 | 要擷取之模型的模型 ID。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `return_content` | Boolean | 若為 `true`，回應會包含 `model_content` 欄位，該欄位儲存使用 [Train API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train/) 訓練之模型的序列化模型內容。預設為 `false`。 |

## 範例請求

```json
GET /_plugins/_ml/models/N8AE1osB0jLkkocYjz7D
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "name" : "all-MiniLM-L6-v2",
  "model_group_id" : "DNrMP6EBzLnYocCrCMsb",
  "algorithm" : "TEXT_EMBEDDING",
  "model_version" : "1",
  "description" : "test model",
  "model_format" : "TORCH_SCRIPT",
  "model_state" : "DEPLOYED",
  "model_content_size_in_bytes" : 91790008,
  "model_content_hash_value" : "c15f0d2e62d872be5b5bc6c84d2e0f4921541e29fefbef51d59cc10a8ae30e0f",
  "model_config" : {
    "model_type" : "bert",
    "embedding_dimension" : 384,
    "framework_type" : "SENTENCE_TRANSFORMERS",
    "all_config" : "{\"_name_or_path\":\"nreimers/MiniLM-L6-H384-uncased\",\"architectures\":[\"BertModel\"],\"attention_probs_dropout_prob\":0.1,\"gradient_checkpointing\":false,\"hidden_act\":\"gelu\",\"hidden_dropout_prob\":0.1,\"hidden_size\":384,\"initializer_range\":0.02,\"intermediate_size\":1536,\"layer_norm_eps\":1e-12,\"max_position_embeddings\":512,\"model_type\":\"bert\",\"num_attention_heads\":12,\"num_hidden_layers\":6,\"pad_token_id\":0,\"position_embedding_type\":\"absolute\",\"transformers_version\":\"4.8.2\",\"type_vocab_size\":2,\"use_cache\":true,\"vocab_size\":30522}"
  },
  "created_time" : 1792071708389,
  "last_updated_time" : 1792071982946,
  "last_registered_time" : 1792071731012,
  "last_deployed_time" : 1792071982946,
  "auto_redeploy_retry_times" : 0,
  "total_chunks" : 10,
  "planning_worker_node_count" : 1,
  "current_worker_node_count" : 1,
  "planning_worker_nodes" : [
    "0b8rV9_nRPWZzG4SHpMPhA"
  ],
  "deploy_to_all_nodes" : true,
  "is_hidden" : false
}
```

## 有效的模型狀態

模型在 OpenSearch 中註冊、部署或取消部署時，會在各種模型狀態之間轉換，以反映其可用性。這些狀態可協助您追蹤模型是否已準備就緒可供使用、載入狀態或失敗情況。

下表列出所有有效的模型狀態。

| 模型狀態          | 說明                                                                                              |
|:---------------------|:---------------------------------------------------------------------------------------------------------|
| `TRAINED`            | 模型已使用 Train API 完成訓練，並已準備就緒可進行預測。已訓練的模型尚未部署。 |
| `REGISTERING`        | 模型正在註冊至叢集。                                          |
| `REGISTERED`         | 模型中繼資料已註冊至叢集，但尚未部署。                                    |
| `DEPLOYED`           | 模型已成功部署／載入至所有符合資格的工作節點，並已準備就緒可進行推論。 |
| `DEPLOYING`          | 模型正在部署至記憶體。                                                 |
| `PARTIALLY_DEPLOYED` | 模型已部署至部分符合資格的工作節點。                                        |
| `UNDEPLOYED`         | 模型已成功從所有節點的記憶體中卸載／取消部署。                        |
| `DEPLOY_FAILED`      | 嘗試將模型部署至叢集節點時發生錯誤。                              |
