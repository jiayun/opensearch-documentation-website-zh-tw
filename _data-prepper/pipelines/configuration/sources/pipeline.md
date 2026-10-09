---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管線"
parent: Sources
grand_parent: Pipelines
nav_order: 90
---

# 管線來源

使用 `pipeline` 接收端從另一個管線讀取資料。

## 組態

`pipeline` 來源支援下列組態選項。

| 選項 | 必要 | 資料類型 | 說明 |
|:-------|:---------|:-------|:---------------------------------------|
| `name` | 是 | 字串 | 要讀取的管線名稱。 |

## 用法

下列範例設定名為 `sample-pipeline` 的 `pipeline` 接收端，它會從名為 `movies` 的管線讀取資料：

```yaml
sample-pipeline:
  source:
    - pipeline:
        name: "movies"
```
{% include copy.html %}
