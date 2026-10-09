---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "自訂模型"
parent: Using ML models within OpenSearch
grand_parent: Integrating ML models
nav_order: 20
---

# 自訂本機模型
**於 2.9 版推出**
{: .label .label-purple }

若要在本機使用自訂模型，您可以將其上傳至 OpenSearch 叢集。

## 模型支援

OpenSearch 支援下列類型的本機模型：

- 文字嵌入模型
- 稀疏編碼模型
- 交叉編碼器模型
- 問答模型

不支援在 CentOS 7 作業系統上執行本機模型。此外，並非所有本機模型都能在所有硬體和作業系統上執行。
{: .important}

## 準備模型

對於所有模型，您必須在模型 zip 檔案內提供斷詞器 JSON 檔案。

對於稀疏編碼模型，請確認您的輸出格式為 `{"output":<sparse_vector>}`，以便 ML Commons 能夠後處理稀疏向量。

如果您在自己的資料集上微調稀疏模型，您可能也會想使用自己的稀疏斷詞器模型。建議您在斷詞器模型 zip 檔案中提供自己的 [IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) JSON 檔案，因為當您在查詢中使用斷詞器模型時，這可提升查詢效能。或者，您可以使用 OpenSearch 提供的通用[來自 MSMARCO 的 IDF](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1/1.0.0/torch_script/opensearch-neural-sparse-tokenizer-v1-1.0.0.zip)。若未提供 IDF 檔案，每個詞元的預設權重會設為 1，這可能會影響稀疏神經搜尋的效能。  

### 模型格式

若要在 OpenSearch 中使用模型，您必須將模型匯出為可攜式格式。OpenSearch 僅支援 [TorchScript](https://pytorch.org/docs/stable/jit.html) 和 [ONNX](https://onnx.ai/) 格式。

您必須先將模型檔案儲存為 zip，才能將其上傳至 OpenSearch。為確保 ML Commons 能夠上傳您的模型，請先壓縮 TorchScript 檔案再上傳。如需範例，請下載 TorchScript [模型檔案](https://github.com/opensearch-project/ml-commons/blob/2.x/ml-algorithms/src/test/resources/org/opensearch/ml/engine/algorithms/text_embedding/all-MiniLM-L6-v2_torchscript_sentence-transformer.zip)。

此外，您必須為模型 zip 檔案計算 SHA256 總和檢查碼，並在註冊模型時提供。例如，在 UNIX 上，使用下列命令取得總和檢查碼：

```bash
shasum -a 256 sentence-transformers_paraphrase-mpnet-base-v2-1.0.0-onnx.zip
```

### 模型大小

大多數深度學習模型都超過 100 MB，因此難以放入單一文件中。OpenSearch 會將模型檔案分割成較小的區塊，以儲存在模型索引中。為您的 OpenSearch 叢集配置 ML 節點或資料節點時，請務必正確調整 ML 節點的大小，以便在進行 ML 推論時有足夠的記憶體。

## 先決條件 

若要將自訂模型上傳至 OpenSearch，您需要在 OpenSearch 叢集外部準備該模型。您可以使用預先訓練的模型 (例如來自 [Hugging Face](https://huggingface.co/) 的模型)，或依照您的需求訓練新模型。

### 叢集設定

此範例使用沒有專用 ML 節點的簡單設定，並允許在非 ML 節點上執行模型。 

在具有專用 ML 節點的叢集上，請指定 `"only_run_on_ml_node": "true"` 以提升效能。如需詳細資訊，請參閱 [ML Commons 叢集設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/)。

為確保此基本本機設定能夠運作，請指定下列叢集設定：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.allow_registering_model_via_url": "true",
    "plugins.ml_commons.only_run_on_ml_node": "false",
    "plugins.ml_commons.model_access_control_enabled": "true",
    "plugins.ml_commons.native_memory_threshold": "99"
  }
}
```
{% include copy-curl.html %}

從 URL 註冊模型時，請確認來源受信任。從不受信任的來源載入模型可能會造成安全性風險。如需詳細資訊，請參閱 [PyTorch 不受信任模型的安全性指導方針](https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models)。
{: .warning}

## 步驟 1：註冊模型群組

若要註冊模型，您有下列選項：

- 您可以使用 `model_group_id` 將模型版本註冊至現有的模型群組。
- 如果您不使用 `model_group_id`，ML Commons 會建立具有新模型群組的模型。

若要註冊模型群組，請傳送下列請求：

```json
POST /_plugins/_ml/model_groups/_register
{
  "name": "local_model_group",
  "description": "A model group for local models"
}
```
{% include copy-curl.html %}

回應包含模型群組 ID，您將使用該 ID 將模型註冊至此模型群組：

```json
{
 "model_group_id": "wlcnb4kBJ1eYAeTMHlV6",
 "status": "CREATED"
}
```

若要進一步了解模型群組，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。

## 步驟 2：註冊本機模型

若要將本機模型註冊至步驟 1 中建立的模型群組，請傳送 Register Model API 請求。如需 Register Model API 參數的說明，請參閱[註冊模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/)。 

`function_name` 對應於模型類型。對於文字嵌入模型，請將此參數設為 `TEXT_EMBEDDING`。對於稀疏編碼模型，請將此參數設為 `SPARSE_ENCODING` 或 `SPARSE_TOKENIZE`。對於交叉編碼器模型，請將此參數設為 `TEXT_SIMILARITY`。對於問答模型，請將此參數設為 `QUESTION_ANSWERING`。在此範例中，請將 `function_name` 設為 `TEXT_EMBEDDING`，因為您要註冊文字嵌入模型。 

提供步驟 1 中的模型群組 ID，並傳送下列請求：

```json
POST /_plugins/_ml/models/_register
{
  "name": "huggingface/sentence-transformers/msmarco-distilbert-base-tas-b",
  "version": "1.0.1",
  "model_group_id": "wlcnb4kBJ1eYAeTMHlV6",
  "description": "This is a port of the DistilBert TAS-B Model to sentence-transformers model: It maps sentences & paragraphs to a 768 dimensional dense vector space and is optimized for the task of semantic search.",
  "function_name": "TEXT_EMBEDDING",
  "model_format": "TORCH_SCRIPT",
  "model_content_size_in_bytes": 266352827,
  "model_content_hash_value": "acdc81b652b83121f914c5912ae27c0fca8fabf270e6f191ace6979a19830413",
  "model_config": {
    "model_type": "distilbert",
    "embedding_dimension": 768,
    "framework_type": "sentence_transformers",
    "all_config": "{\"_name_or_path\":\"old_models/msmarco-distilbert-base-tas-b/0_Transformer\",\"activation\":\"gelu\",\"architectures\":[\"DistilBertModel\"],\"attention_dropout\":0.1,\"dim\":768,\"dropout\":0.1,\"hidden_dim\":3072,\"initializer_range\":0.02,\"max_position_embeddings\":512,\"model_type\":\"distilbert\",\"n_heads\":12,\"n_layers\":6,\"pad_token_id\":0,\"qa_dropout\":0.1,\"seq_classif_dropout\":0.2,\"sinusoidal_pos_embds\":false,\"tie_weights_\":true,\"transformers_version\":\"4.7.0\",\"vocab_size\":30522}"
  },
  "created_time": 1676073973126,
  "url": "https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/msmarco-distilbert-base-tas-b/1.0.1/torch_script/sentence-transformers_msmarco-distilbert-base-tas-b-1.0.1-torch_script.zip"
}
```
{% include copy-curl.html %}

請注意，在 OpenSearch Dashboards 中，將 `all_config` 欄位內容以三個引號 (`"""`) 包住，會自動逸出欄位內的引號，並提供更好的可讀性：

```json
POST /_plugins/_ml/models/_register
{
  "name": "huggingface/sentence-transformers/msmarco-distilbert-base-tas-b",
  "version": "1.0.1",
  "model_group_id": "wlcnb4kBJ1eYAeTMHlV6",
  "description": "This is a port of the DistilBert TAS-B Model to sentence-transformers model: It maps sentences & paragraphs to a 768 dimensional dense vector space and is optimized for the task of semantic search.",
  "function_name": "TEXT_EMBEDDING",
  "model_format": "TORCH_SCRIPT",
  "model_content_size_in_bytes": 266352827,
  "model_content_hash_value": "acdc81b652b83121f914c5912ae27c0fca8fabf270e6f191ace6979a19830413",
  "model_config": {
    "model_type": "distilbert",
    "embedding_dimension": 768,
    "framework_type": "sentence_transformers",
    "all_config": """{"_name_or_path":"old_models/msmarco-distilbert-base-tas-b/0_Transformer","activation":"gelu","architectures":["DistilBertModel"],"attention_dropout":0.1,"dim":768,"dropout":0.1,"hidden_dim":3072,"initializer_range":0.02,"max_position_embeddings":512,"model_type":"distilbert","n_heads":12,"n_layers":6,"pad_token_id":0,"qa_dropout":0.1,"seq_classif_dropout":0.2,"sinusoidal_pos_embds":false,"tie_weights_":true,"transformers_version":"4.7.0","vocab_size":30522}"""
  },
  "created_time": 1676073973126,
  "url": "https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/msmarco-distilbert-base-tas-b/1.0.1/torch_script/sentence-transformers_msmarco-distilbert-base-tas-b-1.0.1-torch_script.zip"
}
```
{% include copy.html %}

OpenSearch 會傳回註冊作業的工作 ID：

```json
{
  "task_id": "cVeMb4kBJ1eYAeTMFFgj",
  "status": "CREATED"
}
```

若要檢查作業的狀態，請將工作 ID 提供給 [Get task]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)：

```bash
GET /_plugins/_ml/tasks/cVeMb4kBJ1eYAeTMFFgj
```
{% include copy-curl.html %}

作業完成後，狀態會變更為 `COMPLETED`：

```json
{
  "model_id": "cleMb4kBJ1eYAeTMFFg4",
  "task_type": "REGISTER_MODEL",
  "function_name": "TEXT_EMBEDDING",
  "state": "COMPLETED",
  "worker_node": [
    "XPcXLV7RQoi5m8NI_jEOVQ"
  ],
  "create_time": 1689793598499,
  "last_update_time": 1689793598530,
  "is_async": false
}
```

請記下傳回的 `model_id`，因為您需要它來部署模型。

## 步驟 3：部署模型

部署作業會從模型索引讀取模型的區塊，然後建立模型實例並載入記憶體。模型越大，切分出的區塊就越多，載入記憶體所需的時間也越長。

若要部署已註冊的模型，請在下列請求中提供步驟 3 取得的模型 ID：

```bash
POST /_plugins/_ml/models/cleMb4kBJ1eYAeTMFFg4/_deploy
```
{% include copy-curl.html %}

回應包含任務 ID，您可以用它來檢查部署作業的狀態：

```json
{
  "task_id": "vVePb4kBJ1eYAeTM7ljG",
  "status": "CREATED"
}
```

如同上一個步驟，呼叫 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 來檢查作業狀態：

```bash
GET /_plugins/_ml/tasks/vVePb4kBJ1eYAeTM7ljG
```
{% include copy-curl.html %}

當作業完成時，狀態會變更為 `COMPLETED`：

```json
{
  "model_id": "cleMb4kBJ1eYAeTMFFg4",
  "task_type": "DEPLOY_MODEL",
  "function_name": "TEXT_EMBEDDING",
  "state": "COMPLETED",
  "worker_node": [
    "n-72khvBTBi3bnIIR8FTTw"
  ],
  "create_time": 1689793851077,
  "last_update_time": 1689793851101,
  "is_async": true
}
```

如果叢集或節點重新啟動，您需要重新部署模型。若要瞭解如何設定自動重新部署，請參閱[模型部署設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/#model-deployment-settings)。
{: .tip} 

## 步驟 4（選用）：測試模型

使用 [Predict API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/) 來測試模型。

若為文字嵌入模型，請傳送下列請求：

```json
POST /_plugins/_ml/_predict/text_embedding/cleMb4kBJ1eYAeTMFFg4
{
  "text_docs":[ "today is sunny"],
  "return_number": true,
  "target_response": ["sentence_embedding"]
}
```
{% include copy-curl.html %}

回應包含所提供句子的文字嵌入：

```json
{
  "inference_results" : [
    {
      "output" : [
        {
          "name" : "sentence_embedding",
          "data_type" : "FLOAT32",
          "shape" : [
            768
          ],
          "data" : [
            0.25517133,
            -0.28009856,
            0.48519906,
            ...
          ]
        }
      ]
    }
  ]
}
```

若為稀疏編碼模型，請傳送下列請求：

```json
POST /_plugins/_ml/_predict/sparse_encoding/cleMb4kBJ1eYAeTMFFg4
{
  "text_docs":[ "today is sunny"]
}
```
{% include copy-curl.html %}

回應包含詞元與權重：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "output",
          "dataAsMap": {
            "response": [
              {
                "saturday": 0.48336542,
                "week": 0.1034762,
                "mood": 0.09698499,
                "sunshine": 0.5738209,
                "bright": 0.1756877,
                ...
              }
          }
        }
    }
}
```

## 步驟 5：使用模型進行搜尋

若要瞭解如何使用模型進行向量搜尋，請參閱 [AI 搜尋方法]({{site.url}}{{site.baseurl}}/vector-search/ai-search/#ai-search-methods)。

## 問答模型

問答模型會從給定的上下文中擷取問題的答案。ML Commons 支援 `text` 格式的上下文。

若要註冊問答模型，請以下列格式傳送請求。將 `function_name` 指定為 `QUESTION_ANSWERING`：

```json
POST /_plugins/_ml/models/_register
{
    "name": "question_answering",
    "version": "1.0.0",
    "function_name": "QUESTION_ANSWERING",
    "description": "test model",
    "model_format": "TORCH_SCRIPT",
    "model_group_id": "lN4AP40BKolAMNtR4KJ5",
    "model_content_hash_value": "e837c8fc05fd58a6e2e8383b319257f9c3859dfb3edc89b26badfaf8a4405ff6",
    "model_config": { 
        "model_type": "bert",
        "framework_type": "huggingface_transformers"
    },
    "url": "https://github.com/opensearch-project/ml-commons/blob/main/ml-algorithms/src/test/resources/org/opensearch/ml/engine/algorithms/question_answering/question_answering_pt.zip?raw=true"
}
```
{% include copy-curl.html %}

接著傳送請求來部署模型：

```json
POST _plugins/_ml/models/{model_id}/_deploy
```
{% include copy-curl.html %}

若要測試問答模型，請傳送下列請求。此請求需要一個 `question` 以及將從中產生答案的相關 `context`：

```json
POST /_plugins/_ml/_predict/question_answering/{model_id}
{
  "question": "Where do I live?"
  "context": "My name is John. I live in New York"
}
```
{% include copy-curl.html %}

回應會根據上下文提供答案：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "result": "New York"
        }
    }
}
```
