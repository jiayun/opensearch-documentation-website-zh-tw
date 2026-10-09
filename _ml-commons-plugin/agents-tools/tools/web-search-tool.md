---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "網頁搜尋工具"
has_children: false
has_toc: false
nav_order: 130
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# 網頁搜尋工具
**推出於 3.0 版**
{: .label .label-purple }
<!-- vale on -->

`WebSearchTool` 會根據使用者的問題擷取搜尋結果。它支援 [Google](#using-google-as-a-search-engine)、Bing 和 [DuckDuckGo](#using-duckduckgo-as-a-search-engine) 作為搜尋引擎，也可以使用[自訂 API](#using-a-custom-api-as-a-search-engine) 來執行搜尋。

## 使用 DuckDuckGo 作為搜尋引擎

若要搭配 `WebSearchTool` 使用 DuckDuckGo 作為搜尋引擎，請依照下列步驟操作。

### 步驟 1：註冊將執行 WebSearchTool 的流程代理程式

流程代理程式會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_WebSearch_tool",
  "type": "flow",
  "description": "this is a test agent for the WebSearchTool",
  "tools": [
    {
      "type": "WebSearchTool",
      "name": "DuckduckgoWebSearchTool",
      "parameters": {
        "engine": "duckduckgo",
        "input": "${parameters.question}"
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

### 步驟 2：執行代理程式

接著，傳送下列請求來執行代理程式（DuckDuckGo 不需要任何認證資訊）：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "question": "How to create a index pattern in OpenSearch?"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會傳回網路搜尋結果：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """
            {
                "next_page": "https://html.duckduckgo.com/html?q=how+to+create+index+pattern+in+OpenSearch&ia=web&dc=11",
                "items": [
                  {
                    "url": "http://someurl",
                    "title": "the page result title",
                    "content": "the page content..."
                  },
                  {
                    "url": "https://anotherurl",
                    "title": "the page result title",
                    "content": "the page content..."
                  }
                  ...
                ]
            }
          """
        }
      ]
    }
  ]
}
```

## 使用 Google 作為搜尋引擎

若要搭配 `WebSearchTool` 使用 Google 作為搜尋引擎，請依照下列步驟操作。

### 步驟 1：註冊將執行 WebSearchTool 的流程代理程式

流程代理程式會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_WebSearch_tool",
  "type": "flow",
  "description": "this is a test agent for the WebSearchTool",
  "tools": [
    {
      "type": "WebSearchTool",
      "name": "GoogleWebSearchTool",
      "parameters": {
        "engine": "google",
        "engine_id": "${your_google_engine_id}",
        "api_key": "${your_google_api_key}",
        "input": "${parameters.question}"
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

### 步驟 2：執行代理程式

執行代理程式之前，請確認您已取得以程式化方式存取 Google 搜尋所需的認證資訊。

接著，傳送下列請求來執行代理程式：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "question": "How to create a index pattern in OpenSearch?"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會傳回網路搜尋結果：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """
            {
                "next_page": "https://customsearch.googleapis.com/customsearch/v1?q=how+to+create+index+pattern+in+OpenSearch&start=10",
                "items": [
                  {
                    "url": "http://someurl",
                    "title": "the page result title",
                    "content": "the page content..."
                  },
                  {
                    "url": "https://anotherurl",
                    "title": "the page result title",
                    "content": "the page content..."
                  }
                  ...
                ]
            }
          """
        }
      ]
    }
  ]
}
```

## 使用自訂 API 作為搜尋引擎

若要搭配 `WebSearchTool` 使用自訂 API 作為搜尋引擎，請依照下列步驟操作。

### 步驟 1：註冊將執行 WebSearchTool 的流程代理程式

若要使用自訂端點進行搜尋，您需要設定下列參數：

- `Authorization`：用於驗證
- `endpoint`：用於 API 連線
- `custom_res_url_jsonpath`：用於解析 JSON 回應並擷取連結

您的 API 必須以 JSON 格式傳回回應。API 傳回的連結必須可使用 [JSONPath](https://en.wikipedia.org/wiki/JSONPath) 運算式擷取。其他參數如 `query_key`、`offset_key` 和 `limit_key` 為選用，但如果您的 API 使用的值與預設值不同，則應指定這些參數。

若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_WebSearch_tool",
  "type": "flow",
  "description": "this is a test agent for the WebSearchTool",
  "tools": [
    {
      "type": "WebSearchTool",
      "name": "CustomWebSearchTool",
      "parameters": {
        "engine": "custom",
        "endpoint": "${your_custom_endpoint}",
        "custom_res_url_jsonpath": "$.data[*].link",
        "Authorization": "Bearer xxxx",
        "query_key": "q",
        "offset_key": "offset",
        "limit_key": "limit"
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

### 步驟 2：執行代理程式

執行代理程式之前，請確認您已取得以程式化方式存取自訂搜尋 API 所需的認證資訊。

接著，傳送下列請求來執行代理程式：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "question": "How to create a index pattern in OpenSearch?"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會傳回網路搜尋結果：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """
            {
                "next_page": "{your_custom_endpoint}?q=how+to+create+index+pattern+in+OpenSearch&offset=10&limit=10",
                "items": [
                  {
                    "url": "http://someurl",
                    "title": "the page result title",
                    "content": "the page content..."
                  },
                  {
                    "url": "https://anotherurl",
                    "title": "the page result title",
                    "content": "the page content..."
                  }
                  ...
                ]
            }
          """
        }
      ]
    }
  ]
}
```



## 註冊參數

下表列出註冊代理程式時可用的所有工具參數。



| 參數 | 類型 | 必要/選用 | 說明 |
|:---|:---|:---|:---|
| `engine` | 字串 | 必要 | 要使用的搜尋引擎。有效值為 `google`、`bing`、`duckduckgo` 或 `custom`。 |
| `engine_id` | 字串 | 選用 | Google 的自訂搜尋引擎 ID。當 `engine` 設為 `google` 時為必要。 |
| `api_key` | 字串 | 選用 | 用於驗證的 API 金鑰。當 `engine` 設為 `google` 或 `bing` 時為必要。 |
| `endpoint` | 字串 | 選用 | 自訂搜尋 API 的 URL 端點。當 `engine` 設為 `custom` 時為必要。 |
| `Authorization` | 字串 | 選用 | 自訂 API 的授權標頭值。當 `engine` 設為 `custom` 時為必要。 |
| `query_key` | 字串 | 選用 | 自訂 API URL 中搜尋查詢的參數名稱（例如 `${endpoint}?my_query_key=${question}`）。預設為 `q`。 |
| `offset_key` | 字串 | 選用 | 自訂 API URL 中分頁位移的參數名稱（例如 `${endpoint}?q=${question}&start=10`）。預設為 `offset`。 |
| `limit_key` | 字串 | 選用 | 自訂 API URL 中結果數量限制的參數名稱（例如 `${endpoint}?q=${question}&start=10&limit=10`）。預設為 `limit`。 |
| `custom_res_url_jsonpath` | 字串 | 選用 | 用於從自訂 API 回應擷取 URL 的 JSONPath 運算式（例如 `$[*].link`）。當 `engine` 設為 `custom` 時為必要。 |

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

參數	| 類型 | 必要/選用 | 說明	
:--- | :--- | :--- | :---
`question` | 字串 | 必要 | 要傳送給 LLM 的自然語言問題。 

## 測試工具

您可以將此工具做為代理程式工作流程的一部分來執行，也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用來測試個別工具或執行獨立作業。