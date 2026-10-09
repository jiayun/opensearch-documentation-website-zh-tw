---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Linux
parent: Supported log types
nav_order: 50 
---

# Linux 記錄檔類型

`linux` 記錄檔類型會記錄 Linux syslog 事件。

下列程式碼片段包含此記錄檔類型的所有 `raw_field` 和 `ecs` 對應：

```json
  "mappings": [
    {
      "raw_field":"name",
      "ecs":"user.filesystem.name"
    },
    {
      "raw_field":"a0",
      "ecs":"auditd.log.a0"
    },
    {
      "raw_field":"comm",
      "ecs":"auditd.log.comm"
    },
    {
      "raw_field":"exe",
      "ecs":"auditd.log.exe"
    },
    {
      "raw_field":"uid",
      "ecs":"auditd.log.uid"
    },
    {
      "raw_field":"USER",
      "ecs":"system.auth.user"
    },
    {
      "raw_field":"User",
      "ecs":"system.auth.user"
    },
    {
      "raw_field":"Image",
      "ecs":"process.exe"
    },
    {
      "raw_field":"DestinationHostname",
      "ecs":"rsa.web.remote_domain"
    },
    {
      "raw_field":"CommandLine",
      "ecs":"process.command_line"
    },
    {
      "raw_field":"ParentImage",
      "ecs":"process.parent.executable"
    },
    {
      "raw_field":"CurrentDirectory",
      "ecs":"process.working_directory"
    },
    {
      "raw_field":"LogonId",
      "ecs":"process.real_user.id"
    },
    {
      "raw_field":"creationTime",
      "ecs":"timestamp"
    }
  ]
```