---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Span 查詢"
has_children: true
has_toc: false
nav_order: 75
redirect_from: 
  - /opensearch/query-dsl/span-query/
  - /query-dsl/query-dsl/span-query/
  - /query-dsl/span-query/
  - /query-dsl/span/
---

# Span 查詢

您可以使用 span 查詢來執行精確的位置搜尋。Span 查詢是低階、特定的查詢，可控制指定查詢詞彙的順序與鄰近程度。它們主要用於搜尋法律文件和專利。

Span 查詢包含下列查詢類型：

| 查詢類型 | 說明 |
| :--- | :--- |
| [Span containing]({{site.url}}{{site.baseurl}}/query-dsl/span/span-containing/) | 傳回包含較小 span 的較大 span。與 `span_within` 查詢相反。 |
| [Span field masking]({{site.url}}{{site.baseurl}}/query-dsl/span/span-field-masking/) | 讓 span 查詢可跨不同欄位運作，方式是讓某個欄位看起來像另一個欄位。當相同文字使用不同分析器編製索引時很有用。 |
| [Span first]({{site.url}}{{site.baseurl}}/query-dsl/span/span-first/) | 比對從欄位開頭起算的指定位置數內出現的詞彙或片語。 |
| [Span multi-term]({{site.url}}{{site.baseurl}}/query-dsl/span/span-multi-term/) | 讓多詞彙查詢 (例如 `prefix`、`wildcard` 或 `fuzzy`) 可在 span 查詢內運作。 |
| [Span near]({{site.url}}{{site.baseurl}}/query-dsl/span/span-near/) | 尋找彼此距離在指定範圍內出現的詞彙或片語。支援要求比對結果必須以特定順序出現。 |
| [Span not]({{site.url}}{{site.baseurl}}/query-dsl/span/span-not/) | 排除與另一個 span 查詢重疊的比對結果。 |
| [Span or]({{site.url}}{{site.baseurl}}/query-dsl/span/span-or/) | 比對符合任何所提供 span 查詢的文件。 |
| [Span term]({{site.url}}{{site.baseurl}}/query-dsl/span/span-term/) | 比對單一詞彙，同時保留位置資訊以供其他 span 查詢使用。 |
| [Span within]({{site.url}}{{site.baseurl}}/query-dsl/span/span-within/) | 傳回被較大 span 包圍的較小 span。與 `span_containing` 查詢相反。 |

## 設定

若要試用本節的範例，請使用下列步驟來設定範例索引。

### 步驟 1：建立索引

首先，為電子商務服飾網站建立索引。`description` 欄位使用預設的 `standard` 分析器，而 `description.stemmed` 子欄位則套用 `english` 分析器以啟用詞幹擷取：

```json
PUT /clothing
{
  "mappings": {
    "properties": {
      "description": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "stemmed": {
            "type": "text",
            "analyzer": "english"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 2：將資料編製索引

將範例文件編製索引至該索引：

```json
POST /clothing/_doc/1
{
  "description": "Long-sleeved dress shirt with a formal collar and button cuffs. "
}

```
{% include copy-curl.html %}

```json
POST /clothing/_doc/2
{
  "description": "Beautiful long dress in red silk, perfect for formal events."
}
```
{% include copy-curl.html %}

```json
POST /clothing/_doc/3
{
  "description": "Short-sleeved shirt with a button-down collar, can be dressed up or down."
}
```
{% include copy-curl.html %}

```json
POST /clothing/_doc/4
{
  "description": "A set of two midi silk shirt dresses with long sleeves in black. "
}
```
{% include copy-curl.html %}
