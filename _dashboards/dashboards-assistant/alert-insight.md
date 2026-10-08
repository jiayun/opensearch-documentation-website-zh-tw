---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "警示洞察"
parent: OpenSearch Assistant for OpenSearch Dashboards
nav_order: 10
has_children: false
---

# 警示洞察

這是一項實驗性功能，不建議在正式環境中使用。若要取得此功能的最新進度或提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)的討論。    
{: .warning}

OpenSearch Dashboards Assistant 的警示洞察可協助產生警示摘要，並根據觸發警示的記錄檔提供記錄模式。

## 設定警示洞察

若要設定警示洞察，請依照下列步驟操作。

### 先決條件

使用警示洞察之前，您必須在叢集上安裝 `alerting` 與 `alerting-dashboards` 外掛程式。根據預設，這些外掛程式會隨標準 OpenSearch 發行版本一併安裝。如需詳細資訊，請參閱[管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。

### 步驟 1：啟用警示洞察

若要啟用警示洞察，請設定下列 `opensearch_dashboards.yml` 設定：

```yaml
assistant.alertInsight.enabled: true
```
{% include copy.html %}

### 步驟 2：建立代理程式

若要協調警示洞察，您需要建立必要的[代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/)。請傳送以下請求，建立用於建立所有必要代理程式的工作流程範本：

<details markdown="block">
<summary>
    請求
</summary>
{: .text-delta}

```json
POST /_plugins/_flow_framework/workflow?provision=true
{
  "name": "Alert Summary Agent",
  "description": "Create Alert Summary Agent using Claude on BedRock",
  "use_case": "REGISTER_AGENT",
  "version": {
    "template": "1.0.0",
    "compatibility": ["2.17.0", "3.0.0"]
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
                "request_body": "{\"prompt\":\"\\n\\nHuman: ${parameters.prompt}\\n\\nAssistant:\", \"max_tokens_to_sample\":${parameters.max_tokens_to_sample}, \"temperature\":${parameters.temperature},  \"anthropic_version\":\"${parameters.anthropic_version}\" }",
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
          "id": "create_alert_summary_ml_model_tool",
          "type": "create_tool",
          "previous_node_inputs": {
            "register_claude_model": "model_id"
          },
          "user_inputs": {
            "parameters": {
              "prompt": "You are an OpenSearch Alert Assistant to help summarize the alerts.\n Here is the detail of alert: ${parameters.context};\n The question is: ${parameters.question}."
            },
            "name": "MLModelTool",
            "type": "MLModelTool"
          }
        },
        {
          "id": "create_alert_summary_agent",
          "type": "register_agent",
          "previous_node_inputs": {
            "create_alert_summary_ml_model_tool": "tools"
          },
          "user_inputs": {
            "parameters": {},
            "type": "flow",
            "name": "Alert Summary Agent",
            "description": "this is an alert summary agent"
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

</details>

如需代理程式範本的範例，請參閱 [Flow Framework 範例範本](https://github.com/opensearch-project/flow-framework/tree/2.x/sample-templates)。請記下代理程式 ID，您將在下一個步驟中使用。

在此範例中，請使用這些範本建立下列代理程式：
- 一個警示洞察代理程式，請參閱[流程範本](https://github.com/opensearch-project/flow-framework/blob/2.x/sample-templates/create-knowledge-base-alert-agent.json)
- 兩個摘要代理程式：
    - 一個基本警示摘要代理程式，請參閱[流程範本](https://github.com/opensearch-project/flow-framework/blob/2.x/sample-templates/alert-summary-agent-claude-tested.json)
    - 一個用於產生包含記錄模式之警示摘要的代理程式，請參閱[流程範本](https://github.com/opensearch-project/flow-framework/blob/2.x/sample-templates/alert-summary-log-pattern-agent.json)

    這些代理程式需要不同的提示詞。記錄模式摘要的提示詞必須包含預留位置 `${parameters.topNLogPatternData}`，以及引導 LLM 有效運用此資訊的額外指示。請注意，記錄模式僅適用於使用 OpenSearch Dashboards 建立的查詢監視器。

### 步驟 3：建立根代理程式

接下來，為上一個步驟中建立的代理程式建立[根代理程式]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-tutorial/#root_agent)。

為警示摘要代理程式建立根代理程式：

```json
POST /.plugins-ml-config/_doc/os_summary
{
  "type": "os_root_agent",
  "configuration": {
    "agent_id": "<SUMMARY_AGENT_ID>"
  }
}
```
{% include copy-curl.html %}

為包含記錄模式的警示摘要代理程式建立根代理程式：

```json
POST /.plugins-ml-config/_doc/os_summary_with_log_pattern
{
  "type": "os_root_agent",
  "configuration": {
    "agent_id": "<SUMMARY_WITH_LOG_PATTERNS_AGENT_ID>"
  }
}
```
{% include copy-curl.html %}

為警示洞察代理程式建立根代理程式：

```json
POST /.plugins-ml-config/_doc/os_insight
{
  "type": "os_root_agent",
  "configuration": {
    "agent_id": "<ALERT_INSIGHTS_AGENT_ID>"
  }
}
```
{% include copy-curl.html %}

所建立的 `os_insight` 代理程式會提供與 OpenSearch 叢集指標相關的警示洞察。若要取得與 OpenSearch 叢集指標無關之警示的洞察，您需要使用[此範本](https://github.com/opensearch-project/flow-framework/blob/2.x/sample-templates/create-knowledge-base-alert-agent.json)註冊代理程式，並將代理程式名稱變更為 `KB_For_Alert_Insight`。
{: .note}

此範例示範的是系統索引。在已啟用安全性的網域中，只有超級管理員才有權限執行此程式碼。如需進行超級管理員呼叫的相關資訊，請參閱[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)。如需存取權限，請聯絡您的系統管理員。
{: .warning}

### 步驟 4：測試代理程式

您可以使用範例承載呼叫代理程式，以確認代理程式已成功建立。

若要測試警示摘要代理程式，請傳送以下請求：

```json
POST /_plugins/_ml/agents/{SUMMARY_AGENT_ID}/_execute
{ 
  "parameters": {
    "question": "Please summarize this alert, do not use any tool.",
    "context": "\n            Here is the detail information about alert Error log over 100\n            ### Monitor definition\n {\"type\":\"monitor\",\"schema_version\":8,\"name\":\"loghub-apache-error-log\",\"monitor_type\":\"query_level_monitor\",\"enabled\":false,\"enabled_time\":null,\"schedule\":{\"period\":{\"interval\":1,\"unit\":\"MINUTES\"}},\"inputs\":[{\"search\":{\"indices\":[\"loghub-apache-new\"],\"query\":{\"size\":0,\"query\":{\"bool\":{\"filter\":[{\"range\":{\"Time\":{\"from\":\"10/12/24 11:21 am CST||-1000000h\",\"to\":\"10/12/24 11:21 am CST\",\"include_lower\":true,\"include_upper\":true,\"boost\":1}}},{\"term\":{\"Level\":{\"value\":\"error\",\"boost\":1}}}],\"adjust_pure_negative\":true,\"boost\":1}}}}}],\"triggers\":[{\"query_level_trigger\":{\"id\":\"NAq7fpIBRJyww-JMjwP_\",\"name\":\"Error log over 100\",\"severity\":\"1\",\"condition\":{\"script\":{\"source\":\"ctx.results[0].hits.total.value > 100\",\"lang\":\"painless\"}},\"actions\":[]}}],\"last_update_time\":1728714554388,\"owner\":\"alerting\",\"associated_workflows\":[],\"associatedCompositeMonitorCnt\":0,\"item_type\":\"query_level_monitor\",\"id\":\"NQq7fpIBRJyww-JMkAMC\",\"version\":3}\n\n            ### Active Alert\n {\"ACTIVE\":1,\"ACKNOWLEDGED\":0,\"ERROR\":0,\"total\":1,\"alerts\":[{\"id\":\"Wgq8fpIBRJyww-JMegNr\",\"monitor_id\":\"NQq7fpIBRJyww-JMkAMC\",\"workflow_id\":\"\",\"workflow_name\":\"\",\"associated_alert_ids\":[],\"schema_version\":5,\"monitor_version\":1,\"monitor_name\":\"loghub-apache-error-log\",\"execution_id\":\"NQq7fpIBRJyww-JMkAMC_2024-10-12T03:18:54.311214115_22d189ce-5e93-4927-b8bb-bcf61b7537e3\",\"trigger_id\":\"NAq7fpIBRJyww-JMjwP_\",\"trigger_name\":\"Error log over 100\",\"finding_ids\":[],\"related_doc_ids\":[],\"state\":\"ACTIVE\",\"error_message\":null,\"alert_history\":[],\"severity\":\"1\",\"action_execution_results\":[],\"start_time\":\"10/12/24 11:18 am CST\",\"last_notification_time\":\"10/12/24 11:21 am CST\",\"end_time\":null,\"acknowledged_time\":null,\"alert_source\":\"monitor\"}],\"trigger_name\":\"Error log over 100\",\"severity\":\"1\",\"start_time\":\"10/12/24 11:18 am CST\",\"last_notification_time\":\"10/12/24 11:21 am CST\",\"monitor_name\":\"loghub-apache-error-log\",\"monitor_id\":\"NQq7fpIBRJyww-JMkAMC\",\"alert_source\":\"monitor\",\"triggerID\":\"NAq7fpIBRJyww-JMjwP_\"}\n\n            ### Value triggers this alert\n 595\n\n            ### Alert query DSL {\"query\":{\"bool\":{\"filter\":[{\"range\":{\"Time\":{\"from\":\"2024-10-12T03:21:54+00:00||-1000000h\",\"to\":\"2024-10-12T03:21:54+00:00\",\"include_lower\":true,\"include_upper\":true,\"boost\":1}}},{\"term\":{\"Level\":{\"value\":\"error\",\"boost\":1}}}],\"adjust_pure_negative\":true,\"boost\":1}}} \n",
  }
}
```
{% include copy-curl.html %}

若要測試包含記錄模式之警示摘要代理程式，請傳送以下請求：

```json
POST /_plugins/_ml/agents/{SUMMARY_WITH_LOG_PATTERNS_AGENT_ID}/_execute
{ 
  "parameters": {
    "question": "Please summarize this alert, do not use any tool.",
    "context": "\n            Here is the detail information about alert Error log over 100\n            ### Monitor definition\n {\"type\":\"monitor\",\"schema_version\":8,\"name\":\"loghub-apache-error-log\",\"monitor_type\":\"query_level_monitor\",\"enabled\":false,\"enabled_time\":null,\"schedule\":{\"period\":{\"interval\":1,\"unit\":\"MINUTES\"}},\"inputs\":[{\"search\":{\"indices\":[\"loghub-apache-new\"],\"query\":{\"size\":0,\"query\":{\"bool\":{\"filter\":[{\"range\":{\"Time\":{\"from\":\"10/12/24 11:21 am CST||-1000000h\",\"to\":\"10/12/24 11:21 am CST\",\"include_lower\":true,\"include_upper\":true,\"boost\":1}}},{\"term\":{\"Level\":{\"value\":\"error\",\"boost\":1}}}],\"adjust_pure_negative\":true,\"boost\":1}}}}}],\"triggers\":[{\"query_level_trigger\":{\"id\":\"NAq7fpIBRJyww-JMjwP_\",\"name\":\"Error log over 100\",\"severity\":\"1\",\"condition\":{\"script\":{\"source\":\"ctx.results[0].hits.total.value > 100\",\"lang\":\"painless\"}},\"actions\":[]}}],\"last_update_time\":1728714554388,\"owner\":\"alerting\",\"associated_workflows\":[],\"associatedCompositeMonitorCnt\":0,\"item_type\":\"query_level_monitor\",\"id\":\"NQq7fpIBRJyww-JMkAMC\",\"version\":3}\n\n            ### Active Alert\n {\"ACTIVE\":1,\"ACKNOWLEDGED\":0,\"ERROR\":0,\"total\":1,\"alerts\":[{\"id\":\"Wgq8fpIBRJyww-JMegNr\",\"monitor_id\":\"NQq7fpIBRJyww-JMkAMC\",\"workflow_id\":\"\",\"workflow_name\":\"\",\"associated_alert_ids\":[],\"schema_version\":5,\"monitor_version\":1,\"monitor_name\":\"loghub-apache-error-log\",\"execution_id\":\"NQq7fpIBRJyww-JMkAMC_2024-10-12T03:18:54.311214115_22d189ce-5e93-4927-b8bb-bcf61b7537e3\",\"trigger_id\":\"NAq7fpIBRJyww-JMjwP_\",\"trigger_name\":\"Error log over 100\",\"finding_ids\":[],\"related_doc_ids\":[],\"state\":\"ACTIVE\",\"error_message\":null,\"alert_history\":[],\"severity\":\"1\",\"action_execution_results\":[],\"start_time\":\"10/12/24 11:18 am CST\",\"last_notification_time\":\"10/12/24 11:21 am CST\",\"end_time\":null,\"acknowledged_time\":null,\"alert_source\":\"monitor\"}],\"trigger_name\":\"Error log over 100\",\"severity\":\"1\",\"start_time\":\"10/12/24 11:18 am CST\",\"last_notification_time\":\"10/12/24 11:21 am CST\",\"monitor_name\":\"loghub-apache-error-log\",\"monitor_id\":\"NQq7fpIBRJyww-JMkAMC\",\"alert_source\":\"monitor\",\"triggerID\":\"NAq7fpIBRJyww-JMjwP_\"}\n\n            ### Value triggers this alert\n 595\n\n            ### Alert query DSL {\"query\":{\"bool\":{\"filter\":[{\"range\":{\"Time\":{\"from\":\"2024-10-12T03:21:54+00:00||-1000000h\",\"to\":\"2024-10-12T03:21:54+00:00\",\"include_lower\":true,\"include_upper\":true,\"boost\":1}}},{\"term\":{\"Level\":{\"value\":\"error\",\"boost\":1}}}],\"adjust_pure_negative\":true,\"boost\":1}}} \n",
    "topNLogPatternData": "[[539,[&quot;[Sun Dec 04 07:12:44 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 06:19:18 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 07:18:00 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 16:52:49 2005] [error] mod_jk child workerEnv in error state 7&quot;,&quot;[Sun Dec 04 06:59:47 2005] [error] mod_jk child workerEnv in error state 8&quot;,&quot;[Sun Dec 04 07:11:22 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 07:18:00 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 17:01:47 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 17:31:12 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 05:04:04 2005] [error] mod_jk child workerEnv in error state 7&quot;,&quot;[Sun Dec 04 20:24:49 2005] [error] mod_jk child workerEnv in error state 8&quot;,&quot;[Sun Dec 04 06:16:23 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 20:47:17 2005] [error] mod_jk child workerEnv in error state 7&quot;,&quot;[Sun Dec 04 06:30:43 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Mon Dec 05 06:35:27 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 07:07:30 2005] [error] mod_jk child workerEnv in error state 8&quot;,&quot;[Sun Dec 04 07:18:00 2005] [error] mod_jk child workerEnv in error state 7&quot;,&quot;[Sun Dec 04 16:32:56 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 17:01:47 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 16:52:49 2005] [error] mod_jk child workerEnv in error state 8&quot;],&quot;[   :: ] [] _      &quot;],[32,[&quot;[Sun Dec 04 14:29:00 2005] [error] [client 4.245.93.87] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 08:54:17 2005] [error] [client 147.31.138.75] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 17:34:57 2005] [error] [client 61.138.216.82] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 07:45:45 2005] [error] [client 63.13.186.196] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 10:53:30 2005] [error] [client 218.76.139.20] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 10:48:48 2005] [error] [client 67.166.248.235] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 15:18:36 2005] [error] [client 67.154.58.130] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 01:30:32 2005] [error] [client 211.62.201.48] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 16:45:04 2005] [error] [client 216.216.185.130] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 17:31:39 2005] [error] [client 218.75.106.250] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 19:00:56 2005] [error] [client 68.228.3.15] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 19:14:09 2005] [error] [client 61.220.139.68] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 09:35:12 2005] [error] [client 207.203.80.15] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 10:28:44 2005] [error] [client 198.232.168.9] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 16:24:05 2005] [error] [client 58.225.62.140] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 17:53:43 2005] [error] [client 218.39.132.175] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 12:33:13 2005] [error] [client 208.51.151.210] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 15:59:01 2005] [error] [client 24.83.37.136] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 11:42:43 2005] [error] [client 216.127.124.16] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 05:15:09 2005] [error] [client 222.166.160.184] Directory index forbidden by rule: /var/www/html/&quot;],&quot;[   :: ] [] [ ...]     : ////&quot;],[12,[&quot;[Sun Dec 04 20:47:17 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Sun Dec 04 20:47:17 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Mon Dec 05 07:57:02 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Sun Dec 04 17:43:12 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Sun Dec 04 20:47:17 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Sun Dec 04 20:47:16 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Mon Dec 05 07:57:02 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Sun Dec 04 17:43:12 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Mon Dec 05 11:06:52 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Mon Dec 05 11:06:52 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Mon Dec 05 11:06:52 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Mon Dec 05 11:06:52 2005] [error] mod_jk child init 1 -2&quot;],&quot;[   :: ] [] _    -&quot;]]"
  }
}
```
{% include copy-curl.html %}

若要測試警示洞察代理程式，請傳送以下請求：

```json
POST /_plugins/_ml/agents/{ALERT_INSIGHTS_AGENT_ID}/_execute
{ 
  "parameters": {
    "question": "Please provide your insight on this alerts.",
    "context": "\n            Here is the detail information about alert Error log over 100\n            ### Monitor definition\n {\"type\":\"monitor\",\"schema_version\":8,\"name\":\"loghub-apache-error-log\",\"monitor_type\":\"query_level_monitor\",\"enabled\":false,\"enabled_time\":null,\"schedule\":{\"period\":{\"interval\":1,\"unit\":\"MINUTES\"}},\"inputs\":[{\"search\":{\"indices\":[\"loghub-apache-new\"],\"query\":{\"size\":0,\"query\":{\"bool\":{\"filter\":[{\"range\":{\"Time\":{\"from\":\"10/12/24 11:21 am CST||-1000000h\",\"to\":\"10/12/24 11:21 am CST\",\"include_lower\":true,\"include_upper\":true,\"boost\":1}}},{\"term\":{\"Level\":{\"value\":\"error\",\"boost\":1}}}],\"adjust_pure_negative\":true,\"boost\":1}}}}}],\"triggers\":[{\"query_level_trigger\":{\"id\":\"NAq7fpIBRJyww-JMjwP_\",\"name\":\"Error log over 100\",\"severity\":\"1\",\"condition\":{\"script\":{\"source\":\"ctx.results[0].hits.total.value > 100\",\"lang\":\"painless\"}},\"actions\":[]}}],\"last_update_time\":1728714554388,\"owner\":\"alerting\",\"associated_workflows\":[],\"associatedCompositeMonitorCnt\":0,\"item_type\":\"query_level_monitor\",\"id\":\"NQq7fpIBRJyww-JMkAMC\",\"version\":3}\n\n            ### Active Alert\n {\"ACTIVE\":1,\"ACKNOWLEDGED\":0,\"ERROR\":0,\"total\":1,\"alerts\":[{\"id\":\"Wgq8fpIBRJyww-JMegNr\",\"monitor_id\":\"NQq7fpIBRJyww-JMkAMC\",\"workflow_id\":\"\",\"workflow_name\":\"\",\"associated_alert_ids\":[],\"schema_version\":5,\"monitor_version\":1,\"monitor_name\":\"loghub-apache-error-log\",\"execution_id\":\"NQq7fpIBRJyww-JMkAMC_2024-10-12T03:18:54.311214115_22d189ce-5e93-4927-b8bb-bcf61b7537e3\",\"trigger_id\":\"NAq7fpIBRJyww-JMjwP_\",\"trigger_name\":\"Error log over 100\",\"finding_ids\":[],\"related_doc_ids\":[],\"state\":\"ACTIVE\",\"error_message\":null,\"alert_history\":[],\"severity\":\"1\",\"action_execution_results\":[],\"start_time\":\"10/12/24 11:18 am CST\",\"last_notification_time\":\"10/12/24 11:21 am CST\",\"end_time\":null,\"acknowledged_time\":null,\"alert_source\":\"monitor\"}],\"trigger_name\":\"Error log over 100\",\"severity\":\"1\",\"start_time\":\"10/12/24 11:18 am CST\",\"last_notification_time\":\"10/12/24 11:21 am CST\",\"monitor_name\":\"loghub-apache-error-log\",\"monitor_id\":\"NQq7fpIBRJyww-JMkAMC\",\"alert_source\":\"monitor\",\"triggerID\":\"NAq7fpIBRJyww-JMjwP_\"}\n\n            ### Value triggers this alert\n 595\n\n            ### Alert query DSL {\"query\":{\"bool\":{\"filter\":[{\"range\":{\"Time\":{\"from\":\"2024-10-12T03:21:54+00:00||-1000000h\",\"to\":\"2024-10-12T03:21:54+00:00\",\"include_lower\":true,\"include_upper\":true,\"boost\":1}}},{\"term\":{\"Level\":{\"value\":\"error\",\"boost\":1}}}],\"adjust_pure_negative\":true,\"boost\":1}}} \n",
    "summary": <OUTPUT FROM ALERT SUMMARY AGENT>
  }
}
```
{% include copy-curl.html %}

## 產生警示摘要

您可以呼叫 `/api/assistant/summary` API 端點來產生警示摘要。若要產生警示摘要，`index`、`dsl` 和 `topNLogPatternData` 欄位皆為選用。如果提供了這三個欄位，代理程式會提供包含記錄檔模式分析的摘要；否則，代理程式會提供一般摘要：

```json
POST /api/assistant/summary
{
  "summaryType": "alerts",
  "question": "Please summarize this alert, do not use any tool.",
  "context": "\n            Here is the detail information about alert Error log over 100\n            ### Monitor definition\n {\"type\":\"monitor\",\"schema_version\":8,\"name\":\"loghub-apache-error-log\",\"monitor_type\":\"query_level_monitor\",\"enabled\":false,\"enabled_time\":null,\"schedule\":{\"period\":{\"interval\":1,\"unit\":\"MINUTES\"}},\"inputs\":[{\"search\":{\"indices\":[\"loghub-apache-new\"],\"query\":{\"size\":0,\"query\":{\"bool\":{\"filter\":[{\"range\":{\"Time\":{\"from\":\"10/12/24 11:21 am CST||-1000000h\",\"to\":\"10/12/24 11:21 am CST\",\"include_lower\":true,\"include_upper\":true,\"boost\":1}}},{\"term\":{\"Level\":{\"value\":\"error\",\"boost\":1}}}],\"adjust_pure_negative\":true,\"boost\":1}}}}}],\"triggers\":[{\"query_level_trigger\":{\"id\":\"NAq7fpIBRJyww-JMjwP_\",\"name\":\"Error log over 100\",\"severity\":\"1\",\"condition\":{\"script\":{\"source\":\"ctx.results[0].hits.total.value > 100\",\"lang\":\"painless\"}},\"actions\":[]}}],\"last_update_time\":1728714554388,\"owner\":\"alerting\",\"associated_workflows\":[],\"associatedCompositeMonitorCnt\":0,\"item_type\":\"query_level_monitor\",\"id\":\"NQq7fpIBRJyww-JMkAMC\",\"version\":3}\n\n            ### Active Alert\n {\"ACTIVE\":1,\"ACKNOWLEDGED\":0,\"ERROR\":0,\"total\":1,\"alerts\":[{\"id\":\"Wgq8fpIBRJyww-JMegNr\",\"monitor_id\":\"NQq7fpIBRJyww-JMkAMC\",\"workflow_id\":\"\",\"workflow_name\":\"\",\"associated_alert_ids\":[],\"schema_version\":5,\"monitor_version\":1,\"monitor_name\":\"loghub-apache-error-log\",\"execution_id\":\"NQq7fpIBRJyww-JMkAMC_2024-10-12T03:18:54.311214115_22d189ce-5e93-4927-b8bb-bcf61b7537e3\",\"trigger_id\":\"NAq7fpIBRJyww-JMjwP_\",\"trigger_name\":\"Error log over 100\",\"finding_ids\":[],\"related_doc_ids\":[],\"state\":\"ACTIVE\",\"error_message\":null,\"alert_history\":[],\"severity\":\"1\",\"action_execution_results\":[],\"start_time\":\"10/12/24 11:18 am CST\",\"last_notification_time\":\"10/12/24 11:21 am CST\",\"end_time\":null,\"acknowledged_time\":null,\"alert_source\":\"monitor\"}],\"trigger_name\":\"Error log over 100\",\"severity\":\"1\",\"start_time\":\"10/12/24 11:18 am CST\",\"last_notification_time\":\"10/12/24 11:21 am CST\",\"monitor_name\":\"loghub-apache-error-log\",\"monitor_id\":\"NQq7fpIBRJyww-JMkAMC\",\"alert_source\":\"monitor\",\"triggerID\":\"NAq7fpIBRJyww-JMjwP_\"}\n\n            ### Value triggers this alert\n 595\n\n            ### Alert query DSL {\"query\":{\"bool\":{\"filter\":[{\"range\":{\"Time\":{\"from\":\"2024-10-12T03:21:54+00:00||-1000000h\",\"to\":\"2024-10-12T03:21:54+00:00\",\"include_lower\":true,\"include_upper\":true,\"boost\":1}}},{\"term\":{\"Level\":{\"value\":\"error\",\"boost\":1}}}],\"adjust_pure_negative\":true,\"boost\":1}}} \n",
  "index": "loghub-apache-new",
  "dsl": "{\"query\":{\"bool\":{\"filter\":[{\"range\":{\"Time\":{\"from\":\"2024-10-12T03:21:54+00:00||-1000000h\",\"to\":\"2024-10-12T03:21:54+00:00\",\"include_lower\":true,\"include_upper\":true,\"boost\":1}}},{\"term\":{\"Level\":{\"value\":\"error\",\"boost\":1}}}],\"adjust_pure_negative\":true,\"boost\":1}}}",
  "topNLogPatternData": "[[539,[&quot;[Sun Dec 04 07:12:44 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 06:19:18 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 07:18:00 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 16:52:49 2005] [error] mod_jk child workerEnv in error state 7&quot;,&quot;[Sun Dec 04 06:59:47 2005] [error] mod_jk child workerEnv in error state 8&quot;,&quot;[Sun Dec 04 07:11:22 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 07:18:00 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 17:01:47 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 17:31:12 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 05:04:04 2005] [error] mod_jk child workerEnv in error state 7&quot;,&quot;[Sun Dec 04 20:24:49 2005] [error] mod_jk child workerEnv in error state 8&quot;,&quot;[Sun Dec 04 06:16:23 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 20:47:17 2005] [error] mod_jk child workerEnv in error state 7&quot;,&quot;[Sun Dec 04 06:30:43 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Mon Dec 05 06:35:27 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 07:07:30 2005] [error] mod_jk child workerEnv in error state 8&quot;,&quot;[Sun Dec 04 07:18:00 2005] [error] mod_jk child workerEnv in error state 7&quot;,&quot;[Sun Dec 04 16:32:56 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 17:01:47 2005] [error] mod_jk child workerEnv in error state 6&quot;,&quot;[Sun Dec 04 16:52:49 2005] [error] mod_jk child workerEnv in error state 8&quot;],&quot;[   :: ] [] _      &quot;],[32,[&quot;[Sun Dec 04 14:29:00 2005] [error] [client 4.245.93.87] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 08:54:17 2005] [error] [client 147.31.138.75] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 17:34:57 2005] [error] [client 61.138.216.82] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 07:45:45 2005] [error] [client 63.13.186.196] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 10:53:30 2005] [error] [client 218.76.139.20] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 10:48:48 2005] [error] [client 67.166.248.235] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 15:18:36 2005] [error] [client 67.154.58.130] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 01:30:32 2005] [error] [client 211.62.201.48] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 16:45:04 2005] [error] [client 216.216.185.130] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 17:31:39 2005] [error] [client 218.75.106.250] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 19:00:56 2005] [error] [client 68.228.3.15] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 19:14:09 2005] [error] [client 61.220.139.68] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 09:35:12 2005] [error] [client 207.203.80.15] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Mon Dec 05 10:28:44 2005] [error] [client 198.232.168.9] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 16:24:05 2005] [error] [client 58.225.62.140] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 17:53:43 2005] [error] [client 218.39.132.175] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 12:33:13 2005] [error] [client 208.51.151.210] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 15:59:01 2005] [error] [client 24.83.37.136] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 11:42:43 2005] [error] [client 216.127.124.16] Directory index forbidden by rule: /var/www/html/&quot;,&quot;[Sun Dec 04 05:15:09 2005] [error] [client 222.166.160.184] Directory index forbidden by rule: /var/www/html/&quot;],&quot;[   :: ] [] [ ...]     : ////&quot;],[12,[&quot;[Sun Dec 04 20:47:17 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Sun Dec 04 20:47:17 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Mon Dec 05 07:57:02 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Sun Dec 04 17:43:12 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Sun Dec 04 20:47:17 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Sun Dec 04 20:47:16 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Mon Dec 05 07:57:02 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Sun Dec 04 17:43:12 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Mon Dec 05 11:06:52 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Mon Dec 05 11:06:52 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Mon Dec 05 11:06:52 2005] [error] mod_jk child init 1 -2&quot;,&quot;[Mon Dec 05 11:06:52 2005] [error] mod_jk child init 1 -2&quot;],&quot;[   :: ] [] _    -&quot;]]"
}
```
{% include copy-curl.html %}

下表說明 Assistant Summary API 的參數。

參數 | 必要/選用 | 說明
:--- | :--- | :---
`summaryType` | 必要 | 指定呼叫此 API 的應用程式類型。若為警示洞察，請使用 `alerts`。
`question` | 必要 | 指定使用者關於警示洞察的問題。預設為 `Please summarize this alert, do not use any tool.` 
`context` | 必要 | 提供警示的內容資訊，包括警示監視器定義、作用中警示以及觸發值。
`index` | 選用 | 警示所監視的索引。如果未提供此參數，則不會回傳記錄檔模式分析。
`dsl` | 選用 | 用於警示監視的 DSL 查詢。如果未提供此參數，則不會回傳記錄檔模式分析。
`topNLogPatternData` | 選用 | 警示觸發資料的記錄檔模式。如果未提供此參數，則不會回傳記錄檔模式分析。

## 產生警示洞察

您可以呼叫 `/api/assistant/insight` API 端點來產生警示洞察。若要產生警示洞察，必須提供以下所有參數：

```json
POST /api/assistant/insight
{
  "summaryType": "alerts",
  "insightType": "user_insight"
  "context": "\n            Here is the detail information about alert Error log over 100\n            ### Monitor definition\n {\"type\":\"monitor\",\"schema_version\":8,\"name\":\"loghub-apache-error-log\",\"monitor_type\":\"query_level_monitor\",\"enabled\":false,\"enabled_time\":null,\"schedule\":{\"period\":{\"interval\":1,\"unit\":\"MINUTES\"}},\"inputs\":[{\"search\":{\"indices\":[\"loghub-apache-new\"],\"query\":{\"size\":0,\"query\":{\"bool\":{\"filter\":[{\"range\":{\"Time\":{\"from\":\"10/12/24 11:21 am CST||-1000000h\",\"to\":\"10/12/24 11:21 am CST\",\"include_lower\":true,\"include_upper\":true,\"boost\":1}}},{\"term\":{\"Level\":{\"value\":\"error\",\"boost\":1}}}],\"adjust_pure_negative\":true,\"boost\":1}}}}}],\"triggers\":[{\"query_level_trigger\":{\"id\":\"NAq7fpIBRJyww-JMjwP_\",\"name\":\"Error log over 100\",\"severity\":\"1\",\"condition\":{\"script\":{\"source\":\"ctx.results[0].hits.total.value > 100\",\"lang\":\"painless\"}},\"actions\":[]}}],\"last_update_time\":1728714554388,\"owner\":\"alerting\",\"associated_workflows\":[],\"associatedCompositeMonitorCnt\":0,\"item_type\":\"query_level_monitor\",\"id\":\"NQq7fpIBRJyww-JMkAMC\",\"version\":3}\n\n            ### Active Alert\n {\"ACTIVE\":1,\"ACKNOWLEDGED\":0,\"ERROR\":0,\"total\":1,\"alerts\":[{\"id\":\"Wgq8fpIBRJyww-JMegNr\",\"monitor_id\":\"NQq7fpIBRJyww-JMkAMC\",\"workflow_id\":\"\",\"workflow_name\":\"\",\"associated_alert_ids\":[],\"schema_version\":5,\"monitor_version\":1,\"monitor_name\":\"loghub-apache-error-log\",\"execution_id\":\"NQq7fpIBRJyww-JMkAMC_2024-10-12T03:18:54.311214115_22d189ce-5e93-4927-b8bb-bcf61b7537e3\",\"trigger_id\":\"NAq7fpIBRJyww-JMjwP_\",\"trigger_name\":\"Error log over 100\",\"finding_ids\":[],\"related_doc_ids\":[],\"state\":\"ACTIVE\",\"error_message\":null,\"alert_history\":[],\"severity\":\"1\",\"action_execution_results\":[],\"start_time\":\"10/12/24 11:18 am CST\",\"last_notification_time\":\"10/12/24 11:21 am CST\",\"end_time\":null,\"acknowledged_time\":null,\"alert_source\":\"monitor\"}],\"trigger_name\":\"Error log over 100\",\"severity\":\"1\",\"start_time\":\"10/12/24 11:18 am CST\",\"last_notification_time\":\"10/12/24 11:21 am CST\",\"monitor_name\":\"loghub-apache-error-log\",\"monitor_id\":\"NQq7fpIBRJyww-JMkAMC\",\"alert_source\":\"monitor\",\"triggerID\":\"NAq7fpIBRJyww-JMjwP_\"}\n\n            ### Value triggers this alert\n 595\n\n            ### Alert query DSL {\"query\":{\"bool\":{\"filter\":[{\"range\":{\"Time\":{\"from\":\"2024-10-12T03:21:54+00:00||-1000000h\",\"to\":\"2024-10-12T03:21:54+00:00\",\"include_lower\":true,\"include_upper\":true,\"boost\":1}}},{\"term\":{\"Level\":{\"value\":\"error\",\"boost\":1}}}],\"adjust_pure_negative\":true,\"boost\":1}}} \n",
  "question": "Please provide your insight on this alerts.",
  "summary": <OUTPUT FROM ALERT SUMMARY AGENT>
}
```
{% include copy-curl.html %}

下表說明 Assistant Insight API 的參數。

參數 | 必要/選用 | 說明 
:--- | :--- | :---
`summaryType` | 必要 | 指定呼叫此 API 的應用程式類型。若為警示洞察，請使用 `alerts`。
`insightType` | 必要 | 定義警示類型。叢集指標警示請使用 `os_insight`，其他警示類型請使用 `user_insight`。
`question` | 必要 | 指定使用者關於警示洞察的問題。預設為 `Please provide your insight on this alerts.` 
`context` | 必要 | 提供警示的內容資訊，包括警示監視器定義、作用中警示以及觸發值。
`summary` | 必要 | 警示摘要代理程式所回傳的結果。


## 在 OpenSearch Dashboards 中檢視警示洞察

在檢視警示洞察之前，您必須先在 OpenSearch Dashboards 中設定警示。如需詳細資訊，請參閱[警示]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/index/)。

若要在 OpenSearch Dashboards 中檢視警示洞察，請使用以下步驟：

1. 在頂端選單列中，前往 **OpenSearch Plugins > Alerting**。系統會顯示所有警示。

1. 將游標停留在所需監視器的警示上。如果您已設定警示洞察，將會在 **Alerts** 欄中的警示旁邊看到閃亮圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards-assistant/sparkle-icon.png" class="inline-icon" alt="sparkle icon"/>{:/})，如下圖所示。
    
    ![含有閃亮圖示的 Alerting 頁面]({{site.url}}{{site.baseurl}}/images/dashboards-assistant/alert-insight-start.png)

1. 選取警示標籤或閃亮圖示。您將會看到產生的摘要，如下圖所示。
    
    ![警示摘要]({{site.url}}{{site.baseurl}}/images/dashboards-assistant/alert-insight-summary.png)

1. 選取資訊圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards-assistant/info-icon.png" class="inline-icon" alt="info icon"/>{:/}) 以檢視警示洞察。您將會看到產生的警示洞察，如下圖所示。
    
    ![警示洞察]({{site.url}}{{site.baseurl}}/images/dashboards-assistant/alert-insight-insight.png)