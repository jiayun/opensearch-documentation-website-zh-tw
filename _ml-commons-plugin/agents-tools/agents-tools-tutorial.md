---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理程式與工具教學"
parent: Agents and tools
grand_parent: ML Commons APIs
nav_order: 5
---

# 代理程式與工具教學
**於 2.13 版推出**
{: .label .label-purple }

下列教學說明如何建立用於檢索增強生成 (RAG) 的流程代理程式。流程代理程式會依指定的順序，循序執行其設定好的工具。在此範例中，您將建立一個含有兩個工具的代理程式：

1. `VectorDBTool`：代理程式將使用此工具擷取與使用者問題相關的 OpenSearch 文件。您會將補充資訊匯入 OpenSearch 索引。為了協助向量搜尋，您將部署文字嵌入模型，將文字轉譯為向量嵌入。OpenSearch 會將匯入的文件轉譯為嵌入，並儲存在索引中。當您向代理程式提供使用者問題時，代理程式會根據該問題建構查詢、在 OpenSearch 索引上執行向量搜尋，並將擷取到的相關文件傳遞給 `MLModelTool`。
1. `MLModelTool`：代理程式將執行此工具以連線至大型語言模型 (LLM)，並將以 OpenSearch 文件增補的使用者查詢傳送給模型。在此範例中，您將使用 [託管於 Amazon Bedrock 的 Anthropic Claude 模型](https://aws.amazon.com/bedrock/claude/)。LLM 接著會根據其知識與提供的文件回答問題。

## 先決條件

若要使用記憶功能，請先設定下列叢集設定。本教學假設您沒有專用的機器學習 (ML) 節點：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.only_run_on_ml_node": "false",
    "plugins.ml_commons.memory_feature_enabled": "true"
  }
}
```
{% include copy-curl.html %}

如需更多資訊，請參閱 [ML Commons 叢集設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/)。

## 步驟 1：註冊並部署文字嵌入模型

您需要文字嵌入模型來協助向量搜尋。本教學將使用 OpenSearch 提供的其中一個預先訓練模型。選取模型時，請留意其維度，因為建立索引時必須提供該維度。

在本教學中，您將使用 `huggingface/sentence-transformers/all-MiniLM-L12-v2` 模型，其會產生 384 維的稠密向量嵌入。若要註冊並部署模型，請傳送下列請求：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "huggingface/sentence-transformers/all-MiniLM-L12-v2",
  "version": "1.0.2",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

註冊模型是非同步工作。OpenSearch 會傳回此工作的任務 ID：

```json
{
  "task_id": "aFeif4oB5Vm0Tdw8yoN7",
  "status": "CREATED"
}
```

您可以呼叫 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 來查看工作狀態：

```json
GET /_plugins/_ml/tasks/aFeif4oB5Vm0Tdw8yoN7
```
{% include copy-curl.html %}

工作完成後，工作狀態會變更為 `COMPLETED`，且 ML Tasks API 回應會包含已部署模型的模型 ID：

```json
{
  "model_id": "aVeif4oB5Vm0Tdw8zYO2",
  "task_type": "REGISTER_MODEL",
  "function_name": "TEXT_EMBEDDING",
  "state": "COMPLETED",
  "worker_node": [
    "4p6FVOmJRtu3wehDD74hzQ"
  ],
  "create_time": 1694358489722,
  "last_update_time": 1694358499139,
  "is_async": true
}
```

## 步驟 2：建立資料匯入管線

若要將文字轉譯為向量嵌入，您將設定資料匯入管線。此管線會轉譯 `text` 欄位，並將產生的向量嵌入寫入 `embedding` 欄位。請在下列請求中指定前一步驟的 `model_id` 來建立管線：

```json
PUT /_ingest/pipeline/test-pipeline-local-model
{
  "description": "text embedding pipeline",
  "processors": [
    {
      "text_embedding": {
        "model_id": "aVeif4oB5Vm0Tdw8zYO2",
        "field_map": {
          "text": "embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 步驟 3：建立向量索引並匯入資料

現在您將把補充資料匯入 OpenSearch 索引。在 OpenSearch 中，向量會儲存在向量索引中。您可以傳送下列請求來建立[向量索引]({{site.url}}{{site.baseurl}}/search-plugins/knn/knn-index/)：

```json
PUT my_test_data
{
  "mappings": {
    "properties": {
      "text": {
        "type": "text"
      },
      "embedding": {
        "type": "knn_vector",
        "dimension": 384
      }
    }
  },
  "settings": {
    "index": {
      "knn.space_type": "cosinesimil",
      "default_pipeline": "test-pipeline-local-model",
      "knn": "true"
    }
  }
}
```
{% include copy-curl.html %}

接著，使用大量請求將資料匯入索引：

```json
POST _bulk
{"index": {"_index": "my_test_data", "_id": "1"}}
{"text": "Chart and table of population level and growth rate for the Ogden-Layton metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\nThe current metro area population of Ogden-Layton in 2023 is 750,000, a 1.63% increase from 2022.\nThe metro area population of Ogden-Layton in 2022 was 738,000, a 1.79% increase from 2021.\nThe metro area population of Ogden-Layton in 2021 was 725,000, a 1.97% increase from 2020.\nThe metro area population of Ogden-Layton in 2020 was 711,000, a 2.16% increase from 2019."}
{"index": {"_index": "my_test_data", "_id": "2"}}
{"text": "Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."}
{"index": {"_index": "my_test_data", "_id": "3"}}
{"text": "Chart and table of population level and growth rate for the Chicago metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Chicago in 2023 is 8,937,000, a 0.4% increase from 2022.\\nThe metro area population of Chicago in 2022 was 8,901,000, a 0.27% increase from 2021.\\nThe metro area population of Chicago in 2021 was 8,877,000, a 0.14% increase from 2020.\\nThe metro area population of Chicago in 2020 was 8,865,000, a 0.03% increase from 2019."}
{"index": {"_index": "my_test_data", "_id": "4"}}
{"text": "Chart and table of population level and growth rate for the Miami metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Miami in 2023 is 6,265,000, a 0.8% increase from 2022.\\nThe metro area population of Miami in 2022 was 6,215,000, a 0.78% increase from 2021.\\nThe metro area population of Miami in 2021 was 6,167,000, a 0.74% increase from 2020.\\nThe metro area population of Miami in 2020 was 6,122,000, a 0.71% increase from 2019."}
{"index": {"_index": "my_test_data", "_id": "5"}}
{"text": "Chart and table of population level and growth rate for the Austin metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Austin in 2023 is 2,228,000, a 2.39% increase from 2022.\\nThe metro area population of Austin in 2022 was 2,176,000, a 2.79% increase from 2021.\\nThe metro area population of Austin in 2021 was 2,117,000, a 3.12% increase from 2020.\\nThe metro area population of Austin in 2020 was 2,053,000, a 3.43% increase from 2019."}
{"index": {"_index": "my_test_data", "_id": "6"}}
{"text": "Chart and table of population level and growth rate for the Seattle metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Seattle in 2023 is 3,519,000, a 0.86% increase from 2022.\\nThe metro area population of Seattle in 2022 was 3,489,000, a 0.81% increase from 2021.\\nThe metro area population of Seattle in 2021 was 3,461,000, a 0.82% increase from 2020.\\nThe metro area population of Seattle in 2020 was 3,433,000, a 0.79% increase from 2019."}
```
{% include copy-curl.html %}

## 步驟 4：建立外部託管模型的連接器

您需要一個 LLM 來產生對使用者問題的回應。LLM 對 OpenSearch 叢集而言太過龐大，因此您將建立與外部託管 LLM 的連線。在本範例中，您將建立連接器，連線至託管於 Amazon Bedrock 的 Anthropic Claude 模型：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "BedRock test claude Connector",
  "description": "The connector to BedRock service for claude model",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
      "region": "us-east-1",
      "service_name": "bedrock",
      "anthropic_version": "bedrock-2023-05-31",
      "endpoint": "bedrock.us-east-1.amazonaws.com",
      "auth": "Sig_V4",
      "content_type": "application/json",
      "max_tokens_to_sample": 8000,
      "temperature": 0.0001,
      "response_filter": "$.completion"
  },
  "credential": {
      "access_key": "<bedrock_access_key>",
      "secret_key": "<bedrock_secret_key>",
      "session_token": "<bedrock_session_token>"
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

回應包含新建連接器的連接器 ID：

```json
{
  "connector_id": "a1eMb4kBJ1eYAeTMAljY"
}
```

## 步驟 5：註冊並部署外部託管模型

如同文字嵌入模型，LLM 也需要註冊並部署到 OpenSearch。若要設定外部託管模型，請先為此模型建立模型群組：

```json
POST /_plugins/_ml/model_groups/_register
{
    "name": "test_model_group_bedrock",
    "description": "This is a public model group"
}
```
{% include copy-curl.html %}

回應包含模型群組 ID，您將使用它將模型註冊到此模型群組：

```json
{
 "model_group_id": "wlcnb4kBJ1eYAeTMHlV6",
 "status": "CREATED"
}

```

接下來，註冊並部署外部託管的 Claude 模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "Bedrock Claude V2 model",
    "function_name": "remote",
    "model_group_id": "wlcnb4kBJ1eYAeTMHlV6",
    "description": "test model",
    "connector_id": "a1eMb4kBJ1eYAeTMAljY"
}
```
{% include copy-curl.html %}

與[步驟 1](#step-1-register-and-deploy-a-text-embedding-model)類似，回應包含一個任務 ID，您可以用它來檢查部署狀態。模型部署完成後，狀態會變更為 `COMPLETED`，且回應會包含 Claude 模型的模型 ID：

```json
{
  "model_id": "NWR9YIsBUysqmzBdifVJ",
  "task_type": "REGISTER_MODEL",
  "function_name": "remote",
  "state": "COMPLETED",
  "worker_node": [
    "4p6FVOmJRtu3wehDD74hzQ"
  ],
  "create_time": 1694358489722,
  "last_update_time": 1694358499139,
  "is_async": true
}
```

若要測試 LLM，請傳送下列 predict 請求：

```json
POST /_plugins/_ml/models/NWR9YIsBUysqmzBdifVJ/_predict
{
  "parameters": {
    "prompt": "\n\nHuman:hello\n\nAssistant:"
  }
}
```
{% include copy-curl.html %}

## 步驟 6：註冊並執行代理程式

最後，您將使用步驟 1 建立的文字嵌入模型與步驟 5 建立的 Claude 模型來建立流程代理程式。此流程代理程式會先執行 `VectorDBTool`，再執行 `MLModelTool`。`VectorDBTool` 已設定為使用步驟 1 建立的文字嵌入模型的模型 ID，以進行向量搜尋。`MLModelTool` 則設定為使用步驟 5 建立的 Claude 模型：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_RAG",
  "type": "flow",
  "description": "this is a test agent",
  "tools": [
    {
      "type": "VectorDBTool",
      "parameters": {
        "model_id": "aVeif4oB5Vm0Tdw8zYO2",
        "index": "my_test_data",
        "embedding_field": "embedding",
        "source_field": ["text"],
        "input": "${parameters.question}"
      }
    },
    {
      "type": "MLModelTool",
      "description": "A general tool to answer any question",
      "parameters": {
        "model_id": "NWR9YIsBUysqmzBdifVJ",
        "prompt": "\n\nHuman:You are a professional data analyst. You will always answer a question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say you don't know. \n\n Context:\n${parameters.VectorDBTool.output}\n\nHuman:${parameters.question}\n\nAssistant:"
      }
    }
  ]
}
```
{% include copy-curl.html %}

OpenSearch 會為新建的代理程式傳回代理程式 ID：

```json
{
  "agent_id": "879v9YwBjWKCe6Kg12Tx"
}
```

您可以向 `agents` 端點傳送請求並提供代理程式 ID，以檢視該代理程式：

```json
GET /_plugins/_ml/agents/879v9YwBjWKCe6Kg12Tx
```
{% include copy-curl.html %}

若要執行代理程式，請傳送下列請求。註冊代理程式時，您已將其設定為接受 `parameters.question`，因此您必須在請求中提供此參數。此參數代表由人工產生的使用者問題：

```json
POST /_plugins/_ml/agents/879v9YwBjWKCe6Kg12Tx/_execute
{
  "parameters": {
    "question": "what's the population increase of Seattle from 2021 to 2023"
  }
}
```
{% include copy-curl.html %}

LLM 的知識庫中沒有最新資訊，因此它會根據已匯入的資料推論問題的回應，這展示了 RAG：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "result": """ Based on the given context, the key information is:

The metro area population of Seattle in 2021 was 3,461,000.
The metro area population of Seattle in 2023 is 3,519,000.

To calculate the population increase from 2021 to 2023:

Population in 2023 (3,519,000) - Population in 2021 (3,461,000) = 58,000

Therefore, the population increase of Seattle from 2021 to 2023 is 58,000."""
        }
      ]
    }
  ]
}
```
