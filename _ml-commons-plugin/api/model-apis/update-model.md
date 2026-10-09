---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "更新模型"
parent: Model APIs
grand_parent: ML Commons APIs
nav_order: 40
---

# Update Model API
**於 2.12 版推出**
{: .label .label-purple }

根據 `model_ID` 更新模型。

有關此 API 的使用者存取權資訊，請參閱[模型存取控制注意事項]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/#model-access-control-considerations)。

## 端點

```json
PUT /_plugins/_ml/models/{model_id}
```

## 請求本文欄位

下表列出可更新的欄位。並非所有請求欄位都適用於所有模型。若要判斷該欄位是否適用於您的模型類型，請參閱 [Register Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/)。

欄位 | 資料類型 |  說明
:---  | :--- | :--- 
`batch_inference_config` | 物件 | 為外部託管的模型設定批次推論。如需更多資訊，請參閱[`batch_inference_config` 參數]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/#the-batch_inference_config-parameter)。
`connector` | 物件 | 包含第三方平台上託管模型之連接器的規格。如需更多資訊，請參閱[為特定模型建立連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/#creating-a-connector-for-a-specific-model)。有關連接器內可更新欄位的資訊，請參閱 [Update Connector API 請求欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/connector-apis/update-connector/#request-body-fields)。
`connector_id` | 字串 | 第三方平台上託管模型之獨立連接器的連接器 ID。如需更多資訊，請參閱[獨立連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/#creating-a-standalone-connector)。若要更新獨立連接器，您必須先取消部署模型、更新連接器，然後重新部署模型。
`description` | 字串 | 模型描述。
`is_enabled`| 布林值 | 指定模型是否已啟用。停用模型會使其無法用於 Predict API 請求，無論模型的部署狀態為何。預設為 `true`。
`model_config` | 物件 | 模型的組態，包括 `model_type`、`embedding_dimension` 和 `framework_type`。`all_config` 是包含所有模型組態的選用 JSON 字串。如需更多資訊，請參閱[`model_config` 物件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model#the-model_config-object)。 |
`model_group_id` | 字串 | 要註冊此模型之模型群組的模型群組 ID。
`name`| 字串 | 模型名稱。
`rate_limiter` | 物件 | 限制任何使用者可以呼叫模型 Predict API 的次數。如需更多資訊，請參閱[限制推論呼叫速率]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#rate-limiting-inference-calls)。
`rate_limiter.limit` | 整數 | 任何使用者在每 `unit` 時間內可以呼叫模型 Predict API 的最大次數。預設情況下，Predict API 呼叫次數沒有限制。一旦設定限制，就無法重設為無限制。替代做法是指定一個高限制值和一個小的時間單位，例如每奈秒 1 個請求。
`rate_limiter.unit` | 字串 | 速率限制器的時間單位。有效值為 `DAYS`、`HOURS`、`MICROSECONDS`、`MILLISECONDS`、`MINUTES`、`NANOSECONDS` 和 `SECONDS`。
`guardrails`| 物件 | 模型的防護機制。
`interface`| 物件 | 模型的介面。

## 範例請求：停用模型

```json
PUT /_plugins/_ml/models/MzcIJX8BA7mbufL6DOwl
{
    "is_enabled": false
}
```
{% include copy-curl.html %}

## 範例請求：限制模型的推論呼叫速率

下列請求將您可對模型呼叫 Predict API 的次數限制為每分鐘 4 次 Predict API 呼叫：

```json
PUT /_plugins/_ml/models/T_S-cY0BKCJ3ot9qr0aP
{
  "rate_limiter": {
    "limit": "4",
    "unit": "MINUTES"
  }
}
```
{% include copy-curl.html %}

## 範例請求：更新防護機制

```json
PUT /_plugins/_ml/models/MzcIJX8BA7mbufL6DOwl
{
  "guardrails": {
    "type": "local_regex",
    "input_guardrail": {
      "stop_words": [
        {
          "index_name": "updated_stop_words_input",
          "source_fields": ["updated_title"]
        }
      ],
      "regex": ["updated_regex1", "updated_regex2"]
    },
    "output_guardrail": {
      "stop_words": [
        {
          "index_name": "updated_stop_words_output",
          "source_fields": ["updated_title"]
        }
      ],
      "regex": ["updated_regex1", "updated_regex2"]
    }
  }
}
```
{% include copy-curl.html %}

```json
PUT /_plugins/_ml/models/9uGdCJABjaMXYrp14YRj
{
  "guardrails": {
    "type": "model",
    "input_guardrail": {
      "model_id": "V-G1CJABjaMXYrp1QoUC",
      "response_validation_regex": "^\\s*[Aa]ccept\\s*$"
    },
    "output_guardrail": {
      "model_id": "V-G1CJABjaMXYrp1QoUC",
      "response_validation_regex": "^\\s*[Aa]ccept\\s*$"
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "_index": ".plugins-ml-model",
  "_id": "MzcIJX8BA7mbufL6DOwl",
  "_version": 10,
  "result": "updated",
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 48,
  "_primary_term": 4
}
```

## 範例請求：更新模型介面

您可以更新模型的介面以定義輸入和輸出結構描述。這在處理缺少預設介面或需要自訂的模型時非常有用。如需模型介面的更多資訊，請參閱[`Interface` 參數]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/#the-interface-parameter)。

下列範例請求為註冊時未包含後處理函式的 [AI21 Labs Jurassic 模型](https://aws.amazon.com/bedrock/ai21/)指定輸出結構描述：

```json
PUT /_plugins/_ml/models/IMcNB5UB7judm8f45nXo
{
    "interface": {
        "output": "{\n  \"type\": \"object\",\n  \"properties\": {\n    \"inference_results\": {\n      \"type\": \"array\",\n      \"items\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"output\": {\n            \"type\": \"array\",\n            \"items\": {\n              \"type\": \"object\",\n              \"properties\": {\n                \"name\": {\n                  \"type\": \"string\"\n                },\n                \"dataAsMap\": {\n                  \"type\": \"object\",\n                  \"properties\": {\n                    \"id\": {\n                      \"type\": \"number\"\n                    },\n                    \"prompt\": {\n                      \"type\": \"object\",\n                      \"properties\": {\n                        \"text\": {\n                          \"type\": \"string\"\n                        },\n                        \"tokens\": {\n                          \"type\": \"array\",\n                          \"items\": {\n                            \"type\": \"object\",\n                            \"properties\": {\n                              \"generatedToken\": {\n                                \"type\": \"object\",\n                                \"properties\": {\n                                  \"token\": {\n                                    \"type\": \"string\"\n                                  },\n                                  \"logprob\": {\n                                    \"type\": \"number\"\n                                  },\n                                  \"raw_logprob\": {\n                                    \"type\": \"number\"\n                                  }\n                                }\n                              },\n                              \"textRange\": {\n                                \"type\": \"object\",\n                                \"properties\": {\n                                  \"start\": {\n                                    \"type\": \"number\"\n                                  },\n                                  \"end\": {\n                                    \"type\": \"number\"\n                                  }\n                                }\n                              }\n                            }\n                          }\n                        }\n                      }\n                    },\n                    \"completions\": {\n                      \"type\": \"array\",\n                      \"items\": {\n                        \"type\": \"object\",\n                        \"properties\": {\n                          \"data\": {\n                            \"type\": \"object\",\n                            \"properties\": {\n                              \"text\": {\n                                \"type\": \"string\"\n                              },\n                              \"tokens\": {\n                                \"type\": \"array\",\n                                \"items\": {\n                                  \"type\": \"object\",\n                                  \"properties\": {\n                                    \"generatedToken\": {\n                                      \"type\": \"object\",\n                                      \"properties\": {\n                                        \"token\": {\n                                          \"type\": \"string\"\n                                        },\n                                        \"logprob\": {\n                                          \"type\": \"number\"\n                                        },\n                                        \"raw_logprob\": {\n                                          \"type\": \"number\"\n                                        }\n                                      }\n                                    },\n                                    \"textRange\": {\n                                      \"type\": \"object\",\n                                      \"properties\": {\n                                        \"start\": {\n                                          \"type\": \"number\"\n                                        },\n                                        \"end\": {\n                                          \"type\": \"number\"\n                                        }\n                                      }\n                                    }\n                                  }\n                                }\n                              }\n                            }\n                          },\n                          \"finishReason\": {\n                            \"type\": \"object\",\n                            \"properties\": {\n                              \"reason\": {\n                                \"type\": \"string\"\n                              },\n                              \"length\": {\n                                \"type\": \"number\"\n                              }\n                            }\n                          }\n                        }\n                      }\n                    }\n                  }\n                }\n              }\n            }\n          },\n          \"status_code\": {\n            \"type\": \"integer\"\n          }\n        }\n      }\n    }\n  }\n}"
    }
}
```
{% include copy-curl.html %}

如果模型是使用 [Amazon Bedrock AI21 Labs Jurassic 藍圖](https://github.com/opensearch-project/ml-commons/blob/2.x/docs/remote_inference_blueprints/bedrock_connector_ai21labs_jurassic_blueprint.md)註冊的，則會自動套用預設介面。
{: .note}

如果不再需要模型介面，您可以移除輸入和輸出結構描述，以略過模型結構描述驗證：

```json
PUT /_plugins/_ml/models/IMcNB5UB7judm8f45nXo
{
  "interface": {
    "input": null,
    "output": null
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "_index": ".plugins-ml-model",
  "_id": "IMcNB5UB7judm8f45nXo",
  "_version": 2,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 2,
    "failed": 0
  },
  "_seq_no": 379,
  "_primary_term": 5
}
```

