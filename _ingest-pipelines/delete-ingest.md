---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除管線"
nav_order: 13
redirect_from:
  - /opensearch/rest-api/ingest-apis/delete-ingest/
  - /api-reference/ingest-apis/delete-ingest/
---

# 刪除管線
**1.0 版推出**
{: .label .label-purple }

使用下列請求來刪除管線。

若要刪除特定的管線，請將管線 ID 作為參數傳入：

```json
DELETE /_ingest/pipeline/{pipeline-id}
```
{% include copy-curl.html %}

若要刪除叢集中的所有管線，請使用萬用字元 (`*`)：

```json
DELETE /_ingest/pipeline/*
```
{% include copy-curl.html %}
