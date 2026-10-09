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

## 範例請求

```json
GET /_plugins/_ml/models/N8AE1osB0jLkkocYjz7D
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "name" : "all-MiniLM-L6-v2_onnx",
  "algorithm" : "TEXT_EMBEDDING",
  "version" : "1",
  "model_format" : "TORCH_SCRIPT",
  "model_state" : "DEPLOYED",
  "model_content_size_in_bytes" : 83408741,
  "model_content_hash_value" : "9376c2ebd7c83f99ec2526323786c348d2382e6d86576f750c89ea544d6bbb14",
  "model_config" : {
      "model_type" : "bert",
      "embedding_dimension" : 384,
      "framework_type" : "SENTENCE_TRANSFORMERS",
      "all_config" : """{"_name_or_path":"nreimers/MiniLM-L6-H384-uncased","architectures":["BertModel"],"attention_probs_dropout_prob":0.1,"gradient_checkpointing":false,"hidden_act":"gelu","hidden_dropout_prob":0.1,"hidden_size":384,"initializer_range":0.02,"intermediate_size":1536,"layer_norm_eps":1e-12,"max_position_embeddings":512,"model_type":"bert","num_attention_heads":12,"num_hidden_layers":6,"pad_token_id":0,"position_embedding_type":"absolute","transformers_version":"4.8.2","type_vocab_size":2,"use_cache":true,"vocab_size":30522}"""
  },
  "created_time" : 1665961344044,
  "last_uploaded_time" : 1665961373000,
  "last_loaded_time" : 1665961815959,
  "total_chunks" : 9
}
```

## 有效的模型狀態

當模型在 OpenSearch 中註冊、部署或解除部署時，會經歷各種反映其可用性的模型狀態。這些狀態可協助您追蹤模型是否可供使用、載入狀態或失敗情況。

下表列出所有有效的模型狀態。

| 模型狀態          | 說明                                                                                              |
|:---------------------|:---------------------------------------------------------------------------------------------------------|
| `REGISTERING `       | 模型正在註冊至叢集。                                          |
| `REGISTERED`         | 模型中繼資料已註冊至叢集，但尚未部署。                                    |
| `DEPLOYED`           | 模型已成功部署/載入至所有符合資格的工作節點，並可進行推論。 |
| `DEPLOYING`          | 模型正在部署至記憶體。                                                 |
| `PARTIALLY_DEPLOYED` | 模型已部署至部分符合資格的工作節點。                                        |
| `UNDEPLOYED`         | 模型已成功從所有節點的記憶體卸載/解除部署。                        |
| `DEPLOY_FAILED`      | 嘗試將模型部署至叢集節點時發生錯誤。                              |
