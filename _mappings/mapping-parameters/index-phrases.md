---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引片語"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/index-phrases/
nav_order: 160
has_children: false
has_toc: false
---

# 索引片語對應參數

`index_phrases` 對應參數決定是否對欄位的文字進行額外處理，以產生片語詞元。啟用時，系統會建立額外的詞元，代表正好兩個連續單字的序列（_雙詞組_）。這可以顯著提升片語查詢的效能與準確性。不過，這也會增加索引大小，以及為文件編製索引所需的時間。

預設情況下，`index_phrases` 設定為 `false`，以維持較精簡的索引與較快的文件匯入速度。

## 在欄位上啟用索引片語

下列範例建立一個名為 `blog` 的索引，其中 `content` 欄位設定為 `index_phrases`：

```json
PUT /blog
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "index_phrases": true
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求為文件編製索引：

```json
PUT /blog/_doc/1
{
  "content": "The slow green turtle swims past the whale"
}
```
{% include copy-curl.html %}

使用下列搜尋請求執行 `match_phrase` 查詢：

```json
POST /blog/_search
{
  "query": {
    "match_phrase": {
      "content": "slow green"
    }
  }
}
```
{% include copy-curl.html %}

查詢會回傳已儲存的文件：

```json
{
  "took": 25,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.5753642,
    "hits": [
      {
        "_index": "blog",
        "_id": "1",
        "_score": 0.5753642,
        "_source": {
          "content": "The slow green turtle swims past the whale"
        }
      }
    ]
  }
}
```

雖然在未提供 `index_phrases` 對應參數時也會回傳相同的命中結果，但使用此參數可確保查詢的執行方式如下：

- 在內部使用 `.index_phrases` 欄位
- 比對預先斷詞的雙詞組，例如 "slow green"、"green turtle" 或 "turtle swims"。
- 略過位置查詢，因此速度更快，尤其是在大規模情境下。