---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "修補稽核組態"
parent: Audit log APIs
grand_parent: Security APIs
nav_order: 20
---

# 修補稽核組態 API
**1.0 版推出**
{: .label .label-purple }

更新稽核組態中指定的欄位。此方法需要操作、路徑及值，才能完成有效的請求。如需使用 `PATCH` 方法的詳細資訊，請參閱 Wikipedia 上的[修補資源](https://en.wikipedia.org/wiki/PATCH_%28HTTP%29#Patching_resources)說明。

使用 `PATCH` 方法也需要使用者具備包含用於加密的管理員憑證的安全性組態。如需深入了解這些憑證，請參閱[設定管理員憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/#configuring-admin-certificates)。

<!-- spec_insert_start
api: security.patch_audit_configuration
component: endpoints
-->
## 端點
```json
PATCH /_plugins/_security/api/audit
```
<!-- spec_insert_end -->

## 請求範例

```json
PATCH _plugins/_security/api/audit
[
  {
    "op": "replace",
    "path": "/config/audit/enable_rest",
    "value": true
  }
]
```
{% include copy-curl.html security=true %}

## 回應範例

```json
{
  "status": "OK",
  "message": "No updates required"
}
```

```bash
HTTP/1.1 200 OK
content-type: application/json; charset=UTF-8
content-length: 45
```

## 回應本文欄位

回應本文是 JSON 物件，包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `status` | 字串 | 請求的狀態。成功的請求會傳回 `OK`。 |
| `message` | 字串 | 說明操作結果的訊息。 |
