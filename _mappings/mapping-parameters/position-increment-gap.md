---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "位置增量間距"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/position-increment-gap/
nav_order: 220
has_children: false
has_toc: false
---

# position_increment_gap 對應參數

`position_increment_gap` 對應參數定義多值欄位的詞元在編製索引時的位置距離。這會影響 [`match_phrase`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/) 與 [`span`]({{site.url}}{{site.baseurl}}/query-dsl/span/index/) 查詢在同一欄位的多個值之間搜尋時的行為。

預設情況下，多值欄位中的每個新值都會被視為與前一個值相隔 `100` 個位置的間距。這有助於避免搜尋可能跨越不同欄位值的片語時產生誤判。

## 設定 position_increment_gap

使用下列請求建立名為 `articles` 的索引，其中包含一個類型為 `text` 的 `tags` 欄位，並將 `position_increment_gap` 設定為 `0`：

```json
PUT /articles
{
  "mappings": {
    "properties": {
      "tags": {
        "type": "text",
        "position_increment_gap": 0
      }
    }
  }
}
```
{% include copy-curl.html %}

## 為多值欄位編製索引

使用下列請求為一份 `tags` 欄位包含多個值的文件編製索引：

```json
PUT /articles/_doc/1
{
  "tags": ["machine", "learning"]
}
```
{% include copy-curl.html %}

## 使用 `match_phrase` 查詢進行搜尋

使用下列 `match_phrase` 查詢在 `tags` 欄位中搜尋 "machine learning"：

```json
GET /articles/_search
{
  "query": {
    "match_phrase": {
      "tags": "machine learning"
    }
  }
}
```
{% include copy-curl.html %}

結果顯示片語比對成功，因為 `position_increment_gap` 設定為 `0`，讓來自不同值的詞元被視為相鄰：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.5753642,
    "hits": [
      {
        "_index": "articles",
        "_id": "1",
        "_score": 0.5753642,
        "_source": {
          "tags": [
            "machine",
            "learning"
          ]
        }
      }
    ]
  }
}
```

如果 `position_increment_gap` 維持在 `100`，則不會傳回任何命中結果，因為詞元 `machine` 與 `learning` 會被視為彼此相距 100 個位置。
