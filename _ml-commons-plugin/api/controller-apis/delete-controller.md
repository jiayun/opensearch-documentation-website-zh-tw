---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除控制器"
parent: Controller APIs
grand_parent: ML Commons APIs
nav_order: 50
---

# 刪除控制器 API
**於 2.12 版導入**
{: .label .label-purple }

使用此 API，根據 `model_id` 刪除模型的控制器。

## 端點

```json
DELETE /_plugins/_ml/controllers/{model_id}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `model_id` | 字串 | 要刪除控制器之模型的模型 ID。 |

## 請求範例

```json
DELETE /_plugins/_ml/controllers/MzcIJX8BA7mbufL6DOwl
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "_index" : ".plugins-ml-controller",
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

如果控制器索引不存在時嘗試刪除控制器，OpenSearch 會傳回 404 Not Found 錯誤：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "index_not_found_exception",
        "reason": "no such index [.plugins-ml-controller]",
        "index": ".plugins-ml-controller",
        "resource.id": ".plugins-ml-controller",
        "resource.type": "index_expression",
        "index_uuid": "_na_"
      }
    ],
    "type": "index_not_found_exception",
    "reason": "no such index [.plugins-ml-controller]",
    "index": ".plugins-ml-controller",
    "resource.id": ".plugins-ml-controller",
    "resource.type": "index_expression",
    "index_uuid": "_na_"
  },
  "status": 404
}
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/opensearch/ml/controllers/delete`。