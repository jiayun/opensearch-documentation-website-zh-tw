---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立異常偵測器工具"
has_children: false
has_toc: false
nav_order: 22
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# 建立異常偵測器工具
**於 2.16 版推出**
{: .label .label-purple }
<!-- vale on -->

這是實驗性功能，不建議在正式環境中使用。如需此功能的最新進展，或想提供意見回饋，請參閱相關的 [GitHub issue](https://github.com/opensearch-project/skills/issues/337)。    
{: .warning}

`CreateAnomalyDetectorTool` 可協助根據您提供的索引建立異常偵測器。此工具會擷取索引對應，並讓大型語言模型 (LLM) 建議類別欄位、彙總欄位及其對應的彙總方法，這些都是 Create Anomaly Detector API 所需的項目。

如需異常偵測器的完整資訊，請參閱[異常偵測]({{site.url}}{{site.baseurl}}/observing-your-data/ad/index/)。
{: .tip}

## 步驟 1：註冊執行 CreateAnomalyDetectorTool 的流程代理程式

流程代理程式會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_Create_Anomaly_Detector_Tool",
  "type": "flow",
  "description": "this is a test agent for the CreateAnomalyDetectorTool",
  "memory": {
    "type": "demo"
  },
  "tools": [
      {
      "type": "CreateAnomalyDetectorTool",
      "name": "DemoCreateAnomalyDetectorTool",
      "parameters": {
        "model_id": "<the model id of LLM>"
      }
    }
  ]
}
```
{% include copy-curl.html %} 

OpenSearch 會回應代理程式 ID，如下列範例所示：

```json
{
  "agent_id": "EuJYYo0B9RaBCvhuy1q8"
}
```
{% include copy-curl.html %} 

## 步驟 2：執行代理程式

傳送下列請求以執行代理程式：

```json
POST /_plugins/_ml/agents/EuJYYo0B9RaBCvhuy1q8/_execute
{
  "parameters": {
    "index": "sample_weblogs_test"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會回應包含建立異常偵測器所需之所有建議參數的 JSON 字串，如下列範例回應所示：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result":"""{"index":"sample_weblogs_test","categoryField":"ip.keyword","aggregationField":"bytes,response,responseLatency","aggregationMethod":"sum,avg,avg","dateFields":"utc_time,timestamp"}"""
        }
      ]
    }
  ]
}
```
{% include copy-curl.html %} 

接著，您可以傳送類似下列的請求，建立包含建議參數的異常偵測器：

```json
POST _plugins/_anomaly_detection/detectors
{
  "name": "test-detector",
  "description": "Test detector",
  "time_field": "timestamp",
  "indices": [
    "sample_weblogs_test"
  ],
  "feature_attributes": [
    {
      "feature_name": "feature_bytes",
      "feature_enabled": true,
      "aggregation_query": {
        "agg1": {
          "sum": {
            "field": "bytes"
          }
        }
      }
    },
    {
      "feature_name": "feature_response",
      "feature_enabled": true,
      "aggregation_query": {
        "agg2": {
          "avg": {
            "field": "response"
          }
        }
      }
    },
    {
      "feature_name": "feature_responseLatency",
      "feature_enabled": true,
      "aggregation_query": {
        "agg3": {
          "avg": {
            "field": "responseLatency"
          }
        }
      }
    }
  ],
  "detection_interval": {
    "period": {
      "interval": 1,
      "unit": "Minutes"
    }
  },
  "window_delay": {
    "period": {
      "interval": 1,
      "unit": "Minutes"
    }
  }
}
```
{% include copy-curl.html %} 

## 註冊參數

下表列出代理程式註冊可用的工具參數。

Parameter	| Type | Required/Optional | Description	
:--- | :--- | :--- | :---
`model_id` | String | Required | 用於建議必要 Create Anomaly Detector API 參數的 LLM 模型 ID。
`model_type` | String | Optional | 模型類型。有效值為 `CLAUDE` (Anthropic Claude 模型) 和 `OPENAI` (OpenAI 模型)。

## 執行參數

下表列出執行代理程式可用的工具參數。

Parameter	| Type | Required/Optional | Description	
:--- | :--- | :--- | :---
`index` | String | Required | 索引名稱。支援萬用字元 (例如 `weblogs-*`)。若使用萬用字元，則工具會從第一個解析出的索引擷取對應，並將其傳送給 LLM。

## 測試工具

您可以將此工具做為代理程式工作流程的一部分執行，或使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用來測試個別工具或執行獨立作業。