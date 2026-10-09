---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "排清快取"
parent: Security APIs
nav_order: 150
redirect_from:
  - /security/api/cache/
  - /security/api/cache/flush-cache/
---

# Flush Cache API
**於 1.0 版推出**
{: .label .label-purple }

排清 Security 外掛程式的使用者、驗證與授權快取。

`DELETE` 是唯一支援的方法。對 `_plugins/_security/api/cache` 傳送 `GET`、`PUT` 與 `POST` 請求會回傳 `405` 錯誤，並指出 `DELETE` 為允許的方法。

<!-- spec_insert_start
api: security.flush_cache
component: endpoints
-->
## 端點
```json
DELETE /_plugins/_security/api/cache
```
<!-- spec_insert_end -->

## 範例請求

```json
DELETE _plugins/_security/api/cache
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "status": "OK",
  "message": "Cache flushed successfully."
}
```

## 回應本文欄位

回應本文是一個包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `status` | 字串 | 請求的狀態。`OK` 表示 OpenSearch 已排清快取。 |
| `message` | 字串 | 確認 OpenSearch 已排清快取的訊息。 |
