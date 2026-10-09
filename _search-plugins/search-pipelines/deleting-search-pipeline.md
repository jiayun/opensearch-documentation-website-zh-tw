---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除搜尋管線"
nav_order: 30
has_children: false
parent: Search pipelines
---

# 刪除搜尋管線

請使用下列請求來刪除管線。

若要刪除特定的搜尋管線，請將管線 ID 作為參數傳入：

```json
DELETE /_search/pipeline/{pipeline-id}
```
{% include copy-curl.html %}

若要刪除叢集中的所有搜尋管線，請使用萬用字元 (`*`)：

```json
DELETE /_search/pipeline/*
```
{% include copy-curl.html %}
