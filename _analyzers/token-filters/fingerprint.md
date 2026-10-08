---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Fingerprint
parent: Token filters
nav_order: 140
---

# Fingerprint 詞元篩選器

`fingerprint` 詞元篩選器用於將文字標準化並去除重複內容。當文字處理的一致性至關重要時，這項功能特別實用。`fingerprint` 詞元篩選器透過下列步驟處理文字來達成此目的：

1. **轉換為小寫**：將所有文字轉換為小寫。
2. **分割**：將文字拆分為詞元。
3. **排序**：依字母順序排列詞元。
4. **移除重複項目**：刪除重複的詞元。
5. **合併詞元**：將詞元組合成單一字串，通常以空格或其他指定的分隔符號連接。

## 參數

`fingerprint` 詞元篩選器可使用下列兩個參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`max_output_size` | 選用 | 整數 | 限制產生的指紋字串長度。如果串接後的字串超過 `max_output_size`，篩選器將不會產生任何輸出，因而產生空的詞元。預設為 `255`。
`separator` | 選用 | 字串 | 定義在詞元排序並去除重複後，用來將詞元合併為單一字串的字元。預設為空格（`" "`）。

## 範例

下列範例請求會建立名為 `my_index` 的新索引，並設定含有 `fingerprint` 詞元篩選器的分析器：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_fingerprint": {
          "type": "fingerprint",
          "max_output_size": 200,
          "separator": "-"
        }
      },
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_fingerprint"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用此分析器產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_analyzer",
  "text": "OpenSearch is a powerful search engine that scales easily"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "a-easily-engine-is-opensearch-powerful-scales-search-that",
      "start_offset": 0,
      "end_offset": 57,
      "type": "fingerprint",
      "position": 0
    }
  ]
}
```
