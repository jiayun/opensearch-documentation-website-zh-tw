---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作流程教學"
nav_order: 20
---

# 工作流程教學

您可以使用 Chain-of-Thought (CoT) 代理程式自動化常見使用案例的設定，例如對話式聊天。_代理程式_ 會協調並執行機器學習模型與工具。_工具_ 則執行一組特定任務。本頁面提供設定 CoT 代理程式的完整範例。如需代理程式與工具的更多資訊，請參閱 [代理程式與工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/)

此設定需要依序執行下列 API 請求，後續請求會使用已佈建的資源。下列清單概述此工作流程所需的步驟。步驟名稱與範本中的名稱相對應：

1. **在叢集上部署模型**
    * [`create_connector_1`](#create_connector_1)：建立連接至外部託管模型的連接器。
    * [`register_model_2`](#register_model_2)：使用您建立的連接器註冊模型。
    * [`deploy_model_3`](#deploy_model_3)：部署模型。
1. **使用已部署的模型進行推論**
    * 設定數個執行特定任務的工具：
      * [`list_index_tool`](#list_index_tool)：設定取得索引資訊的工具。
      * [`ml_model_tool`](#ml_model_tool)：設定機器學習 (ML) 模型工具。
    * 設定一或多個使用這些工具組合的代理程式：
      * [`sub_agent`](#sub_agent)：建立使用 `list_index_tool` 的代理程式。
    * 設定代表這些代理程式的工具：
      * [`agent_tool`](#agent_tool)：包裝 `sub_agent`，以便將其作為工具使用。
    * [`root_agent`](#root_agent)：設定根代理程式，可將任務委派給工具或其他代理程式。

下列章節將詳細說明這些步驟。完整的工作流程範本請參閱 [完整的 YAML 工作流程範本](#complete-yaml-workflow-template)。

## 工作流程圖

上一節所述的工作流程會組織成一個 [範本](#complete-yaml-workflow-template)。請注意，您可以透過多種方式排列步驟順序。在範例範本中，`ml_model_tool` 步驟緊接在 `root_agent` 步驟之前指定，但您也可以在 `deploy_model_3` 步驟之後、`root_agent` 步驟之前的任何位置指定它。下圖顯示 OpenSearch 依範本中指定的順序，為所有步驟建立的有向非循環圖 (DAG)。

![範例工作流程步驟圖]({{site.url}}{{site.baseurl}}/images/automatic-workflow-dag.png){:style="width: 100%; max-width: 600px;" class="img-centered"}

## 1. 在叢集上部署模型

若要在叢集上部署模型，您需要建立連接至該模型的連接器、註冊模型，然後部署模型。

<!-- vale off -->
### create_connector_1
<!-- vale on -->

工作流程的第一步是建立連接至外部託管模型的連接器（在下列範例中，此步驟稱為 `create_connector_1`）。`user_inputs` 欄位的內容與 ML Commons [Create Connector API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/connector-apis/create-connector/) 完全相符：

```yaml
nodes:
- id: create_connector_1
  type: create_connector
  user_inputs:
    name: OpenAI Chat Connector
    description: The connector to public OpenAI model service for gpt-4o-mini
    version: '1'
    protocol: http
    parameters:
      endpoint: api.openai.com
      model: gpt-4o-mini
    credential:
      openAI_key: '12345'
    actions:
    - action_type: predict
      method: POST
      url: https://${parameters.endpoint}/v1/chat/completions
```

建立連接器後，OpenSearch 會傳回 `connector_id`，您需要用它來註冊模型。

<!-- vale off -->
### register_model_2
<!-- vale on -->

註冊模型時，`previous_node_inputs` 欄位會告訴 OpenSearch 從 `create_connector_1` 步驟的輸出取得所需的 `connector_id`。[Register Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/) 所需的其他輸入則包含在 `user_inputs` 欄位中：

```yaml
- id: register_model_2
  type: register_remote_model
  previous_node_inputs:
    create_connector_1: connector_id
  user_inputs:
    name: openAI-gpt-4o-mini
    function_name: remote
    description: test model
```

此步驟的輸出是 `model_id`。接著您必須將已註冊的模型部署到叢集。

<!-- vale off -->
### deploy_model_3
<!-- vale on -->

[Deploy Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/deploy-model/) 需要上一個步驟的 `model_id`，如 `previous_node_inputs` 欄位中所指定：

```yaml
- id: deploy_model_3
  type: deploy_model
  # This step needs the model_id produced as an output of the previous step
  previous_node_inputs:
    register_model_2: model_id
```

直接使用 Deploy Model API 時，會傳回任務 ID，需要使用 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 來判斷部署何時完成。自動化工作流程省去了手動檢查狀態的程序，並直接傳回最終的 `model_id`。

### 排列步驟順序

若要將這些步驟依序排列，您必須在圖形中以邊連接它們。當步驟中存在 `previous_node_input` 欄位時，OpenSearch 會自動為該步驟建立一個包含 `source` 與 `dest` 欄位的節點。`source` 的輸出是 `dest` 所需的輸入。例如，`register_model_2` 步驟需要 `create_connector_1` 步驟的 `connector_id`。同樣地，`deploy_model_3` 步驟需要 `register_model_2` 步驟的 `model_id`。因此，OpenSearch 會如下建立圖形中的前兩條邊，以將輸出與所需輸入相符，並在缺少所需輸入時引發錯誤：

```yaml
edges:
- source: create_connector_1
  dest: register_model_2
- source: register_model_2
  dest: deploy_model_3
```

如果您定義了 `previous_node_inputs`，則邊的定義是選用的。
{: .note}

## 2. 使用已部署的模型進行推論

CoT 代理程式可以在工具中使用已部署的模型。此步驟並不嚴格對應某個 API，而是代表 [Register Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/) 所需請求本文中的一個元件。這可簡化註冊請求，並允許在多個代理程式中重複使用同一工具。如需代理程式與工具的更多資訊，請參閱 [代理程式與工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/)。

<!-- vale off -->
### list_index_tool
<!-- vale on -->

您可以設定其他工具供 CoT 代理程式使用。例如，您可以如下設定 `list_index_tool`。此工具不依賴任何先前的步驟：

```yaml
- id: list_index_tool
  type: create_tool
  user_inputs:
    name: ListIndexTool
    type: ListIndexTool
    parameters:
      max_iteration: 5
```

<!-- vale off -->
### sub_agent
<!-- vale on -->

若要在代理程式組態中使用 `list_index_tool`，請將其指定為代理程式 `previous_node_inputs` 欄位中的其中一個工具。您可以視需要將其他工具加入 `previous_node_inputs`。代理程式也需要一個大型語言模型 (LLM) 才能搭配工具進行推論。LLM 由 `llm.model_id` 欄位定義。此範例假設將使用 `deploy_model_3` 步驟的 `model_id`。不過，如果已有其他模型部署完成，則可以改將先前部署模型的 `model_id` 包含在 `user_inputs` 欄位中：

```yaml
- id: sub_agent
  type: register_agent
  previous_node_inputs:
    # When llm.model_id is not present this can be used as a fallback value
    deploy-model-3: model_id
    list_index_tool: tools
  user_inputs:
    name: Sub Agent
    type: conversational
    description: this is a test agent
    parameters:
      hello: world
    llm.parameters:
      max_iteration: '5'
      stop_when_no_tool_found: 'true'
    memory:
      type: conversation_index
    app_type: chatbot
```

OpenSearch 會自動建立下列邊，讓代理程式能夠從上一個節點擷取欄位：

```yaml
- source: list_index_tool
  dest: sub_agent
- source: deploy_model_3
  dest: sub_agent
```

<!-- vale off -->
### agent_tool
<!-- vale on -->

您可以將代理程式用作另一個代理程式的工具。註冊代理程式會在輸出中產生 `agent_id`。下列步驟定義一個使用上一步驟 `agent_id` 的工具：

```yaml
- id: agent_tool
  type: create_tool
  previous_node_inputs:
    sub_agent: agent_id
  user_inputs:
    name: AgentTool
    type: AgentTool
    description: Agent Tool
    parameters:
      max_iteration: 5
```

由於此步驟指定了 `previous_node_input`，OpenSearch 會自動建立邊緣連線：

```yaml
- source: sub_agent
  dest: agent_tool
```

<!-- vale off -->
### ml_model_tool
<!-- vale on -->

工具可以參照 ML 模型。此範例從先前步驟中部署的模型取得所需的 `model_id`：

```yaml
- id: ml_model_tool
  type: create_tool
  previous_node_inputs:
    deploy-model-3: model_id
  user_inputs:
    name: MLModelTool
    type: MLModelTool
    alias: language_model_tool
    description: A general tool to answer any question.
    parameters:
      prompt: Answer the question as best you can.
      response_filter: choices[0].message.content
```

OpenSearch 會自動建立邊緣以使用 `previous_node_input`：

```yaml
- source: deploy-model-3
  dest: ml_model_tool
```

<!-- vale off -->
### root_agent
<!-- vale on -->

對話式聊天應用程式將與單一根代理程式通訊，該代理程式在其 `tools` 欄位中包含 ML 模型工具與代理程式工具。它也會從已部署的模型取得 `llm.model_id`。某些代理程式要求工具必須以特定順序排列，這可以透過在使用者輸入中包含 `tools_order` 欄位來強制執行：

```yaml
- id: root_agent
  type: register_agent
  previous_node_inputs:
    deploy-model-3: model_id
    ml_model_tool: tools
    agent_tool: tools
  user_inputs:
    name: DEMO-Test_Agent_For_CoT
    type: conversational
    description: this is a test agent
    parameters:
      prompt: Answer the question as best you can.
    llm.parameters:
      max_iteration: '5'
      stop_when_no_tool_found: 'true'
    tools_order: ['agent_tool', 'ml_model_tool']
    memory:
      type: conversation_index
    app_type: chatbot
```

OpenSearch 會自動為 `previous_node_input` 來源建立邊緣：

```yaml
- source: deploy-model-3
  dest: root_agent
- source: ml_model_tool
  dest: root_agent
- source: agent_tool
  dest: root_agent
```

如需 OpenSearch 為此工作流程建立的完整 DAG，請參閱[工作流程圖](#workflow-graph)。

## 完整的 YAML 工作流程範本

以下是以 YAML 格式呈現、包含所有 `provision` 工作流程步驟的最終範本：

<details open markdown="block">
  <summary>
    YAML 範本
  </summary>
  {: .text-delta}

```yaml
# This template demonstrates provisioning the resources for a 
# Chain-of-Thought chat bot
name: tool-register-agent
description: test case
use_case: REGISTER_AGENT
version:
  template: 1.0.0
  compatibility:
  - 2.12.0
  - 3.0.0
workflows:
  # This workflow defines the actions to be taken when the Provision Workflow API is used
  provision:
    nodes:
    # The first three nodes create a connector to a remote model, registers and deploy that model
    - id: create_connector_1
      type: create_connector
      user_inputs:
        name: OpenAI Chat Connector
        description: The connector to public OpenAI model service for gpt-4o-mini
        version: '1'
        protocol: http
        parameters:
          endpoint: api.openai.com
          model: gpt-4o-mini
        credential:
          openAI_key: '12345'
        actions:
        - action_type: predict
          method: POST
          url: https://${parameters.endpoint}/v1/chat/completions
    - id: register_model_2
      type: register_remote_model
      previous_node_inputs:
        create_connector_1: connector_id
      user_inputs:
        # deploy: true could be added here instead of the deploy step below
        name: openAI-gpt-4o-mini
        description: test model
    - id: deploy_model_3
      type: deploy_model
      previous_node_inputs:
        register_model_2: model_id
    # For example purposes, the model_id obtained as the output of the deploy_model_3 step will be used
    # for several below steps.  However, any other deployed model_id can be used for those steps.
    # This is one example tool from the Agent Framework.
    - id: list_index_tool
      type: create_tool
      user_inputs:
        name: ListIndexTool
        type: ListIndexTool
        parameters:
          max_iteration: 5
    # This simple agent only has one tool, but could be configured with many tools
    - id: sub_agent
      type: register_agent
      previous_node_inputs:
        deploy-model-3: model_id
        list_index_tool: tools
      user_inputs:
        name: Sub Agent
        type: conversational
        parameters:
          hello: world
        llm.parameters:
          max_iteration: '5'
          stop_when_no_tool_found: 'true'
        memory:
          type: conversation_index
        app_type: chatbot
    # An agent can be used itself as a tool in a nested relationship
    - id: agent_tool
      type: create_tool
      previous_node_inputs:
        sub_agent: agent_id
      user_inputs:
        name: AgentTool
        type: AgentTool
        parameters:
          max_iteration: 5
    # An ML Model can be used as a tool
    - id: ml_model_tool
      type: create_tool
      previous_node_inputs:
        deploy-model-3: model_id
      user_inputs:
        name: MLModelTool
        type: MLModelTool
        alias: language_model_tool
        parameters:
          prompt: Answer the question as best you can.
          response_filter: choices[0].message.content
    # This final agent will be the interface for the CoT chat user
    # Using a flow agent type tools_order matters
    - id: root_agent
      type: register_agent
      previous_node_inputs:
        deploy-model-3: model_id
        ml_model_tool: tools
        agent_tool: tools
      user_inputs:
        name: DEMO-Test_Agent
        type: flow
        parameters:
          prompt: Answer the question as best you can.
        llm.parameters:
          max_iteration: '5'
          stop_when_no_tool_found: 'true'
        tools_order: ['agent_tool', 'ml_model_tool']
        memory:
          type: conversation_index
        app_type: chatbot
    # These edges are all automatically created with previous_node_input
    edges:
    - source: create_connector_1
      dest: register_model_2
    - source: register_model_2
      dest: deploy_model_3
    - source: list_index_tool
      dest: sub_agent
    - source: deploy_model_3
      dest: sub_agent
    - source: sub_agent
      dest: agent_tool
    - source: deploy-model-3
      dest: ml_model_tool
    - source: deploy-model-3
      dest: root_agent
    - source: ml_model_tool
      dest: root_agent
    - source: agent_tool
      dest: root_agent
```
</details>

## 完整的 JSON 工作流程範本

以下是以 JSON 格式呈現的相同範本：

<details open markdown="block">
  <summary>
    JSON 範本
  </summary>
  {: .text-delta}

```json
{
  "name": "tool-register-agent",
  "description": "test case",
  "use_case": "REGISTER_AGENT",
  "version": {
    "template": "1.0.0",
    "compatibility": [
      "2.12.0",
      "3.0.0"
    ]
  },
  "workflows": {
    "provision": {
      "nodes": [
        {
          "id": "create_connector_1",
          "type": "create_connector",
          "user_inputs": {
            "name": "OpenAI Chat Connector",
            "description": "The connector to public OpenAI model service for gpt-4o-mini",
            "version": "1",
            "protocol": "http",
            "parameters": {
              "endpoint": "api.openai.com",
              "model": "gpt-4o-mini"
            },
            "credential": {
              "openAI_key": "12345"
            },
            "actions": [
              {
                "action_type": "predict",
                "method": "POST",
                "url": "https://${parameters.endpoint}/v1/chat/completions"
              }
            ]
          }
        },
        {
          "id": "register_model_2",
          "type": "register_remote_model",
          "previous_node_inputs": {
            "create_connector_1": "connector_id"
          },
          "user_inputs": {
            "name": "openAI-gpt-4o-mini",
            "description": "test model"
          }
        },
        {
          "id": "deploy_model_3",
          "type": "deploy_model",
          "previous_node_inputs": {
            "register_model_2": "model_id"
          }
        },
        {
          "id": "list_index_tool",
          "type": "create_tool",
          "user_inputs": {
            "name": "ListIndexTool",
            "type": "ListIndexTool",
            "parameters": {
              "max_iteration": 5
            }
          }
        },
        {
          "id": "sub_agent",
          "type": "register_agent",
          "previous_node_inputs": {
            "deploy-model-3": "llm.model_id",
            "list_index_tool": "tools"
          },
          "user_inputs": {
            "name": "Sub Agent",
            "type": "conversational",
            "parameters": {
              "hello": "world"
            },
            "llm.parameters": {
              "max_iteration": "5",
              "stop_when_no_tool_found": "true"
            },
            "memory": {
              "type": "conversation_index"
            },
            "app_type": "chatbot"
          }
        },
        {
          "id": "agent_tool",
          "type": "create_tool",
          "previous_node_inputs": {
            "sub_agent": "agent_id"
          },
          "user_inputs": {
            "name": "AgentTool",
            "type": "AgentTool",
            "parameters": {
              "max_iteration": 5
            }
          }
        },
        {
          "id": "ml_model_tool",
          "type": "create_tool",
          "previous_node_inputs": {
            "deploy-model-3": "model_id"
          },
          "user_inputs": {
            "name": "MLModelTool",
            "type": "MLModelTool",
            "alias": "language_model_tool",
            "parameters": {
              "prompt": "Answer the question as best you can.",
              "response_filter": "choices[0].message.content"
            }
          }
        },
        {
          "id": "root_agent",
          "type": "register_agent",
          "previous_node_inputs": {
            "deploy-model-3": "llm.model_id",
            "ml_model_tool": "tools",
            "agent_tool": "tools"
          },
          "user_inputs": {
            "name": "DEMO-Test_Agent",
            "type": "flow",
            "parameters": {
              "prompt": "Answer the question as best you can."
            },
            "llm.parameters": {
              "max_iteration": "5",
              "stop_when_no_tool_found": "true"
            },
            "tools_order": [
              "agent_tool",
              "ml_model_tool"
            ],
            "memory": {
              "type": "conversation_index"
            },
            "app_type": "chatbot"
          }
        }
      ],
      "edges": [
        {
          "source": "create_connector_1",
          "dest": "register_model_2"
        },
        {
          "source": "register_model_2",
          "dest": "deploy_model_3"
        },
        {
          "source": "list_index_tool",
          "dest": "sub_agent"
        },
        {
          "source": "deploy_model_3",
          "dest": "sub_agent"
        },
        {
          "source": "sub_agent",
          "dest": "agent_tool"
        },
        {
          "source": "deploy-model-3",
          "dest": "ml_model_tool"
        },
        {
          "source": "deploy-model-3",
          "dest": "root_agent"
        },
        {
          "source": "ml_model_tool",
          "dest": "root_agent"
        },
        {
          "source": "agent_tool",
          "dest": "root_agent"
        }
      ]
    }
  }
}
```
</details>

## 後續步驟

若要進一步了解代理程式與工具，請參閱[代理程式與工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/)。