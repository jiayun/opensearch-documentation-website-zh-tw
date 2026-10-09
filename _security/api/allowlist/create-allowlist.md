---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新允許清單"
parent: Allow list APIs
grand_parent: Security APIs
nav_order: 10
---

# 建立或更新允許清單 API
**於 2.1 版推出**
{: .label .label-purple }

建立或取代允許清單組態。

此 API 保留給超級管理員使用。請使用管理員憑證進行驗證，而非使用使用者名稱與密碼。如需更多資訊，請參閱[API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
{: .note}

<!-- spec_insert_start
api: security.create_allowlist
component: endpoints
-->
## 端點
```json
PUT /_plugins/_security/api/allowlist
```
<!-- spec_insert_end -->

## 請求本文欄位

請求本文為必要。其為包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `enabled` | 布林值 | 是否強制執行允許清單。當 `true` 時，沒有管理員權限的使用者只能呼叫 `requests` 中列出的請求。 | 是 |
| `requests` | 物件 | 允許的請求。每個索引鍵都是路徑，例如 `/_cat/nodes`，而每個值都是該路徑允許的 HTTP 方法陣列。 | 是 |

## 範例請求

```json
PUT _plugins/_security/api/allowlist
{
  "enabled": true,
  "requests": {
    "/_cat/nodes": [
      "GET"
    ],
    "/_cat/indices": [
      "GET"
    ],
    "/_plugins/_security/whoami": [
      "GET"
    ]
  }
}
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "status": "OK",
  "message": "'config' updated."
}
```
