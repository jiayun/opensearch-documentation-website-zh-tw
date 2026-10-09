---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得控制器"
parent: Controller APIs
grand_parent: ML Commons APIs
nav_order: 20
---

# 取得控制器 API
**於 2.12 版推出**
{: .label .label-purple }

使用此 API 可依模型 ID 取得模型的控制器相關資訊。

### 端點

```json
GET /_plugins/_ml/controllers/{model_id}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `model_id` | 字串 | 要取得其控制器的模型 ID。 |

## 範例請求

```json
GET /_plugins/_ml/controllers/T_S-cY0BKCJ3ot9qr0aP
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "model_id": "T_S-cY0BKCJ3ot9qr0aP",
  "user_rate_limiter": {
    "user1": {
      "limit": "4",
      "unit": "MINUTES"
    },
    "user2": {
      "limit": "4",
      "unit": "MINUTES"
    }
  }
}
```

如果模型沒有定義控制器，OpenSearch 會傳回錯誤：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "status_exception",
        "reason": "Failed to find model controller with the provided model ID: T_S-cY0BKCJ3ot9qr0aP"
      }
    ],
    "type": "status_exception",
    "reason": "Failed to find model controller with the provided model ID: T_S-cY0BKCJ3ot9qr0aP"
  },
  "status": 404
}
```

## 回應本文欄位

如需回應欄位的說明，請參閱 [Create Controller API 的請求本文欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/controller-apis/create-controller#request-body-fields)。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:admin/opensearch/ml/controllers/get`。