---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "註冊模型"
parent: Model APIs
grand_parent: ML APIs
nav_order: 10
---

# Register Model API

特定模型的所有版本都存放在同一個模型群組中。您可以先[註冊模型群組]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-group-apis/register-model-group/)，再將模型註冊至該群組，或註冊模型的第一個版本，藉此建立群組。叢集中的每個模型群組名稱都必須全域唯一。 

如果您在未先註冊模型群組的情況下註冊模型的第一個版本，系統會自動建立新的模型群組，並使用下列名稱與存取層級：

- 名稱：新模型群組的名稱將與模型相同。由於模型群組名稱必須唯一，請確保您的模型名稱不會與叢集中的任何模型群組同名。 
- 存取層級：新模型群組的存取層級取決於您在請求中傳入的 `access_mode`、`backend_roles` 和 `add_all_backend_roles` 參數。如果您未提供這三個參數中的任何一個，則當叢集已啟用模型存取控制時，新模型群組將為 `private`；當模型存取控制已停用時，則為 `public`。新註冊的模型會是指派給該模型群組的第一個模型版本。 

建立模型群組後，請提供其 `model_group_id`，以將新的模型版本註冊至該模型群組。在此情況下，模型名稱不必唯一。

如果您使用 OpenSearch 提供的[預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models#supported-pretrained-models)，建議您先為這些模型註冊具有唯一名稱的模型群組。接著，將預先訓練模型註冊為該模型群組的版本。這可確保每個模型群組都具有全域唯一的模型群組名稱。
{: .tip}

如需此 API 使用者存取權的相關資訊，請參閱[模型存取控制注意事項]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/#model-access-control-considerations)。

如果模型大小超過 10 MB，OpenSearch 會將其分割為較小的區塊，並將這些區塊儲存在模型的索引中。

## 端點

```json
POST /_plugins/_ml/models/_register
```

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `deploy` | 布林值 | 是否在註冊模型後部署模型。部署作業是透過呼叫 [Deploy Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/deploy-model/) 來執行。預設為 `false`。 |

## 請求本文欄位

請求本文欄位取決於模型類型。

### 註冊 OpenSearch 提供的預先訓練模型

OpenSearch 提供數個預先訓練模型。如需更多資訊，請參閱 [OpenSearch 提供的預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/)。

#### 註冊預先訓練的文字嵌入模型

若要註冊預先訓練的文字嵌入模型，唯一必要的參數是 `name`、`version` 和 `model_format`。

下表列出可用的請求欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:---  | :--- | :--- | :---
`name`| 字串 | 必要 | 模型名稱。 |
`model_id` | 字串 | 選用 | 模型的唯一識別碼。若省略，OpenSearch 會自動產生。 |
`version` | 字串 | 必要 | 模型版本。 |
`model_format` | 字串 | 必要 | 模型檔案的可攜式格式。有效值為 `TORCH_SCRIPT` 和 `ONNX`。 |
`description` | 字串 | 選用| 模型描述。 |
`model_group_id` | 字串 | 選用 | 要註冊模型的模型群組 ID。
`provisioned_by` | 字串 | 選用 | 選用的歸屬標籤，用於識別註冊模型的外掛程式或用戶端（例如 `flow-framework`）。會包含在 ML 統計指標中。

#### 註冊預先訓練的稀疏編碼模型

若要註冊預先訓練的稀疏編碼模型，您必須將函式名稱設為 `SPARSE_ENCODING` 或 `SPARSE_TOKENIZE`。

下表列出可用的請求欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:---  | :--- | :--- | :---
`name`| 字串 | 必要 | 模型名稱。 |
`model_id` | 字串 | 選用 | 模型的唯一識別碼。若省略，OpenSearch 會自動產生一個。 |
`version` | 字串 | 必要 | 模型版本。 |
`model_format` | 字串 | 必要 | 模型檔案的可攜式格式。有效值為 `TORCH_SCRIPT` 和 `ONNX`。 |
`function_name` | 字串 | 必要 | 若是文字嵌入模型，請將此參數設為 `TEXT_EMBEDDING`。若是稀疏編碼模型，請將此參數設為 `SPARSE_ENCODING` 或 `SPARSE_TOKENIZE`。若是交叉編碼器模型，請將此參數設為 `TEXT_SIMILARITY`。若是問答模型，請將此參數設為 `QUESTION_ANSWERING`。
`model_content_hash_value` | 字串 | 必要 | 使用 SHA-256 雜湊演算法產生的模型內容雜湊值。
`url` | 字串 | 必要 | 包含模型的 URL。 |
`description` | 字串 | 選用| 模型說明。 |
`model_group_id` | 字串 | 選用 | 要註冊此模型之目標模型群組的 ID。
`provisioned_by` | 字串 | 選用 | 選用的歸屬標籤，用於識別註冊該模型的外掛程式或用戶端（例如 `flow-framework`）。會納入 ML 統計指標。

### 註冊自訂模型 

若要在 OpenSearch 叢集內本機使用自訂模型，您需要提供該模型的 URL 與組態物件。如需更多資訊，請參閱[自訂本機模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/custom-local-models/)。

下表列出可用的請求欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:---  | :--- | :--- | :---
`name`| 字串 | 必要 | 模型名稱。 |
`model_id` | 字串 | 選用 | 模型的唯一識別碼。若省略，OpenSearch 會自動產生。 |
`version` | 字串 | 必要 | 模型版本。 |
`model_format` | 字串 | 必要 | 模型檔案的可攜式格式。有效值為 `TORCH_SCRIPT` 與 `ONNX`。 |
`function_name` | 字串 | 必要 | 將此參數設定為 `TEXT_EMBEDDING`、`SPARSE_ENCODING`、`SPARSE_TOKENIZE`、`TEXT_SIMILARITY` 或 `QUESTION_ANSWERING`。
`model_content_hash_value` | 字串 | 必要 | 使用 SHA-256 雜湊演算法產生的模型內容雜湊值。
[`model_config`](#the-model_config-object)  | 物件 | 必要 | 模型的組態，包括 `model_type`、`embedding_dimension` 與 `framework_type`。選用的 `all_config` JSON 字串包含所有模型組態。`additional_config` 物件包含預先訓練模型的對應 `space_type`，或自訂模型的指定 `space_type`。請參閱[空間類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-spaces/#distance-calculation)。 |
`url` | 字串 | 必要 | 包含該模型的 URL。 |
`description` | 字串 | 選用| 模型描述。 |
`model_group_id` | 字串 | 選用 | 要註冊此模型之模型群組的模型群組 ID。
`is_enabled`| 布林值 | 選用 | 指定模型是否已啟用。停用模型會使其無法用於 Predict API 請求，無論模型的部署狀態為何。預設為 `true`。
`rate_limiter` | 物件 | 選用 | 限制任何使用者可對該模型呼叫 Predict API 的次數。如需更多資訊，請參閱[限制推論呼叫速率]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#rate-limiting-inference-calls)。
`interface`| 物件 | 選用 | 模型的介面。如需更多資訊，請參閱[介面](#the-interface-parameter)。|
`provisioned_by` | 字串 | 選用 | 選用的歸屬標籤，用於識別註冊該模型的外掛程式或用戶端（例如 `flow-framework`）。會包含在 ML 統計指標中。

#### `model_config` 物件

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- 
| `model_type` | 字串 | 模型類型，例如 `bert`。對於 Hugging Face 模型，模型類型會於 `config.json` 中指定。範例請參閱 [`all-MiniLM-L6-v2` Hugging Face 模型 `config.json`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/blob/main/config.json#L15)。必要。 |
| `embedding_dimension` | 整數 | 模型產生之稠密向量的維度。對於 Hugging Face 模型，維度會於模型卡中指定。例如，在 [`all-MiniLM-L6-v2` Hugging Face 模型卡](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) 中，`384 dimensional dense vector space` 敘述指定 384 為嵌入維度。必要。 |
| `framework_type` | 字串  | 模型使用的架構。OpenSearch 支援 `sentence_transformers` 與 `huggingface_transformers` 架構。`sentence_transformers` 模型會直接輸出文字嵌入，因此 OpenSearch 不會執行任何後處理。對於 `huggingface_transformers`，OpenSearch 會套用均值池化進行後處理，以取得文字嵌入。詳情請參閱範例 [`all-MiniLM-L6-v2` Hugging Face 模型](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)。必要。 |
| `all_config` | 字串 | 此欄位供參考之用。您可以在此欄位中指定所有模型組態。例如，如果您使用 Hugging Face 模型，可以將 `config.json` 檔案縮減為一行，並將其內容儲存於 `all_config` 欄位中。模型上傳後，您可以使用 get model API 操作，取得儲存於此欄位中的所有模型組態。選用。 |
| `additional_config` | 物件 | 其他模型組態。包含 `space_type`，其指定 k-NN 搜尋的距離計量。對於 OpenSearch 提供的預先訓練模型，此值會自動設為對應的計量（例如 `huggingface/sentence-transformers/all-distilroberta-v1` 的 `l2`）。對於自訂模型，請指定您偏好的空間類型。選用。請參閱[空間類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-spaces/#distance-calculation)。 |

您可以使用 `model_config` 物件中的下列選用欄位，進一步自訂預先訓練句子轉換器模型的後處理邏輯。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `pooling_mode` | 字串 | 後處理模型輸出，可為 `mean`、`mean_sqrt_len`、`max`、`weightedmean`、`cls`、`lasttoken` 或 `none`。對於僅解碼器模型（例如 Qwen3-Embedding），請使用 `lasttoken`，此類模型的最後一個非填充詞元會透過因果注意力擷取累積脈絡。對於已提供預先池化輸出的模型（例如 `sentence_embedding` 或 `pooler_output`），請使用 `none` 以略過額外的池化。|
| `normalize_result` | 布林值 | 設為 `true` 時，會將模型輸出正規化，以便縮放至模型的標準範圍。 |

### 註冊託管於第三方平台的模型

若要註冊託管於第三方平台的模型，您可以先建立獨立連接器並提供該連接器的 ID，或為模型指定內部連接器。如需更多資訊，請參閱[為第三方 ML 平台建立連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

下表列出可用的請求欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:---  | :--- | :--- | :---
`name`| 字串 | 必要 | 模型名稱。 |
`function_name` | 字串 | 必要 | 將此參數設定為 `remote`。
`connector_id` | 字串 | 必要 | 託管於第三方平台之模型的獨立連接器 ID。如需更多資訊，請參閱[獨立連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/#creating-a-standalone-connector)。您必須提供 `connector_id` 或 `connector` 其中之一。
`connector` | 物件 | 必要 | 包含託管於第三方平台之模型連接器的規格。如需更多資訊，請參閱[為特定模型建立連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/#creating-a-connector-for-a-specific-model)。您必須提供 `connector_id` 或 `connector` 其中之一。
`model_id` | 字串 | 選用 | 模型的唯一識別碼。若省略，OpenSearch 會自動產生。 |
`description` | 字串 | 選用| 模型描述。 |
`model_group_id` | 字串 | 選用 | 要將此模型註冊至的模型群組之模型群組 ID。
`is_enabled`| 布林值 | 選用 | 指定模型是否已啟用。停用模型會使其無法用於 Predict API 請求，無論模型的部署狀態為何。預設為 `true`。
`rate_limiter` | 物件 | 選用 | 限制任何使用者可以對模型呼叫 Predict API 的次數。如需更多資訊，請參閱[限制推論呼叫速率]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#rate-limiting-inference-calls)。
`guardrails`| 物件 | 選用 | 模型輸入的防護機制。如需更多資訊，請參閱[防護機制](#the-guardrails-parameter)。|
`interface`| 物件 | 選用 | 模型的介面。如需更多資訊，請參閱[介面](#the-interface-parameter)。|
`batch_inference_config` | 物件 | 選用 | 為外部託管的模型設定批次推論。如需更多資訊，請參閱[`batch_inference_config` 參數](#the-batch_inference_config-parameter)。 |
`provisioned_by` | 字串 | 選用 | 選用的歸屬標籤，用於識別註冊模型的外掛程式或用戶端（例如 `flow-framework`）。會包含在 ML 統計指標中。

### 存取控制與部署欄位

下列選用欄位適用於所有模型類型。

欄位 | 資料類型 | 必要/選用 | 說明
:---  | :--- | :--- | :---
`access_mode` | 字串 | 選用 | 為此模型建立的模型群組的存取模式。有效值為 `public`、`private` 和 `restricted`。僅在您註冊模型的第一個版本且未提供 `model_group_id` 時適用。如需詳細資訊，請參閱 [Register Model Group API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-group-apis/register-model-group/)。
`backend_roles` | 陣列 | 選用 | 要新增至為此模型建立之模型群組的模型擁有者後端角色清單。僅在未提供 `model_group_id` 時適用。不能與 `add_all_backend_roles` 同時指定。
`add_all_backend_roles` | 布林值 | 選用 | 若為 `true`，則會將模型擁有者的所有後端角色新增至為此模型建立的模型群組。僅在未提供 `model_group_id` 時適用。不能與 `backend_roles` 同時指定。管理員使用者無法將此參數設為 `true`。
`deploy_setting` | 物件 | 選用 | 模型的部署設定。支援 `model_ttl_minutes` 欄位（Long），其指定部署的模型在幾分鐘後自動取消部署（預設為 `-1`，表示模型不會自動取消部署），以及 `is_auto_deploy_enabled` 欄位（布林值），其指定已取消部署的模型在收到 Predict API 請求時是否自動部署（預設為 `true`）。
`model_node_ids` | 陣列 | 選用 | 在註冊後部署模型時（`deploy=true`），要在其上部署模型的節點 ID 清單。

### `guardrails` 參數

防護機制是大型語言模型 (LLM) 的安全措施。它們提供一組規則與邊界，控制 LLM 的行為方式及其產生的輸出類型。 

若要註冊具有防護機制的外部託管模型，請提供 `guardrails` 參數，該參數支援下列欄位。所有欄位皆為選用。

欄位 | 資料類型 | 說明
:---  | :--- | :---
`type` | 字串 | 防護機制類型。有效值為 [`local_regex`](#example-request-regex-and-stopword-validation) 與 [`model`](#example-request-guardrail-model-validation)。使用 `local_regex` 時，您可以指定正規表示式或停用詞。使用 `model` 時，您可以指定防護機制模型。更多資訊請參閱[防護機制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/guardrails/)。 
`input_guardrail`| 物件 |  模型輸入的防護機制。 
`output_guardrail`| 物件 |  模型輸出的防護機制。 
`stop_words`| 物件 | 包含用於模型輸入/輸出驗證之停用詞的索引清單。若模型提示/回應包含任何索引中的停用詞，則對模型的 predict 請求會被拒絕。 
`index_name`| 物件 | 儲存停用詞的索引名稱。 
`source_fields`| 物件 | 儲存停用詞的欄位名稱。 
`regex`| 物件 |  用於輸入/輸出驗證的正規表示式。若模型提示/回應符合該正規表示式，則對模型的 predict 請求會被拒絕。 
`model_id`| 字串  | 用於驗證使用者輸入與 LLM 輸出的防護機制模型。 
`response_filter`| 字串 | 包含防護機制模型回應之欄位的點路徑。 
`response_validation_regex`| 字串 | 用於驗證防護機制模型回應的正規表示式。     

### `interface` 參數

模型介面提供了一種高度靈活的方式，可透過 JSON schema 語法為所有本機深度學習模型與外部託管模型新增任意中繼資料註解。此註解會在模型呼叫期間，對模型的輸入與輸出欄位啟動驗證檢查。驗證檢查可確保模型執行推論前後，輸入與輸出欄位皆為正確的格式。

若要使用模型介面註冊模型，請提供 `interface` 參數，其支援下列欄位。

欄位 | 資料類型 | 說明                         
:---  | :--- |:------------------------------------
`input`| 物件 | 模型輸入的 JSON schema。 |
`output`| 物件 | 模型輸出的 JSON schema。 |

輸入與輸出欄位會依據所提供的 JSON schema 進行評估。您不需要同時提供這兩個欄位。

#### 連接器模型介面

為了簡化您的工作流程，您可以使用其中一種[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)格式，透過連接器註冊外部託管的模型。若您這麼做，系統會在模型註冊期間自動為此連接器產生預先定義的模型介面。預先定義的模型介面會根據連接器藍圖與模型的中繼資料產生，因此您在建立連接器時必須嚴格遵循藍圖，以避免發生錯誤。

下列連接器藍圖支援建立預先定義的模型介面：

- [Amazon Comprehend](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/amazon_comprehend_connector_blueprint.md)
- [Amazon Textract](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/amazon_textract_connector_blueprint.md)（請注意，預先定義的模型介面僅適用於 `DetectDocumentText` API；不支援 `DetectEnities` API）。
- [Amazon Bedrock AI21 Labs Jurassic](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/bedrock_connector_ai21labs_jurassic_blueprint.md)
- [Amazon Bedrock Anthropic Claude 3](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/bedrock_connector_anthropic_claude3_blueprint.md)
- [Amazon Bedrock Anthropic Claude](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/bedrock_connector_anthropic_claude_blueprint.md)
- [Amazon Bedrock Cohere Embed English v3](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/bedrock_connector_cohere_cohere.embed-english-v3_blueprint.md)
- [Amazon Bedrock Cohere Embed Multilingual v3](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/bedrock_connector_cohere_cohere.embed-multilingual-v3_blueprint.md)
- [Amazon Bedrock Titan Text Embeddings](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/bedrock_connector_titan_embedding_blueprint.md)
- [Amazon Bedrock Titan Multimodal Embeddings](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/bedrock_connector_titan_multimodal_embedding_blueprint.md)

若要進一步了解連接器藍圖，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)。

### `batch_inference_config` 參數

使用 `batch_inference_config` 參數可限制 OpenSearch 在單次呼叫中傳送給模型的輸入字串數量與大小，讓每次呼叫都維持在外部託管模型的限制內。您也可以啟用動態批次處理，將個別請求合併以提升整體輸送量。您必須將 `max_items_per_request` 與 `max_bytes_per_request` 中至少一項設為正值。

下表列出 `batch_inference_config` 欄位。

欄位 | 資料類型 | 必要/選用 | 預設 | 說明
:---  | :--- | :--- | :--- | :---
`max_items_per_request` | 整數 | 選用 | `-1`（停用） | 單次呼叫模型時輸入字串的數量上限。省略此參數或將其設為 `-1` 即可停用此限制。
`max_bytes_per_request` | 長整數 | 選用 | `-1`（停用） | 單次呼叫模型時輸入字串的合併大小上限（以位元組為單位）。此限制不包含連接器請求本文中的其他欄位，因此請將此值設為低於端點的承載限制，以保留空間給這些欄位。省略此參數或將其設為 `-1` 即可停用此限制。
`dynamic_batching` | 物件 | 選用 | | 設定動態批次處理。
`dynamic_batching.enabled` | 布林值 | 選用 | `false` | 當設為 `true` 時，OpenSearch 會先動態批次處理請求，再將其傳送給模型。動態批次處理需要將 `max_items_per_request` 或 `max_bytes_per_request` 設為正值。
`dynamic_batching.flush_timeout_ms` | 長整數 | 選用 | `50` | 第一個請求在模型以批次方式被呼叫前，等待其他請求的最長時間（以毫秒為單位）。有效值為 1--10,000。若累積的輸入字串在逾時前達到 `max_items_per_request` 或 `max_bytes_per_request`，批次可能會提前被呼叫。

## 範例請求

下列範例顯示如何註冊不同類型的模型。

### 範例請求：OpenSearch 提供的文字嵌入模型

```json
POST /_plugins/_ml/models/_register
{
  "name": "huggingface/sentence-transformers/msmarco-distilbert-base-tas-b",
  "version": "1.0.3",
  "model_group_id": "Z1eQf4oB5Vm0Tdw8EIP2",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

### 範例請求：OpenSearch 提供的稀疏編碼模型

```json
POST /_plugins/_ml/models/_register
{
    "name": "amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-distill",
    "version": "1.0.0",
    "model_group_id": "Z1eQf4oB5Vm0Tdw8EIP2",
    "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

### 範例請求：自訂模型

下列範例請求會註冊名為 `all-MiniLM-L6-v2` 的 NLP 句子轉換模型 `1.0.0` 版。

```json
POST /_plugins/_ml/models/_register
{
    "name": "all-MiniLM-L6-v2",
    "version": "1.0.0",
    "description": "test model",
    "model_format": "TORCH_SCRIPT",
    "function_name": "TEXT_EMBEDDING",
    "model_group_id": "FTNlQ4gBYW0Qyy5ZoxfR",
    "model_content_hash_value": "c15f0d2e62d872be5b5bc6c84d2e0f4921541e29fefbef51d59cc10a8ae30e0f",
    "model_config": {
        "model_type": "bert",
        "embedding_dimension": 384,
        "framework_type": "sentence_transformers",
       "all_config": "{\"_name_or_path\":\"nreimers/MiniLM-L6-H384-uncased\",\"architectures\":[\"BertModel\"],\"attention_probs_dropout_prob\":0.1,\"gradient_checkpointing\":false,\"hidden_act\":\"gelu\",\"hidden_dropout_prob\":0.1,\"hidden_size\":384,\"initializer_range\":0.02,\"intermediate_size\":1536,\"layer_norm_eps\":1e-12,\"max_position_embeddings\":512,\"model_type\":\"bert\",\"num_attention_heads\":12,\"num_hidden_layers\":6,\"pad_token_id\":0,\"position_embedding_type\":\"absolute\",\"transformers_version\":\"4.8.2\",\"type_vocab_size\":2,\"use_cache\":true,\"vocab_size\":30522}"
    },
    "url": "https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-MiniLM-L6-v2/1.0.1/torch_script/sentence-transformers_all-MiniLM-L6-v2-1.0.1-torch_script.zip"
}
```
{% include copy-curl.html %}

### 範例請求：使用獨立連接器的外部託管模型

```json
POST /_plugins/_ml/models/_register
{
    "name": "openAI-gpt-4o-mini",
    "function_name": "remote",
    "model_group_id": "1jriBYsBq7EKuKzZX131",
    "description": "test model",
    "connector_id": "a1eMb4kBJ1eYAeTMAljY"
}
```
{% include copy-curl.html %}

### 範例請求：外部託管模型並在模型中指定連接器

```json
POST /_plugins/_ml/models/_register
{
    "name": "openAI-gpt-4o-mini: internal connector",
    "function_name": "remote",
    "model_group_id": "lEFGL4kB4ubqQRzegPo2",
    "description": "test model",
    "connector": {
        "name": "OpenAI Connector",
        "description": "The connector to public OpenAI model service for gpt-4o-mini",
        "version": 1,
        "protocol": "http",
        "parameters": {
            "endpoint": "api.openai.com",
            "max_tokens": 7,
            "temperature": 0,
            "model": "gpt-4o-mini"
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
                "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": [{\"role\": \"user\", \"content\": \"${parameters.prompt}\"}], \"max_tokens\": ${parameters.max_tokens}, \"temperature\": ${parameters.temperature} }"
            }
        ]
    }
}
```
{% include copy-curl.html %}

### 範例請求：正規表示式與停用詞驗證

下列範例使用正規表示式與一組停用詞來驗證 LLM 回應：

```json
POST /_plugins/_ml/models/_register
{
  "name": "openAI-gpt-4o-mini",
  "function_name": "remote",
  "model_group_id": "1jriBYsBq7EKuKzZX131",
  "description": "test model",
  "connector_id": "a1eMb4kBJ1eYAeTMAljY",
  "guardrails": {
    "type": "local_regex",
    "input_guardrail": {
      "stop_words": [
        {
          "index_name": "stop_words_input",
          "source_fields": ["title"]
        }
      ],
      "regex": ["regex1", "regex2"]
    },
    "output_guardrail": {
      "stop_words": [
        {
          "index_name": "stop_words_output",
          "source_fields": ["title"]
        }
      ],
      "regex": ["regex1", "regex2"]
    }
  }
}
```
{% include copy-curl.html %}

完整範例請參閱[使用停用詞與正規表示式驗證輸入/輸出]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/guardrails/#validating-inputoutput-using-stopwords-and-regex)。

### 範例請求：防護機制模型驗證

下列範例使用防護機制模型來驗證 LLM 回應：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "Bedrock Claude Sonnet 4.6 model with guardrails model",
    "function_name": "remote",
    "model_group_id": "ppSmpo8Bi-GZ0tf1i7cD",
    "description": "Bedrock Claude Sonnet 4.6 model with guardrails model",
    "connector_id": "xnJjDZABNFJeYR3IPvTO",
    "guardrails": {
        "input_guardrail": {
            "model_id": "o3JaDZABNFJeYR3I2fRV",
            "response_validation_regex": "^\\s*\"[Aa]ccept\"\\s*$"
        },
        "output_guardrail": {
            "model_id": "o3JaDZABNFJeYR3I2fRV",
            "response_validation_regex": "^\\s*\"[Aa]ccept\"\\s*$"
        },
        "type": "model"
    }
}
```
{% include copy-curl.html %}

如需完整範例，請參閱[使用防護機制模型驗證輸入/輸出]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/guardrails/#validating-inputoutput-using-a-guardrail-model)。

### 範例請求：具有介面的外部託管模型

```json
POST /_plugins/_ml/models/_register
{
    "name": "openAI-gpt-4o-mini",
    "function_name": "remote",
    "description": "test model",
    "connector_id": "A-j7K48BZzNMh1sWVdJu",
    "interface": {
        "input": {
            "properties": {
                "parameters": {
                    "properties": {
                        "messages": {
                            "type": "string",
                            "description": "This is a test description field"
                        }
                    }
                }
            }
        },
        "output": {
            "properties": {
                "inference_results": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "output": {
                                "type": "array",
                                "items": {
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "description": "This is a test description field"
                                        },
                                        "dataAsMap": {
                                            "type": "object",
                                            "description": "This is a test description field"
                                        }
                                    }
                                },
                                "description": "This is a test description field"
                            },
                            "status_code": {
                                "type": "integer",
                                "description": "This is a test description field"
                            }
                        }
                    },
                    "description": "This is a test description field"
                }
            }
        }
    }
}
```
{% include copy-curl.html %}

### 範例請求：批次推論組態

請從該模型與提供者的官方文件取得輸入字串數量 (`max_items_per_request`) 與承載 (`max_bytes_per_request`) 的限制。若為自訂端點，請使用模型伺服器上設定的限制。組態指引請參閱[向外部託管模型傳送批次請求]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/batching-requests/)。

下列請求註冊一個具有大小限制並啟用動態批次處理的外部託管模型：

```json
POST /_plugins/_ml/models/_register
{
  "name": "remote-embedding-model",
  "function_name": "remote",
  "connector_id": "<connector_id>",
  "batch_inference_config": {
    "max_items_per_request": 96,
    "max_bytes_per_request": 4000000,
    "dynamic_batching": {
      "enabled": true,
      "flush_timeout_ms": 50
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

OpenSearch 會以 `task_id` 和任務 `status` 回應。對於外部託管的模型，回應也會包含 `model_id`。對於本機模型，模型 ID 會在註冊完成後於任務中傳回：

```json
{
  "task_id" : "ew8I44MBhyWuIwnfvDIH", 
  "status" : "CREATED",
  "model_id": "t8qvDY4BChVAiNVEuo8q"
}
```

## 檢查模型註冊狀態

若要查看模型註冊的狀態，並取得為新模型版本建立的模型 ID，請將 `task_id` 作為路徑參數傳遞給 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)：

```json
GET /_plugins/_ml/tasks/{task_id}
```
{% include copy-curl.html %}

回應包含該模型版本的模型 ID：

```json
{
  "model_id": "Qr1YbogBYOqeeqR7sI9L",
  "task_type": "REGISTER_MODEL",
  "function_name": "TEXT_EMBEDDING",
  "state": "COMPLETED",
  "worker_node": [
    "N77RInqjTSq_UaLh1k0BUg"
  ],
  "create_time": 1685478486057,
  "last_update_time": 1685478491090,
  "is_async": true
}
```
