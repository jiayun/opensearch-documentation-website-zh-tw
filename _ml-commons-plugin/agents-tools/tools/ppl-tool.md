---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "PPL 工具"
has_children: false
has_toc: false
nav_order: 60
parent: Tools
grand_parent: Agents and tools
---

# PPL 工具
**於 2.13 版推出**
{: .label .label-purple }

`PPLTool` 會將自然語言轉換為 Piped Processing Language (PPL) 查詢。此工具提供 `execute` 旗標，用於指定是否執行查詢。如果您將該旗標設為 `true`，`PPLTool` 會執行查詢並回傳查詢與結果。

## 必要條件

若要建立 PPL 工具，您需要一個能將自然語言轉換為 PPL 查詢的微調模型。或者，您也可以使用大型語言模型進行以提示詞為基礎的轉換。PPL 工具支援 Anthropic Claude 與 OpenAI 模型。

## 步驟 1：為模型建立連接器

下列範例請求會為託管於 Amazon SageMaker 上的模型建立連接器：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "sagemaker: t2ppl",
  "description": "Test connector for Sagemaker t2ppl model",
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

如需連線至 Anthropic Claude 模型或 OpenAI 模型的資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

## 步驟 2：註冊並部署模型

若要將模型註冊並部署至 OpenSearch，請傳送下列請求，並提供上一步驟取得的連接器 ID：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "remote-inference",
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

<!-- vale off -->
## 步驟 3：註冊將執行 PPLTool 的流程代理程式
<!-- vale on -->

流程代理程式會依序執行一連串工具，並回傳最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求，並在 `model_id` 參數中提供模型 ID。若要執行產生的查詢，請將 `execute` 設為 `true`：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_PPL",
  "type": "flow",
  "description": "this is a test agent",
  "memory": {
    "type": "demo"
  },
  "tools": [
    {
      "type": "PPLTool",
      "name": "TransferQuestionToPPLAndExecuteTool",
      "description": "Use this tool to transfer natural language to generate PPL and execute PPL to query inside. Use this tool after you know the index name, otherwise, call IndexRoutingTool first. The input parameters are: {index:IndexName, question:UserQuestion}",
      "parameters": {
        "model_id": "h5AUWo0BkIylWTeYT4SU",
        "model_type": "FINETUNE",
        "execute": true
      }
    }
  ]
}
```
{% include copy-curl.html %} 

如需參數說明，請參閱[註冊參數](#register-parameters)。

OpenSearch 會回應代理程式 ID：

```json
{
  "agent_id": "9X7xWI0Bpc3sThaJdY9i"
}
```

## 步驟 4：執行代理程式

在執行代理程式之前，請確認您已新增 OpenSearch Dashboards 的 `Sample web logs` 範例資料集。若要進一步了解，請參閱[新增範例資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

接著，傳送下列請求來執行代理程式：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "verbose": true,
    "question": "what is the error rate yesterday",
    "index": "opensearch_dashboards_sample_data_logs"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會回傳 PPL 查詢與查詢結果：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result":"{\"ppl\":\"source\=opensearch_dashboards_sample_data_logs| where timestamp \> DATE_SUB(NOW(), INTERVAL 1 DAY) AND timestamp \< NOW() | eval is_error\=IF(response\=\'200\', 0, 1.0) | stats AVG(is_error) as error_rate\",\"executionResult\":\"{\\n  \\\"schema\\\": [\\n    {\\n      \\\"name\\\": \\\"error_rate\\\",\\n      \\\"type\\\": \\\"double\\\"\\n    }\\n  ],\\n  \\\"datarows\\\": [\\n    [\\n      null\\n    ]\\n  ],\\n  \\\"total\\\": 1,\\n  \\\"size\\\": 1\\n}\"}"
        }
      ]
    }
  ]
}
```

如果您將 `execute` 設為 `false`，OpenSearch 只會回傳查詢，但不會執行它：

```json
{
  "inference_results": [
    {
      "output": [
        {
            "name": "response",
            "result": "source=opensearch_dashboards_sample_data_logs| where timestamp > DATE_SUB(NOW(), INTERVAL 1 DAY) AND timestamp < NOW() | eval is_error=IF(response='200', 0, 1.0) | stats AVG(is_error) as error_rate"
        }
      ]
    }
  ]
}
```

## 註冊參數

下表列出註冊代理程式時可使用的所有工具參數。

參數	| 類型 | 必要／選用 | 說明	
:--- | :--- | :--- | :---
`model_id` | 字串 | 必要 | 用於將文字轉換為 PPL 查詢的大型語言模型 (LLM) 模型 ID。
`model_type` | 字串 | 選用 | 模型類型。有效值為 `CLAUDE` (Anthropic Claude 模型)、`OPENAI` (OpenAI 模型) 與 `FINETUNE` (自訂微調模型)。
`prompt` | 字串 | 選用 | 提供給 LLM 的提示詞。
`execute` | 布林值 | 選用 | 指定是否執行 PPL 查詢。預設為 `true`。
`input` | 物件 | 選用 | 包含兩個參數，分別指定要搜尋的索引以及要提供給 LLM 的問題。例如 `"input": "{\"index\": \"${parameters.index}\", \"question\": ${parameters.question} }"`。
`head` | 整數 | 選用 | 當 `execute` 設為 `true` 時，限制回傳的執行結果數量。預設為 `-1` (無限制)。

## 執行參數

下表列出執行代理程式時可使用的所有工具參數。

參數	| 類型 | 必要／選用 | 說明	
:--- | :--- | :--- | :---
`index` | 字串 | 必要 | 要在其上執行 PPL 查詢的索引。
`question` | 字串 | 必要 | 要傳送給 LLM 的自然語言問題。
`verbose` | 布林值 | 選用 | 是否提供詳細輸出。預設為 `false`。

## 測試工具

您可以將此工具作為代理程式工作流程的一部分執行，也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用於測試個別工具或執行獨立作業。