---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除連接器"
parent: Connector APIs
grand_parent: ML Commons APIs
nav_order: 30
---

# 刪除連接器 API

刪除獨立連接器。如需更多資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

## 端點

```json
DELETE /_plugins/_ml/connectors/{connector_id}
```

## 範例請求

```json
DELETE /_plugins/_ml/connectors/KsAo1YsB0jLkkocY6j4U
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "_index" : ".plugins-ml-connector",
  "_id" : "KsAo1YsB0jLkkocY6j4U",
  "_version" : 1,
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

如果您嘗試刪除不存在的連接器，OpenSearch 會傳回 200 回應，其中包含 `"result": "not_found"` 而不是錯誤：

```json
{
  "_index": ".plugins-ml-connector",
  "_id": "nonexistent-connector-id",
  "_version": 1,
  "result": "not_found",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 1,
  "_primary_term": 1
}
```