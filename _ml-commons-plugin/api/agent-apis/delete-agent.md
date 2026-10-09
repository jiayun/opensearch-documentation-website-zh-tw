---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除代理程式"
parent: Agent APIs
grand_parent: ML Commons APIs
nav_order: 40
---

# 刪除代理程式 API
**2.13 版新增**
{: .label .label-purple }

您可以使用此 API 根據 `agent_id` 刪除代理程式。

## 端點

```json
DELETE /_plugins/_ml/agents/{agent_id}
```

## 範例請求

```json
DELETE /_plugins/_ml/agents/MzcIJX8BA7mbufL6DOwl
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "_index" : ".plugins-ml-agent",
  "_id" : "MzcIJX8BA7mbufL6DOwl",
  "_version" : 2,
  "result" : "deleted",
  "_shards" : {
    "total" : 2,
    "successful" : 2,
    "failed" : 0
  },
  "_seq_no" : 27,
  "_primary_term" : 18
}
```

## 錯誤回應

如果您嘗試刪除不存在的代理程式，OpenSearch 會傳回 404 錯誤：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "status_exception",
        "reason": "Fail to find ml agent"
      }
    ],
    "type": "status_exception",
    "reason": "Fail to find ml agent"
  },
  "status": 404
}
```