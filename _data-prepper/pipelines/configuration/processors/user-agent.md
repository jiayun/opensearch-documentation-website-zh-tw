---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用者代理程式"
parent: Processors
grand_parent: Pipelines
nav_order: 430
---

# 使用者代理程式處理器

`user_agent` 處理器會剖析事件中的任何使用者代理程式（UA）字串，然後將剖析結果新增至事件的寫入資料。

## 使用方式

在此範例中，`user_agent` 處理器會呼叫包含 UA 字串的來源，也就是 `ua` 欄位，並指定剖析後的字串將寫入的鍵 `user_agent`，如下列範例所示：

```yaml
  processor:
    - user_agent:
        source: "ua"
        target: "user_agent"
```

下列範例事件包含 `ua` 欄位，其中的字串提供使用者的相關資訊： 

```json
{
  "ua":  "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"
}
```

`user_agent` 處理器會將字串剖析為與 Elastic Common Schema（ECS）相容的格式，然後將結果新增至指定的目標，如下列範例所示：

```json
{
  "user_agent": {
    "original": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
    "os": {
        "version": "13.5.1",
        "full": "iOS 13.5.1",
        "name": "iOS"
    },
    "name": "Mobile Safari",
    "version": "13.1.1",
    "device": {
        "name": "iPhone"
    }
  },
  "ua":  "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"
}
```

## 組態選項

您可以搭配 `user_agent` 處理器使用下列組態選項。

| 選項 | 必要 | 說明 |
| :--- | :--- | :--- |
| `source` | 是 | 事件中要剖析的欄位。 
| `target` | 否 | 剖析後的事件將寫入的欄位。預設為 `user_agent`。 
| `exclude_original` | 否 | 決定是否從剖析結果中排除原始 UA 字串。預設為 `false`。 
| `cache_size` | 否 | 剖析器的快取大小，以 MB 為單位。預設為 `1000`。 |
| `tags_on_parse_failure` | 否 | 當 `user_agent` 處理器無法剖析 UA 字串時，要新增至事件的標籤。 |
