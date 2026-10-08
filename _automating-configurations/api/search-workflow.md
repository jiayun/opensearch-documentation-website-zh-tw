---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋工作流程"
parent: Workflow APIs
nav_order: 60
---

# Search Workflow API

您可以使用 `workflow_id` 擷取已建立的工作流程，或透過符合某欄位的查詢來搜尋工作流程。您可以使用 `use_case` 欄位來搜尋類似的工作流程。

## 端點

```json
GET /_plugins/_flow_framework/workflow/_search
POST /_plugins/_flow_framework/workflow/_search
``` 

## 範例請求：所有已建立的工作流程

```json
GET /_plugins/_flow_framework/workflow/_search
{
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

## 範例請求：所有 `use_case` 為 `REMOTE_MODEL_DEPLOYMENT` 的工作流程

```json
GET /_plugins/_flow_framework/workflow/_search
{
  "query": {
    "match": {
      "use_case": "REMOTE_MODEL_DEPLOYMENT"
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

OpenSearch 會以符合搜尋參數的工作流程範本清單回應。