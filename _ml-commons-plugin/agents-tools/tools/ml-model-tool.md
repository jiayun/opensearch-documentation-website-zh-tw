---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ML Model 工具"
has_children: false
has_toc: false
nav_order: 40
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# ML Model 工具
plugins.ml_commons.rag_pipeline_feature_enabled: true
{: .label .label-purple }
<!-- vale on -->

`MLModelTool` 會執行機器學習 (ML) 模型並回傳推論結果。

## 步驟 1：為模型建立連接器

下列範例請求會為託管於 [Amazon SageMaker](https://aws.amazon.com/pm/sagemaker/) 的模型建立連接器：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "sagemaker model",
  "description": "Test connector for Sagemaker model",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "access_key": "<YOUR ACCESS KEY>",
    "secret_key": "<YOUR SECRET KEY>"
  },
  "parameters": {
    "region": "us-east-1",
    "service_name": "sagemaker"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "headers": {
        "content-type": "application/json"
      },
      "url": "<YOUR SAGEMAKER ENDPOINT>",
      "request_body": """{"prompt":"${parameters.prompt}"}"""
    }
  ]
}
```
{% include copy-curl.html %} 

OpenSearch 會回應連接器 ID：

```json
{
  "connector_id": "eJATWo0BkIylWTeYToTn"
}
```

## 步驟 2：註冊並部署模型

若要將模型註冊並部署到 OpenSearch，請傳送下列請求，並提供上一步驟取得的連接器 ID：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "remote-inferene",
  "function_name": "remote",
  "description": "test model",
  "connector_id": "eJATWo0BkIylWTeYToTn"
}
```
{% include copy-curl.html %} 

OpenSearch 會回應模型 ID：

```json
{
  "task_id": "7X7pWI0Bpc3sThaJ4I8R",
  "status": "CREATED",
  "model_id": "h5AUWo0BkIylWTeYT4SU"
}
```

## 步驟 3：註冊將執行 MLModelTool 的流程代理程式

流程代理程式會依序執行一連串工具，並回傳最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求，並在 `model_id` 參數中提供模型 ID：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test agent for embedding model",
  "type": "flow",
  "description": "this is a test agent",
  "tools": [
    {
      "type": "MLModelTool",
      "description": "A general tool to answer any question",
      "parameters": {
        "model_id": "h5AUWo0BkIylWTeYT4SU",
        "prompt": "\n\nHuman:You are a professional data analyst. You will always answer question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say don't know. \n\nHuman:${parameters.question}\n\nAssistant:"
      }
    }
  ]
}
```
{% include copy-curl.html %} 

參數說明請參閱 [Register parameters](#register-parameters)。

OpenSearch 會回應代理程式 ID：

```json
{
  "agent_id": "9X7xWI0Bpc3sThaJdY9i"
}
```

## 步驟 4：執行代理程式

傳送下列請求以執行代理程式：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "question": "what's the population increase of Seattle from 2021 to 2023"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會回傳推論結果：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": " I do not have direct data on the population increase of Seattle from 2021 to 2023 in the context provided. As a data analyst, I would need to research population statistics from credible sources like the US Census Bureau to analyze population trends and make an informed estimate. Without looking up actual data, I don't have enough information to provide a specific answer to the question."
        }
      ]
    }
  ]
}
```

## 註冊參數

下表列出註冊代理程式時可用的所有工具參數。

Parameter	| Type | Required/Optional | Description	
:--- | :--- | :--- | :---
`model_id` | String | 必要 | 用於產生回應的大型語言模型 (LLM) 之模型 ID。
`prompt` | String | 選用 | 提供給 LLM 的提示詞。
`response_field` | String | 選用 | 回應欄位的名稱。預設為 `response`。

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

Parameter	| Type | Required/Optional | Description	
:--- | :--- | :--- | :---
`question` | String | 必要 | 要傳送給 LLM 的自然語言問題。 

## 測試工具

您可以將此工具作為代理程式工作流程的一部分執行，也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用來測試個別工具或執行獨立作業。