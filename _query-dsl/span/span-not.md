---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Span not
parent: Span queries
grand_parent: Query DSL
nav_order: 60
---

# Span not 查詢

`span_not` 查詢會排除與另一個 span 查詢重疊的 span。您也可以指定在排除的 span 之前或之後的距離，在該距離內不得發生相符項目。

例如，您可以使用 `span_not` 查詢來：
- 尋找詞彙，但排除它們出現在特定片語中的情況。
- 比對 span，除非它們鄰近特定詞彙。
- 排除在其他模式特定距離內發生的相符項目。

## 範例

若要試用本節的範例，請完成[設定步驟]({{site.url}}{{site.baseurl}}/query-dsl/span/#setup)。
{: .tip}

下列查詢會搜尋「dress」這個字，但排除它出現在「dress shirt」片語中的情況：

```json
GET /clothing/_search
{
  "query": {
    "span_not": {
      "include": {
        "span_term": {
          "description": "dress"
        }
      },
      "exclude": {
        "span_near": {
          "clauses": [
            {
              "span_term": {
                "description": "dress"
              }
            },
            {
              "span_term": {
                "description": "shirt"
              }
            }
          ],
          "slop": 0,
          "in_order": true
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

此查詢會比對文件 2，因為它包含「dress」這個字（「Beautiful long dress...」）。文件 1 不相符，因為它包含被排除的「dress shirt」片語。文件 3 和 4 不相符，因為它們包含「dress」這個字的變化形式（「dressed」和「dresses」），而此查詢搜尋的是原始欄位。

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json

```
</details>

## 參數

下表列出 `span_not` 查詢支援的所有最上層參數。

| 參數 | 資料類型 | 說明 | 
|:----------|:-----|:------------|
| `include` | 物件 | 您想尋找其相符項目的 span 查詢。必要。 |
| `exclude` | 物件 | 應排除其相符項目的 span 查詢。必要。 |
| `pre` | 整數 | 指定 `exclude` span 不得出現在 `include` span 之前指定詞元位置數內。選用。預設為 `0`。 |
| `post` | 整數 | 指定 `exclude` span 不得出現在 `include` span 之後指定詞元位置數內。選用。預設為 `0`。 |
| `dist` | 整數 | 等同於將 `pre` 和 `post` 都設為相同的值。選用。 |
