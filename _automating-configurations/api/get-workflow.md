---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得工作流程"
parent: Workflow APIs
nav_order: 20
---

# Get Workflow API

Get Workflow API 會擷取工作流程範本。   

## 端點

```json
GET /_plugins/_flow_framework/workflow/{workflow_id}
```

## 路徑參數

下表列出可用的路徑參數。 

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `workflow_id` | 字串 | 要擷取的工作流程 ID。必要。 |

## 請求範例

```json
GET /_plugins/_flow_framework/workflow/8xL8bowB8y25Tqfenm50
```
{% include copy-curl.html %}

## 回應範例

若要擷取 YAML 格式的範本，請在請求標頭中指定 `Content-Type: application/yaml`：

```bash
curl -XGET "http://localhost:9200/_plugins/_flow_framework/workflow/8xL8bowB8y25Tqfenm50" -H 'Content-Type: application/yaml'
```

若要擷取 JSON 格式的範本，請在請求標頭中指定 `Content-Type: application/json`：

```bash
curl -XGET "http://localhost:9200/_plugins/_flow_framework/workflow/8xL8bowB8y25Tqfenm50" -H 'Content-Type: application/json'
```

OpenSearch 會回傳已儲存的範本，其內容與[建立工作流程]({{site.url}}{{site.baseurl}}/automating-configurations/api/create-workflow/)請求的本文相同。回傳範本中的欄位順序可能與原始範本不完全一致，但功能相同。