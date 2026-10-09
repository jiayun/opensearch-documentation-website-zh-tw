---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "跨度詞元"
parent: Span queries
grand_parent: Query DSL
nav_order: 80
---

# 跨度詞元查詢

`span_term` 查詢是最基本的跨度查詢，用於比對包含單一詞元的跨度。它是建構更複雜跨度查詢的基礎元件。

例如，您可以使用 `span_term` 查詢來：
- 尋找可在其他跨度查詢中使用的精確詞元比對。
- 比對特定單字，同時保留位置資訊。
- 建立可與其他跨度查詢合併的基本跨度。

## 範例

若要嘗試本節中的範例，請完成[設定步驟]({{site.url}}{{site.baseurl}}/query-dsl/span/#setup)。
{: .tip}

下列查詢會搜尋精確詞元 "formal"：

```json
GET /clothing/_search
{
  "query": {
    "span_term": {
      "description": "formal"
    }
  }
}
```
{% include copy-curl.html %}

或者，您可以在 `value` 參數中指定搜尋詞元：

```json
GET /clothing/_search
{
  "query": {
    "span_term": {
      "description": {
        "value": "formal"
      }
    }
  }
}
```
{% include copy-curl.html %}

您也可以指定 `boost` 值，以提高文件分數：

```json
GET /clothing/_search
{
  "query": {
    "span_term": {
      "description": {
        "value": "formal",
        "boost": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

此查詢比對文件 1 和 2，因為它們包含精確詞元 "formal"。位置資訊會保留，供其他 span 查詢使用。

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.498922,
    "hits": [
      {
        "_index": "clothing",
        "_id": "2",
        "_score": 1.498922,
        "_source": {
          "description": "Beautiful long dress in red silk, perfect for formal events."
        }
      },
      {
        "_index": "clothing",
        "_id": "1",
        "_score": 1.4466847,
        "_source": {
          "description": "Long-sleeved dress shirt with a formal collar and button cuffs. "
        }
      }
    ]
  }
}
```
</details>

## 參數

下表列出 `span_term` 查詢支援的所有頂層參數。

| 參數  | 資料類型 | 說明 |
|:----------------|:------------|:--------|
| `<field>` | 字串或物件 | 要搜尋的欄位名稱。 |
