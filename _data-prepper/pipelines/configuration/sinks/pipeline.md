---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管線"
parent: Sinks
grand_parent: Pipelines
nav_order: 55
---

# 管線接收器

使用 `pipeline` 接收器寫入另一個管線。

## 組態選項

`pipeline` 接收器支援下列組態選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
name | 是 | 字串 | 要寫入的管線名稱。

## 使用方式

下列範例設定一個 `pipeline` 接收器，寫入名為 `movies` 的管線：

```yaml
sample-pipeline:
  sink:
    - pipeline:
        name: movies
```
