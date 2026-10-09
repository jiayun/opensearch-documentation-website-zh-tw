---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "檔案"
parent: Sinks
grand_parent: Pipelines
nav_order: 45
---

# 檔案輸出端

使用 `file` 輸出端建立平面檔案輸出，通常是 `.log` 檔案。

## 組態選項

下表說明您可以為 `file` 輸出端設定的選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`path` | 是 | 字串 | 輸出檔案的路徑（例如 `logs/my-transformed-log.log`）。
`append` | 否 | 布林值 | 當 `true` 時，輸出端檔案會以附加模式開啟。

## 用法

以下範例展示 `file` 輸出端的基本用法：

```yaml
sample-pipeline:
  sink:
    - file:
        path: path/to/output-file
```

