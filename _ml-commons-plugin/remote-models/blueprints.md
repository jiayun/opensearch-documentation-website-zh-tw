---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "連接器藍圖"
has_children: false
nav_order: 10
parent: Connectors
grand_parent: Connecting to externally hosted models
great_grand_parent: Integrating ML models
redirect_from: 
  - /ml-commons-plugin/extensibility/blueprints/
---

# 連接器藍圖
**於 2.9 版導入**
{: .label .label-purple }

每個[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)都由一份_連接器藍圖_ (connector blueprint) 定義。藍圖定義了建立連接器時所需提供的所有參數。

例如，下列藍圖是 Amazon SageMaker 連接器的規格：

```json
{
  "name": "<YOUR CONNECTOR NAME>",
  "description": "<YOUR CONNECTOR DESCRIPTION>",
  "version": "<YOUR CONNECTOR VERSION>",
  "protocol": "aws_sigv4",
  "credential": {
    "access_key": "<YOUR AWS ACCESS KEY>",
    "secret_key": "<YOUR AWS SECRET KEY>",
    "session_token": "<YOUR AWS SECURITY TOKEN>"
  },
  "parameters": {
    "region": "<YOUR AWS REGION>",
    "service_name": "sagemaker"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "headers": {
        "content-type": "application/json"
      },
      "url": "<YOUR SAGEMAKER MODEL ENDPOINT URL>",
      "request_body": "<YOUR REQUEST BODY. Example: ${parameters.inputs}>"
    }
  ]
}
```
{% include copy.html %}

## 尋找藍圖

OpenSearch 為許多機器學習 (ML) 平台及模型提供連接器藍圖。如需所有已提供藍圖的平台及模型清單，以及各自使用的驗證通訊協定，請參閱 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/)。

身為 ML 開發人員，您可以為其他平台建置連接器藍圖。管理員和資料科學家可以使用這些藍圖，為託管在這些平台上的模型建立連接器。 

## 請求本文欄位

下表列出建立連接器請求中的欄位。

| 欄位                                            | 資料類型 | 是否必要 | 說明                                                                                                                                                                                                                                                                                                                                                                          |
|:-------------------------------------------------|:---|:------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`                                           | 字串 | 是         | 連接器的名稱。                                                                                                                                                                                                                                                                                                                                                           |
| `connector_id`                                   | 字串 | 否          | 連接器的唯一識別碼。若省略，OpenSearch 會自動產生一個。 |
| `description`                                    | 字串 | 否          | 連接器的說明。                                                                                                                                                                                                                                                                                                                                                      |
| `version`                                        | 整數 | 是         | 連接器版本。                                                                                                                                                                                                                                                                                                                                                        |
| `protocol`                                       | 字串 | 是         | 連線的通訊協定，用於決定 OpenSearch 如何向平台進行驗證。若是 AWS 服務，例如 Amazon SageMaker 和 Amazon Bedrock，請使用 `aws_sigv4`。若是 Google Cloud Vertex AI，請使用 `google_cloud`。若是其他所有平台，請使用 `http`。如需詳細資訊，請參閱[連接器驗證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connector-authentication/)。                                                                                                                                                                                                                                  |
| `parameters`                                     | JSON 物件 | 否          | 預設連接器參數，包括 `endpoint`、`model` 和 `skip_validating_missing_parameters`。此欄位中指定的任何參數，都可由 predict 請求中指定的參數覆寫。                                                                                                                                                                     |
| `credential`                                     | JSON 物件 | 視 `protocol` 而定 | 定義 OpenSearch 用來向您的端點進行驗證的認證資訊變數。除了應用程式預設認證資訊模式（Application Default Credentials，`auth_mode` 設為 `adc`）下的 `google_cloud`，以及會在連接器外部解析認證資訊的 `mcp_sse` 和 `mcp_streamable_http` 通訊協定之外，所有通訊協定都需要此欄位。對於其他所有通訊協定（包括 `http`），若省略此物件或將其留空，會傳回 `400` 錯誤。此物件可接受的欄位取決於 `protocol`。如需詳細資訊，請參閱[連接器驗證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connector-authentication/)。ML Commons 使用 **AES/GCM/NoPadding** 對稱式加密來加密您的認證資訊。啟動叢集連線時，OpenSearch 會建立隨機的 32 位元組加密金鑰，並保存在 OpenSearch 的系統索引中。因此，您不需要手動設定加密金鑰。 |
| `actions`                                        | JSON 陣列  | 是         | 定義可在連接器內執行的動作。若您是建立連線的管理員，請為所需的連線新增[藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)。                                                                                                                                                      |
| `backend_roles`                                  | JSON 陣列  | 否          | OpenSearch 後端角色清單。如需設定後端角色的詳細資訊，請參閱[將後端角色指派給使用者]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control#assigning-backend-roles-to-users)。                                                                                                                                               |
| `access_mode`                                    | 字串 | 否          | 設定模型的存取模式，可為 `public`、`restricted` 或 `private`。預設為 `private`。如需 `access_mode` 的詳細資訊，請參閱[模型群組]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control#model-groups)。                                                                                                                               |
| `add_all_backend_roles`                          | 布林值  | 否          | 若為 `true`，建立連接器之使用者的所有後端角色都會新增至連接器。若您將此參數設為 `true` 而未指定 `access_mode`，存取模式會設為 `restricted`。只能與 `restricted` 存取模式搭配使用，且使用者必須至少有一個後端角色。不能與 `backend_roles` 同時指定。管理員使用者無法將此參數設為 `true`。 |
| `client_config`                                  | JSON 物件 | 否          | 用戶端組態物件，提供控制連接器所使用之用戶端連線行為的設定。這些設定可讓您管理連線限制、逾時和 TLS 選項，確保通訊有效率且可靠。                                                                                                                                |
| `parameters.skip_validating_missing_parameters`  | 布林值 | 否          | 設為 `true` 時，此選項可讓您使用連接器傳送請求，而不驗證任何缺少的參數。預設為 `false`。                                                                                                                                                                                                                                                            |
| `provisioned_by`                                     | 字串 | 否          | 選用的歸屬標籤，用於識別佈建連接器的外掛程式或用戶端（例如 `flow-framework`）。會納入 ML 統計指標。僅在建立時設定；Update Connector API 會忽略此欄位。                                                                                                                                                            |


`actions` 物件支援下列欄位。

| 欄位 | 資料類型 | 說明 |
|:---|:---|:---|
| `action_type` | 字串 | 必要。指定連線時要使用的 ML Commons API 操作。有效值為 `predict`、`batch_predict`、`batch_predict_status`、`cancel_batch_predict` 和 `execute`。 |
| `method`  | 字串 | 必要。定義 API 呼叫的 HTTP 方法。支援 `POST` 和 `GET`。 |
| `url` | 字串      | 必要。指定執行動作的連線端點。此值必須符合[新增受信任端點]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index#adding-trusted-endpoints)時所使用之連線的正規表示式。|
| `request_body` | 字串 | 選用。OpenSearch 針對該動作傳送至模型端點的請求本文範本。使用 `${parameters.<parameter_name>}` 預留位置來插入參數值，例如 `${parameters.inputText}`。 |
| `pre_process_function`  | 字串 | 選用。用於前置處理輸入資料的內建或自訂 Painless 指令碼。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。OpenSearch 提供下列可直接呼叫的內建前置處理函式：<br> - `connector.pre_process.cohere.embedding` 用於 [Cohere](https://cohere.com/) 嵌入模型<br> - `connector.pre_process.openai.embedding` 用於 [OpenAI](https://platform.openai.com/docs/guides/embeddings) 嵌入模型 <br> - `connector.pre_process.default.embedding`，可用於前置處理神經搜尋請求中的文件，使其符合 ML Commons 可使用預設前置處理器處理的格式（OpenSearch 2.11 或更新版本）。如需詳細資訊，請參閱[內建函式](#built-in-pre--and-post-processing-functions)。 |
| `post_process_function` | 字串   | 選用。用於後置處理模型輸出資料的內建或自訂 Painless 指令碼。OpenSearch 提供下列可直接呼叫的內建後置處理函式：<br> - `connector.post_process.cohere.embedding` 用於 [Cohere 文字嵌入模型](https://docs.cohere.com/reference/embed)<br> - `connector.post_process.openai.embedding` 用於 [OpenAI 文字嵌入模型](https://platform.openai.com/docs/api-reference/embeddings) <br> - `connector.post_process.default.embedding`，可用於後置處理模型回應中的文件，使其符合神經搜尋預期的格式（OpenSearch 2.11 或更新版本）。如需詳細資訊，請參閱[內建函式](#built-in-pre--and-post-processing-functions)。 |
| `headers` | JSON 物件 | 指定請求或回應本文中使用的標頭。預設為 `ContentType: application/json`。若您的第三方 ML 工具需要存取控制，請在 `headers` 參數中定義所需的 `credential` 參數。 |
| `supports_structured_output` | 布林值 | 選用。僅適用於用於[代理記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/)（agentic memory）事實擷取之 LLM 連接器的 `predict` 動作。若為 `true`，OpenSearch 會在事實擷取期間於請求本文中新增結構化輸出欄位，讓模型以固定的 JSON 結構描述傳回擷取的事實（受限解碼）。OpenSearch 會根據動作 `url` 中的提供者選擇欄位：Amazon Bedrock Converse API 使用 `toolConfig`、Google Gemini 使用 `generationConfig`，而 OpenAI、Azure OpenAI、DeepSeek、Cohere v2 Chat API 及其他路徑包含 `/v1/chat/completions` 的端點則使用 `response_format`。僅當 `request_body` 為 JSON 物件時才會新增該欄位。若為 `false`，或 OpenSearch 無法辨識提供者，OpenSearch 會在事實擷取提示中新增格式指示。預設為 `false`。 |

`client_config` 物件支援下列欄位。

| 欄位  | 資料類型 | 說明 |
|:---|:---|:---|
| `max_connection` | 整數   | 用戶端可與伺服器建立的同時連線數上限。某些遠端服務（例如 SageMaker）會限制同時連線數上限，並在同時連線數超過門檻時擲出節流例外。OpenSearch 同時連線數上限為 `max_connection`*`node_number_for_connector`。若要緩解此問題，請嘗試降低此參數的值，並修改 `client_config` 中的重試設定。預設為 `30`。 |
| `connection_timeout` | 整數 | 用戶端嘗試建立與伺服器的連線時最多等待的時間（秒）。逾時可避免用戶端無限期等待，並讓用戶端在遇到無法連線的網路端點時能夠復原。預設為 `30`。 |
| `read_timeout` | 整數 | 用戶端送出請求後，等待伺服器回應的最長時間（秒）。當伺服器回應緩慢或在處理請求時發生問題時，此設定很有用。預設為 `30`。 |
| `retry_backoff_policy`  | 字串   | 對遠端連接器重試時使用的退避政策。當流量暴增導致節流例外時，此設定很有用。支援的政策為 `constant`、`exponential_equal_jitter` 與 `exponential_full_jitter`。預設為 `constant`。 |
| `max_retry_times`  | 整數   | 單一遠端推論請求最多重試的次數。當流量暴增導致節流例外時，此設定很有用。設為 `0` 時，停用重試。設為 `-1` 時，OpenSearch 不限制 `retry_times` 的次數。設為正整數則指定重試次數上限。預設為 `0`。       |
| `retry_backoff_millis` | 整數   | 重試政策的基礎退避時間（毫秒）。兩次重試之間的暫停時間由此參數與 `retry_backoff_policy` 決定。預設為 `200`。 |
| `retry_timeout_seconds` | 整數   | 重試的逾時值（秒）。如果重試在指定時間內無法成功，連接器將停止重試並擲出例外。預設為 `30`。 |
| `skip_ssl_verification` | 布林值   | 設為 `true` 時，停用連接器的 SSL 憑證驗證，允許連線至使用自簽或其他無效憑證的端點。僅在開發或測試環境中使用。設為 `false` 時，SSL 憑證驗證保持啟用（建議用於正式環境）。預設為 `false`。 |
| `mutual_tls_enabled` | 布林值 | 設為 `true` 時，連接器會使用相互 TLS（mTLS）向端點出示用戶端憑證。請在連接器的 `credential` 物件中提供憑證資料。僅支援使用 `http` 通訊協定的連接器。無法與 `skip_ssl_verification` 同時啟用。預設為 `false`。如需更多資訊，請參閱[用戶端憑證驗證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/http-authentication/#client-certificate-authentication)。 |
| `keystore_type` | 字串 | 在 `credential` 物件中提供的用戶端憑證資料格式。有效值為 `PEM` 與 `PKCS12`（不區分大小寫）。僅在 `mutual_tls_enabled` 為 `true` 時適用。預設為 `PEM`。 |

## 內建前置與後置處理函式

連線至下列文字嵌入模型，或您部署在遠端伺服器 (例如 Amazon SageMaker) 上的自有文字嵌入模型時，請呼叫內建的前置與後置處理函式，而不要撰寫自訂 Painless 指令碼：

- [OpenAI 模型](https://platform.openai.com/docs/api-reference/embeddings)
- [Cohere 模型](https://docs.cohere.com/reference/embed)

OpenSearch 提供下列前置與後置處理函式：

- OpenAI：`connector.pre_process.openai.embedding` 和 `connector.post_process.openai.embedding`
- Cohere：`connector.pre_process.cohere.embedding` 和 `connector.post_process.cohere.embedding`
- [Amazon SageMaker 神經搜尋預設函式](#amazon-sagemaker-default-pre--and-post-processing-functions-for-neural-search)：`connector.pre_process.default.embedding` 和 `connector.post_process.default.embedding`

### Amazon SageMaker 神經搜尋的預設前置與後置處理函式

當您使用[神經搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-search/)執行向量搜尋時，神經搜尋請求會先路由至 ML Commons，再路由至模型。如果模型是 [OpenSearch 提供的預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/)之一，它可以解析 ML Commons 請求，並以 ML Commons 預期的格式傳回回應。然而，對於託管在外部平台上的模型，預期的格式可能與 ML Commons 格式不同。預設的前置與後置處理函式會在模型預期的格式與神經搜尋預期的格式之間進行轉換。

若要套用預設函式，模型輸入與輸出必須符合以下各節所述的格式。

#### 範例請求

下列範例請求會建立 SageMaker 文字嵌入連接器，並呼叫預設的後處理函式：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Sagemaker text embedding connector",
  "description": "The connector to Sagemaker",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "access_key": "<YOUR SAGEMAKER ACCESS KEY>",
    "secret_key": "<YOUR SAGEMAKER SECRET KEY>",
    "session_token": "<YOUR AWS SECURITY TOKEN>"
  },
  "parameters": {
    "region": "ap-northeast-1",
    "service_name": "sagemaker"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://runtime.sagemaker.ap-northeast-1.amazonaws.com/endpoints/<endpoint_name>/invocations",
      "headers": {
        "content-type": "application/json"
      },
      "post_process_function": "connector.post_process.default.embedding",
      "request_body": "${parameters.input}"
    }
  ]
}
```
{% include copy-curl.html %}

`request_body` 範本必須為 `${parameters.input}`。
{: .important}

### 前置處理函式

`connector.pre_process.default.embedding` 預設前置處理函式會解析神經搜尋請求，並將其轉換為模型預期的輸入格式。

ML Commons [Predict API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/) 提供下列格式的參數：

```json
{
  "parameters": {
    "input": ["hello", "world"]
  }
}
```

預設前置處理函式會將 `input` 欄位內容傳送至模型。因此，模型輸入格式必須是字串清單，例如：

```json
["hello", "world"]
```

### 後置處理函式

`connector.post_process.default.embedding` 預設後置處理函式會解析模型回應，並將其轉換為神經搜尋預期的輸入格式。

遠端文字嵌入模型的輸出必須是二維浮點數陣列，其中每個元素代表輸入清單中一個字串的嵌入。例如，下列二維陣列對應於清單 `["hello", "world"]` 的嵌入：

```json
[
  [
    -0.048237994,
    -0.07612697,
    ...
  ],
  [
    0.32621247,
    0.02328475,
    ...
  ]
]
```

## 自訂前置與後置處理函式

您可以針對自己的模型格式撰寫專屬的前置與後置處理函式。例如，下列 Amazon Bedrock 連接器定義包含適用於 Amazon Bedrock Titan 嵌入模型的自訂前置與後置處理函式：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Amazon Bedrock Connector: embedding",
  "description": "The connector to the Bedrock Titan embedding model",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "<YOUR AWS REGION>",
    "service_name": "bedrock"
  },
  "credential": {
    "access_key": "<YOUR AWS ACCESS KEY>",
    "secret_key": "<YOUR AWS SECRET KEY>",
    "session_token": "<YOUR AWS SECURITY TOKEN>"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://bedrock-runtime.us-east-1.amazonaws.com/model/amazon.titan-embed-text-v1/invoke",
      "headers": {
        "content-type": "application/json",
        "x-amz-content-sha256": "required"
      },
      "request_body": "{ \"inputText\": \"${parameters.inputText}\" }",
      "pre_process_function": "\n    StringBuilder builder = new StringBuilder();\n    builder.append(\"\\\"\");\n    String first = params.text_docs[0];\n    builder.append(first);\n    builder.append(\"\\\"\");\n    def parameters = \"{\" +\"\\\"inputText\\\":\" + builder + \"}\";\n    return  \"{\" +\"\\\"parameters\\\":\" + parameters + \"}\";",
      "post_process_function": "\n      def name = \"sentence_embedding\";\n      def dataType = \"FLOAT32\";\n      if (params.embedding == null || params.embedding.length == 0) {\n        return params.message;\n      }\n      def shape = [params.embedding.length];\n      def json = \"{\" +\n                 \"\\\"name\\\":\\\"\" + name + \"\\\",\" +\n                 \"\\\"data_type\\\":\\\"\" + dataType + \"\\\",\" +\n                 \"\\\"shape\\\":\" + shape + \",\" +\n                 \"\\\"data\\\":\" + params.embedding +\n                 \"}\";\n      return json;\n    "
    }
  ]
}
```
{% include copy-curl.html %}

## 後續步驟

- 若要進一步了解如何連線至外部模型，請參閱[連線至外部託管模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。
- 如需連接器範例，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。
