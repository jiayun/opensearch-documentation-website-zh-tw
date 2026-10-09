---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得管線"
nav_order: 12
redirect_from:
  - /opensearch/rest-api/ingest-apis/get-ingest/
  - /api-reference/ingest-apis/get-ingest/
---

# 取得管線
**於 1.0 版推出**
{: .label .label-purple }

使用取得資料匯入管線的 API 操作，擷取管線的所有資訊。

## 擷取所有管線的資訊

下列範例請求會傳回所有資料匯入管線的資訊：

```json
GET _ingest/pipeline/
```
{% include copy-curl.html %}

## 擷取特定管線的資訊

下列範例請求會傳回特定管線的資訊，本範例中的管線為 `my-pipeline`： 

```json
GET _ingest/pipeline/my-pipeline
```
{% include copy-curl.html %}

回應包含管線資訊：

```json
{
  "my-pipeline": {
    "description": "This pipeline processes student data",
    "processors": [
      {
        "set": {
          "description": "Sets the graduation year to 2023",
          "field": "grad_year",
          "value": 2023
        }
      },
      {
        "set": {
          "description": "Sets graduated to true",
          "field": "graduated",
          "value": true
        }
      },
      {
        "uppercase": {
          "field": "name"
        }
      }
    ]
  }
}
```
