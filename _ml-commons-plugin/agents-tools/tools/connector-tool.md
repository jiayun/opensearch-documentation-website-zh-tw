---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "連接器工具"
has_children: false
has_toc: false
nav_order: 20
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# 連接器工具
**於 2.15 版推出**
{: .label .label-purple }
<!-- vale on -->

`ConnectorTool` 使用[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)來呼叫任何 REST API 函式。例如，您可以使用 `ConnectorTool` 透過其 REST API 介面呼叫 Lambda 函式。

## 步驟 1：以 execute 動作註冊連接器

`ConnectorTool` 只能在連接器內執行 `execute` 動作。在建立 `ConnectorTool` 之前，您需要設定連接器，並在 `actions` 陣列中提供 `execute` 動作。`execute` 動作用於呼叫 REST API 端點上的函式，類似於用於呼叫機器學習 (ML) 模型的 `predict` 動作。

在此範例中，您將為一個接受兩個整數並回傳其總和的簡單 AWS Lambda 函式建立連接器。此函式託管在具有特定 URL 的專用端點上，您將在 `url` 參數中提供該 URL。如需更多資訊，請參閱 [Lambda 函式 URL](https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html)。

若要建立連接器，請傳送下列請求：

```json
POST _plugins/_ml/connectors/_create
{
  "name": "Lambda connector of simple calculator",
  "description": "Demo connector of lambda function",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "YOUR AWS REGION",
    "service_name": "lambda"
  },
  "credential": {
    "access_key": "YOUR ACCESS KEY",
    "secret_key": "YOUR SECRET KEY",
    "session_token": "YOUR SESSION TOKEN"
  },
  "actions": [
    {
      "action_type": "execute",
      "method": "POST",
      "url": "YOUR LAMBDA FUNCTION URL",
      "headers": {
        "content-type": "application/json"
      },
      "request_body": "{ \"number1\":\"${parameters.number1}\", \"number2\":\"${parameters.number2}\" }"
    }
  ]
}
```
{% include copy-curl.html %} 

OpenSearch 會回應連接器 ID：

```json
{
  "connector_id": "Zz1XEJABXWrLmr4mewEF"
}
```

## 步驟 2：註冊將執行 ConnectorTool 的流程代理程式

在此範例中，Lambda 函式會將兩個輸入數字相加，並在 `result` 欄位中回傳其總和：

```json
{
  "result": 5
}
```

預設情況下，`ConnectorTool` 預期來自 Lambda 函式的回應包含名為 `response` 的欄位。然而，在此範例中，Lambda 函式的回應並未包含 `response` 欄位。若要改為從 `result` 欄位擷取結果，您需要提供 `response_filter`，指定指向 `result` 欄位的 [JSON 路徑](https://github.com/json-path/JsonPath)（`$.result`）。透過使用 `response_filter`，`ConnectorTool` 將以指定的 JSON 路徑擷取結果，並在 `response` 欄位中回傳。

若要設定 Lambda 函式的工作流程，請建立流程代理程式。流程代理程式會依序執行一連串工具，並回傳最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求，提供上一步驟的連接器 ID 以及 `response_filter`：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Demo agent of Lambda connector",
  "type": "flow",
  "description": "This is a demo agent",
  "app_type": "demo",
  "tools": [
    {
      "type": "ConnectorTool",
      "name": "lambda_function",
      "parameters": {
        "connector_id": "YOUR CONNECTOR ID",
        "response_filter": "$.result"
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
  "agent_id": "az1XEJABXWrLmr4miAFj"
}
```

## 步驟 3：執行代理程式

接著，傳送下列請求來執行代理程式：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "number1": 2,
    "number2": 3
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會回傳 Lambda 函式執行的輸出。在輸出中，欄位名稱為 `response`，而 `result` 欄位包含 Lambda 函式的結果：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": 5
        }
      ]
    }
  ]
}
```

## 註冊參數

下表列出註冊代理程式時可用的所有工具參數。

參數 | 類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`connector_id` | 字串 | 必要 | 連接器的連接器 ID，該連接器已設定用於呼叫 API 的 `execute` 動作。
`response_filter` | 字串 | 選用 | 指向包含 API 呼叫結果之回應欄位的 [JSON 路徑](https://github.com/json-path/JsonPath)。若未指定 `response_filter`，則 `ConnectorTool` 會預期 API 回應位於名為 `response` 的欄位中。

## 執行參數

執行代理程式時，您可以在連接器的 `execute` 動作的 `request_body` 中定義 API 呼叫所需的任何參數。在此範例中，參數為 `number1` 和 `number2`：

```json
"actions": [
    {
      "action_type": "execute",
      "method": "POST",
      "url": "YOUR LAMBDA FUNCTION URL",
      "headers": {
        "content-type": "application/json"
      },
      "request_body": "{ \"number1\":\"${parameters.number1}\", \"number2\":\"${parameters.number2}\" }"
    }
  ]
```

## 測試工具

您可以將此工具作為代理程式工作流程的一部分執行，或使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適用於測試個別工具或執行獨立操作。