---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: WAF
parent: Supported log types
nav_order: 95
---

# WAF 記錄檔類型

`waf` 記錄檔類型會監視網頁應用程式防火牆 (WAF) 記錄檔。WAF 的作用是監視並篩選網頁應用程式與網際網路之間流動的 HTTP 流量。WAF 可防禦常見的安全性攻擊，例如跨網站指令碼 (XSS) 和 SQL 資料隱碼 (SQLi)。

下列程式碼片段包含此記錄檔類型的所有 `raw_field` 和 `ecs` 對應：

```json
  "mappings": [
    {
      "raw_field":"cs-method",
      "ecs":"waf.request.method"
    },
    {
      "raw_field":"httpRequest.httpMethod",
      "ecs":"waf.request.method"
    },
    {
      "raw_field":"cs-uri-query",
      "ecs":"waf.request.uri_query"
    },
    {
      "raw_field":"httpRequest.uri",
      "ecs":"waf.request.uri_query"
    },
    {
      "raw_field":"httpRequest.args",
      "ecs":"waf.request.uri_query"
    },
    {
      "raw_field":"cs-user-agent",
      "ecs":"waf.request.headers.user_agent"
    },
    {
      "raw_field":"httpRequest.headers",
      "ecs":"waf.request.headers"
    },
    {
      "raw_field":"sc-status",
      "ecs":"waf.response.code"
    },
    {
      "raw_field":"responseCodeSent",
      "ecs":"waf.response.code"
    },
    {
      "raw_field":"timestamp",
      "ecs":"timestamp"
    },
    {
      "raw_field":"httpRequest.headers.value",
      "ecs":"waf.request.headers.value"
    },
    {
      "raw_field":"httpRequest.headers.name",
      "ecs":"waf.request.headers.name"
    }
  ]
```