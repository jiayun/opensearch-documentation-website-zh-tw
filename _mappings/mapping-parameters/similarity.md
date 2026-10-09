---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "相似度"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/similarity/
nav_order: 250
has_children: false
has_toc: false
---

# 相似度對應參數

`similarity` 對應參數可讓您自訂搜尋期間文字欄位的相關性分數計算方式。它會定義用來為相符文件排序的評分演算法，這會直接影響搜尋回應中結果的排序方式。

## 支援的相似度類型

OpenSearch 支援兩種欄位對應的相似度：

**內建相似度**（可直接使用）：
- [`BM25`]({{site.url}}{{site.baseurl}}/im-plugin/similarity/#bm25-similarity-default)（預設）：使用現代機率排序模型，可平衡詞彙頻率、文件長度及反向文件頻率。
- [`boolean`]({{site.url}}{{site.baseurl}}/im-plugin/similarity/#boolean-similarity)：傳回固定分數（`1` 或 `0`），因此若您只在意是否相符，而不在意相關性，則應使用此項。

**自訂相似度**（必須先在索引設定中定義）：
- [DFR、DFI、IB、LM Dirichlet、LM Jelinek Mercer 及指令碼相似度]({{site.url}}{{site.baseurl}}/im-plugin/similarity/#available-similarity-types)：進階相似度演算法，必須先在索引設定中進行組態，才能在欄位對應中以名稱參照。

## 在欄位上設定自訂相似度

下列請求會建立名為 `products` 的索引，其中包含使用 `boolean` 相似度的 `title` 欄位，該相似度會為所有相符項目指派相同的分數：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "similarity": "boolean"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 將文件編製索引

使用下列命令將範例文件編製索引：

```json
PUT /products/_doc/1
{
  "title": "Compact Wireless Mouse"
}
```
{% include copy-curl.html %}

## 查詢並檢查評分影響

使用下列命令依 `title` 欄位搜尋：

```json
POST /products/_search
{
  "query": {
    "match": {
      "title": "wireless mouse"
    }
  }
}
```
{% include copy-curl.html %}

您可以檢查回應的 `_score` 欄位中所傳回的分數：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 2,
    "hits": [
      {
        "_index": "products",
        "_id": "1",
        "_score": 2,
        "_source": {
          "title": "Compact Wireless Mouse"
        }
      }
    ]
  }
}
```

## 相關文件

- [相似度]({{site.url}}{{site.baseurl}}/im-plugin/similarity/)