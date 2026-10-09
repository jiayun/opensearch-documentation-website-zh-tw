---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: GitHub
parent: Supported log types
nav_order: 40
---

# GitHub 記錄類型

`github` 記錄類型會監視由 [GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions) 建立的工作流程。

下列程式碼片段包含此記錄類型的所有 `raw_field` 和 `ecs` 對應：

```json
  "mappings": [
    {
      "raw_field":"action",
      "ecs":"github.action"
    }
  ]
```