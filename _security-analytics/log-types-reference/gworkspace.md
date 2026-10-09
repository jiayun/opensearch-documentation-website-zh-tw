---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Google Workspace
parent: Supported log types
nav_order: 45
---

# Google Workspace 記錄類型

`gworkspace` 記錄類型會監控 Google Workspace 記錄項目，例如以下項目：

- 管理員動作
- 群組與群組成員資格動作
- 與登入相關的事件

下列程式碼片段包含此記錄類型的所有 `raw_field` 與 `ecs` 對應：

```json
  "mappings": [
    {
      "raw_field":"eventSource",
      "ecs":"google_workspace.admin.service.name"
    },
    {
      "raw_field":"eventName",
      "ecs":"google_workspace.event.name"
    },
    {
      "raw_field":"new_value",
      "ecs":"google_workspace.admin.new_value"
    }
  ]
```