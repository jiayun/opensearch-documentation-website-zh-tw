---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: NetFlow
parent: Supported log types
nav_order: 60
---

# NetFlow 記錄類型

`netflow` 記錄類型會記錄整合測試期間所使用的 NetFlow 事件。

下列程式碼片段包含此記錄類型的所有 `raw_field` 與 `ecs` 對應：

```json
"mappings": [
    {
      "raw_field":"netflow.source_ipv4_address",
      "ecs":"source.ip"
    },
    {
      "raw_field":"netflow.source_transport_port",
      "ecs":"source.port"
    },
    {
      "raw_field":"netflow.destination_ipv4_address",
      "ecs":"destination.ip"
    },
    {
      "raw_field":"netflow.destination_transport_port",
      "ecs":"destination.port"
    },
    {
      "raw_field":"http.request.method",
      "ecs":"http.request.method"
    },
    {
      "raw_field":"http.response.status_code",
      "ecs":"http.response.status_code"
    },
    {
      "raw_field":"timestamp",
      "ecs":"timestamp"
    }
  ]
```