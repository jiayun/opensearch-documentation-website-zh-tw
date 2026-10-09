---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引選項"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/index-options/
nav_order: 140
has_children: false
has_toc: false
---

# 索引選項對應參數

`index_options` 對應參數可控制文字欄位在反向索引中儲存的詳細程度。此設定會直接影響索引大小，以及評分、片語比對和突顯功能的可用能力。

`index_options` 參數具有以下有效值。

| 值     | 儲存內容                          | 說明 |
|------------|----------------------------------|-------------|
| `docs`     | 僅文件 ID               | 只在一組文件中為詞元的存在編製索引。不儲存詞頻或位置。可將索引大小減至最小；適合簡單的存在性檢查。 |
| `freqs`    | 文件 ID + 詞頻   | 新增詞頻資訊。有助於改善相關性評分，但不支援片語或鄰近查詢。 |
| `positions`| 文件 ID + 詞頻 + 詞元位置 | 包含詞元在文件中的順序與位置。片語查詢與鄰近搜尋必須使用此選項。 |
| `offsets`  | 文件 ID + 詞頻 + 詞元位置 + 位移 | 最詳細。為相符的詞元新增字元位移。適合用於突顯，但會增加儲存空間。 |

預設情況下，文字欄位會以 `positions` 選項編製索引，以兼顧功能性與索引大小。

## 範例：在欄位上設定 index_options

建立一個名為 `products` 的索引，其中包含一個 `description` 欄位，並為 `index_options` 使用 `positions` 設定：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "description": {
        "type": "text",
        "index_options": "positions"
      }
    }
  }
}
```
{% include copy-curl.html %}

為一個在 `description` 欄位中含內容的文件編製索引：

```json
PUT /products/_doc/1
{
  "description": "This is a sample product description with several terms."
}
```
{% include copy-curl.html %}

對 `description` 欄位執行片語查詢：

```json
POST /products/_search
{
  "query": {
    "match_phrase": {
      "description": "product description"
    }
  }
}
```
{% include copy-curl.html %}

片語查詢成功比對到該文件，示範了 `index_options` 中的 `positions` 設定如何在 `description` 欄位內實現精確的片語比對：

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
        "_index": "products",
        "_id": "1",
        "_score": 0.5753642,
        "_source": {
          "description": "This is a sample product description with several terms."
        }
      }
    ]
  }
}
```
