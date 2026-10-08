---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋工作流程狀態"
parent: Workflow APIs
nav_order: 65
---

# Search Workflow State API

您可以將查詢與欄位進行比對，以搜尋工作流程所建立的資源。可搜尋的欄位對應於 [Get Workflow Status API]({{site.url}}{{site.baseurl}}/automating-configurations/api/get-workflow-status/) 所傳回的欄位。

## 端點

```json
GET /_plugins/_flow_framework/workflow/state/_search
POST /_plugins/_flow_framework/workflow/state/_search
``` 

## 範例請求：所有狀態為 `NOT_STARTED` 的工作流程

```json
GET /_plugins/_flow_framework/workflow/state/_search
{
  "query": {
    "match": {
      "state": "NOT_STARTED"
    }
  }
}
```
{% include copy-curl.html %}

## 範例請求：所有具有 `resources_created` 欄位且其 `workflow_step_id` 為 `register_model_2` 的工作流程

```json
GET /_plugins/_flow_framework/workflow/state/_search
{
  "query": {
    "nested": {
      "path": "resources_created",
      "query": {
        "bool": {
          "must": [
            {
              "match": {
                "resources_created.workflow_step_id": "register_model_2"
              }
            }
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

回應包含符合搜尋參數的文件。