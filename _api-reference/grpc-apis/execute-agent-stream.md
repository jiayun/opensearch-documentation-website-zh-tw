---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行代理程式串流 (gRPC)"
parent: gRPC APIs
nav_order: 50
---

# Execute Agent Stream API (gRPC)
**3.8 版新增**
{: .label .label-purple }

gRPC Execute Agent Stream API 提供二進位介面，可透過 gRPC 使用 protocol buffers 串流執行代理程式。伺服器會在代理程式產生回應區塊時，將其串流傳送至用戶端，因此用戶端可在執行完成前開始處理輸出。串流適用於會從大型語言模型 (LLM) 逐詞元產生輸出的對話式代理程式。

您可以透過 REST 或 gRPC 串流代理程式執行。兩種傳輸方式都會傳回相同的漸進式產生輸出，因此請選擇最適合您用戶端的方式：

- **REST 串流**透過 HTTP 使用伺服器傳送事件 (SSE)，瀏覽器、標準 HTTP 用戶端以及 cURL 等命令列工具都直接支援。這是一項實驗性功能，不建議在正式環境中使用。如需更多資訊，請參閱 [Execute Agent Stream API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-stream-agent/)。
- **gRPC 串流**透過 HTTP/2 使用 protocol buffers。此傳輸方式提供較低的序列化負擔與較小的酬載、具備 HTTP/2 流量控制與連線多工的原生伺服器串流語意，以及強型別結構描述，您可從中產生任何 [gRPC 支援語言](https://grpc.io/docs/languages/)的用戶端。

使用下列外部託管模型的代理程式支援串流代理程式執行：

- [OpenAI Chat Completion](https://platform.openai.com/docs/api-reference/completions)
- [Amazon Bedrock Converse Stream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html)

## 必要條件

使用 gRPC Execute Agent Stream API 之前，請確定您已符合下列必要條件：

- 在叢集上啟用 gRPC 傳輸。如需更多資訊，請參閱[使用 gRPC API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/index/#how-to-use-grpc-apis)。
- 在用戶端取得 ML Commons protobufs。取得 protobufs 的方式請參閱[使用 gRPC API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/index/#how-to-use-grpc-apis)。
- 註冊使用支援串流之模型的代理程式。代理程式與連接器的組態請參閱 [Execute Agent Stream API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-stream-agent/#step-2-register-a-compatible-externally-hosted-model)。

## gRPC 服務與方法

gRPC Execute Agent Stream API 位於 [`MLService`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.6.0/protos/services/ml_service.proto#L22) 服務中。

您可以透過叫用 `MLService` 內的 [`ExecuteAgentStream`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.6.0/protos/services/ml_service.proto#L27) 方法來提交串流代理程式執行請求。該方法接受 [`MlExecuteAgentStreamRequest`](#mlexecuteagentstreamrequest-fields)，並傳回 [`PredictResponse`](#response-fields) 訊息串流。

`ExecuteAgentStream` 是伺服器串流遠端程序呼叫 (RPC)：用戶端傳送單一請求，伺服器則傳回一連串回應訊息。最後一則訊息會將 `is_last` 設為 `true`，然後伺服器關閉串流。
{: .note}

## 請求欄位

gRPC Execute Agent Stream API 支援下列請求欄位。

### MlExecuteAgentStreamRequest 欄位

[`MlExecuteAgentStreamRequest`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.6.0/protos/schemas/common.proto#L3396) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 必要 | 描述 |
| :---- | :---- | :---- | :---- |
| `agent_id` | `string` | 必要 | 要執行之代理程式的 ID。 |
| `ml_execute_agent_stream_request_body` | [`MLExecuteAgentStreamRequestBody`](#mlexecuteagentstreamrequestbody-fields) | 必要 | 包含執行參數的請求酬載。 |

<!-- vale off -->
### MLExecuteAgentStreamRequestBody 欄位
<!-- vale on -->

[`MLExecuteAgentStreamRequestBody`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.6.0/protos/schemas/common.proto#L3318) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 必要 | 描述 |
| :---- | :---- | :---- | :---- |
| `parameters` | [`Parameters`](#parameters-fields) | 必要 | 傳遞給代理程式的輸入參數。 |

### Parameters 欄位

執行代理程式時，[`Parameters`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.6.0/protos/schemas/common.proto#L3356) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 描述 |
| :---- | :---- | :---- |
| `question` | `string` | 傳送給代理程式的輸入問題。 |

## 回應欄位

伺服器會串流傳回一連串 [`PredictResponse`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.6.0/protos/schemas/common.proto#L3367) 訊息。每則訊息承載一個產生輸出的區塊，並提供下列欄位。

| 欄位 | Protobuf 類型 | 描述 |
| :---- | :---- | :---- |
| `inference_results` | `repeated InferenceResults` | 該區塊的推論結果。 |
| `inference_results.output` | `repeated Output` | 每個推論結果的輸出物件。 |
| `inference_results.output.name` | `string` | 輸出欄位的名稱 (通常為 `response`)。 |
| `inference_results.output.result` | `string` | `memory_id` 與 `parent_interaction_id` 欄位的值。 |
| `inference_results.output.data_as_map` | `DataAsMap` | 該區塊的回應內容與中繼資料。 |
| `inference_results.output.data_as_map.content` | `string` | 該區塊的文字內容。將各區塊的 `content` 值串接起來，即可重建完整回應。 |
| `inference_results.output.data_as_map.is_last` | `bool` | 這是否為串流中的最後一個區塊。當為 `true` 時，不會再傳送任何訊息。 |

## 請求範例

下列範例顯示 gRPC 請求訊息的 JSON 表示法。請將 `agent_id` 與 `question` 替換為符合您代理程式組態的值：

```json
{
  "agent_id": "your_agent_id",
  "ml_execute_agent_stream_request_body": {
    "parameters": {
      "question": "List indices in my cluster"
    }
  }
}
```
{% include copy.html %}

下列範例顯示串流執行對話式代理程式的 Java gRPC 用戶端。請將代理程式 ID 與問題替換為符合您代理程式組態的值：

```java
import org.opensearch.protobufs.*;
import org.opensearch.protobufs.services.MLServiceGrpc;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

import java.util.Iterator;

public class ExecuteAgentStreamClient {
    public static void main(String[] args) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 9400)
                .usePlaintext()
                .build();

        // Create a gRPC stub for ML operations
        MLServiceGrpc.MLServiceBlockingStub mlStub = MLServiceGrpc.newBlockingStub(channel);

        // Build the request parameters for the agent
        Parameters parameters = Parameters.newBuilder()
            .setQuestion("List indices in my cluster")
            .build();

        // Create the streaming agent execution request
        MlExecuteAgentStreamRequest request = MlExecuteAgentStreamRequest.newBuilder()
            .setAgentId("your_agent_id")
            .setMlExecuteAgentStreamRequestBody(MLExecuteAgentStreamRequestBody.newBuilder()
                .setParameters(parameters)
                .build())
            .build();

        // Execute the request and read the streamed response
        try {
            Iterator<PredictResponse> responses = mlStub.executeAgentStream(request);
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
            System.err.println("gRPC execute agent stream request failed with status: " + e.getStatus());
            System.err.println("Error message: " + e.getMessage());
        }

        channel.shutdown();
    }
}
```
{% include copy.html %}

## 回應範例

伺服器會傳回一連串 `PredictResponse` 訊息。每則訊息在 `content` 欄位中承載一段產生的文字，而最後一則訊息會將 `isLast` 設為 `true`。下列範例顯示串流區塊的 JSON 表示法：

```json
{
  "inferenceResults": [
    {
      "output": [
        {
          "name": "memory_id",
          "result": "6CMnkJ8BLGHoqtB13ipp"
        },
        {
          "name": "parent_interaction_id",
          "result": "6SMnkJ8BLGHoqtB13irB"
        },
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

- [Execute Agent Stream API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-stream-agent/) -- 串流代理程式執行的 REST 對應版本
- [使用 gRPC API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/index/) -- gRPC 傳輸組態與用戶端需求
