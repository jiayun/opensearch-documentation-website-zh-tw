---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料摘要"
parent: OpenSearch Assistant for OpenSearch Dashboards
nav_order: 30
has_children: false
---

# 資料摘要

這是一項實驗性功能，不建議在正式環境中使用。如需取得此功能的最新進度，或想提供意見回饋，請至 [OpenSearch 論壇](https://forum.opensearch.org/)參與討論。
{: .warning}

OpenSearch Dashboards Assistant 的資料摘要功能使用大型語言模型 (LLM)，協助您為儲存在 OpenSearch 索引中的資料產生摘要。此工具提供一種有效率的方式，協助您從大型資料集中取得洞察，讓您更容易理解 OpenSearch 索引中的資訊，並據以採取行動。

## 組態

若要設定資料摘要功能，請依照下列步驟操作。

### 先決條件

使用資料摘要功能之前，請依照下列方式在 OpenSearch Dashboards 中啟用查詢增強功能：

1. 在頂端選單列中，前往 **Management > Dashboards Management**。
1. 在左側導覽窗格中，選取 **Advanced settings**。
1. 在設定頁面上，將 **Enable query enhancements** 切換為 **On**。

### 步驟 1：啟用資料摘要功能

若要啟用資料摘要功能，請在 `opensearch_dashboards.yml` 中設定以下設定：

```yaml
queryEnhancements.queryAssist.summary.enabled: true
```
{% include copy.html %}

### 步驟 2：建立資料摘要代理程式

若要協調資料摘要作業，請建立一個資料摘要[代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/)。若要建立代理程式，請傳送 `POST /_plugins/_flow_framework/workflow?provision=true` 請求，並以代理程式範本作為承載資料 (payload)：

<details markdown="block">
<summary>
    請求
</summary>
{: .text-delta}

```json
POST /_plugins/_flow_framework/workflow?provision=true
{
  "name": "Query Assist Agent",
  "description": "Create a Query Assist Agent using Claude on BedRock",
  "use_case": "REGISTER_AGENT",
  "version": {
    "template": "1.0.0",
    "compatibility": ["2.13.0", "3.0.0"]
  },
  "workflows": {
    "provision": {
      "user_params": {},
      "nodes": [
        {
          "id": "create_claude_connector",
          "type": "create_connector",
          "previous_node_inputs": {},
          "user_inputs": {
            "version": "1",
            "name": "Claude instant runtime Connector",
            "protocol": "aws_sigv4",
            "description": "The connector to BedRock service for Claude model",
            "actions": [
              {
                "headers": {
                  "x-amz-content-sha256": "required",
                  "content-type": "application/json"
                },
                "method": "POST",
                "request_body": "{\"prompt\":\"${parameters.prompt}\", \"max_tokens_to_sample\":${parameters.max_tokens_to_sample}, \"temperature\":${parameters.temperature},  \"anthropic_version\":\"${parameters.anthropic_version}\" }",
                "action_type": "predict",
                "url": "https://bedrock-runtime.us-west-2.amazonaws.com/model/anthropic.claude-instant-v1/invoke"
              }
            ],
            "credential": {
                "access_key": "<YOUR_ACCESS_KEY>",
                "secret_key": "<YOUR_SECRET_KEY>",
                "session_token": "<YOUR_SESSION_TOKEN>"
            },
            "parameters": {
              "region": "us-west-2",
              "endpoint": "bedrock-runtime.us-west-2.amazonaws.com",
              "content_type": "application/json",
              "auth": "Sig_V4",
              "max_tokens_to_sample": "8000",
              "service_name": "bedrock",
              "temperature": "0.0001",
              "response_filter": "$.completion",
              "anthropic_version": "bedrock-2023-05-31"
            }
          }
        },
        {
          "id": "register_claude_model",
          "type": "register_remote_model",
          "previous_node_inputs": {
            "create_claude_connector": "connector_id"
          },
          "user_inputs": {
            "description": "Claude model",
            "deploy": true,
            "name": "claude-instant"
          }
        },
        {
          "id": "create_query_assist_data_summary_ml_model_tool",
          "type": "create_tool",
          "previous_node_inputs": {
            "register_claude_model": "model_id"
          },
          "user_inputs": {
            "parameters": {
              "prompt": "Human: You are an assistant that helps to summarize the data and provide data insights.\nThe data are queried from OpenSearch index through user's question which was translated into PPL query.\nHere is a sample PPL query: `source=<index> | where <field> = <value>`.\nNow you are given ${parameters.sample_count} sample data out of ${parameters.total_count} total data.\nThe user's question is `${parameters.question}`, the translated PPL query is `${parameters.ppl}` and sample data are:\n```\n${parameters.sample_data}\n```\nCould you help provide a summary of the sample data and provide some useful insights with precise wording and in plain text format, do not use markdown format.\nYou don't need to echo my requirements in response.\n\nAssistant:"
            },
            "name": "MLModelTool",
            "type": "MLModelTool"
          }
        },
        {
          "id": "create_query_assist_data_summary_agent",
          "type": "register_agent",
          "previous_node_inputs": {
            "create_query_assist_data_summary_ml_model_tool": "tools"
          },
          "user_inputs": {
            "parameters": {},
            "type": "flow",
            "name": "Query Assist Data Summary Agent",
            "description": "this is an query assist data summary agent"
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

</details>

如需代理程式範本的範例，請參閱 [Flow Framework 範例範本](https://github.com/opensearch-project/flow-framework/tree/2.x/sample-templates)。請記下代理程式 ID，您將在下一個步驟中使用它。

### 步驟 3：建立根代理程式

接著，為上一個步驟中建立的資料摘要代理程式建立一個[根代理程式]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-tutorial/#root_agent)：

```json
POST /.plugins-ml-config/_doc/os_data2summary
{
  "type": "os_root_agent",
  "configuration": {
    "agent_id": "<DATA_SUMMARY_AGENT_ID>"
  }
}
```
{% include copy-curl.html %}

此範例示範的是系統索引。在已啟用安全性的網域中，只有超級管理員才有權限執行此程式碼。如需有關進行超級管理員呼叫的資訊，請參閱[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)。如需存取權限，請聯絡您的系統管理員。
{: .warning}

### 步驟 4：測試代理程式

您可以使用範例承載資料 (payload) 呼叫代理程式，以驗證資料摘要代理程式是否已成功建立：

```json
POST /_plugins/_ml/agents/{DATA_SUMMARY_AGENT_ID}/_execute
{
  "parameters": {
	"sample_data":"'[{\"_index\":\"90943e30-9a47-11e8-b64d-95841ca0b247\",\"_source\":{\"referer\":\"http://twitter.com/success/gemini-9a\",\"request\":\"/beats/metricbeat/metricbeat-6.3.2-amd64.deb\",\"agent\":\"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)\",\"extension\":\"deb\",\"memory\":null,\"ip\":\"239.67.210.53\",\"index\":\"opensearch_dashboards_sample_data_logs\",\"message\":\"239.67.210.53 - - [2018-08-30T15:29:01.686Z] \\\"GET /beats/metricbeat/metricbeat-6.3.2-amd64.deb HTTP/1.1\\\" 404 2633 \\\"-\\\" \\\"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)\\\"\",\"url\":\"https://artifacts.opensearch.org/downloads/beats/metricbeat/metricbeat-6.3.2-amd64.deb\",\"tags\":\"success\",\"geo\":{\"srcdest\":\"CN:PL\",\"src\":\"CN\",\"coordinates\":{\"lat\":44.91167028,\"lon\":-108.4455092},\"dest\":\"PL\"},\"utc_time\":\"2024-09-05 15:29:01.686\",\"bytes\":2633,\"machine\":{\"os\":\"win xp\",\"ram\":21474836480},\"response\":\"404\",\"clientip\":\"239.67.210.53\",\"host\":\"artifacts.opensearch.org\",\"event\":{\"dataset\":\"sample_web_logs\"},\"phpmemory\":null,\"timestamp\":\"2024-09-05 15:29:01.686\"}}]'",
		"sample_count":1,
		"total_count":383,
		"question":"Are there any errors in my logs?",
		"ppl":"source=opensearch_dashboards_sample_data_logs| where QUERY_STRING(['response'], '4* OR 5*')"}
}
```
{% include copy-curl.html %}

## 產生資料摘要

您可以呼叫 `/api/assistant/data2summary` API 端點來產生資料摘要。`sample_count`、`total_count`、`question` 和 `ppl` 參數為選用：

```json
POST /api/assistant/data2summary
{
	"sample_data":"'[{\"_index\":\"90943e30-9a47-11e8-b64d-95841ca0b247\",\"_source\":{\"referer\":\"http://twitter.com/success/gemini-9a\",\"request\":\"/beats/metricbeat/metricbeat-6.3.2-amd64.deb\",\"agent\":\"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)\",\"extension\":\"deb\",\"memory\":null,\"ip\":\"239.67.210.53\",\"index\":\"opensearch_dashboards_sample_data_logs\",\"message\":\"239.67.210.53 - - [2018-08-30T15:29:01.686Z] \\\"GET /beats/metricbeat/metricbeat-6.3.2-amd64.deb HTTP/1.1\\\" 404 2633 \\\"-\\\" \\\"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)\\\"\",\"url\":\"https://artifacts.opensearch.org/downloads/beats/metricbeat/metricbeat-6.3.2-amd64.deb\",\"tags\":\"success\",\"geo\":{\"srcdest\":\"CN:PL\",\"src\":\"CN\",\"coordinates\":{\"lat\":44.91167028,\"lon\":-108.4455092},\"dest\":\"PL\"},\"utc_time\":\"2024-09-05 15:29:01.686\",\"bytes\":2633,\"machine\":{\"os\":\"win xp\",\"ram\":21474836480},\"response\":\"404\",\"clientip\":\"239.67.210.53\",\"host\":\"artifacts.opensearch.org\",\"event\":{\"dataset\":\"sample_web_logs\"},\"phpmemory\":null,\"timestamp\":\"2024-09-05 15:29:01.686\"}}]'",
    "sample_count":1,
    "total_count":383,
    "question":"Are there any errors in my logs?",
    "ppl":"source=opensearch_dashboards_sample_data_logs| where QUERY_STRING(['response'], '4* OR 5*')"
}
```
{% include copy-curl.html %}

下表說明 Assistant Data Summary API 的參數。

參數 | 必要/選用 | 說明
:--- | :--- | :---
`sample_data` | 必要 | 由指定查詢傳回的資料樣本，用作摘要的輸入。
`question` | 選用 | 使用者以自然語言提出的資料相關問題，用於引導摘要的產生。
`ppl` | 選用 | 用於擷取資料的 Piped Processing Language (PPL) 查詢；在查詢輔助中，此查詢由 LLM 根據使用者的自然語言問題產生。
`sample_count` | 選用 | sample_data 中包含的項目數。
`total_count` | 選用 | 完整查詢結果集中的項目總數。

## 在 OpenSearch Dashboards 中檢視資料摘要

若要在 OpenSearch Dashboards 中檢視警示洞察，請依照下列步驟操作：

1. 在頂端選單列中，前往 **OpenSearch Dashboards > Discover**。

1. 從查詢語言下拉式清單中，選取 **PPL**。您將會在查詢文字之後看到產生的資料摘要，如下圖所示。

    ![資料摘要]({{site.url}}{{site.baseurl}}/images/dashboards-assistant/data-summary.png)
