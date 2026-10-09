---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Scratchpad 工具"
has_children: false
has_toc: false
nav_order: 60
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# Scratchpad 工具
**於 3.3 版推出**
{: .label .label-purple }
<!-- vale on -->

Scratchpad 工具包含 `WriteToScratchPadTool` 與 `ReadFromScratchPadTool`，可讓代理程式在執行階段儲存及擷取中間的想法與結果。這些工具可做為單一代理程式執行工作階段的暫時記憶體，讓代理程式在工具執行期間記筆記並儲存重要發現。

Scratchpad 可做為執行階段記憶體，僅在單一代理程式執行期間持續存在。當您呼叫代理程式的 `_execute` API 時，會為該工作階段建立新的 scratchpad。除了 `persistent_notes` 之外，所有筆記與資料都會在執行完成時清除，確保每次執行都從全新的 scratchpad 開始。
{: .important}

## 使用案例

- **工作分解**：在單一執行內的多步驟作業期間，儲存研究計畫、中間發現與進度筆記。
- **暫時狀態管理**：在目前的代理程式執行工作階段期間，維護脈絡與累積的知識。
- **多步驟工作流程**：在搜尋後儲存重要發現，以在複雜工作中建立完整的回應。
- **執行規劃**：在複雜作業期間儲存並參考逐步計畫。

## Scratchpad 生命週期

Scratchpad 遵循簡單的生命週期：

1. **建立**：代理程式執行開始時，會建立全新且空的 scratchpad。
2. **使用**：在執行期間，代理程式可以多次讀取及寫入 scratchpad。
3. **清理**：執行完成時，scratchpad 會自動清除。

每次呼叫代理程式的 `_execute` API 都會建立全新的 scratchpad，確保各次執行彼此隔離。

## 最佳實務

- **結構化筆記**：鼓勵代理程式在 scratchpad 中維護有條理、結構化的筆記。
- **定期更新**：讓代理程式在每個重要步驟或發現之後更新 scratchpad。
- **工作階段感知**：請記住，scratchpad 內容是暫時的，且專屬於目前的執行。
- **有效率地使用**：將 scratchpad 用於執行期間需要多次參考的中間結果。

## 範例：使用 scratchpad 工具建置研究代理程式

使用下列步驟，以 scratchpad 工具建置研究代理程式。

### 步驟 1：註冊並部署模型

註冊支援代理程式架構的對話模型。下列範例使用 Anthropic Claude：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "Claude Sonnet for Research Agent",
  "function_name": "remote",
  "description": "Claude model for research agent with scratchpad",
  "connector": {
    "name": "Bedrock Claude Sonnet Connector",
    "description": "Amazon Bedrock connector for Claude Sonnet",
    "version": 1,
    "protocol": "aws_sigv4",
    "parameters": {
      "region": "us-east-1",
      "service_name": "bedrock",
      "model": "anthropic.claude-3-5-sonnet-20241022-v2:0"
    },
    "credential": {
      "access_key": "${AWS_ACCESS_KEY_ID}",
      "secret_key": "${AWS_SECRET_ACCESS_KEY}",
      "session_token": "${AWS_SESSION_TOKEN}"
    },
    "actions": [
      {
        "action_type": "predict",
        "method": "POST",
        "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/converse",
        "headers": {
          "content-type": "application/json"
        },
        "request_body": """{"system": [{"text": "${parameters.system_prompt}"}], "messages": ${parameters.messages}, "inferenceConfig": {"maxTokens": 8000, "temperature": 0}}"""
      }
    ]
  }
}
```
{% include copy-curl.html %}

### 步驟 2：註冊含 scratchpad 工具的代理程式

註冊同時包含 scratchpad 工具與其他研究工具的對話代理程式：

```json
POST /_plugins/_ml/agents/_register
{
    "name": "Research Agent with Scratchpad",
    "type": "conversational",
    "description": "Research assistant with persistent scratchpad memory",
    "app_type": "rag",
    "llm": {
        "model_id": "your-model-id",
        "parameters": {
            "max_iteration": 50,
            "system_prompt": "You are a sophisticated research assistant with access to OpenSearch indices and a persistent scratchpad for note-taking.\n\nYour Research Workflow:\n1. Check Scratchpad: Before starting a new research task, check your scratchpad to see if you have any relevant information already saved\n2. Create Research Plan: Create a structured research plan\n3. Write to Scratchpad: Save the research plan and any important information to your scratchpad\n4. Use Search: Gather information using OpenSearch search queries\n5. Update Scratchpad: After each search, update your scratchpad with new findings\n6. Iterate: Repeat searching and updating until you have comprehensive information\n7. Complete Task: Provide a thorough response based on your accumulated research\n\nRemember: Your scratchpad is temporary memory for this execution session only. Use it to organize your thoughts and findings during this task.",
            "prompt": "${parameters.question}"
        }
    },
    "memory": {
        "type": "conversation_index"
    },
    "parameters": {
        "_llm_interface": "bedrock/converse/claude"
    },
    "tools": [
        {
            "type": "SearchIndexTool"
        },
        {
            "type": "ListIndexTool"
        },
        {
            "type": "IndexMappingTool"
        },
        {
            "type": "ReadFromScratchPadTool",
            "name": "ReadFromScratchPadTool",
            "parameters": {
                "persistent_notes": "You are a helpful researcher. Before making searches, use the ListIndexTool to discover available indices. Write down important notes after using tools."
            }
        },
        {
            "type": "WriteToScratchPadTool",
            "name": "WriteToScratchPadTool"
        }
    ]
}
```
{% include copy-curl.html %}

### 步驟 3：執行代理程式

以研究問題執行代理程式：

```json
POST /_plugins/_ml/agents/{your-agent-id}/_execute?async=true
{
    "parameters": {
        "question": "How many residents are in New York?"
    }
}
```
{% include copy-curl.html %}


代理程式將會：
1. 從其 scratchpad 讀取，以檢查是否有現有的相關資訊（新執行會從空白開始）。
2. 建立研究計畫並儲存至 scratchpad。
3. 執行搜尋，並以發現更新 scratchpad。
4. 根據累積的研究提供完整的答案。

使用 `agents/<your-agent-id>/_execute` API 時，您會在回應中取得 `parent_interaction_id` 與 `memory_id`。請記下 `parent_interaction_id`，以供後續追蹤步驟使用。如需更多資訊，請參閱[檢視 scratchpad 活動](#viewing-scratchpad-activity)。

## 工具參數

以下是 scratchpad 工具的參數。

### ReadFromScratchPadTool

以下是新增至代理程式時所使用的**註冊參數**。

參數 | 資料類型 | 必要／選用 | 說明
:--- | :--- | :--- | :---
`persistent_notes` | 字串 | 選用 | 首次建立時要儲存至 scratchpad 的初始筆記或指示。

以下是直接呼叫工具時所使用的**執行參數**。

參數 | 資料類型 | 必要／選用 | 說明
:--- | :--- |:------------------| :---
`persistent_notes` | 字串 | 必要          | 要儲存至 scratchpad 的初始筆記或指示。

### WriteToScratchPadTool

下列**註冊參數**用於將工具加入代理程式時。

參數 | 資料類型 | 必要／選用 | 說明
:--- | :--- | :--- | :---
`return_history` | 布林值 | 選用 | 設定為 `true` 時，寫入後回傳完整的 scratchpad 內容。設為 `false` 或省略（預設）時，回傳新增的筆記及確認訊息。

下列**執行參數**用於直接呼叫工具時。

參數 | 資料類型 | 必要／選用 | 說明
:--- | :--- | :--- | :---
`notes` | 字串 | 必要 | 要寫入 scratchpad 的內容。
`return_history` | 布林值 | 選用 | 設定為 `true` 時，寫入後回傳完整的 scratchpad 內容。設為 `false` 或省略（預設）時，回傳新增的筆記及確認訊息。


## 測試工具

您可以直接使用 Tools API 執行這兩個 scratchpad 工具，並在向代理程式註冊之前測試其回應。

### 測試 ReadFromScratchPadTool

```json
POST /_plugins/_ml/tools/_execute/ReadFromScratchPadTool
{
  "parameters": {
    "persistent_notes": "You are a helpful researcher to conduct searches in OpenSearch cluster. Before making the search, please remember to use the listIndexTool to figure out what are the available indices first. When using listIndexTool, remember the index name has to be in an array format. Please write down important notes after tool used."
  }
}
```
{% include copy-curl.html %}

提供 `persistent_notes` 時，工具會嘗試在回應中顯示持續保存的筆記：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """Notes from scratchpad:
- You are a helpful researcher to conduct searches in OpenSearch cluster. Before making the search, please remember to use the listIndexTool to figure out what are the available indices first. When using listIndexTool, remember the index name has to be in an array format. Please write down important notes after tool used."""
        }
      ]
    }
  ]
}
```

您也可以使用空的 `persistent_notes` 欄位進行測試：

```json 
POST /_plugins/_ml/tools/_execute/ReadFromScratchPadTool
{
  "parameters": {
    "persistent_notes": ""
  }
}
```
{% include copy-curl.html %}

回應表示 scratchpad 為空：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "Scratchpad is empty."
        }
      ]
    }
  ]
}
```

### 測試 WriteToScratchPadTool

您可以直接使用 Tools API 執行 `WriteToScratchPadTool`，並在向代理程式註冊之前測試工具回應。

```json
POST /_plugins/_ml/tools/_execute/WriteToScratchPadTool
{
  "parameters": {
    "notes": "Research Plan for OpenSearch History and ML Evolution:\\n\\n1. OpenSearch version history, major releases after v2.0\\n2. For each major release:\\n    a. Key architectural upgrades\\n    b. New machine learning capabilities, especially ML Commons Agent framework \\n    c. Descriptions of major Agent tools added\\n    d. GitHub issue IDs tied to Agent framework features\\n3. Look for official OpenSearch documentation, release notes, blogs\\n4. Search code repositories for more technical details on ML changes\\n"
  }
}
```
{% include copy-curl.html %}

以下是工具輸出的範例回應：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "Wrote to scratchpad: Research Plan for OpenSearch History and ML Evolution:\\n\\n1. OpenSearch version history, major releases after v2.0\\n2. For each major release:\\n    a. Key architectural upgrades\\n    b. New machine learning capabilities, especially ML Commons Agent framework \\n    c. Descriptions of major Agent tools added\\n    d. GitHub issue IDs tied to Agent framework features\\n3. Look for official OpenSearch documentation, release notes, blogs\\n4. Search code repositories for more technical details on ML changes\\n"
        }
      ]
    }
  ]
}
```

您可以將 `return_history` 參數設定為 `true`，以在寫入後取得完整的 scratchpad 內容：

```json
POST /_plugins/_ml/tools/_execute/WriteToScratchPadTool
{
  "parameters": {
    "notes": "Research Plan for OpenSearch History and ML Evolution:\\n\\n1. OpenSearch version history, major releases after v2.0\\n2. For each major release:\\n    a. Key architectural upgrades\\n    b. New machine learning capabilities, especially ML Commons Agent framework \\n    c. Descriptions of major Agent tools added\\n    d. GitHub issue IDs tied to Agent framework features\\n3. Look for official OpenSearch documentation, release notes, blogs\\n4. Search code repositories for more technical details on ML changes\\n",
    "return_history": true
  }
}
```
{% include copy-curl.html %}

回應包含完整的 scratchpad 內容：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """Scratchpad updated. Full content:
- Research Plan for OpenSearch History and ML Evolution:\n\n1. OpenSearch version history, major releases after v2.0\n2. For each major release:\n    a. Key architectural upgrades\n    b. New machine learning capabilities, especially ML Commons Agent framework \n    c. Descriptions of major Agent tools added\n    d. GitHub issue IDs tied to Agent framework features\n3. Look for official OpenSearch documentation, release notes, blogs\n4. Search code repositories for more technical details on ML changes\n"""
        }
      ]
    }
  ]
}
```

## 檢視 scratchpad 活動

您可以透過檢查執行追蹤來監視代理程式如何使用 scratchpad：

```json
GET /_plugins/_ml/memory/message/{parent_interaction_id}/traces?next_token=0
```
{% include copy-curl.html %}

這些追蹤顯示 scratchpad 讀取與寫入的順序，說明代理程式在執行工作階段期間如何累積知識。

## 相關文件

- [代理程式與工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/)
- [對話式代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/)
