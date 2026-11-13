---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "有界阻塞"
parent: Buffers
grand_parent: Pipelines
nav_order: 50
---

# 有界阻塞緩衝區

`bounded_blocking` 緩衝區是預設的緩衝區，且以記憶體為基礎。下表說明 `bounded_blocking` 緩衝區的參數。

| 選項 | 必要 | 類型 | 說明 |
| --- | --- | --- | --- |
| `buffer_size` | 否 | 整數 | 緩衝區可接受的記錄數量上限。預設值為 `12800`。 |
| `batch_size` | 否 | 整數 | 每次讀取後，緩衝區排出的記錄數量上限。預設值為 `200`。 |

<!--- ## Configuration

Content will be added to this section.

## Metrics

Content will be added to this section. --->