---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立您自己的聊天機器人"
parent: Chatbots
grand_parent: Generative AI
has_children: false
has_toc: false
nav_order: 170
redirect_from:
  - /ml-commons-plugin/tutorials/build-chatbot/
  - /vector-search/tutorials/chatbots/build-chatbot/
---

# 建立您自己的聊天機器人

有時大型語言模型 (LLM) 無法立即回答問題。例如，LLM 無法告訴您上週記錄索引中有多少錯誤，因為其知識庫不包含您的專有資料。在這種情況下，您需要在後續呼叫中向 LLM 提供額外資訊。您可以使用代理程式來解決這類複雜問題。代理程式可以執行工具，從設定的資料來源取得更多資訊，並將額外資訊作為上下文傳送給 LLM。

本教學說明如何使用 `conversational` 代理程式在 OpenSearch 中建立您自己的聊天機器人。如需代理程式的更多資訊，請參閱 [代理程式與工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/index/)。

將以 `your_` 前綴開頭的預留位置替換為您自己的值。
{: .note}

## 必要條件

登入 OpenSearch Dashboards 首頁，選取 **Add sample data**，並新增 **Sample eCommerce orders** 資料。

## 步驟 1：設定知識庫

完成必要條件，並依照 [使用對話流程代理程式的 RAG 教學]({{site.url}}{{site.baseurl}}/ml-commons-plugin/tutorials/rag-conversational-agent/) 的步驟 1 設定 `test_population_data` 知識庫索引，其中包含美國城市人口資料。

建立資料匯入管線：

```json
PUT /_ingest/pipeline/test_stock_price_data_pipeline
{
  "description": "text embedding pipeline",
  "processors": [
    {
      "text_embedding": {
        "model_id": "your_text_embedding_model_id",
        "field_map": {
          "stock_price_history": "stock_price_history_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

建立包含歷史股價資料的 `test_stock_price_data` 索引：

```json
PUT test_stock_price_data
{
  "mappings": {
    "properties": {
      "stock_price_history": {
        "type": "text"
      },
      "stock_price_history_embedding": {
        "type": "knn_vector",
        "dimension": 384
      }
    }
  },
  "settings": {
    "index": {
      "knn.space_type": "cosinesimil",
      "default_pipeline": "test_stock_price_data_pipeline",
      "knn": "true"
    }
  }
}
```
{% include copy-curl.html %}

將資料匯入索引：

```json
POST _bulk
{"index": {"_index": "test_stock_price_data"}}
{"stock_price_history": "This is the historical montly stock price record for Amazon.com, Inc. (AMZN) with CSV format.\nDate,Open,High,Low,Close,Adj Close,Volume\n2023-03-01,93.870003,103.489998,88.120003,103.290001,103.290001,1349240300\n2023-04-01,102.300003,110.860001,97.709999,105.449997,105.449997,1224083600\n2023-05-01,104.949997,122.919998,101.150002,120.580002,120.580002,1432891600\n2023-06-01,120.690002,131.490005,119.930000,130.360001,130.360001,1242648800\n2023-07-01,130.820007,136.649994,125.919998,133.679993,133.679993,1058754800\n2023-08-01,133.550003,143.630005,126.410004,138.009995,138.009995,1210426200\n2023-09-01,139.460007,145.860001,123.040001,127.120003,127.120003,1120271900\n2023-10-01,127.279999,134.479996,118.349998,133.089996,133.089996,1224564700\n2023-11-01,133.960007,149.259995,133.710007,146.089996,146.089996,1025986900\n2023-12-01,146.000000,155.630005,142.809998,151.940002,151.940002,931128600\n2024-01-01,151.539993,161.729996,144.050003,155.199997,155.199997,953344900\n2024-02-01,155.869995,175.000000,155.619995,174.449997,174.449997,437720800\n"}
{"index": {"_index": "test_stock_price_data"}}
{"stock_price_history": "This is the historical montly stock price record for Apple Inc. (AAPL) with CSV format.\nDate,Open,High,Low,Close,Adj Close,Volume\n2023-03-01,146.830002,165.000000,143.899994,164.899994,164.024475,1520266600\n2023-04-01,164.270004,169.850006,159.779999,169.679993,168.779099,969709700\n2023-05-01,169.279999,179.350006,164.309998,177.250000,176.308914,1275155500\n2023-06-01,177.699997,194.479996,176.929993,193.970001,193.207016,1297101100\n2023-07-01,193.779999,198.229996,186.600006,196.449997,195.677261,996066400\n2023-08-01,196.240005,196.729996,171.960007,187.869995,187.130997,1322439400\n2023-09-01,189.490005,189.979996,167.619995,171.210007,170.766846,1337586600\n2023-10-01,171.220001,182.339996,165.669998,170.770004,170.327972,1172719600\n2023-11-01,171.000000,192.929993,170.119995,189.949997,189.458313,1099586100\n2023-12-01,190.330002,199.619995,187.449997,192.529999,192.284637,1062774800\n2024-01-01,187.149994,196.380005,180.169998,184.399994,184.164993,1187219300\n2024-02-01,183.990005,191.050003,179.250000,188.850006,188.609329,420063900\n"}
{"index": {"_index": "test_stock_price_data"}}
{"stock_price_history": "This is the historical montly stock price record for NVIDIA Corporation (NVDA) with CSV format.\nDate,Open,High,Low,Close,Adj Close,Volume\n2023-03-01,231.919998,278.339996,222.970001,277.769989,277.646820,1126373100\n2023-04-01,275.089996,281.100006,262.200012,277.489990,277.414032,743592100\n2023-05-01,278.399994,419.380005,272.399994,378.339996,378.236420,1169636000\n2023-06-01,384.890015,439.899994,373.559998,423.019989,422.904175,1052209200\n2023-07-01,425.170013,480.880005,413.459991,467.290009,467.210449,870489500\n2023-08-01,464.600006,502.660004,403.109985,493.549988,493.465942,1363143600\n2023-09-01,497.619995,498.000000,409.799988,434.989990,434.915924,857510100\n2023-10-01,440.299988,476.089996,392.299988,407.799988,407.764130,1013917700\n2023-11-01,408.839996,505.480011,408.690002,467.700012,467.658905,914386300\n2023-12-01,465.250000,504.329987,450.100006,495.220001,495.176453,740951700\n2024-01-01,492.440002,634.929993,473.200012,615.270020,615.270020,970385300\n2024-02-01,621.000000,721.849976,616.500000,721.330017,721.330017,355346500\n"}
{"index": {"_index": "test_stock_price_data"}}
{"stock_price_history": "This is the historical montly stock price record for Meta Platforms, Inc. (META) with CSV format.\n\nDate,Open,High,Low,Close,Adj Close,Volume\n2023-03-01,174.589996,212.169998,171.429993,211.940002,211.940002,690053000\n2023-04-01,208.839996,241.690002,207.130005,240.320007,240.320007,446687900\n2023-05-01,238.619995,268.649994,229.850006,264.720001,264.720001,486968500\n2023-06-01,265.899994,289.790009,258.880005,286.980011,286.980011,480979900\n2023-07-01,286.700012,326.200012,284.850006,318.600006,318.600006,624605100\n2023-08-01,317.540009,324.140015,274.380005,295.890015,295.890015,423147800\n2023-09-01,299.369995,312.869995,286.790009,300.209991,300.209991,406686600\n2023-10-01,302.739990,330.540009,279.399994,301.269989,301.269989,511307900\n2023-11-01,301.850006,342.920013,301.850006,327.149994,327.149994,329270500\n2023-12-01,325.480011,361.899994,313.660004,353.959991,353.959991,332813800\n2024-01-01,351.320007,406.359985,340.010010,390.140015,390.140015,347020200\n2024-02-01,393.940002,485.959991,393.049988,473.279999,473.279999,294260900\n"}
{"index": {"_index": "test_stock_price_data"}}
{"stock_price_history": "This is the historical montly stock price record for Microsoft Corporation (MSFT) with CSV format.\n\nDate,Open,High,Low,Close,Adj Close,Volume\n2023-03-01,250.759995,289.269989,245.610001,288.299988,285.953064,747635000\n2023-04-01,286.519989,308.929993,275.369995,307.260010,304.758759,551497100\n2023-05-01,306.970001,335.940002,303.399994,328.390015,325.716766,600807200\n2023-06-01,325.929993,351.470001,322.500000,340.540009,338.506226,547588700\n2023-07-01,339.190002,366.779999,327.000000,335.920013,333.913818,666764400\n2023-08-01,335.190002,338.540009,311.549988,327.760010,325.802582,479456700\n2023-09-01,331.309998,340.859985,309.450012,315.750000,314.528809,416680700\n2023-10-01,316.279999,346.200012,311.209991,338.109985,336.802307,540907000\n2023-11-01,339.790009,384.299988,339.649994,378.910004,377.444519,563880300\n2023-12-01,376.760010,378.160004,362.899994,376.040009,375.345886,522003700\n2024-01-01,373.859985,415.320007,366.500000,397.579987,396.846130,528399000\n2024-02-01,401.829987,420.820007,401.799988,409.489990,408.734131,237639700\n"}
{"index": {"_index": "test_stock_price_data"}}
{"stock_price_history": "This is the historical montly stock price record for Alphabet Inc. (GOOG) with CSV format.\n\nDate,Open,High,Low,Close,Adj Close,Volume\n2023-03-01,90.160004,107.510002,89.769997,104.000000,104.000000,725477100\n2023-04-01,102.669998,109.629997,102.379997,108.220001,108.220001,461670700\n2023-05-01,107.720001,127.050003,104.500000,123.370003,123.370003,620317400\n2023-06-01,123.500000,129.550003,116.910004,120.970001,120.970001,521386300\n2023-07-01,120.320000,134.070007,115.830002,133.110001,133.110001,525456900\n2023-08-01,130.854996,138.399994,127.000000,137.350006,137.350006,463482000\n2023-09-01,138.429993,139.929993,128.190002,131.850006,131.850006,389593900\n2023-10-01,132.154999,142.380005,121.459999,125.300003,125.300003,514877100\n2023-11-01,125.339996,141.100006,124.925003,133.919998,133.919998,405635900\n2023-12-01,133.320007,143.945007,129.399994,140.929993,140.929993,482059400\n2024-01-01,139.600006,155.199997,136.850006,141.800003,141.800003,428771200\n2024-02-01,143.690002,150.695007,138.169998,147.139999,147.139999,231934100\n"}
```
{% include copy-curl.html %}

## 步驟 2：準備 LLM

本教學使用 [Amazon Bedrock Claude 模型](https://aws.amazon.com/bedrock/claude/)。您也可以使用其他 LLM。如需更多資訊，請參閱[連線至外部託管的模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。

為模型建立連接器：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Bedrock Claude Sonnet 5",
  "description": "The connector to BedRock service for claude model",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "us-east-1",
    "service_name": "bedrock",
    "model": "us.anthropic.claude-sonnet-5",
    "response_filter": "$.output.message.content[0].text"
  },
  "credential": {
    "access_key": "your_aws_access_key",
    "secret_key": "your_aws_secret_key",
    "session_token": "your_aws_session_token"
  },
  "actions": [{
    "action_type": "predict",
    "method": "POST",
    "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/converse",
    "headers": { "content-type": "application/json" },
    "request_body": "{\"messages\": [${parameters._chat_history:-}{\"role\":\"user\",\"content\":[{\"text\":\"${parameters.prompt:-}\"}]}${parameters._interactions:-}]${parameters.tool_configs:-}}"
  }]
}
```
{% include copy-curl.html %}

請記下連接器 ID；您將使用它來註冊模型。

註冊模型：

```json
POST /_plugins/_ml/models/_register
{
    "name": "Bedrock Claude Instant model",
    "function_name": "remote",
    "description": "Bedrock Claude instant-v1 model",
    "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

請記下 LLM 模型 ID；您將在後續步驟中使用它。

部署模型：

```json
POST /_plugins/_ml/models/your_LLM_model_id/_deploy
```
{% include copy-curl.html %}

測試模型：

```json
POST /_plugins/_ml/models/your_LLM_model_id/_predict
{
  "parameters": {
    "prompt": "\n\nHuman: how are you? \n\nAssistant:"
  }
}
```
{% include copy-curl.html %}

## 步驟 3：使用預設提示建立代理程式

接著，建立並測試代理程式。

### 建立代理程式

建立 `conversational` 類型的代理程式。

代理程式會使用下列資訊進行設定：

- 中繼資訊：`name`、`type`、`description`。
- LLM 資訊：代理程式使用 LLM 進行推理並選擇下一個步驟，包括選擇合適的工具及準備工具輸入。
- 工具：工具是代理程式可執行的函式。每個工具都可以定義自己的 `name`、`description` 和 `parameters`。
- 記憶體：儲存聊天訊息。OpenSearch 支援一種記憶體類型：`conversation_index`。

代理程式包含下列參數：

- `conversational`：此代理程式類型具有內建的提示。若要使用您自己的提示加以覆寫，請參閱[步驟 4](#step-4-optional-create-an-agent-with-a-custom-prompt)。
- `app_type`：指定此參數以供參照之用，以便區分多個代理程式。
- `llm`：定義 LLM 組態：
   - `"max_iteration": 5`：代理程式最多執行 LLM 五次。
   - `"response_filter": "$.completion"`：從 Bedrock Claude 模型回應中擷取 LLM 答案時所需。
   - `"message_history_limit": 5`：代理程式最多擷取五則最近的歷史訊息，並將其加入 LLM 內容。將此參數設為 `0` 以在內容中省略訊息歷史記錄。
   - `disable_trace`：若為 `true`，則代理程式不會將追蹤資料儲存在記憶體中。追蹤資料會包含在每則訊息中，並詳細說明產生訊息時所執行的步驟。
- `memory`：定義如何儲存訊息。OpenSearch 僅支援 `conversation_index` 記憶體，其會將訊息儲存在記憶體索引中。
- 工具：
   - LLM 會進行推理以決定要執行哪個工具，並準備工具的輸入。
   - 若要在回應中包含工具的輸出，請指定 `"include_output_in_agent_response": true`。在本教學中，您將在回應中包含 `PPLTool` 輸出（請參閱[測試代理程式](#test-the-agent)中的範例回應）。
   - 依預設，工具的 `name` 與工具的 `type` 相同，且每個工具都有預設描述。您可以覆寫工具的 `name` 和 `description`。
   - `tools` 清單中的每個工具都必須有唯一的名稱。例如，下列示範代理程式定義了兩個 `VectorDBTool` 類型且名稱不同的工具（`population_data_knowledge_base` 和 `stock_price_data_knowledge_base`）。每個工具都有自訂描述，以便 LLM 輕鬆理解該工具的功能。
   
   如需工具的詳細資訊，請參閱[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。

此範例請求會在代理程式中設定數個範例工具。您可以視需要設定與您的使用案例相關的其他工具。
{: .note}

註冊代理程式：

```json
POST _plugins/_ml/agents/_register
{
  "name": "Chat Agent with Claude",
  "type": "conversational",
  "description": "this is a test agent",
  "app_type": "os_chat",
  "llm": {
    "model_id": "your_llm_model_id_from_step2",
    "parameters": {
      "max_iteration": 5,
      "response_filter": "$.completion",
      "message_history_limit": 5,
      "disable_trace": false
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "tools": [
    {
      "type": "PPLTool",
      "parameters": {
        "model_id": "your_llm_model_id_from_step2",
        "model_type": "CLAUDE",
        "execute": true
      },
      "include_output_in_agent_response": true
    },
    {
      "type": "VisualizationTool",
      "parameters": {
        "index": ".kibana"
      },
      "include_output_in_agent_response": true
    },
    {
      "type": "VectorDBTool",
      "name": "population_data_knowledge_base",
      "description": "This tool provide population data of US cities.",
      "parameters": {
        "input": "${parameters.question}",
        "index": "test_population_data",
        "source_field": [
          "population_description"
        ],
        "model_id": "your_embedding_model_id_from_step1",
        "embedding_field": "population_description_embedding",
        "doc_size": 3
      }
    },
    {
      "type": "VectorDBTool",
      "name": "stock_price_data_knowledge_base",
      "description": "This tool provide stock price data.",
      "parameters": {
        "input": "${parameters.question}",
        "index": "test_stock_price_data",
        "source_field": [
          "stock_price_history"
        ],
        "model_id": "your_embedding_model_id_from_step1",
        "embedding_field": "stock_price_history_embedding",
        "doc_size": 3
      }
    },
    {
      "type": "ListIndexTool",
      "description": "Use this tool to get OpenSearch index information: (health, status, index, uuid, primary count, replica count, docs.count, docs.deleted, store.size, primary.store.size). \nIt takes 2 optional arguments named `index` which is a comma-delimited list of one or more indices to get information from (default is an empty list meaning all indices), and `local` which means whether to return information from the local node only instead of the cluster manager node (default is false)."
    },
    {
      "type": "SearchAnomalyDetectorsTool"
    },
    {
      "type": "SearchAnomalyResultsTool"
    },
    {
      "type": "SearchMonitorsTool"
    },
    {
      "type": "SearchAlertsTool"
    }
  ]
}
```
{% include copy-curl.html %}

請記下代理程式 ID；您將在下一個步驟中使用它。

### 測試代理程式

請注意下列測試提示：

- 您可以透過下列其中一種方式檢視代理程式執行的詳細步驟：
   - 啟用詳細模式：`"verbose": true`。
   - 呼叫 Get Trace API：`GET _plugins/_ml/memory/message/your_message_id/traces`。

- LLM 可能會產生幻覺。它可能選擇錯誤的工具來解決您的問題，尤其是當您設定了許多工具時。為避免產生幻覺，請嘗試下列選項：
   - 避免在代理程式中設定過多工具。
   - 提供詳細的工具說明，釐清該工具可以做什麼。
   - 在 LLM 問題中指定要使用的工具，例如 `Can you use the PPLTool to query the opensearch_dashboards_sample_data_ecommerce index so it can calculate how many orders were placed last week?`。
   - 在執行代理程式時指定要使用的工具。例如，指定僅使用 `PPLTool` 和 `ListIndexTool` 來處理目前的請求。

測試代理程式：

```json
POST _plugins/_ml/agents/your_agent_id/_execute
{
    "parameters": {
    "question": "Can you query with index opensearch_dashboards_sample_data_ecommerce to calculate how many orders in last week?",
    "verbose": false,
    "selected_tools": ["PPLTool", "ListIndexTool"]
    }
}
```
{% include copy-curl.html %}

<!-- vale off -->
#### 測試 PPLTool
<!-- vale on -->

```json
POST _plugins/_ml/agents/your_agent_id/_execute
{
  "parameters": {
    "question": "Can you query with index opensearch_dashboards_sample_data_ecommerce to calculate how many orders in last week?",
    "verbose": false
  }
}
```
{% include copy-curl.html %}

因為您為 `PPLTool` 指定了 `"include_output_in_agent_response": true`，所以回應在 `additional_info` 物件中包含 `PPLTool.output`：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "memory_id",
          "result": "TkJwyI0Bn3OCesyvzuH9"
        },
        {
          "name": "parent_interaction_id",
          "result": "T0JwyI0Bn3OCesyvz-EI"
        },
        {
          "name": "response",
          "dataAsMap": {
            "response": "The tool response from the PPLTool shows that there were 3812 orders in the opensearch_dashboards_sample_data_ecommerce index within the last week.",
            "additional_info": {
              "PPLTool.output": [
                """{"ppl":"source\u003dopensearch_dashboards_sample_data_ecommerce| where order_date \u003e DATE_SUB(NOW(), INTERVAL 1 WEEK) | stats COUNT() AS count","executionResult":"{\n  \"schema\": [\n    {\n      \"name\": \"count\",\n      \"type\": \"integer\"\n    }\n  ],\n  \"datarows\": [\n    [\n      3812\n    ]\n  ],\n  \"total\": 1,\n  \"size\": 1\n}"}"""
              ]
            }
          }
        }
      ]
    }
  ]
}
```
{% include copy-curl.html %}

取得追蹤資料：

```json
GET _plugins/_ml/memory/message/T0JwyI0Bn3OCesyvz-EI/traces
```
{% include copy-curl.html %}

<!-- vale off -->
#### 測試 population_data_knowledge_base VectorDBTool
<!-- vale on -->

若要檢視詳細步驟，請在執行代理程式時將 `verbose` 設定為 `true`：

```json
POST _plugins/_ml/agents/your_agent_id/_execute
{
  "parameters": {
    "question": "What's the population increase of Seattle from 2021 to 2023?",
    "verbose": true
  }
}
```
{% include copy-curl.html %}

回應包含執行步驟：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "memory_id",
          "result": "LkJuyI0Bn3OCesyv3-Ef"
        },
        {
          "name": "parent_interaction_id",
          "result": "L0JuyI0Bn3OCesyv3-Er"
        },
        {
          "name": "response",
          "result": """{
  "thought": "Let me check the population data tool",
  "action": "population_data_knowledge_base",
  "action_input": "{'question': 'What is the population increase of Seattle from 2021 to 2023?', 'cities': ['Seattle']}"
}"""
        },
        {
          "name": "response",
          "result": """{"_index":"test_population_data","_source":{"population_description":"Chart and table of population level and growth rate for the Seattle metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Seattle in 2023 is 3,519,000, a 0.86% increase from 2022.\\nThe metro area population of Seattle in 2022 was 3,489,000, a 0.81% increase from 2021.\\nThe metro area population of Seattle in 2021 was 3,461,000, a 0.82% increase from 2020.\\nThe metro area population of Seattle in 2020 was 3,433,000, a 0.79% increase from 2019."},"_id":"9EJsyI0Bn3OCesyvU-B7","_score":0.75154537}
{"_index":"test_population_data","_source":{"population_description":"Chart and table of population level and growth rate for the Austin metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Austin in 2023 is 2,228,000, a 2.39% increase from 2022.\\nThe metro area population of Austin in 2022 was 2,176,000, a 2.79% increase from 2021.\\nThe metro area population of Austin in 2021 was 2,117,000, a 3.12% increase from 2020.\\nThe metro area population of Austin in 2020 was 2,053,000, a 3.43% increase from 2019."},"_id":"80JsyI0Bn3OCesyvU-B7","_score":0.6689899}
{"_index":"test_population_data","_source":{"population_description":"Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."},"_id":"8EJsyI0Bn3OCesyvU-B7","_score":0.66782206}
"""
        },
        {
          "name": "response",
          "result": "According to the population data tool, the population of Seattle increased by approximately 28,000 people from 2021 to 2023, which is a 0.82% increase from 2021 to 2022 and a 0.86% increase from 2022 to 2023."
        }
      ]
    }
  ]
}
```

取得追蹤資料：

```json
GET _plugins/_ml/memory/message/L0JuyI0Bn3OCesyv3-Er/traces
```
{% include copy-curl.html %}

#### 測試對話記憶

若要延續相同的對話，請在執行代理程式時指定該對話的 `memory_id`：

```json
POST _plugins/_ml/agents/your_agent_id/_execute
{
  "parameters": {
    "question": "What's the population of Austin 2023, compare with Seattle",
    "memory_id": "LkJuyI0Bn3OCesyv3-Ef",
    "verbose": true
  }
}
```
{% include copy-curl.html %}

在回應中，請注意 `population_data_knowledge_base` 並未傳回西雅圖的人口數。代理程式是透過參考歷史訊息得知西雅圖的人口數：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "memory_id",
          "result": "LkJuyI0Bn3OCesyv3-Ef"
        },
        {
          "name": "parent_interaction_id",
          "result": "00J6yI0Bn3OCesyvIuGZ"
        },
        {
          "name": "response",
          "result": """{
  "thought": "Let me check the population data tool first",
  "action": "population_data_knowledge_base",
  "action_input": "{\"city\":\"Austin\",\"year\":2023}"
}"""
        },
        {
          "name": "response",
          "result": """{"_index":"test_population_data","_source":{"population_description":"Chart and table of population level and growth rate for the Austin metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Austin in 2023 is 2,228,000, a 2.39% increase from 2022.\\nThe metro area population of Austin in 2022 was 2,176,000, a 2.79% increase from 2021.\\nThe metro area population of Austin in 2021 was 2,117,000, a 3.12% increase from 2020.\\nThe metro area population of Austin in 2020 was 2,053,000, a 3.43% increase from 2019."},"_id":"BhF5vo0BubpYKX5ER0fT","_score":0.69129956}
{"_index":"test_population_data","_source":{"population_description":"Chart and table of population level and growth rate for the Austin metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Austin in 2023 is 2,228,000, a 2.39% increase from 2022.\\nThe metro area population of Austin in 2022 was 2,176,000, a 2.79% increase from 2021.\\nThe metro area population of Austin in 2021 was 2,117,000, a 3.12% increase from 2020.\\nThe metro area population of Austin in 2020 was 2,053,000, a 3.43% increase from 2019."},"_id":"6zrZvo0BVR2NrurbRIAE","_score":0.69129956}
{"_index":"test_population_data","_source":{"population_description":"Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."},"_id":"AxF5vo0BubpYKX5ER0fT","_score":0.61015373}
"""
        },
        {
          "name": "response",
          "result": "According to the population data tool, the population of Austin in 2023 is approximately 2,228,000 people, a 2.39% increase from 2022. This is lower than the population of Seattle in 2023 which is approximately 3,519,000 people, a 0.86% increase from 2022."
        }
      ]
    }
  ]
}
```

檢視所有訊息：

```json
GET _plugins/_ml/memory/LkJuyI0Bn3OCesyv3-Ef/messages
```
{% include copy-curl.html %}

取得追蹤資料：

```json
GET _plugins/_ml/memory/message/00J6yI0Bn3OCesyvIuGZ/traces
```
{% include copy-curl.html %}

## 步驟 4 (選用)：使用自訂提示建立代理程式

所有代理程式都有下列預設提示：

```json
"prompt": """

Human:${parameters.prompt.prefix}

${parameters.prompt.suffix}

Human: follow RESPONSE FORMAT INSTRUCTIONS

Assistant:"""
```

提示由兩個部分組成：

- `${parameters.prompt.prefix}`：描述 AI 助理能做什麼的提示前置詞。您可以根據使用案例變更此參數，例如 `You are a professional data analyst. You will always answer questions based on the tool response first. If you don't know the answer, just say you don't know.`
- `${parameters.prompt.suffix}`：提示的主要部分，定義工具、聊天記錄、提示格式指示、問題和暫存區。

預設的 `prompt.suffix` 如下：

```json
"prompt.suffix": """Human:TOOLS
------
Assistant can ask Human to use tools to look up information that may be helpful in answering the users original question. The tool response will be listed in "TOOL RESPONSE of {tool name}:". If TOOL RESPONSE is enough to answer human's question, Assistant should avoid rerun the same tool. 
Assistant should NEVER suggest run a tool with same input if it's already in TOOL RESPONSE. 
The tools the human can use are:

${parameters.tool_descriptions}

${parameters.chat_history}

${parameters.prompt.format_instruction}


Human:USER'S INPUT
--------------------
Here is the user's input :
${parameters.question}

${parameters.scratchpad}"""
```

`prompt.suffix` 由下列預留位置組成：

- `${parameters.tool_descriptions}`：此預留位置會填入代理程式的工具資訊：工具名稱和描述。如果您省略此預留位置，代理程式將不會使用任何工具。
- `${parameters.prompt.format_instruction}`：此預留位置定義 LLM 回應格式。此預留位置至關重要，我們不建議移除它。
- `${parameters.chat_history}`：此預留位置會填入目前記憶體的訊息記錄。如果您在執行代理程式時未設定 `memory_id`，或沒有歷史訊息，則此預留位置會是空的。如果您不需要聊天記錄，可以移除此預留位置。
- `${parameters.question}`：此預留位置會填入使用者問題。
- `${parameters.scratchpad}`：此預留位置會填入詳細的代理程式執行步驟。這些步驟與您指定詳細模式或取得追蹤資料時所看到的步驟相同 (請參閱[測試代理程式](#test-the-agent)中的範例)。此預留位置至關重要，可讓 LLM 根據先前步驟的結果進行推理並選取下一個步驟。我們不建議移除此預留位置。

### 自訂提示範例

下列範例示範如何自訂提示。

#### 範例 1：自訂 `prompt.prefix`

使用自訂 `prompt.prefix` 註冊代理程式：

```json
POST _plugins/_ml/agents/_register
{
  "name": "Chat Agent with Custom Prompt",
  "type": "conversational",
  "description": "this is a test agent",
  "app_type": "os_chat",
  "llm": {
    "model_id": "P0L8xI0Bn3OCesyvPsif",
    "parameters": {
      "max_iteration": 3,
      "response_filter": "$.completion",
      "prompt.prefix": "Assistant is a professional data analyst. You will always answer question based on the tool response first. If you don't know the answer, just say don't know.\n"
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "tools": [
    {
      "type": "VectorDBTool",
      "name": "population_data_knowledge_base",
      "description": "This tool provide population data of US cities.",
      "parameters": {
        "input": "${parameters.question}",
        "index": "test_population_data",
        "source_field": [
          "population_description"
        ],
        "model_id": "xkJLyI0Bn3OCesyvf94S",
        "embedding_field": "population_description_embedding",
        "doc_size": 3
      }
    },
    {
      "type": "VectorDBTool",
      "name": "stock_price_data_knowledge_base",
      "description": "This tool provide stock price data.",
      "parameters": {
        "input": "${parameters.question}",
        "index": "test_stock_price_data",
        "source_field": [
          "stock_price_history"
        ],
        "model_id": "xkJLyI0Bn3OCesyvf94S",
        "embedding_field": "stock_price_history_embedding",
        "doc_size": 3
      }
    }
  ]
}
```
{% include copy-curl.html %}

測試代理程式：

```json
POST _plugins/_ml/agents/o0LDyI0Bn3OCesyvr-Zq/_execute
{
  "parameters": {
    "question": "What's the stock price increase of Amazon from May 2023 to Feb 2023?",
    "verbose": true
  }
}
```
{% include copy-curl.html %}

#### 範例 2：使用自訂提示的 OpenAI 模型

為 OpenAI `gpt-4o-mini` 模型建立連接器：

```json
POST _plugins/_ml/connectors/_create
{
  "name": "My openai connector: gpt-4o-mini",
  "description": "The connector to openai chat model",
  "version": 1,
  "protocol": "http",
  "parameters": {
    "model": "gpt-4o-mini",
    "response_filter": "$.choices[0].message.content",
    "stop": ["\n\nHuman:","\nObservation:","\n\tObservation:","\n\tObservation","\n\nQuestion"],
    "system_instruction": "You are an Assistant which can answer kinds of questions."
  },
  "credential": {
    "openAI_key": "your_openAI_key"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://api.openai.com/v1/chat/completions",
      "headers": {
        "Authorization": "Bearer ${credential.openAI_key}"
      },
      "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": [{\"role\":\"system\",\"content\":\"${parameters.system_instruction}\"},{\"role\":\"user\",\"content\":\"${parameters.prompt}\"}] }"
    }
  ]
}
```
{% include copy-curl.html %}

使用回應中的連接器 ID 建立模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "My OpenAI model",
    "function_name": "remote",
    "description": "test model",
    "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

記下模型 ID，並呼叫 Predict API 測試模型：

```json
POST /_plugins/_ml/models/your_openai_model_id/_predict
{
  "parameters": {
    "system_instruction": "You are an Assistant which can answer kinds of questions.",
    "prompt": "hello"
  }
}
```
{% include copy-curl.html %}

使用自訂 `system_instruction` 和 `prompt` 建立代理程式。`prompt` 會自訂 `tool_descriptions`、`chat_history`、`format_instruction`、`question` 和 `scratchpad` 預留位置：

```json
POST _plugins/_ml/agents/_register
{
  "name": "My Chat Agent with OpenAI gpt-4o-mini",
  "type": "conversational",
  "description": "this is a test agent",
  "app_type": "os_chat",
  "llm": {
    "model_id": "your_openai_model_id",
    "parameters": {
      "max_iteration": 3,
      "response_filter": "$.choices[0].message.content",
      "system_instruction": "You are an assistant which is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics.",
      "prompt": "Assistant can ask Human to use tools to look up information that may be helpful in answering the users original question.\n${parameters.tool_descriptions}\n\n${parameters.chat_history}\n\n${parameters.prompt.format_instruction}\n\nHuman: ${parameters.question}\n\n${parameters.scratchpad}\n\nHuman: follow RESPONSE FORMAT INSTRUCTIONS\n\nAssistant:",
      "disable_trace": true
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "tools": [
    {
      "type": "VectorDBTool",
      "name": "population_data_knowledge_base",
      "description": "This tool provide population data of US cities.",
      "parameters": {
        "input": "${parameters.question}",
        "index": "test_population_data",
        "source_field": [
          "population_description"
        ],
        "model_id": "your_embedding_model_id_from_step1",
        "embedding_field": "population_description_embedding",
        "doc_size": 3
      }
    },
    {
      "type": "VectorDBTool",
      "name": "stock_price_data_knowledge_base",
      "description": "This tool provide stock price data.",
      "parameters": {
        "input": "${parameters.question}",
        "index": "test_stock_price_data",
        "source_field": [
          "stock_price_history"
        ],
        "model_id": "your_embedding_model_id_from_step1",
        "embedding_field": "stock_price_history_embedding",
        "doc_size": 3
      }
    }
  ]
}
```
{% include copy-curl.html %}

記下回應中的代理程式 ID，並執行代理程式來測試模型：

```json
POST _plugins/_ml/agents/your_agent_id/_execute
{
  "parameters": {
    "question": "What's the stock price increase of Amazon from May 2023 to Feb 2023?",
    "verbose": true
  }
}
```
{% include copy-curl.html %}

提出一個需要代理程式同時使用兩個已設定工具的問題來測試代理程式：

```json
POST _plugins/_ml/agents/your_agent_id/_execute
{
  "parameters": {
    "question": "What's the population increase of Seattle from 2021 to 2023? Then check what's the stock price increase of Amazon from May 2023 to Feb 2023?",
    "verbose": true
  }
}
```
{% include copy-curl.html %}

回應顯示代理程式同時執行 `population_data_knowledge_base` 和 `stock_price_data_knowledge_base` 工具來取得答案：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "memory_id",
          "result": "_0IByY0Bn3OCesyvJenb"
        },
        {
          "name": "parent_interaction_id",
          "result": "AEIByY0Bn3OCesyvJerm"
        },
        {
          "name": "response",
          "result": """{
    "thought": "I need to use a tool to find the population increase of Seattle from 2021 to 2023",
    "action": "population_data_knowledge_base",
    "action_input": "{\"city\": \"Seattle\", \"start_year\": 2021, \"end_year\": 2023}"
}"""
        },
        {
          "name": "response",
          "result": """{"_index":"test_population_data","_source":{"population_description":"Chart and table of population level and growth rate for the Seattle metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Seattle in 2023 is 3,519,000, a 0.86% increase from 2022.\\nThe metro area population of Seattle in 2022 was 3,489,000, a 0.81% increase from 2021.\\nThe metro area population of Seattle in 2021 was 3,461,000, a 0.82% increase from 2020.\\nThe metro area population of Seattle in 2020 was 3,433,000, a 0.79% increase from 2019."},"_id":"9EJsyI0Bn3OCesyvU-B7","_score":0.6542084}
{"_index":"test_population_data","_source":{"population_description":"Chart and table of population level and growth rate for the New York City metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of New York City in 2023 is 18,937,000, a 0.37% increase from 2022.\\nThe metro area population of New York City in 2022 was 18,867,000, a 0.23% increase from 2021.\\nThe metro area population of New York City in 2021 was 18,823,000, a 0.1% increase from 2020.\\nThe metro area population of New York City in 2020 was 18,804,000, a 0.01% decline from 2019."},"_id":"8EJsyI0Bn3OCesyvU-B7","_score":0.5966786}
{"_index":"test_population_data","_source":{"population_description":"Chart and table of population level and growth rate for the Austin metro area from 1950 to 2023. United Nations population projections are also included through the year 2035.\\nThe current metro area population of Austin in 2023 is 2,228,000, a 2.39% increase from 2022.\\nThe metro area population of Austin in 2022 was 2,176,000, a 2.79% increase from 2021.\\nThe metro area population of Austin in 2021 was 2,117,000, a 3.12% increase from 2020.\\nThe metro area population of Austin in 2020 was 2,053,000, a 3.43% increase from 2019."},"_id":"80JsyI0Bn3OCesyvU-B7","_score":0.5883104}
"""
        },
        {
          "name": "response",
          "result": """{
    "thought": "I need to use a tool to find the stock price increase of Amazon from May 2023 to Feb 2023",
    "action": "stock_price_data_knowledge_base",
    "action_input": "{\"company\": \"Amazon\", \"start_date\": \"May 2023\", \"end_date\": \"Feb 2023\"}"
}"""
        },
        {
          "name": "response",
          "result": """{"_index":"test_stock_price_data","_source":{"stock_price_history":"This is the historical montly stock price record for Amazon.com, Inc. (AMZN) with CSV format.\nDate,Open,High,Low,Close,Adj Close,Volume\n2023-03-01,93.870003,103.489998,88.120003,103.290001,103.290001,1349240300\n2023-04-01,102.300003,110.860001,97.709999,105.449997,105.449997,1224083600\n2023-05-01,104.949997,122.919998,101.150002,120.580002,120.580002,1432891600\n2023-06-01,120.690002,131.490005,119.930000,130.360001,130.360001,1242648800\n2023-07-01,130.820007,136.649994,125.919998,133.679993,133.679993,1058754800\n2023-08-01,133.550003,143.630005,126.410004,138.009995,138.009995,1210426200\n2023-09-01,139.460007,145.860001,123.040001,127.120003,127.120003,1120271900\n2023-10-01,127.279999,134.479996,118.349998,133.089996,133.089996,1224564700\n2023-11-01,133.960007,149.259995,133.710007,146.089996,146.089996,1025986900\n2023-12-01,146.000000,155.630005,142.809998,151.940002,151.940002,931128600\n2024-01-01,151.539993,161.729996,144.050003,155.199997,155.199997,953344900\n2024-02-01,155.869995,175.000000,155.619995,174.449997,174.449997,437720800\n"},"_id":"BUJsyI0Bn3OCesyvveHo","_score":0.63949186}
{"_index":"test_stock_price_data","_source":{"stock_price_history":"This is the historical montly stock price record for Alphabet Inc. (GOOG) with CSV format.\n\nDate,Open,High,Low,Close,Adj Close,Volume\n2023-03-01,90.160004,107.510002,89.769997,104.000000,104.000000,725477100\n2023-04-01,102.669998,109.629997,102.379997,108.220001,108.220001,461670700\n2023-05-01,107.720001,127.050003,104.500000,123.370003,123.370003,620317400\n2023-06-01,123.500000,129.550003,116.910004,120.970001,120.970001,521386300\n2023-07-01,120.320000,134.070007,115.830002,133.110001,133.110001,525456900\n2023-08-01,130.854996,138.399994,127.000000,137.350006,137.350006,463482000\n2023-09-01,138.429993,139.929993,128.190002,131.850006,131.850006,389593900\n2023-10-01,132.154999,142.380005,121.459999,125.300003,125.300003,514877100\n2023-11-01,125.339996,141.100006,124.925003,133.919998,133.919998,405635900\n2023-12-01,133.320007,143.945007,129.399994,140.929993,140.929993,482059400\n2024-01-01,139.600006,155.199997,136.850006,141.800003,141.800003,428771200\n2024-02-01,143.690002,150.695007,138.169998,147.139999,147.139999,231934100\n"},"_id":"CkJsyI0Bn3OCesyvveHo","_score":0.6056718}
{"_index":"test_stock_price_data","_source":{"stock_price_history":"This is the historical montly stock price record for Apple Inc. (AAPL) with CSV format.\nDate,Open,High,Low,Close,Adj Close,Volume\n2023-03-01,146.830002,165.000000,143.899994,164.899994,164.024475,1520266600\n2023-04-01,164.270004,169.850006,159.779999,169.679993,168.779099,969709700\n2023-05-01,169.279999,179.350006,164.309998,177.250000,176.308914,1275155500\n2023-06-01,177.699997,194.479996,176.929993,193.970001,193.207016,1297101100\n2023-07-01,193.779999,198.229996,186.600006,196.449997,195.677261,996066400\n2023-08-01,196.240005,196.729996,171.960007,187.869995,187.130997,1322439400\n2023-09-01,189.490005,189.979996,167.619995,171.210007,170.766846,1337586600\n2023-10-01,171.220001,182.339996,165.669998,170.770004,170.327972,1172719600\n2023-11-01,171.000000,192.929993,170.119995,189.949997,189.458313,1099586100\n2023-12-01,190.330002,199.619995,187.449997,192.529999,192.284637,1062774800\n2024-01-01,187.149994,196.380005,180.169998,184.399994,184.164993,1187219300\n2024-02-01,183.990005,191.050003,179.250000,188.850006,188.609329,420063900\n"},"_id":"BkJsyI0Bn3OCesyvveHo","_score":0.5960163}
"""
        },
        {
          "name": "response",
          "result": "The population increase of Seattle from 2021 to 2023 is 0.86%. The stock price increase of Amazon from May 2023 to Feb 2023 is from $120.58 to $174.45, which is a percentage increase."
        }
      ]
    }
  ]
}
```

## 步驟 5：在 OpenSearch Dashboards 中設定根聊天機器人代理程式

若要使用 [OpenSearch Assistant for OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/dashboards-assistant/index/)，您需要設定一個根聊天機器人代理程式。

根聊天機器人代理程式由以下幾個部分組成：

- 一個 `conversational` 代理程式：在 `AgentTool` 中，您可以使用先前步驟中建立的任何 `conversational` 代理程式。
- 一個 `MLModelTool`：此工具用於根據您目前的問題與模型回應建議新問題。

設定根代理程式：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Chatbot agent",
  "type": "flow",
  "description": "this is a test chatbot agent",
  "tools": [
    {
      "type": "AgentTool",
      "name": "LLMResponseGenerator",
      "parameters": {
        "agent_id": "your_conversational_agent_created_in_prevous_steps" 
      },
      "include_output_in_agent_response": true
    },
    {
      "type": "MLModelTool",
      "name": "QuestionSuggestor",
      "description": "A general tool to answer any question",
      "parameters": {
        "model_id": "your_llm_model_id_created_in_previous_steps",  
        "prompt": "Human:  You are an AI that only speaks JSON. Do not write normal text. Output should follow example JSON format: \n\n {\"response\": [\"question1\", \"question2\"]}\n\n. \n\nHuman:You will be given a chat history between OpenSearch Assistant and a Human.\nUse the context provided to generate follow up questions the Human would ask to the Assistant.\nThe Assistant can answer general questions about logs, traces and metrics.\nAssistant can access a set of tools listed below to answer questions given by the Human:\nQuestion suggestions generator tool\nHere's the chat history between the human and the Assistant.\n${parameters.LLMResponseGenerator.output}\nUse the following steps to generate follow up questions Human may ask after the response of the Assistant:\nStep 1. Use the chat history to understand what human is trying to search and explore.\nStep 2. Understand what capabilities the assistant has with the set of tools it has access to.\nStep 3. Use the above context and generate follow up questions.Step4:You are an AI that only speaks JSON. Do not write normal text. Output should follow example JSON format: \n\n {\"response\": [\"question1\", \"question2\"]} \n \n----------------\n\nAssistant:"
      },
      "include_output_in_agent_response": true
    }
  ],
  "memory": {
    "type": "conversation_index"
  }
}
```
{% include copy-curl.html %}

記下根聊天機器人代理程式 ID，登入您的 OpenSearch 伺服器，前往 OpenSearch 組態資料夾 (`$OS_HOME/config`)，然後執行以下命令：

```bashx
 curl -k --cert ./kirk.pem --key ./kirk-key.pem -X PUT https://localhost:9200/.plugins-ml-config/_doc/os_chat -H 'Content-Type: application/json' -d'
 {
   "type":"os_chat_root_agent",
   "configuration":{
     "agent_id": "your_root_chatbot_agent_id"
   }
 }'
```
{% include copy.html %}

前往您的 OpenSearch Dashboards 組態資料夾 (`$OSD_HOME/config`)，並編輯 `opensearch_dashboards.yml`，在檔案結尾加入以下這一行：`assistant.chat.enabled: true`。

重新啟動 OpenSearch Dashboards，然後選取右上角的聊天圖示，如下圖所示。

![OpenSearch Assistant 圖示]({{site.url}}{{site.baseurl}}/images/dashboards/os-assistant-icon.png){: width="300" }

現在您可以在 OpenSearch Dashboards 中進行聊天，如下圖所示。

![OpenSearch Assistant 聊天畫面]({{site.url}}{{site.baseurl}}/images/dashboards/os-assistant-chat.png)