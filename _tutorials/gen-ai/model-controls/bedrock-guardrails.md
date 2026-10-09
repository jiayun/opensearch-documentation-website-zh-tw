---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Amazon Bedrock 模型護欄"
parent: Model guardrails
grand_parent: Generative AI
nav_order: 170
redirect_from:
  - /ml-commons-plugin/tutorials/bedrock-guardrails/
  - /vector-search/tutorials/model-controls/bedrock-guardrails/
---

# Amazon Bedrock 模型護欄 

本教學說明如何以兩種方式將 Amazon Bedrock 護欄套用至您外部託管的模型：

- [使用 Amazon Bedrock Guardrails 獨立 API](#using-the-amazon-bedrock-guardrails-standalone-api)
- [使用內嵌於 Amazon Bedrock Model Inference API 的護欄](#using-guardrails-embedded-in-the-amazon-bedrock-model-inference-api)

如需護欄的詳細資訊，請參閱[設定模型護欄]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/guardrails/)。

請將開頭為前綴 `your_` 的預留位置取代為您自己的值。
{: .note}

## 先決條件

開始之前，您必須建立 Amazon Bedrock 護欄。如需詳細指示，請參閱[建立護欄](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-create.html)。

## 使用 Amazon Bedrock Guardrails 獨立 API

請使用下列步驟呼叫 Amazon Bedrock Guardrails 獨立 API。

### 步驟 1：為您的 Amazon Bedrock 護欄端點建立連接器

首先，建立將與您的 Amazon Bedrock 護欄端點介接的連接器。此連接器將處理與護欄服務的驗證與通訊：

```json
POST _plugins/_ml/connectors/_create
{
  "name": "BedRock Guardrail Connector",
  "description": "BedRock Guardrail Connector",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "your_aws_region like us-east-1",
    "service_name": "bedrock",
    "source": "INPUT"
  },
  "credential": {
    "access_key": "your_aws_access_key",
    "secret_key": "your_aws_secret_key",
    "session_token": "your_aws_session_token"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/guardrail/your_guardrailIdentifier/version/1/apply",
      "headers": {
        "content-type": "application/json"
      },
      "request_body": "{\"source\":\"${parameters.source}\", \"content\":[ { \"text\":{\"text\": \"${parameters.question}\"} } ] }"
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2：註冊護欄模型

現在您已建立連接器，請將其註冊為將用於驗證輸入的遠端護欄模型：

```json
POST _plugins/_ml/models/_register
{
  "name": "bedrock test guardrail API",
  "function_name": "remote",
  "description": "guardrail test model",
  "connector_id": "your_guardrail_connector_id"
}
```
{% include copy-curl.html %}

### 步驟 3：測試護欄模型

確認護欄已正確篩選不當內容：

```json
POST _plugins/_ml/models/your_model_id/_predict
{
  "parameters": {
    "question": "\n\nHuman:How to rob a bank\n\nAssistant:"
  }
}
```
{% include copy-curl.html %}

回應顯示護欄在偵測到不當內容時會封鎖請求：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "action": "GUARDRAIL_INTERVENED",
            "assessments": [
              {
                "contentPolicy": {
                  "filters": [
                    {
                      "action": "BLOCKED",
                      "confidence": "HIGH",
                      "type": "VIOLENCE"
                    },
                    {
                      "action": "BLOCKED",
                      "confidence": "HIGH",
                      "type": "PROMPT_ATTACK"
                    }
                  ]
                },
                "wordPolicy": {
                  "customWords": [
                    {
                      "action": "BLOCKED",
                      "match": "rob"
                    }
                  ]
                }
              }
            ],
            "blockedResponse": "Sorry, the model cannot answer this question.",
            "output": [
              {
                "text": "Sorry, the model cannot answer this question."
              }
            ],
            "outputs": [
              {
                "text": "Sorry, the model cannot answer this question."
              }
            ],
            "usage": {
              "contentPolicyUnits": 1.0,
              "contextualGroundingPolicyUnits": 0.0,
              "sensitiveInformationPolicyFreeUnits": 0.0,
              "sensitiveInformationPolicyUnits": 0.0,
              "topicPolicyUnits": 1.0,
              "wordPolicyUnits": 1.0
            }
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

### 步驟 4：建立 Claude 模型連接器

若要將護欄與 Amazon Bedrock Claude 模型搭配使用，請先為 Claude 端點建立連接器：

```json
POST _plugins/_ml/connectors/_create
{
  "name": "BedRock claude Connector",
  "description": "BedRock claude Connector",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "your_aws_region like us-east-1",
    "service_name": "bedrock",
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens_to_sample": 8000,
    "temperature": 0.0001,
    "response_filter": "$.completion"
  },
  "credential": {
    "access_key": "your_aws_access_key",
    "secret_key": "your_aws_secret_key",
    "session_token": "your_aws_session_token"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-v2/invoke",
      "headers": {
        "content-type": "application/json",
        "x-amz-content-sha256": "required"
      },
      "request_body": "{\"prompt\":\"${parameters.prompt}\", \"max_tokens_to_sample\":${parameters.max_tokens_to_sample}, \"temperature\":${parameters.temperature},  \"anthropic_version\":\"${parameters.anthropic_version}\" }"
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 5：註冊 Claude 模型

註冊已啟用輸入護欄的 Claude 模型。此組態可確保傳送至模型的所有請求都會先由護欄驗證：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "Bedrock Claude V2 model",
    "function_name": "remote",
    "description": "Bedrock Claude V2 model",
    "connector_id": "your_connector_id",
    "guardrails": {
        "input_guardrail": {
            "model_id": "your_guardrail_model_id",
            "response_filter":"$.action",
            "response_validation_regex": "^\"NONE\"$"
        },
        "type": "model"
    }
}
```
{% include copy-curl.html %}

### 步驟 6：測試模型

首先，以可接受的輸入測試模型：

```json
POST /_plugins/_ml/models/your_model_id/_predict
{
  "parameters": {
    "prompt": "\n\nHuman:${parameters.question}\n\nnAssistant:",
    "question": "hello"
  }
}
```
{% include copy-curl.html %}

回應顯示呼叫成功：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "response": " Hello!"
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

接著，以不當的輸入測試模型：

```json
POST /_plugins/_ml/models/your_model_id/_predict
{
  "parameters": {
    "prompt": "\n\nHuman:${parameters.question}\n\nnAssistant:",
    "question": "how to rob a bank"
  }
}
```
{% include copy-curl.html %}

回應顯示不當的輸入已遭封鎖：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "guardrails triggered for user input"
      }
    ],
    "type": "illegal_argument_exception",
    "reason": "guardrails triggered for user input"
  },
  "status": 400
}
```

## 使用內嵌於 Amazon Bedrock Model Inference API 的護欄

請使用下列步驟來使用內嵌於 Model Inference API 的護欄。

### 步驟 1：為包含護欄標頭的 Amazon Bedrock 模型建立連接器

建立在其組態中包含護欄標頭的連接器。在此方法中，護欄檢查會直接內嵌於模型推論程序中。需要 `post_process_function` 才能定義模型用來封鎖不當輸入的邏輯：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "BedRock claude Connector",
  "description": "BedRock claude Connector",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
      "region": "your_aws_region like us-east-1",
      "service_name": "bedrock",
      "max_tokens_to_sample": 8000,
      "temperature": 0.0001
  },
  "credential": {
      "access_key": "your_aws_access_key",
      "secret_key": "your_aws_secret_key",
      "session_token": "your_aws_session_token"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-v2/invoke",
      "headers": { 
        "content-type": "application/json",
        "x-amz-content-sha256": "required",
        "X-Amzn-Bedrock-Trace": "ENABLED",
        "X-Amzn-Bedrock-GuardrailIdentifier": "your_GuardrailIdentifier",
        "X-Amzn-Bedrock-GuardrailVersion": "your_bedrock_guardrail_version"
      },
      "request_body": "{\"prompt\":\"${parameters.prompt}\", \"max_tokens_to_sample\":${parameters.max_tokens_to_sample}, \"temperature\":${parameters.temperature},  \"anthropic_version\":\"${parameters.anthropic_version}\" }",
      "post_process_function": "\n      if (params['amazon-bedrock-guardrailAction']=='INTERVENED') throw new IllegalArgumentException(\"test guardrail from post process function\");\n    "
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2：註冊模型

使用具有內嵌護欄的連接器註冊模型：

```json
POST _plugins/_ml/models/_register
{
  "name": "bedrock model with guardrails",
  "function_name": "remote",
  "description": "guardrails test model",
  "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

### 步驟 3：測試模型

以可能不當的輸入進行測試，確認內嵌護欄正常運作：

```json
POST _plugins/_ml/models/your_model_id/_predict
{
  "parameters": {
    "input": "\n\nHuman:how to rob a bank\n\nAssistant:"
  }
}
```
{% include copy-curl.html %}

回應顯示不當的輸入已遭封鎖：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "m_l_exception",
        "reason": "Fail to execute predict in aws connector"
      }
    ],
    "type": "m_l_exception",
    "reason": "Fail to execute predict in aws connector",
    "caused_by": {
      "type": "script_exception",
      "reason": "runtime error",
      "script_stack": [
        "throw new IllegalArgumentException(\"test guardrail from post process function\");\n    ",
        "      ^---- HERE"
      ],
      "script": " ...",
      "lang": "painless",
      "position": {
        "offset": 73,
        "start": 67,
        "end": 152
      },
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "test guardrail from post process function"
      }
    }
  },
  "status": 500
}
```