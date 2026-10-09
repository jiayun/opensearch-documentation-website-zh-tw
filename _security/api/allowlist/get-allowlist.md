---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得允許清單"
parent: Allow list APIs
grand_parent: Security APIs
nav_order: 30
---

# Get Allow List API
**於 2.1 版推出**
{: .label .label-purple }

擷取目前的允許清單組態。

此 API 僅供超級管理員使用。請使用管理員憑證進行驗證，而非使用使用者名稱和密碼。如需詳細資訊，請參閱 [API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
{: .note}

<!-- spec_insert_start
api: security.get_allowlist
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/allowlist
```
<!-- spec_insert_end -->

## 請求範例

```json
GET _plugins/_security/api/allowlist
```
{% include copy-curl.html security=true %}

## 回應範例

```json
{
  "config": {
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
}
```
