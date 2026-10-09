---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "其他記錄檔類型對應"
parent: Supported log types
nav_order: 110
---

# 其他記錄檔類型對應

Security Analytics 支援非特定於單一服務或系統的欄位對應。這些對應類型分為以下幾類：

- Application：記錄應用程式記錄檔。
- Advanced Persistent Threat (APT)：記錄通常與 APT 攻擊相關的記錄檔。
- Compliance：記錄與合規性相關的記錄檔。
- macOS：記錄使用 Mac 裝置存取網路時的事件記錄檔。
- Proxy：記錄與代理伺服器事件相關的記錄檔。
- Web：記錄與透過 Web 存取網路相關的記錄檔。

每種記錄檔類型都包含相同的欄位對應，如下列程式碼片段所示：

```json
  "mappings": [
    {
      "raw_field":"record_type",
      "ecs":"dns.answers.type"
    },
    {
      "raw_field":"query",
      "ecs":"dns.question.name"
    },
    {
      "raw_field":"parent_domain",
      "ecs":"dns.question.registered_domain"
    },
    {
      "raw_field":"creationTime",
      "ecs":"timestamp"
    }
  ]
```