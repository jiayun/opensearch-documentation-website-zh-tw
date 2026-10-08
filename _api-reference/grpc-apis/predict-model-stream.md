---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "模型串流預測（gRPC）"
parent: gRPC APIs
nav_order: 40
---

# Predict Model Stream API（gRPC）
**於 3.8 版推出**
{: .label .label-purple }

 gRPC Predict Model Stream API 透過 gRPC 使用 protocol buffers，提供二進位介面，以串流方式傳送遠端機器學習（ML）模型的預測結果。底層模型產生回應區塊時，伺服器便會將區塊以串流方式傳送至用戶端，因此用戶端可在推論完成前開始處理輸出。大型語言模型（LLM）逐一產生詞元時，可使用串流。

您可以透過 REST 或 gRPC 以串流方式傳送預測結果。這兩種傳輸方式都會傳回相同的逐步產生模型輸出，因此請選擇最適合您用戶端的方式：

- **REST 串流**透過 HTTP 使用伺服器傳送事件（SSE），瀏覽器、標準 HTTP 用戶端，以及 cURL 等命令列工具都可直接支援。這是實驗性功能，不建議用於正式環境。如需詳細資訊，請參閱 [Predict Stream API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict-stream/)。
- **gRPC 串流**透過 HTTP/2 使用 protocol buffers。此傳輸方式提供較低的序列化額外負擔與較小的承載資料、搭配 HTTP/2 流量控制與連線多工的原生伺服器串流語意，以及強型別結構描述，讓您能以任何 [gRPC 支援的語言](https://grpc.io/docs/languages/)產生用戶端。

下列外部託管模型支援串流預測：

- [OpenAI Chat Completion](https://platform.openai.com/docs/api-reference/completions)
- [Amazon Bedrock Converse Stream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html)

## 先決條件

使用 gRPC Predict Model Stream API 前，請確認您已滿足下列先決條件：

- 在叢集上啟用 gRPC 傳輸。如需詳細資訊，請參閱[使用 gRPC API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/index/#how-to-use-grpc-apis)。
- 在用戶端取得 ML Commons protobufs。如需取得 protobufs 的方式，請參閱[使用 gRPC API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/index/#how-to-use-grpc-apis)。
- 為支援的模型類型設定外部託管模型與串流連接器。如需模型與連接器的組態資訊，請參閱 [Predict Stream API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict-stream/#step-2-register-a-compatible-externally-hosted-model)。

## gRPC 服務與方法

 gRPC Predict Model Stream API 位於 [`MLService`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.6.0/protos/services/ml_service.proto#L22) 服務中。

您可以呼叫 `MLService` 中的 [`PredictModelStream`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.6.0/protos/services/ml_service.proto#L24) 方法來提交串流預測請求。此方法接受一個 [`MlPredictModelStreamRequest`](#mlpredictmodelstreamrequest-fields)，並傳回由 [`PredictResponse`](#response-fields) 訊息組成的串流。

`PredictModelStream` 是伺服器串流遠端程序呼叫（RPC）：用戶端傳送單一請求，伺服器則傳回一連串回應訊息。最後一則訊息會將 `is_last` 設為 `true`，接著伺服器便會關閉串流。
{: .note}

## 請求欄位

 gRPC Predict Model Stream API 支援下列請求欄位。

### MlPredictModelStreamRequest 欄位

[`MlPredictModelStreamRequest`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.6.0/protos/schemas/common.proto#L3406) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 必要 | 說明 |
| :---- | :---- | :---- | :---- |
| `model_id` | `string` | 必要 | 要執行預測的模型 ID。模型必須是受支援的外部託管模型。 |
| `ml_predict_model_stream_request_body` | [`MLPredictModelStreamRequestBody`](#mlpredictmodelstreamrequestbody-fields) | 必要 | 包含預測參數的請求承載資料。 |

<!-- vale off -->
### MLPredictModelStreamRequestBody 欄位
<!-- vale on -->

[`MLPredictModelStreamRequestBody`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.6.0/protos/schemas/common.proto#L3323) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 必要 | 說明 |
| :---- | :---- | :---- | :---- |
| `parameters` | [`Parameters`](#parameters-fields) | 必要 | 傳遞至遠端模型的輸入參數。 |

### Parameters 欄位

對於串流預測，[`Parameters`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.6.0/protos/schemas/common.proto#L3356) 訊息接受下列欄位。請提供符合您模型類型的欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `messages` | `repeated` [`Messages`](#messages-fields) | 傳送至聊天完成模型（例如 OpenAI Chat Completion）的對話訊息。 |
| `inputs` | `string` | 傳送至模型的輸入文字，例如使用 Amazon Bedrock Converse Stream 模型時。 |
| `x_llm_interface` | `string` | 與您模型類型對應的 LLM 介面。有效值為 `openai/v1/chat/completions` 與 `bedrock/converse/claude`。 |

### Messages 欄位

[`Messages`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.6.0/protos/schemas/common.proto#L3328) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `role` | `string` | 訊息傳送者的角色，例如 `system` 或 `user`。 |
| `content` | `string` | 訊息內容。 |

## 回應欄位

伺服器會以串流方式傳送一連串 [`PredictResponse`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.6.0/protos/schemas/common.proto#L3367) 訊息。每則訊息都包含一個產生的輸出區塊，並提供下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `inference_results` | `repeated InferenceResults` | 該區塊的推論結果。 |
| `inference_results.output` | `repeated Output` | 每個推論結果的輸出物件。 |
| `inference_results.output.name` | `string` | 輸出欄位的名稱（通常為 `response`）。 |
| `inference_results.output.data_as_map` | `DataAsMap` | 該區塊的回應內容與中繼資料。 |
| `inference_results.output.data_as_map.content` | `string` | 該區塊的文字內容。串接各區塊的 `content` 值，即可重建完整回應。 |
| `inference_results.output.data_as_map.is_last` | `bool` | 這是否為串流中的最後一個區塊。當值為 `true` 時，便不會再傳送訊息。 |

## 請求範例

承載模型輸入的欄位與 `x_llm_interface` 值都取決於模型類型。下列範例顯示各個受支援模型類型的 gRPC 請求訊息之 JSON 表示方式。在這兩個範例中，請將 `model_id` 替換為您已註冊模型的 ID。

對於 OpenAI Chat Completion 模型，請在 `messages` 欄位中提供對話，並將 `x_llm_interface` 設為 `openai/v1/chat/completions`：

```json
{
  "model_id": "your_model_id",
  "ml_predict_model_stream_request_body": {
    "parameters": {
      "messages": [
        {
          "role": "system",
          "content": "You are a helpful assistant."
        },
        {
          "role": "user",
          "content": "Can you summarize Prince Hamlet of William Shakespeare in around 100 words?"
        }
      ],
      "x_llm_interface": "openai/v1/chat/completions"
    }
  }
}
```
{% include copy.html %}

對於 Amazon Bedrock Converse Stream 模型，請在 `inputs` 欄位中提供輸入文字，並將 `x_llm_interface` 設為 `bedrock/converse/claude`：

```json
{
  "model_id": "your_model_id",
  "ml_predict_model_stream_request_body": {
    "parameters": {
      "inputs": "Can you summarize Prince Hamlet of William Shakespeare in around 100 words?",
      "x_llm_interface": "bedrock/converse/claude"
    }
  }
}
```
{% include copy.html %}

下列範例顯示一個 Java gRPC 用戶端，以串流方式接收 OpenAI Chat Completion 模型的預測結果。請將模型 ID 與訊息替換為符合您模型組態的值：

```java
import org.opensearch.protobufs.*;
import org.opensearch.protobufs.services.MLServiceGrpc;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

import java.util.Iterator;

public class PredictModelStreamClient {
    public static void main(String[] args) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 9400)
                .usePlaintext()
                .build();

        // Create a gRPC stub for ML operations
        MLServiceGrpc.MLServiceBlockingStub mlStub = MLServiceGrpc.newBlockingStub(channel);

        // Build the request parameters for an OpenAI Chat Completion model
        Parameters parameters = Parameters.newBuilder()
            .addMessages(Messages.newBuilder()
                .setRole("system")
                .setContent("You are a helpful assistant.")
                .build())
            .addMessages(Messages.newBuilder()
                .setRole("user")
                .setContent("Can you summarize Prince Hamlet of William Shakespeare in around 100 words?")
                .build())
            .setXLlmInterface("openai/v1/chat/completions")
            .build();

        // Create the streaming predict request
        MlPredictModelStreamRequest request = MlPredictModelStreamRequest.newBuilder()
            .setModelId("your_model_id")
            .setMlPredictModelStreamRequestBody(MLPredictModelStreamRequestBody.newBuilder()
                .setParameters(parameters)
                .build())
            .build();

        // Execute the request and read the streamed response
        try {
            Iterator<PredictResponse> responses = mlStub.predictModelStream(request);
            while (responses.hasNext()) {
                PredictResponse response = responses.next();
                for (InferenceResults results : response.getInferenceResultsList()) {
                    for (Output output : results.getOutputList()) {
                        DataAsMap chunk = output.getDataAsMap();
                        System.out.print(chunk.getContent());
                        if (chunk.getIsLast()) {
                            System.out.println("\n[stream complete]");
                        }
                    }
                }
            }
        } catch (io.grpc.StatusRuntimeException e) {
            System.err.println("gRPC predict stream request failed with status: " + e.getStatus());
            System.err.println("Error message: " + e.getMessage());
        }

        channel.shutdown();
    }
}
```
{% include copy.html %}

對於 Amazon Bedrock Converse Stream 模型，請使用 `setInputs` 取代 `addMessages` 來建構請求參數。其餘用戶端程式碼維持不變：

```java
Parameters parameters = Parameters.newBuilder()
    .setInputs("Can you summarize Prince Hamlet of William Shakespeare in around 100 words?")
    .setXLlmInterface("bedrock/converse/claude")
    .build();

MlPredictModelStreamRequest request = MlPredictModelStreamRequest.newBuilder()
    .setModelId("your_model_id")
    .setMlPredictModelStreamRequestBody(MLPredictModelStreamRequestBody.newBuilder()
        .setParameters(parameters)
        .build())
    .build();
```
{% include copy.html %}

## 範例回應

伺服器會傳回一連串的 `PredictResponse` 訊息。每個訊息都在 `content` 欄位中攜帶一段產生的文字，而最後一個訊息會將 `isLast` 設為 `true`。以下範例顯示串流區塊的 JSON 表示法：

```json
{
  "inferenceResults": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "content": "Hello",
            "isLast": false
          }
        }
      ]
    }
  ]
}
```

## 相關文件

- [Predict Stream API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict-stream/) -- 串流預測的 REST 對應版本
- [使用 gRPC API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/index/) -- gRPC 傳輸組態與用戶端需求
