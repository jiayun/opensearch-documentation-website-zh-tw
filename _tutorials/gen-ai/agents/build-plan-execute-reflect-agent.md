---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立 plan-execute-reflect 代理程式"
parent: Agentic AI
grand_parent: Generative AI
nav_order: 20
---

# 建立 plan-execute-reflect 代理程式

這是實驗性功能，不建議在正式環境中使用。如需此功能的進度更新，或想提供意見回饋，請參閱相關的 [GitHub 議題](https://github.com/opensearch-project/ml-commons/issues/3745)。    
{: .warning}

本教學說明如何建立及使用 _plan-execute-reflect_ 代理程式。此代理程式可用於解決需要多步驟執行與推理的複雜問題。在此範例中，您將要求代理程式分析 OpenSearch 索引中的航班資料。如需此代理程式的詳細資訊，請參閱 [Plan-execute-reflect 代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/plan-execute-reflect/)。

請將開頭為前置字元 `your_` 的預留位置取代為您自己的值。
{: .note}

## 先決條件

登入 OpenSearch Dashboards 首頁，選取 **Add sample data**，然後新增 **Sample Flight data**。 

## 步驟 1：準備 LLM

plan-execute-reflect 代理程式需要大型語言模型 (LLM) 才能運作。本教學使用 [託管於 Amazon Bedrock 的 Anthropic Claude 3.7 模型](https://aws.amazon.com/bedrock/claude/)。您也可以[使用其他支援的 LLM]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/plan-execute-reflect/#supported-llms)。

### 步驟 1(a)：建立連接器

為模型建立連接器：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "Amazon Bedrock Claude 3.7-sonnet connector",
    "description": "Connector to Amazon Bedrock service for the Claude model",
    "version": 1,
    "protocol": "aws_sigv4",
    "parameters": {
      "region": "your_aws_region",
      "service_name": "bedrock",
      "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
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
        "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/converse",
        "headers": {
          "content-type": "application/json"
        },
        "request_body": "{ \"system\": [{\"text\": \"${parameters.system_prompt}\"}], \"messages\": [${parameters._chat_history:-}{\"role\":\"user\",\"content\":[{\"text\":\"${parameters.prompt}\"}]}${parameters._interactions:-}]${parameters.tool_configs:-} }"
      }
    ]
}
```
{% include copy-curl.html %}

請記下連接器 ID；您將使用它來註冊模型。

### 步驟 1(b)：註冊模型

註冊模型：

```json
POST /_plugins/_ml/models/_register
{
    "name": "Bedrock Claude Sonnet model",
    "function_name": "remote",
    "description": "Bedrock Claude 3.7 sonnet model for Plan, Execute and Reflect Agent",
    "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

請記下模型 ID；您將在後續步驟中使用它。

### 步驟 1(c)：設定重試原則

由於此代理程式是會執行多個步驟的長時間執行代理程式，我們強烈建議為您的連接器設定重試原則。如需詳細資訊，請參閱[請求本文欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#request-body-fields)中的 `client_config` 欄位。例如，若要設定無限重試，請將 `max_retry_times` 設為 `-1`：

```json
PUT /_plugins/_ml/connectors/{connector_id}
{
  "client_config": {
    "max_retry_times": -1,
    "retry_backoff_millis": 300,
    "retry_backoff_policy": "exponential_full_jitter"
  }
}
```
{% include copy-curl.html %}

如果您已部署模型或已進行 predict 呼叫，則必須先取消部署模型，才能更新 `client_config`。如需詳細資訊，請參閱 [Undeploy Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/undeploy-model/)。

如需部署模型的詳細資訊，請參閱 [Deploy Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/deploy-model/)。


## 步驟 2：建立代理程式

建立一個 `plan_execute_and_reflect` 代理程式，並使用下列資訊進行設定：

- 中繼資訊：`name`、`type`、`description`。
- LLM 資訊：代理程式使用 LLM 進行推理、擬定完成工作的計畫、使用適當的工具執行計畫中的步驟，並根據中間結果進行反思，以最佳化計畫。
- 工具：工具是代理程式可執行的函式。每個工具都可以定義自己的 `name`、`description`、`parameters` 和 `attributes`。
- 記憶體：儲存聊天訊息。OpenSearch 支援一種記憶體類型：`conversation_index`。

如需所有請求欄位的詳細資訊，請參閱 [Register Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/#request-body-fields)。

若要註冊代理程式，請傳送下列請求。在此範例中，您將建立一個具有 `ListIndexTool`、`SearchIndexTool` 和 `IndexMappingTool` 的代理程式：

```json
POST _plugins/_ml/agents/_register
{
  "name": "My Plan Execute and Reflect agent with Claude 3.7",
  "type": "plan_execute_and_reflect",
  "description": "this is a test agent",
  "llm": {
    "model_id": "your_llm_model_id_from_step1",
    "parameters": {
      "prompt": "${parameters.question}"
  }},
  "memory": {
    "type": "conversation_index"
  },
  "parameters": {
    "_llm_interface": "bedrock/converse/claude"
  },
  "tools": [
    {
      "type": "ListIndexTool"
    },
    {
      "type": "SearchIndexTool"
    },
    {
      "type": "IndexMappingTool"
    }
  ],
}
```
{% include copy-curl.html %}

請記下代理程式 ID；您將在下一個步驟中使用它。

您可以視需要設定與您的使用案例相關的其他工具。若要設定其他工具，請務必為工具提供 `attributes` 欄位。這點至關重要，因為 `attributes` 用於告知 LLM 執行工具時預期的輸入結構描述。

`ListIndexTool`、`SearchIndexTool`、`IndexMappingTool` 和 `WebSearchTool` 包含預先定義的屬性。例如，`ListIndexTool` 提供下列屬性：

```json
tools: [{
    "type": "ListIndexTool",
    "attributes": {
        "input_schema": {
            "type": "object",
            "properties": {
                "indices": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "OpenSearch index name list, separated by comma. for example: [\"index1\", \"index2\"], use empty array [] to list all indices in the cluster"
                }
            },
        },
        "strict": false
    }
}]
```

### 測試代理程式

使用下列提示來有效測試您的 `plan_execute_and_reflect` 代理程式：

- **追蹤代理程式執行**：使用 Get Message Traces API 檢視詳細的執行步驟：
  ```http
  GET _plugins/_ml/memory/message/your_message_id/traces
  ```

- **減少幻覺**：LLM 可能會因為選錯工具或誤解工作而「產生幻覺」，尤其是在代理程式設定了過多工具時。若要避免幻覺，請嘗試下列選項：
  - 限制代理程式中設定的工具數量。
  - 為每個工具提供清楚且具體的描述。
  - 確保代理程式能存取工作所需的所有工具。
  - 在提示中包含叢集的相關內容；例如 `Can you identify the error in my cluster by analyzing the "spans" and "logs" indexes?`

- **設定重試**：LLM 呼叫偶爾可能會失敗。設定重試可提升可靠性。如需詳細資訊，請參閱[請求本文欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#request-body-fields)中的 `client_config` 欄位。

若要測試代理程式，請使用 [Execute Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/) 執行它。由於此代理程式會執行長時間執行的工作，我們建議以非同步方式執行，以避免逾時。使用 `async=true` 查詢參數將代理程式作為個別工作執行：

```json
POST _plugins/_ml/agents/your_agent_id/_execute?async=true
{
  "parameters": {
    "question": "How many flights from Beijing to Seattle?"
  }
}
```
{% include copy-curl.html %}

請記下回應中的 `task_id` 和 `memory_id`。您將使用這些項目來追蹤進度及檢視結果。

使用下列請求來檢查工作仍在執行中或已完成：

```json
GET _plugins/_ml/tasks/your_task_id
```
{% include copy-curl.html %}

工作完成後，會傳回來自代理程式的回應：

```json
{
  "task_type": "AGENT_EXECUTION",
  "function_name": "AGENT",
  "state": "COMPLETED",
  "worker_node": [
    "q5yAqa75RM-rv0I67V1VVQ"
  ],
  "create_time": 1746148548710,
  "last_update_time": 1746148706345,
  "is_async": false,
  "response": {
    "memory_id": "bzWQjpYBKhItn1nNYHtu",
    "inference_results": [
      {
        "output": [
          {
            "result": "bzWQjpYBKhItn1nNYHtu",
            "name": "memory_id"
          },
          {
            "result": "cDWQjpYBKhItn1nNYHuS",
            "name": "parent_interaction_id"
          },
          {
            "result": "dTWQjpYBKhItn1nNbHsw",
            "name": "executor_agent_memory_id"
          },
          {
            "result": "YjWQjpYBKhItn1nN6oYk",
            "name": "executor_agent_parent_interaction_id"
          },
          {
            "name": "response",
            "dataAsMap": {
              "response": """# Comprehensive Analysis Report: Flights from Beijing to Seattle

## Executive Summary
After analyzing the OpenSearch sample flight dataset, I found that there are 0 direct flights from Beijing to Seattle in the dataset.

## Analysis Process

### Step 1: Identify Available Data Sources
I began by examining the indices available in the OpenSearch cluster to locate flight-related data. This search revealed one relevant index: `opensearch_dashboards_sample_data_flights`, which contains 13,059 flight records with comprehensive information including origin and destination cities, flight numbers, carriers, and other flight details.

### Step 2: Data Schema Analysis
I analyzed the index structure and confirmed it contains the necessary fields for this investigation, including:
- Origin/destination city names (`OriginCityName`, `DestCityName`) 
- Airport codes (`Origin`, `Dest`)
- Airport IDs (`OriginAirportID`, `DestAirportID`)
- Geographic information for origins and destinations

### Step 3: Query Construction and Execution
I created and executed a search query to find flights where:
- Origin city is Beijing (also checked for "Beijing Capital International Airport" and airport code "PEK")
- Destination city is Seattle (also checked for "Seattle Tacoma International Airport" and airport code "SEA")

### Step 4: Result Verification
To ensure the search was properly constructed, I verified that:
1. Flights from Beijing to other destinations exist in the dataset
2. Flights to Seattle from other origins exist in the dataset

This confirmed that both cities are represented in the data, but no flights connect them directly.

## Key Findings
- Beijing appears as an origin city in the dataset, with flights to destinations including Warsaw, Pittsburgh, Xi'an, Vienna, and Chicago/Rockford
- Seattle appears as both origin and destination in the dataset, with connections to cities like Vienna, Istanbul, New Orleans, St Louis, and Treviso
- The dataset contains 0 flights from Beijing to Seattle

## Conclusion
Based on a comprehensive search of the OpenSearch flight sample dataset, there are 0 flights from Beijing to Seattle in this dataset. While both cities appear in the dataset with connections to other locations, this specific route is not represented in the sample data."""
            }
          }
        ]
      }
    ]
  }
}
```

代理程式執行的回應包含幾個關鍵欄位：

- `memory_id`：儲存 `plan_execute_and_reflect` 代理程式與 LLM 之間所有交換訊息的記憶體 ID。
- `parent_interaction_id`：在規劃代理程式中啟動對話的父訊息之 `message_id`。
- `executor_agent_memory_id`：儲存內部執行代理程式與 LLM 之間交換訊息的記憶體 ID。
- `executor_agent_parent_interaction_id`：執行代理程式對話中父訊息的 `message_id`。
- `response`：代理程式在所有步驟執行完畢後產生的最終結果。

當您以非同步方式執行 plan-execute-reflect 代理程式時，API 會在代理程式啟動後傳回規劃代理程式的 `memory_id` 與 `parent_interaction_id`。

在最終回應中，API 也會傳回 `executor_agent_memory_id` 與 `executor_agent_parent_interaction_id`，對應至負責執行計畫中每個步驟的內部執行代理程式。`executor_agent_memory_id` 與 `executor_agent_parent_interaction_id` 一旦可用就會立即更新至任務中，甚至在代理程式完成執行之前。這使得即時追蹤執行過程成為可能。

若要檢視代理程式的訊息歷程記錄，請使用 Get Memory API：

```json
GET _plugins/_ml/memory/your_memory_id/messages
```
{% include copy-curl.html %}

如需更多資訊，請參閱 [Memory APIs]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/)。

記下相關訊息的 `message_id`，並使用它來擷取逐步執行追蹤：

```json
GET _plugins/_ml/memory/message/your_message_id/traces
```
{% include copy-curl.html %}

如需更多資訊，請參閱 [Get Message Traces API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/get-message-traces/)。

### 測試對話記憶

若要繼續相同的對話，請在執行代理程式時指定對話的 `memory_id`。先前的訊息會被擷取並作為上下文提供給模型。使用規劃代理程式的 `memory_id` 來繼續對話：

```json
POST _plugins/_ml/agents/your_agent_id/_execute?async=true
{
  "parameters": {
    "question": "your_question",
    "memory_id": "your_memory_id",
  }
}
```
{% include copy-curl.html %}

## 後續步驟

- 如需使用其他模型的資訊，請參閱 [支援的 LLM]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/plan-execute-reflect/#supported-llms)。
- 如需使用自訂提示建立代理程式的資訊，請參閱 [修改預設提示]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/plan-execute-reflect/#modifying-default-prompts)。