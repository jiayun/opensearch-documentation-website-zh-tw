---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Parent ID
parent: Joining queries
nav_order: 40
---

# Parent ID 查詢

`parent_id` 查詢會傳回其上層文件具有指定 ID 的子文件。您可以使用 [join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 欄位類型，在同一個索引中的文件之間建立上層/子層關係。

## 範例

在執行 `parent_id` 查詢之前，您的索引必須包含 [join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 欄位，才能建立上層/子層關係。索引對應請求使用下列格式：

```json
PUT /example_index
{
  "mappings": {
    "properties": {
      "relationship_field": {
        "type": "join",
        "relations": {
          "parent_doc": "child_doc"
        }
      }
    }
  }
}
```
{% include copy-curl.html %} 

在本範例中，請先依照 [`has_child` 查詢範例]({{site.url}}{{site.baseurl}}/query-dsl/joining/has-child/) 所述，設定一個包含代表產品及其品牌的文件的索引。

若要搜尋特定上層文件的子文件，請使用 `parent_id` 查詢。下列查詢會傳回其上層文件 ID 為 `1` 的子文件（產品）：

```json
GET testindex1/_search
{
  "query": {
    "parent_id": {
      "type": "product",
      "id": "1"
    }
  }
}
```
{% include copy-curl.html %}

回應會傳回子產品：

```json
{
  "took": 57,
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
    "max_score": 0.87546873,
    "hits": [
      {
        "_index": "testindex1",
        "_id": "3",
        "_score": 0.87546873,
        "_routing": "1",
        "_source": {
          "name": "Mechanical watch",
          "sales_count": 150,
          "product_to_brand": {
            "name": "product",
            "parent": "1"
          }
        }
      }
    ]
  }
}
```

## 參數

下表列出 `parent_id` 查詢支援的所有頂層參數。

| 參數  | 必要/選用 | 說明  |
|:---|:---|:---|
| `type` | 必要 | 指定 `join` 欄位對應中所定義的子層關係名稱。 |
| `id` | 必要 | 上層文件的 ID。查詢會傳回與此上層文件相關聯的子文件。 |
| `ignore_unmapped` | 選用 | 指出是否忽略未對應的 `type` 欄位並改為不傳回文件，而不是擲回錯誤。當查詢多個索引（其中某些索引可能不包含 `type` 欄位）時，您可以提供此參數。預設為 `false`。 |