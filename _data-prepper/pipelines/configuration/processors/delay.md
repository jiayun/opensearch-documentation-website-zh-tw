---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "延遲"
parent: Processors
grand_parent: Pipelines
nav_order: 100
---

# 延遲處理器

此處理器會在處理器鏈中加入延遲。一般而言，您應該只在測試、實驗和偵錯時使用此處理器。

## 組態

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`for` | 否 | 持續時間 | 延遲的持續時間。預設為 `1s`。

## 使用方式

下列範例示範如何使用 `delay` 處理器延遲 2 秒。

```yaml
processor:
  - delay:
      for: 2s
```
{% include copy.html %}
