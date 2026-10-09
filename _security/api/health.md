---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安全性外掛程式健康狀態"
parent: Security APIs
nav_order: 170
---

# 安全性外掛程式健康狀態 API
**於 1.0 版推出**
{: .label .label-purple }

檢查 Security 外掛程式是否已啟動並正在執行。此操作不需要已簽署的請求，因此您可以將其用於位於叢集前方的負載平衡器健康檢查。

<!-- spec_insert_start
api: security.health
component: endpoints
-->
## 端點
```json
GET  /_plugins/_security/health
POST /_plugins/_security/health
```
<!-- spec_insert_end -->

## 範例請求

```json
GET _plugins/_security/health
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "message": null,
  "mode": "strict",
  "status": "UP",
  "settings": {
    "plugins.security.cache.ttl_minutes": 60
  }
}
```

## 回應本文欄位

回應本文是包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `status` | 字串 | Security 外掛程式的狀態。`UP` 表示此外掛程式已初始化，並準備好授權請求。 |
| `mode` | 字串 | 此外掛程式的運作模式。強制執行驗證與授權的叢集會傳回 `strict`。 |
| `message` | 字串 | 狀態的其他資訊，或在外掛程式正常執行時為 `null`。 |
| `settings` | 物件 | 隨健康檢查回報的 Security 外掛程式設定。 |
