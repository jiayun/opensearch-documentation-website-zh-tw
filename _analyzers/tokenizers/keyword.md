---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Keyword 
parent: Tokenizers
nav_order: 50
---

# Keyword 斷詞器

`keyword` 斷詞器會匯入文字，並將其原封不動地輸出為單一詞元。當您希望輸入內容保持不變時，這項特性特別實用，例如管理姓名、產品代號或電子郵件地址等結構化資料時。

`keyword` 斷詞器可以搭配詞元篩選器來處理文字，例如將其正規化或移除多餘的字元。

## 範例用法

下列範例請求會建立名為 `my_index` 的新索引，並設定使用 `keyword` 斷詞器的分析器：
 
```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_keyword_analyzer": {
          "type": "custom",
          "tokenizer": "keyword"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "my_keyword_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查該分析器產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_keyword_analyzer",
  "text": "OpenSearch Example"
}
```
{% include copy-curl.html %}

回應中包含代表原始文字的單一詞元：

```json
{
  "tokens": [
    {
      "token": "OpenSearch Example",
      "start_offset": 0,
      "end_offset": 18,
      "type": "word",
      "position": 0
    }
  ]
}
```

## 參數

`keyword` 詞元篩選器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`buffer_size`| 選用 | 整數 | 決定字元緩衝區大小。預設為 `256`。通常不需要變更此設定。

## 將 keyword 斷詞器與詞元篩選器結合使用

若要增強 `keyword` 斷詞器的功能，您可以將其與詞元篩選器結合使用。詞元篩選器可以轉換文字，例如將其轉為小寫或移除不需要的字元。

### 範例：使用 pattern_replace 篩選器與 keyword 斷詞器

在此範例中，`pattern_replace` 篩選器使用規則表達式，將所有非英數字元取代為空字串：

```json
POST _analyze
{
  "tokenizer": "keyword",
  "filter": [
    {
      "type": "pattern_replace",
      "pattern": "[^a-zA-Z0-9]",
      "replacement": ""
    }
  ],
  "text": "Product#1234-XYZ"
}
```
{% include copy-curl.html %}

`pattern_replace` 篩選器會移除非英數字元，並傳回下列詞元：

```json
{
  "tokens": [
    {
      "token": "Product1234XYZ",
      "start_offset": 0,
      "end_offset": 16,
      "type": "word",
      "position": 0
    }
  ]
}
```

