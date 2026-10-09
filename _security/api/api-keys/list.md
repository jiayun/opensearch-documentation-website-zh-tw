---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "列出 API 金鑰"
parent: API key APIs
grand_parent: Security APIs
nav_order: 20
redirect_from:
  - /api-reference/security/api-keys/list/
---

# List API Keys API
**於 3.7 版導入**
{: .label .label-purple }

傳回所有 API 金鑰，包括作用中、已到期與已撤銷的金鑰。

## 端點

```json
GET /_plugins/_security/api/apitokens
```

## 範例請求

```json
GET _plugins/_security/api/apitokens
```
{% include copy-curl.html security=true %}

## 範例回應

```json
[
  {
    "id": "_ofOi6ABkhwU_cGa4M3v",
    "name": "test-token",
    "iat": 1789051986089,
    "expires_at": 1789138386088,
    "cluster_permissions": [
      "cluster_monitor"
    ],
    "index_permissions": [
      {
        "index_pattern": [
          "logs*"
        ],
        "allowed_actions": [
          "read"
        ]
      }
    ],
    "created_by": "admin"
  }
]
```

## 回應本文欄位

回應本文是一個 JSON 物件陣列。每個物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `id` | 字串 | 金鑰的唯一識別碼。 |
| `name` | 字串 | 金鑰名稱。 |
| `iat` | Long | 簽發時間戳記，以 epoch 毫秒表示。 |
| `expires_at` | Long | 到期時間戳記，以 epoch 毫秒表示。 |
| `cluster_permissions` | 字串陣列 | 授權給此金鑰的叢集層級權限。 |
| `index_permissions` | 物件陣列 | 授權給此金鑰的索引層級權限。 |
| `revoked_at` | Long | 撤銷時間戳記，以 epoch 毫秒表示。僅在金鑰已被撤銷時才會出現。 |
| `created_by` | 字串 | 建立此金鑰的使用者。 |
