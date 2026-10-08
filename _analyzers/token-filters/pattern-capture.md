---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "模式擷取"
parent: Token filters
nav_order: 310
---

# 模式擷取詞元篩選器

`pattern_capture` 詞元篩選器是一種功能強大的篩選器，使用正規表示式根據特定模式擷取並取出文字的部分內容。當您想要取出詞元的特定部分，例如電子郵件網域、主題標籤或數字，並將其重複用於進一步分析或編製索引時，此篩選器非常實用。

## 參數

您可以使用下列參數設定 `pattern_capture` 詞元篩選器。

參數 | 必要／選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`patterns` | 必要 | 字串陣列 | 用於擷取文字部分內容的正規表示式陣列。
`preserve_original` | 必要 | 布林值| 是否在輸出中保留原始詞元。預設為 `true`。


## 範例

下列範例請求會建立名為 `email_index` 的新索引，並設定含有 `pattern_capture` 篩選器的分析器，以從電子郵件地址中取出 @ 符號前的部分和網域名稱：

```json
PUT /email_index
{
  "settings": {
    "analysis": {
      "filter": {
        "email_pattern_capture": {
          "type": "pattern_capture",
          "preserve_original": true,
          "patterns": [
            "^([^@]+)",
            "@(.+)$"
          ]
        }
      },
      "analyzer": {
        "email_analyzer": {
          "tokenizer": "uax_url_email",
          "filter": [
            "email_pattern_capture",
            "lowercase"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查分析器產生的詞元：

```json
POST /email_index/_analyze
{
  "text": "john.doe@example.com",
  "analyzer": "email_analyzer"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "john.doe@example.com",
      "start_offset": 0,
      "end_offset": 20,
      "type": "<EMAIL>",
      "position": 0
    },
    {
      "token": "john.doe",
      "start_offset": 0,
      "end_offset": 20,
      "type": "<EMAIL>",
      "position": 0
    },
    {
      "token": "example.com",
      "start_offset": 0,
      "end_offset": 20,
      "type": "<EMAIL>",
      "position": 0
    }
  ]
}
```
