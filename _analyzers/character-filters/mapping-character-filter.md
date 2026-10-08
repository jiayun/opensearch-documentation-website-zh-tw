---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "對應"
parent: Character filters
nav_order: 120
---

# 對應字元篩選器

`mapping` 字元篩選器接受一個用於字元取代的鍵值對對應表。每當篩選器遇到與某個鍵相符的字元字串時，就會將其取代為對應的值。取代值可以是空字串。

此篩選器採用貪婪比對，也就是會比對最長的相符模式。

在斷詞之前需要進行特定文字取代的情境中，`mapping` 字元篩選器相當實用。

## 範例

下列請求會設定一個 `mapping` 字元篩選器，將羅馬數字（例如 I、II 或 III）轉換為對應的阿拉伯數字（1、2 和 3）：

```json
GET /_analyze
{
  "tokenizer": "keyword",
  "char_filter": [
    {
      "type": "mapping",
      "mappings": [
        "I => 1",
        "II => 2",
        "III => 3",
        "IV => 4",
        "V => 5"
      ]
    }
  ],
  "text": "I have III apples and IV oranges"
}
```
{% include copy-curl.html %}

回應包含一個詞元，其中的羅馬數字已取代為阿拉伯數字：

```json
{
  "tokens": [
    {
      "token": "1 have 3 apples and 4 oranges",
      "start_offset": 0,
      "end_offset": 32,
      "type": "word",
      "position": 0
    }
  ]
}
```

## 參數

您可以使用下列任一參數來設定鍵值對應表。

| 參數       | 必要/選用 | 資料類型 | 說明    |
|:---|:---|:---|:---|
| `mappings`       | 選用          | 陣列      | 格式為 `key => value` 的鍵值對陣列。輸入文字中找到的每個鍵都會取代為其對應的值。 |
| `mappings_path`  | 選用          | 字串     | 包含鍵值對應之 UTF-8 編碼檔案的路徑。每個對應應以 `key => value` 格式各自位於新的一行。路徑可以是絕對路徑，或相對於 OpenSearch 組態目錄的相對路徑。 |

### 使用自訂對應字元篩選器

您可以定義自己的一組對應，以建立自訂對應字元篩選器。下列請求會建立一個自訂字元篩選器，用來取代文字中常見的縮寫：

```json
PUT /test-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_abbr_analyzer": {
          "tokenizer": "standard",
          "char_filter": [
            "custom_abbr_filter"
          ]
        }
      },
      "char_filter": {
        "custom_abbr_filter": {
          "type": "mapping",
          "mappings": [
            "BTW => By the way",
            "IDK => I don't know",
            "FYI => For your information"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求來檢查使用此分析器產生的詞元：

```json
GET /text-index/_analyze
{
  "tokenizer": "keyword",
  "char_filter": [ "custom_abbr_filter" ],
  "text": "FYI, updates to the workout schedule are posted. IDK when it takes effect, but we have some details. BTW, the finalized schedule will be released Monday."
}
```
{% include copy-curl.html %}

回應顯示縮寫已被取代：

```json
{
  "tokens": [
    {
      "token": "For your information, updates to the workout schedule are posted. I don't know when it takes effect, but we have some details. By the way, the finalized schedule will be released Monday.",
      "start_offset": 0,
      "end_offset": 153,
      "type": "word",
      "position": 0
    }
  ]
}
```
