---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Classic
parent: Token filters
nav_order: 50
---

# Classic 詞元篩選器

Classic 詞元篩選器的主要功能是搭配 classic 斷詞器使用。它會對詞元套用下列常見的轉換，以協助文字分析與搜尋：
 - 移除所有格字尾，例如 *'s*。舉例來說，*John's* 會變成 *John*。
 - 移除縮寫字中的句點。舉例來說，*D.A.R.P.A.* 會變成 *DARPA*。


## 範例

下列範例請求會建立名為 `custom_classic_filter` 的新索引，並設定一個使用 `classic` 篩選器的分析器：

```json
PUT /custom_classic_filter
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_classic": {
          "type": "custom",
          "tokenizer": "classic",
          "filter": ["classic"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器所產生的詞元：

```json
POST /custom_classic_filter/_analyze
{
  "analyzer": "custom_classic",
  "text": "John's co-operate was excellent."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "John",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<APOSTROPHE>",
      "position": 0
    },
    {
      "token": "co",
      "start_offset": 7,
      "end_offset": 9,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "operate",
      "start_offset": 10,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "was",
      "start_offset": 18,
      "end_offset": 21,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "excellent",
      "start_offset": 22,
      "end_offset": 31,
      "type": "<ALPHANUM>",
      "position": 4
    }
  ]
}
```

