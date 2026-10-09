---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Okta
parent: Supported log types
nav_order: 80
---

# Okta 記錄檔類型

`okta` 記錄檔類型會記錄由各種動作產生的 Okta 事件，例如下載匯出檔案、要求應用程式存取權，或撤銷權限。

下列程式碼片段包含此記錄檔類型的所有 `raw_field` 和 `ecs` 對應：

```json
  "mappings": [
    {
      "raw_field":"eventtype",
      "ecs":"okta.event_type"
    },
    {
      "raw_field":"displaymessage",
      "ecs":"okta.display_message"
    }
  ]
```